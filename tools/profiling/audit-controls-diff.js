// Controls state-space audit (S158): drive every value of every visible control
// in every view and diff the readouts it could plausibly drive.
//
// The question is NOT "does the map change" — it is "which readouts does this
// control reach, and does any readout sit next to a control it ignores?"
// S157 found the Services cost panel byte-identical across all ten service
// layers; this generalizes that one measurement to the whole control surface.
//
// A readout that is INVARIANT across a control's values is a candidate, not a
// verdict — `#coloradj` is *supposed* to leave the title alone. The output is an
// inventory for the brief to judge.
//   node audit-controls-diff.js <url> [hood]
const { chromium } = require('playwright');
const [url, HOOD = 'DOWNTOWN'] = process.argv.slice(2);

const VIEWS = ['money', 'development', 'services', 'ratio', 'uses', 'lab'];

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  // Visible controls, grouped by section. `.svc` rows share a class selector,
  // so the per-service data attribute has to come from the ROW, not the input.
  const inventory = () => page.evaluate(() => {
    const vis = el => {
      for (let n = el; n && n !== document.body; n = n.parentElement) {
        const s = getComputedStyle(n);
        if (s.display === 'none' || s.visibility === 'hidden') return false;
      }
      return true;
    };
    const sel = el => {
      if (el.id) return '#' + el.id;
      const svc = el.closest('.svc');
      if (svc) return `#services .svc[data-service="${svc.dataset.service}"] ${el.tagName.toLowerCase()}.${[...el.classList].join('.')}`;
      const bits = [];
      for (const a of el.attributes) if (a.name.startsWith('data-') && a.name !== 'data-tok') bits.push(`[${a.name}="${a.value}"]`);
      const p = el.closest('[id]');
      return (p ? '#' + p.id + ' ' : '') + el.tagName.toLowerCase() + bits.join('');
    };
    const out = {};
    const seen = new Set();
    for (const r of ['#controls', '#a11y-menu']) {
      const root = document.querySelector(r);
      if (!root) continue;
      for (const el of root.querySelectorAll('button, input[type=checkbox], input[type=radio]')) {
        if (!vis(el)) continue;
        const s = sel(el);
        if (seen.has(s)) continue;
        seen.add(s);
        const group = el.closest('[id]') ? el.closest('[id]').id : '(none)';
        if (['views', 'opt-fold', 'a11y-btn'].includes(group)) continue;
        (out[group] ||= []).push({ sel: s, text: (el.textContent || el.getAttribute('aria-label') || el.closest('.svc')?.textContent || '').trim().slice(0, 40) });
      }
    }
    return out;
  });

  // Every readout a control could plausibly drive, as comparable strings.
  const readouts = () => page.evaluate((HOOD) => {
    // ⚠️ textContent, not innerText: `#peek` is CSS-gated on `(hover: none)` so
    // innerText returns '' for it on a desktop viewport — which silently made
    // this readout constant, i.e. a check that could not fail.
    const txt = id => { const e = document.getElementById(id); return e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '(absent)'; };
    // ⚠️ CAPTURE ORDER IS LOAD-BEARING. `#budget` and `#temporal` contend for
    // the left column, so opening the panel below to read it CLOSES the budget
    // pod — this probe was mutating the state it was measuring, and reported
    // `#budget-pod` as a control that reaches nothing in all six views.
    // Recorded as CLASS + rendered display, because the two can disagree: the
    // pod yields the left column to `#temporal` via CSS, so `body.budget` can
    // say open over a `display:none` pod. Reading either alone hides that.
    const budget = (document.body.classList.contains('budget') ? 'cls:on' : 'cls:off') + '|'
      + (document.getElementById('budget')
        ? getComputedStyle(document.getElementById('budget')).display : 'absent');
    const f = state.data.features.find(x => x.properties.neighbourhood_name === HOOD);
    let tip = '(no feature)';
    // viewTooltip returns deck's `{ html }` wrapper, not a string — String() on
    // it yields a constant "[object Object]", the second way this readout
    // managed to be invariant without being checked.
    try {
      const t = f ? viewTooltip({ object: f }) : null;
      tip = t == null ? tip : (typeof t === 'object' ? (t.html ?? JSON.stringify(t)) : String(t));
    } catch (e) { tip = 'THREW: ' + e.message; }
    let panel = '(not opened)';
    try { openTemporal(HOOD); panel = txt('temporal-body') + '|' + txt('temporal-note'); } catch (e) { panel = 'THREW: ' + e.message; }
    let peek = '(not opened)';
    try { if (f) { closePeek(); openPeek(f.properties); peek = txt('peek'); closePeek(); } } catch (e) { peek = 'THREW: ' + e.message; }
    // Leave the panel shut: an open `#temporal` suppresses the budget pod, so a
    // capture that leaves it open poisons the NEXT capture's budget readout.
    try { document.getElementById('temporal-close').click(); } catch (e) { /* not open */ }
    // `#hoodmode` acts by REDUCING the tooltip, and that reduction lives in
    // tooltipFor, not viewTooltip — reading only the latter makes hoodmode look
    // like a control that reaches nothing.
    let tipFor = '(no feature)';
    try {
      const t = f ? tooltipFor({ object: f }) : null;
      tipFor = t == null ? '(null)' : (typeof t === 'object' ? (t.html ?? JSON.stringify(t)) : String(t));
    } catch (e) { tipFor = 'THREW: ' + e.message; }
    return {
      title: txt('title-h'),
      tipFor,
      // Visibility, not text: the pod's content renders once, so reading text
      // alone reports the app's one non-map control as modifying nothing.
      budget,
      blurb: txt('title-p'),
      legend: txt('legend-label') + '|' + txt('legend-min') + '|' + txt('legend-max') + '|' + txt('legend-cats'),
      tooltip: tip,
      panel,
      peek,
      layers: (typeof overlay !== 'undefined' ? overlay._deck.props.layers.map(l => l.id).sort().join(',') : '(none)'),
    };
  }, HOOD);

  const click = async s => { try { await page.$eval(s, b => b.click()); return true; } catch (e) { return false; } };

  // Falsify the instrument before trusting it: every readout must be non-empty
  // and non-sentinel on the default view, or an "invariant" verdict below is
  // just this probe failing to look.
  const probe0 = await readouts();
  for (const [k, v] of Object.entries(probe0)) {
    const bad = !v || /^\((no feature|not opened|absent|none)\)|^THREW|^\[object /.test(v);
    console.log(`selftest ${k.padEnd(8)} ${bad ? 'DEAD  ' : 'live  '} ${String(v).slice(0, 70)}`);
  }

  const KEYS = ['title', 'blurb', 'legend', 'tooltip', 'tipFor', 'panel', 'peek', 'budget', 'layers'];
  const rows = [];

  for (const v of VIEWS) {
    if (!(await page.$(`#views button[data-view="${v}"]`))) continue;
    await click(`#views button[data-view="${v}"]`);
    await page.waitForTimeout(3500);
    const inv = await inventory();

    for (const [group, items] of Object.entries(inv)) {
      if (items.length < 2 && !group.startsWith('services')) {
        // A lone checkbox is still a two-value control: on and off.
        if (items.length !== 1) continue;
      }
      const caps = [];
      for (const it of items) {
        if (!(await click(it.sel))) continue;
        await page.waitForTimeout(1600);
        caps.push({ label: it.text || it.sel, r: await readouts() });
        if (items.length === 1) { // toggle: capture the other state too
          await click(it.sel); await page.waitForTimeout(1600);
          caps.push({ label: it.text + ' (off)', r: await readouts() });
        }
      }
      if (caps.length < 2) continue;
      const varies = {};
      for (const k of KEYS) varies[k] = new Set(caps.map(c => c.r[k])).size > 1;
      rows.push({ view: v, group, n: caps.length, varies,
                  labels: caps.map(c => c.label) });
      // Re-enter the view so the next group starts from a clean-ish state.
      await click(`#views button[data-view="${v}"]`);
      await page.waitForTimeout(2000);
    }
  }

  console.log('\nview        | control        | n | ' + KEYS.join(' '));
  for (const r of rows) {
    const marks = KEYS.map(k => (r.varies[k] ? 'Y' : '.').padEnd(k.length)).join(' ');
    console.log(`${r.view.padEnd(11)} | ${r.group.padEnd(14)} | ${r.n} | ${marks}`);
  }
  console.log('\n--- controls that reach NOTHING ---');
  for (const r of rows) if (!KEYS.some(k => r.varies[k]))
    console.log(`${r.view} / ${r.group}  [${r.labels.join(' , ')}]`);
  console.log('\n--- readout invariant under a control in the SAME panel ---');
  for (const r of rows) {
    const dead = KEYS.filter(k => !r.varies[k]);
    if (dead.length && dead.length < KEYS.length)
      console.log(`${r.view} / ${r.group}: invariant = ${dead.join(',')}`);
  }
  console.log('\nJSON ' + JSON.stringify(rows));
  await browser.close();
})();

// Verify every public title blurb (#title-p) against the writing rules in
// docs/COPY_DECISIONS.md group B, fast enough to run on every deploy.
//
// Two halves, because each alone can pass under a bug:
//   A. RULES — sets `state` (and camFlat / the active grid) directly and calls
//      currentBlurb() for every public view x control state (~150), without
//      rebuilding the map. Milliseconds per state. Checks the B8 shape (1-3
//      paragraphs, one bold term in P1, <= 400 characters — B5), that a flat
//      camera draws no height so the text claims none (B3), that the colour
//      clause follows the toggle, and that each blurb names what its state
//      shows (metric, cell size, window years).
//   B. WIRING — real clicks on every control that rewrites the blurb, the
//      camera flip, and the landing page. After each, the text on screen must
//      equal currentBlurb() for the live state. This is what ties A to the
//      page: A proves the functions, B proves the page shows them.
//
//   node verify-blurbs.js <url>                 (use ?build=public)
//   node verify-blurbs.js <url> --dump out.json (every state's text, length
//                                                and rendered height)
const { chromium } = require('playwright');
const [url, ...rest] = process.argv.slice(2);
const dumpPath = rest[0] === '--dump' ? rest[1] : null;

// Lenses whose main encoding is height, so their 3D blurb must say so (B3 (a)).
const HEIGHT_LENSES = ['money', 'glass', 'change', 'ratio'];
const PUBLIC_VIEWS = ['money', 'development', 'services', 'ratio'];

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1366, height: 768 } });
  page.on('pageerror', e => { console.log('PAGE EXCEPTION:', e.message); fail++; });
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);
  // The rules are the PUBLIC build's (TODO "Public blurb cleanup"); the full
  // build has more views and cuts than this script enumerates.
  if (await page.evaluate(() => FULL_BUILD)) {
    console.log('FAIL  PARTIAL — ran 0 checks: this is the full build; pass ?build=public or the public root');
    await browser.close();
    process.exit(1);
  }

  // What a reader sees for a blurb string, whitespace-normalised (the landing
  // copy is static HTML with line breaks).
  await page.evaluate(() => {
    window.__plain = t => t.replace(/\*\*/g, '').split(/\n\s*\n/).join('').replace(/\s+/g, ' ').trim();
    window.__shown = () => document.getElementById('title-p').textContent.replace(/\s+/g, ' ').trim();
  });
  const click = sel => page.$eval(sel, b => b.click());
  // Poll: some handlers set the blurb after an async grid load.
  const inSync = async () => {
    for (let i = 0; i < 40; i++) {
      if (await page.evaluate(() => __shown() === __plain(currentBlurb()))) return true;
      await page.waitForTimeout(250);
    }
    return false;
  };

  // ---- B1. the landing page ------------------------------------------------
  // Nothing rewrites the blurb on load, so the static HTML copy IS the landing
  // blurb and must match the code's.
  check('landing: the static HTML blurb equals currentBlurb()', await inSync(),
    await page.evaluate(() => __shown().slice(0, 80)));

  // ---- the public surface this script enumerates ---------------------------
  // Hard-coded below, so assert it still matches the page: a new public view
  // must fail here rather than go unchecked. (Services are enumerated from
  // SERVICES[*].pub, so a newly public service is covered automatically.)
  const surface = await page.evaluate(() => ({
    views: [...document.querySelectorAll('#views button')]
      .filter(b => getComputedStyle(b).display !== 'none').map(b => b.dataset.view),
  }));
  check('public views are the ones enumerated', JSON.stringify(surface.views) === JSON.stringify(PUBLIC_VIEWS),
    surface.views.join(','));

  // Load the grids every public state can reach, once, through the UI.
  await click('#moneydetail button[data-moneydetail="grid"]');
  await click('#moneydetail button[data-moneydetail="grid-fine"]');
  await page.waitForFunction(() => gridStore[100] && gridStore[50], null, { timeout: 60000 });
  await click('#moneydetail button[data-moneydetail="hood"]');
  await click('#views button[data-view="development"]');
  await page.waitForFunction(() => devGridData, null, { timeout: 60000 });
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1000);

  // ---- A. rules over every public state ------------------------------------
  const t0 = Date.now();
  const res = await page.evaluate(({ HEIGHT_LENSES, dump }) => {
    const KEEP = ['view', 'metric', 'denom', 'colorAdjust', 'chgWindow', 'devMetric',
                  'devWindow', 'devGrid', 'svcDriver', 'glassCell'];
    const saved = { ...Object.fromEntries(KEEP.map(k => [k, state[k]])),
                    services: { ...state.services }, camFlat, gridData, gridCell };
    const HEIGHT = /\b(taller|tallest|height|heights|rises where|sinks)\b/i;
    const METRIC_KEYS = ['revenue_per_acre', 'res_revenue_per_acre', 'nonres_revenue_per_acre', 'value_per_acre'];
    const pub = Object.keys(SERVICES).filter(k => SERVICES[k].pub);
    const states = [];
    for (const flat of [false, true]) {
      for (const metric of METRIC_KEYS) for (const denom of ['ground', 'lot'])
        for (const colorAdjust of [true, false]) {
          states.push({ lens: 'money', flat, set: { view: 'money', metric, denom, colorAdjust } });
          for (const cell of [100, 50])
            states.push({ lens: 'glass', flat, cell, set: { view: 'glass', metric, denom, colorAdjust, glassCell: cell } });
        }
      for (const chgWindow of ['long', 'short'])
        states.push({ lens: 'change', flat, set: { view: 'change', chgWindow } });
      for (const devMetric of ['units', 'permits']) for (const devWindow of ['3yr', '5yr', 'long'])
        for (const devGrid of [false, true])
          states.push({ lens: 'development', flat, set: { view: 'development', devMetric, devWindow, devGrid } });
      // Services: the driver is always checked; any subset of the others may be.
      for (const svcDriver of pub) {
        const others = pub.filter(k => k !== svcDriver);
        for (let mask = 0; mask < 1 << others.length; mask++) {
          const on = new Set([svcDriver, ...others.filter((_, i) => mask & (1 << i))]);
          states.push({ lens: 'services', flat, set: { view: 'services', svcDriver },
                        services: Object.fromEntries(Object.keys(state.services).map(k => [k, on.has(k)])) });
        }
      }
      states.push({ lens: 'ratio', flat, set: { view: 'ratio' } });
    }

    const out = [], bad = [];
    for (const s of states) {
      Object.assign(state, s.set);
      if (s.services) state.services = s.services;
      camFlat = s.flat;
      if (s.cell) { gridData = gridStore[s.cell]; gridCell = s.cell; }
      const raw = currentBlurb();
      const paras = raw.split(/\n\s*\n/);
      const plain = paras.map(p => p.replace(/\*\*/g, '')).join(' ');
      const id = [s.lens, ...Object.values(s.set).slice(1), s.cell, s.services &&
        Object.keys(s.services).filter(k => s.services[k]).join('+'), s.flat ? '2d' : '3d']
        .filter(v => v !== undefined && v !== '').join('/');
      const why = [];
      // Markup is well-formed on every lens, rewritten or not.
      if (paras.some(p => (p.match(/\*\*/g) || []).length % 2)) why.push('unpaired **');
      if (!(paras.length >= 1 && paras.length <= 3)) why.push(`${paras.length} paragraphs`);
      const bolds = (raw.match(/\*\*/g) || []).length / 2;
      if (bolds !== 1 || !/\*\*[^*]+\*\*/.test(paras[0])) why.push(`${bolds} bold, not one in P1`);
      if (plain.length > 400) why.push(`${plain.length} chars`);
      if (s.flat && HEIGHT.test(plain)) why.push('2D text claims height: "' + plain.match(HEIGHT)[0] + '"');
      if (HEIGHT_LENSES.includes(s.lens) && !s.flat && !HEIGHT.test(plain)) why.push('3D text omits height');
      if (s.lens === 'money' || s.lens === 'glass') {
        if (state.colorAdjust !== /square-root/.test(plain) || state.colorAdjust === /colour is linear/.test(plain))
          why.push('colour clause does not follow the toggle');
      }
      if (s.lens === 'glass') {
        const label = METRICS[state.metric].legendLabel;
        const want = (state.denom === 'lot' ? label.replace('per acre', 'per lot acre') : label) + ` in ${s.cell} m grid cells`;
        const got = (paras[0].match(/\*\*([^*]+)\*\*/) || [])[1];
        if (got !== want) why.push(`bold "${got}", want "${want}"`);
        // The azure count is a claim about cells that carry tax on THIS cut.
        // Recomputed here from the raw cells, not from glassInstCells(), so a
        // regression in that filter cannot also pass this check (F1).
        const cols = gridData.columns, col = cols[gridColKey()], fcol = cols.exempt_frac ?? -1;
        const want_n = fcol < 0 || !isRevenue(state.metric) ? 0 : gridData.cells.filter(
          c => c[col] > 0 && c[fcol] != null && c[fcol] >= GLASS_EXEMPT_MIN).length;
        const said = plain.match(/([\d,]+) azure cells? (?:is|are)/);
        const said_n = said ? Number(said[1].replace(/,/g, '')) : 0;
        if (said_n !== want_n) why.push(`says ${said_n} azure cells, ${want_n} flagged cells carry tax on this cut`);
      }
      if (s.lens === 'change' && !(plain.includes(CHG_WINDOW_LABEL[state.chgWindow]) &&
          plain.includes(`no ${CHG_WINDOWS[state.chgWindow]} value`)))
        why.push('window years missing');
      if (s.lens === 'development') {
        if (!plain.includes(DEV_WINDOW_LABEL[state.devWindow])) why.push('window years missing');
        if (state.devMetric === 'permits' ? !/New residential permits per acre/.test(plain) || /dwelling units/.test(plain)
                                          : !/New homes per acre/.test(plain)) why.push('metric misnamed');
      }
      if (s.lens === 'services' &&
          Object.values(s.services).filter(Boolean).length > 1 !== /Other checked layers draw neutral/.test(plain))
        why.push('neutral-layers note does not follow the checked set');
      if (why.length) bad.push(id + ': ' + why.join('; '));
      const row = { id, lens: s.lens, chars: plain.length, text: paras.map(p => p.replace(/\*\*/g, '')).join('\n\n') };
      if (dump) { setBlurb(raw); row.px = document.getElementById('title-p').offsetHeight; }
      out.push(row);
    }
    Object.assign(state, Object.fromEntries(KEEP.map(k => [k, saved[k]])));
    state.services = saved.services;
    camFlat = saved.camFlat; gridData = saved.gridData; gridCell = saved.gridCell;
    setBlurb(currentBlurb());
    const byLens = {};
    for (const r of out) byLens[r.lens] = (byLens[r.lens] || 0) + 1;
    return { n: out.length, byLens, bad, max: Math.max(...out.map(r => r.chars)), rows: dump ? out : null };
  }, { HEIGHT_LENSES, dump: !!dumpPath });
  console.log(`rules: ${res.n} states in ${Date.now() - t0} ms  ${JSON.stringify(res.byLens)}`);
  check(`rules: every public state passes (longest ${res.max} chars)`, res.bad.length === 0);
  res.bad.slice(0, 12).forEach(b => console.log('   ' + b));
  if (res.bad.length > 12) console.log(`   ... ${res.bad.length - 12} more`);
  if (dumpPath) require('fs').writeFileSync(dumpPath, JSON.stringify(res.rows, null, 1));

  // ---- B. wiring: every control that rewrites the blurb --------------------
  // One click per setBlurb call site; after each, the page must show the live
  // state's blurb. `pre` clicks set up a state without being checked.
  const steps = [
    ['metric: Value', '#metric-row button[data-metric="value"]'],
    ['lens: Change over time', '#moneymode button[data-moneymode="change"]'],
    ['change window: Since 2019', '#chgwindow button[data-chgwindow="short"]'],
    ['lens: Current', '#moneymode button[data-moneymode="current"]'],
    ['metric: Revenue', '#metric-row button[data-metric="revenue"]'],
    ['cut: Residential', '#revcut button[data-revcut="res_revenue_per_acre"]'],
    ['denominator: lot acres', '#denom button[data-denom="lot"]'],
    ['colour: linear', '#coloradj-btn'],
    ['detail: 100 m grid', '#moneydetail button[data-moneydetail="grid"]'],
    ['detail: 50 m grid', '#moneydetail button[data-moneydetail="grid-fine"]'],
    ['colour: sqrt (in the grid)', '#coloradj-btn'],
    ['detail: neighbourhood', '#moneydetail button[data-moneydetail="hood"]'],
    ['view: Development', '#views button[data-view="development"]'],
    ['dev metric: Permits', '#devmetric button[data-devmetric="permits"]'],
    ['dev window: Last 3 yr', '#devwindow button[data-devwindow="3yr"]'],
    ['dev detail: neighbourhood', '#devdetail button[data-devdetail="hood"]'],
    ['view: Services', '#views button[data-view="services"]'],
    ['service on: Roads cost', '#services .svc[data-service="roadscost"] .svc-on'],
    ['service colour: Roads cost', '#services .svc[data-service="roadscost"] input[name="svc-driver"]'],
    ['view: Ratio', '#views button[data-view="ratio"]'],
    ['view: Money', '#views button[data-view="money"]'],
  ];
  const drift = [];
  for (const [name, sel] of steps) {
    await click(sel);
    if (!(await inSync())) drift.push(name);
  }
  // The camera flip re-renders the blurb (syncMode), with no control clicked.
  for (const [name, flat] of [['camera: 2D', true], ['camera: 3D', false]]) {
    await page.evaluate(f => map.jumpTo({ pitch: f ? 0 : HOME.pitch }), flat);
    if (!(await inSync()) || await page.evaluate(() => camFlat) !== flat) drift.push(name);
  }
  check(`wiring: the page shows the live state's blurb after each of ${steps.length + 2} changes`,
    drift.length === 0, drift.join(', '));

  // setBlurb renders the markup as nodes, never HTML.
  const r = await page.evaluate(() => {
    setBlurb('One **bold <i>x</i>** term.\n\nTwo <b>y</b>.');
    const el = document.getElementById('title-p'), ps = [...el.children];
    const out = { np: ps.length, tags: ps.map(p => p.tagName).join(), b: el.querySelectorAll('b').length,
                  bText: el.querySelector('b')?.textContent, p2: ps[1]?.textContent,
                  first: ps[0].firstChild.nodeType };
    setBlurb(currentBlurb());
    return out;
  });
  check('setBlurb: paragraphs as <p>, one <b>, HTML stays text',
    r.np === 2 && r.tags === 'P,P' && r.b === 1 && r.bText === 'bold <i>x</i>' && r.p2 === 'Two <b>y</b>.' && r.first === 3,
    JSON.stringify(r));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  console.log('COMPLETE — ran every check (public build)');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

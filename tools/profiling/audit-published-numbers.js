// SCOPING INSTRUMENT for the "published number with no check" audit.
//
// ⚠️ It reads the RENDERED page, not the source. A regex over `web/index.html`
// cannot tell a blurb from a code comment — the first attempt at this counted
// `colorClamp: 30_000, // hand-set from the ramp` as a reader-facing claim —
// and the blurbs are `+`-concatenated across lines, so a per-line match splits
// a number from its sentence. Driving the page is the only way to enumerate
// what a reader can actually see.
//
// Emits JSON: every numeric claim visible in blurb / panel note / legend text,
// per view, per money metric and per service layer, with the surface it
// appeared on. It asserts NOTHING — ranking and coverage judgement belong to
// the audit run.
//
// ⚠️ Two limits the first version had, closed 2026-09-15 (S160):
//   1. It looped `Object.keys(VIEWS)`, which has no `money` key — the LANDING
//      view and its four metrics were never captured. They are now captured
//      first, as `view:money` and `metric:<key>`.
//   2. It drove views and services by JS, which works on the PUBLIC build for
//      controls that build hides — so the public inventory counted surfaces a
//      public reader cannot reach. Each surface now carries `reachable`: the
//      button/row that leads to it is visible. Filter on it for public exposure.
//
//   node audit-published-numbers.js <url> [--hoods A,B]   > claims.json
const { chromium } = require('playwright');
const argv = process.argv.slice(2);
const url = argv[0];
const hoodsArg = argv.indexOf('--hoods');
const HOODS = hoodsArg > -1 ? argv[hoodsArg + 1].split(',') : ['DOWNTOWN'];

// Dollar amounts, percentages, distances, magnitudes. Bare small integers are
// excluded: "the two bases" and "31 fire stations" are prose, not a published
// figure a guard could anchor. Years are kept — a stale year IS a published
// number, and this project has shipped one (DECISIONS.md 2026-08-27).
// `k` is in the suffix set because the money legends print their clamps as
// `$50k+` / `$4M+` — without it `$50k` tokenised as `$50` and merged with the
// About panel's "$50 per metre" (found 2026-09-15, S160).
const NUM = /\$[\d,]+(?:\.\d+)?(?:\s?(?:million|billion|M|B|k))?|\d[\d,]*(?:\.\d+)?\s?(?:million|billion|%|km|m\b|×|times)|\b(?:19|20)\d{2}\b/g;

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);

  // `reachable`: the control a reader would press to get here is visible.
  // Views that are render-modes of another view map to that view's button,
  // the same way applyView does.
  const surfaces = async (label, reach) => page.evaluate(({ label, reach }) => {
    const txt = id => (document.getElementById(id) || {}).textContent || '';
    const vis = el => !!el && getComputedStyle(el).display !== 'none';
    const leg = [...document.querySelectorAll('#legend *')]
      .map(e => e.children.length ? '' : e.textContent).join(' ');
    let reachable = true;
    if (reach.view) {
      const v = reach.view;
      const btn = (v === 'glass' || v === 'change') ? 'money'
                : v === 'infill' ? 'development'
                : (typeof LAB_VIEWS !== 'undefined' && LAB_VIEWS.includes(v)) ? 'lab' : v;
      reachable = vis(document.querySelector(`#views button[data-view="${btn}"]`));
    }
    if (reach.service) {
      reachable = vis(document.querySelector(`#views button[data-view="services"]`))
        && [...document.querySelectorAll(`[data-service="${reach.service}"]`)].some(vis);
    }
    if (reach.metric) {
      const btn = reach.metric.includes('revenue') ? 'revenue' : 'value';
      reachable = vis(document.querySelector(`#views button[data-view="money"]`))
        && vis(document.querySelector(`[data-metric="${btn}"]`));
    }
    return {
      label,
      reachable,
      blurb: txt('title-p'),
      title: txt('title-h'),
      note: txt('temporal-note'),
      read: txt('temporal-read'),
      legend: leg.replace(/\s+/g, ' ').trim(),
      about: txt('about-menu'),
    };
  }, { label, reach });

  const out = [];
  const pin = async (hood) => {
    // A hood must be pinned for the panel note to exist at all.
    await page.evaluate((h) => { try { closeTemporal(); } catch (e) {} try { openTemporal(h); } catch (e) {} }, hood);
    await page.waitForTimeout(500);
  };

  for (const hood of HOODS) {
    const tag = HOODS.length > 1 ? `@${hood}` : '';

    // Money — the landing view — and each of its metrics.
    await page.evaluate(async () => { await applyView('money'); });
    await page.waitForTimeout(900);
    await pin(hood);
    out.push(await surfaces(`view:money${tag}`, { view: 'money' }));
    const metrics = await page.evaluate(() => Object.keys(METRICS));
    for (const m of metrics) {
      await page.evaluate((m) => { applyMetric(m); }, m);
      await page.waitForTimeout(600);
      await pin(hood);
      out.push(await surfaces(`metric:${m}${tag}`, { metric: m }));
    }
    await page.evaluate(() => { applyMetric('revenue_per_acre'); });

    const views = await page.evaluate(() => Object.keys(VIEWS));
    for (const v of views) {
      await page.evaluate(async (v) => { await applyView(v); }, v);
      await page.waitForTimeout(900);
      await pin(hood);
      out.push(await surfaces(`view:${v}${tag}`, { view: v }));
      if (v === 'services') {
        const keys = await page.evaluate(() => Object.keys(SERVICES));
        for (const k of keys) {
          await page.evaluate(async (k) => {
            applyService(k, true);
            Object.keys(SERVICES).forEach(s => { if (s !== k) applyService(s, false); });
            if (state.svcDriver !== k) applySvcDriver(k);
          }, k);
          await pin(hood);
          await page.waitForTimeout(700);
          out.push(await surfaces(`service:${k}${tag}`, { service: k }));
        }
      }
    }
  }

  // Collapse to distinct claims, each with the surfaces it appears on.
  const claims = {};
  for (const s of out) {
    for (const [field, text] of Object.entries(s)) {
      if (field === 'label' || field === 'reachable' || !text) continue;
      for (const m of String(text).match(NUM) || []) {
        const k = m.trim();
        const c = (claims[k] ||= { where: new Set(), reachable: new Set() });
        c.where.add(`${s.label}/${field}`);
        if (s.reachable) c.reachable.add(`${s.label}/${field}`);
      }
    }
  }
  const rows = Object.entries(claims)
    .map(([value, c]) => ({ value, n: c.where.size, reachable: c.reachable.size,
                            where: [...c.where].slice(0, 6) }))
    .sort((a, b) => b.n - a.n);
  const reachableSurfaces = out.filter(s => s.reachable).length;
  console.log(JSON.stringify({
    captured: out.length, reachable_surfaces: reachableSurfaces, hoods: HOODS,
    distinct: rows.length, distinct_reachable: rows.filter(r => r.reachable).length, rows,
  }, null, 1));
  await browser.close();
})().catch(e => { console.error('THREW:', e.message); process.exit(1); });

// One-off verify for the "Non-res $" Money metric (2026-07-18) — the
// non-residential decomposition (nonres_revenue_per_acre: the slices billed at
// the Non Residential rate, a SUBSET of Revenue and the complement of
// Residential $ — SPEC_industrial.md A1). Checks: the #toggle button shows only
// when the data carries the column (SKIP-guard otherwise); selecting it
// re-drives the prism column + title/blurb (blurb must carry the "subset of
// Revenue" honesty line); legend anchors ($50k+ hand-set clamp); the subset
// invariant nonres <= rev per hood; res + nonres <= rev (the two subsets can't
// exceed the total — farmland is the only other slice); the lot denominator
// swaps to nonres_revenue_per_lot_acre with an independent p97.5 clamp; Glass
// draws the 100 m nonres cells when the grid file carries the columns and
// falls back to hood prisms on older files — branch-checked.
//   node verify-nonres-revenue.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

function approx(a, b, rel = 1e-6) { return Math.abs(a - b) <= rel * Math.max(Math.abs(a), Math.abs(b), 1); }

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  const click = sel => page.$eval(sel, b => b.click());
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  // --- column guard ---------------------------------------------------------
  const guard = await page.evaluate(() => ({
    has: state.hasNonresRevenue,
    btnShown: getComputedStyle(
      document.querySelector('#toggle button[data-metric="nonres_revenue_per_acre"]')
    ).display !== 'none',
  }));
  if (!guard.has) {
    check('button hidden when column absent (guard)', !guard.btnShown);
    console.log('SKIP  data file predates nonres_revenue_per_acre — nothing more to verify');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }
  check('button shown when column present', guard.btnShown);

  // --- switch to Non-res $ ---------------------------------------------------
  await click('#toggle button[data-metric="nonres_revenue_per_acre"]');
  await page.waitForTimeout(1500);
  const c = await page.evaluate(() => ({
    metric: state.metric,
    title: document.getElementById('title-h').textContent,
    blurb: document.getElementById('title-p').textContent,
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
  }));
  console.log('nonres metric  :', JSON.stringify(c));
  check('state.metric switched', c.metric === 'nonres_revenue_per_acre');
  check('title says Non-Residential Tax Revenue', /Non-Residential Tax Revenue/.test(c.title));
  check('blurb carries the subset-of-Revenue honesty line',
    /subset of Revenue/.test(c.blurb) && /not\s+all of what the land pays/.test(c.blurb));
  check('legend label', c.label === 'Non-residential revenue per acre');
  check('legend max = hand-set clamp', c.max === '$50k+');

  // Prism column re-driven + subset sanity (nonres <= rev; res + nonres <= rev).
  const drive = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'metric-extrusion');
    const f = state.data.features.find(x =>
      x.properties.nonres_revenue_per_acre != null && !x.properties.is_set_aside);
    const eps = 1 + 1e-9;
    const bad = state.data.features.filter(x =>
      x.properties.nonres_revenue_per_acre != null && x.properties.revenue_per_acre != null &&
      x.properties.nonres_revenue_per_acre > x.properties.revenue_per_acre * eps).length;
    const badSum = state.data.features.filter(x =>
      x.properties.nonres_revenue_per_acre != null && x.properties.res_revenue_per_acre != null &&
      x.properties.revenue_per_acre != null &&
      x.properties.nonres_revenue_per_acre + x.properties.res_revenue_per_acre >
        x.properties.revenue_per_acre * eps).length;
    const cfg = METRICS[state.metric];
    return { elev: layer.props.getElevation(f), base: f.properties.nonres_revenue_per_acre,
             clamp: cfg.colorClamp, subsetViolations: bad, sumViolations: badSum };
  });
  check('getElevation reads nonres_revenue_per_acre', approx(drive.elev, drive.base));
  check('nonres <= revenue in every hood (subset invariant)', drive.subsetViolations === 0);
  check('res + nonres <= revenue in every hood (decomposition invariant)',
    drive.sumViolations === 0);

  // Tooltip in the nonres metric: main line is the nonres figure; the
  // residential share line still shows (it renders for every Money metric).
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(x =>
      x.properties.nonres_revenue_per_acre != null && x.properties.revenue_per_acre > 0 &&
      !x.properties.is_set_aside);
    return { html: tooltipFor({ object: f }).html,
             fmt: METRICS[state.metric].fmt(f.properties.nonres_revenue_per_acre) };
  });
  check('nonres tooltip main line is the nonres figure', tip.html.includes(tip.fmt + ' / acre'));
  check('nonres tooltip keeps the residential share line',
    /% of revenue is residential/.test(tip.html));

  // --- lot denominator -------------------------------------------------------
  await click('#denom button[data-denom="lot"]');
  await page.waitForTimeout(1500);
  const lot = await page.evaluate(() => {
    const sc = moneyScale();
    const props = state.data.features.map(f => f.properties);
    const vals = props.filter(p => p[sc.colKey] != null && !p.is_set_aside)
      .map(p => p[sc.colKey]).sort((a, b) => a - b);
    const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
      return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
    const f = state.data.features.find(x => x.properties[sc.colKey] != null && !x.properties.is_set_aside);
    return { colKey: sc.colKey, clamp: sc.clamp, indepClamp: q(vals, 0.975),
             label: document.getElementById('legend-label').textContent,
             tip: tooltipFor({ object: f }).html };
  });
  console.log('lot mode       :', JSON.stringify({ colKey: lot.colKey, clamp: lot.clamp, indepClamp: lot.indepClamp }));
  check('lot column is nonres_revenue_per_lot_acre', lot.colKey === 'nonres_revenue_per_lot_acre');
  check('lot clamp == independent p97.5', approx(lot.clamp, lot.indepClamp, 1e-9));
  check('lot legend label says per lot acre', /per lot acre/.test(lot.label));
  check('lot tooltip says "/ lot acre"', /\/ lot acre/.test(lot.tip));
  await click('#denom button[data-denom="ground"]');
  await page.waitForTimeout(800);

  // --- Glass: grid cells when the file carries the nonres columns, hood-prism
  // fallback on older files — both correct; the column guard decides.
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(2500);
  const glass = await page.evaluate(() => ({
    view: state.view, metric: state.metric,
    gridHasCol: gridData ? (gridData.columns['nonres_revenue_per_acre'] ?? -1) >= 0 : null,
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
    hoodPrisms: !!overlay._deck.props.layers.find(l => l.id === 'glass-extrusion'),
    gridLayer: !!overlay._deck.props.layers.find(l => l.id === 'glass-grid'),
  }));
  console.log('glass          :', JSON.stringify(glass));
  if (glass.gridHasCol) {
    check('grid layer drawn for the nonres metric (no hood-prism fallback)',
      glass.gridLayer === true && glass.hoodPrisms === false);
    const cells = await page.evaluate(() => {
      const layer = overlay._deck.props.layers.find(l => l.id === 'glass-grid');
      const col = gridData.columns['nonres_revenue_per_acre'];
      const rev = gridData.columns['revenue_per_acre'];
      const res = gridData.columns['res_revenue_per_acre'];
      const vals = gridData.cells.map(c => c[col]).filter(v => v != null)
        .sort((a, b) => a - b);
      const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
        return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
      const sample = gridData.cells.find(c => c[col] > 0);
      const bad = gridData.cells.filter(c =>
        c[col] != null && c[rev] != null && c[col] > c[rev] + 1).length; // +1: whole-$ rounding
      const badSum = res >= 0 ? gridData.cells.filter(c =>
        c[col] != null && c[res] != null && c[rev] != null &&
        c[col] + c[res] > c[rev] + 2).length : 0; // +2: two whole-$ roundings
      return { elev: layer.props.getElevation(sample), base: sample[col],
               clamp: gridScale().clamp, indepClamp: q(vals, 0.975),
               subsetViolations: bad, sumViolations: badSum, n: vals.length };
    });
    console.log('glass cells    :', JSON.stringify(cells));
    check('cell elevation reads nonres_revenue_per_acre', approx(cells.elev, cells.base));
    check('cell clamp == independent p97.5 of the nonres cells',
      approx(cells.clamp, cells.indepClamp, 1e-9));
    check('nonres <= revenue in every cell (subset invariant, ±$1 rounding)',
      cells.subsetViolations === 0);
    check('res + nonres <= revenue in every cell (decomposition, ±$2 rounding)',
      cells.sumViolations === 0);
    check('glass legend says 100 m cells', /100 m cells/.test(glass.label));
  } else {
    check('no grid layer drawn for the nonres metric (fallback path)', glass.gridLayer === false);
    check('hood-prism fallback drawn', glass.hoodPrisms === true);
    check('glass legend keeps hood anchors (no "100 m cells")',
      !/100 m cells/.test(glass.label) && glass.max === '$50k+');
  }

  // --- back to Money ---------------------------------------------------------
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(2000);
  const back = await page.evaluate(() => ({ metric: state.metric,
    title: document.getElementById('title-h').textContent }));
  check('metric persists across the Glass round-trip',
    back.metric === 'nonres_revenue_per_acre' && /Non-Residential Tax Revenue/.test(back.title));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

// One-off verify for the "Residential $" Money metric (2026-07-16) — the
// residential-revenue decomposition (res_revenue_per_acre: RESIDENTIAL +
// OTHER RESIDENTIAL class dollars, a SUBSET of Revenue). Checks: the #toggle
// button shows only when the data carries the column (SKIP-guard otherwise);
// selecting it re-drives the prism column + title/blurb (blurb must carry the
// "subset of Revenue" honesty line); legend anchors ($30k+ hand-set clamp);
// the tooltip share line ("N% of revenue is residential") appears in BOTH the
// Revenue and Residential $ metrics and matches an independent res/rev
// recompute; the Residential-only fade lens composes (fade fill + subset
// re-clamp via residentialClampFor); the lot denominator swaps to
// res_revenue_per_lot_acre with an independent p97.5 clamp; Glass draws the
// 100 m res cells when the grid file carries the res columns (pipeline
// 2026-07-17) and falls back to hood prisms on older files — branch-checked.
//   node verify-res-revenue.js <url>
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
    has: state.hasResRevenue,
    btnShown: getComputedStyle(
      document.querySelector('#toggle button[data-metric="res_revenue_per_acre"]')
    ).display !== 'none',
  }));
  if (!guard.has) {
    check('button hidden when column absent (guard)', !guard.btnShown);
    console.log('SKIP  data file predates res_revenue_per_acre — nothing more to verify');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }
  check('button shown when column present', guard.btnShown);

  // --- share line in the DEFAULT Revenue metric -----------------------------
  const revTip = await page.evaluate(() => {
    const f = state.data.features.find(x =>
      x.properties.res_revenue_per_acre != null && x.properties.revenue_per_acre > 0 &&
      !x.properties.is_set_aside);
    const p = f.properties;
    return { html: tooltipFor({ object: f }).html,
             indep: Math.round(100 * p.res_revenue_per_acre / p.revenue_per_acre) };
  });
  check('Revenue tooltip carries the share line',
    /% of revenue is residential/.test(revTip.html));
  check('share line matches independent res/rev recompute',
    new RegExp(`${revTip.indep}% of revenue is residential`).test(revTip.html),
    revTip.html.replace(/<[^>]+>/g, ' '));

  // --- switch to Residential $ -----------------------------------------------
  await click('#toggle button[data-metric="res_revenue_per_acre"]');
  await page.waitForTimeout(1500);
  const c = await page.evaluate(() => ({
    metric: state.metric,
    title: document.getElementById('title-h').textContent,
    blurb: document.getElementById('title-p').textContent,
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
  }));
  console.log('res metric     :', JSON.stringify(c));
  check('state.metric switched', c.metric === 'res_revenue_per_acre');
  check('title says Residential Tax Revenue', /Residential Tax Revenue/.test(c.title));
  check('blurb carries the subset-of-Revenue honesty line',
    /subset of Revenue/.test(c.blurb) && /not\s+all of what the land pays/.test(c.blurb));
  check('legend label', c.label === 'Residential revenue per acre');
  check('legend max = hand-set clamp', c.max === '$30k+');

  // Prism column re-driven + subset sanity (res <= rev everywhere).
  const drive = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'metric-extrusion');
    const f = state.data.features.find(x =>
      x.properties.res_revenue_per_acre != null && !x.properties.is_set_aside);
    const bad = state.data.features.filter(x =>
      x.properties.res_revenue_per_acre != null && x.properties.revenue_per_acre != null &&
      x.properties.res_revenue_per_acre > x.properties.revenue_per_acre * (1 + 1e-9)).length;
    const cfg = METRICS[state.metric];
    return { elev: layer.props.getElevation(f), base: f.properties.res_revenue_per_acre,
             clamp: cfg.colorClamp, subsetViolations: bad };
  });
  check('getElevation reads res_revenue_per_acre', approx(drive.elev, drive.base));
  check('res <= revenue in every hood (subset invariant)', drive.subsetViolations === 0);

  // Tooltip in the res metric: main line is the res figure, share line present.
  const resTip = await page.evaluate(() => {
    const f = state.data.features.find(x =>
      x.properties.res_revenue_per_acre != null && x.properties.revenue_per_acre > 0 &&
      !x.properties.is_set_aside);
    return { html: tooltipFor({ object: f }).html,
             fmt: METRICS[state.metric].fmt(f.properties.res_revenue_per_acre) };
  });
  check('res tooltip main line is the res figure', resTip.html.includes(resTip.fmt + ' / acre'));
  check('res tooltip keeps the share line', /% of revenue is residential/.test(resTip.html));

  // --- Residential-only fade lens composes ----------------------------------
  await click('#lens button[data-lens="residential"]');
  await page.waitForTimeout(1500);
  const lens = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'metric-extrusion');
    const faded = state.data.features.find(x =>
      !x.properties.is_residential && !x.properties.is_set_aside &&
      x.properties.res_revenue_per_acre != null);
    const kept = state.data.features.find(x =>
      x.properties.is_residential && x.properties.res_revenue_per_acre != null);
    return {
      on: state.residential,
      // getFillColor appends the fade's alpha — compare the RGB triple only.
      fadedFill: layer.props.getFillColor(faded).slice(0, 3).join(),
      fade: LENS_FADE_COLOR.slice(0, 3).join(),
      keptColoured: layer.props.getFillColor(kept).slice(0, 3).join() !==
        LENS_FADE_COLOR.slice(0, 3).join(),
      max: document.getElementById('legend-max').textContent,
      indepMax: METRICS[state.metric].fmt(residentialClampFor('res_revenue_per_acre')) + '+',
      aside: document.querySelector('#legend .aside span:last-child').textContent,
    };
  });
  console.log('lens composed  :', JSON.stringify(lens));
  check('lens on', lens.on === true);
  check('non-residential hood fades', lens.fadedFill === lens.fade);
  check('residential hood stays coloured', lens.keptColoured === true);
  check('legend re-clamps to the residential subset', lens.max === lens.indepMax);
  check('aside labels the fade', /non-residential/i.test(lens.aside));
  await click('#lens button[data-lens="residential"]'); // off again
  await page.waitForTimeout(800);

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
  check('lot column is res_revenue_per_lot_acre', lot.colKey === 'res_revenue_per_lot_acre');
  check('lot clamp == independent p97.5', approx(lot.clamp, lot.indepClamp, 1e-9));
  check('lot legend label says per lot acre', /per lot acre/.test(lot.label));
  check('lot tooltip says "/ lot acre" and keeps the share line',
    /\/ lot acre/.test(lot.tip) && /% of revenue is residential/.test(lot.tip));
  await click('#denom button[data-denom="ground"]');
  await page.waitForTimeout(800);

  // --- Glass: grid cells when the file carries the res columns (pipeline
  // 2026-07-17), hood-prism fallback on older files — both are correct; the
  // column guard decides (same idiom as the #toggle guard above).
  await click('#views button[data-view="glass"]');
  await page.waitForTimeout(2500);
  const glass = await page.evaluate(() => ({
    view: state.view, metric: state.metric,
    gridHasCol: gridData ? (gridData.columns['res_revenue_per_acre'] ?? -1) >= 0 : null,
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
    hoodPrisms: !!overlay._deck.props.layers.find(l => l.id === 'glass-extrusion'),
    gridLayer: !!overlay._deck.props.layers.find(l => l.id === 'glass-grid'),
  }));
  console.log('glass          :', JSON.stringify(glass));
  if (glass.gridHasCol) {
    check('grid layer drawn for the res metric (no hood-prism fallback)',
      glass.gridLayer === true && glass.hoodPrisms === false);
    const cells = await page.evaluate(() => {
      const layer = overlay._deck.props.layers.find(l => l.id === 'glass-grid');
      const col = gridData.columns['res_revenue_per_acre'];
      const rev = gridData.columns['revenue_per_acre'];
      const vals = gridData.cells.map(c => c[col]).filter(v => v != null)
        .sort((a, b) => a - b);
      const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
        return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
      const sample = gridData.cells.find(c => c[col] > 0);
      const bad = gridData.cells.filter(c =>
        c[col] != null && c[rev] != null && c[col] > c[rev] + 1).length; // +1: whole-$ rounding
      return { elev: layer.props.getElevation(sample), base: sample[col],
               clamp: gridScale().clamp, indepClamp: q(vals, 0.975),
               subsetViolations: bad, n: vals.length };
    });
    console.log('glass cells    :', JSON.stringify(cells));
    check('cell elevation reads res_revenue_per_acre', approx(cells.elev, cells.base));
    check('cell clamp == independent p97.5 of the res cells',
      approx(cells.clamp, cells.indepClamp, 1e-9));
    check('res <= revenue in every cell (subset invariant, ±$1 rounding)',
      cells.subsetViolations === 0);
    check('glass legend says 100 m cells with the cell clamp',
      /100 m cells/.test(glass.label) && glass.max !== '$30k+');
  } else {
    check('no grid layer drawn for the res metric (fallback path)', glass.gridLayer === false);
    check('hood-prism fallback drawn', glass.hoodPrisms === true);
    check('glass legend keeps hood anchors (no "100 m cells")',
      !/100 m cells/.test(glass.label) && glass.max === '$30k+');
  }

  // --- back to Money ---------------------------------------------------------
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(2000);
  const back = await page.evaluate(() => ({ metric: state.metric,
    title: document.getElementById('title-h').textContent }));
  check('metric persists across the Glass round-trip',
    back.metric === 'res_revenue_per_acre' && /Residential Tax Revenue/.test(back.title));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

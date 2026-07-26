// One-off verify for the Glass view (2026-07-04; grid-cell version). DOM +
// layer checks: layer stack (opaque neutral plane under translucent 100 m
// grid-cell spikes), plane fills (neutral vs set-aside), grid layer props +
// cell count vs the served file, colour clamp = cells' p97.5 (independent
// quantile), elevation parity with the money view's tallest hood, slider ->
// opacity live with per-view defaults, metric toggle renders live with a
// metric-driven title + the glass blurb + cell-scale legend, lens DISABLED,
// labels at ground, tooltip falls through to the money branch.
//   node verify-glass.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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

  // swiftshader can hang page.click while the render loop is busy — dispatch
  // the click from inside the page instead (same workaround as verify-labels).
  const click = sel => page.$eval(sel, b => b.click());
  // Glass is now Money's "100 m grid" render mode (no top-level view button) —
  // reach it by going to Money then flipping the Detail toggle; works from any
  // starting view. Labels moved to the accessibility-menu checkbox.
  const enterGlass = async () => {
    await click('#views button[data-view="money"]');
    await page.waitForTimeout(300);
    await click('#moneydetail button[data-moneydetail="grid"]');
  };
  const toggleLabels = () => page.$eval('#labels-on',
    el => { el.checked = !el.checked; el.dispatchEvent(new Event('change')); });

  const chrome = () => page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    blurbIsGlass: document.getElementById('title-p').textContent === glassBlurb(),
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    // NB: this reads #layers (the whole panel), which is why it stays true in
    // Glass even though Glass dropped the slider 2026-07-25. The prism row itself
    // is reported separately — see verify-glass-no-slider.js for the assertions.
    layersShown: getComputedStyle(document.getElementById('layers')).display !== 'none',
    prismRowShown: document.getElementById('prism-row').offsetParent !== null,
    prismPct: document.getElementById('prism-opacity').value,
    lensDisabled: document.querySelector('#lens button').disabled,
    denomShown: getComputedStyle(document.getElementById('denom')).display !== 'none',
    denom: state.denom,
  }));

  console.log('money default  :', JSON.stringify(await chrome()));

  await enterGlass();
  await page.waitForTimeout(3000);
  console.log('glass          :', JSON.stringify(await chrome()));

  // Layer stack, plane fills, grid props, and the scale anchors — the clamp
  // recomputed here with an independent quantile, and elevation parity:
  // tallest cell must reach exactly the money view's tallest hood prism.
  const stack = await page.evaluate(() => {
    const layers = overlay._deck.props.layers.map(l => l.id);
    const plane = overlay._deck.props.layers.find(l => l.id === 'glass-plane');
    const grid = overlay._deck.props.layers.find(l => l.id === 'glass-grid');
    let neutral = 0, aside = 0, bad = 0;
    for (const f of state.data.features) {
      const fill = plane.props.getFillColor(f).join();
      if (f.properties.is_set_aside) fill === SET_ASIDE_COLOR.join() ? aside++ : bad++;
      else fill === GLASS_PLANE_COLOR.join() ? neutral++ : bad++;
    }
    const col = gridData.columns[state.metric];
    const vals = gridData.cells.map(c => c[col]).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const cfg = METRICS[state.metric];
    const hoodMax = Math.max(...state.data.features.map(f => f.properties[cfg.key] || 0));
    const cellMax = vals[vals.length - 1];
    const gs = gridScale();
    // spot-check a mid cell's fill against the ramp at the sqrt-clamped t
    const mid = gridData.cells[Math.floor(gridData.cells.length / 2)];
    const expected = rampColorAt(Math.sqrt(Math.min(1, mid[col] / gs.clamp)));
    return { layers,
             planePickable: !!plane.props.pickable,
             gridPresent: !!grid, cellSize: grid && grid.props.cellSize,
             gridPickable: grid && !!grid.props.pickable,
             gridOpacity: grid && grid.props.opacity,
             nCells: gridData.cells.length,
             clampMatchesP975: Math.abs(gs.clamp - q) < 1e-6,
             parityOk: Math.abs(gs.elevationScale * cellMax - hoodMax * cfg.elevationScale) < 1e-6,
             midFillOk: grid.props.getFillColor(mid).join() === expected.join(),
             nHoods: state.data.features.length, neutral, aside, bad };
  });
  console.log('stack + scales :', JSON.stringify(stack));

  // Slider drives cell opacity live.
  await page.evaluate(() => {
    const el = document.getElementById('prism-opacity');
    el.value = 90; el.dispatchEvent(new Event('input'));
  });
  await page.waitForTimeout(500);
  const after = await page.evaluate(() =>
    overlay._deck.props.layers.find(l => l.id === 'glass-grid').props.opacity);
  console.log('slider -> 90   :', JSON.stringify({ gridOpacity: after }));

  // Metric toggle renders live: metric title, glass blurb kept, cell legend.
  await click('#metric-row button[data-metric="value"]');
  await page.waitForTimeout(1000);
  console.log('glass + value  :', JSON.stringify(await chrome()));
  await click('#revcut button[data-revcut="revenue_per_acre"]');
  await page.waitForTimeout(1000);

  // Spike denominator toggle (lot-acre variant, 2026-07-05): legend + scale
  // re-anchor to the lot column, null-lot cells drop from the render, the
  // blurb flips, and independent quantile/parity checks hold on the subset.
  await click('#denom button[data-denom="lot"]');
  await page.waitForTimeout(1500);
  const lot = await page.evaluate(() => {
    const grid = overlay._deck.props.layers.find(l => l.id === 'glass-grid');
    const col = gridData.columns.revenue_per_lot_acre;
    const nonNull = gridData.cells.filter(c => c[col] != null);
    const vals = nonNull.map(c => c[col]).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const gs = gridScale();
    const cfg = METRICS[state.metric];
    const hoodMax = Math.max(...state.data.features.map(f => f.properties[cfg.key] || 0));
    const mid = nonNull[Math.floor(nonNull.length / 2)];
    const expected = rampColorAt(Math.sqrt(Math.min(1, mid[col] / gs.clamp)));
    return { denom: state.denom,
             dataN: grid.props.data.length, nonNullN: nonNull.length,
             totalN: gridData.cells.length,
             clampMatchesP975: Math.abs(gs.clamp - q) < 1e-6,
             parityOk: Math.abs(gs.elevationScale * vals[vals.length - 1] - hoodMax * cfg.elevationScale) < 1e-6,
             midFillOk: grid.props.getFillColor(mid).join() === expected.join(),
             label: document.getElementById('legend-label').textContent,
             max: document.getElementById('legend-max').textContent,
             blurbIsLot: document.getElementById('title-p').textContent === GLASS_BLURBS.lot };
  });
  console.log('denom -> lot   :', JSON.stringify(lot));

  // Metric toggle keeps the lot denominator (label follows both).
  await click('#metric-row button[data-metric="value"]');
  await page.waitForTimeout(1000);
  console.log('lot + value    :', JSON.stringify(await chrome()));
  await click('#revcut button[data-revcut="revenue_per_acre"]');
  await page.waitForTimeout(1000);

  // Denominator state persists across a view round-trip; the control hides
  // outside glass.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1000);
  console.log('money (denom?) :', JSON.stringify(await chrome()));
  await enterGlass();
  await page.waitForTimeout(1000);
  console.log('glass (denom?) :', JSON.stringify(await chrome()));
  await click('#denom button[data-denom="ground"]');
  await page.waitForTimeout(1000);
  console.log('denom -> ground:', JSON.stringify(await chrome()));

  // Labels sit at the ground in glass (no hood prisms to ride).
  await toggleLabels();
  await page.waitForTimeout(1500);
  const labels = await page.evaluate(() => {
    const present = overlay._deck.props.layers.some(l => l.id === 'hood-labels');
    const f = state.data.features.find(f => f.properties.neighbourhood_name === 'DOWNTOWN').properties;
    return { present, groundZ: labelZ(f) };
  });
  console.log('labels         :', JSON.stringify(labels));
  await toggleLabels();
  await page.waitForTimeout(500);

  // Tooltip falls through to the money branch (metric + road lines).
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(f => f.properties.neighbourhood_name === 'STRATHCONA');
    return tooltipFor({ object: f }).html;
  });
  console.log('tooltip        :', tip);

  // Leaving: money restores chrome + re-enables the lens; entering ratio
  // resets the slider to ITS default (5), glass again -> its own (60).
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  console.log('back to money  :', JSON.stringify(await chrome()));
  await click('#views button[data-view="ratio"]');
  await page.waitForTimeout(2500);
  console.log('ratio slider   :', JSON.stringify(await chrome()));
  await enterGlass();
  await page.waitForTimeout(1500);
  console.log('glass again    :', JSON.stringify(await chrome()));

  await browser.close();
})();

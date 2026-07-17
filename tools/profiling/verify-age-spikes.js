// One-off verify for the Development view's stock-age spikes (2026-07-17) —
// the Spikes picker (New homes <-> Year built) on the 100 m Detail grid.
// Age cells ride in on the GLASS grid file (export_value_grid
// median_year_built, the whole-roll cell population). Checks: the picker is
// hidden until Detail is on AND the year column has loaded (SKIP-guard on
// older files); selecting Year built swaps the permit-cell layer for the age
// layer, hides the (inert-in-age-mode) Metric/Window pickers, and re-drives
// blurb + legend; height is LINEAR in year off the true oldest cell (no
// percentile trick on heights); colour is LINEAR between the p2.5 anchor
// (independent recompute) and the newest cell, ramp-top (yellow) = newest;
// null-year cells are absent from the layer (never year-0); switching back
// restores the permit spikes + pickers; and the Glass view still draws its
// grid off the same shared fetch.
//   node verify-age-spikes.js <url>
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
  const visible = sel => page.$eval(sel, el => getComputedStyle(el).display !== 'none');
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  // --- enter the development view; picker hidden before Detail --------------
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(2500);
  const pre = await page.evaluate(() => ({
    hasDevGrid: !!devGridData,
    spikeShown: getComputedStyle(document.getElementById('devspike')).display !== 'none',
  }));
  if (!pre.hasDevGrid) {
    console.log('SKIP  dev_grid.json missing — no Detail grid to hang the picker on');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }
  check('Spikes picker hidden before Detail is on', !pre.spikeShown);

  // --- Detail on: value_grid fetch kicks; guard on the year column ----------
  await page.$eval('#dev-grid-on', el => { el.checked = true; el.dispatchEvent(new Event('change')); });
  await page.waitForFunction(() => gridData !== null || gridFetch === null, { timeout: 15000 })
    .catch(() => {});
  await page.waitForTimeout(1000);
  const guard = await page.evaluate(() => ({
    gotGrid: !!gridData,
    col: typeof devAgeCol === 'function' ? devAgeCol() : -1,
    spikeShown: getComputedStyle(document.getElementById('devspike')).display !== 'none',
  }));
  if (guard.col < 0) {
    check('picker stays hidden when the year column is absent (guard)', !guard.spikeShown);
    console.log('SKIP  value_grid.json predates median_year_built — nothing more to verify');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }
  check('Spikes picker shown once the year column loaded', guard.spikeShown);
  const layerIds = () => page.evaluate(() =>
    overlay._deck.props.layers.filter(Boolean).map(l => l.id));
  let ids = await layerIds();
  check('permit spikes up by default', ids.includes('dev-grid-cells') && !ids.includes('dev-age-cells'));

  // --- switch to Year built --------------------------------------------------
  await click('#devspike button[data-devspike="age"]');
  await page.waitForTimeout(1500);
  ids = await layerIds();
  check('age layer swapped in', ids.includes('dev-age-cells') && !ids.includes('dev-grid-cells'));

  const c = await page.evaluate(() => ({
    spikes: state.devSpikes,
    metricShown: getComputedStyle(document.getElementById('devmetric')).display !== 'none',
    windowShown: getComputedStyle(document.getElementById('devwindow')).display !== 'none',
    blurb: document.getElementById('title-p').textContent,
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
  }));
  console.log('age mode       :', JSON.stringify(c));
  check('state.devSpikes = age', c.spikes === 'age');
  check('Metric/Window pickers hidden in age mode (inert controls)',
    !c.metricShown && !c.windowShown);
  check('blurb describes the age scale',
    /median construction year/.test(c.blurb) && /linear in year/.test(c.blurb));
  check('legend label', c.label === 'Median year built (100 m cells, linear colour)');

  // --- independent recompute of the scale + legend anchors -------------------
  const s = await page.evaluate(() => {
    // Independent: sort + linear-interpolated quantile, written out here.
    const col = devAgeCol();
    const years = gridData.cells.map(x => x[col]).filter(v => v != null).sort((a, b) => a - b);
    const pos = (years.length - 1) * 0.025;
    const lo = Math.floor(pos), hi = Math.ceil(pos);
    const p025 = lo === hi ? years[lo] : years[lo] + (years[hi] - years[lo]) * (pos - lo);
    return {
      n: years.length, total: gridData.cells.length,
      yMin: years[0], yMax: years[years.length - 1], p025,
      scale: ageGridScale(),
    };
  });
  console.log('scale          :', JSON.stringify(s));
  check('colour low anchor == independent p2.5 recompute', approx(s.scale.colorLo, s.p025));
  check('height baseline is the TRUE oldest cell (no percentile on heights)',
    s.scale.lo === s.yMin && s.scale.hi === s.yMax);
  check('legend anchors match', c.min === '≤ ' + Math.round(s.p025) &&
    c.max === String(Math.round(s.yMax)), `min=${c.min} max=${c.max}`);
  check('blurb coverage counts match the file',
    c.blurb.includes(s.n.toLocaleString()) && c.blurb.includes(s.total.toLocaleString()));
  check('years plausible (loader window held)', s.yMin >= 1850 && s.yMax <= 2100);

  // --- layer mechanics: null cells absent, height linear, yellow = newest ----
  const mech = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'dev-age-cells');
    const col = devAgeCol();
    const cells = layer.props.data;
    const sc = ageGridScale();
    const newest = cells.find(x => x[col] === sc.hi);
    const oldest = cells.find(x => x[col] === sc.lo);
    const mid = cells.find(x => x[col] > sc.colorLo && x[col] < sc.hi);
    return {
      nData: cells.length, nulls: cells.filter(x => x[col] == null).length,
      elevNewest: layer.props.getElevation(newest),
      elevOldest: layer.props.getElevation(oldest),
      elevMid: layer.props.getElevation(mid), yMid: mid[col],
      elevationScale: layer.props.elevationScale,
      colorNewest: layer.props.getFillColor(newest),
      colorOldest: layer.props.getFillColor(oldest),
      rampTop: rampColorAt(1), rampBottom: rampColorAt(0),
      peak: DEV_GRID_PEAK, lo: sc.lo, hi: sc.hi,
    };
  });
  check('layer data = known-year cells only (null cells absent)',
    mech.nData === s.n && mech.nulls === 0);
  check('height linear in year off the oldest cell',
    approx(mech.elevNewest, mech.hi - mech.lo) && mech.elevOldest === 0 &&
    approx(mech.elevMid, mech.yMid - mech.lo));
  check('peak parity with the permit spikes (elevationScale = PEAK / span)',
    approx(mech.elevationScale, mech.peak / (mech.hi - mech.lo)));
  check('newest cell wears the ramp top (yellow)',
    JSON.stringify(mech.colorNewest) === JSON.stringify(mech.rampTop),
    `newest=${JSON.stringify(mech.colorNewest)}`);
  check('oldest cell wears the ramp bottom (dark)',
    JSON.stringify(mech.colorOldest) === JSON.stringify(mech.rampBottom));

  // --- back to activity: pickers + permit layer restored ---------------------
  await click('#devspike button[data-devspike="activity"]');
  await page.waitForTimeout(1000);
  ids = await layerIds();
  const back = await page.evaluate(() => ({
    metricShown: getComputedStyle(document.getElementById('devmetric')).display !== 'none',
    windowShown: getComputedStyle(document.getElementById('devwindow')).display !== 'none',
  }));
  check('permit spikes restored', ids.includes('dev-grid-cells') && !ids.includes('dev-age-cells'));
  check('Metric/Window pickers restored', back.metricShown && back.windowShown);

  // --- regression: Glass still draws off the shared fetch --------------------
  await click('#views button[data-view="glass"]');
  await page.waitForTimeout(2500);
  ids = await layerIds();
  check('Glass grid still renders (shared ensureGridData)', ids.includes('glass-grid'));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

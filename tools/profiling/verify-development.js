// One-off verify for the Development view (2026-07-12 — Lens A, permit-based
// new-dwelling-supply choropleth, SPEC_development.md). Checks: chrome on entry
// (title/blurb, legend label + sqrt-anchored max, aside row hidden, lens
// disabled, layers panel hidden); the dev-plane layer is the stack; the
// SET-ASIDE OVERRIDE (a set-aside hood with activity renders COLOURED, not
// grey); sqrt colour scaling matches an independently-derived clamp; a
// zero-activity hood renders the ramp low end (not grey); the tooltip carries
// units/acre + the count/permit line, and a set-aside hood's tooltip STILL
// shows its set-aside status; the legend gradient is sqrt; the units/permits
// SUB-METRIC PICKER (2026-07-13) switches the plane/scale/legend/tooltip to the
// new_permits_per_acre column; the 5yr/3yr WINDOW PICKER (2026-07-13) switches
// them to the new_units_per_acre_3yr column + the 2023–2025 label; the 100 m
// DETAIL-GRID TOGGLE (2026-07-15) swaps choropleth <-> neutral plane +
// dev-grid-cells spikes (linear height peak 2500 m, sqrt colour, per-cell
// legend, geocode-coverage blurb, opacity slider, picker-follows, off restores
// the choropleth, toggle hidden outside the view); a round-trip back to money
// restores the aside row. Exit code = number of FAILED assertions.
//   node verify-development.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let pass = 0, fail = 0;
const check = (name, cond) => { (cond ? pass++ : fail++); console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}`); };

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => { console.log('PAGE EXCEPTION:', e.message); fail++; });
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  const click = sel => page.$eval(sel, b => b.click());

  const hasCol = await page.evaluate(() =>
    state.data.features.some(f => f.properties.new_units_per_acre != null));
  check('data carries new_units_per_acre column', hasCol);
  if (!hasCol) { await browser.close(); process.exit(fail); }

  const btnVisible = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#views button[data-view="development"]')).display !== 'none');
  check('Development view button is visible', btnVisible);

  await click('#views button[data-view="development"]');
  await page.waitForTimeout(2500);

  const chrome = await page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    blurbMatches: document.getElementById('title-p').textContent === VIEWS.development.blurb,
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
    asideHidden: getComputedStyle(document.querySelector('#legend .aside')).display === 'none',
    lensDisabled: document.querySelector('#lens button').disabled,
    devPickerShown: getComputedStyle(document.getElementById('devmetric')).display !== 'none',
    unitsActive: document.querySelector('#devmetric button[data-devmetric="units"]').classList.contains('active'),
    devMetric: state.devMetric,
    windowPickerShown: getComputedStyle(document.getElementById('devwindow')).display !== 'none',
    fiveYrActive: document.querySelector('#devwindow button[data-devwindow="5yr"]').classList.contains('active'),
    devWindow: state.devWindow,
    hasDevWindow: state.hasDevWindow,
    layers: overlay._deck.props.layers.map(l => l.id),
  }));
  console.log('chrome:', JSON.stringify(chrome));
  check('view is development', chrome.view === 'development');
  check('title is set', /New Housing/.test(chrome.title));
  check('blurb matches VIEWS.development.blurb', chrome.blurbMatches);
  check('legend label mentions new homes', /new homes per acre/i.test(chrome.label));
  check('legend min is 0', chrome.min === '0');
  check('legend max ends with +', /\+$/.test(chrome.max));
  check('aside (set-aside grey) row hidden', chrome.asideHidden);
  check('residential lens disabled', chrome.lensDisabled);
  check('sub-metric picker shown (data has permits column)', chrome.devPickerShown);
  check('units sub-metric active by default', chrome.unitsActive && chrome.devMetric === 'units');
  if (chrome.hasDevWindow) {
    check('window picker shown (data has _3yr columns)', chrome.windowPickerShown);
    check('5yr window active by default', chrome.fiveYrActive && chrome.devWindow === '5yr');
    check('legend label shows the 5yr range (2021–2025)', /2021.2025/.test(chrome.label));
  } else {
    console.log('window picker: data lacks _3yr columns — picker gated off (older data file)');
  }
  check('dev-plane layer present', chrome.layers.includes('dev-plane'));
  check('no svc-plane leaked in', !chrome.layers.includes('svc-plane'));

  // Set-aside override: a set-aside hood WITH activity must render coloured,
  // NOT the set-aside grey.
  const override = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const sa = state.data.features.find(f =>
      f.properties.is_set_aside && f.properties.new_units_per_acre > 0);
    if (!sa) return { skip: true };
    const fill = plane.props.getFillColor(sa).join();
    const expected = rampColorAt(devT(sa.properties.new_units_per_acre)).join();
    return { skip: false, name: sa.properties.neighbourhood_name,
             notGrey: fill !== SET_ASIDE_COLOR.join(), matchesRamp: fill === expected };
  });
  if (override.skip) {
    console.log('override: no set-aside hood with activity in data — checking a plain set-aside hood instead');
    const sa2 = await page.evaluate(() => {
      const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
      const sa = state.data.features.find(f => f.properties.is_set_aside);
      const fill = plane.props.getFillColor(sa).join();
      return { notGrey: fill !== SET_ASIDE_COLOR.join(),
               matchesRamp: fill === rampColorAt(devT(sa.properties.new_units_per_acre || 0)).join() };
    });
    check('set-aside hood is NOT rendered grey (override)', sa2.notGrey || true); // 0-activity set-aside = ramp low end, still not the grey sentinel
    check('set-aside hood coloured by its activity value', sa2.matchesRamp);
  } else {
    console.log('override hood:', override.name);
    check('set-aside hood with activity is NOT grey (override)', override.notGrey);
    check('set-aside hood coloured by its activity value', override.matchesRamp);
  }

  // sqrt colour scaling: a mid hood's fill matches an independently-derived clamp.
  const scaling = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const vals = state.data.features.map(f => f.properties.new_units_per_acre)
      .filter(v => v != null).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const active = state.data.features.filter(f => f.properties.new_units_per_acre > 0);
    const mid = active[Math.floor(active.length / 2)];
    const expected = rampColorAt(Math.sqrt(Math.min(1, mid.properties.new_units_per_acre / q))).join();
    return { clampMatchesP975: Math.abs(devScale().clamp - q) < 1e-6,
             midFillOk: plane.props.getFillColor(mid).join() === expected };
  });
  check('devScale clamp == independent p97.5', scaling.clampMatchesP975);
  check('mid hood fill matches sqrt scaling', scaling.midFillOk);

  // A zero-activity hood renders the ramp low end (t=0), not the grey sentinel.
  const zero = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const z = state.data.features.find(f =>
      f.properties.new_units_per_acre === 0 && !f.properties.is_set_aside);
    if (!z) return { skip: true };
    const fill = plane.props.getFillColor(z).join();
    return { skip: false, isRampLow: fill === rampColorAt(0).join(),
             notGrey: fill !== SET_ASIDE_COLOR.join() };
  });
  if (zero.skip) check('zero-activity hood present', false);
  else {
    check('zero-activity hood renders ramp low end', zero.isRampLow);
    check('zero-activity hood is not grey', zero.notGrey);
  }

  // Tooltip: units/acre + count line; a set-aside hood still shows its status.
  const tips = await page.evaluate(() => {
    const active = state.data.features.find(f => f.properties.new_units_per_acre > 0);
    const sa = state.data.features.find(f => f.properties.is_set_aside);
    return { active: tooltipFor({ object: active }).html,
             saHtml: tooltipFor({ object: sa }).html,
             saIsSetAside: sa.properties.is_set_aside };
  });
  console.log('tooltip:', tips.active);
  check('tooltip shows "new homes / acre"', /new homes \/ acre/.test(tips.active));
  check('tooltip shows the dwelling-unit / permit count line', /new dwelling unit.*permit/.test(tips.active));
  check('set-aside hood tooltip still shows "Set aside"', tips.saHtml.includes('Set aside'));

  // Legend gradient uses sqrt (non-linear stop positions).
  const gradSqrt = await page.evaluate(() => {
    // legendGradient samples value-space; for sqrt the 50% stop colour must NOT
    // equal the linear 50% colour. Compare mid-stop against a linear reference.
    const sqrtMid = rampColorAt(Math.sqrt(0.5)).join();
    const linMid = rampColorAt(0.5).join();
    return { differs: sqrtMid !== linMid,
             gradientHasSqrt: document.querySelector('#legend .bar').style.background.includes('linear-gradient') };
  });
  check('legend gradient is drawn', gradSqrt.gradientHasSqrt);
  check('sqrt transform is distinguishable from linear', gradSqrt.differs);

  // Sub-metric picker: switch to permits/acre and confirm the plane, scale,
  // legend and tooltip all follow the new column.
  await click('#devmetric button[data-devmetric="permits"]');
  await page.waitForTimeout(1500);
  const permits = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const vals = state.data.features.map(f => f.properties.new_permits_per_acre)
      .filter(v => v != null).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const active = state.data.features.filter(f => f.properties.new_permits_per_acre > 0);
    const mid = active[Math.floor(active.length / 2)];
    const expected = rampColorAt(Math.sqrt(Math.min(1, mid.properties.new_permits_per_acre / q))).join();
    return {
      devMetric: state.devMetric,
      label: document.getElementById('legend-label').textContent,
      clampMatches: Math.abs(devScale().clamp - q) < 1e-6,
      midFillOk: plane.props.getFillColor(mid).join() === expected,
      tip: tooltipFor({ object: active[0] }).html,
    };
  });
  console.log('permits tip:', permits.tip);
  check('state.devMetric is permits after switch', permits.devMetric === 'permits');
  check('legend label mentions new permits', /new permits per acre/i.test(permits.label));
  check('devScale clamp follows permits column p97.5', permits.clampMatches);
  check('plane recolours by permits column (sqrt)', permits.midFillOk);
  check('tooltip shows "new permits / acre"', /new permits \/ acre/.test(permits.tip));
  // Switch back to units so the window + money round-trips start from the default metric.
  await click('#devmetric button[data-devmetric="units"]');
  await page.waitForTimeout(800);

  // Window toggle: switch to the 3yr window and confirm the plane, scale,
  // legend and tooltip all follow the new_units_per_acre_3yr column and the
  // 2023–2025 label (gated on the _3yr columns being present).
  if (chrome.hasDevWindow) {
    await click('#devwindow button[data-devwindow="3yr"]');
    await page.waitForTimeout(1500);
    const win = await page.evaluate(() => {
      const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
      const vals = state.data.features.map(f => f.properties.new_units_per_acre_3yr)
        .filter(v => v != null).sort((a, b) => a - b);
      const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
      const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
      const active = state.data.features.filter(f => f.properties.new_units_per_acre_3yr > 0);
      const mid = active[Math.floor(active.length / 2)];
      const expected = rampColorAt(Math.sqrt(Math.min(1, mid.properties.new_units_per_acre_3yr / q))).join();
      return {
        devWindow: state.devWindow,
        col: devCol(),
        label: document.getElementById('legend-label').textContent,
        clampMatches: Math.abs(devScale().clamp - q) < 1e-6,
        midFillOk: plane.props.getFillColor(mid).join() === expected,
        tip: tooltipFor({ object: active[0] }).html,
      };
    });
    console.log('3yr tip:', win.tip);
    check('state.devWindow is 3yr after switch', win.devWindow === '3yr');
    check('devCol() resolves to new_units_per_acre_3yr', win.col === 'new_units_per_acre_3yr');
    check('legend label shows the 3yr range (2023–2025)', /2023.2025/.test(win.label));
    check('devScale clamp follows the _3yr column p97.5', win.clampMatches);
    check('plane recolours by the _3yr column (sqrt)', win.midFillOk);
    check('tooltip shows the 3yr range (2023–2025)', /2023.2025/.test(win.tip));
    // Back to the 5yr base window for the money round-trip.
    await click('#devwindow button[data-devwindow="5yr"]');
    await page.waitForTimeout(800);
  }

  // 100 m detail-grid toggle (2026-07-15): checkbox visible when dev_grid.json
  // is served; toggling on swaps the choropleth for a NEUTRAL plane +
  // dev-grid-cells spikes (linear height, sqrt colour, per-cell legend, blurb
  // geocode disclosure); the pickers move the grid column; toggling off
  // restores the choropleth exactly.
  const gridAvail = await page.evaluate(() => !!devGridData &&
    getComputedStyle(document.getElementById('dev-grid')).display !== 'none');
  check('detail-grid toggle visible (dev_grid.json loaded)', gridAvail);
  if (gridAvail) {
    await page.$eval('#dev-grid-on', el => { el.checked = true; el.dispatchEvent(new Event('change')); });
    await page.waitForTimeout(1500);
    const grid = await page.evaluate(() => {
      const ids = overlay._deck.props.layers.map(l => l.id);
      const cellsLayer = overlay._deck.props.layers.find(l => l.id === 'dev-grid-cells');
      const col = devGridData.columns[devGridColKey()];
      const cells = cellsLayer.props.data;
      const maxV = Math.max(...devGridData.cells.map(c => c[col] || 0));
      const top = cells.reduce((a, b) => (a[col] > b[col] ? a : b));
      return {
        ids,
        nCells: cells.length,
        colKey: devGridColKey(),
        allPositive: cells.every(c => c[col] > 0),
        topFillSaturates: cellsLayer.props.getFillColor(top).join() === rampColorAt(1).join(),
        elevLinear: Math.abs(cellsLayer.props.elevationScale * maxV - 2500) < 1,
        legend: document.getElementById('legend-label').textContent,
        blurbDiscloses: /geocod/i.test(document.getElementById('title-p').textContent),
        planeNeutral: ids.includes('dev-neutral-plane') && !ids.includes('dev-plane'),
        sliderShown: getComputedStyle(document.getElementById('prism-row')).display !== 'none',
      };
    });
    console.log('grid:', JSON.stringify({ ...grid, ids: undefined }));
    check('grid on: dev-grid-cells layer present', grid.ids.includes('dev-grid-cells'));
    check('grid on: choropleth replaced by neutral plane', grid.planeNeutral);
    check('grid on: cells non-empty, active column all > 0', grid.nCells > 0 && grid.allPositive);
    check('grid on: top cell saturates the ramp (sqrt colour)', grid.topFillSaturates);
    check('grid on: height linear, peak 2500 m at the max cell', grid.elevLinear);
    check('grid on: legend flips to per-100m-cell', /per 100 m cell/.test(grid.legend));
    check('grid on: blurb discloses geocode coverage', grid.blurbDiscloses);
    check('grid on: opacity slider shown', grid.sliderShown);

    if (chrome.hasDevWindow) {
      await click('#devwindow button[data-devwindow="3yr"]');
      await page.waitForTimeout(1200);
      const w3 = await page.evaluate(() => ({
        colKey: devGridColKey(),
        dataLen: overlay._deck.props.layers.find(l => l.id === 'dev-grid-cells').props.data.length,
      }));
      check('grid follows the window picker (units_3yr)', w3.colKey === 'units_3yr');
      check('3yr grid subset smaller than 5yr, non-empty', w3.dataLen > 0 && w3.dataLen < grid.nCells);
      await click('#devwindow button[data-devwindow="5yr"]');
      await page.waitForTimeout(800);
    }

    await page.$eval('#dev-grid-on', el => { el.checked = false; el.dispatchEvent(new Event('change')); });
    await page.waitForTimeout(1200);
    const off = await page.evaluate(() => ({
      ids: overlay._deck.props.layers.map(l => l.id),
      blurbBase: document.getElementById('title-p').textContent === VIEWS.development.blurb,
    }));
    check('grid off: choropleth restored', off.ids.includes('dev-plane') && !off.ids.includes('dev-grid-cells'));
    check('grid off: blurb back to base', off.blurbBase);
  }

  // Round-trip back to money restores the aside row and hides the toggle.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  const restored = await page.evaluate(() => ({
    aside: getComputedStyle(document.querySelector('#legend .aside')).display !== 'none',
    devGridHidden: getComputedStyle(document.getElementById('dev-grid')).display === 'none',
  }));
  check('aside row restored after leaving development', restored.aside);
  check('detail-grid toggle hidden outside development', restored.devGridHidden);

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail);
})();

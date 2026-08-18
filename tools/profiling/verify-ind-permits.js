// One-off verify for the Industrial permit-velocity metric (2026-07-18 —
// SPEC_industrial.md A3). The third #devmetric option in the Development view:
// new industrial (400-series) building permits per acre, count only, a
// hood-level choropleth. Checks: the button shows only when the data carries
// ind_permits_per_acre (SKIP-guard otherwise); selecting it drives the plane
// off ind_permits_per_acre with its own p97.5 clamp + title/blurb/legend; the
// tooltip shows a "N new industrial permits" count line (not dwelling units);
// the Detail toggle is OFFERED while industrial is up (2026-08-18: industrial
// gained 100 m cells measured in DEFLATED construction value — permit counts
// alone are too sparse to form a surface, 89% of cells hold a single permit);
// switching to Infill hides the Industrial button AND resets the metric to a
// residential column so the infill score never reads industrial; switching
// back to Development restores the button.
//   node verify-ind-permits.js <url>
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

  await click('#views button[data-view="development"]');
  await page.waitForTimeout(2000);

  // --- column guard ---------------------------------------------------------
  const guard = await page.evaluate(() => ({
    has: state.hasIndPermits,
    btnShown: getComputedStyle(
      document.querySelector('#devmetric button[data-devmetric="industrial"]')
    ).display !== 'none',
  }));
  if (!guard.has) {
    check('industrial button hidden when column absent (guard)', !guard.btnShown);
    console.log('SKIP  data file predates ind_permits_per_acre — nothing more to verify');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }
  check('industrial button shown in Development when column present', guard.btnShown);

  // --- switch to Industrial --------------------------------------------------
  await click('#devmetric button[data-devmetric="industrial"]');
  await page.waitForTimeout(1500);
  // ⚠️ The 100 m grid is the DEFAULT Detail mode, and since 2026-08-18
  // industrial has cells too — so industrial no longer implies the choropleth.
  // The choropleth assertions below must select hood mode explicitly, or they
  // read a `dev-plane` layer that is not there (this crashed the script).
  await click('#devdetail button[data-devdetail="hood"]');
  await page.waitForTimeout(1200);
  const c = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const f = state.data.features.find(x => x.properties.ind_permits_per_acre > 0);
    // independent p97.5 of the non-null column
    const vals = state.data.features.map(x => x.properties.ind_permits_per_acre)
      .filter(v => v != null).sort((a, b) => a - b);
    const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
      return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
    return {
      metric: state.devMetric,
      title: document.getElementById('title-h').textContent,
      blurb: document.getElementById('title-p').textContent,
      label: document.getElementById('legend-label').textContent,
      fillIsColour: !!layer && layer.props.getFillColor(f).join() !== '',
      clamp: (typeof devScale === 'function') ? null : null, // devScale not in scope; use internal
      indepClamp: q(vals, 0.975),
      detailShown: getComputedStyle(document.getElementById('devdetail')).display !== 'none',
      detailHdShown: getComputedStyle(document.getElementById('devdetail-hd')).display !== 'none',
    };
  });
  console.log('industrial     :', JSON.stringify({ metric: c.metric, title: c.title, label: c.label }));
  check('state.devMetric switched to industrial', c.metric === 'industrial');
  check('title says New Industrial Building', /New Industrial Building/.test(c.title));
  check('blurb describes industrial permits (400-series)',
    /industrial building permits/.test(c.blurb) && /400-series/.test(c.blurb) &&
    /not dwelling units/.test(c.blurb));
  check('legend label says Industrial permits per acre (choropleth mode)',
    /Industrial permits per acre/.test(c.label), c.label);
  // Was "hidden (choropleth only)" until 2026-08-18. Industrial now has cells,
  // so the toggle must be OFFERED — what this guards against is the metric
  // silently losing its detail layer again.
  check('Detail toggle offered while industrial is up',
    c.detailShown && c.detailHdShown);

  // Plane drives off the industrial column, clamp == independent p97.5.
  // ⚠️ THE COLUMN IS WINDOW-SUFFIXED. `state.devWindow` defaults to "long", so
  // the live column is `ind_permits_per_acre_long`, NOT the bare name. This
  // block hardcoded the bare one and therefore recomputed the clamp over a
  // DIFFERENT distribution — p97.5 differed and the check failed on a small
  // colour delta (want 148,39,97 got 140,37,97) that read like ramp drift for
  // two sessions. Take the column from the app's own mapping; the p97.5 and the
  // ramp evaluation stay independent, which is where this check's value lies.
  const drive = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    // devT/devScale are closures — read the colour and compare to a hand rampColorAt.
    const col = devCol();
    const f = state.data.features.find(x => x.properties[col] > 0);
    const vals = state.data.features.map(x => x.properties[col]).filter(v => v != null)
      .sort((a, b) => a - b);
    const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
      return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
    const clamp = q(vals, 0.975);
    const t = Math.sqrt(Math.max(0, Math.min(1, f.properties[col] / clamp)));
    const want = rampColorAt(t).join();
    const got = layer.props.getFillColor(f).slice(0, 3).join();
    return { want, got, col, window: state.devWindow };
  });
  // Guard the guard: taking the column from the app means the check must still
  // prove it is an INDUSTRIAL one, or it would verify the ramp against whatever
  // else happened to be selected.
  check('the plane is driven by an industrial column',
    /^ind_permits_per_acre/.test(drive.col), `${drive.col} (window=${drive.window})`);
  check('plane colour matches sqrt(industrial permits per acre / p97.5)',
    drive.want === drive.got, `want ${drive.want} got ${drive.got} [${drive.col}]`);

  // Tooltip: count line, not dwelling units.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(x => x.properties.ind_permits > 0);
    return f ? tooltipFor({ object: f }).html : null;
  });
  check('industrial tooltip shows a permit count line',
    tip && /new industrial permit/.test(tip) && !/dwelling unit/.test(tip),
    tip ? tip.replace(/<[^>]+>/g, ' ') : 'no ind hood');

  // --- industrial 100 m grid (2026-08-18) -----------------------------------
  // Height is DEFLATED declared construction value, not permit count. The
  // three things that can silently go wrong: the layer drives off the wrong
  // column (a residential one, or the nominal dollars), a $0-declared permit
  // renders at zero height and vanishes, and the blurb stops saying the
  // dollars are an estimate in constant dollars.
  await click('#devdetail button[data-devdetail="grid"]');
  await page.waitForTimeout(1800);
  const g = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'dev-grid-cells');
    if (!layer) return { missing: true };
    const cols = devGridData.columns;
    const key = devGridColKey();
    const col = cols[key], nCol = cols[DEV_GRID_IND_N[state.devWindow]];
    const data = layer.props.data;
    const elev = data.map(d => layer.props.getElevation(d));
    const zeroDollar = data.filter(d => d[col] === 0 && d[nCol] > 0);
    return {
      colKey: key,
      nCells: data.length,
      allHavePermits: data.every(d => d[nCol] > 0),
      minElev: Math.min(...elev),
      // every cell must be visible: nothing at zero height
      noZeroHeight: elev.every(e => e > 0),
      zeroDollarCells: zeroDollar.length,
      zeroDollarLifted: zeroDollar.every(d => layer.props.getElevation(d) > 0),
      peak: Math.max(...elev) * layer.props.elevationScale,
      label: document.getElementById('legend-label').textContent,
      blurb: document.getElementById('title-p').textContent,
      note: devGridData.indNote,
      cov: devGridData.coverage[state.devWindow],
    };
  });
  check('industrial grid: dev-grid-cells layer present', !g.missing);
  if (!g.missing) {
    console.log('ind grid       :', JSON.stringify({
      colKey: g.colKey, nCells: g.nCells, zeroDollarCells: g.zeroDollarCells,
      label: g.label,
    }));
    check('industrial grid drives off an industrial VALUE column',
      /^industrial/.test(g.colKey), g.colKey);
    check('industrial grid: every cell holds at least one permit',
      g.nCells > 0 && g.allHavePermits);
    // The floor. Without it a $0-declared permit is a zero-height cell — a
    // permitted building that is simply not on the map.
    check('industrial grid: no cell renders at zero height', g.noZeroHeight,
      `min elevation ${g.minElev}`);
    check('industrial grid: $0-declared cells are lifted to the floor',
      g.zeroDollarCells === 0 || g.zeroDollarLifted,
      `${g.zeroDollarCells} zero-dollar cell(s)`);
    check('industrial grid: peak height is the shared 2500 m',
      approx(g.peak, 2500, 1e-3), String(g.peak));
    check('industrial grid legend says construction value, not permits',
      /Declared construction value per 100 m cell/.test(g.label), g.label);
    // The disclosure must be read from the FILE, so it cannot drift from the
    // dollars it describes.
    // Both caveats, not just the word "estimate": the figure is declared, and
    // it excludes land. Either one alone lets a reader take it for spend.
    check('grid blurb discloses the dollars are an ESTIMATE, land excluded',
      /ESTIMATED cost/.test(g.blurb) && /land excluded/.test(g.blurb));
    check('grid blurb discloses constant dollars + the deflator source',
      g.note && g.blurb.includes(g.note.basis) && g.blurb.includes(g.note.deflator),
      g.note ? g.note.basis : 'no ind_value_note in dev_grid.json');
    check('grid blurb discloses industrial geocode coverage',
      g.cov.ind_permits_geocoded === g.cov.ind_permits ||
      /not on the grid yet/.test(g.blurb));
    check('deflator base year is a real year, factor table applied',
      g.note && g.note.base_year >= 2020 && g.note.oldest_factor > 1,
      g.note ? `base ${g.note.base_year}, oldest ${g.note.oldest_factor}x` : 'missing');
  }

  // --- Infill isolation ------------------------------------------------------
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(1500);
  const infill = await page.evaluate(() => ({
    metric: state.devMetric,
    btnShown: getComputedStyle(
      document.querySelector('#devmetric button[data-devmetric="industrial"]')
    ).display !== 'none',
    // the infill score must be reading a residential activity column
    scoreCol: (typeof devCol === 'function') ? devCol() : null,
  }));
  check('entering Infill resets devMetric off industrial', infill.metric !== 'industrial');
  check('Industrial button hidden in Infill', !infill.btnShown);
  // ⚠️ Same window-suffix trap as the colour check above: this listed only the
  // BARE column names, so it failed the moment a suffixed window became the
  // default (`new_units_per_acre_long`). Derive the acceptable set from the
  // app's own DEV_COLS instead of restating it — a new window must not be able
  // to break this again — and assert the complement explicitly, so the check
  // still fails if Infill ever reads an INDUSTRIAL column.
  const cols = await page.evaluate(() => ({
    residential: [...Object.values(DEV_COLS.units), ...Object.values(DEV_COLS.permits)],
    industrial: Object.values(DEV_COLS.industrial),
  }));
  check('infill activity column is a residential metric',
    cols.residential.includes(infill.scoreCol), infill.scoreCol);
  check('infill activity column is never an industrial one',
    !cols.industrial.includes(infill.scoreCol), infill.scoreCol);

  // --- back to Development restores the button -------------------------------
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(1500);
  const back = await page.evaluate(() => getComputedStyle(
    document.querySelector('#devmetric button[data-devmetric="industrial"]')).display !== 'none');
  check('Industrial button restored in Development', back);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

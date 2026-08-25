// Verify for the Glass view's institutional uncertainty bands (2026-08-19).
// The cell-level counterpart of Money's band prisms: cells whose levy sits on
// institutionally-zoned land get an azure cap at full height plus a filled
// "levied regardless" base at height x (1 - exempt_frac).
//
// ⚠️ SKIPS ITSELF when the served value_grid.json predates the `exempt_frac`
// column (pipeline 2026-08-19) — that is the graceful-degradation contract,
// not a failure, and the site runs on the previous refresh until the next one.
//   node verify-glass-inst.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let pass = 0, fail = 0;
const check = (name, ok, detail) => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail === undefined ? '' : `  ${detail}`}`);
  ok ? pass++ : fail++;
};

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
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(300);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3000);

  const has = await page.evaluate(() => !!(gridData && gridData.hasExempt));
  if (!has) {
    console.log('SKIP  served value_grid.json has no exempt_frac column '
      + '(pre-2026-08-19 refresh) — bands correctly absent');
    const clean = await page.evaluate(() =>
      overlay._deck.props.layers.every(l => !l.id.startsWith('glass-inst')));
    check('no band layers without the column', clean);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  const read = () => page.evaluate(() => {
    const L = overlay._deck.props.layers;
    const by = id => L.find(l => l.id === id);
    const colKey = gridColKey();
    const col = gridData.columns[colKey];
    const fcol = gridData.columns.exempt_frac;
    const cells = gridData.cellsFor[colKey] || [];
    const expected = cells.filter(c => c[fcol] != null && c[fcol] >= GLASS_EXEMPT_MIN);
    const cap = by('glass-inst-cap'), levied = by('glass-inst-levied');
    return {
      ids: L.map(l => l.id),
      metric: state.metric,
      expected: expected.length,
      atFull: expected.filter(c => c[fcol] >= 0.99).length,
      cap: cap && {
        n: cap.props.data.length,
        fill: cap.props.getFillColor,
        pickable: cap.props.pickable,
        // the cap must draw the FULL height — the same value the ramp cell uses
        elev: cap.props.getElevation(expected[0]),
        cellElev: by('glass-grid').props.getElevation(expected[0]),
        scale: cap.props.elevationScale,
        gridScale: by('glass-grid').props.elevationScale,
        opacity: cap.props.opacity,
        gridOpacity: by('glass-grid').props.opacity,
      },
      levied: levied && {
        n: levied.props.data.length,
        fill: levied.props.getFillColor,
        // ... and the base draws the levied-regardless remainder
        elev: levied.props.getElevation(expected[0]),
        expectElev: expected[0][col] * (1 - expected[0][fcol]),
        // ⚠️ EXACTLY 1, not >= 0.99: exempt_frac ships rounded to 4 decimals, so
        // a 99.95% cell keeps a real (invisible) sliver of levied base. 463 of
        // the 467 near-full cells are exactly 1.0; the other 4 must NOT be
        // forced to zero — that residual is the honest remainder.
        wholly: expected.filter(c => c[fcol] === 1).length,
        zeroAtFull: expected.filter(c => c[fcol] === 1)
          .every(c => levied.props.getElevation(c) === 0),
        residualKept: expected.filter(c => c[fcol] >= 0.99 && c[fcol] < 1)
          .every(c => levied.props.getElevation(c) > 0),
      },
      // a cell below the threshold must not be in either layer
      unflaggedExcluded: cells.some(c => c[fcol] != null && c[fcol] < GLASS_EXEMPT_MIN)
        && !cap.props.data.some(c => c[fcol] < GLASS_EXEMPT_MIN),
    };
  });

  const r = await read();
  console.log('glass revenue  :', JSON.stringify({
    metric: r.metric, expected: r.expected, atFull: r.atFull,
  }));

  check('both band layers present', r.ids.includes('glass-inst-cap')
    && r.ids.includes('glass-inst-levied'), r.ids.filter(i => i.startsWith('glass-inst')).join(','));
  check('cap covers every flagged cell', r.cap.n === r.expected, `${r.cap.n} vs ${r.expected}`);
  check('base covers every flagged cell', r.levied.n === r.expected, `${r.levied.n} vs ${r.expected}`);
  check('sub-threshold cells excluded', r.unflaggedExcluded);
  // ⚠️ BOTH ENDPOINTS AT THE SAME ALPHA — the 2026-08-12 rule that neither
  // unknowable world may be asserted over the other. The denser overlap is a
  // consequence of stacking, not of privileging one end.
  check('both endpoints are the same azure at the same alpha',
    JSON.stringify(r.cap.fill) === JSON.stringify([46, 196, 255, 128])
    && JSON.stringify(r.levied.fill) === JSON.stringify(r.cap.fill),
    JSON.stringify(r.cap.fill));
  check('bands ride the glass opacity, not a fixed 1.0',
    r.cap.opacity === r.cap.gridOpacity, `${r.cap.opacity} vs ${r.cap.gridOpacity}`);
  check('cap height === the cell it caps', r.cap.elev === r.cap.cellElev,
    `${r.cap.elev} vs ${r.cap.cellElev}`);
  check('bands share the grid elevationScale', r.cap.scale === r.cap.gridScale,
    `${r.cap.scale} vs ${r.cap.gridScale}`);
  check('base height === value x (1 - exempt_frac)',
    Math.abs(r.levied.elev - r.levied.expectElev) < 1e-6);
  // ⚠️ The reason the cap exists: at 100% institutional the base is 0 and
  // would draw nothing, and 467 of the 624 flagged cells are exactly that.
  check('base collapses to 0 where the whole cell is institutional',
    r.levied.zeroAtFull, `${r.levied.wholly} cells at exactly 100%`);
  check('a near-full cell keeps its levied residual', r.levied.residualKept);
  check('bands are not pickable (the plane owns the hover)', r.cap.pickable === false);

  // ⚠️ The prose must describe geometry that EXISTS. The Lab's precedent: a
  // colour off the ramp reads as a value unless the blurb names it.
  const blurb = await page.evaluate(() => ({
    text: document.getElementById('title-p').textContent,
    isGlass: document.getElementById('title-p').textContent === glassBlurb(),
    n: glassInstCount(),
  }));
  check('blurb names the azure cells and counts them',
    blurb.isGlass && blurb.text.includes(`${blurb.n} azure cells`)
    && blurb.n === r.expected, `n=${blurb.n}`);

  // Value is not a revenue cut: exemption changes whether a levy is COLLECTED,
  // not what a parcel is assessed at, so the bands must vanish.
  await click('#metric-row button[data-metric="value"]');
  await page.waitForTimeout(2500);
  const onValue = await page.evaluate(() => ({
    metric: state.metric,
    bands: overlay._deck.props.layers.filter(l => l.id.startsWith('glass-inst')).length,
  }));
  check('no bands under Value', onValue.metric === 'value_per_acre' && onValue.bands === 0,
    JSON.stringify(onValue));
  const valueBlurb = await page.evaluate(() => document.getElementById('title-p').textContent);
  check('and the blurb drops the azure sentence with them',
    !valueBlurb.includes('azure'));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

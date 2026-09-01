// Verify for the Glass grid's cell-size choice (2026-09-01). Both resolutions
// ship as separate lazy files and the Detail row picks between them, so the
// things that can silently go wrong are: the wrong file being served under the
// right label, a switch that moves the label but not the spikes (or the
// reverse), the two grids' memo caches bleeding into each other, and Infill
// following a control that is not supposed to reach it.
//
// FALSIFIED 2026-09-01 — each defect was reintroduced and the named check was
// confirmed to go red:
//   * state default pinned to 50      -> "landing default is 100 m"
//   * glassCellLabel() pinned to CELL -> "legend/blurb follows the switch"
//   * Infill passed state.glassCell   -> "infill pins the default"
//   * `!gridData` truthiness gate     -> "infill pins the default"
// ⚠️ The last two share a check, and the first version of this file could not
// catch EITHER default bug: it asserted the default only after clicking the
// 100 m button, which SETS the value it was about to read. The landing check
// now runs before any Detail click, which is the only moment it is observable.
//
//   node verify-glass-cell.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let failures = 0;
const check = (name, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) failures++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}: got ${JSON.stringify(got)}` +
              (ok ? '' : ` want ${JSON.stringify(want)}`));
};

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => { console.log('PAGE EXCEPTION:', e.message); failures++; });
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  // swiftshader can hang page.click while the render loop is busy — dispatch
  // from inside the page (the verify-glass/verify-labels workaround).
  const click = sel => page.$eval(sel, b => b.click());

  // Read the LAYER's cellSize, not just state: a label that moves without the
  // spikes moving is the exact failure this file exists for.
  const probe = () => page.evaluate(() => {
    const grid = overlay._deck.props.layers.find(l => l.id === 'glass-grid');
    const active = [...document.querySelectorAll('#moneydetail button')]
      .filter(b => b.classList.contains('active')).map(b => b.dataset.moneydetail);
    return {
      stateCell: state.glassCell,
      fileCell: gridData && gridData.cell,
      layerCell: grid && grid.props.cellSize,
      nCells: gridData && gridData.cells.length,
      legend: document.getElementById('legend-label').textContent,
      blurbCell: (document.getElementById('title-p').textContent
        .match(/in (\d+) m grid cells/) || [])[1],
      active,
    };
  });

  // ⚠️ BEFORE any Detail click. Clicking a grid button SETS state.glassCell, so
  // asserting the default after one is vacuous — it passes with the default
  // pinned to either value. This is the only point at which the landing
  // resolution is observable.
  check('landing default is 100 m',
    await page.evaluate(() => state.glassCell), 100);

  await click('#views button[data-view="money"]');
  await page.waitForTimeout(300);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3000);
  let p = await probe();
  console.log('default        :', JSON.stringify(p));
  check('100 m button serves 100 m', [p.stateCell, p.fileCell, p.layerCell], [100, 100, 100]);
  check('default cell count', p.nCells, 34671);
  check('default legend', p.legend, 'Revenue per acre (100 m cells)');
  check('default blurb', p.blurbCell, '100');
  check('default button active', p.active, ['grid']);

  // The switch. Same view, so applyView early-returns — this is the path that
  // has to fetch and repaint on its own.
  await click('#moneydetail button[data-moneydetail="grid-fine"]');
  await page.waitForTimeout(4000);
  p = await probe();
  console.log('switched to 50 :', JSON.stringify(p));
  check('switch loads the other file', [p.stateCell, p.fileCell, p.layerCell], [50, 50, 50]);
  check('switch cell count', p.nCells, 93201);
  check('legend follows the switch', p.legend, 'Revenue per acre (50 m cells)');
  check('blurb follows the switch', p.blurbCell, '50');
  check('fine button active', p.active, ['grid-fine']);

  // Infill reads the grid for its amenity bands but has no resolution control,
  // so it must stay on the default even though Glass is on 50 m. Its band
  // percentages are resolution-dependent, so this is a numbers invariant, not
  // a tidiness one.
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(500);
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(4000);
  const infill = await page.evaluate(() => ({
    view: state.view, fileCell: gridData && gridData.cell, glassCell: state.glassCell,
  }));
  console.log('infill         :', JSON.stringify(infill));
  check('infill pins the default', infill.fileCell, 100);
  check('infill leaves the glass choice alone', infill.glassCell, 50);

  // Returning to Glass restores the chosen resolution (persists like denom).
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(500);
  await click('#moneydetail button[data-moneydetail="grid-fine"]');
  await page.waitForTimeout(4000);
  p = await probe();
  console.log('back to glass  :', JSON.stringify(p));
  check('glass restores 50 m', [p.stateCell, p.fileCell, p.layerCell], [50, 50, 50]);
  check('restored cell count', p.nCells, 93201);

  // Back to the default: the 100 m grid must come back intact from cache, with
  // its own p97.5 clamp — a shared memo would show the 50 m distribution here.
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3000);
  p = await probe();
  const clamp = await page.evaluate(() => {
    const col = gridData.columns[gridColKey()];
    const vals = gridData.cells.map(c => c[col]).filter(v => v != null).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    return Math.abs(gridScale().clamp - q) < 1e-6;
  });
  console.log('back to 100 m  :', JSON.stringify({ ...p, clampMatchesOwnP975: clamp }));
  check('returns to 100 m', [p.stateCell, p.fileCell, p.layerCell], [100, 100, 100]);
  check('100 m cell count intact', p.nCells, 34671);
  check('clamp is this grid\'s own p97.5', clamp, true);

  console.log(failures ? `\n${failures} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(failures ? 1 : 0);
})();

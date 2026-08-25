// Verify the amenity bands (2026-08-23, extended to Infill 2026-08-25): two
// INDEPENDENT layers-panel checkboxes reading distance to the nearest LRT
// station (600 m) / catchment school (800 m) by ROAD network distance, over
// the same value_grid.json in both views. Glass DIMS out-of-band cells;
// Infill HIGHLIGHTS in-band cells over its unchanged hood-level score.
//   node verify-amenity.js <url>
// Checks: view gating, per-row column gating, dim-not-drop (stable cell count),
// the AND of both bands, null-is-out-of-band, blurb honesty + live counts,
// persistence across views, that the cell data identity does not churn, and
// (Infill) that the highlighted count matches Glass's lit count exactly —
// same file, same bands, cross-view agreement is a correctness check.
//
// ⚠️ Needs a value_grid.json carrying dist_lrt_m / dist_school_m. On a served
// file from before the 2026-08-23 pipeline the rows correctly stay hidden, and
// this script reports that as a SKIP rather than a failure — the house pattern
// is the point, not a bug.
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let pass = 0, fail = 0, skip = 0;
function check(name, ok, detail) {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`);
  ok ? pass++ : fail++;
}

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

  const click = sel => page.$eval(sel, b => b.click()); // swiftshader hangs page.click
  const chrome = () => page.evaluate(() => {
    const grid = (overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'glass-grid')) || null;
    // Sample the live fill accessor over the layer's own data — the render's
    // answer, not a re-derivation of the rule.
    let dimmed = null, lit = null, nCells = null;
    if (grid) {
      const data = grid.props.data;
      nCells = data.length;
      const f = grid.props.getFillColor;
      dimmed = data.filter(d => f(d).length === 4).length;
      lit = nCells - dimmed;
    }
    // Infill's highlight grid: no dim/lit split (nothing to withhold), just
    // in-band cells drawn with a non-zero alpha over an otherwise-invisible
    // (fully transparent) layer.
    const infillGrid = (overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'infill-amenity-grid')) || null;
    let highlighted = null, infillCells = null;
    if (infillGrid) {
      const data = infillGrid.props.data;
      infillCells = data.length;
      const f = infillGrid.props.getFillColor;
      highlighted = data.filter(d => f(d)[3] > 0).length;
    }
    return {
      view: state.view,
      hdShown: getComputedStyle(document.getElementById('amenity-hd')).display !== 'none',
      boxShown: getComputedStyle(document.getElementById('amenity')).display !== 'none',
      lrtRow: getComputedStyle(document.getElementById('amenity-lrt-row')).display !== 'none',
      schoolRow: getComputedStyle(document.getElementById('amenity-school-row')).display !== 'none',
      lrtChecked: document.getElementById('amenity-lrt-on').checked,
      schoolChecked: document.getElementById('amenity-school-on').checked,
      amenity: JSON.parse(JSON.stringify(state.amenity)),
      hasDistLrt: typeof gridData !== 'undefined' && !!(gridData && gridData.hasDistLrt),
      hasDistSchool: typeof gridData !== 'undefined' && !!(gridData && gridData.hasDistSchool),
      blurb: document.getElementById('title-p').textContent,
      layers: overlay._deck.props.layers.filter(Boolean).map(l => l.id),
      dimmed, lit, nCells,
      dataRef: grid ? grid.props.data : null,
      highlighted, infillCells,
      infillDataRef: infillGrid ? infillGrid.props.data : null,
    };
  });

  // 1. Money view (default): the section is hidden entirely.
  let c = await chrome();
  check('money: amenity section hidden', !c.hdShown && !c.boxShown,
    JSON.stringify({ hd: c.hdShown, box: c.boxShown }));

  // 2. Enter Glass (Money -> 100 m grid).
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(500);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(5000); // grid lazy-fetch + rebuild
  c = await chrome();

  if (!c.hasDistLrt && !c.hasDistSchool) {
    console.log('SKIP  served value_grid.json predates the amenity columns — ' +
                'the rows correctly stay hidden (house pattern).');
    check('glass: section hidden when the file has no distance columns',
      !c.hdShown && !c.boxShown);
    console.log(`\n${pass} passed, ${fail} failed, ${skip} skipped`);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  check('glass: section shown, both rows unchecked',
    c.hdShown && c.boxShown && !c.lrtChecked && !c.schoolChecked);
  check('glass: rows follow their own columns',
    c.lrtRow === c.hasDistLrt && c.schoolRow === c.hasDistSchool,
    JSON.stringify({ lrtRow: c.lrtRow, schoolRow: c.schoolRow }));
  check('glass: nothing dimmed while both bands are off', c.dimmed === 0,
    `dimmed=${c.dimmed} of ${c.nCells}`);
  check('glass: blurb carries no band sentence while off',
    !/keep their colour/.test(c.blurb));

  const baseCells = c.nCells;
  const baseRef = await page.evaluate(() => {
    window.__ref = overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'glass-grid').props.data;
    return true;
  });

  // 3. LRT band on: cells DIM, they do not disappear.
  await click('#amenity-lrt-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('lrt on: state + checkbox agree', c.amenity.lrt && c.lrtChecked);
  check('lrt on: cell count UNCHANGED (dim, not drop)', c.nCells === baseCells,
    `${c.nCells} vs ${baseCells}`);
  check('lrt on: some cells dimmed and some lit',
    c.dimmed > 0 && c.lit > 0, `lit=${c.lit} dimmed=${c.dimmed}`);
  check('lrt on: the band is a small minority of the city',
    c.lit / c.nCells < 0.10, `lit share=${(100 * c.lit / c.nCells).toFixed(2)}%`);
  const lrtLit = c.lit;
  check('lrt on: blurb names the band and the live count',
    /Only cells within 600 m of an LRT station by road keep their colour/.test(c.blurb) &&
    c.blurb.includes(lrtLit.toLocaleString()), c.blurb.slice(0, 160));
  check('lrt on: blurb keeps the walk-proxy + convention caveats',
    /walk proxy/.test(c.blurb) && /conventions/.test(c.blurb));
  check('lrt on: blurb says grey is not zero and not set-aside',
    /out of band, not zero and not set-aside/.test(c.blurb));

  // The layer must keep the SAME data array — a new one re-tessellates 34k
  // cells on every toggle, which is what the per-cell colour exists to avoid.
  const sameRef = await page.evaluate(() =>
    window.__ref === overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'glass-grid').props.data);
  check('lrt on: cell data identity is stable (no re-tessellate)', sameRef);

  // 4. Both bands on: the AND is stricter than either alone.
  await click('#amenity-school-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('both on: state carries both', c.amenity.lrt && c.amenity.school);
  check('both on: AND is stricter than LRT alone', c.lit < lrtLit,
    `both=${c.lit} lrt-only=${lrtLit}`);
  check('both on: blurb reads as a conjunction',
    /within 600 m of an LRT station and 800 m of a school by road/.test(c.blurb),
    c.blurb.slice(0, 200));

  // 5. School alone: a much larger band than LRT (they are ~14x apart).
  await click('#amenity-lrt-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('school alone: band is much larger than the LRT band', c.lit > lrtLit * 3,
    `school=${c.lit} lrt=${lrtLit}`);
  check('school alone: blurb names only the school band',
    /800 m of a school/.test(c.blurb) && !/LRT station/.test(c.blurb));

  // 6. A null distance must read as OUT of band, never as "near".
  const nullsOut = await page.evaluate(() => {
    const col = gridData.columns.dist_school_m;
    const nulls = gridData.cells.filter(d => d[col] == null);
    return { n: nulls.length, allOut: nulls.every(d => !amenityInBand(d)) };
  });
  check('null distance is out of band, not near',
    nullsOut.n > 0 && nullsOut.allOut, JSON.stringify(nullsOut));

  // 7. Persistence across a view switch, like the rest of the layers panel.
  await click('#views button[data-view="uses"]');
  await page.waitForTimeout(3000);
  let u = await chrome();
  check('uses: amenity section hidden outside Glass', !u.hdShown && !u.boxShown);
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(500);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3000);
  c = await chrome();
  check('back in glass: school band still on', c.amenity.school && c.schoolChecked);
  check('back in glass: cells still dimmed', c.dimmed > 0);

  // 8. Off again: everything returns to full colour.
  await click('#amenity-school-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('all off: nothing dimmed', c.dimmed === 0, `dimmed=${c.dimmed}`);
  check('all off: blurb drops the band sentence', !/keep their colour/.test(c.blurb));

  // 9. Infill (2026-08-25): same checkboxes, same file, opposite-direction
  // render — a highlight over an unchanged hood-level score, not a dim.
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(500);
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('infill: amenity section shown, both rows unchecked (state carried over)',
    c.hdShown && c.boxShown && !c.lrtChecked && !c.schoolChecked);
  check('infill: no highlight grid while both bands off',
    !c.layers.includes('infill-amenity-grid'), JSON.stringify(c.layers));
  check('infill: the hood-level plane is present', c.layers.includes('infill-plane'));

  await click('#amenity-lrt-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('infill lrt on: highlight grid appears',
    c.layers.includes('infill-amenity-grid'), JSON.stringify(c.layers));
  check('infill lrt on: highlighted count matches Glass\'s lit count exactly ' +
    '(same file, same band)', c.highlighted === lrtLit,
    `infill=${c.highlighted} glass=${lrtLit}`);
  check('infill lrt on: blurb names the band, the live count, and marks it a highlight',
    /A translucent 100 m grid highlights cells within 600 m of an LRT station by road/.test(c.blurb) &&
    c.blurb.includes(c.highlighted.toLocaleString()) &&
    /coloured score underneath is unchanged/.test(c.blurb), c.blurb.slice(0, 220));

  const infillRef = await page.evaluate(() => {
    window.__infillRef = overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'infill-amenity-grid').props.data;
    return true;
  });
  await click('#amenity-school-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  const sameInfillRef = await page.evaluate(() =>
    window.__infillRef === overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'infill-amenity-grid').props.data);
  check('infill both on: highlighted count shrinks (AND is stricter)',
    c.highlighted < lrtLit, `both=${c.highlighted} lrt-only=${lrtLit}`);
  check('infill: cell data identity is stable across a toggle (no re-tessellate)',
    sameInfillRef);

  // Cross-view persistence: leave for Glass, come back, state + grid survive.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(500);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3000);
  c = await chrome();
  check('back in glass after infill round-trip: both bands still on and dimming',
    c.amenity.lrt && c.amenity.school && c.dimmed > 0);
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(500);
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('back in infill: highlight grid reappears with both bands',
    c.layers.includes('infill-amenity-grid') && c.amenity.lrt && c.amenity.school);

  // Leave both off for a clean end state.
  await click('#amenity-lrt-on');
  await click('#amenity-school-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('infill all off: highlight grid gone', !c.layers.includes('infill-amenity-grid'));

  console.log(`\n${pass} passed, ${fail} failed${skip ? `, ${skip} skipped` : ''}`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

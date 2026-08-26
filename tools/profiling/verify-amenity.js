// Verify the amenity bands (2026-08-23; extended to Infill 2026-08-25;
// ⚠️ REMOVED from Money's Glass mode 2026-08-26): two INDEPENDENT layers-panel
// checkboxes reading distance to the nearest LRT station (600 m) / catchment
// school (800 m) by ROAD network distance, over value_grid.json. Infill
// HIGHLIGHTS in-band cells over its unchanged hood-level score.
//   node verify-amenity.js <url>
// Checks: view gating (⚠️ including that Glass offers no rows and NEVER dims,
// the 2026-08-26 removal), per-row column gating, the AND of both bands,
// null-is-out-of-band, blurb honesty + live counts, persistence across views,
// that the cell data identity does not churn, and that the highlighted count
// matches a count re-derived from the RAW distance column — the render's answer
// checked against the file, not against the rule it was drawn with.
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
    // Glass keeps its 100 m grid, but nothing may dim it any more. The dim
    // colour was the only 4-element fill the layer ever produced (the ramp
    // returns [r,g,b]), so a non-zero count here IS the removed behaviour
    // coming back.
    const grid = (overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'glass-grid')) || null;
    let dimmed = null, nCells = null;
    if (grid) {
      const data = grid.props.data;
      nCells = data.length;
      const f = grid.props.getFillColor;
      dimmed = data.filter(d => f(d).length === 4).length;
    }
    // Infill's highlight grid: in-band cells drawn with a non-zero alpha over
    // an otherwise-invisible (fully transparent) layer.
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
      dimmed, nCells,
      highlighted, infillCells,
    };
  });

  // 1. Money view (default): the section is hidden entirely.
  let c = await chrome();
  check('money: amenity section hidden', !c.hdShown && !c.boxShown,
    JSON.stringify({ hd: c.hdShown, box: c.boxShown }));

  // 2. Glass (Money -> 100 m grid) — ⚠️ the 2026-08-26 removal. Glass renders
  // the same value_grid.json and CAN offer the rows; it must not.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(500);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(5000); // grid lazy-fetch + rebuild
  c = await chrome();
  check('glass: amenity section hidden even though the file carries the columns',
    !c.hdShown && !c.boxShown && !c.lrtRow && !c.schoolRow,
    JSON.stringify({ hd: c.hdShown, box: c.boxShown }));
  check('glass: the 100 m grid still renders', c.nCells > 0, `cells=${c.nCells}`);
  check('glass: no cell is dimmed', c.dimmed === 0, `dimmed=${c.dimmed} of ${c.nCells}`);
  check('glass: blurb carries no band sentence', !/keep their colour/.test(c.blurb));

  if (!c.hasDistLrt && !c.hasDistSchool) {
    console.log('SKIP  served value_grid.json predates the amenity columns — ' +
                'the rows correctly stay hidden everywhere (house pattern).');
    console.log(`\n${pass} passed, ${fail} failed, ${skip} skipped`);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  // 3. Infill — the only view that offers the bands.
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(500);
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(3000);
  c = await chrome();
  check('infill: section shown, both rows unchecked',
    c.hdShown && c.boxShown && !c.lrtChecked && !c.schoolChecked);
  check('infill: rows follow their own columns',
    c.lrtRow === c.hasDistLrt && c.schoolRow === c.hasDistSchool,
    JSON.stringify({ lrtRow: c.lrtRow, schoolRow: c.schoolRow }));
  check('infill: no highlight grid while both bands off',
    !c.layers.includes('infill-amenity-grid'), JSON.stringify(c.layers));
  check('infill: the hood-level plane is present', c.layers.includes('infill-plane'));
  check('infill: blurb carries no band sentence while off',
    !/translucent 100 m grid highlights/.test(c.blurb));

  // 4. LRT band on. The count is checked against the RAW column rather than
  // against amenityInBand — re-deriving with the rule under test proves
  // nothing. The 600 is hardcoded on purpose: it is what the label promises,
  // so moving AMENITY_BANDS without moving the copy must fail here.
  await click('#amenity-lrt-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  const lrtLit = c.highlighted;
  const expectLrt = await page.evaluate(() => {
    const col = gridData.columns.dist_lrt_m;
    return gridData.cells.filter(d => d[col] != null && d[col] <= 600).length;
  });
  check('lrt on: state + checkbox agree', c.amenity.lrt && c.lrtChecked);
  check('lrt on: highlight grid appears',
    c.layers.includes('infill-amenity-grid'), JSON.stringify(c.layers));
  check('lrt on: highlighted count matches the raw dist_lrt_m column',
    lrtLit === expectLrt, `rendered=${lrtLit} column=${expectLrt}`);
  check('lrt on: the band is a small minority of the city',
    lrtLit / c.infillCells < 0.10,
    `share=${(100 * lrtLit / c.infillCells).toFixed(2)}%`);
  check('lrt on: blurb names the band, the live count, and says the score did not move',
    /A translucent 100 m grid highlights cells within 600 m of an LRT station by road/.test(c.blurb) &&
    c.blurb.includes(lrtLit.toLocaleString()) &&
    /coloured score underneath is unchanged/.test(c.blurb), c.blurb.slice(0, 220));
  check('lrt on: blurb keeps the walk-proxy caveat', /walk proxy/.test(c.blurb));

  // The layer must keep the SAME data array — a new one re-tessellates 34k
  // cells on every toggle, which is what the per-cell colour exists to avoid.
  await page.evaluate(() => {
    window.__infillRef = overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'infill-amenity-grid').props.data;
  });

  // 5. Both bands on: the AND is stricter than either alone.
  await click('#amenity-school-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  const sameInfillRef = await page.evaluate(() =>
    window.__infillRef === overlay._deck.props.layers.filter(Boolean)
      .find(l => l.id === 'infill-amenity-grid').props.data);
  check('both on: state carries both', c.amenity.lrt && c.amenity.school);
  check('both on: AND is stricter than LRT alone', c.highlighted < lrtLit,
    `both=${c.highlighted} lrt-only=${lrtLit}`);
  check('both on: blurb reads as a conjunction',
    /within 600 m of an LRT station and 800 m of a school by road/.test(c.blurb),
    c.blurb.slice(0, 220));
  check('both on: cell data identity is stable (no re-tessellate)', sameInfillRef);

  // 6. School alone: a much larger band than LRT (they are ~14x apart).
  await click('#amenity-lrt-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('school alone: band is much larger than the LRT band',
    c.highlighted > lrtLit * 3, `school=${c.highlighted} lrt=${lrtLit}`);
  check('school alone: blurb names only the school band',
    /800 m of a school/.test(c.blurb) && !/LRT station/.test(c.blurb));

  // 7. A null distance must read as OUT of band, never as "near".
  const nullsOut = await page.evaluate(() => {
    const col = gridData.columns.dist_school_m;
    const nulls = gridData.cells.filter(d => d[col] == null);
    return { n: nulls.length, allOut: nulls.every(d => !amenityInBand(d)) };
  });
  check('null distance is out of band, not near',
    nullsOut.n > 0 && nullsOut.allOut, JSON.stringify(nullsOut));

  // 8. Other views hide the section; Glass in particular must stay undimmed
  // while a band is ON — the state persists, the rendering must not follow it.
  await click('#views button[data-view="uses"]');
  await page.waitForTimeout(3000);
  let u = await chrome();
  check('uses: amenity section hidden', !u.hdShown && !u.boxShown);

  await click('#views button[data-view="money"]');
  await page.waitForTimeout(500);
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3000);
  c = await chrome();
  check('glass with the school band ON: section still hidden',
    c.amenity.school && !c.hdShown && !c.boxShown);
  check('glass with the school band ON: still nothing dimmed', c.dimmed === 0,
    `dimmed=${c.dimmed} of ${c.nCells}`);
  check('glass with the school band ON: blurb still carries no band sentence',
    !/keep their colour/.test(c.blurb));

  // 9. Back in Infill the state survived the round trip.
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(500);
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('back in infill: school band still on and highlighting',
    c.amenity.school && c.schoolChecked && c.layers.includes('infill-amenity-grid'));

  // 10. Off again: the overlay goes away entirely.
  await click('#amenity-school-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('all off: highlight grid gone', !c.layers.includes('infill-amenity-grid'));
  check('all off: blurb drops the band sentence',
    !/translucent 100 m grid highlights/.test(c.blurb));

  console.log(`\n${pass} passed, ${fail} failed${skip ? `, ${skip} skipped` : ''}`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

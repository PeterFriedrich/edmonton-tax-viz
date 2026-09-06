// Verify the Services view's three Stage 2 transportation OPERATING cost rows
// (2026-08-03 — SPEC_services "Transportation lens" Stage 2).
//   node verify-transport-cost.js <url>
//
// The three things this exists to catch, in order of how quietly they fail:
//  1. THE LEGEND ELSE FALLS THROUGH TO ROADS. A driver with no legend branch
//     prints "Road metres per acre" over a differently-coloured map — the S88
//     bike bug, confidently wrong rather than blank. Asserted per row.
//  2. A MISSING primaryRow KEY prints "no <label> data" over a hood that has
//     data (the `|| []` fall-through). Asserted per row.
//  3. THE TWO ROAD BASES COLLAPSING. cost_roads_ops_per_acre and
//     cost_roads_life_per_acre are the same metres ~5.4x apart; if a future
//     edit ever wires one rate into both, the readouts stop differing.
//
// Also asserts the 2026-08-03 decision that transport_cost_ops_per_acre ships
// as a COLUMN but gets NO row — it is 91% transit at the median, so a row
// labelled "Transportation" would be mislabeled in the same way the
// all-or-nothing rule already guards against.
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

const ROWS = [
  { svc: 'roadscost',   col: 'cost_roads_ops_per_acre',   legend: /road operating cost/i,       readout: /road operating cost/i },
  { svc: 'transitcost', col: 'cost_transit_ops_per_acre', legend: /ETS bus \+ LRT budget share/i, readout: /ETS operating budget share/i },
  { svc: 'bikecost',    col: 'cost_bike_ops_per_acre',    legend: /bikeway operating cost/i,    readout: /bikeway operating cost/i },
];

let pass = 0, fail = 0;
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

  // ⚠️ Services is PUBLIC again as of the roads-only return (2026-09-02), so a
  // missing view now means a pre-roads DATA file, not the public build.
  const servicesOffered = await page.evaluate(() => {
    const b = document.querySelector('#views button[data-view="services"]');
    return !!b && getComputedStyle(b).display !== 'none';
  });
  if (!servicesOffered) {
    check('pre-roads data file: services view not offered', true);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  // Of this script's three rows only ROADS cost is public; transit and bike
  // cost stay full-only. On the public build assert exactly that split, then
  // stop — the ramp/clamp checks below need the full row set.
  const fullBuild = await page.evaluate(() => FULL_BUILD);
  if (!fullBuild) {
    for (const svc of ['transitcost', 'bikecost']) {
      check(`public build: ${svc} row hidden`, await page.evaluate(s =>
        getComputedStyle(document.querySelector(`#services .svc[data-service="${s}"]`)).display === 'none', svc));
      check(`public build: ${svc} not checked`,
        await page.evaluate(s => state.services[s] === false, svc));
    }
    check('public build: roadscost row still reachable', await page.evaluate(() =>
      getComputedStyle(document.querySelector('#services .svc[data-service="roadscost"]')).display !== 'none'));
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  const hasCols = await page.evaluate(cols =>
    cols.map(c => state.data.features.some(f => f.properties[c] != null)),
    ROWS.map(r => r.col));

  if (!hasCols.every(Boolean)) {
    // Pre-Stage-2 data file. The only correct behaviour is that every row whose
    // column is absent hides itself and stays unchecked — the house pattern.
    for (let i = 0; i < ROWS.length; i++) {
      if (hasCols[i]) continue;
      const r = ROWS[i];
      const hidden = await page.evaluate(svc =>
        getComputedStyle(document.querySelector(`#services .svc[data-service="${svc}"]`)).display === 'none', r.svc);
      check(`pre-Stage-2 file: ${r.svc} row hidden`, hidden);
      const off = await page.evaluate(svc => state.services[svc] === false, r.svc);
      check(`pre-Stage-2 file: ${r.svc} not checked`, off);
    }
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  await click('#views button[data-view="services"]');
  await page.waitForTimeout(1200);

  // --- the composite ships as data, NOT as a row (decision 2026-08-03) -------
  const compositePresent = await page.evaluate(() =>
    state.data.features.some(f => f.properties.transport_cost_ops_per_acre != null));
  check('transport_cost_ops_per_acre ships as a column', compositePresent);
  const compositeRow = await page.evaluate(() =>
    !!document.querySelector('#services .svc[data-service="transportcost"]'));
  check('composite has NO services row (91% transit — would be mislabeled)', !compositeRow);

  // --- the group caption --------------------------------------------------
  const caption = await page.evaluate(() =>
    [...document.querySelectorAll('#services .svc-group')]
      .filter(c => getComputedStyle(c).display !== 'none')
      .map(c => c.textContent.trim()));
  check('operating-cost group caption present', caption.some(c => /Transportation cost/i.test(c)),
        caption.join(' | '));

  for (const r of ROWS) {
    check(`data carries ${r.col}`, true);

    const shown = await page.evaluate(svc =>
      getComputedStyle(document.querySelector(`#services .svc[data-service="${svc}"]`)).display !== 'none', r.svc);
    check(`${r.svc}: row visible`, shown);

    // Drive it: check the box, then hand it the colour ramp.
    await click(`#services .svc[data-service="${r.svc}"] .svc-on`);
    await click(`#services .svc[data-service="${r.svc}"] .svc-colour input`);
    await page.waitForTimeout(900);

    const driver = await page.evaluate(() => state.svcDriver);
    check(`${r.svc}: drives the colour ramp`, driver === r.svc, `svcDriver=${driver}`);

    // (1) THE LEGEND BRANCH — must be its own, not the roads fall-through.
    const legend = await page.evaluate(() =>
      document.getElementById('legend-label').textContent.trim());
    check(`${r.svc}: legend is its own branch`, r.legend.test(legend), legend);
    check(`${r.svc}: legend is NOT the roads fallback`,
          !/^Road metres per acre$/i.test(legend), legend);

    // The legend max must come from this column's own clamp, not a neighbour's.
    const legendMax = await page.evaluate(() =>
      document.getElementById('legend-max').textContent.trim());
    const ownClamp = await page.evaluate(col =>
      Math.round(svcScale(col).clamp).toLocaleString() + '+', r.col);
    check(`${r.svc}: legend max is this column's own clamp`,
          legendMax === '$' + ownClamp, `${legendMax} vs $${ownClamp}`);

    // (2) THE primaryRow KEY — a missing one prints "no <label> data".
    const readout = await page.evaluate(svc => {
      const f = state.data.features.find(x =>
        x.properties[{ roadscost: 'cost_roads_ops_per_acre',
                       transitcost: 'cost_transit_ops_per_acre',
                       bikecost: 'cost_bike_ops_per_acre' }[svc]] > 0);
      return primaryRow(f.properties);
    }, r.svc);
    check(`${r.svc}: readout has a real value`, !/no .* data/i.test(readout), readout);
    check(`${r.svc}: readout names the operating basis`, r.readout.test(readout), readout);

    // The plane really repainted from this column.
    const planeCol = await page.evaluate(() => {
      const l = overlay._deck.props.layers.find(x => x && /svc-plane/.test(x.id));
      return l ? l.id : null;
    });
    check(`${r.svc}: a service plane is rendered`, planeCol != null, planeCol || 'none');
  }

  // --- (3) the two road bases must stay distinct ---------------------------
  // ⚠️ Compared against cost_roads_life_per_acre, NOT the retired roads+fire
  // composite (2026-09-05). It used to read that composite and call it "life",
  // so the FIRE term supplied the gap this check measures — it would have
  // passed with one rate wired into both road columns. Both sides are now the
  // same metres, so the ratio IS the two rates and nothing else.
  const bases = await page.evaluate(() => {
    const f = state.data.features.find(x =>
      x.properties.cost_roads_ops_per_acre > 0 && x.properties.cost_roads_life_per_acre > 0);
    return { ops: f.properties.cost_roads_ops_per_acre,
             life: f.properties.cost_roads_life_per_acre };
  });
  check('roads OPERATING cost is far below the LIFECYCLE cost (bases distinct)',
        bases.ops * 3 < bases.life, `ops $${bases.ops.toFixed(0)} vs life $${bases.life.toFixed(0)}`);
  check('the two road bases sit at the ~5.4x the rates imply',
        Math.abs(bases.life / bases.ops - 50 / 9.32) < 0.05,
        `${(bases.life / bases.ops).toFixed(3)}x`);

  // --- transforms inherited from the supply columns ------------------------
  const transforms = await page.evaluate(() => ({
    roadscost: SERVICES.roadscost.plane.transform || 'linear',
    transitcost: SERVICES.transitcost.plane.transform || 'linear',
    bikecost: SERVICES.bikecost.plane.transform || 'linear',
    roads: 'linear',
    transit: SERVICES.transit.plane.transform,
    bike: SERVICES.bike.plane.transform,
  }));
  check('roadscost transform matches roads (linear)', transforms.roadscost === transforms.roads);
  check('transitcost transform matches transit (sqrt)', transforms.transitcost === transforms.transit);
  check('bikecost transform matches bike (sqrt)', transforms.bikecost === transforms.bike);

  // --- the blurbs must carry the basis caveat ------------------------------
  for (const r of ROWS) {
    const blurb = await page.evaluate(svc => SERVICES[svc].blurb, r.svc);
    check(`${r.svc}: blurb says operating-only`, /[Oo]perating only/.test(blurb));
  }
  const bikeBlurb = await page.evaluate(() => SERVICES.bikecost.blurb);
  check('bikecost blurb discloses the wider clearing network',
        /pedestrian squares|bus stops|staircases/i.test(bikeBlurb));
  const roadsBlurb = await page.evaluate(() => SERVICES.roadscost.blurb);
  check('roadscost blurb distinguishes itself from Service cost',
        /lifecycle/i.test(roadsBlurb));
  const transitBlurb = await page.evaluate(() => SERVICES.transitcost.blurb);
  check('transitcost blurb discloses the DATS exclusion', /DATS/.test(transitBlurb));
  check('transitcost blurb says scheduled, not ridership', /not ridership/i.test(transitBlurb));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

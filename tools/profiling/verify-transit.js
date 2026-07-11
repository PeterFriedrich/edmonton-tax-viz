// Verify the Services view's transit service (2026-07-11 — SPEC_services
// "Transit lens": scheduled GTFS stop-events per acre, sqrt colour
// FINDINGS §6.8, LRT-station/transit-centre context dots). DOM + layer
// accessors against the real served files.
//   node verify-transit.js <url>
// Checks: checkbox gating, single shared svc-plane, station dots + legend
// row, sqrt fill + independent p97.5 clamp, set-aside grey, tooltip row,
// scheduled-not-ridership blurb, driver handoff, persistence round-trip.
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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

  const hasTransit = await page.evaluate(() =>
    state.data.features.some(f => f.properties.transit_dep_per_acre != null));
  if (!hasTransit) {
    // Pre-transit data file: the only correct behaviours are a hidden row
    // and an untouched view — verify that and stop.
    const rowHidden = await page.evaluate(() =>
      getComputedStyle(document.querySelector('#services .svc[data-service="transit"]')).display === 'none');
    check('pre-transit file: checkbox row hidden', rowHidden);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  check('data carries transit_dep_per_acre', true);
  const rowShown = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#services .svc[data-service="transit"]')).display !== 'none');
  check('transit checkbox row present', rowShown);

  await click('#views button[data-view="services"]');
  await page.waitForTimeout(4000); // roads lazy-fetch + rebuild

  // Check transit on (roads still drive): dots lazy-fetch in, exactly one
  // shared svc-plane, plane neutral slate, legend gains the station row.
  await click('#services .svc[data-service="transit"] .svc-on');
  await page.waitForTimeout(2500); // stations lazy-fetch + rebuild
  const on = await page.evaluate(() => {
    const ids = overlay._deck.props.layers.map(l => l.id);
    const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
    const mid = state.data.features.find(f =>
      !f.properties.is_set_aside && f.properties.transit_dep_per_acre > 0);
    return {
      planeCount: ids.filter(id => id === 'svc-plane').length,
      stationsPresent: ids.includes('transit-stations'),
      nStations: transitStationsData ? transitStationsData.stations.length : 0,
      planeNeutral: plane.props.getFillColor(mid).join() === GLASS_PLANE_COLOR.join(),
      cats: document.getElementById('legend-cats').textContent,
    };
  });
  check('single shared svc-plane', on.planeCount === 1, `count=${on.planeCount}`);
  check('station dots layer present', on.stationsPresent);
  check('58 stations loaded', on.nStations === 58, `n=${on.nStations}`);
  check('plane neutral while roads drive', on.planeNeutral);
  check('legend gains station row', on.cats.includes('LRT station / transit centre'), on.cats);

  // Hand the colour to transit: legend re-anchors to the independent p97.5,
  // mid-hood fill matches the SQRT expectation (FINDINGS §6.8), set-aside
  // stays grey, roads render neutral, blurb says scheduled-not-ridership.
  await click('#services .svc[data-service="transit"] input[type="radio"]');
  await page.waitForTimeout(1500);
  const drives = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
    const roads = overlay._deck.props.layers.find(l => l.id === 'roads-ground');
    const kept = state.data.features.filter(f =>
      !f.properties.is_set_aside && f.properties.transit_dep_per_acre != null);
    const vals = kept.map(f => f.properties.transit_dep_per_acre).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const mid = kept[Math.floor(kept.length / 2)];
    const scale = svcScale('transit_dep_per_acre');
    // transit colour is SQRT (FINDINGS §6.8) — re-derived independently of svcT
    const expected = rampColorAt(
      Math.sqrt(Math.min(1, mid.properties.transit_dep_per_acre / scale.clamp)));
    const aside = state.data.features.find(f => f.properties.is_set_aside);
    const access = roadsData.features.find(f => f.properties.t !== 'arterial');
    return {
      clampMatchesP975: Math.abs(scale.clamp - q) < 1e-6,
      clamp: scale.clamp,
      midFillOk: plane.props.getFillColor(mid).join() === expected.join(),
      asideGrey: plane.props.getFillColor(aside).join() === SET_ASIDE_COLOR.join(),
      accessNeutral: roads.props.getLineColor(access).join() === ARTERIAL_COLOR.join(),
      legendLabel: document.getElementById('legend-label').textContent,
      legendMax: document.getElementById('legend-max').textContent,
      blurb: document.getElementById('title-p').textContent,
    };
  });
  check('clamp = independent p97.5', drives.clampMatchesP975, `clamp=${drives.clamp}`);
  check('mid-hood fill matches sqrt ramp', drives.midFillOk);
  check('set-aside hood grey', drives.asideGrey);
  check('road lines neutral under transit driver', drives.accessNeutral);
  check('legend label names the metric + sqrt',
        drives.legendLabel === 'Scheduled transit stop-events per acre / weekday (sqrt colour)',
        drives.legendLabel);
  check('legend max anchors to clamp',
        drives.legendMax === drives.clamp.toFixed(drives.clamp < 10 ? 1 : 0) + '+',
        drives.legendMax);
  check('blurb says scheduled-not-ridership',
        drives.blurb.includes('not') && drives.blurb.toLowerCase().includes('ridership'),
        drives.blurb.slice(0, 90) + '…');

  // Tooltip: the services branch carries the transit row.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(f => f.properties.neighbourhood_name === 'STRATHCONA');
    return tooltipFor({ object: f }).html;
  });
  check('tooltip carries transit row', tip.includes('scheduled transit stop-events / acre / weekday'), tip);

  // Uncheck transit (the driver): dots + legend row leave, the ramp hands
  // itself back to a checked service rather than point at nothing.
  await click('#services .svc[data-service="transit"] .svc-on');
  await page.waitForTimeout(1500);
  const off = await page.evaluate(() => ({
    stationsGone: !overlay._deck.props.layers.some(l => l.id === 'transit-stations'),
    driver: state.svcDriver,
    driverChecked: state.services[state.svcDriver],
    catsGone: !document.getElementById('legend-cats').textContent.includes('LRT station'),
  }));
  check('dots leave the stack on uncheck', off.stationsGone);
  check('driver hands back to a checked service', off.driver !== 'transit' && off.driverChecked,
        `driver=${off.driver}`);
  check('station legend row hides', off.catsGone);

  // Persistence: transit on + driving survives a money round-trip.
  await click('#services .svc[data-service="transit"] .svc-on');
  await page.waitForTimeout(500);
  await click('#services .svc[data-service="transit"] input[type="radio"]');
  await page.waitForTimeout(500);
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  await click('#views button[data-view="services"]');
  await page.waitForTimeout(1500);
  const back = await page.evaluate(() => ({
    on: state.services.transit, driver: state.svcDriver,
    label: document.getElementById('legend-label').textContent,
  }));
  check('state persists across view round-trip',
        back.on && back.driver === 'transit' &&
        back.label.startsWith('Scheduled transit stop-events'),
        JSON.stringify(back));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

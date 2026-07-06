// One-off verify for the Services view (2026-07-05 — the Roads view
// generalized to per-service checkboxes + a stormwater ground plane;
// 2026-07-06 — fire service: shared svc-plane + station dots).
// DOM + layer checks: chrome on entry (roads-only default, radios hidden,
// prism slider hidden, lens disabled), layer stack per checkbox state,
// service plane fills (neutral under a roads driver / ramp-coloured when a
// plane service drives / set-aside grey always), the plane stays SINGLE
// with two plane services checked (coplanar layers would z-fight),
// colour-driver handoff (roads go neutral, legend re-anchors to the
// driver's p97.5 recomputed independently), driver reassignment when the
// driving service unchecks, tooltip carries every service, station dots
// appear with the fire service, state persists across a view round-trip.
// Fire checks SKIP cleanly when the data file predates the fire column.
//   node verify-services.js <url>
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

  const chrome = () => page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    blurbIsServices: document.getElementById('title-p').textContent === servicesBlurb(),
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    cats: document.getElementById('legend-cats').style.display !== 'none'
      ? document.getElementById('legend-cats').textContent.trim() : '',
    panelShown: getComputedStyle(document.getElementById('layers')).display !== 'none',
    servicesShown: getComputedStyle(document.getElementById('services')).display !== 'none',
    prismRowShown: getComputedStyle(document.getElementById('prism-row')).display !== 'none',
    denomShown: getComputedStyle(document.getElementById('denom')).display !== 'none',
    lensDisabled: document.querySelector('#lens button').disabled,
    services: { ...state.services },
    driver: state.svcDriver,
    radiosShown: [...document.querySelectorAll('#services .svc-colour')]
      .map(el => getComputedStyle(el).display !== 'none'),
    layers: typeof overlay !== 'undefined' ? overlay._deck.props.layers.map(l => l.id) : [],
  }));

  console.log('money default  :', JSON.stringify(await chrome()));

  await click('#views button[data-view="services"]');
  await page.waitForTimeout(4000); // roads lazy-fetch + rebuild
  console.log('services entry :', JSON.stringify(await chrome()));

  // Roads-only default: an access segment carries the ramp (not arterial grey).
  const roadsOnly = await page.evaluate(() => {
    const roads = overlay._deck.props.layers.find(l => l.id === 'roads-ground');
    const access = roadsData.features.find(f => f.properties.t !== 'arterial');
    const art = roadsData.features.find(f => f.properties.t === 'arterial');
    return {
      accessColoured: roads.props.getLineColor(access).join() !== ARTERIAL_COLOR.join(),
      arterialNeutral: roads.props.getLineColor(art).join() === ARTERIAL_COLOR.join(),
      svcPlanePresent: overlay._deck.props.layers.some(l => l.id === 'svc-plane'),
    };
  });
  console.log('roads only     :', JSON.stringify(roadsOnly));

  // Check stormwater on: plane appears UNDER the roads, neutral slate (roads
  // still drive the colour); set-aside hoods take the usual grey; the colour
  // radios appear (a real choice now exists).
  await click('#services .svc[data-service="storm"] .svc-on');
  await page.waitForTimeout(1500);
  const bothRoadsDrive = await page.evaluate(() => {
    const ids = overlay._deck.props.layers.map(l => l.id);
    const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
    let neutral = 0, aside = 0, other = 0;
    for (const f of state.data.features) {
      const fill = plane.props.getFillColor(f).join();
      if (f.properties.is_set_aside) fill === SET_ASIDE_COLOR.join() ? aside++ : other++;
      else fill === GLASS_PLANE_COLOR.join() ? neutral++ : other++;
    }
    return { planeBeforeRoads: ids.indexOf('svc-plane') < ids.indexOf('roads-ground'),
             planePickable: !!plane.props.pickable,
             nHoods: state.data.features.length, neutral, aside, other };
  });
  console.log('storm neutral  :', JSON.stringify(bothRoadsDrive));
  console.log('chrome         :', JSON.stringify(await chrome()));

  // Hand the colour to stormwater: legend re-anchors to the storm p97.5
  // (recomputed here with an independent quantile), a mid hood's plane fill
  // matches the ramp at its linear clamped t, and every road line goes
  // neutral.
  await click('#services .svc[data-service="storm"] input[type="radio"]');
  await page.waitForTimeout(1500);
  const stormDrives = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
    const roads = overlay._deck.props.layers.find(l => l.id === 'roads-ground');
    const kept = state.data.features.filter(f =>
      !f.properties.is_set_aside && f.properties.storm_charge_per_acre != null);
    const vals = kept.map(f => f.properties.storm_charge_per_acre).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const mid = kept[Math.floor(kept.length / 2)];
    const scale = svcScale('storm_charge_per_acre');
    const expected = rampColorAt(Math.min(1, mid.properties.storm_charge_per_acre / scale.clamp));
    const access = roadsData.features.find(f => f.properties.t !== 'arterial');
    return { clampMatchesP975: Math.abs(scale.clamp - q) < 1e-6,
             midFillOk: plane.props.getFillColor(mid).join() === expected.join(),
             accessNeutral: roads.props.getLineColor(access).join() === ARTERIAL_COLOR.join(),
             legendMax: document.getElementById('legend-max').textContent };
  });
  console.log('storm drives   :', JSON.stringify(stormDrives));
  console.log('chrome         :', JSON.stringify(await chrome()));

  // Tooltip: the services branch carries every service's numbers.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(f => f.properties.neighbourhood_name === 'STRATHCONA');
    return tooltipFor({ object: f }).html;
  });
  console.log('tooltip        :', tip);

  // --- fire service (2026-07-06) — skipped on pre-fire data files ---------
  const hasFire = await page.evaluate(() =>
    state.data.features.some(f => f.properties.fire_events_per_acre != null));
  if (!hasFire) {
    console.log('fire checks    : SKIPPED — data file has no fire_events_per_acre column');
    console.log('fire row hidden:', JSON.stringify(await page.evaluate(() =>
      getComputedStyle(document.querySelector('#services .svc[data-service="fire"]')).display === 'none')));
  } else {
    // Check fire on (storm still drives): STILL exactly one svc-plane (two
    // coplanar planes would z-fight), station dots appear once fetched,
    // three radios show, the legend gains the station row.
    await click('#services .svc[data-service="fire"] .svc-on');
    await page.waitForTimeout(2500); // stations lazy-fetch + rebuild
    const fireOn = await page.evaluate(() => {
      const ids = overlay._deck.props.layers.map(l => l.id);
      return { planeCount: ids.filter(id => id === 'svc-plane').length,
               stationsPresent: ids.includes('fire-stations'),
               nStations: typeof fireStationsData === 'object' && fireStationsData
                 ? fireStationsData.stations.length : 0 };
    });
    console.log('fire on        :', JSON.stringify(fireOn));
    console.log('chrome         :', JSON.stringify(await chrome()));

    // Hand the colour to fire: legend re-anchors to the fire p97.5
    // (independent quantile), mid-hood plane fill matches, roads neutral.
    await click('#services .svc[data-service="fire"] input[type="radio"]');
    await page.waitForTimeout(1500);
    const fireDrives = await page.evaluate(() => {
      const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
      const kept = state.data.features.filter(f =>
        !f.properties.is_set_aside && f.properties.fire_events_per_acre != null);
      const vals = kept.map(f => f.properties.fire_events_per_acre).sort((a, b) => a - b);
      const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
      const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
      const mid = kept[Math.floor(kept.length / 2)];
      const scale = svcScale('fire_events_per_acre');
      const expected = rampColorAt(Math.min(1, mid.properties.fire_events_per_acre / scale.clamp));
      return { clampMatchesP975: Math.abs(scale.clamp - q) < 1e-6,
               midFillOk: plane.props.getFillColor(mid).join() === expected.join(),
               legendMax: document.getElementById('legend-max').textContent };
    });
    console.log('fire drives    :', JSON.stringify(fireDrives));
    console.log('chrome         :', JSON.stringify(await chrome()));

    // Tooltip now carries all three services.
    console.log('tooltip (fire) :', await page.evaluate(() => {
      const f = state.data.features.find(f => f.properties.neighbourhood_name === 'STRATHCONA');
      return tooltipFor({ object: f }).html;
    }));

    // Uncheck fire: dots leave the stack, driver hands back to a checked
    // service, the station legend row hides.
    await click('#services .svc[data-service="fire"] .svc-on');
    await page.waitForTimeout(1000);
    console.log('fire off       :', JSON.stringify(await chrome()));
  }

  // Uncheck roads: its layer leaves the stack, storm keeps/regains colour.
  await click('#services .svc[data-service="roads"] .svc-on');
  await page.waitForTimeout(1500);
  console.log('storm only     :', JSON.stringify(await chrome()));

  // Re-check roads, then uncheck the DRIVER (storm): the ramp must hand
  // itself back to a checked service rather than point at nothing.
  await click('#services .svc[data-service="roads"] .svc-on');
  await page.waitForTimeout(1000);
  await click('#services .svc[data-service="storm"] .svc-on');
  await page.waitForTimeout(1000);
  console.log('driver handoff :', JSON.stringify(await chrome()));

  // State persists across a view round-trip; the section hides outside
  // services. (Leave with storm on + driving to make persistence visible.)
  await click('#services .svc[data-service="storm"] .svc-on');
  await page.waitForTimeout(500);
  await click('#services .svc[data-service="storm"] input[type="radio"]');
  await page.waitForTimeout(500);
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  console.log('money (hidden?):', JSON.stringify(await chrome()));
  await click('#views button[data-view="services"]');
  await page.waitForTimeout(1500);
  console.log('services again :', JSON.stringify(await chrome()));

  await browser.close();
})();

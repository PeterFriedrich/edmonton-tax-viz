// Verify the Tier-1 geographic reference layer — the North Saskatchewan River
// and the Anthony Henday ring road (web/data/reference.geojson, built offline
// by scripts/build_reference_layers.py).
//
// This map has NO basemap tiles, just a dark backdrop, so these two shapes are
// the only thing telling a first-time viewer where they are. Three properties
// carry the whole feature and each was a real bug during the build:
//
//   1. THE TWO SIT AT OPPOSITE ENDS OF THE STACK, and must stay there.
//      The ring road is drawn LAST: the hood polygons tile the whole city, so
//      underneath it was 99.6% occluded (0.38% of pixels changed, vs 1.22% on
//      top). The river is drawn FIRST: the hood fabric already carries a
//      river-shaped seam (the valley is set-aside parkland), so painting the
//      water over it cut into the geometry and glitched along the shared
//      edges — underneath, it shows through the seam and runs on past the
//      city limit.
//   2. depthTest ON for the ring road. With it off it cut across the faces of
//      the downtown towers. The river needs none — it is the backdrop, drawn
//      before everything, so it neither occludes nor z-fights.
//   3. Present in EVERY view. Both are composed in buildLayers() around
//      buildViewLayers(), so a new view cannot ship without them.
//
//   node tools/profiling/verify-reference-layer.js <url>     (from REPO ROOT)
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// Every view the public and specialist builds can show.
const VIEWS = ['money', 'services', 'ratio', 'uses', 'development'];

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  // `state` is a top-level const, so it is NOT on window — reference it bare.
  const probe = () => page.evaluate(() => {
    const layers = (overlay._deck && overlay._deck.props.layers) || [];
    const ids = layers.filter(Boolean).map(l => l.id);
    const river = layers.filter(Boolean).find(l => l.id === 'reference-river');
    const henday = layers.filter(Boolean).find(l => l.id === 'reference-henday');
    let data = null;
    try { data = referenceData; } catch (e) { /* not yet fetched */ }
    return {
      ids,
      present: !!river && !!henday,
      riverIndex: ids.indexOf('reference-river'),
      hendayIndex: ids.indexOf('reference-henday'),
      count: ids.length,
      depthTest: henday ? henday.props.parameters.depthTest : null,
      riverDepthTest: river ? river.props.parameters.depthTest : null,
      pickable: river ? (river.props.pickable || henday.props.pickable) : null,
      stateOn: state.reference,
      checkbox: document.getElementById('reference-on').checked,
      types: data ? data.features.map(f => f.properties.t).sort() : null,
      geoms: data ? data.features.map(f => f.geometry.type).sort() : null,
    };
  });

  // --- the data file -------------------------------------------------------
  const s0 = await probe();
  check('reference.geojson fetched', s0.types !== null);
  check('carries exactly the two Tier-1 shapes', JSON.stringify(s0.types) === '["henday","river"]',
        JSON.stringify(s0.types));
  // The river is Multi at the shipped 60 km clip — that wide an extent picks up
  // disjoint stretches up- and downstream — but a narrow clip yields a single
  // Polygon, so accept either rather than pinning the margin into the suite.
  check('river is polygonal, ring road is lines',
        /^\["MultiLineString","(Multi)?Polygon"\]$/.test(JSON.stringify(s0.geoms)),
        JSON.stringify(s0.geoms));

  // The ring must be CLOSED. A hole in the east leg (Highway 216 runs
  // concurrent with Highway 14 there, and the feed names only Highway 14)
  // left a 2.9 km break — 73 screen pixels, which reads as a rendering bug.
  // Re-checked here so a future rebuild cannot quietly reintroduce it.
  const ring = await page.evaluate(() => {
    const f = referenceData.features.find(x => x.properties.t === 'henday');
    const parts = f.geometry.coordinates;
    const ends = [];
    for (const p of parts) { ends.push(p[0], p[p.length - 1]); }
    // ~50 m in degrees at Edmonton's latitude, matching the builder's tolerance.
    const TOL = 50 / 111000;
    const near = (a, b) => Math.abs(a[0] - b[0]) < TOL / Math.cos(53.5 * Math.PI / 180)
                        && Math.abs(a[1] - b[1]) < TOL;
    const loose = ends.filter((e, i) => !ends.some((o, j) => j !== i && near(e, o)));
    // Rough length in km, for the "did a leg go missing" guard.
    let km = 0;
    for (const p of parts) {
      for (let i = 1; i < p.length; i++) {
        const dx = (p[i][0] - p[i - 1][0]) * 111 * Math.cos(53.5 * Math.PI / 180);
        const dy = (p[i][1] - p[i - 1][1]) * 111;
        km += Math.hypot(dx, dy);
      }
    }
    return { loose: loose.length, parts: parts.length, km: Math.round(km) };
  });
  check('ring road has no loose ends (no visible break, no spur)', ring.loose === 0,
        `${ring.loose} dangling of ${ring.parts} arcs`);
  check('ring road length is a double ring (~150 km)', ring.km > 120 && ring.km < 200,
        `${ring.km} km`);

  // --- layer composition ---------------------------------------------------
  check('both layers are built', s0.present);
  check('on by default (no basemap — orientation should not need hunting)', s0.stateOn === true);
  check('checkbox agrees with state', s0.checkbox === true);
  check('not pickable (never steals a hood tooltip)', s0.pickable === false);
  check('ring road depthTest ON so prisms occlude it', s0.depthTest === true);
  check('river depthTest OFF (it is the backdrop, not an occluder)',
        s0.riverDepthTest === false);
  check('river composed FIRST, under the data', s0.riverIndex === 0,
        `index ${s0.riverIndex} of ${s0.count}`);
  check('ring road composed LAST, over the data', s0.hendayIndex === s0.count - 1,
        `index ${s0.hendayIndex} of ${s0.count}`);

  // --- present in every view ----------------------------------------------
  for (const v of VIEWS) {
    const btn = await page.$(`#views button[data-view="${v}"]`);
    if (!btn) { console.log(`SKIP  [${v}] not in this build`); continue; }
    await page.evaluate(vv => applyView(vv), v);
    await page.waitForTimeout(1600);
    const s = await probe();
    check(`[${v}] both reference layers present`, s.present);
    check(`[${v}] river still first, ring road still last`,
          s.riverIndex === 0 && s.hendayIndex === s.count - 1,
          `river ${s.riverIndex}, henday ${s.hendayIndex} of ${s.count}`);
  }
  await page.evaluate(() => applyView('money'));
  await page.waitForTimeout(1200);

  // --- the toggle ----------------------------------------------------------
  await page.click('#a11y-btn');
  await page.waitForTimeout(300);
  const box = await page.$('#reference-on');
  const clickable = await page.evaluate(() => {
    const el = document.getElementById('reference-on');
    const r = el.getBoundingClientRect();
    return document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === el;
  });
  check('checkbox is really clickable (not covered)', clickable);
  await box.click();
  await page.waitForTimeout(900);
  const off = await probe();
  check('unticking removes both layers entirely',
        off.riverIndex === -1 && off.hendayIndex === -1 && off.stateOn === false);
  await box.click();
  await page.waitForTimeout(900);
  const on = await probe();
  check('re-ticking restores it', on.present === true && on.stateOn === true);
  check('bracketing survives the round-trip',
        on.riverIndex === 0 && on.hendayIndex === on.count - 1);

  // --- it must actually be VISIBLE, not merely present ---------------------
  // The whole defect that motivated drawing it last was a layer that existed,
  // reported present, and painted almost nothing. Compare rendered pixels.
  await page.evaluate(() => { document.getElementById('a11y').classList.remove('open'); });
  await page.evaluate(() => map.easeTo({ pitch: 0, bearing: 0, duration: 0 }));
  await page.waitForTimeout(1200);
  const shot = async v => {
    await page.evaluate(x => applyReference(x), v);
    await page.waitForTimeout(900);
    return page.screenshot({ timeout: 60000 });
  };
  const onBuf = await shot(true), offBuf = await shot(false);
  await page.evaluate(() => applyReference(true));
  check('rendering actually differs with it on', !onBuf.equals(offBuf));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

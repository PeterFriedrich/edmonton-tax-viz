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

// The regional place names (PLACES in scripts/build_reference_layers.py). They
// are a fourth property of the feature and the odd one out: they render as
// TEXT, sharing one TextLayer and one declutter sweep with the neighbourhood
// labels, while riding the REFERENCE toggle rather than the label one. That
// split is the thing worth pinning — it is what puts a place name on screen
// for a viewer who has touched no control, and it is invisible in the DOM.
const TOWN_COUNT = 9;          // PLACES: 7 + Morinville, Stony Plain (2026-08-08)

// The outlines (REGIONS in scripts/build_reference_layers.py): Edmonton's own
// legal limit plus the four counties it abuts. They share the t="boundary" kind
// with the towns' outlines, so boundaries are NO LONGER 1:1 with place names —
// that used to be the invariant here, and it was retired deliberately on
// 2026-08-08 rather than broken. Kept as its own constant so a region silently
// vanishing from the build still trips the count.
const REGION_COUNT = 5;
const ZONE_COUNT = 1;          // Alberta's Industrial Heartland
const HOOD_LABEL_SIZE = 15;    // LABEL_SIZE in web/index.html
const BOUNDARY_COUNT = TOWN_COUNT + REGION_COUNT + ZONE_COUNT;

// Label anchors, which is NOT the boundary count: Edmonton is drawn but
// deliberately unnamed (the title already says it), and the two econ points
// (Nisku, the airport) are named but have no outline to draw. Both asymmetries
// are decisions, so they are spelled out rather than folded into one number —
// a build that starts labelling Edmonton should trip this, not pass quietly.
const PLACE_COUNT = TOWN_COUNT + (REGION_COUNT - 1) + ZONE_COUNT + 2;

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
    const highway = layers.filter(Boolean).find(l => l.id === 'reference-highway');
    let data = null;
    try { data = referenceData; } catch (e) { /* not yet fetched */ }
    return {
      ids,
      present: !!river && !!highway,
      riverIndex: ids.indexOf('reference-river'),
      highwayIndex: ids.indexOf('reference-highway'),
      count: ids.length,
      depthTest: highway ? highway.props.parameters.depthTest : null,
      riverDepthTest: river ? river.props.parameters.depthTest : null,
      pickable: river ? (river.props.pickable || highway.props.pickable) : null,
      stateOn: state.reference,
      checkbox: document.getElementById('reference-on').checked,
      types: data ? data.features.map(f => f.properties.t).sort() : null,
      geoms: data ? data.features.map(f => f.geometry.type).sort() : null,
    };
  });

  // --- the data file -------------------------------------------------------
  const s0 = await probe();
  check('reference.geojson fetched', s0.types !== null);
  // One river, one ring road, and one point per named place. Asserted as a
  // CLOSED set rather than a minimum: an unexpected `t` means the build script
  // emitted something the renderer has no branch for, which would draw nothing
  // and look exactly like success.
  const kinds = (s0.types || []).reduce((m, t) => (m[t] = (m[t] || 0) + 1, m), {});
  check('carries one river and one highway network',
        kinds.river === 1 && kinds.highway === 1, JSON.stringify(kinds));
  check('carries an outline per named place AND per unlabelled region',
        kinds.boundary === BOUNDARY_COUNT,
        `${kinds.boundary} of ${BOUNDARY_COUNT}`);
  check('carries the regional place points', kinds.place === PLACE_COUNT,
        `${kinds.place} of ${PLACE_COUNT}`);
  check('no unexpected feature kinds',
        Object.keys(kinds).every(t => ['river', 'highway', 'boundary', 'place'].includes(t)),
        JSON.stringify(Object.keys(kinds).sort()));
  // The river is Multi at the shipped 60 km clip — that wide an extent picks up
  // disjoint stretches up- and downstream — but a narrow clip yields a single
  // Polygon, so accept either rather than pinning the margin into the suite.
  const shapeGeoms = (s0.geoms || []).filter(g => g !== 'Point');
  check('river + boundaries are polygonal, highways are lines',
        shapeGeoms.filter(g => g === 'MultiLineString').length === 1 &&
        shapeGeoms.filter(g => /Polygon$/.test(g)).length === BOUNDARY_COUNT + 1,
        JSON.stringify(shapeGeoms));
  check('every place is a Point',
        (s0.geoms || []).filter(g => g === 'Point').length === PLACE_COUNT,
        JSON.stringify(s0.geoms));

  // THE HIGHWAYS MUST RUN OFF THE EDGE OF THE VIEW, not stop at the city
  // limit. That is the whole reason this layer moved off the City centreline
  // feed (2026-08-03): the City feed's highways end at the boundary and read
  // as amputated, the same failure the river's 60 km margin exists to prevent.
  // A regression here draws a plausible-looking map, so it is asserted on
  // GEOMETRY rather than on the source.
  const reach = await page.evaluate(() => {
    const hw = referenceData.features.find(x => x.properties.t === 'highway');
    const parts = hw.geometry.coordinates;
    let hb = [Infinity, Infinity, -Infinity, -Infinity];
    let km = 0;
    for (const p of parts) {
      for (let i = 0; i < p.length; i++) {
        hb[0] = Math.min(hb[0], p[i][0]); hb[1] = Math.min(hb[1], p[i][1]);
        hb[2] = Math.max(hb[2], p[i][0]); hb[3] = Math.max(hb[3], p[i][1]);
        if (i) {
          const dx = (p[i][0] - p[i - 1][0]) * 111 * Math.cos(53.5 * Math.PI / 180);
          const dy = (p[i][1] - p[i - 1][1]) * 111;
          km += Math.hypot(dx, dy);
        }
      }
    }
    // The city's own extent, from the hood polygons the map is actually drawn from.
    let cb = [Infinity, Infinity, -Infinity, -Infinity];
    const walk = c => {
      if (typeof c[0] === 'number') {
        cb[0] = Math.min(cb[0], c[0]); cb[1] = Math.min(cb[1], c[1]);
        cb[2] = Math.max(cb[2], c[0]); cb[3] = Math.max(cb[3], c[1]);
      } else c.forEach(walk);
    };
    state.data.features.forEach(f => walk(f.geometry.coordinates));
    return { hb, cb, km: Math.round(km), parts: parts.length };
  });
  const [hw0, hw1, hw2, hw3] = reach.hb, [c0, c1, c2, c3] = reach.cb;
  check('highways extend past the city on ALL FOUR sides',
        hw0 < c0 && hw1 < c1 && hw2 > c2 && hw3 > c3,
        `hw [${reach.hb.map(v => v.toFixed(2))}] vs city [${reach.cb.map(v => v.toFixed(2))}]`);
  // ~873 km welded over the 60 km clip (2026-08-03). A band, not an equality:
  // OSM is edited continuously, and this is a cartographic layer, not a metric.
  check('highway network is the whole regional net, not one road',
        reach.km > 600 && reach.km < 1300, `${reach.km} km in ${reach.parts} parts`);
  // Highway 216 is the ring; if the network collapsed to a single corridor the
  // part count would crater. Open ends are EXPECTED here (they run off the
  // clip), which is exactly why the old ring-closure assertion was retired
  // rather than adapted.
  check('network is many disjoint corridors', reach.parts > 20, `${reach.parts} parts`);

  // --- layer composition ---------------------------------------------------
  check('the reference layers are built', s0.present);
  check('on by default (no basemap — orientation should not need hunting)', s0.stateOn === true);
  check('checkbox agrees with state', s0.checkbox === true);
  check('not pickable (never steals a hood tooltip)', s0.pickable === false);
  check('highway depthTest ON so prisms occlude it', s0.depthTest === true);
  check('river depthTest OFF (it is the backdrop, not an occluder)',
        s0.riverDepthTest === false);
  check('river composed FIRST, under the data', s0.riverIndex === 0,
        `index ${s0.riverIndex} of ${s0.count}`);
  check('highways composed LAST, over the data', s0.highwayIndex === s0.count - 1,
        `index ${s0.highwayIndex} of ${s0.count}`);

  // --- present in every view ----------------------------------------------
  for (const v of VIEWS) {
    const btn = await page.$(`#views button[data-view="${v}"]`);
    if (!btn) { console.log(`SKIP  [${v}] not in this build`); continue; }
    await page.evaluate(vv => applyView(vv), v);
    await page.waitForTimeout(1600);
    const s = await probe();
    check(`[${v}] both reference layers present`, s.present);
    check(`[${v}] river still first, highways still last`,
          s.riverIndex === 0 && s.highwayIndex === s.count - 1,
          `river ${s.riverIndex}, highway ${s.highwayIndex} of ${s.count}`);
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
        off.riverIndex === -1 && off.highwayIndex === -1 && off.stateOn === false);
  await box.click();
  await page.waitForTimeout(900);
  const on = await probe();
  check('re-ticking restores it', on.present === true && on.stateOn === true);
  check('bracketing survives the round-trip',
        on.riverIndex === 0 && on.highwayIndex === on.count - 1);

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

  // --- the regional place names --------------------------------------------
  // Two classes now share one TextLayer under independent toggles. Each state
  // below broke at some point while wiring it, and none is visible in the DOM.
  const labels = () => page.evaluate(() => {
    const l = overlay._deck.props.layers.find(x => x && x.id === 'hood-labels');
    if (!l) return { layer: false, places: 0, hoods: 0, sizes: [] };
    const d = l.props.data;
    // ⚠️ `x.ref`, not `x.prio === PRIO_PLACE`. Counting by that priority meant
    // "towns", and since 2026-08-08 most regional names are NOT towns — the
    // four counties and the industrial zone sort above it. Left as-is, this
    // counter would have reported every new tier as absent and still passed,
    // which is the coverage hole the tiering was most likely to fall into.
    // `byTier` is what makes a single tier vanishing visible.
    const tiers = {};
    for (const x of d) if (x.ref) tiers[x.tier] = (tiers[x.tier] || 0) + 1;
    return {
      layer: true,
      places: d.filter(x => x.ref).length,
      byTier: tiers,
      hoods: d.filter(x => x.prio === PRIO_HOOD).length,
      sizes: [...new Set(d.map(x => x.size))].sort((a, b) => a - b),
      anchored: placeAnchors().length,
    };
  });
  const setToggles = async (ref, lab) => {
    await page.evaluate(x => applyReference(x), ref);
    await page.evaluate(x => applyLabels(x), lab);
    await page.waitForTimeout(900);
    return labels();
  };

  // ⚠️ Back to HOME first. The checks above leave the camera wherever the
  // highway-extent and view-switch probes put it, and how many names survive the
  // declutter sweep is a function of the camera — so a per-tier count taken
  // here would be asserting against an accident of test order. The tier checks
  // below are the ones that care; the toggle checks never did.
  await page.evaluate(() => map.easeTo({ ...HOME, duration: 0 }));
  await page.waitForTimeout(1200);

  const def = await setToggles(true, false);
  check('all place anchors built from the data file',
        def.anchored === PLACE_COUNT, `${def.anchored} of ${PLACE_COUNT}`);
  // The point of the feature: names on screen with no control touched. Not
  // all 7 — Leduc sits below the bottom edge at the default pitched camera and
  // the sweep correctly culls it — so assert a healthy majority, not equality.
  check('places show with hood labels OFF (the default)',
        def.places >= 5 && def.hoods === 0, `${def.places} places, ${def.hoods} hoods`);
  // The regional-narrative tiers, added 2026-08-08. Counties are the tier that
  // most needs pinning: they are the only names placed by _region_anchor rather
  // than by a centroid, so a regression there (an anchor pushed back out to the
  // true centroid, 27-58 km away) shows up as them silently going missing at the
  // default camera while every other name still draws.
  // 3 of 4, NOT 4: Leduc County's anchor projects to py≈1040 in a 900px
  // viewport at the default pitched camera, so the sweep culls it as offscreen
  // — measured, and the same reason the TOWN of Leduc is culled a few lines up.
  // Asserted as a floor with an explicit exemption rather than loosened to
  // ">= 1", which would pass with three counties silently gone.
  check('every on-screen county is named at the default camera',
        def.byTier.region === REGION_COUNT - 2,
        `${def.byTier.region || 0} of ${REGION_COUNT - 2}: ${JSON.stringify(def.byTier)}`);
  check('the town and econ tiers both draw too',
        def.byTier.place >= 5 && def.byTier.econ === 2, JSON.stringify(def.byTier));
  // ⚠️ WAS `def.sizes.length === 1` — one reference size, because there was one
  // reference tier. Since 2026-08-08 there are four (region/zone/place/econ,
  // REF_TIERS in web/index.html), so equality-to-1 was pinning the old design
  // rather than the invariant. The invariant is the ORDERING, and it survives:
  // regional text is context and must never outweigh a hood name.
  check('every regional name renders smaller than a hood name',
        def.sizes.length >= 1 && def.sizes.length <= 4 &&
        def.sizes.every(s => s < HOOD_LABEL_SIZE), JSON.stringify(def.sizes));

  const both = await setToggles(true, true);
  check('turning hood labels on does not evict the places',
        both.places === def.places && both.hoods > 0,
        `${both.places} places, ${both.hoods} hoods`);
  // Same retirement as above: "exactly 2 sizes" meant "1 reference tier + 1 hood
  // size". What must hold is that BOTH CLASSES are actually on screen — the hood
  // size present, and at least one smaller regional size beside it.
  check('both classes are on screen, hood text the largest',
        both.sizes.includes(HOOD_LABEL_SIZE) &&
        both.sizes.some(s => s < HOOD_LABEL_SIZE), JSON.stringify(both.sizes));

  const hoodsOnly = await setToggles(false, true);
  check('reference off drops the places but keeps the hoods',
        hoodsOnly.places === 0 && hoodsOnly.hoods > 0,
        `${hoodsOnly.places} places, ${hoodsOnly.hoods} hoods`);

  const neither = await setToggles(false, false);
  check('both off removes the text layer entirely', neither.layer === false);

  // --- the sweep must track the camera, in the DEFAULT toggle state ----------
  // Regression: the moveend re-cull was gated on state.labels, which ships
  // false, so with hood labels off the sweep ran once at load and froze. The
  // names never re-culled or resized until an unrelated rebuild unstuck them,
  // and the visible symptom (nearly all of them gone after a zoom-out) looked
  // like a data bug. Comparing DRAWN against a FRESH sweep is what catches it:
  // both were individually plausible, only the mismatch was wrong.
  await setToggles(true, false);
  const atZoom = async z => {
    await page.evaluate(zz => map.easeTo({ zoom: zz, duration: 200 }), z);
    await page.waitForTimeout(1400);
    return page.evaluate(() => {
      const l = overlay._deck.props.layers.flat()
        .find(x => x && x.id === 'hood-labels');
      const drawn = (l ? l.props.data : []).filter(x => x.prio === PRIO_PLACE);
      return {
        drawn: drawn.length,
        fresh: visibleLabels().filter(x => x.prio === PRIO_PLACE).length,
        size: drawn.length ? drawn[0].size : null,
        cached: placeAnchors()[0].size,
      };
    });
  };
  const near = await atZoom(10.2), far = await atZoom(8);
  check('re-cull fires on camera move with hood labels off (near)',
        near.drawn === near.fresh, `drawn ${near.drawn} vs fresh ${near.fresh}`);
  check('re-cull fires on camera move with hood labels off (far)',
        far.drawn === far.fresh, `drawn ${far.drawn} vs fresh ${far.fresh}`);
  check('place labels shrink as the camera pulls back',
        far.size < near.size, `${near.size} -> ${far.size}`);
  // The scaled size rides on a copy; the memoized anchors are shared across
  // every sweep, so a write-back would leak one camera's zoom into the next.
  check('scaling does not mutate the memoized anchors',
        far.cached === near.cached, `${near.cached} -> ${far.cached}`);

  // --- labels must dodge the HTML chrome ------------------------------------
  // The sweep declutters labels against each other but the panels sit over the
  // same canvas, so a label could be KEPT and then painted under the Options
  // panel (FORT SASKATCHEWAN was) or into the title blurb. The invariant is
  // simply that nothing kept overlaps chrome — checked with both label classes
  // on, since hood labels are far more numerous and hit more panels.
  await page.evaluate(() => map.easeTo({ zoom: 10.2, duration: 200 }));
  await page.waitForTimeout(1200);
  for (const lab of [false, true]) {
    await setToggles(true, lab);
    const occ = await page.evaluate(() => {
      const boxes = chromeBoxes();
      const dv = overlay._deck.getViewports()[0];
      return visibleLabels().filter(d => {
        const [px, py] = dv.project([d.position[0], d.position[1], labelZ(d.p)]);
        // Unpadded, matching the cull: LABEL_PAD is label-vs-label breathing
        // room, and charging it against a panel edge culls names whose glyphs
        // are entirely clear of it.
        const w = d.em * d.size * LABEL_DRAW_SCALE;
        const h = d.size * LABEL_DRAW_SCALE;
        return boxes.some(c => px + w / 2 > c.x0 && px - w / 2 < c.x1 &&
                               py + h / 2 > c.y0 && py - h / 2 < c.y1);
      }).map(d => d.name);
    });
    check(`no kept label sits under chrome (hood labels ${lab ? 'on' : 'off'})`,
          occ.length === 0, JSON.stringify(occ));
  }

  // The two checks above re-run visibleLabels(), which re-reads chromeBoxes()
  // in the same tick — so they can only ever agree with themselves. What ships
  // is the DRAWN layer, and that goes stale whenever the chrome CHANGES SIZE
  // after the sweep. Entering Development grows #title from bottom 196 to 462
  // at 1440x900 (its blurb is far longer), and the blurb used to be written
  // AFTER buildLayers — leaving SPRUCE GROVE painted into the new text until
  // some later rebuild. Same shape as the frozen-sweep bug: compare DRAWN
  // against live chrome, never a fresh sweep against itself.
  const drawnOcc = () => page.evaluate(() => {
    const boxes = chromeBoxes();
    const dv = overlay._deck.getViewports()[0];
    const l = overlay._deck.props.layers.flat().find(x => x && x.id === 'hood-labels');
    return (l ? l.props.data : []).filter(d => {
      const [px, py] = dv.project([d.position[0], d.position[1], labelZ(d.p)]);
      const w = d.em * d.size * LABEL_DRAW_SCALE, h = d.size * LABEL_DRAW_SCALE;
      return boxes.some(c => px + w / 2 > c.x0 && px - w / 2 < c.x1 &&
                             py + h / 2 > c.y0 && py - h / 2 < c.y1);
    }).map(d => d.name);
  });
  await setToggles(true, true);   // hood labels on: more labels, more chances
  for (const view of VIEWS) {
    await page.$eval(`#views button[data-view="${view}"]`, b => b.click());
    await page.waitForTimeout(1600);
    const occ = await drawnOcc();
    check(`[${view}] drawn labels dodge chrome immediately after the switch`,
          occ.length === 0, JSON.stringify(occ));
  }
  await page.$eval('#views button[data-view="money"]', b => b.click());
  await page.waitForTimeout(1200);

  // CHROME_IDS is a closed hand-written list. That is the house habit, but a
  // closed list silently rots when a panel is added and nobody updates it —
  // which is precisely how this bug would come back. So assert the list COVERS
  // every .panel in the document: either the panel is named, or an ancestor of
  // it is (#layers/#coloradj are borderless sections inside #optpanel, which is
  // the box that actually paints). A new panel now FAILS here rather than
  // quietly going un-dodged.
  const uncovered = await page.evaluate(() => {
    const named = new Set(CHROME_IDS);
    return [...document.querySelectorAll('.panel')]
      .filter(el => {
        for (let n = el; n; n = n.parentElement) if (named.has(n.id)) return false;
        return true;
      })
      .map(el => el.id || '(no id)');
  });
  check('CHROME_IDS covers every .panel in the document',
        uncovered.length === 0, JSON.stringify(uncovered));

  // Chrome boxes are read live, so a panel that is hidden in this view must not
  // still be culling labels behind it.
  const chromeVisible = await page.evaluate(() => {
    const cv = document.querySelector('#map canvas').getBoundingClientRect();
    return chromeBoxes().every(c => c.x1 > c.x0 && c.y1 > c.y0 &&
                                    c.x1 > 0 && c.y1 > 0 &&
                                    c.x0 < cv.width && c.y0 < cv.height);
  });
  check('chrome boxes are all real, on-canvas rects', chromeVisible);

  await setToggles(true, false);   // leave it at the shipped default

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

// One-off verify for the institutional caveat on the MONEY tooltip (2026-08-15).
// The Lab bands a >=25%-institutional hood into a range and asserts no value;
// the default map keeps the solid prism and says it in words instead. Checks:
// the caveat fires on all three revenue cuts and NOT under Value (exemption
// changes whether a levy is collected, not what a parcel is assessed at); the
// hood set matches the Lab's threshold constant exactly; a low-institutional
// hood stays clean; the copy names ZONING (the row above it is a class share)
// and never asserts a direction.
//   node verify-inst-caveat.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// The wording rule from DECISIONS.md 2026-08-08, same list verify-deviation.js
// greps for: nothing may read as revenue the City fails to collect.
const BANNED = /\b(lost|uncollected|foregone|should be|really|actually)\b/i;

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

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  const tip = (hood, metric) => page.evaluate(([hood, metric]) => {
    if (state.metric !== metric) applyMetric(metric);
    const f = state.data.features.find(x => x.properties.neighbourhood_name === hood);
    return f ? viewTooltip({ object: f }).html : null;
  }, [hood, metric]);

  const CAVEAT = /of revenue is on institutionally-zoned land/;
  const EXEMPT = /the City does not publish which of it is tax-exempt/;

  // --- fires on Total, and prints the hood's own share ----------------------
  const ua = await tip('UNIVERSITY OF ALBERTA', 'revenue_per_acre');
  console.log('U of A / Total :', ua.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
  check('caveat fires on Total revenue', CAVEAT.test(ua) && EXEMPT.test(ua));
  check('share is the hood\'s own rev_frac_exempt', /90% of revenue/.test(ua));
  // U of A is in the CONSEQUENCE tier, so its headline is a range, not a
  // figure: a hollow prism beside a single confident number contradicts itself.
  // ⚠️ Moved 2026-08-25 with the roll: was $17,522 to $171,670 at 2025 mill
  // rates. The 2026 roll bills at 7.7419 / 25.2216 (was 7.6254 / 24.2229), so
  // both endpoints rise ~3.9% — a RATE change, not drift in the band.
  check('a hollow hood prints a RANGE, low end first',
    /\$18,047 to \$178,401\s*\/ acre/.test(ua.replace(/<[^>]+>/g, '')));

  // --- the two subset cuts carry it too ------------------------------------
  for (const m of ['res_revenue_per_acre', 'nonres_revenue_per_acre']) {
    const h = await tip('UNIVERSITY OF ALBERTA', m);
    check(`caveat fires on ${m}`, CAVEAT.test(h) && EXEMPT.test(h));
  }

  // --- and NOT under Value -------------------------------------------------
  const uaVal = await tip('UNIVERSITY OF ALBERTA', 'value_per_acre');
  check('NO caveat under Value (assessment is not uncertain)',
        !CAVEAT.test(uaVal) && !EXEMPT.test(uaVal));

  // --- a low-institutional hood stays clean --------------------------------
  const dt = await tip('DOWNTOWN', 'revenue_per_acre');
  check('DOWNTOWN (5% inst) has no caveat', !CAVEAT.test(dt) && !EXEMPT.test(dt));

  // --- the hood set is the Lab's, by construction --------------------------
  // Not a re-derived list: both surfaces must read EXEMPT_UNCERTAIN_MIN, so a
  // future change to the threshold moves them together or this fails.
  const sets = await page.evaluate(() => {
    if (state.metric !== 'revenue_per_acre') applyMetric('revenue_per_acre');
    const props = state.data.features.map(f => f.properties);
    const live = props.filter(p => !p.is_set_aside && p.revenue_per_acre);
    return {
      min: EXEMPT_UNCERTAIN_MIN,
      flagged: live.filter(p => exemptFrac(p) >= EXEMPT_UNCERTAIN_MIN)
                   .map(p => p.neighbourhood_name).sort(),
      tipped: live.filter(p => /institutionally-zoned/.test(viewTooltip({ object: { properties: p } }).html))
                  .map(p => p.neighbourhood_name).sort(),
    };
  });
  check('threshold is the Lab constant, not a copy', sets.min === 0.25, `min=${sets.min}`);
  check('tooltip set == threshold set',
        JSON.stringify(sets.flagged) === JSON.stringify(sets.tipped),
        `${sets.tipped.length} hoods`);
  // ⚠️ 15 -> 21 on 2026-08-25: the gate moved off the `inst` zoning CATEGORY
  // onto EXEMPT_CANDIDATE_ZONES, which adds `PS` (Parks and Services) — $88M/yr
  // of levy the caveat had been silent about. The six new hoods are all
  // park-dominated (MILL WOODS PARK's entire levy sits on PS).
  check('21 hoods carry the caveat', sets.tipped.length === 21, sets.tipped.join(', '));

  // --- the consequence tier: which prisms become bands ---------------------
  const hollow = await page.evaluate(() => {
    if (state.metric !== 'revenue_per_acre') applyMetric('revenue_per_acre');
    const props = state.data.features.map(f => f.properties);
    const live = props.filter(p => !p.is_set_aside && p.revenue_per_acre);
    const set = p => live.filter(p2 => p2 === p);
    const hollowed = live.filter(instBandedMoney);
    const caveat = live.filter(p => exemptFrac(p) >= EXEMPT_UNCERTAIN_MIN);
    const main = overlay._props.layers.find(l => l.id === 'metric-extrusion');
    const lev = overlay._props.layers.find(l => l.id === 'inst-band-levied');
    const ex = overlay._props.layers.find(l => l.id === 'inst-band-exempt');
    const edges = overlay._props.layers.find(l => l.id === 'top-edges');
    const feat = n => state.data.features.find(f => f.properties.neighbourhood_name === n);
    const ua = feat('UNIVERSITY OF ALBERTA');
    // Same set with the sqrt colour toggle flipped — it must not move.
    const before = hollowed.map(p => p.neighbourhood_name).sort();
    state.colorAdjust = !state.colorAdjust;
    const after = live.filter(instBandedMoney).map(p => p.neighbourhood_name).sort();
    state.colorAdjust = !state.colorAdjust;
    return {
      names: before,
      caveatNames: caveat.map(p => p.neighbourhood_name).sort(),
      outsideCaveat: hollowed.filter(p => exemptFrac(p) < EXEMPT_UNCERTAIN_MIN).length,
      layersExist: !!lev && !!ex,
      bandData: lev ? lev.props.data.length : -1,
      filled: lev ? lev.props.filled : null,
      wireframe: lev ? lev.props.wireframe : null,
      color: lev ? lev.props.getLineColor : null,
      fillAlpha: lev ? lev.props.getFillColor[3] : null,
      fillAlphaExempt: ex ? ex.props.getFillColor[3] : null,
      lineAlpha: lev ? lev.props.getLineColor[3] : null,
      order: (() => {
        const ids = overlay._props.layers.map(l => l.id);
        return ids.indexOf('inst-band-exempt') < ids.indexOf('inst-band-levied')
          ? 'exempt-first' : 'levied-first';
      })(),
      uaFill: main.props.getFillColor(ua),
      uaElev: main.props.getElevation(ua),
      uaLev: lev.props.getElevation(ua),
      uaEx: ex.props.getElevation(ua),
      edgeCount: edges.props.data.length,
      // Rings, not hoods — a MultiPolygon hood emits one path per part, so
      // 406 hoods make 454 rings and a hood-count comparison is meaningless.
      totalRings: topRings(state.data.features, moneyScale().colKey,
                           moneyScale().elevationScale).length,
      afterToggle: after,
    };
  });
  console.log('band set     :', hollow.names.join(', '));
  check('6 hoods get band prisms on Total', hollow.names.length === 6, `${hollow.names.length}`);
  check('*** the band set is a SUBSET of the caveat tier ***', hollow.outsideCaveat === 0,
    `${hollow.outsideCaveat} outside`);
  check('it is a STRICT subset (the floor hoods keep their prisms)',
    hollow.names.length < hollow.caveatNames.length,
    `${hollow.names.length} of ${hollow.caveatNames.length}`);
  check('the two endpoint layers exist', hollow.layersExist);
  check('they carry ONLY the banded hoods, not all 406', hollow.bandData === 6,
    `${hollow.bandData} features`);
  // ⚠️ FILLED since 2026-08-15 — bare wireframes were the Lab's weak point
  // ("that hollow prism is super hard to see"). The 2026-08-12 rule is kept by
  // giving BOTH endpoints the SAME alpha, so neither world gets primacy.
  check('both endpoints are translucent prisms with opaque edges',
    hollow.filled === true && hollow.wireframe === true);
  check('*** both endpoints carry the SAME alpha (no world gets primacy) ***',
    hollow.fillAlpha === hollow.fillAlphaExempt && hollow.fillAlpha === 128,
    `${hollow.fillAlpha} / ${hollow.fillAlphaExempt}`);
  check('the edge stays fully opaque (it carries the ΔE guarantee)',
    hollow.lineAlpha === 255, `${hollow.lineAlpha}`);
  // Exempt must draw BEFORE levied so the certain base composites denser.
  check('exempt layer is drawn before levied', hollow.order === 'exempt-first',
    hollow.order);
  // ⚠️ NOT the Lab's white: glow's peak is #fff6e4 and white against it is
  // ΔE 3.5. Azure #2ec4ff clears 21.5 normal / 19.5 CVD across all three ramps.
  check('outline is the measured azure, not white',
    JSON.stringify((hollow.color || []).slice(0, 3)) === JSON.stringify([46, 196, 255]),
    JSON.stringify(hollow.color));
  check('*** a banded hood draws NO RAMP-COLOURED prism ***',
    hollow.uaElev === 0 && hollow.uaFill[3] === 0, `elev ${hollow.uaElev} alpha ${hollow.uaFill[3]}`);
  check('exempt endpoint sits BELOW levied (always, on an absolute rate)',
    hollow.uaEx < hollow.uaLev, `${Math.round(hollow.uaEx)} < ${Math.round(hollow.uaLev)}`);
  check('the roof-ring layer skips the banded hoods',
    hollow.edgeCount < hollow.totalRings, `${hollow.edgeCount} rings / ${hollow.totalRings} hoods`);
  // ⚠️ A display preference must not change which prisms exist. Under the
  // linear setting the set otherwise loses UNIVERSITY OF ALBERTA FARM.
  check('*** the sqrt colour toggle does NOT move the band set ***',
    JSON.stringify(hollow.names) === JSON.stringify(hollow.afterToggle),
    hollow.afterToggle.join(', '));

  const valHollow = await page.evaluate(() => {
    applyMetric('value_per_acre');
    const n = state.data.features.filter(f => instBandedMoney(f.properties)).length;
    const lev = overlay._props.layers.find(l => l.id === 'inst-band-levied');
    applyMetric('revenue_per_acre');
    return { n, band: lev ? lev.props.data.length : -1 };
  });
  check('NO band prisms under Value', valHollow.n === 0 && valHollow.band === 0,
    `${valHollow.n} hoods, ${valHollow.band} banded`);

  // --- the prism is its own hover target (2026-08-17) -----------------------
  // ⚠️ THE BUG THIS CATCHES IS NOT "no tooltip", IT IS THE WRONG HOOD'S.
  // A banded hood's metric-extrusion geometry is flattened to 0 and painted
  // transparent, so if the azure prism standing over that footprint is not
  // pickable the cursor falls through to whatever is BEHIND it — measured at
  // pitch 55 before the fix: MCKERNAN, RIVER VALLEY VICTORIA, WÎHKWÊNTÔWIN,
  // all while the pointer sat on the U of A's geometry. A flat overhead test
  // cannot see this: at pitch 0 the transparent footprint picks correctly.
  const pick = await page.evaluate(async () => {
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    const rg = f.geometry.type === 'Polygon'
      ? f.geometry.coordinates[0] : f.geometry.coordinates[0][0];
    let lng = 0, lat = 0;
    for (const c of rg) { lng += c[0]; lat += c[1]; }
    lng /= rg.length; lat /= rg.length;
    map.jumpTo({ center: [lng, lat], zoom: 12.4, pitch: 60, bearing: 0 });
    await new Promise(r => setTimeout(r, 1800));
    const vp = overlay._deck.getViewports()[0];
    const [sx, sy] = vp.project([lng, lat]);
    // Walk UP the screen from the footprint, through the prism body.
    const hits = [];
    for (let dy = -30; dy >= -200; dy -= 10) {
      const i = overlay._deck.pickObject({ x: Math.round(sx), y: Math.round(sy + dy), radius: 0 });
      if (i) hits.push({ layer: i.layer.id, hood: i.object.properties.neighbourhood_name });
    }
    const band = overlay._props.layers.filter(l => l.id.startsWith('inst-band'));
    return { hits, pickable: band.map(l => !!l.props.pickable),
             highlight: band.map(l => !!l.props.autoHighlight) };
  });
  const onBand = pick.hits.filter(h => h.layer.startsWith('inst-band'));
  check('*** the azure prism BODY is pickable, not just the flat below it ***',
    onBand.length > 0, `${onBand.length} of ${pick.hits.length} sampled pixels`);
  check('*** every pick on the band returns ITS OWN hood ***',
    onBand.length > 0 && onBand.every(h => h.hood === 'UNIVERSITY OF ALBERTA'),
    [...new Set(onBand.map(h => h.hood))].join(', ') || 'none');
  check('both band layers are pickable',
    pick.pickable.length === 2 && pick.pickable.every(Boolean), JSON.stringify(pick.pickable));
  // The pick lands on ONE of the two shells, so a highlight would light the
  // levied world and leave the exempt one dark — the primacy the band refuses.
  check('neither band layer autoHighlights',
    pick.highlight.every(h => !h), JSON.stringify(pick.highlight));

  // --- the hover glow (2026-08-18) ------------------------------------------
  // ⚠️ WHAT FAILS SILENTLY HERE IS *CONFIRMATION*: pickable alone made the band
  // answer on hover, but it did not light up like every other prism, so nothing
  // on screen told you which hood you were on (Peter). The glow is index-driven
  // rather than autoHighlight so BOTH shells light — autoHighlight lights only
  // the shell the pick landed on, which is the primacy the band refuses.
  // Driven through bandHover() directly rather than a real pointer move: the
  // wiring is asserted separately, and a synthetic call cannot go flaky on the
  // SwiftShader picking pass.
  const glow = await page.evaluate(() => {
    // ⚠️ Report a MISSING handler as a failed check, not a stack trace: a
    // build without it should say which contract broke.
    if (typeof bandHover !== 'function') return { absent: true };
    const bands = () => overlay._deck.props.layers.filter(l => l.id.startsWith('inst-band'));
    const idxs = () => bands().map(l => l.props.highlightedObjectIndex);
    const lev = bands().find(l => l.id === 'inst-band-levied');
    const i = lev.props.data.findIndex(
      f => f.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    const before = idxs();
    bandHover({ picked: true, index: i, layer: { id: 'inst-band-levied' } });
    const during = idxs();
    const colors = bands().map(l => l.props.highlightColor.join(','));
    // Moving off the band must put it out again.
    bandHover({ picked: false, layer: null });
    const off = idxs();
    // A rebuild must CLEAR it: the banded subset is rebuilt by the same toggles,
    // so a carried index would light a different hood than the cursor is on.
    bandHover({ picked: true, index: i, layer: { id: 'inst-band-levied' } });
    overlay.setProps({ layers: buildLayers() });
    const afterRebuild = idxs();
    return { i, before, during, off, afterRebuild, colors,
             wired: overlay._props.onHover === bandHover,
             hood: lev.props.data[i].properties.neighbourhood_name };
  });
  check('the band hover handler EXISTS', !glow.absent);
  if (glow.absent) { glow.before = glow.during = glow.off = glow.afterRebuild = [];
                     glow.colors = []; }
  check('the hover handler is wired into deck', !glow.absent && glow.wired);
  check('nothing is lit at rest', !glow.absent && glow.before.length === 2 && glow.before.every(v => v === -1), JSON.stringify(glow.before));
  check('*** hovering the band lights BOTH shells, not just the picked one ***',
    !glow.absent && glow.during.length === 2 && glow.during.every(v => v === glow.i),
    `${JSON.stringify(glow.during)} for index ${glow.i} (${glow.hood})`);
  check('the glow is the same white every other prism uses',
    !glow.absent && glow.colors.length === 2 && glow.colors.every(c => c === '255,255,255,60'), glow.colors.join(' | '));
  check('moving off the band puts it out', !glow.absent && glow.off.length === 2 && glow.off.every(v => v === -1),
    JSON.stringify(glow.off));
  // ⚠️ Not cosmetic: switching cut or denominator re-selects the banded hoods,
  // so a carried index is a confident highlight on the WRONG neighbourhood.
  check('*** a layer rebuild CLEARS the glow (the index is subset-relative) ***',
    !glow.absent && glow.afterRebuild.length === 2 && glow.afterRebuild.every(v => v === -1), JSON.stringify(glow.afterRebuild));

  // --- wording -------------------------------------------------------------
  check('copy says "zoned" (class share vs zoning share)', /institutionally-zoned/.test(ua));
  check('copy asserts no direction', !BANNED.test(ua.replace(/<[^>]+>/g, ' ')));
  check('does not claim the City fails to collect', !/fails? to collect|owed|should have/i.test(ua));

  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

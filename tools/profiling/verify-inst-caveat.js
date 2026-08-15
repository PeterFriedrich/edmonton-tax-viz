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
  check('share is the hood\'s own rev_frac_inst', /90% of revenue/.test(ua));
  // U of A is in the CONSEQUENCE tier, so its headline is a range, not a
  // figure: a hollow prism beside a single confident number contradicts itself.
  check('a hollow hood prints a RANGE, low end first',
    /\$17,522 to \$171,670\s*\/ acre/.test(ua.replace(/<[^>]+>/g, '')));

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
  // Not a re-derived list: both surfaces must read INST_UNCERTAIN_MIN, so a
  // future change to the threshold moves them together or this fails.
  const sets = await page.evaluate(() => {
    if (state.metric !== 'revenue_per_acre') applyMetric('revenue_per_acre');
    const props = state.data.features.map(f => f.properties);
    const live = props.filter(p => !p.is_set_aside && p.revenue_per_acre);
    return {
      min: INST_UNCERTAIN_MIN,
      flagged: live.filter(p => instFrac(p) >= INST_UNCERTAIN_MIN)
                   .map(p => p.neighbourhood_name).sort(),
      tipped: live.filter(p => /institutionally-zoned/.test(viewTooltip({ object: { properties: p } }).html))
                  .map(p => p.neighbourhood_name).sort(),
    };
  });
  check('threshold is the Lab constant, not a copy', sets.min === 0.25, `min=${sets.min}`);
  check('tooltip set == threshold set',
        JSON.stringify(sets.flagged) === JSON.stringify(sets.tipped),
        `${sets.tipped.length} hoods`);
  check('15 hoods carry the caveat', sets.tipped.length === 15, sets.tipped.join(', '));

  // --- the consequence tier: which prisms go hollow ------------------------
  const hollow = await page.evaluate(() => {
    if (state.metric !== 'revenue_per_acre') applyMetric('revenue_per_acre');
    const props = state.data.features.map(f => f.properties);
    const live = props.filter(p => !p.is_set_aside && p.revenue_per_acre);
    const set = p => live.filter(p2 => p2 === p);
    const hollowed = live.filter(instHollowMoney);
    const caveat = live.filter(p => instFrac(p) >= INST_UNCERTAIN_MIN);
    const main = overlay._props.layers.find(l => l.id === 'metric-extrusion');
    const lev = overlay._props.layers.find(l => l.id === 'inst-band-levied');
    const ex = overlay._props.layers.find(l => l.id === 'inst-band-exempt');
    const edges = overlay._props.layers.find(l => l.id === 'top-edges');
    const feat = n => state.data.features.find(f => f.properties.neighbourhood_name === n);
    const ua = feat('UNIVERSITY OF ALBERTA');
    // Same set with the sqrt colour toggle flipped — it must not move.
    const before = hollowed.map(p => p.neighbourhood_name).sort();
    state.colorAdjust = !state.colorAdjust;
    const after = live.filter(instHollowMoney).map(p => p.neighbourhood_name).sort();
    state.colorAdjust = !state.colorAdjust;
    return {
      names: before,
      caveatNames: caveat.map(p => p.neighbourhood_name).sort(),
      outsideCaveat: hollowed.filter(p => instFrac(p) < INST_UNCERTAIN_MIN).length,
      layersExist: !!lev && !!ex,
      bandData: lev ? lev.props.data.length : -1,
      filled: lev ? lev.props.filled : null,
      wireframe: lev ? lev.props.wireframe : null,
      color: lev ? lev.props.getLineColor : null,
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
  console.log('hollow set   :', hollow.names.join(', '));
  check('6 hoods go hollow on Total', hollow.names.length === 6, `${hollow.names.length}`);
  check('*** hollow is a SUBSET of the caveat tier ***', hollow.outsideCaveat === 0,
    `${hollow.outsideCaveat} outside`);
  check('it is a STRICT subset (the floor hoods keep their prisms)',
    hollow.names.length < hollow.caveatNames.length,
    `${hollow.names.length} of ${hollow.caveatNames.length}`);
  check('the two endpoint layers exist', hollow.layersExist);
  check('they carry ONLY the hollow hoods, not all 406', hollow.bandData === 6,
    `${hollow.bandData} features`);
  check('outline only — no fill on either endpoint',
    hollow.filled === false && hollow.wireframe === true);
  // ⚠️ NOT the Lab's white: glow's peak is #fff6e4 and white against it is
  // ΔE 3.5. Azure #2ec4ff clears 21.5 normal / 19.5 CVD across all three ramps.
  check('outline is the measured azure, not white',
    JSON.stringify((hollow.color || []).slice(0, 3)) === JSON.stringify([46, 196, 255]),
    JSON.stringify(hollow.color));
  check('*** a hollow hood draws NO solid prism ***',
    hollow.uaElev === 0 && hollow.uaFill[3] === 0, `elev ${hollow.uaElev} alpha ${hollow.uaFill[3]}`);
  check('exempt endpoint sits BELOW levied (always, on an absolute rate)',
    hollow.uaEx < hollow.uaLev, `${Math.round(hollow.uaEx)} < ${Math.round(hollow.uaLev)}`);
  check('the roof-ring layer skips the hollow hoods',
    hollow.edgeCount < hollow.totalRings, `${hollow.edgeCount} rings / ${hollow.totalRings} hoods`);
  // ⚠️ A display preference must not change which prisms exist. Under the
  // linear setting the set otherwise loses UNIVERSITY OF ALBERTA FARM.
  check('*** the sqrt colour toggle does NOT move the hollow set ***',
    JSON.stringify(hollow.names) === JSON.stringify(hollow.afterToggle),
    hollow.afterToggle.join(', '));

  const valHollow = await page.evaluate(() => {
    applyMetric('value_per_acre');
    const n = state.data.features.filter(f => instHollowMoney(f.properties)).length;
    const lev = overlay._props.layers.find(l => l.id === 'inst-band-levied');
    applyMetric('revenue_per_acre');
    return { n, band: lev ? lev.props.data.length : -1 };
  });
  check('NO hollow prisms under Value', valHollow.n === 0 && valHollow.band === 0,
    `${valHollow.n} hoods, ${valHollow.band} banded`);

  // --- wording -------------------------------------------------------------
  check('copy says "zoned" (class share vs zoning share)', /institutionally-zoned/.test(ua));
  check('copy asserts no direction', !BANNED.test(ua.replace(/<[^>]+>/g, ' ')));
  check('does not claim the City fails to collect', !/fails? to collect|owed|should have/i.test(ua));

  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

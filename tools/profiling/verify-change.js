// Verify the change lens (SPEC_temporal.md round 2): "how fast did each
// neighbourhood's share of the assessment base move", all 406 at once, as a
// flat diverging choropleth under Money with a two-window picker.
//
// The load-bearing claims, in the order they'd fail silently:
//   1. **ANNUALISED OVER YEARS ELAPSED, NOT OBSERVED INTERVALS.** The 2024 gap
//      makes them differ — the long window spans 13 years but holds 12
//      intervals — so annualising over intervals inflates every hood's rate
//      ~8%. Nothing on screen would look wrong. This is checked FIRST and
//      against the raw file, not against the app's own arithmetic.
//   2. **The rate is COMPOUND, not arithmetic.** The arithmetic form is
//      unbounded above (observed max +2,076%/yr) and would give the diverging
//      ramp two arms 108x apart, so teal would be owned by a few new
//      subdivisions. Proven by measuring a hood where the two forms differ.
//   3. **Both degenerate endpoints are holes, not numbers.** 45 hoods have no
//      first-year baseline and 1 ends at zero share; neither has a defined
//      compound rate. They must render off-scale grey and say WHY — and must
//      NOT read as set-aside land, which is the opposite story (these are the
//      new-growth areas).
//   4. It is a FLAT diverging plane. A prism cannot have negative height, and
//      hoods moved both ways; the in-repo precedent is the infill plane.
//   5. The two windows really do differ, and switching them NEVER refetches.
//   6. It is PUBLIC as of 2026-07-31 (promoted from full-only): `?build=public`
//      offers the lens toggle, and reveals the window picker ON ENTERING change
//      mode — the picker is hidden in Money/current in BOTH builds, so checking
//      it before the switch tests nothing.
//   7. Panel mode's reduced one-liner follows the change lens (the primaryRow
//      trap — a positional "row 0" rule is wrong for services and would be
//      wrong here too).
//   node verify-change.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  const open = async (u, vp) => {
    const page = await browser.newPage({ viewport: vp });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
    return page;
  };

  // ---- desktop, full build ------------------------------------------------
  const reqs = [];
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('request', r => { if (r.url().includes('temporal.json')) reqs.push(r.url()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);

  // The lens toggle ships hidden and is revealed only once the file lands, so
  // it can never offer a lens whose data is absent.
  const vis = id => page.evaluate(i => {
    const el = document.getElementById(i);
    return !!el && getComputedStyle(el).display !== 'none';
  }, id);
  check('Money lens toggle is revealed once temporal.json lands', await vis('moneymode'));
  check('window picker stays hidden outside the change lens', !(await vis('chgwindow')));

  await page.click('#moneymode button[data-moneymode="change"]');
  await page.waitForTimeout(1200);

  // ---- 1. THE YEARS-ELAPSED TRAP -----------------------------------------
  // Recomputed from the RAW served file, so this cannot be satisfied by the
  // app agreeing with itself.
  const raw = await page.evaluate(async () => {
    const d = await (await fetch('./data/temporal.json')).json();
    const ys = d.years, j = ys.length - 1;
    const i = ys.findIndex(y => y >= 2012);
    const row = d.hoods['DOWNTOWN'][0];
    const first = 100 * row[i] / d.share_scale, last = 100 * row[j] / d.share_scale;
    return {
      elapsed: ys[j] - ys[i],          // 13 — the honest divisor
      intervals: j - i,                // 12 — the trap
      compoundElapsed: Math.pow(last / first, 1 / (ys[j] - ys[i])) - 1,
      compoundIntervals: Math.pow(last / first, 1 / (j - i)) - 1,
      arithmeticElapsed: (last / first - 1) / (ys[j] - ys[i]),
    };
  });
  const app = await page.evaluate(() => changeFor('DOWNTOWN'));
  check('the long window spans 13 elapsed years but only 12 observed intervals',
    raw.elapsed === 13 && raw.intervals === 12, `${raw.elapsed} vs ${raw.intervals}`);
  check('*** annualises over YEARS ELAPSED, not observed intervals ***',
    app.years === raw.elapsed && Math.abs(app.rate - raw.compoundElapsed) < 1e-12,
    `years=${app.years}`);
  check('the interval divisor would have given a materially different rate',
    Math.abs(raw.compoundIntervals - raw.compoundElapsed) > 1e-4,
    `${(100 * raw.compoundElapsed).toFixed(3)}%/yr vs ${(100 * raw.compoundIntervals).toFixed(3)}%/yr`);
  check('reported elapsed years equal the endpoint year span',
    app.years === app.to - app.from, `${app.from}-${app.to} = ${app.years}`);

  // ---- 2. compound, not arithmetic ---------------------------------------
  check('the rate is COMPOUND, not arithmetic',
    Math.abs(app.rate - raw.arithmeticElapsed) > 1e-4,
    `compound ${(100 * app.rate).toFixed(2)}%/yr vs arithmetic ${(100 * raw.arithmeticElapsed).toFixed(2)}%/yr`);
  // The property that made compounding necessary: the gaining arm stays bounded
  // close enough to the losing arm for one diverging ramp to carry both.
  const arms = await page.evaluate(() => {
    const s = chgStats();
    return { pos: s.clampPos, neg: s.clampNeg };
  });
  check('the two arms are within one order of magnitude (a shared ramp is honest)',
    arms.pos / arms.neg < 10,
    `+${(100 * arms.pos).toFixed(1)}%/yr vs -${(100 * arms.neg).toFixed(1)}%/yr`);

  // ---- 3. the two degenerate endpoints are holes --------------------------
  const holes = await page.evaluate(() => {
    const names = state.data.features.map(f => f.properties.neighbourhood_name);
    const of = n => changeFor(n);
    const noBase = names.filter(n => { const c = of(n); return c && c.reason === 'no-baseline'; });
    const noEnd = names.filter(n => { const c = of(n); return c && c.reason === 'no-endpoint'; });
    const anyRateOnHole = names.some(n => { const c = of(n); return c && c.reason && c.rate != null; });
    const greyed = noBase.concat(noEnd).every(n => {
      const f = state.data.features.find(x => x.properties.neighbourhood_name === n);
      return chgT(f.properties) === null;
    });
    const tipFor = n => tooltipFor({
      object: state.data.features.find(x => x.properties.neighbourhood_name === n) });
    return {
      noBase: noBase.length, noEnd: noEnd.length, anyRateOnHole, greyed,
      sampleBaseTip: noBase.length ? tipFor(noBase[0]).html : '',
      sampleEndTip: noEnd.length ? tipFor(noEnd[0]).html : '',
      noHistory: names.filter(n => !of(n)).length,
    };
  });
  check('45 hoods have no 2012 baseline (matches the measured gate)',
    holes.noBase === 45, `${holes.noBase}`);
  check('the one hood that fell to zero share is a hole, not -100%/yr',
    holes.noEnd === 1, `${holes.noEnd}`);
  check('no hole ever carries a rate', !holes.anyRateOnHole);
  check('every hole is off the colour scale (renders the off-scale grey)', holes.greyed);
  check('every hood in the map has assessment history', holes.noHistory === 0);
  check('the no-baseline hover names the missing YEAR',
    /No 2012 baseline/.test(holes.sampleBaseTip), '');
  // The trap this feature was warned about: these are new-growth areas, and
  // reading them as protected land inverts the story.
  check('the no-baseline hover does NOT say "set aside"',
    !/set.aside/i.test(holes.sampleBaseTip));
  check('the fell-to-zero hover states its own reason',
    /Holds none of the assessment base in 2025/.test(holes.sampleEndTip));
  const legendAside = await page.evaluate(() =>
    document.querySelector('#legend .aside span:last-child').textContent);
  check('the legend swatch says "no baseline", not "set aside"',
    /No 2012 baseline/.test(legendAside) && !/set.aside/i.test(legendAside), legendAside);

  // ---- 4. a flat diverging plane -----------------------------------------
  const render = await page.evaluate(() => {
    const layers = overlay._props.layers;
    const plane = layers.find(l => l.id === 'change-plane');
    const bar = getComputedStyle(document.querySelector('#legend .bar')).backgroundImage;
    return {
      ids: layers.map(l => l.id),
      extruded: plane && plane.props.extruded,
      hasHover: layers.some(l => l.id === 'hood-hover'),
      barHead: bar.slice(0, 40), barTail: bar.slice(-40),
      neg: infillColorAt(-1), pos: infillColorAt(1),
    };
  });
  check('the change plane is on the map', render.ids.includes('change-plane'));
  check('the plane is FLAT — a prism cannot have negative height',
    render.extruded === false, `extruded=${render.extruded}`);
  check('the flat view carries its own hover layer', render.hasHover);
  check('no money prisms survive into the change lens',
    !render.ids.some(i => /prism|glass|hood-metric/.test(i)), render.ids.join(','));
  check('the legend bar diverges: losing arm at 0%',
    render.barHead.includes(`rgb(${render.neg.join(', ')})`), render.barHead);
  check('the legend bar diverges: gaining arm at 100%',
    render.barTail.includes(`rgb(${render.pos.join(', ')})`), render.barTail);

  // ---- 7. panel mode's reduced readout follows the lens --------------------
  const reduced = await page.evaluate(() => {
    applyHoodMode('panel');
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const html = tooltipFor({ object: f }).html;
    applyHoodMode('popup');
    return html;
  });
  check('panel mode reduces to the CHANGE rate, not the money metric',
    /% \/ yr/.test(reduced) && !/\/ acre/.test(reduced), reduced.replace(/<[^>]+>/g, ' ').trim());

  // ---- the popup tooltip does not print the endpoints twice ---------------
  const dup = await page.evaluate(() => {
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'DOWNTOWN');
    return tooltipFor({ object: f }).html;
  });
  check('the hover states the endpoint pair exactly once',
    (dup.match(/of city base/g) || []).length === 1,
    `${(dup.match(/of city base/g) || []).length}x`);

  // ---- 5. the windows differ, and switching never refetches ---------------
  const before = reqs.length;
  await page.click('#chgwindow button[data-chgwindow="short"]');
  await page.waitForTimeout(1200);
  const shortW = await page.evaluate(() => ({
    dt: changeFor('DOWNTOWN'),
    label: document.getElementById('legend-label').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    noBase: state.data.features
      .map(f => changeFor(f.properties.neighbourhood_name))
      .filter(c => c && c.reason === 'no-baseline').length,
  }));
  check('switching windows NEVER refetches temporal.json',
    reqs.length === before, `${reqs.length - before} new fetch(es) on switch`);
  check('the short window spans 6 elapsed years (2019-2025)',
    shortW.dt.years === 6 && shortW.dt.from === 2019, `${shortW.dt.from}, ${shortW.dt.years} yr`);
  check('the short window gives a different rate than the long one',
    Math.abs(shortW.dt.rate - app.rate) > 1e-4,
    `${(100 * app.rate).toFixed(2)}%/yr -> ${(100 * shortW.dt.rate).toFixed(2)}%/yr`);
  check('the short window has its own (smaller) no-baseline set',
    shortW.noBase === 11, `${shortW.noBase}`);
  check('the legend label follows the window', /2019/.test(shortW.label), shortW.label);
  check('the off-scale swatch follows the window', /No 2019 baseline/.test(shortW.aside));

  // Returning to Current lands on the prisms, never Glass — the Detail
  // selector is hidden in Change, so restoring Glass would drop you somewhere
  // you cannot see you are.
  await page.click('#moneymode button[data-moneymode="current"]');
  await page.waitForTimeout(1000);
  const back = await page.evaluate(() => ({
    view: state.view,
    winShown: getComputedStyle(document.getElementById('chgwindow')).display !== 'none',
    moneyBtnActive: document.querySelector('#views button[data-view="money"]').classList.contains('active'),
  }));
  check('leaving the lens returns to the Money prisms', back.view === 'money', back.view);
  check('the window picker hides again outside the lens', !back.winShown);
  check('the Money view button stays active throughout the lens', back.moneyBtnActive);
  await page.close();

  // ---- 6. PUBLIC build carries the lens (promoted 2026-07-31) -------------
  // Was "FULL-only". DECISIONS.md 2026-07-31 promoted the change sub-mode to
  // the public build, so both checks are inverted deliberately.
  //
  // ⚠️ The window picker is checked AFTER entering change mode. The old
  // negative assertion passed for the wrong reason: #chgwindow is hidden in
  // Money/current regardless of build, so `!win` was true even in the full
  // build and the check never exercised the gate it claimed to.
  const pub = await open(url + '?build=public', { width: 1440, height: 900 });
  const shownIn = i => {
    const el = document.getElementById(i);
    return !!el && getComputedStyle(el).display !== 'none';
  };
  const p = await pub.evaluate((src) => {
    const shown = eval('(' + src + ')');
    return { mode: shown('moneymode'), win: shown('chgwindow'),
             hasFn: typeof changeFor === 'function' };
  }, shownIn.toString());
  check('public build offers the Money lens toggle', p.mode);
  check('public build has the change fn', p.hasFn);
  check('public build hides the window picker until change mode', !p.win);

  const p2 = await pub.evaluate((src) => {
    const shown = eval('(' + src + ')');
    applyMoneyMode('change');
    return { win: shown('chgwindow'), view: state.view };
  }, shownIn.toString());
  check('public build enters change mode', p2.view === 'change');
  check('public build reveals the window picker in change mode', p2.win);
  await pub.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

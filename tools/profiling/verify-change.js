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
//   4. **SIGNED PRISMS on ONE SHARED elevation scale** (2026-08-26 — replaces
//      the flat plane this lens shipped with). Gaining hoods rise, losing
//      hoods sink below the plane. The scale is the thing that fails silently:
//      giving each arm its own would draw a −5%/yr loss and a +34%/yr gain as
//      visibly equal bars, so metres-per-point is asserted EQUAL across the
//      two arms, and the deepest/tallest ratio is checked against the raw
//      file. The 46 degenerate hoods must be FLAT (0), not absent.
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

  // ---- 0. THE LENS TOGGLE IS VALUE'S ROW 2 (moved 2026-08-01) -------------
  // It used to be a "Lens" section in the Options panel, offered under either
  // quantity. It is now #toggle's second row under VALUE, exclusive with the
  // revenue cuts — the change lens reads share of the assessment BASE, which
  // Revenue does not own. Load lands on Revenue, so it starts hidden.
  check('the lens toggle is HIDDEN under Revenue', !(await vis('moneymode')));
  check('the revenue cuts show under Revenue', await vis('revcut'));
  check('the lens toggle lives in #toggle, not the Options panel',
    await page.evaluate(() => document.getElementById('moneymode').parentElement.id === 'toggle'));
  check('the orphaned "Lens" header is gone from the Options panel',
    await page.evaluate(() => !document.getElementById('moneymode-hd')));

  await page.click('#metric-row button[data-metric="value"]');
  await page.waitForTimeout(600);
  check('*** the lens toggle is revealed under Value ***', await vis('moneymode'));
  check('the revenue cuts hide under Value — exactly one row 2 at a time',
    !(await vis('revcut')));
  check('window picker stays hidden outside the change lens', !(await vis('chgwindow')));

  await page.click('#moneymode button[data-moneymode="change"]');
  await page.waitForTimeout(1200);

  // Hiding #toggle in the change view would strand you there: the only way
  // back to Current is the row the pod now hosts.
  check('*** #toggle survives into the change view ***', await vis('toggle'));
  check('the lens toggle is reachable inside the change view', await vis('moneymode'));

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
      lastYear: ys[j],
      elapsed: ys[j] - ys[i],          // 14 — the honest divisor
      intervals: j - i,                // 12 — the trap
      compoundElapsed: Math.pow(last / first, 1 / (ys[j] - ys[i])) - 1,
      compoundIntervals: Math.pow(last / first, 1 / (j - i)) - 1,
      arithmeticElapsed: (last / first - 1) / (ys[j] - ys[i]),
    };
  });
  const app = await page.evaluate(() => changeFor('DOWNTOWN'));
  // 13 -> 14 elapsed on 2026-08-27: the endpoint moved to 2026 and 2025 joined
  // 2024 in the omitted set, so the hole between the divisors WIDENED from one
  // year to two. That makes this check's subject bigger, not stale — the
  // interval divisor now overstates every rate by ~17%.
  check('the long window spans 14 elapsed years but only 12 observed intervals',
    raw.elapsed === 14 && raw.intervals === 12, `${raw.elapsed} vs ${raw.intervals}`);
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
  // DERIVED from the series endpoint, not the literal 2025 this pinned until
  // 2026-08-27 — the app already read the year from data, so the test was the
  // only stale half and it reddened on a roll-forward that broke nothing.
  check('the fell-to-zero hover states its own reason',
    new RegExp(`Holds none of the assessment base in ${raw.lastYear}`)
      .test(holes.sampleEndTip), holes.sampleEndTip);
  const legendAside = await page.evaluate(() =>
    document.querySelector('#legend .aside span:last-child').textContent);
  check('the legend swatch says "no baseline", not "set aside"',
    /No 2012 baseline/.test(legendAside) && !/set.aside/i.test(legendAside), legendAside);

  // ---- 4. signed prisms on one shared scale -------------------------------
  // Sampled through the layer's OWN live getElevation accessor, over the
  // layer's own data — the render's answer, not a re-derivation of the rule.
  const render = await page.evaluate(() => {
    const layers = overlay._props.layers;
    const prisms = layers.find(l => l.id === 'change-prisms');
    const bar = getComputedStyle(document.querySelector('#legend .bar')).backgroundImage;
    let up = 0, down = 0, flat = 0, tallest = 0, deepest = 0;
    let scalePos = null, scaleNeg = null;
    if (prisms) {
      const g = prisms.props.getElevation;
      for (const f of prisms.props.data.features) {
        const e = g(f);
        const c = changeFor(f.properties.neighbourhood_name);
        const rate = c && c.rate != null ? c.rate : null;
        if (e > 0) { up++; if (e > tallest) { tallest = e; scalePos = e / rate; } }
        else if (e < 0) { down++; if (e < deepest) { deepest = e; scaleNeg = e / rate; } }
        else flat++;
        // A degenerate hood (no baseline / no endpoint) must be flat, not tall.
        if (rate === null && e !== 0) flat = -1;
      }
    }
    return {
      ids: layers.map(l => l.id),
      extruded: prisms && prisms.props.extruded,
      pickable: prisms && prisms.props.pickable,
      hasHover: layers.some(l => l.id === 'hood-hover'),
      up, down, flat, tallest, deepest, scalePos, scaleNeg,
      barHead: bar.slice(0, 40), barTail: bar.slice(-40),
      neg: infillColorAt(-1), pos: infillColorAt(1),
    };
  });
  check('the change prisms are on the map', render.ids.includes('change-prisms'));
  check('they are EXTRUDED (2026-08-26 — the lens shipped flat)',
    render.extruded === true, `extruded=${render.extruded}`);
  check('gaining hoods rise AND losing hoods sink below the plane',
    render.up > 0 && render.down > 0, `up=${render.up} down=${render.down}`);
  check('the degenerate hoods are FLAT, not absent and not tall',
    render.flat > 0, `flat=${render.flat}`);
  // ⚠️ The silent failure this lens is exposed to: someone "fixing" the visual
  // asymmetry by scaling each arm to its own p95, which would draw a small
  // loss and a large gain as equal bars. Metres per point of rate must match.
  check('ONE shared elevation scale — metres per point are equal on both arms',
    render.scalePos != null && render.scaleNeg != null &&
    Math.abs(render.scalePos - render.scaleNeg) < 1e-6,
    `pos=${render.scalePos} neg=${render.scaleNeg}`);
  check('the prisms carry the tooltip themselves', render.pickable === true);
  check('no flat hover layer steals picks from the prisms', !render.hasHover);
  check('no money prisms survive into the change lens',
    !render.ids.some(i => /metric-extrusion|glass|uses-res-prisms|top-edges/.test(i)),
    render.ids.join(','));
  check('the legend bar diverges: losing arm at 0%',
    render.barHead.includes(`rgb(${render.neg.join(', ')})`), render.barHead);
  check('the legend bar diverges: gaining arm at 100%',
    render.barTail.includes(`rgb(${render.pos.join(', ')})`), render.barTail);

  // The down arm must stay VISIBLE, not merely present: on one shared scale a
  // lopsided distribution can render every loss as a scratch. Checked against
  // the raw file's own ratio, so it tracks the data rather than a hardcoded
  // expectation of it.
  const armRatio = await page.evaluate(() => {
    const rates = state.data.features
      .map(f => changeFor(f.properties.neighbourhood_name))
      .map(c => c && c.rate).filter(v => v != null);
    return Math.abs(Math.min(...rates)) / Math.max(...rates);
  });
  check('the deepest prism is a readable fraction of the tallest',
    Math.abs(render.deepest) / render.tallest > 0.15 &&
    Math.abs(Math.abs(render.deepest) / render.tallest - armRatio) < 1e-6,
    `rendered=${(100 * Math.abs(render.deepest) / render.tallest).toFixed(1)}% ` +
    `file=${(100 * armRatio).toFixed(1)}%`);

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
  check(`the short window spans ${raw.lastYear - 2019} elapsed years (2019-${raw.lastYear})`,
    shortW.dt.years === raw.lastYear - 2019 && shortW.dt.from === 2019,
    `${shortW.dt.from}, ${shortW.dt.years} yr`);
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

  // Picking Revenue while the change lens is up must LEAVE it. Revenue owns no
  // change lens, so without this the pod would show Revenue lit over a map
  // still drawing share-of-base movement.
  await page.click('#moneymode button[data-moneymode="change"]');
  await page.waitForTimeout(1000);
  await page.click('#metric-row button[data-metric="revenue"]');
  await page.waitForTimeout(1000);
  const viaRev = await page.evaluate(() => ({
    view: state.view,
    metric: state.metric,
    title: document.getElementById('title-h').textContent,
    cuts: getComputedStyle(document.getElementById('revcut')).display !== 'none',
    mode: getComputedStyle(document.getElementById('moneymode')).display !== 'none',
  }));
  check('*** picking Revenue leaves the change view ***', viaRev.view === 'money', viaRev.view);
  check('Revenue restores the last cut', viaRev.metric === 'revenue_per_acre', viaRev.metric);
  check('the title follows the metric out of the lens', /revenue/i.test(viaRev.title), viaRev.title);
  check('the cut row is back and the lens row is gone', viaRev.cuts && !viaRev.mode);
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
    const hiddenUnderRevenue = !shown('moneymode');
    applyMetric('value_per_acre');
    return { hiddenUnderRevenue, mode: shown('moneymode'), win: shown('chgwindow'),
             hasFn: typeof changeFor === 'function' };
  }, shownIn.toString());
  check('public build hides the lens toggle under Revenue', p.hiddenUnderRevenue);
  check('public build offers the Money lens toggle under Value', p.mode);
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

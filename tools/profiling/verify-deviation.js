// Verify the Lab and its first experiment, the deviation lens ("vs peer
// average" — revenue per DEVELOPED acre, population per cut). Full build only.
//
// The six things that fail SILENTLY here, in order of how badly:
//   0. the denominator slips back to BOUNDARY acres, which does not crash but
//      moves the zero line ~47% and reclassifies 127 hoods from below-average
//      to above; or a banded hood draws a solid prism and so asserts a value
//      the roll cannot support;
//   1. the citywide average is recomputed from an external levy total instead
//      of the served features, moving the zero line and reclassifying hoods;
//   2. the Lab borrows Money's state.metric instead of its own state.labCut —
//      entering from the Value map would then average ASSESSED VALUE and label
//      the result revenue, with nothing on screen to give it away;
//   3. the deficit prisms do not actually extrude downward (deck.gl clamping a
//      negative getElevation at 0 would leave a map that looks fine and says
//      nothing);
//   4. the Lab leaks into the public build.
// Each gets an assertion against numbers re-derived in the page, not pinned.
const { chromium } = require('playwright');

const EPS = 1e-6;
let failures = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) failures++;
};

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  // --- full build --------------------------------------------------------
  await page.goto('http://localhost:8777/index.html?build=full', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3500);

  // The Lab is its own top-level #views button, NOT a mode of Money — that
  // separation is the whole point of the container and is asserted, not assumed.
  const btn = page.locator('#views button[data-view="lab"]');
  check('Lab is a top-level #views button', await btn.count() === 1);
  check('Lab button is visible in the full build', await btn.isVisible());
  check('Lab button carries a beta tag', (await btn.innerText()).toLowerCase().includes('beta'));
  check('Lab is NOT a mode of Money',
    await page.locator('#moneymode button[data-moneymode="deviation"]').count() === 0);
  check('#moneymode is untouched: hidden under Revenue as before',
    !(await page.locator('#moneymode').isVisible()));

  await btn.click();
  await page.waitForTimeout(1200);
  // Shot taken HERE, not at the end: the last assertions deliberately leave the
  // page on the Value map, and a screenshot named deviation.png showing some
  // other lens is worse than no screenshot.
  await page.screenshot({ path: 'deviation.png' });

  const st = await page.evaluate(() => {
    const feats = state.data.features.map(f => f.properties);
    return {
      view: state.view,
      title: document.getElementById('title-h').textContent,
      blurb: document.getElementById('title-p').textContent,
      legend: document.getElementById('legend-label').textContent,
      legendMin: document.getElementById('legend-min').textContent,
      legendMax: document.getElementById('legend-max').textContent,
      moneyBtnActive: document.querySelector('#views button[data-view="money"]').classList.contains('active'),
      labBtnActive: document.querySelector('#views button[data-view="lab"]').classList.contains('active'),
      toggleShown: getComputedStyle(document.getElementById('toggle')).display !== 'none',
      pickShown: getComputedStyle(document.getElementById('labpick')).display !== 'none',
      labVariants: LAB_VIEWS.length,
      labCut: state.labCut,
      moneyMetric: state.metric,
      stats: deviationStats(),
      // Re-derive the average here, independently of the page's own helper.
      // ⚠️ DEVELOPED acres, area x (1 - set_aside_frac), over the CUT'S OWN
      // population — set-aside hoods and the wrong side of the residential
      // split are out of both sides. Written out longhand rather than calling
      // inDeviationPop/deviationRate so this stays an independent oracle and
      // not a restatement of the code it checks.
      indep: (() => {
        const cut = state.labCut;
        const pop = p => cut === 'res_revenue_per_acre' ? p.is_residential === true
          : cut === 'nonres_revenue_per_acre' ? p.is_residential === false : true;
        let rev = 0, acres = 0, devAcres = 0, n = 0;
        for (const p of feats) {
          if (!p.revenue_per_acre || p.total_revenue == null) continue;
          const frac = 1 - (p.set_aside_frac || 0);
          if (p.is_set_aside || frac <= 0 || p[cut] == null || !pop(p)) continue;
          const a = p.total_revenue / p.revenue_per_acre;
          rev += p[cut] * a;
          acres += a;
          devAcres += a * frac;
          n++;
        }
        return { avg: rev / devAcres, acres, devAcres, rev, n,
                 setAside: feats.filter(p => p.is_set_aside).length,
                 notSetAside: feats.filter(p => !p.is_set_aside).length };
      })(),
      // The boundary-acre average the lens used before 2026-08-12, kept as the
      // specific wrong answer to guard against: it is what the page reports if
      // the denominator ever slips back to area_acres.
      boundaryAvg: (() => {
        let rev = 0, acres = 0;
        for (const p of feats) {
          if (!p.revenue_per_acre || p.total_revenue == null) continue;
          rev += p.total_revenue;
          acres += p.total_revenue / p.revenue_per_acre;
        }
        return rev / acres;
      })(),
      // Elevation is read off the LIVE LAYER's accessor, not recomputed here —
      // that is what makes "the deficit really extrudes downward" a claim about
      // what deck.gl was handed rather than about our arithmetic.
      elev: (() => {
        const layer = overlay._props.layers.find(l => l.id === 'deviation-extrusion');
        const get = layer.props.getElevation;
        let negative = 0, positive = 0, setAsideNonZero = 0;
        let minValue = Infinity, maxValue = -Infinity;
        for (const f of state.data.features) {
          const z = get(f);
          if (f.properties.is_set_aside) { if (z !== 0) setAsideNonZero++; continue; }
          if (z < 0) negative++; else if (z > 0) positive++;
          minValue = Math.min(minValue, z);
          maxValue = Math.max(maxValue, z);
        }
        return { negative, positive, setAsideNonZero, minValue, maxValue,
                 scored: negative + positive, scale: layer.props.elevationScale };
      })(),
    };
  });

  check('Lab opens its first experiment', st.view === 'deviation', st.view);
  check('the Lab #views button is the active one', st.labBtnActive);
  check('Money is NOT left active', !st.moneyBtnActive);
  check('the metric pod is hidden in the Lab', !st.toggleShown);
  check('the experiment picker stays hidden while there is only one',
    st.labVariants === 1 ? !st.pickShown : st.pickShown,
    `${st.labVariants} experiment(s), picker ${st.pickShown ? 'shown' : 'hidden'}`);
  check('title names the comparison',
    /vs the City Average|vs Residential Peers|vs Non-Residential Peers/i.test(st.title), st.title);
  check('title names the DEVELOPED-acre denominator',
    /per Developed Acre/i.test(st.title), st.title);

  // 1 — the average comes from the served features.
  check('peer average == sum(dollars) / sum(DEVELOPED acres) over the cut population',
    Math.abs(st.stats.avg - st.indep.avg) < EPS,
    `page ${st.stats.avg.toFixed(6)} vs independent ${st.indep.avg.toFixed(6)}`);
  // Guards the specific wrong answer: the City's budgeted levy over the same
  // acres. If someone swaps the numerator this is what the average becomes.
  const budgetAvg = 2317789000 / st.indep.acres;
  check('average is NOT the external budgeted-levy figure',
    Math.abs(st.stats.avg - budgetAvg) > 1,
    `modelled ${st.stats.avg.toFixed(0)} vs budgeted-levy ${budgetAvg.toFixed(0)}`);
  // ⚠️ The regression this change exists to prevent. Held-out land is 33% of
  // Edmonton's acreage and 0.65% of its revenue, so a denominator that slips
  // back to boundary acres does not crash — it quietly moves the zero line
  // down ~47% and reclassifies 127 hoods from below-average to above.
  check('average is NOT the old boundary-acre figure',
    st.stats.avg - st.boundaryAvg > 1000,
    `developed ${st.stats.avg.toFixed(0)} vs boundary ${st.boundaryAvg.toFixed(0)}`);
  check('developed acres are a strict subset of boundary acres',
    st.indep.devAcres > 0 && st.indep.devAcres < st.indep.acres,
    `${st.indep.devAcres.toFixed(0)} developed of ${st.indep.acres.toFixed(0)} boundary`);
  // The population is the cut's own, not the whole city: Total scores every
  // developed hood, the two split cuts score only their own half.
  check('the scored population matches the independent count',
    st.stats.scored === st.indep.n, `page ${st.stats.scored} vs independent ${st.indep.n}`);
  check('set-aside hoods are OUT of the average, not merely off the scale',
    st.indep.n <= st.indep.notSetAside && st.indep.setAside > 0,
    `${st.indep.n} scored, ${st.indep.setAside} set aside`);

  // --- the institutional uncertainty band --------------------------------
  // ⚠️ The band exists because the roll does not publish exemption status, so
  // the FAILURE MODE IS EDITORIAL as much as numeric: a banded hood must not
  // assert a value, and the copy must not imply the low end is the true one.
  const band = await page.evaluate(() => {
    const hi = overlay._props.layers.find(l => l.id === 'deviation-band-levied');
    const lo = overlay._props.layers.find(l => l.id === 'deviation-band-exempt');
    const main = overlay._props.layers.find(l => l.id === 'deviation-extrusion');
    if (!hi || !lo) return { missing: true };
    let drawn = 0, crossZero = 0, stillExtruded = 0, wrongOrder = 0, unbandedDrawn = 0, inverted = 0;
    for (const f of state.data.features) {
      const b = deviationBand(f.properties);
      const a = hi.props.getElevation(f), c = lo.props.getElevation(f);
      if (b) {
        drawn++;
        if (a > 0 && c < 0) crossZero++;
        if (main.props.getElevation(f) !== 0) stillExtruded++;
        // ⚠️ NOT "exempt <= levied" — that is FALSE and an earlier version of
        // this check asserted it. Removing institutional revenue also drops
        // the citywide average, so a hood losing less than the city gains
        // ground (EVERGREEN +$87, RIVER VALLEY CAMERON +$842). The real
        // invariant is on REVENUE, not on the deviation: the exempt rate can
        // never exceed the levied rate for the same hood.
        if (deviationRateExempt(f.properties) > deviationRate(f.properties) + 1e-6) wrongOrder++;
        if (c > a) inverted++;
      } else if (a !== 0 || c !== 0) unbandedDrawn++;
    }
    const s = deviationStats();
    const ua = state.data.features.find(f =>
      f.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    // Every hood that would have been banded on SHARE alone, split by whether
    // the consequence cut kept it — the 2026-08-15 narrowing.
    const shareTier = state.data.features.filter(f =>
      inDeviationPop(f.properties) && instFrac(f.properties) >= INST_UNCERTAIN_MIN);
    const invertedAnywhere = shareTier.filter(f => {
      const b = deviationBandRaw(f.properties);
      return b.exempt > b.levied;
    });
    return { drawn, crossZero, stillExtruded, wrongOrder, unbandedDrawn, inverted,
             banded: deviationBandedCount(), avg: s.avg, avgExempt: s.avgExempt,
             shareTier: shareTier.length,
             caveatOnly: shareTier.filter(f => instCaveatOnly(f.properties)).length,
             invertedAnywhere: invertedAnywhere.length,
             invertedAndBanded: invertedAnywhere.filter(f => isUncertain(f.properties)).length,
             crossersNotBanded: shareTier.filter(f => {
               const b = deviationBandRaw(f.properties);
               return (b.levied > 0) !== (b.exempt > 0) && !isUncertain(f.properties);
             }).length,
             caveatTip: (() => {
               const f = shareTier.find(x => instCaveatOnly(x.properties));
               return f ? viewTooltip({ object: f }).html : '';
             })(),
             hiFilled: hi.props.filled, hiWireframe: hi.props.wireframe,
             bandColor: hi.props.getLineColor,
             bandedFill: (() => {
               const f = state.data.features.find(x => deviationBand(x.properties));
               return f ? main.props.getFillColor(f) : null;
             })(),
             tip: ua ? viewTooltip({ object: ua }).html : '' };
  });
  check('the band layers exist', !band.missing);
  check('every banded hood draws a band', band.drawn === band.banded && band.drawn > 0,
    `${band.drawn} drawn, ${band.banded} banded`);
  check('NO un-banded hood draws a band', band.unbandedDrawn === 0, `${band.unbandedDrawn}`);
  // ⚠️ THE "REPLACED, NOT ANNOTATED" RULE. A banded hood that still extrudes a
  // solid prism would assert the modelled value and contradict its own band.
  check('*** a banded hood draws NO solid prism ***', band.stillExtruded === 0,
    `${band.stillExtruded} banded hoods still extruded`);
  check('the exempt RATE never exceeds the levied rate', band.wrongOrder === 0,
    `${band.wrongOrder} inverted`);

  // --- the band is its own hover target (2026-08-17) -----------------------
  // ⚠️ THE OUTLINE LAYERS CANNOT OWN THE PICKING and must not be made to: with
  // filled:false the only pickable surface is the 2px wireframe, and turning
  // their fill on — even at alpha 0 — costs 499 px of render, because a
  // depth-writing fill hides the prism's OWN back edges and the see-through
  // cage that lets you read both endpoints becomes a box. The hover target is
  // therefore a separate invisible solid with depthMask off. What fails
  // silently if that regresses: the pointer sits on a banded hood's geometry
  // and the tooltip names a DIFFERENT hood (pre-fix, at pitch 60, the U of A's
  // prism picked WÎHKWÊNTÔWIN) — which on this lens is the wrong hood's
  // uncertainty range.
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
    const hits = [];
    for (let dy = -30; dy >= -200; dy -= 10) {
      const i = overlay._deck.pickObject({ x: Math.round(sx), y: Math.round(sy + dy), radius: 0 });
      if (i) hits.push({ layer: i.layer.id, hood: i.object.properties.neighbourhood_name });
    }
    const outlines = overlay._props.layers.filter(
      l => /^deviation-band-(levied|exempt)$/.test(l.id));
    const targets = overlay._props.layers.filter(l => l.id.includes('band-pick'));
    return { hits,
             outlinesPickable: outlines.map(l => !!l.props.pickable),
             targetsPickable: targets.map(l => !!l.props.pickable),
             targetFillAlpha: targets.map(l => l.props.getFillColor[3]),
             depthMask: targets.map(l => l.props.parameters && l.props.parameters.depthMask),
             targetRows: targets.map(l => l.props.data.length) };
  });
  const onBand = pick.hits.filter(h => h.layer.includes('band-pick'));
  check('*** the band prism BODY is pickable, not just the flat below it ***',
    onBand.length > 0, `${onBand.length} of ${pick.hits.length} sampled pixels`);
  check('*** every pick on the band returns ITS OWN hood ***',
    onBand.length > 0 && onBand.every(h => h.hood === 'UNIVERSITY OF ALBERTA'),
    [...new Set(onBand.map(h => h.hood))].join(', ') || 'none');
  check('the OUTLINE layers stay unpickable (their fill must stay off)',
    pick.outlinesPickable.length === 2 && !pick.outlinesPickable.some(Boolean),
    JSON.stringify(pick.outlinesPickable));
  // ⚠️ Length asserted explicitly: every `.every()` below is vacuously true on
  // an empty array, so without this the whole group passes on a build that
  // ships no pick targets at all.
  check('both pick targets exist and are pickable',
    pick.targetsPickable.length === 2 && pick.targetsPickable.every(Boolean),
    JSON.stringify(pick.targetsPickable));
  check('the pick targets are invisible', pick.targetFillAlpha.every(a => a === 0),
    JSON.stringify(pick.targetFillAlpha));
  // depthMask:false is what keeps an invisible solid from occluding the
  // outlines behind it. depthTest stays ON — a prism genuinely in front must
  // still win the pick.
  check('the pick targets write no depth', pick.depthMask.every(d => d === false),
    JSON.stringify(pick.depthMask));
  // Filtered to the banded hoods: at 406 rows these height-0 transparent
  // targets would win the pick from deviation-extrusion over every certain
  // hood, which DOES autoHighlight — so every hood in the Lab would silently
  // stop lighting up on hover.
  check('the pick targets carry only the banded hoods',
    pick.targetRows.every(n => n === band.drawn), `${pick.targetRows} vs ${band.drawn} banded`);

  // ⚠️ THE GLOW IS WHY THE TARGETS ARE INDEX-DRIVEN RATHER THAN autoHighlight,
  // and this lens is where the difference is stark. A crossing band's exempt
  // endpoint extrudes DOWNWARD, mostly underground, and it is the last pickable
  // layer drawn — so it wins the pick, and autoHighlight would then light 276
  // px against the levied prism's 19,654. Lighting BOTH by index also keeps the
  // no-primacy rule: neither unknowable world may be singled out.
  const glow = await page.evaluate(() => {
    // ⚠️ Report a MISSING handler as a failed check, not a stack trace: a
    // build without it should say which contract broke.
    if (typeof bandHover !== 'function') return { absent: true };
    const tg = () => overlay._deck.props.layers.filter(l => l.id.includes('band-pick'));
    const idxs = () => tg().map(l => l.props.highlightedObjectIndex);
    const lev = tg().find(l => l.id === 'deviation-band-pick-levied');
    const i = lev.props.data.findIndex(
      f => f.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    const before = idxs();
    bandHover({ picked: true, index: i, layer: { id: 'deviation-band-pick-exempt' } });
    const during = idxs();
    bandHover({ picked: false, layer: null });
    return { i, before, during, off: idxs(),
             hood: lev.props.data[i].properties.neighbourhood_name,
             colors: tg().map(l => l.props.highlightColor.join(',')) };
  });
  check('the band hover handler EXISTS', !glow.absent);
  check('*** the hidden endpoint winning the pick still lights BOTH ***',
    !glow.absent && glow.during.length === 2 && glow.during.every(v => v === glow.i),
    `${JSON.stringify(glow.during)} for index ${glow.i} (${glow.hood})`);
  check('the Lab glow is the same white as every other prism',
    !glow.absent && glow.colors.length === 2 && glow.colors.every(c => c === '255,255,255,60'), glow.colors.join(' | '));
  check('the Lab band is unlit at rest and goes out again',
    !glow.absent && glow.before.length === 2 && glow.before.every(v => v === -1) && glow.off.every(v => v === -1),
    `${JSON.stringify(glow.before)} -> ${JSON.stringify(glow.off)}`);
  // ⚠️ THE INVERSION MOVED, IT DID NOT GO AWAY. Until 2026-08-15 this asserted
  // that at least one DRAWN band inverts (EVERGREEN +$87, RIVER VALLEY CAMERON
  // +$842), which justified deviationBandSpan sorting for display. The
  // consequence cut drops exactly those hoods, and that is structural, not
  // luck: a band inverts only when the hood loses LESS than the $1,303/acre the
  // citywide average loses, so its span is under $1,303 against clamps of
  // $21,470/$48,047 — Δt < 0.061, never the 0.25 required to draw. So the
  // inversion still exists in the DATA and must never be drawn.
  check('inverted bands still exist in the share tier', band.invertedAnywhere > 0,
    `${band.invertedAnywhere} invert`);
  check('*** no INVERTED band is ever drawn (Δt < 0.061 < 0.25) ***',
    band.invertedAndBanded === 0, `${band.invertedAndBanded} drawn`);
  check('no drawn band inverts', band.inverted === 0, `${band.inverted} of ${band.drawn}`);
  // The consequence cut narrows the set; the caveat must not narrow with it.
  check('the consequence cut is a strict subset of the share tier',
    band.drawn < band.shareTier && band.drawn > 0, `${band.drawn} of ${band.shareTier}`);
  check('every share-tier hood it drops still gets the WORDS',
    band.caveatOnly === band.shareTier - band.drawn, `${band.caveatOnly} caveat-only`);
  check('a caveat-only hood names the zoning share and the unpublished status',
    /institutionally-zoned land/.test(band.caveatTip)
    && /does not publish which of it is tax-exempt/.test(band.caveatTip));
  // Δt >= 0.25 contains every zero-crossing band today. A crossing band with
  // both endpoints near zero would flip the lens's above/below claim while
  // moving nothing visible; none exists, and this is how we hear about the
  // first one instead of shipping it silently.
  check('no zero-crossing band is dropped by the consequence cut',
    band.crossersNotBanded === 0, `${band.crossersNotBanded} dropped`);
  check('some bands cross the ground plane', band.crossZero > 0, `${band.crossZero}`);
  // Outline only: a solid endpoint gives one of two unknowable worlds primacy.
  check('band endpoints are OUTLINE ONLY (filled:false, wireframe:true)',
    band.hiFilled === false && band.hiWireframe === true,
    `filled=${band.hiFilled} wireframe=${band.hiWireframe}`);
  // Both sides move together — the low endpoint is scored against the exempt
  // average, not the levied one. Mixing them is the cross-universe error.
  check('the exempt-scenario average is lower than the levied one',
    band.avgExempt < band.avg && band.avgExempt > 0,
    `exempt ${band.avgExempt.toFixed(0)} vs levied ${band.avg.toFixed(0)}`);
  // ⚠️ THE WORDING RULE MADE VISUAL. A tinted band leans toward a pole and so
  // asserts the direction the copy is forbidden to assert. Amber shipped first
  // and measured ΔE 9.5 against the deficit orange under NORMAL vision (floor
  // 15), i.e. the "unknown" hoods read as "below average" to everyone.
  check('*** the band colour is ACHROMATIC (cannot imply a pole) ***',
    band.bandColor && band.bandColor[0] === band.bandColor[1] &&
    band.bandColor[1] === band.bandColor[2],
    `rgb(${(band.bandColor || []).slice(0, 3).join(',')})`);
  // A filled floor under a hollow prism reads as a value the hood does not have.
  check('a banded hood has NO fill under it', band.bandedFill && band.bandedFill[3] === 0,
    `alpha ${(band.bandedFill || [])[3]}`);

  const tipText = band.tip.replace(/<[^>]+>/g, ' ');
  check('a banded tooltip prints a RANGE, not a single value', / to /.test(tipText), tipText.slice(0, 90));
  // ⚠️ The locked wording rule: never "revenue lost" / "uncollected", and no
  // claim about which end is true (DECISIONS.md 2026-08-08).
  check('*** the band copy asserts NO direction ***',
    !/lost|uncollect|foregone|should be|really|actually/i.test(tipText), tipText.slice(0, 120));

  // 2 — the deficit half really extrudes below the plane.
  check('some hoods extrude BELOW the ground plane', st.elev.negative > 0,
    `${st.elev.negative} negative of ${st.elev.scored} scored`);
  check('some hoods extrude above', st.elev.positive > 0, `${st.elev.positive}`);
  check('set-aside hoods are flat', st.elev.setAsideNonZero === 0,
    `${st.elev.setAsideNonZero} set-aside hoods with non-zero height`);
  // True-to-scale, and the floor is a BOUND rather than an observed value: no
  // hood can dive past -average (revenue per acre cannot be negative), and the
  // deepest one gets close because the quietest hoods sit near $0/acre. Both
  // halves matter — a breach means the arithmetic is wrong, and a deepest dive
  // far short of the floor would mean the blurb overstates the range.
  check('no hood dives past the -average floor',
    st.elev.minValue >= -st.stats.avg - EPS,
    `min ${st.elev.minValue.toFixed(0)} vs floor ${(-st.stats.avg).toFixed(0)}`);
  check('the deepest deficit reaches the floor within 1%',
    Math.abs(st.elev.minValue - -st.stats.avg) < 0.01 * st.stats.avg,
    `min ${st.elev.minValue.toFixed(0)} vs floor ${(-st.stats.avg).toFixed(0)}`);
  check('surplus arm dwarfs deficit arm (true to scale)',
    st.elev.maxValue > 5 * Math.abs(st.elev.minValue),
    `+${st.elev.maxValue.toFixed(0)} vs ${st.elev.minValue.toFixed(0)}`);

  // 3 — copy honesty. The lens must never be named as a cost comparison.
  const copy = (st.title + ' ' + st.blurb + ' ' + st.legend).toLowerCase();
  check('blurb disclaims the cost reading', /not a cost-of-service comparison/.test(copy));
  check('blurb marks it experimental', /experimental/.test(copy));
  check('blurb states the floor', /floor/.test(copy));
  check('no "cost of service" / "COSA" naming of the lens itself',
    !/\bcosa\b/.test(copy) && !/cost of service/.test(copy), copy.slice(0, 120));
  check('legend names the average it measures against',
    /peer average/i.test(st.legend) && /\$/.test(st.legend), st.legend);
  check('legend names the DEVELOPED-acre denominator',
    /developed acre/i.test(st.legend), st.legend);
  check('legend ends are signed', st.legendMin.includes('−$') && st.legendMax.includes('+$'),
    `${st.legendMin} | ${st.legendMax}`);

  // Tooltip prints both terms, so the signed number is checkable — and the
  // check is that the two printed terms ACTUALLY RECONCILE to the bold one.
  // ⚠️ The failure this exists for is silent: the served column is per
  // BOUNDARY acre while the average is per DEVELOPED acre, so printing
  // p[state.labCut] beside it renders two numbers whose difference is not the
  // bold number, on every hood with any held-out land.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(x => !x.properties.is_set_aside &&
      (x.properties.set_aside_frac || 0) > 0.05);
    const p = f.properties;
    const html = viewTooltip({ object: f }).html;
    // Sign-aware: fmtDeviation carries the minus OUTSIDE the dollar sign
    // ("−$4,120"), and it is the U+2212 minus, not a hyphen.
    const nums = [...html.matchAll(/([+−-]?)\$([\d,]+)/g)]
      .map(m => (m[1] === '−' || m[1] === '-' ? -1 : 1) * +m[2].replace(/,/g, ''));
    return { html, nums, rate: deviationRate(p), avg: deviationStats().avg,
             d: deviationOf(p), raw: p[state.labCut] };
  });
  check('tooltip prints the hood value AND the peer average',
    /here/.test(tip.html) && /across/.test(tip.html),
    tip.html.replace(/<[^>]+>/g, ' ').slice(0, 110));
  check('the two printed terms reconcile to the signed number',
    tip.nums.length === 3 && Math.abs((tip.nums[1] - tip.nums[2]) - tip.nums[0]) <= 2,
    `${tip.nums[1]} − ${tip.nums[2]} vs ${tip.nums[0]}`);
  check('tooltip shows the DEVELOPED rate, not the served boundary rate',
    Math.abs(tip.nums[1] - tip.rate) < 1 && tip.rate > tip.raw,
    `printed ${tip.nums[1]}, developed ${tip.rate.toFixed(0)}, served ${tip.raw.toFixed(0)}`);

  // 2 — the Lab keeps its OWN cut. Money's metric must be untouched by it.
  check('the Lab reads state.labCut, not state.metric',
    st.labCut === 'revenue_per_acre' && st.moneyMetric === 'revenue_per_acre',
    `labCut ${st.labCut}, metric ${st.moneyMetric}`);

  // Switching the revenue cut must re-render, not just repaint the buttons.
  const before = st.stats.avg;
  await page.locator('#labcut button[data-labcut="res_revenue_per_acre"]').click();
  await page.waitForTimeout(900);
  const after = await page.evaluate(() => ({
    avg: deviationStats().avg,
    title: document.getElementById('title-h').textContent,
    view: state.view,
    metric: state.metric,
  }));
  check('revenue cut re-renders the lens', Math.abs(after.avg - before) > 1 && after.view === 'deviation',
    `total ${before.toFixed(0)} -> residential ${after.avg.toFixed(0)}`);
  check('title follows the cut', /Residential/i.test(after.title), after.title);
  check("the Lab's cut does NOT move Money's metric",
    after.metric === 'revenue_per_acre', after.metric);

  // ⚠️ THE POPULATION FOLLOWS THE CUT. On the residential cut a NON-residential
  // hood must be null — off the scale, flat, and out of the average — because
  // a citywide residential average is diluted by industrial land that levies
  // almost no residential tax, which let nearly every residential hood clear a
  // bar that was never about it. Asserted on the live elevation accessor, so
  // it is a claim about what deck.gl was handed.
  const pop = await page.evaluate(() => {
    const layer = overlay._props.layers.find(l => l.id === 'deviation-extrusion');
    const get = layer.props.getElevation;
    let resScored = 0, nonresScored = 0, nonresFlat = 0;
    for (const f of state.data.features) {
      const p = f.properties;
      if (p.is_set_aside) continue;
      const z = get(f);
      if (p.is_residential === true) { if (z !== 0) resScored++; }
      else if (z !== 0) nonresScored++; else nonresFlat++;
    }
    return { resScored, nonresScored, nonresFlat, scored: deviationStats().scored };
  });
  check('the residential cut scores ONLY residential hoods',
    pop.nonresScored === 0 && pop.resScored > 0,
    `${pop.resScored} residential scored, ${pop.nonresScored} non-residential scored`);
  check('non-residential hoods are flat under the residential cut',
    pop.nonresFlat > 0, `${pop.nonresFlat} flat`);
  check('the residential population is smaller than the total one',
    pop.scored < st.stats.scored, `${pop.scored} residential vs ${st.stats.scored} total`);

  // ⚠️ THE ONE THAT WOULD BE INVISIBLE: enter the Lab from the Value map. If
  // the lens read state.metric it would average value_per_acre (~$1.8M/acre)
  // and print it under a title saying "Revenue". The average must not move.
  const viaValue = await page.evaluate(async () => {
    await applyView('money');
    applyMetric('value_per_acre');
    await applyView('deviation');
    return { avg: deviationStats().avg, title: document.getElementById('title-h').textContent,
             cut: state.labCut, metric: state.metric };
  });
  check('*** entering the Lab from the Value map still averages REVENUE ***',
    Math.abs(viaValue.avg - after.avg) < EPS && viaValue.cut === 'res_revenue_per_acre',
    `avg ${viaValue.avg.toFixed(2)} on cut ${viaValue.cut} while Money holds ${viaValue.metric}`);
  check('the title does not claim a quantity it is not showing',
    /Revenue/i.test(viaValue.title) && !/Assessed Value/i.test(viaValue.title), viaValue.title);

  // --- public build ------------------------------------------------------
  await page.goto('http://localhost:8777/index.html?build=public', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  check('the Lab button is HIDDEN in the public build',
    !(await page.locator('#views button[data-view="lab"]').isVisible()));
  // ...and adding it changed nothing else about that row. Measured, not
  // assumed: the public build already hid services/ratio/uses on its own
  // (their own FULL_BUILD gates further down), so the published set is these
  // two — if a future gate moves, this catches it here rather than in
  // production.
  check('the public #views row is otherwise unchanged',
    await page.evaluate(() => [...document.querySelectorAll('#views button')]
      .filter(b => getComputedStyle(b).display !== 'none')
      .map(b => b.dataset.view).join(',')) === 'money,development');

  check('no page errors', errs.length === 0, errs.slice(0, 3).join(' | '));

  await browser.close();
  console.log(failures ? `\n${failures} FAILURE(S)` : '\nall checks passed');
  process.exit(failures ? 1 : 0);
})();

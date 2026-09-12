// Verify the Ratio view's denominator picker (2026-07-10): per-service
// ratios — revenue per road metre | per fire event (SPEC_utilities
// decision 3). DOM + layer-accessor level, against the real served file.
//   node verify-ratio-denom.js <url>
// Checks: control visibility gating, chrome/legend swap, independent
// anchor recomputation (log p2.5–p97.5 of each kept subset), height
// parity, fire-floor artifact greying, tooltip prose, persistence across
// views, residential-lens re-anchoring, and the institutional uncertainty
// band (2026-09-12) including the two 90%-exempt hoods a naive port of Money's
// consequence threshold would silently drop.
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
  const chrome = () => page.evaluate(() => ({
    title: document.getElementById('title-h').textContent,
    blurb: document.getElementById('title-p').textContent,
    legend: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    hdShown: document.getElementById('ratio-denom-hd').style.display !== 'none' &&
             getComputedStyle(document.getElementById('ratio-denom-hd')).display !== 'none',
    pickerShown: getComputedStyle(document.getElementById('ratio-denom')).display !== 'none',
    active: [...document.querySelectorAll('#ratio-denom button')]
      .find(b => b.classList.contains('active'))?.dataset.ratioDenom,
    ratioDenom: state.ratioDenom,
    view: state.view,
  }));

  // Independent anchors: same math as ratioScale, recomputed from raw
  // feature properties without touching ratioOf/ratioKept/ratioScale.
  const independent = (col, floor, resOnly) => page.evaluate(([col, floor, resOnly]) => {
    const vals = state.data.features.map(f => f.properties)
      .filter(p => !p.is_set_aside && p[col] != null && p[col] >= floor &&
                   p.revenue_per_acre != null && (!resOnly || p.is_residential))
      .map(p => p.revenue_per_acre / p[col]).sort((a, b) => a - b);
    const q = (s, x) => { const pos = (s.length - 1) * x, lo = Math.floor(pos), hi = Math.ceil(pos);
      return lo === hi ? s[lo] : s[lo] + (s[hi] - s[lo]) * (pos - lo); };
    return { n: vals.length, lo: q(vals, 0.025), hi: q(vals, 0.975), max: vals[vals.length - 1] };
  }, [col, floor, resOnly || false]);

  // 1. Money view (default): picker hidden.
  let c = await chrome();
  check('money: picker hidden', !c.hdShown && !c.pickerShown, JSON.stringify({ hd: c.hdShown, picker: c.pickerShown }));

  // 2. Enter Ratio: picker shown, roads default, roads chrome.
  await click('#views button[data-view="ratio"]');
  await page.waitForTimeout(5000); // roads lazy-fetch + rebuild
  c = await chrome();
  check('ratio: picker shown', c.hdShown && c.pickerShown);
  check('ratio: roads default active', c.active === 'roads' && c.ratioDenom === 'roads');
  check('ratio: roads title', c.title === 'Edmonton: Revenue per Road Metre', c.title);
  check('ratio: roads legend', c.legend === 'Revenue per road metre (log colour)', c.legend);
  check('ratio: roads aside', c.aside === 'Set aside / insufficient road base', c.aside);

  // 3. Roads legend anchors == independent p2.5/p97.5 of the roads kept subset.
  const roadsInd = await independent('road_m_per_acre', 5);
  check('roads legend min == p2.5',
    c.min === '≤ $' + Math.round(roadsInd.lo).toLocaleString(), `${c.min} vs ${Math.round(roadsInd.lo)}`);
  check('roads legend max == p97.5',
    c.max === '$' + Math.round(roadsInd.hi).toLocaleString() + '+', `${c.max} vs ${Math.round(roadsInd.hi)}`);

  // 4. Swap to fire: chrome + legend swap, anchors match the fire subset.
  await click('#ratio-denom button[data-ratio-denom="fire"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('fire: active + state', c.active === 'fire' && c.ratioDenom === 'fire');
  check('fire: title', c.title === 'Edmonton: Revenue per Fire Event', c.title);
  check('fire: legend', c.legend === 'Revenue per fire event (log colour)', c.legend);
  check('fire: aside', c.aside === 'Set aside / too few fire events', c.aside);
  check('fire: blurb says demand-not-coverage', /Demand,\s*not response coverage/.test(c.blurb));
  const fireInd = await independent('fire_events_per_acre', 0.005);
  check('fire legend min == p2.5',
    c.min === '≤ $' + Math.round(fireInd.lo).toLocaleString(), `${c.min} vs ${Math.round(fireInd.lo)}`);
  check('fire legend max == p97.5',
    c.max === '$' + Math.round(fireInd.hi).toLocaleString() + '+', `${c.max} vs ${Math.round(fireInd.hi)}`);

  // 5. Layer accessors under fire: height parity, artifact greying, kept ramp.
  // deck applies the new layers prop on its own frame cadence (erratic under
  // swiftshader) — poll until the rebuilt layer's static elevationScale prop
  // lands before reading it, rather than trusting a fixed sleep. This also
  // asserts the prop swap actually happens (times out → FAIL).
  let esApplied = true;
  await page.waitForFunction(() => {
    const layer = overlay._deck.layerManager.layers.find(l => l.id === 'ratio-extrusion');
    return layer && layer.props.elevationScale === ratioScale().elevationScale;
  }, { timeout: 20000 }).catch(() => { esApplied = false; });
  check('fire: rebuilt layer prop applied', esApplied);
  const layerFacts = await page.evaluate(() => {
    const layer = overlay._deck.layerManager.layers.find(l => l.id === 'ratio-extrusion');
    const feats = state.data.features;
    const props = f => f.properties;
    // kept under roads but below the fire floor => the picker's own artifact set
    const artifact = feats.find(f => !props(f).is_set_aside &&
      props(f).road_m_per_acre >= 5 && props(f).fire_events_per_acre != null &&
      props(f).fire_events_per_acre < 0.005);
    const zero = feats.find(f => !props(f).is_set_aside && props(f).fire_events_per_acre === 0);
    const kept = feats.find(f => props(f).neighbourhood_name === 'DOWNTOWN');
    return {
      artifactName: artifact && props(artifact).neighbourhood_name,
      artifactFill: artifact && layer.props.getFillColor(artifact),
      artifactElev: artifact && layer.props.getElevation(artifact),
      zeroName: zero && props(zero).neighbourhood_name,
      zeroFill: zero && layer.props.getFillColor(zero),
      keptFill: kept && layer.props.getFillColor(kept),
      keptElev: kept && layer.props.getElevation(kept),
      elevationScale: layer.props.elevationScale,
      setAsideColor: SET_ASIDE_COLOR,
    };
  });
  const grey = JSON.stringify(layerFacts.setAsideColor);
  check('fire: sub-floor hood greyed + flat',
    JSON.stringify(layerFacts.artifactFill) === grey && layerFacts.artifactElev === 0,
    `${layerFacts.artifactName} fill=${JSON.stringify(layerFacts.artifactFill)} elev=${layerFacts.artifactElev}`);
  check('fire: zero-event hood greyed',
    JSON.stringify(layerFacts.zeroFill) === grey, layerFacts.zeroName);
  check('fire: kept hood on ramp + extruded',
    JSON.stringify(layerFacts.keptFill) !== grey && layerFacts.keptElev > 0);
  check('fire: height parity (max kept reaches 8220)',
    Math.abs(layerFacts.elevationScale * fireInd.max - 8220) < 1,
    `${(layerFacts.elevationScale * fireInd.max).toFixed(1)}`);

  // 6. Tooltip prose under fire.
  const tips = await page.evaluate(() => {
    const feats = state.data.features;
    const kept = feats.find(f => f.properties.neighbourhood_name === 'DOWNTOWN');
    const artifact = feats.find(f => !f.properties.is_set_aside &&
      f.properties.fire_events_per_acre != null && f.properties.fire_events_per_acre > 0 &&
      f.properties.fire_events_per_acre < 0.005);
    return {
      kept: tooltipFor({ object: kept }).html,
      artifact: tooltipFor({ object: artifact }).html,
    };
  });
  check('fire tooltip: $/fire event + components',
    / \/ fire event/.test(tips.kept) && /fire events \/ acre \/ yr/.test(tips.kept) &&
    /revenue \/ acre/.test(tips.kept));
  check('fire tooltip: off-scale names the floor',
    /fewer than 0.005 fire events/.test(tips.artifact), tips.artifact);

  // 6b. The service-cost coverage denominator was RETIRED 2026-09-05 — the
  // audit found its denominator 88.6% fire-allocation variance, so "revenue per
  // modeled service dollar" was revenue per fire dispatch (DECISIONS.md;
  // docs/FINDINGS_services_cost_lens_verdict.md §3). The picker is back to the
  // two physical denominators. ⚠️ Asserted gone, not simply deleted.
  // ⚠️ UI only. The served geojson carries svc_cost_per_acre until the next
  // refresh, so asserting the column is gone would be red for a week against a
  // correct build; that removal is pinned in tests/test_join_and_calculate.py.
  check('svccost: denominator retired (no button, no RATIO_DENOMS entry)',
    await page.evaluate(() => !document.querySelector('#ratio-denom button[data-ratio-denom="servicecost"]')
      && !('servicecost' in RATIO_DENOMS)));
  check('picker offers exactly the two physical denominators',
    await page.evaluate(() => JSON.stringify([...document.querySelectorAll('#ratio-denom button')]
      .map(b => b.dataset.ratioDenom)) === '["roads","fire"]'));
  // Leave fire active for the persistence checks below.
  await click('#ratio-denom button[data-ratio-denom="fire"]');
  await page.waitForTimeout(1500);

  // 8. Persistence: leave to Money (picker hides), return (fire still active).
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('money: picker hidden again, state kept',
    !c.pickerShown && c.ratioDenom === 'fire', JSON.stringify({ picker: c.pickerShown, d: c.ratioDenom }));
  await click('#views button[data-view="ratio"]');
  await page.waitForTimeout(2000);
  c = await chrome();
  check('ratio again: fire persisted', c.active === 'fire' && c.title === 'Edmonton: Revenue per Fire Event');

  // 9. Back to roads: original chrome restored.
  await click('#ratio-denom button[data-ratio-denom="roads"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('back to roads: chrome restored',
    c.title === 'Edmonton: Revenue per Road Metre' && c.min === '≤ $' + Math.round(roadsInd.lo).toLocaleString());

  // 10. The institutional uncertainty band (2026-09-12). Ratio draws the same
  //     azure pair Money and Glass do, selected on SHARE ALONE — see the
  //     instBandedRatio comment for why the consequence tier does not port to a
  //     log ramp. These checks pin the decision, not just the drawing.
  const band = await page.evaluate(() => {
    const ls = buildLayers().filter(Boolean);
    const b = ls.filter(l => l.id.startsWith('ratio-inst'));
    const prisms = ls.find(l => l.id === 'ratio-extrusion');
    const of = n => state.data.features.find(f => f.properties.neighbourhood_name === n);
    const uofa = of('UNIVERSITY OF ALBERTA'), gb = of('RIVER VALLEY GOLD BAR');
    return {
      ids: b.map(l => l.id),
      opacity: b.map(l => l.props.opacity),
      pickable: b.map(l => l.props.pickable),
      prismOpacity: state.prismOpacity,
      n: state.data.features.filter(f => instBandedRatio(f.properties)).length,
      uofa: instBandedRatio(uofa.properties),
      goldBar: instBandedRatio(gb.properties),
      uofaElev: prisms.props.getElevation(uofa),
      uofaFill: prisms.props.getFillColor(uofa),
      bandElev: b.map(l => Math.round(l.props.getElevation(uofa))),
      blurb: document.getElementById('title-p').textContent,
    };
  });
  check('ratio draws the azure pair', band.ids.length === 2, JSON.stringify(band.ids));
  // ⚠️ Against state.prismOpacity, not against a literal — this is a GHOST-prism
  //    view, so a band pinned at 1.0 would sit on top of the composition
  //    instead of in it (the measured reason Glass rides the same value).
  check('band rides the ghost opacity',
    band.opacity.every(o => o === band.prismOpacity), JSON.stringify(band.opacity));
  check('band is unpickable (hood-hover owns tooltips)',
    band.pickable.every(v => v === false));
  // ⚠️ THE REGRESSION GUARD FOR THE THRESHOLD DECISION. Both hoods are 90%
  //    exempt and BOTH are dropped by a naive port of Money's
  //    INST_CONSEQUENCE_MIN — U of A shifts 0.229 (log compresses its 9.9x
  //    span), Gold Bar 0.000 (both endpoints clamp below the p2.5 anchor).
  //    If someone "restores parity" by adding a consequence term, these go red.
  check('U of A is banded (naive consequence port would drop it)', band.uofa);
  check('River Valley Gold Bar is banded (both endpoints clamp)', band.goldBar);
  check('band selects on share alone', band.n === 16, `${band.n} hoods`);
  // The ordinary prism must be flattened AND emptied — a ramp-coloured floor
  // under the band would assert the value the band exists to withhold.
  check('banded hood is flattened out of ratio-extrusion', band.uofaElev === 0);
  check('banded hood is fully transparent there',
    band.uofaFill[3] === 0, JSON.stringify(band.uofaFill));
  check('the two shells straddle the ratio', band.bandElev[0] < band.bandElev[1],
    JSON.stringify(band.bandElev));
  check('blurb explains the azure', /azure/.test(band.blurb));

  // 11. A banded hood must not print a single number, and an ordinary one must.
  const bandTips = await page.evaluate(() => {
    const t = n => tooltipFor({ object: state.data.features.find(
      f => f.properties.neighbourhood_name === n) }).html;
    return { uofa: t('UNIVERSITY OF ALBERTA'), plain: t('STRATHCONA') };
  });
  check('banded tooltip prints a RANGE', / to .*road metre/.test(bandTips.uofa),
    bandTips.uofa.slice(0, 150));
  check('banded tooltip carries the provenance caveat',
    /institutionally-zoned land/.test(bandTips.uofa) &&
    /does not publish which of it is tax-exempt/.test(bandTips.uofa));
  // ⚠️ The revenue row moves WITH the headline. A point revenue under a range
  //    headline would have the tooltip contradict itself in two lines.
  check('banded revenue row is a range too', / to .*revenue \/ acre/.test(bandTips.uofa));
  // ⚠️ Scoped to the HEADLINE ROW, not the whole tooltip: the pinned-history
  //    line ends "click to pin", so a whole-string " to " test passes on the
  //    wrong text and would go green under a genuinely banded headline.
  const headline = h => h.split('<br/>')[1] || '';
  check('an ordinary hood still prints one number',
    !/ to /.test(headline(bandTips.plain)) && /road metre/.test(headline(bandTips.plain)),
    headline(bandTips.plain));
  check('and the banded headline is the one carrying the range',
    / to /.test(headline(bandTips.uofa)), headline(bandTips.uofa));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

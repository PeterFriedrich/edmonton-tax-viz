// Verify the Ratio view's denominator picker (2026-07-10): per-service
// ratios — revenue per road metre | per fire event (SPEC_utilities
// decision 3). DOM + layer-accessor level, against the real served file.
//   node verify-ratio-denom.js <url>
// Checks: control visibility gating, chrome/legend swap, independent
// anchor recomputation (log p2.5–p97.5 of each kept subset), height
// parity, fire-floor artifact greying, tooltip prose, persistence across
// views, residential-lens re-anchoring.
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

  // 6b. Service-cost coverage denominator (2026-07-16, decision 3(b)) —
  // skipped on data files that predate the svc_cost_per_acre column. A
  // dimensionless ratio (revenue ÷ modeled service cost): legend bounds show
  // as ×-multiples (boundFmt), NOT dollars; the blurb must own the "not
  // paying its full way" caveat (full revenue over a two-service cost).
  const hasSvcCost = await page.evaluate(() =>
    state.data.features.some(f => f.properties.svc_cost_per_acre != null));
  if (!hasSvcCost) {
    check('svccost: SKIPPED (no svc_cost_per_acre column)', true);
    check('svccost: ratio button hidden', await page.evaluate(() =>
      getComputedStyle(document.querySelector('#ratio-denom button[data-ratio-denom="servicecost"]')).display === 'none'));
  } else {
    const fmtX = v => v.toFixed(v < 10 ? 1 : 0) + '×';
    await click('#ratio-denom button[data-ratio-denom="servicecost"]');
    await page.waitForTimeout(1500);
    c = await chrome();
    check('svccost: active + state', c.active === 'servicecost' && c.ratioDenom === 'servicecost');
    check('svccost: title', c.title === 'Edmonton: Revenue vs Modeled Service Cost', c.title);
    check('svccost: legend', c.legend === 'Revenue ÷ modeled roads+fire cost (log colour)', c.legend);
    check('svccost: aside', c.aside === 'Set aside / insufficient service base', c.aside);
    check('svccost: blurb owns the partial-cost caveat',
      /not a sign the land\s+pays its full way/.test(c.blurb) && /Roads and fire only/.test(c.blurb));
    const svcInd = await independent('svc_cost_per_acre', 230);
    check('svccost legend min == p2.5 (× format)',
      c.min === '≤ ' + fmtX(svcInd.lo), `${c.min} vs ${fmtX(svcInd.lo)}`);
    check('svccost legend max == p97.5 (× format)',
      c.max === fmtX(svcInd.hi) + '+', `${c.max} vs ${fmtX(svcInd.hi)}`);
    // Layer parity: max kept coverage reaches the 8220 height ceiling; a
    // kept hood extrudes on the ramp; a below-floor hood greys flat.
    await page.waitForFunction(() => {
      const layer = overlay._deck.layerManager.layers.find(l => l.id === 'ratio-extrusion');
      return layer && layer.props.elevationScale === ratioScale().elevationScale;
    }, { timeout: 20000 }).catch(() => {});
    const svcFacts = await page.evaluate(() => {
      const layer = overlay._deck.layerManager.layers.find(l => l.id === 'ratio-extrusion');
      const feats = state.data.features, props = f => f.properties;
      const artifact = feats.find(f => !props(f).is_set_aside &&
        props(f).svc_cost_per_acre != null && props(f).svc_cost_per_acre < 230);
      const kept = feats.find(f => props(f).neighbourhood_name === 'DOWNTOWN');
      return {
        artifactFill: artifact && layer.props.getFillColor(artifact),
        artifactElev: artifact && layer.props.getElevation(artifact),
        keptFill: kept && layer.props.getFillColor(kept),
        keptElev: kept && layer.props.getElevation(kept),
        elevationScale: layer.props.elevationScale,
        setAsideColor: SET_ASIDE_COLOR,
      };
    });
    const svcGrey = JSON.stringify(svcFacts.setAsideColor);
    check('svccost: below-floor hood greyed + flat',
      svcFacts.artifactFill == null ||
      (JSON.stringify(svcFacts.artifactFill) === svcGrey && svcFacts.artifactElev === 0));
    check('svccost: kept hood on ramp + extruded',
      JSON.stringify(svcFacts.keptFill) !== svcGrey && svcFacts.keptElev > 0);
    check('svccost: height parity (max kept reaches 8220)',
      Math.abs(svcFacts.elevationScale * svcInd.max - 8220) < 1,
      `${(svcFacts.elevationScale * svcInd.max).toFixed(1)}`);
    // Tooltip prose: ×-multiple + the underlying modeled cost component.
    const svcTip = await page.evaluate(() => {
      const kept = state.data.features.find(f => f.properties.neighbourhood_name === 'DOWNTOWN');
      return tooltipFor({ object: kept }).html;
    });
    check('svccost tooltip: ×-multiple + cost component',
      /× the modeled roads\+fire cost/.test(svcTip) &&
      /modeled roads\+fire cost \/ acre \/ yr/.test(svcTip), svcTip);
    // Restore fire as the active denom for the persistence checks below.
    await click('#ratio-denom button[data-ratio-denom="fire"]');
    await page.waitForTimeout(1500);
  }

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

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

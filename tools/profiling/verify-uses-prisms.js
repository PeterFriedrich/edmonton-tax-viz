// Verify the Uses view's residential prisms (2026-07-10): a layers-panel
// toggle that raises translucent prisms over the zoning fabric — height =
// each hood's share of zoned land that is residential, fixed 0–100% linear
// scale (100% = the standard ~8.2 km peak). DOM + layer-accessor level.
//   node verify-uses-prisms.js <url>
// Checks: control visibility gating, layer stack on/off, elevation +
// fill + opacity accessors, zero-share filtering, slider wiring, blurb
// honesty line, label roof-z, persistence across views.
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
    hdShown: getComputedStyle(document.getElementById('uses-prisms-hd')).display !== 'none',
    boxShown: getComputedStyle(document.getElementById('uses-prisms')).display !== 'none',
    sliderShown: getComputedStyle(document.getElementById('prism-row')).display !== 'none',
    sliderVal: document.getElementById('prism-opacity').value,
    checked: document.getElementById('uses-prisms-on').checked,
    usesPrisms: state.usesPrisms,
    layers: overlay._deck.layerManager.layers.map(l => l.id),
    view: state.view,
  }));

  // 1. Money view (default): the uses section is hidden.
  let c = await chrome();
  check('money: uses-prisms control hidden', !c.hdShown && !c.boxShown,
    JSON.stringify({ hd: c.hdShown, box: c.boxShown }));

  // 2. Enter Uses: control shown unchecked, no prism layer, slider hidden.
  await click('#views button[data-view="uses"]');
  await page.waitForTimeout(5000); // zoning lazy-fetch + rebuild
  c = await chrome();
  check('uses: control shown, unchecked', c.hdShown && c.boxShown && !c.checked && !c.usesPrisms);
  check('uses: default stack has no prisms',
    c.layers.includes('zoning-ground') && !c.layers.includes('uses-res-prisms'),
    JSON.stringify(c.layers));
  check('uses: slider hidden while off', !c.sliderShown);
  check('uses: blurb has no height sentence', !/prisms rise/i.test(c.blurb));

  // 3. Check the box: prism layer appears between fabric and hover, slider
  //    shows at the view default (35%), blurb gains the honesty line.
  await click('#uses-prisms-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('on: prism layer in stack', c.layers.includes('uses-res-prisms'), JSON.stringify(c.layers));
  check('on: prisms above fabric, below hover',
    c.layers.indexOf('zoning-ground') < c.layers.indexOf('uses-res-prisms') &&
    c.layers.indexOf('uses-res-prisms') < c.layers.indexOf('hood-hover'));
  check('on: slider shown at uses default 35%', c.sliderShown && c.sliderVal === '35',
    `shown=${c.sliderShown} val=${c.sliderVal}`);
  check('on: blurb says share of zoned land',
    /residential share of its zoned land/.test(c.blurb) && /100%\s*residential/.test(c.blurb));

  // 4. Layer facts: static scale prop, elevation = frac, identity sand fill,
  //    zero-share hoods filtered, opacity follows the slider state. Poll the
  //    static prop first — deck applies new layers on its own frame cadence.
  let applied = true;
  await page.waitForFunction(() => {
    const l = overlay._deck.layerManager.layers.find(x => x.id === 'uses-res-prisms');
    return l && l.props.elevationScale === USES_PRISM_PEAK;
  }, { timeout: 20000 }).catch(() => { applied = false; });
  check('on: elevationScale = USES_PRISM_PEAK applied', applied);
  const facts = await page.evaluate(() => {
    const l = overlay._deck.layerManager.layers.find(x => x.id === 'uses-res-prisms');
    const feats = state.data.features;
    const top = feats.map(f => f.properties)
      .reduce((a, p) => (p.frac_residential || 0) > (a.frac_residential || 0) ? p : a);
    const sample = l.props.data.features.find(
      f => f.properties.neighbourhood_name === top.neighbourhood_name);
    const zeros = feats.filter(f => (f.properties.frac_residential || 0) <= 0).length;
    return {
      peak: USES_PRISM_PEAK,
      topName: top.neighbourhood_name,
      topFrac: top.frac_residential,
      elevOfTop: sample && l.props.getElevation(sample),
      fill: l.props.getFillColor, // constant accessor
      sand: USE_BY_KEY.res.color,
      opacity: l.props.opacity,
      pickable: !!l.props.pickable,
      nPrisms: l.props.data.features.length,
      nHoods: feats.length,
      nZeros: zeros,
    };
  });
  check('on: elevation accessor = frac_residential',
    Math.abs(facts.elevOfTop - facts.topFrac) < 1e-9,
    `${facts.topName} frac=${facts.topFrac?.toFixed(3)} → ${(facts.elevOfTop * facts.peak).toFixed(0)} m`);
  check('on: fill = residential identity sand',
    JSON.stringify(facts.fill) === JSON.stringify(facts.sand), JSON.stringify(facts.fill));
  check('on: zero-share hoods filtered out',
    facts.nPrisms === facts.nHoods - facts.nZeros,
    `${facts.nPrisms} prisms = ${facts.nHoods} hoods − ${facts.nZeros} zero-share`);
  check('on: translucent at 35% + not pickable',
    Math.abs(facts.opacity - 0.35) < 1e-9 && !facts.pickable, `opacity=${facts.opacity}`);

  // 5. Slider drives live opacity.
  await page.$eval('#prism-opacity', el => {
    el.value = 80; el.dispatchEvent(new Event('input', { bubbles: true }));
  });
  let slid = true;
  await page.waitForFunction(() => {
    const l = overlay._deck.layerManager.layers.find(x => x.id === 'uses-res-prisms');
    return l && Math.abs(l.props.opacity - 0.8) < 1e-9;
  }, { timeout: 20000 }).catch(() => { slid = false; });
  check('slider: opacity 80% applied live', slid);

  // 6. Labels ride the prism roofs while prisms are on.
  await page.$eval('#labels-on', el => { el.checked = !el.checked; el.dispatchEvent(new Event('change')); });
  await page.waitForTimeout(1500);
  const roofZ = await page.evaluate(() => {
    const top = state.data.features.map(f => f.properties)
      .reduce((a, p) => (p.frac_residential || 0) > (a.frac_residential || 0) ? p : a);
    return { z: labelZ(top), expect: top.frac_residential * USES_PRISM_PEAK + 60 };
  });
  check('labels: roof-z = frac × peak + lift',
    Math.abs(roofZ.z - roofZ.expect) < 1e-6, `${roofZ.z.toFixed(1)} vs ${roofZ.expect.toFixed(1)}`);
  await page.$eval('#labels-on', el => { el.checked = !el.checked; el.dispatchEvent(new Event('change')); }); // labels off again
  await page.waitForTimeout(1000);

  // 7. Persistence: leave to Money (control hides, layer gone), return
  //    (still checked, prisms back, slider reset to the view default).
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('money: control hidden again, state kept',
    !c.boxShown && !c.sliderShown && c.usesPrisms &&
    !c.layers.includes('uses-res-prisms'),
    JSON.stringify({ box: c.boxShown, kept: c.usesPrisms }));
  await click('#views button[data-view="uses"]');
  await page.waitForTimeout(2000);
  c = await chrome();
  check('uses again: prisms persisted, slider back at 35%',
    c.checked && c.layers.includes('uses-res-prisms') && c.sliderShown && c.sliderVal === '35',
    JSON.stringify({ checked: c.checked, val: c.sliderVal }));

  // 8. Uncheck: layer gone, slider hides, blurb sentence drops.
  await click('#uses-prisms-on');
  await page.waitForTimeout(1500);
  c = await chrome();
  check('off: prism layer removed + slider hidden',
    !c.layers.includes('uses-res-prisms') && !c.sliderShown && !c.usesPrisms);
  check('off: blurb restored', !/prisms rise/i.test(c.blurb));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

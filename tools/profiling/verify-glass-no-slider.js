// Verify that Money -> 100 m grid (Glass) no longer offers the prism-opacity
// slider (2026-07-25), WITHOUT changing what it renders: Glass keeps its fixed
// 60% translucency because applyView re-applies VIEWS.glass.opacity on entry.
// Also guards that the slider survives where it IS still wanted — Ratio, Uses
// with residential prisms on, and Development's activity grid — and that a
// detour through Ratio (which sets 5%) can't strand Glass at a stale opacity.
//   node verify-glass-no-slider.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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
  const probe = () => page.evaluate(() => {
    const shown = id => document.getElementById(id).offsetParent !== null;
    const grid = overlay._deck.props.layers.find(l => l && l.id === 'glass-grid');
    const ghost = overlay._deck.props.layers.find(l => l && /ratio-extrusion|glass-extrusion|uses-res-prisms|dev-grid-cells/.test(l.id));
    return { view: state.view, sliderShown: shown('prism-row'), headerShown: shown('prism-hd'),
             layersShown: shown('layers'), opacity: state.prismOpacity,
             sliderVal: +document.getElementById('prism-opacity').value,
             gridOpacity: grid ? grid.props.opacity : null,
             ghostLayer: ghost ? ghost.id : null,
             ghostOpacity: ghost ? ghost.props.opacity : null,
             blurb: document.getElementById('title-p').textContent };
  });
  const view = async v => { await page.click(`#views button[data-view="${v}"]`); await page.waitForTimeout(3000); };
  const detail = async d => { await page.click(`#moneydetail button[data-moneydetail="${d}"]`); await page.waitForTimeout(3500); };

  // --- Money -> 100 m grid: no slider, render unchanged at 60%
  await detail('grid');
  const glass = await probe();
  console.log('glass      :', JSON.stringify(glass));
  check('[glass] view is the 100 m grid mode', glass.view === 'glass');
  check('[glass] slider is GONE', glass.sliderShown === false);
  check('[glass] "Money plane" header is gone too', glass.headerShown === false);
  check('[glass] layers panel still open (Detail/Denominator)', glass.layersShown === true);
  check('[glass] translucency unchanged at 60%', glass.opacity === 0.6, `opacity=${glass.opacity}`);
  check('[glass] grid layer really renders at 0.6', glass.gridOpacity === 0.6, `gridOpacity=${glass.gridOpacity}`);
  // Honesty: the prose must not point at a control that is no longer there.
  check('[glass] blurb no longer promises a slider', !/slider/i.test(glass.blurb));
  // ...and the denominator variant carries its own copy of that sentence.
  await page.click('#denom button[data-denom="lot"]');
  await page.waitForTimeout(3000);
  const lot = await probe();
  check('[glass/lot acres] blurb no longer promises a slider', !/slider/i.test(lot.blurb));
  check('[glass/lot acres] still the lot blurb', /parcel|lot/i.test(lot.blurb));
  await page.click('#denom button[data-denom="ground"]');
  await page.waitForTimeout(3000);

  // --- back to Neighbourhood: still no slider (money never had one)
  await detail('hood');
  const money = await probe();
  check('[money] no slider', money.sliderShown === false && money.headerShown === false);

  // --- Ratio still has it, at its own 5% default
  await view('ratio');
  const ratio = await probe();
  console.log('ratio      :', JSON.stringify(ratio));
  check('[ratio] slider still offered', ratio.sliderShown === true);
  check('[ratio] header still offered', ratio.headerShown === true);
  check('[ratio] at its own 5% default', ratio.sliderVal === 5 && ratio.opacity === 0.05);
  // drive it, to prove the control still works
  await page.locator('#prism-opacity').fill('80');
  await page.locator('#prism-opacity').dispatchEvent('input');
  await page.waitForTimeout(1800);
  const ratio80 = await probe();
  check('[ratio] slider still drives the render', ratio80.opacity === 0.8 && ratio80.ghostOpacity === 0.8,
        `${ratio80.ghostLayer}=${ratio80.ghostOpacity}`);

  // --- the stale-value trap: Ratio at 80% -> Glass must re-apply 60%
  await view('money');
  await detail('grid');
  const after = await probe();
  console.log('glass again:', JSON.stringify(after));
  check('[glass] re-entry resets to 60% (no stale value stranded)',
        after.opacity === 0.6 && after.gridOpacity === 0.6, `opacity=${after.opacity}`);
  check('[glass] still no slider on re-entry', after.sliderShown === false);
  await detail('hood');

  // --- Uses (full build only) keeps its slider with residential prisms on
  const usesBtn = await page.$('#views button[data-view="uses"]');
  if (usesBtn && await usesBtn.isVisible()) {
    await view('uses');
    const usesOff = await probe();
    check('[uses] no slider while prisms are off', usesOff.sliderShown === false);
    await page.check('#uses-prisms-on');
    await page.waitForTimeout(2500);
    const usesOn = await probe();
    check('[uses] slider returns with residential prisms on', usesOn.sliderShown === true);
    await page.uncheck('#uses-prisms-on');
    await page.waitForTimeout(1500);
  } else {
    console.log('SKIP  uses view not in this build');
  }

  // --- Development's activity grid keeps its slider
  await view('development');
  const devHood = await probe();
  check('[development] no slider on the neighbourhood choropleth', devHood.sliderShown === false);
  const devGrid = await page.$('#devdetail button[data-devdetail="grid"]');
  if (devGrid && await devGrid.isVisible()) {
    await devGrid.click();
    await page.waitForTimeout(4000);
    const g = await probe();
    check('[development] slider returns on the activity grid', g.sliderShown === true);
  } else {
    console.log('SKIP  development activity grid not offerable');
  }

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

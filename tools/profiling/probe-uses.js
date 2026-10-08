// One-off verify for the Uses view (2026-07-03). DOM-level checks:
// legend swaps to categorical rows (and back), per-hood fills match the
// dominant composition category, tooltip composition, lens-button disable
// in Uses, and the layer stack (single flat pickable layer, no prisms).
//   node probe-uses.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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

  const chrome = () => page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    label: document.getElementById('legend-label').textContent,
    barShown: document.querySelector('#legend .bar').style.display !== 'none',
    catRows: [...document.querySelectorAll('#legend .cat span:last-child')].map(s => s.textContent),
  }));

  // Both directions (tools/profiling/README.md, "Gate an early exit on the BUILD"): Uses is full-only, so on public the button
  // must be hidden and nothing below can run.
  const fullBuild = await page.evaluate(() => FULL_BUILD);
  const usesShown = await page.locator('#views button[data-view="uses"]').isVisible();
  const gateOk = usesShown === fullBuild;
  console.log(`${gateOk ? 'PASS' : 'FAIL'} Uses button ${fullBuild ? 'shown' : 'hidden'} on this build (shown=${usesShown})`);
  if (!gateOk) process.exitCode = 1;
  if (!fullBuild) {
    await browser.close();
    console.log('\nPARTIAL — ran 1 check, then stopped: public build, Uses is full-only');
    return;
  }

  console.log('money default  :', JSON.stringify(await chrome()));

  await page.click('#views button[data-view="uses"]');
  await page.waitForTimeout(2500);
  console.log('uses           :', JSON.stringify(await chrome()));

  // Layer stack + per-category fills on the zoning ground layer: every
  // feature's fill must equal its category colour from USE_CATEGORIES.
  const fills = await page.evaluate(() => {
    const layers = overlay._deck.layerManager.layers.map(l => l.id);
    const layer = overlay._deck.layerManager.layers.find(l => l.id === 'zoning-ground');
    if (!layer) return { layers, error: 'zoning-ground layer missing (fallback path?)' };
    const getFill = layer.props.getFillColor;
    let mismatches = 0;
    const cats = {};
    for (const f of zoningData.features) {
      const u = USE_BY_KEY[f.properties.u];
      const fill = getFill(f);
      if (!u || fill.join() !== tc(u.color).join()) mismatches++;
      else cats[u.label] = fill;
    }
    return { layers, extruded: !!layer.props.extruded, pickable: !!layer.props.pickable,
             nFeatures: zoningData.features.length, mismatches, cats };
  });
  console.log('zoning fills   :', JSON.stringify(fills, null, 1));

  // Tooltip composition for a known DC-dominant hood (big-box power centre).
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(
      f => f.properties.neighbourhood_name === 'SOUTH EDMONTON COMMON');
    return tooltipFor({ object: f }).html;
  });
  console.log('tooltip (SEC)  :', tip);

  // Leaving Uses restores the gradient legend + re-enables the lens.
  await page.click('#views button[data-view="money"]');
  await page.waitForTimeout(2000);
  console.log('back to money  :', JSON.stringify(await chrome()));

  await browser.close();
})();

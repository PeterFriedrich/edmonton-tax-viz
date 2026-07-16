// One-off: screenshot the Ratio view under each denominator (roads | fire |
// servicecost), prisms at 60% so the prism colours are visible (default 5%
// ghosts are near-invisible by design). node shot-ratio-denom.js <url> <out-prefix>
// → <out-prefix>-roads.png, <out-prefix>-fire.png[, <out-prefix>-servicecost.png]
// (servicecost skipped when the data file has no svc_cost_per_acre column)
const { chromium } = require('playwright');
const [url, prefix] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  await page.$eval('#views button[data-view="ratio"]', b => b.click());
  await page.waitForTimeout(5000);
  const hasSvcCost = await page.evaluate(() =>
    state.data.features.some(f => f.properties.svc_cost_per_acre != null));
  const denoms = ['roads', 'fire', ...(hasSvcCost ? ['servicecost'] : [])];
  for (const d of denoms) {
    await page.$eval(`#ratio-denom button[data-ratio-denom="${d}"]`, b => b.click());
    await page.evaluate(() => {
      setPrismOpacity(60);
      overlay.setProps({ layers: buildLayers() });
    });
    await page.waitForTimeout(60000); // swiftshader needs ~60s with roads on
    const out = `${prefix}-${d}.png`;
    await page.screenshot({ path: out, timeout: 90000, animations: 'disabled', caret: 'initial' });
    console.log('wrote', out);
  }
  await browser.close();
})();

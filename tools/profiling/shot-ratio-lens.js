// One-off: screenshot the ratio view with the residential lens on, prisms at
// 60% so the fade grey is visible (default 5% ghosts are near-invisible by
// design). node shot-ratio-lens.js <url> <out.png>
const { chromium } = require('playwright');
const [url, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  await page.click('#views button[data-view="ratio"]');
  await page.waitForTimeout(5000);
  await page.click('#lens button');
  await page.evaluate(() => {
    setPrismOpacity(60);
    overlay.setProps({ layers: buildLayers() });
  });
  await page.waitForTimeout(60000); // swiftshader needs ~60s with roads on
  await page.screenshot({ path: out, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', out);
  await browser.close();
})();

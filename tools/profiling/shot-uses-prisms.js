// One-off: screenshot the Uses view with the residential prisms off and on
// (at the 35% default and at 70% for a stronger read).
//   node shot-uses-prisms.js <url> <out-prefix>
// → <out-prefix>-off.png, <out-prefix>-35.png, <out-prefix>-70.png
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
  await page.$eval('#views button[data-view="uses"]', b => b.click());
  await page.waitForTimeout(8000); // zoning lazy-fetch + swiftshader tessellation
  const shots = [
    ['off', null],
    ['35', 35],
    ['70', 70],
  ];
  for (const [tag, pct] of shots) {
    if (pct != null) {
      await page.evaluate(p => {
        if (!state.usesPrisms) document.getElementById('uses-prisms-on').click();
        setPrismOpacity(p);
        overlay.setProps({ layers: buildLayers() });
      }, pct);
      await page.waitForTimeout(20000);
    }
    const out = `${prefix}-${tag}.png`;
    await page.screenshot({ path: out, timeout: 90000, animations: 'disabled', caret: 'initial' });
    console.log('wrote', out);
  }
  await browser.close();
})();

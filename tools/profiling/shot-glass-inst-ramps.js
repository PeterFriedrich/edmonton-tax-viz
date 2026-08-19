// Screenshot the Glass institutional bands under each ramp — the azure was
// validated as an OUTLINE against the ramp stops; as a translucent FILL it
// blends with them, so cividis (whose low end is dark blue) needs looking at.
const { chromium } = require('playwright');
const [url, prefix] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1000, height: 660 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  await page.$eval('#moneydetail button[data-moneydetail="grid"]', b => b.click());
  await page.waitForTimeout(4000);
  await page.evaluate(() => map.jumpTo(
    { center: [-113.525, 53.523], zoom: 14.2, pitch: 60, bearing: 20 }));
  for (const ramp of ['cividis', 'glow']) {
    await page.$eval(`button[data-ramp="${ramp}"]`, b => b.click());
    await page.waitForTimeout(30000);
    await page.screenshot({ path: `${prefix}-${ramp}.png`, timeout: 90000, animations: 'disabled' });
    console.log('wrote', `${prefix}-${ramp}.png`);
  }
  await browser.close();
})();

// One-off: screenshot the Glass view's institutional uncertainty bands, framed
// on the U of A / Garneau cluster where the flagged cells concentrate.
// node shot-glass-inst.js <url> <out-prefix>
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
  await page.$eval('#moneydetail button[data-moneydetail="grid"]', b => b.click());
  await page.waitForTimeout(6000);
  await page.evaluate(() => map.jumpTo(
    { center: [-113.525, 53.523], zoom: 14.2, pitch: 60, bearing: 20 }));
  await page.waitForTimeout(45000);
  await page.screenshot({ path: `${prefix}-uofa.png`, timeout: 90000, animations: 'disabled' });
  console.log('wrote', `${prefix}-uofa.png`);
  await browser.close();
})();

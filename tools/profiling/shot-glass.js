// One-off: screenshot the Glass view (translucent 100 m grid-cell spikes
// over the neutral hood plane) at the default 60% and at a solid 100%.
// node shot-glass.js <url> <out-prefix>   -> <prefix>-60.png, <prefix>-100.png
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
  await page.waitForTimeout(45000); // swiftshader render settle
  await page.screenshot({ path: `${prefix}-60.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-60.png`);
  await page.evaluate(() => {
    const el = document.getElementById('prism-opacity');
    el.value = 100; el.dispatchEvent(new Event('input'));
  });
  await page.waitForTimeout(20000);
  await page.screenshot({ path: `${prefix}-100.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-100.png`);
  await browser.close();
})();

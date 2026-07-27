// One-off: screenshot the Development view with the 100 m detail grid on.
// node shot-dev-grid.js <url> <out.png>
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
  await page.click('#views button[data-view="development"]');
  await page.waitForTimeout(3000);
  await page.$eval('#devdetail button[data-devdetail="grid"]', b => b.click());
  // tilt like the glass shots so the spikes read
  await page.evaluate(() => map.easeTo({ pitch: 55, bearing: -15, duration: 0 }));
  await page.waitForTimeout(45000); // swiftshader render settle
  await page.screenshot({ path: out, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', out);
  await browser.close();
})();

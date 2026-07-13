// One-off: screenshot the Infill view (diverging suitability × activity, with
// the residential opportunity gate). node shot-infill.js <url> <out.png>
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
  await page.click('#views button[data-view="infill"]');
  await page.waitForTimeout(45000); // swiftshader render settle
  await page.screenshot({ path: out, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', out);
  await browser.close();
})();

// One-off: screenshot the Glass view under BOTH spike denominators at solid
// opacity — the ground-vs-lot comparison (WEM de-needling is the visual test:
// the tallest spike in the west should collapse in lot mode).
// node shot-denom.js <url> <out-prefix>  -> <prefix>-ground.png, <prefix>-lot.png
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
  await page.$eval('#views button[data-view="glass"]', b => b.click());
  await page.waitForTimeout(8000);
  await page.evaluate(() => {
    const el = document.getElementById('prism-opacity');
    el.value = 100; el.dispatchEvent(new Event('input'));
  });
  await page.waitForTimeout(45000); // swiftshader render settle
  await page.screenshot({ path: `${prefix}-ground.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-ground.png`);
  await page.$eval('#denom button[data-denom="lot"]', b => b.click());
  await page.waitForTimeout(25000);
  await page.screenshot({ path: `${prefix}-lot.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-lot.png`);
  await browser.close();
})();

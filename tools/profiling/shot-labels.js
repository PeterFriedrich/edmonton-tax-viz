// One-off: screenshot the neighbourhood-labels toggle. Two frames per run:
// the default city view and a zoomed close-up (collision filter should show
// few labels city-wide, more up close).
// node shot-labels.js <url> <out-prefix>   -> <prefix>-city.png, <prefix>-zoom.png
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
  await page.$eval('#lens button[data-lens="labels"]', b => b.click());
  await page.waitForTimeout(45000); // swiftshader render + font atlas settle
  await page.screenshot({ path: `${prefix}-city.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-city.png`);
  await page.evaluate(() => map.jumpTo({ center: [-113.51, 53.54], zoom: 12.2, pitch: 52, bearing: -18 }));
  await page.waitForTimeout(30000);
  await page.screenshot({ path: `${prefix}-zoom.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-zoom.png`);
  await browser.close();
})();

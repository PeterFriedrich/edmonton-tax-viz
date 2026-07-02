// Screenshot after clicking a selector — for states behind a UI toggle
// (e.g. the roads service layer). Usage:
//   node shot-click.js <url> <click-selector> <out.png>
const { chromium } = require('playwright');
const [url, selector, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  await page.click(selector);
  await page.waitForTimeout(6000);
  // caret:"initial" skips the stable-screenshot dance that can time out while
  // deck.gl keeps redrawing under swiftshader.
  await page.screenshot({ path: out, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', out);
  await browser.close();
})();

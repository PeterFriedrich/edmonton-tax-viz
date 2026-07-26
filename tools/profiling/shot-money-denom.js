// Screenshots of the Money view under each denominator (2026-07-08): the
// neighbourhood prisms in ground-acre vs lot-acre mode, for Peter's eyeball.
//   node shot-money-denom.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4500);
  const click = sel => page.$eval(sel, b => b.click());

  await page.screenshot({ path: 'money-ground.png' });
  console.log('wrote money-ground.png');

  await click('#denom button[data-denom="lot"]');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'money-lot.png' });
  console.log('wrote money-lot.png');

  // value metric, lot mode — the biggest reshuffle (Downtown vs river valley)
  await click('#metric-row button[data-metric="value"]');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'money-lot-value.png' });
  console.log('wrote money-lot-value.png');

  await browser.close();
})();

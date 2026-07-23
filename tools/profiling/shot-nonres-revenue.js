// Screenshots of the "Non-res $" Money metric (2026-07-18), for Peter's
// eyeball: the non-residential-revenue choropleth and the Glass view's 100 m
// nonres cells (SPEC_industrial.md A1).
//   node shot-nonres-revenue.js <url>
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

  await click('#toggle button[data-metric="nonres_revenue_per_acre"]');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'nonres-revenue.png' });
  console.log('wrote nonres-revenue.png');

  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3500);
  await page.screenshot({ path: 'nonres-revenue-glass.png' });
  console.log('wrote nonres-revenue-glass.png');

  await browser.close();
})();

// Screenshots of the "Residential $" Money metric (2026-07-16), for Peter's
// eyeball: the residential-revenue choropleth, the same with the
// Residential-only fade lens composed on top (residential dollars on
// majority-residential-zoned land), and the Glass view's 100 m res cells
// (grid res columns, 2026-07-17).
//   node shot-res-revenue.js <url>
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

  await click('#toggle button[data-metric="res_revenue_per_acre"]');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'res-revenue.png' });
  console.log('wrote res-revenue.png');

  await click('#lens button[data-lens="residential"]');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'res-revenue-lens.png' });
  console.log('wrote res-revenue-lens.png');

  await click('#lens button[data-lens="residential"]'); // lens off (disabled in Glass anyway)
  await click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3500);
  await page.screenshot({ path: 'res-revenue-glass.png' });
  console.log('wrote res-revenue-glass.png');

  await browser.close();
})();

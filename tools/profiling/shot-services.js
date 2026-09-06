// One-off: screenshot the Services view in its colour states — roads only
// (the old Roads view look), both services with roads driving (storm plane
// neutral below the coloured network), both with stormwater driving
// (coloured plane, neutral network), and — when the data carries the fire
// column — fire driving (fire plane + station dots), and — when the data
// carries the water column — water driving (modeled water+sewer plane).
// node shot-services.js <url> <out-prefix>
//   -> <prefix>-roads.png, <prefix>-both-roads.png, <prefix>-storm.png
//      [, <prefix>-fire.png] [, <prefix>-water.png]
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
  await page.$eval('#views button[data-view="services"]', b => b.click());
  await page.waitForTimeout(30000); // roads fetch + swiftshader render settle
  await page.screenshot({ path: `${prefix}-roads.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-roads.png`);
  await page.$eval('#services .svc[data-service="storm"] .svc-on', b => b.click());
  await page.waitForTimeout(20000);
  await page.screenshot({ path: `${prefix}-both-roads.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-both-roads.png`);
  await page.$eval('#services .svc[data-service="storm"] input[type="radio"]', b => b.click());
  await page.waitForTimeout(20000);
  await page.screenshot({ path: `${prefix}-storm.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
  console.log('wrote', `${prefix}-storm.png`);
  const hasFire = await page.evaluate(() =>
    state.data.features.some(f => f.properties.fire_events_per_acre != null));
  if (hasFire) {
    await page.$eval('#services .svc[data-service="fire"] .svc-on', b => b.click());
    await page.waitForTimeout(5000); // station dots fetch
    await page.$eval('#services .svc[data-service="fire"] input[type="radio"]', b => b.click());
    await page.waitForTimeout(20000);
    await page.screenshot({ path: `${prefix}-fire.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
    console.log('wrote', `${prefix}-fire.png`);
  } else {
    console.log('fire shot skipped — data file has no fire_events_per_acre column');
  }
  const hasWater = await page.evaluate(() =>
    state.data.features.some(f => f.properties.water_charge_per_acre != null));
  if (hasWater) {
    await page.$eval('#services .svc[data-service="water"] .svc-on', b => b.click());
    await page.waitForTimeout(2000);
    await page.$eval('#services .svc[data-service="water"] input[type="radio"]', b => b.click());
    await page.waitForTimeout(20000);
    await page.screenshot({ path: `${prefix}-water.png`, timeout: 90000, animations: 'disabled', caret: 'initial' });
    console.log('wrote', `${prefix}-water.png`);
  } else {
    console.log('water shot skipped — data file has no water_charge_per_acre column');
  }
  await browser.close();
})();

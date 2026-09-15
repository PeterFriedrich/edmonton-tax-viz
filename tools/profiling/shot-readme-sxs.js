// README side-by-side: Money neighbourhood prisms | Money 50 m grid, one camera.
// Stage 1 of 2 — compose-readme-sxs.py turns the two panels into the final image.
//
//   node tools/profiling/shot-readme-sxs.js http://localhost:8947/index.html <dir>
//
// ⚠️ Point it at the PUBLIC build (the root, not /full/). A README image gets
// shared cold, and the full build carries specialist lenses that are not public.
// ⚠️ Restart the static server before running — it wedges after a Playwright run,
// staying alive and returning empty responses (session notes, S156 §3h).
const { chromium } = require('playwright');
const [url, outdir] = process.argv.slice(2);
const W = 1000, H = 900;

// One camera for both panels, so the pair reads as the same place at two
// resolutions — the whole point of the comparison.
const CAM = { lon: -113.4870, lat: 53.5180, zoom: 10.05, pitch: 47, bearing: -17 };

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist','--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 });
  const errs = [];
  page.on('pageerror', e => errs.push('EXC ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('ERR ' + m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(5000);

  // Fold the Options pod: at README width its text is illegible anyway and it
  // sits over the prisms. The view/metric row and the legend stay — they say
  // "app", not "render".
  await page.$eval('#opt-fold', b => b.click()).catch(() => {});
  // The long methods paragraph is unreadable when the shot is 480px wide and
  // covers a third of the city. Keep the H1.
  await page.$eval('#title-p', p => { p.style.display = 'none'; }).catch(() => {});
  await page.waitForTimeout(400);

  const setCam = async () => {
    await page.evaluate(c => map.jumpTo({
      center: [c.lon, c.lat], zoom: c.zoom, pitch: c.pitch, bearing: c.bearing }), CAM);
    await page.waitForTimeout(2800);
  };

  const shoot = async (name) => {
    await page.screenshot({ path: `${outdir}/${name}.png` });
    const s = await page.evaluate(() => ({
      view: state.view, cell: state.glassCell, metric: state.metric, denom: state.denom }));
    console.log('wrote', name, JSON.stringify(s));
  };

  await setCam();
  await shoot('panel-a-hood');

  await page.$eval('#moneydetail button[data-moneydetail="grid-fine"]', b => b.click());
  await page.waitForFunction(() => state.glassCell === 50 && gridData, null, { timeout: 90000 });
  await page.waitForTimeout(4000);
  await setCam();
  await shoot('panel-b-grid50');

  console.log('--- page errors ---');
  console.log(errs.length ? errs.join('\n') : '(none)');
  await browser.close();
})();

// Verify for the "Center 2D" framing button (#center2d, bottom-left next to
// "Center 3D", added 2026-07-24; was the earlier toggle-style "Flip to 2D").
// It recenters the camera to a straight-down, NORTH-UP plan (HOME_2D: pitch 0,
// bearing 0) — flat at the -18 tilt-rotation looked skewed, so 2D snaps north-
// aligned. Checks: the button is really clickable; from the tilted/rotated
// default it flattens to pitch 0 AND bearing 0 and recenters to HOME position/
// zoom; gold state tracks the flat camera; and it north-aligns even when the
// user starts rotated.
//   node verify-center2d.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  const cam = () => page.evaluate(() => ({
    lng: +map.getCenter().lng.toFixed(3), lat: +map.getCenter().lat.toFixed(3),
    zoom: +map.getZoom().toFixed(2), pitch: +map.getPitch().toFixed(1), bearing: +map.getBearing().toFixed(1),
    label: document.getElementById('center2d').textContent,
    flat: document.getElementById('center2d').classList.contains('flat'),
    hit: (() => { const el = document.getElementById('center2d'), r = el.getBoundingClientRect();
      return document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === el; })(),
  }));
  const home = await page.evaluate(() => HOME);
  const settleFlat = async () => {
    for (let i = 0; i < 50; i++) {
      if ((await page.evaluate(() => map.getPitch())) < 0.5) return;
      await page.waitForTimeout(100);
    }
  };

  const init = await cam();
  console.log('initial   :', JSON.stringify({ pitch: init.pitch, bearing: init.bearing }));
  check('starts tilted + rotated (3D default)', init.pitch > 40 && init.bearing !== 0);
  check('label is "Center 2D"', init.label === 'Center 2D');
  check('button hit-tests as itself (clickable)', init.hit === true);
  check('not gold while tilted', init.flat === false);

  // From the tilted default: Center 2D flattens AND north-aligns AND recenters.
  await page.click('#center2d');
  await settleFlat();
  const flat = await cam();
  console.log('center 2D :', JSON.stringify({ lng: flat.lng, lat: flat.lat, zoom: flat.zoom, pitch: flat.pitch, bearing: flat.bearing }));
  check('flattens to top-down (pitch 0)', flat.pitch < 1);
  check('snaps north-up (bearing 0)', Math.abs(flat.bearing) < 0.5);
  check('recenters to HOME position', Math.abs(flat.lng - home.center[0]) < 0.01 && Math.abs(flat.lat - home.center[1]) < 0.01);
  check('recenters to HOME zoom', Math.abs(flat.zoom - home.zoom) < 0.05);
  check('gold state on (2D engaged)', flat.flat === true);

  // Even starting rotated-but-not-flat, Center 2D must north-align (regression
  // guard for the original skew complaint).
  await page.evaluate(() => map.jumpTo({ bearing: 35, pitch: 30 }));
  await page.waitForTimeout(300);
  await page.click('#center2d');
  await settleFlat();
  const c = await cam();
  console.log('from skew :', JSON.stringify({ pitch: c.pitch, bearing: c.bearing }));
  check('north-aligns from a rotated start', Math.abs(c.bearing) < 0.5 && c.pitch < 1);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

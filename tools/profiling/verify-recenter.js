// Verify for the "Center 3D" recenter button (#recenter, bottom-left next to
// "Center 2D", added 2026-07-24). It eases the whole camera back to the default
// framing HOME (center, zoom, pitch 52, bearing -18). Checks: the button is
// really clickable; from a panned/zoomed/rotated/flattened camera it restores
// all four axes to HOME; and it clears the Center 2D gold state (the tilt is
// back up, so the camera is no longer flat).
//   node verify-recenter.js <url>
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
    home: window.HOME || null,
    c2dFlat: document.getElementById('center2d').classList.contains('flat'),
    hit: (() => { const el = document.getElementById('recenter'), r = el.getBoundingClientRect();
      return document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === el; })(),
  }));
  const home = await page.evaluate(() => HOME);
  const settleHome = async () => {
    for (let i = 0; i < 50; i++) {
      const c = await page.evaluate(() => ({ p: map.getPitch(), z: map.getZoom() }));
      if (Math.abs(c.p - home.pitch) < 0.5 && Math.abs(c.z - home.zoom) < 0.02) return;
      await page.waitForTimeout(100);
    }
  };

  const start = await cam();
  check('recenter button hit-tests as itself (clickable)', start.hit === true);

  // Shove the camera well off HOME on every axis, including flattened (2D).
  await page.evaluate(h => map.jumpTo({
    center: [h.center[0] + 0.15, h.center[1] - 0.1], zoom: h.zoom + 2, pitch: 0, bearing: 40,
  }), home);
  await page.waitForTimeout(400);
  const moved = await cam();
  console.log('moved off :', JSON.stringify({ lng: moved.lng, lat: moved.lat, zoom: moved.zoom, pitch: moved.pitch, bearing: moved.bearing }));
  check('camera actually moved off HOME', moved.pitch < 1 && Math.abs(moved.zoom - home.zoom) > 1 && moved.bearing !== home.bearing);
  check('Center 2D gold reflects the flattened camera', moved.c2dFlat === true);

  // Recenter.
  await page.click('#recenter');
  await settleHome();
  const c = await cam();
  console.log('recentered:', JSON.stringify({ lng: c.lng, lat: c.lat, zoom: c.zoom, pitch: c.pitch, bearing: c.bearing }));
  check('center restored', Math.abs(c.lng - home.center[0]) < 0.01 && Math.abs(c.lat - home.center[1]) < 0.01);
  check('zoom restored', Math.abs(c.zoom - home.zoom) < 0.05);
  check('pitch restored (3D tilt)', Math.abs(c.pitch - home.pitch) < 1);
  check('bearing restored', Math.abs(c.bearing - home.bearing) < 0.5);
  check('Center 2D gold cleared (back in 3D)', c.c2dFlat === false);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

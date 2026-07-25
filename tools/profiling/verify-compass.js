// Verify for the bottom-left compass (#compass: #rot-ccw / #tonorth / #rot-cw,
// added 2026-07-25). The compass exists to advertise that the map rotates and to
// offer an IN-PLACE north-up (unlike Center 2D, which reframes the whole city).
// Checks: all three buttons are really clickable (real hit-test, not a JS
// .click()); each arrow walks bearing to the next 30° detent in its own
// direction; rapid presses keep advancing instead of collapsing onto one target;
// the needle counter-rotates so it holds true north; #tonorth snaps bearing to 0
// while LEAVING position/zoom/pitch alone.
//   node verify-compass.js <url>
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
  const bearing = () => page.evaluate(() => +map.getBearing().toFixed(2));
  const cam = () => page.evaluate(() => ({
    lng: +map.getCenter().lng.toFixed(3), lat: +map.getCenter().lat.toFixed(3),
    zoom: +map.getZoom().toFixed(2), pitch: +map.getPitch().toFixed(1),
    bearing: +map.getBearing().toFixed(2),
    // needle transform is set inline as rotate(Ndeg) — read the angle back
    needle: parseFloat((document.getElementById('needle').style.transform.match(/-?[\d.]+/) || [NaN])[0]),
    north: document.getElementById('tonorth').classList.contains('north'),
  }));
  const hit = id => page.evaluate(sel => {
    const el = document.getElementById(sel), r = el.getBoundingClientRect();
    return document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === el
        || el.contains(document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2));
  }, id);
  // swiftshader animates easeTo slowly — poll until the camera stops moving.
  // The lead-in delay matters: an ease takes a frame to register, so polling
  // immediately sees the OLD settled bearing and returns one step stale.
  const settle = async () => {
    await page.waitForTimeout(200);
    for (let i = 0; i < 80; i++) {
      if (!(await page.evaluate(() => map.isEasing() || map.isMoving()))) return;
      await page.waitForTimeout(100);
    }
  };

  // --- clickability (the S67 regression class: visible but pointer-events dead)
  for (const id of ['rot-ccw', 'tonorth', 'rot-cw']) {
    check(`#${id} hit-tests as itself (clickable)`, await hit(id));
  }

  const init = await cam();
  console.log('initial   :', JSON.stringify({ bearing: init.bearing, needle: init.needle, north: init.north }));
  check('starts at the rotated 3D default', Math.abs(init.bearing) > 1);
  check('needle counter-rotates to hold north', Math.abs(init.needle + init.bearing) < 0.5,
        `needle=${init.needle} bearing=${init.bearing}`);
  check('not flagged north-up while rotated', init.north === false);

  // --- clockwise arrow: -18 -> next detent below = -30, then -60
  await page.click('#rot-cw');
  await settle();
  const cw1 = await bearing();
  check('clockwise walks to the next 30° detent', cw1 === -30, `bearing=${cw1}`);
  await page.click('#rot-cw');
  await settle();
  const cw2 = await bearing();
  check('clockwise again advances one detent', cw2 === -60, `bearing=${cw2}`);

  // --- counter-clockwise arrow reverses it
  await page.click('#rot-ccw');
  await settle();
  const ccw1 = await bearing();
  check('counter-clockwise walks back up', ccw1 === -30, `bearing=${ccw1}`);

  // --- rapid presses must chain (regression guard: reading the live mid-ease
  //     bearing made every press after the first a no-op)
  await page.evaluate(() => map.jumpTo({ bearing: 0 }));
  await page.waitForTimeout(200);
  // JS .click() here on purpose: playwright's actionability checks make real
  // clicks too slow to land inside the chaining window. Clickability is asserted
  // separately above, so bypassing pointer-events is safe for this timing check.
  await page.evaluate(() => {
    const b = document.getElementById('rot-ccw');
    b.click(); b.click(); b.click();
  });
  await settle();
  const rapid = await bearing();
  check('3 rapid presses = 3 detents (90°)', rapid === 90, `bearing=${rapid}`);

  // --- needle tracks a free drag-rotate, and the arrow re-aligns to the grid
  await page.evaluate(() => map.jumpTo({ bearing: 47 }));
  await page.waitForTimeout(300);
  const dragged = await cam();
  check('needle tracks an off-grid bearing', Math.abs(dragged.needle + 47) < 0.5, `needle=${dragged.needle}`);
  await page.click('#rot-cw');
  await settle();
  const regrid = await bearing();
  check('arrow re-aligns an off-grid bearing to the grid', regrid === 30, `bearing=${regrid}`);

  // --- #tonorth: bearing only. Move off HOME first so a reframe would show up.
  await page.evaluate(() => map.jumpTo({ center: [-113.40, 53.60], zoom: 12.5, pitch: 45, bearing: 65 }));
  await page.waitForTimeout(300);
  const before = await cam();
  await page.click('#tonorth');
  await settle();
  const after = await cam();
  console.log('to north  :', JSON.stringify(after));
  check('snaps to bearing 0', Math.abs(after.bearing) < 0.5, `bearing=${after.bearing}`);
  check('keeps position (does NOT reframe)',
        after.lng === before.lng && after.lat === before.lat, `${after.lng},${after.lat}`);
  check('keeps zoom', after.zoom === before.zoom, `zoom=${after.zoom}`);
  check('keeps tilt (still 3D)', Math.abs(after.pitch - before.pitch) < 0.5, `pitch=${after.pitch}`);
  check('needle upright at north', Math.abs(after.needle) < 0.5, `needle=${after.needle}`);
  check('flagged north-up', after.north === true);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

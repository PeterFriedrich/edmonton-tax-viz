// Verify for the 2D/3D flip button (#flip2d, bottom-left above the legend,
// added 2026-07-24). The app is a 3D extrusion viz; this button eases the
// camera between the tilted default (pitch 52) and a straight-down 2D plan
// (pitch 0), keyed off the live pitch so it survives manual tilt. Checks:
// the button is really clickable (hit-tests as itself); clicking flattens to
// pitch 0 and the label/gold state follow; clicking again restores the tilt;
// bearing is left untouched (2D-ness is only pitch); and the label syncs when
// pitch is changed by other means (a manual tilt drag).
//   node verify-flip2d.js <url>
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
  const snap = () => page.evaluate(() => ({
    pitch: +map.getPitch().toFixed(1),
    bearing: +map.getBearing().toFixed(1),
    label: document.getElementById('flip2d').textContent,
    flat: document.getElementById('flip2d').classList.contains('flat'),
    hit: (() => { const el = document.getElementById('flip2d'), r = el.getBoundingClientRect();
      return document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === el; })(),
  }));
  // easeTo animates; poll until the camera settles so we don't sample mid-flight.
  const settle = async want => {
    for (let i = 0; i < 40; i++) {
      if (Math.abs((await page.evaluate(() => map.getPitch())) - want) < 0.5) return;
      await page.waitForTimeout(100);
    }
  };

  const init = await snap();
  console.log('initial   :', JSON.stringify(init));
  check('starts tilted (3D default)', init.pitch > 40);
  check('label starts "Flip to 2D"', init.label === 'Flip to 2D' && !init.flat);
  check('button hit-tests as itself (clickable)', init.hit === true);

  await page.click('#flip2d');
  await settle(0);
  const flat = await snap();
  console.log('after 2D  :', JSON.stringify(flat));
  check('flips to top-down (pitch 0)', flat.pitch < 1);
  check('bearing untouched by flip', flat.bearing === init.bearing);
  check('label + gold state follow (2D engaged)', flat.label === 'Flip to 3D' && flat.flat === true);

  await page.click('#flip2d');
  await settle(init.pitch);
  const back = await snap();
  console.log('after 3D  :', JSON.stringify(back));
  check('flips back to the prior tilt', Math.abs(back.pitch - init.pitch) < 1);
  check('label + gold state reset', back.label === 'Flip to 2D' && back.flat === false);

  // Label must track pitch changed by other means (e.g. a manual tilt drag).
  await page.evaluate(() => map.easeTo({ pitch: 0, duration: 0 }));
  await settle(0);
  const manual = await snap();
  console.log('api-flat  :', JSON.stringify(manual));
  check('label syncs to a non-button pitch change', manual.label === 'Flip to 3D' && manual.flat === true);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

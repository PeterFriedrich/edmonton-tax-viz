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
  const sq0 = await page.evaluate(() => overlay._deck.props.layers.filter(Boolean)
    .filter(l => l.props.modelMatrix && l.props.modelMatrix[10] < 0.01).length);
  check('no layer is flattened while tilted', sq0 === 0, `${sq0} flattened`);

  // From the tilted default: Center 2D flattens AND north-aligns AND recenters.
  // Spy on the in-ease flatten so the BUTTON is proven to arm it; the curve
  // itself is checked on a slowed ease further down.
  await page.evaluate(() => { const f = flattenDuringEase; window.__armed = 0;
    flattenDuringEase = () => { window.__armed++; return f(); }; });
  await page.click('#center2d');
  await settleFlat();
  const flat = await cam();
  console.log('center 2D :', JSON.stringify({ lng: flat.lng, lat: flat.lat, zoom: flat.zoom, pitch: flat.pitch, bearing: flat.bearing }));
  check('flattens to top-down (pitch 0)', flat.pitch < 1);
  check('snaps north-up (bearing 0)', Math.abs(flat.bearing) < 0.5);
  check('recenters to HOME position', Math.abs(flat.lng - home.center[0]) < 0.01 && Math.abs(flat.lat - home.center[1]) < 0.01);
  check('recenters to HOME zoom', Math.abs(flat.zoom - home.zoom) < 0.05);
  check('gold state on (2D engaged)', flat.flat === true);
  check('Center 2D arms the in-ease flatten', await page.evaluate(() => window.__armed === 1));

  // The lens flattens with the camera (2026-09-23): every layer carries the
  // z-squash while flat and none does while tilted. Read off the live layer
  // list, since a stale list is exactly what a missed rebuild leaves behind.
  const squashed = () => page.evaluate(() => {
    const ls = overlay._deck.props.layers.filter(Boolean);
    const z = l => (l.props.modelMatrix ? l.props.modelMatrix[10] : 1);
    return { n: ls.length, flat: ls.filter(l => z(l) < 0.01).length,
             zeroed: ls.filter(l => z(l) === 0).length };
  });
  const sq = await squashed();
  check('every layer is flattened in 2D', sq.n > 0 && sq.flat === sq.n, JSON.stringify(sq));

  // ⚠️ Squashed, not zeroed: a zero z-scale also zeroes the roofs' lighting
  // normals, and every fill went ~38% darker than its legend colour. Compare
  // one low hood's pixel flattened vs the same camera unflattened — at pitch 0
  // a low roof sits almost on its footprint, so the two must agree.
  const pixel = async (x, y) => {
    const b64 = (await page.screenshot({ clip: { x, y, width: 1, height: 1 }, timeout: 60000 })).toString('base64');
    return page.evaluate(async s => {
      const img = new Image(); img.src = 'data:image/png;base64,' + s; await img.decode();
      const c = document.createElement('canvas'); c.width = c.height = 1;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0);
      return [...g.getImageData(0, 0, 1, 1).data].slice(0, 3);
    }, b64);
  };
  const probe = await page.evaluate(() => {
    const key = moneyScale().colKey;
    const fs = state.data.features.filter(f => f.properties[key] > 0 && !f.properties.is_set_aside && !instBandedMoney(f.properties));
    const vals = fs.map(f => f.properties[key]).sort((a, b) => a - b);
    const low = vals[Math.floor(vals.length * 0.25)];
    const cands = fs.filter(f => f.properties[key] <= low).map(f => {
      const ring = f.geometry.type === 'Polygon' ? f.geometry.coordinates[0] : f.geometry.coordinates[0][0];
      const c = ring.reduce((a, p) => [a[0] + p[0] / ring.length, a[1] + p[1] / ring.length], [0, 0]);
      return { c, p: map.project(c), name: f.properties.neighbourhood_name };
    });
    const mid = [640, 400];
    cands.sort((a, b) => Math.hypot(a.p.x - mid[0], a.p.y - mid[1]) - Math.hypot(b.p.x - mid[0], b.p.y - mid[1]));
    return { x: Math.round(cands[0].p.x), y: Math.round(cands[0].p.y), name: cands[0].name };
  });
  await page.waitForTimeout(1500);
  const flatPx = await pixel(probe.x, probe.y);
  await page.evaluate(() => { camFlat = false; overlay.setProps({ layers: buildLayers() }); });
  await page.waitForTimeout(1500);
  const tallPx = await pixel(probe.x, probe.y);
  await page.evaluate(() => { camFlat = true; overlay.setProps({ layers: buildLayers() }); });
  const dPx = Math.max(...flatPx.map((v, i) => Math.abs(v - tallPx[i])));
  check('flattened roofs keep their lit colour', dPx <= 6,
    `${probe.name} @${probe.x},${probe.y} flat ${flatPx} vs unflattened ${tallPx}`);

  // Center 2D lowers the heights over the LAST QUARTER OF THE TILT (pitch
  // start/4 -> 0), not at the end (2026-09-23). Every sampled frame must sit
  // on that curve — true whatever the frame rate — and a slowed ease must
  // land at least one frame strictly between full height and flat.
  await page.evaluate(() => map.jumpTo(HOME));
  await page.waitForTimeout(800);
  const samples = await page.evaluate(() => new Promise(res => {
    const MS = 8000, out = [], t0 = performance.now(), from = map.getPitch() / 4;
    map.easeTo({ ...HOME_2D, duration: MS });
    flattenDuringEase();
    const z = () => { const l = overlay._deck.props.layers.find(Boolean);
      return l.props.modelMatrix ? l.props.modelMatrix[10] : 1; };
    const tick = () => {
      const t = (performance.now() - t0) / MS;
      out.push([t, z(), map.getPitch(), from]);
      if (t < 1.2) requestAnimationFrame(tick); else res(out);
    };
    requestAnimationFrame(tick);
  }));
  const off = samples.filter(([, z, p, from]) => {
    const want = p >= from ? 1 : p < 1 ? 1e-4 : p / from;
    return Math.abs(z - want) > 0.02;
  });
  const partial = samples.filter(([, z]) => z > 0.001 && z < 0.99);
  const last = samples[samples.length - 1];
  check('height follows the last quarter of the tilt', off.length === 0,
    off.length ? `off-curve: pitch ${off[0][2].toFixed(1)} z ${off[0][1].toFixed(3)}` : `${samples.length} frames`);
  check('heights pass through partial frames', partial.length > 0,
    partial.length ? `${partial.length} frames, e.g. pitch ${partial[0][2].toFixed(1)} z ${partial[0][1].toFixed(2)}` : 'none');
  check('ends flat', last[1] < 0.01 && await page.evaluate(() => camFlat), `z=${last[1]}`);

  // A drag that stops the ease part-way restores full height.
  await page.evaluate(() => map.jumpTo(HOME));
  await page.waitForTimeout(800);
  const stopped = await page.evaluate(() => new Promise(res => {
    map.easeTo({ ...HOME_2D, duration: 8000 });
    flattenDuringEase();
    const wait = () => {
      if (map.getPitch() < 8) { map.stop(); requestAnimationFrame(() => {
        const l = overlay._deck.props.layers.find(Boolean);
        res({ pitch: map.getPitch(), z: l.props.modelMatrix ? l.props.modelMatrix[10] : 1, squashZ });
      }); } else requestAnimationFrame(wait);
    };
    requestAnimationFrame(wait);
  }));
  check('an interrupted ease restores full height', stopped.z === 1 && stopped.squashZ === null,
    JSON.stringify(stopped));
  await page.evaluate(() => map.jumpTo(HOME_2D));
  await page.waitForTimeout(500);

  // Tilting by drag (no button) snaps the heights back.
  await page.evaluate(() => map.jumpTo({ pitch: 30 }));
  await page.waitForTimeout(300);
  const sq3 = await squashed();
  check('tilting restores full height', sq3.flat === 0, JSON.stringify(sq3));
  await page.click('#center2d');
  await settleFlat();

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

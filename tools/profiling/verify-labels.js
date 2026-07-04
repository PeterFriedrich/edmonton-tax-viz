// One-off verify for the neighbourhood-labels toggle (2026-07-03).
// DOM/accessor-level: label layer present per view when on, absent when off,
// anchors sane, roof-height z in extruded views, greedy culling overlap-free
// and zoom-responsive, residential-lens disable untouched by the new button.
//   node verify-labels.js <url>
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

  const snap = () => page.evaluate(() => {
    // props.layers is the exact array buildLayers() produced — deterministic,
    // unlike layerManager.layers which holds finalizing layers for a beat.
    const layer = overlay._deck.props.layers.find(l => l.id === 'hood-labels');
    return {
      view: state.view,
      labels: state.labels,
      layerPresent: !!layer,
      labelsBtnActive: document.querySelector('#lens button[data-lens="labels"]').classList.contains('active'),
      resBtnDisabled: document.querySelector('#lens button[data-lens="residential"]').disabled,
      shown: layer ? layer.props.data.length : 0,
    };
  });

  console.log('money, labels off:', JSON.stringify(await snap()));

  await page.$eval('#lens button[data-lens="labels"]', b => b.click());
  await page.waitForTimeout(2500); // font atlas build
  console.log('money, labels ON :', JSON.stringify(await snap()));

  // Anchor + culling sanity in the money view: all 406 anchors inside the
  // city bbox; the shown subset is a real cull (0 < shown < all), overlap-free
  // under the layer's own box model, includes the biggest on-screen hoods, and
  // the tallest hood's label z is its prism roof + lift.
  const culling = await page.evaluate(() => {
    const all = labelAnchors();
    const badAnchor = all.filter(d => {
      const [x, y] = d.position;
      return !(x > -113.8 && x < -113.2 && y > 53.3 && y < 53.8);
    });
    const shown = overlay._deck.props.layers.find(l => l.id === 'hood-labels').props.data;
    const vp = overlay._deck.getViewports()[0];
    const box = d => {
      const [px, py] = vp.project([d.position[0], d.position[1], labelZ(d.p)]);
      return { px, py, w: d.em * LABEL_SIZE * LABEL_DRAW_SCALE + 16, h: LABEL_SIZE * LABEL_DRAW_SCALE + 16 };
    };
    let overlaps = 0;
    const boxes = shown.map(box);
    for (let i = 0; i < boxes.length; i++)
      for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j];
        if (Math.abs(a.px - b.px) * 2 <= a.w + b.w && Math.abs(a.py - b.py) * 2 <= a.h + b.h) overlaps++;
      }
    // The page's LABEL_DRAW_SCALE must cover deck's real glyph scale-up, or
    // rendered text spills out of the culling boxes and labels butt together.
    const chars = overlay._deck.layerManager.layers.find(l => l.id.includes('hood-labels-characters'));
    const deckSizeScale = chars ? chars.props.sizeScale : null;
    const cfg = METRICS[state.metric];
    const tall = all.reduce((a, b) => (a.p[cfg.key] || 0) > (b.p[cfg.key] || 0) ? a : b);
    const names = new Set(shown.map(d => d.name));
    return {
      total: all.length,
      shown: shown.length,
      badAnchors: badAnchor.map(d => d.name),
      overlaps,
      hasWihkwentowinAnchor: all.some(d => d.name === 'WÎHKWÊNTÔWIN'),
      deckSizeScale,
      drawScaleCovers: deckSizeScale != null && LABEL_DRAW_SCALE >= deckSizeScale,
      biggestShown: names.has(all.reduce((a, b) => a.area > b.area ? a : b).name),
      tallest: tall.name,
      tallZOk: Math.abs(labelZ(tall.p) - (tall.p[cfg.key] * cfg.elevationScale + 60)) < 1e-6,
    };
  });
  console.log('culling          :', JSON.stringify(culling));

  // Zooming in must reveal more labels (moveend re-cull).
  const cityShown = culling.shown;
  await page.evaluate(() => map.jumpTo({ center: [-113.51, 53.54], zoom: 12.2, pitch: 52, bearing: -18 }));
  await page.waitForTimeout(3000);
  const zoomShown = (await snap()).shown;
  console.log('zoom re-cull     :', JSON.stringify({ cityShown, zoomShown, more: zoomShown > cityShown }));
  await page.evaluate(() => map.jumpTo({ center: [-113.50, 53.52], zoom: 10.2, pitch: 52, bearing: -18 }));
  await page.waitForTimeout(3000);

  // Labels must survive every view; residential-lens disable rules unchanged.
  for (const v of ['roads', 'ratio', 'uses', 'money']) {
    await page.$eval(`#views button[data-view="${v}"]`, b => b.click());
    await page.waitForTimeout(v === 'money' ? 2000 : 5000); // lazy fetches
    console.log(`${v.padEnd(5)}, labels ON :`, JSON.stringify(await snap()));
  }

  // Ratio z: a kept hood labels at its prism roof, an off-scale hood at ~ground.
  await page.$eval('#views button[data-view="ratio"]', b => b.click());
  await page.waitForTimeout(3000);
  const ratioZ = await page.evaluate(() => {
    const kept = labelAnchors().find(d => ratioKept(d.p));
    const off = labelAnchors().find(d => !ratioKept(d.p));
    const s = ratioScale();
    return {
      keptZOk: Math.abs(labelZ(kept.p) - (ratioOf(kept.p) * s.elevationScale + 60)) < 1e-6,
      offZ: labelZ(off.p), // expect exactly 60 (ground + lift)
    };
  });
  console.log('ratio z          :', JSON.stringify(ratioZ));

  await page.$eval('#views button[data-view="money"]', b => b.click());
  await page.waitForTimeout(1500);
  await page.$eval('#lens button[data-lens="labels"]', b => b.click());
  await page.waitForTimeout(1000);
  console.log('money, labels off:', JSON.stringify(await snap()));

  await browser.close();
})();

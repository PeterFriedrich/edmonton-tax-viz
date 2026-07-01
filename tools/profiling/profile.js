const { chromium } = require('playwright');
const url = process.argv[2];
const label = process.argv[3] || url;

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000); // let deck.gl settle

  // inject a frame-time collector
  await page.evaluate(() => {
    window.__frames = [];
    let last = performance.now();
    function tick(t) { window.__frames.push(t - last); last = t; window.__raf = requestAnimationFrame(tick); }
    window.__raf = requestAnimationFrame(tick);
  });

  // drive a continuous ctrl+drag rotate across the map to force re-renders
  const cx = 640, cy = 420;
  await page.keyboard.down('Control');
  await page.mouse.move(cx, cy);
  await page.mouse.down();
  const STEPS = 90;
  for (let i = 0; i < STEPS; i++) {
    const x = cx + Math.round(180 * Math.sin(i / STEPS * Math.PI * 2));
    await page.mouse.move(x, cy);
    await page.waitForTimeout(16); // ~1.5s of dragging
  }
  await page.mouse.up();
  await page.keyboard.up('Control');

  const stats = await page.evaluate(() => {
    const f = window.__frames.filter(d => d > 0 && d < 2000);
    const s = [...f].sort((a, b) => a - b);
    const pct = p => s[Math.min(s.length - 1, Math.floor(p / 100 * s.length))] || 0;
    const mean = f.reduce((a, b) => a + b, 0) / (f.length || 1);
    return { frames: f.length, mean, median: pct(50), p95: pct(95), max: Math.max(...f, 0) };
  });

  const fps = 1000 / stats.mean;
  console.log(
    `${label.padEnd(22)} | frames ${String(stats.frames).padStart(4)} | ` +
    `mean ${stats.mean.toFixed(1)}ms (${fps.toFixed(1)} fps) | ` +
    `median ${stats.median.toFixed(1)}ms | p95 ${stats.p95.toFixed(1)}ms | max ${stats.max.toFixed(0)}ms`
  );
  await browser.close();
})();

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });

  const msgs = [];
  page.on('console', m => msgs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', e => msgs.push(`[pageerror] ${e.message}`));
  page.on('requestfailed', r => msgs.push(`[reqfail] ${r.url()} ${r.failure()?.errorText}`));

  await page.goto('http://localhost:8777/index.html', { waitUntil: 'networkidle', timeout: 30000 });
  // give deck.gl a few frames to fetch geojson + render the extrusion
  await page.waitForTimeout(4000);

  // does a non-empty deck canvas exist?
  const canvasInfo = await page.evaluate(() => {
    const cs = [...document.querySelectorAll('canvas')];
    return cs.map(c => ({ w: c.width, h: c.height }));
  });

  await page.screenshot({ path: 'render.png' });
  console.log('canvases:', JSON.stringify(canvasInfo));
  console.log('--- browser messages ---');
  console.log(msgs.join('\n') || '(none)');
  await browser.close();
})();

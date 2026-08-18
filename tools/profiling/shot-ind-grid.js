// Screenshot the industrial 100 m grid (SPEC_industrial.md A3, 2026-08-18).
// Scratch visual check — playwright is not resolvable from /tmp, so scratch
// scripts live here (session gotcha, hit repeatedly).
//   node shot-ind-grid.js <url> [outdir]
const { chromium } = require('playwright');
const [url, outdir = '/tmp'] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  const click = sel => page.$eval(sel, b => b.click());

  await click('#views button[data-view="development"]');
  await page.waitForTimeout(2000);
  await click('#devmetric button[data-devmetric="industrial"]');
  await page.waitForTimeout(1500);
  await click('#devdetail button[data-devdetail="grid"]');
  await page.waitForTimeout(2000);

  // Tilt so the spikes read as heights, not as dots.
  await page.evaluate(() => {
    overlay._deck.setProps({
      viewState: { longitude: -113.49, latitude: 53.52, zoom: 10.2,
                   pitch: 55, bearing: 20 },
    });
  });
  await page.waitForTimeout(2500);

  for (const [win, label] of [['long', '2009-2025'], ['5yr', '2021-2025']]) {
    await page.evaluate(w => {
      document.querySelector(`#devwindow button[data-devwindow="${w}"]`).click();
    }, win);
    await page.waitForTimeout(2200);
    const out = `${outdir}/ind-grid-${win}.png`;
    await page.screenshot({ path: out });
    const info = await page.evaluate(() => {
      const l = overlay._deck.props.layers.find(x => x.id === 'dev-grid-cells');
      const h = l.props.data.map(d => l.props.getElevation(d) * l.props.elevationScale)
        .sort((a, b) => a - b);
      const q = p => h[Math.floor((h.length - 1) * p)];
      return { cells: h.length, median: +q(.5).toFixed(1), p90: +q(.9).toFixed(0),
               max: +h[h.length - 1].toFixed(0),
               atFloor: h.filter(v => v <= 6.001).length,
               legend: document.getElementById('legend-label').textContent };
    });
    console.log(label, JSON.stringify(info));
    console.log('  ->', out);
  }
  await browser.close();
})();

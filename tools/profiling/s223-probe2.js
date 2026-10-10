const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'] });
  const p = await b.newPage({ viewport: {width:360,height:740}, hasTouch: true, isMobile: true });
  await p.goto(process.argv[2], { waitUntil: 'networkidle' }); await p.waitForTimeout(4000);
  const st = () => p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  await p.evaluate(() => applyMetric('revenue_per_acre')); await st();
  await p.evaluate(() => document.getElementById('title').click()); await st();
  await p.evaluate(() => applyMetric('nonres_revenue_per_acre')); await st();
  await p.evaluate(() => applyHoodMode('panel', true)); await st();
  await p.evaluate(() => openTemporal('DOWNTOWN')); await st(); await p.waitForTimeout(1500); await st();
  console.log(await p.evaluate(() => {
    const out = [];
    const w = document.createTreeWalker(document.getElementById('millrates'), NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) { if (!n.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
      for (const q of r.getClientRects()) out.push(`${Math.round(q.top)}-${Math.round(q.bottom)} ${n.textContent.trim().slice(0,40)}`); }
    const ms = getComputedStyle(document.getElementById('millrates'));
    out.push('pad-bottom ' + ms.paddingBottom + ' margin-bottom ' + ms.marginBottom);
    out.push('title text: ' + document.querySelector('#title-p').textContent.trim().slice(0,400));
    return out.join('\n');
  }));
  await p.screenshot({ path: process.argv[3] });
  process.exit(0);
})();

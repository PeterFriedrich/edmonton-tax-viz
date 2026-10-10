const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'] });
  for (const vp of [{width:390,height:844},{width:360,height:740}]) {
    const p = await b.newPage({ viewport: vp, hasTouch: true, isMobile: true });
    await p.goto(process.argv[2], { waitUntil: 'networkidle' }); await p.waitForTimeout(4000);
    const st = () => p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    const m = (label) => p.evaluate(l => {
      const g = id => { const e = document.getElementById(id); if (!e) return null; const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
        return `${id}:${Math.round(r.top)}-${Math.round(r.bottom)} h${Math.round(r.height)} disp=${cs.display} maxH=${cs.maxHeight} pos=${cs.position}`; };
      return l + '\n  ' + ['title','title-p','millrates','temporal','legend','controls'].map(g).join('\n  ');
    }, label);
    await p.evaluate(() => applyMetric('revenue_per_acre')); await st();
    await p.evaluate(() => document.getElementById('title').click()); await st();
    console.log(vp.width, await m('blurb open'));
    await p.evaluate(() => applyMetric('nonres_revenue_per_acre')); await st();
    console.log(await m('nonres'));
    await p.evaluate(() => applyHoodMode('panel', true)); await st();
    await p.evaluate(() => openTemporal('DOWNTOWN')); await st(); await p.waitForTimeout(1500); await st();
    console.log(await m('pinned'));
    await p.close();
  }
  process.exit(0);
})();

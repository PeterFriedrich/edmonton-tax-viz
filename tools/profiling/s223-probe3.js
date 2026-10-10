const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'] });
  for (const vp of [{width:390,height:844},{width:360,height:740},{width:320,height:640}]) {
  const p = await b.newPage({ viewport: vp, hasTouch: true, isMobile: true });
  await p.goto(process.argv[2], { waitUntil: 'networkidle' }); await p.waitForTimeout(4000);
  const st = () => p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  for (const state of ['collapsed','expanded']) {
    if (state==='expanded') { await p.evaluate(() => document.getElementById('title').click()); await st(); }
    console.log(vp.width, state, await p.evaluate(() => {
      const t = document.getElementById('title'); const r = t.getBoundingClientRect(); const cs = getComputedStyle(t);
      return JSON.stringify({left:r.left,right:r.right,w:r.width,maxW:cs.maxWidth,boxSizing:cs.boxSizing,padL:cs.paddingLeft,padR:cs.paddingRight,
        docW:document.documentElement.scrollWidth, clientW:document.documentElement.clientWidth, inner:innerWidth,
        overflowX: t.scrollWidth - t.clientWidth});
    }));
  }
  if (vp.width===390) await p.screenshot({ path: process.argv[3] });
  await p.close(); }
  process.exit(0);
})();

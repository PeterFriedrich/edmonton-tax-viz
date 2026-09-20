const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const w of [390, 768, 1280]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    for (const f of process.argv.slice(2)) {
      await p.goto('file://' + f, { waitUntil: 'load' });
      await p.waitForTimeout(400);
      const r = await p.evaluate(() => {
        const eds = [...document.querySelectorAll('.jp-InputArea-editor')];
        const clipped = eds.filter(e => e.scrollWidth > e.clientWidth + 2);
        const worst = clipped.reduce((a,e)=>Math.max(a, e.scrollWidth - e.clientWidth), 0);
        return { total: eds.length, clipped: clipped.length, worstPx: worst };
      });
      console.log(`${String(w).padStart(4)}px  ${f.split('/').pop().padEnd(32)} clipped ${r.clipped}/${r.total} cells, worst ${r.worstPx}px lost`);
    }
    await p.close();
  }
  await b.close();
})();

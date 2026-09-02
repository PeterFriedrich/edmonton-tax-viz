const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl']});
  const page = await b.newPage({viewport:{width:1280,height:800}});
  await page.goto(process.argv[2], {waitUntil:'networkidle',timeout:30000});
  await page.waitForTimeout(4000);
  console.log(JSON.stringify(await page.evaluate(() => {
    const p = state.data.features.find(f => f.properties.road_m_per_acre > 0 && f.properties.revenue_per_acre != null).properties;
    return { view: state.view, metric: state.metric, isRev: typeof isRevenue==='function' ? isRevenue(state.metric) : 'n/a',
             roadm: p.road_m_per_acre, hasTooltipFor: typeof tooltipFor, html: (typeof tooltipFor==='function' && tooltipFor(p)) ? tooltipFor(p).html : null };
  }), null, 1));
  await b.close();
})();

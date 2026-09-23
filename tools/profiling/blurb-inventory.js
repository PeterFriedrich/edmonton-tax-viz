// Inventory of every public title blurb (TODO "Public blurb cleanup",
// COPY_DECISIONS.md group B). Clicks through each public view x control state
// and writes {state, title, blurb, chars, h} rows; h = #title panel height.
// Re-run after a rewrite to re-measure lengths.
//   node blurb-inventory.js "<url>?build=public" out.json
const { chromium } = require('playwright');
const [url, out] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'] });
  const page = await browser.newPage({ viewport: { width: 1366, height: 768 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(5000);
  const click = sel => page.evaluate(s => { const b = document.querySelector(s); if (!b) throw new Error('no ' + s); b.click(); }, sel);
  const vis = sel => page.evaluate(s => { const b = document.querySelector(s); return !!b && b.offsetParent !== null; }, sel);
  const rows = [];
  const grab = async (state) => {
    await page.waitForTimeout(2500);
    const r = await page.evaluate(() => ({
      title: document.getElementById('title-h').textContent,
      blurb: document.getElementById('title-p').textContent.replace(/\s+/g, ' ').trim(),
      h: Math.round(document.getElementById('title').getBoundingClientRect().height),
    }));
    rows.push({ state, ...r, chars: r.blurb.length });
    console.log(state, r.blurb.length, r.h);
  };
  const colour = async on => {
    const act = await page.evaluate(() => document.getElementById('coloradj-btn').classList.contains('active'));
    if (act !== on) await click('#coloradj-btn');
  };
  // Money
  await click('#views button[data-view="money"]');
  for (const [m, cuts] of [['revenue', ['revenue_per_acre','res_revenue_per_acre','nonres_revenue_per_acre']], ['value', [null]]]) {
    await click(`#metric-row button[data-metric="${m}"]`);
    if (m === 'value') await click('#moneymode button[data-moneymode="current"]');
    for (const c of cuts) {
      if (c) await click(`#revcut button[data-revcut="${c}"]`);
      for (const d of ['hood','grid','grid-fine']) {
        if (!(await vis(`#moneydetail button[data-moneydetail="${d}"]`))) { console.log('hidden detail', d); }
        await click(`#moneydetail button[data-moneydetail="${d}"]`);
        for (const den of ['ground','lot']) {
          await click(`button[data-denom="${den}"]`);
          for (const ca of [true,false]) { await colour(ca); await grab(`money/${m}/${c||'value'}/${d}/${den}/colour-${ca?'sqrt':'linear'}`); }
          await colour(true);
        }
      }
      await click('#moneydetail button[data-moneydetail="hood"]');
      await click('button[data-denom="ground"]');
    }
  }
  await click('#moneymode button[data-moneymode="change"]');
  for (const w of ['long','short']) { await click(`button[data-chgwindow="${w}"]`); await grab(`money/value/change/${w}`); }
  await click('#moneymode button[data-moneymode="current"]');
  await click('#metric-row button[data-metric="revenue"]');
  // Development
  await click('#views button[data-view="development"]');
  for (const dm of ['units','permits']) { await click(`button[data-devmetric="${dm}"]`);
    for (const w of ['3yr','5yr','long']) { await click(`button[data-devwindow="${w}"]`);
      for (const dd of ['hood','grid']) { await click(`button[data-devdetail="${dd}"]`); await grab(`dev/${dm}/${w}/${dd}`); } } }
  // Services
  await click('#views button[data-view="services"]');
  const svcs = await page.evaluate(() => [...document.querySelectorAll('#services .svc')].filter(e => e.offsetParent !== null).map(e => e.dataset.service));
  console.log('public services', svcs);
  for (const s of svcs) {
    // The colour radio only takes when the row's checkbox is on; check it, drive
    // it, then uncheck so the next state doesn't carry a "renders neutral" clause.
    await page.evaluate(s => { const r = document.querySelector(`#services .svc[data-service="${s}"]`);
      const cb = r.querySelector('.svc-on'); if (!cb.checked) cb.click(); r.querySelector('input[name="svc-driver"]').click(); }, s);
    await grab(`services/driver-${s}`);
    if (s !== 'roads') await page.evaluate(s => { document.querySelector('#services .svc[data-service="roads"] input[name="svc-driver"]').click();
      document.querySelector(`#services .svc[data-service="${s}"] .svc-on`).click(); }, s);
  }
  // Ratio
  await click('#views button[data-view="ratio"]');
  await grab('ratio/roads');
  require('fs').writeFileSync(out, JSON.stringify(rows, null, 1));
  await browser.close();
})();

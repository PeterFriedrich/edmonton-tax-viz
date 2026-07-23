// One-off verify for the Industrial permit-velocity metric (2026-07-18 —
// SPEC_industrial.md A3). The third #devmetric option in the Development view:
// new industrial (400-series) building permits per acre, count only, a
// hood-level choropleth. Checks: the button shows only when the data carries
// ind_permits_per_acre (SKIP-guard otherwise); selecting it drives the plane
// off ind_permits_per_acre with its own p97.5 clamp + title/blurb/legend; the
// tooltip shows a "N new industrial permits" count line (not dwelling units);
// the Detail toggle HIDES while industrial is up (choropleth-only, no cells);
// switching to Infill hides the Industrial button AND resets the metric to a
// residential column so the infill score never reads industrial; switching
// back to Development restores the button.
//   node verify-ind-permits.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

function approx(a, b, rel = 1e-6) { return Math.abs(a - b) <= rel * Math.max(Math.abs(a), Math.abs(b), 1); }

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

  const click = sel => page.$eval(sel, b => b.click());
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  await click('#views button[data-view="development"]');
  await page.waitForTimeout(2000);

  // --- column guard ---------------------------------------------------------
  const guard = await page.evaluate(() => ({
    has: state.hasIndPermits,
    btnShown: getComputedStyle(
      document.querySelector('#devmetric button[data-devmetric="industrial"]')
    ).display !== 'none',
  }));
  if (!guard.has) {
    check('industrial button hidden when column absent (guard)', !guard.btnShown);
    console.log('SKIP  data file predates ind_permits_per_acre — nothing more to verify');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }
  check('industrial button shown in Development when column present', guard.btnShown);

  // --- switch to Industrial --------------------------------------------------
  await click('#devmetric button[data-devmetric="industrial"]');
  await page.waitForTimeout(1500);
  const c = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const f = state.data.features.find(x => x.properties.ind_permits_per_acre > 0);
    // independent p97.5 of the non-null column
    const vals = state.data.features.map(x => x.properties.ind_permits_per_acre)
      .filter(v => v != null).sort((a, b) => a - b);
    const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
      return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
    return {
      metric: state.devMetric,
      title: document.getElementById('title-h').textContent,
      blurb: document.getElementById('title-p').textContent,
      label: document.getElementById('legend-label').textContent,
      fillIsColour: !!layer && layer.props.getFillColor(f).join() !== '',
      clamp: (typeof devScale === 'function') ? null : null, // devScale not in scope; use internal
      indepClamp: q(vals, 0.975),
      detailShown: getComputedStyle(document.getElementById('devdetail')).display !== 'none',
      detailHdShown: getComputedStyle(document.getElementById('devdetail-hd')).display !== 'none',
    };
  });
  console.log('industrial     :', JSON.stringify({ metric: c.metric, title: c.title, label: c.label }));
  check('state.devMetric switched to industrial', c.metric === 'industrial');
  check('title says New Industrial Building', /New Industrial Building/.test(c.title));
  check('blurb describes industrial permits (400-series)',
    /industrial building permits/.test(c.blurb) && /400-series/.test(c.blurb) &&
    /not dwelling units/.test(c.blurb));
  check('legend label says Industrial permits per acre',
    /Industrial permits per acre/.test(c.label));
  check('Detail toggle hidden while industrial is up (choropleth only)',
    !c.detailShown && !c.detailHdShown);

  // Plane drives off the industrial column, clamp == independent p97.5.
  const drive = await page.evaluate(() => {
    const layer = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const f = state.data.features.find(x => x.properties.ind_permits_per_acre > 0);
    // devT/devScale are closures — read the colour and compare to a hand rampColorAt.
    const col = 'ind_permits_per_acre';
    const vals = state.data.features.map(x => x.properties[col]).filter(v => v != null)
      .sort((a, b) => a - b);
    const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
      return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
    const clamp = q(vals, 0.975);
    const t = Math.sqrt(Math.max(0, Math.min(1, f.properties[col] / clamp)));
    const want = rampColorAt(t).join();
    const got = layer.props.getFillColor(f).slice(0, 3).join();
    return { want, got };
  });
  check('plane colour matches sqrt(ind_permits_per_acre / p97.5)', drive.want === drive.got,
    `want ${drive.want} got ${drive.got}`);

  // Tooltip: count line, not dwelling units.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(x => x.properties.ind_permits > 0);
    return f ? tooltipFor({ object: f }).html : null;
  });
  check('industrial tooltip shows a permit count line',
    tip && /new industrial permit/.test(tip) && !/dwelling unit/.test(tip),
    tip ? tip.replace(/<[^>]+>/g, ' ') : 'no ind hood');

  // --- Infill isolation ------------------------------------------------------
  await click('#devmode button[data-devmode="infill"]');
  await page.waitForTimeout(1500);
  const infill = await page.evaluate(() => ({
    metric: state.devMetric,
    btnShown: getComputedStyle(
      document.querySelector('#devmetric button[data-devmetric="industrial"]')
    ).display !== 'none',
    // the infill score must be reading a residential activity column
    scoreCol: (typeof devCol === 'function') ? devCol() : null,
  }));
  check('entering Infill resets devMetric off industrial', infill.metric !== 'industrial');
  check('Industrial button hidden in Infill', !infill.btnShown);
  check('infill activity column is a residential metric',
    infill.scoreCol === 'new_units_per_acre' || infill.scoreCol === 'new_permits_per_acre',
    infill.scoreCol);

  // --- back to Development restores the button -------------------------------
  await click('#views button[data-view="development"]');
  await page.waitForTimeout(1500);
  const back = await page.evaluate(() => getComputedStyle(
    document.querySelector('#devmetric button[data-devmetric="industrial"]')).display !== 'none');
  check('Industrial button restored in Development', back);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

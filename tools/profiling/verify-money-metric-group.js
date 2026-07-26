// Verify the two-level Money metric picker (2026-07-26).
//
// #toggle used to be a flat row of four peers — Revenue · Value · Residential $
// · Non-res $ — which misrepresented the data: `levy == res + nonres + farmland`
// (DECISIONS 2026-07-18), so the last two are SUBSETS of Revenue, not siblings
// of it. It is now Revenue | Value on top, with Total | Residential |
// Non-residential nested underneath, shown only under Revenue.
//
// The invariant worth protecting: METRICS stays flat and `state.metric` stays
// the single source of truth — only the chrome is hierarchical. So every check
// here asserts the CHROME against `state.metric`, never a parallel state field.
//   node tools/profiling/verify-money-metric-group.js <url>     (from REPO ROOT)
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

const CUTS = {
  revenue_per_acre: 'Total',
  res_revenue_per_acre: 'Residential',
  nonres_revenue_per_acre: 'Non-residential',
};

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  const probe = () => page.evaluate(() => {
    const row = sel => [...document.querySelectorAll(sel)].map(b => ({
      label: b.textContent.trim(),
      key: b.dataset.revcut || b.dataset.metric,
      active: b.classList.contains('active'),
      shown: getComputedStyle(b).display !== 'none',
    }));
    const box = el => { const r = el.getBoundingClientRect();
                        return { l: Math.round(r.left), r: Math.round(r.right) }; };
    return {
      metric: state.metric,
      metricRow: row('#metric-row button'),
      cuts: row('#revcut button'),
      cutRowShown: document.getElementById('revcut').offsetParent !== null,
      podShown: document.getElementById('toggle').offsetParent !== null,
      title: document.getElementById('title-h').textContent,
      legend: document.querySelector('#legend .lbl')?.textContent
              ?? document.getElementById('legend').textContent.trim().split('\n')[0],
      pod: box(document.getElementById('toggle')),
      mRow: box(document.getElementById('metric-row')),
      cRow: box(document.getElementById('revcut')),
    };
  });
  const goView = async v => { await page.click(`#views button[data-view="${v}"]`);
                              await page.waitForTimeout(2500); };

  // --- structure: two rows, right buttons, no leftover "$" labels
  const p0 = await probe();
  check('metric row is exactly Revenue | Value',
        p0.metricRow.map(b => b.label).join('|') === 'Revenue|Value',
        p0.metricRow.map(b => b.label).join('|'));
  check('cut row is exactly Total | Residential | Non-residential',
        p0.cuts.map(b => b.label).join('|') === 'Total|Residential|Non-residential',
        p0.cuts.map(b => b.label).join('|'));
  // The old labels leaned on a "$" suffix to say "these are dollars"; the parent
  // Revenue button carries that now, which was half the point of the regroup.
  check('no "$"-suffixed labels survive anywhere in the pod',
        !/\$/.test([...p0.metricRow, ...p0.cuts].map(b => b.label).join(' ')));

  // --- defaults
  check('opens on Revenue', p0.metricRow.find(b => b.key === 'revenue').active === true);
  check('opens on the Total cut', p0.cuts.find(b => b.key === 'revenue_per_acre').active === true);
  check('state.metric is the total-revenue column', p0.metric === 'revenue_per_acre', p0.metric);
  check('cut row visible under Revenue', p0.cutRowShown === true);

  // --- exactly one active per row, always (the rows are radio groups)
  const oneActive = (p, where) => {
    check(`[${where}] exactly one active in the metric row`,
          p.metricRow.filter(b => b.active).length === 1);
    check(`[${where}] at most one active in the cut row`,
          p.cuts.filter(b => b.active).length <= 1);
  };
  oneActive(p0, 'initial');

  // --- each cut drives the real column + retitles + relabels the legend
  const seen = new Set();
  for (const [key, label] of Object.entries(CUTS)) {
    await page.click(`#revcut button[data-revcut="${key}"]`);
    await page.waitForTimeout(2500);
    const p = await probe();
    check(`[${label}] state.metric follows the cut`, p.metric === key, p.metric);
    check(`[${label}] that cut is the active one`,
          p.cuts.find(b => b.key === key).active === true);
    check(`[${label}] Revenue stays active in the parent row`,
          p.metricRow.find(b => b.key === 'revenue').active === true);
    check(`[${label}] title changed to match the cut`, !seen.has(p.title), p.title);
    seen.add(p.title);
    oneActive(p, label);
  }

  // --- Value is a leaf: the cut row must disappear (no decomposition exists)
  await page.click('#metric-row button[data-metric="value"]');
  await page.waitForTimeout(2500);
  const pv = await probe();
  check('[Value] state.metric is the value column', pv.metric === 'value_per_acre', pv.metric);
  check('[Value] cut row HIDES (value has no res/nonres columns)', pv.cutRowShown === false);
  check('[Value] no cut is left marked active', pv.cuts.every(b => !b.active));
  oneActive(pv, 'Value');

  // --- returning to Revenue restores the cut you left, not a silent reset
  await page.click('#metric-row button[data-metric="revenue"]');
  await page.waitForTimeout(2500);
  const pr = await probe();
  check('[Revenue] restores the LAST cut used (sticky, was Non-residential)',
        pr.metric === 'nonres_revenue_per_acre', pr.metric);
  check('[Revenue] cut row returns', pr.cutRowShown === true);

  // --- geometry: the two rows share the pod width (no dead cell beside Revenue)
  check('both rows span the full pod width',
        pr.mRow.l === pr.cRow.l && pr.mRow.r === pr.cRow.r,
        `metric ${pr.mRow.l}..${pr.mRow.r} vs cut ${pr.cRow.l}..${pr.cRow.r}`);

  // --- real clicks (the JS-.click() suites cannot see pointer-events problems)
  for (const sel of ['#metric-row button[data-metric="value"]',
                     '#metric-row button[data-metric="revenue"]',
                     '#revcut button[data-revcut="revenue_per_acre"]']) {
    const el = page.locator(sel);
    const box = await el.boundingBox();
    const top = box && await page.evaluate(({ x, y }) => {
      const e = document.elementFromPoint(x, y);
      return e && (e.dataset.metric || e.dataset.revcut) || (e && e.id) || 'nothing';
    }, { x: box.x + box.width / 2, y: box.y + box.height / 2 });
    check(`hit-test reaches ${sel.match(/"(.*?)"/)[1]}`,
          top === (sel.includes('revcut') ? 'revenue_per_acre'
                   : sel.includes('value') ? 'value' : 'revenue'), `topmost=${top}`);
  }

  // --- the picker still works in Money's 100 m grid (the grid carries the cuts)
  await page.click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3500);
  const pg = await probe();
  check('[100 m grid] cut row still offered', pg.cutRowShown === true, `view via title: ${pg.title}`);
  await page.click('#revcut button[data-revcut="res_revenue_per_acre"]');
  await page.waitForTimeout(3000);
  check('[100 m grid] a cut still drives state.metric',
        (await probe()).metric === 'res_revenue_per_acre');
  await page.click('#moneydetail button[data-moneydetail="hood"]');
  await page.waitForTimeout(3000);

  // --- the whole pod is Money-scoped; the cut row must not outlive it
  for (const v of ['services', 'ratio', 'development']) {
    await goView(v);
    const p = await probe();
    check(`[${v}] whole metric pod hidden`, p.podShown === false);
    check(`[${v}] cut row hidden with it`, p.cutRowShown === false);
  }
  await goView('money');
  check('[money] pod returns after the tour', (await probe()).podShown === true);

  // --- data gate: with BOTH cut columns absent, Revenue is a leaf and the row
  // collapses rather than showing a pointless one-button "Total" row. Driven
  // white-box (hide the buttons, re-sync) because there is no old-format
  // fixture to load.
  const collapsed = await page.evaluate(() => {
    const b = k => document.querySelector(`#revcut button[data-revcut="${k}"]`);
    const prev = [b('res_revenue_per_acre').style.display, b('nonres_revenue_per_acre').style.display];
    b('res_revenue_per_acre').style.display = 'none';
    b('nonres_revenue_per_acre').style.display = 'none';
    syncMetricButtons();
    const shown = document.getElementById('revcut').offsetParent !== null;
    b('res_revenue_per_acre').style.display = prev[0];
    b('nonres_revenue_per_acre').style.display = prev[1];
    syncMetricButtons();
    return shown;
  });
  check('cut row collapses when NEITHER cut column exists', collapsed === false);
  check('cut row restored after the probe', (await probe()).cutRowShown === true);

  // --- the tooltip accuracy fix: res + nonres do NOT sum to total (farmland)
  const tip = await page.getAttribute('#revcut button[data-revcut="nonres_revenue_per_acre"]', 'title');
  check('non-residential tooltip no longer claims to be the "complement"',
        !/complement/i.test(tip));
  check('non-residential tooltip names farmland as the reason they do not sum',
        /farmland/i.test(tip), tip.slice(-70));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

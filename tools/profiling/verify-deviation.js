// Verify the experimental deviation lens ("vs city average", full build only).
//
// The three things that fail SILENTLY here, in order of how badly:
//   1. the citywide average is recomputed from an external levy total instead
//      of the served features, moving the zero line and reclassifying hoods;
//   2. the deficit prisms do not actually extrude downward (deck.gl clamping a
//      negative getElevation at 0 would leave a map that looks fine and says
//      nothing);
//   3. the lens leaks into the public build.
// Each gets an assertion against numbers re-derived in the page, not pinned.
const { chromium } = require('playwright');

const EPS = 1e-6;
let failures = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) failures++;
};

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });

  // --- full build --------------------------------------------------------
  await page.goto('http://localhost:8777/index.html?build=full', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3500);

  // Enter the lens: Revenue is the default metric, so #moneymode is already
  // showing its deviation button.
  const btn = page.locator('#moneymode button[data-moneymode="deviation"]');
  check('deviation button exists in full build', await btn.count() === 1);
  check('deviation button is visible under Revenue', await btn.isVisible());
  check('change button is HIDDEN under Revenue',
    !(await page.locator('#moneymode button[data-moneymode="change"]').isVisible()));
  check('button carries a beta tag', (await btn.innerText()).toLowerCase().includes('beta'));

  await btn.click();
  await page.waitForTimeout(1200);
  // Shot taken HERE, not at the end: the last assertions deliberately leave the
  // page on the Value map, and a screenshot named deviation.png showing some
  // other lens is worse than no screenshot.
  await page.screenshot({ path: 'deviation.png' });

  const st = await page.evaluate(() => {
    const feats = state.data.features.map(f => f.properties);
    return {
      view: state.view,
      title: document.getElementById('title-h').textContent,
      blurb: document.getElementById('title-p').textContent,
      legend: document.getElementById('legend-label').textContent,
      legendMin: document.getElementById('legend-min').textContent,
      legendMax: document.getElementById('legend-max').textContent,
      moneyBtnActive: document.querySelector('#views button[data-view="money"]').classList.contains('active'),
      stats: deviationStats(),
      // Re-derive the average here, independently of the page's own helper.
      indep: (() => {
        let rev = 0, acres = 0;
        for (const p of feats) {
          if (!p.revenue_per_acre || p.total_revenue == null) continue;
          rev += p.total_revenue;
          acres += p.total_revenue / p.revenue_per_acre;
        }
        return { avg: rev / acres, acres, rev };
      })(),
      // Elevation is read off the LIVE LAYER's accessor, not recomputed here —
      // that is what makes "the deficit really extrudes downward" a claim about
      // what deck.gl was handed rather than about our arithmetic.
      elev: (() => {
        const layer = overlay._props.layers.find(l => l.id === 'deviation-extrusion');
        const get = layer.props.getElevation;
        let negative = 0, positive = 0, setAsideNonZero = 0;
        let minValue = Infinity, maxValue = -Infinity;
        for (const f of state.data.features) {
          const z = get(f);
          if (f.properties.is_set_aside) { if (z !== 0) setAsideNonZero++; continue; }
          if (z < 0) negative++; else if (z > 0) positive++;
          minValue = Math.min(minValue, z);
          maxValue = Math.max(maxValue, z);
        }
        return { negative, positive, setAsideNonZero, minValue, maxValue,
                 scored: negative + positive, scale: layer.props.elevationScale };
      })(),
    };
  });

  check('view switched to deviation', st.view === 'deviation', st.view);
  check('Money #views button stays active', st.moneyBtnActive);
  check('title names the comparison', /vs the Citywide Average/i.test(st.title), st.title);

  // 1 — the average comes from the served features.
  check('citywide average == sum(total_revenue) / sum(derived acres)',
    Math.abs(st.stats.avg - st.indep.avg) < EPS,
    `page ${st.stats.avg.toFixed(6)} vs independent ${st.indep.avg.toFixed(6)}`);
  // Guards the specific wrong answer: the City's budgeted levy over the same
  // acres. If someone swaps the numerator this is what the average becomes.
  const budgetAvg = 2317789000 / st.indep.acres;
  check('average is NOT the external budgeted-levy figure',
    Math.abs(st.stats.avg - budgetAvg) > 1,
    `modelled ${st.stats.avg.toFixed(0)} vs budgeted-levy ${budgetAvg.toFixed(0)}`);

  // 2 — the deficit half really extrudes below the plane.
  check('some hoods extrude BELOW the ground plane', st.elev.negative > 0,
    `${st.elev.negative} negative of ${st.elev.scored} scored`);
  check('some hoods extrude above', st.elev.positive > 0, `${st.elev.positive}`);
  check('set-aside hoods are flat', st.elev.setAsideNonZero === 0,
    `${st.elev.setAsideNonZero} set-aside hoods with non-zero height`);
  // True-to-scale, and the floor is a BOUND rather than an observed value: no
  // hood can dive past -average (revenue per acre cannot be negative), and the
  // deepest one gets close because the quietest hoods sit near $0/acre. Both
  // halves matter — a breach means the arithmetic is wrong, and a deepest dive
  // far short of the floor would mean the blurb overstates the range.
  check('no hood dives past the -average floor',
    st.elev.minValue >= -st.stats.avg - EPS,
    `min ${st.elev.minValue.toFixed(0)} vs floor ${(-st.stats.avg).toFixed(0)}`);
  check('the deepest deficit reaches the floor within 1%',
    Math.abs(st.elev.minValue - -st.stats.avg) < 0.01 * st.stats.avg,
    `min ${st.elev.minValue.toFixed(0)} vs floor ${(-st.stats.avg).toFixed(0)}`);
  check('surplus arm dwarfs deficit arm (true to scale)',
    st.elev.maxValue > 5 * Math.abs(st.elev.minValue),
    `+${st.elev.maxValue.toFixed(0)} vs ${st.elev.minValue.toFixed(0)}`);

  // 3 — copy honesty. The lens must never be named as a cost comparison.
  const copy = (st.title + ' ' + st.blurb + ' ' + st.legend).toLowerCase();
  check('blurb disclaims the cost reading', /not a cost-of-service comparison/.test(copy));
  check('blurb marks it experimental', /experimental/.test(copy));
  check('blurb states the floor', /floor/.test(copy));
  check('no "cost of service" / "COSA" naming of the lens itself',
    !/\bcosa\b/.test(copy) && !/cost of service/.test(copy), copy.slice(0, 120));
  check('legend names the average it measures against',
    /citywide average/i.test(st.legend) && /\$/.test(st.legend), st.legend);
  check('legend ends are signed', st.legendMin.includes('−$') && st.legendMax.includes('+$'),
    `${st.legendMin} | ${st.legendMax}`);

  // Tooltip prints both terms, so the signed number is checkable.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(x => !x.properties.is_set_aside);
    return viewTooltip({ object: f }).html;
  });
  check('tooltip prints the hood value AND the citywide average',
    /here/.test(tip) && /citywide/.test(tip), tip.replace(/<[^>]+>/g, ' ').slice(0, 110));

  // Switching the revenue cut must re-render, not just repaint the buttons.
  const before = st.stats.avg;
  await page.locator('#revcut button[data-revcut="res_revenue_per_acre"]').click();
  await page.waitForTimeout(900);
  const after = await page.evaluate(() => ({
    avg: deviationStats().avg,
    title: document.getElementById('title-h').textContent,
    view: state.view,
  }));
  check('revenue cut re-renders the lens', Math.abs(after.avg - before) > 1 && after.view === 'deviation',
    `total ${before.toFixed(0)} -> residential ${after.avg.toFixed(0)}`);
  check('title follows the cut', /Residential/i.test(after.title), after.title);

  // Leaving Revenue for Value must leave the lens (it reads a revenue column).
  await page.locator('#metric-row button[data-metric="value"]').click();
  await page.waitForTimeout(900);
  check('switching to Value exits the deviation view',
    await page.evaluate(() => state.view) === 'money');

  // --- public build ------------------------------------------------------
  await page.goto('http://localhost:8777/index.html?build=public', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  check('deviation button HIDDEN in public build',
    !(await page.locator('#moneymode button[data-moneymode="deviation"]').isVisible()));

  check('no page errors', errs.length === 0, errs.slice(0, 3).join(' | '));

  await browser.close();
  console.log(failures ? `\n${failures} FAILURE(S)` : '\nall checks passed');
  process.exit(failures ? 1 : 0);
})();

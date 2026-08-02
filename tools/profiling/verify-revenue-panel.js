// Money's REVENUE PANEL: on the revenue metrics the pinned panel shows where a
// neighbourhood's levy comes from, by zone category, instead of the assessment
// history (Peter, 2026-08-01: "for revenue I want the panel to just be the top
// contributing zones by percent of hood revenue").
//
// What this script is defending, in order of how quietly it would fail:
//   1. **The numbers come from the SERVED geojson.** Every share is recomputed
//      here from the raw file, so nothing below can be satisfied by the app
//      agreeing with itself.
//   2. **The borrowed CSS.** The colour bar reuses `.mixbar`, whose rule was
//      scoped `.tip .mixbar, #peek-read .mixbar`. Borrowing the markup without
//      the selector loses `display:flex` and collapses the bar to NOTHING
//      VISIBLE — the exact S83 failure, which no id-based assertion would see.
//   3. **The lens swap.** The panel's content is lens-dependent now, so a
//      metric or view change while a hood is pinned has to re-render it. A
//      revenue breakdown left under a value map is a silent-correctness bug.
//   4. **The denominator is NAMED.** The shares are of the hood's TOTAL levy,
//      but Residential / Non-residential colour one class of it — so on those
//      cuts the panel and the map divide by different things and the panel has
//      to say so.
//   5. **The copy that advertises the panel** (`#peek-go`, `#temporal-hint`,
//      the tooltip's invite) names the panel it actually opens.
//   6. **Sub-0.1% prints "<0.1%", never "0.0%"** — a category that earned a row
//      must not then claim to contribute nothing.
//   node verify-revenue-panel.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  const open = async (u, vp, opts = {}) => {
    const page = await browser.newPage({ viewport: vp, ...opts });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
    return page;
  };

  const page = await open(url, { width: 1440, height: 900 });

  // ---- 0. GROUND TRUTH from the served file, not from the app -------------
  const raw = await page.evaluate(async () => {
    const d = await (await fetch('./data/neighbourhood_value_per_acre.geojson')).json();
    const p = d.features.map(f => f.properties)
      .find(x => x.neighbourhood_name === 'DOWNTOWN');
    const mix = Object.keys(p).filter(k => k.startsWith('rev_frac_') && p[k] > 0)
      .map(k => [k, p[k]]).sort((a, b) => b[1] - a[1]);
    return { levy: p.total_revenue, share: p.revenue_share_city, mix,
             sum: mix.reduce((a, kv) => a + kv[1], 0) };
  });
  check('the served file carries the revenue columns',
    raw.levy > 0 && raw.share > 0 && raw.mix.length > 0,
    `levy=${raw.levy} share=${raw.share} cats=${raw.mix.length}`);
  check('the served shares sum to 1 (no unstated remainder)',
    Math.abs(raw.sum - 1) < 0.005, raw.sum.toFixed(6));

  // ---- 1. THE PANEL RENDERS THE MIX, NOT THE CHART ------------------------
  const panel = await page.evaluate(() => {
    applyMetric('revenue_per_acre');
    openTemporal('DOWNTOWN');
    const el = document.getElementById('temporal');
    const bar = el.querySelector('.mixbar');
    const rows = [...el.querySelectorAll('.revrow')].map(r => ({
      label: r.querySelector('span').textContent,
      pct: r.querySelector('b').textContent,
      swatch: getComputedStyle(r.querySelector('i')).backgroundColor,
      flex: 0,
    }));
    return {
      open: el.classList.contains('open'),
      hasChartSvg: !!el.querySelector('#temporal-chart svg'),
      barDisplay: bar ? getComputedStyle(bar).display : 'NO BAR',
      barWidth: bar ? Math.round(bar.getBoundingClientRect().width) : 0,
      segments: bar ? [...bar.querySelectorAll('span')].map(
        s => Math.round(s.getBoundingClientRect().width)) : [],
      rows,
      read: document.getElementById('temporal-read').textContent,
      note: document.getElementById('temporal-note').textContent,
      // The Uses lens's identity colour for the same category, so the two
      // lenses can be compared rather than assumed equal.
      usesColour: (() => {
        const u = USE_CATEGORIES.find(x => x.label === 'Commercial');
        return `rgb(${u.color.join(', ')})`;
      })(),
    };
  });
  check('the panel opens on a revenue metric', panel.open);
  check('*** it shows the mix, NOT the assessment chart ***', !panel.hasChartSvg);
  check('*** the borrowed .mixbar keeps display:flex ***',
    panel.barDisplay === 'flex', panel.barDisplay);
  check('the bar has real width (not collapsed)', panel.barWidth > 200, `${panel.barWidth}px`);
  check('every category got a bar segment',
    panel.segments.length === panel.rows.length &&
    panel.segments.every(w => w >= 0), `${panel.segments.length} segs`);

  // ---- 2. THE ROWS MATCH THE SERVED FILE ---------------------------------
  check('*** one row per non-zero category, none dropped ***',
    panel.rows.length === raw.mix.length, `${panel.rows.length} vs ${raw.mix.length}`);
  const pcts = panel.rows.map(r => r.pct);
  const expected = raw.mix.map(([, v]) =>
    v * 100 < 0.05 ? '<0.1%' : (v * 100).toFixed(1) + '%');
  check('*** every share matches the served file, in rank order ***',
    JSON.stringify(pcts) === JSON.stringify(expected),
    `${pcts.join(',')} vs ${expected.join(',')}`);
  check('rows are sorted largest first',
    panel.rows.every((r, i, a) => i === 0 ||
      parseFloat(a[i - 1].pct.replace('<', '')) >= parseFloat(r.pct.replace('<', ''))));
  // Downtown carries a 0.013% river-valley sliver — the case that would print
  // "0.0%" if the floor were a plain toFixed(1).
  check('*** a sub-0.1% category prints "<0.1%", never "0.0%" ***',
    pcts.includes('<0.1%') && !pcts.includes('0.0%'), pcts.join(','));

  // ---- 3. ONE CATEGORY SET WITH THE USES LENS ----------------------------
  const commercial = panel.rows.find(r => r.label === 'Commercial');
  check('the categories carry the Uses lens\'s own identity colour',
    commercial && commercial.swatch === panel.usesColour,
    commercial ? `${commercial.swatch} vs ${panel.usesColour}` : 'no Commercial row');

  // ---- 4. THE HEADER NUMBERS ---------------------------------------------
  // fmtBig (the history panel's formatter) rounds megas to whole numbers, which
  // would print a $1,876,137 levy as "$2M". The levy formatter keeps 2 decimals.
  const levyStr = '$' + (raw.levy / 1e6).toFixed(2) + 'M';
  check('*** the levy keeps 2-decimal precision (not fmtBig\'s rounding) ***',
    panel.read.includes(levyStr), `want ${levyStr}`);
  const shareStr = (raw.share * 100).toFixed(2) + '%';
  check('the city share is quoted to 2 decimals',
    panel.read.includes(shareStr), `want ${shareStr}`);
  check('the city share names what it is a share OF',
    /of Edmonton's municipal revenue/.test(panel.read));

  // ---- 5. THE DENOMINATOR IS NAMED ---------------------------------------
  check('*** the note names the TOTAL-levy denominator ***',
    /total municipal levy/.test(panel.note), panel.note.slice(0, 60));
  check('the note discloses the exempt-land gap',
    /exempt/i.test(panel.note));

  // The cuts colour one class while the panel describes all of them — the panel
  // must still show, and must still name its own denominator.
  for (const cut of ['res_revenue_per_acre', 'nonres_revenue_per_acre']) {
    const c = await page.evaluate((m) => {
      applyMetric(m);
      return { open: document.getElementById('temporal').classList.contains('open'),
               rows: document.querySelectorAll('.revrow').length,
               note: document.getElementById('temporal-note').textContent };
    }, cut);
    check(`${cut}: the panel still shows the mix`, c.open && c.rows > 0, `${c.rows} rows`);
    check(`${cut}: the total-levy denominator is still named`,
      /total municipal levy/.test(c.note));
  }

  // ---- 6. THE LENS SWAP RE-RENDERS A PINNED PANEL ------------------------
  const swap = await page.evaluate(() => {
    const state1 = () => ({
      chart: !!document.querySelector('#temporal-chart svg'),
      mix: document.querySelectorAll('.revrow').length,
      open: document.getElementById('temporal').classList.contains('open'),
    });
    applyMetric('revenue_per_acre');
    const rev = state1();
    applyMetric('value_per_acre');
    const val = state1();
    applyMetric('revenue_per_acre');
    const back = state1();
    return { rev, val, back };
  });
  check('*** switching to Value swaps in the assessment chart ***',
    swap.val.open && swap.val.chart && swap.val.mix === 0, JSON.stringify(swap.val));
  check('*** switching back to Revenue swaps the mix in again ***',
    swap.back.open && !swap.back.chart && swap.back.mix > 0, JSON.stringify(swap.back));
  check('the hood stays pinned across the swap', swap.rev.open && swap.val.open);

  // Leaving Money entirely: the breakdown is a Money readout, so it must not
  // survive into a view that does not draw revenue.
  const left = await page.evaluate(async () => {
    await applyView('development');
    return { chart: !!document.querySelector('#temporal-chart svg'),
             mix: document.querySelectorAll('.revrow').length };
  });
  check('*** leaving Money takes the revenue breakdown with it ***',
    left.mix === 0, `${left.mix} rows still shown`);
  await page.evaluate(async () => { await applyView('money'); applyMetric('revenue_per_acre'); });

  // ---- 7. THE COPY NAMES THE PANEL IT OPENS ------------------------------
  const copy = await page.evaluate(() => {
    const hint = () => document.getElementById('temporal-hint').textContent;
    const invite = () => {
      const f = state.data.features.find(
        x => x.properties.neighbourhood_name === 'DOWNTOWN');
      return tooltipFor({ object: f }).html;
    };
    applyMetric('revenue_per_acre');
    const rev = { hint: hint(), tip: invite() };
    applyMetric('value_per_acre');
    const val = { hint: hint(), tip: invite() };
    applyMetric('revenue_per_acre');
    return { rev, val };
  });
  check('*** the empty-panel prompt names the revenue panel ***',
    /where its revenue comes from/.test(copy.rev.hint), copy.rev.hint);
  check('the prompt still names history under Value',
    /assessment history/.test(copy.val.hint), copy.val.hint);
  check('*** the tooltip invite names the revenue mix, not "pin" ***',
    /click for the revenue mix/.test(copy.rev.tip) && !/click to pin/.test(copy.rev.tip));
  check('the tooltip invite is unchanged under Value',
    /click to pin/.test(copy.val.tip));

  // ---- 8. DEGRADES WITHOUT THE COLUMNS -----------------------------------
  // The columns arrived in the 2026-08-01 refresh. A stale geojson must fall
  // back to the history panel, not render an empty box.
  const degraded = await page.evaluate(() => {
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const saved = { ...f.properties };
    Object.keys(f.properties).forEach(k => {
      if (k === 'total_revenue' || k.startsWith('rev_frac_')) delete f.properties[k];
    });
    applyMetric('revenue_per_acre');
    openTemporal('DOWNTOWN');
    const out = {
      open: document.getElementById('temporal').classList.contains('open'),
      chart: !!document.querySelector('#temporal-chart svg'),
      mix: document.querySelectorAll('.revrow').length,
    };
    Object.assign(f.properties, saved);
    return out;
  });
  check('*** no revenue columns => falls back to the history panel ***',
    degraded.open && degraded.chart && degraded.mix === 0, JSON.stringify(degraded));
  await page.close();

  // ---- 9. TOUCH: the peek card advertises the right panel -----------------
  const phone = await open(url, { width: 390, height: 844 },
                           { hasTouch: true, isMobile: true });
  const touch = await phone.evaluate(() => {
    const props = n => state.data.features.find(
      x => x.properties.neighbourhood_name === n).properties;
    const go = () => document.getElementById('peek-go').textContent;
    applyMetric('revenue_per_acre');
    openPeek(props('DOWNTOWN'));
    const rev = go();
    closePeek();
    applyMetric('value_per_acre');
    openPeek(props('DOWNTOWN'));
    const val = go();
    closePeek();
    applyMetric('revenue_per_acre');
    openTemporal('DOWNTOWN');
    const el = document.getElementById('temporal');
    const bar = el.querySelector('.mixbar');
    return { rev, val,
             sheet: el.getBoundingClientRect().toJSON(),
             h: innerHeight, w: innerWidth,
             barDisplay: bar ? getComputedStyle(bar).display : 'NO BAR',
             rows: el.querySelectorAll('.revrow').length };
  });
  check('*** the peek card offers the revenue breakdown on revenue ***',
    /revenue breakdown/.test(touch.rev), touch.rev);
  check('the peek card still offers history under Value',
    /assessment history/.test(touch.val), touch.val);
  check('phone: the mix renders in the bottom sheet',
    touch.barDisplay === 'flex' && touch.rows > 0,
    `${touch.barDisplay} ${touch.rows} rows`);
  check('phone: the sheet still fits the viewport',
    touch.sheet.left >= 0 && touch.sheet.right <= touch.w &&
    touch.sheet.bottom <= touch.h + 1,
    `${touch.sheet.left}..${touch.sheet.right} of ${touch.w}, bottom ${touch.sheet.bottom.toFixed(0)}/${touch.h}`);
  await phone.close();

  // ---- 10. PUBLIC BUILD ---------------------------------------------------
  // Money is public and so are these columns — the breakdown must not be a
  // full-build accident.
  const pub = await open(url + (url.includes('?') ? '&' : '?') + 'build=public',
                         { width: 1440, height: 900 });
  const p = await pub.evaluate(() => {
    applyMetric('revenue_per_acre');
    openTemporal('DOWNTOWN');
    const el = document.getElementById('temporal');
    return { open: el.classList.contains('open'),
             rows: el.querySelectorAll('.revrow').length,
             barDisplay: el.querySelector('.mixbar')
               ? getComputedStyle(el.querySelector('.mixbar')).display : 'NO BAR',
             note: document.getElementById('temporal-note').textContent };
  });
  check('public build renders the revenue panel', p.open && p.rows > 0, `${p.rows} rows`);
  check('public build keeps the bar visible', p.barDisplay === 'flex', p.barDisplay);
  check('public build names the denominator', /total municipal levy/.test(p.note));
  await pub.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

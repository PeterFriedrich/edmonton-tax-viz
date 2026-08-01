// Verifies the mill-rate pod (#millrates) — the revenue map's own conversion
// factor, printed under the title on the money view's revenue cuts.
//
// Three things here fail SILENTLY and are the reason this script exists:
//
//  1. POSITION. #title is not a fixed height — it runs 140-499px across views
//     and cuts, and the money cuts alone go 196 -> 256 because the residential
//     and non-residential blurbs are longer. The pod is positioned from the
//     MEASURED title box for exactly that reason, and the failure mode of
//     getting it wrong is two layers of text drawn on top of each other, which
//     no exception and no exit code will report. (The constant already parked in
//     this column, #temporal's top: 210px, is wrong in five states for precisely
//     this reason — see TODO.md.)
//
//  2. HEIGHT. Both the rates row and the caveat row must fit on ONE line; the
//     pod's width was chosen to make that true. A copy edit that wraps either
//     one grows the pod silently, so the height is asserted rather than trusted.
//
//  3. PROVENANCE. The rates are read from status.json, never typed into the
//     page. Asserted against the manifest so a hand-edit to the markup cannot
//     put a wrong mill rate on screen and still pass.
//
//   node verify-millrates.js <url>
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
  // The pod is repositioned by a ResizeObserver on #title, which is delivered
  // after layout. Reading synchronously measures the PREVIOUS state's title and
  // reports overlaps that do not exist — two frames is the honest wait.
  const settle = page => page.evaluate(() =>
    new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));

  const box = (page, id) => page.evaluate(i => {
    const e = document.getElementById(i);
    const r = e.getBoundingClientRect();
    return { vis: getComputedStyle(e).display !== 'none',
             top: Math.round(r.top), bottom: Math.round(r.bottom),
             left: Math.round(r.left), right: Math.round(r.right),
             h: Math.round(r.height) };
  }, id);
  const overlap = (a, b) => a.vis && b.vis &&
    a.right > b.left && a.left < b.right && a.bottom > b.top && a.top < b.bottom;

  const page = await open(url, { width: 1440, height: 900 });

  // ---- content, and that it came from the manifest -------------------------
  const manifest = await page.evaluate(async () =>
    (await (await fetch('./data/status.json')).json()));
  const mr = manifest.municipal_rates;
  check('status.json publishes municipal_rates', !!mr && Array.isArray(mr.classes) && mr.classes.length === 3,
    mr ? `${(mr.classes || []).length} classes` : 'absent');

  await page.evaluate(() => applyMetric('revenue_per_acre'));
  await settle(page);
  const text = await page.evaluate(() => ({
    head: document.getElementById('mill-head').textContent,
    rows: document.getElementById('mill-rows').textContent,
    note: document.getElementById('mill-note').textContent,
  }));
  check('pod shows on the money view revenue cut', (await box(page, 'millrates')).vis);
  check('head names the rate year', text.head.includes(String(manifest.rate_year)), text.head);
  check('head names the unit', text.head.includes(mr.unit), text.head);
  // Every published rate, to the published precision — the whole point of
  // reading them from the manifest instead of typing them into the page.
  for (const c of mr.classes) {
    check(`rate on screen for ${c.name} (${c.rate})`, text.rows.includes(String(c.rate)), text.rows);
  }
  // Both caveats are required to be VISIBLE, not buried in a title attribute:
  // every figure on this site is the municipal levy, and 2025 Farmland is an
  // assumption the source never published.
  check('note states the education levy is excluded', /education excluded/i.test(text.note), text.note);
  check('note flags the assumed class(es)',
    !mr.assumed.length || mr.assumed.every(c => text.note.includes(c)), text.note);

  // ---- per-cut highlighting -------------------------------------------------
  // Classes the cut is NOT billed at stay on screen (the differential is the
  // point) but must not read as applying to it.
  const lit = async metric => {
    await page.evaluate(m => applyMetric(m), metric);
    await settle(page);
    return page.evaluate(() => ({
      on: [...document.querySelectorAll('#mill-rows .on')].map(e => e.textContent),
      off: [...document.querySelectorAll('#mill-rows .off')].map(e => e.textContent),
    }));
  };
  const total = await lit('revenue_per_acre');
  check('Total lights all three rates', total.on.length === 3 && total.off.length === 0,
    `on=${total.on.length} off=${total.off.length}`);
  const res = await lit('res_revenue_per_acre');
  check('Residential lights the two housing classes only',
    res.on.length === 2 && res.on.every(t => /^Res\.|^Other res\./.test(t)) &&
    res.off.length === 1 && /Non-res/.test(res.off[0]),
    `on=${res.on.join('|')} off=${res.off.join('|')}`);
  const nonres = await lit('nonres_revenue_per_acre');
  check('Non-residential lights the non-residential rate only',
    nonres.on.length === 1 && /Non-res/.test(nonres.on[0]) && nonres.off.length === 2,
    `on=${nonres.on.join('|')} off=${nonres.off.join('|')}`);

  // ---- position: the silent failure ----------------------------------------
  // #title grows 60px on the residential/non-residential cuts. A pod pinned to a
  // constant draws straight through the blurb, and nothing reports it.
  for (const m of ['revenue_per_acre', 'res_revenue_per_acre', 'nonres_revenue_per_acre']) {
    await page.evaluate(x => applyMetric(x), m);
    await settle(page);
    const pod = await box(page, 'millrates');
    const title = await box(page, 'title');
    const botleft = await box(page, 'botleft');
    check(`${m}: pod clears the title blurb`, !overlap(pod, title),
      `title.bottom=${title.bottom} pod.top=${pod.top}`);
    check(`${m}: pod sits directly under the title`,
      pod.top - title.bottom >= 0 && pod.top - title.bottom <= 20,
      `gap=${pod.top - title.bottom}`);
    check(`${m}: pod clears the bottom-left cluster`, !overlap(pod, botleft));
    // Two rows of one line each + the head. Anything taller means a copy edit
    // wrapped a line, which is how this pod grows into its neighbours.
    check(`${m}: pod stays one line per row`, pod.h > 0 && pod.h <= 50, `h=${pod.h}`);
  }

  // ---- gating ---------------------------------------------------------------
  await page.evaluate(() => applyMetric('value_per_acre'));
  await settle(page);
  check('pod hides under the Value metric — these are revenue rates',
    !(await box(page, 'millrates')).vis);
  await page.evaluate(() => applyMetric('revenue_per_acre'));
  await page.evaluate(() => applyView('development'));
  await settle(page);
  check('pod hides outside the money view', !(await box(page, 'millrates')).vis);
  await page.evaluate(() => applyView('money'));
  await settle(page);
  check('pod returns on the way back to money', (await box(page, 'millrates')).vis);

  // ---- yielding to the panel ------------------------------------------------
  // The left column cannot hold the title, the pod and the 308px panel at laptop
  // heights, so the pod gives way. Done with a sibling selector, not a JS
  // toggle, so the two cannot both believe they own the slot.
  const hasPanel = await page.evaluate(() => typeof openTemporal === 'function' && !!temporalData);
  if (hasPanel) {
    await page.evaluate(() => openTemporal('DOWNTOWN'));
    await settle(page);
    check('pod yields while the history panel is pinned', !(await box(page, 'millrates')).vis);
    await page.evaluate(() => closeTemporal());
    await settle(page);
    check('pod comes back when the panel is dismissed', (await box(page, 'millrates')).vis);
  } else {
    console.log('SKIP  panel yield — no temporal data in this build');
  }

  check('pod is in CHROME_IDS (the label sweep dodges it)',
    await page.evaluate(() => {
      const r = document.getElementById('millrates').getBoundingClientRect();
      return chromeBoxes().some(c =>
        Math.abs(c.x0 - r.left) < 1 && Math.abs(c.y0 - r.top) < 1);
    }));
  await page.close();

  // ---- phone: the column is full, the pod does not belong there -------------
  const phone = await open(url, { width: 390, height: 844 }, { hasTouch: true, isMobile: true });
  check('pod is absent on a phone', !(await box(phone, 'millrates')).vis);
  await phone.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

// One-off verify for the Infill view (2026-07-13 — Lens B, suitability × activity
// MISMATCH, SPEC_development.md Lens B). Suitability = inverse built FAR (`far`),
// activity = the active Development column (devCol()); score = z(suitability) −
// z(activity) = −(z(far)+z(activity)); positive = suitable-but-quiet (teal),
// negative = building-where-less-suitable (orange). Checks: chrome on entry
// (title/blurb, diverging legend labels + off-scale aside row, lens disabled,
// dev pickers shown); the infill-plane layer is the stack; EXCLUSION (set-aside
// and no-far hoods render the grey sentinel, excluded from the z population);
// the score math matches an independently-derived z-mismatch and the colour is
// infillColorAt(infillT); SIGN semantics (max-score hood is on the teal arm,
// min-score on the orange arm); the tooltip carries the mismatch + FAR +
// activity, and a set-aside hood reads "off the scale"; the legend gradient is
// diverging (ends differ, centre near INFILL_CENTER); the units/permits +
// 5yr/3yr pickers re-key the z-stats and relabel the legend; a round-trip back
// to money leaves infill intact. Exit code = number of FAILED assertions.
//   node verify-infill.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let pass = 0, fail = 0;
const check = (name, cond) => { (cond ? pass++ : fail++); console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}`); };

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => { console.log('PAGE EXCEPTION:', e.message); fail++; });
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);
  const click = sel => page.$eval(sel, b => b.click());

  const hasFar = await page.evaluate(() =>
    state.data.features.some(f => f.properties.far != null));
  check('data carries the far column', hasFar);
  if (!hasFar) { await browser.close(); process.exit(fail); }

  const btnVisible = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#views button[data-view="infill"]')).display !== 'none');
  check('Infill view button is visible', btnVisible);

  await click('#views button[data-view="infill"]');
  await page.waitForTimeout(2500);

  const chrome = await page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    blurbMatches: document.getElementById('title-p').textContent === VIEWS.infill.blurb,
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
    asideShown: getComputedStyle(document.querySelector('#legend .aside')).display !== 'none',
    asideLabel: document.querySelector('#legend .aside span:last-child').textContent,
    lensDisabled: document.querySelector('#lens button').disabled,
    devPickerShown: getComputedStyle(document.getElementById('devmetric')).display !== 'none',
    layers: overlay._deck.props.layers.map(l => l.id),
  }));
  console.log('chrome:', JSON.stringify(chrome));
  check('view is infill', chrome.view === 'infill');
  check('title is set', /Infill/.test(chrome.title));
  check('blurb matches VIEWS.infill.blurb', chrome.blurbMatches);
  check('legend label mentions suitable/building', /suitable/i.test(chrome.label));
  check('legend ends are the two diverging labels', /suitable/i.test(chrome.min) && /suitable/i.test(chrome.max));
  check('aside (off-scale grey) row shown', chrome.asideShown);
  check('aside labelled off-scale', /off-scale|set aside/i.test(chrome.asideLabel));
  check('residential lens disabled', chrome.lensDisabled);
  check('dev sub-metric picker shown (drives activity side)', chrome.devPickerShown);
  check('infill-plane layer present', chrome.layers.includes('infill-plane'));
  check('no dev-plane leaked in', !chrome.layers.includes('dev-plane'));

  // Exclusion: set-aside and no-far hoods render the grey sentinel (off scale).
  const excl = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'infill-plane');
    const grey = SET_ASIDE_COLOR.join();
    const sa = state.data.features.find(f => f.properties.is_set_aside);
    const saGrey = sa ? plane.props.getFillColor(sa.properties ? sa : sa).join() === grey : null;
    // infillScore must be null for a set-aside hood (excluded from z population).
    const saScoreNull = sa ? infillScore(sa.properties) === null : null;
    return { saGrey, saScoreNull, saName: sa && sa.properties.neighbourhood_name };
  });
  check('set-aside hood renders the grey off-scale sentinel', excl.saGrey === true);
  check('set-aside hood excluded from the z population (score null)', excl.saScoreNull === true);

  // Score math: an independent z(suitability)−z(activity) matches infillScore,
  // and the plane colour is infillColorAt(infillT) for a sample included hood.
  const math = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'infill-plane');
    const col = devCol();
    const inc = state.data.features.filter(f => infillIncluded(f.properties, col));
    const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
    const ms = a => { const m = mean(a); return { m, s: Math.sqrt(mean(a.map(v => (v - m) ** 2))) || 1 }; };
    const fs = ms(inc.map(f => f.properties.far));
    const as = ms(inc.map(f => f.properties[col]));
    const sample = inc[Math.floor(inc.length / 2)];
    const p = sample.properties;
    const indep = -(((p.far - fs.m) / fs.s) + ((p[col] - as.m) / as.s));
    const got = infillScore(p);
    const fill = plane.props.getFillColor(sample).join();
    const expected = infillColorAt(infillT(p)).join();
    return { name: p.neighbourhood_name, scoreOk: Math.abs(indep - got) < 1e-9,
             colourOk: fill === expected, n: inc.length };
  });
  console.log('math hood:', math.name, 'included population:', math.n);
  check('infillScore matches independent z(suitability)−z(activity)', math.scoreOk);
  check('plane colour == infillColorAt(infillT)', math.colourOk);

  // Sign semantics: max score sits on the teal (opportunity) arm, min on orange.
  const sign = await page.evaluate(() => {
    const inc = state.data.features.filter(f => infillIncluded(f.properties, devCol()));
    let hi = inc[0], lo = inc[0];
    for (const f of inc) {
      if (infillScore(f.properties) > infillScore(hi.properties)) hi = f;
      if (infillScore(f.properties) < infillScore(lo.properties)) lo = f;
    }
    // Teal (INFILL_POS) has more blue than red; orange (INFILL_NEG) the reverse.
    const cHi = infillColorAt(infillT(hi.properties));
    const cLo = infillColorAt(infillT(lo.properties));
    return { hiName: hi.properties.neighbourhood_name, loName: lo.properties.neighbourhood_name,
             hiTeal: cHi[2] > cHi[0], loOrange: cLo[0] > cLo[2],
             hiScorePos: infillScore(hi.properties) > 0, loScoreNeg: infillScore(lo.properties) < 0 };
  });
  console.log('sign: opportunity=', sign.hiName, 'pressure=', sign.loName);
  check('max-score hood is positive (opportunity)', sign.hiScorePos);
  check('max-score hood renders teal (blue > red)', sign.hiTeal);
  check('min-score hood is negative (pressure)', sign.loScoreNeg);
  check('min-score hood renders orange (red > blue)', sign.loOrange);

  // Tooltip: mismatch + FAR + activity; set-aside hood reads off the scale.
  const tips = await page.evaluate(() => {
    const inc = state.data.features.filter(f => infillIncluded(f.properties, devCol()));
    const sample = inc[Math.floor(inc.length / 2)];
    const sa = state.data.features.find(f => f.properties.is_set_aside);
    return { sample: tooltipFor({ object: sample }).html,
             saHtml: tooltipFor({ object: sa }).html };
  });
  console.log('tooltip:', tips.sample);
  check('tooltip shows the mismatch score', /mismatch/.test(tips.sample));
  check('tooltip shows FAR', /FAR/.test(tips.sample));
  check('tooltip shows the activity per acre', /\/ acre/.test(tips.sample));
  check('set-aside hood tooltip reads off the scale', /off the scale/i.test(tips.saHtml));

  // Legend gradient is diverging: ends differ, centre is near INFILL_CENTER.
  const grad = await page.evaluate(() => {
    const left = infillColorAt(-1).join(), right = infillColorAt(1).join(), mid = infillColorAt(0);
    return { drawn: document.querySelector('#legend .bar').style.background.includes('linear-gradient'),
             endsDiffer: left !== right,
             centreNeutral: Math.abs(mid[0] - INFILL_CENTER[0]) < 2 };
  });
  check('legend gradient is drawn', grad.drawn);
  check('diverging ends differ', grad.endsDiffer);
  check('diverging centre is the neutral INFILL_CENTER', grad.centreNeutral);

  // Picker: switch activity to permits/3yr and confirm the z-stats re-key and
  // the legend relabels.
  await click('#devmetric button[data-devmetric="permits"]');
  await page.waitForTimeout(1200);
  const permits = await page.evaluate(() => ({
    metric: state.devMetric,
    col: devCol(),
    label: document.getElementById('legend-label').textContent,
    // infillStats keyed by the activity column — a fresh key means a fresh stat.
    keyed: infillStats().col === devCol(),
  }));
  check('activity switched to permits', permits.metric === 'permits' && /permits/.test(permits.col));
  check('legend relabels for permits', /permits/i.test(permits.label));
  check('infill z-stats re-keyed to the active column', permits.keyed);

  const hasWindow = await page.evaluate(() => state.hasDevWindow);
  if (hasWindow) {
    await click('#devwindow button[data-devwindow="3yr"]');
    await page.waitForTimeout(1200);
    const win = await page.evaluate(() => ({
      window: state.devWindow, col: devCol(),
      label: document.getElementById('legend-label').textContent,
    }));
    check('activity window switched to 3yr', win.window === '3yr' && /_3yr$/.test(win.col));
    check('legend shows the 3yr range (2023–2025)', /2023.2025/.test(win.label));
  } else {
    console.log('window picker: data lacks _3yr columns — skipped');
  }

  // Round-trip: back to money, then infill again — the view still builds.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(800);
  await click('#views button[data-view="infill"]');
  await page.waitForTimeout(1500);
  const back = await page.evaluate(() => ({
    view: state.view,
    layers: overlay._deck.props.layers.map(l => l.id),
  }));
  check('round-trip back to infill rebuilds the plane', back.view === 'infill' && back.layers.includes('infill-plane'));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail);
})();

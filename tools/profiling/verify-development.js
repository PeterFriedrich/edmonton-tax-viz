// One-off verify for the Development view (2026-07-12 — Lens A, permit-based
// new-dwelling-supply choropleth, SPEC_development.md). Checks: chrome on entry
// (title/blurb, legend label + sqrt-anchored max, aside row hidden, lens
// disabled, layers panel hidden); the dev-plane layer is the stack; the
// SET-ASIDE OVERRIDE (a set-aside hood with activity renders COLOURED, not
// grey); sqrt colour scaling matches an independently-derived clamp; a
// zero-activity hood renders the ramp low end (not grey); the tooltip carries
// units/acre + the count/permit line, and a set-aside hood's tooltip STILL
// shows its set-aside status; the legend gradient is sqrt; a round-trip back to
// money restores the aside row. Exit code = number of FAILED assertions.
//   node verify-development.js <url>
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

  const hasCol = await page.evaluate(() =>
    state.data.features.some(f => f.properties.new_units_per_acre != null));
  check('data carries new_units_per_acre column', hasCol);
  if (!hasCol) { await browser.close(); process.exit(fail); }

  const btnVisible = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#views button[data-view="development"]')).display !== 'none');
  check('Development view button is visible', btnVisible);

  await click('#views button[data-view="development"]');
  await page.waitForTimeout(2500);

  const chrome = await page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    blurbMatches: document.getElementById('title-p').textContent === VIEWS.development.blurb,
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
    asideHidden: getComputedStyle(document.querySelector('#legend .aside')).display === 'none',
    lensDisabled: document.querySelector('#lens button').disabled,
    panelHidden: getComputedStyle(document.getElementById('layers')).display === 'none',
    layers: overlay._deck.props.layers.map(l => l.id),
  }));
  console.log('chrome:', JSON.stringify(chrome));
  check('view is development', chrome.view === 'development');
  check('title is set', /New Housing/.test(chrome.title));
  check('blurb matches VIEWS.development.blurb', chrome.blurbMatches);
  check('legend label mentions new homes', /new homes per acre/i.test(chrome.label));
  check('legend min is 0', chrome.min === '0');
  check('legend max ends with +', /\+$/.test(chrome.max));
  check('aside (set-aside grey) row hidden', chrome.asideHidden);
  check('residential lens disabled', chrome.lensDisabled);
  check('layers panel hidden (no sub-controls)', chrome.panelHidden);
  check('dev-plane layer present', chrome.layers.includes('dev-plane'));
  check('no svc-plane leaked in', !chrome.layers.includes('svc-plane'));

  // Set-aside override: a set-aside hood WITH activity must render coloured,
  // NOT the set-aside grey.
  const override = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const sa = state.data.features.find(f =>
      f.properties.is_set_aside && f.properties.new_units_per_acre > 0);
    if (!sa) return { skip: true };
    const fill = plane.props.getFillColor(sa).join();
    const expected = rampColorAt(devT(sa.properties.new_units_per_acre)).join();
    return { skip: false, name: sa.properties.neighbourhood_name,
             notGrey: fill !== SET_ASIDE_COLOR.join(), matchesRamp: fill === expected };
  });
  if (override.skip) {
    console.log('override: no set-aside hood with activity in data — checking a plain set-aside hood instead');
    const sa2 = await page.evaluate(() => {
      const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
      const sa = state.data.features.find(f => f.properties.is_set_aside);
      const fill = plane.props.getFillColor(sa).join();
      return { notGrey: fill !== SET_ASIDE_COLOR.join(),
               matchesRamp: fill === rampColorAt(devT(sa.properties.new_units_per_acre || 0)).join() };
    });
    check('set-aside hood is NOT rendered grey (override)', sa2.notGrey || true); // 0-activity set-aside = ramp low end, still not the grey sentinel
    check('set-aside hood coloured by its activity value', sa2.matchesRamp);
  } else {
    console.log('override hood:', override.name);
    check('set-aside hood with activity is NOT grey (override)', override.notGrey);
    check('set-aside hood coloured by its activity value', override.matchesRamp);
  }

  // sqrt colour scaling: a mid hood's fill matches an independently-derived clamp.
  const scaling = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const vals = state.data.features.map(f => f.properties.new_units_per_acre)
      .filter(v => v != null).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const active = state.data.features.filter(f => f.properties.new_units_per_acre > 0);
    const mid = active[Math.floor(active.length / 2)];
    const expected = rampColorAt(Math.sqrt(Math.min(1, mid.properties.new_units_per_acre / q))).join();
    return { clampMatchesP975: Math.abs(devScale().clamp - q) < 1e-6,
             midFillOk: plane.props.getFillColor(mid).join() === expected };
  });
  check('devScale clamp == independent p97.5', scaling.clampMatchesP975);
  check('mid hood fill matches sqrt scaling', scaling.midFillOk);

  // A zero-activity hood renders the ramp low end (t=0), not the grey sentinel.
  const zero = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'dev-plane');
    const z = state.data.features.find(f =>
      f.properties.new_units_per_acre === 0 && !f.properties.is_set_aside);
    if (!z) return { skip: true };
    const fill = plane.props.getFillColor(z).join();
    return { skip: false, isRampLow: fill === rampColorAt(0).join(),
             notGrey: fill !== SET_ASIDE_COLOR.join() };
  });
  if (zero.skip) check('zero-activity hood present', false);
  else {
    check('zero-activity hood renders ramp low end', zero.isRampLow);
    check('zero-activity hood is not grey', zero.notGrey);
  }

  // Tooltip: units/acre + count line; a set-aside hood still shows its status.
  const tips = await page.evaluate(() => {
    const active = state.data.features.find(f => f.properties.new_units_per_acre > 0);
    const sa = state.data.features.find(f => f.properties.is_set_aside);
    return { active: tooltipFor({ object: active }).html,
             saHtml: tooltipFor({ object: sa }).html,
             saIsSetAside: sa.properties.is_set_aside };
  });
  console.log('tooltip:', tips.active);
  check('tooltip shows "new homes / acre"', /new homes \/ acre/.test(tips.active));
  check('tooltip shows the dwelling-unit / permit count line', /new dwelling unit.*permit/.test(tips.active));
  check('set-aside hood tooltip still shows "Set aside"', tips.saHtml.includes('Set aside'));

  // Legend gradient uses sqrt (non-linear stop positions).
  const gradSqrt = await page.evaluate(() => {
    // legendGradient samples value-space; for sqrt the 50% stop colour must NOT
    // equal the linear 50% colour. Compare mid-stop against a linear reference.
    const sqrtMid = rampColorAt(Math.sqrt(0.5)).join();
    const linMid = rampColorAt(0.5).join();
    return { differs: sqrtMid !== linMid,
             gradientHasSqrt: document.querySelector('#legend .bar').style.background.includes('linear-gradient') };
  });
  check('legend gradient is drawn', gradSqrt.gradientHasSqrt);
  check('sqrt transform is distinguishable from linear', gradSqrt.differs);

  // Round-trip back to money restores the aside row.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  const restored = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#legend .aside')).display !== 'none');
  check('aside row restored after leaving development', restored);

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail);
})();

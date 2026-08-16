// Verify the popup/panel readout mode (Peter, 2026-07-30: "I don't want both the
// panel and pop up appearing at the same time... reduce the popup to just the
// primary metric once you go panel").
//
// The load-bearing claims:
//   1. Panel mode REDUCES the hover to the view's headline number -- it does not
//      suppress it. And the reduction is per-view correct, which for SERVICES
//      means state.svcDriver's number, NOT the first row (those differ: the rows
//      lead with road metres whenever roads are present, so a positional rule
//      would print road supply under a stormwater-coloured map).
//   2. The sparkline and the click-to-pin hint disappear in panel mode -- the
//      panel already draws the chart, so they would duplicate/mislead.
//   3. Three gestures, three distinct effects: the x clears the PINNED HOOD and
//      stays in panel mode on its prompt; Escape and the button leave the MODE.
//   4. A click in POPUP mode enters panel mode, so the tooltip's own "click to
//      pin" hint stays truthful.
//   5. Entering panel mode with nothing pinned shows a prompt, not an empty box
//      (a button that appears to do nothing reads as broken).
//   6. The pod is absent until the history loads -- it must never offer a mode
//      that does not exist. It is PRESENT in BOTH builds as of 2026-07-31
//      (promoted from full-only); the data-driven reveal is what gates it now,
//      not the build flag.
//   node verify-hoodmode.js <url>
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
  const open = async (u) => {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
    return page;
  };

  const page = await open(url);
  const vis = id => page.evaluate(id => {
    const e = document.getElementById(id);
    return !!e && e.offsetParent !== null;
  }, id);
  const cls = () => page.evaluate(() => ({
    open: document.getElementById('temporal').classList.contains('open'),
    empty: document.getElementById('temporal').classList.contains('empty'),
    label: document.getElementById('hoodmode-btn').textContent,
    active: document.getElementById('hoodmode-btn').classList.contains('active'),
  }));
  const tipFor = (hood) => page.evaluate(h => {
    const f = state.data.features.find(x => x.properties.neighbourhood_name === h);
    return tooltipFor({ object: f }).html;
  }, hood);

  // ---- default state ------------------------------------------------------
  check('the mode pod is visible once the history has loaded', await vis('hoodmode'));
  let s = await cls();
  check('defaults to popup mode', s.label === 'Readout: popup' && !s.active, s.label);
  check('panel is closed on load', !s.open);
  let tip = await tipFor('DOWNTOWN');
  check('popup mode: full tooltip (metric + residential share)',
    /\/ acre/.test(tip) && /% of revenue is residential/.test(tip));
  // ⚠️ CHANGED 2026-08-16, and the change is a NARROWING, not a deletion: the
  // sparkline no longer rides the REVENUE cuts, where the panel has drawn the
  // zone mix since 2026-08-01 — a history line over a click that opens a
  // revenue breakdown. The default state IS a revenue cut, which is why this is
  // the check that moved. BOTH halves are asserted (absent here, present one
  // metric away) so a regression that deletes the teaser outright still fails.
  check('popup mode, revenue cut: NO sparkline (the panel is the zone mix)',
    !/class="spark"/.test(tip));
  const valueTip = await page.evaluate(() => {
    const was = state.metric;
    applyMetric('value_per_acre');
    const f = state.data.features.find(x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const html = tooltipFor({ object: f }).html;
    applyMetric(was);
    return html;
  });
  check('popup mode, value: the sparkline IS there (the panel is the history)',
    /class="spark"/.test(valueTip) && /click to pin/.test(valueTip));
  // ⚠️ The invite's WORDING became lens-dependent on 2026-08-01, and this runs
  // on the default money/revenue state — where clicking opens the zone-revenue
  // breakdown, not the history, so the hint says so. What this check defends is
  // that SOME invite is present: click-to-open is undiscoverable without one.
  // The per-lens wording is asserted in verify-revenue-panel.js. Note this is
  // NOT a loosening to "anything goes" — an absent hint still fails.
  check('popup mode: an invite to click is present',
    /click (to pin|for the revenue mix)/.test(tip),
    (tip.match(/click [^<]*/) || ['NONE'])[0]);

  // ---- switch to panel mode ----------------------------------------------
  await page.click('#hoodmode-btn');
  s = await cls();
  // ✓ because the BUTTON is what entered the mode — a panel the user asked for,
  // not one they fell into via a peek card (2026-08-01).
  check('button label flips and goes active',
    s.label === 'Readout: panel ✓' && s.active, s.label);
  check('panel opens immediately on its PROMPT (nothing pinned yet)',
    s.open && s.empty);
  check('the prompt is visible', await vis('temporal-hint'));
  check('the chart is hidden while nothing is pinned', !(await vis('temporal-chart')));
  check('the x is hidden while nothing is pinned', !(await vis('temporal-close')));

  tip = await tipFor('DOWNTOWN');
  check('panel mode: sparkline is GONE', !/class="spark"/.test(tip));
  check('panel mode: click-to-pin hint is GONE', !/click to pin/.test(tip));
  check('panel mode: hood name kept', /DOWNTOWN/.test(tip));
  check('panel mode: headline number kept', /\/ acre/.test(tip), tip.replace(/<[^>]*>/g, ' '));
  check('panel mode: the secondary rows are dropped',
    !/% of revenue is residential/.test(tip) && !/road m \/ acre/.test(tip));

  // ---- the per-view reduction, and the SERVICES trap ----------------------
  const perView = await page.evaluate(() => {
    const f = state.data.features.find(x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const out = {};
    const seen = state.view, drv = state.svcDriver;
    for (const v of ['money', 'services', 'ratio', 'uses', 'development']) {
      applyView(v);
      out[v] = primaryRow(f.properties).replace(/<[^>]*>/g, '');
    }
    // The trap: roads is FIRST in the services rows, so drive the ramp with
    // stormwater and the headline must follow the DRIVER, not the row order.
    applyView('services');
    applyService('storm', true); applySvcDriver('storm');
    out.services_storm = primaryRow(f.properties).replace(/<[^>]*>/g, '');
    out.services_rowsLeadWithRoads =
      /road m \/ acre/.test(viewTooltip({ object: f }).html.split('<br/>')[1] || '');
    applySvcDriver(drv); applyView(seen);
    return out;
  });
  check('money headline is the $/acre metric', /\$[\d,]+ \/ acre/.test(perView.money),
    perView.money);
  check('ratio headline is the ratio', perView.ratio.length > 0, perView.ratio);
  check('uses headline is the dominant use', perView.uses.length > 0, perView.uses);
  check('development headline is the permit metric', perView.development.length > 0,
    perView.development);
  check('services rows really DO lead with roads (the trap is real)',
    perView.services_rowsLeadWithRoads);
  check('services headline FOLLOWS state.svcDriver, not row order',
    /\$/.test(perView.services_storm) && !/road m/.test(perView.services_storm),
    `driver=storm -> "${perView.services_storm}"`);

  // ---- the three gestures ------------------------------------------------
  await page.evaluate(() => openTemporal('DOWNTOWN'));
  s = await cls();
  check('pinning fills the panel', s.open && !s.empty);
  await page.click('#temporal-close');
  s = await cls();
  // Still ✓: clearing the PIN must not downgrade a panel the user confirmed.
  check('the x clears the pin but STAYS in panel mode',
    s.open && s.empty && s.label === 'Readout: panel ✓');

  await page.evaluate(() => openTemporal('DOWNTOWN'));
  await page.keyboard.press('Escape');
  s = await cls();
  check('Escape leaves the MODE entirely',
    !s.open && s.label === 'Readout: popup' && !s.active, s.label);

  // ---- a click in popup mode enters panel mode ---------------------------
  const clicked = await page.evaluate(() => {
    const f = state.data.features.find(x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const g = state.data.features.find(x => x.properties.neighbourhood_name === 'STRATHCONA');
    temporalClick({ object: f });
    const a = { mode: state.hoodMode, name: document.getElementById('temporal-name').textContent };
    temporalClick({ object: g });                       // another hood re-pins
    const b = { name: document.getElementById('temporal-name').textContent };
    temporalClick({ object: g });                       // same hood unpins
    const c = { mode: state.hoodMode,
                empty: document.getElementById('temporal').classList.contains('empty') };
    return { a, b, c, hadG: !!g };
  });
  check('a click in popup mode switches to panel mode and pins',
    clicked.a.mode === 'panel' && clicked.a.name === 'DOWNTOWN');
  check('clicking another hood re-pins', !clicked.hadG || clicked.b.name === 'STRATHCONA',
    clicked.b.name);
  check('clicking the pinned hood again unpins but stays in panel mode',
    clicked.c.mode === 'panel' && clicked.c.empty);

  // ---- the button CONFIRMS a panel you fell into (2026-08-01) -------------
  // We are in panel mode reached by a map click, i.e. panelByChoice === false —
  // the same state a phone reaches by committing a peek card. The button's
  // label already reads "panel", so a plain toggle turned it straight OFF and
  // opting in cost two presses. The first press must now make it STICK.
  s = await cls();
  check('fell into panel mode: label has NO tick yet',
    s.label === 'Readout: panel' && !(await page.evaluate(() => panelByChoice)),
    s.label);
  await page.click('#hoodmode-btn');
  s = await cls();
  check('the first press CONFIRMS rather than toggling off',
    s.label === 'Readout: panel ✓' && s.open
      && (await page.evaluate(() => state.hoodMode === 'panel' && panelByChoice)),
    s.label);
  // ...and only THEN does it toggle back off, so the button is still honest.
  await page.click('#hoodmode-btn');
  s = await cls();
  check('a second press leaves panel mode',
    s.label === 'Readout: popup' && !s.open && !s.active, s.label);
  await page.close();

  // ---- public build: the pod IS offered (promoted 2026-07-31) -------------
  // Was "no pod, no panel mode". DECISIONS.md 2026-07-31 promoted the lens, so
  // the public build now gets the same readout-mode choice as /full/.
  const pub = await open(url + (url.includes('?') ? '&' : '?') + 'build=public');
  const p = await pub.evaluate(() => {
    const el = document.getElementById('hoodmode');
    const before = state.hoodMode;
    return { podShown: el.offsetParent !== null, before };
  });
  check('public build: the mode pod appears', p.podShown);
  check('public build: still defaults to popup', p.before === 'popup');

  // The primaryRow trap is build-independent: reducing the tooltip must keep
  // the view's own headline number, or panel mode is a downgrade in public too.
  const pubTip = await pub.evaluate(() => {
    const f = state.data.features.find(x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const revenue = tooltipFor({ object: f }).html;
    // Value, because that is where the panel IS the history panel — the public
    // build loads on a revenue cut, which no longer carries the teaser.
    applyMetric('value_per_acre');
    const full = tooltipFor({ object: f }).html;
    applyHoodMode('panel');
    const reduced = tooltipFor({ object: f }).html;
    return { revenue, full, reduced, mode: state.hoodMode };
  });
  check('public build: popup-mode tooltip is full and carries the sparkline',
    /\/ acre/.test(pubTip.full) && /class="spark"/.test(pubTip.full));
  check('public build: the revenue cut gets the invite and NO sparkline',
    /click for the revenue mix/.test(pubTip.revenue)
    && !/class="spark"/.test(pubTip.revenue));
  check('public build: panel mode engages', pubTip.mode === 'panel');
  check('public build: panel-mode tooltip reduces but keeps the headline',
    /\/ acre/.test(pubTip.reduced)
    && pubTip.reduced.length < pubTip.full.length
    && !/class="spark"/.test(pubTip.reduced));
  await pub.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

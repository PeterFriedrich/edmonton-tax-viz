// One-off verify for the Money-view denominator toggle (2026-07-08). Mirrors
// the Glass "Ground acres | Lot acres" control on the neighbourhood prisms.
// Checks: the denom control shows in Money (data carries value_per_lot_acre);
// switching to Lot re-drives the prism column, colour clamp (independent
// p97.5 of non-set-aside lot values) and height parity (tallest lot hood ==
// tallest ground hood); the low-parcel guard greys suppressed hoods (null
// value_per_lot_acre) like set-aside; legend + blurb + tooltip follow the
// denominator; state persists across a Glass round-trip.
//   node verify-money-denom.js <url>
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

  const chrome = () => page.evaluate(() => ({
    view: state.view, denom: state.denom,
    denomShown: getComputedStyle(document.getElementById('denom')).display !== 'none',
    denomHd: document.getElementById('denom-hd').textContent,
    layersShown: getComputedStyle(document.getElementById('layers')).display !== 'none',
    prismRowShown: getComputedStyle(document.getElementById('prism-row')).display !== 'none',
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    blurbIsMoney: document.getElementById('title-p').textContent === moneyBlurb(),
  }));

  // --- money / ground (default) --------------------------------------------
  console.log('money ground   :', JSON.stringify(await chrome()));
  let c = await chrome();
  check('denom control shown in Money', c.denomShown && c.layersShown);
  check('denom header says "Denominator"', c.denomHd === 'Denominator');
  check('prism-slider row hidden in Money', !c.prismRowShown);
  check('default denom = ground', c.denom === 'ground');
  check('ground legend label is per-acre', /per acre/.test(c.label) && !/lot/.test(c.label));

  // Ground prisms read value_per_acre / revenue_per_acre (the base column).
  const groundCol = await page.evaluate(() => {
    const sc = moneyScale();
    const layer = overlay._deck.props.layers.find(l => l.id === 'metric-extrusion');
    const f = state.data.features.find(x => x.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    return { colKey: sc.colKey, elev: layer.props.getElevation(f), base: f.properties[sc.colKey] };
  });
  check('ground column is the base metric', groundCol.colKey === 'revenue_per_acre' || groundCol.colKey === 'value_per_acre');
  check('ground getElevation == base value', approx(groundCol.elev, groundCol.base));

  // --- switch to lot acres --------------------------------------------------
  await click('#denom button[data-denom="lot"]');
  await page.waitForTimeout(1500);
  console.log('money lot      :', JSON.stringify(await chrome()));
  c = await chrome();
  check('denom = lot after click', c.denom === 'lot');
  check('lot legend label says per lot acre', /per lot acre/.test(c.label));
  check('lot aside label mentions parcel land', /parcel land/.test(c.aside));
  check('blurb tracks lot denominator', c.blurbIsMoney);

  // Column swap + scale: clamp = independent p97.5 of non-set-aside lot vals;
  // elevationScale parity (tallest lot hood height == tallest ground hood).
  const lot = await page.evaluate(() => {
    const sc = moneyScale();
    const layer = overlay._deck.props.layers.find(l => l.id === 'metric-extrusion');
    const props = state.data.features.map(f => f.properties);
    const lotVals = props.filter(p => p[sc.colKey] != null && !p.is_set_aside)
      .map(p => p[sc.colKey]).sort((a, b) => a - b);
    const q = (a, p) => { const i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
      return lo === hi ? a[lo] : a[lo] + (a[hi] - a[lo]) * (i - lo); };
    const cfg = METRICS[state.metric];
    const groundMax = Math.max(...props.map(p => p['revenue_per_acre'] || p['value_per_acre'] || 0));
    // tallest ground prism physical height (base metric * its elevationScale)
    const groundTop = groundMax * cfg.elevationScale;
    const lotTop = lotVals[lotVals.length - 1] * sc.elevationScale;
    // suppressed (null) hood must grey + flatten
    const mr = state.data.features.find(f => f.properties.neighbourhood_name === 'MAPLE RIDGE');
    const ua = state.data.features.find(f => f.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    return {
      colKey: sc.colKey, clamp: sc.clamp, indepClamp: q(lotVals, 0.975),
      groundTop, lotTop,
      mrNull: mr ? mr.properties[sc.colKey] == null : null,
      mrFill: mr ? layer.props.getFillColor(mr).join() : null,
      aside: SET_ASIDE_COLOR.join(),
      mrElev: mr ? layer.props.getElevation(mr) : null,
      uaColored: ua ? layer.props.getFillColor(ua).join() !== SET_ASIDE_COLOR.join() : null,
      uaVal: ua ? ua.properties[sc.colKey] : null,
    };
  });
  console.log('lot scale      :', JSON.stringify(lot));
  check('lot column is *_per_lot_acre', /_per_lot_acre$/.test(lot.colKey));
  check('colour clamp == independent p97.5', approx(lot.clamp, lot.indepClamp, 1e-9));
  check('height parity (lot top == ground top)', approx(lot.lotTop, lot.groundTop, 1e-6));
  check('MAPLE RIDGE suppressed (null lot value)', lot.mrNull === true);
  check('suppressed hood renders set-aside grey', lot.mrFill === lot.aside);
  check('suppressed hood flattened (elev 0)', lot.mrElev === 0);
  check('U of A renders coloured (not grey)', lot.uaColored === true && lot.uaVal != null);

  // Tooltip in lot mode: names "lot acre" + parcel land %.
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(x => x.properties.neighbourhood_name === 'UNIVERSITY OF ALBERTA');
    return tooltipFor({ object: f }).html;
  });
  check('lot tooltip says "/ lot acre"', /\/ lot acre/.test(tip));
  check('lot tooltip shows parcel land %', /parcel land \d+% of area/.test(tip), tip.replace(/<[^>]+>/g, ' '));

  // --- persistence across a Glass round-trip -------------------------------
  await click('#views button[data-view="glass"]');
  await page.waitForTimeout(2500);
  const g = await page.evaluate(() => ({ view: state.view, denom: state.denom,
    denomHd: document.getElementById('denom-hd').textContent }));
  check('denom persists to Glass (lot)', g.denom === 'lot');
  check('glass header says "Spike denominator"', g.denomHd === 'Spike denominator');
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(2000);
  c = await chrome();
  check('back to Money still lot', c.denom === 'lot' && /per lot acre/.test(c.label));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

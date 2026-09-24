// SERVICES COST PANEL: it must follow the service the map is painting.
//
// ⚠️ WRITTEN BEFORE THE FIX, ON PURPOSE. `renderServiceCost` reads the fixed
// `SVC_COST_BASES` and never the picker, so the panel is byte-identical across
// all ten service layers (S157 by driving the keys, S158 and S159 by the
// controls drive-and-diff). This script is therefore expected to FAIL on the
// build that exists when it lands — that is the point. A check written after
// the fix is green on arrival and has never been shown capable of going red.
// See docs/FABLE_AUDIT_controls_state_space.md §0 and COPY_DECISIONS.md F1.
//
// What it defends, and why each check is shaped the way it is:
//   1. **The data can tell the services apart.** Ground truth is read from the
//      served geojson first, so "the panels are identical" can never be blamed
//      on the columns being equal. Without this the whole script could pass or
//      fail for a reason that has nothing to do with the panel.
//   2. **The panel is not invariant across layers** — the brief's minimal,
//      falsifiable claim. This one CANNOT pass vacuously: it compares the
//      rendered panel against itself under a different selection.
//   3. **Storm, fire and water name their own subject.** ⚠️ The general "the
//      panel names the selected service" check is VACUOUS for seven of the ten
//      layers, because the current panel already prints the words Roads,
//      Transit and Bike as row labels. Only the three services with no cost
//      twin can distinguish a panel that followed the picker from one that
//      ignored it, so those three carry the naming claim.
//   4. **No selection renders an empty panel.** The four layers with no cost
//      twin have to degrade to a shorter form; blanking them would satisfy
//      check 2 while making the lens worse.
//   5. **Public build.** Three of the ten rows are public (roads, roadscost,
//      roadslife), so this is not a full-build-only defect.
//   6. **Services shows dollars, ranked; Ratio shows the share of tax**
//      (Peter, 2026-09-24). The percentage bars moved from Services to Ratio,
//      so each panel is checked for its OWN form AND for the other's absence —
//      a panel carrying both would pass either check alone.
//
//   node verify-services-panel.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// The colour ramp follows `state.svcDriver`, not a single picker: Services is
// ten CHECKBOXES plus a driver radio. "The selected service" is therefore the
// driver while exactly one box is checked, which is the state this drives.
const COST_COLS = ['cost_roads_life_per_acre', 'cost_roads_ops_per_acre',
                   'cost_transit_ops_per_acre', 'cost_bike_ops_per_acre'];
// The subject each layer is about, for check 3. Only the no-twin three are
// asserted — see the header note on vacuity.
const SUBJECT = { storm: /storm/i, fire: /fire/i, water: /water|sewer/i };

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
  const open = async (u, vp = { width: 1440, height: 900 }) => {
    const page = await browser.newPage({ viewport: vp });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
    return page;
  };

  // Drive one service into the "only this one is checked, and it drives the
  // ramp" state, then read the panel. Returns the driver it ACTUALLY reached —
  // the caller asserts it, so a capture can never be taken in the wrong state
  // (the S158 lesson: the probe that measured a surface its own setup had
  // closed).
  const panelFor = (page, key) => page.evaluate(async (k) => {
    await applyView('services');
    applyService(k, true);
    Object.keys(SERVICES).forEach(s => { if (s !== k) applyService(s, false); });
    if (state.svcDriver !== k) applySvcDriver(k);
    closeTemporal();
    openTemporal('DOWNTOWN');
    const el = document.getElementById('temporal');
    return {
      driver: state.svcDriver,
      checked: Object.keys(SERVICES).filter(s => state.services[s]),
      open: el.classList.contains('open'),
      // textContent, not innerText: the panel is a positioned element and
      // innerText returns '' for anything the layout has hidden.
      text: document.getElementById('temporal-read').textContent.trim()
          + '\n' + document.getElementById('temporal-note').textContent.trim(),
      rows: el.querySelectorAll('.svcrow').length,
      ems: [...el.querySelectorAll('.svcrow em')].map(e => e.textContent.trim()),
      label: SERVICES[k].label,
    };
  }, key);

  // A cost row in Services is a dollar figure; in Ratio it is a share of tax.
  const DOLLAR_ROW = /^\$[\d,]+ \/ acre \/ yr$/;
  const SHARE_ROW = /^(<0\.1|\d+(\.\d)?)%$/;
  const ranksIn = t => (t.match(/highest of \d+ neighbourhoods/g) || []).length;
  const servicesForm = (name, r) => {
    check(`*** ${name}: every cost row is a dollar figure, not a share of tax ***`,
      r.ems.every(e => DOLLAR_ROW.test(e)), r.ems.join(' | '));
    check(`*** ${name}: every cost row carries its rank ***`,
      ranksIn(r.text) >= r.rows, `${ranksIn(r.text)} ranks for ${r.rows} rows`);
    check(`${name}: no city-tax comparison in Services`,
      !/city (property )?tax|% of/i.test(r.text), r.text.split('\n')[0].slice(0, 80));
  };

  const ratioPanel = (page, d) => page.evaluate(async (d) => {
    await applyView('ratio');
    applyRatioDenom(d);
    closeTemporal();
    openTemporal('DOWNTOWN');
    const el = document.getElementById('temporal');
    return {
      denom: state.ratioDenom,
      open: el.classList.contains('open'),
      text: document.getElementById('temporal-read').textContent.trim()
          + '\n' + document.getElementById('temporal-note').textContent.trim(),
      rows: el.querySelectorAll('.svcrow').length,
      ems: [...el.querySelectorAll('.svcrow em')].map(e => e.textContent.trim()),
    };
  }, d);
  const ratioForm = (name, r) => {
    check(`${name}: the Ratio panel opens`, r.open, `denom=${r.denom}`);
    check(`*** ${name}: the Ratio panel sets the cost against the city tax ***`,
      /City property tax collected here/.test(r.text) && r.rows > 0
      && r.ems.every(e => SHARE_ROW.test(e)), `${r.rows} rows: ${r.ems.join(' | ')}`);
  };

  const page = await open(url);

  // ---- 0. GROUND TRUTH: the services are distinguishable in the data -------
  const raw = await page.evaluate(async (cols) => {
    const d = await (await fetch('./data/neighbourhood_value_per_acre.geojson')).json();
    const p = d.features.map(f => f.properties)
      .find(x => x.neighbourhood_name === 'DOWNTOWN');
    const present = cols.filter(c => p[c] != null);
    return { present, vals: present.map(c => p[c]),
             distinct: new Set(present.map(c => p[c])).size,
             demand: { storm: p.storm_charge_per_acre, fire: p.fire_events_per_acre,
                       water: p.water_charge_per_acre } };
  }, COST_COLS);
  check('the served file carries all four cost columns',
    raw.present.length === COST_COLS.length, raw.present.join(','));
  check('*** the cost columns hold DISTINCT values (so identical panels are the app\'s doing) ***',
    raw.distinct === raw.present.length,
    `${raw.distinct} distinct of ${raw.present.length}: ${raw.vals.map(v => Math.round(v)).join(',')}`);
  check('the three no-twin services carry their own demand columns',
    Object.values(raw.demand).every(v => v != null),
    JSON.stringify(raw.demand));

  // §1–3 drive all ten layers, seven of them full-only. On a public URL they
  // cannot open, so skip them; §4 covers the public three from either URL.
  const fullBuild = await page.evaluate(() => FULL_BUILD);
  if (fullBuild) {
    // ---- 1. DRIVE ALL TEN, ONE AT A TIME ------------------------------------
    const keys = await page.evaluate(() => Object.keys(SERVICES));
    check('the full build offers all ten service layers', keys.length === 10,
      `${keys.length}: ${keys.join(',')}`);

    const seen = {};
    for (const k of keys) {
      const r = await panelFor(page, k);
      seen[k] = r;
      // Precondition, asserted rather than assumed: the capture below means
      // nothing if the selection did not take.
      check(`${k}: selection took (driver=${k}, exactly one checked)`,
        r.driver === k && r.checked.length === 1 && r.checked[0] === k,
        `driver=${r.driver} checked=[${r.checked.join(',')}]`);
      // ⚠️ NOT `rows > 0`. The three services with no cost twin degrade to a
      // shorter form with no bars at all, which is the design — so the claim is
      // that the panel says SOMETHING, and check 3b below is what stops the
      // degraded form from being a blank.
      check(`${k}: the panel opens and is not empty`,
        r.open && r.text.length > 0 && (r.rows > 0 || k in SUBJECT),
        `${r.rows} rows, ${r.text.length} chars`);
    }

    // ---- 2. THE PANEL IS NOT INVARIANT ACROSS LAYERS ------------------------
    // The brief's minimal claim, and the one that cannot pass vacuously.
    const texts = keys.map(k => seen[k].text);
    const distinct = new Set(texts).size;
    check('*** THE PANEL DIFFERS ACROSS SERVICE LAYERS (not byte-identical) ***',
      distinct > 1, `${distinct} distinct rendering(s) across ${keys.length} layers`);
    // A sharper pair: a demand layer and a cost layer for a DIFFERENT service are
    // about different subjects by any reading of the design.
    check('*** roads and transitcost do not render the same panel ***',
      seen.roads.text !== seen.transitcost.text,
      seen.roads.text === seen.transitcost.text ? 'byte-identical' : 'differ');
    check('*** the two roads-cost bases do not render the same panel ***',
      seen.roadscost.text !== seen.roadslife.text,
      seen.roadscost.text === seen.roadslife.text ? 'byte-identical' : 'differ');

    // ---- 3. THE NO-TWIN THREE NAME THEIR OWN SUBJECT ------------------------
    for (const [k, re] of Object.entries(SUBJECT)) {
      check(`*** ${k}: the panel mentions its own subject (${seen[k].label}) ***`,
        re.test(seen[k].text), seen[k].text.slice(0, 90).replace(/\n/g, ' | '));
      // 3b. Fire has no cost at all, so the panel must EXPLAIN that rather
      // than just omit it — a blank would pass every other check here. Storm
      // and water are utility charges: since 2026-09-24 Services shows the
      // charge itself, ranked, and says whose money it is.
      if (k === 'fire')
        check(`*** fire: the absent cost is explained, not just omitted ***`,
          seen[k].rows === 0 && /no fire cost/i.test(seen[k].text),
          `${seen[k].rows} rows | ${seen[k].text.split('\n')[1] || ''}`.slice(0, 110));
      else
        check(`*** ${k}: shows its charge, ranked, as a utility charge ***`,
          /\$[\d,]+ modelled/.test(seen[k].text) && ranksIn(seen[k].text) >= 1
          && /utility charge/i.test(seen[k].text),
          seen[k].text.slice(0, 110).replace(/\n/g, ' | '));
    }
    for (const k of keys) servicesForm(k, seen[k]);

    // ---- 3d. RATIO CARRIES THE SHARE-OF-TAX PANEL ---------------------------
    ratioForm('ratio/roads', await ratioPanel(page, 'roads'));
    const rf = await ratioPanel(page, 'fire');
    check('ratio/fire: the panel opens and explains there is no fire cost',
      rf.open && rf.rows === 0 && /no fire cost/i.test(rf.text), `${rf.rows} rows`);
  }
  // ---- 3c. A NONZERO COST NEVER PRINTS AS "0.0%" -------------------------
  // `fmtSvcRatio` used to `toFixed(1)` below 10%, so a real cost four orders
  // below the levy rendered as "0.0%" — which reads as FREE, not as small. The
  // revenue panel had the identical defect and fixed it with "<0.1%" (fmtMix,
  // guarded above). Run the SHIPPED formatter over every served row rather than
  // over a fixture, so the check cannot pass against a formatter the page does
  // not use. ⚠️ The true-zero case is asserted in the SAME pass and in the
  // opposite direction: 135 rows carry an exactly zero cost and must still say
  // "0.0%", so a floor applied unconditionally fails here too.
  const ratio = await page.evaluate(async () => {
    const d = await (await fetch('./data/neighbourhood_value_per_acre.geojson')).json();
    const cols = ['cost_roads_life_per_acre', 'cost_roads_ops_per_acre',
                  'cost_transit_ops_per_acre', 'cost_bike_ops_per_acre'];
    let nonzeroAsZero = 0, trueZeroMislabelled = 0, floored = 0, seen = 0;
    for (const f of d.features) {
      const p = f.properties, rev = p.revenue_per_acre;
      if (!(rev > 0)) continue;
      for (const c of cols) {
        const v = p[c];
        if (v == null) continue;
        seen++;
        const out = fmtSvcRatio(v / rev);
        if (v > 0 && out === '0.0%') nonzeroAsZero++;
        if (v === 0 && out !== '0.0%') trueZeroMislabelled++;
        if (out === '<0.1%') floored++;
      }
    }
    return { nonzeroAsZero, trueZeroMislabelled, floored, seen };
  });
  check('*** a nonzero service cost never prints as "0.0%" ***',
    ratio.nonzeroAsZero === 0 && ratio.seen > 1000,
    `${ratio.nonzeroAsZero} of ${ratio.seen} rows`);
  check('*** an exactly-zero cost still prints "0.0%", not the floor ***',
    ratio.trueZeroMislabelled === 0, `${ratio.trueZeroMislabelled} mislabelled`);
  check('the floor actually fires on this data (the check is not vacuous)',
    ratio.floored > 0, `${ratio.floored} rows print "<0.1%"`);

  // ---- 3d. THE DOLLAR FLOOR IS NOT VACUOUS EITHER -------------------------
  // The companion to `verify-smoke.js` §C9, and the half that does NOT belong
  // on the weekly gate: C9 asserts the invariant (no nonzero renders "$0", no
  // true zero renders the floor), which is value-free and safe to run every
  // refresh. Whether the floor ever FIRES depends on the data — a roll where no
  // hood sits under $0.50/acre is perfectly legitimate — so pinning it there
  // would cry wolf, and a check that cries wolf gets ignored. It lives here,
  // hand-run, where a zero count is a prompt to re-measure rather than a red
  // deploy. Measured 2026-09-19: 16 of 3,248 values floor on the eight columns
  // below. C9 counts 21 because it sweeps the four lot-acre variants too — the
  // two numbers describe different column sets, not a discrepancy.
  const floor = await page.evaluate(async () => {
    const d = await (await fetch('./data/neighbourhood_value_per_acre.geojson')).json();
    const cols = ['storm_charge_per_acre', 'water_charge_per_acre',
                  'cost_roads_ops_per_acre', 'cost_roads_life_per_acre',
                  'cost_transit_ops_per_acre', 'cost_bike_ops_per_acre',
                  'res_revenue_per_acre', 'revenue_per_acre'];
    let floored = 0, seen = 0;
    for (const f of d.features) {
      for (const c of cols) {
        const v = f.properties[c];
        if (v == null) continue;
        seen++;
        if (money0(v) === '<$1') floored++;
      }
    }
    return { floored, seen };
  });
  check('the dollar floor actually fires on this data (not vacuous)',
    floor.floored > 0, `${floor.floored} of ${floor.seen} values print "<$1"`);

  // ---- 3e. NOR IS THE NON-DOLLAR FLOOR ------------------------------------
  // Same split as 3d against `verify-smoke.js` §C10. Measured 2026-09-20 over
  // the served file: fire 10, transit 2, revenue_share_city 20 — and the
  // temporal shares add 726 more in their own file, not swept here.
  // ⚠️ A zero count here is a PROMPT TO RE-MEASURE, not a defect: if the fire
  // tail ever empties, the floor stops being load-bearing and S7's fire row
  // should be reopened rather than the check quietly relaxed.
  const smallFloor = await page.evaluate(async () => {
    const d = await (await fetch('./data/neighbourhood_value_per_acre.geojson')).json();
    let fire = 0, transit = 0, share = 0, seen = 0;
    for (const f of d.features) {
      const p = f.properties;
      seen++;
      if (p.fire_events_per_acre != null
        && fmtFire(p.fire_events_per_acre).startsWith('<0.01')) fire++;
      if (p.transit_dep_per_acre != null
        && fmtTransit(p.transit_dep_per_acre).startsWith('<0.01')) transit++;
      if (p.revenue_share_city != null
        && fmtPct(p.revenue_share_city * 100) === '<0.01%') share++;
    }
    return { fire, transit, share, seen };
  });
  check('the non-dollar floor actually fires on this data (not vacuous)',
    smallFloor.fire + smallFloor.transit + smallFloor.share > 0,
    `fire ${smallFloor.fire}, transit ${smallFloor.transit}, `
    + `city share ${smallFloor.share} of ${smallFloor.seen} hoods`);

  await page.close();

  // ---- 4. PUBLIC BUILD ----------------------------------------------------
  // roads, roadscost and roadslife are public, so the defect is not full-only.
  const pub = await open(url + (url.includes('?') ? '&' : '?') + 'build=public');
  const pubKeys = await pub.evaluate(() =>
    Object.keys(SERVICES).filter(k => SERVICES[k].pub));
  check('the public build offers three service layers', pubKeys.length === 3,
    pubKeys.join(','));
  const pubSeen = {};
  for (const k of pubKeys) {
    const r = await panelFor(pub, k);
    pubSeen[k] = r;
    check(`public ${k}: selection took`, r.driver === k, `driver=${r.driver}`);
    check(`public ${k}: the panel opens and is not empty`,
      r.open && r.rows > 0, `${r.rows} rows`);
    servicesForm(`public ${k}`, r);
  }
  ratioForm('public ratio/roads', await ratioPanel(pub, 'roads'));
  const pubDistinct = new Set(pubKeys.map(k => pubSeen[k].text)).size;
  check('*** PUBLIC: the panel differs across the three public layers ***',
    pubDistinct > 1, `${pubDistinct} distinct rendering(s) across ${pubKeys.length} layers`);
  await pub.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  if (!fullBuild) console.log('PARTIAL — skipped §1–3: public URL, seven of the ten service layers are full-only');
  process.exit(fail ? 1 : 0);
})();

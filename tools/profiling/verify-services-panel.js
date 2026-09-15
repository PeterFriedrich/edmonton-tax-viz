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
      label: SERVICES[k].label,
    };
  }, key);

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
    // 3b. The degraded form must EXPLAIN the missing cost, not just omit it.
    // These three have no City cost because of what the money is — utility
    // charges, and a demand-only measure — so the panel states a scope. A
    // blank would satisfy every other check here while reading as a gap.
    check(`*** ${k}: the absent cost is explained, not just omitted ***`,
      seen[k].rows === 0 && /utility charge|no fire cost|demand/i.test(seen[k].text),
      `${seen[k].rows} rows | ${seen[k].text.split('\n')[1] || ''}`.slice(0, 110));
  }
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
  }
  const pubDistinct = new Set(pubKeys.map(k => pubSeen[k].text)).size;
  check('*** PUBLIC: the panel differs across the three public layers ***',
    pubDistinct > 1, `${pubDistinct} distinct rendering(s) across ${pubKeys.length} layers`);
  await pub.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

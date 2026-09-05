// Verify the ROADS-ONLY public Services lens (2026-09-02 — SPEC_services.md
// "Roads returns to the public build"): the first exercise of the 2026-07-28
// staged-return rule.
//   node verify-services-public.js <url>            # public build
//   node verify-services-public.js <url>?build=full # full build
//
// The failure this exists to catch is a full-only service reaching the public
// root. That failure is SILENT — a stray row just renders, looking exactly like
// a feature someone shipped on purpose — so every assertion below is written
// against the PUBLIC build and the full build is checked only for the converse
// (that nothing was hidden everywhere by accident).
//
// ⚠️ Hiding the row is not the whole invariant. An unchecked-but-present
// service is still reachable through the colour radio and still contributes a
// tooltip row, so `state.services[k]` must be false too — this asserts both.
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// The split, restated independently of the page. Deliberately NOT read from
// SERVICES.pub at runtime: a guard that asks the code under test what it should
// do passes under any bug that changes both halves together.
const PUBLIC_SVC = ['roads', 'roadscost', 'roadslife'];
const FULL_ONLY_SVC = ['storm', 'fire', 'water', 'transit', 'bike',
                       'transitcost', 'bikecost'];
// Retired 2026-09-05, so it is in NEITHER list — absent from both builds.
const RETIRED_SVC = ['servicecost'];

let pass = 0, fail = 0;
function check(name, ok, detail) {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`);
  ok ? pass++ : fail++;
}

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

  const click = sel => page.$eval(sel, b => b.click()); // swiftshader hangs page.click
  const visible = svc => page.evaluate(s => {
    const r = document.querySelector(`#services .svc[data-service="${s}"]`);
    return !!r && getComputedStyle(r).display !== 'none';
  }, svc);

  const fullBuild = await page.evaluate(() => FULL_BUILD);
  console.log(`\n--- build: ${fullBuild ? 'FULL' : 'PUBLIC'} ---\n`);

  // 1. The view itself. This is the change: it used to be hidden publicly.
  check('services view button is offered', await page.evaluate(() => {
    const b = document.querySelector('#views button[data-view="services"]');
    return !!b && getComputedStyle(b).display !== 'none';
  }));

  // 2. Ratio did NOT come with it — it is a separate lens on its own release.
  const ratioOffered = await page.evaluate(() => {
    const b = document.querySelector('#views button[data-view="ratio"]');
    return !!b && getComputedStyle(b).display !== 'none';
  });
  check(fullBuild ? 'full build: ratio view offered' : 'public build: ratio view still hidden',
    fullBuild ? ratioOffered : !ratioOffered);

  await click('#views button[data-view="services"]');
  await page.waitForTimeout(1500);

  // 3. The row split, both halves of the invariant.
  for (const svc of PUBLIC_SVC) {
    check(`public row reachable: ${svc}`, await visible(svc));
  }
  for (const svc of FULL_ONLY_SVC) {
    const vis = await visible(svc);
    check(`${svc} row ${fullBuild ? 'shown in full' : 'HIDDEN in public'}`,
      fullBuild ? vis : !vis);
    if (!fullBuild) {
      check(`${svc} not checked in public`,
        await page.evaluate(s => state.services[s] === false, svc));
    }
  }

  // 3b. The retired composite is in NEITHER build (2026-09-05). ⚠️ UI only —
  //     the served geojson keeps svc_cost_per_acre until the next refresh, so a
  //     column check here would be red for a week against a correct build; the
  //     column's removal is pinned in tests/test_join_and_calculate.py.
  for (const svc of RETIRED_SVC) {
    check(`${svc} row absent from BOTH builds`,
      await page.evaluate(s => !document.querySelector(`#services .svc[data-service="${s}"]`), svc));
    check(`${svc} absent from SERVICES`,
      await page.evaluate(s => !(s in SERVICES), svc));
  }

  // 3c. THE PANEL OBEYS THE SAME SPLIT AS THE ROWS. It did not until
  //     2026-09-05: the panel carried its own per-row publish flag, so the
  //     PUBLIC hood panel printed modelled Transit and Bike cost while the
  //     public Services list hid both services — published in one place and
  //     hidden in another, which is the failure the `pub` tag exists to make
  //     unrepresentable. Derived from the same lists as the rows above.
  const panelSvcs = await page.evaluate(() => {
    const p = state.data.features.find(f => f.properties.revenue_per_acre != null).properties;
    return svcCostRows(p).flatMap(g => g.rows.map(r => r.svc));
  });
  check('panel rows match the build split',
    panelSvcs.every(s => fullBuild || PUBLIC_SVC.includes(s)),
    JSON.stringify(panelSvcs));

  // 4. A full-only service must not be driving the ramp on the public build —
  //    the radio is the second way in, and clearing the checkbox alone would
  //    leave a stale driver colouring the map.
  const driver = await page.evaluate(() => state.svcDriver);
  check('colour driver is a public service',
    fullBuild || PUBLIC_SVC.includes(driver), `driver=${driver}`);

  // 5. The lifecycle row: legend branch + primaryRow key. ⚠️ THE LEGEND IS AN
  //    IF/ELSE CHAIN WHOSE else PRINTS THE ROAD LEGEND, so a missing branch
  //    renders a confident wrong caption rather than a blank one — the exact
  //    way the bike lens shipped. Assert it is not the road fallback BY NAME.
  const hasLife = await page.evaluate(() =>
    state.data.features.some(f => f.properties.cost_roads_life_per_acre != null));
  if (!hasLife) {
    check('pre-lifecycle data file: roadslife row hidden', !(await visible('roadslife')));
    console.log('\n(data predates cost_roads_life_per_acre — stopping here)');
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  await page.$eval('#services .svc[data-service="roadslife"] input.svc-on', el => el.click());
  await page.waitForTimeout(400);
  await page.$eval('#services .svc[data-service="roadslife"] input[type="radio"]', el => el.click());
  await page.waitForTimeout(1200);

  const legend = await page.evaluate(() => ({
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
  }));
  check('lifecycle legend is NOT the road-supply fallback',
    legend.label !== 'Road metres per acre', JSON.stringify(legend));
  check('lifecycle legend names the basis',
    /lifecycle/i.test(legend.label), legend.label);
  check('lifecycle legend is in dollars', legend.min === '$0' && /^\$[\d,]+\+$/.test(legend.max),
    `${legend.min}..${legend.max}`);

  // 6. primaryRow: a missing key falls to `|| []` and prints "no X data" over a
  //    hood that HAS data.
  const primary = await page.evaluate(() => {
    const p = state.data.features.find(f =>
      f.properties.cost_roads_life_per_acre != null).properties;
    return primaryRow(p);
  });
  check('primaryRow has a roadslife entry', !/no .* data/i.test(primary), primary);
  check('primaryRow says "lifecycle"', /lifecycle/i.test(primary), primary);

  // 7. The two road cost numbers must be distinguishable in the readout. They
  //    are the SAME METRES ~11x apart, so a readout omitting its basis is
  //    indistinguishable from the other one.
  const both = await page.evaluate(() => {
    const p = state.data.features.find(f =>
      f.properties.cost_roads_life_per_acre != null
      && f.properties.cost_roads_ops_per_acre != null).properties;
    return { life: p.cost_roads_life_per_acre, ops: p.cost_roads_ops_per_acre,
             name: p.neighbourhood_name };
  });
  check('lifecycle exceeds operating on the same hood', both.life > both.ops,
    `${both.name}: $${Math.round(both.life)} vs $${Math.round(both.ops)}`);

  // 8. The panel. Public sees roads on two bases and no fire-bearing row; full
  //    additionally sees "Roads + fire", labelled as CONTAINING the row above.
  await page.evaluate(() => {
    const p = state.data.features.find(f =>
      f.properties.cost_roads_life_per_acre != null).properties;
    if (typeof renderServiceCost === 'function') renderServiceCost(p);
  });
  await page.waitForTimeout(300);
  const panel = await page.evaluate(() => {
    const el = document.getElementById('svccost');
    return { html: el ? el.innerHTML : '',
             note: document.getElementById('temporal-note').textContent };
  });
  check('panel shows a lifecycle basis group', /lifecycle/i.test(panel.html),
    panel.html.slice(0, 160));
  check('panel says there is no total', /no total/i.test(panel.note));
  // ⚠️ NO ROW MAY CONTAIN ANOTHER, in either build. Until 2026-09-05 the
  // lifecycle group had a nested "Roads + fire" row labelled "(incl. above)",
  // with a matching clause in the note; both went with the retired composite.
  // These assert the wording is gone with the row — a stale "(incl. above)" on
  // a peer row would tell the reader not to add two figures that DO add, and a
  // stale note clause would name a row that is not on screen.
  check('no nested-row label in either build', !/incl\. above/i.test(panel.html),
    panel.html.slice(0, 200));
  check('note does not warn about a nesting that no longer exists',
    !/already contains/i.test(panel.note), panel.note);
  check('no roads+fire row in the panel', !/fire/i.test(panel.html),
    panel.html.slice(0, 200));
  if (fullBuild) {
    check('full: note still warns the operating three are not added',
      /operating three/i.test(panel.note), panel.note);
  } else {
    check('public: note does not cite rows that are absent',
      !/operating three/i.test(panel.note), panel.note);
  }

  // 9. Attribution + the modelled caveat. Both are REQUIRED on the public build
  //    — it draws the road network and colours by two modelled cost columns.
  const about = await page.evaluate(() => {
    const vis = id => {
      const el = document.getElementById(id);
      return !!el && getComputedStyle(el).display !== 'none';
    };
    return { roadsCredit: vis('about-src-roads'),
             otherCredit: vis('about-src-services'),
             roadsCaveat: vis('about-modelled-roads'),
             otherCaveat: vis('about-modelled') };
  });
  check('road network is credited', about.roadsCredit);
  check('road cost carries a modelled caveat', about.roadsCaveat);
  check(`fire/transit credit ${fullBuild ? 'shown' : 'hidden'}`,
    fullBuild ? about.otherCredit : !about.otherCredit);
  check(`full-only modelled caveat ${fullBuild ? 'shown' : 'hidden'}`,
    fullBuild ? about.otherCaveat : !about.otherCaveat);

  // 10. The Money tooltip split: supply came back, the ratio row did not.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1200);
  // ⚠️ tooltipFor takes a deck PICK object, not bare properties — passing the
  // properties returns null, which reads as "the row is missing" and would have
  // this script report a gate that is working as a gate that is broken.
  const tip = await page.evaluate(() => {
    const feat = state.data.features.find(f => f.properties.road_m_per_acre > 0
      && f.properties.revenue_per_acre != null);
    const t = tooltipFor({ object: feat });
    return t ? t.html : '(tooltipFor returned null)';
  });
  check('money tooltip carries road m / acre', /road m \/ acre/.test(tip));
  check(`money tooltip ${fullBuild ? 'carries' : 'omits'} revenue / road metre`,
    fullBuild === /revenue \/ road metre/.test(tip), tip.slice(0, 220));

  console.log(`\n${pass} passed, ${fail} failed`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

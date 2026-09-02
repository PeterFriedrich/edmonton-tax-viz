// Verify the Services view's bike service (2026-08-02 — SPEC_services
// "Transportation lens": dedicated cycling metres per acre, sqrt colour
// FINDINGS §6.9, bike-network context lines) AND the Transportation /
// Other services grouping the same change introduced.
//   node verify-bike.js <url>
// Checks: checkbox gating, group captions + membership, single shared
// svc-plane, context lines, sqrt fill + independent p97.5 clamp, set-aside
// grey, LEGEND BRANCH (the else falls through to roads — a missing branch
// silently prints the road legend), tooltip row, dedicated-only blurb,
// driver handoff.
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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

  // ⚠️ Services is PUBLIC again as of the roads-only return (2026-09-02), so
  // "the view is hidden" is no longer the public build's signature — BIKE is
  // what stays full-only. A missing view now means a pre-roads data file.
  const servicesOffered = await page.evaluate(() => {
    const b = document.querySelector('#views button[data-view="services"]');
    return !!b && getComputedStyle(b).display !== 'none';
  });
  if (!servicesOffered) {
    check('pre-roads data file: services view not offered', true);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  // The public build reaches the view but must not reach this row. Assert both
  // halves — a hidden row whose state stayed checked would still colour the
  // ramp and still print a tooltip line.
  const bikeReachable = await page.evaluate(() => {
    const r = document.querySelector('#services .svc[data-service="bike"]');
    return !!r && getComputedStyle(r).display !== 'none';
  });
  if (!bikeReachable) {
    check('public build: bike row hidden', true);
    check('public build: bike not checked',
      await page.evaluate(() => state.services.bike === false));
    check('public build: bike is not the colour driver',
      await page.evaluate(() => state.svcDriver !== 'bike'));
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  const hasBike = await page.evaluate(() =>
    state.data.features.some(f => f.properties.bike_m_per_acre != null));
  if (!hasBike) {
    // Pre-bike data file: the only correct behaviours are a hidden row and
    // an untouched view — verify that and stop.
    const rowHidden = await page.evaluate(() =>
      getComputedStyle(document.querySelector('#services .svc[data-service="bike"]')).display === 'none');
    check('pre-bike file: checkbox row hidden', rowHidden);
    const stateOff = await page.evaluate(() => state.services.bike === false);
    check('pre-bike file: bike not checked', stateOff);
    await browser.close();
    process.exit(fail ? 1 : 0);
  }

  check('data carries bike_m_per_acre', true);
  const rowShown = await page.evaluate(() =>
    getComputedStyle(document.querySelector('#services .svc[data-service="bike"]')).display !== 'none');
  check('bike checkbox row present', rowShown);

  // --- the grouping (Stage 3) ---------------------------------------------
  // Group captions are labels, not controls: they must not carry inputs, and
  // each visible caption must have at least one visible row under it.
  const groups = await page.evaluate(() => {
    const kids = [...document.getElementById('services').children];
    const out = []; let cur = null;
    for (const el of kids) {
      if (el.classList.contains('svc-group')) {
        cur = { caption: el.textContent.trim(),
                hidden: getComputedStyle(el).display === 'none',
                inputs: el.querySelectorAll('input').length, rows: [] };
        out.push(cur);
      } else if (el.classList.contains('svc') && cur) {
        cur.rows.push({ k: el.dataset.service,
                        hidden: getComputedStyle(el).display === 'none' });
      }
    }
    return out;
  });
  const transport = groups.find(g => g.caption === 'Transportation');
  const other = groups.find(g => g.caption === 'Other services');
  check('Transportation group exists', !!transport);
  check('Other services group exists', !!other);
  check('every row belongs to a group',
        groups.reduce((n, g) => n + g.rows.length, 0) ===
          await page.evaluate(() => document.querySelectorAll('#services .svc').length));
  if (transport) {
    check('Transportation holds roads + transit + bike',
          ['roads', 'transit', 'bike'].every(k => transport.rows.some(r => r.k === k)),
          transport.rows.map(r => r.k).join(','));
    check('Transportation holds no non-transport service',
          !transport.rows.some(r => ['storm', 'water', 'fire'].includes(r.k)),
          transport.rows.map(r => r.k).join(','));
  }
  check('group captions carry no controls',
        groups.every(g => g.inputs === 0));
  check('no caption is left over a fully hidden group',
        groups.every(g => g.hidden || g.rows.some(r => !r.hidden)),
        groups.map(g => `${g.caption}:${g.rows.filter(r => !r.hidden).length}`).join(' '));

  await click('#views button[data-view="services"]');
  await page.waitForTimeout(4000); // roads lazy-fetch + rebuild

  // --- bike on, roads still driving ---------------------------------------
  await click('#services .svc[data-service="bike"] .svc-on');
  await page.waitForTimeout(3000); // context lines lazy-fetch + rebuild
  const on = await page.evaluate(() => {
    const ids = overlay._deck.props.layers.map(l => l.id);
    const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
    const mid = state.data.features.find(f =>
      !f.properties.is_set_aside && f.properties.bike_m_per_acre > 0);
    return {
      planeCount: ids.filter(id => id === 'svc-plane').length,
      linesPresent: ids.includes('bike-lines'),
      nLines: bikeLinesData ? bikeLinesData.lines.length : 0,
      planeNeutral: plane.props.getFillColor(mid).join() === GLASS_PLANE_COLOR.join(),
    };
  });
  check('single shared svc-plane', on.planeCount === 1, `count=${on.planeCount}`);
  check('bike context lines layer present', on.linesPresent);
  check('bike network loaded', on.nLines > 0, `n=${on.nLines}`);
  check('plane neutral while roads drive', on.planeNeutral);

  // --- hand the colour to bike --------------------------------------------
  await click('#services .svc[data-service="bike"] input[type="radio"]');
  await page.waitForTimeout(1500);
  const drives = await page.evaluate(() => {
    const plane = overlay._deck.props.layers.find(l => l.id === 'svc-plane');
    const kept = state.data.features.filter(f =>
      !f.properties.is_set_aside && f.properties.bike_m_per_acre != null);
    const vals = kept.map(f => f.properties.bike_m_per_acre).sort((a, b) => a - b);
    const pos = (vals.length - 1) * 0.975, lo = Math.floor(pos);
    const q = vals[lo] + (vals[Math.ceil(pos)] - vals[lo]) * (pos - lo);
    const mid = kept[Math.floor(kept.length / 2)];
    const scale = svcScale('bike_m_per_acre');
    // bike colour is SQRT (FINDINGS §6.9) — re-derived independently of svcT
    const expected = rampColorAt(
      Math.sqrt(Math.min(1, mid.properties.bike_m_per_acre / scale.clamp)));
    // A LINEAR ramp must NOT also satisfy this check, or the assertion cannot
    // reject the wrong transform (the S85 "reject both" rule).
    const linear = rampColorAt(Math.min(1, mid.properties.bike_m_per_acre / scale.clamp));
    const aside = state.data.features.find(f => f.properties.is_set_aside);
    return {
      clampMatchesP975: Math.abs(scale.clamp - q) < 1e-6,
      clamp: scale.clamp,
      transform: scale.transform,
      midFillOk: plane.props.getFillColor(mid).join() === expected.join(),
      sqrtDiffersFromLinear: expected.join() !== linear.join(),
      asideGrey: plane.props.getFillColor(aside).join() === SET_ASIDE_COLOR.join(),
      legendLabel: document.getElementById('legend-label').textContent,
      legendMin: document.getElementById('legend-min').textContent,
      legendMax: document.getElementById('legend-max').textContent,
      blurb: document.getElementById('title-p').textContent,
      tip: primaryRow(mid.properties),
    };
  });
  check('transform is sqrt', drives.transform === 'sqrt', drives.transform);
  check('clamp = independent p97.5', drives.clampMatchesP975, `clamp=${drives.clamp}`);
  check('mid-hood fill matches sqrt ramp', drives.midFillOk);
  check('the sqrt assertion would reject a linear ramp', drives.sqrtDiffersFromLinear);
  check('set-aside hood grey', drives.asideGrey);

  // THE LEGEND BRANCH. The services legend is an if/else chain whose else
  // prints the ROAD legend, so a missing branch fails silently and looks fine.
  check('legend label names the bike metric, not roads',
        drives.legendLabel === 'Dedicated bike route metres per acre (sqrt colour)',
        drives.legendLabel);
  check('legend is not the road fallback',
        !/road metres/i.test(drives.legendLabel), drives.legendLabel);
  check('legend min is 0 m', drives.legendMin === '0 m', drives.legendMin);
  check('legend max anchors to clamp',
        drives.legendMax === Math.round(drives.clamp).toLocaleString() + ' m+',
        `${drives.legendMax} vs clamp ${drives.clamp}`);

  // The tooltip headline follows the driver (not a positional row).
  check('tooltip headline names dedicated bike metres',
        /dedicated bike route m \/ acre/.test(drives.tip), drives.tip);

  // The blurb must carry the three exclusions the metric depends on —
  // without them the number reads as "all bike routes", which it is not.
  check('blurb says shared streets are already counted as roads',
        /already counted as roads/.test(drives.blurb));
  check('blurb says coming-soon routes are excluded',
        /coming soon/.test(drives.blurb));
  check('blurb warns the peaks are river-valley set-aside land',
        /river valley/.test(drives.blurb));

  // --- driver handoff ------------------------------------------------------
  // Unchecking the driving service must hand the ramp to another CHECKED
  // service, never leave the map coloured by a service that is off.
  await click('#services .svc[data-service="bike"] .svc-on');
  await page.waitForTimeout(1500);
  const off = await page.evaluate(() => {
    const ids = overlay._deck.props.layers.map(l => l.id);
    return {
      bikeOff: state.services.bike === false,
      driver: state.svcDriver,
      driverChecked: state.services[state.svcDriver] === true,
      linesGone: !ids.includes('bike-lines'),
      legendLabel: document.getElementById('legend-label').textContent,
    };
  });
  check('unchecking bike clears it', off.bikeOff);
  check('ramp hands off to a checked service', off.driverChecked, `driver=${off.driver}`);
  check('bike context lines removed with the service', off.linesGone);
  check('legend follows the new driver',
        !/bike/i.test(off.legendLabel), off.legendLabel);

  console.log(`\n${fail ? 'FAILURES: ' + fail : 'ALL CHECKS PASSED'} (${pass} passed)`);
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

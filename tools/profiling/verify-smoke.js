// Render smoke check for the WEEKLY DATA REFRESH — the one path that changes
// what the site shows without anyone looking at it.
//
// `refresh.yml` downloads, regenerates, commits AND DEPLOYS in a single run. It
// carries four guards — check_unmatched_names, year alignment,
// check_value_anchors, check_temporal_years — and every one of them is
// DATA-side. Until this script, nothing on that path had ever looked at the
// rendered page. A refresh rewrites four served files (measured on ab8bac7):
//
//   neighbourhood_value_per_acre.geojson   every lens reads it
//   temporal.json                          history panel, sparkline, change lens
//   dev_grid.json                          development / infill
//   status.json                            banner, mill rates, vintage
//
// ⚠️ EVERY ASSERTION HERE IS AN INVARIANT. NOTHING IS PINNED TO A DATA VALUE,
// and that is the whole design. `verify-temporal.js` went red on the 2026-08-01
// refresh because it pinned a live year that `check_temporal_years.py`
// explicitly refuses to band — cry-wolf by construction. A weekly check that
// cries wolf gets ignored, which is strictly worse than no check. So counts are
// DERIVED from the served files, and the headline family (C) asserts only that
// nothing renders as garbage — true of every legitimate refresh, false the
// moment a column changes shape.
//
// ⚠️ It drives NO real pointer. View switching goes through the page's own
// applyView/applyMetric, so this cannot inherit quirk (mmm) — real-pointer
// scripts flake when they share a box, and a flaky gate that blocks the weekly
// publish would be worse than the gap it closes. Clickability is other scripts'
// job; this one is about the data reaching the pixels.
//
// ⚠️ RUN IT AGAINST BOTH BUILDS. The dev server serves the full build (quirk
// rrr), so full-only states are always present locally and a check that assumes
// them passes locally and fails on the public root — that is what PR #141
// existed to fix. Full-only states are gated on BUILD read from the page.
//
//   node tools/profiling/verify-smoke.js http://localhost:8931/index.html
//   node tools/profiling/verify-smoke.js http://localhost:8931/full/index.html
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

if (!url) {
  console.error('usage: node verify-smoke.js <url>');
  process.exit(2);
}

// The strings that mean "a number did not survive the pipeline". Rendered text
// is the last place these show up and the only place anyone would see them —
// no exception is thrown and no exit code changes when a column goes missing,
// which is exactly why this family exists.
const GARBAGE = /\bNaN\b|\bundefined\b|\bnull\b|\bInfinity\b|\$NaN|\$undefined/;

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

  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  // ---- A. LOAD INTEGRITY --------------------------------------------------
  // Collected from the first navigation, so a 404 on any data file is caught
  // even though the page is written to degrade quietly when one is missing.
  const bad = [];        // non-2xx responses
  const failed = [];     // requests that never completed
  const pageErrors = [];
  const consoleErrors = [];
  const dataHits = new Set();
  page.on('response', r => {
    if (/\/data\//.test(r.url())) dataHits.add(r.url().split('/').pop().split('?')[0]);
    if (r.status() >= 400) bad.push(`${r.status()} ${r.url()}`);
  });
  page.on('requestfailed', r => failed.push(r.url()));
  page.on('pageerror', e => pageErrors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });

  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);

  check('A1: no 4xx/5xx on any request', bad.length === 0, bad.join('; '));
  check('A2: no failed requests', failed.length === 0, failed.join('; '));
  check('A3: no uncaught page exceptions', pageErrors.length === 0, pageErrors.join('; '));
  check('A4: no console errors', consoleErrors.length === 0, consoleErrors.slice(0, 3).join('; '));

  const build = await page.evaluate(() => BUILD);
  console.log(`\n(build = ${build}, data files fetched: ${[...dataHits].sort().join(', ')})\n`);

  // The four files a refresh rewrites must actually have been fetched. A
  // silently-skipped fetch would make every downstream check vacuous — the
  // page degrades on purpose when a file is absent, so "no error" is not
  // evidence the data arrived. temporal.json is fetched by BOTH builds (the
  // lens went public 2026-07-31); dev_grid only where Development exists.
  check('A5: the refreshed geojson was fetched',
    dataHits.has('neighbourhood_value_per_acre.geojson'));
  check('A6: temporal.json was fetched', dataHits.has('temporal.json'));
  check('A7: status.json was fetched', dataHits.has('status.json'));

  // ---- B. SHAPE, DERIVED FROM THE SERVED FILES ----------------------------
  // ⚠️ Every count below is read from the file the page actually loaded, never
  // typed in. A literal here would be the 2026-08-01 bug again: 839 cells moved
  // in a legitimate refresh and any pinned number would have gone red.
  const shape = await page.evaluate(async () => {
    const geo = await fetch('./data/neighbourhood_value_per_acre.geojson').then(r => r.json());
    const temporal = await fetch('./data/temporal.json').then(r => r.json());
    const status = await fetch('./data/status.json').then(r => r.json());

    // ⚠️ THE SERVICE PLANE COLUMNS — B6's coupling applied to the surface B6
    // does not reach. `SERVICES` alone is NOT the whole list: Roads is a ground
    // layer rather than a plane service and carries no `plane.col`, so
    // `road_m_per_acre` appears only in RATIO_DENOMS. Taking the union means
    // neither the services view nor the ratio picker can grow a column these
    // checks do not know about.
    const svcCols = [...new Set([
      ...Object.values(SERVICES).map(s => s.plane && s.plane.col),
      ...Object.values(RATIO_DENOMS).map(d => d.col),
    ].filter(Boolean))].sort();

    return {
      served: geo.features.length,
      loaded: state.data ? state.data.features.length : -1,
      years: (temporal.years || []).length,
      hoodsInTemporal: Object.keys(temporal.hoods || temporal.series || {}).length,
      status,
      // The columns the lenses read, derived from the page's own category
      // config rather than listed again here — the same coupling that stops
      // the Uses area shares and the revenue shares drifting apart.
      useFracs: (typeof USE_CATEGORIES !== 'undefined' ? USE_CATEGORIES : []).map(u => u.frac),
      sample: geo.features[0] ? Object.keys(geo.features[0].properties) : [],
      // ⚠️ THE COLUMN EVERY MONEY LENS COLOURS BY, derived from METRICS' own
      // `key` rather than listed here. Falsification showed why this is needed:
      // renaming `revenue_per_acre` did NOT trip the readout sweep, because
      // viewTooltip guards each row with `!= null` and therefore OMITS the row
      // rather than printing NaN. A silently dropped row is this project's
      // cardinal failure and the garbage sweep cannot see it.
      // ABSENT (undefined) only — a null is a legitimate "no value for this
      // hood" (set-aside land), and treating it as missing would cry wolf.
      missingMetricCols: (() => {
        const out = {};
        Object.values(METRICS).forEach(m => {
          const n = geo.features.filter(f => f.properties[m.key] === undefined).length;
          if (n) out[m.key] = n;
        });
        return out;
      })(),
      svcCols,
      // Absence per service column, ABSENT (undefined) only — same rule as B6.
      // Unlike the money metrics these columns carry no nulls at all today
      // (set-aside is its own `is_set_aside` flag, and only the four
      // `_per_lot_acre` columns are ever null), but reading `undefined` keeps
      // the two families answering the same question.
      svcColAbsent: Object.fromEntries(
        svcCols.map(col => [col, geo.features.filter(f => f.properties[col] === undefined).length])),
      // The flag the data gate actually writes: each services row is
      // `style.display = "none"`d when its column is missing. Read the row's
      // OWN inline display, never computed visibility — a computed test would
      // report every row as gated off whenever the panel itself is closed.
      //
      // ⚠️ FULL-ONLY ROWS ARE EXCLUDED IN THE PUBLIC BUILD (2026-09-02). Two
      // different gates now write the same inline `display:none`: the DATA gate
      // (column missing) and the BUILD gate (`SERVICES[k].pub`). B8 is about the
      // first, and since the roads-only return the public build legitimately
      // hides eight rows whose columns are present — without this filter B8
      // reports all eight as data-gate bugs.
      svcRowHidden: Object.fromEntries(
        Object.entries(SERVICES)
          .filter(([, s]) => s.plane && s.plane.col && (FULL_BUILD || s.pub))
          .map(([key, s]) => {
            const row = document.querySelector(`#services .svc[data-service="${key}"]`);
            return [s.plane.col, row ? row.style.display === 'none' : null];
          })),
    };
  });

  check('B1: every served feature is loaded into state',
    shape.loaded === shape.served, `loaded ${shape.loaded} of ${shape.served}`);
  check('B2: the geojson is non-empty', shape.served > 0, `${shape.served} features`);
  check('B3: temporal.json carries a year list', shape.years > 0, `${shape.years} years`);

  // Land-use fraction columns: derived list, so adding a category cannot leave
  // this check behind.
  const missingUse = shape.useFracs.filter(f => !shape.sample.includes(f));
  check('B4: every USE_CATEGORIES fraction column is present',
    missingUse.length === 0, missingUse.join(', '));

  const missingMetric = Object.entries(shape.missingMetricCols);
  check('B6: every METRICS column is present on every feature',
    missingMetric.length === 0,
    missingMetric.map(([k, n]) => `${k} absent on ${n}`).join('; '));

  // ⚠️ WHAT B7 CATCHES AND, MORE IMPORTANTLY, WHAT IT DOES NOT.
  // It catches a service column present for some hoods and missing for others —
  // the per-hood failure family C exists for, seen at the schema level.
  //
  // It does NOT catch a service column dropped from EVERY feature, and that is
  // structural, not an oversight: a dropped column has to be tolerated here
  // because a legitimately-not-yet-shipped one looks identical from inside the
  // browser (bike_m_per_acre was exactly this between the 2026-08-02 merge and
  // the refresh that followed it). Failing on absence would red the weekly
  // publish over a column that was never supposed to be there yet — the
  // cry-wolf failure this whole file is built to avoid.
  //
  // The full drop is `scripts/check_served_columns.py`'s job. That guard holds a
  // COMMITTED baseline, so it can tell "not shipped yet" from "was here last
  // week and is gone now"; nothing derived from the served file alone can, since
  // data and check move together (the same limit B5 documents for temporal.json).
  const svcAbsent = Object.entries(shape.svcColAbsent);
  const svcPartial = svcAbsent.filter(([, n]) => n > 0 && n < shape.served);
  const svcGone = svcAbsent.filter(([, n]) => n === shape.served).map(([k]) => k);
  check('B7: every SERVICES/RATIO_DENOMS column is present on every feature or on none',
    svcPartial.length === 0,
    svcPartial.length
      ? svcPartial.map(([k, n]) => `${k} absent on ${n} of ${shape.served}`).join('; ')
      : `${shape.svcCols.length} columns${svcGone.length ? `, not yet shipped: ${svcGone.join(', ')}` : ''}`);

  // The other direction, and the one B7 cannot see from the data alone: every
  // services row self-gates on its own column, so a gate that disagrees with the
  // data is silent both ways — a row offered over a column that is not there
  // renders "no X data" over hoods that have it, and a row hidden over a column
  // that IS there simply loses a lens with no error anywhere.
  const svcGateBad = Object.entries(shape.svcRowHidden)
    .filter(([col, hidden]) => hidden !== null && hidden !== (shape.svcColAbsent[col] === shape.served))
    .map(([col, hidden]) => `${col} ${hidden ? 'gated off but present' : 'offered but absent'}`);
  check('B8: each services row is offered exactly when its column is present',
    svcGateBad.length === 0, svcGateBad.join('; '));

  // The panel's chart must plot one point per PUBLISHED year. The year list is
  // deliberately non-contiguous (2024 omitted by decision), so this compares
  // against the file's own list rather than a range.
  // ⚠️ WHAT THIS DOES AND DOES NOT CATCH, established by falsification:
  // it catches the CHART disagreeing with the data it was handed — an off-by-one
  // splice, a bridged gap, a dropped run. It does NOT catch temporal.json itself
  // losing a year: the chart renders from that same file, so both sides move
  // together and the check stays green. That is `check_temporal_years.py`'s job
  // (it holds an archive to compare against); pinning a year COUNT here would
  // instead cry wolf at the January roll-forward.
  // ⚠️ COUNT DISTINCT PLOTTED POSITIONS, not elements. The line is drawn as RUNS
  // SPLIT AT EVERY GAP (invariant 1 — nothing may bridge the hole), so a
  // single-year run renders as a <circle> rather than a <path>, and the latest
  // point carries a second marker circle at the same coordinates. Counting
  // elements would under- or over-count depending on where the gaps fall.
  // Positions are safe to dedupe on because x is scaled from the YEAR VALUE,
  // so two years can never plot at the same x.
  await page.evaluate(() => {
    applyMetric('value_per_acre');
    openTemporal(state.data.features[0].properties.neighbourhood_name);
  });
  await page.waitForTimeout(400);
  const linePts = await page.evaluate(() => {
    const el = document.getElementById('temporal-chart');
    const seen = new Set();
    el.querySelectorAll('path').forEach(p => {
      (p.getAttribute('d') || '').replace(/[ML]/g, ' ').trim().split(/\s+/)
        .filter(Boolean).forEach(xy => seen.add(xy));
    });
    el.querySelectorAll('circle').forEach(c => {
      seen.add(`${c.getAttribute('cx')},${c.getAttribute('cy')}`);
    });
    return seen.size;
  });
  await page.evaluate(() => closeTemporal());
  check('B5: the chart plots one point per published year',
    linePts === shape.years, `${linePts} plotted vs ${shape.years} years`);

  // ---- C. NOTHING RENDERS AS GARBAGE --------------------------------------
  // ⚠️ THE HIGHEST-VALUE FAMILY AND THE ONLY FULLY VALUE-FREE ONE. A dropped or
  // renamed column does not throw — it renders "$NaN" or "undefined" into a
  // readout and the page otherwise behaves. This sweeps EVERY hood through
  // EVERY lens's own tooltip renderer, which is ~400 x 10 renders and costs
  // about a second, because the failure is per-hood: a column can survive for
  // 405 neighbourhoods and vanish for one.
  const STATES = [
    ['money / revenue',        () => { applyView('money'); applyMetric('revenue_per_acre'); }],
    ['money / residential',    () => applyMetric('res_revenue_per_acre')],
    ['money / non-residential', () => applyMetric('nonres_revenue_per_acre')],
    ['money / value',          () => applyMetric('value_per_acre')],
    ['services',               () => applyView('services')],
    ['ratio',                  () => applyView('ratio')],
    ['development',            () => applyView('development')],
    ['uses',                   () => applyView('uses'), 'full'],
  ];

  for (const [label, fn, needs] of STATES) {
    if (needs === 'full' && build !== 'full') {
      check(`C-${label}: full-only, correctly skipped on this build`, true);
      continue;
    }
    // ⚠️ SWITCH, SETTLE, THEN READ — in three steps, not one evaluate. Some
    // views load their own geometry on entry (services fetches roads), so a
    // legend read in the same synchronous turn returns the PREVIOUS view's
    // text. The first draft did exactly that and reported money's "$0 .. $4M+"
    // for services, ratio and development — three checks that looked green
    // while testing nothing.
    await page.evaluate(body => { eval(`(${body})()`); }, fn.toString());
    await page.waitForTimeout(700);
    const r = await page.evaluate(() => {
      const out = { offenders: [], rendered: 0, legend: null };
      for (const f of state.data.features) {
        const html = viewTooltip({ object: f });
        if (html == null) continue;
        out.rendered++;
        if (/\bNaN\b|\bundefined\b|\bnull\b|\bInfinity\b|\$NaN|\$undefined/.test(html))
          out.offenders.push(f.properties.neighbourhood_name);
      }
      // ⚠️ READ WHICHEVER LEGEND SURFACE IS ACTUALLY SHOWING. Uses is
      // categorical — it fills #legend-cats and leaves min/max hidden and
      // STALE, so asserting min/max there silently re-tests the previous
      // view's legend instead of this one.
      const cats = document.getElementById('legend-cats');
      out.legend = {
        min: document.getElementById('legend-min').textContent,
        max: document.getElementById('legend-max').textContent,
        cats: cats.textContent.trim(),
        catsVis: getComputedStyle(cats).display !== 'none',
      };
      return out;
    });

    check(`C-${label}: every hood renders a readout`,
      r.rendered > 0, `${r.rendered} rendered`);
    check(`C-${label}: no NaN/undefined in any hood's readout`,
      r.offenders.length === 0,
      r.offenders.length ? `${r.offenders.length} hoods, e.g. ${r.offenders.slice(0, 3).join(', ')}` : '');
    if (r.legend.catsVis) {
      check(`C-${label}: the category legend is populated and clean`,
        r.legend.cats.length > 0 && !GARBAGE.test(r.legend.cats),
        r.legend.cats.slice(0, 60).replace(/\s+/g, ' '));
    } else {
      check(`C-${label}: legend bounds are not garbage`,
        !GARBAGE.test(r.legend.min + ' ' + r.legend.max),
        `${r.legend.min} .. ${r.legend.max}`);
    }
  }

  // ---- D. PROVENANCE ------------------------------------------------------
  // The rates on screen are a fiscal headline read straight from the manifest;
  // a refresh that rewrites status.json must not leave the pod disagreeing with
  // it. Compared as PARSED NUMBERS, never as strings built with the page's own
  // formatter — that would hide a formatter bug, which is how "$1,876,137"
  // shipped as "$2M" (S85).
  // ⚠️ SCOPE, established by falsification: this catches the POD drifting from
  // the manifest — a hardcoded rate, a wrong field, a class dropped from the
  // render. It does NOT catch a wrong rate IN the manifest, because the pod
  // reads that same file and the two move together. Whether the rates are
  // correct is `data/mill_rates.json`'s reviewed-input problem, upstream of
  // anything the browser can see.
  const prov = await page.evaluate(() => {
    applyView('money'); applyMetric('revenue_per_acre');
    const pod = document.getElementById('millrates');
    return {
      text: pod ? pod.textContent : null,
      vis: pod ? pod.getClientRects().length > 0 : false,
      banner: (document.getElementById('banner').textContent || '').trim(),
      bannerVis: document.getElementById('banner').getClientRects().length > 0,
    };
  });

  // municipal_rates is {unit, classes:[{name, rate}], assumed:[...]} — the
  // rates live under `classes`, not as top-level values.
  const rateVals = ((shape.status.municipal_rates || {}).classes || [])
    .map(c => c.rate).filter(v => typeof v === 'number');

  // ⚠️ ASSERT AGREEMENT, NEVER THE MANIFEST'S CONTENT. An earlier draft failed
  // when `municipal_rates` was absent — and the inverse test caught it crying
  // wolf on pre-2026-08-01 data, from before the pod existed. Whether rates are
  // PUBLISHED is a reviewed-input question (`data/mill_rates.json`), and at a
  // January roll they can legitimately lag; a render gate that blocks the weekly
  // publish over that is the exact failure this file is built to avoid. So:
  // rates present ⇒ the pod must show them; rates absent ⇒ the pod must not
  // show numbers it cannot source. Both directions are real regressions.
  if (!rateVals.length) {
    check('D1: no manifest rates, so the pod shows none either', !prov.vis,
      'manifest carries no municipal_rates');
  } else {
    check('D1: the mill-rate pod is rendered', prov.vis, `${rateVals.length} classes in manifest`);
  }
  if (prov.vis && rateVals.length) {
    // Parsed numbers, never a string built with the page's own formatter —
    // that would make a formatter bug invisible (how "$1,876,137" shipped as
    // "$2M"). Tolerance is well under one display digit.
    const shown = (prov.text.match(/\d+\.\d+/g) || []).map(Number);
    const missing = rateVals.filter(v => !shown.some(s => Math.abs(s - v) < 0.0001));
    check('D2: every manifest mill rate appears in the pod',
      missing.length === 0, missing.length ? `missing ${missing.join(', ')}` : '');
  }

  // A banner is shown when and only when the manifest asks for one — a stale
  // banner outlives the condition it reported, and a missing one hides a hold.
  const wantBanner = !!(shape.status.banner && String(shape.status.banner).trim());
  check('D3: banner state matches the manifest',
    wantBanner === prov.bannerVis,
    `manifest ${wantBanner ? 'wants' : 'wants no'} banner, page ${prov.bannerVis ? 'shows' : 'shows none'}`);

  check('D4: no garbage in the banner text', !GARBAGE.test(prov.banner), prov.banner);

  // Errors accumulated during the whole sweep, not just first paint.
  check('A8: no page exceptions across the full sweep',
    pageErrors.length === 0, pageErrors.join('; '));

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

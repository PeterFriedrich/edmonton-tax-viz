// Verify the temporal lens's render (SPEC_temporal.md phase 3): the hover
// sparkline and the click-to-pin assessment-history panel.
//
// The load-bearing claims, in the order they'd fail silently:
//   1. **2024 LOOKS ABSENT.** The published year list is deliberately
//      non-contiguous (§0.2). So the line must be drawn as TWO runs, not one
//      polyline bridging the hole, and x must be scaled from the year value —
//      proven here by measuring the gap span against an ordinary one-year step
//      (must be ~2x, not 1x, which is what index positioning would give).
//   2. **Both y endpoints are labelled**, because the axis does not start at
//      zero (most hoods are under 1% of the base; zero-basing shows nothing).
//   3. Both denominators are named — total base AND commercial base (§6): the
//      commercial figure is what public reporting quotes.
//   4. The gap's reason is stated, and says outright that nothing was
//      interpolated.
//   5. It dismisses three ways (the x, Escape, a second click on the same hood)
//      and clicking ANOTHER hood re-pins rather than closing.
//   6. The panel is in CHROME_IDS, so the label sweep dodges it — otherwise hood
//      names paint underneath it.
//   7. It is PUBLIC as of 2026-07-31 (promoted from full-only): `?build=public`
//      fetches the history, carries the sparkline, pins the panel, and STATES
//      the 2024 omission — a public gap with no explanation reads as broken.
//   8. It collides with nothing on desktop, and becomes a bottom sheet that
//      spares the control column at 390px.
//   node verify-temporal.js <url>
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
  // ⚠️ THE HISTORY PANEL LIVES UNDER **VALUE** SINCE 2026-08-01. The app loads
  // on Revenue, where #temporal now shows the zone-revenue breakdown instead
  // (DECISIONS.md, and `verify-revenue-panel.js` owns that side). Every page
  // this script opens therefore selects Value first — otherwise the whole file
  // would be asserting the history contract against a panel deliberately
  // showing something else. This is a change of LENS, not of behaviour: nothing
  // below was relaxed.
  const open = async (u, vp) => {
    const page = await browser.newPage({ viewport: vp });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
    await page.evaluate(() => applyMetric('value_per_acre'));
    await page.waitForTimeout(600);
    return page;
  };
  const overlap = (a, b) => a.right > b.left && a.left < b.right &&
                            a.bottom > b.top && a.top < b.bottom;

  // ---- desktop, full build ------------------------------------------------
  const page = await open(url, { width: 1440, height: 900 });

  const loaded = await page.evaluate(() => {
    // temporalData is a top-level `let` and so NOT on window; probe it through
    // temporalFor, which IS (function declarations become window properties).
    const t = temporalFor('DOWNTOWN');
    const i = t && t.years.length - 1;
    return t && {
      years: t.years, first: t.share[0], last: t.share[i],
      // The live year's rendered numbers are checked against THESE, not against
      // literals — see the note on `near` below.
      liveYear: t.years[i], liveValue: t.value[i], liveComm: t.commercial[i],
      lo: Math.min(...t.share), hi: Math.max(...t.share),
      peak: Math.max(...t.share), peakYear: t.years[t.share.indexOf(Math.max(...t.share))],
    };
  });
  check('temporal.json loaded and decodes', !!loaded);
  check('2024 is absent from the year list',
    loaded && !loaded.years.includes(2024) && loaded.years.includes(2023) &&
    loaded.years.includes(2025), loaded ? `n=${loaded.years.length}` : '');
  // ⚠️ THE LIVE YEAR IS NOT PINNABLE, AND PINNING IT HERE CRIED WOLF (S86).
  // This file used to assert Downtown 5.09% (2012) -> 3.30% (2025) as equalities.
  // The 2026-08-01 refresh moved the 2025 slice and reddened 5 checks with
  // nothing wrong: the diff was 839 changed cells, EVERY ONE of them in 2025,
  // with 2012-2023 bit-identical across all 406 hoods and the shares still
  // conserving to 100%. That is the pipeline working as designed —
  // `scripts/check_temporal_years.py` deliberately refuses to band the live year
  // ("a live snapshot that genuinely moves week to week"), so a front-end
  // equality on it contradicts the guard and goes red after every roll update.
  //
  // The split below is the fix: HISTORICAL years are frozen by decision and stay
  // pinned tight (they are the anchor that proves the splice didn't shift),
  // while every live-year number is DERIVED from the loaded series and compared
  // to the rendered string. Deriving beats banding here because it still fails
  // on the bug a band would wave through — the panel rendering the wrong hood,
  // the wrong series, or the wrong index.
  check('Downtown decodes to the audited 2012 share (frozen)',
    loaded && Math.abs(loaded.first - 5.09) < 0.01,
    loaded ? `${loaded.first.toFixed(2)}%` : '');
  check('the live year decodes to a plausible share',
    loaded && loaded.last > 0 && loaded.last < 100,
    loaded ? `${loaded.liveYear}: ${loaded.last.toFixed(2)}%` : '');

  // ⚠️ Compare PARSED NUMBERS, never a formatted string built with the page's own
  // formatter — that would make a formatter bug invisible, and S85 shipped one
  // (`fmtBig` printed a $1,876,137 levy as "$2M"). Tolerance is one display ulp:
  // fmtPct and fmtBig both carry two decimals, so half of the last place is
  // 0.005 and anything coarser than the display claims fails.
  const near = (a, b) => a !== null && a !== undefined && Math.abs(a - b) < 0.006;
  const num = (s, re) => { const m = re.exec(s); return m ? parseFloat(m[1]) : null; };

  // ---- the hover teaser ---------------------------------------------------
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'DOWNTOWN');
    const money = tooltipFor({ object: f });
    // A no-data branch must still carry the sparkline: value history exists
    // regardless of whether the current view has a number for the hood.
    const setAside = state.data.features.find(x => x.properties.is_set_aside);
    // Bare references, not window.*: top-level consts aren't window properties
    // but do resolve in the page's global lexical scope.
    const g = temporalGeom(temporalFor('DOWNTOWN'), SPARK_W, SPARK_H, 3);
    return {
      html: money.html,
      runs: g.runs.map(r => r.length),
      gaps: g.gaps.map(gp => gp.years),
      onSetAside: setAside
        ? (tooltipFor({ object: setAside }).html.match(/class="spark"/g) || []).length : -1,
    };
  });
  check('sparkline is in the tooltip', /class="spark"/.test(tip.html));
  // Two runs of 12 and 1: the 2025 point is deliberately NOT joined to 2023, so
  // it renders as a detached dot. One run of 13 would mean the hole was bridged.
  check('the series splits into runs at the gap, and does not bridge it',
    tip.runs.length === 2 && tip.runs[0] === 12 && tip.runs[1] === 1 &&
    tip.gaps.length === 1 && tip.gaps[0] === 1,
    `runs=[${tip.runs}] gaps=[${tip.gaps}]`);
  // Endpoints derived: the 2012 end is frozen, the live end tracks the roll.
  const tipRow = /([\d.]+)% → ([\d.]+)% of city base, (\d{4})–(\d{4})/.exec(tip.html);
  check('tooltip row names the denominator + endpoints',
    !!tipRow && near(parseFloat(tipRow[1]), loaded.first) &&
    near(parseFloat(tipRow[2]), loaded.last) &&
    +tipRow[3] === loaded.years[0] && +tipRow[4] === loaded.liveYear,
    tipRow ? tipRow[0] : 'row absent');
  check('tooltip row flags the 2024 hole', /\(2024 n\/a\)/.test(tip.html));
  check('tooltip advertises click-to-pin', /click to pin/.test(tip.html));
  check('sparkline also rides a set-aside tooltip', tip.onSetAside === 1);

  // ---- the pinned panel ---------------------------------------------------
  const panel = await page.evaluate(() => {
    openTemporal('DOWNTOWN');
    const svg = document.querySelector('#temporal-chart svg');
    const rectEls = [...svg.querySelectorAll('rect')];
    const band = { x0: +rectEls[0].getAttribute('x'), w: +rectEls[0].getAttribute('width') };
    // Every drawn x, so the band can be checked for anything crossing it.
    const paths = [...svg.querySelectorAll('path')].map(p => p.getAttribute('d'));
    const xs = paths.map(d => d.slice(1).split('L').map(pt => +pt.split(',')[0]));
    const first = xs[0];
    return {
      band,
      // A path that has a point on both sides of the band spans the hole.
      spansBand: xs.some(p => p.some(x => x < band.x0 + 0.5) &&
                              p.some(x => x > band.x0 + band.w - 0.5)),
      open: document.getElementById('temporal').classList.contains('open'),
      name: document.getElementById('temporal-name').textContent,
      read: document.getElementById('temporal-read').textContent,
      note: document.getElementById('temporal-note').textContent,
      svgText: [...svg.querySelectorAll('text')].map(t => t.textContent),
      nPaths: paths.length,
      stepW: first.length > 1 ? first[1] - first[0] : 0,
      // 2023 (the last point of the long run) to 2025 (the detached dot).
      jumpW: +svg.querySelectorAll('g circle')[0].getAttribute('cx')
             - first[first.length - 1],
      chromeHitsPanel: (() => {
        const r = document.getElementById('temporal').getBoundingClientRect();
        return chromeBoxes().some(c =>
          Math.abs(c.x0 - r.left) < 1 && Math.abs(c.y0 - r.top) < 1);
      })(),
      rect: document.getElementById('temporal').getBoundingClientRect().toJSON(),
      title: document.getElementById('title').getBoundingClientRect().toJSON(),
      botleft: document.getElementById('botleft').getBoundingClientRect().toJSON(),
      controls: document.getElementById('controls').getBoundingClientRect().toJSON(),
    };
  });
  check('clicking pins the panel open', panel.open);
  check('panel names the hood', panel.name === 'DOWNTOWN', panel.name);
  check('no drawn line crosses the no-data band', !panel.spansBand);
  // 2023 -> 2025 must be TWICE an ordinary one-year step. Index positioning
  // would make it one, which is the whole failure this measurement exists to
  // catch — and it is invisible to the eye on a series this dense.
  check('x is year-scaled: 2023->2025 is ~2x a one-year step',
    panel.stepW > 0 && Math.abs(panel.jumpW / panel.stepW - 2) < 0.15,
    `jump=${panel.jumpW.toFixed(1)} step=${panel.stepW.toFixed(1)} ratio=${(panel.jumpW / panel.stepW).toFixed(2)}`);
  // One year wide, not the whole 2023->2025 run: shading the bracketing years
  // would claim they are missing too.
  check('the band covers the missing year only',
    Math.abs(panel.band.w / panel.stepW - 1) < 0.15,
    `band=${panel.band.w.toFixed(1)} step=${panel.stepW.toFixed(1)}`);
  check('the gap is shaded and labelled "no data"',
    panel.svgText.includes('no data'));
  // The endpoints are the series MIN and MAX, derived — not the first and last
  // year, and not literals. §2's invariant is that BOTH carry a label, because
  // the axis does not start at zero.
  const pctLabels = panel.svgText.map(s => num(s, /^([\d.]+)%$/)).filter(v => v !== null);
  check('both y endpoints are labelled (axis is not zero-based)',
    pctLabels.some(v => near(v, loaded.lo)) && pctLabels.some(v => near(v, loaded.hi)),
    panel.svgText.join(' | '));
  check('x axis names the first and last year',
    panel.svgText.includes('2012') && panel.svgText.includes('2025'));
  // Headline, commercial share and value are all the LIVE year — derived. The
  // year is asserted alongside the number so an off-by-one on the last index
  // cannot pass by landing on a neighbouring year's share.
  const headline = new RegExp(`${loaded.liveYear}: ([\\d.]+)% of Edmonton's total assessment base`)
    .exec(panel.read);
  check('read-out names the TOTAL base', !!headline && near(parseFloat(headline[1]), loaded.last),
    headline ? headline[0] : panel.read);
  check('read-out names the COMMERCIAL base',
    near(num(panel.read, /([\d.]+)% of the commercial base/), loaded.liveComm),
    panel.read);
  // Downtown's base is billions, so fmtBig's B branch is the one in play; if the
  // unit ever changes this fails loudly rather than silently matching nothing.
  check('read-out gives the current value',
    near(num(panel.read, /\$([\d.]+)B assessed/), loaded.liveValue / 1e9),
    panel.read);
  // Frozen anchor, deliberately still an equality: 2016 is a settled historical
  // year, so this is what proves the archive half of the splice did not shift.
  check('read-out gives the peak', /peak share 5\.55% in 2016/.test(panel.read));
  check('note states the 2024 reason', /missing 2,448 accounts/.test(panel.note));
  check('note says the gap is not interpolated', /not interpolated/.test(panel.note));
  check('panel is in CHROME_IDS (label sweep dodges it)', panel.chromeHitsPanel);
  check('panel clears the title', !overlap(panel.rect, panel.title));
  check('panel clears the bottom-left cluster', !overlap(panel.rect, panel.botleft));
  check('panel clears the control column', !overlap(panel.rect, panel.controls));

  // ---- the clearance sweep, ACROSS STATES ---------------------------------
  // ⚠️ THE THREE CHECKS ABOVE RAN IN ONE STATE, AND THAT IS HOW THE BUG THEY
  // GUARD SHIPPED. `#temporal` was pinned at a constant `top: 210px` from a
  // sweep over the five views on their DEFAULT metric, where #title is
  // 176-179px tall. Money's cuts, the change lens, Development and Infill push
  // it to 256/368/462/499, and the panel buried the blurb in all five by up to
  // 289px while `panel clears the title` stayed green — it only ever ran on
  // money/value. The state list below is the fix for the CHECK; syncTemporalPos
  // is the fix for the panel.
  const STATES = [
    // ⚠️ Revenue first: this file opens every page on Value (see `open`), which
    // hides #revcut and shows #moneymode in its place — the two row-2s are
    // exclusive. These two states also show the REVENUE-MIX panel, not the
    // history, and it is ~15px shorter; the clearance has to hold for both
    // modes, which is exactly why they are in this sweep.
    ['money / residential',   ['#metric-row button[data-metric="revenue"]',
                               '#revcut button[data-revcut="res_revenue_per_acre"]']],
    ['money / non-residential', ['#revcut button[data-revcut="nonres_revenue_per_acre"]']],
    ['money / change lens',   ['#metric-row button[data-metric="value"]',
                               '#moneymode button[data-moneymode="change"]']],
    ['development',           ['#views button[data-view="development"]']],
    ['development / infill',  ['#devmode button[data-devmode="infill"]']],
    ['uses',                  ['#views button[data-view="uses"]']],
  ];
  for (const [label, clicks] of STATES) {
    for (const sel of clicks) {
      try { await page.click(sel, { timeout: 4000 }); await page.waitForTimeout(350); }
      catch (e) { check(`${label}: control ${sel} is clickable`, false, e.message.split('\n')[0]); }
    }
    await page.waitForTimeout(450);
    const s = await page.evaluate(() => {
      openTemporal('DOWNTOWN');
      const r = id => document.getElementById(id).getBoundingClientRect().toJSON();
      const body = document.getElementById('temporal-body');
      const p = r('temporal');
      const inBox = id => {
        const c = document.getElementById(id).getBoundingClientRect();
        return c.top >= p.top - 1 && c.bottom <= p.bottom + 1;
      };
      body.scrollTop = body.scrollHeight;      // worst case for the sticky bits
      const survives = inBox('temporal-close') && inBox('temporal-name');
      body.scrollTop = 0;
      return { panel: p, title: r('title'), botleft: r('botleft'), survives,
               open: document.getElementById('temporal').classList.contains('open') };
    });
    check(`${label}: panel opens`, s.open);
    // The load-bearing one: the blurb is the content that explains the map, and
    // burying it is the failure this sweep exists for.
    check(`${label}: panel clears the title blurb`, !overlap(s.panel, s.title),
      `title ${Math.round(s.title.bottom)} vs panel ${Math.round(s.panel.top)}`);
    check(`${label}: panel clears the bottom-left cluster`, !overlap(s.panel, s.botleft),
      `panel ${Math.round(s.panel.bottom)} vs botleft ${Math.round(s.botleft.top)}`);
    // ⚠️ Scrolling is how the panel yields, so the two things you need in order
    // to USE a scrolled panel — which hood it is, and how to close it — must
    // stay out of the scrolling region. Both left the box before #temporal-body
    // existed.
    check(`${label}: the name and the x survive a scroll`, s.survives);
  }
  // Back to the state the rest of the file assumes.
  await page.click('#views button[data-view="money"]');
  await page.waitForTimeout(350);
  await page.evaluate(() => applyMetric('value_per_acre'));
  await page.waitForTimeout(450);
  await page.evaluate(() => openTemporal('DOWNTOWN'));

  // ---- dismissal ----------------------------------------------------------
  await page.click('#temporal-close');
  check('the x closes it',
    !(await page.evaluate(() => document.getElementById('temporal').classList.contains('open'))));
  await page.evaluate(() => openTemporal('DOWNTOWN'));
  await page.keyboard.press('Escape');
  check('Escape closes it',
    !(await page.evaluate(() => document.getElementById('temporal').classList.contains('open'))));

  // A real map click, through deck's picking — not a direct call. Flatten the
  // camera first: at the default 52° pitch a prism is drawn well above its own
  // footprint, so the pixel over a hood's centroid can pick the hood BEHIND it.
  await page.click('#center2d');
  await page.waitForTimeout(1500);
  const clicked = await page.evaluate(async () => {
    // `empty` (panel open, nothing pinned) matters as much as `open` since the
    // readout-mode toggle landed: clicking through no longer CLOSES the panel,
    // it clears the pin and leaves the mode's prompt up. `mode` is read off the
    // button label because state.hoodMode is a plain property of a top-level
    // const, reachable here, but the label is what the user actually sees.
    const st = () => ({
      open: document.getElementById('temporal').classList.contains('open'),
      empty: document.getElementById('temporal').classList.contains('empty'),
      name: document.getElementById('temporal-name').textContent,
      mode: state.hoodMode,
    });
    // Pick a hood off the live viewport rather than guessing a pixel.
    const vp = overlay._deck.getViewports()[0];
    const named = n => state.data.features.find(
      f => f.properties.neighbourhood_name === n);
    const centroid = f => {
      const rings = f.geometry.type === 'MultiPolygon'
        ? f.geometry.coordinates.flat() : f.geometry.coordinates;
      const pts = rings[0];
      return [pts.reduce((a, p) => a + p[0], 0) / pts.length,
              pts.reduce((a, p) => a + p[1], 0) / pts.length];
    };
    // No layerIds filter: the MONEY view has no `hood-hover` layer at all — its
    // metric prisms are the pickable surface, and only the flat views add a
    // dedicated hover layer. Filtering on it picked nothing here.
    const hit = n => {
      const f = named(n);
      if (!f) return null;   // OLIVER is WÎHKWÊNTÔWIN from 2025 — try both
      const [x, y] = vp.project(centroid(f));
      const p = overlay._deck.pickObject({ x, y, radius: 2 });
      // A neighbouring polygon under the pixel is fine for this test; a pick
      // with no hood name at all is not.
      return p && p.object && p.object.properties &&
             p.object.properties.neighbourhood_name ? p : null;
    };
    const a = hit('DOWNTOWN'), b = hit('WÎHKWÊNTÔWIN') || hit('OLIVER');
    if (!a || !b || a.object.properties.neighbourhood_name ===
                    b.object.properties.neighbourhood_name) return { picked: false };
    temporalClick(a); const first = st();
    temporalClick(b); const second = st();
    temporalClick(b); const third = st();
    temporalClick({ object: null }); const fourth = st();
    return { picked: true, first, second, third, fourth,
             wantA: a.object.properties.neighbourhood_name,
             wantB: b.object.properties.neighbourhood_name };
  });
  check('deck picking reaches the hood layer', clicked.picked);
  if (clicked.picked) {
    check('a map click pins that hood, and enters panel mode',
      clicked.first.open && !clicked.first.empty &&
      clicked.first.name === clicked.wantA && clicked.first.mode === 'panel',
      `${clicked.first.name} / ${clicked.first.mode}`);
    check('clicking ANOTHER hood re-pins instead of closing',
      clicked.second.open && !clicked.second.empty &&
      clicked.second.name === clicked.wantB, clicked.second.name);
    // CONTRACT CHANGED with the readout-mode toggle (2026-07-30): a second click
    // still UNPINS, but it no longer closes the panel — the mode was not what was
    // dismissed, so the prompt stays up. Tested as "unpinned AND still in the
    // mode", which is a stricter claim than the old `!open`.
    check('a second click on the pinned hood unpins but keeps panel mode',
      clicked.third.open && clicked.third.empty && clicked.third.mode === 'panel',
      `open=${clicked.third.open} empty=${clicked.third.empty} mode=${clicked.third.mode}`);
    // Inertness stated as "nothing about the state moved", rather than the old
    // "stays closed" — same claim, and it no longer depends on which state the
    // preceding click happened to leave behind.
    check('an empty-map click is inert (no crash, state unchanged)',
      JSON.stringify(clicked.fourth) === JSON.stringify(clicked.third),
      JSON.stringify(clicked.fourth));
  }

  // ---- mobile: the bottom sheet -------------------------------------------
  const phone = await open(url, { width: 390, height: 844 });
  const m = await phone.evaluate(() => {
    openTemporal('DOWNTOWN');
    return {
      rect: document.getElementById('temporal').getBoundingClientRect().toJSON(),
      views: document.getElementById('views').getBoundingClientRect().toJSON(),
      controls: document.getElementById('controls').getBoundingClientRect().toJSON(),
      w: innerWidth, h: innerHeight,
    };
  });
  check('phone: panel is a bottom sheet', m.rect.bottom > m.h - 20 && m.rect.top > m.h / 2,
    `top=${m.rect.top.toFixed(0)} bottom=${m.rect.bottom.toFixed(0)} h=${m.h}`);
  check('phone: panel fits the viewport',
    m.rect.left >= 0 && m.rect.right <= m.w, `${m.rect.left}..${m.rect.right} of ${m.w}`);
  check('phone: panel does not cover the view buttons', !overlap(m.rect, m.views));
  check('phone: panel does not cover the control column', !overlap(m.rect, m.controls));
  await phone.close();

  // ---- public build: the lens is PRESENT (promoted 2026-07-31) ------------
  // These three checks previously asserted the lens was ABSENT here. The
  // promotion (DECISIONS.md 2026-07-31) inverted the contract, and this script
  // went red on exactly those three — the intended behaviour of a regression
  // net, so they are rewritten deliberately rather than deleted.
  //
  // Asserting "the panel opens" is STRICTER than the old "it cannot open":
  // a build that failed to load temporal.json at all would have satisfied the
  // old assertion, so the absence check could not distinguish "correctly
  // withheld" from "silently broken". The presence check can only pass if the
  // fetch, the join and the render all work.
  const pub = await open(url + (url.includes('?') ? '&' : '?') + 'build=public',
                         { width: 1440, height: 900 });
  const p = await pub.evaluate(() => {
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'DOWNTOWN');
    openTemporal('DOWNTOWN');
    return {
      series: temporalFor('DOWNTOWN'),
      tipHasSpark: /class="spark"/.test(tooltipFor({ object: f }).html),
      open: document.getElementById('temporal').classList.contains('open'),
      noteShown: document.getElementById('temporal-note').textContent,
    };
  });
  check('public build fetches the history', p.series !== null
        && Array.isArray(p.series.years) && p.series.years.length > 0);
  check('public build has the sparkline', p.tipHasSpark);
  check('public build can pin the panel', p.open);
  // The 2024 omission must be STATED publicly, not merely rendered as a hole —
  // a visible gap with no explanation reads as broken data (SPEC_temporal §0).
  check('public build states the 2024 omission', /2024 is omitted/.test(p.noteShown)
        && /not interpolated/.test(p.noteShown));
  await pub.close();

  await page.close();
  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

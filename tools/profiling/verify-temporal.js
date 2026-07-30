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
//   7. It is FULL-only: `?build=public` gets no sparkline and cannot pin.
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
  const open = async (u, vp) => {
    const page = await browser.newPage({ viewport: vp });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);
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
    return t && { years: t.years, first: t.share[0], last: t.share[t.share.length - 1] };
  });
  check('temporal.json loaded and decodes', !!loaded);
  check('2024 is absent from the year list',
    loaded && !loaded.years.includes(2024) && loaded.years.includes(2023) &&
    loaded.years.includes(2025), loaded ? `n=${loaded.years.length}` : '');
  // Anchors from the served file (S76 audit): Downtown 5.09% (2012) -> 3.30% (2025).
  check('Downtown decodes to the audited shares',
    loaded && Math.abs(loaded.first - 5.09) < 0.01 && Math.abs(loaded.last - 3.30) < 0.01,
    loaded ? `${loaded.first.toFixed(2)}% -> ${loaded.last.toFixed(2)}%` : '');

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
  check('tooltip row names the denominator + endpoints',
    /5\.09% → 3\.30% of city base, 2012–2025/.test(tip.html));
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
  check('both y endpoints are labelled (axis is not zero-based)',
    panel.svgText.includes('5.55%') && panel.svgText.includes('3.30%'),
    panel.svgText.join(' | '));
  check('x axis names the first and last year',
    panel.svgText.includes('2012') && panel.svgText.includes('2025'));
  check('read-out names the TOTAL base', /of Edmonton's total assessment base/.test(panel.read));
  check('read-out names the COMMERCIAL base', /9\.24% of the commercial base/.test(panel.read));
  check('read-out gives the current value', /\$7\.84B assessed/.test(panel.read));
  check('read-out gives the peak', /peak share 5\.55% in 2016/.test(panel.read));
  check('note states the 2024 reason', /missing 2,448 accounts/.test(panel.note));
  check('note says the gap is not interpolated', /not interpolated/.test(panel.note));
  check('panel is in CHROME_IDS (label sweep dodges it)', panel.chromeHitsPanel);
  check('panel clears the title', !overlap(panel.rect, panel.title));
  check('panel clears the bottom-left cluster', !overlap(panel.rect, panel.botleft));
  check('panel clears the control column', !overlap(panel.rect, panel.controls));

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

  // ---- public build: the lens is absent -----------------------------------
  const pub = await open(url + (url.includes('?') ? '&' : '?') + 'build=public',
                         { width: 1440, height: 900 });
  const p = await pub.evaluate(() => {
    const f = state.data.features.find(
      x => x.properties.neighbourhood_name === 'DOWNTOWN');
    openTemporal('DOWNTOWN');   // must be a no-op, not a crash
    return {
      series: temporalFor('DOWNTOWN'),
      tipHasSpark: /class="spark"/.test(tooltipFor({ object: f }).html),
      open: document.getElementById('temporal').classList.contains('open'),
    };
  });
  check('public build never fetches the history', p.series === null);
  check('public build has no sparkline', !p.tipHasSpark);
  check('public build cannot pin the panel', !p.open);
  await pub.close();

  await page.close();
  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

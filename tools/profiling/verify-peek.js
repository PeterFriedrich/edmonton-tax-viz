// Verify the touch-only peek card (Peter, 2026-07-31: "i actually want ... the
// panel on mobile to be harder to activate ... on mobile, you only [have] the
// choice of tapping. also the x on the panel needs to be twice as big").
//
// ⚠️ THIS IS THE FIRST SCRIPT IN THE SUITE THAT DRIVES A REAL POINTER AT THE
// MAP. Every other verify-*.js calls temporalClick()/openTemporal() directly in
// JS, which is why the single-tap-opens-everything behaviour survived unnoticed
// through the whole temporal lens build. Use page.touchscreen.tap / page.mouse
// here, never the JS entry points -- the gate being tested lives between the
// gesture and those functions, so calling them directly would bypass it.
//
// The load-bearing claims:
//   1. DESKTOP IS UNCHANGED. One mouse click still pins; the card never shows.
//   2. On touch, the first tap PEEKS -- the panel does not open.
//   3. The card commits: tapping it opens the panel on the peeked hood.
//   4. Tapping a different hood re-peeks; re-tapping the SAME hood is a no-op
//      and a tap on empty map dismisses. The no-op matters: a touch tap can
//      deliver temporalClick twice (touch event + compatibility mouse event),
//      measured on 2026-07-31, so any toggle here would fire at random.
//   5. The gate is on the way IN only: with panel mode already on, a tap pins
//      directly, so pin-then-browse still costs one tap per hood.
//   6. The card's headline is the SAME string panel mode reduces the hover to,
//      so the two cannot drift apart.
//   7. The close button clears the 44px touch minimum on touch, and is NOT
//      enlarged for a mouse -- and the hood name never sits under it.
//   node verify-peek.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let fail = 0;
const check = (name, cond, extra) => {
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
  if (!cond) fail++;
};

const boot = async (browser, opts) => {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);
  // Flatten: at the default 52 deg pitch a prism paints well above its own
  // footprint, so a picked pixel can belong to the hood BEHIND it (quirk x).
  await page.click('#center2d');
  await page.waitForTimeout(2500);   // the flatten is an eased camera move
  return { ctx, page };
};

// A pixel that picks a hood WITH history and is not under chrome. Returned as a
// list so the test can peek one hood and then re-peek a different one.
//
// ⚠️ The pick must be STABLE across a few pixels, not merely non-null. Deck's
// click-time picking rounds device pixels slightly differently from a manual
// pickObject, so a pixel sitting on a polygon EDGE can report hood A here and
// deliver hood B (or nothing) to the real click -- which then looks exactly
// like the gesture under test being broken. Requiring the same hood across an
// 8px ring in eight directions puts the target well inside a polygon.
// Hoods with no history are skipped because temporalClick correctly ignores
// them, as are set-aside hoods, which have no prism to hit in Money (quirk w).
const targets = (page, n) => page.evaluate((n) => {
  const at = (x, y) => {
    const o = overlay._deck.pickObject({ x, y, radius: 0 });
    return (o && o.object && o.object.properties) || null;
  };
  const out = [], seen = new Set();
  const H = innerHeight, W = innerWidth;
  // Start from the middle of the map, not its left edge: the west edge at this
  // zoom is the river valley, where the hoods are narrow slivers and no pixel is
  // far enough from a boundary to tap reliably.
  for (let y = Math.round(H * 0.55); y > H * 0.25 && out.length < n; y -= 9) {
    for (let x = Math.round(W * 0.30); x < W * 0.80 && out.length < n; x += 9) {
      const top = document.elementFromPoint(x, y);
      if (!top || top.tagName !== 'CANVAS') continue;
      const p = at(x, y);
      const nm = p && p.neighbourhood_name;
      if (!nm || seen.has(nm) || p.is_set_aside || !temporalFor(nm)) continue;
      const solid = [[8, 0], [-8, 0], [0, 8], [0, -8],
                     [6, 6], [-6, 6], [6, -6], [-6, -6]].every(([dx, dy]) => {
        const q = at(x + dx, y + dy);
        return q && q.neighbourhood_name === nm;
      });
      if (!solid) continue;
      seen.add(nm); out.push({ x, y, name: nm });
    }
  }
  return out;
}, n);

// ⚠️ EVERY map gesture must go through this. Deck renders its picking buffer on
// demand, and under headless SwiftShader that first pass after an idle moment is
// too slow for the click's synchronous pick, so taps land on nothing at random:
// measured 2026-07-31 as 2 of 4 taps registering bare, versus 4 of 4 when a
// pickObject is issued first. The explicit pick just warms that buffer. This is
// a software-GL artifact of the harness (same family as quirks x and y), NOT
// something a real device with hardware GL does -- do not "fix" the app for it.
// The buffer can also go cold again in the round-trip between warming it and
// delivering the gesture, which is why a gesture that should change something
// and provably did not is re-sent (seen under the 3-up runner, where the
// contending SwiftShader contexts make that pass slower still). Bounded, and it
// cannot manufacture a pass: if the gesture never registers the check still
// fails. `expectChange: false` is for the genuinely inert ones -- retrying those
// would just cost three rounds of nothing.
const gesture = async (page, x, y, touch, expectChange = true) => {
  const st = () => page.evaluate(() => `${peekHood}|${pinnedHood}|${state.hoodMode}`);
  for (let i = 0; i < 3; i++) {
    const before = await st();
    await page.evaluate(([x, y]) => overlay._deck.pickObject({ x, y, radius: 0 }), [x, y]);
    if (touch) await page.touchscreen.tap(x, y); else await page.mouse.click(x, y);
    await page.waitForTimeout(1400);
    if (!expectChange || await st() !== before) return;
  }
};

const snap = page => page.evaluate(() => {
  const pk = document.getElementById('peek'), tp = document.getElementById('temporal');
  return {
    peekShown: pk.offsetParent !== null && pk.classList.contains('open'),
    peekName: document.getElementById('peek-name').textContent,
    peekRead: document.getElementById('peek-read').innerHTML,
    peekHood: typeof peekHood !== 'undefined' ? peekHood : '(n/a)',
    panelOpen: tp.classList.contains('open') && !tp.classList.contains('empty'),
    pinned: pinnedHood, mode: state.hoodMode,
  };
});

// ⚠️ The name is a block div, so its RECT always spans the panel and always
// "overlaps" the button. What actually keeps the text clear is its padding, so
// that is what gets compared against the button's width.
const closeBox = page => page.evaluate(() => {
  const b = document.getElementById('temporal-close');
  const r = b.getBoundingClientRect();
  return { w: +r.width.toFixed(1), h: +r.height.toFixed(1),
           namePad: parseFloat(getComputedStyle(
             document.getElementById('temporal-name')).paddingRight) };
});

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });

  // ---------- DESKTOP: the change must be invisible here ----------
  {
    const { ctx, page } = await boot(browser, { viewport: { width: 1440, height: 900 } });
    const t = await targets(page, 1);
    check('desktop: found a pickable hood with history', t.length === 1, JSON.stringify(t[0]));
    if (t.length) {
      await gesture(page, t[0].x, t[0].y, false);
      const s = await snap(page);
      check('desktop: ONE click still pins (no card stage)',
        s.panelOpen && s.pinned === t[0].name, `pinned=${s.pinned} mode=${s.mode}`);
      check('desktop: the peek card never displays', !s.peekShown);
    }
    const b = await closeBox(page);
    check('desktop: close button NOT enlarged for a mouse', b.w < 30 && b.h < 30,
      `${b.w}x${b.h}`);
    await ctx.close();
  }

  // ---------- TOUCH ----------
  {
    const { ctx, page } = await boot(browser, {
      viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true,
      deviceScaleFactor: 3 });

    const hoverNone = await page.evaluate(() => matchMedia('(hover: none)').matches);
    check('touch: (hover: none) is the active seam', hoverNone);

    const t = await targets(page, 2);
    check('touch: found two distinct pickable hoods', t.length === 2,
      t.map(x => x.name).join(' / '));
    if (t.length < 2) { await ctx.close(); await browser.close(); process.exit(fail ? 1 : 0); }

    // The city fills the middle of the map at this zoom, so an unpicked pixel
    // only exists out near the corners -- scan the whole canvas, not the centre.
    const empty = await page.evaluate(() => {
      for (let y = innerHeight - 90; y > 200; y -= 7) {
        for (let x = 4; x < innerWidth - 4; x += 7) {
          const top = document.elementFromPoint(x, y);
          if (!top || top.tagName !== 'CANVAS') continue;
          if (!overlay._deck.pickObject({ x, y, radius: 6 })) return { x, y };
        }
      }
      return null;
    });
    check('touch: found an empty-map pixel', !!empty, JSON.stringify(empty));

    // ⚠️ WARM-UP, and it is load-bearing. The target scan above runs thousands
    // of pickObject passes, and the first real tap after that burst is
    // swallowed -- measured repeatedly on 2026-07-31, and it makes every
    // assertion below fail as though the gesture were broken. Spend it on the
    // empty pixel, where the handler's only effect is a closePeek() no-op.
    if (empty) await gesture(page, empty.x, empty.y, true, false);

    await gesture(page, t[0].x, t[0].y, true);
    let s = await snap(page);
    check('touch: first tap PEEKS, panel stays shut',
      s.peekShown && !s.panelOpen && s.pinned === null,
      `peek=${s.peekHood} panel=${s.panelOpen}`);
    check('touch: the card names the tapped hood', s.peekName === t[0].name,
      `"${s.peekName}" vs "${t[0].name}"`);
    check('touch: mode is still popup after a peek', s.mode === 'popup', s.mode);

    // The card's headline must be the same string panel mode reduces the hover
    // to -- one definition of "this hood's headline".
    const reduced = await page.evaluate((n) => {
      const f = state.data.features.find(x => x.properties.neighbourhood_name === n);
      return primaryRow(f.properties);
    }, t[0].name);
    check('touch: card headline == panel-mode reduced hover', s.peekRead === reduced,
      `card="${s.peekRead}"`);

    // Tapping a DIFFERENT hood re-peeks rather than committing.
    await gesture(page, t[1].x, t[1].y, true);
    s = await snap(page);
    check('touch: tapping another hood re-peeks, still no panel',
      s.peekShown && !s.panelOpen && s.peekName === t[1].name,
      `peek=${s.peekName} panel=${s.panelOpen}`);

    // Re-tapping the SAME hood must be inert -- the doubled touch event makes
    // any toggle here non-deterministic.
    await gesture(page, t[1].x, t[1].y, true, false);
    s = await snap(page);
    check('touch: re-tapping the peeked hood is a NO-OP (doubled-event safe)',
      s.peekShown && s.peekName === t[1].name && !s.panelOpen,
      `peek=${s.peekName} panel=${s.panelOpen}`);

    // A tap on empty map dismisses the card (the panel's opposite rule).
    if (empty) {
      await gesture(page, empty.x, empty.y, true);
      s = await snap(page);
      check('touch: a tap on empty map dismisses the card',
        !s.peekShown && s.peekHood === null, `peek=${s.peekHood}`);
    }

    // Peek, then commit by tapping the CARD.
    await gesture(page, t[0].x, t[0].y, true);
    const cardBox = await page.evaluate(() => {
      const r = document.getElementById('peek').getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2,
               w: +r.width.toFixed(1), h: +r.height.toFixed(1) };
    });
    check('touch: the card is a large target', cardBox.h >= 44 && cardBox.w >= 200,
      `${cardBox.w}x${cardBox.h}`);
    await page.touchscreen.tap(cardBox.x, cardBox.y);
    await page.waitForTimeout(1200);
    s = await snap(page);
    check('touch: tapping the card OPENS the panel on that hood',
      s.panelOpen && s.pinned === t[0].name, `pinned=${s.pinned} mode=${s.mode}`);
    check('touch: the card is gone once the panel is up', !s.peekShown);

    // The gate is on the way IN only.
    await gesture(page, t[1].x, t[1].y, true);
    s = await snap(page);
    check('touch: with the panel open, a tap pins DIRECTLY (browse costs 1 tap)',
      s.panelOpen && s.pinned === t[1].name && !s.peekShown,
      `pinned=${s.pinned} peek=${s.peekShown}`);

    // The x: twice the size, and clearing the 44px minimum.
    const b = await closeBox(page);
    check('touch: close button clears the 44px minimum', b.w >= 44 && b.h >= 44,
      `${b.w}x${b.h}`);
    check('touch: the hood name is padded clear of the enlarged button',
      b.namePad >= b.w, `padding-right ${b.namePad} vs button ${b.w}`);

    // And it actually dismisses when tapped at its centre.
    const cb = await page.evaluate(() => {
      const r = document.getElementById('temporal-close').getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    });
    await page.touchscreen.tap(cb.x, cb.y);
    await page.waitForTimeout(1000);
    s = await snap(page);
    check('touch: tapping the x un-pins', s.pinned === null, `pinned=${s.pinned}`);

    await ctx.close();
  }

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();

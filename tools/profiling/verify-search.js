// Verify the neighbourhood search (2026-10-01: "a neighborhood search feature.
// Especially usable on mobile"). Driven by REAL gestures — mouse, keyboard and
// touchscreen.tap — never by calling pickSearch() in JS, because what is under
// test is the path from the gesture to it (the verify-peek lesson).
//
// The load-bearing claims:
//   1. Matching: a query finds by name start, by a later word ("brooks" →
//      TWIN BROOKS), ignoring case, apostrophes and hyphens; no match SAYS so.
//   2. A pick reads like a click on desktop (the panel pins on that hood) and
//      like a tap on a phone (the peek card, NOT the panel), and the camera
//      moves to it.
//   3. The picked hood is OUTLINED, the outline follows the readout (closing
//      the panel removes it), and a pick that opens no readout is still
//      outlined (searchHood).
//   4. Re-picking the pinned hood does not unpin it (a click on it would).
//   5. Keyboard: "/" opens, arrows move, Enter picks, Escape closes search
//      BEFORE it touches the panel.
//   6. Phone: the field's text is >= 16px (iOS zooms the page otherwise), the
//      keyboard is dropped after a pick (input blurred), the magnifier clears
//      the title in EVERY view, and nothing open runs off-screen.
//   node verify-search.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let fail = 0, ran = 0;
const check = (name, cond, extra) => {
  ran++;
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
  if (!cond) fail++;
};

const boot = async (browser, opts) => {
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForFunction(() => getComputedStyle(document.getElementById('search')).display !== 'none',
                             null, { timeout: 30000 });
  await page.waitForTimeout(3000);
  return { ctx, page };
};

const outlined = page => page.evaluate(() => {
  const l = (overlay._deck.props.layers || []).find(x => x && x.id === 'hood-selected');
  return l ? l.props.data[0].properties.neighbourhood_name : null;
});
const listed = page => page.$$eval('#search-list li', els => els.map(e => e.textContent));
const state_ = page => page.evaluate(() => ({
  pinned: pinnedHood, peek: peekHood, search: searchHood,
  open: document.getElementById('search').classList.contains('open'),
  focused: document.activeElement && document.activeElement.id,
  center: map.getCenter().toArray(), zoom: map.getZoom(),
  panelOpen: document.getElementById('temporal').classList.contains('open'),
  peekOpen: document.getElementById('peek').classList.contains('open'),
}));
// Is the camera centre inside the hood's bounding box?
const centredOn = (page, name) => page.evaluate(name => {
  const f = state.data.features.find(x => x.properties.neighbourhood_name === name);
  const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const p of polys) for (const [x, y] of p[0]) {
    x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);
  }
  const [cx, cy] = map.getCenter().toArray();
  return cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1;
}, name);
const overlap = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
const rect = (page, sel) => page.$eval(sel, e => { const r = e.getBoundingClientRect();
  return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, w: r.width, h: r.height }; });

(async () => {
  // ---------------------------------------------------------------- desktop
  {
    const browser = await chromium.launch();
    const { page } = await boot(browser, { viewport: { width: 1440, height: 900 } });

    check('desktop: magnifier clears the title',
          !overlap(await rect(page, '#search-btn'), await rect(page, '#title')));

    await page.click('#search-btn');
    let s = await state_(page);
    check('desktop: the magnifier opens the field and focuses it', s.open && s.focused === 'search-input');

    await page.keyboard.type('BROOKS');
    let L = await listed(page);
    check('match: a later WORD matches ("BROOKS" → TWIN BROOKS)', L.includes('TWIN BROOKS'), JSON.stringify(L));
    await page.fill('#search-input', '');
    await page.keyboard.type('rivers edge');
    L = await listed(page);
    check('match: apostrophe dropped ("rivers edge" → RIVER\'S EDGE)', L[0] === "RIVER'S EDGE", JSON.stringify(L));
    await page.fill('#search-input', '');
    await page.keyboard.type('hollick kenyon');
    L = await listed(page);
    check('match: hyphen as space ("hollick kenyon" → HOLLICK-KENYON)', L[0] === 'HOLLICK-KENYON', JSON.stringify(L));
    await page.fill('#search-input', '');
    await page.keyboard.type('zzqx');
    L = await listed(page);
    check('match: no match says so', L.length === 1 && /No neighbourhood/.test(L[0]), JSON.stringify(L));
    await page.fill('#search-input', '');
    await page.keyboard.type('a');
    L = await listed(page);
    check('match: capped at 8 rows, name-start ranked first', L.length === 8 && L.every(n => n.startsWith('A')),
          JSON.stringify(L));

    // Arrows then Enter: the SECOND row, not the first.
    await page.fill('#search-input', '');
    await page.keyboard.type('glen');
    L = await listed(page);
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    s = await state_(page);
    check('keyboard: ArrowDown + Enter picks the second row', s.pinned === L[1], `${s.pinned} vs ${JSON.stringify(L)}`);
    check('desktop pick: the panel pins (as a click does), no peek card', s.panelOpen && !s.peekOpen && !s.peek);
    check('desktop pick: search closes', !s.open);
    check('desktop pick: the camera centres on the hood', await centredOn(page, L[1]));
    check('outline: the picked hood is outlined', (await outlined(page)) === L[1], await outlined(page));
    const picked = L[1];

    // Re-pick the pinned hood: must stay pinned (a click on it would unpin).
    await page.keyboard.press('/');
    s = await state_(page);
    check('"/" opens search', s.open && s.focused === 'search-input');
    await page.keyboard.type(picked);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1200);
    s = await state_(page);
    check('re-picking the pinned hood keeps it pinned', s.pinned === picked && s.panelOpen, s.pinned);

    // Escape: search first, panel untouched.
    await page.keyboard.press('/');
    await page.keyboard.press('Escape');
    s = await state_(page);
    check('Escape closes search and leaves the panel', !s.open && s.pinned === picked && s.panelOpen);

    // Click-outside closes.
    await page.click('#search-btn');
    await page.mouse.click(720, 880);
    s = await state_(page);
    check('a click outside closes search', !s.open);

    // A pick that opens NO readout: the outline alone marks it. Every hood has
    // a history row today, so force the state a stale or partial deploy would
    // give — the Value map with the history file missing.
    await page.click('#metric-row [data-metric="value"]');
    await page.waitForTimeout(1000);
    await page.evaluate(() => { closeTemporal(); temporalData = null; });
    await page.click('#search-btn');
    await page.keyboard.type('TWIN BROOKS');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    s = await state_(page);
    const o = await outlined(page);
    check('no readout to open: the pick is still outlined (searchHood)',
          s.search === 'TWIN BROOKS' && !s.pinned && o === 'TWIN BROOKS',
          JSON.stringify({ search: s.search, pinned: s.pinned, outline: o }));
    await page.keyboard.press('Escape');
    check('Escape clears a search-only outline', (await outlined(page)) === null);
    await Promise.race([browser.close(), new Promise(r => setTimeout(r, 3000))]);
  }

  // ------------------------------------------------------------------ phone
  for (const width of [390, 360]) {
    const browser = await chromium.launch();
    const { page } = await boot(browser, {
      viewport: { width, height: 800 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2,
    });
    const tag = `phone ${width}`;

    // The magnifier must clear the title in every view: titles differ per view.
    const views = await page.$$eval('#views button', bs =>
      bs.filter(b => b.offsetParent !== null).map(b => b.dataset.view));
    const clashes = [];
    for (const id of views) {
      await page.evaluate(v => document.querySelector(`#views [data-view="${v}"]`).click(), id);
      await page.waitForTimeout(600);
      const t = await rect(page, '#title-h'), b = await rect(page, '#search-btn');
      if (overlap(t, b) || t.right > b.left) clashes.push(`${id}: title right ${Math.round(t.right)} vs btn ${Math.round(b.left)}`);
      // The narrower title may wrap: it should still end above the controls.
      // ⚠️ WARN, not FAIL: this box has no web fonts and measures text 15-20%
      // wide, so it over-wraps (Lab at 360 reads 3 lines here). Three views sat
      // at exactly the 58px limit here before search existed. A real phone is
      // the oracle; MOBILE_USABILITY §2b.
      const c = await rect(page, '#controls');
      if (t.bottom > c.top) console.log(`WARN  ${tag}: ${id} title bottom ${Math.round(t.bottom)} > controls top ${Math.round(c.top)} (font-dependent)`);
    }
    check(`${tag}: magnifier clears the title in all ${views.length} views`, !clashes.length, clashes.join('; '));
    await page.evaluate(v => document.querySelector(`#views [data-view="${v}"]`).click(), views[0]);
    await page.waitForTimeout(800);

    // Expanded blurb card: full width again, so the heading TEXT (not its
    // padded box) must clear the magnifier, and the magnifier must stay on top.
    await page.tap('#title-h');
    await page.waitForTimeout(300);
    const exp = await page.evaluate(() => {
      const h = document.getElementById('title-h'), b = document.getElementById('search-btn');
      const rg = document.createRange(); rg.selectNodeContents(h);
      const textRight = Math.max(...[...rg.getClientRects()].map(r => r.right));
      const br = b.getBoundingClientRect();
      const top = document.elementFromPoint(br.left + br.width / 2, br.top + br.height / 2);
      return { expanded: document.getElementById('title').classList.contains('expanded'),
               textRight: Math.round(textRight), btnLeft: Math.round(br.left), onTop: b.contains(top) };
    });
    check(`${tag}: expanded card — heading clears the magnifier, magnifier on top`,
          exp.expanded && exp.textRight < exp.btnLeft && exp.onTop, JSON.stringify(exp));
    await page.tap('#title-h');
    await page.waitForTimeout(300);

    const btn = await rect(page, '#search-btn');
    check(`${tag}: magnifier is a 40px target`, btn.w >= 40 && btn.h >= 40, `${btn.w}x${btn.h}`);

    await page.tap('#search-btn');
    let s = await state_(page);
    check(`${tag}: a tap opens and focuses the field`, s.open && s.focused === 'search-input');
    const fs = await page.$eval('#search-input', e => parseFloat(getComputedStyle(e).fontSize));
    check(`${tag}: field text >= 16px (no iOS zoom on focus)`, fs >= 16, `${fs}px`);

    await page.keyboard.type('twin br');
    const L = await listed(page);
    check(`${tag}: results list`, L[0] === 'TWIN BROOKS', JSON.stringify(L));
    const box = await rect(page, '#search-box'), list = await rect(page, '#search-list');
    check(`${tag}: open field and list stay on screen`,
          box.left >= 0 && box.right <= width && list.right <= width && list.left >= 0,
          JSON.stringify({ box, list }));
    check(`${tag}: list sits in the top half (above a keyboard)`, list.bottom <= 800 * 0.6, `bottom ${list.bottom}`);

    await page.tap('#search-list li[role=option]');
    await page.waitForTimeout(1500);
    s = await state_(page);
    check(`${tag}: pick shows the peek card, not the panel`, s.peek === 'TWIN BROOKS' && s.peekOpen && !s.panelOpen,
          JSON.stringify({ peek: s.peek, panel: s.panelOpen }));
    check(`${tag}: keyboard dropped (field blurred) and search closed`, !s.open && s.focused !== 'search-input');
    check(`${tag}: camera centres on the hood`, await centredOn(page, 'TWIN BROOKS'));
    check(`${tag}: outlined`, (await outlined(page)) === 'TWIN BROOKS');
    check(`${tag}: the card names the hood`,
          (await page.$eval('#peek-name', e => e.textContent)) === 'TWIN BROOKS');

    // Committing the card opens the panel on the same hood; the outline stays.
    await page.tap('#peek');
    await page.waitForTimeout(800);
    s = await state_(page);
    check(`${tag}: card commit pins the picked hood, outline kept`,
          s.pinned === 'TWIN BROOKS' && s.panelOpen && (await outlined(page)) === 'TWIN BROOKS');
    // With BOTH label classes off: the reference layer is on by default, so
    // the old label-gated rebuild would still fire and hide a missing one.
    await page.evaluate(() => ['reference-on', 'labels-on'].forEach(id => {
      const c = document.getElementById(id); if (c.checked) c.click(); }));
    await page.waitForTimeout(400);
    check(`${tag}: label pool empty for the next check`, await page.evaluate(() => labelPool().length === 0));
    await page.tap('#temporal-close');
    await page.waitForTimeout(400);
    check(`${tag}: closing the panel removes the outline`, (await outlined(page)) === null, await outlined(page));
    await Promise.race([browser.close(), new Promise(r => setTimeout(r, 3000))]);
  }

  console.log(`\n${ran - fail}/${ran} passed`);
  process.exit(fail ? 1 : 0);
})();

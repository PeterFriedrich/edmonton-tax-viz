// Verify the how-to-read guide (Peter, 2026-10-08: "a question mark near the
// search button, so people can bring it up again ... a big X to exit at any
// time"). Real gestures throughout: mouse clicks on desktop, touchscreen taps
// on a phone.
//
// The load-bearing claims:
//   1. A first visit gets the full card once the loading overlay lifts; a
//      reload does not; the ? brings it back, and the x or Escape closes it.
//   2. A shared link (a state hash) gets the one-line offer instead, which
//      names the x as the way out and expands to the full card on request.
//   3. Blocked storage still shows the card and throws nothing.
//   4. Under automation the card never opens by itself — every other verify
//      script depends on that. So every check of the auto path below first
//      unsets navigator.webdriver, or it would test the gate, not the card.
//   5. Small against a desktop screen; on a phone the x is a 44px target, the
//      card stays on-screen, and the ? clears the title in every view.
//   node verify-guide.js <url>   (the PUBLIC build: the card lists its four views)
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let fail = 0, ran = 0;
const check = (name, cond, extra) => {
  ran++;
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
  if (!cond) fail++;
};

const AS_A_PERSON = () => Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false });
const NO_STORAGE = () => {
  const boom = () => { throw new DOMException('blocked', 'SecurityError'); };
  Storage.prototype.getItem = boom;
  Storage.prototype.setItem = boom;
};

const boot = async (ctx, target = url) => {
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => { errors.push(e.message); console.log('PAGE EXCEPTION:', e.message); });
  await page.goto(target, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForFunction(() => getComputedStyle(document.getElementById('guide-btn')).display !== 'none',
                             null, { timeout: 30000 });
  await page.waitForFunction(() => document.getElementById('loading').hidden, null, { timeout: 30000 });
  await page.waitForTimeout(500);
  return { page, errors };
};

const guide = page => page.evaluate(() => {
  const g = document.getElementById('guide');
  const r = g.getBoundingClientRect();
  return { open: g.classList.contains('open'), ask: g.classList.contains('ask'),
           expanded: document.getElementById('guide-btn').getAttribute('aria-expanded'),
           text: g.innerText, w: r.width, h: r.height,
           left: r.left, right: r.right, top: r.top, bottom: r.bottom,
           vw: innerWidth, vh: innerHeight };
});
const overlap = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
const rect = (page, sel) => page.$eval(sel, e => { const r = e.getBoundingClientRect();
  return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, w: r.width, h: r.height }; });

(async () => {
  const browser = await chromium.launch();
  const desk = { viewport: { width: 1280, height: 800 } };

  // ------------------------------------------------------ automation gate
  {
    const ctx = await browser.newContext(desk);
    const { page } = await boot(ctx);
    check('automation: no card opens by itself', !(await guide(page)).open);
    check('desktop: ? clears the magnifier and the title',
          !overlap(await rect(page, '#guide-btn'), await rect(page, '#search-btn')) &&
          !overlap(await rect(page, '#guide-btn'), await rect(page, '#title')));
    await ctx.close();
  }

  // ---------------------------------------------------- first visit, desktop
  {
    const ctx = await browser.newContext(desk);
    await ctx.addInitScript(AS_A_PERSON);
    let { page, errors } = await boot(ctx);
    let g = await guide(page);
    check('first visit: the full card opens by itself', g.open && !g.ask && g.expanded === 'true');
    check('card names the thesis, the views and both camera presets',
          /pays the City in property tax, per acre/.test(g.text) &&
          /Money · Development · Services · Ratio/.test(g.text) &&
          /Center 2D/.test(g.text) && /Center 3D/.test(g.text));
    const bold = await page.$$eval('#guide-body b', bs => bs.map(b => b.textContent));
    check('Center 2D and Center 3D are bold', bold.includes('Center 2D') && bold.includes('Center 3D'), bold.join(' | '));
    // The card names buttons; a rename that leaves the card behind goes red here.
    const live = await page.evaluate(() => {
      const txt = sel => [...document.querySelectorAll(sel)]
        .filter(b => b.offsetParent !== null).map(b => b.textContent.trim());
      return { views: txt('#views button').join(' · '), metric: txt('#metric-row button').join(' | '),
               c2: document.getElementById('center2d').textContent.trim(),
               c3: document.getElementById('recenter').textContent.trim() };
    });
    check('the names in the card are the buttons on screen',
          bold.includes(live.views) && bold.includes(live.metric) &&
          bold.includes(live.c2) && bold.includes(live.c3), JSON.stringify(live));
    check('desktop: says "click", not "tap"', /Click a neighbourhood/.test(g.text));
    check('desktop: card is small against the screen',
          g.w <= 340 && g.w * g.h < 0.25 * g.vw * g.vh, `${Math.round(g.w)}x${Math.round(g.h)}`);
    const x = await rect(page, '#guide-close');
    check('desktop: the x is at least 36px', x.w >= 36 && x.h >= 36, `${x.w}x${x.h}`);
    await page.mouse.click(x.left + x.w / 2, x.top + x.h / 2);
    await page.waitForTimeout(200);
    g = await guide(page);
    check('the x closes it', !g.open && g.expanded === 'false');

    await page.reload({ waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.getElementById('loading').hidden, null, { timeout: 30000 });
    await page.waitForTimeout(500);
    check('a reload does not show it again', !(await guide(page)).open);

    await page.click('#guide-btn');
    await page.waitForTimeout(200);
    g = await guide(page);
    check('the ? reopens the full card', g.open && !g.ask);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(200);
    check('Escape closes it', !(await guide(page)).open);
    await page.click('#guide-btn');
    await page.click('#guide-btn');
    await page.waitForTimeout(200);
    check('a second click on the ? closes it', !(await guide(page)).open);

    // A click on the map behind an open card must not dismiss it.
    await page.click('#guide-btn');
    const onMap = await page.evaluate(() => document.elementFromPoint(950, 450).tagName === 'CANVAS');
    check('the probe point is bare map', onMap);
    await page.mouse.click(950, 450);
    await page.waitForTimeout(300);
    check('a click on the map leaves it open', (await guide(page)).open);
    await page.keyboard.press('Escape');

    // An open search hides the ?.
    await page.click('#search-btn');
    await page.waitForTimeout(200);
    check('an open search hides the ?',
          await page.$eval('#guide-btn', e => getComputedStyle(e).visibility === 'hidden'));
    await page.keyboard.press('Escape');
    check('no page errors (desktop)', !errors.length, errors.join('; '));
    await ctx.close();
  }

  // ------------------------------------------------------------ shared link
  {
    const ctx = await browser.newContext(desk);
    await ctx.addInitScript(AS_A_PERSON);
    const { page } = await boot(ctx, url.replace(/#.*$/, '') + '#view=development');
    let g = await guide(page);
    check('shared link: the one-line offer, not the full card', g.open && g.ask, JSON.stringify(g.text));
    check('the offer names the x as the way out', /click ✕ to go straight to the map/.test(g.text));
    check('the link\'s view was still applied', await page.evaluate(() => state.view === 'development'));
    await page.click('#guide-show');
    await page.waitForTimeout(200);
    g = await guide(page);
    check('"Show the guide" expands to the full card', g.open && !g.ask && /How to read this map/.test(g.text));
    await page.click('#guide-close');
    check('the x closes it', !(await guide(page)).open);
    await ctx.close();
  }

  // --------------------------------------------------------- blocked storage
  {
    const ctx = await browser.newContext(desk);
    await ctx.addInitScript(AS_A_PERSON);
    await ctx.addInitScript(NO_STORAGE);
    const { page, errors } = await boot(ctx);
    check('blocked storage: the card still shows', (await guide(page)).open);
    check('blocked storage: no page errors', !errors.length, errors.join('; '));
    await ctx.close();
  }
  await browser.close();

  // ------------------------------------------------------------------ phone
  for (const width of [390, 360]) {
    const b = await chromium.launch();
    const ctx = await b.newContext({
      viewport: { width, height: 800 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2,
    });
    await ctx.addInitScript(AS_A_PERSON);
    const { page, errors } = await boot(ctx);
    const tag = `phone ${width}`;
    let g = await guide(page);
    check(`${tag}: the card opens by itself and says "tap"`, g.open && /Tap a neighbourhood/.test(g.text));
    check(`${tag}: the card is fully on-screen`,
          g.left >= 0 && g.top >= 0 && g.right <= g.vw && g.bottom <= g.vh,
          `${Math.round(g.left)},${Math.round(g.top)} → ${Math.round(g.right)},${Math.round(g.bottom)}`);
    const x = await rect(page, '#guide-close');
    check(`${tag}: the x is a 44px target`, x.w >= 44 && x.h >= 44, `${x.w}x${x.h}`);
    await page.tap('#guide-close');
    await page.waitForTimeout(200);
    check(`${tag}: a tap on the x closes it`, !(await guide(page)).open);

    const q = await rect(page, '#guide-btn'), s = await rect(page, '#search-btn');
    check(`${tag}: ? is a 40px target beside the magnifier, not on it`,
          q.w >= 40 && q.h >= 40 && !overlap(q, s) && q.right <= s.left && Math.abs(q.top - s.top) < 1,
          `? ${Math.round(q.left)}-${Math.round(q.right)}, magnifier ${Math.round(s.left)}`);

    const views = await page.$$eval('#views button', bs =>
      bs.filter(b => b.offsetParent !== null).map(b => b.dataset.view));
    const clashes = [];
    for (const id of views) {
      await page.evaluate(v => document.querySelector(`#views [data-view="${v}"]`).click(), id);
      await page.waitForTimeout(600);
      const t = await rect(page, '#title-h'), qq = await rect(page, '#guide-btn');
      if (overlap(t, qq) || t.right > qq.left) clashes.push(`${id}: title right ${Math.round(t.right)} vs ? ${Math.round(qq.left)}`);
      // WARN, not FAIL, as in verify-search.js: this box has no web fonts and
      // over-wraps by 15-20%. A real phone is the oracle.
      const c = await rect(page, '#controls');
      if (t.bottom > c.top) console.log(`WARN  ${tag}: ${id} title bottom ${Math.round(t.bottom)} > controls top ${Math.round(c.top)} (font-dependent)`);
    }
    check(`${tag}: ? clears the title in all ${views.length} views`, !clashes.length, clashes.join('; '));
    await page.evaluate(v => document.querySelector(`#views [data-view="${v}"]`).click(), views[0]);
    await page.waitForTimeout(600);

    // Expanded blurb: the heading TEXT must end left of the ?, which stays on top.
    await page.tap('#title-h');
    await page.waitForTimeout(300);
    const exp = await page.evaluate(() => {
      const h = document.getElementById('title-h'), q = document.getElementById('guide-btn');
      const rg = document.createRange(); rg.selectNodeContents(h);
      const textRight = Math.max(...[...rg.getClientRects()].map(r => r.right));
      const qr = q.getBoundingClientRect();
      const top = document.elementFromPoint(qr.left + qr.width / 2, qr.top + qr.height / 2);
      return { textRight: Math.round(textRight), qLeft: Math.round(qr.left), onTop: q.contains(top) };
    });
    check(`${tag}: expanded title — heading clears the ?, ? on top`,
          exp.textRight < exp.qLeft && exp.onTop, JSON.stringify(exp));
    await page.tap('#title-h');
    await page.waitForTimeout(300);

    await page.tap('#guide-btn');
    await page.waitForTimeout(200);
    check(`${tag}: a tap on the ? reopens it`, (await guide(page)).open);
    check(`${tag}: no page errors`, !errors.length, errors.join('; '));
    await b.close();
  }

  console.log(`\n${ran - fail}/${ran} passed`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });

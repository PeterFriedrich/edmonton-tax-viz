// Mobile-emulation ground-truth pass: renders index.html in an iPhone-class
// viewport with touch, screenshots the default view, then taps the map centre
// to confirm the #peek card appears (S81: on (hover: none) a tap shows the peek
// card — the deck.gl built-in tooltip node never exists at all on touch, so
// probing for it always reported "not found" and read as a regression).
// Establishes CONFIRMED facts for docs/MOBILE_USABILITY.md instead of assumptions.
//
// Usage: node tools/profiling/shot-mobile.js [url]
const { chromium } = require('playwright');

const url = process.argv[2] || 'http://localhost:8931/index.html';

// Chrome the page itself tracks (CHROME_IDS, read live below) plus the rows
// CHROME_IDS deliberately omits: it exists to dodge LABELS, so it carries
// #optpanel alone and skips the borderless sections inside it. Overflow is a
// per-row question — #moneymode clipping is invisible in #optpanel's box.
const EXTRA_IDS = ['controls', 'layers', 'coloradj', 'moneymode', 'chgwindow',
                   'moneydetail', 'devdetail', 'devmode', 'devmetric',
                   'devwindow', 'palette'];

// The id list reports known chrome (and catches an id that DISAPPEARS). It
// cannot catch chrome that has no id — the hover tooltip is `div.tip`, and it
// overflows a 390px viewport by ~127px. So sweep for overflow generically too.
const overflowing = page => page.evaluate(() => {
  const W = window.innerWidth, H = window.innerHeight;
  return [...document.querySelectorAll('body *')].filter(el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0
      && (r.right > W + 0.5 || r.left < -0.5 || r.bottom > H + 0.5);
  }).map(el => {
    const r = el.getBoundingClientRect();
    return {
      tag: el.tagName, id: el.id || null,
      cls: (el.className || '').toString().slice(0, 60) || null,
      left: Math.round(r.left), right: Math.round(r.right),
      top: Math.round(r.top), bottom: Math.round(r.bottom),
      text: (el.textContent || '').trim().slice(0, 40),
    };
  });
});

const measure = page => page.evaluate((extra) => {
  const W = window.innerWidth, H = window.innerHeight;
  const ids = [...new Set([...(typeof CHROME_IDS !== 'undefined' ? CHROME_IDS : []), ...extra])];
  return ids.map(id => {
    const el = document.getElementById(id);
    if (!el) return { id, present: false };
    const r = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return {
      id, present: true, display: style.display,
      left: Math.round(r.left), right: Math.round(r.right),
      top: Math.round(r.top), bottom: Math.round(r.bottom),
      offRight: r.right > W, offBottom: r.bottom > H, offLeft: r.left < 0,
    };
  });
}, EXTRA_IDS);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  // iPhone 13 logical viewport; hasTouch + isMobile so pointer:coarse / touch fire.
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 3,
    isMobile: true,
    hasTouch: true,
  });
  const page = await context.newPage();

  const msgs = [];
  page.on('console', m => msgs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', e => msgs.push(`[pageerror] ${e.message}`));

  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  await page.screenshot({ path: 'mobile-default.png' });

  // Which UI panels overflow the 390px-wide viewport? #peek and #temporal are
  // display:none until something opens them, so they measure 0,0 here — the
  // post-tap pass below is where the peek card has a real box.
  const overflow = await measure(page);

  // Tap the map centre and see whether the peek card appears. Warm the picking
  // buffer first (quirk kk): deck renders it on demand and headless SwiftShader
  // is too slow for a click's synchronous pick, so a bare tap lands on nothing
  // about half the time. Harness artifact, not device behaviour.
  await page.evaluate(([x, y]) => overlay._deck.pickObject({ x, y, radius: 0 }), [195, 480]);
  await page.touchscreen.tap(195, 480);
  await page.waitForTimeout(800);
  const peek = await page.evaluate(() => {
    const p = document.getElementById('peek');
    if (!p) return { found: false, why: 'no #peek element' };
    const visible = getComputedStyle(p).display !== 'none';
    const name = document.getElementById('peek-name');
    return {
      found: visible,
      hood: name ? (name.textContent || '').trim() : null,
      read: (document.getElementById('peek-read') || {}).textContent,
      deckTooltipExists: !!document.querySelector('.deck-tooltip'),
    };
  });
  const overflowAfterTap = await measure(page);
  const strays = await overflowing(page);
  await page.screenshot({ path: 'mobile-after-tap.png' });

  console.log('url:', url);
  console.log('viewport:', 390, 'x', 844);
  console.log('PANEL OVERFLOW:', JSON.stringify(overflow, null, 2));
  console.log('TAP PEEK:', JSON.stringify(peek));
  console.log('PEEK BOX (post-tap):',
    JSON.stringify(overflowAfterTap.filter(o => o.id === 'peek'), null, 2));
  console.log('OVERFLOWING ELEMENTS (post-tap, id or not):',
    JSON.stringify(strays, null, 2));
  console.log('--- browser messages ---');
  console.log(msgs.slice(0, 20).join('\n') || '(none)');
  await browser.close();
})();

// Mobile-emulation ground-truth pass: renders index.html in an iPhone-class
// viewport with touch, screenshots the default view, then taps the map centre
// to confirm whether the deck.gl built-in tooltip appears on tap (it should —
// getTooltip is hover-pick driven, and a tap produces a pick). Establishes
// CONFIRMED facts for docs/MOBILE_USABILITY.md instead of assumptions.
const { chromium } = require('playwright');

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

  await page.goto('http://localhost:8931/index.html', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  await page.screenshot({ path: 'mobile-default.png' });

  // Which UI panels overflow the 390px-wide viewport?
  const overflow = await page.evaluate(() => {
    const W = window.innerWidth, H = window.innerHeight;
    // Post-regroup (S65) control structure: #controls is a flex column holding
    // the pods; per-view sub-groups live inside #layers; #a11y is the Display
    // popover (palette + labels). #views is now 5 (Money·Services·Ratio·Uses·Dev).
    const ids = ['title','banner','controls','views','layers','coloradj','toggle',
                 'lens','moneydetail','devdetail','devmode','devmetric','devwindow',
                 'a11y','palette','legend'];
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
  });

  // Tap the map centre and see whether a tooltip element appears.
  await page.touchscreen.tap(195, 480);
  await page.waitForTimeout(600);
  const tip = await page.evaluate(() => {
    const t = document.querySelector('.deck-tooltip, #deck-tooltip, [class*="tooltip"]');
    return t ? { found: true, text: (t.textContent || '').slice(0, 120), visible: getComputedStyle(t).display !== 'none' } : { found: false };
  });
  await page.screenshot({ path: 'mobile-after-tap.png' });

  console.log('viewport:', 390, 'x', 844);
  console.log('PANEL OVERFLOW:', JSON.stringify(overflow, null, 2));
  console.log('TAP TOOLTIP:', JSON.stringify(tip));
  console.log('--- browser messages ---');
  console.log(msgs.slice(0, 20).join('\n') || '(none)');
  await browser.close();
})();

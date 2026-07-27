// Hit-test guard for the control chrome (added 2026-07-24 after the #84
// foldable-Options refactor shipped Detail/Denominator unclickable: #layers
// carries class="panel" (pointer-events:none) and got dropped from the flip
// list, so its buttons fell through to #opt-body).
//
// The functional verifies (verify-money-denom, verify-development, …) drive
// controls with page.$eval(sel, b => b.click()) — a direct JS .click() that
// bypasses pointer-events AND z-order, so they can't catch a control that is
// visible but not actually clickable. This script does the opposite: for every
// view, it unfolds the Options panel and asserts each *visible* control button
// hit-tests as itself — the topmost element at its centre is the button (or a
// child), and its computed pointer-events isn't "none". That is exactly what a
// real mouse needs, and exactly what the #84 regression broke.
//   node verify-controls-clickable.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  // The views actually offered in this build (public build hides some).
  const views = await page.$$eval('#views button', bs =>
    bs.filter(b => getComputedStyle(b).display !== 'none').map(b => b.dataset.view));
  console.log('views offered  :', views.join(', '));

  for (const view of views) {
    await page.$eval(`#views button[data-view="${view}"]`, b => b.click());
    await page.waitForTimeout(1200);
    // Unfold the Options panel so its body is laid out (default is folded on
    // mobile; on desktop it's open, but force it either way).
    await page.evaluate(() => document.getElementById('optpanel').classList.remove('folded'));
    await page.waitForTimeout(150);

    // Every button that is genuinely on screen: laid out, non-zero, inside the
    // viewport, and with no display:none ancestor. Report the ones a mouse
    // could NOT actuate (blocked by an overlay or pointer-events:none).
    const blocked = await page.evaluate(() => {
      const vw = innerWidth, vh = innerHeight;
      const out = [];
      const buttons = [
        // buttons + form controls: the services checkboxes/radios and the prism
        // slider live in #layers too, so they'd break the same way.
        ...document.querySelectorAll('#controls button, #controls input'),
        document.getElementById('a11y-btn'), // Display popover trigger (bottom-right)
      ].filter(Boolean);
      for (const el of buttons) {
        if (getComputedStyle(el).display === 'none') continue;
        // display:none anywhere up the chain?
        let hidden = false;
        for (let n = el; n; n = n.parentElement)
          if (n.nodeType === 1 && getComputedStyle(n).display === 'none') { hidden = true; break; }
        if (hidden) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 2 || r.height < 2) continue;
        const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        if (cx < 0 || cy < 0 || cx > vw || cy > vh) continue; // off-screen
        const top = document.elementFromPoint(cx, cy);
        const pe = getComputedStyle(el).pointerEvents;
        const hit = el.contains(top) || top === el;
        if (!hit || pe === 'none') {
          out.push({
            label: (el.id ? '#' + el.id : '') +
                   (el.dataset && Object.keys(el.dataset)[0]
                     ? `[${Object.keys(el.dataset)[0]}=${el.dataset[Object.keys(el.dataset)[0]]}]` : '') +
                   ' “' + (el.textContent || '').trim().slice(0, 24) + '”',
            pointerEvents: pe,
            blockedBy: top ? (top.tagName + (top.id ? '#' + top.id : '')) : null,
          });
        }
      }
      return out;
    });

    check(`[${view}] all visible controls hit-test as themselves`,
      blocked.length === 0,
      blocked.length ? '\n    ' + blocked.map(b => JSON.stringify(b)).join('\n    ') : '');
  }

  // --- double-tap zoom on the controls --------------------------------------
  // iOS Safari keeps double-tap-to-zoom on a device-width viewport, so tapping
  // a control twice quickly — the natural way to rotate further — zoomed the
  // page. `touch-action: manipulation` on the chrome roots kills only that
  // gesture. Headless Chromium cannot reproduce the iOS behaviour, so what is
  // asserted here is the mechanism: the property actually lands on every
  // control (touch-action resolves against ancestors, so a control outside all
  // three roots would silently miss out), and the MAP does NOT inherit it,
  // since double-tap zoom is the standard gesture there and must survive.
  const ta = await page.evaluate(() => {
    // Every control, not just the ones visible in the current view — a pod
    // that is hidden here shows in another, and would carry the bug with it.
    const ctrls = [...document.querySelectorAll('button, input')];
    const bad = ctrls.filter(el => {
      const v = getComputedStyle(el).touchAction;
      return v !== 'manipulation' && v !== 'none';
    }).map(el => (el.id || el.tagName) + ' “' +
                 (el.textContent || '').trim().slice(0, 20) + '”');
    const canvas = document.querySelector('#map canvas');
    return {
      total: ctrls.length, bad,
      map: getComputedStyle(document.getElementById('map')).touchAction,
      canvas: canvas ? getComputedStyle(canvas).touchAction : null,
    };
  });
  check('every control suppresses double-tap zoom (hidden ones too)',
        ta.bad.length === 0, `${ta.total - ta.bad.length}/${ta.total}` +
        (ta.bad.length ? ' — ' + JSON.stringify(ta.bad) : ''));
  check('the map keeps its own double-tap zoom gesture',
        ta.map !== 'manipulation', `#map touch-action: ${ta.map}`);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

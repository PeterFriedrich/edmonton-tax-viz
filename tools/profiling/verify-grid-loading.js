// Verify for the grid Detail buttons' loading state (2026-09-01). The two grid
// files are lazy and large (1.0 MB gzipped at 100 m, 2.8 MB at 50 m) and
// syncMoneyDetail lights the clicked button ACTIVE before the fetch starts, so
// the control reports "done" while the map has not moved. The busy stripe is
// what closes that gap, and it can go wrong four ways: never appear, appear on
// the wrong button, strand on after the grid lands, or flash on a switch back
// to a resolution that is already parsed (feedback for a wait that isn't).
//
// ⚠️ SAMPLING THE CLASS CANNOT CATCH ANY OF THIS. Over localhost the fetch
// settles in tens of milliseconds, so a poll between clicks reads "not busy"
// whether the stripe worked perfectly or was never written at all — the S129
// lesson (a check placed where the value cannot be wrong) in its exact shape.
// This file records class TRANSITIONS with a MutationObserver installed before
// the first click, so a correct busy window and a missing one are distinct
// observations no matter how fast the fetch is.
//
// It also samples the ::after pseudo-element AT THE MOMENT the class lands: the
// class being right does not make the stripe visible, and a wrong selector or a
// clipped pseudo would leave every class assertion green over an invisible
// control.
//
// FALSIFIED 2026-09-01 — each defect was reintroduced and the named check went
// red:
//   * busy state never set                -> "100 m cold: stripe appeared"
//   * cleared only on the caller's render -> "50 m cold: stripe cleared"
//                                            + "end state: nothing left busy"
//   * CSS rule renamed (#detail button)   -> "100 m cold: sweep is animated"
//
// ⚠️ HISTORY ON THE `gridStore` GATE, because it changed status. Before the
// prefetch existed, swapping it for `gridFetches[cellM]` passed EVERY check here
// — including an in-flight re-entry written specifically to separate them, which
// failed to, because on re-entry the first call's stripe is still up and the
// suppressed second add changes nothing observable. That was recorded as "no
// check justifies this choice". **The prefetch made it falsifiable**: the warm
// sets `gridFetches[100]` seconds before `gridStore[100]`, so a click landing in
// that window distinguishes them, and the last section below now reds under the
// swap. The choice is checked, not merely stated.
//
// ⚠️ "stripe cleared" was VACUOUS in the first version of this file: keyed on
// `mine.length`, it read true under a build where the stripe was never added at
// all, because classList.remove() writes the class attribute regardless. See the
// note on `cleared` below.
//
//   node verify-grid-loading.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let failures = 0;
const check = (name, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) failures++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}: got ${JSON.stringify(got)}` +
              (ok ? '' : ` want ${JSON.stringify(want)}`));
};

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => { console.log('PAGE EXCEPTION:', e.message); failures++; });
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  // swiftshader can hang page.click while the render loop is busy — dispatch
  // from inside the page (the verify-glass/verify-glass-cell workaround).
  const click = mode => page.$eval(`#moneydetail button[data-moneydetail="${mode}"]`, b => b.click());

  // Installed BEFORE the first click, so nothing that happens during a fetch is
  // observed after the fact. Each entry is one add or remove, in order, with the
  // rendered pseudo-element read at that instant.
  await page.evaluate(() => {
    window.__busyLog = [];
    for (const btn of document.querySelectorAll('#moneydetail button')) {
      new MutationObserver(() => {
        const on = btn.classList.contains('is-loading');
        const css = on ? getComputedStyle(btn, '::after') : null;
        window.__busyLog.push({
          mode: btn.dataset.moneydetail,
          on,
          ariaBusy: btn.getAttribute('aria-busy'),
          // A class with no drawn stripe behind it is the silent failure here.
          drawn: on ? css.content !== 'none' && css.animationName === 'moneydetail-sweep' : null,
        });
      }).observe(btn, { attributes: true, attributeFilter: ['class'] });
    }
  });

  // Drain ONCE per click and summarise every button's transitions from that one
  // read — draining per button would let the first call discard the rows the
  // second one exists to inspect.
  const drain = async () => {
    const rows = await page.evaluate(() => {
      const r = window.__busyLog; window.__busyLog = []; return r;
    });
    const per = mode => {
      const mine = rows.filter(r => r.mode === mode);
      const on = mine.filter(r => r.on);
      return {
        appeared: on.length > 0,
        // ⚠️ `on.length > 0`, not `mine.length > 0`: classList.remove() writes
        // the class attribute even when the class was never there, so a build
        // with the ADD disabled still logs a trailing off-row. Keyed on
        // mine.length this read "cleared: true" under a stripe that had never
        // existed — green for the wrong reason, which is the defect this whole
        // file is written against.
        cleared: on.length > 0 && !mine[mine.length - 1].on,
        drawn: on.length > 0 && on.every(r => r.drawn),
        ariaOn: on.length > 0 && on.every(r => r.ariaBusy === 'true'),
        ariaOff: mine.filter(r => !r.on).every(r => r.ariaBusy === null),
      };
    };
    return { hood: per('hood'), grid: per('grid'), fine: per('grid-fine') };
  };

  // Any button carrying the stripe right now. The end-state guard: a stranded
  // stripe is the failure a per-click check cannot see.
  const stuck = () => page.evaluate(() =>
    [...document.querySelectorAll('#moneydetail button')]
      .filter(b => b.classList.contains('is-loading')).map(b => b.dataset.moneydetail));

  check('landing: no stripe before any click', await stuck(), []);

  // --- the idle prefetch of the DEFAULT resolution ------------------------
  // Fired from hideLoading once the overlay lifts. The 4 s settle above covers
  // it on this box; waitForFunction rather than a bare read so a slower machine
  // does not fail on scheduling.
  // ⚠️ Reads the parsed CELL COUNT, and swallows the timeout so a build with no
  // prefetch reds a NAMED check instead of crashing the run — a suite that dies
  // on the first missing feature reports one defect and hides the rest. Also not
  // `check(true, true)` beside the wait: that prints a green line asserting
  // nothing, the vacuous shape this file's header is about.
  const warmCells = await page
    .waitForFunction(() => gridStore[100] != null, null, { timeout: 30000 })
    .then(() => page.evaluate(() => gridStore[100].cells.length))
    .catch(() => null);
  check('prefetch: 100 m is warm with no click', warmCells, 34671);
  check('prefetch: 50 m was NOT pushed',
        await page.evaluate(() => gridStore[50] == null || gridFetches[50] === undefined), true);

  // ⚠️ THE INVARIANT THE loadGridData/ensureGridData SPLIT EXISTS FOR. A warm
  // must not repoint the ACTIVE grid: gridCell is what applyView's
  // `gridCell !== wantCell` gate reads, so a prefetch that set it would make the
  // view believe a grid it has never drawn is already on screen.
  // ⚠️ `gridData != null` as a BOOLEAN, never the object: `check` prints its
  // operands on failure, and a red that dumps 93k cells buries every other line.
  check('prefetch: did not activate the grid',
        await page.evaluate(() => ({ cell: gridCell, hasData: gridData != null, view: state.view })),
        { cell: null, hasData: false, view: 'money' });
  check('prefetch: drew no stripe', await stuck(), []);
  await drain(); // discard: nothing should be in here, and the checks above said so

  // --- 100 m, now WARM ----------------------------------------------------
  // The common path after the prefetch lands: no stripe, because there is no
  // wait to report. Absence here is the feature, not a broken indicator.
  await click('grid');
  await page.waitForFunction(() => gridCell === 100, null, { timeout: 20000 });
  await page.waitForTimeout(300);
  let d = await drain();
  check('100 m warm: no stripe', d.grid.appeared, false);
  check('100 m warm: still renders', await page.evaluate(() =>
    overlay._deck.props.layers.some(l => l.id === 'glass-grid')), true);

  // --- 50 m, cold --------------------------------------------------------
  await click('grid-fine');
  await page.waitForFunction(() => gridCell === 50, null, { timeout: 30000 });
  await page.waitForTimeout(300);
  d = await drain();
  check('50 m cold: stripe appeared', d.fine.appeared, true);
  check('50 m cold: stripe cleared', d.fine.cleared, true);
  check('50 m cold: sweep is animated', d.fine.drawn, true);
  check('50 m cold: no stripe on the other two',
        [d.grid.appeared, d.hood.appeared], [false, false]);

  // --- back to 100 m, now CACHED ----------------------------------------
  // The switch resolves in one microtask; a stripe here is feedback for a wait
  // that does not happen, which reads as a stutter rather than as progress.
  await click('grid');
  await page.waitForFunction(() => gridCell === 100, null, { timeout: 20000 });
  await page.waitForTimeout(300);
  check('100 m cached: no stripe', (await drain()).grid.appeared, false);

  await click('grid-fine');
  await page.waitForFunction(() => gridCell === 50, null, { timeout: 20000 });
  await page.waitForTimeout(300);
  check('50 m cached: no stripe', (await drain()).fine.appeared, false);

  check('end state: nothing left busy', await stuck(), []);

  // --- the hover warm ----------------------------------------------------
  // Reaching for a button starts its file. Silent: no stripe, no repaint, no
  // change to the active grid — hovering a control is not a request to see it.
  const ctxH = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const pH = await ctxH.newPage();
  await pH.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await pH.waitForTimeout(4000);
  await pH.waitForFunction(() => gridStore[100] != null, null, { timeout: 30000 })
    .catch(() => {}); // reported by the check above; don't crash the rest
  check('hover: 50 m not fetched before the pointer arrives',
        await pH.evaluate(() => gridFetches[50] === undefined), true);
  await pH.hover('#moneydetail button[data-moneydetail="grid-fine"]');
  await pH.waitForTimeout(200);
  check('hover: 50 m fetch started',
        await pH.evaluate(() => gridFetches[50] !== undefined), true);
  check('hover: drew no stripe and changed nothing',
        await pH.evaluate(() => ({
          busy: [...document.querySelectorAll('#moneydetail button')]
            .some(b => b.classList.contains('is-loading')),
          cell: gridCell, view: state.view,
        })), { busy: false, cell: null, view: 'money' });
  await ctxH.close();

  // --- re-entry WHILE THE FETCH IS STILL IN FLIGHT -----------------------
  // A fresh context, because the assertion needs an UNFETCHED 50 m grid; the
  // route delay makes the in-flight window deterministic instead of racing a
  // localhost fetch that settles in ~200 ms.
  const ctx2 = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const p2 = await ctx2.newPage();
  await p2.route('**/value_grid_50.json', async route => {
    await new Promise(r => setTimeout(r, 2500));
    await route.continue();
  });
  await p2.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await p2.waitForTimeout(4000);
  const click2 = mode => p2.$eval(`#moneydetail button[data-moneydetail="${mode}"]`, b => b.click());
  const busyNow = () => p2.$eval('#moneydetail button[data-moneydetail="grid-fine"]',
                                 b => b.classList.contains('is-loading'));

  await click2('grid-fine');
  await p2.waitForTimeout(400);
  check('50 m in flight: stripe is up', await busyNow(), true);

  await click2('hood');            // leave mid-fetch
  await click2('grid-fine');       // and come back, bytes still arriving
  await p2.waitForTimeout(400);
  check('50 m re-entered in flight: stripe still up', await busyNow(), true);

  await p2.waitForFunction(() => gridCell === 50, null, { timeout: 30000 });
  await p2.waitForTimeout(400);
  check('50 m re-entered in flight: stripe cleared on arrival', await busyNow(), false);
  await ctx2.close();

  // --- CLICKING BEFORE THE PREFETCH LANDS --------------------------------
  // ⚠️ This is the case that finally separates the `gridStore` gate from a
  // `gridFetches` one, and it exists only BECAUSE of the prefetch. The warm sets
  // gridFetches[100] seconds before gridStore[100], so for that whole window the
  // two gates disagree: gridStore correctly sees "cells not ready, this reader
  // is about to wait" and raises the stripe, while gridFetches sees "a fetch
  // exists" and shows nothing — leaving a click that beat the prefetch with no
  // feedback at all, which is the exact complaint the stripe was built for.
  // Before the prefetch, no arrangement of clicks could tell them apart (see the
  // header note); now one can, so the gate is a checked decision rather than a
  // stated preference.
  const ctx3 = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const p3 = await ctx3.newPage();
  await p3.route('**/value_grid.json', async route => {
    await new Promise(r => setTimeout(r, 4000));
    await route.continue();
  });
  await p3.goto(url, { waitUntil: 'networkidle', timeout: 40000 });
  // Wait for the warm to START, not to finish — the click has to land inside it.
  const inWarm = await p3.waitForFunction(() => typeof gridFetches !== 'undefined'
    && gridFetches[100] !== undefined && gridStore[100] == null,
    null, { timeout: 40000 }).then(() => true).catch(() => false);
  check('a prefetch window exists to click into', inWarm, true);
  await p3.$eval('#moneydetail button[data-moneydetail="grid"]', b => b.click());
  await p3.waitForTimeout(300);
  check('clicked before the prefetch landed: stripe is up',
        await p3.$eval('#moneydetail button[data-moneydetail="grid"]',
                       b => b.classList.contains('is-loading')), true);
  await p3.waitForFunction(() => gridCell === 100, null, { timeout: 40000 });
  await p3.waitForTimeout(300);
  check('clicked before the prefetch landed: stripe cleared on arrival',
        await p3.$eval('#moneydetail button[data-moneydetail="grid"]',
                       b => b.classList.contains('is-loading')), false);

  await browser.close();
  console.log(failures ? `\n${failures} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(failures ? 1 : 0);
})();

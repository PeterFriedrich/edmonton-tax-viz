// Verify for the loading overlay (#loading, added 2026-08-28). It covers the
// gap between first paint and the first deck frame, lifting only once BOTH
// gates pass: MapLibre `idle` (the basemap came up) and deck's first draw that
// has layers (the prisms are on screen).
//
// The checks that matter here are about WHICH FRAME lifts it, because every
// failure mode is SILENT — the overlay still works:
//   - Early: lifting on the map's first `render` after the overlay attaches,
//     which has no deck layers in it, uncovers an empty backdrop.
//   - Late: gating on a later map `idle`, or a min-display floor implemented
//     as a plain timer and starved by post-paint JSON parsing, sits over a
//     correct map.
// Timing is read from a MutationObserver, NOT by polling — polling the overlay
// every 100ms perturbs the render loop enough to move these numbers.
//
// Also checks the failure paths, which are the reason the overlay exists in
// prod: a non-ok data fetch, a hung one, and that retry recovers.
//   node verify-loading-overlay.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

const DATA_FILE = 'neighbourhood_value_per_acre';
const FADE_MIN_MS = 250;    // below this the overlay flashes rather than reads
const FADE_MAX_MS = 8000;   // backstop only; the lift waits out shader linking, ~2.9s on this box
const TIMEOUT_WAIT_MS = 17000; // the overlay's own timeout is 15s

const GL = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
            '--ignore-gpu-blocklist', '--enable-webgl'];

// Records when the overlay first carries .is-hidden, without polling it.
// ⚠️ Attached from DOCUMENT CREATION, not DOMContentLoaded. The basemap gate
// resolves in ~50ms here (the style declares no tile sources), so the first
// status text is already gone by DOMContentLoaded at ~530ms — an observer that
// starts there records one text and the swap looks broken.
const OBSERVE = () => {
  window.__ov = { firstDisplay: null, fadeStartMs: null, texts: [] };
  const el = () => document.getElementById('loading');
  const note = () => {
    const box = el();
    if (!box) return;
    const t = document.getElementById('loading-text').textContent;
    if (window.__ov.texts[window.__ov.texts.length - 1] !== t) window.__ov.texts.push(t);
    if (window.__ov.fadeStartMs === null && box.classList.contains('is-hidden')) {
      window.__ov.fadeStartMs = Math.round(performance.now());
      // What deck had to draw when the overlay let go. null = could not read.
      try { window.__ov.layersAtFade = overlay._deck.layerManager.getLayers().length; }
      catch (e) { window.__ov.layersAtFade = null; }
    }
  };
  // Idle timestamps, so the gate check can be RELATIVE. An absolute ms ceiling
  // cannot separate the shipped lift (~560ms) from an idle-gated one (~1045ms)
  // without flaking on a loaded box; "lifted before the map's post-layer idle"
  // is the same statement and scales with the machine.
  window.__ov.idles = [];
  // ⚠️ NOT `window.map` — that is the <div id="map">, which the id-global rule
  // puts on window. The MapLibre instance is a top-level `const`, which lives
  // in the global LEXICAL scope and shadows the div for a bare identifier only.
  // The try/catch is the TDZ window: once the page script starts but before the
  // const initializes, touching `map` throws rather than returning undefined.
  const hunt = setInterval(() => {
    let m;
    try { m = map; } catch (e) { return; }
    if (!m || typeof m.on !== 'function') return;   // still the div
    clearInterval(hunt);
    m.on('idle', () => window.__ov.idles.push(Math.round(performance.now())));
    // The first map frame in which deck has layers: the frame the lift belongs to.
    window.__ov.firstLayeredMs = null;
    m.on('render', () => {
      if (window.__ov.firstLayeredMs !== null) return;
      try {
        if (overlay._deck.layerManager.getLayers().length)
          window.__ov.firstLayeredMs = Math.round(performance.now());
      } catch (e) {}
    });
  }, 10);

  let bound = false;
  const bind = () => {
    const box = el();
    if (!box || bound) return;
    bound = true;
    note();
    new MutationObserver(note).observe(box, {
      attributes: true, attributeFilter: ['class', 'style', 'hidden'],
      subtree: true, childList: true, characterData: true,
    });
  };
  // `document` is observable before documentElement exists.
  new MutationObserver(bind).observe(document, { childList: true, subtree: true });
  // Read display only once the stylesheet has certainly applied — at parse time
  // it can still be the UA default, which would not be a real assertion.
  document.addEventListener('DOMContentLoaded', () => {
    bind();
    if (el()) window.__ov.firstDisplay = getComputedStyle(el()).display;
  });
};

const errState = () => {
  const el = document.getElementById('loading');
  const btn = document.getElementById('loading-retry');
  return {
    isError: el.classList.contains('is-error'),
    text: document.getElementById('loading-text').textContent,
    retryVisible: !btn.hidden,
    spinnerHidden: getComputedStyle(document.getElementById('loading-spinner')).display === 'none',
    display: getComputedStyle(el).display,
  };
};

(async () => {
  const browser = await chromium.launch({ args: GL });
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  // --- A. the normal load ---------------------------------------------------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    const exceptions = [];
    page.on('pageerror', e => exceptions.push(e.message));
    await page.addInitScript(OBSERVE);
    // ⚠️ The boot data is held back, as a real network holds it. Served from
    // localhost it can land before the map's first idle, and then the basemap
    // gate is the late one and the data gate is never the thing under test: a
    // lift on a frame with no deck layers in it went unseen that way until
    // 2026-10-13.
    await page.route(`**/${DATA_FILE}*`, async r => {
      await new Promise(f => setTimeout(f, 400));
      r.continue();
    });
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(4000);

    const ov = await page.evaluate(() => window.__ov);
    console.log('overlay   :', JSON.stringify(ov));

    check('overlay ships VISIBLE (no JS needed to show it)', ov.firstDisplay === 'flex',
          `first computed display: ${ov.firstDisplay}`);
    // Both gate labels must actually appear. This is the only on-screen signal
    // of WHICH gate is pending, which is what makes a slow load diagnosable.
    check('status text names the pending gate, and swaps', ov.texts.length >= 2,
          JSON.stringify(ov.texts));
    check('the swap lands on the data gate', ov.texts[ov.texts.length - 1] === 'Loading tax data…',
          JSON.stringify(ov.texts[ov.texts.length - 1]));
    check('overlay lifted at all', ov.fadeStartMs !== null);
    // The overlay exists to cover the wait for the prisms. MapLibre's first
    // `render` after the overlay control attaches has NO deck layers in it;
    // deck builds them, and links their shaders, on the frame after.
    check('deck had layers to draw when the overlay lifted', ov.layersAtFade > 0,
          `layers at lift: ${ov.layersAtFade}`);

    // THE regression guard, and the reason this file exists. The lift belongs
    // to ONE frame: the first in which deck has layers. Every known defect
    // moves it off that frame, and all of them are silent:
    //   - early: gating on the map's first `render` after the overlay attaches,
    //     a frame with no deck layers in it (shipped 2026-08-28 to 2026-10-13;
    //     the check above);
    //   - late: gating on a later map `idle`, or racing the min-display floor
    //     as a third promise where a busy main thread starves it.
    // Relative to the frame, not a position on the clock, so it scales with the
    // machine. ⚠️ An earlier version asserted the lift did NOT coincide with a
    // map idle. The correct lift does coincide with one (measured: fade 2859ms,
    // idles 695 / 2858 / 3676), so that check could only pass on the early lift.
    const COINCIDE_MS = 40;
    // Fails loudly rather than passing vacuously if it could not measure.
    check('a frame with deck layers was observed (otherwise the next check is vacuous)',
          ov.firstLayeredMs !== null);
    check('lift lands on the first frame that has deck layers, not after it',
          ov.firstLayeredMs !== null && ov.fadeStartMs !== null &&
          Math.abs(ov.fadeStartMs - ov.firstLayeredMs) <= COINCIDE_MS,
          `fade ${ov.fadeStartMs}ms, first layered frame ${ov.firstLayeredMs}ms, idles ${JSON.stringify(ov.idles)}`);
    // Coarse backstop only. It does not discriminate between the variants
    // above; it catches a gate that never fires or a genuinely stalled load.
    check('lift is not grossly stalled', ov.fadeStartMs !== null && ov.fadeStartMs <= FADE_MAX_MS,
          `fade started ${ov.fadeStartMs}ms (ceiling ${FADE_MAX_MS}ms)`);
    check('overlay was shown long enough to read, not flashed',
          ov.fadeStartMs !== null && ov.fadeStartMs >= FADE_MIN_MS,
          `fade started ${ov.fadeStartMs}ms (floor ${FADE_MIN_MS}ms)`);

    const after = await page.evaluate(() => {
      const el = document.getElementById('loading');
      const mid = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
      const rc = document.getElementById('recenter');
      const r = rc.getBoundingClientRect();
      return {
        display: getComputedStyle(el).display,
        hidden: el.hidden,
        blocksCentre: mid === el || el.contains(mid),
        controlHit: document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) === rc,
      };
    });
    console.log('post-load :', JSON.stringify(after));
    check('overlay ends display:none', after.display === 'none');
    // Distinct from display:none — the fade window is transparent but still
    // present, so pointer-events is what keeps it out of the hit-test tree.
    check('overlay does not intercept the map centre', after.blocksCentre === false);
    check('a real control under the overlay is clickable', after.controlHit === true);
    check('no page exceptions on the loading path', exceptions.length === 0,
          exceptions.join(' | '));
    await page.close();
  }

  // --- B. a non-ok data response -------------------------------------------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.route('**/*', r => r.request().url().includes(DATA_FILE)
      ? r.fulfill({ status: 404, body: 'not found' }) : r.continue());
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(4000);
    const s = await page.evaluate(errState);
    console.log('404       :', JSON.stringify(s));
    check('[404] overlay enters the error state', s.isError === true);
    check('[404] overlay stays up rather than uncovering a dead map', s.display !== 'none');
    check('[404] retry is offered', s.retryVisible === true);
    check('[404] the spinner stops', s.spinnerHidden === true);
    await page.close();
  }

  // --- C. a hung data request must trip the timeout -------------------------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.route('**/*', r => r.request().url().includes(DATA_FILE)
      ? new Promise(() => {}) : r.continue());
    await page.goto(url, { waitUntil: 'commit', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(TIMEOUT_WAIT_MS);
    const s = await page.evaluate(errState);
    console.log('hang      :', JSON.stringify(s));
    check('[hang] the timeout fires rather than spinning forever', s.isError === true);
    check('[hang] retry is offered', s.retryVisible === true);
    await page.close();
  }

  // --- D. retry recovers once upstream heals --------------------------------
  {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    let broken = true;
    await page.route('**/*', r => (broken && r.request().url().includes(DATA_FILE))
      ? r.fulfill({ status: 404, body: 'not found' }) : r.continue());
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(3000);
    const before = await page.evaluate(errState);
    broken = false;
    // A real click, not JS .click() — this is also the assertion that the error
    // state's retry is genuinely hit-testable.
    await page.click('#loading-retry');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(4000);
    const s = await page.evaluate(() => {
      const el = document.getElementById('loading');
      return {
        display: getComputedStyle(el).display,
        isError: el.classList.contains('is-error'),
        canvas: !!document.querySelector('canvas'),
      };
    });
    console.log('retry     :', JSON.stringify(s));
    check('[retry] the error state preceded it', before.isError === true);
    check('[retry] a real click on the button works', s.isError === false);
    check('[retry] the overlay clears after recovery', s.display === 'none');
    check('[retry] the map renders after recovery', s.canvas === true);
    await page.close();
  }

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

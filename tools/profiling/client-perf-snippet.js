// Client-side perf capture — PASTE INTO THE BROWSER CONSOLE on the live site.
// Not a Playwright script: the whole point is a real GPU on a real display,
// which this project's Oracle box (SwiftShader, no GPU) cannot provide.
//
// Exists because the FIRST capture (old laptop, 2026-09-01) was ad hoc, and its
// three caveats are all "we didn't pin the conditions". This file pins them, so
// capture #2 and any later one are comparable by construction rather than by
// remembering.
//
// ── HOW TO RUN ────────────────────────────────────────────────────────────
//  1. Open the site. **Reload once and let it settle** — the baseline capture
//     was WARM (download_ms 0, ttfb 26 ms), so a cold run measures cache state
//     and nothing else.
//  2. ⚠️ **Make the viewport as TALL as you can** — undock devtools into its
//     own window rather than docking it. "Dock it at the bottom" was the
//     instruction for the first two captures and it was WRONG: the gaming
//     laptop came back at 1363x264 against the old laptop's 1534x503, so the
//     two disagreed by 13% on device pixels and could not be compared on fill
//     rate at all. Fragment cost scales with pixels, so a short viewport
//     measures DRAW cost well and hides FILL cost.
//     **Compare `devicePx total` between machines before trusting any fps
//     ratio across them.** The script warns below if the viewport is short.
//  3. Paste this whole file into the Console and press Enter. It takes ~25 s:
//     it pans the map twice, once per grid resolution.
//  4. Copy the printed markdown table back.
//  5. ⚠️ Read the REAL adapter separately — Firefox sanitises the WebGL
//     renderer string to "Intel(R) HD Graphics, or similar", which is a privacy
//     placeholder, not your card. Firefox: about:support -> Graphics ->
//     "Description". Chrome: chrome://gpu. On a laptop with switchable
//     graphics this is also what reveals it quietly running integrated.
// ──────────────────────────────────────────────────────────────────────────
(async () => {
  const nav = performance.getEntriesByType('navigation')[0] || {};
  const gl = document.createElement('canvas').getContext('webgl');
  const dbg = gl && gl.getExtension('WEBGL_debug_renderer_info');
  const canvas = document.querySelector('#map canvas');

  // Frames actually painted during a fixed camera move. Counting rAF is the
  // honest measure here: it counts what the compositor delivered, not what the
  // app asked for. A fixed DURATION with a fixed path keeps the work constant
  // across machines, so the frame count is the only thing that varies.
  const panFps = async label => {
    map.jumpTo({ center: [-113.49, 53.54], zoom: 11.2, pitch: 52, bearing: -18 });
    await new Promise(r => setTimeout(r, 1500));       // let tiles + layers settle
    let frames = 0, stop = false;
    const tick = () => { if (!stop) { frames++; requestAnimationFrame(tick); } };
    requestAnimationFrame(tick);
    const t0 = performance.now();
    map.easeTo({ center: [-113.42, 53.58], zoom: 11.6, bearing: 12,
                 duration: 8000, essential: true });
    await new Promise(r => setTimeout(r, 8000));
    const elapsed = performance.now() - t0;
    stop = true;
    return { label, frames, fps: +(frames / (elapsed / 1000)).toFixed(1) };
  };

  const enter = async detail => {
    document.querySelector('#views button[data-view="money"]').click();
    await new Promise(r => setTimeout(r, 400));
    document.querySelector(`#moneydetail button[data-moneydetail="${detail}"]`).click();
    // the fine grid is a 8 MB fetch on first pick — wait for the cells to land
    for (let i = 0; i < 60; i++) {
      await new Promise(r => setTimeout(r, 500));
      if (typeof gridData !== 'undefined' && gridData) break;
    }
    await new Promise(r => setTimeout(r, 1500));
  };

  await enter('grid');
  const cells100 = gridData && gridData.cells.length;
  const fps100 = await panFps('100 m grid');
  await enter('grid-fine');
  const cells50 = gridData && gridData.cells.length;
  const fps50 = await panFps('50 m grid');

  const rows = [
    ['dpr', devicePixelRatio],
    ['screen', `${screen.width}x${screen.height}`],
    ['cssPx', canvas ? `${canvas.clientWidth}x${canvas.clientHeight}` : 'n/a'],
    ['devicePx', canvas ? `${canvas.width}x${canvas.height}` : 'n/a'],
    ['devicePx total', canvas ? (canvas.width * canvas.height).toLocaleString() : 'n/a'],
    ['gpu (SANITISED — see about:support)',
      dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : 'unavailable'],
    ['ttfb_ms', Math.round(nav.responseStart - nav.requestStart)],
    ['download_ms', Math.round(nav.responseEnd - nav.responseStart)],
    ['domInteractive_ms', Math.round(nav.domInteractive)],
    ['loadEvent_ms', Math.round(nav.loadEventEnd || nav.duration)],
    ['cells @100 m', cells100 && cells100.toLocaleString()],
    ['pan fps @100 m', `${fps100.fps} (${fps100.frames} frames / 8 s)`],
    ['cells @50 m', cells50 && cells50.toLocaleString()],
    ['pan fps @50 m', `${fps50.fps} (${fps50.frames} frames / 8 s)`],
    ['fps ratio 50/100', +(fps50.fps / fps100.fps).toFixed(2)],
  ];
  console.log('\n| field | value |\n|---|---|\n' +
    rows.map(([k, v]) => `| \`${k}\` | ${v} |`).join('\n') + '\n');
  console.log('⚠️ warm run? download_ms should be ~0. If not, reload and re-run.');
  // Raw frame counts are printed above for a reason: if BOTH readings are in
  // single digits the renderer is saturated and the ratio is meaningless, not
  // evidence of "no difference". That is what this box reports (SwiftShader,
  // 0.9 fps at both resolutions), which is why the capture has to happen on
  // real hardware. A discriminating result needs a healthy 100 m baseline —
  // if @100 m is not comfortably above 30 fps, report that instead of a ratio.
  if (fps100.fps < 30) {
    console.warn('⚠️ 100 m baseline is under 30 fps — the ratio below it is ' +
                 'not meaningful. Report the raw frame counts.');
  }
  // ⚠️ The viewport guard, added after the gaming-laptop capture came back at
  // 264 px tall (baseline 503) because devtools was docked. Fill rate scales
  // with pixels, so a short viewport quietly turns a fill-rate test into a draw
  // -call test and reports a reassuring number for the wrong question.
  if (canvas && canvas.clientHeight < 400) {
    console.warn(`⚠️ viewport is only ${canvas.clientHeight} px tall — devtools ` +
      'is probably docked. Fill rate is UNDER-STRESSED, so the fps ratio ' +
      'understates the finer grid\'s cost. Undock devtools and re-run.');
  }
  console.log('⚠️ cross-machine: compare `devicePx total` first. Two machines ' +
    'at different device-pixel counts are not comparable on frame rate.');
})();

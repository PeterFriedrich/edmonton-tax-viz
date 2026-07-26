// Verify the Colour-scaling pod (#coloradj) — successor to
// verify-lens-visibility.js, which also covered the residential lens until that
// lens was removed on 2026-07-26 (redundant with the Residential revenue cut and
// the tooltip's "% of revenue is residential", both continuous where the lens
// was a binary fade).
//
// #coloradj is now the Options panel's ONLY presentation control and sits at the
// BOTTOM of it, below #layers. It HIDES in views where it has no effect rather
// than greying — greyed #4a4a5e on a dark panel reads as *broken*, which
// produced a real bug report in 2026-07. Because it is a direct child of
// #opt-body, hiding it takes its own row with it: there is no separate column to
// collapse any more.
//   node tools/profiling/verify-coloradj.js <url>          (from REPO ROOT)
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };
  const probe = () => page.evaluate(() => {
    const pod = document.getElementById('coloradj'), b = document.getElementById('coloradj-btn');
    const r = b.getBoundingClientRect();
    const at = r.width ? document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) : null;
    const body = document.getElementById('opt-body');
    return {
      shown: pod.offsetParent !== null,
      disabled: b.disabled,
      label: b.textContent.trim(),
      active: b.classList.contains('active'),
      hitIsBtn: at === b,
      podW: Math.round(pod.getBoundingClientRect().width),
      // Bottom-of-panel ordering: #coloradj must be the LAST child of #opt-body
      // and paint below #layers.
      lastChild: body.lastElementChild.id,
      childOrder: [...body.children].map(c => c.id).join(' > '),
      layersBottom: Math.round(document.getElementById('layers').getBoundingClientRect().bottom),
      coloradjTop: Math.round(r.top),
      sqrt: state.colorAdjust,
      view: state.view,
      // The removed lens must leave nothing behind.
      lensGone: document.getElementById('lens') === null,
      presGone: document.getElementById('opt-pres') === null,
    };
  });
  const goView = async v => { await page.click(`#views button[data-view="${v}"]`);
                              await page.waitForTimeout(2500); };

  // --- the residential lens is really gone (DOM, state and globals)
  const p0 = await probe();
  check('#lens element removed', p0.lensGone === true);
  check('#opt-pres wrapper removed (no column left to collapse)', p0.presGone === true);
  const leftovers = await page.evaluate(() => ({
    stateField: 'residential' in state,
    applyLens: typeof applyLens !== 'undefined',
    fade: typeof LENS_FADE_COLOR !== 'undefined',
    clampFn: typeof residentialClampFor !== 'undefined',
  }));
  check('state.residential field removed', leftovers.stateField === false);
  check('applyLens / LENS_FADE_COLOR / residentialClampFor all gone',
        !leftovers.applyLens && !leftovers.fade && !leftovers.clampFn,
        JSON.stringify(leftovers));

  // --- it sits at the BOTTOM of the Options panel
  check('#coloradj is the last child of #opt-body', p0.lastChild === 'coloradj', p0.childOrder);
  check('#coloradj paints below #layers', p0.coloradjTop >= p0.layersBottom,
        `layers bottom ${p0.layersBottom}, coloradj top ${p0.coloradjTop}`);

  // --- label is the readout, and does not jitter between states
  check('[money] shown + enabled', p0.shown === true && p0.disabled === false);
  check('[money] hit-tests as itself', p0.hitIsBtn === true);
  check('label names the active scaling', p0.label === 'Colour: sqrt scaling', p0.label);
  check('state caption element is still gone',
        await page.evaluate(() => !document.getElementById('coloradj-state')));
  await page.click('#coloradj-btn');
  await page.waitForTimeout(900);
  const off = await probe();
  check('label flips to "Colour: linear"', off.label === 'Colour: linear', off.label);
  check('gold clears when linear', off.active === false);
  check('width does not jump between labels', off.podW === p0.podW, `${off.podW} vs ${p0.podW}`);

  // --- survives Money's 100 m grid (it applies there too)
  await page.click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3500);
  const grid = await probe();
  check('[100 m grid] still shown + enabled', grid.shown === true && grid.disabled === false,
        `view=${grid.view}`);
  check('[100 m grid] linear state carried in', grid.sqrt === false);
  check('[100 m grid] still the last child', grid.lastChild === 'coloradj');
  await page.click('#moneydetail button[data-moneydetail="hood"]');
  await page.waitForTimeout(3000);

  // --- hidden everywhere it has no effect; state survives the round-trip
  const views = await page.evaluate(() =>
    [...document.querySelectorAll('#views button')].filter(b => b.offsetParent !== null)
      .map(b => b.dataset.view));
  console.log('views     :', views.join(', '));
  for (const v of views.filter(v => v !== 'money')) {
    await goView(v);
    const s = await probe();
    check(`[${v}] hidden, not greyed`, s.shown === false && s.disabled === true);
    // The panel must not be left empty by the hide — #layers still fills it.
    check(`[${v}] Options panel still has content (#layers)`,
          await page.evaluate(() => document.getElementById('layers').offsetParent !== null));
  }
  await goView('money');
  const back = await probe();
  check('[money] returns after the tour', back.shown === true && back.disabled === false);
  check('[money] linear survived the hide/show round-trip', back.sqrt === false);
  check('[money] label still reads the restored state', back.label === 'Colour: linear', back.label);
  check('[money] still the last child after the tour', back.lastChild === 'coloradj');
  await page.click('#coloradj-btn');   // leave it on sqrt, the default
  await page.waitForTimeout(900);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

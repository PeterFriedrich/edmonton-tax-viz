// Verify for the Tier-3 modifier pods (#lens + #coloradj) and the column that
// holds them. Both now HIDE in views where they have no effect rather than
// greying out — greyed #4a4a5e on a dark panel reads as *broken*, which
// produced a real bug report ("the highlight residential button doesn't work").
// #lens stopped greying 2026-07-25; #coloradj followed 2026-07-26, and because
// the column can now be entirely empty it collapses too (it was left as a
// visible gap by the Glass opacity-slider removal).
// Checks: #lens shows only in Money(neighbourhood)+Ratio, #coloradj only in
// Money+100m grid, each really clickable where shown, #opt-pres collapses where
// both hide, #layers still fills the panel there, and both pods' state survives
// a hide/show round-trip. Also the Colour label carries its own state.
//   node verify-lens-visibility.js <url>
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
  // Both Tier-3 pods plus the column that holds them. #coloradj joined #lens in
  // hiding on 2026-07-26, so the column can now be entirely empty and has to
  // collapse with them — probed here rather than in a second script that could
  // drift out of step with this one.
  const pods = () => page.evaluate(() => {
    const info = id => {
      const pod = document.getElementById(id), b = pod.querySelector('button');
      const r = b.getBoundingClientRect();
      const at = r.width ? document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) : null;
      return { shown: pod.offsetParent !== null, disabled: b.disabled,
               active: b.classList.contains('active'), hitIsBtn: at === b };
    };
    return { ...info('lens'), coloradj: info('coloradj'),
             presShown: document.getElementById('opt-pres').offsetParent !== null,
             layersShown: document.getElementById('layers').offsetParent !== null,
             res: state.residential, sqrt: state.colorAdjust, view: state.view };
  });
  const lens = pods;   // the pre-existing lens checks read the spread-in lens fields
  const goView = async v => {
    await page.click(`#views button[data-view="${v}"]`);
    await page.waitForTimeout(2500);
  };

  // --- Colour-scaling button: label is the readout, caption element is gone
  const cadj = await page.evaluate(() => {
    const b = document.getElementById('coloradj-btn');
    return { label: b.textContent.trim(), caption: !!document.getElementById('coloradj-state'),
             podW: +document.getElementById('coloradj').getBoundingClientRect().width.toFixed(0),
             panelW: +document.getElementById('optpanel').getBoundingClientRect().width.toFixed(0) };
  });
  console.log('coloradj  :', JSON.stringify(cadj));
  check('state caption element is gone', cadj.caption === false);
  check('label names the active scaling', cadj.label === 'Colour: sqrt scaling', cadj.label);
  check('pod no longer sticks out (was 417px)', cadj.podW < 220, `${cadj.podW}px`);
  await page.click('#coloradj-btn');
  await page.waitForTimeout(800);
  const off = await page.evaluate(() => {
    const b = document.getElementById('coloradj-btn');
    return { label: b.textContent.trim(), gold: b.classList.contains('active'),
             podW: +document.getElementById('coloradj').getBoundingClientRect().width.toFixed(0) };
  });
  check('label flips to "Colour: linear"', off.label === 'Colour: linear', off.label);
  check('gold clears when linear', off.gold === false);
  check('width does not jump between labels', off.podW === cadj.podW, `${off.podW} vs ${cadj.podW}`);
  await page.click('#coloradj-btn');
  await page.waitForTimeout(800);

  // --- lens: shown + live in Money
  const money = await lens();
  console.log('money     :', JSON.stringify(money));
  check('[money] lens shown', money.shown === true);
  check('[money] lens enabled', money.disabled === false);
  check('[money] lens hit-tests as itself', money.hitIsBtn === true);
  await page.click('#lens button');
  await page.waitForTimeout(1500);
  const on = await lens();
  check('[money] click toggles the lens on', on.res === true && on.active === true);

  // --- hidden in Money's 100 m grid (glass): the grid carries no res flag
  await page.click('#moneydetail button[data-moneydetail="grid"]');
  await page.waitForTimeout(3500);
  const grid = await lens();
  console.log('100m grid :', JSON.stringify(grid));
  check('[money/100m grid] lens hidden, not greyed', grid.shown === false, `view=${grid.view}`);
  check('[money/100m grid] lens also disabled', grid.disabled === true);
  await page.click('#moneydetail button[data-moneydetail="hood"]');
  await page.waitForTimeout(3000);
  const back = await lens();
  check('[money] lens returns, state survived the round-trip',
        back.shown === true && back.res === true && back.active === true);

  // --- hidden in every other visible view; shown in ratio
  // Expected per view: #lens bites in money+ratio, #coloradj in money+glass, so
  // the T3 column is EMPTY in services/uses/development and must collapse.
  const views = await page.evaluate(() =>
    [...document.querySelectorAll('#views button')].filter(b => b.offsetParent !== null)
      .map(b => b.dataset.view));
  console.log('views     :', views.join(', '));
  for (const v of views.filter(v => v !== 'money')) {
    await goView(v);
    const s = await lens();
    if (v === 'ratio') {
      check(`[${v}] lens shown + enabled`, s.shown === true && s.disabled === false);
      check(`[${v}] lens hit-tests as itself`, s.hitIsBtn === true);
    } else {
      check(`[${v}] lens hidden, not greyed`, s.shown === false && s.disabled === true);
    }
    // #coloradj drives the money/glass sqrt transform only.
    check(`[${v}] coloradj hidden, not greyed`,
          s.coloradj.shown === false && s.coloradj.disabled === true);
    const wantPres = v === 'ratio';
    check(`[${v}] T3 column ${wantPres ? 'stays open' : 'collapses (both pods hidden)'}`,
          s.presShown === wantPres);
    // Why #optpanel itself needs no collapse logic: every view with an empty T3
    // column still has a #layers section, so the panel is never wholly empty.
    // If this ever fails, #optpanel needs the same treatment as #opt-pres.
    if (!wantPres) check(`[${v}] Options panel still has content (#layers)`, s.layersShown === true);
  }
  await goView('money');
  const tour = await lens();
  check('[money] still live after the tour', tour.disabled === false);
  check('[money] coloradj live again after the tour', tour.coloradj.shown === true
        && tour.coloradj.disabled === false && tour.coloradj.hitIsBtn === true);
  check('[money] T3 column reopens', tour.presShown === true);

  // --- coloradj state survives the hide/show round-trip, like the lens does
  await page.click('#coloradj-btn');            // -> linear
  await page.waitForTimeout(1200);
  check('[money] switched to linear', (await lens()).sqrt === false);
  await goView('services');
  check('[services] coloradj hidden while linear is set', (await lens()).coloradj.shown === false);
  await goView('money');
  const rt = await lens();
  check('[money] linear survived the hide/show round-trip', rt.sqrt === false);
  check('[money] label still reads the restored state',
        (await page.textContent('#coloradj-btn')).trim() === 'Colour: linear');

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

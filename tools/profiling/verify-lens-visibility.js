// Verify for the residential-lens visibility rule + the Colour-scaling label
// (2026-07-25). The lens now HIDES in views where it has no effect instead of
// greying out (greyed read as broken — it was reported as "the highlight
// residential button doesn't work"). Checks: the lens shows ONLY in Money
// (neighbourhood) and Ratio, is really clickable and toggles there, is absent in
// Services / Development / Money's 100 m grid, and that lens state survives a
// hide/show round-trip. Also asserts the Colour button's label carries its own
// state (no separate caption element) and that the pod stopped sticking out.
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
  const lens = () => page.evaluate(() => {
    const pod = document.getElementById('lens'), b = pod.querySelector('button');
    const r = b.getBoundingClientRect();
    const at = r.width ? document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) : null;
    return { shown: pod.offsetParent !== null, disabled: b.disabled,
             active: b.classList.contains('active'), hitIsBtn: at === b,
             res: state.residential, view: state.view };
  });
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
  }
  await goView('money');
  check('[money] still live after the tour', (await lens()).disabled === false);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

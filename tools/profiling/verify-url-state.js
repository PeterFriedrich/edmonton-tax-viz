// Verify for the shareable URL hash (2026-09-28). The hash names the view on
// screen (`#view=development&metric=permits`), and restore may only select a
// control that is offered. What can go silently wrong:
//   * a control the hash writer does not cover — its state is lost on reload.
//     Caught by the ROUND TRIP: every offered control is clicked for real, the
//     hash read, a fresh page opened on it, and the two screens compared. It
//     walks the controls, not a key list, so a new control is covered unasked.
//   * a link reaching a state no button can (a full-only lens on the public
//     build, Change with no history file behind it).
//   * a bad value breaking the page or taking good keys down with it.
//   * the full build's <base href="../"> moving the address bar to the root.
//
// FALSIFIED 2026-09-28 — each defect was reintroduced and went red by name:
//   * relative replaceState("#…")   -> "<walk>: path is unchanged after writing"
//                                      (full build; every round trip)
//   * offered() always true          -> "#view=lab&cut=residential lands on"
//                                      and 6 more links a button cannot reach
//                                      (re-run 2026-09-29, after the change below)
//   * no metric revert when Change is
//     not offered                    -> "no history file: #mode=change lands on"
//   * `detail` dropped from urlHash() -> "round trip money > moneydetail…" and
//                                      both grid "lands on" links
//   * offered() hides #devmetric/#revcut
//     (both keys drop from every link) -> "round trip money > revcut…" and
//                                      "round trip development > devmetric…"
//
// What is on screen is decided by the browser (checkVisibility), NEVER by the
// page's own offered(): the hash writer and restore both lean on offered(), so
// a checker using it too walked 26 trips instead of 31 and passed while two
// keys vanished from every link (docs/FINDINGS_url_state.md F1).
// Runtime on the Oracle box: public ~3 min (31 trips), full ~6 min (58).
//
//   node verify-url-state.js <url>      (run once per build)
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

let failures = 0;
const check = (name, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) failures++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}: got ${JSON.stringify(got)}` +
              (ok ? '' : ` want ${JSON.stringify(want)}`));
};

// Not part of the URL by decision: the fold, the readout mode, the budget
// panel, and the opacity slider.
const SKIP = '#opt-fold, #hoodmode-btn, #budget-btn, #prism-opacity';

// A control's identity: its section and its data-* attributes — never its
// text, which can change after load (the 50 m button gains its file size at
// idle). NOT the view it sits in: that walked Money's controls again inside
// each grid, and leaving a grid page costs 10–25 s under software GL. The
// grid-only combinations are pinned as links below instead.
const IDENT = `el => el.closest('[id]').id + '|' + (el.id || JSON.stringify(
  Object.fromEntries(Object.entries(el.dataset).filter(([k]) => k !== 'tok')))
  + (el.closest('[data-service]') ? el.closest('[data-service]').dataset.service + '/' + el.type : ''))`;

// What a reader sees: the view, the title, and every offered control's state.
const screen = page => page.evaluate(skip => {
  const on = [...document.querySelectorAll('#controls button, #controls input')]
    .filter(el => !el.matches(skip) && el.checkVisibility())
    .filter(el => el.tagName === 'BUTTON' ? el.classList.contains('active') : el.checked)
    .map(el => (el.closest('[id]').id + ':' + (el.textContent.trim() ||
      el.closest('[data-service]')?.dataset.service + '/' + el.type)));
  return { view: state.view, title: document.getElementById('title-h').textContent, on };
}, SKIP);

(async () => {
  // A NEW BROWSER PER LOAD, and the old one SIGKILLed. Restore assumes it
  // starts from the defaults, so every load must be a cold one — and tearing
  // down a page that drew a grid frees its GPU buffers at ~10 s a time under
  // software GL (measured 2026-09-28; closing, reloading and navigating away
  // all pay it). Killing the process skips the teardown; relaunch is ~0.2 s.
  let server = null;
  const open = async (hash = '', { blockTemporal = false } = {}) => {
    if (server) await server.kill();
    server = await chromium.launchServer({
      args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
             '--ignore-gpu-blocklist', '--enable-webgl'],
    });
    const browser = await chromium.connect(server.wsEndpoint());
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    page.on('pageerror', e => { console.log('PAGE EXCEPTION:', e.message); failures++; });
    if (blockTemporal) await page.route('**/temporal.json', r => r.abort());
    await page.goto(url + hash, { waitUntil: 'networkidle', timeout: 60000 });
    await settle(page);
    return page;
  };
  const settle = async page => {
    // Timer polling: the default polls on rAF, which software GL starves.
    await page.waitForFunction(() => typeof state !== 'undefined' && state.data && !restoring,
                               null, { timeout: 60000, polling: 100 });
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(300);
  };
  const hashOf = page => page.evaluate(() => location.hash.replace(/^#/, ''));

  const home = await open();
  const FULL = await home.evaluate(() => FULL_BUILD);
  const path = await home.evaluate(() => location.pathname);
  console.log(`build: ${FULL ? 'full' : 'public'}  ${url}`);
  check('default view writes no hash', await home.evaluate(() => location.href.includes('#')), false);

  // --- round trip: every offered control, clicked for real ------------------
  // Each control is reached from a FRESH page by real clicks along a path, so
  // controls a click reveals (Change's window, the services colour radios,
  // Infill's amenity rows) are walked too. A control is identified by the view
  // it sits in plus its own attributes, and walked once per view.
  // JS .click(), the house convention (verify-controls-clickable.js owns
  // clickability): it fires the same bubbling click the hash listener hears,
  // without Playwright's stability wait, which costs ~4 s a click on the grid
  // under software GL.
  const keysOf = page => page.evaluate(([skip, ident]) => {
    const id = eval(ident);
    return [...document.querySelectorAll('#controls button, #controls input')]
      .filter(el => !el.matches(skip) && !el.closest('#views') && el.checkVisibility())
      // An active button in a group is a no-op; a lone toggle (the colour
      // scale, which is active by default) is not.
      .filter(el => !(el.tagName === 'BUTTON' && el.classList.contains('active')
                      && Object.keys(el.dataset).length))
      .map(id);
  }, [SKIP, IDENT]);
  const clickKey = async (page, key) => {
    const found = await page.evaluate(([skip, ident, key]) => {
      const id = eval(ident);
      const el = [...document.querySelectorAll('#controls button, #controls input')]
        .find(el => !el.matches(skip) && el.checkVisibility() && id(el) === key);
      if (el) el.click();
      return !!el;
    }, [SKIP, IDENT, key]);
    if (!found) throw new Error(`control vanished on replay: ${key}`);
    await settle(page);
  };
  const freshAt = async (v, path) => {
    const page = await open();
    await page.evaluate(v => document.querySelector(`#views button[data-view="${v}"]`).click(), v);
    await settle(page);
    for (const k of path) await clickKey(page, k);
    return page;
  };
  let trips = 0;
  const roundTrip = async (page, label) => {
    const want = await screen(page);
    const hash = await hashOf(page);
    check(`${label}: path is unchanged after writing`, await page.evaluate(() => location.pathname), path);
    const fresh = await open(hash ? '#' + hash : '');
    check(`round trip ${label} -> #${hash}`, await screen(fresh), want);
    check(`round trip ${label} rewrites the same hash`, await hashOf(fresh), hash);
    trips++;
  };
  const views = await home.evaluate(() => [...document.querySelectorAll('#views button')]
    .filter(b => b.checkVisibility()).map(b => b.dataset.view));
  for (const v of views) {
    const seen = new Set();
    const visit = async trail => {
      const page = await freshAt(v, trail);
      const next = (await keysOf(page)).filter(k => !seen.has(k));
      await roundTrip(page, [v, ...trail.map(k => k.replace('|', ':'))].join(' > '));
      next.forEach(k => seen.add(k));
      if (trail.length < 3) for (const k of next) await visit([...trail, k]);
    };
    await visit([]);
  }
  console.log(`(${trips} round trips)`);

  // --- links a button cannot reach, and bad values ---------------------------
  const lands = async (hash, wantHash, wantView, opts) => {
    const p = await open('#' + hash, opts);
    check(`${opts ? 'no history file: ' : ''}#${hash} lands on`,
          [await hashOf(p), await p.evaluate(() => state.view)], [wantHash, wantView]);
  };
  await lands('view=bogus', '', 'money');
  await lands('metric=__proto__&denom=constructor&scale=x&detail=toString', '', 'money');
  await lands('view=development&metric=bogus&window=3yr', 'view=development&window=3yr', 'development');
  await lands('view=services&on=constructor,roads&colour=__proto__', 'view=services', 'services');
  await lands('view=services&on=none', 'view=services&on=none', 'services');
  await lands('mode=change&window=short', 'mode=change&window=short', 'change');
  await lands('mode=change', '', 'money', { blockTemporal: true });
  await lands('detail=grid50&metric=value', 'metric=value&detail=grid50', 'glass');
  // Glass's denominator row is gated on the grid file's own lot column, which
  // exists only after the grid lands — the restore must wait for it.
  await lands('detail=grid&denom=lot&scale=linear', 'detail=grid&denom=lot&scale=linear', 'glass');
  if (!FULL) {
    for (const [h, want, v] of [
      ['view=uses&prisms=1', '', 'money'],
      ['view=lab&cut=residential', '', 'money'],
      ['view=development&metric=industrial', 'view=development', 'development'],
      ['view=development&mode=infill&amenity=lrt', 'view=development', 'development'],
      ['view=services&on=roads,fire,transit', 'view=services', 'services'],
      ['view=ratio&denom=fire', 'view=ratio', 'ratio'],
    ]) await lands(h, want, v);
  } else {
    await lands('view=uses&prisms=1', 'view=uses&prisms=1', 'uses');
    await lands('view=lab&cut=residential', 'view=lab&cut=residential', 'deviation');
    await lands('view=development&mode=infill&metric=industrial',
                'view=development&mode=infill', 'infill');
  }

  // An edited hash is honoured without a manual reload. A page on the
  // default, so this hash is a change and does fire hashchange.
  const edited = await open();
  await Promise.all([edited.waitForEvent('load'),
                     edited.evaluate(() => { location.hash = 'view=services&on=none'; })]);
  await settle(edited);
  check('an edited hash is applied', await edited.evaluate(() =>
    [state.view, Object.values(state.services).some(Boolean)]), ['services', false]);

  await server.kill();
  console.log(failures ? `\n${failures} FAILED` : '\nall passed');
  process.exit(failures ? 1 : 0);
})();

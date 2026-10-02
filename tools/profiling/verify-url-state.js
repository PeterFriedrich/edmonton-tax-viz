// Verify for the shareable URL hash (2026-09-28; behind a Copy link button
// since 2026-10-01). The hash names the view on screen
// (`#view=development&metric=permits`), the address bar stays clean, and
// restore may only select a control that is offered. What can go silently
// wrong:
//   * a control the hash writer does not cover — its state is lost on reload.
//     Caught by the ROUND TRIP: every offered control is clicked for real, the
//     hash read, a fresh page opened on it, and the two screens compared. It
//     walks the controls, not a key list, so a new control is covered unasked.
//   * a link reaching a state no button can (a full-only lens on the public
//     build, Change with no history file behind it).
//   * a bad value breaking the page or taking good keys down with it.
//   * the full build's <base href="../"> pointing the copied link at the root.
//   * a hash left in the address bar after restore, naming a view the reader
//     has since left.
//
// FALSIFIED 2026-09-28 — each defect was reintroduced and went red by name:
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
// FALSIFIED 2026-10-01, the Copy link button:
//   * link resolved against <base>   -> "<walk>: the link keeps the page's
//                                      path" (full build; every round trip)
//   * hash not removed after restore -> "<walk>: the address bar is clean
//                                      after restore" (every round trip)
//   * no address-bar fallback        -> "no clipboard: the link goes in the
//                                      address bar"
//
// FALSIFIED 2026-10-01, the frozen vocabulary (URL audit F2), with all 31
// public round trips still green under both mutants:
//   * URL_METRIC residential -> res  -> "frozen #metric=residential&… restores
//                                      to itself"
//   * SERVICES roadscost -> roadcost -> "frozen #view=services&on=roadscost…"
//     (a consistent internal rename)    and the three-service link
//
// The link is read from the real clipboard (the context grants
// clipboard-read), so the button's own path is what is tested.
//
//   node verify-url-state.js <url>      (run once per build)
//
// SHARDS (CI runs six in parallel, tests.yml `url-state`; 2026-10-02). With no
// flags it runs everything, as above. Optional:
//   --part=walk|links          only the round-trip walk, or only the links
//                              section (unreachable links, bad values, the
//                              frozen vocabulary, edited hash, no clipboard)
//   --views=a,b                walk only these views
//   --views-except=a,b         walk every offered view but these
// ⚠️ The catch-all shard is --views-except, so a view added later is walked
// unasked. A named view that is not offered is a FAIL, not an empty walk — a
// renamed view would otherwise drop out of CI silently.
const { chromium } = require('playwright');
const [url, ...flags] = process.argv.slice(2);
const flag = n => (flags.find(f => f.startsWith(`--${n}=`)) || '').slice(n.length + 3);
const PART = flag('part') || 'all';
const ONLY = flag('views') ? flag('views').split(',') : null;
const EXCEPT = flag('views-except') ? flag('views-except').split(',') : [];
const unknown = flags.filter(f => !/^--(part|views|views-except)=./.test(f));
if (unknown.length || !['all', 'walk', 'links'].includes(PART)) {
  console.error(`bad flags: ${flags.join(' ')}`);
  process.exit(2);
}

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
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 },
                                         permissions: ['clipboard-read', 'clipboard-write'] });
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
  // Pressing Copy link, and reading back what it put on the clipboard.
  const linkOf = async page => {
    await page.evaluate(() => navigator.clipboard.writeText(''));
    await page.evaluate(() => document.getElementById('share-btn').click());
    await page.waitForFunction(() => document.getElementById('share-btn').textContent === 'Link copied',
                               null, { timeout: 5000, polling: 50 });
    return page.evaluate(() => navigator.clipboard.readText());
  };
  const hashOf = async page => new URL(await linkOf(page)).hash.replace(/^#/, '');
  const barOf = page => page.evaluate(() => location.href.includes('#'));

  const home = await open();
  const FULL = await home.evaluate(() => FULL_BUILD);
  const path = await home.evaluate(() => location.pathname);
  console.log(`build: ${FULL ? 'full' : 'public'}  ${url}`);
  check('default view: the link carries no hash', (await linkOf(home)).includes('#'), false);

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
    check(`${label}: the address bar is clean after clicks`, await barOf(page), false);
    const link = await linkOf(page);
    const hash = new URL(link).hash.replace(/^#/, '');
    check(`${label}: the link keeps the page's path`, new URL(link).pathname, path);
    const fresh = await open(hash ? '#' + hash : '');
    check(`round trip ${label} -> #${hash}`, await screen(fresh), want);
    check(`round trip ${label}: the address bar is clean after restore`, await barOf(fresh), false);
    check(`round trip ${label} copies the same link`, await hashOf(fresh), hash);
    trips++;
  };
  const offeredViews = await home.evaluate(() => [...document.querySelectorAll('#views button')]
    .filter(b => b.checkVisibility()).map(b => b.dataset.view));
  for (const v of [...(ONLY || []), ...EXCEPT])
    check(`--views names an offered view: ${v}`, offeredViews.includes(v), true);
  const views = PART === 'links' ? [] : offeredViews.filter(
    v => (!ONLY || ONLY.includes(v)) && !EXCEPT.includes(v));
  if (PART !== 'links') check('the walk has a view to walk', views.length > 0, true);
  console.log(`walking: ${views.join(', ') || '(none)'}`);
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
  if (PART !== 'walk') {

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
    await lands('mode=change', '', 'money', { blockTemporal: true });
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
      await lands('view=development&mode=infill&metric=industrial',
                  'view=development&mode=infill', 'infill');
    }

    // --- the frozen vocabulary (URL audit F2) ----------------------------------
    // Every value a link can carry (CONTROLS_MATRIX §8), each in at least one
    // link that must restore to itself. The round trip above cannot see a
    // rename: the page writes the new name and reads it back. These links were
    // written by hand on 2026-10-01 and are what readers may hold.
    // ⚠️ A RED HERE MEANS A SHARED LINK BROKE. Don't edit the link to match:
    // add an alias that maps the old value to the new one (the rule beside
    // URL_METRIC), and give the entry its new expected link as a third element.
    // A retired value with nothing to map to moves to the expected-to-drop
    // links above instead.
    const norm = h => [...new URLSearchParams(h)].map(([k, v]) => `${k}=${v}`).sort().join('&');
    const FROZEN = [
      ['metric=residential&denom=lot&scale=linear', 'money'],
      // Glass's denominator row is gated on the grid file's own lot column,
      // which exists only after the grid lands — the restore must wait for it.
      ['metric=nonresidential&detail=grid&denom=lot&scale=linear', 'glass'],
      ['metric=value&detail=grid50', 'glass'],
      ['mode=change&window=short', 'change'],
      ['view=development&metric=permits&window=3yr&detail=hood', 'development'],
      ['view=development&window=5yr', 'development'],
      ['view=services&on=none', 'services'],
      ['view=services&on=roadscost', 'services'],
      ['view=services&on=roads,roadscost,roadslife&colour=roadslife', 'services'],
      ['view=ratio', 'ratio'],
    ];
    const FROZEN_FULL = [
      ['view=development&metric=industrial&window=3yr', 'development'],
      ['view=development&mode=infill&metric=permits&amenity=lrt,school', 'infill'],
      ['view=services&on=storm,fire,water,transit,bike,transitcost,bikecost&colour=bikecost', 'services'],
      ['view=ratio&denom=fire', 'ratio'],
      ['view=uses&prisms=1', 'uses'],
      ['view=lab&cut=residential', 'deviation'],
      ['view=lab&exp=deviation&cut=nonresidential', 'deviation', 'view=lab&cut=nonresidential'],
    ];
    for (const [h, view, want = h] of [...FROZEN, ...(FULL ? FROZEN_FULL : [])]) {
      const p = await open('#' + h);
      check(`frozen #${h} restores to itself`,
            [norm(await hashOf(p)), await p.evaluate(() => state.view)], [norm(want), view]);
    }

    // An edited hash is honoured without a manual reload. A page on the
    // default, so this hash is a change and does fire hashchange.
    const edited = await open();
    await Promise.all([edited.waitForEvent('load'),
                       edited.evaluate(() => { location.hash = 'view=services&on=none'; })]);
    await settle(edited);
    check('an edited hash is applied', await edited.evaluate(() =>
      [state.view, Object.values(state.services).some(Boolean)]), ['services', false]);

    // No clipboard (an insecure origin, a denied permission): the link must
    // still reach the reader, through the address bar. Reached by a CLICK, not
    // a restored hash: a hash that restore failed to remove passed this check
    // with the fallback deleted.
    const blind = await open();
    await blind.evaluate(() => document.querySelector('#views button[data-view="services"]').click());
    await settle(blind);
    await blind.evaluate(() => { navigator.clipboard.writeText = () => Promise.reject(new Error('denied')); });
    await blind.evaluate(() => document.getElementById('share-btn').click());
    await blind.waitForTimeout(300);
    check('no clipboard: the link goes in the address bar', await blind.evaluate(() =>
      [location.hash, document.getElementById('share-btn').textContent]),
      ['#view=services', 'Link in address bar']);
  }

  await server.kill();
  console.log(failures ? `\n${failures} FAILED` : '\nall passed');
  process.exit(failures ? 1 : 0);
})();

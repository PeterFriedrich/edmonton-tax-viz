// Verify the theme plumbing (light mode, phase 1 — docs/UI.md → Light mode →
// Build plan). Every backdrop-dependent colour is declared with themed() and
// read through tc(); a layer that captured a colour at build time, or whose
// accessor lacks state.theme in its updateTriggers, keeps drawing the DARK
// value after a theme switch, and nothing looks wrong until light ships.
//
// So the check does not wait for real light colours. It registers a sentinel
// theme (`__probe`) with a distinct colour for every THEMED entry, switches to
// it, and fails if any dark themed value is still in a layer's colour
// attributes or colour props, or in the legend. The probe theme also carries a
// one-colour ramp in THEME_RAMPS, so a ramp-coloured layer that kept the dark
// ramp fails the same way. Then it switches back and requires the dark colours
// to return exactly.
//
// Each state switches on what is off by default (labels, every service, both
// amenity bands, a selected hood) so the layers that carry those colours exist.
//   node verify-theme.js <base-url>   (the site root: checks index.html and dev-build-full/)
const { chromium } = require('playwright');
const [base] = process.argv.slice(2);
// The sentinel ramp (one colour), roof edge and backdrop the probe theme swaps in.
const PROBE_RAMP = [5, 250, 7], PROBE_EDGE = [9, 250, 9, 201], PROBE_BG = '#123456';

let fail = 0, ran = 0;
const check = (name, cond, extra) => {
  ran++;
  console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
  if (!cond) fail++;
};

const STATES = [
  ['index.html', ''],
  ['index.html', '#detail=grid'],
  ['index.html', '#mode=change'],
  ['index.html', '#view=development'],
  ['index.html', '#view=development&detail=hood'],
  ['index.html', '#view=services'],
  ['index.html', '#view=ratio'],
  ['dev-build-full/index.html', '#view=development&mode=infill&amenity=lrt,school'],
  ['dev-build-full/index.html', '#view=services&on=ALL'],
  ['dev-build-full/index.html', '#view=lab'],
  ['dev-build-full/index.html', '#view=uses&prisms=1'],
];

// Every RGB(A) tuple in use: colour attributes (deduped) and colour/material props.
const collect = page => page.evaluate(() => {
  const seen = new Map();   // "r,g,b,a" -> Set(layer ids)
  const add = (t, id) => { const k = t.join(','); (seen.get(k) || seen.set(k, new Set()).get(k)).add(id); };
  const walk = (v, id) => {
    if (Array.isArray(v) && (v.length === 3 || v.length === 4) && v.every(x => typeof x === 'number')) add(v, id);
    else if (v && typeof v === 'object' && !ArrayBuffer.isView(v)) for (const x of Object.values(v)) walk(x, id);
  };
  for (const l of overlay._deck.layerManager.getLayers()) {
    const am = l.getAttributeManager && l.getAttributeManager();
    if (am) for (const [k, a] of Object.entries(am.attributes)) {
      if (!/olor/i.test(k) || /Picking|ColorModes/.test(k) || !a.value || !a.value.length) continue;
      const n = a.size || 4, scale = a.value instanceof Float32Array ? 255 : 1;
      // Only the drawn part: a reused buffer keeps the previous data's values
      // past numInstances (the selected-hood prism carried money-view colours
      // into Change and Ratio, S218).
      const end = Math.min(a.value.length, l.getNumInstances() * n);
      for (let i = 0; i + n <= end; i += n)
        add(Array.from(a.value.slice(i, i + n), x => Math.round(x * scale)), l.id);
    }
    for (const [k, v] of Object.entries(l.props))
      if (/olor|material/i.test(k) && v != null && typeof v !== 'function') walk(v, l.id);
  }
  const out = {};
  for (const [k, ids] of seen) out[k] = [...ids];
  return { colours: out, legend: document.getElementById('legend').innerHTML };
});

// A dark themed value matches a tuple when RGB agree and (for RGBA values) alpha too.
const hits = (darks, colours) => {
  const found = [];
  for (const d of darks) for (const [k, ids] of Object.entries(colours)) {
    const t = k.split(',').map(Number);
    if (!(t[0] === d[0] && t[1] === d[1] && t[2] === d[2] && (d.length === 3 || t[3] === d[3]))) continue;
    // Opaque black is also deck's default for every unused colour channel, so
    // the dark label outline (the one themed opaque black) is looked for only
    // in the label layers.
    const where = d.join() === '0,0,0,255' ? ids.filter(id => /label/.test(id)) : ids;
    if (where.length) found.push(`${d.join(',')} in ${where.slice(0, 3).join('/')}`);
  }
  return found;
};

// What a reader meets (light mode phases 5–6): the theme chosen before first
// paint, the OS followed live until a choice is stored, the stored choice
// winning after a reload, Glow leaving with the dark theme, and no blurb saying
// "brighter" where the high end is darker. Automation is pinned to dark unless
// a choice is stored, so the OS path runs with navigator.webdriver unset, as
// verify-guide.js does.
async function readerPaths() {
  const b = await chromium.launch();
  const ready = async p => {
    await p.waitForFunction(() => document.getElementById('loading').hidden, null, { timeout: 60000 });
    await p.waitForTimeout(1500);
  };
  const theme = p => p.evaluate(() => [document.documentElement.dataset.theme, state.theme,
    map.getPaintProperty('bg', 'background-color')].join(' '));
  const lightBg = 'light light #f7f7f4', darkBg = 'dark dark #0a0a0f';

  let ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, colorScheme: 'light' });
  let page = await ctx.newPage();
  await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' }); await ready(page);
  check('reader: automation on a light OS gets dark', await theme(page) === darkBg, await theme(page));
  await ctx.close();

  ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, colorScheme: 'light' });
  await ctx.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => false }));
  page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' }); await ready(page);
  check('reader: a light OS opens in light', await theme(page) === lightBg, await theme(page));
  check('reader: the landing blurb says darker', await page.evaluate(() =>
    !/bright/i.test(document.getElementById('title-p').textContent) &&
    /darker/.test(document.getElementById('title-p').textContent)));
  check('reader: the guide card says darker', await page.evaluate(() =>
    [...document.querySelectorAll('.more-word')].every(s => s.textContent === 'darker')));
  await page.emulateMedia({ colorScheme: 'dark' }); await page.waitForTimeout(1500);
  check('reader: an OS switch is followed live', await theme(page) === darkBg, await theme(page));
  check('reader: back in dark the blurb says brighter', await page.evaluate(() =>
    /brighter/i.test(document.getElementById('title-p').textContent)));

  await page.click('#a11y-btn');
  await page.evaluate(() => applyPalette('glow'));
  await page.click('#theme button[data-pick="light"]'); await page.waitForTimeout(1500);
  check('reader: the Light button switches', await theme(page) === lightBg, await theme(page));
  check('reader: Glow gives way to Inferno in light', await page.evaluate(() =>
    state.ramp === 'current' &&
    document.querySelector('#palette button[data-ramp="current"]').classList.contains('active') &&
    getComputedStyle(document.querySelector('#palette button[data-ramp="glow"]')).display === 'none'));
  check('reader: the Light button is marked', await page.evaluate(() =>
    document.querySelector('#theme button[data-pick="light"]').classList.contains('active') &&
    !document.querySelector('#theme button[data-pick="dark"]').classList.contains('active')));
  await page.reload({ waitUntil: 'networkidle' }); await ready(page);
  check('reader: the choice beats a dark OS after a reload', await theme(page) === lightBg, await theme(page));
  await page.emulateMedia({ colorScheme: 'light' }); await page.emulateMedia({ colorScheme: 'dark' });
  await page.waitForTimeout(1000);
  check('reader: with a choice stored, an OS switch is ignored', await theme(page) === lightBg, await theme(page));

  // Every public blurb family, in 3D and 2D, rendered in light.
  for (const hash of ['', '#detail=grid', '#mode=change', '#view=development', '#view=development&detail=hood',
                      '#view=services', '#view=services&on=roadscost', '#view=services&on=roadslife', '#view=ratio']) {
    await page.goto(`${base}/index.html${hash}`, { waitUntil: 'networkidle' }); await ready(page);
    for (const pitch of [null, 0]) {
      if (pitch === 0) { await page.evaluate(() => map.jumpTo({ pitch: 0 })); await page.waitForTimeout(800); }
      const text = await page.evaluate(() => document.getElementById('title-p').textContent);
      check(`reader: light ${hash || '(default)'}${pitch === 0 ? ' 2D' : ''} blurb never says brighter`,
        !/bright/i.test(text), text.match(/.{0,30}bright.{0,20}/i)?.[0]);
    }
  }
  check('reader: no page errors', !errors.length, errors.join('; '));
  await b.close();
}

(async () => {
  const covered = new Set();
  let allDarks = [];
  for (const [page_, hash] of STATES) {
    const b = await chromium.launch();
    const page = await (await b.newContext({ viewport: { width: 1280, height: 800 } })).newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    let h = hash;
    if (h.includes('on=ALL')) {
      // Every service key, read from the page itself so a new service is covered.
      await page.goto(`${base}/${page_}`, { waitUntil: 'networkidle' });
      await page.waitForFunction(() => document.getElementById('loading').hidden, null, { timeout: 60000 });
      h = h.replace('ALL', await page.evaluate(() => Object.keys(SERVICES).join(',')));
    }
    await page.goto(`${base}/${page_}${h}`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.getElementById('loading').hidden, null, { timeout: 60000 });
    await page.waitForTimeout(2500);
    const tag = `${page_.startsWith('dev') ? 'full' : 'public'} ${hash || '(default)'}`;
    await page.evaluate(() => {
      applyLabels(true);
      searchHood = state.data.features.find(f => !f.properties.is_set_aside).properties.neighbourhood_name;
      overlay.setProps({ layers: buildLayers() });
    });
    await page.waitForTimeout(2000);

    const darks = await page.evaluate(() => THEMED.map(c => c.dark));
    const before = await collect(page);
    const present = hits(darks, before.colours);
    allDarks = darks;
    for (const x of present) covered.add(x.split(' in ')[0]);
    check(`${tag}: dark themed colours are on screen to test`, present.length > 0, `${present.length} found`);

    // Every colour the dark ramp can produce, and its roof edge (RGB only:
    // layers append their own alpha).
    const rampDark = new Set(await page.evaluate(() => {
      const s = new Set([activeRamp().edge.slice(0, 3).join()]);
      for (let i = 0; i <= 1000; i++) s.add(rampColorAt(i / 1000).join());
      return [...s];
    }));
    const rgbIn = colours => Object.keys(colours).filter(k => rampDark.has(k.split(',').slice(0, 3).join()));
    const rampBefore = rgbIn(before.colours);

    await page.evaluate(([ramp, edge, bg]) => {
      THEMED.forEach((c, i) => {
        c.__probe = [(37 * i + 11) % 256, 3, 251];
        if (c.dark.length === 4) c.__probe.push(c.dark[3]);
      });
      // A one-colour ramp: any dark ramp colour still drawn after the switch
      // is a layer that did not re-read activeRamp().
      THEME_RAMPS.__probe = { current: { bg, edge, stops: [[0, ramp], [1, ramp]] } };
      applyTheme('__probe');
    }, [PROBE_RAMP, PROBE_EDGE, PROBE_BG]);
    await page.waitForTimeout(2000);
    const probe = await collect(page);
    const left = hits(darks, probe.colours);
    check(`${tag}: no dark themed colour survives the switch`, !left.length, left.slice(0, 6).join('; '));
    if (rampBefore.length) {
      const rampLeft = rgbIn(probe.colours).filter(k => rampBefore.includes(k));
      check(`${tag}: no dark ramp colour survives the switch`, !rampLeft.length,
        rampLeft.slice(0, 4).map(k => `${k} in ${probe.colours[k].slice(0, 3).join('/')}`).join('; '));
      check(`${tag}: the theme's ramp is drawn`, Object.keys(probe.colours).some(k => k.startsWith(PROBE_RAMP.join() + ',')));
    }
    check(`${tag}: the backdrop follows the theme`,
      await page.evaluate(() => map.getPaintProperty('bg', 'background-color')) === PROBE_BG);
    const swatch = await page.evaluate(() => `rgb(${SET_ASIDE_COLOR.dark.join(',')})`);
    if (before.legend.includes(swatch))
      check(`${tag}: the legend's set-aside swatch follows the theme`, !probe.legend.includes(swatch));

    await page.evaluate(() => applyTheme('dark'));
    await page.waitForTimeout(2000);
    const back = await collect(page);
    const lost = present.filter(x => !hits(darks, back.colours).includes(x));
    check(`${tag}: switching back restores every dark colour`, !lost.length, lost.slice(0, 4).join('; '));
    check(`${tag}: no page errors`, !errors.length, errors.join('; '));
    await b.close();
  }
  // A themed colour no state draws is one this check never tested.
  // Named exemptions, each with the reason it cannot be drawn here. A new
  // themed colour that no state draws fails until it is drawn or listed.
  const UNDRAWN = {
    '88,90,102': 'Uses "Unclassified": no zoning feature carries it today',
    '70,72,84': 'unzoned revenue share: HTML panel only, never a layer',
    '166,140,108,230': 'zone-name labels: same tc(d.col) path as the three tiers drawn here',
  };
  const unseen = [...new Set(allDarks.map(d => d.join(',')))].filter(k => !covered.has(k));
  for (const k of unseen.filter(k => UNDRAWN[k])) console.log(`NOTE  not drawn: ${k} (${UNDRAWN[k]})`);
  const missing = unseen.filter(k => !UNDRAWN[k]);
  check('every themed colour is drawn in at least one state, or named as undrawable', !missing.length, missing.join('; '));
  await readerPaths();
  console.log(`\n${ran - fail}/${ran} passed`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });

// Verify the theme plumbing (light mode, phase 1 — docs/UI.md → Light mode →
// Build plan). Every backdrop-dependent colour is declared with themed() and
// read through tc(); a layer that captured a colour at build time, or whose
// accessor lacks state.theme in its updateTriggers, keeps drawing the DARK
// value after a theme switch, and nothing looks wrong until light ships.
//
// So the check does not wait for real light colours. It registers a sentinel
// theme (`__probe`) with a distinct colour for every THEMED entry, switches to
// it, and fails if any dark themed value is still in a layer's colour
// attributes or colour props, or in the legend. Then it switches back and
// requires the dark colours to return exactly.
//
// Each state switches on what is off by default (labels, every service, both
// amenity bands, a selected hood) so the layers that carry those colours exist.
//   node verify-theme.js <base-url>   (the site root: checks index.html and dev-build-full/)
const { chromium } = require('playwright');
const [base] = process.argv.slice(2);

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
      for (let i = 0; i + n <= a.value.length; i += n)
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

    await page.evaluate(() => {
      THEMED.forEach((c, i) => {
        c.__probe = [(37 * i + 11) % 256, 3, 251];
        if (c.dark.length === 4) c.__probe.push(c.dark[3]);
      });
      applyTheme('__probe');
    });
    await page.waitForTimeout(2000);
    const probe = await collect(page);
    const left = hits(darks, probe.colours);
    check(`${tag}: no dark themed colour survives the switch`, !left.length, left.slice(0, 6).join('; '));
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
  console.log(`\n${ran - fail}/${ran} passed`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });

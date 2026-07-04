// One-off verify for the Glass view (2026-07-04). DOM + layer checks:
// layer stack (opaque neutral plane under translucent metric prisms),
// plane fills (neutral vs set-aside), prism opacity follows the slider and
// each ghost view's default, metric toggle renders live with a metric-driven
// title + the glass blurb, residential lens applies, labels ride the prism
// roofs, tooltip falls through to the money branch.
//   node verify-glass.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  // swiftshader can hang page.click while the render loop is busy — dispatch
  // the click from inside the page instead (same workaround as verify-labels).
  const click = sel => page.$eval(sel, b => b.click());

  const chrome = () => page.evaluate(() => ({
    view: state.view,
    title: document.getElementById('title-h').textContent,
    blurbIsGlass: document.getElementById('title-p').textContent === VIEWS.glass.blurb,
    label: document.getElementById('legend-label').textContent,
    max: document.getElementById('legend-max').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    sliderShown: getComputedStyle(document.getElementById('layers')).display !== 'none',
    sliderPct: document.getElementById('prism-opacity').value,
    lensDisabled: document.querySelector('#lens button').disabled,
  }));

  console.log('money default  :', JSON.stringify(await chrome()));

  await click('#views button[data-view="glass"]');
  await page.waitForTimeout(2500);
  console.log('glass          :', JSON.stringify(await chrome()));

  // Layer stack + plane fills. The plane must be flat, opaque-ish, pickable;
  // the prisms extruded, translucent at the view default, not pickable.
  const stack = await page.evaluate(() => {
    const layers = overlay._deck.props.layers.map(l => l.id);
    const plane = overlay._deck.props.layers.find(l => l.id === 'glass-plane');
    const prisms = overlay._deck.props.layers.find(l => l.id === 'glass-extrusion');
    let neutral = 0, aside = 0, bad = 0;
    for (const f of state.data.features) {
      const fill = plane.props.getFillColor(f).join();
      if (f.properties.is_set_aside) fill === SET_ASIDE_COLOR.join() ? aside++ : bad++;
      else fill === GLASS_PLANE_COLOR.join() ? neutral++ : bad++;
    }
    return { layers,
             planeFlat: !plane.props.extruded, planePickable: !!plane.props.pickable,
             prismsExtruded: !!prisms.props.extruded, prismsPickable: !!prisms.props.pickable,
             prismOpacity: prisms.props.opacity,
             nHoods: state.data.features.length, neutral, aside, bad };
  });
  console.log('stack + plane  :', JSON.stringify(stack));

  // Slider drives prism opacity live.
  await page.evaluate(() => {
    const el = document.getElementById('prism-opacity');
    el.value = 60; el.dispatchEvent(new Event('input'));
  });
  await page.waitForTimeout(500);
  const after = await page.evaluate(() =>
    overlay._deck.props.layers.find(l => l.id === 'glass-extrusion').props.opacity);
  console.log('slider -> 60   :', JSON.stringify({ prismOpacity: after }));

  // Metric toggle renders live in glass: metric title, glass blurb kept.
  await click('#toggle button[data-metric="value_per_acre"]');
  await page.waitForTimeout(1000);
  console.log('glass + value  :', JSON.stringify(await chrome()));
  await click('#toggle button[data-metric="revenue_per_acre"]');
  await page.waitForTimeout(1000);

  // Residential lens applies to the prisms (fade fill for non-res).
  await click('#lens button');
  await page.waitForTimeout(1000);
  const lens = await page.evaluate(() => {
    const prisms = overlay._deck.props.layers.find(l => l.id === 'glass-extrusion');
    const nonRes = state.data.features.find(f => !f.properties.is_residential && !f.properties.is_set_aside);
    const res = state.data.features.find(f => f.properties.is_residential);
    return { residential: state.residential,
             nonResFill: prisms.props.getFillColor(nonRes),
             resKeepsColour: prisms.props.getFillColor(res).join() !==
                             [...LENS_FADE_COLOR, LENS_FADE_ALPHA].join() };
  });
  console.log('lens on        :', JSON.stringify(lens), '|', JSON.stringify(await chrome()));
  await click('#lens button');
  await page.waitForTimeout(500);

  // Labels ride the prism roofs (money-style labelZ).
  await click('#lens button[data-lens="labels"]');
  await page.waitForTimeout(1500);
  const labels = await page.evaluate(() => {
    const present = overlay._deck.props.layers.some(l => l.id === 'hood-labels');
    const cfg = METRICS[state.metric];
    const f = state.data.features.find(f => f.properties.neighbourhood_name === 'DOWNTOWN').properties;
    return { present, roofZOk: Math.abs(labelZ(f) - (f[cfg.key] * cfg.elevationScale + 60)) < 1e-6 };
  });
  console.log('labels         :', JSON.stringify(labels));
  await click('#lens button[data-lens="labels"]');
  await page.waitForTimeout(500);

  // Tooltip falls through to the money branch (metric + road lines).
  const tip = await page.evaluate(() => {
    const f = state.data.features.find(f => f.properties.neighbourhood_name === 'STRATHCONA');
    return tooltipFor({ object: f }).html;
  });
  console.log('tooltip        :', tip);

  // Leaving: money restores opaque pickable prisms + metric blurb; entering
  // ratio resets the slider to ITS default (5), glass again -> 30.
  await click('#views button[data-view="money"]');
  await page.waitForTimeout(1500);
  console.log('back to money  :', JSON.stringify(await chrome()));
  await click('#views button[data-view="ratio"]');
  await page.waitForTimeout(2500);
  console.log('ratio slider   :', JSON.stringify(await chrome()));
  await click('#views button[data-view="glass"]');
  await page.waitForTimeout(1500);
  console.log('glass again    :', JSON.stringify(await chrome()));

  await browser.close();
})();

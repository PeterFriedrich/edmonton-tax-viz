// One-off verify for the ratio-view residential lens (2026-07-03).
// Checks legend anchors/swatch across view+lens combinations and the
// lens-button disable in Roads. DOM-level — see shot-click.js for pixels.
//   node verify-lens.js <url>
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

  const legend = () => page.evaluate(() => ({
    label: document.getElementById('legend-label').textContent,
    min: document.getElementById('legend-min').textContent,
    max: document.getElementById('legend-max').textContent,
    aside: document.querySelector('#legend .aside span:last-child').textContent,
    residential: state.residential,
    view: state.view,
    lensDisabled: document.querySelector('#lens button').disabled,
  }));

  console.log('money, lens off:', JSON.stringify(await legend()));

  await page.click('#views button[data-view="ratio"]');
  await page.waitForTimeout(5000); // roads lazy-fetch + rebuild
  console.log('ratio, lens off:', JSON.stringify(await legend()));

  await page.click('#lens button');
  await page.waitForTimeout(1500);
  console.log('ratio, lens ON :', JSON.stringify(await legend()));

  // fill colours under the lens: a non-residential kept hood must be the fade
  // grey; a residential kept hood must carry a ramp colour.
  const fills = await page.evaluate(() => {
    const layer = overlay._deck.layerManager.layers.find(l => l.id === 'ratio-extrusion');
    const getFill = layer.props.getFillColor;
    const feats = state.data.features;
    const pick = pred => feats.find(f => ratioKept(f.properties) && pred(f.properties));
    return {
      nonRes: getFill(pick(p => !p.is_residential)),
      res: getFill(pick(p => p.is_residential)),
    };
  });
  console.log('ratio fills, lens ON:', JSON.stringify(fills));

  await page.click('#views button[data-view="roads"]');
  await page.waitForTimeout(2000);
  console.log('roads          :', JSON.stringify(await legend()));

  await page.click('#views button[data-view="money"]');
  await page.waitForTimeout(2000);
  console.log('money, lens ON :', JSON.stringify(await legend()));

  await browser.close();
})();

// Screenshot one web tree at several sizes and themes, for a before/after.
// Serves --root itself (node http, port 0), so there is no python server to
// pick, wedge or pkill. One browser per shot, SIGKILLed after, because a
// graceful close after a grid page costs 10-30 s under SwiftShader.
//
// NODE_PATH=/home/opc/edmonton-tax-viz/tools/profiling/node_modules \
//   node render.js --root <dir> --out <dir> --label before \
//     [--page index.html] [--size 360x780,800x900,1280x800] [--theme dark,light]
//     [--hash 'view=development&window=3yr'] [--js '<async expr after ready>']
//     [--settle 1500] [--touch auto|on|off]
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const opt = { page: 'index.html', size: '360x780,800x900,1280x800', theme: 'dark,light',
              hash: '', js: '', settle: '1500', touch: 'auto' };
const argv = process.argv.slice(2);
for (let i = 0; i < argv.length; i += 2) opt[argv[i].replace(/^--/, '')] = argv[i + 1];
if (!opt.root || !opt.out || !opt.label) {
  console.error('need --root, --out and --label'); process.exit(2);
}
const root = path.resolve(opt.root);
if (!fs.existsSync(path.join(root, opt.page))) {
  console.error(`no ${opt.page} under ${root}`); process.exit(2);
}
fs.mkdirSync(opt.out, { recursive: true });

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.geojson': 'application/geo+json', '.png': 'image/png',
  '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.txt': 'text/plain' };
const server = http.createServer((req, res) => {
  const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '') || opt.page;
  const file = path.join(root, rel);
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404); return res.end();
  }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

const ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
              '--ignore-gpu-blocklist', '--enable-webgl'];

async function shot(base, w, h, theme) {
  const bs = await chromium.launchServer({ args: ARGS });
  const errors = [];
  let ready = true;
  try {
    const browser = await chromium.connect(bs.wsEndpoint());
    const touch = opt.touch === 'on' || (opt.touch === 'auto' && w < 641);
    const page = await browser.newPage({ viewport: { width: w, height: h },
                                         hasTouch: touch, isMobile: touch });
    page.on('pageerror', e => errors.push(e.message));
    // The page reads its theme from localStorage before first paint.
    await page.addInitScript(t => { try { localStorage.setItem('theme', t); } catch (e) {} }, theme);
    await page.goto(base + (opt.hash ? '#' + opt.hash : ''), { waitUntil: 'networkidle', timeout: 90000 });
    // #loading is hidden once data and map are both up (hideLoading()).
    await page.waitForFunction(() => {
      const el = document.getElementById('loading');
      return !el || el.hidden || getComputedStyle(el).display === 'none';
    }, null, { timeout: 90000 }).catch(() => { ready = false; });
    if (opt.js) await page.evaluate(`(async () => { ${opt.js} })()`);
    await page.waitForTimeout(Number(opt.settle));
    const file = path.join(opt.out, `${opt.label}_${w}x${h}_${theme}.png`);
    await page.screenshot({ path: file });
    console.log(JSON.stringify({ file, w, h, theme, touch, ready, errors }));
  } finally {
    await bs.kill();
  }
}

server.listen(0, '127.0.0.1', async () => {
  const base = `http://127.0.0.1:${server.address().port}/${opt.page}`;
  let bad = 0;
  try {
    for (const s of opt.size.split(',')) {
      const [w, h] = s.split('x').map(Number);
      for (const t of opt.theme.split(',')) {
        try { await shot(base, w, h, t); }
        catch (e) { bad++; console.log(JSON.stringify({ w, h, theme: t, error: e.message })); }
      }
    }
  } finally {
    server.close();
    process.exit(bad ? 1 : 0);
  }
});

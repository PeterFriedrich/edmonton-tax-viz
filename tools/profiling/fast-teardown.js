// Preload for the verify runner: one browser PROCESS per page/context,
// SIGKILLed on close. verify.js injects it with `NODE_OPTIONS=--require`.
//
// Why: after a page has drawn a grid, Chromium's graceful close does not skip
// the GPU teardown, it DEFERS it — page.close() returns in 0.01 s and the next
// newPage() pays 6–8 s; a final browser.close() paid 30 s after 4 grid pages.
// That was 31% of the suite. Killing a process pays nothing, and no page ever
// inherits a predecessor's teardown. Measured 82 → 57 min, 90/90 statuses and
// check counts unchanged (docs/FINDINGS_verify_runtime.md §2).
//
// A preload rather than an edit to each script: the scripts stay runnable on
// their own, and one file is one place to be wrong. It works because every
// script's require('playwright') resolves to this directory's node_modules, the
// same cached module this patches. verify-url-state.js already does this by
// hand via launchServer, which is left unpatched.
const pw = require('playwright');

const launchServer = pw.chromium.launchServer.bind(pw.chromium);
pw.chromium.launch = async (opts = {}) => {
  const servers = [];
  const spawn = async () => {
    const s = await launchServer(opts);
    servers.push(s);
    return { s, b: await pw.chromium.connect(s.wsEndpoint()) };
  };
  const base = await spawn();
  return new Proxy(base.b, { get(t, k) {
    if (k === 'newPage') return async o => {
      const { s, b } = await spawn();
      const p = await b.newPage(o);
      p.close = async () => { await s.kill(); };
      return p;
    };
    if (k === 'newContext') return async o => {
      const { s, b } = await spawn();
      const c = await b.newContext(o);
      c.close = async () => { await s.kill(); };
      return c;
    };
    if (k === 'close') return async () => { await Promise.all(servers.map(s => s.kill())); };
    const v = t[k];
    return typeof v === 'function' ? v.bind(t) : v;
  }});
};

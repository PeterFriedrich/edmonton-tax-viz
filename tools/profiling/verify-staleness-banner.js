// Verify the client-side staleness banner (P2.2, 2026-07-26).
//
// The failure this guards: the weekly refresh stops (GitHub auto-disables cron
// workflows after 60 idle days, or the heartbeat PAT expires) and the public
// site serves frozen data with a clean UI forever. Nothing is left server-side
// to set a banner in that world, so the page ages status.json's own
// `last_checked` and raises the banner itself past STALE_DAYS (14).
//
// status.json is intercepted per-case, so this never touches the real manifest
// and the assertions do not rot as the committed date moves.
//   node tools/profiling/verify-staleness-banner.js <url>     (from REPO ROOT)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [url] = process.argv.slice(2);

const STALE_DAYS = 14;
// UTC date string N days back. The page floors (now - midnight(date))/1d, so
// daysAgo(N) reads back as exactly N regardless of the time of day this runs.
const daysAgo = n => new Date(Date.now() - n * 86400000).toISOString().slice(0, 10);

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  // Load the map with status.json replaced by `manifest` (or aborted when null)
  // and report what the banner did. Vintages come back too: a stale manifest
  // must still populate the sources pod, not trade one feature for the other.
  const load = async manifest => {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.route('**/data/status.json*', r =>
      manifest === null
        ? r.abort()
        : r.fulfill({ status: 200, contentType: 'application/json',
                      body: JSON.stringify(manifest) }));
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3500);
    const out = await page.evaluate(() => {
      const b = document.getElementById('banner');
      return {
        shown: getComputedStyle(b).display !== 'none',
        text: b.textContent,
        vintage: (document.getElementById('about-vintage') || {}).textContent || '',
        // `state` is a top-level const, so it is NOT on window — reference it
        // bare and let the try/catch cover the not-yet-loaded case.
        features: (() => { try { return state.data.features.length; } catch { return 0; } })(),
      };
    });
    await page.close();
    return out;
  };

  const base = { data_year: 2025, rate_year: 2025, zoning_year: 2024,
                 generated: daysAgo(20), banner: null };

  // --- The tunable itself is part of the contract
  const src = fs.readFileSync(path.join(__dirname, '..', '..', 'web', 'index.html'), 'utf8');
  const m = src.match(/const STALE_DAYS = (\d+);/);
  check('STALE_DAYS is declared and is 14', m && +m[1] === STALE_DAYS,
        m ? `(found ${m[1]})` : '(not found)');

  // --- Fresh manifest: silent
  const fresh = await load({ ...base, last_checked: daysAgo(0) });
  check('fresh manifest (checked today) shows NO banner', fresh.shown === false,
        fresh.shown ? `text="${fresh.text}"` : '');
  check('fresh manifest still renders the map', fresh.features > 0,
        `(${fresh.features} features)`);

  // --- Boundary: 13 days quiet, 14 days speaks
  const day13 = await load({ ...base, last_checked: daysAgo(STALE_DAYS - 1) });
  check(`${STALE_DAYS - 1} days old is still quiet (one missed weekly run)`,
        day13.shown === false, day13.shown ? `text="${day13.text}"` : '');

  const day14 = await load({ ...base, last_checked: daysAgo(STALE_DAYS) });
  check(`${STALE_DAYS} days old RAISES the banner`, day14.shown === true);
  check(`${STALE_DAYS}-day banner names the date and the age`,
        day14.text.includes(daysAgo(STALE_DAYS)) && /14 days ago/.test(day14.text),
        `text="${day14.text}"`);
  check('stale banner still says the map works', /still works/i.test(day14.text));
  check('stale manifest STILL populates the sources-pod vintages',
        /assessment 2025/.test(day14.vintage), `vintage="${day14.vintage}"`);

  const old = await load({ ...base, last_checked: daysAgo(400) });
  check('400 days old raises the banner', old.shown === true);
  check('400-day banner reports the real age', /400 days ago/.test(old.text),
        `text="${old.text}"`);

  // --- A backend banner is more specific and must win
  const held = await load({ ...base, last_checked: daysAgo(90),
                            banner: 'Showing 2025 data — 2026 rates not published yet.' });
  check('backend banner WINS over staleness (year-hold message survives)',
        held.text === 'Showing 2025 data — 2026 rates not published yet.',
        `text="${held.text}"`);

  // --- Every uncertain input must stay silent rather than invent a warning
  const noField = await load({ ...base });
  check('manifest with NO last_checked shows no banner', noField.shown === false,
        noField.shown ? `text="${noField.text}"` : '');

  const garbage = await load({ ...base, last_checked: 'not-a-date' });
  check('unparseable last_checked shows no banner', garbage.shown === false,
        garbage.shown ? `text="${garbage.text}"` : '');

  // Visitor's clock behind the build date: not staleness, must not warn.
  const future = await load({ ...base, last_checked: daysAgo(-30) });
  check('FUTURE last_checked (clock skew) shows no banner', future.shown === false,
        future.shown ? `text="${future.text}"` : '');

  const gone = await load(null);
  check('unreachable status.json shows no banner', gone.shown === false,
        gone.shown ? `text="${gone.text}"` : '');
  check('unreachable status.json still renders the map', gone.features > 0,
        `(${gone.features} features)`);

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();

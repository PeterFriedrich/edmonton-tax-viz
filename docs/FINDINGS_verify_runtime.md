# Findings — pre-merge verify runtime (S206, 2026-09-29)

Peter's ask (S205): *does the verify step before a PR need to take this long?*
Opus 5.5, `xhigh`. Everything below was measured on the Oracle box, running one
script at a time, against a fresh `build_site.py` output.

## 0. The answer

- **Nothing browser-driven gates a merge.** The merge gate is `tests.yml`: pytest
  (~16 s) plus four offline Python guards. `deploy.yml` runs `verify-smoke.js`
  (both builds) and `verify-blurbs.js` (public), and those gate only the
  **publish**. Every other `verify-*.js` minute is paid by a session out of
  habit.
- **The whole suite takes 82 min on this box**: 38.2 min on the public build
  and 43.7 min on the full build. Nobody should run it per PR, and nobody does.
- **31% of that is one avoidable cost:** GPU teardown under software GL, charged
  when a browser is closed gracefully (§2). A runner-level fix removes it
  without editing any check. Measured with a preload: **82 → 57 min, and every
  script's status and check count is unchanged (90/90 script runs).**
- **Of what is left, 43% is fixed sleeps:** 798 s of `waitForTimeout` on the
  full build (§3). Loads reach network-idle in ~1–2 s, but most scripts then
  sleep 3.5–4 s.
- **S205's ~15 min was neither of those.** It was `verify-url-state.js`: 195 s
  on public and 328 s on full, plus two mutant runs. That script already avoids
  the teardown (it opens a fresh browser for every load) and barely sleeps. Its
  time is the walk itself: ≈2 cold loads per round trip, with 31 round trips on
  public and 58 on full. Neither fix touches it. It was the right cost *for that
  PR*, because the diff changed the verify itself and falsifying the verify
  needs the full walk. F3's 2-min targeted probe is the right size for an
  ordinary `web/index.html` change.

## 1. Wall time per script (s), the baseline

Run through `verify.js --jobs 1`, sorted by the full-build time. The "kill"
columns are the same run with the §2 preload.

| script | public | pub kill | full | full kill | fixed sleeps (full) |
|---|---:|---:|---:|---:|---:|
| verify-url-state | 195 | 192 | 328 | 327 | ~0 (300 ms `settle`) |
| verify-peek | 205 | 199 | 216 | 218 | 39 |
| verify-about | 119 | 74 | 131 | 74 | 45 |
| verify-reference-layer | 122 | 104 | 123 | 107 | 41 |
| verify-grid-loading | 123 | 32 | 119 | 32 | 15 |
| verify-budget-panel | 42 ✗ | 40 ✗ | 104 | 104 | 13 |
| verify-staleness-banner | 105 | 47 | 101 | 48 | 32 |
| verify-center2d | 68 | 65 | 74 | 65 | 16 |
| verify-glass-no-slider | 67 | 57 | 68 | 68 | 50 |
| verify-temporal | 59 | 48 | 68 | 49 | 22 |
| verify-money-metric-group | 66 | 44 | 66 | 44 | 36 |
| verify-millrates | 61 | 31 | 61 | 31 | 12 |
| verify-labels | 61 | 45 | 60 | 45 | 35 |
| … 32 more, each ≤ 57 s | | | | | |
| **total** | **2296** | **1587** | **2622** | **1853** | **798** |

✗ = red for a harness reason (§4). The raw runner output was not kept, since
it is reproducible with the commands in §6.

## 2. The teardown tax: graceful close defers it, it doesn't skip it

The ~10 s grid teardown that `verify-url-state.js`'s header records is real,
but it is charged somewhere other than where it looks:

| after a page drew a grid, the next action is | cost |
|---|---:|
| `page.reload()` / `page.goto()` on the same page | **13–28 s** (grid-fine worst) |
| `page.close()` | 0.01 s, but then the **next `browser.newPage()` takes 6–8 s** |
| `browser.close()` after 4 such pages | **30 s** |
| SIGKILL the browser process (`launchServer` + `server.kill()`) | 0.03 s |

Timed by phase in `verify-staleness-banner.js`: each reload is ~7 s of a
previous page's teardown, then 0.9 s of real load, then 3.5 s of fixed sleep.
44 of the 45 scripts `chromium.launch()` a browser, open pages on it, and end
with `browser.close()`. So:
- a multi-page script pays the tax on every page after the first;
- a single-page script pays it once, at exit, after its last check has
  already run (that is where the 8–30 s saved on one-page scripts comes from).

**Fix, measured and not built:** a `--require` preload that the runner
`verify.js` injects. It makes `chromium.launch()` return a browser whose
`newPage()` / `newContext()` each run in their own `launchServer` process, and
whose close SIGKILLs it. That is the same mechanism `verify-url-state.js`
already uses by hand.
- **Semantics:** `browser.newPage()` already gives every page its own context,
  so no state that was shared before stops being shared. Only the GPU process
  was shared.
- **Scope:** no script is edited. `browser.contexts()` / `version()` are unused
  in the suite.
- **CI:** unaffected, because `deploy.yml` calls its two scripts directly, not
  through the runner.
- **Precedent:** this is the DECISIONS 2026-07-30 shape, where the runner wraps
  the scripts rather than every script being edited.

It changes no assertion, so the falsified-mutant re-run the TODO demands for a
*trimmed* check doesn't apply. The equality of all 90 status and check counts
is the evidence instead.

## 3. Fixed sleeps: the next 43%, and costlier to cut

Counted per script by wrapping `waitForTimeout`. In 29 scripts it is ≥ 60% of
the post-fix time (e.g. `verify-development` 27 of 30 s, `verify-loading-overlay`
32 of 38 s). Replacing a sleep with a ready condition (`waitForFunction` on
state, as `verify-url-state.js`'s `settle` does) is a per-script edit that can
blind a check: a sleep sometimes covers a deck.gl frame that a pixel read
needs. **So each one needs its own falsification.**
- **Recommendation:** don't sweep. Convert a script only when it earns a place
  on a schedule or a gate, and falsify it then.

## 4. Suite hygiene the run surfaced (not runtime, but real)

1. **Three public-build reds, all harness defects, not regressions.**
   - `verify-uses.js` and `verify-budget-panel.js` drive full-only controls with
     no `FULL_BUILD` gate, so they crash on public (Uses is hidden; "opener is
     visible in the full build" fails, then a timeout). This is the V4 build-gate
     class from `FINDINGS_vacuous_guards.md`. Neither was among the 10 scripts
     the S144 sweep gated.
   - `verify-deviation.js` **ignores its URL argument**: it hardcodes
     `localhost:8777/index.html?build=…`. It runs only when someone serves `web/`
     on :8777. Through the runner it always fails, on either build.
2. **Four `verify-*` scripts contain no assertions:** `verify-glass`,
   `verify-labels`, `verify-services`, `verify-uses`.
   - They print state for a human and exit 0 unless they crash, and they cost
     ~2 min per build after the fix.
   - They are named like guards, the runner lists them as `ok`, and the runner
     counts "0 checks" for them without flagging it.
3. **The runner can't count 4 more:** `verify-glass-cell`, `verify-grid-loading`,
   `verify-url-state` and `verify-budget-panel` print checks in a format other
   than `^PASS`/`^FAIL`, so they read as "0 checks".
   - They do exit non-zero on failure, so the runner is not blind to them, just
     uninformative.
   - ⚠️ `verify-budget-panel` indents its `  FAIL` lines, so the runner shows
     only the tail of the crash, never the failing check's name.
4. **`verify-blurbs` refuses the full build by design**, and the runner reports
   that as FAIL. That's noise on every full-build sweep.

## 5. Environment finding

A `python3 -` from a 2026-09-21 background task (the dark-mode token
inertness check, whose shell exited 144) **sat at 100% CPU for 7 days**. It was
orphaned to PID 1, alongside a stale `http.server 8931` from the same run.
- **Effect:** every verify timing from 2026-09-21 to 2026-09-29, S205's
  included, ran on 3 of the 4 cores.
- **Action:** killed at the start of this session, before any measurement.
- **Likely cause:** exit 144 matches the `pkill -f`-shoots-its-own-shell signature (memory
  `pgrep-watchers-match-themselves`). The victim's child survives it.

## 6. Reproduce

- Build and serve:
  `.venv/bin/python scripts/build_site.py --src web --out <scratch>/site`, then
  serve `<scratch>/site` on :8956 (confirm the serving root).
- Baseline:
  `node tools/profiling/verify.js http://localhost:8956/index.html --jobs 1`
  (and again with `/dev-build-full/index.html`).
- Fixed variant: the same, with `NODE_OPTIONS="--require <preload>"`, using the
  measurement preload below. It is not committed; it becomes a real file only if
  the fix is approved.

```js
// Measurement preload: one browser PROCESS per page/context, SIGKILLed on close,
// so no page ever pays a predecessor's deferred GPU teardown.
const pw = require('/home/opc/edmonton-tax-viz/tools/profiling/node_modules/playwright');
const launchServer = pw.chromium.launchServer.bind(pw.chromium);
pw.chromium.launch = async (opts = {}) => {
  const servers = [];
  const spawn = async () => {
    const s = await launchServer(opts); servers.push(s);
    return { s, b: await pw.chromium.connect(s.wsEndpoint()) };
  };
  const base = await spawn();
  return new Proxy(base.b, { get(t, k) {
    if (k === 'newPage') return async o => { const { s, b } = await spawn(); const p = await b.newPage(o); p.close = async () => { await s.kill(); }; return p; };
    if (k === 'newContext') return async o => { const { s, b } = await spawn(); const c = await b.newContext(o); c.close = async () => { await s.kill(); }; return c; };
    if (k === 'close') return async () => { await Promise.all(servers.map(s => s.kill())); };
    const v = t[k]; return typeof v === 'function' ? v.bind(t) : v;
  }});
};
```


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


## 7. Close-out (S213, 2026-10-02): the speed-ups audited, the sweep re-run

Opus 5.5, `high`, run from `docs/FABLE_AUDIT_test_runtime.md` (ledger item 17).
⚠️ **The builder's model graded its own work:** #620–#642 were built on Opus
5.5, and so was this run (DECISIONS 2026-10-02). §1–§6 above are S206's and
are left as they were.

### 7a. Part A, top-down

| Level | Verdict | In one line |
|---|---|---|
| L0 the right thing gated | **CONDITIONAL** | Every number-protecting guard is on the merge gate; `url-state` is not a gate (F1) |
| L1 coverage kept | **SOUND in effect; its guard was BLIND** | Shards = one run, check for check; the partition test missed 3 coverage-dropping mutations (F2, fixed in #646) |
| L2 where time is paid | **SOUND** | The only cost anyone waits on is the required `test` job, ~1 min |
| L3 hygiene | **WARN** | "0 checks" and the `verify-blurbs` full-build red fixed (#647); doc drift (F3); `verify-about` red on external hosts in 3 of 7 runs (F4) |

**L0. Is the right thing gated? CONDITIONAL.**
- **F1: `url-state` gates nothing until it is required.** Branch protection
  requires `test` only (read from the API, 2026-10-02). Since #619 the walk
  has run on 10 PRs, and **4 of them merged before it reported**: #619 (5.4 min
  early), #629 (7.0), #634 (6.5), #636 (1.1). Each one deployed first. All 10
  ended green, so nothing shipped broken. But DECISIONS 2026-09-29 says the
  check "gates the merge", and on 40% of its runs it gated nothing. Its only
  reader on red is GitHub's failed-run email, which arrives after the deploy.
  - **Remedy (Peter's): add `url-state` to the required checks.** It is one
    setting, and the aggregate job was built for it. On a PR it doesn't apply
    to it goes green in 9–14 s, inside the required `test` job's 43–63 s, so
    it adds no wait there (6 PRs, #639–#645). On a `web/` PR it takes ~3 min.
  - **The sharpest counter-argument:** it has never been red on CI, so a required
    check costs ~3 min per `web/` PR to catch something that hasn't happened.
    **What would change the verdict:** a `url-state` red on any PR.
  - ✅ **Done 2026-10-03 (S214):** `url-state` added to the required checks
    (API read-back: `test`, `url-state`).
- **The ungated class is UI behaviour, not numbers.** 11 DECISIONS rows cite only
  a hand-run `verify-*`. About 6 are still live: Center 2D ×3, search marking
  ×2, services panel ×1. Every guard that protects a published number is
  pytest or an offline `check_*` on the merge gate. That split is acceptable
  under the S206 cost regime: the suite is 62 min here.
- **Checked, and not a gap:** `refresh.yml` pushes `web/data` straight to
  master, so `url-state` never sees a data change, even though data gates some
  controls (Development's `_long` window, Glass's lot row). A dropped column is
  `check_served_columns.py`'s job on that path, before the publish.

**L1. Did the speed-ups keep coverage? SOUND in effect; the guard was BLIND.**
- **Shards against one run, same `web/` tree.** No `web/` file changed between
  #636 (one unsharded job) and #642 (seven shards), so their CI logs compare
  like for like.
  - Round trips: public 15 + 16 + 0 = **31**; full 15 + 21 + 13 + 9 = **58**.
    Both equal the unsharded run and S204's figures. No drift.
  - Every unsharded check name is in the sharded set (public 179 → 185, full
    316 → 329). The extras are the per-shard preamble only: the default-view
    link, `--views names an offered view`, and `the walk has a view to walk`.
  - Offered views: public money, development, services, ratio; full adds uses
    and lab.
- **F2: the partition test passed under three mutations that drop coverage.**
  Each one leaves every shard green and all 1097 tests green:
  1. `--part=links` on both money shards: money is walked on neither build.
  2. The full catch-all made `--part=links`: ratio, uses, lab and any future
     view are walked nowhere.
  3. Every `dev-build-full` shard deleted.

  The test counted a view **named** by a links-only shard as **walked**, and
  it never counted builds. The script can't catch this either: `the walk has a
  view to walk` is skipped under `--part=links`. **Fixed in #646:** two
  assertions. Control green; these three, a public-only money variant and the
  S211 comma split all red.
- **The change filter is complete for PR-borne changes.**
  - `build_site.py` is stdlib-only and reads only `--src`, plus `git` for the
    stamp.
  - `verify-url-state.js` requires only `playwright`, and
    `package(-lock).json` and `tests.yml` are both in the filter.
- **`--only-shell` changed nothing that runs.** Playwright 1.61.1's default
  headless `launchServer` spawns `chromium_headless_shell-1228/…/headless_shell`
  (read from `/proc/<pid>/exe`). So CI was already on the shell before #642,
  which only stopped downloading a binary nobody launched.
  - The walk compares DOM state (view, title, active controls via
    `checkVisibility`), never pixels: 0 screenshot or pixel calls.
  - A future headed or `channel` launch would fail loudly on a missing binary,
    not silently.
- **The preload still holds.** A/B on the 6 scripts changed or added since
  S206 (about, budget-panel, controls-clickable, deviation, peek, search), both
  builds, each with and without the preload: **12/12 pairs identical in status
  and check count.**
  - Two apparent differences are the network, not the mode. Public `verify-about`
    read 78 vs 79 because GitHub returned 429 on one link, which the script
    skips by design. Full `verify-about` failed in **both** modes on a 20 s
    timeout from data.edmonton.ca, which answered 200 in 1.4 s when re-fetched.
  - The other 36 scripts are unchanged since S206's 90/90.
  - Time saved: about 59 s / 55 s (public/full), controls-clickable 14 s /
    19 s, peek and search about 0.

**L2. Where wall time is paid. SOUND.** Runs since 2026-09-22:

| where | runs | median | who waits |
|---|---|---:|---|
| `test` (required) | 50 PR + 50 push in 6 days | 62 s / 58 s | every merge. Steps ≈ 40 s, of which `pip install` is 20 s |
| `url-state` | 10 walking PRs in 4 days | 177 s (#642) | nobody today; ~3 min per `web/` PR once required (F1) |
| deploy | 36 in 9 days | 126 s | nobody (post-merge). Smoke 74 s, harness install 33 s |
| refresh | weekly | 761 s | nobody |

Nothing here is worth cutting: the one cost paid while waiting is `test`, at
about a minute. `deploy.yml` and `refresh.yml` still install full Chrome
(`--with-deps chromium`, ~6 s each, unused). #642's flag applies there too,
but those are publish gates, so make that change only when they are next
touched for another reason.

**L3. Hygiene. WARN.**
- **"0 checks":** three scripts, all in one format (`ok  `/`FAIL`), and no
  other script prints `ok  `. A one-regex runner change counts them (#647; on
  full: glass-cell 27, grid-loading 23).
- **`verify-blurbs` on the full build:** the runner now reports its deliberate
  refusal as `skip`. That is safe because `deploy.yml` calls the script
  directly, never through the runner. Falsified with stub scripts:
  - a refusal plus a real FAIL stays FAIL;
  - all-`ok` with exit 1 stays FAIL.
- **Assertion-less `verify-*`: none left.** #622 renamed the four to `probe-*`,
  and every remaining `verify-*` has a FAIL path and a non-zero exit.
- **F3, doc drift:** DECISIONS 2026-10-02 (sharding) and the
  `verify-url-state.js` header both say "six shards"; there are seven since #642.
  The header is fixed in #647. The DECISIONS row is point-in-time and
  the decision itself didn't change.
- **F4, external-link flakes:** `verify-about` was red in **3 of its 7 runs
  today**, every time on a host we don't control: openstreetmap.org 503 once,
  and a 20 s timeout from data.edmonton.ca twice. Both hosts answered 200 when
  re-fetched. The script already treats a 429 as SKIP, but not a 5xx or a
  timeout, so a down host reads as a broken link. Remedy (a script change,
  Peter's): treat 5xx and timeouts like 429, and keep 404/410 red.
  - Separately, `verify-grid-loading` (public) went red once in the sweep with
    "a prefetch window exists to click into: got false" (73 s, against 32 s
    alone). Green when re-run alone.

### 7b. Part B: the sweep, both builds, `--jobs 1`, alone

The box was quiet throughout: load was sampled every 60 s, and nothing but
`headless_shell` and `node` exceeded 10% CPU. The serving root was confirmed
from `/proc/<pid>/cwd`. Master was at `684ffc0`.

| min | S206 baseline | S206 + preload | **S213** |
|---|---:|---:|---:|
| public | 38.2 | 26.5 | **29.0** |
| full | 43.7 | 30.9 | **33.0** |
| total | 82 | 57.3 | **62.0** |

The +4.7 min decomposes as follows:
- `verify-search` is new: +213 s.
- `verify-peek` is slower: +198 s, and the cause is **the lit selected-hood
  prism (#635/#636), not #639**. `peek` on public takes 224 s on the
  pre-search build (`71bf5dd`), 212 s at #634 (search, outline dropped) and
  310–316 s now. It is not teardown either: the A/B shows `peek` equal with
  and without the preload. Under SwiftShader every tap now builds a lit prism.
  Whether a phone feels that is a question for the S210 phone checks.
- `verify-url-state` added frozen links and Copy-link checks: +48 s.
- The `grid-loading` flake cost +41 s.
- Four scripts moved to `probe-*`: about −240 s.
- `budget-panel` is now build-gated on public: −27 s.
- The remaining ~+50 s is spread over 30-odd scripts.

Results:
- **Scripts: 42 per build** (45 − 4 probes + `verify-search`). The runner
  reported checks of public 1,218 and full 1,461, but that undercounts the
  three `ok  ` scripts.
- **Reds:** `verify-about` (OSM 503) and `verify-grid-loading` on public,
  and `verify-blurbs`' refusal on full. **No real red**: both public reds were
  green when re-run alone (F4).
- Scripts over 60 s: `url-state` 210/357, `peek` 316/299, `search` 104/109,
  `reference-layer` 109/101, `budget-panel` –/104, `about` 78/78, `center2d`
  65/68.

### 7c. The open "Verify runtime" items, closed

- **Fixed sleeps: closed, no sweep.** None of the 798 s is paid on any gate or
  schedule: the gated scripts are `url-state` (300 ms `settle` only), `smoke`
  and `blurbs`, and nobody waits on the sweep. §3's rule stands: convert a
  script when it is promoted to a gate or a schedule, and falsify it then.
- **"0 checks" and `verify-blurbs` on the full build: fixed in #647**, which
  waits for Peter.

### 7d. What this run got wrong

1. **My first PR classifier counted docs PRs as walked.** The change filter's
   job is also named `url-state-…`, so a docs PR looked like a run and
   "merged before the result" read 9 of 9. It also missed every PR before #637,
   which had one job and no shards. Re-cut on "a `url-state*` job ran over
   60 s", which gives 10 PRs and 4 early merges. Only that version is above.
2. **My first money mutation hit both money shards, not one.** `sed` replaced
   both lines. The pre-fix green was for the stronger mutation, and I never ran
   the public-only variant against the old test. It is red against the new
   one.
3. **I nearly reported the data path as a gap.** "`url-state` never sees a
   refresh, and data gates controls" is true, but `check_served_columns.py`
   fails the refresh on a dropped column first. That is the confident-negative
   shape the skill warns about, caught only because I went looking for the
   reader.
4. **I first blamed #639 for `verify-peek`'s +100 s**, because it was the only
   change to the script. The diff is 9 lines that change one comparison. Two
   builds bisected it to the app instead (#635/#636). A slower check can be a
   slower page.
5. **`git stash -u` before a branch switch swallowed my uncommitted ledger
   rows.** I popped them straight back. It's the same hazard as memory
   `commit-before-falsifying`, one step removed.
6. **Same model as the builder.** L1's "SOUND in effect" rests on one pair of
   CI logs and on reading the code. A different reader should try to break
   the partition another way than these five mutations.

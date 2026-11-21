# Findings — which verify scripts a PR needs (S257, 2026-11-20)

Peter's ask (S256 TODO "Audit when a PR needs the whole browser suite", widened
in S257: "can we do this more efficiently? Can anything be sped up, or
replaced, or is anything not necessary"). Opus 5.5. Nothing browser-driven was
run for this; the inputs are the S256 sweep log (`--jobs 1`, raw `web/`, which
serves the full build), git history, the handoffs, and
`docs/FINDINGS_verify_runtime.md` / `docs/FINDINGS_test_estate.md`.

## 0. The answer

- **No PR needs the whole suite.** Across the four recorded sweeps, 14 reds
  came from outside the area a PR touched, and **one** of them was a real page
  bug (§1). The rest were stale expectations, flakes and one test bug. That is
  the value of a periodic sweep, not of a per-PR one.
- **Per PR, run a targeted set by change class** (§3, now in
  `docs/CHANGE_PIPELINE.md` step 5). For #852 that set is about 2.5 min against
  the 40 min S256 paid.
- **Two parts of the S256 sweep bought nothing:** `verify-url-state` (348 s)
  is a required CI check on every `web/` PR already, and `verify-theme` (167 s)
  is red by construction on raw `web/` (it needs a `build_site.py` tree).
- **Nothing is worth deleting.** Seven scripts are 55% of the time, the other
  37 average ~25 s, and each covers something no other script does (§2).
- **The full sweep's real job is drift detection, and it belongs off the box**
  (§4, a proposal): a GitHub Actions matrix on the public repo is free, runs
  the scripts in parallel on separate VMs, and removes both the CPU contention
  and the 10-minute Bash cap.

## 1. What the full sweep has caught

Every recorded full sweep, each red classified by how it was resolved:

| Sweep | Reds | Real page bug | Stale expectation | Test bug | Flake / harness |
|---|---:|---:|---:|---:|---:|
| 2026-09-05 (`3861cbf`) | 4 | 1 | 3 | | |
| 2026-10-02 S213 (`FINDINGS_verify_runtime.md` §7b) | 2 | | | | 2 |
| 2026-11-15 S247 (`FINDINGS_test_estate.md` F5, fixed S251–S253) | 8 | | 4 | 1 | 3 |
| 2026-11-20 S256 (`suite.log`) | 0 unexpected | | | | |
| **Total** | **14** | **1** | **7** | **1** | **5** |

- **The one real bug:** `CHROME_IDS` lacked `#budget`/`#budget-pod`, so place
  labels drew over the budget panel on the full build. `verify-reference-layer`
  caught it. The diff that caused it added a panel and did not touch
  `CHROME_IDS`, which is why §3 has a "new panel or chrome element" row.
- **Stale:** copy merged in #808 (`about`, `nonres-revenue`), refresh-moved
  counts (`transit` 58→59, `glass-cell`/`grid-loading` cell counts), the
  public `#views` row after Services published (`deviation`), the Unclassified
  colour exemption (`theme`).
- **Flake / harness:** `peek` (scan mid-flatten), `temporal` (click timeout
  under software WebGL), `center2d` (green on re-run), `about` (external host
  503/timeout), `grid-loading` (under load).
- **Not counted:** reds a session saw and fixed inside its own PR before
  pushing. Nothing records them, and they are the targeted scripts doing their
  job, not the sweep.

So the sweep's yield per PR is about one real bug in four months, while its
stale reds are caused by refreshes and copy merges whatever the PR is. Those
sat unnoticed for days (F5: two days) because nothing runs the sweep on a
schedule.

## 2. Where the 40 minutes go (S256, 2,402 s, full build)

| Script | s | Note |
|---|---:|---|
| `verify-url-state` | 348 | **Duplicate:** required CI check, 7 shards, both builds, every `web/` PR |
| `verify-peek` | 331 | 94 → 310 s since the lit selected-hood prism (#635/#636); already a TODO under "Verify runtime" |
| `verify-theme` | 167 | **Red by construction on raw `web/`**; run it on a `build_site.py --out` tree |
| `verify-guide` | 130 | |
| `verify-search` | 119 | |
| `verify-budget-panel` | 113 | full build only |
| `verify-reference-layer` | 105 | the script that made the one real catch |
| 37 others | 1,089 | ~25 s each; boot (launch + load + data) is ~10 s of each |

- **Fixed sleeps:** 307 `waitForTimeout` calls, 540 s if each runs once.
  `FINDINGS_verify_runtime.md` §7c already closed this: convert a script when
  it is promoted to a gate or a schedule. That still holds; §4 is that
  promotion.
- **Deletion candidates: none.** The cheap scripts cost too little to matter,
  and the expensive ones each guard something unique (touch, theme, guide,
  search, the label sweep).

## 3. Selecting scripts from the diff

A prototype (`scratchpad/pick_scripts.py`, not committed) mapped the
`web/index.html` symbols and element ids a commit touches to the verify scripts
that name them. On the last 12 `web/` commits:

- 10 got 1–10 scripts; the S232 layout commit `c3e908a` correctly got 35.
- #852 (`8dc9ae2`) got 7: `deviation`, `glass-inst`, `inst-caveat` (the ones
  S256 had chosen by hand), plus `hoodmode`, `infill`, `peek`, `smoke`. It
  **missed `verify-blurbs`**, which checks length and rules, not symbols.
- `2f69cca` (the Enoch Cree Nation reserve) got **0**; `reference-layer` was
  the right script.

So a symbol match is a good start and needs a floor by change class. The
rules are in `docs/CHANGE_PIPELINE.md` step 5. The lookup is a `grep -lw` by
hand today; a `verify.js --changed` flag is the tooling version (§5).

## 4. Proposal: the full sweep on GitHub Actions (CI change — Peter's yes needed)

**Approved and built (S259, stage 1):** `.github/workflows/verify-sweep.yml` +
`scripts/verify_sweep.py`, manual runs only until the runner timings are
calibrated. The shape that shipped is the `DECISIONS.md` 2026-11-20 row; it
uses 16 shards rather than one job per script. Triage: `docs/RUNBOOK.md` §0g.

**Calibration run 1 (S260, 2026-11-20, run `44805707305` on `a8d4b35`):**
84 of 84 results, 83 green, 1 red twice, 0 flaky.

- **The red was the test, not the page.** `verify-search` (public) failed
  "2D: the pick is outlined instead" and "back in 3D", both reading
  `BELGRAVIA`. Its "click outside closes search" clicked the map at
  (720, 880), which is BELGRAVIA's prism once the camera sits on GLENORA, and
  a map click pins the hood under it. On this box the pin didn't land in time
  to matter. With a pick read just before the click and a 500 ms wait after it, the box reproduces the runner
  exactly. Fixed: the click goes on `#temporal-name`, and a new check, "the
  outside click leaves the pin alone", goes red first under the old click.
  The full build's run was green (82 s).
- **`verify-loading-overlay`'s 250 / 8000 / 40 ms held on x86** in both
  builds, as did `peek`, `temporal` and `grid-loading`. One run, so not yet a
  calibration.
- **Time:** 3,005 s of script time over the 84 runs (longest: public `theme`
  249 s, `peek` 227–228 s in each build). Jobs total 4,285 s (~71 runner-min,
  free on a public repo), and the run took about 12.5 min wall.
- **Setup varies 25×.** "Install the verify harness" (`npm ci` +
  `playwright install --with-deps`) took 16 s on `public 7` but 372 s and
  430 s on `full 1` and `public 2`, which made those the two slowest jobs.
  The apt step in `--with-deps` is the likely cause (not split out yet). It
  doesn't matter for an unattended weekly run unless it gets worse.

**Calibration run 2 (S260, run `44809650803`, on the #864 branch):** 84 of 84,
83 green, 0 red, 1 flaky. `verify-search` was green in both builds (65 s,
70 s).

- **The flake is the same mechanism.** `verify-budget-panel` (full) failed
  "survives a map click" on its first try, then crashed on a null
  `boundingBox()` (17 of 58 checks, 8 s), and passed on the retry. Its click
  at (720, 500) is PAPASCHASE INDUSTRIAL, a pin opens `#temporal`, and
  `#temporal.open ~ #budget` hides the budget by design. On this box a bare
  `page.mouse.click` on a hood never pins, but a hover first pins it every
  time, so the box can force the runner's case. Fixed: the script finds a
  bare-map pixel by picking (`found a bare-map pixel to click`). A hovered
  click there stays green, and a page that closes the budget on any click
  turns the check red.
- **A class, not two scripts.** A verify script whose map click is meant to
  do nothing must click a pixel it has shown is bare. Only
  `verify-guide.js` does another raw map click. It asserts its point is
  canvas, not that no hood is under it. It passed in both runs and is left
  alone for now.
- **Time:** 3,003 s of script time, jobs 3,845 s, the longest job 425 s.
  The install step took at most 31 s on any job this time.

**Calibration run 3 (S260, run `44814225000`, on the #865 branch `8ff32ba`):**
84 of 84, 84 green, 0 red, 0 flaky (84 result lines, so no retries ran).
`verify-budget-panel` (full) passed 59 checks first try (43 s); `verify-guide`
was green in both builds (66 s, 54 s). Collected 2026-11-21 by the next
session: S260 died in the box hang before reading it.

- **Time:** 2,975 s of script time (longest: public `theme` 232 s, `peek`
  228–230 s), jobs 3,932 s, the longest job 606 s (`full 1`), about 10.3 min
  wall. Install step 12–277 s.
- **Three runs, one real finding class** (the map click that should do
  nothing) and no runner-only timing reds. `loading-overlay`'s
  250 / 8000 / 40 ms held in all three.


- **What:** a new workflow, `workflow_dispatch` plus weekly after the Monday
  refresh. It builds with `build_site.py`, then runs one matrix job per
  script per build. It is non-blocking, and on a red it files one issue (the
  `vintage-digest.yml` pattern).
- **Why there:** the repo is public, so standard runners cost nothing, and
  `tests.yml`'s `url-state` matrix is the working prior art. The wall time is
  roughly the longest script plus ~1 min of setup, so ~6–7 min, with every
  script on its own VM: no contention and no `--jobs 1`.
- **Blocker, the same one the 2026-09-08 "Tier 3" proposal named:** a script
  run unattended after a refresh must not pin data counts, or it cries wolf
  every roll. Pinned refresh-sensitive literals have to be derived from the
  served files first (`verify-inst-caveat`, `verify-ratio-denom` are known;
  the rest need reading, not a regex screen). That is S256's carried item 4.
- **Unmeasured:** behaviour on x86 runners under SwiftShader. The first runs
  calibrate. `verify-about`'s F4 remedy (5xx and timeout read as SKIP) was
  already in, from #650 (2026-10-02); this bullet and the TODO had gone stale.

## 4b. The pinned-literal read (S258, 2026-11-20)

Every one of the 44 scripts and the runner was read, not screened. A literal
counts as **refresh-sensitive** only when a served file that the refresh
rewrites can move it with nothing wrong. Commit counts since 2026-09-20:
geojson 10, status 10, value_grid 9, dev_grid 7, temporal 5, transit_stations
3. `lrt_lines.json` has not changed since 2026-07-11, and `reference.geojson`
changed once, in a code PR.

**Derived in this change (all from the served file, never from the helper under
test):**

| Script | Was | Now |
|---|---|---|
| `verify-inst-caveat` | caveat counts 20/6/164, band counts 5/0/8, U of A `90%` and `$18,047 to $178,401`, ASPEN GARDENS `9%`/`100%`, HUDSON + ROYAL GARDENS, DOWNTOWN `5%` | sets recomputed from `rev_frac_exempt[_res\|_nonres]` and the 0.25 bar written out; range parsed and compared to `v·(1−e)` and `v`; split-share exemplar picked from the data |
| `verify-ratio-denom` | share-tier band `=== 15` | count from the raw file (road floor 5, bar 0.25) |
| `verify-change` | no-baseline 45 and 11, fell-to-zero 1, elapsed 14 / intervals 12 | holes counted from `temporal.json` with changeFor's rule; the divisor gap asserted as 2 |
| `verify-infill` | `DOWNTOWN still top pressure` (weekly permit data) | the min-score hood carries the minimum t |
| `verify-revenue-panel` | DOWNTOWN must hold a sub-0.05% category | the `<0.1%` check runs only when one is served; `0.0%` is never allowed |
| `verify-theme` | hand-edited Unclassified exemption (dropped 11-09, restored 11-19, both after refreshes) | exempt exactly when no served zone is `other` and no hood has `frac_other` |
| `verify-temporal` | x-axis `'2026'`, runs `[12,1]`, the 2023→2026 jump read off the first circle | live year and run lengths from the year list; the jump reads the second path once a year follows 2026 |

**Left pinned, on purpose:**

- **They move only with a code change**, so the same PR updates them: the
  Development window labels (`2009–2025`, `2021–2025`, `2023–2025`, from
  `WINDOWS`), the change-lens start years, the `PLACES` counts in
  `verify-reference-layer`, the public view list in `verify-deviation`, the
  frozen links in `verify-url-state`, the service-layer counts (10, 3) and the
  hand-set clamps (`$30k+`, `$50k+`).
- **Frozen history:** `verify-temporal`'s DOWNTOWN 2012 = 5.09% and peak 5.55%
  in 2016 (2012–2023 are bit-identical across refreshes).
- **Static file:** `verify-transit`'s 343 LRT lines.
- **Stable named exemplars:** U of A and Gold Bar banded (90% exempt), MAPLE
  RIDGE's null lot value, TWIN BROOKS in search. A red on one of these is a real
  event worth an issue, not churn.
- **Data-shape checks that are rare and meaningful:** `verify-services-panel`'s
  "the floor actually fires" (its own comment calls a zero a prompt to
  re-measure, which is what an issue is), `verify-deviation`'s inverted and
  zero-crossing bands, and the 5× surplus arm.
- **Runner-sensitive, not data:** `verify-loading-overlay`'s 250 / 8000 / 40 ms.
  The first x86 runs calibrate these.

## 5. Not done, in order

1. §4 stage 2: calibrate on the first manual runs, then trigger on the
   refresh's completion (`workflow_run`).
2. `verify.js --changed [base]`: the prototype plus §3's floor. Tools change,
   Peter merges. Worth it only if per-PR selection by hand still costs time.
3. `verify-peek`'s 331 s: existing TODO ("The lit selected-hood prism").

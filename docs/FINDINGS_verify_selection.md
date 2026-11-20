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
  calibrate; `verify-about`'s external-host checks need F4's remedy (5xx and
  timeout read as SKIP) first or they will flake there too.

## 5. Not done, in order

1. §4, after the pinned-count read (its own TODO).
2. `verify.js --changed [base]`: the prototype plus §3's floor. Tools change,
   Peter merges. Worth it only if per-PR selection by hand still costs time.
3. `verify-peek`'s 331 s: existing TODO ("The lit selected-hood prism").

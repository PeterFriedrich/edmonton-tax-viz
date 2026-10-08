# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **Tutorial pop-up for the toolbar on a first mobile visit, and maybe a
  smaller one on desktop.** DONE S217 (2026-10-08): one card, `?` beside the
  magnifier, offer-only on a shared link; DECISIONS 2026-10-08, `verify-guide.js`. It would show once and walk through the controls.
  Nothing in `DECISIONS.md` covers onboarding or a tutorial yet.
  - Before designing, read `docs/MOBILE_USABILITY.md` and `docs/CONTROLS_MATRIX.md`.
    The controls are shared DOM, so a tour of them touches desktop too.
  - A "seen it" flag in `localStorage` must fail safe: private windows and
    headless runs start empty, and the verify scripts will meet the pop-up.

- [x] **Make `url-state` a required check (S213 F1).** Done 2026-10-03 (S214). Peter's call; it is one
  branch-protection setting.** It walked 10 PRs, and 4 merged before it
  reported and deployed first. DECISIONS 2026-09-29 says it "gates the merge".
  On non-`web/` PRs it finishes inside `test`'s time, so requiring it costs
  ~3 min on `web/` PRs only. If Peter declines, mark that row amended:
  advisory, read by email.

- [x] **`verify-about`: treat 5xx and timeouts like 429 (S213 F4).** It was red
  in 3 of 7 runs on 2026-10-02, each time on a host we don't control. Keep
  404/410 red. Script change, so Peter's.
  - **Fixed in #650 (S214), merged 2026-10-03.**

- [x] **Runner reports "0 checks" for `verify-glass-cell`, `verify-grid-loading`,
  `verify-url-state` (findings §4.3).** They gate by exit code, so this is
  reporting, not coverage: print `PASS`/`FAIL` lines, or teach the runner
  their format.
  - **Fixed in #647 (S213), merged 2026-10-02.**

- [x] **`verify-blurbs` reads FAIL on every full-build sweep (findings §4.4).** It
  refuses the full build by design; the runner should skip or mark it, not
  count it red.
  - **Fixed in #647 (S213), merged 2026-10-02.**

- [x] **Merge #646 (S213 F2)** — merged 2026-10-02, the shard-partition test. It currently passes
  with money, the full catch-all, or the whole full build dropped from the
  walk.

- [x] **Fixed sleeps: 798 s of `waitForTimeout` on the full build (findings §3).** CLOSED S213, no sweep: none of the 798 s is paid on any gate or schedule (findings §7c).
  Loads settle in ~1–2 s, then most scripts sleep 3.5–4 s. Don't sweep: a sleep
  can cover a deck.gl frame a pixel read needs. Convert a script to a ready
  condition (`waitForFunction`, as `verify-url-state.js`'s `settle`) only when
  it earns a gate or a schedule, and falsify it then.

- [x] **A smaller `url-state` check for ordinary `web/` PRs.** Done differently
  (S211): six parallel shards, full coverage kept, ~8 → ~2.5 min wall
  (`DECISIONS.md` 2026-10-02).

- [x] **Pin the URL vocabulary (URL audit F2) — DONE S209.** A rename of any value passes
  the round trip. Add every §8 value to the verify as a frozen link that must
  restore to itself, and **Peter to decide the policy**: rename/retire = an
  alias entry, never a silent drop (OWID's `GrapherUrlMigrations.ts` is the
  prior art). Fix §8's "public names" sentence to say which keys are mapped.
  **Done S209 (2026-10-01):** Peter approved the alias policy; 17 frozen links
  (10 both builds, 7 full) cover every §8 value. DECISIONS 2026-10-01.

- [x] **Make the URL feature a button export, not default exposed — DONE S209** (Peter,
  2026-09-30). Today `writeUrlHash` rewrites the address bar on every control
  change (`history.replaceState`), so the state hash is always visible. Wanted:
  a clean URL by default, and a button that produces the share link on demand.
  This revisits the 2026-09-28 DECISIONS row (#608). Before building, decide
  whether restore-from-hash on load stays as-is (a shared link must still
  open), and update `verify-url-state.js`, which round-trips through the live
  hash.
  **Done S209 (2026-10-01):** a Copy link pod tops the bottom-right stack;
  restore stays and then removes the hash; no-clipboard falls back to the
  address bar. DECISIONS 2026-10-01, `CONTROLS_MATRIX.md` §8.


- [x] **Four verify scripts assert nothing — DONE S207, renamed `probe-*`** (S106): `verify-glass`, `-labels`, `-services`, `-uses` print values and always exit 0, so `verify.js` lists them `ok` with 0 checks. Add assertions, or rename them as probes so the runner stops counting them. Local sweeps only; CI does not run them.

- [x] **Four `verify-*` scripts have no assertions — DONE S207, renamed `probe-*`** (`glass`, `labels`,
  `services`, `uses`). They are named like guards but can only fail by
  crashing. Peter's call: rename them to `probe-*` (the runner would drop
  them), or give them asserts.


- [x] **Three verify scripts are red on public for harness reasons — DONE S207** (gates + argv URL; `verify-deviation` then caught a stale public-views literal missing `ratio`, fixed; `verify-budget-panel` lines made runner-countable) (findings §4.1):
  - `verify-uses.js` and `verify-budget-panel.js` need a `FULL_BUILD` gate.
    Use the README convention: `PARTIAL` plus a both-directions assert.
  - `verify-deviation.js` must take its URL from `argv`, not hardcode `:8777`.

- [x] **Runner preload: a browser process per page, SIGKILL on close — DONE S207** (`tools/profiling/fast-teardown.js`, wired in `verify.js`; re-run 26.6 + 30.9 = 57.5 min, only the 5 known harness reds).
  Measured 82 → 57 min for the whole suite (both builds), with 90/90 script
  statuses and check counts unchanged. It is a new file in `tools/profiling/`
  plus an `env` line in `verify.js`'s `spawn`. No script is edited and CI is
  untouched. The measurement preload is in the findings doc §6.

- [x] **Audit the pre-merge verify runtime: does it need to take this long?** — DONE S206: `docs/FINDINGS_verify_runtime.md`
  Peter asked after F1/F3 (PRs #613/#614). Each needed ~15 min of headless runs
  before a PR could open: `verify-url-state.js` alone is ~3 min on public and
  ~6 min on full, and the runs must be sequential on this 4-core box.
  - **Measure first; don't guess.** Inventory which checks actually gate a merge
    (`tests.yml` pytest is ~16 s) versus which are by-hand habit (73
    `tools/profiling/*.js`). Get each one's wall time, and where that time goes:
    - a browser relaunch per load;
    - grid teardown under software GL (~10 s);
    - `settle` / `networkidle` waits;
    - walk depth and repeated states (the URL walk revisits views from cold).
  - **Then decide per script:** keep, trim, or move to a scheduled or deploy-time
    run. Which checks does a given kind of diff actually need?
  - **Don't cut a check without re-running its FALSIFIED mutants** on the
    trimmed version. A faster guard that goes blind is the F1 failure again.
  - **Feeds** the pending CI decision for `verify-url-state.js` (S203's four
    options; CI would pay the same minutes).


- [x] **`state.devWindow` defaults to a window the data may lack (URL audit
  F3) — DONE S205 (PR pending merge).** `applyDevWindow("5yr")` at the gate; on a `_long`-stripped copy Development opens 5yr lit, 406/406 values (old page: 0/406); served data unchanged (long, 406). On a no-`_long` file (a supported pipeline output) Development opens
  titled 2009–2025 with 0/406 values. One line at the `hasLongWindow` gate
  (fall back to `5yr`) plus the comment beside it, which says the opposite.

- [x] **`verify-url-state.js` must not share `offered()` with the page (URL
  audit F1) — DONE S205 (PR pending merge).** Re-run 2026-09-29: clean public 31 / full 58 all passed; F1 mutant 6 FAILED by name; `offered()`-always-true mutant 7 FAILED (lands-on links). A control `offered()` wrongly hides drops from every link and
  the verify stays green (mutant: 31→26 trips, all passed). Swap the four
  `offered` uses in the script for `el.checkVisibility()` — validated: red by
  name on the mutant, green on clean (public 31, full 58). Worth doing BEFORE
  the CI decision above, or CI gates on a blind check. Tools change → PR for Peter.

- [x] **F2 copy (provisional):** Non-res P1 and button titles now say "business, industry and institutions" (PR, S200); revisit when the exemption data request answers.

- [x] ✅ **F1 — DONE S197 (PR pending merge):** move `Run verified notebooks` after `Update status manifest (provenance + heartbeat)` in `refresh.yml`** (CI change, needs Peter's OK), then delete invariant 1. Until then the page's dates are one run stale, and the first refresh after the January year-roll checklist's step 9 reds on healthy data. ⚠️ **Do this before January.** First, check the 2026-09-28 render: it should say *last checked 2026-09-21*.

- [x] ✅ **F2 — DONE S197 (mutant reds by name, 8,159 unclassified):** replace the located-dollars identity with `rows["eligible"].notna().all()` and use `.astype(bool)` masks (findings §3).

- [x] **A verified notebook for the roads lens (Services).** ✅ 2026-09-28: `notebooks/verified/04_roads_lens.py`, 15 invariants + a week-over-week road-move table (info only); falsified ×3. The chain from
  road centrelines to road-metres per neighbourhood to the $/acre the panel shows
  has no end-to-end re-run. `docs/VERIFICATION.md` "What's covered so far" lists
  it among the uncovered `/full/` lenses. Model it on `01_money_lens.py`: import
  `src/` and assert invariants. It joins the weekly publish gate automatically,
  because the runner globs `notebooks/verified/`.
  - ⚠️ **Now also the only road delta signal (S202 audit §5):** nothing reads a
    served road column between refreshes; the 2026-09-28 refresh moved 45 hoods
    > 5% and only a by-hand decomposition explained them. Invariants measured
    that day, ready to assert: citywide metric km in a band (3,655.4); split
    conserves exactly; served = `load_roads` rebuild to 1e-3; `roads.geojson`
    `v` = served to 0.06; cost ÷ length = config rate; `road_m_unknown` = 0;
    outside-boundary share < 1% (0.28%). Feasible on CI: `03_assumptions`
    already runs `load_roads` on the runner. (Services is PUBLIC since
    2026-09-02 — "`/full/` lenses" above is stale.)

- [x] **Possibly an `AGENTS.md` for the repo**, so tools other than Claude Code
  get the same instructions. Decide whether it is a pointer or symlink to
  `CLAUDE.md` or a separate file. A copy would drift, and `CLAUDE.md` changes
  weekly. Check what `cc-data-project-template` does and keep the two consistent.
  **CLOSED 2026-09-25 (S196), no file:** Peter's call. An agent from another tool finds `CLAUDE.md` by looking around the repo, the repo takes no outside contributions, and much of `CLAUDE.md` is Claude-Code-specific anyway. Revisit in `cc-data-project-template` if anywhere.

- [x] **SERVICES' HOVER STILL TEASES A CHART ITS PANEL DOES NOT OPEN** — CLOSED 2026-09-24 (S194): Peter picked `click to compare with service costs`; Ratio lost its fallback history panel and 44 Development hoods stopped falling through to it (`verify-hoodmode.js` sweep). **Was:** the same
  defect fixed on the revenue cuts 2026-08-16, left live because the replacement
  copy is Peter's call.** In Services (with the cost columns shipped) the hover
  plots the **assessment-share sparkline** and says **`click to pin`**, while the
  click opens the **cost-against-revenue panel** (`servicePanelFor`, 2026-08-10).
  Measured, not inferred: `hoodPanelLens()` is `!serviceLens() || state.hasRoadsLife`,
  so the teaser is appended there like anywhere else. ⚠️ **Predicate name
  corrected 2026-09-16 (S166) — it read `state.hasSvcCost` until 2026-09-05,
  when the retired roads+fire composite took that flag with it; the gate had to
  name a column the PUBLIC build actually shows. The DEFECT is unchanged and
  still live — `web/index.html`'s own comment above `tooltipFor` says so:
  *"SERVICES IS NOT YET EXCEPTED though it should be … the hover still plots
  history under a click that opens costs."*
  - ⚠️ **`docs/CONTROLS_MATRIX.md` asserted the OPPOSITE** ("the sparkline is
    not [offered in Services]") from 2026-08-10 until this was measured on
    2026-08-16. The cell is corrected; the point is that the claim sat unchecked
    for six days because nobody hovered a Services hood.
  - **The fix is one predicate** — the revenue branch in `tooltipFor` already
    demonstrates it; Services needs `servicePanelFor(p)` treated the same way.
  - **What is NOT decided is the invite's wording.** The revenue cuts say
    `click for the revenue mix`; Services would need its own line (`click for the
    cost breakdown`?), and naming a "cost" in one phrase brushes the locked rule
    that ⚠️ **there is no single cost number and there cannot be** — two bases,
    ~10.8× apart, deliberately not summed (`data/DATA.md` §13, `SPEC_services.md`).
    A hint that implies one total would be the same class of error as the chart.
  - Precedent + full reasoning: `docs/DECISIONS.md` 2026-08-16 (the sparkline
    row), `docs/SPEC_temporal.md` §2 (the amended row).


### `verify-services-panel.js` and `verify-ratio-denom.js` are red on the public build (FOUND 2026-09-24 S193)

Four checks fail on master as well as on branches: *"transit / bike / transitcost /
bikecost: the panel opens and is not empty — 0 rows"*. Those services are
full-only (`SERVICES[*].pub` false), so the public build has no rows to show. It
is the missing build gate `tools/profiling/README.md` convention 1 describes.
The script is not in CI, which is why nobody saw it. Fix: gate those four on
`FULL_BUILD` and print `PARTIAL`, the way `verify-transport-cost.js` does.

`verify-ratio-denom.js` has the same defect: *"ratio: picker shown"* fails on
the public build, where the denominator picker is full-only by design
(`ratioDenomShow` requires `FULL_BUILD`). It passes 42/42 on the full build.

**CLOSED 2026-09-24 (S194):** both scripts read `FULL_BUILD`. `verify-services-panel.js` skips §1–3 on a public URL (its §4 already covers the three public layers) and prints `PARTIAL`. `verify-ratio-denom.js` asserts the picker matches the build in both directions, skips the fire §4–9 on public, and prints `COMPLETE`/`PARTIAL`. The public run had been passing ~20 fire checks by JS-clicking the hidden picker. Falsified: ungating `ratioDenomShow` turns the public run red.

### Publish-path ordering — two latent CI races (OPEN 2026-10-05 S215, `docs/FINDINGS_ci_publish_paths.md`)
- **F1:** a `web/**` merge during a refresh queues a `deploy.yml` run that checks
  out its trigger SHA and republishes last week's data. Proposed: `ref: master`
  on deploy.yml's checkout, plus a `test_ci_workflows.py` assertion.
- **F2:** a later code push cancels a PENDING refresh (default `queue: single`).
  Proposed: `queue: max` on both workflows.
- CI changes → Peter's OK before building. Neither race has fired (0 of 100 deploys).

**CLOSED 2026-10-05 (S216):** both fixes built — `ref: master` on `deploy.yml`'s checkout, `queue: max` on both workflows' `concurrency`; guarded by `test_the_code_deploy_builds_from_the_branch_tip` and `test_the_publish_group_keeps_every_pending_run`.

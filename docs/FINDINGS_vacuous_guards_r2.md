# Findings — checks that cannot fail, run 2 (2026-09-08, Fable 5.1, read-cold)

Instrument: `docs/FABLE_AUDIT_vacuous_guards.md` (T2 method corrected 2026-09-08).
Run 1 (Opus 5, 2026-09-07): `docs/FINDINGS_vacuous_guards.md`. This run is the
**first cross-model check** on run 1's findings, S145's fixes and S146's
withdrawal — the "instrument-chain" caveat those handoffs carried. Ledger row:
2026-09-08. Scope as the brief defines it: the guard/test estate and its wiring,
not the lenses.

**Two HIGH defects, both reproduced end to end; one MEDIUM in the publish gate;
one mutation-sweep triage; one latent collapse. Every prior fix re-falsified
and still red. Three claims formed mid-run were WRONG and are recorded in §7.**

Method, as the brief demands: **falsification, not reasoning.** Every finding
below names the check, the mutation, and what actually went red. Suite baseline
**800 pass**. All measurements were run alone (no concurrent verify runs).

---

## R1 — a served column can go ALL-NULL and the entire weekly publish path stays green  (T3, HIGH) — **FIXED 2026-09-08**

**The check:** `scripts/check_served_columns.py`, the committed schema
baseline (`data/expected_columns.json`, 67 columns), the guard `DECISIONS.md`
2026-08-03 installed because *"a dropped column is caught by a committed schema
baseline on the data side, not by the render gate."* S146 pinned
`rev_frac_exempt` in it two days ago.

**The property it names:** every baselined column is on every feature.

**Why it cannot vary in the way that matters:** `column_presence()` counts
**key presence, not non-null values** — documented, and for a good reason (the
four `*_per_lot_acre` columns are null on the seven set-aside hoods by
design). But *"null on some hoods"* and *"null on every hood"* are different
states, and the guard cannot tell them apart. A pipeline that emits NaN for a
column (a failed join, a renamed upstream field read with `.get()`) serialises
to `null` on all 406 features, the key is present on all 406, and the guard
reports OK.

**Falsified 2026-09-08, three ways:**

| mutation (committed served file, copy) | `check_served_columns` | `verify-smoke.js` (public) |
|---|---|---|
| `revenue_per_acre` → null on 406/406 | **exit 0** — "all 67 baselined columns present on all 406 features" | exit 1 — but **only** `C-ratio: legend bounds … ≤ $NaN .. $NaN+` |
| `res_revenue_per_acre` → null on 406/406 | **exit 0** | **exit 0 — ALL CHECKS PASSED** |
| (control) `rev_frac_exempt` key removed | exit 5, `MISSING` | — |

⚠️ **The second row is the finding.** With the public Residential-revenue lens
carrying no number for any neighbourhood, the data guard passes, the render
gate passes, and `refresh.yml` would commit and deploy it. The first row only
reddened because the **ratio** view divides by revenue — a *different*
assertion in a *downstream* view, which §5 of the brief classes as itself the
finding.

**Why the render gate is structurally blind here, not merely unlucky:**

- `C-money / residential: every hood renders a readout — 406 rendered`:
  `viewTooltip` omits a null row rather than printing it, so the tooltip still
  renders and still counts. Run 1's B6 comment already records this limit.
- `C-money / residential: legend bounds are not garbage — $0 .. $30k+`: the
  money legends are **static literals** (`legendMax: "$30k+"` in `METRICS`),
  not derived from the data, so a data collapse cannot reach them.
- `check_revenue_deltas.py` compares `METRIC = "total_revenue"` only.
- Nothing else on the path reads per-hood values of a served column.

**Sized against the distribution (the `size-remedies-against-the-distribution`
rule):** in today's served file **0 of 67** baselined columns are all-null;
**5** carry any nulls at all (`far` 16, the four `*_per_lot_acre` 7 each), so a
worst case of 16/406 = 3.9%. An *all-null is drift* rule would red nothing
today and would have red both mutations above.

**Blast radius:** T3 — wrong (empty) public data for up to a week, on the one
path that changes the site with nobody looking. It is exactly the class the
2026-08-03 decision was written for, one state further along: the column is
present and empty instead of absent.

**Fix — PROPOSAL, not built (it changes what the publish gate accepts):**
extend the baseline to carry a per-column null count (or null fraction) and
fail on a column that is null on **every** feature; optionally warn on a null
count that jumps by more than the baseline tolerates. The committed baseline is
the right place because, as run 1 noted for B7, only a baseline can tell "was
numeric last week" from "legitimately null". Pair it with the R3 one-liner in
the same PR (both are publish-gate tightenings). Falsification for the fix:
the two all-null copies above must return exit 5 and the unmutated file exit 0.

---

## R2 — the merge gate's guards can be neutered at their exit line, or deleted from the workflow, with 800 tests green  (T1, HIGH) — **FIXED 2026-09-08**

**The checks:** `check_cost_copy.py` (T1 merge gate — the *only* tie between
the map's rates and its captions, hardened in run 1), `check_value_anchors.py`
and `check_temporal_years.py` (T3, both gate the weekly publish), and the
wiring test `tests/test_ci_workflows.py`.

**The property they name:** drift → non-zero exit → the workflow step fails.

**Why it cannot vary:** every test for these three guards exercises the
*detector* (`check()`, `structural_checks()`, the anchor comparison) and none
exercises `main()`. `grep -c "main(" tests/test_check_{cost_copy,value_anchors,temporal_years}.py`
→ **0, 0, 0.** The detector can find drift and `main()` can still return 0, and
the suite is the same 800 green. Run 1 gave `check_cost_copy` 13 tests "led by
the falsification"; all 13 stop one line short of the exit code CI reads.

**Falsified 2026-09-08 — four mutations, each run alone, each 800 pass:**

| mutation | suite |
|---|---|
| `check_cost_copy.py` drift branch `return 5` → `return 0` | **800 passed** |
| `check_value_anchors.py` dangerous-move branch `return EXIT_DRIFT` → `EXIT_OK` | **800 passed** |
| `check_temporal_years.py` failures branch `return EXIT_DRIFT` → `EXIT_OK` | **800 passed** |
| `tests.yml` with the cost-copy step **deleted** | **800 passed** |

The fourth row is the wiring half. `test_ci_workflows.py` was written (audit
2026-08-28 F3) to pin *"membership IS the wiring"* — and it pins **pytest's**
membership in `tests.yml` and `refresh.yml`, i.e. 2 of the ~14 guard steps
across the three workflows. The cost-copy and doc-citation steps on the merge
gate, the six `check_*.py` steps and the smoke-before-upload order on the
refresh path, and the smoke's *position* before `upload-pages-artifact` are
all unpinned. Its one pytest assertion is also `any("pytest" in r …)` — a
`run:` step reading `echo skipping pytest` satisfies it.

**Same shape, one level down, from the sweep (§R4):** `refresh.yml` maps the
year guards' exit codes with literal `case 0) 3) 4)` labels while the scripts
define `EXIT_HOLD = 3`, `EXIT_INCONCLUSIVE = 4`. Mutating `EXIT_HOLD` 3 → 6 is
**green** (the tests import the constant from the module). In CI a genuine
hold would then fall to `*) exit $code` — a hard failure with **no banner and
no hold state written**, instead of the designed keep-last-good-plus-banner.
Loud rather than silent, so lower severity — but the two literals agree by
coincidence, pinned by nothing.

**Blast radius:** T1 for `check_cost_copy` — a wrong public rate merges and
publishes minutes later, which is the project's cardinal failure and the thing
this guard exists for. T3 for the other two.

**Fix — test-only, ready to build, no CI behaviour change:** one `main()`-level
test per guard asserting the exit code on a drifting fixture (`check_cost_copy.main()`
takes no `argv`, so monkeypatch `sys.argv`); and `test_ci_workflows.py` pins
for (a) every guard step's command in each workflow, (b) smoke on **both**
builds immediately before `upload-pages-artifact` in `refresh.yml`, and (c) the
`case` labels equal to the scripts' `EXIT_*` constants. Falsification for the
fix: the four mutations above must each red **by name**.


### ✅ FIXED 2026-09-08 (S147) — test-only, 800 → 820, no CI behaviour changed

**Every mutation in the table above now reds by name, and only that name.**

| what | pin |
|---|---|
| the three guards' exit mapping | `test_main_exits_nonzero_on_drift` (cost copy), `test_main_exits_with_the_drift_code_*` (value anchors, temporal years) — each drives the real `main()`, and each has an **opposite-direction sibling** asserting the OK exit, so a guard wired to always drift cannot pass them |
| the guards' membership in every workflow | `test_the_merge_gate_runs_both_offline_guards`, `test_the_weekly_refresh_runs_every_data_guard` (8 steps), `test_the_monthly_digest_runs_the_report_that_carries_the_checks` |
| the smoke gate's POSITION | `test_the_smoke_gate_sits_between_the_build_and_the_upload` — asserts `upload - smoke == 1`, so a step inserted between them reds too; `test_the_smoke_gate_covers_both_builds` pins the two invocations |
| `refresh.yml`'s `case` labels | `test_the_refresh_case_labels_match_the_scripts_exit_codes` — the labels are **derived** from each script's `EXIT_*`, so the two drifting apart reds here |

⚠️ **Only the CSV READERS are replaced in the two `main()` tests.** The anchor
computation, the splice, the structural checks, the band comparison and the exit
mapping are the real ones — a test that stubbed the detector would assert the
stub. The temporal fixture spans `FIRST_YEAR` onward because `main()` calls
`structural_checks` with the default `first_year`, so a short fixture would red
for a reason unrelated to the test.

⚠️ **The value-anchor bands are written as literals, not derived from the live
frame** — a baseline computed from the data the guard reads is exactly the
vacuity this file documents.

⚠️ **Found while writing it, and it is this class again:** the first draft read
the success code as `getattr(mod, "EXIT_OK", None) or getattr(mod, "EXIT_ALIGNED")`.
`EXIT_OK` is **0**, so `or` fell through and the test raised `AttributeError`
instead of comparing anything. Caught because the test ran red; a falsy pin that
had happened to be non-zero would have passed while comparing the wrong thing.

---

## R3 — `verify-smoke.js` B8 examines rows through a selector and drops the misses, so a markup rename leaves it green with zero rows examined  (T3, MEDIUM) — **FIXED 2026-09-08**

**The check:** B8, *"each services row is offered exactly when its column is
present"*, in the one browser check that gates a publish.

**The property it names:** a services row's inline `display` agrees with its
column's presence, for every row in the build's population.

**Why it cannot vary:** rows are found with
`document.querySelector('#services .svc[data-service="…"]')`; a miss yields
`null`, and the comparison filters `hidden !== null` **out**. Rename the
attribute, move the rows out of `#services`, or change the class, and every
entry is `null`, the filtered list is empty, and B8 prints PASS with nothing
examined — §1's "N passed" that is not a measurement.

**Falsified 2026-09-08 on the full build (population 9 plane rows; public is 2 —
`roadscost`, `roadslife`):**

| mutation (built copy) | B8 |
|---|---|
| `transit` row given inline `display:none` while its column is present | **FAIL — `transit_dep_per_acre gated off but present`** (B8 can red) |
| every `data-service=` → `data-svc=` | **PASS**, 0 rows examined, ALL CHECKS PASSED |

⚠️ **Method note, because the first attempt proved nothing:** the first
falsification hid the **roads** row — the one service with no `plane.col`,
which B8 excludes by design — and B8 passed. That PASS said nothing about B8.
Confirm the mutated element is in the check's population before reading the
result (§7).

**Blast radius:** T3, narrow — the failure it would miss is a services-row
gate mismatch after a markup refactor of `#services`. Low probability, but the
fix is one line.

**Fix — one line, bundle with R1's proposal:** report `n rows examined` in the
extra text and fail when `n === 0`.


### ✅ FIXED 2026-09-08 (S147) — R1 and R3, one PR, as proposed

**R1 — `empty_columns()` in `check_served_columns.py`.** A baselined column
carried on **every** feature and null on **all** of them is now a third failing
bucket, `EMPTY`, alongside `MISSING` and `PARTIAL`. Falsified against the real
served file three ways — `res_revenue_per_acre`, `revenue_per_acre` and
`rev_frac_exempt` each nulled on all 406 features → **exit 5** with
`EMPTY — present but null on all 406 features`; the unmutated file → **exit 0**.

⚠️ **The other direction is pinned too, because it is the cry-wolf risk:** a
column null on *some* features stays OK (`far` is null on 16 of 406 hoods and
the four `*_per_lot_acre` on the seven set-aside hoods, by design), and an
absent or half-written column is still reported as `MISSING`/`PARTIAL` only —
one defect, one diagnosis. Five tests, including both directions of `main()`.

⚠️ **The render gate is unchanged and still cannot see this.** Re-measured after
the fix: the all-null copy gives `verify-smoke.js` **ALL CHECKS PASSED** and
`check_served_columns.py` **exit 5**. That split is the 2026-08-03 decision
working as designed — only a committed baseline can tell "empty now" from
"empty always" — not a gap left open.

**R3 — B8 counts its population.** `svcGateSeen` is the rows the selector
actually found; the check now requires `> 0` and prints `N rows examined`.
Falsified on built copies: base **PASS, 2 rows examined** (public) and **9**
(full); every `data-service=` → `data-svc=` gives **FAIL, 0 rows examined** on
both builds; and a genuinely mis-gated row still reds with its own message
(`transit_dep_per_acre gated off but present`), so the new guard did not
displace the old one.

**Suite 820 → 825.** `DECISIONS.md` 2026-09-08.

---

## R4 — mutation sweep: 58 of 75 UPPERCASE numeric constants move with the suite green — triaged, most are NOT findings  (T5/T3)

**Instrument:** each `NAME = <number>` in `src/*.py` and `scripts/*.py`,
mutated one at a time (×2; years +1), suite run alone, file restored. **The
instrument produced negatives before its totals were read:** both
`SQ_M_PER_ACRE` pins red **by name** (`test_sq_m_per_acre_is_the_international_acre`
in both modules), and 17 constants red overall — `LOW_PARCEL_FRAC`,
`SET_ASIDE_THRESHOLD`, `RESIDENTIAL_THRESHOLD`, `FIRST_YEAR`, `SHARE_SCALE`,
`WEB_PRECISION`/`WEB_SIGNIFICANT_FIGURES`, `DATA_YEAR`, `MIN_PCT`,
`MIN_ABS_DOLLARS`, `NEEDLE_PCTILE`, … each by a test that names it.

**The 58 greens, ranked (only the first group is a finding):**

1. **Guard bands and calibration, unpinned (6) — T3, MEDIUM.**
   `check_temporal_years.HISTORICAL_TOLERANCE` 0.5% → 1% (the band on settled
   years — the sentinel over the 2024-signature defect — **doubles unnoticed**),
   `LIVE_GROWTH_MIN` −0.5% → −1%, `LIVE_GROWTH_MAX` 25% → 50%,
   `check_roll_year_against_fir.MAX_PLAUSIBLE_RESIDUAL` 5% → 10%,
   `check_value_anchors.STALE_RAW_DAYS` 14 → 28 and `MISMATCHED_RAW_DAYS` 2 → 4.
   A loosened guard is silent by definition. ⚠️ The estate already has the
   fix, applied to one guard: `test_thresholds_are_the_measured_pair` pins
   `MIN_PCT`/`MIN_ABS_DOLLARS` in `check_revenue_deltas`. And
   `test_growth_floor_sits_below_the_observed_minimum` **cannot** catch a
   loosening floor — a wider band still sits below the observed minimum.
   **Fix:** literal pins with the measurement that set each value, per the
   revenue-deltas pattern. Test-only.
   ✅ **FIXED 2026-09-08 (S147)** — all six pinned to their literals with the
   measurement that set them, per the `test_thresholds_are_the_measured_pair`
   pattern: `test_the_growth_band_is_the_measured_pair` and
   `test_the_historical_band_stays_tight` (temporal years),
   `test_the_raw_vintage_windows_are_the_documented_pair` (value anchors),
   `test_the_fit_thresholds_are_the_documented_pair` (roll year — `MIN_SEPARATION`
   pinned alongside, since the same tests build their fixtures from both). Each
   reds by name when its constant moves.

2. **Published provenance, unguarded (1) — LOW.** `generate_status.ZONING_YEAR`
   2024 → 2025 is served as `status.json` `zoning_year` and nothing measures
   it. `RATE_YEAR` is caught monthly by `vintage_report.check_year_constants`
   (not by pytest — `test_year_constants_flag_drift` asserts only that
   `"DATA_YEAR"` appears in the detail, so dropping `RATE_YEAR` from that check
   is also green).
3. **`EXIT_*` codes (14) — self-referential, matters only in `refresh.yml`'s
   `case` labels.** Tests import them from the module under test. Folded into
   R2.
4. **Checked and NOT findings (7):** `load_temporal.VALUE_UNIT` (travels in
   `temporal.json` as `value_unit` and the page reads it — a ×2 changes
   precision, not values; its sibling `SHARE_SCALE` is pinned because the test
   asserts a ppm literal); `load_roads.WEB_MIN_PART_M` and the `WEB_SIMPLIFY_*`
   family (applied in `export_roads_web` only; `road_m_per_acre` is computed
   upstream from the overlay); `YEAR_BUILT_MIN/MAX` (flag and log, not drop);
   `INST_FRAC_DECIMALS`, `FRACTION_DECIMALS` (rounding); `UNASSIGNED_WARN_FRAC`
   ×2 (warn thresholds); `NODE_SNAP_M`.
5. **Off every automated path (30):** `build_reference_layers.py` ×10 —
   including `WORKING_EPSG` 3400 → **6800, a CRS that does not exist**, so the
   script's CRS path is simply untested — `build_levy_catchments.AREA_CRS`,
   `fetch_fir_debt`, `fetch_construction_price_index`, `scrape_dc_provisions`,
   `export_budget_ranked`, `check_doc_citations.MIN_BARE_NAME`. Hand-run
   producers of committed artefacts; recorded, not ranked.

⚠️ **Do not quote "58 green" as a defect count.** Five is the number of
constants whose silent movement would let wrong data or a loosened guard
through; the rest are precision, warnings, or scripts nothing schedules.

---

## R5 — `check_revenue_deltas.load_committed` turns ANY `git show` failure into "first publish, nothing to compare"  (T3, LOW — latent)

`load_committed()` returns `None` on any non-zero `git show` exit; `main()`
logs *"first publish, nothing to compare against"* at INFO, writes
`flagged=0`, exits 0. "Path not in that commit" and "git failed" (wrong cwd,
shallow-history surprise, binary missing) collapse into the same silent skip.
**Confirmed live in the 2026-09-07 run log** — *"Revenue-delta guard OK …
across 406 neighbourhoods"* — so this is a latent collapse, not a current
one, and the guard is warn-only by policy. **Fix:** distinguish the two
(`git cat-file -e` first, or match the "does not exist in" stderr) and make
the second a WARNING with a distinct line.

---

## §6 — Tiers and prior fixes that came back clean (falsified, not assumed)

- **Every run-1 / S145 / S146 fix still reds when falsified.** `SQ_M_PER_ACRE`
  ×2 by name (sweep); `SETBACK_CRS` — mutating `load_boundaries` alone reds the
  derived assertion (`assert 3400 == 26911`); `rev_frac_exempt` removed →
  `check_served_columns` exit 5 `MISSING`; the V4 build-gated scripts were not
  re-run (no change to them since the S145 20/20 sweep).
- **Wiring confirmed in run logs, not callers** (the corrected T2 method):
  refresh run `34130304644` (2026-09-07, scheduled) carries
  `ALL CHECKS PASSED` for **both** builds plus the roll-year ("aligned,
  residual +1.2%"), unmatched-names, value-anchor (6/6) and revenue-delta
  (406) verdict lines; tests.yml run `34182562756` on `18792ab` carries the
  doc-citation and "all 7 quoted rates match" lines. `check_year_alignment`
  reports INCONCLUSIVE **every** run by design (`DECISIONS.md` 2026-08-25 —
  the proxy class), so its `::warning::` fires weekly; noted, not a finding
  here.
- **T5 fixture shapes.** An AST scan for (a) asserts with identical sides,
  (b) `assert <truthy literal>`, (c) the same function called on both sides of
  `==`, (d) dict fixtures giving two keys the same number (the S142 `$2.0`
  shape) returned three candidates in (d), each inspected: every one has a
  second row that separates the values (`test_aggregate_by_neighbourhood`
  ×2, `test_join_and_calculate:378`). No `skip`, `xfail`, or bare `except` in
  `tests/`. `pytest -q` reports **800 passed, 0 skipped**.
- **T2 `deploy.yml`:** unchanged since run 1 — still no check between build
  and upload; the S146 Tier 1/2/3 proposal stands and is Peter's call.
- **T4 tautology grep** (`check(name, true)` outside early exits;
  `.length >= 0`): the only hits are the sanctioned early-exit reporters and
  `verify-revenue-panel.js`'s `segments.every(w => w >= 0)`, which sits behind
  a real `length === rows.length` conjunct. Not findings.

---

## §7 — What this run got wrong

1. ⚠️ **"WRONG SERVER" ×4 on servers that were right.** My harness compared
   `/proc/<pid>/cwd` with the served directory and aborted every smoke run —
   but `python -m http.server --directory X` does **not** chdir, so cwd was
   the repo. The memory `confirm-the-server-you-measure` assumes a server
   started *from* the directory; it has been corrected. Re-run with
   `(cd X && exec python -m http.server …)`.
2. ⚠️ **The first B8 falsification landed on a row B8 excludes** (roads, no
   `plane.col`) and I briefly read its PASS as evidence about B8. Rule added
   to the brief: confirm the mutated element is in the check's population.
3. **`build_site.py` failed under the box's `python3` (3.6, no
   `capture_output`)** — CI runs 3.12; instrument, not estate.

The class under audit reappeared twice in the audit's own instruments, as it
did in run 1 — a check that reads the wrong thing and reports confidently.

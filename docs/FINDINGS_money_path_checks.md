# Findings — which automatic checks protect the Money path (S264, 2026-11-26, Opus 5.5)

Run of `docs/FABLE_AUDIT_money_path_checks.md`. Measured at `6c77dd2`
(origin/master), on data downloaded fresh by `scripts/download_data.py` on
2026-11-26 into a scratch worktree. The plain-language checklist built from this
matrix is `docs/MONEY_PATH_CHECKS.md`.

## 0. The answer

**The machine protects the Money path against code bugs. It does not protect it
against bad data.**

- All 11 code mutations (M4–M14) turn the merge gate red by name, so none of
  them can reach master through a PR. For 6 of the 11, the only red check is
  pytest: one test file, or one test.
- Of the 5 input mutations (M1, M2, M2b, M3, plus T1b's year re-run), only M1 (last
  year's roll) is held. **Three publish with every blocking check green:**
  - a roll with its top 1% of accounts missing (citywide levy −42.9%);
  - a roll with 1% of accounts missing at random (−1.1%, one hood −32%);
  - a 2026 residential mill rate 10% too high (+4.5%).

  The first of the three files a GitHub issue after the data has published. The
  other two produce no signal anywhere.
- The project's real failures have come from upstream data (`DERELICT
  RESIDENTIAL`, GTFS dates, account `9977123` in #818), not from code edits. So
  the weak side is the side that has actually failed.

| Level | Question | Verdict |
|---|---|---|
| L0 | Is "mutate one step, see what goes red" the right measure? | **SOUND, weighted.** Right for code; data mutations count for more here, and they are where the checks are weak |
| L1 | A blocking red for every mutation, per C step? | C2 **CONDITIONAL** (year yes, completeness no) · C3 **UNSOUND** (rate value) · C4 **SOUND** · C5 **SOUND** · C6 **SOUND** · C8 **SOUND** |
| L2 | Single points of failure | 5 checks: `tests/test_apply_tax_rates.py` (M4–M7), the lot-acre tests in `tests/test_join_and_calculate.py` (M10), `test_sq_m_per_acre_is_the_international_acre` (M12), the Money notebook's two "aggregation preserves" checks (M8), `check_roll_year_against_fir.py` (M1) |
| L3 | Mutations caught by 3+ blocking checks | **2** (M9, M13). Left alone |
| L4 | Do warn-only catches reach a reader? | **Yes where they fire** (issues for M2, M5, M8). M2b and M3 fire nothing at all |

## 1. Method, as run

- A scratch `git worktree` at `6c77dd2`, with its own fresh `data/raw/` (the
  shared copy in the main checkout dated from 2026-09-03, so it was not used).
  The roll was saved untouched once.
- Between mutations, `restore.sh` ran `git checkout -- .`, restored the untouched
  roll, cleared `__pycache__`, and asserted a clean tree. "clean: 6c77dd2" was
  printed before every mutation.
- The tiers ran in CI order:
  1. pytest and the four merge-gate scripts;
  2. `check_unmatched_names`, `check_permit_names`, `check_year_alignment`,
     `check_roll_year_against_fir`;
  3. `main.py --skip-png`;
  4. `check_value_anchors`, `check_suite_share`, `check_served_columns`,
     `check_colour_clamps`, `check_revenue_deltas`, `check_temporal_years`,
     `generate_status`;
  5. all four verified notebooks;
  6. `build_site` and `verify-smoke.js` on both builds;
  7. pytest again on the regenerated data ("next week's" gate).
- Browser checks ran one at a time. The http log was read to confirm the smoke
  checks hit this run's `_site`.
- **Control:** every step green. 1,242 passed (pre and post), 0 revenue deltas,
  smoke PASS on both builds. `check_year_alignment` exits 4 (the known
  inconclusive, a warning in CI) in every run, the control included, so it is
  left out of the matrix.
- **Mutant loaded:** every mutation that ran to the end changed the served file.
  The diff against the control's `neighbourhood_value_per_acre.geojson` is in §2.
  None of the gaps is a mutation that changed nothing served.

## 2. The matrix

Cells: **F** blocks (fail, hold or raise) · **W** warns through a GitHub issue · `·`
green · `–` not reached in CI. The red message is in the notes column.

| ID | C | Mutation (as applied) | Served effect | pytest | unmatched | roll-year | main.py | nb 01 | nb 02/04 | smoke | rev-delta | clamp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | C2 | roll values × 0.9237 (the FIR 2025/2026 residential ratio; no prior-year parcel file exists) | levy −7.6% | · | · | **F** hold | – | – | – | – | – | – |
| M2 | C2 | top 1% of accounts by value dropped (4,399; 25.8% of value) | levy −42.9%; DOWNTOWN −84% | · | · | · (+1.6% → +0.4%) | · | · | · | · | **W** 205 hoods | **W** |
| M2b | C2 | 1% of accounts dropped at random (4,398; 1.03% of value) | levy −1.1%; MILL WOODS PARK −32% | · | · | · | · | · | · | · | · | · |
| M3 | C3 | 2026 Residential 7.7419 → 8.5161 (×1.10), `status.json` regenerated | levy +4.5%; worst hood +9.99% | · | · | · | · | · | · | · | · (under 10%) | · |
| M4 | C3 | `load_mill_rates` reads year − 1 | levy −2.5% | **F** 8 tests | · | · | · | · | · | · | · | · |
| M5 | C4 | `COMMERCIAL` → `Residential` | levy −33.1% | **F** 2 tests | · | · | · | · | · | · | W 156 | W |
| M6 | C4 | slot 1 at 100%, slots 2–3 at 0% | 157 hoods move, up to +8.8% | **F** 4 tests | · | · | · | · | · | · | · | · |
| M7 | C4 | exempt label billed at Non Residential | +$192k in 3 hoods | **F** 2 tests | · | · | · | · | · | · | · | · |
| M8 | C5 | aggregation keeps only `[A-Z ]+` names | 3 hoods vanish (wîhkwêntôwin, Hollick-Kenyon, River's Edge; $5.6B, $58.6M levy) | · | · | · | · | **F** | · | · | W 3 disappeared | · |
| M9 | C5 | name corrections moved after aggregation | (raised) | **F** 2 tests | **F** exit 5 | · | **F** `MergeError` (`validate="m:1"`) | – | – | – | – | – |
| M10 | C6 | `safe_lot = safe_area` (ground acres in the lot-acre ratio) | lot-acre metrics, worst −83.7% | **F** 3 tests | · | · | · | · | · | · | · | · |
| M11 | C6 | area taken before `to_crs(3400)` | (raised) | **F** 1 test | · | · | **F** `check_lot_acre_bounds` (405 hoods) | – | – | – | – | – |
| M12 | C6 | `SQ_M_PER_ACRE` 4046.86 → 4000 | every per-acre −1.16% | **F** 1 test | · | · | · | · | · | · | · | · |
| M13 | C6 | set-aside `>=` → `<` | all 406 grey flags flipped | **F** 7 tests | · | · | · | · | **F** nb 02 | **F** | · | W |
| M14 | C8 | export at 3 significant figures (was 6) | every money figure ≤0.5% off | **F** 1 test | · | · | · | · | **F** nb 04 (roads) | F* | · | · |

\* M14's smoke red, and the one M1 would have shown if CI had not held it, is
the same knife-edge on one hood. It counts as caught by accident (F3).

**Notes on the red checks:**
- **M4.** The tests fail with `KeyError: No mill rates for year …` because their
  fixtures carry one year. They also compare levies to expected values, so a
  fixture with two years would still fail on the values. The pipeline itself ran
  M4 without raising, because 2025 exists in `mill_rates.json`.
- **M8.** The red is the Money notebook's "aggregation preserves total assessed
  value" (delta $5.6B) and "aggregation preserves total levy" (delta $58.6M).
  `check_unmatched_names` stays green because it compares names, and these names
  never reach the join.
- **M9.** Three blocking checks fire. `check_unmatched_names` says `NAME DRIFT —
  10 assessment neighbourhood(s) newly have no boundary match`, and the merge
  raises on its `validate="m:1"` guard.
- **M13.** Notebook 02 fails on "the grey flag is exactly the set-aside share at
  or above the threshold — 358 flagged". The smoke check fails on zero-looking
  `(0%` shares in 19 hoods.
- **M14.** Notebook 04 (Roads) fails on "served road metres per acre equals the
  rebuild" (max diff 0.049). That is a cross-lens catch: **no Money check reads
  the served file.**
- **T1b re-run (brief §0.2).**
  - `city_budget_context.json` `year` 2025 → 2019, with `status.json` regenerated,
    is **now red by name**: `test_acknowledgement_does_not_reach_the_published_manifest`
    (`assert 2019 == 2025`, test added 2026-09-17). `check_budget_context()`
    now runs in the monthly digest. T1b's M3 is closed.
  - T1b's M4′ (a wrong rate, propagated consistently) still passes. It is M3 here.

## 3. Findings

### F1. A partial roll publishes: nothing blocks missing accounts, and a small loss is silent (C2)

**Evidence.** M2 and M2b, above. The download step's count check compares against
the server's own `count(*)`, so a publisher-side omission passes it by
construction. `check_roll_year_against_fir.py` reads only the residential taxable
base, by design, so M2's 25.8% value loss moved its residual only from +1.6%
(control) to +0.4%: the top 1% of accounts are mostly non-residential. M2b moved
it to +0.6%. Both sit far inside its 5% plausibility band. The guard answers
"which year is this roll", not "is the roll whole", and its docstring says so.

**Shape.** This is #818's shape: account `9977123` ($67.5M) left the roll, and the
only signal was the revenue-delta issue, because that one move was large. Losses
under ≥10% **and** ≥$1M per hood, or spread across hoods, publish with no
signal. M2b took MILL WOODS PARK down 32% and stayed under $1M.

**Proposal, not built** (a guard is a code PR for Peter): compare the
**non-residential and total** taxable base to FIR as well as the residential one,
as a completeness band. `FINDINGS_levy_as_revenue.md` §0.2 records the known
total gap (+11.2%), so the band would be set on that residual, and its movement
would carry the signal.

### F2. A wrong mill rate still publishes with every check green (C3; T1b M4′ re-confirmed 72 days on)

**Evidence.** M3. `vintage_report.check_mill_rates` still compares years only.
The value comparison T1b proposed on 2026-09-15 was not built. The 10% error
lands at most at +9.99% in any one hood, so the revenue-delta guard (≥10%)
misses it by construction, and a smaller error is further below. The merge gate
catches a rate edit only when `status.json` is left stale. A PR that regenerates
it, as a careful author would, passes.

**Proposal, not built:** T1b's loop. Compare the pinned year's five class rates
in `pwis-wc4c` to `mill_rates.json` inside `check_mill_rates`.

### F3. The smoke check's zero-readout test can fail a correct page at UNIVERSITY OF ALBERTA FARM

**Evidence.** The hood's served `rev_frac_exempt` (its share of levy on
exempt-candidate zoning, `src/revenue_by_zone.py`) is `0.999997`. Under M1
(values −7.6%) and under M14 (3 significant figures) it becomes exactly `1.0`.
The tooltip's low endpoint, revenue × (1 − share) (`web/index.html`, the
`exemptFrac` range), then prints `$0`. `C-money / revenue`, `C-money /
non-residential` and `C-ratio / fire` go red on both builds. Nothing else about
that hood changed.

**Mechanism.** At a share of 1.0 that `$0` is a true computed zero: if every
exempt candidate pays nothing, this hood pays nothing. The check's zero test
blanks exactly-zero *properties* and re-renders. A zero *computed* from a
nonzero revenue and a share of 1.0 survives that, so the check reads it as a
floored figure.

**Risk.** A legitimate refresh that moves this hood's 3e-06 non-exempt remainder
can red the weekly publish on a correct page. Latent: it has not fired on real
data. The fix belongs in the check (`tools/profiling/verify-smoke.js`), and it is
a code PR for Peter.

### F4. The Money notebook cannot see a wrong number, only a lost one (design, recorded)

`notebooks/verified/01_money_lens.py` re-runs the same `src/` functions on the
raw data. It never reads the served file, so it agrees with the pipeline under
every mutation that is self-consistent (M3–M7, M10, M12, M14). Its one catch is
M8, where it is the **only** blocking check. This follows from its own rule
("invariants are asserted, values are not"), so it is not a defect. It does mean
"the verified notebook passed" says nothing about whether a Money figure is
right. The `MONEY_PATH_CHECKS.md` checklist says so plainly.

### Not findings (checked)

- Data commits to master before the smoke check runs. This is recorded in
  `PROJECT_AUDIT.md` step 8; the deploy is what is gated. One consequence not
  written there: next week's revenue-delta baseline is `git show HEAD`, i.e. the
  data the smoke check held back.
- `check_unmatched_names` is green under M8. It guards names at the join, and M8
  drops rows before the join. The notebook covers that case.
- 6 of the 11 code mutations are caught only by pytest. That is the merge gate
  doing its job. It is listed under L2 so nobody deletes those tests as
  redundant.

## 4. What this run got wrong

- **My own mutation sites favour the tests.** I chose the brief's sites, and most
  of them are where earlier audits put a test (M12's literal pin exists because
  of `FINDINGS_vacuous_guards.md` V2). A code bug at an untested site would score
  worse than 11 of 11. The same model wrote many of these checks. "Code is
  covered" holds for these sites, not for `src/` in general.
- **M11's first patch never applied.** It assumed the `to_crs` and area lines were
  adjacent, but a comment sits between them. The run printed the assertion and
  moved on, and the first pass reported 13 mutations, not 14. M11 was rewritten
  and run separately.
- **My T1b re-run loop passed each script its own name as an argument.** That
  produced three `rc=2` (argparse) results that looked like reds. They were
  re-run individually: all 0.
- **F1's first draft quoted the wrong residuals.** It said M2 moved the roll-year
  residual "+0.4% to +0.4%", from a log tail read without filenames. Re-read per
  file, the control is +1.6%. The verdict didn't change, but the number would have
  shipped wrong.
- **F3 was first drafted as a wrong readout** ("the figure is not actually $0").
  Reading the tooltip code showed the `$0` is a true computed endpoint, so the
  finding is about the check, not the page.
- **M1 is a model.** It is a uniform scaling, not a real 2025 roll. That is enough
  for the FIR guard, which fits one number, but a real prior-year roll also
  shifts hoods unevenly.
- **M1's downstream cells are "not reached".** My harness ran `main.py` after the
  hold, which CI would not. The smoke red it produced (F3) is real but would not
  happen in CI for M1.
- **M3's 10% size sits exactly at the delta threshold.** A 15% error would file
  warnings, and a 3% one would be quieter still. The verdict (no blocking check)
  does not depend on the size.

## 5. Not covered

- Lenses other than Money.
- Correctness against the City: that is C1–C10.
- C7 (weighting by units) and C9/C10. The brief scoped C2–C6 and C8.
- The browser suite beyond `verify-smoke.js`.
- `deploy.yml`'s path, and the monthly digest's checks other than
  `check_mill_rates` and `check_budget_context`.
- A second model's read. Optional per the brief, not done.

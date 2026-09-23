# Findings — the evidence recheck guard (S191, 2026-09-23)

**Target:** `scripts/recheck_evidence_notebooks.py` + `.github/workflows/evidence-recheck.yml`
(#510 S182, CI path S183), S173–S186 backlog item #4 in `docs/AUDIT_LEDGER.md`.
**Questions (from the ledger):** can each invariant flip, and does ❓ fire on a dead
source instead of folding into ✅? First scheduled run: **2026-10-15**.
**Model:** Opus 5.5, `high` effort. ⚠️ Same family as the author (Opus 5), so this
is weaker independence than a Fable run.

**Method:** static read of every `check()` call site (88 sites, 101 invariants
counting loops), then **dynamic simulation**. Each evidence notebook was copied to
a scratch dir with a source patch, either "the publisher fixed it" or "a
source returns 200 with no rows", and run through the script's own `run_one()`.
The harness was `scratchpad/mutate.py` (not committed; the patches are listed in
§3 so they can be rebuilt). Baseline first: a **cold-cache** live run with the
three download caches moved aside. All 7 notebooks passed in 1 min 55 s.

## 1. Verdict

**CONDITIONAL.** The script's three-way classifier is sound for what it was
tested on: a network error becomes ❓, and exit 0 without invariants is not a
pass. **But the premise it reports under, that an evidence notebook "fails when
the publisher fixes the defect", holds for 2 of the 5.** Of the other three:

- one stays **✅** under a fix;
- one reports the fix as **❓ "could not run"**;
- one flips only through a NaN comparison and a claim that retargets itself to
  another year.

A dead catalogue search folds into ✅ on the school report. No shipped number is
affected: this guard gates nothing and reports only.

## 2. Decision stack

| level | question | verdict |
|---|---|---|
| **L0** | Should a scheduled re-run exist at all? | **CONDITIONAL**, see §2a |
| **L1** | Are three outcomes (✅ / ⚠️ / ❓) the right shape? | **SOUND** |
| **L2** | Does ⚠️ mean "the publisher fixed it" for each evidence notebook? | **UNSOUND for `exemption_uncertainty`; CONDITIONAL for `historical_2024_gap`, `roll_year_metadata`; SOUND for `school_coverage_gap`, `permit_neighbourhood_list`** (§3) |
| **L3** | Does a dead source land in ❓, never ✅? | **CONDITIONAL**: transport failure yes, an empty 200 no (§4) |
| **L4** | Are the counts and details in the issue body right? | **WARN**: 17 phantom invariants (§5) |
| **L5** | Does the workflow deliver an issue in every case it claims to? | **WARN**: timeout budget, `tee` (§6) |

### 2a. L0: the recheck contradicts a locked row that was never amended

`DECISIONS.md` **2026-08-29** records Peter **rejecting a monthly re-run** of
these notebooks. He called them snapshots ("each report mostly matters as a
snapshot in time for me"), and the row says it was *"rejected on purpose, not on
cost"*. The **2026-09-21** row then built exactly that. It does not cite 08-29,
and 08-29 carries no AMENDED marker. #510's PR body does not mention it either.

Peter merged #510, and it came out of his own S182 question (*"do we have any
record of these datasets actually being fixed… or is it just 'updated on so and
so'"*). So this is probably a **deliberate reversal, but an unrecorded one**. It
is the `COPY_DECISIONS` S9 shape: a decided row re-proposed under a framing that
did not say it was settled.

- **Sharpest argument against L0:** the snapshot model says a report is dated
  evidence and is not meant to stay true. A monthly ✅ then stamps a date on
  each report that the published page does not show.
- **What would settle it:** one line from Peter, then mark 08-29 AMENDED with a
  pointer to 09-21.

The rest of this audit assumes the recheck stands.

## 3. L2: what each evidence notebook reports when the publisher FIXES it

| notebook | simulated fix | recheck says | why |
|---|---|---|---|
| `school_coverage_gap` | catalogue returns a "Private School Locations" set | ⚠️ **2 flipped** | built for it (`DECISIONS` 2026-08-29, the absence row) |
| `permit_neighbourhood_list` | permit `neighbourhood like '%,%'` returns 0 rows | ⚠️ **2 flipped** | `list_rows > 0` and the three-causes check |
| `roll_year_metadata` | `Period of Coverage` names the next year | ❓ **"exit 1, no invariant verdict — IndexError"** | `hist.loc[hist.assessment_year == claimed_year].iloc[0]` has no row for the corrected year, so it crashes before any check can fail |
| `historical_2024_gap`, 2024 backfilled | 2023∩current re-added to the 2024 slice | ⚠️ **1 flipped (reported as 2)** | **by accident**, see below |
| `historical_2024_gap`, 2024 + 2025 backfilled | same for both slices | ⚠️ 2 flipped, **naming 2018** | the claims retarget themselves |
| `exemption_uncertainty`, fully fixed | top commercial / apartment / residential / farm properties relabelled `NONRES MUNICIPAL/RES EDUCATION` up to 98% of each class gap | ❓ **IndexError** in `subset_reaching` | the negative "invisible" target crashes the subset search |
| `exemption_uncertainty`, **non-residential only** | the commercial half of that fix | ✅ **"22 invariant(s) held"** | **no invariant reads the flag** |

**`exemption_uncertainty` is UNSOUND as a fix detector.** Its headline claim, in
`DATA_ISSUES.md` issue 4, is that the roll flags **3 properties / $7.6M**
as exempt, about 0.05% of what must be. **No `check()` reads `flagged_value`.**
In the simulation the roll flags **$8.78B** as exempt, the page's own printout
contradicts its headline, and the recheck reports all green. This is not a
bug in the notebook. Its `check()` docstring says these are *"structural invariants…
claims that must hold for ANY vintage"*. It was written on 2026-08-26, **three
days before the "fail when fixed" house style existed** (`EVIDENCE_NOTEBOOKS.md`
"Adding a report"). The recheck and `RUNBOOK.md` §0e apply the later style to all
five without checking.

**`historical_2024_gap` flips for the wrong reasons.**

- `ODD_YEAR = growth.idxmin()` and `worst = defects["union"].idxmax()` pick the
  year to test from the data. So **`growth[ODD_YEAR] < others.min()` is a
  tautology**: the minimum is below every other value unless two years tie, and
  it can never fail.
- With 2024 fixed, "worst" moves to 2025. That year has no detector A, so
  `wa = NaN`. `wb > wa` is then False, and that is the only flip.
- With both years fixed, the notebook reports *"**2018** is an outlier by an order
  of magnitude"* failing. The reader gets a report about 2018, on a page about
  2024.

The fix is detected, but the issue body describes the wrong event.

**`roll_year_metadata` reports the fix as ❓.** `RUNBOOK.md` §0e reads ❓ as "it
could not fetch, it timed out, or it exited 0 without recording". That points the
reader at a dead URL when the real cause is the fix the report asked for.
`check(len(coverage_years) > 0, …)` can never be observed failing, because
`claimed_year = coverage_years[-1]` runs first and raises.

## 4. L3: does a dead source fold into ✅?

**Transport failure → ❓, as designed.** urllib and requests raise on 4xx/5xx and
on timeouts. The notebook then exits non-zero without `AssertionError`.
`test_recheck_evidence_notebooks.py` pins this.

**An empty 200 is different.** A source that answers with no rows:

| simulation | recheck says |
|---|---|
| `school_coverage_gap`: the five falsifying catalogue searches return `[]` (the broad `school` search still answers) | ✅ **"4 invariant(s) held"**: both absence checks pass because nothing was searched |
| `school_coverage_gap`: every catalogue search returns `[]` | ❓, but only because `broad_df["operator"]` raises `KeyError` on an empty frame, **not by design** |
| `permit_neighbourhood_list`: `q7d6-ambg` answers 0 rows | ✅: claim 5 ("no other dataset holds a list") passes vacuously |

The school case is the one that matters. That report argues an absence, so a
search that returns nothing is indistinguishable from the absence it asserts.
The notebook prints each search's raw result count and never asserts it. The fix
is a liveness floor: each falsifying search must return **≥1 result of any
kind**. The loose match returns playgrounds for "private school", so a nonzero
count costs nothing today.

## 5. L4: the invariant count is inflated by 17

`historical_2024_gap` and `exemption_uncertainty` print `[PASS]`/`[FAIL]` twice.
The first print is inside `check()`. The second is in the final summary loop, which in the
other five goes through `display()`. `run_one()` counts the lines, so:

| notebook | real | reported |
|---|---|---|
| `historical_2024_gap` | 6 | **12** |
| `exemption_uncertainty` | 11 | **22** |
| **total** | **101** | **118** (113 before S187) |

Each notebook's own output reads `invariants checked: 6/6` and `11/11`. So does
`EVIDENCE_NOTEBOOKS.md`'s status table, one screen above the baseline table
that says 12 and 22. On a flip the ⚠️ detail reads "2 of 12 flipped" for one
failure, and lists the same `[FAIL]` line twice.

**Fix:** count unique claim lines, or have those two summaries stop printing
the `[PASS]`/`[FAIL]` token. The first is a one-line change in `run_one`.

## 6. L5: operational

1. **Timeout budget.** `PER_NOTEBOOK_TIMEOUT = 1500` s across 7 notebooks is 175
   min, but the job has `timeout-minutes: 60`. The workflow's own comment says
   the script *"reports a timeout as 'could not check' rather than letting the
   job die with no issue filed"*. That holds for at most two hung notebooks;
   a third means the job is killed and **no issue is filed**.
   - The cold run takes about 2 min in total, so ~420 s per notebook fits 7 inside 60 min with
     over 10× headroom.
   - The alternative is a job timeout of ≥180 min.
2. **`python … | tee recheck.md` has no `pipefail`.** GitHub's default `bash -e`
   does not set it. If the script itself crashes, the step still goes green, no
   `title` output is written, and `gh issue create --title ""` fails the job.
   The failure still reaches Peter as a failed-scheduled-run email, not as an
   issue, so it is visible but on a different channel. `shell: bash` (which adds
   `-o pipefail`) makes it fail at the right step.
3. **A hand run on this box is not a live check.** `RUNBOOK.md` §0e gives
   `recheck_evidence_notebooks.py` as the manual command. The three notebooks with
   download caches read them when present:
   - `exemption_uncertainty` read the roll, zoning and FIR workbook from cache
     (`cached assessment_roll.csv`), with **no freshness check**;
   - `roll_year_metadata` read its FIR workbooks from cache.

   CI always starts cold, so the scheduled run is live. **Fix:** `run_one` sets
   `EXEMPTION_NB_DATA` / `HISTORICAL_GAP_DATA` / `ROLL_YEAR_DATA`, which the
   notebooks already honour, to a fresh temp dir.
4. **❓ does not say which kind it is.** A `URLError`/`HTTPError`/timeout (source dead)
   and an `IndexError`/`KeyError` (the data changed shape, which is the probable fix
   in §3) both render as "exit 1, no invariant verdict". The fix is to name the
   exception class in the detail and split the RUNBOOK triage by it. It is cheap
   because the stderr tail already carries it.

## 7. The justification notebooks: delta on S187 only

S187 (`FINDINGS_roads_rate_notebooks.md` §5) already recorded the
constants-arithmetic class. It found 16 of 40 lifecycle invariants blind to the
source, and S187 added checks pinning the tables to the PDFs. Two items are new here, both low:

- **`PAVED_25` / `UNPAVED_25` are still unpinned.** `8,204,164,788` and
  `182,805,696` are on Appendix B p37. I checked this against a fresh fetch. But
  only the Roads and Curbs strings are asserted, so
  `abs(PAVED_25 + UNPAVED_25 + CURBS_25 - ROADS_25) < 0.001` is arithmetic on
  four literals, and the `blend` check behind the 11.2% headline uses the
  unpinned Paved value.
- **`roads_operating_rate` §3 prose is false about its own invariant.** It says
  *"The invariant above it is the one that does real work: it measures the
  City's own centreline feed"*. The check reads `CENTRELINE`, a hardcoded dict,
  and can never flip. S187 listed the table as a constant but not the prose.
  The notebook is unpublished, so no reader has seen it.

## 8. Proposed fixes, all code or CI, so Peter's to merge

| # | fix | where |
|---|---|---|
| F1 | Count unique `[PASS]`/`[FAIL]` claim lines | `run_one` |
| F2 | Name the exception class in ❓ details, and split `RUNBOOK` §0e: a network class means a dead source, a shape class means the data changed, possibly the fix | `run_one`, RUNBOOK |
| F3 | Run notebooks with the three cache env vars pointed at a temp dir | `run_one` |
| F4 | `PER_NOTEBOOK_TIMEOUT` ≈ 420, or job timeout ≥ 180; add `shell: bash` to the recheck step | script, workflow |
| F5 | **`exemption_uncertainty`: add a fail-when-fixed invariant on `flagged_value`** (for example `flagged_value < 0.01 * gaps["gap"].sum()`) | notebook, re-render the page |
| F6 | `school_coverage_gap`: assert each falsifying search returned ≥1 raw result | notebook |
| F7 | `historical_2024_gap`: pin `ODD_YEAR`/`worst` to the documented year (2024) instead of `idxmin`/`idxmax`, so a fix fails the claim it was written about | notebook |
| F8 | `roll_year_metadata`: guard `hist_claimed` so that a coverage year with no historical slice fails an invariant rather than crashing | notebook |
| F9 | Pin `PAVED_25`/`UNPAVED_25`; reword the §3 "does real work" sentence | roads notebooks |
| F10 | Mark `DECISIONS` 2026-08-29 AMENDED → 2026-09-21, **if Peter confirms** §2a | DECISIONS |

F5 to F8 change published evidence pages. Each needs a re-execute and re-render,
and `FIRST_MEASURED` stays unchanged, per `EVIDENCE_NOTEBOOKS.md`. **F1 to F4
should land before 2026-10-15**, so the first scheduled issue reports true
counts and names the ❓ kind.

## 9. What this run got wrong

- **The exemption simulation is not a realistic fix.** It relabels the
  highest-value properties in each class, not the ones that are actually exempt. The
  printed "flag accounts for 142% of it" is an artefact of that: the flagged
  value is divided by a gap the relabelling itself shrank. Quote only the
  conclusion, that no invariant reads the flag. That part rests on the source (no
  `check()` touches `flagged_value`), and the simulation only demonstrates it.
- **The historical fix simulation disabled one invariant on purpose.** I replaced the
  per-year server-count comparison with `True`, because my patched sets could
  not match the live server. In a real backfill that check would pass on its
  own. I also added approximate per-year increments (2,322 / 2,448). The
  retargeting finding does not depend on either.
- **I first read `check(len(coverage_years) > 0)` as a liveness guard.** It isn't:
  the line above it raises first. I caught this only while reading why the
  roll-year fix crashed.
- **I nearly reported the `CENTRELINE` constant as new.** S187 already had it;
  only the prose is new. It came up while re-reading S187 §5 *after* drafting
  the claim, which is the step the skill says to do first.
- **The dead-source coverage is sampled, not exhaustive.** Three empty-200 cases
  across two notebooks. The other three evidence notebooks were read for the
  shape, not run. `historical_2024_gap`'s `fetch_frame` cross-checks every
  download against the server's count, and an emptied slice would change
  `growth`. I did not simulate it.

## 10. F5–F8 applied (S192, 2026-09-23)

Each change was re-run through `run_one()` under the §3/§4 patches, with a
live control, and then reverted on its own to confirm it is the thing that
changes the verdict.

| scenario | before (§3/§4) | after | with only this fix reverted |
|---|---|---|---|
| exemption, control | ✅ 11 | ✅ 12 | — |
| exemption, non-residential fix | ✅ | ⚠️ 1 of 12, the flag claim | ✅ 12 (F5 check off) |
| exemption, full fix | ❓ IndexError | ⚠️ 2 of 12 | ❓ IndexError (`dtype=int` off) |
| school, control | ✅ 4 | ✅ 5 | — |
| school, falsifying searches empty | ✅ 4 | ⚠️ 1 of 5, the liveness floor | ✅ 5 (floor off) |
| school, private set published | ⚠️ 2 | ⚠️ 2 of 5 | — |
| roll year, control | ✅ 8 | ✅ 9 | — |
| roll year, coverage fixed | ❓ IndexError | ⚠️ 1 of 2, the slice claim | per §3 |
| historical, control | ✅ 6 | ✅ 6 | — |
| historical, 2024 fixed | ⚠️ 1, via NaN | ⚠️ 3 of 6, all naming 2024 | per §3 |
| historical, 2024 + 2025 fixed | ⚠️ naming **2018** | ⚠️ 3 of 5, naming 2024 | ❓ ValueError in a chart (stop off) |

Where these depart from §8:

- ⚠️ **F6 as proposed would have failed on a healthy catalogue.** §4 said "a
  nonzero count costs nothing today". It was measured for "private school"
  only. `charter school` and `Centre-Nord` return **0 results** on a live
  catalogue (the five return 15/0/6/1/0). The floor is therefore on the
  **sum** of the five. The control run caught this: the first version failed
  1 of 5 unpatched. The sum floor cannot see one search going dead while the
  others answer. That limit comes from what the catalogue returns, not from
  the floor.
- **F5 needed a second change.** With the flag fully populated, the invisible
  apartment gap goes negative, `subset_reaching` returns an empty float
  array, and indexing with it raises `IndexError` *after* the new check has
  failed. The recheck would then call it ❓. The fix returns the indices as
  `int`.
- **F7 needed a second change as well.** With both years repaired, the missing
  set is empty and a chart crashes on a NaN axis limit. The notebook now raises
  `AssertionError` right after the "non-empty" check. F8 uses the same
  pattern: a fix stops the run as a failed invariant instead of crashing
  later.
- A stopped run reports only the checks that ran before the stop ("1 of 2",
  "3 of 5"). The denominator is not the notebook's full count.

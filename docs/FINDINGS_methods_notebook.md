# Findings — the Methods notebook (`notebooks/verified/02_methods.py`, #578)

**Run:** 2026-09-25 (S197), Opus 5.5, `edmonton-audit`. Audit-ledger queue item 11.
**Target:** the public Methods & definitions page, which since #578 is also a
**publish gate** in `refresh.yml` (a failing invariant stops the weekly commit).
Two questions: does every figure the page prints match what it computes, and
can each of its 6 invariants fail on a real defect **and not** on a healthy run?
**Deadline:** its first scheduled execution is the 2026-09-28 refresh.

## 0. Verdict

| # | Finding | Severity | Status |
|---|---|---|---|
| F1 | The notebook runs **before** the status manifest is rewritten, so the year invariant **fails on a healthy January run** (reproduced) and the page's vintage and last-checked dates are **always one run stale** | MEDIUM | CI fix proposed, needs Peter |
| F2 | The "every located dollar is in the lot-acre view or reported as excluded" invariant is an **identity**: it passes with 43% and with 100% of located dollars missing | LOW | code fix proposed |
| F3 | The public page describes **full-only** layers with live numbers and omits **two public lenses** | WARN | Peter's call |
| F4 | The stormwater figure lost the qualifier the old doc paired it with | LOW | Peter's call |

**The printed figures are right.** Every computed number reproduces, and the
ones that can be tied to an independent total tie (§1). Nothing the page
publishes today is wrong. The defects are in **when** it runs and **what** its
guards can see.

## 1. Every printed figure, checked

| Figure (render of 2026-09-24) | Check | Result |
|---|---|---|
| Citywide levy **$2.78B** on 439,569 accounts | served `revenue_per_acre × ground acres` summed = **$2.782B** | ties |
| 439,569 accounts | raw roll 439,622 rows; `load_assessment` drops 53 null/zero-value rows (logged at INFO, hidden by the page's WARNING log level) | correct; the 53 carry $0 |
| Rates 7.7419 / 8.2064 / 25.2216, **3.3×** | 25.2216 / 7.7419 = 3.258 | correct |
| 406 hoods, 193,237 ground acres | recomputed | correct |
| **7** hoods below the 15% lot floor | served: 7 null `value_per_lot_acre`, 7 below floor, **0** null for any other reason; same for `revenue_per_lot_acre` | correct |
| Largest account $1.29B, Summerlea, 79%; cell rank 1 of 34,664; lot-acre rank 177; **51×** | 15,443,990 / 302,525 = 51.05 | correct |
| 287,032 points, 2,997 multi-unit, 58 excluded, $1.23B (0.52%), 142,033 acres (74%) | re-run in-process | reproduces |
| Known bound exceptions: Pembina | `KNOWN_BOUND_OUTLIERS = ('PEMBINA',)` | correct |
| 48 of 406 grey, threshold 90% | served | correct |
| 100 m cells, 34,664 hold an account | 34,664 cells, 0 with revenue ≤ 0 | correct |
| Road 3,655 km, fire 88,047/yr, storm $256.9M, water $588.3M | each column's per-acre denominator is ground acres (`join_and_calculate.py` `safe_area`), so per-acre × ground acres is the pipeline total | self-consistent; not tied to raw (see §6) |
| Prose: training/operational fire events excluded; arterials and alleys out | `load_fire.NOISE_GROUPS`; `load_roads.METRIC_GROUPS = ("collector", "local")` | correct |

## 2. F1 — the notebook reads last week's `status.json` (MEDIUM)

**Mechanism.** In `refresh.yml` the order is `Run verified notebooks` (line
~198), then `Update status manifest` (line ~222, `generate_status.py`), then the
commit. `02_methods.py` reads `web/data/status.json`, so it sees the manifest
**committed by the previous run**, not the one this run is about to publish.
It is the only verified notebook that reads it (`01_money_lens.py` does not).
`run_verified_notebooks.py` is called from nowhere else.

**Consequence (a), stale figures on every run.** The header's "served data
generated" and §7's "data last checked" and vintage line always show the
previous run's values. On 2026-09-28 the page will say *last checked
2026-09-21* while the site's own manifest says 2026-09-28. That is the defect
the notebook was built to end ("still quoting the 2025 mill rates"), one level
down.

**Consequence (b), the year invariant fails on healthy data once a year.**
Invariant 1 compares `main.ASSESSMENT_YEAR` with `status.json`'s `rate_year`.
The January checklist (`RUNBOOK.md` §1) bumps `ASSESSMENT_YEAR`, `DATA_YEAR`
and `RATE_YEAR` in step 3/6, commits and **triggers the refresh in step 9**,
and regenerates `status.json` only in **step 10**, after the refresh. So the
refresh in step 9 runs with the new constant and the old manifest. The
pipeline then builds this run's data with the new year, and the invariant reds
anyway.

- **Reproduced:** `status.json` `rate_year`/`data_year` set to 2025 against
  `ASSESSMENT_YEAR = 2026`, then `run_verified_notebooks.py --only 02_methods` fails
  with *"main.ASSESSMENT_YEAR=2026, status.json rate_year=2025"*, and the publish is
  held. (Restored with `git checkout` afterwards.)
- **It does not unstick itself.** A failed run stops before `generate_status.py`,
  so the manifest never advances, and every following weekly run fails the same
  way until someone runs step 10 by hand.
- **It catches nothing the test suite misses.** In the steady state, the page
  and the pipeline both read `main.ASSESSMENT_YEAR` in the same run, and
  `tests/test_generate_status.py::test_zoning_year_is_the_bylaw_year_and_does_not_track_the_roll`
  already pins `(DATA_YEAR, RATE_YEAR) == ASSESSMENT_YEAR`. So a year mismatch
  that is a real defect is already caught. The only state this invariant can
  detect is the ordering artefact above.

**Fix (proposed; changes CI, needs Peter's OK):** move the `Run verified notebooks`
step to just after `Update status manifest (provenance + heartbeat)` and before
the commit step, with the same `if:`. A failure there still stops the run
before the commit, so `status.json` still goes unbumped in the repo and the
staleness banner still fires. The heartbeat behaviour doesn't change. Once the
step is moved, invariant 1 compares two values the test already pins equal, so
**delete it** rather than keep a check that cannot fail.
**Fallback without a CI change:** delete invariant 1 and the two date prints,
and read the vintages from `generate_status`'s constants.

## 3. F2 — the located-dollars invariant is an identity (LOW)

```python
inelig_value = rows.loc[~rows["eligible"].fillna(False), "assessed_value"].sum()
elig_value   = rows.loc[rows["eligible"].fillna(False),  "assessed_value"].sum()
check(abs(inelig_value + elig_value - roll_value) < 1.0, ...)
```

`x` and `~x` partition every row, so the sum is the roll by construction.
`fillna(False)` makes it worse. A point that `_point_lot_stats` never classified,
which is a **silent drop**, is counted as "excluded" even though nothing reported
it. That is the case the printed claim names.

The mutants were run in-process with a dtype-safe mask:

| Mutant | Check | "excluded" | points actually reported |
|---|---|---|---|
| control | PASS | $1.23B | 58 |
| 20,000 largest points dropped from `per_point` | **PASS** | $102.75B | 55 |
| every point ineligible | **PASS** | $238.36B (100%) | 287,032 |

- **Today a drop would still stop the publish, but by accident.** Under
  pandas 3.0.3 (pinned in both requirements files), a partial merge leaves
  `eligible` as an object column. `~` then yields integers −1/−2, and `.loc`
  raises `KeyError`. That crash is what fails closed, not the check.
- **No coverage gap.** `check_value_anchors.py` bounds `ineligible_points` and
  `ineligible_value_frac` against `data/expected_value_anchors.json` at
  `refresh.yml` line ~138, before the notebooks run. So the class is guarded.
  The defect is a printed claim stronger than what it tests.

**Fix:** replace the identity with what the claim says, the check that every
located account's point was classified:
`check(rows["eligible"].notna().all(), "every located account's point was classified as eligible or excluded", f"{rows['eligible'].isna().sum()} unclassified")`.
It reds on the drop mutant and passes today. Then compute the two sums with
`.astype(bool)`, so the crash no longer depends on pandas behaviour.

## 4. The other four invariants

- **Every served hood has a boundary area:** can fail on a name mismatch
  between the served file and the boundaries. It is weak but real, and passes
  (0 without).
- **Lot-acre figure never served below the floor** and **grey flag = threshold
  rule:** each replays one pipeline line (`join_and_calculate.py` ~902 and
  `load_zoning.py` ~348). They are regression tests on that line, not
  independent measurements, and can fail only if the rule is edited. That is
  fine, but it isn't "differently-shaped recomputation".
  - ⚠️ I nearly reported the grey-flag check as blind to an **all-null**
    set-aside column. `check_served_columns.py`'s `empty_columns()` (S147 R1)
    already fails that earlier in the same run.
  - What neither guard sees is the set-aside layer collapsing to 0 flagged
    with non-null zeros, and no check anywhere bounds the grey count. That is a
    gap, but a pipeline-guard gap, not this page's. It is noted and not queued.
- **Road metric covers a positive length:** a smoke check. It is fine as one.

## 5. F3 / F4 — what the public page says (WARN, Peter's call)

**F3.** The About panel links this page on the **public** build, and the link
says "how every metric is built". But:

- **§5 describes full-only layers as present:** Fire, Stormwater, Water +
  sanitary, and a Ratio "picker" for fire events. The public `SERVICES`
  carries only `roads`, `roadscost` and `roadslife` (`pub: true`), and
  `ratioDenomShow` is `&& FULL_BUILD`. It also prints live citywide figures
  for them ($256.9M, $588.3M, 88,047 events).
  - The 2026-07-28 `DECISIONS.md` row gated the **in-app** Data & Methods copy
    for exactly this reason. Its words: *"warning about or crediting things a
    public visitor cannot reach"*.
- **Two public lenses are absent:** Development (permits) and Change over time
  (temporal). Their datasets are missing from the §7 source table too.
  - The Change lens carries a deliberate, two-year, non-contiguous gap
    (`SPEC_temporal.md` §0), which is exactly the kind of thing a methods
    reader looks for.
- **This is inherited, not introduced.** The retired `docs/METHODS.md` had the
  same scope. But #578 moved it from a GitHub doc onto the site's own domain,
  with weekly-refreshed numbers.

**Options:** (a) add Development and Change sections and gate or label the
full-only layers, (b) label §5's full-only layers "not in the public map
yet", or (c) leave it as is on purpose. Per the 2026-09-11 row, which layers
the public build shows is a weight judgement that belongs to Peter.

**F4.** The old doc paired modelled stormwater ($240.4M) with the figure
excluding land EPCOR does not bill ($190.5M), and with the ~11% residential
validation. The page now prints **$256.9M** bare. The pairing is recomputable,
so the "cite without a number" rule doesn't cover dropping it.

## 6. What this run got wrong

1. **The first mutation harness crashed, and I nearly read the crash as the
   check working.** The 20,000-point drop raised `KeyError`, which looks like
   "the notebook fails on a drop". It was pandas' object-dtype `~`, not the
   invariant. The re-run with `.astype(bool)` showed PASS. The crash still
   fails closed today, which is why F2 is LOW, but that is luck, not design.
2. **The all-null claim about the grey-flag invariant** (§4) was a confident
   negative ("nothing catches an all-null set-aside column"). It was wrong:
   S147's `empty_columns()` catches it. I found the reader before writing the
   finding, not after.
3. **F1(b) depends on how the checklist is followed.** A maintainer who
   regenerates `status.json` before triggering the refresh, or who runs step
   10 first, never meets it. The claim is that **the checklist as written**
   walks into it, not that it will certainly happen. F1(a) holds on every run
   regardless.
4. **F1 is read from the step order, not observed in CI.** `02_methods.py` has
   never run in a scheduled refresh. The 2026-09-28 run is the first
   observation: its page should show *last checked 2026-09-21*. If it shows
   09-28, this finding is wrong.
5. **The four citywide cost figures are only self-consistent.** Per-acre ×
   ground acres reproduces them exactly, which proves the page reads the
   served columns correctly. It does not prove the served columns are right,
   because nothing was tied to raw events, raw centrelines or EPCOR totals
   here. The road total is consistent with S187's 95.2 km = 2.6% boundary
   figure (≈3,660 km).
6. **Same-family audit.** The page was written by Opus 5.5 (S195), and this
   audit is also Opus 5.5. The ledger calls that weaker independence than a
   Fable read.

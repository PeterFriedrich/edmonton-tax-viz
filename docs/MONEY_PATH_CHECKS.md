# Money path: what the automatic checks catch, and what only a person catches

**Last measured 2026-11-26 at `6c77dd2`** (S264). This page is a snapshot. To
update it, re-run `docs/FABLE_AUDIT_money_path_checks.md`; don't edit it by hand.
The evidence behind every line is the matrix in
`docs/FINDINGS_money_path_checks.md` §2. Each entry carries its mutation ID (M1,
M2…).

**How to read it.** Each section is one step of the human verification chain
(C2–C6, C8). Under each step:
- *What could go wrong* is a realistic mistake we made on purpose.
- *Stops the publish* lists the automatic checks that turned red and kept it off
  the site.
- *Only warns* lists checks that open a GitHub issue but let the data publish.
- *Nothing catches this* means your hand check is the only line.

**The short version.** If someone breaks the **code**, the tests stop it before it
merges. If the **data** is wrong, because the City's file is missing accounts or a
mill rate was typed wrong, it can publish. Only one of those data cases (last
year's roll) is held automatically. Put hand checks there.

Only the Money lens is covered. Roads, Development, Services, Ratio, Uses,
Glass and Change over time are not, and neither are C1, C7, C9 or C10.

---

## C2 — Is it this year's roll, and is all of it there?

**What could go wrong**
- The pipeline reads last year's roll instead of this year's (M1).
- The City's roll is missing its biggest accounts: the top 1% by value, about a
  quarter of all assessed value (M2).
- The City's roll is missing a scattering of accounts, 1% of them at random
  (M2b). This is the many-small version of #818, where one $67.5M account left
  Virginia Park.

**Stops the publish**
- Last year's roll: the roll-year check holds the weekly refresh, keeps last
  week's data live and puts a banner on the site
  (`scripts/check_roll_year_against_fir.py`). It compares our residential base to
  what Edmonton filed with Alberta.

**Only warns**
- A big loss: the revenue-delta check opens a "Big revenue delta" issue after the
  data has published, here for 205 neighbourhoods
  (`scripts/check_revenue_deltas.py`). The colour-clamp drift check also opens
  one (`scripts/check_colour_clamps.py`).

**Nothing catches this**
- **Missing accounts, at any size, never stop the publish.**
- A small or scattered loss produces no signal at all. In M2b citywide revenue
  fell 1.1% and one neighbourhood (Mill Woods Park) fell 32%, but no hood moved
  both 10% and $1M, so the delta check stayed quiet.
- The download's own count check can't help. It compares our download with the
  City's count, and the City's count agrees with the City's file.
- *Your C2 check is the only line for completeness.*

**How to re-check**
- In a scratch worktree, drop rows from
  `data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv`.
- Run `python main.py --skip-png && python scripts/check_revenue_deltas.py`.
- Every blocking step stays green.

---

## C3 — Are the mill rates right?

**What could go wrong**
- One 2026 rate is wrong by 10%: the Residential rate typed as 8.5161 instead
  of 7.7419 (M3).
- The code picks last year's rates (M4).

**Stops the publish**
- Last year's rates: the rate tests in the merge gate go red (8 tests in
  `tests/test_apply_tax_rates.py`), so the change can't merge.

**Only warns**
- Nothing.

**Nothing catches this**
- **A wrong rate value.** Revenue rose 4.5% citywide, and no neighbourhood rose
  by 10% or more, because a 10% rate error spreads under the delta check's
  threshold.
- The monthly digest checks only that a rate year *exists*, not that its numbers
  match the City's (`scripts/vintage_report.py`, `check_mill_rates`).
- The merge gate catches a rate edit only if `status.json` was left stale. A PR
  that regenerates it passes.
- First found 2026-09-15 (`FINDINGS_published_numbers.md` T1b) and still open.
- *Your C3 check against `pwis-wc4c` is the only line.*

**How to re-check**
- Edit one 2026 `municipal` value in `data/mill_rates.json`.
- Run `python scripts/generate_status.py && python -m pytest tests/ -q`.
- It stays green.

---

## C4 — Is each property billed in the right class, with the right split?

**What could go wrong**
- Commercial property billed at the residential rate (M5).
- Mixed-class properties billed as 100% of their first class (M6).
- Exempt properties billed tax (M7).

**Stops the publish**
- All three: the rate tests in the merge gate (`tests/test_apply_tax_rates.py`;
  2, 4 and 2 tests respectively).
- That one test file is the **only** thing that stops any of them. Don't delete
  its tests as duplicates.

**Only warns**
- The commercial mix-up also opens revenue-delta and colour-clamp issues.
- The other two are too small to warn: the exempt mistake added $192k in 3
  neighbourhoods.

**Nothing catches this**
- Nothing, for these three as built. A *new* class label the code doesn't know
  stops the run (`src/apply_tax_rates.py` raises).
- A label mapped to the wrong class on purpose is caught only if a test names
  that label.

**How to re-check**
- Change one entry in `ASSESSMENT_CLASS_TO_RATE_CLASS`.
- Run `python -m pytest tests/test_apply_tax_rates.py -q`.

---

## C5 — Does every property land in the right neighbourhood, once?

**What could go wrong**
- Neighbourhoods whose names have accents or punctuation are silently dropped:
  wîhkwêntôwin, Hollick-Kenyon and River's Edge, $5.6B of value (M8).
- Name fixes applied in the wrong order, so one neighbourhood appears twice (M9).

**Stops the publish**
- Dropped neighbourhoods: the weekly Money notebook's "aggregation can't lose
  value" and "aggregation can't lose levy" checks
  (`notebooks/verified/01_money_lens.py`). They are the **only** thing that stops
  it.
- Duplicated neighbourhoods: three things.
  - The name-correction tests (`tests/test_load_assessment.py`).
  - The unmatched-names check, which reports "NAME DRIFT"
    (`scripts/check_unmatched_names.py`).
  - The join itself, which refuses a duplicate (`src/join_and_calculate.py`,
    `validate="m:1"`).

**Only warns**
- The revenue-delta issue lists the 3 dropped neighbourhoods as "disappeared".

**Nothing catches this**
- Nothing, for these two.

**How to re-check**
- Add a filter on `neighbourhood_name` in `src/aggregate_by_neighbourhood.py`.
- Run `python tools/run_verified_notebooks.py --only 01 --out-dir /tmp/v`.

---

## C6 — Is the area right?

**What could go wrong**
- Ground acres used where lot acres are meant (M10).
- Area measured before the map is converted to metres (M11).
- The square-metres-per-acre constant slightly off, so every figure is 1.2% wrong
  (M12).
- The "set aside" grey flag reversed (M13).

**Stops the publish**
- Lot acres: the lot-acre tests (`tests/test_join_and_calculate.py`), the only
  thing that stops it.
- Area before conversion: the area test (`tests/test_load_boundaries.py`), and the
  lot-acre bounds check inside the pipeline
  (`src/export_value_grid.py`, `check_lot_acre_bounds`).
- The constant: one test that pins the exact value
  (`test_sq_m_per_acre_is_the_international_acre`), the only thing that stops it.
- The grey flag: the zoning tests (`tests/test_load_zoning.py`), the Methods
  notebook (`notebooks/verified/02_methods.py`) and the render smoke check
  (`tools/profiling/verify-smoke.js`).

**Only warns**
- The grey flag also opens a colour-clamp issue.

**Nothing catches this**
- Nothing, for these four.

**How to re-check**
- Make the edit named in the findings matrix.
- Run `python -m pytest tests/test_join_and_calculate.py tests/test_load_boundaries.py tests/test_load_zoning.py -q`.

---

## C8 — Is the published file what the pipeline computed?

**What could go wrong**
- The export rounds every money figure to 3 significant figures, so figures are
  off by up to 0.5% (M14).

**Stops the publish**
- The export-precision test (`tests/test_join_and_calculate.py`,
  `test_export_rounds_served_precision`).
- The Roads notebook, which compares the published file with a rebuild
  (`notebooks/verified/04_roads_lens.py`).
- No Money check reads the published file.

**Only warns**
- Nothing.

**Nothing catches this**
- Nothing, for this one.

**How to re-check**
- Change `WEB_SIGNIFICANT_FIGURES` in `src/join_and_calculate.py`.
- Run `python -m pytest tests/test_join_and_calculate.py -q`.

---

## Two things to know about the checks themselves

- **The Money notebook passing doesn't mean the numbers are right.** It re-runs
  the same code on the same data and checks that nothing leaks between steps. A
  wrong rate or a wrong acre passes it.
- **One neighbourhood can stop the weekly publish on a correct page.** Nearly
  all of University of Alberta Farm's levy sits on land that may be tax-exempt
  (a share of 0.999997). If that share rounds to exactly 1, the low end of its
  "if that land pays nothing" range is a true $0. The render smoke check can't
  tell that from a mis-rounded figure, so it stops the publish. This happened
  under two of these mutations, not yet on real data
  (`FINDINGS_money_path_checks.md` F3).

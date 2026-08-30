# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **CLOSED 2026-08-29 — the three verify failures are resolved, and one of
  them was NEVER a master failure.** Replaces the two items previously here
  (`verify-temporal.js` "fails on unmodified master", and the two "stale
  expectation" scripts). Reproduced before acting, per the standing rule.
  - **`verify-temporal.js` — NOT a defect, and the item's headline was wrong.**
    6/6 PASS on clean `master` on an idle box. Re-run under deliberate
    contention (12 concurrent chromiums) it FAILS **on the exact selectors the
    old item named**, both `Timeout 4000ms exceeded`. ⚠️ **This is the
    already-documented `run-verify-scripts-alone` condition, not a third
    broken script** — the 2026-08-16 "4 failures in 4 sequential runs" was
    measured on a box that was not actually idle. **The 4000ms budget was NOT
    raised**: nothing is wrong with it under the protocol the project already
    requires. Folded into the `verify-peek.js` flakiness item below, which is
    the same root cause.
  - **`verify-revenue-panel.js` — FIXED, and the old diagnosis was stale.** It
    listed 3 failures with one cause; there were **6 with two**, and the new
    three were the interesting ones. ⚠️ **`rev_frac_*` is NOT one partition —
    it is two overlapping dimensions.** `rev_frac_exempt` is a CROSS-CUTTING
    flag (an exempt institutional parcel counts in `rev_frac_inst` AND in
    `rev_frac_exempt`), so the test's ground truth of "every `rev_frac_*` > 0"
    summed to 1.054081 for DOWNTOWN — the excess being exactly its 0.054082
    exempt share. The app was right throughout: `REV_CATEGORIES` excludes
    exempt by construction and the panel note discloses it separately. Ground
    truth now excludes it, **and a new check asserts exempt IS cross-cutting**
    so the exclusion did not silently drop coverage. The other three were the
    known element-vs-visible count, fixed with the house `getClientRects()`
    idiom.
  - **`verify-nonres-revenue.js` — FIXED by DERIVING the tolerance, not
    widening it.** The old `1 + 1e-9` predated the 6-significant-figure export
    decision (`DECISIONS.md` 2026-08-09) and failed on 127 of 406 hoods. ⚠️
    **The invariant was checked against what the rounding can produce before
    any epsilon was touched**, which is what the old item demanded: measured
    across all 406 hoods, **every breach sits inside the half-ULP bound of the
    three rounded values and NONE exceeds it** (worst: WÎHKWÊNTÔWIN, excess
    0.4 against a bound of 0.6). So the decomposition is exact upstream. The
    test now computes that per-hood bound instead of carrying a magic number.
    **Falsified against injected breaches**: 0.5× the bound passes, 2× and 10×
    both fail — it discriminates at the rounding boundary rather than being
    loosened into uselessness.


- [x] **✅ DONE 2026-08-28 — the archive can no longer freeze the wrong year.**
  Built on Peter's *"do f1 and f3"*. `write_archive(..., confirmed=)` refuses to
  overwrite a confirmed entry with an unconfirmed capture; the caller MEASURES
  the capture (reusing `detect_year`, never a second comparison) instead of
  trusting the pin; `_year_confirmed` backfilled from the standalone guard's own
  verdict. ⚠️ **Deliberately NOT the proposed "skip on inconclusive"** — that
  would leave the archive empty through the months-long FIR lag and cost a year
  outright if Alberta ran late, reintroducing the original loss. The data is
  irreplaceable; only the label was ever wrong. Regression test falsified against
  the old logic (fails on the OVERWRITE, not the signature).
  Original item — audit F1, 2026-08-28;
  `docs/FINDINGS_proxy_guards.md` T1. **The 2026-08-27 fix deleted the bad
  entry; it did not close the door.**
  - **Reproduced, not inferred:** `write_archive`'s freeze protects *other*
    years — the **pinned** year's entry is reassigned every run (by design, so
    the live capture improves). Under a **stale pin** that writes the NEW roll
    over a CORRECT archived year, weekly and silently.
  - ⚠️ **The FIR guard cannot catch it**: `detect_year`'s candidate set is
    years **Alberta has filed**, and Alberta files months after Edmonton rolls.
    Simulated on Edmonton's own history — a next-year roll at **+2%/+4%**
    returns a confident **ALIGNED on the wrong year**; at **+6%/+8.3%/+12%**
    it returns inconclusive, which `refresh.yml` treats as **proceed**.
    **No revaluation rate protects the archive.**
  - **The missed distinction is REVERSIBILITY.** "Inconclusive → proceed" is
    right for regenerating `web/data` (recomputable) and wrong for the freeze
    (permanent). They share one gate.
  - **Proposed:** make `--write-archive` require a *positively confirmed* year
    and SKIP on inconclusive, leaving regeneration untouched. A skipped capture
    is recoverable next week; a wrong one never is. **Changes
    `check_temporal_years.py`'s contract — propose-first, hence not built.**


- [x] **✅ DONE 2026-08-28 — the merge gate exists.** `.github/workflows/tests.yml`
  runs `pytest` + `check_doc_citations.py` on `pull_request` and `push: master`;
  offline and secret-free, so it cannot flake on an upstream outage. ⚠️
  **`refresh.yml`'s own pytest step STAYS** — that one gates the weekly data
  publish, this one gates the change; a test pins both, because the tempting
  cleanup is to drop the "duplicate". ⚠️ **Branch protection is still OFF** —
  the gate reports, but nothing blocks a merge on it. That is a repo-settings
  change only Peter can make. Original item — audit F3, 2026-08-28. `pytest` appears in **exactly one place**:
  `refresh.yml`, a weekly cron. No `pull_request` workflow exists and `master`
  is **not protected** (API returns `Branch not protected`).
  - **`deploy.yml` publishes to the live site on every push with zero test
    execution**, and "746 passed" in a PR body attests to the author's laptop,
    not the merged state.
  - A failure introduced on a Tuesday surfaces the following **Monday as a held
    data refresh** — the symptom is a stale map, not a red check on the cause.
  - **Real mitigation, stated honestly:** the placement *inside* `refresh.yml`
    is correct (before download/regeneration), so a broken suite holds the data
    path rather than corrupting it. The gap is release-gate vs merge-gate.
  - **Proposed:** a `pull_request` + `push: master` workflow running
    `pytest tests/ -q` + `check_doc_citations.py` — both offline, ~11s, no
    secrets, no network. **Changes CI behaviour — propose-first, hence not
    built.**


- [x] **✅ DONE 2026-08-27 — the temporal archive's mislabelled 2025 entry is
  deleted, and 2025 is accepted as unrecoverable.** Found 2026-08-26, fixed
  2026-08-27; full write-up in `docs/DATA_ISSUES.md` §2 and `DECISIONS.md`
  2026-08-27. Deleted rather than relabelled — a correct `2026` entry already
  existed (342/406 hoods byte-identical, totals +0.0021% apart). ⚠️ **Deleting
  did NOT restore 2025**: it is in `HISTORICAL_DEFECT_YEARS`, so the year is
  OMITTED rather than falling back to the historical file, whose 2025 slice
  carries the same 2,448-account hole that got 2024 omitted. **Published series
  is now 2012–2023 + 2026.** Moved with it: the `expected_temporal_years.json`
  2025 anchor (removed, with an in-file re-pin prohibition), `CHG_WINDOW_LABEL`
  → `2012–2026`, the tooltip's hardcoded `(2024 n/a)` (now derived), and 9
  rescaled checks across `verify-temporal.js` / `verify-change.js` — all green.
  `check_temporal_archive_year.py` now exits **0**.
  - ⚠️ **STILL OPEN, split out below:** wiring that guard into a workflow. It
    was unwired only because it failed by design; that reason is now gone.


- [x] **▶▶ FIXED 2026-08-25 — THE MEASURED ROLL-YEAR GUARD EXISTED BUT RAN
  NOWHERE — `check_roll_year_against_fir.py` was not wired into any workflow.**
  Opened and closed 2026-08-25, immediately after the item below shipped it.
  - **The gap.** The item below replaced the blind metadata guard with one that
    measures parcels, and deliberately downgraded `check_year_alignment.py` so
    it can now return only `aligned`-on-current-metadata, `inconclusive`, or
    `hold`. But `refresh.yml` still invoked **only** `check_year_alignment.py`.
    Net effect: with the coverage string stale (which it is), CI had **no
    positive confirmation of the roll year at all** — the new detector ran only
    when a human remembered to type it. A guard that exists and never executes
    is documentation, not a guard.
  - **Fixed by** adding a `rollyear` step to `refresh.yml` immediately after the
    metadata guard (it must follow `Download source data` — it reads the
    downloaded roll), and giving the script the same `$GITHUB_OUTPUT` contract
    the metadata guard already had (`result` / `detected_year` / `pinned_year` /
    `banner`), so the workflow can gate on either identically.
  - **Exit 3 HOLDS** — skip regeneration, keep serving the last committed data,
    raise the banner (Peter's call, 2026-08-25). Reasoning: unlike the metadata
    string, this guard *measures*, so a mismatch is evidence rather than a
    guess, and it is the exact failure that billed a 2026 roll at 2025 rates for
    months. False-positive risk is low by construction — the script returns 4
    (inconclusive), never 3, unless another year fits within 5% **and** beats
    the runner-up by 3%.
  - ⚠️ **Both guards can hold, so all seven publish steps now gate on BOTH**
    (`steps.yearcheck… != 'hold' && steps.rollyear… != 'hold'`), and the banner
    step fires on either, preferring the FIR banner because it measured the
    parcels. `test_refresh_workflow_gates_every_publish_step_on_both_guards`
    parses `refresh.yml` and asserts the coverage holds — the failure it exists
    to catch is a future step copying a neighbour's `if:` and gating on only one.
  - ⚠️ **`PyYAML` had to be added to `requirements-ci.txt`.** That test parses
    the workflow; PyYAML was in `requirements.txt` only, so the test passed
    locally and would have errored at import inside the very `pytest` step that
    gates the refresh. `jupytext` pulls it in transitively, but a guard-shape
    test must not rest on a transitive dep.
  - **Verified:** 727 tests pass (713 + 14 new); the workflow parses and all
    eight gated steps carry both conditions.

- [x] **▶▶▶ FIXED 2026-08-25 — THE LIVE ROLL IS THE 2026 ROLL AND WE BILLED IT
  AT 2025 MILL RATES —
  the year-alignment guard cannot see it, because it reads a Socrata metadata
  STRING instead of the data.** Opened 2026-08-25, found by the FIR comparison
  below (which is how a wrong number got caught: my own first pass compared the
  roll to the wrong FIR year and reported +18.2%; see the correction there).
  - ⚠️ **THE EVIDENCE — residential is the tell.** Residential land is barely
    exempt anywhere, so our residential base should match the province's filed
    residential base closely. Ours is **$162,273,056,185**. Against FIR:

    | FIR year | filed residential base | ours reads |
    |---|---|---|
    | 2023 | $131,284,317,914 | +23.6% |
    | 2024 | $134,439,557,008 | +20.7% |
    | 2025 | $148,128,818,480 | +9.5% |
    | **2026** | **$160,372,669,990** | **+1.2%** |

    Monotonic, and 2026 fits to within noise. **The roll advanced and nothing
    noticed.**
  - **Corroborated three ways, independently:** (a) the dataset is literally
    named *Property Assessment Data (**Current Calendar Year**)* and it is
    August **2026**; (b) `data/mill_rates.json`'s 2026 block matches FIR 2026
    `MR(3)` **exactly** (Residential `7.7419`, Non-Residential `25.2216`) — the
    City published 2026 rates and we already hold them; (c) the residential fit
    above.
  - ⚠️ **WHY THE GUARD IS BLIND.** `scripts/check_year_alignment.py`
    `parse_coverage_year()` reads
    `metadata.custom_fields["Time Frame"]["Period of Coverage"]`, which still
    says `"2025-01-01 to 2025-12-31"` (`Date Updated: 2026-05-11`). **The City
    did not update that string when the roll rolled.** `vintage_report.py`
    reports "Roll is 2025, pin is 2025 — aligned" and the January year-roll
    checklist never fires. **A guard that trusts a publisher's free-text
    metadata field is not measuring the data** — this is the project's
    signature failure mode wearing a green checkmark.
  - ⚠️ **IMPACT ON EVERY PUBLISHED LEVY NUMBER.** `main.py ASSESSMENT_YEAR = 2025`
    feeds `apply_tax_rates(..., assessment_year)`, so the 2026 roll is billed at
    2025 rates: Residential `7.6254` vs `7.7419` (**−1.5%**), Non-Residential
    `24.2229` vs `25.2216` (**−4.0%**). Citywide our levy reads **$2,714,729,701**
    at 2025 rates vs **$2,784,219,936** at 2026 — the site **understates by
    ~$69.5M (2.5%)** from the rate year alone, on top of showing a 2026 roll
    labelled 2025.
  - ✅ **APPLIED 2026-08-25** (Peter: "yeah sure can you just do them?"):
    1. **Detector fixed FIRST**, so this cannot recur silently every January.
       New `scripts/check_roll_year_against_fir.py` measures the **parcels**:
       our residential base vs Edmonton's filed base (FIR `MR(2)`), exit 3 on
       mismatch. New `scripts/fetch_fir_tax_base.py` → committed
       `data/fir_tax_base.json` (manual/reviewed, the mill-rates pattern;
       `data/DATA.md` §21). `check_year_alignment.py` now returns INCONCLUSIVE
       — never "aligned" — when the coverage string is older than the calendar
       year, so a stale string can no longer read as agreement.
    2. **Re-pinned** `ASSESSMENT_YEAR` (`main.py`) and `DATA_YEAR`/`RATE_YEAR`
       (`generate_status.py`) to 2026. Verified against `docs/RUNBOOK.md` §1:
       mill rates 2026 pre-staged and complete for `DISPLAY_RATE_CLASSES`,
       stormwater has 2026, `WATER_RATE_YEAR`/`FRANCHISE_RATE_YEAR` already
       2026 and left alone.
    3. ⚠️ **Activity windows deliberately NOT bumped** — `FIRE_YEARS` /
       `PERMIT_YEARS` / `PERMIT_YEARS_RECENT` pin the last **COMPLETE** calendar
       year, which is still 2025 in Aug 2026. No deflator re-run needed either
       (no new permit year pulled in).
    4. **Temporal baseline re-pinned** (`--write-baseline`) after reading the
       guard first, per RUNBOOK step 8. 2025 correctly moved live→archive; the
       series is now 2012-2023, 2025-2026, live year 2026, no hard-fail.
    5. **Measured result:** citywide levy $2,714,729,701 → **$2,784,219,621**
       (+$69.5M, the rate year alone). Pipeline run end-to-end, `pytest` 713
       passed.
  - ⚠️ **NOT DONE — the banner.** `generate_status.py --clear-banner` (RUNBOOK
    step 10) was not run: no banner was ever raised, because the guard never
    detected the roll. Confirm none is showing after the next refresh deploy.


- [x] **▶▶ FIXED 2026-08-25 — THE MAP'S LEVIED/EXEMPT UNCERTAINTY BAND WAS TOO
  NARROW — `PS`
  ("Parks and Services") is categorised `never`, not `inst`, so $88M/yr of levy
  is missing from the exempt scenario.** Opened 2026-08-25, falls straight out
  of the zone decomposition above. ⚠️ **This one DOES reach the rendered map**
  (the FIR findings above are all docs-only so far).
  - **What the band is.** `web/index.html` renders a two-scenario uncertainty
    band per hood — a levied prism and an exempt prism
    (`inst-band-levied`/`inst-band-exempt`, `deviation-band-*`) — gated on
    `INST_UNCERTAIN_MIN = 0.25` against `rev_frac_inst`. Deliberately
    **achromatic**, because a band asserting no direction must not be tinted
    toward either pole. `GLASS_INST_MIN = 0.25` does the same for the 100 m
    grid via `inst_frac`.
  - ⚠️ **The defect.** `rev_frac_inst` comes from `load_zoning.ZONE_CATEGORY`,
    where **`PS` → `"never"`** while only `AJ`/`UF`/`UI`/`PU` → `"inst"`.
    Measured on the 2026 roll at 2026 rates:

    | | levy | share of citywide |
    |---|---|---|
    | AJ/UF/UI/PU — drives the band | $136,423,407 | 4.90% |
    | **PS — excluded from it** | **$88,038,783** | **3.16%** |

    **Treating PS as institutional would widen the band by 65%.**
  - ⚠️ **ONE MAPPING IS DOING TWO INCOMPATIBLE JOBS.** `ZONE_CATEGORY` answers
    both *"can this ever be developed?"* (where `PS` → `never` is **correct** —
    parks aren't infill) and *"might this be exempt?"* (where `PS` → `never` is
    **wrong** — parks are prime exempt candidates). A single category cannot
    express both. ⚠️ **Do not "fix" this by moving `PS` to `inst`** — that
    would break the development lens. It needs a second, independent
    exempt-candidate set.
  - **Hoods that would newly cross the 0.25 gate: 17 → 24 (+7).**

    | hood | today | with PS |
    |---|---|---|
    | MILL WOODS PARK | 0.000 | **1.000** |
    | MCQUEEN | 0.190 | 0.412 |
    | CALLINGWOOD NORTH | 0.000 | 0.373 |
    | ROYAL GARDENS | 0.000 | 0.318 |
    | HERITAGE VALLEY TOWN CENTRE | 0.030 | 0.310 |
    | WOODCROFT | 0.196 | 0.298 |
    | LEGER | 0.003 | 0.291 |

    ⚠️ **MILL WOODS PARK is the headline: its ENTIRE levy sits on `PS` zoning,
    and the map currently draws it as fully certain** — no band at all — when
    it may be the most exempt-exposed hood in the city.
  - ⚠️ **My 17 is an approximation of the code's 15** (`INST_UNCERTAIN_MIN`'s
    comment says *"15 hoods on Total; 2 on Residential"*). I counted every hood
    with levy; the map also applies `inDeviationPop(p)`, which I did not
    replicate, and the comment predates the 2026 roll. **Re-derive in-code
    before quoting either number.**
  - ✅ **APPLIED 2026-08-25, together with the roll-vintage fix above.**
    - New `load_zoning.EXEMPT_CANDIDATE_ZONES = ("AJ","UF","UI","PU","PS")`,
      **deliberately independent of `ZONE_CATEGORY`** — which keeps `PS` →
      `never`, so the development lens is untouched. Both sets carry comments
      saying why the other exists and warning against merging them.
    - `property_zone_categories` refactored onto a new `property_zone_codes`,
      so the exempt share reads the raw zone CODE off the **same single**
      440k-point join rather than adding a second one.
    - New per-hood `rev_frac_exempt` (NOT folded into the `rev_frac_*` family,
      which partitions levy and sums to 1.0 — this cuts across it). Grid's
      `inst_levy`/`inst_frac` renamed `exempt_levy`/`exempt_frac`; client's
      `instFrac`/`INST_UNCERTAIN_MIN`/`GLASS_INST_MIN` renamed to match, because
      a column named `inst_*` that includes parks is a lie.
    - **Measured on the real pipeline output, not a model:** hoods at/over the
      0.25 gate **17 → 24** citywide; **MILL WOODS PARK 0.000 → 1.000**. In the
      tooltip's deviation population the caveat tier is **15 → 21** (the six new
      ones all park-dominated) and the band-prism set is unchanged at 6.
    - **Verified:** `verify-glass-inst.js` 15/15, `verify-inst-caveat.js` 25/25
      (two hardcoded expectations updated with the reason recorded: the U of A
      range moved on 2026 RATES, the count on `PS`), `verify-amenity.js` 35/35,
      `pytest` 713 passed.
  - **Next:** re-derive independently before trusting it; decide whether the
    site should state a measured overstatement against a filed figure. ⚠️
    **This is a public-number question and Peter's call**, same as sub-item (3)
    above — but it now has an external reference point, which is exactly what
    that item said it lacked.


- [x] **Sweep the doc-to-doc citations — DONE 2026-08-09 (S104). ONE REAL
  DEFECT, and it was a locked decision built on a display artifact.** The
  mechanical half was already automated (`scripts/check_doc_citations.py`,
  S103); this ran the judgement half — whether the prose a citation points at
  still supports the claim — over the 168 doc-to-doc citation sites that carry a
  falsifiable figure, re-deriving from `data/raw/` rather than comparing texts.
  ⚠️ **RETRACTED: "14% of Edmonton has no neighbourhood polygon" (2026-08-08).**
  It read **672.4 km²** of drawn hood fabric against a **782.1 km²** city and
  called the **109.6 km²** difference annexed land carrying no neighbourhood, in
  `DATA.md` §3 + §14, `DECISIONS.md`, `build_reference_layers.py` and a
  `web/index.html` comment. Measured in `EPSG:3400`, the same 406 hoods cover
  **782.0 km² in the RAW boundary file** against a **782.4 km²** legal outline —
  agreeing to **1.4 km²**, inside that outline's own 100 m simplification noise.
  **The raw fabric tiles the city.** The 109.6 km² is `main.py`'s
  **`SETBACK_M = 45.0`** display buffer: **all 406 hoods lose area** (median
  **18.3%**, min 2.7%, max 65.9% — perimeter-proportional, the signature of a
  shrink, not of missing land), and `buffer(-45)` + `simplify(10)` reproduces
  the shipped **672.42 km²** to the decimal. **No wrong number reached the
  public page** — code comments and docs only. The 2026-08-08 decision to draw
  the limit **survives**; its stated evidence did not.
  ⚠️ **The generalisable lesson: a number read off a SHIPPED DISPLAY FILE is not
  a fact about the world.** `neighbourhood_value_per_acre.geojson` is
  post-setback, post-simplify geometry, and `join_and_calculate.py` already
  documented both as display-only — the doc that got it wrong never opened it.
  **Also fixed:** both outstanding guard warnings (`UI.md "Roads ground layer"`
  → `"Services views"`; the audit brief's `docs/SPEC` → `docs/SPEC_phase1.md`,
  a file that **never existed in history**), an overstatement in S103's own
  record (it called three cited files missing; **two have existed since
  2026-05-16** and the ledger's 2026-07-09 row records the brief being executed
  against one of them), a `FINDINGS_lot_dedupe.md` pointer, and an external
  "project knowledge" reference now marked as unverifiable-in-repo. Citation
  guard: **0 warnings, down from 5**. — 2026-08-09 · `docs/TODO_archive.md`
  **Verified correct and left alone** (re-derived, not compared): the `$50k` /
  `$4M` colour clamps still sit at **p97.0 / p97.5** on live data; roads
  `$264–$3,253` and fire `$7,092–$298,901` anchors; `rho +0.959` over all 406;
  the served grid's top three lot-acre cells **612.3 / 149.3 / 143.0** (exact);
  the whole Open-Budget corroboration table (**99.7% / 99.1% / 97.1%**, snow to
  **99.2%**, roads **4.6×**); the census anchor **459,859**. Two dated
  measurements have drifted with the weekly refresh and were left as dated:
  the stock-age grid (**34,675** cells → 34,671) and the 5yr geocode coverage
  (**47,125/59,697** → 47,052/59,687) — both still support their conclusions.
  Full result: `docs/AUDIT_LEDGER.md` 2026-08-09 (S104).


- [x] **`WEST MEADOWLARK PARK`'s revenue MORE THAN DOUBLED in one auto-refresh —
  EXPLAINED 2026-08-07: a RENUMBERING GAP CLOSING, so the +130% was the
  CORRECTION, not the defect.**
  `total_revenue` $4.63M → $10.63M (+130%). ⚠️ **`$4.63M` was the wrong number;
  `$10.63M` is right — the map had been UNDERSTATING this hood by ~$250M of
  assessed value / ~$6M/yr for as long as the gap lasted.**
  - ⚠️ **THE ANSWER MOVED THREE TIMES AND THE FIRST TWO ARE IN THE COMMIT
    HISTORY. Do not cite them.**
    1. *"One new $247.8M parcel arrived."* **True but shallow** — every figure
       below still holds, it just is not what happened.
    2. *"Is a hospital supposed to be taxable?"* **THE WRONG QUESTION.** It
       always was taxable and always was on the roll.
    3. ✅ **A RENUMBERING GAP.** Misericordia has been continuously assessed
       **2012–2025** as account **`10095840`** (~$200–260M, always WEST
       MEADOWLARK PARK, always COMMERCIAL). It was renumbered to `11495573` and
       was simply **absent from the published current roll** during the
       changeover. Nothing arrived; something came back.
  - **The pipeline did the right thing throughout.** Account **`11495573`, 16940
    87 AVENUE NW**, `tax_class = Non Residential`. Parcel count 1079 → 1080 and
    `$438,858,000 + $247,780,500 = $686,638,500` **exactly**. Implied rate
    **2.4223%** = **24.223 mills** = exactly the 2025 Non Residential municipal
    rate in `data/mill_rates.json` (24.2229). Value rose 56.5% while revenue rose
    129.7% purely because the parcel is taxed at 3.2× the residential rate.
  - **The other candidates are ruled out by measurement.** Not a hood
    reassignment — the largest value *drop* anywhere was QUEEN MARY PARK at
    ≈$6.6M, nothing lost $247M. Not `qi6a-xuwt` — that defect is accounts
    *missing* from the historical roll; this is one *arriving* in the current
    one. Not a code change — `git log f76fc7d..f464bdf` is the single data-bot
    commit.
  - ⚠️ **The item's own reproduce line was off by one refresh.** The jump landed
    at **`f464bdf`, the SECOND 2026-08-03 refresh**, not the 08-03 → 08-04
    boundary. Eleventh time a stated basis did not survive re-measurement.
  - ⚠️ **This is the event that exposed the guard hole, and that is one durable
    outcome.** The run was **green** — all five guards passed, no email, four
    days on the live map, found only by diffing git revisions for an unrelated
    reason. `scripts/check_revenue_deltas.py` now exists because of it, and
    **warn-not-fail turned out to be right for a reason only visible at the
    end**: the event it catches is a correction, so failing the publish on it
    would have been exactly backwards.
  - ⚠️ **The other durable outcome is the general lesson:** every identifier in
    the assessment data churns independently (account renumbered, address
    re-addressed, neighbourhood renamed), so a check built on any one of them
    reports churn as loss. `tools/audit_roll_continuity.py` matches by
    **position** because of this. See `docs/DECISIONS.md` 2026-08-07 (×2) and
    the session-summary for S100.
  - **The residual question is upstream and is its own open item** (whether the
    revenue model should treat `AJ/PU/UI/UF` differently at all — ~$125.4M/yr of
    modelled levy, Peter's call, not decidable from this dataset). ⚠️ Note that
    this is **no longer** framed as "was West Meadowlark's parcel anomalous" —
    it was not; it is 5% of a pre-existing exposure present in every published
    number all along. Revenue side only — `road_m_per_acre` changed in 0 of 406
    hoods, so no renewal figure moved.


- [x] **RE-PIN `data/expected_columns.json` ONCE the four Stage 2 columns ship
  — CLOSED 2026-08-04, 62 → 66.** (`cost_roads_ops_per_acre`,
  `cost_transit_ops_per_acre`, `cost_bike_ops_per_acre`,
  `transport_cost_ops_per_acre`.)
  - The item's gate was *"do NOT re-pin before the refresh carries them"*, and
    the weekly cron was 6 days out (Monday 2026-08-10). Peter chose to
    **dispatch `refresh.yml` by hand** instead of waiting — run
    `30909649645`, success, data commit `024ecc6`.
  - ⚠️ **The item's prediction held exactly, which is worth recording because
    the previous two closed items' predictions did NOT.** Against the freshly
    published GeoJSON the guard warned on all four columns as NEW and exited
    **0** — the correct interim state, not a problem. It took that same path in
    CI on the same run.
  - Verified before re-pinning: all four columns present on all **406**
    features, 66 columns total, and the composite sums exactly
    (`88.92 + 13820.65 + 129.59 = 14039.16`). Re-pin diff is a pure four-line
    addition — no column silently changed name or vanished. Clean re-run
    afterwards: *"all 66 baselined columns present on all 406 features"*.
  - ⚠️ **`python` on this box is the SYSTEM interpreter and cannot run this
    script** — `dict[str, int]` raises `TypeError: 'type' object is not
    subscriptable`. Use `.venv/bin/python`. The restoration procedures write
    bare `python` after a `source .venv/bin/activate` that is easy to skip.

- [x] **THE SERVED-COLUMN GUARD HAD NEVER RUN IN CI — CLOSED 2026-08-04 on the
  same run.** Carried S89 → S91 as a next-step, never as a `TODO.md` item.
  Step *"Check served columns (guard after regenerating)"* executed and
  reported success on run `30909649645`. It is no longer an untested code path
  in the weekly publish.
  - Also closed on that run: both S90 features' **data** finally shipped. The
    three transport cost rows and the budget-context pod had been correctly
    hidden since 2026-08-03 because those were code-only deploys.
  - Verified against **production**, not a local build:
    `verify-transport-cost.js` went **6 → 41 passed / 0 failed** against
    `/full/` — including the load-bearing two-bases assertion, roads operating
    **$89** vs lifecycle svc **$7,527** on the same metres — and
    `verify-about.js` returned **ALL CHECKS PASSED** against the public root,
    recomputing all four budget shares independently from the published dollars
    (12.2% / 1.3% / 0.79% / 0.15%) and fitting the pod at 720px tall.

- [x] **`verify-peek.js` WAS 71% OF THE SUITE'S WALL TIME — FIXED 2026-08-04,
  437s → 94s, all 27 checks still green.** The item was right that the script
  dominated the suite and right that the cost was software-GL picking. ⚠️ **It
  named the wrong loop, and both of its proposed levers were wrong** — which is
  why the first thing done was to re-measure rather than act on it.
  - **The item blamed `findTappableHoods` (the `targets` grid sweep). Measured
    2026-08-04, that sweep is 46s of 408s.** It exits as soon as it has `n`
    hoods, so it never approaches its 2,400-candidate worst case: **1 candidate
    / 9 picks** on desktop, **22 candidates / 57 picks** on touch. The real cost
    was the **empty-map-pixel scan** — **346s, 85% of the total** — a blind 7px
    sweep making **~2,470 picks** before it found a pixel that picks nothing.
  - ⚠️ **A PICK COSTS ~137ms AND NEITHER `radius` NOR `deviceScaleFactor`
    CHANGES THAT** (measured: r0 vs r6 identical; dsf3 vs dsf1 identical). The
    cost is deck **re-rendering the whole picking buffer** on the CPU under
    SwiftShader on *every* `pickObject` call, not the buffer readback. So the
    only lever that works is **making fewer picks**. Separately, the **first**
    pick burst in a context carries a **one-off ~20s** of shader warm-up, which
    is what `targets`' remaining 46s almost entirely is — it is already at the
    floor and was deliberately left alone.
  - ⚠️ **"Coarsen the grid" was measured and is a TRAP.** Step 7 → 25 still
    costs 30s, and **step 40 finds no empty pixel at all** and would fail the
    check. Empty pixels are genuinely scarce here: only **17 of the 4,400**
    points on the 7px grid are clear.
  - **The fix is the item's *other* lever, applied to the loop that actually
    cost the time: derive the pixel from geometry, pick only to confirm.**
    `metric-extrusion` is the **only pickable layer**, so "no hood polygon
    covers this pixel" and "`pickObject` returns nothing" are the same
    statement — and `boot()` has already flattened the map, so a prism's screen
    footprint is just its projected polygon. Project all 406 hoods' rings to
    screen (**9,236 vertices, 14ms**), ray-cast point-in-polygon with a bbox
    pre-filter, require an 8-point ring at 7px to be clear as well, then confirm
    the first candidate with **one** real pick. **2,474 picks → 1**, landing on
    the *same* pixel (382,425) the blind sweep found. Falls back to a 3px grid
    if the 7px one yields nothing, since geometry tests are free where picks are
    not. — 2026-08-04 · `tools/profiling/verify-peek.js`

- [x] **▶ THE HISTORY PANEL PAINTS OVER THE TITLE BLURB IN FIVE STATES.
  FIXED 2026-08-02** (`verify-temporal.js` **43 → 67 checks**). Measured on clean
  master 2026-08-01; **re-measured 2026-08-02 before anything was touched and
  found identical** — 46 / 46 / 158 / 252 / 289px — despite three PRs having
  landed on this area since. A rare case of a carried item whose numbers were
  *not* stale.
  - ⚠️ **Two things in the item WERE stale, and the re-measurement caught both.**
    Its title says *"the history panel"*, but two of the five states now show the
    **revenue-mix** panel, which did not exist when it was written — and the two
    modes are **different heights** (293 vs 308px), so a fix assuming one height
    is wrong in the other. And it asserted that moving the panel below the blurb
    "does not fit", generalising from Infill: it fits in **3 of the 5** (money's
    cuts with 172px spare, the change lens with 45px) and fails only in
    Development (by 26px) and Infill (by 100px).
  - **Ruled (Peter): track the measured title, and cap.** `syncTemporalPos`
    measures `#title` and `#botleft` and places the panel between them —
    `syncMillRates` + its `ResizeObserver` was the pattern, and observers now
    watch **both** boxes, since `#botleft`'s legend changes height per view.
  - ⚠️ **WHICH ELEMENT YIELDS REVERSED DURING IMPLEMENTATION, on a finding.**
    The ruling was *cap the blurb*; `#title` is `class="panel"` and `.panel` sets
    **`pointer-events: none`**, so a capped, scrollable blurb **cannot be
    scrolled to** — it would hide text with no way to reach it. Giving `#title p`
    pointer-events:auto would steal a ~360×380px region from map dragging, the
    failure `#botleft`'s own comment records having caused. `#temporal` is
    already pointer-events:auto, so the **panel** yields instead. Re-ruled by
    Peter on that evidence.
  - ⚠️ **TWO DEFECTS THE FIRST IMPLEMENTATION SHIPPED, BOTH FOUND BY MEASURING
    THE FIX RATHER THAN ASSUMING IT:**
    - `max-height` is **content-box** by default, so it excluded the 21px of
      vertical padding + border and the panel overshot `#botleft` by exactly
      that minus the gap — **11px, in every state that capped**, including two
      that did not even scroll. `#temporal` is `box-sizing: border-box` now
      (width 300 → 328 keeps the content box identical).
    - **An absolutely-positioned close button inside a scroll container scrolls
      away with the content.** The x *and* the hood name both left the box in
      Infill — the two things you need in order to use a scrolled panel. New
      `#temporal-body` wrapper holds the scrolling region.
  - **Result at 1440×900: all ten states clear both the blurb and `#botleft`.**
    Two scroll (Development −38px, Infill −112px). Below ~768px tall the two
    longest blurbs hit the min-height floor and reach into `#botleft` — left
    open in `TODO.md`, because at 1280×720 Infill's blurb is 479px of a 720px
    screen and the column has **36px** free, so no placement rule can fix it.
  - ⚠️ **The CHECK was the other half of the bug.** `panel clears the title`
    passed throughout, because it only ever ran on money/value — the same narrow
    case the original 210px sweep was written from. It now sweeps **six states**,
    and also asserts the name and the x survive a scroll. **Falsified both:**
    restoring the constant `top` fails exactly the five original states; moving
    the name back into the scrolling region fails the two that scroll.

- [x] **`verify-temporal.js` HAD BEEN RED SINCE THE 2026-08-01 AUTO-REFRESH, and
  nothing reported it. DIAGNOSED AND FIXED 2026-08-02** (42 → 43 checks, green).
  5 of 42 checks failed on clean master: Downtown's share read **3.28%** where
  the script pinned **3.30%**, with the commercial-base and current-value
  literals moved with it.
  - **The item asked: did the data move, or did the splice move? Answer: the
    data, and only its live year.** Diffing the served `temporal.json` at
    `ab8bac7` against `4466fbf` across all 406 hoods and all three series:
    **839 cells changed and every single one is in the 2025 column.**
    2012–2023 are **bit-identical**, the hood set is unchanged (nonzero counts
    404 / 406 / 402 both sides), and the shares still conserve to 100%
    (999,993 → 1,000,008 ppm). Citywide 2025 value rose 0.296%
    ($237.50B → $238.20B) while Downtown's own fell 0.32%, which is exactly why
    its share fell 3.2991% → 3.2788%. The archive half of the splice never moved.
  - ⚠️ **THE DEFECT WAS IN THE SCRIPT, AND IT CONTRADICTED A GUARD THAT WAS
    ALREADY RIGHT.** `scripts/check_temporal_years.py` ran on that refresh and
    **passed**; its docstring pre-registers this exact movement — *"The live
    year is NOT pinned to a band. It is a live snapshot that genuinely moves
    week to week … so a pinned band would cry wolf continuously."*
    `verify-temporal.js` pinned that same quantity to **equalities**. This was
    not a near-miss the guard failed to catch; it was cry-wolf by construction,
    and it would have gone red after essentially every roll update.
  - ⚠️ **The item's own premise was false and is corrected in place:** it claimed
    the temporal file "has no equivalent" of `check_value_anchors.py`. The guard
    exists and runs in `refresh.yml` before the status-manifest step. **Sixth
    time an open item's stated cause did not survive reproduction.**
  - **Fix: derive, don't band** (Peter's call over the standing *pin bands*
    rule). Live-year numbers are read from the loaded series via `temporalFor`
    and compared against the rendered strings; historical anchors (2012 5.09%,
    peak 5.55% in 2016) stay pinned tight, because those are what prove the
    archive half held. A band would still have needed a width guess and would
    still drift; deriving cannot cry wolf and additionally catches the panel
    rendering the wrong hood, series or index.
  - ⚠️ **Compare PARSED NUMBERS, never a string built with the page's own
    formatter** — that would have made S85's `fmtBig` bug invisible. Tolerance
    is one display ulp (0.006; both formatters carry two decimals).
  - **Falsified all three, per the standing rule:** an off-by-one live index
    (`length - 2`) fails 3 checks; the commercial slot rendering `share` instead
    of `commercial` fails 1; `fmtBig` dropping a decimal (**"$8B"** — the S85
    bug shape exactly) fails 1.
  - **Left open as a proposal:** a data-only refresh still triggers no deploy and
    runs no front-end check at all. The data side is guarded; the *render* is not.

- [x] **UI BUG: the Display popover and the Data & Methods pod overlap.
  FIXED 2026-08-02** (`#a11y-menu { bottom: calc(200% + 8px) }`;
  `verify-about.js` **44 → 50 checks**). Reported by Peter 2026-07-28.
  **Both the reported DIRECTION and the suspected CAUSE failed to survive
  reproduction — the fifth time an open item's stated cause proved wrong.**
  - **The direction was backwards.** The item said Display "covers" the
    Data & Methods button. Measured, it is the reverse: equal `z-index` falls
    back to DOM order and `#about` is later, so the **button paints over the
    menu**, truncating *"Landmarks & nearby pla⌷es"*. Found in a screenshot;
    the `elementFromPoint` probe agreed.
  - **The cause was not the z-index asymmetry.** It is that the two pods form a
    **stack** in one column (`#a11y` `bottom:40px`, `#about` `bottom:68px`,
    both buttons 26px tall) while `#a11y-menu` was anchored to its **own**
    button's top (`calc(100% + 6px)`), ignoring the sibling above it. Both
    offsets are fixed, so the ~23px collision was identical at 1440x900,
    390x844 and 360x780.
  - ⚠️ **THE SUSPECTED FIX WOULD HAVE BEEN WORSE THAN THE BUG.** The
    hypothesised `#a11y.open { z-index: 5 }` was **falsified by applying it**:
    it paints the menu over the button, and `verify-about.js` then **times
    out** because the *"Landmarks & nearby places"* label **intercepts pointer
    events** — the Data & Methods button becomes **unclickable**. A visual
    defect would have been traded for a dead control. (Caught only because
    `verify-about.js` uses a real `page.click()`; a JS `.click()` bypasses
    `pointer-events` and would have passed.)
  - ⚠️ **The new checks assert GEOMETRY (no overlap), not paint order.** A
    "menu is on top" assertion passes for the z-index version — the very
    outcome to reject. Only *they do not overlap at all* rejects both failures.
  - `calc(200% + 8px)` tracks the shared button styling (the pod's own height
    counted twice, plus the 2px inter-pod gap and the 6px the menu already
    wanted) instead of hardcoding 60px.


- [x] **▶ REVENUE-LENS READOUT — phase 2 of 2: the UI. DONE 2026-08-01 (both
  halves).** Phase 1 (the pipeline) shipped the columns earlier the same day.
  Peter: *"I actually want this in the popup panel, instead of the assessment
  graph, on the revenue lens. also can we have the current relevant mill rates in
  the top left on this lens?"*
  - **Decisions RULED by Peter:** top by **category**, not raw zone code; on
    Money/Revenue the panel shows the breakdown **instead of** the assessment
    graph, with history staying reachable via the Change-over-time lens;
    pipeline before UI.
  - [x] **(a) The panel. DONE 2026-08-01** (`renderRevenueMix`,
    `verify-revenue-panel.js`, **37 checks**). `#temporal` gained a MODE rather
    than a sibling — it already owned the three dismissals, the `CHROME_IDS`
    exemption, the phone bottom-sheet form, `#hoodmode` and the peek card's
    commit path. Three rulings taken at build time, all revising the brief:
    - **ALL non-zero categories, ranked — not top 3.** The panel has the room a
      tooltip doesn't, so the rows sum to 100% with no unstated remainder
      (Downtown's top 3 is only 90%).
    - **Shown on the Residential/Non-residential cuts too, with the denominator
      NAMED.** `rev_frac_*` are shares of the hood's TOTAL levy while those cuts
      colour one class of it — so panel and map divide by different things, and
      §6's rule applies: an unnamed denominator is how a correct number reads as
      wrong.
    - **The header keeps `total_revenue` + `revenue_share_city`.**
    - ⚠️ **The categories are `USE_CATEGORIES`' OWN**, column derived as
      `"rev_" + u.frac` rather than listed again — that is what stops the Uses
      lens's area shares and this panel's revenue shares drifting apart.
    - ⚠️ **Three surfaces advertise the panel and all three follow the lens**
      (`#peek-go`, `#temporal-hint`, the tooltip's invite). A pinned panel also
      re-renders on any lens change (`syncPinnedPanel`) — a revenue breakdown
      left under a value map is a silent-correctness failure.
    - ⚠️ **`fmtBig` could NOT be reused for the levy:** calibrated for
      assessment totals ($10M–$10B), it rounds megas whole and printed a
      $1,876,137 levy as **"$2M"** — a 7% error on a fiscal headline. `fmtLevy`
      keeps two decimals. Caught by reading the rendered output, not by a test.
    - `SPEC_temporal.md` §2 now opens with the warning that the panel is the
      history surface **only under Value**; `verify-temporal.js` selects Value
      on every page it opens.
  - [x] **(b) Mill rates. DONE 2026-08-01** (`#millrates`,
    `verify-millrates.js`, **54 checks**; PRs #131 / #132 / #133, **production
    verified in both builds**). Three things the brief got wrong, all found by
    measuring:
    - **"~500px of left column is free" was measured with the panel CLOSED.**
      `#temporal` owns that column: it is **308px** tall (its own CSS comment
      says ~265), leaving 211px of slack at 1440x900 but **79px at 1366x768** and
      **31px at 1280x720**. There is no room for pod *and* panel on a laptop, so
      **the pod yields while a hood is pinned** (Peter, after re-measurement,
      reversing his first call to push the panel down).
    - **"Top left is an open spot" is false on two of the three cuts** —
      residential and non-residential blurbs push `#title` to 256, not 196. The
      pod is positioned from the **measured** title box, never a constant.
      This is the same defect the panel has, unfixed — see the item above.
    - **"Relevant = follow the sub-metric" became: show all three, light the
      active ones** (Peter's ruling). Dropping rows would hide the 7.6254-vs-
      24.2229 differential, which is the fact the map rests on.
    - Rates ship in `status.json` as `municipal_rates`, derived from
      `data/mill_rates.json` — never typed into the page. `assumed` is data, so
      the Farmland caveat stops printing by itself when a real row is published.
    - **The PHONE FORM took two goes, and the second deleted the first.** Peter
      saw the desktop-only build (*"no rates show on mobile"*), described a
      standalone stack, then rejected it on sight: ***"i don't like the
      independent mill rates panel. folding it into the tax revenue blurb is
      fine."*** Final: `#millrates` is **re-parented into `#title`** below 640px,
      so the rates open and close with the description blurb and add nothing to
      the default render. Only the stacking (one rate per row) survives from the
      standalone version. ⚠️ **Every problem that version had to solve — an
      anchor clear of `#controls`, its own card background, the inherited
      panel-yield — was an artifact of it being a separate surface.**
      `MOBILE_USABILITY.md` §2 and `DECISIONS.md` have it.
    - ⚠️ **One bug shipped and was fixed inside the day:** the desktop yield
      `#temporal.open ~ #millrates` went out **ungated**, so switching the phone
      readout to **panel mode** blanked the rates with nothing contending (the
      panel is a bottom sheet there). The comment said "desktop-only in effect" —
      reasoning about the LAYOUT, not the SELECTOR. **A media gate was written,
      then falsified as redundant** (a child of `#title` is not `#temporal`'s
      sibling) and dropped. `verify-millrates.js` asserts the behaviour instead.
  - **Available columns** (shipped by phase 1): `total_revenue`,
    `revenue_share_city`, and `rev_frac_{never,notyet,inst,residential,
    commercial,industrial,mixed,dc,other,unzoned}`.
  - ⚠️ **`rev_frac_unzoned` is the honesty column** — 0.002% citywide today. If
    it ever grows, the top-3 is quietly describing less than the whole hood. Do
    not hide it; `src/revenue_by_zone.top_zones()` already excludes it from the
    ranking by default rather than letting it take a slot.


- [x] **UI BUG: the hover tooltip `div.tip` rendered on TOUCH, 127px off the
  right edge. CONFIRMED ON DEVICE and FIXED 2026-07-31.** `tooltipFor` now
  returns null under `noHover()`. Full reasoning in `DECISIONS.md` and
  `SPEC_temporal.md` §2; regression net in `verify-peek.js`.


- [x] **PROMOTED the temporal + change lenses to the PUBLIC build — DONE
  2026-07-31 (PR #121, merged `828bb5a`, deploy green, LIVE).** Peter: *"can we
  actually move those value change over time features to the public build"* →
  **both**. A **content-split tag change, not a re-opened lock**.
  - **Cost: three `FULL_BUILD` conjuncts.** No pipeline, no new columns, no
    build plumbing — `temporal.json` (42 kB gzipped) **already shipped to the
    public root** and the controls were **hidden, not stripped**. The **data**
    gate survives, which is the half that matters.
  - **The verify scripts caught the contract change** — five "the public build
    does NOT have this" assertions. Two made **stricter**: "panel opens" beats
    "cannot open" (a build that failed to load `temporal.json` SATISFIED the old
    absence check, so it could not tell *correctly withheld* from *silently
    broken*), and the change-window check now runs AFTER entering change mode
    (`#chgwindow` is hidden in Money/current in BOTH builds, so the old
    assertion passed for the wrong reason).
  - **A caveat must travel with the lens it qualifies** — new check that the
    public build STATES the 2024 omission.
  - **Verified in the BUILT tree**, not just `?build=public` on source.
  - ⚠️ **`#hoodmode` moved ABOVE `#coloradj`** (Peter), which also fixed
    `verify-coloradj.js`. **That commit was STRANDED** — #121 merged the
    previous commit only, in the gap between the PR-state check and the push
    landing; recovered by cherry-pick into #122. **Re-measuring on the new
    branch is what caught it.**


- [x] **ALL THREE PRE-EXISTING VERIFY FAILURES ARE FIXED (2026-07-31). THE
  SUITE IS GREEN: 26 scripts, 0 failures.** First found 2026-07-29 while
  verifying the CSS extraction (not caused by it), carried through S79 as "fix
  or waive". **All three were STALE TEST EXPECTATIONS, not app bugs** — the app
  was right every time, which is why nothing looked broken on screen.
  - [x] `verify-ind-permits.js` — **both failures were ONE root cause: the
    window suffix.** `state.devWindow` defaults to `"long"`, so the live columns
    are `ind_permits_per_acre_long` / `new_units_per_acre_long`, while the
    script hardcoded the BARE names. The colour check therefore recomputed p97.5
    over a *different distribution* and failed on a small delta
    (`want 148,39,97 got 140,37,97`) that read like ramp drift; the infill check
    listed only the bare names. Both now derive the column from the app's own
    `devCol()`/`DEV_COLS`, so **a future window cannot break them again**. Two
    checks ADDED to keep them honest once the column is app-supplied: the plane
    must be driven by an `ind_permits_per_acre*` column, and infill must never
    read an industrial one.
  - [x] `verify-glass-no-slider.js` — **the 100 m grid is Development's DEFAULT
    (`devGrid: true`), so entering the view lands on the grid, where the slider
    is CORRECT.** The script probed straight after switching view and called the
    result "the neighbourhood choropleth". True when the grid was opt-in, stale
    since. It now selects the choropleth EXPLICITLY rather than trusting the
    view default. (The suspected causes recorded here — the removed Glass slider
    and the moved `#coloradj` — were both wrong.)
  - [x] `verify-coloradj.js` — a THIRD failure, found 2026-07-31 and not
    previously listed. `#coloradj is the last child of #opt-body` and two
    re-checks, all reporting `layers > coloradj > hoodmode`. Confirmed
    pre-existing on master; cause dated to **S78 (#119)**, where `#hoodmode` was
    added to `#opt-body` *after* `#coloradj`. **Unnoticed because S79's gate ran
    3 of the 26 scripts** — the standing cost of a targeted gate. Fixed by
    Peter's call: `#hoodmode` moved ABOVE `#coloradj`, restoring the 2026-07-26
    intent that colour scaling reads last. No CSS `order:` on these pods, so
    markup order is visual order.
  - **Generalisable:** all three failed because a test restated a value the app
    owns (a column name, a default mode, a markup position) instead of reading
    it. ⚠️ **And all three were invisible on screen** — the standing rule is
    that a red verify script is evidence about the *test* as often as the app,
    so diagnose before "fixing" either.
  - **Full-suite baseline, 2026-07-31: 26 scripts / 0 failures.** Run it in
    batches (quirk t): `node tools/profiling/verify.js <url> <names...>`


- [x] ~~**ASSESSMENT-OVER-TIME GRAPH PER NEIGHBOURHOOD**~~ — **✅ COMPLETE
  2026-07-29, live in `/full/`. All four phases shipped; `SPEC_temporal.md` has
  nothing pending.** Read that spec before editing the lens: **§2** for the
  panel's design and the two silent-failure rendering invariants, **§0** before
  touching anything that reads the historical file. Regression net:
  `tools/profiling/verify-temporal.js` (38 checks). The sub-items below are kept
  as the record of how it was decided, not as work.
  Original ask (Peter, 2026-07-28): *"you mouse over and get a line graph of the
  assessment value over time, for that hood."* The data exists and the
  aggregate is cheap — see `data/DATA.md` §"Property Assessment Data
  (Historical)". Measured, not assumed:
  - **`qi6a-xuwt` "Property Assessment Data (Historical)" — 14 years, 2012–2025,
    5.5M rows**, and it carries `neighbourhood_name`, so it never has to be
    downloaded whole. One server-side `$group=neighbourhood_name,assessment_year`
    returns **5,577 rows / 443 hoods in ~3 s, 534 kB raw** — and that is verbose
    JSON; as array-of-arrays it is well under 100 kB before gzip, i.e. ~1% of the
    current 7.7 MB payload. **This is the cheapest new lens the project has ever
    had available.**
  - **The series is a real story, not decoration.** Downtown: $7.30B (2012) →
    **$10.28B peak (2016)** → **$7.09B (2025)** — down ~31% from peak — while its
    account count *rose* 8,716 → 10,307. A revenue-per-acre project that cannot
    show that is leaving its best material on the table.
  - [x] ~~**The home for it**~~ — **sparkline in the hover tooltip PLUS a
    click-to-pin panel.** Peter asked "can that go in the pop ups?" Mechanically
    yes: `tooltipFor` returns an HTML string and a 14-point sparkline is one
    inline `<svg><polyline>` — no library, no dependency. But hover **vanishes on
    mouse-out, cannot be studied, and does not exist on touch at all**, and the
    Money tooltip already carries 3–4 rows — so the sparkline is the teaser and
    the panel is the home. ⚠️ **Attribution, so nobody re-litigates it as
    settled-by-Peter: this was decided on the merits in `SPEC_temporal.md` §2,
    NOT asked.** The touch argument makes it close to forced, and it is cheap to
    reverse, but it is mine. Say so if it comes up.
  - [x] ~~**The pinned panel's DESIGN**~~ — **SETTLED 2026-07-29. Full table in
    `SPEC_temporal.md` §2.** Left column under the title (`top: 210px`, measured
    against a 176–179px title box, not estimated); dismisses three ways (×,
    Escape, a second click on the pinned hood); clicking **another** hood re-pins
    and an empty-map click is **inert**; the sparkline rides **every** view's
    tooltip via one wrapper; phone = a near-opaque bottom sheet. ⚠️ **Attribution:
    decided ON THE MERITS BY ME, not asked** (Peter's instruction was "just pick
    the panel design"). Cheap to reverse.
  - [x] ~~**Where it gets built**~~ — **`/full/` (specialist build), 2026-07-28,
    Peter: "we'd prototype this in full for now."** Natural home: it already
    carries the work-in-progress badge, so an unfinished lens is labelled as
    one. Gate it the established way (`|| !FULL_BUILD` beside the data guard);
    `CONTROLS_MATRIX.md` §2 notes the three places a lens leaks if it is ever
    promoted to public.
  - [x] ~~**Map the defect across all 14 years**~~ — **DONE 2026-07-28**,
    `tools/audit_historical_roll_gaps.py`, map in `output/historical_roll_gaps.json`.
    **Confined to 2024–2025; one dropout event, not systemic.** 2013–2023 clean
    (0–14 accounts/yr = 0.00%); 2024 = 2,322, 2025 = 131 incremental (~2,448
    cumulative). **2012–2023 usable, 2025 repairable via the current roll, 2024
    irreparable.** Full read-out: `docs/SPEC_temporal.md` §0.1.
  - [x] ~~**How to treat 2024**~~ — **OMITTED. Decided 2026-07-28 (Peter).** An
    honest gap in the line, reason stated on hover. **This reversed the balanced
    panel §0.2 originally recommended**: share-of-base is self-normalizing per
    year, so the metric needs each year's roll *complete*, not the account
    universe *constant* — a fixed panel would punch the same $2.93B hole into
    twelve clean years to rescue one broken one. Flag and uncertainty-band lose
    on display grain (invisible at sparkline size). Interpolation stays ruled
    out. Full reasoning: `SPEC_temporal.md` §0.2.
  - [x] ~~**Metric, denominator, per-acre**~~ — **ALL THREE DECIDED 2026-07-28
    (Peter); `SPEC_temporal.md` §7 is now empty and the rows live in §6.** The
    settled cut is **share of the TOTAL citywide base · assessed VALUE · TOTAL
    not per-acre**, the only combination needing no deflator, no area assumption
    and no mill-rate table. Value over revenue (reaches 2012 vs 2014, and skips
    the class-differential caveats); **commercial-base share appears as a
    labelled number in the pinned panel, not a second sparkline**.
  - [x] ~~**The splice + the guard**~~ — **DONE 2026-07-28. PHASE 0 IS CLOSED.**
    `src/load_temporal.py` (splice) + `scripts/check_temporal_years.py` (guard,
    wired into `refresh.yml` before the status-manifest step) + the year × hood ×
    class aggregate added to `download_data.py`. 33 new tests. Read
    `SPEC_temporal.md` §0.3–§0.4 and `ARCHITECTURE.md` before touching either.
  - [x] ~~**Archive the live year, or lose 2025**~~ — **DONE 2026-07-28.**
    `data/temporal_archive.json` (~74 kB/yr, committed), captured on every run
    by `check_temporal_years.py --write-archive`. Freeze rule: only the live
    year is ever written. The archive wins only for `HISTORICAL_DEFECT_YEARS` —
    using it for a clean year would mix vintages. `SPEC_temporal.md` §0.4.
  - [x] ~~**Phases 1, 2 and 4**~~ — **DONE 2026-07-28.** The hood × year module,
    the served file (`web/data/temporal.json`, 406 hoods × 13 years, **89.2 kB**
    of a 100 kB budget), and the guard. Wired into `main.py`.
  - [x] ~~**Phase 3: render it in `/full/`**~~ — **DONE 2026-07-29. THE LENS IS
    COMPLETE; all four phases are shipped.** Sparkline in the tooltip +
    `#temporal` click-to-pin panel; `#temporal` is in `CHROME_IDS`; gated
    `|| !FULL_BUILD` beside a defensive fetch. Regression net:
    **`tools/profiling/verify-temporal.js`, 38 checks.** ⚠️ **Two invariants that
    fail SILENTLY — read `SPEC_temporal.md` §2 before editing the chart:**
    x is scaled from the **year value** and the line is drawn as **runs split at
    every gap** (index positioning or one polyline would hide the 2024 hole, and
    neither is visible to the eye — the verify script *measures* the 2× ratio);
    and the **y axis is not zero-based**, so both endpoints are labelled (most
    hoods are under 1% of the base, so zero-basing flattens 406 series).
    The verify script also earned its keep on the way in: it caught a title
    overlap at the first `top` offset, and the `OLIVER`→`WÎHKWÊNTÔWIN` rename
    crashing its own hood lookup.
  - **Context — the 2024/2025 slices of `qi6a-xuwt` are PROVEN INCOMPLETE** (2026-07-28; evidence in `data/DATA.md` §0). For assessment year
    2025, same year, the current roll has **11,216 Downtown accounts / $7.81B**
    and the historical file has **10,307 / $7.09B** — a **909-account, ~$720M
    hole**, including two entire ICE District towers that are present in 2023,
    absent 2024–25, and present again in the current roll.
    - **This is not a curiosity, it changes the headline number.** The apparent
      Downtown collapse was $2.07B; the real one is **$1.35B**. Peak-to-2025 is
      **−24%, not −31%**. Roughly a third of the story was the hole.
    - **Build the guard first, the graph second.** Same idiom as
      `check_year_alignment.py` / `check_value_anchors.py`: reconcile each year's
      account count + total against a control, and refuse to publish a year that
      does not. **Likely shape: historical for 2012–2023, the current roll for
      the live year.**
    - [x] ~~**Quantify how far the defect reaches**~~ — **DONE 2026-07-28**, all
      14 years. Confined to 2024–2025, one dropout event; 2012–2023 clean.
      ~~"~8,000 accounts short citywide"~~ **was wrong** — inferred from row
      counts of different vintages, and most of that gap is new construction.
      The measured figure is **2,448**. See §0.1 of `SPEC_temporal.md`.
    - [ ] **BUG REPORT to Edmonton Open Data — worth doing (Peter, 2026-07-28),
      gated on Peter reviewing it by hand first.**
      - ⚠️ **THIS SUB-ITEM IS LIVE WORK AND WAS RE-PROMOTED TO `TODO.md` ON
        2026-08-06** — it rode its closed parent into the archive on 2026-07-31
        and was invisible for six days. **Track it in `TODO.md`, not here**;
        the copy below is kept only because this file is verbatim history.
        `tools/todo_archive.py` now refuses to archive a closed parent that
        still has unchecked children.
      Notebook written for exactly
      that: **`notebooks/exploration/03_historical_roll_gap.ipynb`** — hits the
      live API only, no local data, runs top to bottom, re-derives every claim.
      - ✅ **SCOPE NOW MEASURED (2026-07-28) — it is CITYWIDE, and the earlier
        "~8,000" was wrong.** That figure was inferred from row counts; most of
        the gap is new construction. Verified account-by-account: **2,448
        accounts / $2.93B / 188 neighbourhoods** existed in 2023 *and* exist in
        the current roll but are absent from historical 2025. Downtown holds
        1,292 (53%); Magrath Heights 430 (17% of the hood), Glenora 269 (15%).
        **Report the 2,448, never the 8,000.**
      - ✅ **Cite dataset IDs and query params, not prose.** `qi6a-xuwt`
        (Historical) and `q7d6-ambg` (Current Calendar Year); City data staff
        will want exact resource IDs + the SoQL used. The notebook prints both.
      - ⚠️ **LEAVE THE CAUSE UNSTATED.** Describe the symptom — whole multi-unit
        buildings absent together, citywide — and let the City diagnose. Do not
        speculate about leasehold/condo record handling or ETL join logic in the
        report, however tempting the address clustering makes it.
      - [x] ~~Whether the gap reaches years **before 2024**~~ — **SETTLED
        2026-07-28: it does not.** 2012–2023 are clean (0–14 accounts/yr).
        ⚠️ **The N−1/N+1 detector this item originally pointed at cannot answer
        the question** — it is blind to dropouts that never return, and reported
        **5** for 2024 against a true 2,321. The answer came from the
        current-roll control detector. `SPEC_temporal.md` §0.1 (not §4.1 — that
        section number no longer exists).
      - [ ] Still to do before filing: spot-check a few missing accounts against
        the City's public assessment lookup, so the report cites something a
        human can open.
      - **Strongest single exhibit: Stantec Tower** (10310 102 ST NW):
        Edmonton's tallest building, 309 accounts in the 2023 slice, **zero rows
        in 2024 and 2025**, and 310 accounts / $105.7M in the current roll.
  - [x] ~~**⚠️ NAME THE DENOMINATOR IN THE UI**~~ — **DECIDED 2026-07-28: the
    sparkline plots share of the TOTAL base; the pinned panel ALSO states the
    commercial-base share as a labelled number** (not a second line — two series
    is past what a 14-point sparkline carries). Downtown is **3.22% of the total
    base but 9.30% of the COMMERCIAL base** (2025); public reporting (CBC/council
    ~5.2%) quotes the second kind, so an incoming claim that those figures
    "match the project's" does **not** hold against total-value share, and
    publishing 3.22% beside an article saying 5.2% makes the project look wrong
    when it is not. Full table in `ANALYSIS_BACKLOG.md`. **Still binding on the
    build: recompute BOTH from the current roll before publishing.**
  - **RESOLVED 2026-07-28: the office-devaluation story survives, at ~2/3 the
    headline size.** Commercial fell **$6.32B → $4.85B (−23%) on a near-stable
    account count** (822 → 723) — the same buildings reassessed lower, confirmed
    against the roll we ship rather than the suspect historical file. Annotating
    2024 as a "discontinuity" is no longer the plan: it was mostly a data hole,
    so the fix is to **use good data**, not to annotate bad data.
  - **RESOLVED 2026-07-28: the 1,280 missing residential accounts are the
    defect, not an event.** Traced individually — 1,358 of 1,359 exist nowhere in
    the 2024 roll, exactly one moved (to OLIVER), only 2 return in 2025. Not a
    reclassification, not a boundary redraw, not condo-to-rental consolidation.
  - [ ] **Decide the metric: assessed value, or revenue.** Value is available
    2012–2025 directly. *Revenue* needs historical mill rates — we already have
    them (`pwis-wc4c`, "2014 onward"), so a revenue series is possible but starts
    **2014**, not 2012, and inherits every class-differential caveat.
  - [ ] **⚠️ NORMALIZE AGAINST THE CITYWIDE BASE — this is not a polish item, it
    decides whether the graph means anything (Peter asked "does inflation matter
    for people doing this?", 2026-07-28).** The answer is that **inflation is the
    *second*-order problem**. The first-order one: the **mill rate is a
    residual** — council sets a budget, rate = levy ÷ total assessed base — so a
    citywide revaluation is *fiscally neutral* (the rate absorbs it) and a hood's
    tax burden moves **only when its assessment moves differently from the city
    average**. A nominal per-hood series conflates those two. **CPI-deflating
    does not separate them** — it answers a purchasing-power question, not a
    tax-share one. The normalizer that does is the **citywide base itself**
    (share of base, or hood indexed to city): unit-free, no deflator, no vintage
    to maintain.
    - **This changes how the Downtown finding must be read** (see
      `ANALYSIS_BACKLOG.md`): −31% nominal is uninterpretable until set against
      what the citywide base did over the same years. Same query, minus the hood
      dimension.
    - **Where inflation genuinely does bite:** dollars-per-acre *levels* compared
      across years; and the services lens if it ever gets a time axis — revenue
      and modeled cost must share a year's dollars, and city input costs track a
      **Municipal Price Index**, not CPI (asphalt/equipment/wages). CPI on the
      cost side would be the wrong index, not merely imprecise.
    - **Trap:** assessed values embed **house-price** inflation, which has
      diverged sharply from CPI. Deflating asset prices with a consumer index
      reads rigorous and is apples/oranges.
    - **Vintage, affects axis labelling:** Alberta assessments are market value
      as of **July 1 of the preceding year** (MGA) — the 2025 column reflects
      mid-2024 conditions. **Stated from domain knowledge; confirm against
      Edmonton's own published wording before it reaches user-facing copy.**
  - [ ] **Per-acre or total?** The whole project is per-acre, but hood boundaries
    and the account count both move over 14 years (Downtown gained ~1,600
    accounts). A per-acre series divides by a *current* area — state whether that
    is honest before shipping it.
  - ⚠️ **Do not skip the year-alignment question.** `scripts/check_year_alignment.py`
    and the year-roll machinery exist because the current roll's year moves. A
    historical series that silently ends one year early each January is exactly
    the failure this project already guards against elsewhere.


- [x] ~~**TEMPORAL, ROUND 2 — "HOW MUCH HAS EACH HOOD CHANGED?" AS A MAP METRIC,
  WITH SELECTABLE WINDOWS (Peter, 2026-07-30).**~~ — **✅ BUILT 2026-07-30
  (S79), branch `change-metric-map`.** Money sub-mode `#moneymode` (Current /
  Change over time) + `#chgwindow` (Since 2012 / Since 2019), flat diverging
  choropleth, `/full/`-only, no pipeline work. **`verify-change.js`, 36 checks.**
  Full record in `SPEC_temporal.md` **§6b**; three rows in `DECISIONS.md`.
  ⚠️ **TWO OF THE BUILD NOTES BELOW WERE WRONG AND MEASUREMENT CAUGHT THEM** —
  read §6b before touching the metric:
  - **The rate had to become COMPOUND, not arithmetic.** `(last/first - 1)/years`
    is unbounded above (observed max **+2,076%/yr**) and gave the diverging ramp
    arms **108× apart**, so teal was owned by a few new subdivisions. Geometric:
    max +54%/yr, arms 6× apart.
  - **A SECOND degenerate endpoint existed.** The 45 no-baseline hoods were
    known; one hood *ends* at zero share and printed **`-100.00% / yr`**. Both
    ends are off-scale holes with distinct reasons now.
  - The years-elapsed trap flagged below was real and is avoided (13, not 12);
    it is `verify-change.js`'s first check, recomputed from the raw file.
  The sub-items below are kept as the record of how it was decided, not as work.
  Original ask: *"what I want is like, timelines
  options, for how much each hood has changed on average over time… and spike
  chloro map eventually. Like half the time going back, and all the way back in
  the dataset."* The shipped lens answers **one hood at a time**; this asks the
  same data for **all 406 at once**, which is where the fiscal story actually
  reads off the map.
  - **✅ NO PIPELINE WORK, NO NEW COLUMNS.** `web/data/temporal.json` (406 hoods
    × 13 years, already in the browser in `/full/`) has everything. Derive the
    change per hood **client-side** and join it onto `state.data.features` at
    load. Consequence: switching windows recomputes instantly with no refetch —
    and the whole family is **`/full/`-only**, like the lens it reads.
  - ⚠️ **A SPIKE MAP AND A SIGNED METRIC CONTRADICT EACH OTHER — this is the main
    design tension in the ask.** A prism cannot have negative height, and hoods
    moved **both** directions. **In-repo prior art settled this once already:**
    the Infill lens is a signed z-score and renders as a **flat plane with a
    dark-centred diverging ramp**, not spikes (`infillColorAt` / `INFILL_CENTER`
    / `INFILL_POS` / `INFILL_NEG` in `web/index.html` — symbols, not line
    numbers: those had already drifted 16 lines by the next day). Two honest
    options: (a) **choropleth only**, reusing `infillColorAt` — cheapest, and
    consistent with the one precedent; or (b) **height = |change|, colour =
    direction**, which is legitimate but has to be *said*, because a tall spike
    would then mean "moved a lot" in either direction. **Do not invent a third
    ramp, and do not force a sequential one** — the existing ramps are
    luminance-sequential by decision and cannot show a sign.
  - ⚠️ **THE 2024 GAP BITES AGAIN, IN A NEW PLACE — likely the feature's one
    silent bug.** "Average annual change" must divide by **years elapsed (13)**,
    never by **observed intervals (12)**. The gap means those differ, so dividing
    by intervals inflates every hood's annual rate by ~8%. Same class as
    index-vs-year positioning in the chart, so **make it the first verify check.**
  - **✅ THE GATE HAS BEEN RUN — `ANALYSIS_BACKLOG.md` §10, 2026-07-30. IT PARTLY
    FAILS, so read it before building anything here.** Prompted by Peter: *"I've
    already seen some graphs that have like, a peak in the middle. So straight
    average would be 0."* He is right, and the measurement turned up three things
    that outrank the hump. **Two recommendations this item previously carried were
    WRONG and are struck below.**
  - [x] ~~**DECISION 1 — which measure**~~ — **DECIDED 2026-07-30 (Peter):
    RELATIVE change, with the 45 undefined hoods rendered in the established
    off-scale grey and the reason stated.** Chosen over pp-with-a-sqrt-transform
    because that would rescale a metric which genuinely does not separate rather
    than fixing it — presentation papering over distribution, next door to the
    linear-elevation honesty choice. Cost accepted: **45 grey holes, and they are
    the new-growth areas** — visible absence rather than a wrong number. The
    measured basis is `ANALYSIS_BACKLOG.md` §10; the short version of the bind:
    - `last/first` **does not exist for 45 of 406 hoods (11%)** whose 2012 share
      is zero — Blatchford, Decoteau, Keswick, Glenridding Ravine, Graydon Hill,
      Rosenthal, Stillwater, the Anthony Henday segments. **Exactly the hoods a
      change map most needs to show.**
    - But percentage-point change, which *is* defined everywhere, **does not
      separate**: median hood **−0.032 pp** vs Downtown **−1.791 pp** (**56×**),
      and **15% of hoods move under 0.01 pp in thirteen years**. A pp choropleth
      is Downtown blazing over ~380 visually identical hoods.
    - **Rejected, for the record:** (b) pp with a sqrt/rank transform — see the
      reason above; and (c) relative from each hood's first non-zero year, which
      is defensible but silently puts a 3-year and a 13-year change on one ramp,
      **the comparability trap this project keeps meeting.**
    - [x] ~~⚠️ **Still to settle when it is built: what the 45 grey hoods say on
      hover.**~~ — **✅ DECIDED 2026-07-30, and the honest phrasing was the right
      one.** Hover reads `No 2012 baseline — held none of the assessment base
      that year`; the legend swatch says `No 2012 baseline — off-scale`. Both
      name the YEAR so the absence is checkable against the sparkline
      underneath, and `verify-change.js` asserts the string never contains "set
      aside". The window picker rewrites both to 2019 in the short window.
  - **DECISION 2 — endpoints, and the hump needs a SECOND NUMBER, not a different
    one.** ~~Recommend measuring whether endpoints and OLS slope disagree~~ —
    **measured: rho +0.959 over all 406**, so they are near-duplicates; **+0.719
    restricted to the 34 real humps**, which is Peter's point quantified. ⚠️ **And
    peak-drawdown does NOT fix it either — rho +0.919 against net change**, i.e.
    almost the same ranking. **So use endpoints (explainable, and no worse), and
    give a peaked hood its peak value + peak year as a second reading rather than
    hunting for a cleverer single number.** The panel already computes and shows
    exactly that (`peak share 5.55% in 2016`). Humps are **34 hoods (8%)**;
    71% of hoods are monotone and endpoint arithmetic describes them honestly.
  - **DECISION 3 — the windows. ✅ CONFIRMED WORTH HAVING.** Long (2012→2025) vs
    short (2019→2025): rho **+0.734**, and the sign **flips for 55 of 406 hoods
    (14%)** — so the two windows genuinely tell different stories for a seventh
    of the city, and the "timeline options" ask is not decorative. **Use the
    Development view's window-picker idiom (`#devwindow`: 3yr/5yr/long)** — direct
    in-repo precedent for exactly this control — rather than a free year picker.


- [x] ~~**UI: the pinned panel and the hover popup must not both be up — add an
  explicit MODE toggle**~~ — **✅ DONE 2026-07-30** (Peter: *"I don't want both the
  panel and pop up appearing at the same time… a button that will convert you to
  panel mode, or back to pop up mode"*). `#hoodmode` in `#opt-body` beside
  `#coloradj`, label-is-the-state (`Readout: popup` / `Readout: panel`), hidden
  until `temporal.json` loads so it can never offer a mode that does not exist.
  Regression net: **`tools/profiling/verify-hoodmode.js`, 31 checks.**
  - **Three gestures, three distinct effects — the layering is the design:** the
    **×** clears the pinned hood and stays in panel mode on its prompt; **Escape**
    and **the button** leave the mode. A click in **popup** mode enters panel mode
    *and* pins, which keeps the tooltip's own "click to pin" hint truthful.
  - ⚠️ **This CHANGED `verify-temporal.js`'s contract** and the script caught it:
    a second click on the pinned hood no longer *closes* the panel, it unpins and
    leaves the prompt. Two expectations were rewritten deliberately (and made
    stricter — inertness is now "state unchanged", not "stays closed").
  - **Popup mode** (default): the full hover tooltip, sparkline included.
    **Panel mode**: the tooltip reduced to the headline number + the panel.
    Clicking different hoods still works in panel mode — Peter accepted that it
    is harder.
  - [x] ~~**What happens to the readout in panel mode**~~ — **DECIDED (Peter,
    2026-07-30): the popup is NOT suppressed, it is REDUCED to just the primary
    metric.** *"reduce the popup to just the primary metric once you go panel."*
    So panel mode = a one-line hover (hood name + the view's headline number),
    with the panel carrying the history. Better than either option that was put
    to him: hovering stays useful while browsing hoods, and the objection was
    never "two surfaces at once", it was **two dense blocks competing**.
    - **The sparkline and the `click to pin` hint drop out entirely in panel
      mode** — the panel already draws the chart, so the teaser would duplicate
      it, and the hint is pointless once you are in the mode. Clean shape:
      `tooltipFor` = `viewTooltip` (reduced when in panel mode) **plus** the
      temporal block **only in popup mode**.
    - ⚠️ **DO NOT implement the reduction as "keep row 1".** It happens to be
      right for five of the six views — money, ratio, development, infill, and
      uses (whose primary is the dominant-use label, the mixbar and composition
      being the detail) — but **services is the exception**: its rows lead with
      `road_m_per_acre` whenever roads are present, *regardless of which service
      is driving the ramp*. A naive first-row rule would print road metres while
      the colour is driven by stormwater. **Services' primary is
      `state.svcDriver`'s number.**
    - The set-aside and no-data branches already return a single muted line, so
      they pass through the reduction unchanged.
  - [x] ~~**Where the button goes**~~ — `#opt-body` beside `#coloradj` (Tier 3:
    applies in every view, presentation not data), **not** the Display popover,
    which is accessibility. `CONTROLS_MATRIX.md` §3 updated: `#temporal` is no
    longer tier-less, `#hoodmode` is its control.
  - [x] ~~**The two smaller open ends**~~ — panel mode with nothing pinned shows
    a **prompt** ("Click a neighbourhood to see its assessment history"), because
    a button that appears to do nothing reads as broken; and the **× clears the
    pin only**, since the button that put you in the mode is the one that takes
    you out.


- [x] ~~**NEEDS A PHONE, NOT A BOX: confirm the double-tap-zoom fix (PR #107).**~~
  **CONFIRMED ON DEVICE 2026-07-27** — Peter, on a phone: *"double tap on phone
  no longer zooms in for the buttons, only the map."* Both halves of the design
  hold: the chrome no longer hijacks the gesture, and the map deliberately still
  does. Headless asserts the *mechanism* only (55/55 controls carry
  `touch-action: manipulation`, `#map` does not); the device check is what
  settled the *outcome*, per the tooltip precedent. See `DECISIONS.md`
  2026-07-27, `docs/MOBILE_USABILITY.md` §2b.
  - [ ] **Still open, one gesture:** nobody has actually **pinch-zoomed**. The
    fix deliberately avoids `user-scalable=no` (which would fail WCAG 1.4.4), so
    pinch should be unaffected — but that is reasoning, not a check. Fold it
    into the next phone session rather than making a trip for it.


- [x] ~~**LABEL SWEEP IS BLIND TO DOM CHROME.**~~ **DONE 2026-07-27.**
  `visibleLabels()` now culls labels landing under the HTML chrome, skipping
  them like the existing offscreen cull. Two calls worth knowing before
  touching it: `CHROME_IDS` omits `#layers`/`#coloradj` (borderless sections
  inside `#optpanel`, which is the box that actually paints) and *includes*
  `#title`/`#legend` (no background, but text-over-text is the reported case);
  and the chrome test is **unpadded**, unlike the label-vs-label sweep, because
  `LABEL_PAD` is inter-label breathing room and charging it against a panel
  edge cost DOWNTOWN on a phone. A verify check asserts `CHROME_IDS` covers
  every `.panel` in the document, so a future panel fails loudly. Measured cost
  none: readable-label counts identical (32/32 desktop, 25/25 at 390x844).
  See `DECISIONS.md` 2026-07-27, `docs/UI.md` "Labels dodge the chrome".
  - [ ] **Follow-on, unresolved:** on a phone the chrome covers ~45% of the
    screen, so labels are genuinely scarce there — the cull is correct but the
    underlying problem is that the panels are too big, which is
    `MOBILE_USABILITY.md`'s headline fix (collapse the blurb), not a label
    problem. Worth revisiting label density on mobile only after that lands.


- [x] ~~**PUBLIC BUILD SHAPE**~~ — **LOCKED 2026-07-28: two views, Money ·
  Development.** Peter: *"2 views is fine for release, lock it in."* The three
  provisional full-only tags (Uses, Services, Ratio) are settled, not pending.
  See `DECISIONS.md` 2026-07-28.
  - [ ] **Post-launch: return the pulled lenses ONE AT A TIME, each its own
    release** (Peter: *"we'll add the other stuff later, like one lense at a
    time"*). Not a batch un-pull. Each one needs its own decision, its own
    verification **in the public build**, and its own reason.
    - **Ungating is not just the `#views` line.** `CONTROLS_MATRIX.md` §2 names
      the three places a lens leaks: `tooltipFor`, the Data & Methods copy, the
      legend. Ratio in particular owns two Money-tooltip rows and Services owns
      the modelled-layers caveat + the road/fire/transit source credits.
    - Suggested order is **Ratio or Services first** — they share the roads
      fetch, so whichever lands first pays that cost and the second is nearly
      free. Uses is independent.


- [x] ~~**RIVER GEOMETRY IS UNTRIMMED AND UNCHECKED (audited 2026-07-27).**~~
  **CLOSED 2026-07-27 — NO ACTION.** The river is 95% of `reference.geojson`
  (2,316 verts, 50.7 kB) and `RIVER_SIMPLIFY_M = 25` is ~3× finer than a pixel
  at HOME zoom, with 104 islands = 35% of its vertex budget, 99 on the bare
  tails. Re-simplifying at 100 m would halve the file. The item was scoped as
  *one look decides it*, because there was never a performance argument (54 kB
  = 0.7% of a 7.7 MB payload) — only the visual question of whether the 52–95 m
  islands (~1 px) speckle the tails. **Peter looked on device: they do not.**
  With the only open question answered no, the trim buys nothing. Reopen only
  if speckle shows up at some zoom nobody has tried.


- [x] ~~**FLAKY TEST: `verify-uses-prisms.js` "money: control hidden again, state
  kept" (found 2026-07-27).**~~ **CLOSED 2026-07-28 — NO LONGER REPRODUCIBLE.**
  S71 measured it failing ~3 runs in 4; on 2026-07-28 the **unmodified master
  version passed 4/4**, and a scratch harness replaying the exact check at its
  own 1500 ms sample point passed **8/8**. Most likely already fixed by S73's
  PR #108, which repaired two "chrome read before it was final" ordering bugs in
  `applyView` — the same class that would make this check's `boxShown` /
  `sliderShown` conjuncts race. **Nobody proved that link**; the honest statement
  is only that it does not reproduce.
  - **The inherited diagnosis was wrong in a checkable way, and this is the
    reusable part.** It blamed `layerManager.layers` holding `uses-res-prisms`
    "for a beat" after a view switch. Measured: the managed list is stale only at
    **0 ms** (4 of 30 samples, all at delay 0); by **50 ms** it agrees with
    `props.layers`, and the check samples at **1500 ms**. So that mechanism is
    real but **cannot** explain a failure at the suite's sample point — and the
    check has four conjuncts, not just the layer one. A confident cause named in
    a handoff is still a hypothesis.
  - The probe was switched to `props.layers` anyway (2026-07-28) as **consistency,
    not a bugfix** — it was the only one of nine verify scripts reading deck's
    internal managed list, which also carries sublayers
    (`hood-labels-characters`, `…-polygons-fill`) and is genuinely stale at 0 ms.
    That makes it a latent trap if any delay in the suite is ever shortened.


- [x] ~~**SMALL OPEN UI DECISIONS (2026-07-25).**~~ **ALL THREE CLOSED 2026-07-26**
  (Peter decided; see `DECISIONS.md` 2026-07-26 for the reasoning on each).
  - [x] ~~Does `#coloradj` hide when it doesn't apply?~~ **Yes — built.** _Later
    the same day `#lens` was removed outright, which emptied that column for good:
    `#opt-pres` and `syncPresColumn` are gone and `#coloradj` moved to the BOTTOM
    of the Options panel (`CONTROLS_MATRIX.md` §5.1/§5.2)._
  - [x] ~~Should `#views` keep 14px on phones?~~ **No — stays 12.5px, one row.**
    Deliberate no-op, not an oversight: wrapping the primary control costs more
    than 1.5px buys, and 12.5px still out-ranks the 11.5px modifiers.
  - [x] ~~Center 2D: reframe vs flatten-in-place?~~ **Keeps reframing.** Deliberate
    no-op: the compass needle already does in-place north-up, and both Center
    buttons reframing preserves the only "put the camera back" recovery.


- [x] ~~**Residential revenue metric ("Residential $", Peter 2026-07-16)**~~ —
  **SHIPPED 2026-07-16.** The numerator decomposition Peter asked for (explicit
  residential tax dollars, vs the zoned-area fade lens): `res_levy`
  (RESIDENTIAL + OTHER RESIDENTIAL; MA DERELICT excluded → DECISIONS.md
  2026-07-16) → `res_revenue_per_acre` / `_per_lot_acre` → third Money metric
  + "N% of revenue is residential" tooltip line in all Money metrics.
  DATA.md §4 decomposition, UI.md "Residential revenue metric",
  `verify-res-revenue.js`. Follow-on:
  - [x] ~~**Glass grid file res columns**~~ — **SHIPPED 2026-07-17.**
    `export_value_grid.py` rolls `res_levy` into the 100 m cells
    (`res_revenue_per_acre` / `_per_lot_acre` appended to the payload);
    Glass renders real res cells instead of the hood-prism fallback. Size
    cost weighed: ~1.76 → ~2.1 MB raw (gzipped on Pages). DATA.md §4 "Glass
    grid variant", UI.md Glass bullet; columns reach live on the next weekly
    refresh (column guard until then).


- [x] ~~**Dev+Infill ROUND-2 delta audit**~~ — **EXECUTED 2026-07-16 (S56, same
  session the brief was written; this line was stale until 2026-07-17).**
  Dispositions in `session-summary/2026-07-16.md` §2.D + `docs/AUDIT_LEDGER.md`:
  **0 DEGRADED**; D1+D2 CLOSED (L4→SOUND; denominator bias immaterial), D3
  numbers → recommend disclose-only, D6 SOUND (WATCH: orange clamp = p95 of a
  ~105-member arm). What's LEFT is the **post-audit copy PR** below.
  - [ ] **Post-audit copy PR (small, any model):** apply the D4 verdict-grammar
    copy ("Room to add, quiet lately" / "More building than room suggests" /
    "Activity ≈ room") + the three S56-proposed caveat texts (D2 denominator
    note, D5 z-compression + 0.50-cliff clauses, D3 suite-conversion
    disclosure) to `web/index.html` blurb/tooltip + `docs/SPEC_development.md`
    Lens B — pending Peter's picks on D4 grammar and the D3 fork
    (recommendation: disclose-only). Texts: `session-summary/2026-07-16.md`
    §2.D.


- [x] ~~**PRIORITY — Lot-acre denominator TOGGLE on the neighbourhood (first) lens
  (NEW 2026-07-08, out of the cardinality audit below).**~~ **BUILT 2026-07-08**
  (branch `feature/hood-lot-acre-toggle`): `export_value_grid.build_hood_lot_acres`
  (per-hood dedupe rollup reusing `_point_lot_stats`/`SHARE_MAX_M2`) →
  `join_and_calculate` `lot_acres=` param computes `value_per_lot_acre` /
  `revenue_per_lot_acre` + `parcel_frac`, with a `LOW_PARCEL_FRAC = 0.15` guard
  (7 hoods suppressed on 2025 data — 6 set-aside + MAPLE RIDGE 1.6%); `main.py`
  builds it from the shared `grid_input`; columns in `SLIM_COLUMNS`. Frontend:
  the Glass `#denom` control mirrored onto the Money view (shared `state.denom`,
  `moneyScale()` with runtime p97.5 clamp + height parity, `lotBlurb`/legend/
  tooltip follow). +9 pytest (247), headless-verified
  (`verify-money-denom.js`, all PASS) + screenshots. Real numbers match the
  findings: U of A ×2.0, Rossdale ×2.8, Riverdale ×2.5. **SHIPPED 2026-07-09 —
  PR #23 merged + deployed** (refresh run 28987792808, green; roads download
  fixed by PR #24's 900s timeout + retry same run). Auto-refresh commit `bb224da`
  verified data-only: 0 geometry changes (the Session-27 additive graft matched
  CI-canonical geometry exactly), only `parcel_frac`×233 + `storm_charge`×3 value
  drift from the fresh roll. Original brief kept below for reference.
  <details><summary>original item</summary>
   The audit found the first
  lens has NO bug to fix, but a parcel/lot-acre denominator is worth OFFERING: it
  systematically boosts park/river-valley hoods (median ×2.47 $/acre for the 51 hoods
  <55% parcel land; Rossdale ×2.8, Riverdale ×2.4) — the Urban3-analogous "value per
  *developable* acre" view. 35 of 406 hoods move >50 ranks (Spearman 0.959). Build:
  mirror the Glass view's "Ground acres | Lot acres" toggle on the neighbourhood
  choropleth — add `value_per_lot_acre` / `revenue_per_lot_acre` hood columns
  (aggregate deduped `lot_size` per hood via the shipped `SHARE_MAX_M2` /
  `_point_lot_stats` heuristic in `export_value_grid.py`; reuse `load_property_info`),
  a per-column scale anchor, and a **low-parcel-fraction guard** (suppress hoods
  below ~15% parcel to an "n/a" grey — else near-zero-parcel hoods explode, e.g. Mill
  Woods Golf Course ×6960; plus the `KNOWN_BOUND_OUTLIERS` >100% tail, Pembina).
  Frame honestly: ground-acre = cardinality-robust default, lot-acre = Urban3-analogous.
  Full numbers + rationale: `docs/FINDINGS_denominator_cardinality.md`.
  **Validation/guard fixtures (worked in the findings doc, 2026-07-08):** University
  of Alberta = a guard-PASS case (50% parcel, $7.6M→$15.2M/ac = ×2.0, exempt
  campus/hospital land off-roll) — a new *exempt-institutional* rise category beyond
  the park/river-valley examples; pair it with Mill Woods Golf Course (0% parcel,
  ×6960) as the guard-FAIL case when regression-testing the ~15% floor. NB the toggle
  makes U of A's revenue intensity honest but can't show its exempt-land service
  free-riding — that's the services lens, not this one.
  </details>


- [x] ~~**PRE-LAUNCH AUDIT — record-to-parcel cardinality bug (WEM numerator + condo
  denominator) & lot-acre vs ground-acre methodology (NEW 2026-07-08).**~~ **CLOSED
  2026-07-09** (Q1/Q2/Q5 answered 2026-07-08; Q6/Q7 methodology-note cleanup done
  2026-07-09 — see below). Part of a
  broader sweep to check the main lenses before this goes public/live officially.
  **Q1/Q2/Q5 ANSWERED 2026-07-08** — `docs/FINDINGS_denominator_cardinality.md`
  (`tools/audit_cardinality_denominators.py`): the **first lens is immune to both bugs,
  structurally and empirically** (numerator sums the real per-account roll and never
  joins parcel geometry; denominator is boundary area and never reads lot_size). WEM is
  a SINGLE $1.285B account (a grid needle, not a numerator double-count — the brief's
  premise was inverted). Condo denominator inflation is 0.1% citywide / +12% worst hood
  and the `SHARE_MAX_M2` dedupe already handles it. Ground-acre = 74% parcel land
  citywide (~26% roads/parks/ROW); it is NOT Urban3 lineage (Q6 — Urban3's denominator
  is closer to lot-acre). The lot-acre neighbourhood lens that fell out is now the
  PRIORITY item above. **Q6 + Q7 DONE 2026-07-09 — the methodology-note cleanup:**
  swept the docs (README, SPEC_revenue, ARCHITECTURE, UI, FINDINGS_lot_dedupe,
  DATA_INTEGRITY, web tooltips) and found NO doc actually asserted "ground-acre =
  Urban3/gross-area" — every Urban3 mention already pinned the lineage to *parcel/
  lot*-acre. Added a positive not-Urban3-lineage note to `ARCHITECTURE.md`'s
  ground-acre bullet (so the distinction survives outside the findings doc) + the
  condo-exclusion-as-industry-norm paragraph to `FINDINGS_lot_dedupe.md` §1. Q3 (single
  join-integrity fix) is effectively moot for the first lens — there is no bug to fix; the
  grid already carries the only dedupe needed. Sweep the docs (`FINDINGS_lot_dedupe.md`,
  `DATA_INTEGRITY.md`, README/UI methodology blurbs) for stale Urban3-lineage claims.
  **Original brief for reference —** two
  known distortions share ONE root cause — a **record-to-parcel cardinality mismatch**
  (multiple assessment records → one parcel geometry) — but push in OPPOSITE directions,
  so they do NOT cancel in aggregate and summing-before-dividing at the hood level does
  NOT protect against either (corruption is upstream, in the raw components):
  1. **WEM**: many assessment records join one parcel → inflates the revenue *numerator*,
     denominator unchanged.
  2. **Condos**: shared lot area duplicated across unit records → inflates the area
     *denominator*.
  Overlaps existing machinery: the lot-acre denominator work (PR #12,
  `docs/FINDINGS_lot_dedupe.md`) already ships a repeat-aware `SHARE_MAX_M2` dedupe +
  `*_per_lot_acre` columns and verified WEM as a single-account needle — this audit is
  the systematic pre-launch confirmation + the ground-acre methodology cleanup, not a
  from-scratch dig. **Anchor docs:** `FINDINGS_lot_dedupe.md`, `DATA_INTEGRITY.md`,
  `DATA.md` §2 (condo/lot_size quirks); consider driving with the `edmonton-audit` skill.
  **Questions to answer in code/data (numbers, not yes/no):**
  1. **Quantify WEM's numerator inflation.** Count assessment records per underlying WEM
     parcel geometry; compute the hood's revenue/acre with duplicate-join revenue
     collapsed to one record/parcel vs the current summed total. Report the % distortion.
  2. **Quantify condo denominator inflation.** Confirm whether unit-level records each
     carry the FULL shared lot area (vs a prorated per-unit share); find the hoods with
     the highest condo-titled-unit concentration; compute the % area overcount there
     under current logic vs a corrected (dedup/prorated) area.
  3. **Confirm the root cause is shared** — both bugs = multiple records → one geometry —
     and scope a SINGLE join-integrity fix covering both, not two patches.
  4. **Test ground-acre as a partial mitigation.** Confirm ground-acre (boundary-polygon
     hood area) is structurally immune to the condo bug (never touches parcel/unit
     records), and confirm it does NOT fix the WEM numerator bug (revenue is still summed
     from assessment records regardless of denominator).
  5. **Characterize what ground-acre actually measures.** Does the hood boundary area
     include non-parcel land (roads, alleys, parks, ROW) alongside parcel land? If so,
     quantify the ground-acre vs summed-lot-acre gap on a sample of hoods, so the methods
     note can state precisely what ground-acre includes that lot-acre excludes.
  6. **Correct any "Urban3-standard / gross land area" claim for ground-acre.** Web
     research indicates Urban3 computes value/acre as total *parcel* value ÷ total
     *parcel* area — i.e. their denominator is closer to this project's **lot-acre**, NOT
     a boundary-derived gross area. No evidence Urban3 uses a gross/boundary denominator.
     Fix any doc language implying ground-acre has Urban3 lineage: ground-acre is an
     **independent addition here, justified on cardinality-robustness grounds**, not
     methodological continuity with Urban3.
  7. **Document condo handling as an industry-wide open problem**, not just an internal
     bug: independent Urban3-method replications (e.g. the Bloomington-Normal Strong Towns
     GIS group) reportedly EXCLUDED condo parcels entirely rather than solve the ownership
     complexity. This project's dedupe (if it ships as the fix) is a genuine improvement
     over exclusion — useful methods-note context.
  **Deliverable:** a short written finding per question (with numbers) — likely a FINDINGS
  doc; recommended scope for the single join-integrity fix (WEM + condos); and methods-note
  language distinguishing **lot-acre (Urban3-analogous)** from **ground-acre (this
  project's own robustness-motivated addition)**, incl. what land ground-acre includes
  that lot-acre excludes.


- [x] ~~**Neighbourhood labels — finish + ship**~~ — SHIPPED 2026-07-04
  (PR #11 merged, deployed run `28712502638` — one transient Pages failure,
  fixed by `gh run rerun --failed` — live-verified). Final styling: 15 px /
  weight 800, 128 px SDF atlas (`radius: 24`, `smoothing: 0.08`) for
  city-zoom sharpness; Peter approved on-device. 27 labels at city zoom /
  64 at zoom 12.2. See UI.md "Neighbourhood labels" for the
  CollisionFilterExtension and glyph-scale gotchas.


- [x] ~~**Ghost prisms over a neutral hood plane (Peter, 2026-07-03; design
  clarified 2026-07-04).**~~ **SHIPPED 2026-07-05 — PR #12 merged + deployed**
  (run `28757734787`, green first try; live site serves the Glass view +
  `value_grid.json` with the lot-acre columns, 1.76 MB / 200). Full design
  trail below; the denominator story continues in the lot-size item after it.
  The Urban3-infographic composition: keep the
  extruded prisms but render them **transparent**, over a flat hood plane
  UNDERNEATH that is **one neutral colour — NOT metric-coloured** (Peter:
  "i don't actually want the color on the hood underneath"). The plane is
  mouseover geography, not a signal carrier; ALL metric signal stays in the
  prisms. Exception: **set-aside/holdout hoods get their own distinct colour**
  on the plane. Hover/tooltip lives on the hood plane, like the Uses-view
  pattern (hood layer under a display layer carries picking + highlight).
  DECIDED 2026-07-04: **its own (fifth) view button** — "directly cribbing
  the Urban3 style thing, just with our own interactive flavor" (Peter).
  V1 (hood-prism glass, built + verified on `feature/glass-view`) was then
  refined by Peter: the spikes should be **finer than the hood unit** — the
  Urban3 detail level. DECIDED 2026-07-04 (after the condo lot_size probe —
  see DATA.md §2): **100 m grid cells** (~35k, in Peter's "a tenth of 287k"
  range), height = **revenue in cell ÷ cell GROUND acres** (consistent with
  the hood metric's boundary-acre denominator; no condo/lot_size artifacts).
  Built on `feature/glass-view` (merged in PR #12): pipeline grid export +
  Glass view renders the cells over the neutral hood plane (pure point
  binning, 34,675 cells). Tests + verify-glass.js green; screenshots
  eyeballed.
  - [x] ~~**Confirm the set-aside artifacting is gone (Peter, on-device).**~~
    CONFIRMED 2026-07-05 — Peter eyeballed the local preview (reverted
    point-binned grid + the new denominator toggle): "looks fine". The
    rollback stands; no further diagnosis needed. Original context below.
    Peter saw "really bad artifacting, specifically in areas that are
    actually set asides" (2026-07-04) after the footprint-spreading round.
    DECIDED 2026-07-04: **spreading ROLLED BACK** (`70a5d54` reverted in
    `19c25fb`) rather than diagnosed — back to point binning. The
    artifacting is presumed caused by the spreading (synthetic footprint
    squares up to 1.2 km painting faint cells over river valley /
    set-aside land, plus tens of thousands of sub-1 m cells coplanar with
    the plane); needs Peter's eyeball on the reverted grid to confirm
    before ship.
  - [x] ~~**Large single-point lots needle the grid (known limitation,
    post-rollback).**~~ RESOLVED by the lot-acre denominator toggle
    (shipped in the same PR — see the lot-size item below); the needle
    remains visible in ground-acre mode by design (that metric honestly
    shows dollars-per-map-cell). Original context: One lat/long per
    account means WEM ($1.285B,
    43 ha) is a single $12.6M/acre spike — #1 citywide, 2× the top
    downtown tower; lots > 1 ha are 5,524 rows / ~18% of citywide value.
    **Chosen fix: the PRIORITY lot-size denominator variant below** (per
    parcel acre, the tower correctly beats WEM ~50×). The reverted
    footprint-spreading approach (spread value over a lot-area square
    centred on the point, `git show 70a5d54`) also de-needled WEM but
    caused the set-aside artifacting above; if ever revisited instead,
    fix the spillover first (clip spread cells to the parcel's hood
    polygon, cap the square side, floor displayed $/acre — REPORTED,
    not silent).


- [x] ~~**PRIORITY — Lot-size denominator variant for the grid spikes**~~
  **SHIPPED 2026-07-05 — PR #12** (with the Glass view above; deployed +
  live-verified). (Peter, 2026-07-04; prioritized after the WEM
  verification.) The true Urban3
  metric is revenue per PARCEL acre (`dkk9-cj3x` `lot_size`), not per
  ground acre. **Why it's now priority:** verified 2026-07-04 that the
  ground-acre grid ranks WEM (single account, $1.285B, 107-acre lot, one
  lat/long → one 2.47-acre cell → $12.6M levy/acre needle, #1 citywide)
  2× above the top downtown tower ($620M on 0.93 acres) — but per LOT
  acre the tower beats WEM ~50× ($612M vs $12M value/lot-acre). Point
  binning ÷ fixed cell area rewards "most dollars pinned to one point",
  not land productivity; the lot-acre denominator is the chosen fix
  (preferred over resurrecting the reverted footprint spreading).
  **PIPELINE BUILT + VALIDATED 2026-07-05** (`docs/FINDINGS_lot_dedupe.md`):
  - [x] ~~Dedupe heuristic~~ — REVISED same day after cell-level validation:
    the first-draft distinct-sum collapsed identically-apportioned townhouse
    complexes (KAMEYOSEK 309 units → 0.04 ac → fake $1.2B/lot-acre needles).
    Shipped rule = repeat-aware (`SHARE_MAX_M2 = 1000 m²`): repeated values
    < 1000 m² count per unit (real shares), ≥ 1000 m² count once (duplication
    guard); majority-null multi-unit points ineligible (56 points / $1.23B /
    0.52% of roll, excluded + REPORTED). Threshold insensitive 500–2000 m².
  - [x] ~~Wire into `export_value_grid`~~ — done: `load_property_info.py`
    (new), `account_number` in load_assessment, `*_per_lot_acre` columns in
    `value_grid.json` (1.8 MB, null where no eligible acres),
    `check_lot_acre_bounds` RAISES on new bound violations (PEMBINA the
    committed `KNOWN_BOUND_OUTLIERS`); `--skip-property-info` degrades to
    ground-acre only. 163 tests green (+23).
  - [x] ~~Validation vs ground-acre~~ — done (FINDINGS §6.5): top-10
    lot-acre cells all Downtown CBD; WEM $12.6M → $290k; tower cell #1 at
    $14.8M revenue/lot-acre; p97.5 $105k vs $144k ground.
  - [x] ~~**Frontend: denominator toggle in the Glass view**~~ (Peter,
    2026-07-05: "make it togglable, so i can view both") — built 2026-07-05:
    "Ground acres | Lot acres" in the layers panel (Glass-only; hidden on
    grid files without the lot columns), per-column scale anchors, null-lot
    cells DROPPED in lot mode (28), legend/blurb follow the denominator.
    verify-glass extended (denominator matrix green; lens+uses regressions
    green); shot-denom.js eyeballed — WEM needle collapses in lot mode.
    UI.md synced. Peter's on-device eyeball PASSED 2026-07-05 ("looks
    fine"); PR #12 merged + deployed same day (README view list rode in
    the PR).


- [x] ~~**SCOPE: composition numbers now; full zoning POLYGON layer in the viewer is a
  SEPARATE later product decision**~~ — RESOLVED 2026-07-03: Peter opted in for the
  Uses view (PR #10) — the real bylaw geometry renders there, category-dissolved and
  clipped to the hood setbacks. The metric views (Money/Roads/Ratio) stay
  overlay-free; any zoning overlay ON those views would be a new decision.


- [x] ~~**UI control hierarchy: separate "Color Adjustment" from lens controls.**~~
  **BUILT 2026-07-07** (`web/index.html`, `#coloradj` panel at the top of the right-hand
  stack, above the lens controls; UI.md "Colour Adjustment toggle" bullet is the as-built).
  - [x] ~~sqrt as a runtime toggle~~ — `state.colorAdjust` (default **on**) gates the
    money/glass sqrt in `scaleT`; off = linear+clamp (true magnitude). Legend follows via
    `legendGradient`→`scaleT`; the money/glass blurb colour clause swaps via
    `withColourClause` (honesty). Height stays LINEAR either way. **Scope = `scaleT`
    consumers (money + glass) only** — greys out (disabled) in services/ratio/uses, which
    use their own transforms (`svcT`, `ratioT`).
  - [x] ~~Self-describing state label~~ — `#coloradj-state`: On → "colour spread across
    distribution", Off → "colour shows true magnitude".
  - **Not visually verified in a browser** (no headless browser on the laptop) — awaits
    Peter's on-device eyeball. JS syntax `node --check` green.
  - Deferred follow-on (if Peter wants it): a single GLOBAL "sqrt colour" switch that also
    drives fire's sqrt (services) — currently fire/ratio transforms are independent.


- [x] **Deployment — LIVE (2026-07-01/02)** at
  https://peterfriedrich.github.io/edmonton-tax-viz/ (merged to master, PRs #1–3).
  Scheduled GitHub Action (`.github/workflows/refresh.yml`, weekly Mon 08:00 UTC +
  dispatch) downloads all inputs → `main.py` → `status.json` heartbeat →
  commit-if-changed → deploy Pages. `scripts/download_data.py` (all three inputs),
  `scripts/generate_status.py`, frontend banner, `requirements-ci.txt`. Pages enabled
  `build_type: workflow`; first run + node24-bump run both green in production.
  Decisions settled: rerun+git-diff / weekly / `GITHUB_TOKEN`. See `docs/SPEC_deployment.md`.
  **Deferred follow-ons still open (below).**

## Cache-bust `styles.css` at build time — CLOSED 2026-08-02

Closed by stamping `styles.css?v=<content hash>` in `scripts/build_site.py`.
Full reasoning (why a content hash and not the commit sha, why a query and not
a hashed filename, and the limitation it does NOT cover) is the 2026-08-02 row
in `docs/DECISIONS.md`. Original item as it stood:

- [ ] **PROPOSE: cache-bust `styles.css` at build time.** Peter, 2026-08-01, on a
  phone after a successful deploy: *"i'm still not seeing the mill rates on
  mobile… i can see it when i open it in a private window on my phone. but it's
  refusing to show on normal safari."* The change was live and correct; his
  Safari held the old stylesheet. **This is new since 2026-07-29**, when
  `styles.css` was extracted out of `index.html` — a CSS-only change now ships in
  a separate file with its own cache lifetime, so a stale stylesheet renders
  against a fresh page and the feature looks half-deployed.
  - Both files serve `cache-control: max-age=600` with matching `last-modified`,
    so the intended window is 10 minutes; observed Safari behaviour was longer.
  - **Fix:** inject a version query on the `<link>` in `scripts/build_site.py`
    (content hash or commit sha). ⚠️ **Changes CI behaviour → propose, do not
    smuggle**, and ⚠️ that script's base-tag guard does a plain substring test
    over the whole source, which has already killed one deploy — anything near
    the `<head>` needs the guard re-run. Triage order: `RUNBOOK.md` §3c.
    *(The guard was scoped to the `<head>` slice on 2026-08-04, so the
    whole-source substring test described here no longer exists.)*

## A data-only refresh runs no front-end check — CLOSED 2026-08-02

Closed by `tools/profiling/verify-smoke.js`, gated into `refresh.yml` before
`upload-pages-artifact`. Full reasoning (why the existing suite was refused,
what the falsification and inverse tests found, and the two checks whose scope
is narrower than it looks) is the 2026-08-02 row in `docs/DECISIONS.md`.
⚠️ The item's premise that a refresh 'triggers no deploy' was FALSE — refresh.yml
deploys itself; the gap was an unchecked deploy, not a missing one. Original item:

- [ ] **PROPOSE: a data-only refresh runs no front-end check at all.** The
  narrow symptom is closed (see `## Done`, 2026-08-02) but the structural gap it
  exposed is not. `deploy.yml` is scoped to `web/**` minus `web/data/**`, so a
  refresh that rewrites `web/data/` triggers **no deploy**, and `refresh.yml`
  runs no verify script — a data change can therefore alter what the site
  renders with nothing on fire.
  - ⚠️ **Correcting this item's own former claim:** it used to say the temporal
    file "has no equivalent" of `check_value_anchors.py`. **False** —
    `scripts/check_temporal_years.py` exists, runs in `refresh.yml` before the
    status-manifest step, and **passed on the 2026-08-01 refresh**. The data
    side is guarded. What is unguarded is the *render*.
  - **Open question, not an obvious build:** the verify suite needs a browser
    and ~1 min/script, and the pipeline guards already cover data correctness —
    so a full suite on every refresh may cost more than it catches. A single
    smoke script over the panels that read refreshed data is the cheaper shape.
    ⚠️ **Changes CI behaviour → propose, do not smuggle.**

## `verify-smoke.js` guards the METRICS columns but not the SERVICES ones — CLOSED 2026-08-03

Closed by `verify-smoke.js` `B7`/`B8` **plus** `scripts/check_served_columns.py`
+ `data/expected_columns.json`. Full reasoning is the 2026-08-03 row in
`docs/DECISIONS.md`.

⚠️ **The item's prescribed fix does not catch the failure the item names**, and
that is the whole finding. It asked for *"present on every feature OR absent from
every feature, never partially"* — but a refresh that silently drops a service
column drops it from **all 406** features, which is "absent from every feature",
which that rule tolerates. Falsification F2 confirmed it: with `bike_m_per_acre`
deleted from every feature, B7 passes green. The tolerance is not removable
either — `bike_m_per_acre` was legitimately absent for exactly this reason
between the 2026-08-02 merge and the refresh that followed it, and failing on
absence would have redded the weekly publish over a column that was not supposed
to exist yet. Telling the two apart needs **memory of last week's schema**, which
no check derived from the served file can have; hence the committed baseline.

Two corrections to the item's own text, both found by reading the config:
`SERVICES` is **not** the whole list (Roads is a ground layer with no
`plane.col`, so `road_m_per_acre` appears only in `RATIO_DENOMS`), and the
service columns carry **no nulls at all** — set-aside is its own `is_set_aside`
flag, so the null-vs-undefined care B6 needs does not arise here, though the
check reads `undefined` anyway to keep the two families asking one question.

Original item:

- [ ] **`verify-smoke.js` GUARDS THE METRICS COLUMNS BUT NOT THE SERVICES ONES
  — a dropped service column is invisible by design.** Found 2026-08-02 while
  adding the bike lens. `B6` asserts every `METRICS` column is present on every
  feature, derived from the config; `B4` does the same for `USE_CATEGORIES`.
  **Nothing derives from `SERVICES`**, so the 7 service plane columns
  (`road_m_per_acre`, `bike_m_per_acre`, `transit_dep_per_acre`,
  `storm_charge_per_acre`, `water_charge_per_acre`, `fire_events_per_acre`,
  `svc_cost_per_acre`) are unguarded.
  - ⚠️ **The failure is SILENT BY CONSTRUCTION:** every services row
    self-gates on its own column, so a refresh that silently dropped one would
    simply hide the row. No error, no NaN, no banner — the exact "a dropped
    fact is this project's cardinal failure" case B6 exists for, on a surface
    that just grew from 6 rows to 7.
  - **Fix is cheap and mirrors B6:** derive the required column list from
    `SERVICES`' own `plane.col` values rather than listing them.
  - ⚠️ Must stay tolerant of legitimately-absent columns (an old data file, or
    a lens whose reviewed input has not landed) — the S87 cry-wolf lesson.
    Probably "present on every feature OR absent from every feature", never
    partially.

## Mobile chrome — the bottom-sheet question — CLOSED 2026-08-04 (no code change)

The last open piece of the mobile-chrome quick pass (`docs/MOBILE_USABILITY.md`
§3). Steps 1 and 2 shipped in `0089eba` and Peter confirmed the blurb collapse
on device; step 3 (the left-edge clip) closed 2026-07-31 as not reproducible.
What remained was **a decision, not a build item** — whether the flex control
column is enough on a phone or the controls should move into a bottom sheet /
hamburger.

⚠️ **The item was re-measured before being decided, and the basis had moved.**
The union coverage method reproduced the default state **to the decimal
(27.9%)**, so the deltas below are real movement and not method drift:

| state | recorded 2026-08-01 | measured 2026-08-04 |
|---|---|---|
| default (Money, folded) | 27.9% | **27.9%** ✅ |
| **Money UNFOLDED** | **54.3%** | **47.9%** ⬇ |
| Services unfolded *(full only)* | never measured | **53.1%** |
| Development unfolded | never measured | **52.7%** (public 44.7%) |
| Ratio / Uses unfolded *(full only)* | never measured | 37.4% / 31.6% |
| worst **public** state (Dev unfolded + peek) | never measured | **52.3%** |

⚠️ **THE ">HALF THE SCREEN" CLAIM WAS ATTACHED TO THE WRONG STATE.** The doc
named Money unfolded at 54.3%; it is now **47.9%, under half**, because
`#moneymode` left the Options panel for `#toggle` row 2 on **2026-08-02 — one
day after the measurement was taken**. The states that *are* over half
(Services, Development) had never been measured at all: the 08-01 pass took one
view and generalised from it.

⚠️ **A SECOND STALE LINE, FOUND ON THE WAY.** §3 claimed *"public `#views` is
now 4 buttons"*. It is **two — Money · Development**. Services and Ratio were
pulled to full-only on 2026-07-28 (`|| !FULL_BUILD`, the `applyView`
data-presence gate). This is load-bearing for the decision: **the public build
cannot reach the 53.1% state at all.**

**Peter's call: the column stays as-is.** The reasoning, recorded so it is not
re-opened on the old numbers:
- The >50% states are **transient and user-initiated** — reachable only by
  deliberately unfolding Options, and they fold away again. The **default**
  render, which is what a phone user meets first, is **27.9%** vs desktop's
  20.3% — about 7 points.
- The worst *public* state (52.3%) needs an unfold **and** a neighbourhood tap,
  and the peek card is the answer to that tap. Rendered and eyeballed: nothing
  clips, nothing overlaps, the middle ~40% of the map stays clear.
- A bottom sheet is a refactor of **shared desktop+mobile DOM**
  (`CONTROLS_MATRIX.md`: grouping drives both) — real desktop regression risk
  for a state the user can dismiss.

⚠️ **`#views` POSITION (the "too far from the map" hierarchy question) LOSES ITS
VEHICLE.** It had been parked pending "the move-2 fork", which this refuses. It
now needs its own proposal if it is ever revisited.

**Still genuinely open and NOT closed by this** (own item): the Services panel
grouping has never been touched on a **real phone** — the geometry is measured
clean at 390/360/320, but real-device touch and the **folded default** state are
unconfirmed, and the verify scripts drive `.click()`, which bypasses
`pointer-events`.

⚠️ **Tenth time a carried item's stated basis did not survive re-measurement —
and the first where re-measuring CLOSED the item instead of redirecting it.**

---

## Replace the derived $14.135M roads-maintenance figure — CLOSED 2026-08-04

**Closed by correcting it, not by confirming it.** The item read *"it is the one
soft number in that table; the other three are quoted directly"* and framed the
work as *"a single value swap plus dropping `derived_component`"*. The swap was
indeed a single value — but the figure being replaced was **about 5× too low**,
and it had been **live on a public page since the 2026-08-04 manual refresh**.

### The original figure and why it failed
`$1,285/km × ~11,000 km = $14,135,000`. Two inferences stacked: a narrow unit
rate from Taproot reporting, multiplied across the citywide network, with the
**snow-clearing** network reused as a maintenance denominator. Against the
City's own published program the implied rate is **~$5,900/km**, not $1,285/km.

⚠️ **The error was in the repo's derivation, not in the source.** Taproot's
*totals* hold up; only the rate×network product did not. That distinction is
what the cross-check below establishes, and it matters — the instinct on finding
a bad number is to distrust the source.

### What was found
`https://budget.edmonton.ca/api/operating_budget.csv` — the City's Open Budget
portal, **program-level, machine-readable, FY2017–FY2026**, 7,283 rows. Now
`DATA.md` **§17**. The Approved Operating Budget PDF stops at branch level
(`Parks and Roads Services`, FY2026 gross $303.361M) where roads are bundled
with parks — 6× the whole roads row, and unusable for this.

### The cross-check that exposed it
| | |
|---|---|
| Published `Snow and Ice Control` program, FY2025 | **$67,553,815** |
| Pod's roads snow $36.85M + path snow $30.15M | **$67,000,000** |
| | **99.2%** |

Same source, two numbers: the snow figures reconcile almost exactly, the
maintenance figure was out by 5×. **The asymmetry is the finding.**

### Why FY2017, a stale vintage
**It is the only year Edmonton ever published a roads-only maintenance
program** (`Roadway Maintenance`, **$65,671,000**; alongside `Snow and Ice
Control` $63,709,000 — a 1.03 ratio, where the pod's derived figure implied
0.38× its own snow, **4.9× apart**). The tree was **re-cut in 2018** into
`OPS/PARS - Infrastructure Maintenance`, which also covers sidewalks, pathways
and bridges — using it would **double-count against this table's own sidewalks
and bike-lane rows** — and **re-cut again in 2026** into `Mobility
Infrastructure Services`. Peter's call: **roads-only scope beats matching
vintage, documented rather than silently mixed**, the same call already made for
ETS 2025 vs fire 2026. Being 2017 dollars it is if anything a **lower bound** —
the branch grew ~34% ($244.9M → $327.1M) by 2025.

### Effect
Roads **$50.985M → $102.521M**, i.e. **1.33% → 2.67%** of the operating budget;
transit:roads **9.2× → 4.6×**. `derived_component` dropped, so the pod's public
asterisk is gone. Transit, bike and sidewalk rows unaffected.

⚠️ **Because nothing downstream pins a share, this was a one-value edit** — the
UI divides. That is the second time a number in this table has been corrected
after publication, and the standing argument for the no-pinned-ratios rule.

### Guarding it
`test_committed_budget_file_shares_are_what_we_claim` **failed on the change, as
designed**, and was updated with a warning that moving it is correct only
alongside a sourced value change. A new
`test_committed_budget_roads_maintenance_is_no_longer_derived` pins the value
and the absence of `derived_component` against a revert.

---

## Tighten the cardinality-guard bands — CLOSED 2026-08-05 (four of six)

**The item said "tighten the bands once there is variance data." The variance
data existed, and it said two different things about the six anchors.**

### Where the variance data was
Not in git, and not in the baseline file — **the guard prints every anchor value
in CI on every run**, and those logs are retrievable. Harvested from the
`refresh.yml` runs' job logs.

⚠️ **`gh run view --log` returns nothing even for a COMPLETED run here; the jobs
API works.** Quirk (qqqq) had recorded the in-progress half of this; the
completed half is new:
```bash
JOB=$(gh api repos/PeterFriedrich/edmonton-tax-viz/actions/runs/<id>/jobs -q '.jobs[0].id')
gh api "repos/PeterFriedrich/edmonton-tax-viz/actions/jobs/$JOB/logs"
```

⚠️ **Five runs, but only THREE independent observations.** The 2026-08-02 and
2026-08-05 runs committed `status.json` only, so their anchors re-measure
unchanged input. Checking *what each auto-refresh commit actually touched* is
what separates a real observation from a re-reading.

### What it showed
| anchor | observed spread | action |
|---|---|---|
| `dup_parcel_points` | 0.00% (constant 33) | tightened 2× |
| `lot_needle_ratio` | 0.00% | tightened 2× |
| `dedupe_effect_pct` | 0.01% | tightened 2× |
| `dup_parcel_value_frac` | 0.11% | tightened 2× |
| `ineligible_points` | 7.1% | ⚠️ **left wide** |
| `ineligible_value_frac` | 22.3% | ⚠️ **left wide** |

**The last two are not noisy — they are trending**, monotonically upward on
every independent data change, with no reversal:
```
ineligible_points      56 -> 58 -> 60
ineligible_value_frac  0.00517 -> 0.00575 -> 0.00633
```
That is the **dangerous** direction by the guard's own `DANGER` map. Tightening
them to observed spread would have red the weekly publish on the next real data
change and read as a false alarm rather than the regime signal the guard exists
to give. `ineligible_value_frac` has consumed ~72% of its band already.

### Two things the item got wrong
1. **Its prescribed mechanism cannot express the result.**
   `--write-baseline --tolerance` applies ONE global tolerance to every anchor.
   The bands are now hand-set per anchor — which needs **no code change**, since
   the comparator reads `min`/`max` per key and ignores `_`-prefixed notes — and
   that flag would silently flatten them back. Recorded in the baseline's own
   `_bands_are_per_anchor` field and pinned by a test.
2. **"Observed spread" is the wrong target anyway.** The guard exists mainly for
   the **January year-roll**, and **no observation across a year-roll exists** —
   it shipped 2026-07-28. Three weekly readings say nothing about reassessment,
   so ±25% buys a real 2× tightening while leaving room for the event the guard
   was built for. Going tighter is a decision for after the first January roll.

### Guarding it
Three tests, none of which existed before (nothing pinned the committed baseline
at all): every CI reading must stay in band; the drifting pair must stay wide;
the four tightened anchors must stay at ±25%. ⚠️ **The tightening test was
falsified against the old baseline first** — it fails there and passes here, so
it pins the change rather than merely describing it.

## Finish the doc-citation sweep: `src/`, `scripts/`, `tools/` — CLOSED 2026-08-09 (S103)

Opened 2026-08-08 by S102, which swept only `web/index.html` (40 sites, 14 docs)
and found a **wrong number live on the site**. The other three trees cite docs
too and had never been checked. Closed by sweeping them: **216 citation sites
across 51 files**, triaged to the ~20 that back a falsifiable number or a data
contract — the rest are bare "see `SPEC_x.md`" pointers with nothing to be wrong
about.

**Method (the part worth reusing):** every numeric claim re-derived from
`data/raw/` rather than compared against the doc text — point-in-polygon for the
containment counts, a chunked scan of the 363 MB fire feed, feature counts on
the road/bike GeoJSONs, groupby on the historical aggregate. Then
`git log -S '<figure>'` **paired with** `git show <commit>:data/DATA.md` to
separate a citation that *drifted* from one that was *never right* — S102 used
only the first half, and only the pairing distinguishes the two.

**Three defects, all comment-level; nothing wrong reached shipped data.**

1. ⚠️ **A line-number citation drifted.** `tools/audit_exempt_institutional.py`
   cited the institutional zone codes as *"DATA.md line ~308"*. `git show` at the
   authoring commit proves it was **right on 2026-07-09**; DATA.md has grown
   ~240 lines since, so line 308 now lands on `Total Gross Area`/FAR. Re-pointed
   at **§5 "Set-aside categories"**. The project already bans line-number
   citations for `CODEMAP.md`; this was the same failure one file over.
2. **A unit mislabel.** `src/load_temporal.py` justified `COMMERCIAL_CLASSES`
   with *"NONRES MUNICIPAL/RES EDUCATION is 19 rows across all 14 years"*. **19
   is the account count; rows are 16.** The locked decision is unaffected (still
   noise on single accounts) but the stated evidence was not what it claimed.
3. ⚠️ **S102's own follow-up note was FALSE and is retracted.** It recorded that
   `web/index.html` self-flags `SPEC_temporal.md` §2 as stale and *"the doc was
   never updated"*. `git log -S` shows §2's **READ FIRST banner and that very
   comment landed in the same commit, `7e065ef`** — the doc was updated the day
   the comment was written. The comment was **obsolete on arrival**, pointing
   readers at a §2 that already opens with the correction. Rewritten to send
   them to the banner.

**One imprecision, stage now stated.** `load_temporal.py`'s *"32 historical names
have no current boundary"* reproduces **only** at the shared-`NAME_CORRECTIONS`
stage while counting the `""` null bucket (3 null rows) as a name: 31 + 1. Raw
is **41**; after both correction layers, **25**. The nulls are *not* a silent
drop — `normalize_hood` does `fillna("")`, so they survive into the denominator
and get reported, which is what trap 2 requires.

**Verified correct and left alone** (re-derived, not compared): roads **53,720**
and bike **10,417** features (exact); fire noise `TRAINING/MAINTENANCE`
**18,144** / `COMMUNITY EVENT` **2,491** / `PRE-INCIDENT PLANNING` **515**
(exact); `ZONE_CATEGORY` **95** base codes; `gross_area` null/zero **6.19%**
(DATA.md's own 27,202 / ~6.2% exact); the historical aggregate at **14,842**
rows with the class dimension costing **9,265** ("~14,800" / "~9,300"); spatial
containment **945/946** and **100/103** (exact); **0** null coordinates in the
current roll; permit geocoding **94.8–98.0%** for 2009–2023 and **71.6%** for
2025; OLIVER's straggler at exactly **1 row / $500**; the census anchor
**459,859**; and every DATA.md section number cited (§2/§5/§10/§11/§13/§14/§15)
plus `SPEC_temporal` §0.1–§0.4.

**Two left deliberately unchanged.** `SPUR LINES` is a second unmatched name
($0, 1 row), so `load_assessment.py`'s *"the lone remaining unmatched name"* is
**correct only in scope** — the zero-value drop runs first, so SPUR LINES never
reaches that join — and it is documented in three places; the two texts
reconcile only if you know the ordering. And `load_stormwater.py`'s **$49.8M**
unbilled is a difference the cited doc never states (§3 gives $240.4M and
$190.5M, rounded difference **$49.9M**) — within rounding of the unrounded
inputs, but a derived figure with no source.

**Successor:** the `docs/` tree itself is still unswept, and docs cite each
other constantly. See `## Open work`.

## The Services lens has no hood panel — BUILT 2026-08-10

Closed 2026-08-10. The panel confronts revenue per acre with each service
cost, grouped by basis, with **no total** — forced by the two no-sum rules
(`DECISIONS.md` 2026-08-10, `docs/SPEC_services.md` "Hood panel").
`verify-peek.js`'s Services block was rewritten: the invariant is "a tap
produces a readout", not "a tap opens the card".

- [x] **The Services lens has no hood panel — build the service-specific one.**
  Opened 2026-08-06. Clicking a hood in Services now does nothing by design
  (`hoodPanelLens()`; `DECISIONS.md` 2026-08-06): the assessment-history panel
  was the wrong content there, so it was gated out, and Peter's stated intent is
  *"we'll probably have something service specific"*. Until that exists the lens
  is hover/card-only, which is a **complete** readout — this is a feature gap,
  not a defect, and nothing is currently broken by leaving it.
  - **What the panel would hold (undecided — this is the actual open question,
    not the plumbing):** the per-service rows already exist in the tooltip, so a
    panel that only repeats them earns nothing. The candidate that would justify
    it is the **cost-vs-revenue confrontation** the Ratio view gestures at —
    this hood's modelled service cost per acre beside its revenue per acre — but
    ⚠️ the cost terms carry incompatible bases (`DATA.md` §13: `roadway_om_renewal`
    lifecycle vs `roadway_ops` operating, ~10.8× apart, never to be summed or
    compared), so any such panel needs its basis named on screen or it becomes
    a headline number that is arithmetically true and descriptively false.
  - **The plumbing is already in place and is the cheap half:** flip
    `hoodPanelLens()` for services, give `#temporal` a third render mode beside
    `renderHistory` / `renderRevenueMix`, and point `#peek-go` / `#temporal-hint`
    at it — all three advertisements already follow the lens.
  - ⚠️ **Re-read the `verify-peek.js` Services block before touching any of
    this.** It encodes a regression that reached production (the card is the
    ONLY per-hood readout on touch); the checks there are what stop it
    recurring, and they must keep passing in whatever the panel becomes.

---

## `gross_area` null-vs-zero in `far` — CLOSED 2026-08-22

- [ ] **⚠️ `gross_area` MISSING AND `gross_area` ZERO ARE THE SAME NUMBER IN THE
  GRID PATH — a cell with no data emits `far = 0`, which reads as maximum infill
  opportunity.** Measured 2026-08-22: the field is null/zero on **6.25% of
  eligible rows**, `build_hood_lot_acres` / `_cell_lot_metrics` sum it with
  `NaN → 0`, and at 100 m grain **16.2% of cells land on `far == 0` with 100% of
  their own properties missing the field** (median). 3,964 in-scale cells tie at
  the identical maximum opportunity score.
  - **The fix:** emit `null` where no property in the unit has a usable
    `gross_area`, the way `median_year_built` already does for year (*"age has no
    meaningful zero"* — same argument, same file).
  - ⚠️ **The SHIPPED hood lens is NOT wrong today** — reproduce before "fixing"
    the live output. 69 in-scale hoods exceed 50% missing but **only 2 are
    residential**, so the asymmetric residential gate bars the rest from the teal
    end anyway. The defect is real; its blast radius at hood grain is 2 hoods,
    both with 3–4 eligible rows.
  - ⚠️ **The gate absorbing a DATA gap is undocumented behaviour** — `SPEC_development.md`
    Lens B justifies it purely as a land-use filter. Worth stating there, because
    it is precisely what the gate cannot do per-cell.
  - Prerequisite for any cell-grain FAR. Full measurements:
    `docs/FINDINGS_infill_granularity.md`; open work:
    `docs/ANALYSIS_BACKLOG.md` §12.

**Outcome:** fixed in `build_hood_lot_acres` (null and zero both masked, `min_count=1`), +3 tests. 16 of 410 hoods go null; 12 were already set-aside grey. EVERGREEN leaves the Infill scale and `SPEC_development.md` Lens B was amended — its teal was never a measurement. ⚠️ **PARTIAL coverage is still open** (MAPLE RIDGE, ~33% recorded, #2 on the teal arm): `docs/ANALYSIS_BACKLOG.md` §12. Full reasoning: `docs/DECISIONS.md` 2026-08-22, `docs/FINDINGS_infill_granularity.md` §6a.

---

- [ ] **Wire `check_temporal_archive_year.py` into the monthly vintage digest.**
  Unblocked 2026-08-27 — it exits 0 now, so gating no longer means holding the
  site over an open decision. `vintage-digest.yml` already holds `issues: write`
  and already opens `⚠️`-titled issues, and `DECISIONS.md` 2026-08-26 named it
  the honest home for a guard that cannot gate a publish but must not go quiet.
  ⚠️ **CI change → propose the plan first** (`CLAUDE.md` Comments & Scope).
  Rejected once already: warn-only inside a green run, which reaches nobody.

**Outcome (2026-08-27, PR #258):** wired, and **no CI change was needed** — the digest already runs `vintage_report.py` and already folds ⚠️ into the issue title, so it is a check function plus a `CHECKS` entry (membership IS the wiring, and a test pins it). Reuses `filed_bases()`/`detect_year()`/`archived_residential_bases()` so the digest and the standalone guard cannot disagree. Reads only committed files, so it cannot fail on the network. Two deliberate reporting choices: a year outside `fir_tax_base.json` is named NOT CHECKED and never counted as passing, and a green over ONE archived year carries its own thin-population caveat. ⚠️ **A false alarm was found in the same file and fixed**: `check_assessment_roll` compared the coverage string to our pin itself, bypassing `check_alignment()`'s 2026-08-25 stale-metadata downgrade, and would have reported "Roll has moved to 2025, pin is still 2026" every month starting 2026-09-01 — recorded as issue 1's THIRD consequence (`docs/DATA_ISSUES.md`, PR #259).

---

- [x] **CLOSED 2026-08-30 — the 15 hardcoded activity-window labels now read from
  one constant, and drift fails the build.** Audit F4, opened 2026-08-28.

  Original item:
  - `FIRE_YEARS` / `PERMIT_YEARS` / `PERMIT_YEARS_RECENT` are restated as
    literals across 15 user-facing sites in `web/index.html` (`DEV_WINDOW_LABEL`
    alone feeds 5 render sites). **All correct today** — only because the
    project is younger than one year-roll.
  - Step 4 bumps the pins and re-runs the deflator, and says the drift guard
    means a stale pin "can't be missed silently". **True of the pin, false of
    all 15 strings.**
  - ⚠️ **This is the `(2024 n/a)` defect (S122) at 15×**, with the same tell:
    correctly-derived copy sits beside it (the vintage footer reads
    `status.json`).
  - **Not a one-line fix:** `status.json` carries no activity window, so the
    browser cannot derive these. Closing it means `generate_status.py`
    publishing the three windows — an **output-schema change**, propose-first.
    ⚠️ **Do not ship the cheap partial alone** (a RUNBOOK line + a test pinning
    label against pin) without deciding: a half-fix that makes step 4 *look*
    complete is its own hazard.

**Outcome:** closed the other way round from what the item proposed. The
`status.json` route was **rejected on measurement, not cost** — the manifest is
fetched async and lands after first render (`web/index.html`, the STATUS_URL
fetch), so every label would still need a literal fallback and the fix would
have created **two** sources of truth rather than removing one.

Shipped instead: a single `WINDOWS` block in the tunables, `${WIN.<key>}` at
every JS site and `{{<key>}}` placeholders in the seven static tooltips,
substituted at parse time. `tests/test_window_labels.py` (4 tests) asserts
`WINDOWS` equals `main.py`'s pins, that both change windows end at
`ASSESSMENT_YEAR`, that no user-facing string spells a range out, and that every
placeholder names a real key. RUNBOOK §1 step 4 now names the second edit.

⚠️ **Scope grew by one lens on Peter's call**: `CHG_WINDOW_LABEL` /
`CHG_WINDOWS` (2012–2026 / 2019–2026) carry the same defect on a different pin
and were folded in. Their ends stay PINNED rather than read off `temporal.json`
— the 2026-08-27 phantom-year decision — and the comment saying so was kept and
amended rather than deleted.

⚠️ **The four remaining literals in the file are comments**, one describing an
unrelated ASTER window that happens to share a range; the guard strips comments
for that reason. The other three were reworded to stop restating years.

Verified: mutation (a stale pin and a reintroduced literal each fail the guard),
760 tests, and the live page — all six ranges render byte-identical to before,
no unsubstituted token, no page error. Full reasoning: `docs/DECISIONS.md`
2026-08-30.

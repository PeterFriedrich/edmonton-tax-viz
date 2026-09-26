# FINDINGS — public blurb claims (ledger item 12)

**Run:** 2026-09-26, S199, Opus 5.5, `high`. **Target:** every number and
factual claim in the public `#title-p` blurbs after the #559–#571 rewrite
(COPY_DECISIONS BD1/BC1/BM1/BG1/BS1/BR1). `verify-blurbs.js` checks shape,
length and wiring, never truth; this run checks truth.

**Instrument.** `node tools/profiling/verify-blurbs.js "<url>?build=public" --dump
out.json` gives all 150 public states; they reduce to **77 distinct
paragraphs**. Each claim was checked against served data (`web/data/*`), the
code path that renders the state, and where the served files can't answer,
the raw inputs (`data/raw/*`, vintage 2026-09-03; the served dev coverage
ties to it within 15 units). Served root confirmed by md5 of `index.html`.
To re-run: dump, split on paragraphs, and walk §3's table.

## 1. Verdict

**Every stated NUMBER is correct.** Two blurbs describe the wrong quantity
on subset cuts (F1, F2, one root cause), and four explanatory clauses are
wrong or half-wrong (F3–F6). Nothing blocks: no published figure is
miscomputed; the defects are what the words say the figures mean.

Decision stack, top-down:

| level | question | verdict |
|---|---|---|
| L0 | Should blurbs carry figures and claims at all? | SOUND. Decided (B5/B8), and the live counts are read from data, not typed |
| L1 | Does each blurb describe the quantity its state renders? | **CONDITIONAL.** Holds on the Total cut and every non-Money view. Fails on the Residential and Non-residential cuts, where the institutional note and the non-res P1 describe the total levy's composition (F1, F2) |
| L2 | Is every number right? | **SOUND.** 23 numbers checked, all tie (§3) |
| L3 | Are the causal and descriptive clauses true? | **CONDITIONAL.** F3–F6 |
| L4 | Can a guard catch this class? | `verify-blurbs.js` cannot by design. F1 is guardable: the stated azure count must equal the flagged cells with a nonzero value on the active column |

Sharpest argument against L1's verdict: the 2026-08-19 decision chose to
draw the Glass band on *all* revenue cuts ("Revenue cuts only, same rule as
the hood caveat"), so F1 is a decided design. Answer: the decision settled
*whether* the band draws on subset cuts. It never addressed that
`exempt_frac` is a share of the **total** levy, and the count sentence that
now states it (BG1, 2026-09-24) postdates it. What would change this: a
DECISIONS row that weighs the total-vs-class share. None exists (`grep
exempt_frac docs/DECISIONS.md`).

## 2. Findings

### F1 — MEDIUM · Glass azure count on the Residential cut counts cells with no residential tax
The Residential grid blurb says **"1,332 azure cells are mostly institutional
land … only the solid part is certain."** 1,064 of those 1,332 have **$0
residential city tax**. They draw as flat azure squares on the ground (the
U of A campus in the screenshot, `resazure-res_revenue_per_acre.png`,
scratch). 268 carry any residential tax. At 50 m: 1,816 stated, **144**
nonzero. Lot acres: 1,324 → 267, and 1,803 → 143.

Cause: `glassInstCells()` filters `c[col] != null` (0 passes) and gates on
`exempt_frac`, which `export_value_grid.py:328` computes as
`exempt_levy / levy`, the **total** levy. The same share then sets the
"certain" base height as `value × (1 − exempt_frac)` on every cut. By roll
zoning, 94% of exempt-candidate assessed value is Non-residential class, so on
the Residential cut the share is mostly about dollars that are not on screen.

Same root, not in a blurb (side): Money's hood band (`instBandedMoney`),
Money's tooltip caveat and Ratio's tooltip all read `rev_frac_exempt`, the
total share. On the Residential cut, 4 of the 21 flagged hoods have **under 0.5%**
residential levy (EDMONTON NORTHLANDS, RIVER VALLEY CAMERON, RIVER VALLEY
GOLD BAR, YELLOWHEAD CORRIDOR WEST), yet the tooltip says "97% of revenue is
on institutionally-zoned land".

### F2 — MEDIUM · "what commercial and industrial property pays" includes schools, parks and institutions, uncaveated on that cut
Non-residential P1: **"what commercial and industrial property pays the City."**
The non-res-rate levy includes every Non-residential-class parcel on
exempt-candidate zoning (AJ/UF/UI/PU/**PS**): universities, hospitals,
utilities, and, in residential neighbourhoods, school and park sites zoned
`PS`.
- **Citywide**, by roll zoning: **9%** of non-residential assessed value.
  The pipeline's served shares imply up to 17%, under the assumption that all
  exempt-candidate levy is non-res class. That assumption breaks for EVERGREEN
  (41% exempt-candidate, 88% residential class), so treat 9–17% as the range.
- **Per hood**, by roll zoning: in **112** non-set-aside hoods, ≥25% of the
  non-res figure sits on exempt-candidate zoning. In **63** hoods it is ≥50%.
  Examples: TWEDDLE PLACE 99%, OXFORD 99%, CHAMBERY 96%, ASPEN GARDENS 91%
  (all of it `PS`). The pipeline-implied share agrees for 7 of the 8 checked;
  ALCES disagrees (17% vs 85%), because spatial and roll zoning differ.
- **None of those 112 gets a band or a tooltip caveat on this cut**, because
  every gate reads the total share. ASPEN GARDENS' 9% of total levy is under
  0.25, even though that 9% is its entire non-res figure. Verified by reading
  the gates, not by absence: `instBandedMoney` (≈l.3073) and the tooltip row
  (≈l.6245) both test `exemptFrac(p) >= EXEMPT_UNCERTAIN_MIN`.

Magnitude is low in dollars: these hoods' non-res figures are small. But the
sqrt ramp exists "to show the low end", so the colour a residential hood gets
on this cut is set mostly by its school sites.

### F3 — LOW · Lot-acre P1: "so parks, river valley and big lots don't dilute it"
- **Big lots** are *in* the lot-acre denominator. A neighbourhood of big lots
  reads *lower* per lot acre, not unaffected, so the clause is backwards.
- **Parks** on the roll are counted. Parcels zoned `A`/`PS`/`PSN`/`NA` are
  **7.2%** of lot acres in non-set-aside hoods: median hood 6.5%, EVERGREEN
  65%, CLOVERDALE 58% (raw, pre-dedupe).

What the lot denominator actually drops is unparcelled land: roads, and
unparcelled valley and water. The clause was inherited from the pre-rewrite
text ("large-lot land stop diluting the figure").

### F4 — LOW-MEDIUM · Development grid: "(the newest permits lag geocoding)" is half-wrong on Since 2009 · units
On the default Development state (units, since 2009, grid) the blurb says
~16% of homes aren't on the grid "yet" because of lag.
- **13,557 of the 26,286 off-grid units (52%)** come from 2009–2020 permits,
  5–16 years old: a permanent gap, not a lag.
- They are big multi-unit permits: 7.3 units per missing permit vs 1.75 per
  geocoded one. Apartment units 2009–20 are 77% geocoded, other types 91%.
- By neighbourhood, of 2009–20 units: DOWNTOWN 47% off-grid, ERMINESKIN 57%,
  AMBLESIDE 28%.
  The long grid under-places older *dense* growth.

The clause holds elsewhere. For 3yr and 5yr units, 92% and 85% of the gap is
2024–25. For permits since 2009 it is 67%.

The docs carry the root error. DATA.md and SPEC_development say "2009–2023
sit at 95–98% geocoded", which is true **by permit count**. By units those
years run 80–93%. (Corrected in this PR.)

### F5 — LOW · Development P2: "so a few dense-infill areas don't wash out the rest"
The neighbourhoods at the top of the scale are **greenfield subdivisions**,
not infill:
- units since 2009: CRYSTALLINA NERA WEST, CALLAGHAN, ALLARD, PAISLEY,
  SECORD, WALKER;
- permits since 2009: CY BECKER, PAISLEY, LAUREL, SECORD, MCCONACHIE.

Only 3yr and 5yr have infill near the top (GARNEAU, SHERWOOD). The clause
also contradicts the blurb's own P3 ("greenfield … is where much new building
lands").

### F6 — LOW · two wording claims
- **Value P1, "What the land is worth":** assessed value is land **plus
  buildings**. For a value-per-acre map, "land value" is a term of art that
  means something else.
- **Roads P2:** it names only "Arterials show neutral grey". Set-aside
  neighbourhoods also render grey on that state (`servicePlaneLayer`), and
  the blurb doesn't say so. Every other Services state says "Grey = set-aside
  land".

## 3. Claims that check out

| claim | evidence |
|---|---|
| 1,332 / 1,816 / 1,324 / 1,803 azure cells (**Total cut**) | recomputed from `value_grid*.json`, ≥0.25; 93% / 98% of flagged cells are ≥50% exempt-candidate, so "mostly" holds |
| 16 hoods, "a quarter or more", Ratio | `EXEMPT_UNCERTAIN_MIN = 0.25`, live count, matches DECISIONS 2026-09-12 |
| ~30/21/16% of homes, ~31/19/8% of permits off-grid | `dev_grid.json` coverage: 29.9 / 21.4 / 16.2, 30.7 / 18.8 / 8.4 |
| "they still count in the neighbourhood view" | hood sums within 0.35% of coverage totals; the rest is the 565 decided-unmatched multi-hood units |
| "one permit per building" | semi-detached 2.17 units/permit, row 4.8–5.2, single 1.06 |
| $5,970 per lane-km (2017 budget), $3,350 snow | `city_unit_costs.json` `roadway_ops`; unit is lane-km (S149); `check_cost_copy.py` ties the text |
| $50/m = ($600,000 + $1,900,000) / km over 50 years | (0.6M + 1.9M) / 50 / 1000 = 50 |
| windows 2012–2026, 2019–2026, 2023–25, 2021–25, 2009–25 | `temporal.json` years; `WINDOWS` pins |
| colour sqrt / linear / log per view | `METRICS[*].transform`, `devT`, `scaleT`, ratio log path, `withColourClause` |
| Grey = set-aside (Money ground), + thin lot (Money lot), + thin road (Ratio) | all 48 set-aside hoods carry values and are greyed by `fillFor`; the one non-set-aside null lot is MAPLE RIDGE |
| Change "Grey = no {y0} value" | 45 of 46 grey hoods; the 46th is MILL WOODS GOLF COURSE (no endpoint) |
| Change "the tallest are small new subdivisions" | long: top 12 all new subdivisions. Short: 8 of 12 (the exceptions are HERITAGE VALLEY AREA, WHITEMUD CREEK RAVINE NORTH, EDMONTON NORTHLANDS and MARQUIS at 2,485 acres) |
| Residential = "houses, condos and apartment buildings" | RESIDENTIAL + OTHER RESIDENTIAL, DECISIONS 2026-07-16 |
| Roads "city-maintained collector and local" | `load_roads.py` Road + City of Edmonton + `METRIC_GROUPS` |

**Not re-opened:** "pay the City" on a modelled levy is N5 (applied
2026-09-18), with the exemption doubt carried by the azure bands (DECISIONS
2026-08-12). F2 is about *which* hoods get that doubt on a subset cut, not
the noun.

## 4. Remedies (none applied — copy is Peter's call, F1/F2 touch a data contract)

- **F1/F2 (one fix):** gate and scale the band per cut on that cut's own
  exempt share. That needs class-split exempt levy from the pipeline
  (`exempt_res_levy` / `exempt_nonres_levy` or per-cut `exempt_frac_*`), which
  is a **data-contract change, so propose first**. Interim, copy only: drop the
  azure count on subset cuts, or count only nonzero cells. The guard: the
  stated count must equal the flagged cells with `c[col] > 0`.
- **F2 copy:** "what non-residential property pays: shops, offices,
  industry, and institutions such as schools and hospitals" (≤400 still fits).
- **F3:** "…divided by the parcel land they own, so roads and unparcelled
  river valley don't dilute it."
- **F4:** say "(most are recent permits not yet geocoded; some older apartment
  permits never were)", or make P3 read the per-year split.
- **F5:** "so a few fast-growing areas don't wash out the rest."
- **F6:** Value → "What the property is worth, not what it pays"; Roads →
  add "Grey neighbourhoods = set-aside land."

## 5. What this run got wrong

- **My first hypothesis for "1,332" was a double count** (two azure layers per
  cell). The count is per cell. The real defect was on a different axis: the
  count is right on Total and wrong on the subset cuts.
- **F2's first number (150 hoods) was an upper bound presented to myself as a
  count.** It assumed all exempt-candidate levy is non-res class. The
  tooltip's own comment (EVERGREEN 89% residential and 41% institutional)
  refutes that assumption for at least one hood. The class-aware roll-zoning
  count (112) is the headline. The two instruments also disagree on ALCES by
  5×, so per-hood F2 figures are ±, not exact.
- **F2's citywide share spans 9–17%** across the two instruments, and I have
  not reconciled why (spatial 2024-bylaw zoning vs the roll's `zoning` field
  is the likely split).
- **F3, F4 and the F2 roll figures come from `data/raw` of 2026-09-03**, not
  the served week. F4 ties to served coverage within 15 units. F3's park
  share has no served-data check.
- **F1's screenshot** was taken under SwiftShader. Flat azure squares
  rendering at z=0 is confirmed there, not on a GPU.
- **Same-model check.** Opus 5.5 wrote these blurbs and graded them here. A
  cross-model read of F2 and F4 before acting is warranted.

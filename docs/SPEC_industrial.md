# Scope: Industrial & non-residential lens family (Track A) + regional non-residential context (Track B)

**Status:** SPEC'd 2026-07-18. **A1 + A3 BUILT same day** (A1: `nonres_levy` →
fourth Money metric + Glass grid columns; A3: `ind_permits_per_acre` → third
`#devmetric` "Industrial" choropleth — TODO.md has both as-built summaries);
the rest is PLAN. This doc specs
the non-residential side of the fiscal picture: where the commercial/industrial
tax base sits, how much industrial land is shovel-ready, where non-residential
construction is actually happening, and — Track B — how Edmonton's
non-residential assessment base and tax rates compare across the metro region.

**Policy anchor (citable, public):** the City's **Industrial Investment Action
Plan** (IIAP — originated 2016, updated 2024 and March 2025) treats
non-residential assessment-base growth as an active fiscal-sustainability
concern, and a potential incentive-fund item is slated for consideration in the
**2027–2030 budget cycle**. The lenses here are descriptive context for that
public policy conversation — they show what the assessment, land-supply, and
permit records say, nothing more.

**⚠ Tone rule (stricter here than elsewhere).** Cross-municipality
competitiveness comparison is the most advocacy-adjacent territory in the
project. Every lens and every line of copy stays **descriptive and
non-editorializing** — state what the data shows, cite the source, no
"Edmonton should…" framing, no characterizing any party's position. If a copy
draft reads like a case *for* something, rewrite it as a description *of*
something.

| | Item | Answers | Scope frame | Phase |
|---|---|---|---|---|
| **A1** | Non-residential $ cut | where the non-res tax base is, per acre | existing hood/grid | 1 (greenlit) |
| **A3** | Industrial permit velocity | where industrial construction is happening | existing hood frame | 1 (greenlit) |
| **A2** | Shovel-ready industrial land | how much vacant serviced industrial land, where | existing hood frame + points | 2 |
| **A4** | Assessment-lag methods note | permit → full assessed value lag (3–5 yr) | methods note, not a lens | 2 |
| **B2** | Regional non-res mill rates | rate levels across the metro region, multi-year | citywide aggregates | 3 |
| **B1** | Regional non-res assessment share | Edmonton's share of regional non-res base over time | citywide aggregates | 3 |
| **B3** | Industrial-areas context map | where the region's industrial land sits | illustrative map | 4 |

Build order: A1 → A3 → A2 → B2 → B1 → B3. One PR per coherent piece. A4 rides
along as a methods note whenever its source lands.

---

## Why

Every Money metric today either aggregates all classes or cuts out the
*residential* side (`res_levy`, shipped 2026-07-16). The non-residential base —
the ~59% of levy dollars that isn't residential — has no lens of its own,
even though it is the side the City's own IIAP identifies as the
fiscal-sustainability question. Track A decomposes what we already hold. Track
B adds the regional context that citywide-only data can support: assessment
share and rate levels across neighbouring municipalities, from provincial
sources that are class-complete and licensing-clean — precisely the "coarser
but class-complete alternative" the parked per-parcel regional lens left open
(`docs/SPIKE_regional_lens.md`).

**Relation to the PARKED regional lens (important):** Track B uses **zero St.
Albert per-parcel data and zero Strathcona parcel data**. Its sources are
Alberta Municipal Affairs publications (OGL-Alberta). The park and its un-park
conditions (St. Albert licensing, Strathcona dedup) are untouched and still
stand.

---

## Track A — inside the existing parcel/neighbourhood frame

### A1 — Non-residential $ cut (greenlit)

The exact complement of the shipped residential decomposition, and near-free:
the levy machinery already computes per-class slices
(`docs/FINDINGS_assessment_classes.md` unified formula).

- **`nonres_levy`** = the slices billed at the **Non Residential** rate class:
  `COMMERCIAL` + `MA DERELICT RESIDENTIAL` (the city deliberately bills
  derelict at the non-res rate — mirror of its exclusion from `res_levy`,
  DECISIONS 2026-07-16) + `DESIGNATED IND PROPERTIES` (as built: the set is
  derived from the label→rate-class map, `NONRES_RATE_LABELS`, so a future
  non-res label can't be missed; the exempt label carries no rate and
  contributes $0 regardless). **Farmland excluded** (own rate class, 509
  parcels, immaterial — real-data residual ~$532K of a $2.704B levy).
- **Testable identity:** `levy == res_levy + nonres_levy + farmland_levy`
  (whole-$ tolerance) — decomposition sums to total by construction.
- **Columns:** `nonres_revenue_per_acre` / `nonres_revenue_per_lot_acre`
  (hood) + the two Glass-grid cell columns (pattern proven 4×: value, revenue,
  res, age). Real zero vs null conventions mirror `res_levy` exactly (a cell
  with property but no non-res levy reads a real $0).
- **Display:** fourth Money metric ("Non-res $") mirroring Residential $ —
  same denominator toggle, same runtime p97.5 clamp, same Glass cells.
- **Grid file size:** +2 rounded ints × ~34.7k cells ≈ +0.17 MB raw (Pages
  gzips; precedent weighed and accepted twice already).

**⚠ Roll nuance — there is NO industrial-vs-commercial split in the
assessment roll.** `Tax Class` = "Non Residential" and `Assessment Class 1` =
"COMMERCIAL" both cover *all* non-res (DATA.md §2). An *industrial-specific*
dollar cut would need a zoning-layer join (industrial zones), with the
zoning≠assessment-class caveat attached. That is a possible later refinement,
**not** part of A1 — A1 is the honest class-complete non-res cut.

### A3 — Industrial permit velocity — BUILT 2026-07-18

**As built** (`feat/ind-permit-velocity`): `INDUSTRIAL_BUILDING_TYPES` in
`load_permits` (400-series, full-string) → `ind_permits` count →
`ind_permits_per_acre` (+ `_3yr`) in `SLIM_COLUMNS`. Third `#devmetric` option
**"Industrial"** — a Development-view choropleth (not an Infill activity:
entering Infill resets the metric to a residential column and hides the
button). Column-guarded (`state.hasIndPermits`). Real data: 283 permits / 117
hoods (5yr), top hoods = the industrial areas. Display open-decision resolved
to the recommendation below (Peter, 2026-07-18). `verify-ind-permits.js` ALL
PASS. Original spec kept below.

**Amended 2026-08-18 — the metric gained a 100 m detail grid, and it is
measured in DOLLARS.** The Detail toggle no longer hides while Industrial is
up. Three things were measured before building, and each changed the design:

- ⚠️ **Permit COUNT does not form a surface at 100 m.** 89% of 5yr industrial
  cells hold exactly one permit (81% on the long window); the tallest holds
  ten. A count-driven grid is a dot map wearing a density map's clothes.
- ⚠️ **Enlarging the cell does NOT fix it.** 100 m → 400 m is a **16× area
  increase that removes 19 of 184 cells** and drops singletons from 89% to
  78%; even 800 m leaves 145 cells and 75% singletons. Industrial permits are
  not clustered at the sub-kilometre scale, so merging cells merges nothing.
  The $ spread is near-invariant to cell size (281× at 100 m, 292× at 400 m),
  confirming the differentiation comes from permit SIZE, not clustering. The
  100 m cell is kept — it preserves the shared geometry with the Glass grid.
- **`construction_value` is what carries the pattern** — 172 distinct heights
  across 184 5yr cells (723 of 835 on the long window), max/median 164×. The
  reservation on this column (below, "Numerator") is therefore LIFTED for the
  grid; the choropleth stays permit count per acre.

⚠️ **What the dollars ARE.** The dataset documents `CONSTRUCTION_VALUE` as
*"Estimated value of construction work"* — a **declared estimate at permit
application**. Not audited spend, never reconciled; the permit fee is derived
from it (an incentive to declare low); land is excluded. 78% of values end in
`000` and 26% in `00000`, which is the signature of round-number estimating.
It is a **scale-of-development proxy**, not investment, and the blurb says so.

⚠️ **They are deflated, and they had to be.** Nominal sums encode
construction-cost inflation as development. Two independent measurements
agree: StatCan BCPI (Edmonton, industrial buildings) puts 2009→2025 at
**1.72×** and 2021→2025 at 1.33×; the permits' own warehouse $/sqft says 1.92×
over the same span. Values are expressed in **constant 2025 dollars** via
`scripts/fetch_construction_price_index.py` →
`data/construction_price_index.json` (a manual reviewed input, mill-rates
pattern — NOT on the weekly refresh). A permit year with no deflator
**hard-fails**; it never passes through at nominal.

⚠️ **The live StatCan table is 18-10-0289.** Its two predecessors are
**ARCHIVED** — 18-10-0135 stops at 2022-Q2, 18-10-0276 at 2024-Q2 — and both
still download and still answer queries. A stale pin fails **silently**, which
is why the fetcher checks `archiveStatusEn` and warns.

⚠️ **A $0-declared permit would vanish.** 12 of 1,281 industrial permits are
declared at exactly $0 (118 at ≤$10k). On a dollar-driven height that is a
permitted building simply not on the map. Cells are therefore kept on the
permit COUNT (`ind_n`), not the dollars, and a **6 m display floor** keeps
every cell visible. The floor is small on purpose: dwelling units are
QUANTISED (a permit adds ≥1, so 0% of residential cells render under 5 m)
while dollars are CONTINUOUS to zero (39–44% of industrial cells do). An
earlier 60 m floor lifted cells worth up to **$4.6M** to the same height as
$0, erasing the very differentiation the dollars provide.

**Consequence for a locked decision, NOT resolved here:** `DECISIONS.md`
2026-07-23 made Industrial `/full/`-only *because* it was choropleth-only and
would "leave the new 3-way Detail selector with dead options". That rationale
no longer holds — Industrial is now grid-capable. Whether it becomes public is
Peter's call; nothing was changed.

A filter on data already in the pipeline (General Building Permits
`24uj-dj8v`, DATA.md §10). `building_type` carries a coded taxonomy (live
counts 2026-07-18): **400-series = industrial** — `Animal and Plant Services
(410)` 166, `Manufacturing Buildings (430)` 468, `Transportation Terminals
(440)` 159, `Storage Buildings, Warehouses (460)` 4,849, `Utility Buildings
(480)` 344, `Engineering (490)` 277. 500-series = commercial (Retail 510,
Office 520, Hotels 530, …), 600-series = institutional.

- **Enumerate by full string, not code** — codes duplicate across unrelated
  types (`Parkade (490)` vs `Engineering (490)`; `Mixed Use (522)` vs `Office
  Complex (522)`). Hand-enumerated dict + warn-on-unseen, the exact
  `load_permits.py` idiom.
- **Numerator:** permit **count** (`ind_permits_per_acre`). `units_added` is
  meaningless for industrial; `construction_value` is available and is the
  natural intensity measure but stays **reserved** for now (consistent with
  the Lens C reservation, SPEC_development) — revisit if count alone reads
  flat. ⚠️ **RESOLVED 2026-08-18: it did read flat, on the 100 m grid.** The
  reservation is lifted for the DETAIL GRID only (deflated dollars); the
  choropleth is still permit count per acre. See the amendment above.
  `floor_area` was considered as the intensity measure instead and **rejected
  on coverage**: it is populated on only **51%** of industrial new-construction
  permits (vs 99% residential), where `construction_value` is on 99.6%.
- **Window:** the pinned Lens A windows (5yr base + 3yr recent), same
  `work_type` new-construction set.
- **Display (open decision, recommendation below):** the Development view is
  currently *residential* new construction, and the Infill z-score reads its
  activity metric — industrial must not silently pollute that. Recommended:
  third option in the existing `#devmetric` picker (Units | Permits |
  Industrial), with the Infill view gated to the residential metrics.
  Alternative: keep the column pipeline-only until a better surface exists.
  **Peter's pick at build time.**

### A2 — Shovel-ready industrial land (phase 2)

**Dataset verified live 2026-07-18:** `stt5-pzaa` "Vacant Land - Industrial"
(data.edmonton.ca, Socrata). **Annual snapshots 2016–2023**, ~480 parcels/yr,
3,631 rows total; dataset last updated 2025-02-19 (no 2024 vintage as open
data yet). Extracted from the City's Tax Assessment Control System per the
dataset description. Fields: `year`, `address`, `area_ha`, `size_category`,
`zoning` (old-bylaw codes — all vintages predate Zoning Bylaw 20001),
`neighbourhood_number`/`neighbourhood_name` (industrial-area naming — join
compatibility unverified; **prefer lat/long point-in-hood join**, the dev-grid
geocode idiom), `ward`, `district`, **`servicing`** (the serviced/unserviced
status), `ownership_type`, `latitude`/`longitude`/`geometry_point` (centroids).

- Being a time series, **absorption is computable directly from snapshot
  diffs** (parcels leaving the vacant inventory year-over-year) — better than
  the annual report's tables, and reproducible.
- The City's annual "Industrial Land Supply and Absorption" report (2022,
  2023, 2024 editions confirmed to exist) is the corroboration source; the
  2023+ editions are aligned to Bylaw 20001. Report PDFs live on edmonton.ca
  (**laptop-gated from the Oracle box**).
- Display: undecided (point layer per vintage? hood rollup of vacant serviced
  acres? supply time series needs a chart surface that doesn't exist — same
  INTERACTION PREREQ as the debt lens). Data layer can be built and committed
  ahead of display.

### A4 — Assessment-lag methods note (phase 2, source fetch = Peter)

A **November 29, 2024 council memo** on the IIAP carries an attachment
(Table 1: Change in Industrial Assessment by Year) built to analyze the lag
between permit issuance and full assessed value being realized (**typically
3–5 years**). Pull the attachment rather than re-deriving the lag. It is a
methods-note input (caveat language for A3/B1: recent permits haven't reached
the assessment base yet), not a lens. edmonton.ca is laptop-gated from the
Oracle box — fetching the PDF is Peter's action; test reachability before
assuming.

---

## Track B — citywide-aggregate regional context

**Scope lock: citywide aggregates only.** No cross-municipal per-parcel data
of any kind (see the park note above). All Track B sources are Alberta
Municipal Affairs publications under **OGL-Alberta**.

**Source-category note (resolved 2026-07-18):** AMA/open.alberta.ca is
**already an established project source** — `scripts/fetch_fir_debt.py`
(debt-lens D5, 2026-07-14) pulls the same FIR workbooks (2003–2025, every
municipality, manual-reviewed-input pattern, anchor cross-checks, DATA.md
§11). Track B extends that fetch idiom to more schedules and more
municipalities; it is not a new source category. Older zips exist back to
**1994** if the historical series wants pre-2003 depth.

### B2 — Regional non-residential mill rate comparison (phase 3)

- **Source verified live 2026-07-18:** the FIR dataset page carries
  `2026_Tax_Rates.xlsx` directly (one file, every municipality), plus the
  yearly financial workbooks for history.
- **Municipalities:** Edmonton, Strathcona County, Sturgeon County, Parkland
  County, City of Leduc, Leduc County — extend the `MUNICIPALITIES`
  stable-code dict pattern from `fetch_fir_debt.py`.
- Replaces the secondary-source snapshot numbers currently in hand with a
  proper multi-year primary series. Output: reviewed JSON
  (mill-rates/fir_debt pattern), display later.
- **Comparability caveats carry into copy:** rate-bundling differs across
  municipalities (requisitions, special levies — see the SPIKE doc's
  Strathcona notes); municipal-only vs total-bill must be stated explicitly.

### B1 — Regional non-residential assessment share over time (phase 3)

Two provincial sources, used together:

1. **FIR/SIR yearly workbooks** (established fetch) — assessment and tax
   fields per municipality-year. Raw FIR values are **not
   revaluation-adjusted**, so cross-municipality *level* comparison from raw
   FIR alone is invalid; within-year shares are usable with care.
2. **Equalized assessment report — XLSX, not PDF** (verified 2026-07-18):
   `open.alberta.ca/dataset/equalized-assessment-report`, **2024/2025/2026
   workbooks, OGL-Alberta**. Equalization adjusts every municipality to a
   common valuation basis — the valid instrument for cross-municipality
   comparison. **Older years:** check whether equalized assessment appears in
   the FIR/SIR workbooks themselves or in older report editions
   (possibly PDF) — exhaust the machine-readable path before any PDF
   extraction.

**Discrepancy to resolve from primary data:** a 2016 city report cited
Edmonton's regional non-residential assessment share falling **76% → 72%**
over the prior 15 years; a late-2024 industry publication cited a decline
from a "record high" **72% in 2008-09 to 60% in 2022**. The two published
series don't obviously reconcile (different denominators? different
equalization vintages? different class definitions?). Rebuild the share
series from the primary FIR/equalized data and state what it actually shows —
do not cite either secondary figure as fact. (→ also listed in
`docs/ANALYSIS_BACKLOG.md`.)

### B3 — Industrial-areas context map (phase 4)

Illustrative only: existing Designated Industrial Areas / zoning layers plus a
municipal-boundary layer (Alberta municipal boundaries are published
provincially — source + licence to verify at build time), styled to show where
the region's industrial land sits (Refinery Row is in Strathcona County
immediately east of the city boundary — a descriptive geographic fact dating
to the late-1940s refinery siting). No metric, no per-parcel data.

---

## Open decisions (Peter)

1. ~~**A3 display**~~ — RESOLVED 2026-07-18: third `#devmetric` option,
   choropleth only, Infill gated to residential (the recommendation, built).
2. **A2 display** — point layer / hood rollup / table; and whether the supply
   *time series* waits for a chart surface.
3. **B display** — all Track B outputs are charts/tables, and no non-map
   surface exists yet (same prerequisite as debt-lens D5-chart). Data layers
   proceed regardless.
4. **A1 industrial-specific refinement** — whether a zoning-join industrial $
   cut is ever wanted on top of the class-complete non-res cut.

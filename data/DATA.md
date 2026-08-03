# Data Sources

Reference for raw input files. Update this file when you discover column name quirks, encoding issues, or anything unexpected. Do not rely on memory — write it down here.

**Socrata download completeness (applies to every source below):** Socrata
truncates silently at `$limit` — it returns exactly that many rows with no
error. Historically SODA 2.0 also imposed a **server-side 50,000-row cap** on
`$limit`; Edmonton's endpoints demonstrably don't today (the road network
returned 53,720 features in one request, 2026-07-01), but a platform cap could
(re)appear without touching our config. `scripts/download_data.py` therefore
verifies every download two ways: post-download count vs. **our** declared
`$limit` (fails at count >= limit), and vs. the **live server count** via
`$select=count(*)` (mismatch fails hard; an unreachable count endpoint only
warns — the guard must not add fragility). Verified against all four sources
2026-07-01.

---

## 0. Property Assessment Data (Historical) — CATALOGUED 2026-07-28, NOT YET USED

**Not in `download_data.py` and not in `data/raw/`.** Catalogued because the
shape was measured live and it unblocks the per-neighbourhood assessment-over-
time graph (`TODO.md`). Numbers below are from the API on 2026-07-28.

> ### 🛑 THE RECENT SLICES ARE INCOMPLETE — DO NOT USE 2024/2025 AS-IS
>
> **Proven 2026-07-28 against the current roll (§1), same assessment year:**
>
> | Downtown, assessment year 2025 | accounts | value |
> |---|---|---|
> | **`q7d6-ambg` current roll (what we ship)** | **11,216** | **$7.81B** |
> | `qi6a-xuwt` historical, 2025 slice | 10,307 | $7.09B |
> | **missing from historical** | **909** | **~$720M** |
>
> Two entire ICE District towers are absent from the historical dataset's 2024
> **and** 2025 slices while present in the current roll:
> **10310 102 STREET NW** (Stantec Tower — 309 accounts / $144.5M in the 2023
> historical slice, **gone** in 2024–25, but **310 accounts / $105.7M in the
> current roll**) and **10360 102 STREET NW** (261 accounts / $206.0M → gone →
> **261 / $202.1M in the current roll**). Buildings that appear in 2023, vanish
> in 2024–25, and reappear in the current roll were not demolished.
>
> **SCOPE — CITYWIDE, measured account-by-account 2026-07-28.** An earlier
> "~8,000 accounts citywide" figure was **inferred from row counts and was
> misleading** — most of that gap is new construction, not defect. The honest
> decomposition of the 7,929-account net gap:
>
> | | accounts | what it is |
> |---|---|---|
> | in current roll, **absent from historical 2025, and not in 2023 either** | 8,171 | almost certainly new titles/construction — a snapshot-vintage difference, benign |
> | in historical 2025 but not the current roll | ~2,690 | demolitions/consolidations between snapshots, benign |
> | **in historical 2023 AND in the current roll, but ABSENT from historical 2025** | **2,448** | **the genuine defect — a property that existed then and exists now cannot legitimately be missing in between** |
>
> **The 2,448 carry $2.93B of current assessed value and span 188
> neighbourhoods** — so this is citywide, not a Downtown curiosity, though
> Downtown holds **1,292 of them (53%)**. Next worst: MAGRATH HEIGHTS 430,
> GLENORA 269, WÎHKWÊNTÔWIN 124. By class: 2,056 residential, 373 commercial.
>
> **They cluster at individual multi-unit addresses — whole buildings vanish
> together**, and not only downtown towers: 10310 102 ST NW (310), 10360 102 ST
> NW (261), **7463 MAY COMMON NW (162, Magrath Heights)**, 10155 116 ST NW (123,
> Wîhkwêntôwin), 14105 WEST BLOCK DRIVE NW (60, Glenora). *Stated as a symptom
> only — the cause is not ours to diagnose.*
>
> **Practical effect per hood:** Magrath Heights is missing 17% of its accounts
> and Glenora 15%, so the 2025 slice is unusable at hood level well beyond
> Downtown.
>
> **Mechanism of the disappearance, measured:** 1,359 Downtown accounts present
> in the 2023 slice are absent from the 2024 slice. Traced individually across
> the whole 2024 roll — **1,358 of 1,359 do not exist anywhere in it**; exactly
> one moved (to OLIVER). They did not change neighbourhood, were not recoded into
> another hood, and only 2 reappear in 2025.
>
> **EXTENT — MAPPED 2026-07-28** (`tools/audit_historical_roll_gaps.py`, all 14
> years): **the defect is confined to 2024–2025.** 2013–2023 show 0–14 defect
> accounts per year against rolls of 346k–426k (0.00%); 2024 shows **2,322** and
> 2025 a further **131** incremental, ~2,448 cumulative. **One event, two
> slices** — not systemic decay. So **2012–2023 are usable**, 2025 is repairable
> by splicing the current roll, and **2024 is the only irreparable year**.
>
> ⚠️ **The obvious detector does not work here.** "Present in N−1 and N+1, absent
> from N" is blind to a dropout that never returns — it reported **5** for 2024
> where the truth is 2,321. Any check of this dataset must also test against the
> **current roll**, which is independent and complete.
>
> **Before ANY series ships:** validate each historical year against a control,
> and treat recent years as suspect until they reconcile with the current roll.
> Same guard idiom as `check_year_alignment.py` / `check_value_anchors.py`.
> **Splice: historical for 2012–2023, the current roll for the live year.**
> **2024 has no such fix** — there is no current-roll equivalent for it.
>
> ✅ **BOTH ARE BUILT (2026-07-28):** the splice is `src/load_temporal.py` and the
> guard is `scripts/check_temporal_years.py` (wired into `refresh.yml` before the
> status-manifest step). **This dataset is no longer "not yet used" — but note
> what IS used: `scripts/download_data.py --only assessment_historical` fetches a
> ~14,800-row SERVER-SIDE AGGREGATE** (`$group` by year × hood × mill class) into
> `data/raw/assessment_historical_by_hood.csv`, never the 5.5M raw rows.
>
> ⚠️ **The generic truncation check does not apply to an aggregate.** A `$group`
> download's row count is the number of GROUPS, so it can never equal the
> dataset's `count(*)`. The source declares `sum_column: n_accounts` instead and
> `download_data.verify_download` checks that the per-group counts **sum** to the
> live row count (5,501,958 as of 2026-07-28) — strictly stronger, since it also
> catches a whole group vanishing.
>
> ⚠️ **2025 IS ONLY REPAIRABLE WHILE IT IS THE LIVE YEAR.** The current roll
> covers exactly one year. When the roll advances to 2026, 2025 loses its only
> complete source and **drops out of the published series** — `publishable_years`
> handles this, and the guard fails if it is ever republished from the historical
> file. Preserving 2025's repaired numbers past that point needs an archived
> artifact that does not exist yet (`TODO.md`).
>
> **Do not silently smooth this.** A 909-account hole in the headline
> neighbourhood produced an apparent $2.07B collapse where the real decline is
> $1.35B — see `docs/ANALYSIS_BACKLOG.md`.

**Source:** Edmonton Open Data — dataset ID `qi6a-xuwt` ("Property Assessment
Data (Historical)")
**Coverage:** **14 years, 2012–2025**, 5,501,958 rows total (337k in 2012 rising
to 432k in 2025 — the roll grows with the city).
**Columns:** same shape as the current roll (§1) — `account_number`,
`assessment_year`, `neighbourhood_name`, `assessed_value`, `mill_class_1`,
`tax_class_pct_1`, `lot_size`, `zoning`, `year_built`, `latitude`/`longitude`,
`point_location`.

**⚠️ Do NOT download this whole dataset — aggregate server-side.** It carries
`neighbourhood_name`, so Socrata can do the grouping:

```
https://data.edmonton.ca/resource/qi6a-xuwt.json
  ?$select=neighbourhood_name,assessment_year,sum(assessed_value) as total,count(1) as n
  &$group=neighbourhood_name,assessment_year
  &$limit=50000
```

**Measured:** 5,577 rows / **443 neighbourhoods** in **~3 s, 534 kB** of verbose
JSON. Re-shaped as array-of-arrays that is well under 100 kB before gzip.
Note `$limit=50000` is required — the default page size is 1,000, and 443×14
would silently truncate. (See §head for the historical 50,000-row server cap.)

**Known quirks:**
- **443 hoods here vs the current roll's count** — expect names that have since
  been renamed, merged, or annexed. Any join to the neighbourhood boundary file
  MUST go through the same normalization + `check_unmatched_names.py` policy as
  everything else; no silent drops.
- Some rows carry a null/blank `neighbourhood_name` (filtered in the count
  above) — they are not free to ignore, they need the same explicit flagging.
- **`mill_class_1` alone does not reconstruct revenue** — the current pipeline
  uses the full class/percentage split. Historical *rates* live in `pwis-wc4c`
  (§"Property and Education Tax Rates"), which starts **2014**, so a revenue
  series cannot reach back to 2012 even though value does.

---

## 1. Property Assessment Data

**File:** `data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv` *(filename as delivered by the API)*
**Download:** `scripts/download_data.py`
**Source:** [Edmonton Open Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg) — dataset ID `q7d6-ambg`
**API URL:** `https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD`
**Format:** CSV, 439,769 rows. **Live feed, updated weekly** (Socrata
`Update Frequency: Weekly`); the assessment *year* rolls annually.
**Assessment year:** **2025** — i.e. effective 2025-01-01 to 2025-12-31. The year
is **not a column in the rows**; it lives only in the dataset metadata
(`https://data.edmonton.ca/api/views/q7d6-ambg.json` → description /
`custom_fields.Time Frame.Period of Coverage`). Our local snapshot was downloaded
2026-05-16 and is 2025 data. **Re-check the metadata after any re-download** — a
later pull can roll to a new year, which would silently desync from any
year-matched mill rates (see `docs/SPEC_revenue.md`). **This re-check is now
automated in CI** (`scripts/check_year_alignment.py`, added 2026-07-01): every
scheduled refresh compares the metadata year against the pinned
`ASSESSMENT_YEAR` and holds (skip regen + banner) on mismatch.
**Re-download 2026-07-02** (deployment dry-run + first CI run): metadata still
effective **2025** (intra-year edits only, no year roll), so 2025 rates stay
aligned. That pull also surfaced a new `Assessment Class 1` label
`DESIGNATED IND PROPERTIES` (1 row) — mapped to Non Residential; see
`docs/FINDINGS_assessment_classes.md`.
**Licence:** Open Government Licence – City of Edmonton

### Columns (confirmed 2026-05-22)

| Column | Type | Notes |
|--------|------|-------|
| `Account Number` | int64 | Unique property identifier |
| `Suite` | float64 | Mixed types — use `low_memory=False` on load |
| `House Number` | int64 | |
| `Street Name` | str | |
| `Neighbourhood ID` | int64 | Numeric neighbourhood key |
| `Neighbourhood` | str | Normalize (strip + uppercase) for joining |
| `Ward` | str | |
| `Assessed Value` | int64 | Main metric — 46 zero-value rows, 0 nulls (confirmed) |
| `Tax Class` | str | Values: Residential, Non Residential, Other Residential, Farmland |
| `Garage` | str | |
| `Assessment Class 1` | str | See values below — no explicit "exempt" flag |
| `Assessment Class 2` | float64 | |
| `Assessment Class 3` | float64 | |
| `Assessment Class % 1` | int64 | |
| `Assessment Class % 2` | float64 | |
| `Assessment Class % 3` | float64 | |
| `Latitude` | float64 | |
| `Longitude` | float64 | |
| `Point Location` | str | |

**Assessment Class 1 values:** RESIDENTIAL (411,563), COMMERCIAL (23,054), OTHER RESIDENTIAL (4,356), FARMLAND (509), MA DERELICT RESIDENTIAL (284), NONRES MUNICIPAL/RES EDUCATION (3)

**Tax-exempt flag:** No explicit exempt boolean. Best proxy is `Assessment Class 1 == 'NONRES MUNICIPAL/RES EDUCATION'` (3 rows). Flag these on load as `is_exempt`. **Note (2026-06-29):** this proxy catches almost nothing — tax-exempt institutional land (Legislature, schools, hospitals, City property) is **absent from the taxable roll entirely**, not flagged or zeroed. So `is_exempt` cannot identify exempt-heavy neighbourhoods, and revenue/acre silently understates any neighbourhood holding large exempt institutions. See `docs/FINDINGS_revenue_scale.md` §4–5.

### Known Quirks

- Condo units: multiple rows share one land parcel — this is expected and correct for this analysis
- `Suite` column has mixed types — always load with `low_memory=False`
- 46 rows have `Assessed Value == 0` — drop and flag count on load
- No explicit tax-exempt column; proxy is `Assessment Class 1 == 'NONRES MUNICIPAL/RES EDUCATION'` — but exempt institutional land is absent from the roll, so the proxy is near-empty (3 rows). The near-zero-revenue tail is **low-coverage** land (river valley / undeveloped), not exempt. See `docs/FINDINGS_revenue_scale.md`.
- Assessment year is metadata-only, not in the rows (year = 2025; see Format note above) — pin it against the mill-rate year for the revenue phase

---

## 2. Property Info Dataset (Lot Size, Zoning, Year Built)

**Source:** Edmonton Open Data — dataset ID `dkk9-cj3x` ("Property Info - Current Calendar Year")
**API URL:** `https://data.edmonton.ca/resource/dkk9-cj3x.json`
**Format:** SODA JSON API (no bulk CSV download confirmed; query via API)
**Rows:** 439,769 (confirmed 2026-05-27 — closely matches assessment CSV row count)
**Licence:** Open Government Licence – City of Edmonton

**Reference implementation:** `scripts/edmonton_property_api_stuff.py` — Python equivalents of the JS query functions from the open-property app (github.com/[author]/open-property), reverse-engineered to understand how lot_size is sourced.

### Columns (confirmed 2026-05-27)

| Column | Type | Notes |
|--------|------|-------|
| `account_number` | str | Join key to assessment dataset (`q7d6-ambg`) |
| `house_number` | str | |
| `street_name` | str | |
| `legal_description` | str | |
| `zoning` | str | e.g. `RSF` — nullable |
| `lot_size` | str (numeric) | Pre-computed by city; **not geometry-derived**. Units: sq metres (confirmed — sample value 335 m² is a typical residential lot). 2,728 nulls (~0.6%). |
| `total_gross_area` | str | Building floor area |
| `year_built` | str | Nullable. **Loaded since 2026-07-17** (Development stock-age spikes): 418,368 of 439,685 rows (95.2%), range 1881–2026, zero non-numeric junk; every row with a year also has coordinates. Loader nulls values outside [1850, 2100] (plausibility window, `load_property_info.YEAR_BUILT_MIN/MAX`). |
| `garage` | str | |
| `neighbourhood_id` | str | Numeric key |
| `neighbourhood` | str | ALL CAPS — consistent with assessment data |
| `ward` | str | |
| `latitude` | str | |
| `longitude` | str | |
| `point_location` | GeoJSON Point | Single coordinate per property — **no parcel polygon** |

### Key Findings

- **`lot_size` is a city-provided field, not computed** — Edmonton supplies it directly via the API. No geometry math needed.
- **No parcel polygon geometry** — only a centroid point. Edmonton transferred parcel GIS data to AltaLIS in 2021; it's no longer freely available. Polygon boundaries require the neighbourhood boundary file (dataset `65fr-66s6`).
- **`lot_size` units are sq metres** — divide by 4046.86 to get acres. (~0.6% null — minor, flag on load)
- **`Total Gross Area` units are sq metres too** (confirmed 2026-07-07: the
  RESIDENTIAL-class median is 112.7 — a ~1,200 sq ft house). The water lens
  (`src/load_water.py`) uses it to estimate multi-res unit counts (90 m²
  gross/unit assumption); 1,018 of 4,353 OTHER RESIDENTIAL rows have
  null/zero values — those buildings drop from the water model, counted.
- **`Total Gross Area` is now loaded by `load_property_info` (as `gross_area`)
  for the Development Lens B FAR** (2026-07-13) — the built floor-area ratio
  suitability proxy: `far` = Σ `gross_area` (per unit, over eligible points) ÷
  deduped lot area per hood, computed in `build_hood_lot_acres` on the same
  dedupe as the lot-acre denominator. 27,202 rows (~6.2%) have null/zero
  `gross_area` (flagged on load); all 406 hoods still get a `far`. Sanity: FAR
  ranges DOWNTOWN 3.37 / WÎHKWÊNTÔWIN 1.89 / GARNEAU 1.53 (densest) down to ≈0
  at River Valley / Anthony Henday greenfield edges. Low FAR = underused. Ships
  in the neighbourhood geojson (`far`, SLIM). See `docs/SPEC_development.md`
  Lens B for the proxy decision + the low-FAR park/greenfield caveat.
- **Condo `lot_size` semantics are INCONSISTENT (confirmed 2026-07-04)** — at the
  3,002 lat/long points holding multiple units, `lot_size` is sometimes the parcel
  size duplicated on every unit (summing overcounts the land), sometimes per-unit
  apportioned shares (summing is correct), and sometimes null/zero (one 1,059-unit
  building has nulls on 1,051 of them). No flag distinguishes the regimes. This is
  why the Glass view's grid export divides by cell GROUND acres, not lot acres
  (`src/export_value_grid.py`). **Dedupe heuristic built + validated
  2026-07-05** — repeat-aware: repeated values < 1000 m² are per-unit shares
  (count each; a plain distinct-sum collapses townhouse complexes and fakes
  needles), ≥ 1000 m² are duplicated parcels (count once); majority-null
  multi-unit points ineligible (56 points / 0.52% of roll, reported); per-hood
  bound test passes 405/406 (PEMBINA the known outlier, enforced by
  `check_lot_acre_bounds`). Full numbers: `docs/FINDINGS_lot_dedupe.md`.
- **One lat/long per account concentrates large parcels onto a single point
  (quantified 2026-07-04)** — the coordinate is a centroid regardless of lot
  size, so any point-binned density map needles big lots: West Edmonton Mall
  is one account ($1.285B assessed, 433,592 m² lot) behind one point — in the
  100 m Glass grid that's the #1 cell citywide at $12.6M levy/acre, 2× the top
  downtown tower ($620M on 3,754 m²), even though per LOT acre the tower beats
  WEM ~50× ($612M vs $12M value/lot-acre). Citywide, lots > 1 ha are 5,524
  rows carrying ~18% of the $237.5B roll. The lot-acre denominator variant
  (TODO.md, PRIORITY) is the chosen correction.
- **Downloaded via `scripts/download_data.py --only property_info`** (added
  2026-07-04): full-CSV export endpoint, server count(*) cross-check; lands at
  `data/raw/Property_Info__Current_Calendar_Year_.csv`. Join to the assessment
  roll on `Account Number`: 100% coverage (439,685 rows both sides, 2026-07-04).
- **`zoning` column probed 2026-07-05 (for the stormwater lens,
  `docs/SPEC_utilities.md`):** null on 157,030 rows (35.71%); 78 distinct base
  codes (first token) among the rest, and they are **current Bylaw 20001
  vocabulary** (RS 146,567 / RSF 98,606 dominant — no legacy RF1-style codes in
  the top ranks). 98.2% of non-null rows use base codes that appear directly in
  EPCOR's runoff-coefficient table; the remainder are special-area codes (GLDF,
  PLD, SLD, BRH, …) needing explicit hand assignments. 282,655 rows (64.3%)
  have both non-null `zoning` and positive `lot_size`. Zone-null fallback:
  point-in-polygon against `fixa-tstc` (§5). Follow-ups from the build run:
  - The null `zoning` rows are almost all condo units at points where another
    row carries the zone: per POINT, only 4,509 of 287,163 lack any zone, and
    the `fixa-tstc` fallback resolves 4,508 of those (1 unresolved citywide).
  - **Three legacy old-bylaw codes linger** (1 point each): `US`, `CSC`, `RSL`
    — Bylaw 12800 vocabulary that never appears in `fixa-tstc`. Excluded +
    reported by `load_stormwater` (`ZONE_RUNOFF` covers current codes only).
  - **`Neighbourhood` contains two non-boundary names:** the known `OLIVER`
    straggler (1 row, zero lot) and `SPUR LINES` (1 row, 62.5 ha of IM-zoned
    rail-spur land, no boundary polygon) — both dropped + flagged at the
    stormwater join, immaterial by count.

### Architecture Decision — Phase 1

For Phase 1 (neighbourhood-level choropleth), two approaches are viable:

| Approach | How | Tradeoff |
|----------|-----|----------|
| **A — Boundary join** | Sum `assessed_value` by neighbourhood → join to boundary polygons → divide by polygon area | Requires `load_boundaries.py` + area calc; clean for mapping |
| **B — Parcel lot_size** | Join `dkk9-cj3x` to `q7d6-ambg` on `account_number` → sum `assessed_value` / sum `lot_size` by neighbourhood | Bypasses boundary file; condo duplication needs investigation first |

**Current plan: Approach A** (boundary join) — boundary file already downloaded, simpler data flow, no condo ambiguity. Revisit Approach B for Phase 2 if parcel-level detail is needed.

---

## 3. Neighbourhood Boundaries

**File:** `data/raw/neighbourhoods.geojson`
**Source:** [Edmonton Open Data](https://data.edmonton.ca/resource/65fr-66s6.geojson) — dataset ID `65fr-66s6` ("City of Edmonton Neighbourhoods")
**Download URL:** `https://data.edmonton.ca/resource/65fr-66s6.geojson?$limit=50000`
**Download:** `scripts/download_data.py` (fetches this alongside assessment + zoning; uses `$limit=500`, which covers all 407)
**Format:** GeoJSON, 2.9 MB
**Features:** 407 neighbourhoods
**Geometry type:** MultiPolygon (all features)
**CRS:** EPSG:4326 (WGS84) — reproject to EPSG:3400 before area calculation
**Licence:** Open Government Licence – City of Edmonton

### Columns (confirmed 2026-05-27)

| Column | Type | Notes |
|--------|------|-------|
| `neighbourhood_number` | str | Numeric neighbourhood key |
| `name` | str | ALL CAPS — use as `neighbourhood_name` join key |
| `descriptive_name` | str | Human-readable name (may differ from `name`) |
| `civic_ward_name` | str | Ward name |
| `district` | str | District name |
| `effective_start_date` | str | |
| `effective_end_date` | str | |
| `description` | str | |
| `geometry` | MultiPolygon | Boundary polygon |

### Known Quirks

- `name` is already ALL CAPS — matches our `neighbourhood_name` normalization convention
- 407 boundary features. Join outcome (after the 2026-07-01 audit corrections): 1 assessment neighbourhood with no boundary match (the immaterial `OLIVER` straggler, $500 — deliberately unmapped) and 1 boundary neighbourhood with no assessment data (`LEWIS FARMS`) → 406 of 407 boundaries rendered. See "Name Matching" below; flagged in `join_and_calculate.py`.

---

## 4. Property and Education Tax Rates (revenue phase)

**File:** `data/mill_rates.json` *(curated extract — see provenance inside)*
**Source:** [Edmonton Open Data](https://data.edmonton.ca/resource/pwis-wc4c.json) — dataset ID `pwis-wc4c` ("Property and Education Tax Rates (2014 onward)")
**Format:** Socrata JSON/SODA API (live; updated annually — 2026 rates already present, last update 2026-04-29)
**Units:** amount per **$1,000** of assessed value (mills); also published per-dollar
**Licence:** Open Government Licence – City of Edmonton

Columns: `tax_year`, `tax_rate_type` (Municipal / Education / Education Requisition Allowance), `assessment_class`, `amount_per_1_000_of_assessed_value`, `amount_per_dollar_of_assessed_value`.

**2025 Municipal rates (per $1,000)** — the year matching our assessment snapshot:

| Tax Class | Municipal mill rate |
|-----------|---------------------|
| Residential | 7.6254 |
| Other Residential | 8.3116 |
| Non Residential | 24.2229 |
| Farmland | 7.6254 *(assumed = Residential — see quirks)* |

Non-residential is ~3.2× residential — this class differential is the basis of the revenue phase (`docs/SPEC_revenue.md`).

### Known Quirks

- **Join on assessment `Tax Class`** (clean 4-value field). Rate-table class names use spaces (`Non Residential`); some historical years use a hyphenated `Non-Residential` — normalize on load.
- **No 2025 Farmland rate published.** The source dropped a separate Farmland class in 2025. Municipal Farmland == Municipal Residential in every year 2014–2024, so `mill_rates.json` sets 2025 Farmland municipal = Residential (7.6254) as a **flagged assumption**, not authoritative. Low impact (509 farmland parcels).
  - ⚠️ **That assumption is now ON SCREEN** (2026-08-01): the mill-rate pod prints "Farmland rate assumed" beside the rates. It is driven by the **`_assumed` key in this file**, which `generate_status.py` turns into a list in `status.json` — so **adding a real 2025+ Farmland row with no `_assumed` key silently and correctly retires the caveat**. Do not delete the key to "clean up"; deleting it claims the rate was published.
- ⚠️ **This file now feeds the FRONT END, not just the pipeline** (2026-08-01). `generate_status.py` copies the current year's municipal rates into `web/data/status.json` as `municipal_rates`, which the mill-rate pod renders. Rates are never typed into `web/index.html`. Consequence for the January roll: adding a year here is still the single edit, but the committed `status.json` only picks it up when the refresh runs — `tests/test_generate_status.py` asserts the committed manifest matches what the generator would write, so a drift fails the suite rather than shipping stale rates.
- Rate-type label changed over time: older years (2014–2018) use `Municipal Tax Rate` / `Education Tax Rate`; 2019+ use `Municipal` / `Education`. Only 2019+ form is needed for 2025.
- `Mature Area Derelict Residential` and `Transitional Residential` exist as rate classes but not as assessment `Tax Class` values — unused by the Tax-Class join.
- **Two class vocabularies in the assessment CSV.** `Tax Class` (col 9) is the clean 4-value field used for the join. The `Assessment Class 1/2/3` (+ `% 1/2/3`) columns describe split-class parcels using *different* labels (`COMMERCIAL` = `Non Residential`, plus `MA DERELICT RESIDENTIAL` → Non Residential, `NONRES MUNICIPAL/RES EDUCATION` → exempt). `map(Assessment Class 1)` equals `Tax Class` in 100% of rows, so only the 2nd/3rd slices add information; split-class is rare (~0.25% of rows). Full label→rate-class map, counts, and the unified levy formula: `docs/FINDINGS_assessment_classes.md`.

### Residential-revenue decomposition (added 2026-07-16)

`apply_tax_rates.py` also emits **`res_levy`** — the subset of each parcel's levy
billed on **`RESIDENTIAL` + `OTHER RESIDENTIAL`** class slices (all housing:
houses/condos <4 units *and* 4+ unit apartment buildings; split-class parcels
contribute only their residential slice). **`MA DERELICT RESIDENTIAL` is
excluded** — the city deliberately bills it at the punitive Non Residential
rate, so its dollars are non-residential-rate dollars. Flows: `res_levy` →
`total_res_revenue` (aggregate) → **`res_revenue_per_acre`** /
**`res_revenue_per_lot_acre`** (slim GeoJSON; the lot variant inherits the
LOW_PARCEL_FRAC suppression). No share column ships — the client derives the
residential share as `res_revenue_per_acre / revenue_per_acre` (identical
denominators cancel). Real-data anchors (2025 roll): residential-class =
**52.6% of the citywide levy**; hood median share ~75%, DOWNTOWN ~16%; ground
p97.5 ≈ $28.5k/acre (web clamp $30k). Distinct from `is_residential`
(§ Residential split below), which is a *zoned-area* display flag, not dollars.

**Glass grid variant (added 2026-07-17):** `export_value_grid.py` rolls the
same `res_levy` into the 100 m cells — payload columns
**`res_revenue_per_acre`** / **`res_revenue_per_lot_acre`** appended after the
existing six (`value_grid.json` ~1.76 → ~2.1 MB raw; Pages gzips). A cell with
assessed property but no residential-class levy reads a **real 0**, not null
(distinct from "no cell" = no property); lot slots stay null where no eligible
lot acres, exactly like value/revenue. ~79% of cells have res > 0; res ≤ rev
per cell (±$1 whole-dollar rounding). Older files lack the columns and the
Glass Residential $ metric falls back to hood prisms (web column guard).

### Non-residential decomposition (added 2026-07-18 — SPEC_industrial.md A1)

`apply_tax_rates.py` also emits **`nonres_levy`** — the subset of each parcel's
levy billed **at the Non Residential rate**: `COMMERCIAL` + `MA DERELICT
RESIDENTIAL` + `DESIGNATED IND PROPERTIES` slices (`NONRES_RATE_LABELS`,
derived from the label→rate-class map so a future non-res label can't be
missed). The complement of `res_levy` by rate class; farmland (its own rate
class, 509 parcels) is the only slice in neither subset, so the identity
**`levy == res_levy + nonres_levy + farmland slices`** holds exactly (tested).
Flows mirror res: `nonres_levy` → `total_nonres_revenue` →
**`nonres_revenue_per_acre`** / **`nonres_revenue_per_lot_acre`** (slim
GeoJSON, LOW_PARCEL_FRAC suppression inherited) and into the 100 m cells
(payload columns appended LAST, after `median_year_built`; real-0/null
conventions identical to res; `value_grid.json` ~2.28 → ~2.50 MB raw). NOTE
there is **no industrial-vs-commercial split in the roll** — `COMMERCIAL`
covers all non-res (§ 2) — so this is the honest class-complete cut; an
industrial-only cut would need a zoning join. Real-data anchors (2025 roll):
non-res-rate = **47.4% of the citywide levy** ($1.281B of $2.704B; farmland
residual ~$532K); 34% of grid cells have nonres > 0; hood ground p97.5 ≈
$48.4k/acre (web clamp $50k). Web: fourth Money metric ("Non-res $"),
column-guarded like Residential $.

**Stock-age grid column (added 2026-07-17):** `export_value_grid.py` also
rolls `year_built` (property-info, § 2) into **`median_year_built`** per 100 m
cell — appended LAST in the payload columns; whole-year ints. Median over
ROWS (unit-weighted), which makes the multi-unit duplication regimes moot: a
tower repeating one year on every unit row medians to that year, no dedupe
machinery. A cell where **no property has a known year carries `null`, never
0** — age has no meaningful zero ("year 0" would be a lie; contrast
`res_levy`'s real $0). Consumed by the **Development view's Spikes picker**
("Year built" — height + colour linear in year, recency bright), NOT by
Glass; it rides in this file because the age layer needs the whole-roll cell
population, which `dev_grid.json` (permit cells only) doesn't have. Older
files lack the column and the picker stays hidden.

---

## 5. Zoning Bylaw Geographical Data (land-use layer, added 2026-06-29)

**Source:** Edmonton Open Data — dataset ID `fixa-tstc` ("Zoning Bylaw Geographical Data")
**Download URL:** `https://data.edmonton.ca/resource/fixa-tstc.geojson?$limit=20000`
**Download:** `scripts/download_data.py` (fetches this alongside assessment + boundaries)
**Format:** GeoJSON, ~9.2 MB
**Features:** 11,510 zoning polygons (MultiPolygon)
**CRS:** CRS84 / EPSG:4326 — reproject to EPSG:3400 before any overlay/area
**Vintage:** the **2024 Zoning Bylaw** (new codes, e.g. `RSF` = "Small Scale Flex
Residential"). Assessment is 2025 — close enough; zoning is stable. Record the
download date / `date_ext` for provenance.

**Why:** neighbourhood-level aggregation needs explicit categorization of
non-developable land (River Valley, parks, undeveloped) that parcel-level analysis
handles implicitly. Overlaid on neighbourhood boundaries → land-use composition %
per neighbourhood → drives the colour-scale set-aside. See `SPEC_revenue.md`
(Update 2026-06-29) and `FINDINGS_revenue_scale.md`.

### Columns (confirmed 2026-06-30)
| Column | Notes |
|--------|-------|
| `zoning` | zone code, e.g. `RSF`, `A`, `RM h16` — height/overlay suffixes appended; parse the **first token** for the base code |
| `description` | human-readable, e.g. "River Valley", "Small Scale Flex Residential" |
| `url` | link to the bylaw page. **The path encodes the authoritative bylaw section** — `…/part-2-…/residential-zones/…`, `…/industrial-zones/…`, `…/open-space-and-urban-services-zones/…`, `…/agricultural-zones/…`, plus `…-special-area` groups. Use as an independent **cross-check** when building the code→category dict (see quirks), NOT as the category itself (groups are mixed — see below) |
| `dc2_sub_area` | sub-area for `DC2` site-specific zones |
| `date_ext` | extract timestamp (e.g. `2026-06-29 02:07:03`) — record for provenance |
| `id`, `agreement_no` | record identifiers |
| `geometry` | polygon (Socrata source field `geometry_multipolygon`; geopandas reads it as `geometry`) |

### Known Quirks
- **Geometry needs cleaning before overlay.** Raw polygons are invalid/mixed-dimension
  → geopandas `overlay` raises `GEOSException`. Fix: `buffer(0)`, drop empty + keep
  only Polygon/MultiPolygon parts.
- **Do NOT categorize by keyword/prefix.** "Energy & Technology **Park**" is industrial,
  "Century **Park**" is a TOD redevelopment — the word "Park" ≠ green park. The `A*`
  codes are mostly River Valley special areas (Hawrelak, Muttart) but `AED` =
  Arena/Entertainment District (downtown), `ALA` = Ambleside apartments. Use an
  **explicit `code → category` dictionary** (exactly **95 base codes** confirmed
  2026-06-30; `description` + `url` make each obvious). Lives in `src/load_zoning.py`.
- **`url` cross-check (confirmed 2026-06-30).** The `url` path's bylaw section is a
  useful *verification* signal but is NOT a drop-in category — groups mix set-aside and
  developed codes. The `open-space-and-urban-services-zones` group is the clearest case:
  it contains set-aside `A`/`NA`/`PS`/`PSN` **and** developed infrastructure `PU` (Public
  Utility), `UF` (Urban Facilities), `UI` (Urban Institution), `AJ` (Alternative
  Jurisdiction). Categorize at the code level; use `url` only to catch dict errors (e.g.
  it correctly resolves the `A*` trap: `AED`→`downtown-special-area`, `ALA`/`AUVC`→
  `ambleside-special-area`, not river valley).
- **Direct Control zones (`DC`, `DC1`, `DC2`) — confirmed 2026-06-30.** ~1,081 rows are
  site-specific / special-area zones with no standard `/part-N/` bylaw section in `url`
  (`DC*`, plus named zones like Blatchford, Century Park, River Crossing). **Rule:**
  `DC`/`DC1`/`DC2` default to **developed** (stay on scale — conservative, won't wrongly
  hide land). Named-natural special-area codes (`NSRVES`, `A7` Hawrelak, etc.) are caught
  by their own explicit dict entry, not by the `DC` default.
- **`url = "legacy"` sentinel (confirmed 2026-07-07).** 44 polygons (611 ha) carry the
  literal string `legacy` in `url` instead of a bylaw-page path — pre-2024-Bylaw zones
  (mostly bare `DC`, some special-area) never migrated to the per-provision page system.
  There is **no page to scrape** for these, and the bare-`DC` ones also lack an
  `agreement_no`, so they are unclassifiable from this dataset alone (distinct from the
  ~19 unpublished provision pages that 403). The DC-use pipeline (`ANALYSIS_BACKLOG` item
  3) rolls them up as `frac_dc_unknown`; the largest single one (id `173291`, 50 ha) is
  West Edmonton Mall, geometrically coincident with the migrated `dc2-1198` polygon.
- **Set-aside categories:** never = River Valley (`A`,`NA`)/Parks (`PS`,`PSN`); not-yet
  = Future (`FD`)/rural (`AG`,`RR`)/industrial reserve (`EET*`). Institutional
  (`UI`,`UF`,`AJ`,`PU`) is a proxy for where exempt-roll understatement lives.
- **Residential split (added 2026-07-01, for the residential-only lens).** The developed
  bucket is split by each code's `description` into `res` (primary permitted use is
  housing — the `RS*`/`RM`/`RL`/`HDR`/`RMU` standard zones + special-area row-housing /
  apartment / low-density codes, e.g. `GRH`, `BLMR`, `SRH`, `CCLD`) and the
  non-residential group. `is_residential` = `frac_residential` ≥ **0.50** of *zoned*
  area (a display filter, **orthogonal to** `is_set_aside` — the two can't both be
  true since fractions sum to 1). Per-code assignments live in `src/load_zoning.py`.
- **Non-residential split (added 2026-07-03, for the use-mix view).** The old `nonres`
  bucket is split four ways: `com` (commercial/retail/entertainment, 14 codes),
  `ind` (industrial/warehousing/business employment, 7), `mix` (mixed use, 14), and
  `dc` (Direct Control — bespoke per-site bylaws, no single use claimable; 24% of
  nonres area so it can't honestly fold into another bucket). **Names mislead —
  ambiguous codes were resolved from the bylaw page's purpose statement (the `url`
  field):** `UW` "Urban Warehouse" is a downtown *mixed-use* zone, not warehousing;
  `BE` "Business Employment" sits in the bylaw's *industrial-zones* part; `HA`
  Heritage Area and `MMS` Marquis Main Street are mixed (ground-floor retail +
  res/office above); `MED`/`AED` entertainment districts are commercial. Unknown
  codes now default to `other` (on scale, claimed as no specific use, flagged
  loudly) instead of `nonres`; `frac_nonres` is kept as the sum of the four split
  categories + `other` for continuity. `frac_other` = 0 on current data (all 95
  codes mapped).
- **Refresh requirement:** re-pull each pipeline cycle so developing land (rezoned
  FD/AG → residential) graduates off the set-aside list automatically.

---

## 6. Road Network (road supply layer, added 2026-07-01)

**Source:** Edmonton Open Data — dataset ID `9j8t-zm52` ("Road Network")
**Download URL:** `https://data.edmonton.ca/resource/9j8t-zm52.geojson?$limit=100000`
**Download:** `scripts/download_data.py` → `data/raw/roads.geojson` (gitignored)
**Format:** GeoJSON, ~62 MB — centreline **LineStrings**, no surface polygons
**Features:** 53,720 segments (confirmed vs `count(*)` 2026-07-01)
**CRS:** EPSG:4326 — reproject to EPSG:3400 before any length calculation

**Why:** the services lens (`docs/SPEC_services.md`) — city-maintained road
length per neighbourhood, the first cost-side metric. Consumed by
`src/load_roads.py`; the shipped metric is **collector + local metres per
boundary acre** (`road_m_per_acre`).

### Key columns
| Column | Notes |
|---|---|
| `centerline_type` | `Road` 39,515 / `Alley` 12,088 / `Railway` 2,117 — **filter to `Road`** |
| `responsible_party_description` | City of Edmonton 49,794; Province 1,164 (ring road); CN/CP rail; Private 566; neighbouring municipalities — **filter to `City of Edmonton`** |
| `functional_class_code` | closed enumeration, 15 values (4 Arterial classes, Collector/Local by adjoining land use, `Local-ParkWay`, `Local-Private`, `Alley-Residential`) — explicit dict `CLASS_GROUP` in `load_roads.py` |
| `geometry` | LineString centrelines |

### Known Quirks
- **Null `functional_class_code` = Alley + Railway exactly** (14,205 = 12,088 +
  2,117, verified 2026-07-01). After the Road + City filters every row is
  classified — a null/unknown there means upstream drift (`load_roads` warns
  loudly and defaults to `local` so the length stays in the metric).
- **41 Road-type rows are functionally classed `Alley-Residential`** (all
  City-owned, 5.7 km). Excluded per the alleys-out decision — function
  governs, not `centerline_type` (SPEC_services.md).
- **`Local-Private` ≠ privately owned:** 73 of the 376 `Local-Private` rows are
  `responsible_party = City of Edmonton` and survive the ownership filter —
  kept as `local` (responsibility governs, not the name).
- **Arterials are computed but excluded from `road_m_total`** (shared
  infrastructure — SPEC_services.md; don't re-litigate). ~0.28% of filtered
  length falls outside all neighbourhood polygons (conservation guard reports
  it every run).
- **Vintage:** live feed like the others; no year semantics of its own (the
  network changes continuously, not per roll year). Refresh weekly with the
  other inputs.

## 7. Fire Response Events (fire lens, added 2026-07-06)

**Source:** Edmonton Open Data — dataset ID `7hsn-idqi` ("Fire Response: Current and Historical")
**Download URL:** `https://data.edmonton.ca/resource/7hsn-idqi.csv?$limit=2000000`
**Download:** `scripts/download_data.py` → `data/raw/fire_response.csv` (gitignored)
**Format:** CSV via the SODA resource endpoint (snake_case API headers)
**Rows:** 948,086 dispatched events, 2011–mid-2026 (pulled 2026-07-06); ~90k/yr in the 2023–2025 window — the long-run ~65k/yr average understates current volume
**Licence:** Open Government Licence – City of Edmonton

**Why:** the fire lens (`docs/SPEC_services.md` "Fire lens") — dispatched
emergency events per neighbourhood per year, the first *demand*-side
service. Consumed by `src/load_fire.py`; the shipped metric is
**`fire_events_per_acre`** (mean annual kept events over the pinned
`FIRE_YEARS` window ÷ boundary acres).

### Key columns (headers confirmed on the first real pull, 2026-07-06; counts from the Session-12 probe)
| Column | Notes |
|---|---|
| `dispatch_datetime` | **confirmed** — resolves as the first exact candidate in `DISPATCH_COLUMN_CANDIDATES` (the resolver + substring fallback + hard error stay as drift insurance). Only 186 of 948k rows unparseable. |
| `event_close_datetime` + `event_duration_mins` | dispatch→CLOSE, i.e. incident length. **There is NO on-scene-arrival timestamp anywhere** — a true response-time metric is NOT buildable from this data (confirmed against the full column list) |
| `event_type_group` | **two-letter CODES** (MD, AL, TA, OF, CA, FR, HZ, TM…), NOT the long names the Session-12 probe showed — those live in `event_description`. ~1k rows over 15 years are code-only with a null description (DR 762, `86` 165, FP 83, HO 47, `88` 1) — kept under the bare code. |
| `event_description` | the long-name vocabulary (one-to-one with the codes): MEDICAL 57% (536k), ALARMS 144k, MOTOR VEHICLE INCIDENT 65k, OUTSIDE FIRE 48k, CITIZEN ASSIST 36k, FIRE 24k, HAZARDOUS MATERIALS 20k, OTHER 10k, RESCUE 7k, VEHICLE FIRE 5k, MESS 137, PERMIT-BURNING OR OTHER 10, + operational noise (TRAINING/MAINTENANCE 18k, COMMUNITY EVENT 2.5k, PRE-INCIDENT PLANNING 515, 31k both-null). **`load_fire` filters on this column** (bare-code fallback). |
| `response_code` | dispatch-priority letters (D 446k, AL, NF, C, B, SR, E…) — **undecoded; never filter on it** |
| `neighbourhood_name` | **pre-joined on ~99% of rows** (8,093 null over the full history) — the per-hood metric needs no spatial work |
| lat/long | present; unused by the lens (locked: no spatial fallback) |

### Known Quirks
- **The 57% MEDICAL share is the interpretive trap** — the metric is
  fire-department *demand*, mostly medical calls, not fires. Legend/blurb
  caveat by locked decision, never a filter.
- Live feed (current + historical); the metric window is pinned
  (`FIRE_YEARS` in `main.py`, last 3 FULL years) so weekly refreshes don't
  average in a partial year. Bump each January (blurb + legend years in
  `web/index.html` ride along).
- `load_fire` HARD-ERRORS if a window year has zero rows (wrong pin or
  upstream drift) and keeps-but-logs group vocabulary outside
  `KNOWN_GROUPS`. **The Session-12 probe read `event_description` values,
  not `event_type_group`** — the first real pull (2026-07-06) caught the
  original code filtering on the wrong column via exactly that unknown-
  vocabulary warning (the noise filter matched nothing, MEDICAL logged 0%).
- **Hood names lag the boundary file** — `FIRE_NAME_CORRECTIONS` in
  `src/load_fire.py` layers fire-specific fixes on top of the shared
  `NAME_CORRECTIONS`: `OLIVER → WÎHKWÊNTÔWIN` (the fire CSV still uses the
  old name; 1,476 events/yr — 5th-highest hood, displayed as 0 until the
  first production refresh caught it), plus `KESWICK/MCCONACHIE/WINDERMERE
  AREA` → their boundary hoods. Kept out of the shared dict because the
  assessment side's OLIVER straggler is deliberately unmapped (see "Name
  Matching"). Legitimately unmatched leftovers (~18 events/yr, flagged at
  the join): COREYLAND, EDMONTON MUNICIPAL AIRPORT, UNKNOWN, RURAL SOUTH
  EAST — no boundary polygon exists for them.

## 8. Fire Stations (fire lens context dots, added 2026-07-06)

**Source:** Edmonton Open Data — dataset ID `b4y7-zhnz` ("Fire Stations")
**Download URL:** `https://data.edmonton.ca/resource/b4y7-zhnz.csv?$limit=500`
**Download:** `scripts/download_data.py` → `data/raw/fire_stations.csv` (gitignored)
**Rows:** 31 — station number, address, lat/long point ONLY (no
staffing/coverage/response data; probed 2026-07-05).
Exported by `load_fire.export_fire_stations_web` to
`web/data/fire_stations.json` (committed) as `{"stations": [[lon, lat,
label], …]}` — context dots in the Services view, not a coverage claim.
Column resolution uses the same explicit-candidates rule as §7.

## 9. ETS GTFS Static Feed (transit lens, added 2026-07-11)

**Source:** Edmonton Open Data — the GTFS static feed published as FIVE
individual Socrata tables (the "zipped files" dataset `urjq-fvmq` is an
href-only landing page, no machine-readable blob; the `yiem-dcbw` "GTFS
Downloads" dataset is download-count *stats*, not the feed):

| Table | Dataset | Rows (2026-07-11) | Downloaded to |
|---|---|---|---|
| Stops | `4vt2-8zrq` | 6,882 | `data/raw/gtfs_stops.csv` |
| Routes | `d577-xky7` | 238 | `data/raw/gtfs_routes.csv` |
| Trips | `ctwr-tvrd` | 56,812 | `data/raw/gtfs_trips.csv` |
| Stop Times | `greh-g7ac` | 1,744,051 | `data/raw/gtfs_stop_times.csv` |
| Calendar Dates | `f2sy-bth7` | 9,248 | `data/raw/gtfs_calendar_dates.csv` |
| LRT Routes | `rpjw-4jft` | 4 | `data/raw/lrt_routes.geojson` |

**Download:** `scripts/download_data.py` (all gitignored). Trips and
stop_times use `$select` for only the keyed columns — trips otherwise
carries a per-trip `geometry_line` that dominates the file; stop_times
needs only `trip_id,stop_id` (31.6 MB slimmed). `$select` doesn't change
the row count, so both truncation guards still apply. LRT Routes is a
small GeoJSON (4 features), a separate 6th input feeding only the track-line
context layer — the metric runs without it.
**Why:** the transit lens (`docs/SPEC_services.md` "Transit lens") —
mean-weekday scheduled stop-events per neighbourhood. Consumed by
`src/load_transit.py`; the shipped metric is **`transit_dep_per_acre`**.

### Key columns
| Column | Notes |
|---|---|
| stops: `stop_id`, `stop_lat`/`stop_lon`, `location_type` | types: 0 stop/platform (6,673), 1 station (58 — LRT stations + transit centres, the context-dot export), 2 entrance (109), 3 node (42). **The feed includes REGIONAL stops** (Spruce Grove, St. Albert park-and-rides etc.) — they fall outside every hood polygon and land in the reported unassigned bucket (~5.8% of stop-events, 2026-07-11). |
| routes: `route_id`, `route_type_descr` | "Bus" 235 / "Tram, Streetcar, Light rail" 3 — the explicit `ROUTE_MODE` dict in `load_transit.py`; unknown values kept as `other`, logged. |
| trips: `trip_id`, `route_id`, `service_id` | plain join keys. |
| stop_times: `trip_id`, `stop_id` | one row = one scheduled stop-event; only these two columns downloaded. |
| calendar_dates: `service_id`, `date`, `exception_type` | **calendar-dates-only feed** — every active service day is an `exception_type` 1 row (no calendar.txt); type-2 removals honoured generically if they ever appear. |
| lrt_routes: `lrt_route_id`, `lrt_route_name`, `lrt_route` (multiline) | **Not part of the metric — a map context layer only.** Four route multilines: 021R Capital, 022R Metro, 023R Valley, and `HER` (High Level Bridge heritage streetcar). `export_transit_lines_web` **drops HER** (`EXCLUDED_LRT_ROUTE_IDS` — volunteer-run, not ETS LRT service, absent from the GTFS routes counted) and flattens the rest to `web/data/lrt_lines.json` (343 segments, 2026-07-11). |

### Known Quirks
- **The feed is a snapshot of the CURRENT signup only** — probed window
  2026-06-18 → 2026-08-29 (the SUMMER schedule, the seasonal low).
  Weekly refreshes will step the metric at signup boundaries. No roll-year
  semantics; provenance = download date + the window logged every load.
- **No ridership anywhere:** the portal's `sfwk-p9kr`/`77dh-qrp7` (on-time
  %) and `wh9u-ef4x` (revenue vehicle hours) are citywide-monthly only
  (probed 2026-07-11) — no stop/route/neighbourhood usage exists. The lens
  is scheduled supply and must be labelled as such.
- **On-demand transit zones are not in the GTFS** (238 fixed routes only) —
  invisible to the metric; documented limitation for the on-demand fringe.
- ~253 service_ids (~20.6k trips, 2026-07-11) are weekend/holiday-only —
  they weigh 0 in the weekday metric by construction, logged not dropped.

## 10. Building Permits (development & infill lens A, added 2026-07-12)

**Source:** Edmonton Open Data — dataset ID `24uj-dj8v` ("General Building Permits")
**Download URL:** `https://data.edmonton.ca/resource/24uj-dj8v.csv?$select=year,issue_date,work_type,building_type,units_added,neighbourhood,latitude,longitude&$limit=1000000`
*(latitude/longitude added 2026-07-15 for the 100 m detail grid —
`load_permits.export_dev_grid` → `web/data/dev_grid.json`; see the
geocoding-lag quirk below.)*
**Download:** `scripts/download_data.py` → `data/raw/building_permits.csv` (gitignored)
**Format:** CSV via the SODA resource endpoint, **slim `$select`** — only the 6
filter/join/numerator columns (the full schema is 34 cols; we skip
`construction_value`, `geometry_point`, `zoning`, `floor_area`, etc.). `$select`
does not change the row count, so both truncation guards still apply.
**Rows:** 243,371 permits, `issue_date` 2009-01-05 → present (pulled 2026-07-12)
**Licence:** Open Government Licence – City of Edmonton

**Why:** the Development & Infill lens A (`docs/SPEC_development.md`) — new
dwelling units built per neighbourhood, the project's first *change/flow* metric
(everything else describes the roll as it stands today). Consumed by
`src/load_permits.py`; the default metric is **`new_units_per_acre`** (Σ
`units_added` on new-construction ∩ residential permits over the pinned
`PERMIT_YEARS` window ÷ boundary acres). A second metric **`new_permits_per_acre`**
(permit count ÷ boundary acres, added 2026-07-13) drives the web view's
units/permits sub-metric picker — project density vs dwelling supply.
`new_dwelling_units` (window total) + `new_dwelling_permits` (count) ride into the
slim file for the tooltip.

**Window toggle (added 2026-07-13).** A second, shorter pinned window
(`PERMIT_YEARS_RECENT` in `main.py` = the last 3 full years, 2023–2025) is
aggregated by a second `load_permits` call and emits `_3yr`-suffixed twins of all
four columns (`new_units_per_acre_3yr`, `new_permits_per_acre_3yr`,
`new_dwelling_units_3yr`, `new_dwelling_permits_3yr`). The base (5yr, 2021–2025)
columns stay **unsuffixed** for backward-compat with the live geojson + web
gates. The web `#devwindow` picker switches 5yr ↔ 3yr; it's gated on the `_3yr`
columns being present (older data files show the 5yr base only). Both windows are
pinned + drift-guarded and bump together each January.

**Long "since 2009" window (added 2026-07-21).** A third window `PERMIT_YEARS_LONG`
(`main.py`) emits `_long`-suffixed twins of all four residential columns (plus
`ind_permits_per_acre_long`) — the cumulative **"density added over the era"** cut
that reproduces the inspiration lens's 2009–2023 "homes added" map. Unlike the two
sliding windows it is **anchored**: the start is fixed at `PERMIT_START_YEAR = 2009`
(the permit record's first year, DATA.md above) and only the end advances, so it is
DERIVED as `range(2009, PERMIT_YEARS[-1] + 1)` — the annual January bump of
`PERMIT_YEARS` extends it automatically, no separate pin to roll. Citywide it sums
~160k units (2009–2025) vs ~60k (5yr) / ~39k (3yr). The web `#devwindow` gains a
**"Since 2009"** button (gated on the `_long` columns) — a **first-class window**:
it drives both the hood choropleth AND its own 100 m detail grid (`export_dev_grid`
emits `units_long`/`permits_long` cells + `coverage["long"]`, added 2026-07-22).
The geocoding lag is on the NEWEST permits, not the oldest — **2009–2023 sit at
95–98% geocoded, 2025 at ~72%** — so the long window is the *best*-covered of the
three grids (84% of units on the grid, vs 79% / 71% for 5yr / 3yr). An earlier cut
made it choropleth-only on the mistaken belief that early-year geocoding was sparse;
the data disproved it (`.venv/bin/python` count by year).

### Key columns (live vocab confirmed 2026-07-12)
| Column | Notes |
|---|---|
| `units_added` | dwelling-unit numerator. A single apartment permit adds many (GRIESBACH: 2,274 units from 349 permits); a single-detached permit adds 1. Non-numeric → 0 units, kept as a permit, warned. |
| `work_type` | **new-construction filter.** `NEW_WORK_TYPES` = `(01) New` + `(01) Building - New` + `(01) New House`. Suite-adds/conversions (`(07)`/`(08)`/`(09)`) add dwellings but are INFILL densification — excluded from Lens A (they're the Lens B story). ~41k of ~78k in-window rows are null/blank `work_type` — excluded, count reported. **Verified (S48 Fable audit, 2026-07-13): all 40,956 in-window (2021–2025) null-`work_type` rows carry `units_added` = 0 (sum exactly 0), so the exclusion loses ZERO dwelling units** — they are 0-unit sub-permit-like rows (33,669 are `building_type` = Single Detached House), NOT old miscoded new-construction. (The earlier "most predate consistent coding" rationale was wrong.) |
| `building_type` | **residential-dwelling filter.** 71 distinct values with many spelling variants of each category — `Apartments (310)`/`Apartment (310)`/`Apartment Condos (315)`; `Row House (330)`/`Row Houses (330)`; `Semi Detached House` (no code); `Backyard House (110)` (a garden suite, counted). All enumerated in `RESIDENTIAL_BUILDING_TYPES`, never prefix-matched. Garages, commercial, `Mixed Use (522)` excluded. **Also `INDUSTRIAL_BUILDING_TYPES`** (400-series: Animal & Plant Services 410, Manufacturing 430, Transport Terminals 440, Maintenance/Hangars 450, Warehouses 460, Communication 470, Utility 480, Engineering 490) drives the separate industrial-permit-velocity count (§ below) — enumerated by FULL STRING because codes duplicate across unrelated types (`Parkade (490)` is NOT industrial). |
| `year` | integer permit year — drives the pinned window filter (vs parsing `issue_date`). |
| `neighbourhood` | **UPPERCASE, matches `neighbourhood_name`** — the join key. |

### Known Quirks
- **`count(*)` aliases as `count_1`, not `count`** on this dataset (a Socrata
  inconsistency — roads returns `count`). `download_data.server_count` was
  hardened 2026-07-12 to read the sole count column by value, so the truncation
  cross-check works everywhere.
- **"Same data, different cuts":** seven other portal datasets are saved
  filters/map-views over the same two source tables (building permits + dev
  permits) — proven by identical `rowsUpdatedAt`. We pull `24uj-dj8v` and filter
  ourselves; **ignore `itki-s8y9`/`jsf3-5dv2`/`537d-t4az`/`uep4-4w4g`/`ramb-ihnk`**
  (building) and `66ut-y7w2` (dev). See `docs/SPEC_development.md` "Data".
- **Activity ≠ money path** — the name join is **warn-not-fail** (unlike the
  assessment money guard, `scripts/check_unmatched_names.py`): an unmatched
  permit hood is a blank hood, not a silent dollar loss. `CHAPPELLE AREA →
  CHAPPELLE` etc. resolve via the shared `NAME_CORRECTIONS`; the only leftover
  straggler is `GLENORA, ROSSLYN` (1 unit, immaterial).
- `load_permits` HARD-ERRORS if a window year has zero permits (stale
  `PERMIT_YEARS` pin or upstream drift), and keeps-but-warns any `work_type` /
  `building_type` value outside the `KNOWN_*` vocab (it might be a new
  residential variant to count) — same explicit-dictionary discipline as
  `load_fire`. Bump **both** `PERMIT_YEARS` and `PERMIT_YEARS_RECENT` each January.
- **`occupancy_granted_date`** exists in the full schema (a completed-builds
  variant) but is only populated for residential finalized ≥ Jan 1 2022 /
  non-residential ≥ Jan 1 2024 — useless for historical totals, not fetched.
- **Geocoding lags on the newest permits** (`latitude`/`longitude`, probed
  2026-07-14): among in-window new-construction rows, nulls are ~1–2%/yr for
  2021–2023 but 994 permits in 2024 and 3,564 in 2025 — a lag, not a
  structural hole (nearly all null-coord rows still carry `neighbourhood`, so
  hood aggregation is unaffected). The 100 m detail grid
  (`export_dev_grid`) therefore bins **geocoded permits only** — 5yr window at
  build time: 47,125 of 59,697 units (~21% not yet mapped; 3yr ~29%) — and
  writes per-window `coverage` into `dev_grid.json` so the web blurb
  discloses the live percentage. Never backfill with hood centroids. Expect
  coverage to improve as the city geocodes its backlog; the weekly regen
  picks that up automatically.

### Industrial permit velocity (SPEC_industrial.md A3, added 2026-07-18)

The same `24uj-dj8v` permits, cut for industrial construction: `load_permits`
counts new-construction (`NEW_WORK_TYPES`) ∩ `INDUSTRIAL_BUILDING_TYPES`
(400-series, above) permits per hood over the same pinned windows, emitting
**`ind_permits`** (count) → `join_and_calculate` **`ind_permits_per_acre`**
(+ the `_3yr` pair), in `SLIM_COLUMNS`. **Count only** — `units_added` is
meaningless for industrial (no dwellings), and `construction_value` is
reserved (consistent with the Lens C reservation). Aggregated separately from
the residential rollup and outer-merged, so a hood with one kind of activity
but not the other carries a true 0 in the missing column. Real data (2021–2025
window, build time): **283 new industrial permits across 117 hoods** (3yr: 189
across 85); top hoods are the industrial areas (SOUTHEAST INDUSTRIAL, MISTATIM,
CLOVER BAR, WINTERBURN, EASTGATE BUSINESS PARK); per-acre is small (p97.5 ≈
0.015/acre). Web: third `#devmetric` option "Industrial" — a Development-view
**choropleth only** (no detail-grid cells; not an Infill activity — the roll
has no industrial-vs-commercial split anyway, § 2). **NOTE — no
industrial-vs-commercial split exists in the assessment roll** (§ 2), so this
permit-based cut is the ONLY industrial-specific spatial signal the project
has; it is construction activity, not assessment base.

## 11. Alberta FIR Debt Series (debt lens D5, added 2026-07-14)

**Source:** Alberta Municipal Affairs — Municipal Financial and Statistical
Data (FIR/SIR), `https://open.alberta.ca/opendata/municipal-financial-and-statistical-data`
**Fetch:** `scripts/fetch_fir_debt.py` → committed `data/fir_debt_series.json`
(12 KB). **Manual, reviewed input** (mill-rates pattern): NOT part of the weekly
refresh — re-run when a new financial year publishes (~annually, watch for it
alongside the January year-roll), eyeball the diff, commit. openpyxl/xlrd are
dev-only deps (`requirements.txt`, not `requirements-ci.txt`); the test module
skips itself on CI.
**Format:** one XLSX workbook per financial year, every Alberta municipality.
The debt schedule ("Schedule AA", 8 identical columns 2003–2025) carries FIR
item codes `05700` Debt Limit / `05710` Total Debt / `05720` Debt Service
Limit / `05730` Total Debt Service Costs.
**Extracted:** EDMONTON (code `0098`), ST. ALBERT (`0292`), STRATHCONA COUNTY
(`0302`) — the two peers the debt-lens brief benchmarks against — for
2003–2025 (23 years; one year further than the brief expected).
**Licence:** Open Government Licence – Alberta

**Why:** debt-lens ticket D5 (`docs/fable_brief_debt_lens.md` Component 2) —
the citywide debt context annotation (trend + peer benchmark, explicitly
non-spatial). The display/chart is a separate, undecided design step; this is
the data layer only.

### Format eras (all verified 2026-07-14)
| Years | Where | Debt sheet |
|---|---|---|
| 2017–2025 | standalone `YYYY_financial_year.xlsx` on the dataset page | `AA(1)-Debt` |
| 2009–2016 | inside `2009-2016-municipal_financial-data-and-statistics.zip` | `AA(1)-Debt` |
| 2004–2008 | inside `xlsx-2003-2008.zip`, per-schedule `YYYY/YYYY-AA-Debt Info.xlsx` | `Schedule AA` |
| 2003 | same zip, legacy `2003-EA-MR/GR Debt Info.xls` (xlrd) | `GR Debt Info` |

(A `xlsx-2002-1994.zip` also exists if the series is ever extended back.)

### Known Quirks
- **STRATHCONA COUNTY 2013 is reported in $000s** in the source workbook (debt
  limit `485,926` between real-dollar neighbours 473.9M/504.2M). The fetch
  script applies a documented ×1000 correction (`KNOWN_UNIT_CORRECTIONS`),
  records `unit_corrected: 1000` on that year's JSON record, and a
  neighbour-band sanity check (factor 5 vs adjacent years) hard-fails if a new
  unit slip ever appears.
- **The FIR "Debt Limit" is the MGA regulation limit** (Debt Limit Regulation
  255/2000 — 2× revenue for most municipalities; Edmonton/Calgary have their
  own), **NOT Edmonton's internal DMFP policy limits** (≤18% tax-supported /
  ≤21% total debt servicing) that the "69% of limit" headline in the debt-lens
  brief refers to. Don't conflate the two in any display. On FIR terms,
  Edmonton 2025 total debt = 59.3% of its MGA debt limit.
- **Anchor cross-checks** pin the extraction to independently published
  figures: Edmonton 2025 total debt $4,592,150,000 (the brief's "$4.6B"
  reported to Council 2026-03-17) and Strathcona County 2022 $133,070,148 (the
  brief's audited peer datapoint). A mismatch on re-fetch means the province
  restated data → human review (`--allow-anchor-drift` to accept).
- Edmonton's series is NOT monotonic — e.g. 2017 drops to $2.91B from $3.34B
  (2016) before climbing again; real amortization, not a data error (both
  years pass the neighbour band).

## 12. Off-Site Levy Fire-Hall Catchments (debt lens D0, added 2026-07-15)
Source: **Off-Site Levy Bylaw 19340**, `edmonton.ca/business_economy/off-site-levy-bylaw`
(laptop-reachable only). The 12 fire-hall levy catchments are the Component 1
spatial join key in the debt-lens brief.
- Raw artifacts in `data/raw/offsite_levy/`: `BL19340_offsite_levy_bylaw.pdf`,
  `ScheduleA_catchment_map.jpg` (the catchment map exhibit, bylaw p.7),
  `2026_approved_rates.pdf` (cost/area/rate table).
- **No GIS vector layer exists** — data.edmonton.ca (0 Socrata hits), ArcGIS Hub
  (Calgary layers only), and the bylaw page all lack one. Boundaries are
  published **only as the Schedule A raster**. Full investigation +
  neighbourhood-union feasibility (which catchments the 407-hood grid can/can't
  reproduce, with per-catchment area validation) in
  `docs/FINDINGS_offsite_levy_catchments.md`.
- **Derived product: `data/levy_catchments.geojson`** (10 features, committed) —
  each catchment approximated as a union of neighbourhoods via
  `scripts/build_levy_catchments.py` (manual reviewed input, like
  `fetch_fir_debt.py`; NOT in the weekly refresh). The editable `CATCHMENT_HOODS`
  table maps hoods to catchments read off Schedule A. The 12 bylaw catchments
  collapse to **10 units**: EETP + Northeast EETP and Horse Hill + Northeast
  Horse Hill are each merged (the far-greenfield grid is one giant hood per
  corner). Each feature carries the brief's levy attributes + a `union_ha` /
  `area_ratio` QA field + an `approximation` label. Tests:
  `tests/test_build_levy_catchments.py`.
### Known Quirks
- **Boundaries are advisory** — the bylaw states the City "may adjust and refine"
  catchment boundaries over time; the map footnote says "subject to change." Any
  derived polygon layer must be labelled "approximated to neighbourhood
  boundaries," not presented as authoritative.
- **`EDMONTON ENERGY AND TECHNOLOGY PARK` (one 5,334 ha hood) spans BOTH the EETP
  and Northeast EETP catchments** — the neighbourhood grid is too coarse in the
  far greenfield to separate them by union (see FINDINGS §3).

## 13. City Service Unit Costs (V2 cost-per-acre, added 2026-07-15)
`data/city_unit_costs.json` — MODELED unit costs for the V2 "city service cost
per acre" composite (`SPEC_utilities` decision 3). Manual reviewed input
(mill-rates pattern; NOT auto-fetched, NOT in the weekly refresh). Sourced on
Peter's laptop (edmonton.ca unreachable from the Oracle box). **Roads + fire
only** — never label the derived metric "total city cost".
- **Roadway = $50/m/yr** (O&M + renewal). Source: edmonton.ca "Development Impact
  on Infrastructure" — neighbourhood road $600k O&M + $1.9M renewal per km,
  annualized over a 50-yr life (Peter's call 2026-07-15); 3%-of-value rule
  cross-checks (~$45). Applies to the collector+local `road_m_per_acre` metres.
- **Fire = 2026 gross operating budget $276.706M** (net $273.598M, 1,361 FTE).
  Source: City of Edmonton 2026 Approved Operating Budget PDF, Fire Rescue
  Services line. The V2 fire term divides this by the pipeline's OWN citywide
  kept-event total (don't hardcode dispatches), so the unit cost's denominator
  matches the `fire_events_per_acre` numerator.
- **Consumed (2026-07-15)** by `join_and_calculate.load_unit_costs` (validates
  loudly — a malformed hand edit fails the pipeline) → the `unit_costs` arg
  computes `svc_cost_per_acre` (in `SLIM_COLUMNS`). The per-event divisor is
  the fire frame's citywide sum PRE-join (unmatched fire hoods stay in the
  denominator). Composite requires BOTH the roads and fire lenses; either
  missing → warn + skip. `main.py --skip-service-cost` / `--unit-costs-json`.
- **Displayed (2026-07-16)** two ways (`web/index.html`): the Services view's
  "Service cost (roads+fire)" checkbox (SERVICES `servicecost`, sqrt colour on
  the shared `svc-plane`) AND the Ratio view's "Per service $" denominator
  (`revenue_per_acre / svc_cost_per_acre` — dimensionless coverage, log colour,
  RATIO_DENOMS `servicecost`). Both carry the caveats below; the ratio copy also
  states it reads ≫1 because the cost side is only two services (median ≈5.8×),
  NOT "pays its way". The column ships to the live GeoJSON on the first refresh
  after the metric PR #59 — until then both controls are column-guarded off.
### The OPERATING trio (added 2026-08-03, transportation lens Stage 2)
The same file also carries `roadway_ops`, `bikeway_ops` and `transit_ets`, on a
**strictly operating basis** — maintenance + snow clearing, **no capital**.
- **Roadway ops = $4.635/m/yr** ($1,285/km maintain + $3,350/km snow).
- **Bikeway ops = $20.278/m/yr** ($178/km maintain + $20,100/km snow) — a
  bikeway metre costs **4.4× a road metre** to operate: cheap to keep up,
  expensive to clear (24-hour bare-pavement standard).
- **Transit = ETS bus+LRT gross $436.605M (2025)**; **DATS excluded** ($31.966M
  of the $468.571M total) because it is door-to-door and generates no scheduled
  stop-events. Divided by the pipeline's OWN citywide stop-event total, like fire.
- Source for the two rates: Taproot Edmonton reporting quoting City infrastructure
  field operations staff; ETS from the 2024/2025 Annual Service Plan Appendix A.
  Both **relayed**, not fetched from the Oracle box.
### Known Quirks
- **The fire term is a demand ALLOCATION of a mostly-fixed budget** — a hood with
  2× the events does not cost the City 2× (most fire cost is standing capacity).
  Carry that caveat in any UI copy. **The transit term has the identical shape.**
- ⚠️ **THIS FILE HOLDS TWO INCOMPATIBLE BASES.** `roadway_om_renewal` is
  **$50/m/yr lifecycle**; `roadway_ops` is **$4.635/m/yr operating** — the SAME
  metres, **~10.8× apart**, and both ship to the served GeoJSON. Never sum or
  compare them. The `_ops` column suffix exists solely to keep them apart; a
  test pins them distinct. See the file's own `_two_bases` field.
- ⚠️ **$178/km/yr IS NOT A LIFECYCLE RATE**, though it was proposed as one on the
  phrasing "replace, repair, and maintain". It derives from ~$0.27M/yr over
  ~1,500 km; the same source puts snow clearing on that network at **113× it**;
  at a 50-yr life it totals **$8,900/km** for build plus all replacement; and
  against the City's own ~3%/yr set-aside rule it is **~33× low**. Full record in
  `bikeway_ops.rejected_lifecycle_reading`. **No bikeway lifecycle figure exists
  yet** — that is an open TODO item.
- ⚠️ **Two rate/denominator mismatches, recorded not absorbed.** The bike snow
  rate blends over a ~1,500 km network the source defines as *"bike lanes,
  multi-use paths, public pedestrian squares, bus stops, LRT platforms, and
  staircases"* — substantially **not** dedicated bikeway, while our numerator
  (~981 km) is. The road snow rate blends over ~11,000 km **including arterials**,
  which are priority-cleared and cost more per km, so the local-road term is
  likely a little high. **The 11,000 km denominator is never imported into the
  spatial pipeline** — only the per-km rate is.
- ⚠️ **Vintage mismatch, accepted:** ETS is 2025 while fire is 2026 Approved.
  They never enter the same composite (fire → `svc_cost_per_acre`, transit →
  `transport_cost_ops_per_acre`), so it is across columns, not inside a number.
- **Sidewalks are a separate, non-overlapping category** (~5,776 km, ~$5.9M/yr
  ops) and are in neither the bike metric nor the 1,500 km snow denominator.

## 14. Geographic Reference Layers (orientation, added 2026-07-27)
`web/data/reference.geojson` (**70 kB, 16 features**, committed) — the North
Saskatchewan River, the regional **highway network**, and the seven
neighbouring municipalities as both an **outline** and a name, so a first-time
viewer can orient before reading the fiscal data. The map has **no basemap
tiles** (just a dark backdrop), so without these there is no geographic context
at all. Purely cartographic: no metric, no tooltip.

Built by `scripts/build_reference_layers.py`. **NOT in the weekly refresh** —
static geography, same posture as `build_levy_catchments.py`; the endpoints are
queried once at build time, never at runtime. Features carry `t`
(`"river"` | `"highway"` | `"boundary"` | `"place"`), matching
`roads.geojson`'s convention; `place` features additionally carry `name`.

⚠️ **REVISED 2026-08-03 — `t="henday"` IS GONE, replaced by `t="highway"`.**
The old layer was the Anthony Henday alone, hand-extracted from the City
centreline feed, and it **stopped at the city limit**. Peter's ask was for the
main highways to run off the edge of the frame the way the river does. See
"Why OSM" below; the retired extraction's quirks are in `TODO_archive.md`.

- **River** — Alberta `base_water_feature` MapServer **layer 72**
  (`Lake/River (20K)`), `NAME='North Saskatchewan River'` (7 polygons
  province-wide, all genuinely the river). Clipped to the city bbox + a **60 km**
  margin so it runs clean off the edge of the view rather than stopping dead —
  the city sits *on* a river that comes from and goes somewhere, and two square
  ends just inside the frame read as a lake. The margin is sized against the
  default camera: at HOME zoom 10.2 and latitude 53.5 the scale is ~79 m/px, so
  a 1440px viewport spans ~114 km flat and the 52° pitch pushes the horizon
  further; the city half-width is only ~15 km. Natively **EPSG:3400**.
  **95% of the file** and deliberately never re-simplified (settled 2026-07-27:
  Peter checked the sub-pixel islands on device — they do not read as speckle).
- **Highways** — **OpenStreetMap via Overpass** (`overpass-api.de`), classes
  **`motorway` + `trunk`**, clipped to the *same* 60 km box as the river.
  Measured 2026-08-03: 1,194 ways / 999 km raw → **871 km welded in 89 parts**,
  of which **68% lies outside the city** and the extent exceeds the city bbox on
  all four sides. Top routes: Hwy 16 (Yellowhead) 337 km, Hwy 2 (QEII) 213 km,
  Hwy 216 (Henday) 156 km, Hwy 43 131 km, then 63/28/15/16A.
- **Boundaries + places** — Alberta `urban_and_rural_municipality` MapServer.
  Seven names (`PLACES` in the build script): St. Albert, Sherwood Park, Spruce
  Grove, Fort Saskatchewan, Leduc, Beaumont, Devon. Each yields **one Polygon**
  (the largest, simplified at 100 m — 169 vertices for all seven, ~3.6 kB) and
  **one Point** at that same polygon's centroid, so a label and the shape it
  names cannot disagree. Natively **EPSG:3400**.

### Why OSM, and the trap in the obvious alternative
Two sources were tried and rejected on 2026-08-03:
- **The City centreline feed** (`data/raw/roads.geojson`) carries every main
  highway — Yellowhead, Calgary Trail, Manning, Sherwood Park Fwy, Hwy 14/15/216
  — as `Province of Alberta` rows that `load_roads` filters out. But it is a
  *City* feed: the highways **stop at the municipal boundary**, which is exactly
  the amputated look `MARGIN_M` exists to prevent for the river.
- ⚠️ **Alberta's `transportation/highways_public` MapServer RETURNS NULL
  GEOMETRY.** It has ideal attributes (510 `IN SERVICE` segments with
  `ROAD_NUMBER` over this extent) and answers **HTTP 200 with all 510 features
  and no shapes** — in `f=geojson` and `f=json`, with and without `outSR`, with
  and without an envelope, on the simplest possible `where`. Its
  `capabilities` still advertise `Query`. **A reader that trusts the feature
  count would emit an empty highway layer and log success.**

### Known Quirks
- ⚠️ **Overpass answers `406 Not Acceptable` to a raw POST body or an anonymous
  client.** The query must be **form-encoded as `data=`** with a **named
  `User-Agent`** (`OVERPASS_USER_AGENT`), as its usage policy asks.
- **OSM is ODbL**, so the credit is required *wherever the data is used*. The
  Data & Methods pod carries it in **both** builds — unlike the City
  road/fire/transit credits, which are full-only because those lenses are.
- **`primary` is deliberately NOT in `HIGHWAY_CLASSES`** — it would add ~1,591
  ways and ~1,786 km of in-city arterials, tripling the file and competing with
  the choropleth on a map that has no basemap precisely so the data reads first.
- **The highway layer is many OPEN-ENDED corridors** (89 parts), by design: they
  run off the clip edge. Anything asserting closure — as the retired Henday ring
  check did — is asserting the wrong invariant. The live assertion is that the
  network **extends past the city on all four sides**
  (`verify-reference-layer.js`), falsified by clipping it to the city limit.
- **Hwy 216 measures 156 km in OSM vs the 149 km** the retired City-feed
  extraction produced for the ring's two carriageways. Agreement within ~5% is
  what justified dropping the hand-tuned extractor; `HIGHWAY_RING_REF_KM` warns
  if that drifts past 25%.
- **At the 60 km clip the river is a MultiPolygon** (disjoint stretches up- and
  downstream), where a narrow clip yields a single Polygon. Anything asserting
  its geometry type must accept both.
- **Municipal outlines are drawn UNDER the data**, with the river. The seven
  places sit outside Edmonton, so no hood polygon hides them (measured: 0–0.7%
  of each outline overlaps the city fabric) — and underneath they can never cut
  across a prism the way an over-composed line would.
- **The municipality service models legal STATUS, not size, so the seven places
  need THREE sublayers** — and the obvious single-layer implementation silently
  finds nothing for two of them:
  | Sublayer | Name | Field | Places |
  |---|---|---|---|
  | **78** | City | `CITY_NAME` | St. Albert, Spruce Grove, Fort Saskatchewan, Leduc, Beaumont |
  | **56** | Town | `TOWN_NAME` | Devon |
  | **66** | Urban Service Area | `USA_NAME` | Sherwood Park |
  **Sherwood Park is the trap:** it is not a town or a city but an urban
  service area of Strathcona County, so it is in neither 78 nor 56. (Distinct
  again from **104**, `Specialized Municipality`, which holds *Strathcona
  County itself* — see the Tier 3 boundary note.) **Beaumont has been a city
  since 2019**, so it is in 78 rather than 56.
- **Sublayer 66 also holds `Sherwood Park (Bremner)`**, a separate
  future-growth polygon ~10 km east. The query matches on **equality**, not a
  prefix or `LIKE` — a pattern match would pull Bremner in and drag the label
  anchor off the real town.
- **`PLACES` is a closed hand-written list, not a radius query.** Which names
  belong on the map is a cartographic judgement (how populated should the frame
  feel?), so it is stated rather than derived: a bbox sweep would silently gain
  and lose names as the province edits boundaries, and the map's composition
  would drift with it. A name that stops resolving **raises** rather than
  quietly shipping a map with a hole in its orientation.
- **Leduc is off the bottom edge at the default camera** (projects to y≈1102 in
  a 900px viewport at HOME zoom + 52° pitch) and is culled by the label
  declutterer. That is correct behaviour, not a missing label — it appears on
  pan or zoom-out. Anything asserting "all seven visible" will fail.

## Name Matching

Neighbourhood names between the two sources may not align exactly. Normalization (strip + uppercase) and the `NAME_CORRECTIONS` dict (keyed assessment name → boundary name) are applied in `load_assessment.py`, *before* aggregation — applying corrections after aggregation could collapse two summed rows onto one boundary and duplicate it. `join_and_calculate.py` then does a normalized exact match on the already-corrected names and flags whatever remains unmatched.

**Investigation script:** `scripts/investigate_neighbourhood_names.py`

### Confirmed correction dict (assessment name → boundary name)

```python
NAME_CORRECTIONS = {
    "ANTHONY HENDAY SOUTHEAST":        "ANTHONY HENDAY SOUTH EAST",
    "CHAPPELLE AREA":                   "CHAPPELLE",
    "EDMONTON RESEARCH AND DEVEL PARK": "EDMONTON RESEARCH AND DEVELOPMENT PARK",
    "HERITAGE VALLEY TOWN CENTRE AREA": "HERITAGE VALLEY TOWN CENTRE",
    "LEWIS FARMS INDUSTRIAL":           "LEWIS FARMS BUSINESS EMPLOYMENT",
    "PLACE LA RUE":                     "PLACE LARUE",
    "RAPPERSWIL":                       "RAPPERSWILL",
    "RIVER VALLEY WINDEMERE":           "RIVER VALLEY WINDERMERE",
    "SOUTHEAST (ANNEXED) INDUSTRIAL":   "SOUTHEAST INDUSTRIAL",
    "WESTBROOK ESTATE":                 "WESTBROOK ESTATES",
}
```

### Resolved

| Assessment name | Boundary name | Resolution |
|----------------|--------------|------------|
| `OLIVER` | `WÎHKWÊNTÔWIN` (#1151) | 2024 rename. Assessment data has already migrated: 12,234 rows / $4.12B are tagged `WÎHKWÊNTÔWIN` (matches the boundary directly), with a single straggler row still tagged `OLIVER` ($500 total). The unmatched warning is real but immaterial — no correction-dict entry added, since mapping it would shift $500 onto a $4.12B neighbourhood. |
| `HERITAGE VALLEY TOWN CENTRE AREA` | `HERITAGE VALLEY TOWN CENTRE` | Resolved 2026-07-01 (data-integrity audit): spatial containment — 945 of 946 properties fall inside the HVTC boundary polygon (1 in adjacent Desrochers). Before the correction the boundary matched only a 15-row / $2.25M slice under the exact name, rendering the hood at ~1/250th of its real $572.7M — a *partial* match, so the error was invisible on the map. Correction added. See `docs/FINDINGS_data_integrity_audit.md` §1. |
| `LEWIS FARMS INDUSTRIAL` | `LEWIS FARMS BUSINESS EMPLOYMENT` | Resolved 2026-07-01 (data-integrity audit): spatial containment — 100 of 103 properties ($106.3M) fall inside the LFBE polygon (3 spill into adjacent LEWIS FARMS, boundary-edge cases). Previously LFBE had zero matched rows → dropped at export → hole in the map. Correction added. See `docs/FINDINGS_data_integrity_audit.md` §2. |

### Unresolved

*None.* The only expected unmatched warning is the `OLIVER` straggler (immaterial, deliberate — see Resolved above). Any **other** name appearing in the unmatched warning is new drift and should be investigated (spatial containment via the assessment lat/lon columns is the decisive test). **This is now enforced in CI:** `scripts/check_unmatched_names.py` asserts the live money-path unmatched set equals the committed baseline `data/expected_unmatched.json` (`{OLIVER}` assessment-side, `{LEWIS FARMS}` boundary-side) and fails the weekly build on a new assessment-side name — see RUNBOOK §2 "Check unmatched names".

---

## Per-property zoning: use the POLYGONS, not `dkk9-cj3x`'s `zoning` field (2026-08-01)

Measured while building the revenue-lens readout (`src/revenue_by_zone.py`).

`dkk9-cj3x` ("Property Info") carries a `zoning` string per account, and joining
it to the assessment roll on `account_number` is clean — 1:1, no duplicates, every
tax class matched. **It is still the wrong source here.**

| | |
|---|---|
| properties with **null** `zoning` | **35.7%** (157,030 / 439,685) |
| **revenue** with null `zoning` | **16.0%** ($433M of $2.70B) |
| **DOWNTOWN**'s revenue with null `zoning` | **42%** |

The nulls are **condo units** — Downtown is 95% unzoned by property count. A
"top 3 zones by revenue" built on this field showed *unzoned* as Downtown's
largest single entry.

**The fix, and why it is better than a workaround:** every one of those
properties has coordinates (`latitude`/`longitude`, 100% non-null in the cleaned
assessment frame), and a point-in-polygon against `data/raw/zoning.geojson`
placed **11,022 / 11,022** of Downtown's unzoned properties. Citywide the
unplaced share falls from 16.0% to **0.002%** (8 properties, $9,034). Because
those are the *same* polygons the Uses lens colours by area, revenue-by-zone and
the Uses composition become one map read two ways and cannot disagree.

**Two traps found doing this, both silent:**
- `.str.split().str[0]` on an empty string yields **NaN, not `""`** — a
  "code is present but unmatched" filter written the obvious way silently
  swallows every null-zoning row, and reported 16.04% of revenue as sitting in
  three rare zone codes. It is 0.003%.
- `gpd.sjoin` where **both** frames carry a `zoning` column suffixes them to
  `zoning_left`/`zoning_right`, and the later lookup fails or silently reads the
  wrong side. Drop the left one first.

**Coverage of the category map:** 75 of the 78 codes present resolve through
`load_zoning.ZONE_CATEGORY`; the three that do not (`CSC`, `RSL`, `US`) carry
**0.003%** of revenue and fall to `other`, flagged.

⚠️ **1,585 properties sit exactly on a zone boundary** and match two polygons.
`sjoin` emits a row per match, so they must be de-duplicated or their levy is
double-counted and the per-hood fractions stop summing to 1.

## 15. Bike Routes (transportation lens, added 2026-08-02)
`vd4b-a4iv` ("Bike Routes") — on- and off-road cycling routes as
MultiLineStrings, EPSG:4326 via Socrata GeoJSON. **10,417 segments** on first
pull (2026-08-02); 8.0 MB raw. Feed is live and City-maintained (`updatedAt`
2026-07-27). Downloaded by `scripts/download_data.py` (`bike_routes`), both
truncation guards active (`$limit=20000`, server `count(*)` cross-check).
**Consumed by `src/load_bike.py`** → `bike_m_per_acre` (SPEC_services.md
"Transportation lens"). Carries no roll-year pin — like roads and transit its
provenance is `last_checked`.

### Key columns
- `classification` — the 12-value closed enumeration that decides what counts;
  see the table below. Mapped by an EXPLICIT dict (`CLASSIFICATION_GROUP`).
- `route_coming_soon` — real bool. **651 rows are `True`**: planned, not built.
- `type` — `ON ROAD` / `OFF ROAD`. Orthogonal to `classification` (Shared
  Pathway appears as both), so it is kept only as the internal
  `bike_m_onroad` / `bike_m_offroad` split, never as the classifier.
- `network_classification`, `road_segment_type`, `construction_year`,
  `street_name_full`, `duration`, `line_weight` — unused.

### What counts, and the two traps
Measured 2026-08-02, kilometres of built (not coming-soon) route:

| classification | km | group |
|---|---|---|
| Shared Pathway | 806.4 | **dedicated** |
| Shared Trail | 74.7 | **dedicated** |
| Protected Bike Lane | 56.7 | **dedicated** |
| Painted Bike Lane | 27.9 | **dedicated** |
| Local Street Bikeway | 7.9 | **dedicated** |
| Contra-Flow Bike Lane | 7.4 | **dedicated** |
| Shared Roadway - Lower Traffic | 194.7 | shared_roadway (excluded) |
| Shared Roadway - Higher Traffic | 76.4 | shared_roadway (excluded) |
| Bus / Bike / Taxi Lane | 9.0 | shared_roadway (excluded) |
| Walkway / Breezeway | 238.7 | pedestrian (excluded) |
| Maintenance Access | 1.9 | pedestrian (excluded) |
| Unclassified | — | unclassified (excluded; 100% coming-soon) |

⚠️ **TRAP 1 — "Shared Roadway" IS A ROAD, AND IT IS ALREADY COUNTED.** Those
280 km are ordinary streets carrying a bike-route designation. They add no
asset, and `load_roads` already counts their metres in `road_m_total`, so
including them double-counts the road network against itself. This is why the
two supply columns are safe to read side by side.

⚠️ **TRAP 2 — "Walkway / Breezeway" IS 3,031 ROWS OF PEDESTRIAN PATH**, the
second-largest classification in the whole feed. A naive "sum the bike routes"
metric is ~50% not-bike by length.

### Known Quirks
- **Unmatched classifications default to EXCLUDED**, the opposite of
  `load_roads`' default-to-local. The feed is mostly *not* bike infrastructure,
  so an unrecognised value is more likely another non-asset; defaulting in would
  let upstream drift silently inflate a supply metric. Warned loudly either way.
- **981 km kept, 1.17% falls outside every neighbourhood polygon** (conservation
  guard, well under the 5% warn threshold). **335 of 407 hoods** have any
  dedicated route; the other 72 are true zeros at the join.
- ⚠️ **The metric is 82% off-road pathway, much of it river-valley and ravine
  trail** — so `bike_m_per_acre` peaks in exactly the set-aside hoods that
  generate almost no revenue (top 4: MILL CREEK RAVINE NORTH/SOUTH, RIVER VALLEY
  WALTERDALE/GLENORA, all set-aside). Same shape as the `RATIO_ROAD_FLOOR`
  denominator artifact. The UI blurb says so.
- **`web/data/bike_routes.json`** (committed, lazy-loaded, 0.24 MB, 4,049 welded
  path segments) is the map's context layer — the LRT-lines format
  (`{"lines": [...]}`), geometry only, no per-feature value.

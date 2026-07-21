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
**"Since 2009"** button (gated on the `_long` columns); it is **choropleth-only** —
the 100 m detail grid stays on the 5yr/3yr windows because early-year permit
geocoding is sparse (a long-window CELL layer would under-render 2009–2015), while
the hood rollup joins on name and is complete regardless. Selecting it hides the
Detail toggle, like the industrial metric.

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
### Known Quirks
- **The fire term is a demand ALLOCATION of a mostly-fixed budget** — a hood with
  2× the events does not cost the City 2× (most fire cost is standing capacity).
  Carry that caveat in any UI copy.

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

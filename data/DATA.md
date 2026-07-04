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
| `year_built` | str | Nullable |
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
- **Condo `lot_size` semantics are INCONSISTENT (confirmed 2026-07-04)** — at the
  3,002 lat/long points holding multiple units, `lot_size` is sometimes the parcel
  size duplicated on every unit (summing overcounts the land), sometimes per-unit
  apportioned shares (summing is correct), and sometimes null/zero (one 1,059-unit
  building has nulls on 1,051 of them). No flag distinguishes the regimes. This is
  why the Glass view's grid export divides by cell GROUND acres, not lot acres
  (`src/export_value_grid.py`); a lot-acre variant needs a documented dedupe
  heuristic first (TODO.md).
- **Downloaded via `scripts/download_data.py --only property_info`** (added
  2026-07-04): full-CSV export endpoint, server count(*) cross-check; lands at
  `data/raw/Property_Info__Current_Calendar_Year_.csv`. Join to the assessment
  roll on `Account Number`: 100% coverage (439,685 rows both sides, 2026-07-04).

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

*None.* The only expected unmatched warning is the `OLIVER` straggler (immaterial, deliberate — see Resolved above). Any **other** name appearing in the unmatched warning is new drift and should be investigated (spatial containment via the assessment lat/lon columns is the decisive test).

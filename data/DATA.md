# Data Sources

Reference for raw input files. Update this file when you discover column name quirks, encoding issues, or anything unexpected. Do not rely on memory — write it down here.

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
year-matched mill rates (see `docs/SPEC_revenue.md`).
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

**Tax-exempt flag:** No explicit exempt boolean. Best proxy is `Assessment Class 1 == 'NONRES MUNICIPAL/RES EDUCATION'` (3 rows). Flag these on load as `is_exempt`.

### Known Quirks

- Condo units: multiple rows share one land parcel — this is expected and correct for this analysis
- `Suite` column has mixed types — always load with `low_memory=False`
- 46 rows have `Assessed Value == 0` — drop and flag count on load
- No explicit tax-exempt column; proxy is `Assessment Class 1 == 'NONRES MUNICIPAL/RES EDUCATION'`
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
- **Condo duplication TBC** — need to confirm whether multiple condo units on one parcel share a lot_size row or are duplicated. This matters for parcel-level $/acre aggregation.

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
- 407 boundary features vs 408 neighbourhoods in assessment aggregate. Actual join outcome: 3 assessment neighbourhoods with no boundary match (OLIVER, HERITAGE VALLEY TOWN CENTRE AREA, LEWIS FARMS INDUSTRIAL) and 2 boundary neighbourhoods with no assessment data (LEWIS FARMS, LEWIS FARMS BUSINESS EMPLOYMENT) → 405 of 407 boundaries rendered. See "Name Matching" below; flagged in `join_and_calculate.py`.

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

---

## Name Matching

Neighbourhood names between the two sources may not align exactly. Normalization (strip + uppercase) and the `NAME_CORRECTIONS` dict (keyed assessment name → boundary name) are applied in `load_assessment.py`, *before* aggregation — applying corrections after aggregation could collapse two summed rows onto one boundary and duplicate it. `join_and_calculate.py` then does a normalized exact match on the already-corrected names and flags whatever remains unmatched.

**Investigation script:** `scripts/investigate_neighbourhood_names.py`

### Confirmed correction dict (assessment name → boundary name)

```python
NAME_CORRECTIONS = {
    "ANTHONY HENDAY SOUTHEAST":        "ANTHONY HENDAY SOUTH EAST",
    "CHAPPELLE AREA":                   "CHAPPELLE",
    "EDMONTON RESEARCH AND DEVEL PARK": "EDMONTON RESEARCH AND DEVELOPMENT PARK",
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

### Unresolved (as of 2026-06-24)

| Assessment name | Boundary name | Issue |
|----------------|--------------|-------|
| `HERITAGE VALLEY TOWN CENTRE AREA` | *(no match)* | Possibly a new neighbourhood not yet in boundary file |
| `LEWIS FARMS INDUSTRIAL` | `LEWIS FARMS BUSINESS EMPLOYMENT` | Genuine rename or different polygon? Check `neighbourhood_number` |

These 2 are dropped from the join and flagged in `join_and_calculate.py` output. The lone `OLIVER` straggler is also flagged but is immaterial (see Resolved above).

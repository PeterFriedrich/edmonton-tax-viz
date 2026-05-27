# Data Sources

Reference for raw input files. Update this file when you discover column name quirks, encoding issues, or anything unexpected. Do not rely on memory — write it down here.

---

## 1. Property Assessment Data

**File:** `data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv` *(filename as delivered by the API)*
**Download:** `scripts/download_data.py`
**Source:** [Edmonton Open Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg) — dataset ID `q7d6-ambg`
**API URL:** `https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD`
**Format:** CSV, ~448,000 rows, updated annually (last confirmed: 2026-05-11)
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
- 407 features vs 408 neighbourhoods in assessment aggregate — expect ~1 unmatched; investigate in `join_and_calculate.py`

---

## Name Matching

Neighbourhood names between the two sources may not align exactly. Normalized exact match (strip + uppercase) is attempted first in `join_and_calculate.py`. Known mismatches are resolved via a correction dict in that module (keyed on assessment name → boundary name).

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

### Unresolved (as of 2026-05-27)

| Assessment name | Boundary name | Issue |
|----------------|--------------|-------|
| `OLIVER` | *(no match)* | May be listed under a different name in boundaries — check `descriptive_name` |
| `HERITAGE VALLEY TOWN CENTRE AREA` | *(no match)* | Possibly a new neighbourhood not yet in boundary file |
| `LEWIS FARMS INDUSTRIAL` | `LEWIS FARMS BUSINESS EMPLOYMENT` | Genuine rename or different polygon? Check `neighbourhood_number` |

These 3 will be dropped from the join and flagged in `join_and_calculate.py` output.

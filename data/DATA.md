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

## 2. Neighbourhood Boundaries

**File:** `data/raw/neighbourhoods.geojson` *(or `.shp` — confirm format on download)*
**Source:** [Edmonton ArcGIS](https://www.arcgis.com/home/item.html?id=558aec1b4d504f809cbbfa774c611230)
**Format:** GeoJSON or Shapefile
**CRS:** Likely WGS84 (EPSG:4326) — confirm on load, reproject to EPSG:3400 before area calculation

### Expected Columns

| Column | Type | Notes |
|--------|------|-------|
| `neighbourhood_name` | str | May differ in casing/spelling from assessment data — normalize on load |
| `geometry` | geometry | Polygon boundaries |

**Update this table with actual column names after first load.**

### Known Quirks

- *(Add quirks here as discovered)*

---

## Name Matching

Neighbourhood names between the two sources may not align exactly. Normalized exact match (strip + uppercase) is attempted first in `join_and_calculate.py`. If unmatched count is high after normalization, a correction dict lives in that module.

**Document confirmed mismatches here as they are found:**

| Assessment name | Boundary name | Resolution |
|----------------|--------------|------------|
| *(TBC)* | *(TBC)* | *(TBC)* |

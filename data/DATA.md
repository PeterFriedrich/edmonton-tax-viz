# Data Sources

Reference for raw input files. Update this file when you discover column name quirks, encoding issues, or anything unexpected. Do not rely on memory — write it down here.

---

## 1. Property Assessment Data

**File:** `data/raw/property_assessment.csv`
**Source:** [Edmonton Open Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg)
**Format:** CSV, ~448,000 rows, updated annually
**Licence:** Open Government Licence – City of Edmonton

### Expected Columns

To be confirmed on first load. Known relevant fields based on dataset documentation:

| Column | Type | Notes |
|--------|------|-------|
| `neighbourhood_name` | str | May have whitespace or casing inconsistencies — normalize on load |
| `assessed_value` | float | Some rows may be null or zero — flag and drop |
| *(tax-exempt flag)* | ? | Column name TBC — flag these rows, do not silently drop |

**Update this table with actual column names after first load.**

### Known Quirks

- Condo units: multiple rows share one land parcel — this is expected and correct for this analysis
- Tax-exempt properties (government, nonprofits) are included in the raw data — flag on load
- *(Add quirks here as discovered)*

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

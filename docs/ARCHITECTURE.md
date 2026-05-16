# Architecture: Edmonton Revenue Per Acre

Derived from `SPEC_phase1.md`. Describes module responsibilities, interfaces, and data flow.

---

## Data Flow

```
Raw CSV (assessment)         Raw GeoJSON (boundaries)
        |                            |
  load_assessment.py         load_boundaries.py
        |                            |
  DataFrame:                  GeoDataFrame:
  neighbourhood_name          neighbourhood_name
  assessed_value              geometry (projected)
        |                     area_acres
        |                            |
  aggregate_by_neighbourhood.py      |
        |                            |
  DataFrame:                         |
  neighbourhood_name                 |
  total_assessed_value               |
        \                           /
         \                         /
          join_and_calculate.py
                  |
          GeoDataFrame:
          neighbourhood_name
          total_assessed_value
          area_acres
          value_per_acre
          geometry
                  |
          plot_choropleth.py
                  |
          output/edmonton_value_per_acre.png
```

---

## Modules

### `src/load_assessment.py`

**Inputs:** path to raw assessment CSV

**Outputs:** `pd.DataFrame` with columns:
- `neighbourhood_name` (str, normalized — stripped, uppercased)
- `assessed_value` (float)

**Responsibilities:**
- Load CSV, select relevant columns
- Drop rows where `assessed_value` is null or zero (flag count to stdout)
- Normalize `neighbourhood_name` for joining (strip whitespace, uppercase)
- Flag tax-exempt properties (do not silently drop — print count and examples)

**Does not:** aggregate, join, or touch geometry

---

### `src/aggregate_by_neighbourhood.py`

**Inputs:** cleaned DataFrame from `load_assessment.py`

**Outputs:** `pd.DataFrame` with columns:
- `neighbourhood_name` (str)
- `total_assessed_value` (float)

**Responsibilities:**
- Group by `neighbourhood_name`, sum `assessed_value`
- No filtering or dropping here — that belongs upstream

**Does not:** touch geometry or know about boundaries

---

### `src/load_boundaries.py`

**Inputs:** path to neighbourhood boundary GeoJSON or Shapefile

**Outputs:** `gpd.GeoDataFrame` with columns:
- `neighbourhood_name` (str, normalized — stripped, uppercased)
- `geometry` (projected CRS — see CRS note below)
- `area_acres` (float, derived from projected geometry)

**Responsibilities:**
- Load boundary file
- Reproject to a suitable projected CRS for Alberta (EPSG:3400 — NAD83 / Alberta 10-TM Forest) before calculating area
- Calculate `area_acres` from projected geometry
- Normalize `neighbourhood_name` for joining

**CRS note:** Input is likely WGS84 (EPSG:4326). Always reproject explicitly — never assume input CRS is suitable for area calculation.

**Does not:** join assessment data or do any aggregation

---

### `src/join_and_calculate.py`

**Inputs:**
- Aggregated assessment DataFrame from `aggregate_by_neighbourhood.py`
- Boundary GeoDataFrame from `load_boundaries.py`

**Outputs:** `gpd.GeoDataFrame` with columns:
- `neighbourhood_name`
- `total_assessed_value`
- `area_acres`
- `value_per_acre`
- `geometry`

**Responsibilities:**
- Left join boundaries → assessment on `neighbourhood_name`
- Flag boundary neighbourhoods with no assessment match (print names)
- Flag assessment neighbourhoods with no boundary match (print names)
- Calculate `value_per_acre = total_assessed_value / area_acres`
- Guard against division by zero (flag, do not crash)

**Matching note:** Neighbourhood names between the two sources may not align exactly. A normalized exact match is attempted first. If unmatched count is high, a fuzzy match lookup table may be needed — that lives here as a correction dict, not in upstream modules.

---

### `src/plot_choropleth.py`

**Inputs:** joined GeoDataFrame from `join_and_calculate.py`

**Outputs:** saved image at configured output path

**Responsibilities:**
- Render choropleth using `value_per_acre` as the colour variable
- Use a perceptually uniform colormap (e.g. `YlOrRd`)
- Add title, colorbar with units ($/acre)
- Save to output path — do not show interactively
- No analysis logic here

**Does not:** calculate anything, filter data, or know about file paths beyond the output path it receives

---

### `main.py`

**Responsibilities:**
- Define input/output paths as constants at the top (no hardcoding deeper in)
- Call each module in order, passing outputs as inputs
- Single entrypoint: `python main.py`

---

## Key Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| CRS for area calc | EPSG:3400 (Alberta 10-TM Forest) | Equal-area, appropriate for Alberta, avoids distortion of WGS84 |
| Name normalization | Strip + uppercase | Cheapest reliable fix for whitespace/case mismatches |
| Tax-exempt handling | Flag, include | Analysis is of assessed value, not tax yield — exclusion would be a separate policy choice |
| Condo parcels | Include as-is | Multiple units on one land record inflates $/acre for high-rises, which reflects real density |
| Module boundaries | One file per processing step | Each step independently runnable and inspectable |

---

## Testing

### Structure

```
tests/
├── test_load_assessment.py
├── test_aggregate_by_neighbourhood.py
├── test_load_boundaries.py
├── test_join_and_calculate.py
└── test_plot_choropleth.py
```

Tests use `pytest`. All fixtures are synthetic — small inline DataFrames/GeoDataFrames. No real data files required, since raw data is not committed.

### What to test per module

**`test_load_assessment.py`**
- Null/zero `assessed_value` rows are dropped and count is printed
- Tax-exempt properties are flagged (not silently dropped)
- `neighbourhood_name` is normalized (strip + uppercase)

**`test_aggregate_by_neighbourhood.py`**
- Values for the same neighbourhood are summed correctly
- Output has exactly one row per neighbourhood

**`test_load_boundaries.py`**
- CRS is reprojected before `area_acres` is calculated (not after)
- `area_acres` is a positive float for valid polygons
- `neighbourhood_name` is normalized

**`test_join_and_calculate.py`**
- Boundary rows with no assessment match are flagged
- Assessment rows with no boundary match are flagged
- `value_per_acre` is calculated correctly
- Zero `area_acres` does not crash (flagged instead)
- Join is a left join on boundaries — no boundary rows silently dropped

**`test_plot_choropleth.py`**
- Output file is created at the specified path
- No analysis logic is called from within this module

---

## What's Not Here (Phase 1 Scope)

- Cost/expenditure side
- Interactive or web output
- Parcel-level granularity
- Per-ward breakdowns
- Any database or GIS software dependency

## Deployment Horizon

Phase 1 outputs a static PNG. The planned Phase 2 stack:

- Phase 1 pipeline outputs a **GeoJSON** (in addition to the PNG) — this is the handoff artifact
- **Kepler.gl** renders the GeoJSON as an interactive 3D hex bin map
- Exported as a **self-contained HTML file** hosted on **GitHub Pages** — no server, no backend
- If custom UI controls are needed (sliders, comparison tools), migrate to **deck.gl + React** at that point — not before

Phase 1 decisions to keep Phase 2 viable:
- No hardcoded paths
- Clean module boundary between analysis and rendering (`plot_choropleth.py` does not contain analysis logic)
- GeoJSON output from `join_and_calculate.py` should be straightforward to add alongside the PNG

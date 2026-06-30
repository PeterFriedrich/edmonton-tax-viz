# Architecture: Edmonton Revenue Per Acre

Derived from `SPEC_phase1.md`. Describes module responsibilities, interfaces, and data flow.

---

## Data Flow

```
Raw CSV (assessment)         Raw GeoJSON (boundaries)      Raw GeoJSON (zoning, fixa-tstc)
        |                            |                              |
  load_assessment.py         load_boundaries.py            load_zoning.py
        |  (+ class columns)         |   \________________________/  (overlay)
  apply_tax_rates.py  <-- mill_rates.json                  |  set_aside_frac, is_set_aside
        |  (+ per-property levy)     |                      |  (merged in join_and_calculate)
  DataFrame:                  GeoDataFrame:
  neighbourhood_name          neighbourhood_name
  assessed_value, levy        geometry (projected)
        |                     area_acres
        |                            |
  aggregate_by_neighbourhood.py      |
        |                            |
  DataFrame:                         |
  neighbourhood_name                 |
  total_assessed_value               |
  total_revenue                      |
        \                           /
         \                         /
          join_and_calculate.py
                  |
          GeoDataFrame:
          neighbourhood_name
          total_assessed_value, total_revenue
          area_acres
          value_per_acre, revenue_per_acre
          geometry
                 / \
                /   \
   plot_choropleth.py  export_geojson()
        |                   |
  output/...png        web/data/...geojson  (both metrics → web toggle)
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
- Apply `NAME_CORRECTIONS` (assessment name → boundary name) *before* aggregation, so names that collapse to one boundary are summed rather than duplicated at the join
- Flag tax-exempt properties (do not silently drop — print count and examples)

**Does not:** aggregate, join, or touch geometry

---

### `src/apply_tax_rates.py` (revenue phase)

**Inputs:** cleaned DataFrame from `load_assessment.py`; path to `data/mill_rates.json`; assessment year

**Outputs:** the same DataFrame with a per-property `levy` column (float, dollars) appended

**Responsibilities:**
- Load municipal mill rates for the year from `mill_rates.json` (keyed by year + class — not hardcoded)
- Compute `levy = assessed_value × Σ_slot (pct/100) × (rate[class]/1000)` over the up-to-3 split-class slices
- Bridge the two class vocabularies (`COMMERCIAL` → `Non Residential`, etc. — see `docs/FINDINGS_assessment_classes.md`); exempt slices → $0
- Flag (don't drop/normalize) rows whose class %s don't sum to 100; hard-error on an unmapped class label

**Does not:** aggregate, join, or touch geometry. Skipped entirely on the Phase 1 (value-only) path — `aggregate`/`join` degrade gracefully when `levy`/`total_revenue` is absent.

---

### `src/aggregate_by_neighbourhood.py`

**Inputs:** cleaned DataFrame from `load_assessment.py` (optionally with `levy` from `apply_tax_rates.py`)

**Outputs:** `pd.DataFrame` with columns:
- `neighbourhood_name` (str)
- `total_assessed_value` (float)
- `total_revenue` (float) — only when `levy` is present (revenue phase)

**Responsibilities:**
- Group by `neighbourhood_name`, sum `assessed_value` (and `levy` → `total_revenue` if present)
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

### `src/load_zoning.py` (land-use layer — added 2026-06-29, design stage)

**Inputs:** path to the zoning GeoJSON (`fixa-tstc`, see `DATA.md` §5); the boundary
GeoDataFrame from `load_boundaries.py` (needs projected geometry for the overlay)

**Outputs:** `pd.DataFrame` keyed by `neighbourhood_name`:
- `set_aside_frac` (float 0–1) — share of neighbourhood area that is never/not-yet land
- `is_set_aside` (bool) — `set_aside_frac >= 0.90`
- land-use composition columns (developed vs never/not-yet categories) + a dominant
  set-aside reason label for the tooltip

**Responsibilities:**
- Load zoning polygons, reproject to **EPSG:3400** (CRS set explicitly, per project
  rule), clean geometry (`buffer(0)`; drop non-polygonal parts — raw municipal
  polygons fail GEOS overlay otherwise)
- Map zone code → land-use category via an **explicit `code → category` dictionary**
  (NOT keyword/prefix heuristics — place-names like "Energy & Technology *Park*" and
  the `A*` river-valley codes break fuzzy matching; see `FINDINGS_revenue_scale.md`)
- Spatial-overlay zoning × neighbourhoods; sum intersection area by category →
  composition %; derive `set_aside_frac` from never+not-yet categories
- **Set-aside = never (River Valley/Natural/Parks) + not-yet (Future/rural/reserve)**,
  threshold 0.90 (decision in `SPEC_revenue.md`)

**Does not:** touch assessment/revenue values or fit the colour scale (that's a
display decision downstream). Zoning is a **refreshed input** — re-pull each cycle so
developing land graduates off the set-aside list automatically (see SPEC_deployment.md).

---

### `src/join_and_calculate.py`

**Inputs:**
- Aggregated assessment DataFrame from `aggregate_by_neighbourhood.py`
- Boundary GeoDataFrame from `load_boundaries.py`
- (optional) zoning composition DataFrame from `load_zoning.py` — merged on
  `neighbourhood_name`, adding `set_aside_frac` / `is_set_aside` to the output (and
  thus the GeoJSON). Degrades gracefully when absent, like the revenue columns.

**Outputs:** `gpd.GeoDataFrame` with columns:
- `neighbourhood_name`
- `total_assessed_value`
- `total_revenue` — only on the revenue path (when `aggregate` produced it)
- `area_acres`
- `value_per_acre`
- `revenue_per_acre` — only on the revenue path
- `geometry`

**Responsibilities:**
- Left join boundaries → assessment on `neighbourhood_name`
- Flag boundary neighbourhoods with no assessment match (print names)
- Flag assessment neighbourhoods with no boundary match (print names)
- Calculate `value_per_acre = total_assessed_value / area_acres` (and `revenue_per_acre = total_revenue / area_acres` when present — both metrics, web toggle)
- Guard against division by zero (flag, do not crash)

**Matching note:** Neighbourhood names between the two sources may not align exactly. Normalization (strip + uppercase) and the `NAME_CORRECTIONS` lookup are applied upstream in `load_assessment.py`, before aggregation — applying corrections after aggregation risks collapsing two summed rows onto one boundary and duplicating it. This module attempts a normalized exact match on the already-corrected names and flags whatever remains unmatched.

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

## Notebooks

```
notebooks/
├── exploration/    # scratch — understanding the data
└── analysis/       # deeper dives, feature work, model experiments
```

Notebooks are for exploration and visualization only. They call `src/` modules rather than reimplementing logic. Notebook outputs (cell results, plots) are not committed — use `nbstripout` or strip manually before committing.

---

## What's Not Here (Phase 1 Scope)

- Cost/expenditure side
- Interactive or web output
- Parcel-level granularity
- Per-ward breakdowns
- Any database or GIS software dependency

## Deployment Horizon

The Python pipeline is stable across all phases — only the rendering layer changes.

| Phase | Rendering | Hosting |
|-------|-----------|---------|
| 1 | matplotlib → static PNG | local |
| 2 | MapLibre GL JS + deck.gl → static HTML | GitHub Pages |
| 3 | deck.gl + React | TBD — only if Phase 2 insufficient |

**Phase 2 design decisions:**
- **MapLibre + deck.gl directly** — Kepler.gl is just a UI wrapper around deck.gl; going direct gives full control over camera, layer styling, and interaction without the constraints
- **Extruded PolygonLayer** (not H3 hex bins) — neighbourhood boundary shapes are meaningful to Edmonton readers; height = `value_per_acre`
- **No basemap for v1** — neighbourhood polygons on a dark background are self-describing. Add CARTO Dark Matter free tiles if geographic context is needed; no R2 or Protomaps required at this traffic level
- **No scheduled preprocessor** — assessment data updates once a year. Pipeline runs locally (or via oracle server cron), outputs updated GeoJSON, commit to repo. GitHub Pages picks it up automatically.

**Phase 2 handoff:** `join_and_calculate.py` exports a slim GeoJSON via `export_geojson()` — only `neighbourhood_name`, `value_per_acre`, and `geometry`, reprojected to EPSG:4326 (deck.gl/MapLibre expect lon/lat). No changes to upstream modules needed.

**Web app layout & export target:** The Phase 2 app lives in `web/` (`web/index.html` + `web/data/`). The export writes to **`web/data/neighbourhood_value_per_acre.geojson`** — a *tracked, served* location — NOT `output/` (which is gitignored as throwaway artifacts and cannot be served by Pages). `main.py` must point the GeoJSON export at `web/data/`, so each run regenerates the committed served file in place. The PNG stays in `output/` as a static fallback.

**GitHub Pages serves only from repo root or `docs/`, not `web/`.** To keep the clean `web/` layout while still publishing, the intended path is a GitHub Action (`.github/workflows`) that serves `web/`. Alternatives if the Action is undesired: move the app to `docs/` or root. Decided at deploy time (Phase 2 step 4).

**Phase 2 theming & accessibility** (palette, light mode, colourblind mode) lives in `UI.md`. **Render/performance** tradeoffs (vertex count, simplify, outline cost) live in `PERFORMANCE.md`.

**Phase 2 visual tuning (2026-06-25):**
- **Camera — zoom out (+ proportional height bump, bundled, DEFERRED).** Initial view was too tight; neighbourhoods read as crowded. Pull the starting `zoom` back (~10.2 → ~9.4). To be applied together with a *proportional* `ELEVATION_SCALE` increase (global multiplier — every column taller by the same factor, so height ratios stay honest; this is NOT the super-linear power curve below). Both held until we tune them together against the zoomed-out view. Pure camera + uniform scale, no data impact.
- **Setbacks / inter-column gaps (DECIDED + IMPLEMENTED, display-only).** Shrink each polygon inward (negative buffer in EPSG:3400) before export so extruded columns don't touch — reads like city blocks rather than a solid mass. Landed at **45 m** (tested 20→35→50; zero polygon collapses at any value up to 50 m — Edmonton polygons are chunky). This is **display geometry only**: `value_per_acre` is computed from true area upstream and is unaffected. Lives as the `setback_m` param on `export_geojson()` (`_apply_setback()` helper) so the PNG pipeline is untouched. Sliver neighbourhoods that collapse to empty/invalid under the negative buffer fall back to the original shape, logged (no silent drops).
- **Geometry simplification (DECIDED + IMPLEMENTED, display-only).** **Vertex count is the dominant render-cost lever** for the iGPU baseline audience (see `PERFORMANCE.md`). A Douglas–Peucker simplify (`shapely.simplify`, `preserve_topology=True`) in EPSG:3400, applied *after* the setback. Same family as the setback: **display geometry only** (`value_per_acre` is from true area upstream), the `simplify_tolerance_m` param on `export_geojson()`, logging the vertex reduction + any empty/invalid fallback (no silent changes). **Landed at 10 m** — chosen from an empirical sweep (vertices vs max boundary shift vs file size): 10 m cuts the boundary vertex count **84%** with a max boundary shift of ~11 m, invisible at city zoom and well under the 45 m setback. Tolerance must stay under the setback to avoid shifting the gaps (30 m's ~47 m shift exceeded it — rejected).
- **Transform order: setback THEN simplify (matters).** Simplify runs *last* so the final Douglas–Peucker pass also collapses the rounded-corner vertices the negative buffer adds. Order matters a lot for the served file: setback→simplify gives **9,229 vertices / 0.49 MB**, whereas simplify→setback leaves **38,607 vertices / 1.84 MB** (the buffer re-inflates a simplified shape). The only cost of this order is buffering full-resolution geometry at export time — a once-a-year non-issue. (`value_per_acre` is from true upstream area regardless of order.)
- **Spike emphasis — taller spikes relative to small ones (OPEN, NOT decided).** Want Downtown / high-value districts to stand out more vs the mid-band. A *global* `ELEVATION_SCALE` increase raises everything proportionally (won't separate the top); only a **super-linear transform** (`value^k`, k>1) actually pulls spikes away from the pack. **Tension:** Phase 1 deliberately chose **linear elevation because it is honest** ("Downtown's spike IS the story"). A power curve exaggerates — at k=2 a 2× district looks ~4× taller — which is a real risk for a civic analysis that will be scrutinised. **Held as a note; revisit alternatives later** (mild k≈1.3–1.5 + legend disclosure, vs keeping linear and solving crowding via zoom + setbacks alone). Do NOT implement until chosen.

Phase 1 decisions that keep this viable:
- No hardcoded paths
- No analysis logic in `plot_choropleth.py` — rendering only, swappable
- Clean module boundaries so GeoJSON export can be added to `join_and_calculate.py` without touching other modules

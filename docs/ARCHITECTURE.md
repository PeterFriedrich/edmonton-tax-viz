# Architecture: Edmonton Revenue Per Acre

Derived from `SPEC_phase1.md`. Describes module responsibilities, interfaces, and data flow.

---

## Data Flow

```
Raw CSV (assessment)         Raw GeoJSON (boundaries)      Raw GeoJSON (zoning, fixa-tstc)
        |                            |                              |
  load_assessment.py         load_boundaries.py            load_zoning.py
        |  (+ class columns)         |   \________________________/  (overlay)
  apply_tax_rates.py  <-- mill_rates.json                  |  set_aside_frac, is_set_aside, is_residential
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

**Also in the flow (services lens, built 2026-07-01):** `load_roads.py` enters the
diagram exactly where `load_zoning.py` does — a raw GeoJSON (`9j8t-zm52`) overlaid
against the boundary frame, producing per-hood columns merged in
`join_and_calculate` (`road_m_total`; `road_m_per_acre` computed there).

**Also in the flow (Glass-view grid, 2026-07-04/05):** a side branch that never
touches the hood join — `main.py` takes the PER-PROPERTY frame (post
`apply_tax_rates`), merges `load_property_info.py`'s `account_number → lot_size`
onto it, runs `check_lot_acre_bounds` against the boundary frame (physical-bound
validation, raises on new violations), and hands it to `export_value_grid.py`
for the 100 m cell file (`web/data/value_grid.json`, ground- AND lot-acre
metrics). Absent property-info file → ground-acre only.

**Also in the flow (stormwater lens, built 2026-07-05):** `load_stormwater.py`
reads the property-info CSV directly (per-point A × I × R charge model — see
its module entry) with a `fixa-tstc` point-in-polygon fallback for zone-null
rows, and produces per-hood columns merged in `join_and_calculate`
(`storm_charge_annual`; `storm_charge_per_acre` computed there). Rates come
from `data/stormwater_rates.json`, year-keyed like `mill_rates.json`.

**Also in the flow (fire lens, built 2026-07-06):** `load_fire.py` reads the
fire-response CSV (`7hsn-idqi` — the neighbourhood comes pre-joined, so no
overlay) and produces a per-hood column merged in `join_and_calculate`
(`fire_events_per_year`; `fire_events_per_acre` computed there). It also
exports the 31 station points (`b4y7-zhnz`) to `web/data/fire_stations.json`
for the Services view's context dots.

**Also in the flow (transit lens, built 2026-07-11):** `load_transit.py`
reads the five GTFS tables (DATA.md §9) and the boundary frame (stop
point-in-polygon) and produces a per-hood column merged in
`join_and_calculate` (`transit_dep_total`; `transit_dep_per_acre` computed
there). It also exports the location_type-1 stations (LRT + transit
centres) to `web/data/transit_stations.json` for the Services view's
context dots. Full module section below.

**Also in the flow (water lens, built 2026-07-07):** `load_water.py` reads
the assessment CSV (scope classes, roll points) plus the property-info CSV
(gross floor area for multi-res unit estimates) and produces two per-hood
columns merged in `join_and_calculate` (`water_charge_annual` +
`water_fixed_annual`; the per-acre pair computed there). Rates come from
`data/water_rates.json`, year-keyed — but the tariff vintage is pinned
independently of the roll year (`WATER_RATE_YEAR` in main.py; a modeled
forward-looking bill, unlike mill rates). Residential scope only
(SPEC_utilities Lens 2, locked 2026-07-06).

**Also in the flow (franchise lens, built 2026-07-07):** `load_franchise.py`
reuses `load_water.build_connections` (extracted as a shared helper so the two
lenses share ONE dwelling model — 551,831) and produces five per-hood columns
merged in `join_and_calculate` (`FRANCHISE_COLUMNS`: `dwelling_count` plus the
modeled electricity/gas distribution + franchise-fee revenue). Rates in
`data/franchise_rates.json` (`FRANCHISE_RATE_YEAR`). **Columns only — no
display layer** (they're collinear with dwelling count; SPEC_utilities Lens 3),
so they are carried on the full frame but kept OUT of `SLIM_COLUMNS` with no
per-acre derived. The value is the citywide City-revenue totals + per-hood
attribution.

**One metric family exists ONLY in the browser:** the Ratio view's per-service
ratios — revenue per road metre (`revenue_per_acre / road_m_per_acre`) and,
since 2026-07-10, revenue per fire event (`/ fire_events_per_acre`), a
denominator picker (`RATIO_DENOMS`) — the acres cancel in both. They are
derived client-side in `web/index.html` from published GeoJSON columns. No
pipeline stage computes or exports them; scale anchors (log-colour p2.5–p97.5,
height parity) are computed at page load from the served data (`ratioScale()`,
cached per denominator), so they track weekly refreshes automatically — one
anchor pair per denominator for the full kept subset, one for the residential
lens (2026-07-03). Transform decisions + the artifact floors (roads 5 m/acre,
fire 0.005 events/acre/yr) + the residential anchors: FINDINGS §6.4 / §6.7.
Why only levy-funded denominators are offered: SPEC_utilities decision 3.

---

## Modules

### `src/load_assessment.py`

**Inputs:** path to raw assessment CSV

**Outputs:** `pd.DataFrame` with columns:
- `account_number` (int — join key to property-info `dkk9-cj3x`; feeds the
  grid export's lot_size merge in `main.py`)
- `neighbourhood_name` (str, normalized — stripped, uppercased)
- `assessed_value` (float)
- `latitude` / `longitude` (float — the property point; feeds the grid export,
  0 nulls as of 2026-07)

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

### `src/load_zoning.py` (land-use layer — added 2026-06-29)

**Inputs:** path to the zoning GeoJSON (`fixa-tstc`, see `DATA.md` §5); the boundary
GeoDataFrame from `load_boundaries.py` (needs projected geometry for the overlay)

**Outputs:** `pd.DataFrame` keyed by `neighbourhood_name`:
- `set_aside_frac` (float 0–1) — share of neighbourhood area that is never/not-yet land
- `is_set_aside` (bool) — `set_aside_frac >= 0.90`
- `set_aside_reason` (str) — dominant set-aside category label for the tooltip; "" if not
- `frac_residential` / `is_residential` — residential share of zoned area + `>= 0.50`
  flag (residential-only lens; orthogonal to `is_set_aside`, added 2026-07-01)
- land-use composition columns (`frac_never`/`frac_notyet`/`frac_inst`/`frac_residential`/
  `frac_commercial`/`frac_industrial`/`frac_mixed`/`frac_dc`/`frac_other`, shares of
  zoned area, sum to 1 — the use-mix view's input; nonres split 4 ways 2026-07-03,
  ambiguous codes resolved from bylaw purpose statements, DATA.md §5)
- `frac_nonres` — sum of com/ind/mix/dc/other (the pre-split bucket, kept for continuity)

**Responsibilities:**
- Load zoning polygons, reproject to **EPSG:3400** (CRS set explicitly, per project
  rule), clean geometry (`buffer(0)`; drop non-polygonal parts — raw municipal
  polygons fail GEOS overlay otherwise)
- Map zone code → land-use category via an **explicit `code → category` dictionary**
  (`never`/`notyet`/`inst`/`res`/`nonres`; NOT keyword/prefix heuristics — place-names
  like "Energy & Technology *Park*" and the `A*` river-valley codes break fuzzy
  matching; see `FINDINGS_revenue_scale.md`)
- Spatial-overlay zoning × neighbourhoods; sum intersection area by category →
  composition %; derive `set_aside_frac` from never+not-yet and `frac_residential`
  from the `res` category
- **Set-aside = never (River Valley/Natural/Parks) + not-yet (Future/rural/reserve)**,
  threshold 0.90 (decision in `SPEC_revenue.md`)

**Does not:** touch assessment/revenue values or fit the colour scale (that's a
display decision downstream). Zoning is a **refreshed input** — re-pull each cycle so
developing land graduates off the set-aside list automatically (see SPEC_deployment.md).

**Also exports (added 2026-07-03):** `export_zoning_web(zoning_path, boundaries,
out_path)` — the Uses-view ground layer (`web/data/zoning.geojson`, committed):
the raw zoning polygons dissolved **citywide** into one MultiPolygon per
land-use category, **clipped to the setback-shrunk neighbourhood footprints**
(45 m — the same "city block" gaps the prisms carry, so the hood unit stays
visible; collapsed slivers keep their full footprint, logged), simplified 10 m,
coordinates snapped to the 1e-5 grid **topology-aware** (`shapely.set_precision`
— plain rounding after a validity pass re-introduces degenerate rings that break
the browser's tessellator), single `u` prop (category key). Shares
`_load_categorized()` with `load_zoning` (the raw file is read once per entry
point — same accepted pattern as `load_roads`' `_prepare_segments`). Display
geometry only — all published composition metrics come from the full-resolution
overlay.

---

### `src/load_roads.py` (services lens — added 2026-07-01)

Full methodology + locked decisions in `docs/SPEC_services.md`; dataset quirks
in `DATA.md` §6. Built to this contract (13 synthetic tests).

**Inputs:** path to the Road Network GeoJSON (`9j8t-zm52`, centreline
LineStrings; `DATA.md` §6); the boundary GeoDataFrame from
`load_boundaries.py` (projected geometry for the overlay)

**Outputs:** `pd.DataFrame` keyed by `neighbourhood_name`:
- `road_m_collector` / `road_m_local` (float, metres) — city-maintained
  centreline length within the hood, by class group
- `road_m_arterial` (float, metres) — **internal only**: computed and carried
  (conservation guard, possible later views) but NEVER included in the metric
- `road_m_total` (float) — **collector + local only** (arterials excluded:
  shared infrastructure — see SPEC_services.md; alleys/railway excluded at the
  row filter)

(`road_m_per_acre = road_m_total / area_acres` is computed downstream in
`join_and_calculate`, boundary-acre denominator — same acre as value/revenue.)

**Responsibilities:**
- Load centrelines; **filter rows**: `centerline_type == "Road"` (drops all
  alleys + railway) and `responsible_party_description == "City of Edmonton"`
  (drops provincial/private/rail/neighbouring-municipality segments)
- Reproject to **EPSG:3400** (CRS set explicitly before any length calculation)
- Map `functional_class_code` → class group via an **explicit code → group
  dictionary** (arterial/collector/local; same philosophy as `ZONE_CATEGORY` —
  every code hand-assigned, unknown codes warn loudly, no prefix heuristics)
- Verify the null-class invariant: after the Road filter, every row has a
  functional class (nulls = alleys + railway exactly, confirmed 2026-07-01)
- Overlay lines × boundary polygons (`how="intersection"`,
  `keep_geom_type=True`), sum clipped `.length` per (hood, class group)
- **Conservation guard (no silent drops):** post-overlay total length ≈
  pre-overlay filtered total within tolerance; report unassigned remainder
  (segments outside any hood) explicitly

**Does not:** weight classes by cost, compute ratios against revenue (that's
the V2 fast-follow, a downstream/display concern), or touch assessment data.
Like zoning, roads are a **refreshed input** (weekly CI re-pull; vintage in
status.json).

**Also exports (added 2026-07-02):** `export_roads_web(roads_path, boundaries,
out_path)` — the ground-layer GeoJSON the web map renders
(`web/data/roads.geojson`, committed; SPEC_services.md "Display architecture").
Shares the load→filter→classify→clip front half with `load_roads` via
`_prepare_segments()` (the raw file is read twice per pipeline run — accepted,
keeps the two entry points independent). Access roads dissolve to one
MultiLineString per neighbourhood (they carry the per-hood colour value);
arterials dissolve CITYWIDE into a single no-metric context feature (per-hood
clipping only chops them at boundary crossings). Both are welded end-to-end
(`linemerge` — raw segments average ~2 vertices, so simplify has nothing to
drop until streets are merged into longer lines), simplified (access 20 m /
arterial 40 m), thinned of sub-20 m access clip slivers (reported, not
silent), and written with coordinates rounded to 5 dp and props `n` / `t` /
`v` (hood name, null on the arterial feature / `"arterial"`|`"access"` /
`road_m_per_acre` on access only). Display geometry only — all published
metrics still come from `load_roads`, computed before any thinning.

---

### `src/load_property_info.py` (lot-size join — added 2026-07-05)

**Inputs:** the property-info CSV (`dkk9-cj3x`,
`data/raw/Property_Info__Current_Calendar_Year_.csv`)

**Outputs:** DataFrame `account_number` / `lot_size` / `gross_area` (both m²,
non-positive → NaN, nulls counted and reported). `gross_area` (source
`Total Gross Area`, added 2026-07-13) is the Development Lens B FAR numerator
(built floor area). Raises if the account key stops being unique. Deliberately
slim — `year_built` etc. stay out until the diversity analysis needs them
(ANALYSIS_BACKLOG 4). Does NOT resolve the condo `lot_size` inconsistency; that
lives with its consumer (`export_value_grid._point_lot_stats`).

### `src/export_value_grid.py` (Glass-view spikes — added 2026-07-04; lot-acre variant 2026-07-05)

**Inputs:** the per-property DataFrame from `load_assessment.py` (needs
`latitude`/`longitude`/`assessed_value`; `levy` optional from
`apply_tax_rates.py`; `lot_size` optional — `main.py` merges it in from
`load_property_info.py` on `account_number`); output path; `cell_m`
(default 100.0, pinned as `GRID_CELL_M` in `main.py`)

**Outputs:** compact flat-JSON web file (`web/data/value_grid.json`): one row
per occupied grid cell — `[lon, lat, value_per_acre, revenue_per_acre,
value_per_lot_acre, revenue_per_lot_acre]` at the cell's SW corner
(`revenue_*` omitted on the value-only path; `*_per_lot_acre` omitted when
`lot_size` is absent; lot-acre slots `null` where the cell has no eligible
lot acres). ~34.7k cells / 1.8 MB on current data. Returns a stats dict.

**Responsibilities:**
- Bin property points into `cell_m` squares in **EPSG:3400** (CRS explicit,
  per project rule); sum value (and levy) per cell
- **Ground-acre metrics** (always): divide by the cell's fixed area —
  consistent with the hood metrics' boundary-acre denominator. This is **this
  project's own cardinality-robust default, NOT Urban3 lineage** (audit Q6,
  docs/FINDINGS_denominator_cardinality.md §Q5): Urban3 divides by *parcel*
  area, so their denominator is closer to lot-acre below. Ground-acre earns its
  place by being immune to the record-to-parcel bugs, not by matching Urban3.
  Known cost: large parcels needle (one point per account — DATA.md §2, WEM).
- **Lot-acre metrics** (when `lot_size` is present): divide ELIGIBLE dollars
  by deduped parcel acres — the Urban3 land-productivity metric. Dedupe =
  the repeat-aware heuristic of docs/FINDINGS_lot_dedupe.md
  (`_point_lot_stats` / `SHARE_MAX_M2`); majority-null multi-unit points are
  ineligible (excluded from numerator AND denominator, count + value
  reported).
- `check_lot_acre_bounds(df, boundaries)`: physical-bound validation —
  per-hood deduped lot acres ≤ boundary acres, `KNOWN_BOUND_OUTLIERS`
  (PEMBINA) exempt; RAISES on any new violation. `main.py` runs it before
  every lot-acre export.
- No silent drops: null-coordinate rows counted and reported; lot-ineligible
  points reported with their value; a conservation guard errors if cell sums
  don't reproduce the input totals

**Does not:** pick colour/height scales — the browser computes the cell
clamp (p97.5) and elevation parity from the served file at load
(`gridScale()` in `web/index.html`, same pattern as `ratioScale()`), so they
track weekly refreshes.

**Also exports (added 2026-07-08):** `build_hood_lot_acres(df)` — the same
lot-dedupe rollup one level up, at the NEIGHBOURHOOD unit, for the Money view's
lot-acre denominator toggle. Takes the per-property frame
(`neighbourhood_name`/`latitude`/`longitude`/`lot_size`/`assessed_value`,
optional `levy` and `gross_area`), reuses `_point_lot_stats`/`SHARE_MAX_M2`, and
returns per-hood `lot_acres_eligible` + `value_lot_eligible`
(+ `revenue_lot_eligible`), the eligible-point deduped acres and the dollars at
those points. When `gross_area` is present it also returns `far` (Development
Lens B built floor-area ratio = Σ floor area over eligible-point rows ÷ deduped
lot m²; low FAR = underused/suitable — SPEC_development Lens B). `main.py` builds
it from the same `grid_input` (assessment + `load_property_info`) that feeds the
grid, and hands it to `join_and_calculate` — which divides + guards (below);
`far` rides through UNSUPPRESSED (a density ratio, not a per-lot-acre dollar).
Ineligible points are excluded from BOTH numerator and denominator and reported.

### `src/load_stormwater.py` (utility lens #1 — added 2026-07-05)

Full methodology + open decisions in `docs/SPEC_utilities.md` Lens 1; tariff
source `docs/utility_cost_estimation_lens_methods.md` §C. **Everything this
module outputs is MODELED (bylaw formula on open data), not billed.**

**Inputs:** the property-info CSV (`dkk9-cj3x` — needs `zoning`, `lot_size`,
`Latitude`/`Longitude`, `Neighbourhood`; mixed header casing, DATA.md §2);
optional path to the zoning GeoJSON (`fixa-tstc`) for the zone-null spatial
fallback; `data/stormwater_rates.json` (rate by year — same year-keyed
pattern as `mill_rates.json`); the assessment year (rates must match the
roll year, like mill rates).

**Outputs:** `pd.DataFrame` keyed by `neighbourhood_name`:
- `storm_lot_m2` (float) — Σ eligible deduped parcel area
- `storm_effective_m2` (float) — Σ A × I × R (rate-independent quantity)
- `storm_charge_annual` (float, $/yr) — `storm_effective_m2` × annualized rate

(`storm_charge_per_acre = storm_charge_annual / area_acres` is computed
downstream in `join_and_calculate`, boundary-acre denominator — same acre as
every other per-acre metric. As of 2026-07-05 it is in `SLIM_COLUMNS` and
ships in the web GeoJSON — the Services view's stormwater plane reads it;
the raw `storm_*` totals stay out of the slim file like every other total.)

**Responsibilities:**
- Compute the Bylaw 20865 daily stormwater charge per PROPERTY POINT:
  `A × I × R × rate`, I = 1.0 (`intensity_default`; SIAP reductions out of
  scope v1), annualized per the rate's unit (monthly × 12 / daily × 365)
- **A (parcel area):** group rows by exact lat/long and reuse
  `export_value_grid._point_lot_stats` — the repeat-aware condo dedupe
  (FINDINGS_lot_dedupe) IS the bylaw's per-unit apportionment read back;
  majority-null multi-unit points are ineligible, excluded + REPORTED
  (accepted cross-module helper use, like `load_roads._prepare_segments`)
- **R (runoff coefficient):** explicit `ZONE_RUNOFF` dict — every base code
  hand-assigned (same philosophy as `ZONE_CATEGORY`), verified Bylaw-table
  rows marked, special-area codes assigned by closest-aligned zone (the
  bylaw's own rule for unlisted zones); lot-size splits (<450/>450 m² res,
  <700/>700 m² DC) applied against the point's deduped area; unknown codes
  warn loudly, excluded + reported
- **Zone resolution order (each path's count reported):** (1) the row's own
  `zoning` column (first token); (2) modal zone among rows at the same
  point; (3) point-in-polygon against the `fixa-tstc` polygons (EPSG:3400,
  explicit CRS) — never the stale historical layer `67p2-r285`;
  (4) unresolved → excluded + reported
- Aggregate points → hood via the CSV's `Neighbourhood` column (strip +
  uppercase + `NAME_CORRECTIONS` from `load_assessment`, applied BEFORE
  aggregation, same rule as everywhere)
- No silent drops: every exclusion (ineligible lot, unknown zone,
  unresolved zone, null coordinates) counted + reported with area/value

**Known limitation (same as revenue):** the roll omits exempt institutional
land entirely, so hood totals understate where exempt land dominates —
recorded, not corrected.

**Does not:** decide display (open decision — SPEC_utilities), apply SIAP/LID
credits, project forward rates (PBR escalation out of scope), or claim
billing accuracy for any specific address.

---

### `src/load_fire.py` (services lens #3 — added 2026-07-06)

Full methodology + the four locked decisions in `docs/SPEC_services.md`
"Fire lens"; dataset facts in `DATA.md` §7–8. **Demand metric only** — the
data has no on-scene-arrival timestamp, so no response-time/coverage claim
is buildable (locked; don't oversell).

**Inputs:** the fire-response CSV (`7hsn-idqi`, `data/raw/fire_response.csv`
— snake_case API headers from the resource endpoint); the year window
(pinned as `FIRE_YEARS` in `main.py` — the last 3 FULL calendar years,
bumped manually each January so a partial year never dilutes the average).

**Outputs:** `pd.DataFrame` keyed by `neighbourhood_name`:
- `fire_events_per_year` (float) — mean annual dispatched emergency events
  in the window (kept events ÷ window length; a hood missing a year counts
  0 for it)

(`fire_events_per_acre = fire_events_per_year / area_acres` is computed
downstream in `join_and_calculate`, boundary-acre denominator — same acre
as every other per-acre metric. It is in `SLIM_COLUMNS` and ships in the
web GeoJSON; the Services view's fire plane reads it.)

**Responsibilities:**
- Resolve the dispatch-datetime column from an explicit candidate list
  (`DISPATCH_COLUMN_CANDIDATES`) — HARD-ERROR listing the file's actual
  headers if none match (the build session could not reach the API to pin
  the name; the other keyed columns — `event_type_group`,
  `neighbourhood_name` — were confirmed in the Session-12 probe)
- Filter rows to the year window (unparseable dispatch dates counted +
  reported); HARD-ERROR if any window year has zero rows (wrong pin or
  upstream drift, never a real empty year)
- Drop operational noise by `event_type_group` — the explicit
  `NOISE_GROUPS` set (TRAINING/MAINTENANCE, COMMUNITY EVENT, PRE-INCIDENT
  PLANNING) and null groups, each count reported. Everything else is KEPT,
  including unrecognized new groups (logged loudly — they are presumably
  real dispatches). The ~57% MEDICAL share is a display caveat, NOT a
  filter (locked decision 2)
- Log the kept-group mix (medical share included) every load
- Normalize `neighbourhood_name` (strip + uppercase + `NAME_CORRECTIONS`)
  BEFORE aggregation; null-hood rows excluded + counted (no spatial
  fallback — locked: 99% pre-joined coverage)
- Count events per (hood, year), average over the window

**Also exports:** `export_fire_stations_web(stations_csv, out_path)` — the
31 station points (`b4y7-zhnz`) as `web/data/fire_stations.json`
(committed, lazy-loaded by the frontend): `{"stations": [[lon, lat,
label], ...]}`. Lat/long columns resolved like the dispatch column
(explicit candidates, hard error); null-coordinate rows dropped + reported.

**Does not:** decode `response_code` (dispatch-priority letters, undecoded
— never filter on it), touch geometry/boundaries, or claim
coverage/response adequacy.

---

### `src/load_transit.py` (services lens #4 — added 2026-07-11)

Full methodology + the two locked decisions in `docs/SPEC_services.md`
"Transit lens"; dataset facts in `DATA.md` §9. **Scheduled service supply
only** — ETS publishes no stop-level ridership, so never present this as
usage, cost, or coverage.

**Inputs:** the five GTFS CSVs (`data/raw/gtfs_{stops,routes,trips,
stop_times,calendar_dates}.csv` — one logical input; main.py runs the lens
only when all five exist); the boundary GeoDataFrame from
`load_boundaries.py` (projected geometry for the stop point-in-polygon).

**Outputs:** `pd.DataFrame` keyed by `neighbourhood_name`:
- `transit_dep_bus` / `transit_dep_lrt` (float) — mean-weekday scheduled
  stop-events by mode (internal, the road-class pattern)
- `transit_dep_total` (float) — all modes, incl. any unknown `other`

(`transit_dep_per_acre = transit_dep_total / area_acres` is computed
downstream in `join_and_calculate`, boundary-acre denominator. It is in
`SLIM_COLUMNS` and ships in the web GeoJSON; the Services view's transit
plane reads it.)

**Responsibilities:**
- Active weekday (Mon–Fri) service days per service_id from calendar_dates
  (calendar-dates-only feed; type-2 removals honoured generically);
  HARD-ERROR on zero active weekday dates
- Mode via the explicit `ROUTE_MODE` dict (bus/lrt; unknown types KEPT as
  `other`, logged loudly)
- Count stop-events per (trip, stop) from stop_times; weight each trip by
  its service's active-weekday share, so no per-date loop
- Stops → hood point-in-polygon in **EPSG:3400** (CRS explicit);
  boundary-coincident multi-matches deduped + reported
- **No silent drops:** referential breaks (orphan stop_times, unknown
  stop_ids), null-coordinate stops, and out-of-boundary (regional) stops
  all counted; their events form the reported UNASSIGNED bucket; a
  **conservation check** requires assigned + unassigned == citywide total
- Log the feed window + per-mode citywide totals every load (the
  current-signup seasonality is the metric's main caveat)

**Also exports:** `export_transit_stations_web(stops_csv, out_path)` — the
location_type-1 stations (58: LRT stations + transit centres) as
`web/data/transit_stations.json` (committed, lazy-loaded), fire-station
pattern and shape.

**Does not:** claim ridership/usage, model cost, apply the metric to
on-demand transit (absent from GTFS), or touch assessment data. Like
roads, a **refreshed input** with no roll-year pin (weekly CI re-pull).

---

### `src/load_permits.py` (Development & Infill lens A — added 2026-07-12; dev grid 2026-07-15)

Full methodology + locked decisions in `docs/SPEC_development.md` "Lens A";
dataset facts in `DATA.md` §10. **New-CONSTRUCTION activity only** — the
project's first change/flow metric (everything else describes the roll as it
stands). Not a money path: an unmatched permit hood is a blank hood, not a
silent dollar loss, so the name join is warn-not-fail (unlike the assessment
CI guard).

**Inputs:** `data/raw/building_permits.csv` (`24uj-dj8v`, slim `$select`); a
pinned window tuple (`PERMIT_YEARS` / `PERMIT_YEARS_RECENT` in `main.py`).

**`load_permits(csv, years)` → `pd.DataFrame`** keyed by `neighbourhood_name`:
- `new_dwelling_units` (float) — Σ `units_added` over new-construction ∩
  residential permits in the window
- `new_dwelling_permits` (int) — the permit count behind that sum

(`new_units_per_acre` / `new_permits_per_acre` are computed downstream in
`join_and_calculate`, boundary-acre denominator; both windows emit their
columns, the 3yr twins `_3yr`-suffixed. In `SLIM_COLUMNS`, ship in the web
GeoJSON; the Development view choropleth + Infill Lens B activity term read
them.)

**Responsibilities / no silent drops:**
- `work_type` ∈ `NEW_WORK_TYPES` and `building_type` ∈
  `RESIDENTIAL_BUILDING_TYPES` — **explicit hand-enumerated dicts**, every
  spelling variant, warn-loudly-on-unseen (never prefix-match the `(NNN)`
  code); suite-conversions `(07)/(08)/(09)` are Lens B, out here
- Drift guard: a window year with zero permits HARD-ERRORS (stale pin /
  upstream drift — fire-lens precedent)
- Non-numeric `units_added` → 0 (kept as a permit), reported; null/blank
  `neighbourhood` excluded + unit loss reported; `PERMIT_NAME_CORRECTIONS`
  (= the shared `NAME_CORRECTIONS`) resolves `CHAPPELLE AREA` etc.

**Also exports:** `export_dev_grid(csv, out_path, years, years_recent,
cell_m)` — the Development view's **100 m detail layer** (added 2026-07-15).
Bins GEOCODED new-construction ∩ residential permits into the **same
EPSG:3400 100 m cells as `export_value_grid`** (Glass grid) →
`web/data/dev_grid.json` (committed, lazy-loaded): `[lon, lat, units,
permits, units_3yr, permits_3yr]` rows at each cell's SW corner, plus a
per-window `coverage` block. **Geocode coverage is reported, not silent** —
coordinates lag on the newest permits (DATA.md §10), so ungeocoded permits
are excluded from cells but counted in `coverage` for the web blurb to
disclose; positions are never faked. Raises if the CSV predates the
lat/long `$select`.

**Does not:** count suite conversions / additions / demolitions, join
parcel geometry, or touch the money path. A **refreshed input** with a
January window-pin bump (both `PERMIT_YEARS` tuples).

---

### `src/join_and_calculate.py`

**Inputs:**
- Aggregated assessment DataFrame from `aggregate_by_neighbourhood.py`
- Boundary GeoDataFrame from `load_boundaries.py`
- (optional) zoning composition DataFrame from `load_zoning.py` — merged on
  `neighbourhood_name`, adding the set-aside flags, the residential-lens flag, and
  the full land-use composition fractions (the `ZONING_COLUMNS` list — use-mix view)
  to the output and thus the GeoJSON. Degrades gracefully when absent, like the
  revenue columns.
- (optional) roads DataFrame from `load_roads.py` (`SPEC_services.md`) — a
  `ROAD_COLUMNS` merge on `neighbourhood_name`, same graceful-when-absent
  pattern; `road_m_per_acre = road_m_total / area_acres` computed here.
  Boundaries with no roads overlay default to a true 0 m (flagged) — unlike
  the zoning NaNs, no overlay genuinely means no city collector/local road.
- (optional) stormwater DataFrame from `load_stormwater.py`
  (`SPEC_utilities.md` Lens 1) — a `STORM_COLUMNS` merge on
  `neighbourhood_name`; `storm_charge_per_acre = storm_charge_annual /
  area_acres` computed here. Boundaries with no roll parcels default to a
  true modeled $0 (flagged) — roads semantics, with the exempt-land
  understatement caveat recorded in the module.
- (optional) lot-acre DataFrame from `export_value_grid.build_hood_lot_acres`
  (added 2026-07-08) — the neighbourhood lot-acre denominator toggle. Merged on
  `neighbourhood_name`; `value_per_lot_acre` / `revenue_per_lot_acre` =
  eligible dollars ÷ deduped parcel acres (NOT boundary acres), and
  `parcel_frac = lot_acres_eligible / area_acres` ships alongside. Hoods below
  `LOW_PARCEL_FRAC` (0.15) parcel land are suppressed to NaN (rendered n/a
  grey) so the near-zero-denominator tail doesn't explode; `parcel_frac` still
  ships. An editorial alternative denominator ("value per developable acre",
  `docs/FINDINGS_denominator_cardinality.md`), NOT a correction — the
  ground-acre `value_per_acre` stays the cardinality-robust default.

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
- **Scheduled preprocessor (BUILT + LIVE 2026-07-01/02)** — a weekly GitHub Action (`.github/workflows/refresh.yml`) downloads the source data, runs `main.py`, writes a `status.json` heartbeat, commits regenerated GeoJSON only if it changed, and deploys `web/` to Pages. Two supporting scripts: `scripts/download_data.py` (fetch assessment + boundaries + zoning) and `scripts/generate_status.py` (the manifest/heartbeat/banner). Optimized for rare (annual) data changes — see `docs/SPEC_deployment.md`.

**Phase 2 handoff:** `join_and_calculate.py` exports a slim GeoJSON via `export_geojson()` — only `neighbourhood_name`, `value_per_acre`, and `geometry`, reprojected to EPSG:4326 (deck.gl/MapLibre expect lon/lat). No changes to upstream modules needed.

**Web app layout & export target:** The Phase 2 app lives in `web/` (`web/index.html` + `web/data/`). The export writes to **`web/data/neighbourhood_value_per_acre.geojson`** — a *tracked, served* location — NOT `output/` (which is gitignored as throwaway artifacts and cannot be served by Pages). `main.py` must point the GeoJSON export at `web/data/`, so each run regenerates the committed served file in place. The PNG stays in `output/` as a static fallback.

**GitHub Pages serving `web/` (RESOLVED + LIVE).** Pages can't serve a subfolder from a branch, so the workflow uses the official Pages actions (`upload-pages-artifact` with `path: web` → `deploy-pages`) to publish `web/` directly — no `gh-pages` branch and no moving the app to `docs/`/root. Pages is enabled with `build_type: workflow`. Live at https://peterfriedrich.github.io/edmonton-tax-viz/.

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

---

## Reconciliation notes — 2026-07-09 audit (drift flagged, NOT fixed)

Doc-vs-implementation check, per the audit brief. **No behavioural drift found**:
the implemented modules match their documented contracts everywhere spot-checked
(`load_assessment`/`aggregate_by_neighbourhood`/`load_boundaries`/`plot_choropleth`
read in full; interface + constant verification across the rest; the published
GeoJSON's 24 properties are exactly `SLIM_COLUMNS`; franchise columns confirmed
carried-but-not-slim; zero-area guard, unmapped-class hard error, and
`GITHUB_OUTPUT` plumbing for the year-alignment hold all verified in code). The
drift is documentation lagging the build:

1. **`load_water.py` and `load_franchise.py` have no Modules-section entries** —
   they exist only as "Also in the flow" paragraphs above, unlike stormwater and
   fire, which got full module sections when added. The paragraphs are accurate;
   the section depth is just inconsistent.
2. **Testing section lists 5 test files; `tests/` has 18** — one per src module
   plus `test_main.py`, `test_download_data.py`, `test_check_year_alignment.py`,
   `test_generate_status.py`. The "what to test per module" lists were never
   extended past Phase 1.
3. **`join_and_calculate` "Outputs" block lists only the 7 core columns** — the
   implementation also carries every documented optional-merge column
   (`ZONING_COLUMNS`, `ROAD_COLUMNS`, `STORM_COLUMNS`, `FIRE_COLUMNS`,
   `WATER_COLUMNS`, `FRANCHISE_COLUMNS`, `LOT_ACRE_COLUMNS` and the per-acre
   derivatives). The Inputs bullets describe them; the Outputs block was never
   updated to match.
4. **`main.py` docstring says "override any input/output path" via CLI**, but the
   web side-output paths (`ROADS_WEB_OUT`, `ZONING_WEB_OUT`, `GRID_WEB_OUT`,
   `FIRE_STATIONS_WEB_OUT`) and the three utility rates paths are module
   constants with no CLI flags (main.py:62-65, 328-330). Consistent with "paths
   as constants at top"; inconsistent with the docstring's claim.
5. **`CONTRIBUTING.md` Project Structure is Phase-1 vintage** — missing `web/`,
   `scripts/`, `tools/`, `.github/`, nine src modules; places `SPEC_phase1.md`/
   `ARCHITECTURE.md` at repo root; names "Claude Sonnet" as the assistant. Not
   this doc, but flagged here for completeness.
6. **"What's Not Here (Phase 1 Scope)" says no web output / no cost side** —
   both now exist and are documented in the sections above it; the Phase-1 list
   reads as current-state but is historical. Cosmetic.

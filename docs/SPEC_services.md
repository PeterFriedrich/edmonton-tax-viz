# Scope: Services Lens — Road Supply (first service)

**Status: SPEC 2026-07-01. Not built.** Branch `feature/services-lens`.

This opens the **cost side** of the fiscal picture — explicitly out of scope in
`SPEC_phase1.md` ("no service cost allocation yet — revenue only"). It is scoped
as a **general services lens** whose first (and for now only) service is the
**road network**: the module boundaries, output shape, and frontend slot are
designed so later services (water, drainage, transit, …) can slot in as
additional per-neighbourhood supply columns without rework.

## Why

Every metric shipped so far (assessed value/acre, revenue/acre) measures what a
neighbourhood *produces*. None measures what it *consumes*. Road supply is the
natural first consumption proxy: it is the largest linear infrastructure network
the City maintains, the data is public and city-maintained, and length per acre
is a defensible physical quantity requiring no cost model or allocation
assumptions.

**V1 metric — DECIDED: road supply first, ratio as a fast follow.**
- **V1 ships `road_m_per_acre`** — metres of city-maintained road centreline per
  acre of neighbourhood area. Purely descriptive infrastructure intensity.
- **V2 (fast follow, same data):** revenue per road-metre — the fiscal
  "does this land's revenue cover its road supply" ratio. Deferred so the road
  layer is validated *before* anything is derived from it, and because the ratio
  needs a day-one answer for set-aside / near-zero-revenue hoods (river-valley
  parkways divided by ~$0 revenue) that the supply metric doesn't.

This is a **new metric, not a display filter**. The residential lens and the
set-aside treatment subset/re-colour the *existing* revenue/value data; road
supply is a new quantity and joins the Revenue/Value metric toggle as a third
option.

## Data

**Source: Edmonton Open Data `9j8t-zm52` ("Road Network")** — centreline
LineStrings, EPSG:4326 via Socrata GeoJSON. Inspected 2026-07-01:

- **53,720 segments total.** `centerline_type`: Road 39,515 / Alley 12,088 /
  Railway 2,117.
- `responsible_party_description`: City of Edmonton 49,794; Province of Alberta
  1,164 (ring road etc.); CN 1,604 / CP 384; Private Organization 566; small
  counts for neighbouring municipalities (Strathcona County, St. Albert,
  Beaumont, Leduc County, CFB Namao).
- `functional_class_code`: 15 values (Local-Residential 20,284 dominant; four
  Arterial classes A–D; Collector and Local split by adjoining land use;
  Local-ParkWay; Local-Private). **Null class count (14,205) equals
  Alley + Railway exactly** — so after the Road filter, class coverage is 100%.
  Verify this invariant at load; it makes the per-class breakout gap-free.
- Centrelines only — **no surface polygons**, so the honest v1 quantity is
  **length**, not road area. Right-of-way area (buffer by class width) is a
  possible later refinement, not v1.

**Row filters — DECIDED:**
- **`centerline_type == "Road"` only.**
  - Railway out (not city road liability; CN/CP own their lines).
  - **Alleys out.** Alleys have a genuinely contested interpretive status — the
    groups with a stake in them (residents, the City, developers) each have
    different reasons for being fine with them — so folding them into a road
    metric would embed an interpretation into a descriptive layer, against the
    project's neutral-tone rule. Excluded from v1 entirely. If ever revisited,
    they enter as a deliberately separate class/column, never merged into the
    road totals. **Don't re-litigate; don't "helpfully" re-add.**
- **`responsible_party_description == "City of Edmonton"` only.** Same logic
  that excluded the education levy in `SPEC_revenue.md`: this project models
  *City* fiscal sustainability. The City does not maintain the Henday
  (provincial), private roads, rail, or neighbouring municipalities' segments.
  - Note: verify at build time how `Local-Private` interacts with this filter
    (private *function* vs City *responsibility* may not coincide); report the
    count either way.

## Computation

```
per hood:  road_m_<class> = Σ length(city road centrelines ∩ hood polygon), by class group
           road_m_total   = Σ over class groups
           road_m_per_acre = road_m_total / area_acres      # boundary acres
```

- **Class groups:** roll the 15 codes up to **arterial / collector / local**
  (explicit dict, same philosophy as `ZONE_CATEGORY` — first-token/pattern
  parsing with every code hand-assigned, unknown codes warn loudly). Emit
  per-group metres even though v1 displays only the total — it is cheap and
  unblocks class weighting later without a pipeline change.
- **Denominator = boundary `area_acres`** (from `load_boundaries`), NOT the
  zoning module's zoned-area denominator. Roads largely run through
  right-of-way that zoning polygons don't cover — the zoning lesson runs in
  reverse here. This also matches the revenue/value metrics' denominator, so
  all three metrics are per the same acre.
- **Lengths in EPSG:3400 metres** (CRS set explicitly before any length
  calculation, per project rule). Overlay via
  `gpd.overlay(roads, boundaries, how="intersection", keep_geom_type=True)`
  (LineString × Polygon → clipped LineStrings), then `.length` and group-sum.

**Guards (no silent drops):**
- **Conservation check:** total post-overlay length must be within a small
  tolerance of the citywide filtered pre-overlay total; report the unassigned
  remainder (segments outside any hood polygon — e.g. beyond city limits)
  explicitly, never silently.
- **Boundary-coincident arterials caveat:** arterials commonly run *along*
  neighbourhood boundaries, so assignment of a centreline lying exactly on a
  shared edge is knife-edge. Accept the assignment noise in v1 (the
  conservation check bounds the damage); note it as a known limitation.
- **Download truncation:** 53,720 rows **exceeds the `$limit=20000` pattern**
  used for zoning — a copy-paste download would silently keep 37% of the
  network. The count-vs-limit assertion in `scripts/download_data.py` (already
  an open data-integrity follow-on in `TODO.md`) is a **prerequisite commit**
  of this feature, not an optional follow-on.

## Code changes

- **New module `src/load_roads.py`** — mirrors `load_zoning.py`'s shape: load →
  filter → `set_crs(4326)` → `to_crs(3400)` → overlay → per-hood sums; returns
  a plain DataFrame keyed by `neighbourhood_name` (`road_m_arterial`,
  `road_m_collector`, `road_m_local`, `road_m_total`). Synthetic-geometry unit
  tests like `tests/test_load_zoning.py`.
- **`scripts/download_data.py`** — add `9j8t-zm52` to `SOURCES` (with a limit
  above the row count) **and** the count-vs-limit truncation assertion for all
  sources (prerequisite, its own commit — closes the audit follow-on).
- **`src/join_and_calculate.py`** — `ROAD_COLUMNS` merged on
  `neighbourhood_name` (left join, graceful when absent, same pattern as
  zoning); compute `road_m_per_acre`; extend `SLIM_COLUMNS`.
- **`main.py`** — load roads by default with graceful skip + warning if the
  file is absent; `--roads-geojson` / `--skip-roads` flags.
- **`web/index.html`** — third entry in the metric toggle. Colour clamp/
  transform TBD from data (below).
- **Docs:** `DATA.md` new §6 (dataset facts above + any build-time
  discoveries); `ARCHITECTURE.md` module entry; `generate_status.py` vintage
  fields if roads become a refreshed CI input (lean: yes, same weekly refresh
  as zoning).

## Methodology decisions to settle

- **Alleys — DECIDED: excluded** (see Row filters). Recorded here so it
  doesn't get re-opened casually.
- **Ownership — DECIDED: City of Edmonton only.**
- **V1 metric — DECIDED: supply (`road_m_per_acre`); ratio is V2.**
- **Colour transform — OPEN, decide empirically.** Run the established skew
  method (`scripts/investigate_skew.py` pattern, biased skew) on
  `road_m_per_acre` once real numbers exist; don't assume sqrt carries over
  from revenue/value.
- **Set-aside grey under the roads metric — OPEN, lean: keep grey in v1.**
  Set-aside hoods have real roads (river-valley parkways), so a supply metric
  *could* legitimately colour them. But keeping the grey treatment consistent
  across all metrics is simpler to read and to explain; revisit when the V2
  ratio forces the question anyway.
- **Class weighting (arterial ≠ local in cost) — DEFERRED.** V1 is unweighted
  total metres; the per-class columns exist so weighting is a display/derived
  change later, not a pipeline change.

## Cross-refs

- Cost side declared out of scope in Phase 1: `docs/SPEC_phase1.md` (Out of Scope).
- Municipal-only scoping precedent (education levy exclusion): `docs/SPEC_revenue.md`.
- Module pattern + explicit-dict philosophy: `src/load_zoning.py`, `docs/ARCHITECTURE.md`.
- `$limit` truncation risk: `docs/FINDINGS_data_integrity_audit.md`, `TODO.md`
  (data-integrity follow-ons).
- Set-aside / residential lens treatments (what this is *not*): `docs/UI.md`.

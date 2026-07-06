# Scope: Services Lens — Road Supply (first service)

**Status: V1 BUILT 2026-07-01** (same day as the spec), branch
`feature/services-lens`. As built: `scripts/download_data.py` roads source +
two-tier truncation guard; `src/load_roads.py` (13 tests; real data 3,644 km
collector+local in the metric, 1,353 km arterial internal, 0.28% unassigned);
`join_and_calculate` `ROAD_COLUMNS` merge + `road_m_per_acre`; `main.py`
`--roads-geojson`/`--skip-roads`; **colour DECIDED: linear** (FINDINGS §6.3 —
raw skew −0.29; the spec's don't-assume-sqrt caution was warranted); web map
Roads toggle with per-metric transforms, headless-verified. Dataset facts +
quirks: `DATA.md` §6.
**Provenance note:** roads carries NO year pin in `status.json` — the network
is a continuously-updated feed with no roll-year semantics (unlike
assessment/rates/zoning); its provenance is `last_checked` itself.
**Remaining from this spec:** the V2 revenue-per-road-metre ratio (fast
follow, needs the set-aside/near-zero-revenue day-one answer).

## Display architecture — REVISED 2026-07-01 (two-plane, stackable services)

The road-supply **prism view built above is RETIRED** the same day (Peter's
call). The metric/pipeline work stands unchanged — `road_m_per_acre` colours
the network below and feeds the eventual ratio — but services do not render
as extrusions. The display model going forward:

- **Ground plane — service layers, STACKABLE.** Each service renders as its
  own toggleable ground-level layer in a layers panel; roads are the first,
  later services (each with its own spec section when it comes) add a
  checkbox, not a rework. For roads: the actual centreline network —
  **arterials in a neutral colour** (context: shared infrastructure, carries
  no metric) and **collector + local roads coloured by their neighbourhood's
  `road_m_per_acre`** (linear, clamp 53 — the §6.3 decision applies to the
  network colouring).
- **Above — the revenue/value prisms**, unchanged today; LATER gains a
  transparency control so the money plane can overlay the service plane
  without hiding it.
- **Finally — a synthesis view:** the ratio of revenue to total services
  (definition of "total services" deliberately deferred until more than one
  service exists; revenue-per-road-metre is its single-service special case).

Staging: (1) roads ground layer + layers panel ← NOW; (2) prism transparency
overlay; (3) ratio view.

**Web export (new pipeline output):** the browser needs road *geometry*,
which the 62 MB raw file can't ship. Export a slim `web/data/roads.geojson`:
City-filtered clipped segments, dissolved per (neighbourhood × arterial/access),
line-simplified + coordinate-trimmed, properties reduced to the group flag and
the hood's metric value. Lazy-loaded by the frontend on first toggle so the
initial page payload is unchanged.

*As built (2026-07-02):* `export_roads_web()` in `src/load_roads.py`, called
from `main.py` alongside the polygon export (skipped with `--skip-roads`).
Shares the load→filter→classify→clip front half with `load_roads` via
`_prepare_segments()`. Per-feature properties: `n` (hood name), `t`
(`"arterial"` | `"access"` = collector+local), `v` (the hood's
`road_m_per_acre`, access only, null on arterials — same number
`join_and_calculate` publishes). Render-cost tuning (2026-07-02, after
observed browser lag; all display-only, metrics computed before thinning):
contiguous parts welded (`linemerge`); access simplify 20 m + sub-20 m clip
slivers dropped (~12% of paths, <1% of length); **arterials dissolved
CITYWIDE into one feature** (they carry no metric — per-hood clipping only
chopped them at every boundary crossing; `n` is null) + simplify 40 m.
Net vs the first cut: −33% paths, −30% vertices → **398 features, 1.6 MB**;
committed to the repo like the polygons file so CI's commit-if-changed step
tracks it weekly. Vertex floor: most remaining vertices are path endpoints
at junctions, which no simplify tolerance can remove — next lever, if ever
needed, is zoom-dependent rendering.

*Frontend as built — ALL THREE STAGES (2026-07-02, `web/index.html`; full
display details in `UI.md` "Services views"):* after two intermediate
control models (Roads checkbox + opacity slider; slider-at-0% roads-only
mode), Peter settled on **three discrete views** — **Money** (the classic
prisms, opaque), **Roads** (the network alone, access roads ramp-coloured by
`road_m_per_acre`, no prism layers at all), and **Ratio** (stage 3: ghost
prisms — default 5% opacity, slider-adjustable — of **revenue per road
metre** over the all-neutral network). The ratio is computed client-side
from the two published columns; colour is LOG (FINDINGS §6.4 — skew 19.7,
log 0.32; anchors p2.5–p97.5 of the kept subset, runtime-computed), height
linear. Set-aside hoods and hoods with `road_m_per_acre < 5`
(`RATIO_ROAD_FLOOR`; denominator artifacts — WESTVIEW VILLAGE $1.3M/m)
render grey + flat, off-scale. Road geometry lazy-loads on first non-Money
view; a flat invisible hood layer carries tooltips + hover highlight in the
Roads/Ratio views (roads/ratio prisms are not pickable — picking ignores
opacity). "Total services" definition remains deferred until a second
service exists; revenue-per-road-metre is its single-service case, now
shipped.

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
- **V1 ships `road_m_per_acre`** — metres of city-maintained **collector +
  local** road centreline per acre of neighbourhood area (arterials excluded —
  see Row filters). Purely descriptive infrastructure intensity.
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
- **Arterials excluded from the metric (all four Arterial classes A–D).**
  Arterials are **shared infrastructure**: they carry city-wide traffic and any
  development pattern would entail them, so attributing their metres to the
  neighbourhood they happen to pass through would embed a city-wide quantity
  into a per-neighbourhood metric. The shipped total is **collector + local**
  — the road supply that exists because of that neighbourhood's own layout.
  `road_m_arterial` is still computed and kept as an internal column (it costs
  nothing, feeds the conservation guard, and preserves the option of a later
  arterial view), but it never enters `road_m_total` / `road_m_per_acre`.
  Side effect: this removes most of the boundary-coincident assignment noise,
  since arterials are precisely the segments that run along neighbourhood
  boundaries (see Guards).

## Computation

```
per hood:  road_m_<class>  = Σ length(city road centrelines ∩ hood polygon), by class group
           road_m_total    = road_m_collector + road_m_local   # arterials NOT included
           road_m_per_acre = road_m_total / area_acres         # boundary acres
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
- **Boundary-coincident segments caveat:** roads running *along* a
  neighbourhood boundary are knife-edge in the overlay. Excluding arterials
  from the metric removes most of this (they are the main boundary-runners);
  collectors can still trace boundaries occasionally. Accept the residual
  noise in v1 (the conservation check bounds the damage); note it as a known
  limitation.
- **Download truncation — BUILT 2026-07-01 (the prerequisite commit):**
  53,720 rows exceeds the `$limit=20000` pattern used for zoning — a
  copy-paste download would have silently kept 37% of the network.
  `scripts/download_data.py` now guards every source two ways: count vs. our
  declared `$limit`, and count vs. the live Socrata `$select=count(*)` (which
  also catches any *server-side* cap — SODA 2.0 historically capped `$limit`
  at 50,000; see the completeness note at the top of `DATA.md`). Closed the
  data-integrity audit `$limit` follow-on.

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
- **Arterials — DECIDED: excluded from the metric** (shared infrastructure;
  see Row filters). Kept as an internal column only.
- **Ownership — DECIDED: City of Edmonton only.**
- **V1 metric — DECIDED: supply (`road_m_per_acre` = collector + local); ratio
  is V2.**
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

- **Candidate next services (each fires the Services-view UI trigger above):**
  fire lens (datasets probed, design open — TODO.md "More service layers") and
  the five utility cost lenses (`docs/SPEC_utilities.md`, SPEC'd 2026-07-05 —
  stormwater recommended first; tariff methods in
  `docs/utility_cost_estimation_lens_methods.md`).
- Cost side declared out of scope in Phase 1: `docs/SPEC_phase1.md` (Out of Scope).
- Municipal-only scoping precedent (education levy exclusion): `docs/SPEC_revenue.md`.
- Module pattern + explicit-dict philosophy: `src/load_zoning.py`, `docs/ARCHITECTURE.md`.
- `$limit` truncation risk: `docs/FINDINGS_data_integrity_audit.md`, `TODO.md`
  (data-integrity follow-ons).
- Set-aside / residential lens treatments (what this is *not*): `docs/UI.md`.

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
metre** over the all-neutral network). *2026-07-05: Roads GENERALIZED to the
**Services view*** — per-service checkboxes (Roads, Stormwater; the original
stackable idea, one level down), a "colour" radio picking which checked
service drives the ramp (the rest render neutral), defaults reproducing the
old Roads view exactly. The second service is the stormwater hood plane
(`SPEC_utilities.md` Lens 1, MODELED label). The ratio is computed client-side
from the two published columns; colour is LOG (FINDINGS §6.4 — skew 19.7,
log 0.32; anchors p2.5–p97.5 of the kept subset, runtime-computed), height
linear. Set-aside hoods and hoods with `road_m_per_acre < 5`
(`RATIO_ROAD_FLOOR`; denominator artifacts — WESTVIEW VILLAGE $1.3M/m)
render grey + flat, off-scale. Road geometry lazy-loads on first non-Money
view; a flat invisible hood layer carries tooltips + hover highlight in the
Roads/Ratio views (roads/ratio prisms are not pickable — picking ignores
opacity). *2026-07-10: the "total services" question was DECIDED
(SPEC_utilities decision 3) — the ratio stays PER-SERVICE, as a
denominator picker* (revenue per road metre | per fire event; modeled
EPCOR dollars excluded by the money-flow honesty rule; a combined
unit-cost denominator is the V2 follow-on). Fire-ratio floor + log
colour: `FINDINGS_revenue_scale.md` §6.7; verify:
`tools/profiling/verify-ratio-denom.js`.

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

This is a **new metric, not a display filter**. The set-aside treatment (and,
until it was removed on 2026-07-26, the residential fade lens) subsets or
re-colours the *existing* revenue/value data; road supply is a new quantity and
joins the Revenue/Value metric toggle as a third option.

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

## Fire lens — dispatched-event demand (third service; added 2026-07-06)

**Status: design LOCKED 2026-07-05 (Peter, all four decisions); BUILT
2026-07-06** (loader + join wiring + Services-view checkbox + station dots).
Build-session caveat: the dev environment could not reach data.edmonton.ca
(network policy), so the first real-data run happens in CI — the loader
resolves its one unverified column name (the dispatch datetime) from an
explicit candidate list and HARD-ERRORS listing the actual header if none
match (see `src/load_fire.py`). Everything else is tested synthetically,
the project's standard test pattern.

### Why

Roads measure physical supply; stormwater models a utility charge. Fire is
the first *demand* service: how often the city's emergency apparatus is
dispatched to a neighbourhood's land. It requires no cost model — an event
count per acre per year is a defensible physical quantity, same spirit as
road metres per acre.

**What this is NOT (locked, don't oversell):** the events data has dispatch
and close timestamps but **no on-scene-arrival timestamp anywhere**, so a
true response-time / coverage-adequacy metric is NOT buildable from open
data (confirmed against the full column list, Session 12). This lens is
demand only; the 31 stations render as context dots, not a coverage claim.

### Data

Two sources (probed 2026-07-05; facts recorded in DATA.md §7–8):

- **`7hsn-idqi` "Fire Response: Current and Historical"** — ~948k
  dispatched events 2011–mid-2026, ~90k/yr in the current window. Key
  fields: dispatch + close datetimes, `event_type_group` (two-letter
  CODES) + `event_description` (the long-name vocabulary — **the filter
  column**; confirmed 2026-07-06, DATA.md §7), dispatch-priority
  `response_code` (letters, undecoded — do NOT filter on it), lat/long, and
  **`neighbourhood_name` pre-joined on ~99% of rows** — the per-hood metric
  needs no spatial work.
- **`b4y7-zhnz` "Fire Stations"** — 31 rows: station number, address,
  lat/long point only (no staffing/coverage data).

### The four locked decisions (Peter, 2026-07-05)

1. **Lens shape** — demand metric `fire_events_per_acre` (mean annual
   dispatched emergency events per boundary acre) as the Services-view
   ground plane, + the 31 stations as context dots.
2. **Event filter** — ALL emergency responses MINUS operational noise:
   events whose group (`event_description`, bare-code fallback) is
   TRAINING/MAINTENANCE, COMMUNITY EVENT, PRE-INCIDENT PLANNING, and
   null groups are excluded (each count reported). **The ~57% MEDICAL share is a legend/blurb caveat, NOT a
   filter** — don't re-litigate; the mix is logged every load so drift is
   visible. Unrecognized new groups stay IN (they are presumably real
   dispatches) and are logged loudly.
3. **Year window** — the last 3 full calendar years, **pinned as
   `FIRE_YEARS = (2023, 2024, 2025)` in `main.py`** (an auto-rolling window
   could silently average in a partial year). Averaged, not summed, so the
   number reads "events per year". Bump the pin manually each January.
4. **Branch point** — after the Services-view UI generalization (landed
   2026-07-05, PR #14).

### Computation

```
per hood:  events_y = count(kept events in year y, by neighbourhood_name)
           fire_events_per_year = mean(events_2023, events_2024, events_2025)
           fire_events_per_acre = fire_events_per_year / area_acres   # boundary acres, in join_and_calculate
```

- Hood names: strip + uppercase + `NAME_CORRECTIONS`, applied BEFORE
  aggregation (the standard rule). Events with null `neighbourhood_name`
  are excluded + counted (locked design: no spatial fallback — 99%
  pre-joined coverage makes it not worth the machinery).
- A hood with no kept events in the window is a true 0 events/yr
  (roads-style fill semantics at the join).

**Guards (no silent drops):**
- Per-year kept-event counts logged; a window year with ZERO rows
  HARD-ERRORS (wrong window pin or upstream drift, never a real year of
  no fires citywide).
- Excluded groups reported with counts; null-group and null-hood rows
  counted; the full kept-group mix (medical share included) logged.
- Download truncation: both `download_data.py` guards apply (explicit
  `$limit` + live `count(*)` cross-check).

### Display (as built)

Third checkbox in the Services view (`web/index.html`): a flat hood plane
coloured by `fire_events_per_acre` on the active ramp — the same plane
machinery as stormwater (one shared hood plane; whichever plane-service
drives the colour paints it, others render neutral slate). Station dots
(`web/data/fire_stations.json`, committed, lazy-loaded) draw whenever the
fire service is checked, driver or not. Legend + blurb carry the medical
caveat and the "demand, not coverage" framing. The checkbox hides on data
files without the fire column (same guard as stormwater).

**Colour transform — DECIDED: SQRT (2026-07-06), clamp = runtime p97.5 of
non-set-aside hoods (the stormScale pattern).** The skew check on the first
real numbers (FINDINGS §6.5) found the worst right skew in the project
(raw +7.86, clamp/median 5.8×) — linear crammed 59% of hoods into the
bottom fifth of the ramp; log over-corrects and is undefined for the 5
true-zero hoods. Storm and roads stay linear (their clamp/median ratios
don't warrant a transform). Height: no extrusion (flat plane).

## Transit lens — scheduled service supply (fourth service; added 2026-07-11)

**Status: design LOCKED 2026-07-11 (Peter, both decisions below); build starts
same session.** Note: the 2026-07-09 public-release scope lock kept transit
OUT of the release — Peter's full-lens call here AMENDS that lock (his call
to make; recorded in DECISIONS.md).

### Why

Roads measure physical supply, fire measures dispatched demand; transit is
the second *supply* service: how much scheduled transit service the city
runs to a neighbourhood's land. Like road metres and fire events it is a
defensible physical quantity — counted from the published schedule, no cost
model, no allocation assumptions.

**What this is NOT (locked, don't oversell):** ETS publishes NO stop- or
neighbourhood-level ridership; the portal's ridership/performance datasets
(`sfwk-p9kr` / `77dh-qrp7` on-time %, `wh9u-ef4x` revenue vehicle hours —
probed 2026-07-11) are citywide-monthly only. This lens is **scheduled
service, not usage** — a supply proxy, never a ridership or cost claim.
On-demand transit zones are not in the GTFS (238 fixed routes only) and are
therefore invisible to this metric — a documented limitation for the
on-demand-served fringe hoods.

### The two locked decisions (Peter, 2026-07-11)

1. **Metric** — `transit_dep_per_acre`: scheduled transit stop-events
   (departures) per boundary acre on a **mean weekday**, bus + LRT combined
   in the metric with per-mode columns kept internal (the road-class
   pattern). Rejected: stops/acre (frequency-blind), weekly total (mixes
   weekday/weekend service regimes).
2. **Scope** — full lens including the web display: pipeline module, weekly
   refresh, Services-view checkbox (hood plane + station context dots).

### Data

Five Socrata tables — the GTFS static feed published as individual datasets
(probed 2026-07-11; facts in DATA.md §9). The zip bundle (`urjq-fvmq`) is an
href-only page, so the tables are the machine path:

- **`4vt2-8zrq` Stops** — 6,882 rows; `stop_id`, lat/lon, `location_type`
  (0 = stop/platform 6,673; 1 = station 58; 2 = entrance 109; 3 = node 42).
- **`d577-xky7` Routes** — 238 rows; `route_type_descr`: Bus 235, "Tram,
  Streetcar, Light rail" 3.
- **`ctwr-tvrd` Trips** — 56,812 rows; `trip_id → (route_id, service_id)`.
  Carries a per-trip `geometry_line` — `$select` it away at download (it
  would dominate the file size for nothing).
- **`greh-g7ac` Stop Times** — 1,744,051 rows; only `trip_id`, `stop_id`
  needed (`$select`ed, ~2-column CSV). Comparable weekly-download weight to
  the 948k-row fire feed.
- **`f2sy-bth7` Calendar Dates** — 9,248 rows; calendar-dates-only feed
  (every active (service_id, date) enumerated with `exception_type` 1).
- **`rpjw-4jft` LRT Routes** — 4 route multilines (GeoJSON); a map **context
  layer only, not part of the metric** (added 2026-07-11). The loader drops
  the `HER` High Level Bridge heritage streetcar (`EXCLUDED_LRT_ROUTE_IDS`
  — volunteer-run, not ETS LRT service, absent from the GTFS routes we
  count) and keeps 021R Capital / 022R Metro / 023R Valley.

**Feed window semantics (the load-bearing caveat):** the feed is a daily
snapshot of the CURRENT signup only — probed window 2026-06-18 → 2026-08-29,
i.e. the SUMMER schedule, the seasonal service low. The metric will step at
signup boundaries under the weekly refresh. Like roads, transit carries no
roll-year pin; its provenance is `last_checked` plus the feed window logged
at load. Legend/blurb carries the "scheduled service for the current
signup" framing.

### Computation

```
stop → hood:   point-in-polygon, stops × boundary polygons (EPSG:3400)
per service:   n_dep(service_id, stop_id, mode) from stop_times ⋈ trips ⋈ routes
active days:   weekdays(service_id) = count of Mon–Fri dates active in calendar_dates
per stop:      dep_weekday(stop, mode) = Σ_service n_dep × weekdays(service) / n_weekday_dates
per hood:      transit_dep_bus / transit_dep_lrt / transit_dep_total = Σ stops in hood
               transit_dep_per_acre = transit_dep_total / area_acres   # boundary acres, in join_and_calculate
```

- Every scheduled stop-time row counts as one stop-event (the final stop of
  a trip is an arrival-only event; counted anyway — the honest name is
  "scheduled stop-events", displayed as scheduled service).
- Mode via an explicit `route_type_descr → mode` dict (bus/lrt); unknown
  route types are KEPT in the total under `other` and logged loudly (they
  are presumably real service).
- A hood with no stops is a true 0 (roads fill semantics at the join).

**Guards (no silent drops):**
- HARD-ERROR if calendar_dates yields zero weekday dates (wrong/empty feed).
- Referential breaks counted + reported, never silent: stop_times rows whose
  `trip_id` is missing from trips, trips whose `route_id` is missing from
  routes, stop-events at `stop_id`s missing from stops.
- Stops (with service) falling outside every hood polygon: their stop-events
  land in a reported "unassigned" bucket; **conservation check** — assigned
  + unassigned must equal the citywide total exactly.
- Download truncation: both `download_data.py` guards on all five sources.

### Display

Fourth checkbox in the Services view (`web/index.html`): the shared hood
plane coloured by `transit_dep_per_acre`; the 58 `location_type == 1`
stations (LRT stations + transit centres, `web/data/transit_stations.json`,
committed, lazy-loaded) draw as context dots whenever transit is checked —
the fire-station pattern. The **LRT track lines** (Capital/Metro/Valley,
`web/data/lrt_lines.json`, 343 committed path segments, lazy-loaded) draw as
a `PathLayer` under the dots in the same accent colour — a companion context
layer, added 2026-07-11 (SPEC/DATA §9). Legend + blurb carry the
scheduled-not-ridership framing and the current-signup (seasonal) caveat.
Checkbox hides on data files without the transit column (same guard as
stormwater/fire).

**Colour transform — OPEN, decide empirically** on the first real numbers
(the established skew method; fire needed sqrt, roads/storm stayed linear —
don't assume either carries over).

## Transportation lens — grouping the transport services (2026-08-02)

**Status: STAGE 1 BUILT 2026-08-02** (bike supply + the panel grouping);
**STAGE 2 BLOCKED on two reviewed unit-cost numbers** (below).

Peter's ask: *"a transportation lens in full... gather all the transport costs
for people to see. so roads will go in there. transit. but also bike lanes?"*

### The three decisions (Peter, 2026-08-02)

1. **Modelled dollars per acre**, not a supply grouping — the lens is about
   cost. (Stage 2; Stage 1 ships the missing supply input it needs.)
2. **A group INSIDE the Services view**, not a new top-level view. Services
   already owns the plane, the checkboxes and the colour-driver radio; a new
   view would duplicate all of it and add a row to the CONTROLS_MATRIX state
   space for nothing.
3. **Dedicated bike assets only** — see DATA.md §15 for the vocabulary and the
   two traps.

**Services stays FULL-only** (the 2026-07-28 lock); this changes nothing there.

### Why roads and transit were already here

Both existed as Services rows before this lens. The change is that they now
read as *one thing* — and that bike, the missing third, exists at all.

### Stage 1 (BUILT): bike supply

`src/load_bike.py` → `bike_m_per_acre`. Modelled on `load_roads`: explicit
classification dict, EPSG:3400 overlay, conservation guard, slim web export.
Metric = **dedicated** cycling assets only. Colour **sqrt**
(`FINDINGS_revenue_scale.md` §6.9 — decided empirically, not assumed).
Display: the shared hood plane + the network as a **context PathLayer** (the
LRT-lines pattern — the plane carries the metric, the lines just show where).

⚠️ **The exclusions ARE the metric.** Shared roadways are already in
`road_m_total`; walkways are pedestrian; coming-soon routes are not built. Get
any of the three wrong and the number is not what its label says. DATA.md §15.

**Panel grouping:** `#services` splits into **Transportation** (Roads · Transit
· Bike) and **Other services** (Stormwater · Fire · Water/sewer · Service
cost). Captions are labels — they gate nothing, carry no controls, and a
caption whose rows are all data-gated away hides itself.

⚠️ **THE SERVICES LEGEND IS AN IF/ELSE CHAIN WHOSE `else` PRINTS THE ROAD
LEGEND.** A new service without its own branch renders a confident, wrong
legend rather than a blank one — bike shipped "Road metres per acre, 0..53 m+"
over a bike-coloured map until the rendered output was read. **Any future
service must add a legend branch AND a `primaryRow` entry** (the tooltip has
the same shape: a missing key falls to `|| []` and prints "no X data" over a
hood that has data). `verify-bike.js` asserts both, and asserts the legend is
not the road fallback specifically.

### Stage 2 (BLOCKED): the transportation cost composite

**Publish disjoint per-term cost columns rather than a second overlapping
composite** — `svc_cost_per_acre` already contains roads, so a
`transport_cost_per_acre` containing roads too would leave two cost columns
that cannot be read together:

```
cost_roads_per_acre    = road_m_per_acre      x road_dollars_per_m
cost_transit_per_acre  = transit_dep_per_acre x (ETS budget / citywide weekday departures)
cost_bike_per_acre     = bike_m_per_acre      x bikeway_dollars_per_m
cost_fire_per_acre     = fire_events_per_acre x (fire budget / citywide events)

transport_cost_per_acre = roads + transit + bike
svc_cost_per_acre       = roads + fire        # UNCHANGED value and definition
```

The transit term is the **fire pattern exactly**: allocate the annual budget by
each hood's share of citywide scheduled departures, dividing by the pipeline's
OWN citywide total so numerator and denominator match. It is a **demand
ALLOCATION of a mostly-fixed budget** — a hood with twice the service does not
cost ETS twice — and that caveat belongs in the UI copy the way fire's does.

⚠️ **BLOCKED ON PETER: two manual reviewed inputs** (the mill-rates pattern,
`data/city_unit_costs.json`; DATA.md §13 records that edmonton.ca is unreachable
from the Oracle box):
- **ETS gross annual operating budget** — 2026 Approved Operating Budget PDF,
  the same document the fire figure came from.
- **Bikeway lifecycle $/metre/year** — the roadway figure's analogue.

Both keys stay OPTIONAL in `load_unit_costs`, and `transport_cost_per_acre` is
**all-or-nothing** across its three terms: a two-term metric labelled
"transportation" would be mislabeled, the same rule the existing composite uses.

## Cross-refs

- **Candidate next services — the Services-view UI trigger FIRED and the
  shape is DECIDED (2026-07-05, Peter): the Roads view generalizes to a
  "Services" view with per-service checkboxes.** Stormwater is the second
  service (pipeline built, display = per-hood ground-plane layer —
  `docs/SPEC_utilities.md` decision 2); fire is the third (dispatched-event
  demand — its own section above). Tariff methods in
  `docs/utility_cost_estimation_lens_methods.md`.
- Cost side declared out of scope in Phase 1: `docs/SPEC_phase1.md` (Out of Scope).
- Municipal-only scoping precedent (education levy exclusion): `docs/SPEC_revenue.md`.
- Module pattern + explicit-dict philosophy: `src/load_zoning.py`, `docs/ARCHITECTURE.md`.
- `$limit` truncation risk: `docs/FINDINGS_data_integrity_audit.md`, `TODO.md`
  (data-integrity follow-ons).
- Set-aside / residential lens treatments (what this is *not*): `docs/UI.md`.

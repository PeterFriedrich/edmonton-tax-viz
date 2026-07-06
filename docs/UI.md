# UI & Accessibility (Phase 2 web map)

Visual theming and accessibility decisions for the interactive map. Phase 1
(static PNG) is out of scope. Render/performance tradeoffs live in
`PERFORMANCE.md`; data-shape decisions in `ARCHITECTURE.md`.

---

## Current state (updated 2026-07-01)

- **Dark theme only.** No basemap (polygons on dark are self-describing — see
  ARCHITECTURE.md Phase 2 notes).
- **Three swappable colour ramps** (`RAMPS` in `index.html`, palette switcher under
  the Revenue/Value toggle), each carrying its own background + roof-edge colour:
  - **Inferno** — original warm ramp, bg `#0a0a0f`, teal edge.
  - **Glow** — near-white peak so the tallest towers glow, bg `#08060f`, cool slate
    edge (this partly addresses the "edge not finalized" item below).
  - **Cividis** — perceptually uniform + colour-blind safe (the colourblind-mode ramp;
    see "Colourblind mode" — CVD-simulator verification still pending).
  - All three are neutral luminance-sequential (magnitude = brightness, no good/bad hue).
- **Colour transform is PER-METRIC** (`transform` in each `METRICS` entry, read by
  `scaleT`/`legendGradient`; DECIDED 2026-07-01): **sqrt** for both right-skewed
  money metrics (revenue clamp `$50k`, value `$4M`, ≈ p97.5 — FINDINGS §6.1). The
  machinery stays per-metric (the legend gradient re-renders on metric switch via
  `applyMetric`) even though both current metrics happen to share sqrt — the roads
  ground layer uses its own linear mapping (below). Set-aside land is off the ramp
  entirely (grey, below). Height stays LINEAR for every metric.
- **deck.gl gotcha:** colour accessors that depend on runtime state need that state in
  their `updateTriggers` (the data reference is stable, so deck.gl skips the re-render
  otherwise). `getFillColor` uses `[state.metric, state.ramp, state.residential]`;
  the roads layer's `getLineColor` uses `state.ramp`.

### Maintenance banner (built 2026-07-02, deployment)
On load the page fetches `web/data/status.json` (`cache: no-store`) and, if its
`banner` field is non-null, renders an amber notice (`#banner`) top-centre above the
map. Used for the year-mismatch holding window and any maintenance note — the backend
sets it in `status.json` with no frontend redeploy. Fetched defensively and separately
from the map data: a missing/broken `status.json` never blanks the map. Hidden when
`banner` is null. See `SPEC_deployment.md` ("Status manifest + banner").

### Set-aside neutral treatment (built 2026-07-01)
Neighbourhoods that are ≥90% never/not-yet land (River Valley, parks, undeveloped —
see `SPEC_revenue.md`) render in a **neutral grey** (`SET_ASIDE_COLOR`), distinct from
the ramp, so they read as "outside the fiscal comparison" rather than as red/low. They
are excluded from the colour-scale fit; the tooltip shows the set-aside reason + %; the
legend carries a grey swatch. The full zoning-polygon overlay layer is a separate later
product decision.

### Residential-only lens (built 2026-07-01; extended to the Ratio view 2026-07-03)
A **"Residential only" toggle** (`#lens` panel, below the palette switcher) isolates
residential land so it compares like-to-like without the Downtown / class-rate-
differential confound (the motivating problem in `SPEC_revenue.md`). Off by default
(default view unchanged); preserves the metric + palette state. Applies in the
**Money and Ratio** views; **disabled in Roads** (no per-hood prisms to fade — the
button greys out, state persists and re-applies on leaving). Two effects when on:
- **Non-residential hoods → one uniform light grey** (`LENS_FADE_COLOR` at α90; roof
  edge `LENS_FADE_EDGE`). Deliberately a *single* neutral colour, not a translucent
  version of each hood's ramp colour — the differing colours were visual interference
  that competed with the residential read. Visible-but-see-through (dimmed, not removed)
  so the city still reads as spatial context. Set-aside hoods fade with the rest (a
  set-aside hood is never residential).
- **Residential colour is RE-SCALED** to the residential subset's p97.5
  (`residentialClampFor`), so residential hoods spread across the full ramp instead of
  crushing into the low end. The legend max + grey swatch/label update to match
  (`refreshLegend`). Height stays absolute/linear (only colour rescales). NOTE: this
  bites mainly on **Revenue** (residential clamp ≈ $37k vs the fixed $50k — non-res mill
  rate drives the high revenue tail); **Value** barely moves (≈ $3.88M vs $4M).
- **In the Ratio view** (2026-07-03) the same two effects apply to the ratio prisms:
  non-residential kept hoods take the fade grey (height untouched, matching Money),
  and the log colour anchors rescale to the **residential kept subset** —
  ≤ $258 … $916+ vs the full set's $264 … $3,253 (FINDINGS §6.4: the ratio's entire
  high tail is non-residential land). Off-scale hoods (set-aside / below the road
  floor) stay dark grey + flat regardless of lens. At the default 5% ghost opacity
  the fade is near-invisible; it reads at higher slider values.
- Drives off `is_residential` (≥0.50 residential zoned area; see `DATA.md` §5);
  orthogonal to the set-aside flag by construction.
- **Still open** (`TODO.md`): the fuller "Color Adjustment vs lens controls" hierarchy +
  self-describing state labels; the toggle is currently a plain button. Alpha / grey /
  clamp-percentile are easy tunables. Not yet visually verified in a browser.

### Neighbourhood labels (built 2026-07-03)
A **"Labels" toggle** (second button in the `#lens` panel, after "Residential only")
shows neighbourhood names on the map — the "which hood is that?" answer without
hovering every prism. Off by default; works in **all four views** (never disabled;
the residential button's disable rules are untouched). Implementation
(`web/index.html`):
- **One anchor per hood** (`labelAnchors`): the shoelace centroid of its largest
  polygon (multipolygon hoods label the main body). Computed once per data load
  from `neighbourhood_name` already in the main GeoJSON — no pipeline change.
- **Billboarded `TextLayer`**, 15 px extra-bold (weight 800), near-white with
  a 3 px black SDF outline rendered from a 128 px glyph atlas (deck's default
  64 px atlas blurs at city zoom; radius scales with it so the outline fits
  the SDF spread); `characterSet: "auto"` (WÎHKWÊNTÔWIN is beyond
  ASCII). Names stay the data's ALL-CAPS — standard cartographic style for
  area labels. `depthTest: false` so towers in front never swallow labels
  behind.
- **Roof-height anchoring** (`labelZ`): in Money/Ratio the label sits at the
  prism's top + 60 m, so a label rides the tower it names; flat views (Roads/
  Uses) label at ground + 60 m. Off-scale ratio hoods label at ground.
- **Greedy screen-space decluttering** (`visibleLabels`): anchors project through
  the live deck viewport; labels keep biggest-hood-first, dropping any whose
  text box overlaps a kept one. Box width is the name's REAL rendered width:
  canvas-`measureText` ems (a flat chars-per-em guess drifts with the glyph
  mix) × size × `LABEL_DRAW_SCALE` 1.35 — deck draws TextLayer glyphs at
  `getSize` × (atlas glyph height / fontSize) ≈ 1.26 with the 128 px atlas,
  so un-scaled boxes let
  long names butt into neighbours ("STRATHCONA JUNCTION|RITCHIE" was the
  tell) — + 8 px pad. ~27 of 406 show at city zoom; zooming in reveals more
  (a `moveend` hook re-culls when the camera settles). deck.gl's
  `CollisionFilterExtension` was the off-the-shelf answer but its collision
  render pass draws nothing under this interleaved MapLibre overlay (verified
  2026-07-03: layer present, everything culled) — the JS cull is
  deterministic and testable instead.
- **Verified** headless (`tools/profiling/verify-labels.js`): layer present/absent
  per toggle across all four views, anchors in-bbox, overlap-free kept set,
  `LABEL_DRAW_SCALE` covers deck's live sublayer `sizeScale`, zoom re-cull
  (27 → 64), roof-z exact in Money and Ratio, residential-lens disable matrix
  unchanged; screenshot eyeball `tools/profiling/shot-labels.js`.
  The existing verify scripts' `#lens button` selectors still resolve to the
  residential button (Labels is second in the DOM — keep it that way).

### Services views: Money | Services | Ratio (built 2026-07-02 as Money | Roads | Ratio; Roads GENERALIZED to Services 2026-07-05)
The road-prism metric view built earlier on 2026-07-01 was **retired the same day**
(`SPEC_services.md` "Display architecture — REVISED"). After two intermediate
iterations (a Roads checkbox + free opacity slider; then a slider-at-0% roads-only
mode), Peter settled the control model as **three discrete views** (`#views`
buttons, below the lens button; `state.view`). On 2026-07-05 — the second
service (stormwater) being the standing trigger — the Roads view became the
**Services view** (Peter's call, per-service checkboxes; the top bar stays at
five buttons regardless of service count):

- **Money** (default): the classic revenue/value prisms, always opaque. Metric
  toggle, palette, residential lens all behave as before. Hood tooltip: active
  metric + `19.2 road m / acre` + `$967 revenue / road metre` (ratio omitted when
  road base is 0 / columns absent; set-aside tooltip unchanged).
- **Services** (generalized from Roads 2026-07-05): city services as stackable
  ground-level layers — **no prism layers at all** (an opacity-0 layer still
  tessellates, draws, picks, and auto-highlights; dropping them is the honest
  render and the perf win). Per-service checkboxes live in the `#layers` panel
  (`#services`, `state.services`); with 2+ checked, a **"colour" radio**
  (`state.svcDriver`) picks which service drives the active ramp — the others
  render neutral, so exactly one scale is on screen at a time. Legend and blurb
  follow the driver (`servicesBlurb()` appends a line naming any neutral layer).
  Both persist across view switches, like the Glass denominator. Services:
  - **Roads** (default on, default driver — entering the view with defaults IS
    the old Roads view): arterials neutral grey (`ARTERIAL_COLOR`, 2 px, no
    metric); collector + local coloured by their hood's `road_m_per_acre` —
    **LINEAR, clamp 53** (FINDINGS §6.3), 1.2 px. Neutral mode (storm drives):
    the whole network in the arterial grey, same as the Ratio view's.
  - **Stormwater** (default off; second service, SPEC_utilities Lens 1): a flat
    hood plane coloured by `storm_charge_per_acre` — **MODELED** utility
    charges (bylaw lot area × runoff × rate), EPCOR money not city tax revenue;
    the legend says "Modeled" and the blurb says "modeled, not billed".
    **LINEAR, clamp p97.5 of non-set-aside hoods** (runtime,
    ≈ $2,700 on 2025 data; storm p97.5/median ≈ 1.8 — no skew correction
    warranted). Set-aside hoods grey (the usual off-scale convention); neutral
    mode (roads drive) renders the plane in the Glass view's signal-free slate
    (`GLASS_PLANE_COLOR`). Drawn before the road lines: coplanar at z=0,
    LEQUAL depth lets the later-drawn lines win. No fetch — the column rides
    the main GeoJSON (SLIM_COLUMNS, 2026-07-05).
  - **Fire** (default off; third service, SPEC_services "Fire lens",
    2026-07-06): dispatched-event **DEMAND** — `fire_events_per_acre` (mean
    annual kept events 2023–2025 ÷ boundary acres), NOT response coverage
    (no on-scene times exist in the open data) — the blurb and legend say
    so, and carry the medical-share caveat (most dispatches are medical
    calls). Rendering: the same flat hood plane as stormwater,
    **provisionally LINEAR, clamp p97.5 of non-set-aside hoods** (skew
    check on real data is an open follow-up — the build session had no
    data access), plus the **31 station context dots** (`fire-stations`
    ScatterplotLayer, orange + white stroke, `depthTest: false` so they
    sit over the coplanar layers; lazy `web/data/fire_stations.json`,
    drawn whenever the service is checked — driver or not; a
    "Fire station" row joins the legend via `#legend-cats`). Checkbox
    hides on data files without the column, same guard as stormwater.
  **Plane sharing (2026-07-06):** the plane services (storm, fire) draw ONE
  `svc-plane` layer between them — two coplanar polygon layers would
  z-fight, and a non-driving plane's "neutral" render is the same slate
  surface anyway. `servicePlaneLayer(col)` paints the driver's column, or
  slate when roads drive; `svcScale(col)` holds the per-column runtime
  p97.5 clamps (replaced the storm-only `stormScale()`).
  Tooltip: EVERY service's number whatever is checked (the neutral layers'
  values stay readable there). Hood hover via the invisible `hood-hover` layer,
  as before. Title "Edmonton: City Services".
- **Ratio** (stage 3, the synthesis): ghost prisms of **revenue per road metre**
  (`revenue_per_acre / road_m_per_acre`, client-side — no pipeline change) over
  the network in all-neutral grey. Prism **colour is LOG** between the kept
  subset's p2.5–p97.5 (≈ $264–$3,253; FINDINGS §6.4 — first log metric, skew
  19.7 → 0.32), **height linear** (max kept ≈ $18k at the standard ~8.2 km peak;
  `ratioScale()` computes anchors at runtime, cached). **Off-scale grey + flat:**
  set-aside hoods AND hoods below `RATIO_ROAD_FLOOR = 5 m/acre` (denominator
  artifacts — WESTVIEW VILLAGE hits $1.3M/m on a near-zero road base). Default
  prism opacity **5%**, adjustable via the "Money plane" slider (`#layers` panel,
  visible in this view only). Tooltip: ratio + both components, or the off-scale
  reason. Legend: log gradient, `≤ $lo` / `$hi+`.

Shared machinery:
- **Lazy load:** `web/data/roads.geojson` (1.6 MB; ~400 dissolved features, slim
  `n`/`t`/`v` props — ARCHITECTURE `export_roads_web`) fetched once, on first
  non-Money view. Initial page payload unchanged.
- **`hood-hover` layer** (Roads + Ratio views): flat, invisible, pickable —
  carries the tooltips and lights the hovered hood (white α40, `depthTest:
  false`). The road lines and ratio prisms themselves are NOT pickable (picking
  ignores opacity; a prism always beat the roads, which is how this design
  started).
- Metric toggle in non-Money views only marks state (applies on return); the
  residential lens applies in Money AND Ratio (2026-07-03), disabled in
  Services. Services/Ratio buttons hide when the served GeoJSON predates the
  road column; a file with roads but no `storm_charge_per_acre` /
  `fire_events_per_acre` keeps the view and just hides that service's row.
- Headless-verified via Playwright (all three views: layer stacks, legend swaps,
  tooltips incl. floored/set-aside cases, slider visibility) 2026-07-02; lens ×
  view matrix (anchors, fills, button disable) 2026-07-03
  (`tools/profiling/verify-lens.js`); Services generalization 2026-07-05
  (`tools/profiling/verify-services.js` — chrome on entry, per-checkbox layer
  stacks, storm plane fills in all three colour states, independent p97.5
  clamp check, driver handoff on unchecking the driving service, tooltip,
  persistence round-trip; screenshots `tools/profiling/shot-services.js`);
  fire service 2026-07-06 (same script, extended: single shared plane with
  both plane services checked, station dots, fire p97.5 re-anchor, station
  legend row — fire checks skip cleanly on pre-fire data files. Verified
  against a mock bed with a SYNTHETIC fire column; the real-data eyeball
  waits for the first CI refresh — data.edmonton.ca was unreachable from
  the build session's environment).
  Translucent-prism depth-ordering quirks: same acceptance as the residential
  lens fade.

### Uses view (built 2026-07-03 — fourth view button; real geometry same day)
**The city's actual zoning geometry**, coloured by land-use category. Shows what
the land IS, not what it yields; the blurb states the zoning caveat
(designation ≠ built).

- **Ground layer = real bylaw polygons** (`web/data/zoning.geojson`, 1.2 MB —
  `export_zoning_web`: the 11.5k zoning polygons dissolved CITYWIDE into one
  MultiPolygon per category, **clipped to the setback-shrunk hood footprints
  (45 m, same as the prisms) so the neighbourhood "city block" gaps stay
  visible under the zoning fabric** (Peter's ask 2026-07-03), simplified 10 m,
  5 dp, single `u` prop). Lazy-loaded like roads, on first Uses view. Flat,
  not pickable; the invisible **hood-hover layer** on top carries the
  per-neighbourhood tooltip (the composition data's granularity) + hover
  highlight, and its (equally setback) footprint aligns with the visible
  blocks. **Fallback:** if the file is missing (older deploy / fetch failure)
  the view falls back to colouring each hood by its dominant category from
  the main GeoJSON, and the legend label switches "Zoned land use" →
  "Dominant zoned land use".
- **Geometry-validity gotcha (found live):** rounding coordinates AFTER a
  validity pass re-introduces degenerate rings, which deck.gl's tessellator
  renders as stray filled black triangles. `export_zoning_web` therefore snaps
  to the 1e-5 grid topology-aware (`shapely.set_precision`) before writing, so
  the served file holds exactly the validated geometry (read-back all-valid).
- Colours are static per feature: no updateTriggers. No extrusion (category is
  identity, not magnitude) and no roads layer.
- **Palette (dark bg):** 7 chromatic hues following zoning-map convention —
  sand `#ad8a3a` Residential, red `#e05252` Commercial, violet `#8f80e0`
  Industrial, brown-orange `#a54c1f` Mixed use, magenta `#d55181` Direct
  Control, blue `#2a63b8` Institutional, green `#27853a` River valley / parks —
  plus two **deliberate neutrals outside the identity set**: Future / rural
  takes the set-aside grey (the app's "outside the fiscal story" colour) and
  Unclassified a darker grey (never occurs on current data). Validated with the
  dataviz six checks against `#0a0a0f`: all in the dark lightness band, chroma
  floor, ≥3:1 contrast; **min all-pairs CVD ΔE 10.6** (protan, green↔sand) —
  the 8–12 floor band, carried by secondary encoding (45 m setback gaps between
  every polygon, hover tooltip naming the category, legend). Palette chosen by
  brute-force search through the validator, not eyeballed. The palette switcher
  (Inferno/Glow/Cividis) doesn't recolour this view — only the background
  changes; the categorical colours are fixed.
- **Legend** swaps the gradient bar for categorical swatch rows (`#legend-cats`),
  **data-driven**: the categories present in the zoning ground layer (8 today —
  the real geometry surfaces the mixed-use zones even though no hood is
  mixed-DOMINANT; unclassified is empty by construction). On the fallback
  path: only dominant-somewhere categories (7).
- **Tooltip:** dominant category + a **mini stacked composition bar**
  (`.mixbar` — 190×8 px, segments flex-grow proportional to each share in the
  category colours, 2px surface gaps between segments) + the full composition
  largest-first as text (sub-1% shares omitted), e.g. SOUTH EDMONTON COMMON →
  "Direct Control 81% · Institutional 17% · Future / rural 2%". `.tip` gained
  `max-width: 300px` so long compositions wrap.
- **Residential lens disables** here (like Roads) — residential land is already
  an explicit category; state persists and re-applies on leaving. The metric
  toggle just marks state, as in Roads/Ratio.
- **Old-data guard:** the Uses button hides when the served GeoJSON predates the
  composition columns (checks `frac_commercial`), same pattern as Roads/Ratio.
- Headless-verified 2026-07-03 (`tools/profiling/verify-uses.js`: legend row
  swap + restore, layer stack zoning-ground + hood-hover, 0/8 category fill
  mismatches, tooltip composition, lens disable/re-enable) + screenshot
  eyeball (`tools/profiling/shot-uses.js`); the lens × view regression matrix
  (`verify-lens.js`) re-run green after the applyView/refreshLegend changes.

### Glass view (built 2026-07-04 — fifth view button; grid cells same day)
The revenue-per-acre-infographic composition (the Urban3 style, with this
project's interactivity): **translucent 100 m grid-cell spikes** over an
**opaque neutral hood plane**. The cells carry all the metric signal; the
plane is mouseover geography. Implementation (`web/index.html`,
`state.view === "glass"`):
- **Two layers**: `glass-plane` — flat hood polygons, one neutral dark slate
  (`GLASS_PLANE_COLOR` `[50,53,63]`) for every hood EXCEPT set-aside hoods,
  which take the standard `SET_ASIDE_COLOR` grey so "off the fiscal scale"
  reads on the ground too; pickable + `autoHighlight` (the highlight shows
  through the glass). `glass-grid` — a `GridCellLayer` of the pipeline's
  100 m cells (`web/data/value_grid.json`, `export_value_grid.py`: property
  points binned in EPSG:3400, cell total ÷ cell GROUND acres — see
  ARCHITECTURE for the denominator decision), lazy-loaded like roads/zoning,
  at `state.prismOpacity`, not pickable.
- **Cell scale anchors** (`gridScale()`, per metric, cached — the
  `ratioScale()` pattern): colour clamp at the cells' **p97.5** (~$144k/acre
  revenue on 2025 data — the cell distribution is its own scale, far above
  the hood clamp), sqrt colour transform like the hood money metrics;
  **elevation parity** — the tallest cell (~$12.6M/acre — West Edmonton
  Mall, verified 2026-07-04: one $1.285B account whose 107-acre lot
  collapses onto a single point → one 2.47-acre cell) reaches exactly the
  money view's tallest hood prism. Both linear (the honesty rule). Legend
  relabels "… (100 m cells)".
- **Spike denominator toggle (added 2026-07-05)**: a "Ground acres | Lot
  acres" control in the layers panel (`#denom`, `state.denom`,
  `applyDenom()`), Glass-only, hidden when the grid file predates the
  lot-acre columns (`gridData.hasLot`). **Ground** (default) divides each
  cell's total by the cell's fixed 2.47 acres; **Lot** divides by the parcel
  acres the cell's properties own (`*_per_lot_acre` columns —
  `export_value_grid.py`, dedupe heuristic in
  `docs/FINDINGS_lot_dedupe.md`). Lot mode fixes the single-point-needle
  caveat: a large parcel's whole value lands in one cell under ground acres
  (WEM reads 2× the top downtown tower; per lot acre the tower is ~50× WEM —
  DATA.md §2). `gridColKey()` maps metric+denom to the grid column; scale
  anchors cache per column; cells with `null` lot acres (28 on 2025 data —
  no eligible lot size) are **dropped** from the lot render (filtered lists
  cached in `gridData.cellsFor` so moveend rebuilds diff to no-ops). Legend
  relabels "… per lot acre (100 m cells)" (lot clamp ~$105k revenue vs
  ~$144k ground); the blurb follows the denominator (`GLASS_BLURBS`). The
  denominator persists across view round-trips; the control hides outside
  Glass.
- **Spike opacity**: the ratio view's slider panel shows here too; entering
  Glass resets it to the view's own default (**60%**; Ratio stays 5%).
- **Metric-driven like Money**: the Revenue/Value toggle renders live
  (title follows the metric; the blurb stays the Glass one); the tooltip is
  the Money tooltip (plane-picked). The **residential lens disables** (grid
  cells carry no residential flag). Labels sit at the ground (like
  Roads/Uses).
- **Fallback**: when `value_grid.json` is absent (older deploy), the view
  renders translucent NEIGHBOURHOOD prisms — the coarse version of the same
  composition (no lens handling; the button is disabled here anyway).
- Headless-verified 2026-07-04, extended 2026-07-05
  (`tools/profiling/verify-glass.js`: layer stack, 358 neutral + 48
  set-aside plane fills / 0 mismatches, 34,675 cells, clamp == independent
  p97.5, elevation parity exact, mid-cell fill matches the ramp — all
  re-checked per denominator on its own non-null subset (34,647 lot cells) —
  slider → opacity live, per-view slider defaults, metric toggle chrome +
  cell legend under both denominators, denominator persistence + hide
  outside Glass, lens disabled, ground-z labels, money-branch tooltip) +
  screenshot eyeball at 60% and 100% (`tools/profiling/shot-glass.js`) and
  ground-vs-lot at 100% (`tools/profiling/shot-denom.js` — the WEM needle
  visibly collapses in lot mode; downtown becomes the sole peak).

---

## Open / unresolved

- **Top-cap edge colour — NOT finalized (as of 2026-06-26).** The developer is
  not happy with it yet. Tried so far: `[120,215,255]` bright cyan (too hot) →
  `[55,130,160]` dark teal (still a touch bright) → `[40,95,120]` deep muted teal
  (current, still not right). Still iterating — don't treat the current value as
  settled. Worth considering alongside the light-mode work below, since the right
  edge colour depends on the background.

---

## Interaction & navigation

The map opens tilted (pitch 52°) and relies on rotation to read the 3D
extrusion, so camera control is core to the UX — not a nicety.

**Current gestures** (MapLibre defaults — nothing in `index.html` customizes the
interaction handlers):

| Action | Desktop | Mobile / touch |
| --- | --- | --- |
| Spin / rotate (bearing) | Ctrl + drag | two-finger twist |
| Tilt (pitch) | Ctrl + drag (vertical) | two-finger drag up/down |
| Zoom | scroll | pinch |
| Pan | drag | one-finger drag |

**Gaps (as of 2026-06-26):**
- **No reset / compass control.** No `NavigationControl` is added, so there's no
  affordance to snap bearing back to north or reset pitch. A user who rotates into
  an awkward angle — easy to do on a phone — has no obvious way back.
- **Rotation is undiscoverable.** Both the desktop modifier (Ctrl) and the mobile
  two-finger twist are hidden; first-time users often don't realize the view spins
  at all, and the twist competes with pinch-zoom.

**Proposed fix:** add the standard control —
```js
map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }));
```
Gives a compass (tap to reset bearing), zoom buttons, and a pitch indicator. The
compass also doubles as a visible hint that the map rotates. Cheap, idiomatic, and
helps desktop and mobile alike. Not yet added — flagged here for a UX pass.

**Wishlist (later — to design as a UX pass):**
- **Recenter / reset-view button.** Distinct from the compass: snaps the *whole*
  camera back to the default `CENTER` / zoom / pitch / bearing in one tap, not just
  bearing-to-north. Needs a custom control (store the initial camera, `flyTo` it).
- Other camera/UX niceties to gather here as they come up (e.g. preset viewpoints,
  a "what am I looking at" intro hint, keyboard shortcuts list).

---

## Planned (later)

### Light mode
- Needs more than flipping the background: the inferno ramp and the cool edge are
  tuned for a dark backdrop and won't read the same on light. Expect to rework
  the background, the fill ramp's dark end, and `TOP_EDGE_COLOR` together.
- **Implementation direction:** factor the colour tunables into a named theme
  object (e.g. `THEMES.dark` / `THEMES.light`) rather than loose top-level
  constants, with a toggle. Keeps the two palettes from drifting.

### Colourblind mode
- The current sequential ramp varies mostly in **luminance**, which is already
  reasonably robust for red-green CVD (deuteranopia/protanopia). The main risk is
  **tritanopia** (blue-yellow), where the warm fills + cool teal edge could lose
  separation.
- **Implementation direction:** offer a CVD-safe ramp toggle. `cividis` is
  designed specifically so red-green CVD viewers perceive it near-identically to
  normal vision — a strong default for this mode. Verify any palette against a CVD
  simulator before shipping; don't rely on eyeballing.
- Fits the same theme-object structure as light mode — treat both as palette
  variants behind one toggle.

---

## Principles

- **Don't rely on colour alone.** Height already encodes `value_per_acre`
  redundantly with colour — keep it that way so the map survives any palette.
- **Verify, don't eyeball, accessibility.** Use a CVD simulator and (eventually)
  a contrast check; a screenshot under normal vision proves nothing about CVD.
- **One source of palette truth.** As modes land, all colours flow from the theme
  object so dark/light/CVD stay in sync.

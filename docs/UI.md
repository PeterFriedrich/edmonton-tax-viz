# UI & Accessibility (Phase 2 web map)

Visual theming and accessibility decisions for the interactive map. Phase 1
(static PNG) is out of scope. Render/performance tradeoffs live in
`PERFORMANCE.md`; data-shape decisions in `ARCHITECTURE.md`.

This file is the chronological **build log** (why each feature was built). For a
current-state **snapshot of every view × control combination** (what shows when,
what gates what, flagged awkward couplings), see `docs/CONTROLS_MATRIX.md`.
Mobile/small-screen layout: `docs/MOBILE_USABILITY.md`.

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
- **Colour Adjustment toggle (built 2026-07-07, `#coloradj` panel — top of the
  right-hand stack, ABOVE the lens controls).** The money/glass sqrt is now a runtime
  toggle (`state.colorAdjust`, default **on**), so `scaleT` returns sqrt only when the
  toggle is on; off = linear+clamp (**true magnitude**). Deliberately grouped apart
  from the lens controls (metric/palette/residential): it's about *how* colour renders,
  not *what* you're looking at. **The button label IS the state readout** — "Colour:
  sqrt scaling" / "Colour: linear" (2026-07-25). It previously carried a separate
  caption (`#coloradj-state`: "On — colour spread across distribution" / "Off — colour
  shows true magnitude"); that said the same thing at 2.5× the width and made the pod
  stick out (`#coloradj` 417px → **169px**, `#optpanel` 645px → 398px), so it was
  dropped at every breakpoint. The long form survives in the button's `title`, and the
  blurb's colour clause already spells out the linear case. Only
  bites in **money + glass** (the `scaleT` consumers) — greys out (disabled) in
  services/ratio/uses, which drive colour through their
  own transforms (`svcT` sqrt/linear, `ratioT` log). Height stays LINEAR either way.
  Legend gradient follows automatically (`legendGradient` → `scaleT`); the money/glass
  blurb's colour clause is swapped to match via `withColourClause` (honesty: prose must
  not contradict the render). *Fire's sqrt and ratio's log are NOT wired to this toggle
  — if Peter wants a single global "sqrt colour" switch, that's a follow-on.*
- **deck.gl gotcha:** colour accessors that depend on runtime state need that state in
  their `updateTriggers` (the data reference is stable, so deck.gl skips the re-render
  otherwise). The money `getFillColor` uses
  `[state.metric, state.ramp, state.residential, state.colorAdjust]` (glass grid +
  fallback carry `state.colorAdjust` too); the roads layer's `getLineColor` uses
  `state.ramp`. **Adding a runtime dependency to a `scaleT` accessor means adding it
  here — the Colour Adjustment toggle was a silent no-op until `state.colorAdjust`
  joined these triggers.**

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
- **Done 2026-07-07:** the "Color Adjustment vs lens controls" hierarchy + self-describing
  state labels shipped — see the Colour Adjustment toggle bullet above. Residential lens
  alpha / grey / clamp-percentile remain easy tunables. Residential lens itself not yet
  visually verified in a browser (no headless browser on the laptop).

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
    **SQRT colour (FINDINGS §6.5, decided 2026-07-06 on real data — raw
    skew +7.86, the project's worst), clamp p97.5 of non-set-aside
    hoods**, plus the **31 station context dots** (`fire-stations`
    ScatterplotLayer, orange + white stroke, `depthTest: false` so they
    sit over the coplanar layers; lazy `web/data/fire_stations.json`,
    drawn whenever the service is checked — driver or not; a
    "Fire station" row joins the legend via `#legend-cats`). Checkbox
    hides on data files without the column, same guard as stormwater.
  - **Water/sewer** (default off; utility lens #2, SPEC_utilities Lens 2,
    2026-07-07): **MODELED residential water + sanitary charge** —
    `water_charge_per_acre` colours the plane (**LINEAR**, FINDINGS §6.6),
    `water_fixed_per_acre` rides along so the tooltip shows the
    connection-vs-consumption split ("$X modeled water+sewer / acre / yr
    (fixed $Y)"). Blurb carries three caveats: modeled-not-billed,
    commercial-not-modeled, and consumption-tracks-household-density
    (Methods §G). Legend label names the 2026 tariff vintage. Checkbox
    hides on data files without the column, same guard as the others.
  - **Transit** (default off; fourth service, SPEC_services "Transit lens",
    2026-07-11): **SCHEDULED service supply** — `transit_dep_per_acre`
    (mean-weekday GTFS stop-events ÷ boundary acres), NOT ridership (no
    stop-level usage exists in open data) — blurb and legend say so, and
    carry the current-signup seasonality caveat (summer schedules run
    lighter; the metric steps at signup boundaries). Rendering: the shared
    flat hood plane, **SQRT colour (FINDINGS §6.8, decided 2026-07-11 on
    real data — raw skew +3.34, clamp/median 4.3×), clamp p97.5 of
    non-set-aside hoods**, plus **58 station context dots**
    (`transit-stations` ScatterplotLayer, blue + white stroke — the GTFS
    location_type-1 LRT stations + transit centres; lazy
    `web/data/transit_stations.json`, drawn whenever the service is
    checked; an "LRT station / transit centre" row joins the legend via
    `#legend-cats`, which now composes rows across fire + transit).
    Checkbox hides on data files without the column, same guard as the
    others.
  - **Service cost (roads+fire)** (default off; fifth service — the V2
    composite, SPEC_utilities decision 3, 2026-07-16): the one MODELED
    "city service cost per acre" — `svc_cost_per_acre` = road metres ×
    $50/m/yr + fire dispatches × (Fire Rescue budget ÷ citywide dispatches).
    A composite/summary line, NOT another single service; blurb and legend
    carry the mandatory "roads + fire only, never total city cost" and
    fixed-budget-allocation caveats. Rendering: the shared flat hood plane,
    **SQRT colour** (fire-dominated skew — downtown ≈90% fire, ~10× the
    suburban median), clamp p97.5 of non-set-aside hoods. No context dots.
    Checkbox hides on data files without the column (it ships on the first
    refresh after the metric PR #59), same guard as the others.
  **Plane sharing (2026-07-06):** the plane services (storm, fire, water, transit, servicecost) draw ONE
  `svc-plane` layer between them — two coplanar polygon layers would
  z-fight, and a non-driving plane's "neutral" render is the same slate
  surface anyway. `servicePlaneLayer(col)` paints the driver's column, or
  slate when roads drive; `svcScale(col)` holds the per-column runtime
  p97.5 clamps (replaced the storm-only `stormScale()`).
  Tooltip: EVERY service's number whatever is checked (the neutral layers'
  values stay readable there). Hood hover via the invisible `hood-hover` layer,
  as before. Title "Edmonton: City Services".
- **Ratio** (stage 3, the synthesis): ghost prisms of **revenue per unit of a
  picked levy-funded service** (client-side — no pipeline change) over the
  network in all-neutral grey. *2026-07-10: the denominator became a PICKER*
  ("Ratio denominator" control in the `#layers` panel, Ratio view only) —
  **per road metre** (`revenue_per_acre / road_m_per_acre`, the original),
  **per fire event** (`revenue_per_acre / fire_events_per_acre`), or — added
  2026-07-16, SPEC_utilities decision 3(b) — **per service $**
  (`revenue_per_acre / svc_cost_per_acre`, the V2 composite): a DIMENSIONLESS
  coverage ratio (revenue $ per modeled roads+fire $). Config in
  `RATIO_DENOMS`, state `state.ratioDenom` (persists across views like the
  acre denominator; picker opens on `hasFire || hasSvcCost`, and each button
  is column-guarded — the fire/service-cost options hide when their column is
  absent). Modeled EPCOR services (storm/water) are deliberately NOT offered —
  SPEC_utilities decision 3 (money-flow honesty). All three prism **colours
  are LOG** between each kept subset's p2.5–p97.5 (roads ≈ $264–$3,253,
  FINDINGS §6.4; fire ≈ $7,092–$298,901, §6.7; service-$ ≈ 1.8×–28×, raw skew
  2.4 → log 0.17), **height linear** (each denominator's max kept hood at the
  standard ~8.2 km peak; `ratioScale()` computes anchors at runtime, cached
  per denominator). The **service-$ ratio is MAGNITUDE, not break-even**
  (Peter 2026-07-16): the same log ramp, no 1.0 marking — the numerator is
  FULL property tax but the cost side is only two services, so it reads ≫1
  almost everywhere (median ≈5.8×); the blurb/tooltip own that ("not a sign
  the land pays its full way"). **Off-scale grey + flat:** set-aside hoods
  AND hoods below the denominator's floor (roads 5 m/acre — WESTVIEW VILLAGE
  hits $1.3M/m; fire 0.005 events/acre/yr — four annexed-fringe hoods hit
  $1.3–1.7M/event, plus four zero-event hoods; service-$ $230/acre — the
  near-zero-cost hoods). Title/blurb/legend/aside follow the picked
  denominator. Default prism opacity **5%**, adjustable via the "Money plane"
  slider (`#layers` panel, visible in this view only). Tooltip: ratio + both
  components, or the off-scale reason naming the floor. Legend: log gradient,
  `≤ $lo` / `$hi+` for the $/unit denominators, `≤ N×` / `N×+` for service-$
  (`boundFmt`).

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
  the build session's environment); ratio denominator picker 2026-07-10
  (`tools/profiling/verify-ratio-denom.js` — 27 checks against the real
  served file: visibility gating, chrome/legend swap, independent anchor
  recomputation for both denominators + the residential subset, fire-floor
  greying, height parity, tooltip prose, cross-view persistence;
  screenshots `tools/profiling/shot-ratio-denom.js`).
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
- Colours are static per feature: no updateTriggers. No extrusion on the
  ground layer (category is identity, not magnitude) and no roads layer.
- **Residential prisms (built 2026-07-10, Peter's ask: "how much residential
  is in each neighbourhood").** A layers-panel checkbox (`#uses-prisms`,
  `state.usesPrisms`, default off — unchecked, the view is exactly the flat
  fabric above) raises **translucent prisms over the zoning fabric: height =
  `frac_residential`**, the hood's share of ZONED area (the frac_* columns
  sum to 1), linear on a **fixed 0–100% scale**. The peak (`USES_PRISM_PEAK`
  2,500 m) is deliberately BELOW the ~8.2 km cross-view parity height: that
  parity is calibrated for extreme-skew money metrics where only outliers
  are tall, but a bounded share clusters at 40–95% (median 61%) — at full
  parity the city renders as a solid wall that buries the fabric (verified
  by screenshot before lowering). No parity is owed: a share isn't
  comparable to dollars. Fill is the Residential category's identity sand,
  constant — magnitude lives in height alone; opacity rides the shared
  prism slider (shows while checked; Uses entry default **35%**).
  Zero-share hoods (40 on 2025 data) are omitted from the layer — a flat
  translucent polygon would z-fight the coplanar fabric. Blurb gains the
  height sentence while on (honesty: the render gains a magnitude); labels
  ride the prism roofs (`labelZ`); state persists across views like the
  rest of the layers panel; prisms not pickable (hood-hover still carries
  the composition tooltip, which is where the exact % lives). Works over
  the dominant-colour fallback path too.
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
  Residential prisms verified 2026-07-10 (`verify-uses-prisms.js` — 20
  checks: control gating, stack on/off + ordering, elevation = frac ×
  `USES_PRISM_PEAK`, identity fill, zero-share filtering, slider wiring +
  per-view default, label roof-z, blurb swap, cross-view persistence;
  screenshots `shot-uses-prisms.js`), full regression suite re-run green.

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
- **Spike denominator toggle (added 2026-07-05; shared with the Money view
  2026-07-08)**: a "Ground acres | Lot acres" control in the layers panel
  (`#denom`, `state.denom`, `applyDenom()`), hidden when the grid file
  predates the lot-acre columns (`gridData.hasLot`). The same `state.denom`
  drives the Money view's neighbourhood toggle (below), so it persists across
  the two — flip to lot in Glass and Money shows lot too. **Ground** (default)
  divides each
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
- **Spike opacity — FIXED at 60%, no slider (2026-07-25).** Glass used to share
  the ratio view's slider, resetting to its own 60% default on entry. Peter: the
  slider is "no longer necessary in this lens" — 60% *is* the translucency that
  makes the composition legible, and nobody was tuning it. The control (and its
  "Money plane" header) now hides in Glass; `state.prismOpacity` is still what
  drives the grid layer, and entry still re-applies `VIEWS.glass.opacity`, so the
  render is byte-identical and a detour through Ratio (5%) can't strand a stale
  value. The blurb's "The slider sets spike opacity." sentence went with it —
  prose must not point at a control that isn't there. Ratio (5%), Uses' residential
  prisms (35%) and Development's activity grid keep their sliders.
- **Metric-driven like Money**: the Revenue/Value toggle renders live
  (title follows the metric; the blurb stays the Glass one); the tooltip is
  the Money tooltip (plane-picked). The **residential lens hides** (grid
  cells carry no residential flag; it greyed out until 2026-07-25). Labels sit
  at the ground (like Roads/Uses).
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

### Neighbourhood denominator toggle (Money view, built 2026-07-08)
The Glass "Ground acres | Lot acres" control, mirrored onto the **Money view's
neighbourhood prisms** — the "value per *developable* acre" view (Urban3-
analogous), an editorial alternative denominator, NOT a correction (the first
lens is cardinality-robust either way — `docs/FINDINGS_denominator_cardinality.md`).
Implementation (`web/index.html`):
- **Same control, shared state**: the `#denom` panel shows in Money too (the
  layers panel opens for it; the ghost-prism slider rows hide), gated on the
  hood GeoJSON carrying `value_per_lot_acre` (`state.hasHoodLot`, set at load).
  The header reads "Denominator" in Money, "Spike denominator" in Glass.
- **`moneyScale()`** (the `gridScale()`/`svcScale()` pattern, cached per
  column): **Ground** keeps each metric's fixed clamp + elevation (or the
  residential-subset clamp when the lens is on). **Lot** swaps to the
  `*_per_lot_acre` column with a **runtime p97.5 colour clamp** and **height
  parity** — the tallest lot-acre hood reaches exactly the tallest ground-acre
  prism (both LINEAR, the honesty rule). `moneyColKey()` maps metric+denom to
  the column; `fillFor`/`topRings`/`labelZ` take the column key.
- **Low-parcel guard**: hoods below **15% parcel land** (and hoods with no
  eligible parcels) carry a `null` `value_per_lot_acre` from the pipeline
  (`join_and_calculate.LOW_PARCEL_FRAC`), so lot mode renders them the
  set-aside grey and flat — otherwise the near-zero denominator explodes (Mill
  Woods Golf Course 0% → ×6960). On 2025 data 7 hoods suppress (6 set-aside +
  MAPLE RIDGE at 1.6%). `parcel_frac` still ships for the tooltip.
- **Chrome follows the denominator**: legend relabels "… per lot acre" with a
  runtime max ($77,714+ revenue vs $50k+ ground), the aside swatch reads "Set
  aside, or too little parcel land", the blurb swaps to the metric's `lotBlurb`
  (`moneyBlurb()`), and the tooltip shows "$… / lot acre" + "parcel land X% of
  area". Verified numbers: U of A $7.6M→$15.2M/ac ×2.0 (50% parcel), Rossdale
  ×2.8, Riverdale ×2.5 — river-valley/park/exempt-institutional hoods rise.
- Headless-verified (`tools/profiling/verify-money-denom.js`: control shown +
  header, column swap, clamp == independent p97.5, height parity exact,
  MAPLE RIDGE suppressed→grey+flat, U of A coloured, tooltip prose, denom
  persistence across a Glass round-trip — all PASS) + screenshots
  (`tools/profiling/shot-money-denom.js`).

### Residential revenue metric (Money view, built 2026-07-16)

A third `#toggle` metric — **Revenue | Value | Residential $**
(`res_revenue_per_acre`): the **residential-class share of the levy in
dollars** (`RESIDENTIAL` + `OTHER RESIDENTIAL` slices — houses, condos AND
apartment buildings; DATA.md §4 "Residential-revenue decomposition").
**Disambiguation — this is NOT the "Residential only" lens** (§ Residential-only
lens above): the lens *fades hoods* below the 0.50 zoned-area threshold and
never changes the dollars; this metric *changes the numerator* to
residential-class dollars and colours every hood by it. The two compose —
residential dollars on majority-residential-zoned land — and the lens's
subset re-clamp (`residentialClampFor`) is key-generic, so it just works.
Implementation (`web/index.html`):
- **A plain third `METRICS` entry**, so the whole Money/Glass path (clamp,
  legend, `withColourClause` blurb, denominator toggle via the
  `lotKey()` naming convention → `res_revenue_per_lot_acre`, low-parcel
  suppression) applies unchanged. `elevationScale` **equals Revenue's 0.033 on
  purpose** — residential bars read as directly comparable subsets of the
  total-revenue bars. Clamp $30k hand-set from the real-data p97.5 (~$28.5k).
- **Honesty line lives in the blurb**: "a subset of Revenue, not all of what
  the land pays — commercial and industrial dollars are excluded here."
- **Share tooltip line in ALL Money metrics**: "N% of revenue is residential",
  derived client-side as `res_revenue_per_acre / revenue_per_acre` (identical
  denominators cancel; no share column ships). Real-data anchors: citywide
  52.6%, hood median ~75%, DOWNTOWN ~16%.
- **Column-guarded** (`state.hasResRevenue`): the button hides on data files
  predating the column; no persistence, so `state.metric` can't be stuck on it.
- **Glass (real cells since 2026-07-17)**: the 100 m grid file carries
  `res_revenue_per_acre` / `res_revenue_per_lot_acre` (DATA.md §4, Glass grid
  variant), wired into the `gridData.columns` map — the whole Glass path
  (cell render, `gridScale()` runtime p97.5 clamp ≈ $58k, denominator toggle,
  "(100 m cells)" legend) applies unchanged. Zero-res cells (commercial/
  industrial) draw flat at the ramp bottom — a real $0, visually distinct from
  no-property gaps. On older grid files the columns index to −1 and the
  metric falls back to hood prisms with its own anchors (the pre-existing
  older-deploy fallback path).
- Headless-verified (`tools/profiling/verify-res-revenue.js`: guard, column
  drive, subset invariant res ≤ rev in every hood, share line == independent
  recompute, blurb honesty line, lens composition incl. subset re-clamp, lot
  denominator with independent p97.5, Glass branch-checked — grid cells with
  independent cell-clamp recompute + per-cell subset invariant when the
  columns are present, hood-prism fallback when absent — metric persistence —
  ALL PASS) + screenshots (`tools/profiling/shot-res-revenue.js`: plain +
  lens-composed + Glass cells).

### Non-residential revenue metric (Money view, built 2026-07-18)

A fourth `#toggle` metric — **Revenue | Value | Residential $ | Non-res $**
(`nonres_revenue_per_acre`): the **non-res-rate share of the levy in dollars**
(`COMMERCIAL` + `MA DERELICT` + `DESIGNATED IND PROPERTIES` slices — the
complement of Residential $ by rate class; DATA.md §4 "Non-residential
decomposition"; SPEC_industrial.md A1). Same construction as Residential $ in
every respect — a plain `METRICS` entry, so clamp/legend/blurb/denominator
toggle/lens re-clamp all apply unchanged:
- `elevationScale` = Revenue's 0.033 (comparable-subset bars); clamp **$50k**
  hand-set from the real-data p97.5 (~$48.4k — coincidentally Revenue's own
  clamp value).
- Blurb honesty line: "a subset of Revenue, not all of what the land pays —
  residential dollars are excluded here."
- No new tooltip line — the existing "N% of revenue is residential" line
  (shown for every Money metric) already implies the complement.
- **Column-guarded** (`state.hasNonresRevenue`); Glass cells via the two grid
  columns in `gridData.columns` (appended LAST in the payload, after
  `median_year_built`), hood-prism fallback on older files.
- Headless-verified (`tools/profiling/verify-nonres-revenue.js`: guard, column
  drive, subset invariant nonres ≤ rev AND res + nonres ≤ rev per hood and per
  cell, blurb honesty line, lot denominator with independent p97.5, Glass
  branch-checked, metric persistence — ALL PASS) + screenshots
  (`tools/profiling/shot-nonres-revenue.js`: plain + Glass cells; commercial
  corridors bright, residential fabric dark real-zeros — the inverse of the
  res pattern).

### Camera framing buttons: Center 2D / Center 3D (built 2026-07-24)

Two bottom-left buttons (`#viewbtns` row, stacked above the legend in the new
`#botleft` wrapper) that reframe the camera in one tap. The app is a 3D
extrusion viz, so these are core UX, not a nicety (see "Interaction &
navigation" below).

- **Center 3D** → the tilted default framing (`HOME`: `CENTER` / zoom 10.2 /
  pitch 52 / bearing −18). A whole-camera reset for after panning, zooming,
  rotating, or flattening.
- **Center 2D** → a straight-down, **north-up** plan (`HOME_2D`: same
  centre/zoom, pitch 0, **bearing 0**). Flattening while keeping the −18°
  tilt-era bearing read as a skew; 2D snaps north-aligned so the map squares to
  the frame. Shows gold while the camera is flat (`pitch < 1`), keyed off the
  live pitch so it stays right even if the user tilts by drag.
- **One source of framing truth:** `HOME` / `HOME_2D` constants drive the map
  constructor AND both buttons — no scattered pitch/bearing literals.
- **History:** shipped first as a single toggle "Flip to 2D/3D" (kept the
  bearing, which skewed), then split into the two framing presets above. The
  bottom-left placement was Peter's call.
- **Verified:** `tools/profiling/verify-center2d.js` (pitch 0 + bearing 0 +
  recenter, incl. from a rotated start) and `verify-recenter.js` (all four axes
  back to `HOME`, gold cleared). Both real-hit-test the buttons.

### Control hierarchy sizing: views bar, Options header (2026-07-25)

The stack now renders its tiers at the right relative weight. Previously `#views`
— Tier 1, the primary control — tied for the *smallest* type on screen, which is
why it under-read as chrome (`MOBILE_USABILITY.md`).

| Control | Tier | Before | After |
| --- | --- | --- | --- |
| `#views` | 1 (primary) | 11.5px / 6px 12px | **14px / 9px 18px** |
| `#toggle` (metric) | 2 | 12.5px / 7px 15px | unchanged |
| `#opt-fold` (Options) | — (header) | 11.5px / 6px 12px | **13px / 8px 14px** |
| `#coloradj`, `#lens` | 3 | 11.5px | unchanged |

- **Phones scale `#views` back** to 12.5px / 7px 11px in the `@media` block: at
  14px the four public views no longer fit one 390px row, and wrapping the primary
  control costs more than the size buys. Verified one row at 390px for both the
  4-view public and 5-view full builds.
- **`#opt-fold` gets `min-width: 180px`**, which widens the FOLDED header
  *leftward* — the pod is right-anchored, so extra width grows left. Bigger target,
  further from the corner, and the right edge stays flush with the bars above
  (measured: `#views` / `#toggle` / `#optpanel` all end at the same x). No effect
  when open, where the body is wider than the minimum. Chosen over shifting the
  pod left, which would have broken that flush edge when open.

### Compass with rotation arrows (built 2026-07-25)

A third bottom-left row (`#compass`, above `#viewbtns`): **rotate
counter-clockwise · needle · rotate clockwise**. This closes the two gaps the
Center buttons left open — rotation *discoverability* and an **in-place**
bearing-to-north.

- **Explicit arrow buttons, not a drag target.** The whole point is to advertise
  that the map rotates at all; drag-rotate (Ctrl+drag / two-finger twist) is
  invisible. Each arrow walks the bearing to the next **`ROT_STEP` = 30°** detent
  in its own direction (12 presses = a full turn), so presses land on a clean 30°
  grid and *re-align* it after a free drag-rotate.
- **The arrow you press is the direction the map turns.** Both the world and the
  needle rotate that way, so the mapping is self-evident. (Note MapLibre's
  bearing runs the other way — clockwise on screen means bearing *decreasing*.)
- **Rapid presses chain off the previous target, not the live bearing.**
  Mid-ease `getBearing()` returns an intermediate value that hasn't passed the
  last detent yet, so recomputing from it made the 2nd click a no-op. A press is
  chained only while its ease could still be running (`ROT_MS` = 300ms window),
  which is also what stops the target going stale after a drag.
- **The needle (`#tonorth`) snaps north IN PLACE** — bearing only, keeping
  position / zoom / tilt. This is the deliberate contrast with **Center 2D**,
  which reframes the whole city. The needle counter-rotates
  (`rotate(-bearing)`) so it holds true north, and the button takes a gold ring
  (`.north`) when already north-up.
- **Icons are inline SVG, not glyphs.** The headless font lacks the curved-arrow
  codepoints (same tofu class as U+24D8), and `◀`/`▶` would read as pan /
  prev-next rather than rotate. `currentColor` keeps them on the hover
  transition.
- **Verified:** `tools/profiling/verify-compass.js` — real hit-test on all three
  buttons, detent walk in both directions, the rapid-press chain (3 presses =
  90°), off-grid re-alignment, needle angle tracking, and `#tonorth` changing
  bearing *only*. Screenshot-checked at 1280px and 390px (the `#botleft` stack of
  compass + framing pair + legend fits a phone without collision).

### Control clickability regression + hit-test guard (fixed 2026-07-24)

The S65 foldable-Options refactor dropped `#layers` from the `pointer-events:
auto` flip list; since `#layers` carries `class="panel"` (`pointer-events:
none`), its Detail / Denominator / dev / services controls fell through to
`#opt-body` and were **unclickable on the live site**. Fix: restore
`pointer-events: auto` on the `#optpanel .panel` re-normalization rule (one
line, covers `#layers` uniformly). The functional `verify-*.js` suite missed it
because they actuate controls with `page.$eval(sel, b => b.click())` — a direct
JS `.click()` that bypasses `pointer-events` and z-order. Added
`tools/profiling/verify-controls-clickable.js`, which real-hit-tests every
visible control per view; **run it after any control-chrome / CSS refactor.**

### Sources & attribution pod (2026-07-25, P1.2)

The live map had **no** link to the repo, the data sources or the methodology —
the highest credibility-per-effort gap on the public-release list, and an
outstanding licence obligation (every dataset rendered is City of Edmonton open
data under the Open Government Licence, which asks for visible attribution).

- **The credit is the button label, not something behind the click** —
  `Data: City of Edmonton Open Data · 2025`. A link you have to find first
  doesn't attribute anything, so the licence-facing half is readable at rest and
  the popover carries only what a label can't. Same "the label is the readout"
  idiom as `#coloradj` (2026-07-25).
- **Every year comes from `status.json`, never a literal.** The manifest the
  pipeline already writes (`data_year` / `rate_year` / `zoning_year` /
  `generated`) is already fetched for the maintenance banner, so the pod rides
  that same request. This is deliberate: a hardcoded "2025" silently goes wrong
  every January (`RUNBOOK.md` year-roll). Each line degrades independently — a
  missing manifest leaves the vintages blank and the **credit still reads**,
  which the verify asserts by aborting the `status.json` route.
- **The panel says the thing the project must not bury:** revenue is *modelled,
  not billed* (mill rates applied to assessed value, not anyone's tax bill), the
  utility/service layers are modelled too, and they cover only the services this
  project can measure — never the full cost of running the city.
- **Denser background than the control pods** (0.92 vs the shared 0.7): it's a
  paragraph to read, not a strip of buttons. Matches `.tip` and `#banner`.
- **Two bugs the build surfaced, both in existing code:**
  1. **`#botleft` was eating pointer events across its whole box.** The wrapper
     (compass + Center 2D/3D + legend) had no `pointer-events: none`, so its
     rectangle — as wide as the legend — swallowed clicks. At 390px it reached
     the bottom-right pods and made the new credit button **unclickable**; at
     every size it was quietly stealing map drags in that corner. Every
     interactive child already sets `pointer-events: auto` for itself, so the
     wrapper just needed the `.panel`/`#controls` treatment. **Caught only
     because this verify uses a real `page.click()`** — the JS-`.click()` suites
     would have sailed past it (same lesson as the 2026-07-23 entry above).
  2. **Everything on the map shares `z-index: 1`,** so paint order fell back to
     DOM order and `#botleft` drew *through* the panel on a phone. `#about.open`
     now lifts to 5. Regression-tested with `elementFromPoint` over the overlap.

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

Rotation and tilt are also reachable without a modifier: the **compass arrows**
(bottom-left) step the bearing in 30° detents, and the Center buttons set tilt.

**Gaps (as of 2026-06-26; closed 2026-07-24 / 2026-07-25):**
- **~~No reset control.~~ CLOSED 2026-07-24** by the Center 2D / Center 3D
  framing buttons (see the build-log entry above) — one tap returns to the
  tilted default or a north-up plan.
- **~~Rotation is undiscoverable.~~ CLOSED 2026-07-25** by the compass row: the
  two arrow buttons make rotation visible and clickable (no Ctrl, no twist), and
  the needle both shows the current bearing and snaps north *in place*. The
  hidden gestures still work; they're no longer the only way. (The twist still
  competes with pinch-zoom on mobile — the arrows are the way around that.)

**Rejected: `NavigationControl`.** The idiomatic
`map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }))` was
the standing proposal, but a custom `#compass` won: it matches the app's chrome
(the stock control is light-themed and fights the dark palette), it gives
*explicit arrow buttons* instead of a drag-to-rotate target, and it drops the
zoom +/− buttons we don't want (scroll/pinch already cover zoom). See
`DECISIONS.md`.

**Wishlist (later — to design as a UX pass):**
- **~~Recenter / reset-view button.~~ BUILT 2026-07-24** as Center 3D (whole
  camera → `HOME`) + Center 2D (→ north-up `HOME_2D`). See the build-log entry.
- **~~Compass~~ BUILT 2026-07-25** as the custom `#compass` row (arrows + needle;
  in-place north-up). See the build-log entry.
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

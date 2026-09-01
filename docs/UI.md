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

- **Money** (default): the classic revenue/value prisms, opaque. Metric toggle
  and palette behave as before. Hood tooltip: active metric + `19.2 road m /
  acre` + `$967 revenue / road metre` (ratio omitted when road base is 0 /
  columns absent; set-aside tooltip unchanged).
  - ⚠️ **This bullet is a 2026-07-05 snapshot and three of its claims have since
    moved.** *"residential lens"* — **deleted** 2026-08 (`6fb448e`), redundant
    against the Residential $ metric; its fade was Money's only translucent
    element, which is why "always opaque" read as a rule later. The **road rows
    are now revenue-cuts-only and full-build-only** (2026-07-28), not
    unconditional. And **"always opaque" is no longer true** — see below.
  - ⚠️ **THE ONE OPACITY EXCEPTION (2026-08-16):** the institutional band prisms
    render at **alpha 128 with opaque edges** on the ≥25%-institutional hoods
    that also clear the consequence cut — **6 of 358 on Total**. Everything else
    in Money stays fully opaque, and `state.prismOpacity` is still `1` here (the
    exception is a per-layer fill alpha, not the ghost-prism channel that
    `ratio`/`glass`/`uses`/`development` use). **The depth-ordering quirk this
    file flags for translucent prisms was measured before shipping this time** —
    four camera angles, bearing 0/45/180/270° at pitch 30–70°, no incorrect
    occlusion against the opaque prisms behind. Rationale:
    `docs/SPEC_revenue.md` "Translucent prisms, not wireframes".
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

#### Amenity bands (built 2026-08-23 here — ⚠️ **moved out of Glass 2026-08-26**, see below)
Filter the cells by road-network distance to an LRT station (600 m) or a
catchment school (800 m). **The control no longer appears in Glass** — it is
Infill-only as of 2026-08-26. This entry is kept because the reasoning below
still governs the surviving control; only the dim rendering died with the move.
Design + the locked calls: `SPEC_development.md` "Amenity distance",
`DECISIONS.md` 2026-08-23 + 2026-08-26, state space in `CONTROLS_MATRIX.md`.
- **Two independent rows, not one composite switch** — the bands are ~14x
  apart in what they select (1.6% vs 21.8% of cells at 600 m) and ANDing the
  conventional pair leaves **0.8%**. One switch would hide that collapse
  behind a word, and would be a weighted index by another name.
- **~~Out-of-band cells DIM, they do not disappear.~~** ⚠️ **Gone 2026-08-26**
  with the Glass control (`AMENITY_DIM_ALPHA` and `amenityBlurb()` deleted). The
  reason it was a dim and not a hide still stands and transferred: at 1.6% a
  hard hide leaves scattered dots with nothing to place them against, and one
  stable cell array means a toggle cannot re-tessellate 34k cells — Infill's
  highlight keeps both properties.
- ⚠️ **The blurb had to say grey was "not zero and not set-aside"** — the legend
  already spends that grey on set-aside land, so a greyed CELL was ambiguous
  without the sentence. Retired with the dim; the surviving lesson is that the
  blurb carries the **live in-band count**, because at 1.6% a filtered map
  otherwise looks broken.
- ⚠️ **The negative phrasing does not survive two bands** — "further than 600 m
  of an LRT station AND within 800 m of a school" is a contradiction. The
  prose is built around what KEEPS the highlight.
- **Rows self-gate on their own column** and are hidden on a served file from
  before the pipeline (the house pattern). `syncAmenityControls` runs from
  `applyView` **after** `await ensureGridData()`, and once at init because
  `applyView` is not called on load.
- Headless-verified 2026-08-23 (`tools/profiling/verify-amenity.js`, then 24
  checks). Blurb height measured rather than assumed: +113px, still clearing
  `#botleft` by 166px at 1280x720.

#### Extended to Infill (built 2026-08-25)
The same `#amenity` checkboxes were added under the Infill lens (reading the
same `value_grid.json` file Glass renders) — housing the "distance to LRT/
schools" thread that Peter originally asked for under Infill but which
`DECISIONS.md` 2026-08-22 kept out of the score itself. `syncAmenityControls`
widened from `v === "glass"` to `v === "glass" || v === "infill"`;
`ensureGridData()` fetches on entering either view.
- **Rendering direction inverts, deliberately.** Glass DIMMED out-of-band cells
  (there was a metric colour to withhold). Infill has no per-cell metric to
  withhold — the hood-level suitability×activity score never changes — so it
  HIGHLIGHTS in-band cells instead: a flat, non-extruded, non-pickable
  `GridCellLayer` (`infill-amenity-grid`, `AMENITY_HIGHLIGHT_COLOR` — white at
  alpha 70) drawn over `infill-plane`, present only while a band is checked.
  Reuses `amenityInBand` — a null distance is OUT of band.
  `infillAmenityBlurb()` is the Infill-specific sentence ("marks reach only;
  the coloured score underneath is unchanged").
- ⚠️ **This is a placeholder, not a finished cell-grain Infill lens.** A real
  per-cell score is still blocked on two open items in
  `docs/ANALYSIS_BACKLOG.md` §12 (a per-cell residential-gate equivalent, and
  what a diverging score means as a height) — see `SPEC_development.md`
  "Amenity distance" for the full reasoning.

#### Removed from Glass (2026-08-26) — Infill is the only home
Peter, seeing the rows under Money → 100 m grid: *"remove it from money."*
Nothing had regressed — 2026-08-25 **widened** the gate rather than moving it,
so both views carried the control for a day. Two copies of one control read as
clutter rather than as two questions, and Infill is the lens the filter was
asked for. `DECISIONS.md` 2026-08-26.
- `syncAmenityControls` gates on `v === "infill"` alone; `applyAmenity` no
  longer branches on the view. `ensureGridData()`'s fetch gate is **unchanged**
  — Glass still needs the grid file for its own spikes.
- **Deleted, not left dormant:** `AMENITY_DIM_ALPHA`, `amenityBlurb()`, the
  `glass-grid` fill branch and its two `state.amenity` `updateTriggers`.
  `amenityWhichPhrase()` survives with one caller (Infill's blurb).
- ⚠️ **Band state persists across views**, so the removal has to be *asserted*:
  `verify-amenity.js` (now 30 checks) enters Glass **with a band switched on**
  and requires the section hidden, `dimmed === 0`, and no band sentence in the
  blurb. Without that check the dim could come back silently.
- The cross-view correctness check died with the second copy (it compared
  Infill's highlighted count to Glass's lit count). Replaced by something
  stronger: the rendered highlight count is now checked against a count
  re-derived from the **raw `dist_lrt_m` column** at a hardcoded 600 m, so the
  render is measured against the file rather than against the rule that drew it
  — and moving `AMENITY_BANDS` without moving the label fails loudly.

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
data under the Open Government Licence, which asks for an attribution statement
plus a link to the licence — **verified against the licence text 2026-07-26**;
see "What other maps actually do" below for what it does and doesn't require
about placement, and for the two gaps that verification caught).

- **The button is a short entry point: `Data & Methods`.** It shipped as the full
  credit (`Data: City of Edmonton Open Data · 2025`) on the theory that a link
  you have to find first attributes nothing — **reverted within the hour**, on
  geometry *and* on convention (below). That label measured **294px**; at 390px `#legend` reaches x=304, so
  the button was painted straight on top of the legend text (Peter: "it's still
  overlapping"). The short label clears it (246..367 against a cluster ending at
  237) at both 390 and 360px. Attribution isn't weakened — the City of Edmonton
  credit and the Open Government Licence are the first thing in the panel, and
  the map's own MapLibre attribution uses the same collapsed pattern. **The
  lesson: a label carrying prose has to be measured against the other anchored
  chrome before it's called a design.**
- **Phones also bound `#botleft`** (`max-width: calc(100vw - 175px)`) so
  `#legend`'s longest line ("Set aside — natural / undeveloped land") wraps
  instead of running under the right-hand column. The bar and scale are a fixed
  200px, so only the aside moves.
- Panel heading is **"Important caveats"** (was "Read the numbers carefully" —
  Peter, same pass).

#### What other maps actually do (2026-07-25)

Peter asked the right question after the reversal — *what does everyone else
use?* The answer settles whether "behind one tap" is a compromise or the norm.
**It's the norm.**

| Pattern | Who | Notes |
|---|---|---|
| **A bare ⓘ glyph, bottom-right, expanding inline on tap** | Leaflet, MapLibre, Mapbox — the library default | Their attribution controls **auto-collapse to ⓘ on narrow screens** (`compact: true`). This is the single most common mobile map-attribution pattern. |
| **Tiny always-on credit text** | OSM-based sites ("© OpenStreetMap contributors") | Works while the string is short; it's exactly what failed here at 294px. |
| **A word button** | civic dashboards | Almost always *About* / *Sources* / *Data* / *About this data* / *Legal* — **essentially never the word "Attribution"**, which is jargon nobody scans for. |

Two conclusions this locks in:

1. **`Data & Methods` is squarely conventional.** No reason to revisit the label.
2. **The claim that drove the original design was overstated.** "A link behind a
   click attributes nothing" is not how the field treats it — the collapsed-ⓘ
   pattern exists *precisely* so attribution survives small screens, and the
   major providers accept it (OSM's guidance allows credit behind an interactive
   element on constrained displays as long as it's discoverable in-page).

**A wrinkle specific to this map: there is no basemap.** The style is
`sources: {}` — every pixel is drawn from our own GeoJSON, no tile provider. So
the MapLibre ⓘ in the corner credits the *library*, not any tiles, and the
OSM/Mapbox attribution regimes don't apply at all. **The only obligation in play
is the Open Government Licence – City of Edmonton on the data**, which the panel
carries.

**VERIFIED 2026-07-26 — read directly, and the placement assumption holds.**
The Open Government Licence – City of Edmonton (v1.0, July 2022; a near-verbatim
adaptation of OGL–Canada 2.0) requires only:

> Acknowledge the source of the Information by including any attribution
> statement specified by the Information Provider(s) and, where possible,
> provide a link to this licence.

**Nothing about placement.** So the collapsed pod stands and the surfaced-credit
design does not come back — the one thing that would have argued for it is
absent. Text: `data.edmonton.ca/stories/s/City-of-Edmonton-Open-Data-Terms-of-Use/msh8-if28/`.

Reading it did surface **two gaps in what shipped**, both fixed the same day:

1. **No link to the licence** — "where possible" plainly applied (the pod
   already linked two other things). This was the one unambiguous miss.
2. **The prescribed statement was paraphrased.** Where the provider specifies no
   statement of its own, the licence mandates exact wording: *"Contains
   information licensed under the Open Government Licence – City of Edmonton."*
   Socrata carries only `attribution: "City of Edmonton"` (a "data provided by"
   field, not a statement) across seven datasets, so the fallback wording
   governs. It is now present **verbatim** and asserted as such by
   `verify-about.js` — a reworded version is not compliance.

Also added, **not required by the licence**: a non-endorsement line. The licence
grants no right to imply official status or endorsement, and a civic map built
from City data is precisely what a reader might mistake for official.
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

---

## Removing the residential fade lens; colour scaling moves to the bottom (2026-07-26)

Peter: *"remove Highlight residential as an option — it feels redundant / not as
good as our %residential."*

**Why it was redundant, specifically.** The lens faded every neighbourhood below
50% residential *zoned area*. That is a **binary** cut, and both of the things
that now answer the same question are **continuous**:

1. The **Residential** revenue cut in `#toggle` (shipped hours earlier the same
   day) shows residential dollars directly, per neighbourhood, on the real scale.
2. Every Money tooltip already carries `X% of revenue is residential`.

The lens could only say "mostly residential: yes/no". Both successors give the
magnitude. It was also the source of a genuine confusion the docs had to keep
disambiguating — "Highlight residential" (a fade on zoned area) vs "Residential
$" (tax dollars) — and that footgun disappears with it.

**What came out:** `state.residential`, `applyLens`, `residentialClampFor` and its
cache, the `LENS_FADE_*` constants, the fade branches in `fillFor` / the ratio
extrusion fill / the roof edges, the residential anchor set in `ratioScale`, and
both legend fade branches.

**What deliberately stayed: `is_residential`.** It is load-bearing for Infill's
opportunity gate (`p.is_residential === false && infillScore(p) > 0`). Removing a
control is not licence to remove the column it happened to read — that was worth
checking before deleting, and it was the one thing that would have broken quietly.

### The knock-on: the Options panel is now one column

`#opt-pres` existed to stack two presentation pods. With the lens gone it held
one, so the wrapper and its `syncPresColumn` helper were deleted and `#coloradj`
became a direct child of `#opt-body` — which also means hiding it now takes its
own row with it, needing no collapse step at all.

Peter asked for it at the **bottom**, and the reason generalises: `#coloradj` is
the only control in the panel that changes how the data is *drawn* rather than
*which data is shown*, so it belongs after the sections it modifies.

**Measured:** the panel went two-column → one and **398px → 216px** wide at
1440px. Worth recording that "Ground acres" wrapping to two lines is
**pre-existing** — measured against master before the change, precisely so the
narrower panel didn't get blamed for it.

## Geographic reference layer — river + Anthony Henday ring (2026-07-27)

Tier 1 of the reference-geography brief. The map has **no basemap tiles** —
`web/index.html` has said "just a dark backdrop" since v1 — so a first-time
viewer had no way to tell which part of the city a prism sat in. Two shapes fix
that: the North Saskatchewan River and the ring road. Flat greys, unlabelled,
not pickable, no metric attached.

**The layer-order finding — and it splits by feature.** The instinct is to put
reference geography *underneath* the data, the way a basemap sits under a
choropleth. For the **ring road** that is wrong here: Edmonton's hood polygons
tile straight across it, so composed first it changed **0.38% of screen
pixels** — 99.6% occluded. Composed last it changes **1.22%** and reads clearly
around the perimeter.

For the **river** the opposite holds, which only became clear once it shipped.
Drawn on top it cut into the neighbourhood geometry and glitched along the
shared edges. The reason: the hood fabric **already traces the river** — the
valley is set-aside parkland, so there is a river-shaped seam through the
choropleth — and painting the water over it fought a shape that was already
there. Underneath, the river shows *through* that seam and runs on past the
city limit where nothing occludes it, which is the better read anyway: a city
sitting on a river that comes from and goes somewhere.

So the two **bracket** the view's own layers rather than sitting together, and
`depthTest` splits with them: ON for the ring road, because with it off the road
cut across the faces of the downtown towers (it is *ground*, not a billboarded
marker like the fire dots and LRT lines); OFF for the river, which is the
backdrop — drawn before everything, so it neither occludes nor z-fights.

**The river runs 60 km past the city**, sized against the default camera rather
than guessed: at HOME zoom 10.2 and latitude 53.5 the scale is ~79 m/px, so a
1440px viewport spans ~114 km flat and the 52° pitch pushes the horizon further,
against a city half-width of only ~15 km. Those tails land on the bare `#0a0a0f`
backdrop, where the original `[26,34,48]` was effectively invisible — extending a
river nobody can see achieves nothing — so the fill lifted to `[50,66,94]`, still
~5× the backdrop luminance and far below the set-aside grey.

**Composed around, not inside.** `buildLayers()` now wraps `buildViewLayers()`
and appends the reference layer once. `buildViewLayers` has one `return` per
view; prepending in each branch would have left a future view silently shipping
without orientation.

**Toggle placement.** It sits in the `#a11y` **Display** popover next to
`Neighbourhood labels`, not in the Options panel — Display is where
view-independent map furniture lives, whereas `#layers` content is per-view. It
defaults **ON** where labels default off: labels are an enhancement, this is the
only thing telling a newcomer where they are.

**Data-side note worth carrying:** the ring is extracted from the road feed
already in the repo, not a new source, but naming alone gives 275.7 km of ramps
and interchange lanes and a 2.9 km hole where Highway 216 runs concurrent with
Highway 14. See `DECISIONS.md` 2026-07-27 and `data/DATA.md` §14.

## Regional place names (2026-07-27)

The river and the ring road say *where the shapes are*; they do not say *what
is next door*. Seven neighbouring municipalities now float as names on the
backdrop — St. Albert, Sherwood Park, Spruce Grove, Fort Saskatchewan, Leduc,
Beaumont, Devon — which is the rest of what a first-time viewer needs to place
the frame.

**Two toggles now co-own one layer, and that is the whole design.** The
locked Tier-2 decision said district and place names must feed the *existing*
`visibleLabels()` declutterer rather than get a second label layer, because a
second layer cannot see the first one's boxes and the names would stack. That
still holds. But it silently implied something else that does not: hood labels
are gated on `state.labels`, which **ships `false`**. Routing orientation names
through that flag would have hidden the thing a newcomer most needs behind a
checkbox they never flip — while the river and ring road are deliberately on.

So the two concerns got separated. `labelPool()` gates each class on its own
flag and concatenates; `labelLayer()` gates on **the pool being non-empty**
rather than on `state.labels`; one TextLayer, one sweep, two independent
switches. Anything reasoning "labels off ⇒ no text layer" is now wrong.

**The sweep needed a priority it did not have.** It ordered by polygon area —
bigger hoods win the spot — and a place is a `Point`, which has no area. An
explicit `prio` now sorts first (places win), area second. Faking a huge area
would have worked and would have been the kind of thing that drifts.

**Two smaller things that were real.** `labelZ(p)` indexes into hood
properties to find the prism roof a label sits on; places carry none and stand
outside the city where nothing is extruded, so it guards on `!p` and returns
ground. And the box math multiplied by the `LABEL_SIZE` constant — with two
text sizes in one pool that either overlaps or over-reserves, so it reads
`d.size`.

**Sizing and register.** 12 px against the hood labels' 15, `[150,160,178]`
against their near-white, uppercase like them. Context at the edge of the
frame: legible without competing with the data for the eye.

**Leduc does not show at the default camera** — it projects to y≈1102 in a
900px viewport under HOME zoom and 52° pitch, so the sweep culls it as
offscreen, correctly. It appears on pan or zoom-out. The verify suite asserts
a healthy majority rather than all seven for exactly this reason.

**~~Known gap:~~ CLOSED 2026-07-27** — the sweep had no knowledge of DOM chrome,
so a name could land under the Options panel. See "Labels dodge the chrome".

## The frozen sweep, and place labels that scale (2026-07-27)

Peter, on the shipped names: *"Currently only see St. Albert, until I turn the
names on and off. Also they a bit too big on zoom out."* One symptom, two
causes, both fallout from the two-toggle split above.

**The re-cull was gated on the wrong flag.** The `moveend` hook read
`if (state.labels)` — the last place still reasoning "labels off ⇒ no text
layer", which the split had just made wrong. Hood labels ship **off**, so in the
default state the sweep ran once at load and then never again. Measured: the
drawn set stayed the same 6 names from zoom 10.2 down to 6.0, while a fresh
sweep at those cameras would have returned 7, 5, 4 and 2. Toggling the reference
checkbox rebuilds the layers for its own reasons, which is the only thing that
unstuck it — hence "until I turn the names on and off". Now gated on
`labelPool().length`.

**Comparing DRAWN against a FRESH sweep is what catches this**, and it is the
check the suite gained. Either number alone looks entirely plausible; only the
mismatch is wrong. A screenshot would not have caught it either — the frame
shows *names*, just the previous camera's names.

**The names did not shrink with the map.** `sizeUnits: "pixels"` is right for a
label you want legible at any zoom, but pulling back leaves the text at a fixed
size against a shrinking city — oversized, and worse, the collision boxes stay
just as wide while the anchors converge, so the sweep starts dropping names
exactly when orientation matters most. `placeSize()` now interpolates 12 px →
7 px between zoom 10 and 7, floored so they stay legible. All seven survive at
z=8 where five did.

**Which names survived a collapse was arbitrary.** Every place ties on `prio`
and carries `area: 0`, so the stable sort fell through to **file order** — St.
Albert is simply first in `PLACES`. Scaling makes the collapse rare rather than
principled; if it ever needs a real tie-break, that is the seam.

**Two implementation notes.** The effective size is resolved **once**, in the
sweep, so the collision box and the glyphs it reserves room for cannot
disagree — `getSize` reads it back off the datum. And it rides out on a
**copy**: the anchor arrays are memoized and shared across every sweep, so
writing the scaled size back onto an anchor would leak one camera's zoom into
the next one's box math.

This is the app's first zoom-dependent render behaviour — Tier 1's river and
ring road remain deliberately zoom-independent. Sizes update when the camera
**settles**, not per frame, consistent with how the cull has always worked.

## Labels dodge the chrome (2026-07-27)

The third of the three label bugs, and the one that had been logged longest.
`visibleLabels()` declutters labels against *each other* in screen space, but
the HTML panels sit over the same canvas — so a label could win its spot and
then be painted underneath one. FORT SASKATCHEWAN did, under the Options panel
at 1440×900.

An occluded label is now **skipped**, exactly like the existing offscreen cull,
rather than kept and then lost: it can neither be read nor sensibly block a
label that *isn't* occluded.

**Which boxes count, and why it isn't just "the opaque ones".** `CHROME_IDS` is
an explicit closed list. Two membership calls are load-bearing:

- `#layers` and `#coloradj` are **absent**. They are borderless sections inside
  `#optpanel`, which paints the background for all of them — so `#optpanel`'s
  box is the real obstacle, and using the children would leave the gaps between
  them uncovered.
- `#title` and `#legend` paint **no background at all** and are included anyway.
  The test is whether the chrome makes a label unreadable, not whether it is
  opaque, and text-over-text is the case actually reported.

**A closed list that can rot is worse than no list**, since the failure is
silent and looks exactly like the original bug. So the verify suite asserts
`CHROME_IDS` **covers every `.panel` in the document** — each panel is either
named or has a named ancestor. Add a panel and forget this list, and the suite
fails.

**The chrome test is UNPADDED, unlike the label-vs-label sweep.** `LABEL_PAD`
is breathing room between two labels; a panel edge is not another label.
Charging it that clearance cost **DOWNTOWN** on a phone — its padding clipped
the Options panel by 3px while its glyphs cleared it by 5. Against chrome the
question is literally: do the glyphs land on it.

**Measured cost: none.** Readable-label counts are identical before and after —
32/32 at 1440×900, 25/25 at 390×844 — because only labels that were already
invisible are removed. Worth being honest that the "frees its spot for a name
that isn't occluded" rationale, while architecturally right, yielded **no
measurable gain**: a spot under a panel has nothing else competing for it.

**It matters far more on a phone**, as `MOBILE_USABILITY.md` predicted. Chrome
covers ~45% of a 390×844 screen against ~27% at 1440×900, and the mobile
before-shot had THE ORCHARDS AT ELLERSLIE painted across the compass buttons
and EDMONTON SOUTH EAST straight through the legend, obscuring the `$50k+`
scale label.

## Stock age withdrawn from Development; grid spikes default to 50% (2026-07-27)

Peter's call on the Stock-age Detail option: *"it's just not working well as an
option."* Removed. The Detail selector goes back to two choices, Neighbourhood
and 100 m grid — activity.

**Removed at the UI and render layer only.** `median_year_built` is still
produced by `export_value_grid.py` and still ships in `value_grid.json`
(173 kB, 6.9% of that file, 2.2% of total payload). The data is the expensive
half; a better presentation later should not need a pipeline regen. The
scaling analysis in `FINDINGS_stock_age_spike_scaling.md` stands on its own.

**The unplanned win: Development no longer fetches `value_grid.json` at all.**
`ensureAgeData()` kicked that 2.5 MB file on *every* entry to the view — not on
demand, deliberately up front, so the Stock-age button could be offered before
you toggled into grid mode. Development's own spikes come from `dev_grid.json`
(362 kB), and `gridData` has no consumer outside Glass. So a view that never
needed the big file was pulling it every time.

**Three things folded away with it**, each of which existed only for the age
mode and each of which was a special case in shared code:

- the sqrt exemption in `devT` — year is an interval scale, so it alone
  skipped the locked sqrt colour transform;
- the Metric/Window suppression in `syncDevControls` — a stock snapshot has no
  permit metric or window, so it hid two pickers the other modes show;
- the age branch of the Development legend.

**It also closed two of the flagged "weird combos"** in `CONTROLS_MATRIX.md`
§5: #3 (*"Stock age still morphs the Development panel"*) and #6 (*"Stock age
is arguably a lens wearing a Detail costume"*). #6 is worth keeping in mind in
the shape it was written — **if a control ignores the pickers around it, it is
probably a lens, not a detail mode.** Industrial was the surviving instance.

⚠️ **Industrial stopped being that instance on 2026-08-18**, and the way it
stopped is the point. It ignored the Detail picker (the toggle hid) not because
it was secretly a lens, but because **nobody had built its cells** — the
"ignores its neighbours" signal was reporting missing data, not a mis-typed
control. Giving it a grid made it an ordinary metric that answers to all three
pickers. ⚠️ **So the #6 heuristic needs a second question before it fires: is
this control ignoring its neighbours because it is a different KIND of thing,
or because its version of the shared thing was never built?** Stock age was the
first; Industrial was the second, and reading it as the first would have argued
for promoting it to a lens instead of finishing it.

**Separately: the activity spikes now default to 50% opacity.**
`VIEWS.development.opacity` was `null`, commented *"no prisms in this view"* —
which was untrue once the Detail grid shipped. Because no default was ever
applied on entry, the spikes inherited whatever `state.prismOpacity` last held:
100% on a fresh load, or **5% if the viewer had passed through Ratio**. Setting
it to 50 makes entry deterministic and lets the neutral hood plane read through
the spikes. The slider still shows in grid mode, so it is a starting point, not
a fixed value like Glass's 60%.

## The temporal lens lands: sparkline + pinned history panel (2026-07-29)

Phase 3 of `SPEC_temporal.md`, and the last piece of that lens — the data side
shipped 2026-07-28. Two surfaces: a **sparkline on the hover tooltip** as the
glance, and **`#temporal`**, a click-to-pin panel, as the readable version. The
split was already decided; **the panel's design was the open item**, and it is
settled in `SPEC_temporal.md` §2 (a table of six choices with their reasons).
The short version of the layout:

- **Left column under `#title`, `top: 210px`.** The only region no other chrome
  claims, so pinning cannot bury a control. The offset was **measured, not
  estimated** — the title's box runs 176–179px across all five views because the
  blurb wraps to ~8 lines at 360px, and the first pass at 128px overlapped it.
  `verify-temporal.js` asserts clearance against `#title`, `#botleft` and
  `#controls`, so a future longer blurb fails a check instead of overlapping.
- **Three dismissals: the ×, Escape, a second click on the pinned hood.**
  Clicking *another* hood re-pins — pin-then-browse is the point — and an
  **empty-map click is deliberately inert**, so the panel can't vanish on the
  tail of a drag. Escape earns its place here more than on the popovers: this
  panel is opened by clicking the *map*, so there is no button to un-press.
- **Phone: a bottom sheet.** Its desktop home is where the control column lives
  at ≤640px. It covers the legend and both bottom-right pods, which is fine in a
  way covering a *control* is not — a deliberate tap opens it and a deliberate
  tap closes it.

### The sparkline goes on every view's tooltip, in one wrapper

`tooltipFor` is now a thin wrapper over the old per-view body (renamed
`viewTooltip`) that appends the sparkline and one muted row. A hood's assessment
history is a fact about the **neighbourhood**, not about the lens you happen to
be in, and a teaser nobody sees in the view they're in is not a teaser. One
wrapper is also a smaller change than six branch edits that must then stay in
step. The row carries **`click to pin`** — the panel is undiscoverable otherwise,
the same argument that made the compass visible buttons instead of relying on
drag-rotate.

### Two rendering invariants, both silent, both measured rather than eyeballed

**1. 2024 must LOOK absent.** x is scaled from the **year value**, never the
array index, and the line is drawn as **runs split at every gap** — so 2023→2025
spans twice an ordinary step and no stroke bridges the hole. The shaded band
covers the **missing year only** (half-step bounds); shading the whole 2023→2025
run would claim 2023 and 2025 are missing too. The break is **derived from the
year steps**, not from a hard-coded `2024`, so January's roll-forward needs no
edit here.

The reason this is a *verify* concern and not a *look at it* concern: on a
13-point series, index positioning and a bridging polyline are **both invisible
to the eye**. So the script measures — the 2023→2025 x-distance must be 2.00×
an ordinary step, and no path may have points on both sides of the band.

**2. The y axis is not zero-based, so both endpoints are labelled.** Most hoods
are well under 1% of the citywide base; zero-basing would flatten 406 series to
a flat line at the bottom and show nothing. Scaling to each series' own range is
what makes the shape legible, and printing the min and max is what keeps that
honest. The labels needed **their own left gutter**: at `x=0` the max label
landed on the line, because 2012 is near Downtown's maximum.

### Three things caught by looking at it, after the checks were green

Worth recording because none of them were logic bugs, and all three were only
visible in a screenshot:

- **"no data" spilled out of the band.** The band was one year wide (~20px) and
  the label set horizontally ran onto the adjacent year's tick. Rotated −90° it
  fits the band's *height* instead — the usual way a narrow annotation band is
  labelled.
- **The band label collided with the last point.** Bottom-anchored text sat
  exactly where Downtown's 2025 dot lands, because 2025 is that series' minimum
  *and* the gap is the most recent span. Now vertically centred.
- **The phone sheet was too transparent.** At the desktop `0.92` the legend and
  both bottom-right pods read straight through the panel's text. `0.985` in the
  media block. Recorded in `MOBILE_USABILITY.md` §1: **0.92 is enough over the
  map, not over other chrome** — and on a phone almost anything full-width lands
  on other chrome.

### Gating

`|| !FULL_BUILD` beside a defensive fetch, the established idiom: no file or a
broken one leaves the lens simply absent and every other view working.
**`web/data/temporal.json` still ships to the public root**, which looks like 89
kB of dead weight and is not — `/full/` is `index.html` alone under
`<base href="../" />`, so `./data/temporal.json` resolves to the root copy.
Verified in the **built** tree (public root: zero requests for it; `/full/`: 200,
no 4xx anywhere), because that is the same failure shape as the `styles.css` 404
risk from the CSS extraction. `#temporal` is in `CHROME_IDS`, so the label sweep
dodges it — and the panel re-runs the sweep on open and close rather than waiting
for the next camera move.

## Popup or panel: a readout mode, and why the popup shrinks instead of vanishing (2026-07-30)

Peter, having used the shipped temporal lens: *"I don't want both the panel and
pop up appearing at the same time. So basically like a button that will convert
you to panel mode, or back to pop up mode."* Then, on being shown the cost:
*"reduce the popup to just the primary metric once you go panel."*

`#hoodmode` sits in `#opt-body` directly under `#coloradj`, shares all of its
styling, and follows the same **label-is-the-state** idiom: `Readout: popup` /
`Readout: panel`, gold when panel mode is engaged. Tier 3 — it applies in every
view and is about presentation, not which data is shown. It is **hidden until
`web/data/temporal.json` loads**, so it never appears in the public build: with no
panel to switch to, the control would offer a mode that does not exist.

### The decision that mattered was reduce, not suppress

The obvious reading of "don't show both" is *suppress the tooltip in panel mode*.
That would have been wrong, and the reason generalises: **the tooltip is the only
thing carrying the view's own number** — `$248,462 / acre`, the residential share,
road metres. Suppress it and panel mode goes blind in every view, so browsing
hood to hood (the exact thing the panel is for) gets worse, not better. Peter's
answer was better than either option put to him: keep the popup, **shrink it to
the headline number**. The objection was never "two surfaces at once", it was
**two dense blocks competing**.

The sparkline and the `click to pin` hint also drop out in panel mode — the panel
already draws the chart, and the hint would be advertising a mode you are in.

### ⚠️ The reduction is per-view explicit, NOT "row 0"

`primaryRow(p)` names each view's headline itself. The tempting one-liner — take
the tooltip's first row — is right for money, ratio, uses, development and infill,
and **wrong for services**, whose rows lead with `road_m_per_acre` whenever roads
are present *regardless of which service is driving the ramp*. A positional rule
would print road supply under a stormwater-coloured map. Services reads
`state.svcDriver`.

`verify-hoodmode.js` asserts **both halves** of that: that the services rows
really do lead with roads (so the trap is real, not hypothetical), and that the
headline nonetheless follows the driver. A check that only asserted the second
half would still pass if someone quietly reordered the rows.

### Three gestures, three scopes

Deliberately layered, so none of them surprises:

| gesture | effect |
|---|---|
| the panel's **×** | clears the pinned hood; **stays** in panel mode, showing its prompt |
| **Escape** | leaves the mode entirely |
| **`#hoodmode`** | leaves the mode entirely |
| a **map click in popup mode** | enters panel mode *and* pins |

That last row is what keeps the tooltip's own "click to pin" hint truthful, and
makes the panel reachable without first finding the control. The button is then
the way back — and the way in for someone who would rather not click the map.

Panel mode with nothing pinned shows a **prompt** ("Click a neighbourhood to see
its assessment history"), with the chart, read-out and the × all hidden. Entering
a mode has to look like it did something, and an × that closes nothing is worse
than no ×.

### The verify script caught its own contract changing

`verify-temporal.js` went red on exactly two checks, both intended: a second
click on the pinned hood no longer *closes* the panel, it unpins and leaves the
prompt. Both expectations were rewritten **deliberately, and one was made
stricter** — inertness of an empty-map click is now asserted as "no part of the
state moved" rather than "stays closed", which no longer depends on whatever state
the preceding click happened to leave behind. Worth noting as the good case: the
script did its job by disagreeing with the change, and the change was still right.

## Mill rates on the revenue lens: a pod on desktop, a paragraph on a phone (2026-08-01)

Peter: *"can we have the current relevant mill rates in the top left on this
lens? since thats an open spot anyway"*. It isn't an open spot, and both halves
of that sentence turned out to be wrong in ways only measurement showed.

**The column is the history panel's.** The "~500px free at 1440×900" in the brief
was measured with `#temporal` **closed**. Open, it is **308px** tall — its own CSS
comment says ~265 — and the slack between its bottom and the bottom-left cluster
is 211px at 1440×900 but **79px at 1366×768** and **31px at 1280×720**. There is
no room for a pod *and* a panel on a laptop.

**And "top left" is only empty on one of the three cuts.** `#title` runs
**140–499px** across the app; the residential and non-residential blurbs alone
push it from 196 to **256**. So the pod's `top` is read from the measured title
box on every sync, never a constant — a `ResizeObserver` on `#title` covers the
paths that write the blurb *after* the sync runs.

That measurement also exposed a **pre-existing bug**: `#temporal`'s own
`top: 210px` was pinned from a sweep that covered the five views on the default
metric only, and it paints over the blurb in **five** states — by 46px on the
money cuts, 158px in Change, 252px in Development, **289px in Infill**. Left
unfixed on purpose (in Infill the title ends at 499, the panel is 308 and the
legend starts at 729 — it does not fit anywhere), and written up in `TODO.md`.

### All three rates, always, with the billed ones lit

Peter's ruling, against the brief's "show only the relevant rate". Dropping rows
would hide the **7.6254-vs-24.2229 differential**, which is the fact the whole
revenue map rests on; and a fixed row count keeps the pod's height stable, which
the crowded column needs. `MILL_CUT_CLASSES` maps each cut to the classes it is
actually billed at — Total has **no entry on purpose**, so "no entry" reads as
"all" and a fourth class arriving in the manifest lights up under Total without a
matching line in the front end.

Both caveats are on the pod, visible rather than buried: **municipal levy only**
(the education levy is provincial), and **Farmland's 2025 rate is assumed**. The
second is driven by an `assumed` list in the manifest rather than typed into the
page, so it stops printing by itself the year the source publishes a real row.

### The phone form took two goes, and the second deleted the first

Shipped desktop-only first. Peter: *"no rates show on mobile"*, then a
description — *"stacked, like bullet points almost, top left, where the
description bubble would be, then folded in when you open the bubble"* — and then,
on seeing exactly that built: ***"i don't like the independent mill rates panel.
folding it into the tax revenue blurb is fine."***

The standalone version is worth recording because **everything it had to solve was
an artifact of it being a separate surface**:

| it needed | why | folded into the blurb |
|---|---|---|
| an anchor | "under the title" is not a phone location — `#title` collapsed is 20–43, but `#controls` owns **58–197** | nothing floats, so nothing must clear anything |
| its own card background | the map fills a phone screen; the pod sat on the downtown prisms, where 10.5px muted text is unreadable | the card already has one |
| to inherit the desktop yield | `#temporal.open ~ #millrates` | desktop-only *by construction* — a child of `#title` is not `#temporal`'s sibling |

`#millrates` is now re-parented into `#title` below 640px: the rates open and
close with the blurb and add **nothing** to the default render. Only the stacking
survives — one rate per row, because the desktop one-liner wraps at 360px and
breaks between a class and its number.

### The yield that reasoned about the wrong thing

That third row cost a shipped bug. `#temporal.open ~ #millrates` went out
**ungated**, under a comment claiming it was "desktop-only in effect" — which
reasoned about the **layout** (the panel is a bottom sheet on a phone, so they
never overlap) and not about the **selector**, which matched everywhere.
Switching the phone readout to **panel mode** blanked the rates with the sheet at
y≈799 and the pod at y≈207, nothing contending.

⚠️ **The fix was written, then falsified.** A media gate looked right and passed;
removing it *also* passed, because re-parenting had already made the selector
unmatchable on a phone. The gate was redundant and was dropped rather than shipped
under a comment calling it load-bearing. `verify-millrates.js` asserts the
**behaviour** — rates survive panel mode, rates hide with the blurb — so the
property holds however a future form achieves it.

### Rates are data, not copy

They ship in `status.json` as `municipal_rates`, derived by
`generate_status.py` from `data/mill_rates.json` (the manual, reviewed input), so
the January roll has one source and the page has none. `verify-millrates.js`
asserts every rate on screen against the served manifest, so a hand-edit to the
markup cannot put a wrong mill rate in front of a reader and still pass.

### Postscript: the report that was a cache

*"i'm still not seeing the mill rates on mobile… i can see it when i open it in a
private window on my phone."* The deploy was fine. `styles.css` has been a
separate file since 2026-07-29, so a **CSS-only change now has its own cache
lifetime** and can render stale against a fresh page — a failure that looks
exactly like a half-deployed feature. `RUNBOOK.md` §3c has the triage order;
cache-busting the stylesheet is proposed in `TODO.md`, not smuggled in.

---

## The change lens moves under Value (2026-08-01)

Peter: *"move the current/change over time buttons to just be under Value. But I
want them popped out in the same way the total/residential/non-residential
buttons options are for revenue."*

`#moneymode` (Current | Change over time) had lived in the Options panel since
2026-07-30 as a section headed **Lens**. It is now `#toggle`'s second row under
**Value**, exclusive with `#revcut`.

### The old placement was the defect, not just the location

In `#layers` the toggle showed whenever the view was Money — under **Revenue**
as much as Value. But the change lens measures movement in each hood's share of
Edmonton's **assessment base**: the value side. Offering it under Revenue was
offering a lens that reads a column Revenue does not own. Moving it under Value
is not decoration; it stops the pod claiming something untrue.

### Two rows, two different kinds of nesting

The 2026-07-26 regroup nested `#revcut` under Revenue because the cuts are
genuine **subsets** — `levy == res + nonres + farmland`. `#moneymode` is *not* a
decomposition: it is two **lenses** on one quantity. Both are subordinate to the
row above them and both are styled that way (hairline separator, 11px, dimmer),
but the relationship differs, and `#toggle`'s comment now says so rather than
letting a future reader infer that everything in row 2 sums to its parent.

`syncMetricButtons` owns both rows and shows exactly one. `#moneymode` defaults
**hidden** in CSS where `#revcut` defaults visible — it is gated on
`temporal.json`, which lands after first paint, so a `display: flex` default
would flash a lens that may not exist.

### The consequence that had to be handled

⚠️ **`#toggle` had been hidden in the change view since the 2026-07-23
Money-scoping pass** — correct when the pod was only a metric picker, wrong the
moment it hosts the only way back to `Current`. Hiding it would have stranded the
user in the lens. It now survives into `change`, where **Value reads lit**, which
is honest: the metric on screen *is* movement in the assessment base.

⚠️ **And picking Revenue while the lens is up has to leave it.** Revenue owns no
change lens, so without that the pod would show Revenue lit over a map still
drawing share-of-base movement — the same class of mismatch the move was made to
fix. `applyMetric` only marks state outside money/glass, so the handler calls
`applyView("money")` after it, in that order, and the title follows the metric
out.

### What stayed put

`#chgwindow` (Since 2012 | Since 2019) **remains in the Options panel** (Peter's
call). `#toggle` stays strictly two-level; a third row would have broken the rule
the 2026-07-26 regroup rests on, for a control that only ever shows in one state.
The "Window" header now stands alone in that section.

**Mobile gained a tap and lost a hunt.** Reaching the lens on a phone was: unfold
Options → find "Lens" → tap. It is now Value → Change over time, both on the map
surface, and the pod still fits one row at 390px (measured 180,97 202x55).

---

## The revenue panel: where a hood's levy comes from (2026-08-01)

Peter, on the lens regroup shipped hours earlier: *"under revenue, the panel
still pops up with the assessment over time graph. For revenue I want the panel
to just be the top contributing zones by percent of hood revenue."*

Phase 2 of the revenue-lens readout. Phase 1 shipped the columns that morning
(`total_revenue`, `revenue_share_city`, ten `rev_frac_*`).

### One element, two modes — not a second panel

`#temporal` already owns the three dismissals (×, Escape, re-click), the
`CHROME_IDS` label-sweep exemption, the phone bottom-sheet form, `#hoodmode` and
the peek card's commit path. A sibling panel would have had to duplicate all of
it and then stay in step. So `openTemporal` branches to `renderHistory` or
`renderRevenueMix`, and everything around the content is shared.

The split follows the `#toggle` regroup made the same day: **the panel follows
the quantity, exactly as row 2 does.** Revenue gets the breakdown; Value keeps
the history, which is what it actually describes.

### Three rulings, all of which revised the brief

The recorded brief said "top 3". Building it changed all three answers:

- **All non-zero categories, ranked — not top 3.** The panel has room a tooltip
  does not, so the rows sum to 100% with no unstated remainder. Downtown's top 3
  is 90%; the missing 10% would have been invisible.
- **Shown on the Residential and Non-residential cuts too, with the denominator
  NAMED.** ⚠️ `rev_frac_*` are shares of the hood's **total** levy, while those
  cuts colour one class of it — panel and map divide by different things. The
  house rule from `SPEC_temporal.md` §6 applies: an unnamed denominator is how a
  correct number reads as wrong.
- **The header keeps the levy and the city share.** They give the percentages
  something to be a share *of*.

### The categories are the Uses lens's own

`revenue_by_zone.py`'s `OUTPUT_NAMES` mirror `USE_CATEGORIES`' keys deliberately,
so the column is **derived** as `"rev_" + u.frac` rather than listed again. That
is what stops the Uses lens's *area* shares and this panel's *revenue* shares
drifting onto two category sets — and it means a category added to one lens
cannot go missing from the other. The swatches are the same identity colours the
Uses lens paints, so the two lenses read as one map.

`unzoned` is the exception, with no area counterpart: area always lands in some
polygon, but a property's point can miss every one. It stays visible when
non-zero rather than folding into "other", so a growing gap can't quietly inflate
every real category.

### Three surfaces were advertising the wrong panel

`#peek-go` ("See assessment history ›"), `#temporal-hint`, and the tooltip's
`click to pin` all promise history. On revenue they'd be teasers for a panel that
shows something else, so all three follow the lens now. The tooltip's sparkline
**stays** — a hood's assessment history is still a true fact about it — but its
invite reads *click for the revenue mix*.

⚠️ **And a pinned panel has to re-render when the lens changes.**
`syncPinnedPanel` runs from `applyMetric`, `applyView`, `applyHoodMode` and once
at init. Leaving a revenue breakdown sitting under a value map is a
silent-correctness failure, not a cosmetic one, so the branch that cannot render
**closes** the panel rather than leaving it.

### `fmtBig` was the wrong formatter, and only the rendered output showed it

The history panel's `fmtBig` is calibrated for assessment totals ($10M–$10B) and
rounds the mega band to whole numbers. Reused for a levy it printed
**$1,876,137 as "$2M"** — a 7% error on the headline number of a fiscal tool.
`fmtLevy` keeps two decimals. The same pass caught `revenue_share_city` rendering
0.069% as "0.1%": the city share spans 0.0007%–5.2%, so it takes `fmtPct`'s two
decimals while the category shares take one. **Two different ranges, two
precisions** — neither was visible in a passing test, only in the output.

### Verification

`verify-revenue-panel.js`, 37 checks. Every share is recomputed from the **served
geojson**, so nothing can be satisfied by the app agreeing with itself. The two
checks worth keeping honest were **falsified** before being trusted: removing the
`#temporal-chart .mixbar` selector turns the bar `block` and fails, and removing
`syncPinnedPanel` from `applyMetric` fails the lens swap.

⚠️ The borrowed `.mixbar` needed its borrowed CSS — the S83 lesson, second
occurrence. Scoped `.tip .mixbar, #peek-read .mixbar`, it would have lost
`display:flex` and collapsed the bar to nothing visible, which no id-based
assertion would have seen.

---

## The Display menu clears the Data & Methods pod (2026-08-02)

Carried from 2026-07-28. Small fix; the value is in what reproduction overturned.

### The report's direction was backwards

The item read *"opening Display covers the Data & Methods button"*. Measured, it
is the reverse: both pods sit at `z-index: 1`, so paint order falls back to DOM
order, `#about` is later, and the **button paints over the menu** — truncating
*"Landmarks & nearby pla⌷es"*. Found by looking at a screenshot;
`elementFromPoint` at the button's centre confirmed it returned `about-btn`.

### The recorded cause was wrong too

The item had flagged a z-index asymmetry (`#about.open` lifts to 5, `#a11y` has
no equivalent) for six sessions. That is real, and irrelevant. The actual cause:
`#a11y` and `#about` are a **stack** in one column — `bottom: 40px` and `68px`,
both buttons 26px tall — while `#a11y-menu` was anchored to its **own** button's
top (`calc(100% + 6px)`), which ignores the sibling above it. Both offsets are
fixed, so the ~23px collision was identical at 1440×900, 390×844 and 360×780.

`bottom: calc(200% + 8px)` clears the stack: the pod's own height counted twice
(itself plus `#about`'s button, which shares its font and padding), plus the 2px
inter-pod gap and the 6px the menu already wanted. That tracks the shared button
styling instead of hardcoding 60px.

### ⚠️ The suspected fix would have been worse than the bug

Applying `#a11y.open { z-index: 5 }` is how that was established, rather than
argued. It paints the menu over the button, and `verify-about.js` then **times
out**: the *"Landmarks & nearby places"* label **intercepts pointer events**, so
the Data & Methods button becomes **unclickable**. A visual defect would have
been traded for a dead control.

It surfaced only because `verify-about.js` drives a real `page.click()`. **A JS
`.click()` bypasses `pointer-events` and would have passed** — the standing
warning about this repo's other verify scripts, paid out.

**So the new checks assert GEOMETRY, not paint order.** "The menu is on top"
passes for the z-index version, which is exactly the outcome to reject; only
*they do not overlap at all* rejects both failures. `verify-about.js`, 44 → 50
checks across three viewports, falsified in both directions.

### The generalisable part

Fifth time a carried item's stated cause did not survive reproduction — and the
first where **the recorded fix would have caused a worse bug than the one it
described**. The rule has been "reproduce the symptom before fixing"; this
extends it: **the hypothesis in the ticket is not evidence either, and applying
it is a cheap way to find out.**

## Transportation cost: three rows, not one number (2026-08-03)

Stage 2 of the transportation lens put dollars on the map. The panel gained a
third caption — **Transportation cost — operating** — holding Roads cost,
Transit cost and Bike cost, so `#services` is now **10 rows in 3 groups**.

**Why a separate caption rather than folding into Transportation.** The group
above is *supply* (metres, stop-events); these are *dollars*. And Roads cost is
the same road metres as Other services' Service cost on a different basis —
**$4.635/m/yr operating vs $50/m/yr lifecycle, ~10.8× apart, both in the same
served file**. The caption is the one place in the panel where that shows.
Every column carries an `_ops` suffix for the same reason.

**Why there is no "Transportation" row.** The composite exists as a column and
was built as one, then measured: it is **90.8% transit at the median** (transit
$2,808/acre/yr, roads $151, bike $109). ETS's budget pays to *run a service* —
drivers, fuel, vehicles — while the roads and bike figures only *maintain an
asset*; the City never pays for the cars. A row labelled "Transportation" would
therefore be 91% one term, mislabeled in exactly the way the all-or-nothing rule
already guards against, and it would bury the finding that makes the lens worth
having: **a bikeway metre costs 4.4× a road metre to operate**, cheap to keep up
and expensive to clear, so bike lands at a cost per acre comparable to roads on
about a sixth of the length. Peter's call: three rows, no composite row.

**Colour transforms inherit rather than being re-derived.** Each cost column is
a positive scalar multiple of its supply column, so skew is unchanged (measured
identical to 3 dp): roads linear, transit and bike sqrt.

⚠️ **The legend `else` still prints the ROAD legend**, and the tooltip's missing
key still prints "no X data" over a hood that has data. Both were re-paid here —
three legend branches, three `primaryRow` entries — and `verify-transport-cost.js`
(41 checks) asserts each row's legend is its own *and* is specifically not the
roads fallback. It earned its keep immediately: the transit blurb had never said
*operating only*, though ETS capital is excluded.

**Mobile:** measured at 390/360/320 px with all 10 rows visible and the Options
pod unfolded — no clip, no overflow, 178–235px clearance to `#botleft`. The
earlier "all zeros" probe result was the probe's own fault: `#optpanel` carries
`.folded` by default at ≤640px, so its rows have no layout box until you remove
the class.

## The budget pod: how big is this, really (2026-08-03)

The Data & Methods popover gained a fourth section, **In the city budget** —
four rows putting transit, roads, bike lanes and sidewalks against the City's
$3.8B 2025 operating budget (12.18% / 1.33% / 0.79% / 0.15%).

> ⚠️ **Historical — the roads share is now 2.67%, not 1.33%.** Corrected
> 2026-08-04 when the roads-maintenance component was replaced with a published
> program line (the derived one measured ~5× low). The build-log entry below is
> left as written; `data/DATA.md` §16 carries the current figures.

**Why here and not a new pod.** It is context for reading the map, not a finding
of its own; `#about` already carries vintages, licence and caveats, is collapsed
by default so it costs no screen space, and adding a third pod to the
bottom-right stack means re-opening a collision that took two sessions to
diagnose. It also answers the standing *"where does a non-map panel live?"*
question with an existing surface.

**No bar.** The first version drew one by reusing `.revrow`'s 9px swatch as a
proportional fill. That squeezed the label column, wrapped every row, and took
the section to **348px** — which pushed the whole pod off the **top** of the
screen at every height from 900 down to 720. In a compact text popover four
percentages carry the comparison on their own.

⚠️ **The pod is anchored bottom and grows upward, so it overflows upward with no
scrollbar to notice** — and it was already within **~112px** of doing so at
720px tall *before* any of this. Now capped with `max-height: calc(100vh -
110px)` + `overflow-y: auto`, with `box-sizing: border-box` because `max-height`
is content-box by default and the padding would otherwise sit outside the cap
(the `#temporal` lesson, 2026-08-02). That latent overflow is the more useful of
the two finds.

⚠️ **The shares are derived in the page, never published.** The manifest carries
dollars and a total; `renderBudgetContext` divides. The research this table came
from shipped ratios that had slid one row — *"transit is roughly 15× the road
ops budget"* when it was then **9.2×** — and deriving makes that class of error
unrepresentable. `verify-about.js` recomputes all four independently.
⚠️ **That 9.2× is now 4.6×** (roads corrected 2026-08-04), which is the rule
paying for itself: the fix was one dollar value, with nothing downstream to
re-pin.

## The Lab: a sixth button that is not a lens (2026-08-11)

Asked for as an experimental family with more to come — *"a whole separate
button outside of revenue or money… I may add other experiments to that lens."*
It shipped **twice in one day**, and the difference between the two versions is
the part worth keeping.

**Version 1 was a third `#moneymode` button** under Revenue, beside Current and
Change over time. It worked, it verified, and it was wrong on the thing that
matters: **a mode reads as a variant of the lens hosting it.** An experiment
parked under Money inherits Money's credibility, and the entire reason this work
is separate is that it has not earned it. `#moneymode` also had to grow a
per-quantity gate (Change under Value, deviation under Revenue) — chrome
complexity bought purely to host something that did not belong there.

**Version 2 is its own `#views` button with a `beta` tag**, hidden outright in
the public build, and `#moneymode` went back to exactly what it was.

⚠️ **Moving it exposed a real defect, which is the argument for the separation
rather than a bonus.** As a `#moneymode` button the lens read `state.metric` —
the same variable Money uses. `#moneymode` shows under **Value**. So entering
the lens from the Value map would have computed a "citywide average" over
**assessed value** (~$1.8M/acre) and printed it under a title reading
*Revenue*: internally consistent arithmetic, labelled wrong, with nothing on
screen to give it away. The container fixed it structurally — an experiment
keeps its own state (`state.labCut`) — rather than by adding a guard.
`verify-deviation.js` now drives that exact path and asserts the average does
not move.

**Built as a container from the first commit, not retrofitted later.**
`LAB_EXPERIMENTS` is a registry; `#labpick` renders from it and **stays hidden
while there is only one entry** — a chooser with one option is not a choice,
the same rule `syncServiceControls` applies to the service radios. So the
container costs no dead chrome today, and the second experiment costs no chrome
work.

**Three smaller calls:**
- **`.beta` is a generic class, not `#moneymode .beta`.** It inherits
  `currentColor` so it stays legible on the amber active state.
- **The Lab gates at the `#views` button in the one-time `if (!FULL_BUILD)`
  block**, not beside a data guard like Infill and Industrial — it has no data
  dependency, so nothing else would keep it off the published page.
- **`#labcut` is the Lab's OWN copy of Money's three revenue cuts.** Duplicating
  three buttons was preferred over either reaching into `#toggle` for state or
  pinning the lens to Total and losing the cuts.

**Naming:** "Lab" over "Experiments" because `#views` is now six buttons and
that row wraps at ≤640px — the shortest label that still reads as unfinished.
⚠️ **That row is the one piece of chrome every view shares, and it has not been
checked on a phone** (`TODO.md`).

## The city budget panel: a readout that is not a lens, in two forms (2026-08-16)

*"could we do a test lens in full, listing off the highest cost budget items in
a simple way"* — followed, once it shipped, by *"can we try a phone form?"*

**It is not a lens, and that was the first decision.** The Lab exists for
experiments, and the obvious move was to add a seventh `#views` button. But a
view has to fill `buildViewLayers`, `viewTooltip` and `refreshLegend`, and
**branch budgets are citywide totals with no neighbourhood dimension** — there
is nothing to draw and nothing to hover. It would have been a view with no
prisms and an empty legend. So it is a pod that opens a readout, and
`CONTROLS_MATRIX.md` records it as the first control there that never "bites in"
on any view.

**The split at the top of the list is the content decision.** Ranked naively,
the City's largest operating line is `Capital Project Financing` at **$687.6M** —
ahead of Police. That is true of the ledger and misleading about the City, so
the list separates branches that deliver a service from branches that only move
money. ⚠️ **The rule is derived from each branch's category mix, never a
branch-name list**: measured, `Transfer to Reserves` spans 11 branches
*including Police*, so a category filter would strip service branches of their
own budget, and a name list would misclassify the first time the budget tree is
re-cut — which it has been, twice, inside Parks and Roads alone.

**Two forms, and the phone one is a bottom sheet.** Desktop is a left-column pod
in `#millrates`' slot. On a phone that slot is where `#controls` lives
(`#title` collapsed is 20–43, `#controls` owns **58–197**), so it becomes a
sheet — the same answer `#temporal` reached at the same seam.

⚠️ **The mill-rates test was applied and came out the other way.** The locked
rule is *"on a phone, ask whether a thing needs to be its own surface before
asking where to put it"*, and the mill rates famously did not — they fold into
the blurb card. **43 ranked branches plus a note cannot**, and folding them
would bury the blurb they were folded into. The 2026-08-04 bottom-sheet refusal
does not reach this either: that refused moving the **controls** into a sheet.

**Three details that are not cosmetic:**
- **`0.985` opaque on the sheet, not the desktop `0.92`.** A sheet sits over the
  legend and both bottom-right pods, and at 0.92 their labels read through its
  rows. The `#about-menu` lesson one step further: 0.92 is enough over the map,
  not over other chrome.
- **The body scrolls, not the panel.** With the panel as the scroller, the
  `$4.04B` that every percentage is a share *of* is the first thing lost. Same
  `#temporal-body` split — and it was wrong on **desktop** too until the phone
  form forced the question.
- **A phone-only `×`.** A sheet is at the opposite end of the screen from the
  button that opened it, so the toggle stops being a usable dismissal. On
  desktop the opener sits beside the panel and lights up, so a `×` there would
  be chrome with no job.

⚠️ **The layout bug that assertions missed.** The desktop panel's first height
cap fitted the viewport — and ran **117px straight through the compass, legend
and set-aside swatch**, identically at 900/800/720 because both boxes are
anchored to the viewport bottom. `panel fits inside the viewport` passed the
whole time; a **screenshot** caught it. Fixed by capping to clear `#botleft`,
**not** by a z-index bump, which would have buried the legend rather than
cleared it. The clearance is now asserted at all three heights.

## What the hover promises, and what it confirms (2026-08-16 → 18)

Three changes in two days, all one question: when the pointer is over something,
does the readout tell the truth about *what you are on* and *what clicking will
give you*.

### The teaser was promising a chart the click no longer opened

*"the money revenue lense has the assessment plot coming up when you mouse over…
maybe find out why that popped up again without permission"*

**It never popped back — it never left.** `git log -S "sparklineSvg(t)"` returns
one commit, the temporal lens's phase 3. The sparkline had ridden the revenue
cuts continuously since 2026-07-29 under *"the sparkline rides every view's
tooltip."* What moved was underneath it: on **2026-08-01** the revenue cuts got
their own panel — the zone mix, not the history. That change spotted the
mismatch and fixed **half** of it, rewriting the invite's wording
(`click to pin` → `click for the revenue mix`) and leaving the chart.

⚠️ **The chart is the louder half.** A reader sees a line move and expects the
click to enlarge *that*. The teaser is a promise about the click, so it now
rides only where the click delivers history — Value keeps it, the three revenue
cuts get the invite alone. The invite stays either way: click-to-open is
undiscoverable without it, and it is the only route to the revenue mix.

### The band prism was answering with the wrong hood's numbers

*"i want people to be able to just mouse over prisms (or tap on mobile) cuz
they're gonna wanna see why they're special color"*

⚠️ **Not a missing tooltip — the WRONG hood's.** A banded hood's own geometry is
flattened to 0 and painted transparent, so the azure prism is the only thing
over that footprint; unpickable, it fell through to whoever stood **behind** it.
At pitch 60 over the U of A: `MCKERNAN`, `RIVER VALLEY VICTORIA`,
`WÎHKWÊNTÔWIN`, pointer on U of A geometry throughout.

⚠️ **A flat overhead check cannot see it** — at pitch 0 the transparent footprint
picks correctly, which is exactly why "you had to mouse over the neighbourhood
flat below it" described the *good* case. The full reasoning, including why the
Lab needed separate invisible pick targets rather than a fill, is in
`SPEC_revenue.md`.

### Answering is not confirming

*"the banded prisms now don't glow the same as the regular prisms when you mouse
over, so lacking proper confirmation you hovered … on the intended hood"*

The same-day cost of making the prism pickable but refusing `autoHighlight`
(which lights only one of the band's two shells, and so grants one unknowable
world primacy over the other). **Measured: hovering a banded prism moved 0
pixels.** The answer was not to accept the primacy but to light **both** shells
by index — mean Δ73 (Money) and Δ98 (Lab) against an ordinary prism's Δ34.

**The generalisable part:** a *principled* refusal to draw something still has to
be checked against the affordance it removes. Both halves here — the teaser that
kept promising, and the glow that stopped confirming — were caught by Peter
using the map, not by a suite that covers both surfaces in detail.

## The change lens gets signed prisms (2026-08-26)

Peter, looking at the flat change choropleth beside the Lab's deviation lens:
*"i want the value → change over time lens to use the same prism system as
'lab revenue per developed acre vs the city average'. like how positives go up,
but negatives actually go down before the floor. the lens is organized by
'since 2012/2019'. so that should already provide a natural 0 to go up or down
from."*

He was right about the zero, and right that nothing was stopping it.

**The decision that was in the way had already half-collapsed.** `DECISIONS.md`
2026-07-30 locked the lens flat for two reasons:

1. *"A prism cannot have negative height."* **False**, and known to be false
   since 2026-08-11 — the deviation lens measured deck.gl 9.0.38 rendering a
   negative `getElevation` below the ground plane
   (`tools/profiling/probe-negative-elevation.html`) and shipped on it. The
   `changePlaneLayer` comment had *recorded the retraction* while the render
   kept the conclusion.
2. *"Extruding a percentage reads as magnitude when the metric is deliberately
   size-independent."* Still true. Now deliberately accepted, and paid for in
   the blurb rather than by staying flat.

⚠️ **A retracted premise does not retract the conclusion by itself** — but it
does mean the conclusion is standing on one leg, and nothing was tracking that.
Six days of "do not re-open this" guarded a decision that had already lost half
its support.

**What shipped.** `changePlaneLayer` → `changePrismLayer`, `change-plane` →
`change-prisms` (a layer named *plane* that extrudes is the kind of lie this
project's docs exist to prevent).
- **ONE shared elevation scale**, `CHG_ELEV_SCALE = 9000` — fixed, not
  per-window, not per-arm. Per-arm scales are the trap: the p95 arms are ~6×
  apart, so scaling each to its own would draw a −5%/yr loss and a +34%/yr gain
  as equal bars. Colour keeps its per-arm clamps, which is a *different*
  question — a ramp has two ends to spend, a height has one origin.
- **Measured before picking the constant**, not after: fastest hood in either
  window +51.6%/yr, deepest −22.3%/yr, so the down arm renders at **35–43%** of
  the tallest — legible on a shared scale without any help. The tallest prism
  lands ~4,600 m, the same order as Money's tallest (~4,900 m).
- **The 46 degenerate hoods stay flat at 0**, not absent. A hole in the height
  reads as "did not move" — the exact reading the colour scale already refuses
  for them.
- **`hood-hover` is gone from this view.** The prisms are pickable themselves
  (deviation's pattern); a flat `depthTest:false` pick target sitting under
  extruded geometry steals every pick.
- The blurb now leads with *"Height and colour"* and carries the cost of the
  accepted objection: ⚠️ height is a **RATE**, so the tallest prisms are small
  new subdivisions growing off a near-empty baseline, not the biggest tax bases.

**`verify-change.js`** asserts the two things that would fail silently: that
metres-per-point are **equal on both arms**, and that the rendered
deepest/tallest ratio matches the **raw file's** — because the way this
regresses is someone "fixing" the visual asymmetry.

---

## Glass cell size as a third Detail button (2026-09-01)

Peter: *"let's do the 50m option, keep 100m as default. Can 50m not just be a
third option"*. `#moneydetail` goes from two buttons to three — **Neighbourhood
/ 100 m grid / 50 m grid** — rather than gaining a separate cell-size row.

Why the third button beat the separate row, which was the alternative on the
table:
- **No new control row**, so no `CONTROLS_MATRIX` regrouping and no mobile
  chrome risk. Grouping is shared DOM: it drives desktop and phone together.
- `#moneydetail` is **already Money-only and already hidden in Change**, so the
  resolution choice inherits exactly the right gating without new conditions.
- It **dissolves the "does Infill follow the switch?" question by
  construction** — Infill is not in that row, so it pins the default. That was
  a genuinely open design question under the separate-row shape.

⚠️ **Three buttons over two views**, so the active button cannot be derived from
the view alone — `syncMoneyDetail` disambiguates the grid pair on
`state.glassCell`. And switching *between* the two grid buttons changes no view,
so `applyView` early-returns; `applyMoneyDetail` owns that path's fetch and
repaint (blurb, legend, layers — **legend before layers**, per the label-sweep
ordering rule that already governs `applyView`).

⚠️ **The button labels stay `CELLS` pins; the prose does not.** Each button names
a fixed shipped resolution, so both are correct at parse time — this is the F4
machinery unchanged. Prose that describes the grid *on screen* reads
`glassCellLabel()` off the loaded file instead, which is the "pin the default,
read the switch" resolution of F4's async constraint.

**`verify-glass-cell.js`** covers the switch. ⚠️ **Its first version could not
catch either default bug**: it asserted the default only after clicking the
100 m button, which SETS the value it was about to read, so it passed with the
default pinned to 50. That was found by running the falsification, not by
reading the test — the landing check now runs before any Detail click, which is
the only moment the default is observable. All four target defects were
reintroduced and confirmed to go red.

#### The grid buttons' busy state (2026-09-01)

Peter, on the live site: *"50 m grid, and to some degree 100 m grid take visible
time to load."* Both files are lazy, and `syncMoneyDetail` lights the clicked
button **active before the fetch starts** — so the control reported "done" while
the map sat unchanged. The affordance that was missing is feedback, not speed.

An **indeterminate sweep across the pending button** (`.is-loading`, a `::after`
gradient), set and cleared inside `ensureGridData` — the single choke point both
call paths go through, so the clear cannot leak down one of them. Indeterminate
because a `fetch`+`json()` reports no progress fraction to draw a real bar from.
Dark ink, since the sweep only ever runs over the yellow `.active` background.
`aria-busy` rides along on the same two writes. `prefers-reduced-motion` drops to
a static tint, the same trade `#loading-spinner` already makes one screen up.

⚠️ **Gated on the grid not being parsed yet**, so switching back to a resolution
already in `gridStore` does not flash a stripe for one frame — feedback for a
wait that isn't reads as a stutter. ⚠️ **Cleared on the fetch's own settle, not
after the caller's re-render**: a failed fetch resolves (see the `.catch`), so
this is also what stops a dead request stranding the stripe on forever.

**`verify-grid-loading.js`** covers it, and the instrument is the point: over
localhost the fetch settles in tens of milliseconds, so **sampling the class
between clicks reads "not busy" whether the stripe worked perfectly or was never
written at all**. It records class *transitions* with a `MutationObserver`
installed before the first click, and samples the `::after` pseudo at the moment
the class lands — a right class behind a wrong selector is an invisible control
with green assertions. ⚠️ **Two findings came out of falsifying it**, both
written into the file: `stripe cleared` was **vacuous** in the first version
(`classList.remove()` writes the class attribute even when the class was never
there, so it read true under a build that never added one), and the
`gridStore`-vs-`gridFetches` gate **could not be falsified at all** — the two are
equivalent on the success path, so no check here justifies that choice.

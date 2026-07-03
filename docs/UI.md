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

### Services views: Money | Roads | Ratio (built 2026-07-02, display pivot complete)
The road-prism metric view built earlier on 2026-07-01 was **retired the same day**
(`SPEC_services.md` "Display architecture — REVISED"). After two intermediate
iterations (a Roads checkbox + free opacity slider; then a slider-at-0% roads-only
mode), Peter settled the control model as **three discrete views** (`#views`
buttons, below the lens button; `state.view`):

- **Money** (default): the classic revenue/value prisms, always opaque. Metric
  toggle, palette, residential lens all behave as before. Hood tooltip: active
  metric + `19.2 road m / acre` + `$967 revenue / road metre` (ratio omitted when
  road base is 0 / columns absent; set-aside tooltip unchanged).
- **Roads**: the network alone on the ground — **no prism layers at all** (an
  opacity-0 layer still tessellates, draws, picks, and auto-highlights; dropping
  them is the honest render and the perf win). Arterials neutral grey
  (`ARTERIAL_COLOR`, 2 px, no metric); collector + local coloured by their hood's
  `road_m_per_acre` on the active ramp — **LINEAR, clamp 53** (FINDINGS §6.3),
  1.2 px. Legend: road scale. Tooltip: road amount only. Title/blurb swap with the
  view (`VIEWS` object).
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
  residential lens applies in Money AND Ratio (2026-07-03), disabled in Roads.
  Roads/Ratio buttons hide when the served GeoJSON predates the services
  columns.
- Headless-verified via Playwright (all three views: layer stacks, legend swaps,
  tooltips incl. floored/set-aside cases, slider visibility) 2026-07-02; lens ×
  view matrix (anchors, fills, button disable) 2026-07-03
  (`tools/profiling/verify-lens.js`). Translucent-prism depth-ordering quirks:
  same acceptance as the residential lens fade.

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

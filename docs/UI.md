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

### Residential-only lens (built 2026-07-01)
A **"Residential only" toggle** (`#lens` panel, below the palette switcher) isolates
residential land so it compares like-to-like without the Downtown / class-rate-
differential confound (the motivating problem in `SPEC_revenue.md`). Off by default
(default view unchanged); preserves the metric + palette state. Two effects when on:
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
- Drives off `is_residential` (≥0.50 residential zoned area; see `DATA.md` §5);
  orthogonal to the set-aside flag by construction.
- **Still open** (`TODO.md`): the fuller "Color Adjustment vs lens controls" hierarchy +
  self-describing state labels; the toggle is currently a plain button. Alpha / grey /
  clamp-percentile are easy tunables. Not yet visually verified in a browser.

### Roads ground layer + service layers panel (built 2026-07-02, display pivot stages 1–2)
The road-prism metric view built earlier on 2026-07-01 was **retired the same day**
(`SPEC_services.md` "Display architecture — REVISED"): road supply renders as the
**actual network on the ground plane**, not as extrusions. As built:
- **`#layers` panel** ("Service layers", below the lens button): stackable checkboxes,
  Roads first — later services add a checkbox + a `state.layers` key, not a rework.
  Default OFF; the initial view is unchanged.
- **Lazy load:** `web/data/roads.geojson` (2.0 MB; 791 dissolved features, slim
  `n`/`t`/`v` props — ARCHITECTURE `export_roads_web`) is fetched once, on first
  enable. Initial page payload unchanged.
- **Ground `GeoJsonLayer`** (first in the layer stack, z=0 under the prisms):
  **arterials neutral grey** (`ARTERIAL_COLOR`, 2 px — context skeleton, no metric);
  **collector + local coloured by their hood's `road_m_per_acre`** on the active
  ramp — **LINEAR, clamp 53 m/acre** (≈ p97.5; FINDINGS §6.3 — sqrt/log over-correct
  a bounded, near-symmetric quantity), 1.2 px. The palette switcher applies to the
  network too. Tooltips: hood + `38.2 road m / acre (collector + local)`, or
  "Arterial — shared infrastructure, no metric".
- **Money-plane opacity slider** (same panel, "Prisms", 0–100%): layer-level
  `opacity` on the prism fill AND the roof-edge rings (outlines floating over a
  ghosted plane read as clutter). This is what makes the ground plane *visible* —
  verified headless: at 100% prism opacity the network only peeks through the 45 m
  setback gaps (~0.5% of pixels).
- **Auto-nudge:** enabling Roads with the slider untouched at 100% drops it to
  **45%** (visibly — the slider moves); disabling the last ground layer restores
  100% if the nudge is still what set it; any manual slider move cancels the
  auto behaviour (`opacityAutoSet`). Prevents the "toggle appears to do nothing"
  trap without taking the control away from the user.
- Set-aside hoods keep their grey prisms; the network renders underneath like
  everywhere else (a set-aside hood's sparse roads are themselves informative).
- The old Roads metric-toggle button, its `METRICS` entry (`elevationScale: 137`),
  and the hide-if-absent fallback are **removed**.
- Headless-verified via Playwright (layer on/off, ramp switch with layer on,
  auto-nudge + restore) 2026-07-02. Known composition quirk: translucent extruded
  prisms have the same deck.gl depth-ordering quirks as the residential-lens fade —
  accepted there, same acceptance here.

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

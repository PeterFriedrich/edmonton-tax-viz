# UI & Accessibility (Phase 2 web map)

Visual theming and accessibility decisions for the interactive map. Phase 1
(static PNG) is out of scope. Render/performance tradeoffs live in
`PERFORMANCE.md`; data-shape decisions in `ARCHITECTURE.md`.

---

## Current state

- **Dark theme only.** Background `#0a0a0f`, no basemap (polygons on dark are
  self-describing — see ARCHITECTURE.md Phase 2 notes).
- **Fill ramp:** sequential dark→bright inferno-ish (`RAMP` in `index.html`),
  clamped at `$4M`/acre (`COLOR_CLAMP`) for mid-band contrast.
- **Top-cap edge:** deep muted teal, cool against the warm fills.
- **Tunables** live at the top of `web/index.html`'s `<script>`: `RAMP`,
  `COLOR_CLAMP`, `TOP_EDGE_COLOR`, and the MapLibre `background-color`.

---

## Open / unresolved

- **Top-cap edge colour — NOT finalized (as of 2026-06-26).** The developer is
  not happy with it yet. Tried so far: `[120,215,255]` bright cyan (too hot) →
  `[55,130,160]` dark teal (still a touch bright) → `[40,95,120]` deep muted teal
  (current, still not right). Still iterating — don't treat the current value as
  settled. Worth considering alongside the light-mode work below, since the right
  edge colour depends on the background.

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

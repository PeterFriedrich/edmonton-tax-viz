# Performance & Profiling (Phase 2 web map)

How the interactive 3D map performs, how to measure it, and the findings that
shape the current `web/index.html` config. Phase 1 (static PNG) has no runtime
performance concerns — this doc is Phase 2 only.

---

## Audience baseline: assume no discrete GPU

The map must stay usable on **integrated graphics and software-rendered WebGL**,
not just gaming GPUs. The developer's own Linux laptop has no discrete GPU (iGPU
only) and is treated as a representative low end, not an edge case. A civic data
viz gets opened on municipal desktops, old laptops, and locked-down work
machines — if it only feels smooth on a dedicated GPU, it's too heavy.

**Implication:** every rendering choice is judged against the weak-GPU baseline.
Effects that "only cost a bit" on a strong GPU (rounded line joints, wireframe,
high vertex counts) can be the difference between 60fps and a stutter on an iGPU.

---

## How to profile

### 1. Headless harness (relative comparison, CI-friendly)

A Playwright + Chromium script drives a rotate-drag and records frame times.
Chromium runs under **software WebGL (`--use-angle=swiftshader`)**.

- **Good for:** A/B comparing two configs (does option X cost more than Y?).
  Software rendering exaggerates CPU-side and fill-rate costs, which actually
  makes it a decent proxy for the iGPU low end.
- **Not good for:** absolute FPS numbers — swiftshader is far slower than any
  real GPU, and a heavy config can stall the harness itself (see findings).

The harness lives in **`tools/profiling/`** (see its `README.md` for setup +
usage): `shot.js` (screenshot + console/WebGL error capture), `shot2.js`
(screenshot an arbitrary URL), and `profile.js` (frame-time stats under a driven
drag). One-time setup is `npm install && npx playwright install chromium`; the
scripts point at a local `python -m http.server 8777` served from `web/`.

### 2. Real GPU (the authoritative measurement)

For numbers that reflect a real user: open the map in Chrome, DevTools →
**Performance** tab, record while rotating/zooming. Look at the FPS meter and
the GPU/raster track. This is the source of truth; the headless harness only
narrows down *which* option to suspect.

### 3. Live FPS overlay (optional, not yet built)

deck.gl exposes a stats widget. A `?stats` URL param could mount a live FPS/
draw-call counter so the developer can watch cost while tuning. Flagged as a
nice-to-have; implement if tuning becomes frequent.

---

## Findings

| Config / option | Verdict | Why |
|-----------------|---------|-----|
| Extruded prisms only (no outline) | **Smooth** (60fps median even headless) | Baseline cost is fine; the prisms are not the problem |
| `wireframe: true` on the GeoJsonLayer | **Laggy — do not use** | Draws *every triangulation edge* of all 405 prisms |
| Top-cap `PathLayer`, `jointRounded`/`capRounded: true` | **Hangs the render** | Rounded joints fan out extra triangles at *every vertex*; with ~89k ring vertices the tessellation explodes (hung even headless) |
| Top-cap `PathLayer`, miter joints (default) | **Smooth, visually identical** at 1.4px | One thin segment per edge; current config |

**The dominant cost lever is vertex count.** Before simplification the served
GeoJSON carried **~89,000 ring vertices** (the 45 m setback buffer inflated the
raw ~66k boundary vertices with rounded corners). That count drives the cost of
the extrusion, the top-cap outline, and anything per-vertex — and the download
size. A display-only Douglas–Peucker simplify (see ARCHITECTURE.md), run *after*
the setback so it also collapses the buffer's added vertices, cuts this to
**~9,200 vertices** and the file from **3.0 MB → 0.49 MB** with no visible change
at city zoom. Reducing vertex count speeds up *everything* at once.

---

## Current config (web/index.html) and the rationale

- **Filled extruded prisms, `stroked: false`.** The 45 m setback gaps already
  give every shape a dark border at ground level, so a footprint stroke is
  redundant (verified by A/B render — stroke on vs off was indistinguishable).
- **Top-cap outline via a separate `PathLayer`** at each prism's roof elevation
  (`z = value × ELEVATION_SCALE`), miter joints, cool-cyan against the warm
  fills. Crisp roof edges at ~one ring per shape — cheap, unlike `wireframe`.
- **`wireframe: false`** — never re-enable casually (see table).

---

## Payload, as distinct from render cost (2026-08-10)

Everything above is about **frames**. This section is about **bytes**, which is a
separate budget with a separate audience: render cost is paid by whoever opens a
heavy lens, payload is paid by everyone who loads the page.

**Adding a lens does NOT slow the site down.** Two mechanisms, both verified:

- **Fetches are lazily memoized per lens** (`??=` guards, `web/index.html`) — an
  unopened lens is never downloaded.
- **`buildViewLayers()` early-returns on `state.view`** — only the active lens
  constructs layers, so inactive lenses cost nothing per frame. The Services
  block comments on why an opacity-0 layer is not acceptable ("would still
  tessellate, draw, pick, and highlight").

Measured over the wire (GitHub Pages gzips everything, `.geojson` included;
`cache-control: max-age=600`, so repeat visitors re-pay the boot set):

| when | payload | gzip |
|---|---|---|
| **boot, always** | deck.gl + maplibre + `index.html` + css | ~680 KB |
| **boot, always** | `neighbourhood_value_per_acre.geojson` (awaited, blocks the data draw) | **~185 KB** |
| **boot, always** | reference + temporal + status | ~69 KB |
| Glass | `value_grid.json` | 930 KB |
| Uses | `zoning.geojson` | ~444 KB |
| Services / Ratio | `roads.geojson` (+ bike 52, lrt 4.5, transit 1.1, fire 0.4) | ~264 KB |
| Development | `dev_grid.json` | **~111 KB** |
| Money / Value / Infill / Change | reads `state.data` | **0** |

⚠️ **THE ONE COST THAT SCALES WITH LENS COUNT is the served hood GeoJSON**, because
each lens adds per-hood columns to it and every visitor fetches it at boot. At 66
columns its attributes (176 KB gzip) had already outgrown its geometry (138 KB).
Precision was the fix — see `DECISIONS.md` 2026-08-09 and `DATA.md` §3: **340 KB
→ 166 KB**, from two kwargs. Before adding a lens's columns there, check what the
boot payload is at.

**`dev_grid.json` grew ~92 → ~111 KB gzip on 2026-08-18** (raw 0.36 → 0.51 MB)
when the industrial detail cells landed: four new columns on every row plus
~835 industrial-only cells. Lazy-loaded on entering Development, so it is not
boot cost. The two industrial columns per window are the price of keeping the
$0-declared permits visible — `ind_n` (count) cannot be derived from `ind_cv`.

⚠️ **`value_grid.json` is measured and deliberately left alone** — only 16%
available, nobody pays it at boot, and `median_year_built` is a column where
scale-invariant rounding is actively wrong. Do not re-open without reading the
2026-08-09 decision.

## Rules of thumb

1. **No `wireframe: true`** on extruded layers at this polygon count.
2. **No rounded line joints/caps** on detailed rings — miter only.
3. **Keep vertex count down** — it's the lever that helps every layer. Prefer a
   display-only simplify over per-layer micro-tuning.
4. **Judge on the iGPU baseline,** not a discrete GPU.
5. **Confirm the *feel* on a real GPU** (DevTools Performance) before declaring a
   perf change done — the headless harness only points at the suspect.

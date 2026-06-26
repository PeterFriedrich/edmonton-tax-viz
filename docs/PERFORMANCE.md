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

Scripts live in the session scratchpad (not committed): `shot.js` (screenshot +
console/WebGL error capture) and `profile.js` (frame-time stats under a driven
drag). Re-create as needed; they point at a local `python -m http.server` in `web/`.

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

## Rules of thumb

1. **No `wireframe: true`** on extruded layers at this polygon count.
2. **No rounded line joints/caps** on detailed rings — miter only.
3. **Keep vertex count down** — it's the lever that helps every layer. Prefer a
   display-only simplify over per-layer micro-tuning.
4. **Judge on the iGPU baseline,** not a discrete GPU.
5. **Confirm the *feel* on a real GPU** (DevTools Performance) before declaring a
   perf change done — the headless harness only points at the suspect.

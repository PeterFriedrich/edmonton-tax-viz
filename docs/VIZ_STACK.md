# Visualization stack — current, compared, and the alternatives

What this project renders with, what a directly comparable Edmonton site renders
with, and what we'd switch to if a constraint changed. Written 2026-08-07 after
measuring both sites.

This is a **reference doc, not a decision doc**. Nothing here is locked; if
something here gets chosen, it goes in `docs/DECISIONS.md` with its own line.

---

## 0. The short version

We run **MapLibre GL as a camera and deck.gl as the renderer**, over raw GeoJSON
files, with hand-rolled SVG for charts, no build step, and every library
vendored. That is an unusual combination and it is the *right* one for what's
built — 3D prisms, per-feature JS at draw time, and a hard offline constraint.

**Cold load is one file.** `web/data/` totals ~8.4 MB on disk, but boot awaits
only `neighbourhood_value_per_acre.geojson` (1.4 MB raw) — every other heavy file
sits behind a memoized `??=` lazy fetch gated on the view that needs it. Don't
read the 8.4 MB as a page weight; it isn't one. See §5.

---

## 1. What we run today (measured)

| Layer | Choice | Notes |
|---|---|---|
| App shell | One static `web/index.html`, 297 KB + `styles.css`, 42 KB | No framework, no bundler, no build step for the site |
| Map engine | **MapLibre GL JS 4.7.1**, vendored (`web/vendor/`, 784 KB) | Camera / projection / interaction **only** |
| Basemap | **None.** Style is `sources: {}` + one background layer `#0a0a0f` | `web/index.html` — "no basemap tiles for v1 — just a dark backdrop" |
| Data rendering | **deck.gl 9.0.38**, vendored (1.19 MB), via `MapboxOverlay` | `GeoJsonLayer` (fills, 3D extrusions, roads, prism roof rings), `ScatterplotLayer` (stations, points) |
| Charts | **Hand-rolled inline SVG** (sparklines, temporal chart) | No chart library at all |
| Geometry transport | Raw `.geojson` / `.json`, committed to the repo | `web/data/`, ~8.4 MB on disk across 12 files |
| Hosting | GitHub Pages via `.github/workflows/deploy.yml` | Data committed by the refresh bot; deploy re-uploads `web/` |
| Pipeline | Python — geopandas, shapely, pyogrio, pyproj, pandas | `src/` modules → `web/data/*` |

**Loading is already lazy, per view.** Boot awaits `DATA_URL`
(`neighbourhood_value_per_acre.geojson`, 1.4 MB) and nothing else. The rest are
memoized single-flight fetches — `gridFetch ??= fetch(GRID_URL)` and siblings —
triggered by the view or toggle that needs them:

| File | On disk | Fetched when |
|---|---|---|
| `neighbourhood_value_per_acre.geojson` | 1.4 MB | **boot** |
| `value_grid.json` | 2.5 MB | Glass / grid detail |
| `zoning.geojson` | 2.2 MB | Uses |
| `roads.geojson` | 1.6 MB | Services |
| `dev_grid.json` | 362 KB | Development |
| `bike_routes.json`, `temporal.json`, `reference.geojson`, LRT/stations | ≤236 KB each | their own toggles |

On-disk sizes. Pages gzips on the wire, so transfer is smaller — **unmeasured**.

**The load-bearing choice:** MapLibre draws *nothing* here. It owns the camera,
the pointer events, and the projection; deck.gl draws every pixel of data. That
means the MapLibre style-spec expression DSL is unused — all per-feature logic is
plain JavaScript accessors.

## 2. What map.kunicki.app/assessment/ runs (measured 2026-08-07)

Same city, same open data, independently built — a useful contrast.

| Layer | Choice |
|---|---|
| App shell | One static HTML file, 129,653 B / 3,451 lines, 1 inline `<style>`, 3 `<script>` tags |
| Map engine | MapLibre GL JS, **`maplibre-gl@4` from unpkg** — floating major pin |
| Rendering | **MapLibre native layers** — `fill`, `fill-extrusion`, `symbol`, style expressions, `setData`/`setPaintProperty`. No deck.gl |
| Charts | **Chart.js v4** from jsDelivr (also a floating `@4` pin) |
| Geometry transport | Raw GeoJSON/JSON, 6 files fetched in one `Promise.all` at boot (≈1 MB gzipped / 3.7 MB raw), plus lazy per-neighbourhood `prop_details/<slug>.json` |
| Hosting | Cloudflare in front of an nginx origin (`cf-cache-status: DYNAMIC` — edge not caching) |

Also vanilla JS, no framework, no build step. Converges with us on the shape of
the problem and diverges on the renderer.

⚠️ **Their lazy `prop_details/<slug>.json` pattern is NOT something to import** —
it looked like the one transferable idea here, and it isn't. We already do the
same thing more broadly (§1): they shard a detail sidecar by neighbourhood, we
lazy-load whole per-view datasets behind `??=`, including the four files bigger
than anything they ship. Checked 2026-08-07; don't re-propose it.

## 3. deck.gl vs MapLibre-native — the choice that actually matters

This is the fork in the road for a project like ours, so it's worth stating
plainly.

**MapLibre-native** (kunicki's pick). Data goes in as a GeoJSON source; you style
it with the style-spec expression language (`['interpolate', ['linear'], ['get',
'value'], …]`). Updates are `setData` / `setPaintProperty`.

- Buys: one library (784 KB, not 2 MB). Fewer moving parts. Styling is
  declarative and serializable. `fill-extrusion` gives basic 3D.
- Costs: the expression DSL is a real language you have to think in, and it
  can't call your JavaScript. Anything genuinely per-feature and computed —
  our client-side ratio metrics, live z-scores, per-arm scaling — has to be
  precomputed into feature properties before it reaches the map.

**deck.gl over MapLibre** (our pick). MapLibre is the camera; deck.gl layers draw
on the GPU with plain JS accessors (`getFillColor: f => …`).

- Buys: arbitrary JS at draw time — the accessor *is* the styling logic, so
  derived metrics never need a precompute pass. Real 3D (our prisms + roof
  rings). Composable layers. Uniform handling of polygons, paths, and points.
- Costs: 1.19 MB more JavaScript, a second API surface, and a version-coupling
  between deck.gl and MapLibre that has to be respected on upgrades.

**Verdict for us: keep deck.gl.** The 3D prisms and the client-side-derived
metrics (`docs/DECISIONS.md`, 2026-07-02/03: "ratio metric is derived
client-side") are exactly the two things MapLibre-native is worst at. Dropping
deck.gl would mean pushing derived metrics back into the Python pipeline —
re-coupling the thing we deliberately decoupled.

## 4. Alternative stacks

Each entry: what it is, what it would change here, and when it's worth it.

### A. Status quo — MapLibre (camera) + deck.gl (render) + raw GeoJSON
The baseline. Worth keeping while feature counts stay in the hundreds-to-low-
thousands and 3D stays a headline feature.

### B. MapLibre-only — drop deck.gl
Saves 1.19 MB. Requires precomputing every derived metric into properties and
rewriting all styling into the expression DSL. **Worth it only if** we drop 3D
*and* stop deriving metrics in the browser. Not our direction.

### C. MapLibre/deck.gl + **PMTiles** — the parcel-scale answer
Replace raw GeoJSON with a single `.pmtiles` archive of vector tiles, served over
HTTP range requests off any static host — **GitHub Pages included, verified**
(§7). No tile server. Build with `tippecanoe`; read with `pmtiles` + the MapLibre
protocol handler, or deck.gl's `MVTLayer`.

- Buys: the browser fetches only the tiles for the current viewport and zoom.
  This is what makes ~400k parcels viable at all.
- Costs: a `tippecanoe` step in the pipeline (a non-Python binary — check it
  against the "Python-only, no GIS software" rule in `CLAUDE.md` before
  committing), and feature properties get baked at tile-build time, which cuts
  against client-side derivation.
- **This is the one alternative gated to a real future need** —
  `docs/PARCEL_LEVEL_OPPORTUNITIES.md`. At neighbourhood granularity it's
  premature.

### D. Leaflet + GeoJSON
Smallest and oldest option (~40 KB). 2D raster/SVG only, no GPU, no 3D, degrades
past a few thousand polygons. A downgrade for us; listed because it's the default
answer everywhere else and it's worth knowing why we said no.

### E. OpenLayers
Heavier than Leaflet, far more projection machinery, strong on WMS/WFS and
non-Web-Mercator CRS. Real advantage only if we needed to render in EPSG:3400
directly rather than reprojecting in the pipeline. We don't — we project in
geopandas.

### F. D3 / Observable Plot — no map engine at all
Project the geometry ourselves and draw SVG or canvas. Total control, tiny
dependency, and excellent for a *static* choropleth. Loses pan/zoom/tiles/3D and
all the interaction machinery. Viable for a print-style companion figure or a
verified-notebook output; not for the live map.

### G. Framework shells — React (`react-map-gl`, `@deck.gl/react`), Svelte, Observable Framework
Would give component structure and state management for a 4,250-line file that's
outgrowing plain JS. Costs a build step, a `node_modules`, and the ability to
open `web/index.html` and just read it. Given `docs/CODEMAP.md` exists precisely
to navigate that file, the pressure is real — but a build step also breaks the
"vendored, works offline" property below. Not now.

### H. Python-native rendering
Relevant because our pipeline is already Python.

- **pydeck** — deck.gl bindings; emits HTML. Good for notebook exploration,
  weak for a hand-tuned production UI.
- **Folium** — Leaflet from Python. Same 2D ceiling as D.
- **Lonboard** — deck.gl + GeoArrow, built for large datasets in notebooks.
  Genuinely interesting for the parcel-scale exploration phase.
- **kepler.gl** — configure-not-code; great for exploration, wrong for a
  bespoke published UI.
- **Plotly/Dash, Streamlit** — need a running server. Incompatible with static
  GitHub Pages hosting. Non-starters for the published site.

Use these for *analysis* (`docs/ANALYSIS_BACKLOG.md`), not for the site.

### I. Charts — the one place we're the outlier
We hand-roll SVG; kunicki uses Chart.js. Options if the chart set grows:

| Option | Size | When |
|---|---|---|
| Hand-rolled SVG (current) | 0 | Few chart types, full control, no dep. Correct today |
| **uPlot** | ~45 KB | Many time series, performance-critical |
| **Chart.js** | ~200 KB | Standard bar/line/stacked, want it done fast |
| **Observable Plot** | ~200 KB | Grammar-of-graphics, exploratory variety |
| **Vega-Lite** | ~1 MB+ | Declarative specs as data. Overkill here |

**Recommendation: stay hand-rolled.** The chart inventory is small and the
temporal chart has two rendering invariants that fail silently
(`docs/SPEC_temporal.md` §2) — invariants that are easier to hold in code we own
than in a library's config surface.

## 5. How to actually choose — the axes

1. **Feature count on screen.** Hundreds → anything. Tens of thousands → GPU
   (deck.gl). Hundreds of thousands → tiles (§C), no exceptions.
2. **3D?** deck.gl or MapLibre `fill-extrusion`. Rules out D, E, F.
3. **Per-feature JS at draw time?** deck.gl accessors. Rules out MapLibre-native.
4. **Cold-load budget.** Not 8.4 MB — a cold first visit is **1.99 MB of
   vendored libraries** (deck.gl 1.19 + maplibre 0.78 + CSS 0.06) plus **1.4 MB
   of boot geometry**. Uncompressed; wire figures unmeasured, and JS and GeoJSON
   don't gzip at the same ratio, so measure before ranking them. Note the
   libraries are the *larger* half — which is the one honest argument for §B,
   though not enough of one. The remaining geometry lever is simplification and
   coordinate quantization of that single boot file, since lazy-loading is
   already done.
5. **Offline / air-gapped.** See §6 — this constraint is doing more work than it
   looks like.
6. **Build step?** Every framework option costs one. Currently zero.

## 6. Traps — things not to change casually

- **Keep libraries vendored, not CDN'd.** `web/vendor/` is why the site builds
  and verifies in a Claude Code remote VM, where the network policy blocks
  unpkg (`docs/REMOTE_VM.md`). It also removes a third-party runtime dependency
  from a public-interest site. kunicki's CDN pins are a live dependency on two
  external hosts.
- **Keep exact version pins.** We pin `maplibre-gl-4.7.1.js` / `deck.gl-9.0.38`.
  kunicki pins `maplibre-gl@4` and `chart.js@4` — floating majors, so an
  upstream minor release can change the live site with no commit and no way to
  bisect. Our vintage-digest discipline (`docs/RUNBOOK.md` §0) exists because
  silent upstream drift is this project's characteristic failure.
- **Don't precompute derived metrics just to satisfy a renderer.** Client-side
  derivation is a locked decision (`docs/DECISIONS.md`, 2026-07-02/03).
- **Don't add a basemap without deciding what it costs.** Right now there are no
  tile requests at all — no third-party host sees our users, and there's no
  attribution or rate-limit surface to manage. That's a feature.

## 7. Hosting — does an origin server buy anything here?

Tempting assumption: kunicki's choices are enabled by running a real host
(nginx behind Cloudflare) where we're on static GitHub Pages. **Measured
2026-08-07, that's backwards** — nothing on their site uses the server, and for
this workload Pages is the stronger host.

**Their origin serves static files and nothing else.** Query strings change
nothing (`/assessment/`, `?nbhd=OLIVER`, `?year=2020` → 129,653 bytes every
time). No dynamic endpoint, no API, no server-side filtering. Their
`prop_details/<slug>.json` lazy-loading is per-neighbourhood static files —
exactly what Pages serves.

**Measured head-to-head:**

| | GitHub Pages (ours) | Cloudflare + nginx (theirs) |
|---|---|---|
| `Range: bytes=0-99` | **`206`**, `content-range: bytes 0-99/2495037` | **`200`** — full body, no `accept-ranges` |
| `accept-ranges` | `bytes` | absent |
| Edge cache | Fastly/Varnish (`via: 1.1 varnish`, `x-cache`, `cache-control: max-age=600`) | `cf-cache-status: DYNAMIC` on repeat hits — **edge never caches** |
| CORS | `access-control-allow-origin: *` | not set |
| HSTS | `max-age=31556952` | not set; `/assessment` redirects to plain `http://` |
| Unknown paths | real 404 | soft-404: `200` + the 28,859-byte portal index |

Two consequences worth naming. Their edge not caching means the origin pays for
every cold visitor's 709 KB of GeoJSON. And **no Range support means PMTiles
would not work on their host as configured** — the one upgrade that actually
needs a capability, and the static host has it while the "real server" doesn't.
(Common cause is on-the-fly edge compression, which is incompatible with byte
ranges; fixable, but it's off today.)

**The renderer choice is entirely client-side.** MapLibre-native vs deck.gl,
CDN vs vendored — none of it is downstream of hosting. If anything, owning the
origin makes self-hosting libraries *easier*, so their CDN pins aren't
server-explained either.

**Where a real host would genuinely help us** — and it isn't the viz stack:
GitHub Pages' soft limits (≈1 GB repo, 100 MB per file, 100 GB/month bandwidth).
A parcel-scale PMTiles archive is the plausible first thing to brush them. That
is a data-volume argument, not a rendering one.

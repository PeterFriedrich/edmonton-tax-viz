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
  unopened lens is never downloaded. ⚠️ **ONE DELIBERATE EXCEPTION since
  2026-09-01:** the **100 m** grid is warmed in the background once the loading
  overlay lifts, so every visitor pays its 1.05 MB whether or not they open
  Glass. See "The grid switch's wait" below for why that one and not the other.
  Nothing else prefetches, and the 50 m grid explicitly does not.
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
| **boot, always (2026-09-01)** | `value_grid.json` — 100 m grid, **prefetched on idle** | **~1.05 MB** |
| Glass (50 m, on switch or hover) | `value_grid_50.json` | **~2.78 MB** |
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

**The 50 m grid is a SECOND file, not a bigger one (2026-09-01).** Both ship;
the Detail row picks between them and each is lazy, so the cost is **per-choice,
not additive** — a visitor who never switches pays ~1.08 MB, one who does pays
~2.82 MB for the second, and **boot is untouched either way**. The 2.69× cell
count (34.7k → 93.2k) is sub-linear because quartering a cell leaves empty
quarters: roads, parks, river valley.

**MEASURED on real hardware — the finer grid's cost is HARDWARE-DEPENDENT and
there is no single number for it: ~10.3% of frame rate on Intel Iris Xe, ~42% on
Intel HD Graphics 4400.** Acceptable for an opt-in lazy layer that starts
unselected, and the option stays — but **quote the range, never one figure**.

| machine | GPU | device px | @100 m | @50 m | cost |
|---|---|---|---|---|---|
| newer laptop | Iris Xe (Tiger Lake, 2020, 96 EU) | 1,083,214 | 117.3 | 105.2 | **10.3%** |
| older laptop | HD Graphics 4400 (Haswell GT2, 2013, 20 EU) | 845,234 | 36.6 | 21.4 | **42%** |

Both Firefox; both integrated; the older machine has **no second adapter** and
runs Mesa's **legacy `crocus`** driver (gen4–gen7; `iris` starts at Broadwell).
⚠️ **The ~4x difference in relative impact is the finding.** Ranking the machines
is safe, but see the vsync caveat below before converting either row to
milliseconds.
⚠️ **The older laptop was measured at 22% FEWER device pixels** and still came in
3.2x slower at 100 m — the confound runs in its favour, so the gap is real.
⚠️ **10.3% is an INTEGRATED-GPU number: Intel Iris Xe.** The machine it came from
also carries an NVIDIA RTX 3050 Ti, and `about:support` shows it `Active: No` —
Firefox was on the integrated adapter throughout, confirmed by WebGPU reporting
`wgpuDeviceType: "IntegratedGpu"`. **This site has never been measured on a
discrete GPU.** That is the right default to tune against (it is what most
readers have), but it means the numbers here are a floor-ish case, not a ceiling,
and nothing in this repo selects the adapter — it is a Windows per-app graphics
preference.

⚠️ **THE COST IS ALSO VIEWPORT-DEPENDENT, and the first measurement understated
it by ~3x.** A short-viewport run (668,880 px, devtools docked) read **3.7%**
against the tall run's 10.3% — superlinear, because a taller viewport shows
**more cells**, not merely more pixels per cell: geometry count and fragment load
both rise.
⚠️ **Do not extrapolate from two points.** Fullscreen at that DPR is ~2.07M px,
**1.91x** the tall run — plausibly worse than 10.3%, but that is arithmetic, not
a measurement. **Always record `devicePx total` beside any fps figure here**; a
frame rate without the pixel count it was measured at is not a fact about the
site, and quoting one across viewports is how 3.7% happened.

⚠️ **DO NOT CONVERT THESE fps FIGURES TO MILLISECONDS PER CELL (withdrawn
2026-09-02).** rAF frame times **quantise to multiples of 1/refresh**, and the
two machines were never in the same presentation regime: the older laptop is
**vsync-capped at 60 Hz** (`Target Frame Rate: 60`, 60 Hz panel) while the newer
one reported **117–139 fps**. Consequences, both load-bearing:
- The older laptop's 36.6 fps is a **mix of 1- and 2-vsync frames** (~64%
  spilled), not a 27.3 ms render. Bounding its true marginal cost gives roughly
  **3–36 ms** — any point estimate inside that is not a measurement.
- An earlier version of this section quoted marginal frame times of **0.274 ms
  and 0.981 ms**. Those are **smaller than that machine's own vsync quantum**
  (6.9–8.3 ms) and have been removed.
- **What survives:** mean fps over ~900 frames is a sound *monotone proxy* for
  render cost **within one machine at a fixed viewport** — sub-quantum changes
  shift how many frames spill into the next interval. So within-machine ratios
  (10.3%, 42%) stand; cross-machine millisecond arithmetic does not.
- `client-perf-snippet.js` now records a `refresh ceiling (idle rAF)` row and
  warns when a reading is within 5% of it. ⚠️ The 3.7% run's **139 fps trips that
  guard** against a plausible 144 Hz panel, so it may also have been clipped.

⚠️ **NEITHER capture controlled the browser environment.** The older laptop ran
with **Dark Reader, AdBlock and uBlock Origin** enabled — Dark Reader can apply a
page-level CSS filter, a fill-rate cost scaling with viewport pixels, i.e. the
variable under test. The newer machine's extension set was never recorded. A
controlled re-run means **extensions off and viewport tall**.

✅ The comparative claim (*"pans more smoothly on the newer laptop"*) is
**CONFIRMED**: 117.3 vs 36.6 fps at 100 m, with the confound in the older
machine's favour (22% fewer device pixels).
⚠️ Not measurable on the Oracle box — SwiftShader saturates at ~0.9 fps on BOTH
resolutions and once reported the finer grid as *faster* (ratio 1.29).

## The grid switch's wait is TRANSFER, and trimming the file does not fix it (2026-09-01)

Prompted by Peter: *"50 m grid, and to some degree 100 m grid take visible time
to load… I'm assuming we can't really speed it up too much."* Correct, and the
breakdown says why — the wait is almost entirely bytes on the wire.

| stage | 100 m | 50 m | measured how |
|---|---|---|---|
| transfer | **1.05 MB** gzip (2.83 MB raw) | **2.78 MB** gzip (7.63 MB raw) | `curl -w` against the live site |
| `JSON.parse` | ~30 ms | **~90 ms** | node, 3 runs, this box (ARM) |
| `gridScale()` first call | one sort of 34,671 values | one sort of 93,201 values | per metric+denominator, memoised on `gridData` |

**GitHub Pages already gzips it** — confirmed 2026-09-01, `content-encoding:
gzip`, 8,004,569 → 2,915,574 bytes on `value_grid_50.json`. There is no
compression win left to take, and nothing in this repo controls the encoding.

⚠️ **Payload trimming was measured and is NOT worth doing.** Three candidates,
all against the gzipped size, which is what is actually transferred:

| change | 100 m | 50 m |
|---|---|---|
| drop `median_year_built` | −3.3% | −2.8% |
| lon/lat to 5 dp + `exempt_frac` to 3 dp | −3.6% | −3.6% |
| both | **−7.0%** | **−6.4%** |

2.78 MB → 2.57 MB is not a perceptible change, and each costs something real: a
data-contract edit, or coordinates re-rounded under a 50 m grid. **Don't re-open
this without a plan that changes the format, not the contents** — a quantised
binary/typed-array payload is the only thing in the same conversation as a 2–3×
win, and that is a project (new decode path, new schema), not a tweak.

⚠️ **`median_year_built` ships in both grids and `web/index.html` never reads
it** — it is absent from `ensureGridData`'s column map, though the pipeline fills
it 89.9% / 92.6% and `export_value_grid.py` documents it as intended for
Development's stock-age spikes. It is ~3% of the payload. **Left in place
deliberately**: removing it is an output-schema change, so it is propose-first,
and 3% is not a reason.

**What was done instead — two things.** The wait is *reported* (an indeterminate
sweep on the pending Detail button, `docs/UI.md`), and for the default
resolution it is largely *moved off the click*.

### The prefetch, and why the boot finding is what makes it cheap

Peter: *"can we not actually do background loading, before they even select it?"*
The §Boot section below is what makes the answer yes: **every byte is on the page
by ~600 ms and the remaining seconds are GPU shader linking**, so through the
whole tail of boot **the wire is idle**. A background fetch there contends with
nothing — the boot's scarce resource is the GPU and the main thread, not
bandwidth.

- **Fires from `hideLoading()`**, via `requestIdleCallback` (1.2 s `setTimeout`
  fallback). ⚠️ **Not one step earlier**: `json()` parses on the **main thread**,
  and dropping ~30 ms of parse into the shader-link window would spend the one
  budget the boot is actually short of. Hanging it off the overlay lift also
  means a **failed** load never prefetches — `failLoading` does not route through
  there.
- **100 m only.** It is the default resolution and the one Infill needs anyway.
  The 50 m file is **2.78 MB against a ~3.56 MB boot set** — too much to push at
  a reader who may never open the Detail row — so it stays demand-driven, warmed
  on `pointerenter`/`focus` of its own button instead. Hover→click buys a few
  hundred ms on desktop and little on touch, but it is free and wastes nothing.
- **Save-Data is honoured for the unsolicited warm only** (`saveData`, or an
  `effectiveType` of 2g). A pointer already on the button is a request, not a
  guess, so the hover path does not consult it.

⚠️ **A warm must not activate.** `loadGridData` fills `gridStore` and touches
nothing else; only `ensureGridData` repoints `gridData`/`gridCell`, which are
statements about what is **on screen**. A prefetch that set them would make
`applyView`'s `gridCell !== wantCell` gate believe a never-drawn grid was already
up. `verify-grid-loading.js` asserts the split directly.

⚠️ **The prefetch made the busy stripe's gate falsifiable**, which it had not
been: the warm sets `gridFetches[100]` seconds before `gridStore[100]`, so a
click landing in that window is a real wait that the `gridFetches` gate would
show nothing for. Before the prefetch, no arrangement of clicks distinguished the
two.

⚠️ The remaining un-costed step is the deck.gl layer rebuild and first GPU upload
of 93,201 instances, which **cannot be measured on this box** (SwiftShader, see
above). If the switch still feels slow with the stripe in place — or if 100 m
still feels slow *now that its bytes arrive before the click* — that is the thing
to capture on real hardware. It would mean the cost was never the bytes.

## Boot time is a THIRD budget, and it is neither frames nor bytes (2026-08-30)

Prompted by Peter: *"why is mobile super fast to load, but desktop is not"*.
Measured against a local server on an idle box, median of 5 runs per profile,
Playwright device emulation.

**The answer is that the page has no device-dependent load path at all, and the
load is not network-bound either.**

| | desktop 1440×900 | mobile (Pixel 5) |
|---|---|---|
| loading overlay hidden | 5,722 ms | 5,841 ms |
| first contentful paint | 236 ms | 248 ms |
| requests / bytes | 10 / 3.56 MB | 10 / 3.56 MB |

Identical, with emulated mobile marginally **slower**. The three `matchMedia`
calls in `web/index.html` gate chrome only — a bottom-sheet position, a blurb
placement, a folded panel. **No fetch is gated on viewport**, and the lazy `??=`
memoization above means the boot set is the same everywhere.

⚠️ **Every byte is on the page by ~600 ms.** Vendor JS lands at 37 ms, the hood
GeoJSON at 240 ms, reference/temporal/status by 600. **The remaining 5–9 seconds
is GPU work, not download and not application JS**: a CDP CPU profile of the
whole boot attributes **94.6% of samples to `(program)`** — native/GL time — and
the highest real JS frame is deck.gl's `_getLinkStatus`, i.e. **shader program
linking**. Application code does not appear.

**So a "slow load" report is a driver question first.** A phone always gets
hardware WebGL; a desktop Chrome that has fallen back to software rendering does
not, and it will lose to a phone on precisely this workload — which is the only
shape of explanation that fits an otherwise backwards symptom. Check
`chrome://gpu` (**WebGL / WebGL2**: *Hardware accelerated* vs *Software only*)
before touching the page. Usual causes: hardware acceleration disabled in
settings, a blocklisted or stale driver, a VM or remote-desktop session.

⚠️ **Two limits on the numbers above, both load-bearing:**

- **This box has no GPU.** Its renderer is `ANGLE (… SwiftShader driver)`, so
  5.7 s is a *software-GL* figure and is not what anyone's desktop sees. It is
  valid for A/B comparison (§How to profile, harness 1) and worthless as an
  absolute.
- **Emulation shares the host GPU.** Playwright's mobile profile changes
  viewport, DPR, touch and UA — nothing else. That is exactly why this test can
  prove **no code branch** explains a device gap, and can prove **nothing** about
  hardware. Do not use it to argue a device is fast or slow.

**If the shader-link cost ever needs reducing**, the lever is the number of
distinct **layer types** in the boot stack, not the data volume —
`buildLayers()` returns `referenceUnderLayers() + buildViewLayers() +
referenceOverLayers()` in one shot, and each distinct layer class costs its own
program compile. Vertex count (the lever for §Findings) does **not** help here.

---

## Rules of thumb

1. **No `wireframe: true`** on extruded layers at this polygon count.
2. **No rounded line joints/caps** on detailed rings — miter only.
3. **Keep vertex count down** — it's the lever that helps every layer. Prefer a
   display-only simplify over per-layer micro-tuning.
4. **Judge on the iGPU baseline,** not a discrete GPU. The concrete baseline is
   now named: **Intel HD Graphics 4400 (Haswell GT2, 2013), Mesa `crocus`,
   60 Hz** — the older laptop. The site has **never** been measured on a
   discrete GPU.
5. **Confirm the *feel* on a real GPU** (DevTools Performance) before declaring a
   perf change done — the headless harness only points at the suspect.
6. **A "slow load" is a GPU question until proven otherwise.** Boot is ~600 ms of
   network and seconds of shader link; check `chrome://gpu` before profiling the
   page. And ⚠️ **never conclude a device difference from emulation** — it shares
   the host GPU (2026-08-30).
7. **Record the refresh ceiling beside every fps figure, and never convert fps
   to milliseconds across machines.** Frame times quantise to 1/refresh, so a
   60 Hz machine and a 144 Hz one are not on the same scale; a reading near the
   ceiling is measuring the display, not the site. Within-machine ratios at a
   fixed viewport are the comparable quantity (2026-09-02).
8. **A capture must control the browser, not just the machine** — extensions off
   (Dark Reader's page filter is a fill-rate cost), viewport tall, run warm.

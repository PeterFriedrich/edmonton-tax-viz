# Web map profiling harness

Headless screenshot + frame-time profiling for the Phase 2 web map
(`web/index.html`). Node + [Playwright](https://playwright.dev/) driving
Chromium with **software WebGL** (`--use-angle=swiftshader`), so it renders
with no GPU — this deliberately mirrors the low-end iGPU audience baseline
(see `docs/PERFORMANCE.md`).

This is dev tooling, not part of the shipped app. It lives outside `web/`
on purpose: GitHub Pages deploys `web/`, and we don't want `node_modules/`
dragged into the deploy.

## Setup (once)

```bash
cd tools/profiling
npm install
npx playwright install chromium   # downloads the browser binary
```

`node_modules/` and the browser binary are gitignored — re-run the above on
a fresh checkout.

## Usage

All scripts need the map served first. From the repo root, in another terminal:

```bash
cd web && python -m http.server 8777
```

Then, from `tools/profiling/`:

```bash
# 1. Screenshot + console/WebGL error capture (writes render.png)
node shot.js

# 2. Screenshot an arbitrary URL to a named file
node shot2.js "http://localhost:8777/index.html" out.png

# 3. Frame-time profile under a driven Ctrl+drag rotate
#    Prints frames / mean (fps) / median / p95 / max
node profile.js "http://localhost:8777/index.html" "baseline"
```

`.png` outputs are gitignored — they're throwaway render artifacts.

## Caveat

Software WebGL is a *proxy*, not ground truth. Use it to catch hangs and
gross regressions (it's how the rounded-joint render hang was found). For
final fps numbers, profile on a real GPU via browser DevTools — see
`docs/PERFORMANCE.md`.

## Conventions for `verify-*.js`

Two rules, both learned from defects the harness itself carried
(`docs/FINDINGS_vacuous_guards.md` V4).

### 1. Gate an early exit on the BUILD, not on the DATA

There are two builds — public (`/index.html`) and specialist (`/full/`) — and
**they serve the SAME GeoJSON**. A column being present therefore says *nothing*
about which build you are on. Full-only UI is gated in the app on `FULL_BUILD`
(or on `SERVICES[x].pub` for a service row), so:

```js
const hasX = ...state.data.features.some(f => f.properties.x != null);  // DATA
const fullBuild = await page.evaluate(() => FULL_BUILD);                // BUILD
```

Check the **data** gate first (an old data file hides the control everywhere),
then the **build** gate. Getting this wrong fails in both directions and both
were live on 2026-09-07: `verify-transit.js` and `verify-ind-permits.js` were
**red on a correct public build**, while `verify-bike.js` ran 3 of 37 checks and
exited 0. Assert the control matches the build in **both** directions —
`shown === fullBuild`, not `shown` — so the check still fails if the public
build starts showing something it must not.

⚠️ **`click` in these scripts is `page.$eval(sel, b => b.click())`, a JS click
that ignores visibility and `pointer-events`.** A missing build gate does not
stop the script; it drives the hidden control and reports PASS. That is how
`verify-transit.js` passed 23 checks against a UI the public cannot reach.

### 2. Say whether the run was complete

A script that early-exits prints a pass line and exits 0, which is
indistinguishable from a full run. Every script with an early exit therefore
ends one of two ways:

```
PARTIAL — ran 4 checks, then stopped: public build, transit is full-only
COMPLETE — ran 26 checks
```

**A consumer should treat `PARTIAL` as the signal** — the 32 scripts with no
early exit never print either line, so absence of `PARTIAL` is the passing
condition, not presence of `COMPLETE`.

⚠️ **Run these one at a time.** Concurrent runs manufacture failures on a
4-core box; re-run a red **alone** before believing it.

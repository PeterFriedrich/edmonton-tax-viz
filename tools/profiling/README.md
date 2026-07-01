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

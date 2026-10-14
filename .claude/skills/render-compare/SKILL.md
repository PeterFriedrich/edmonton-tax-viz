---
name: render-compare
description: >
  Render the Edmonton web app before and after a change, side by side, at
  phone/tablet/desktop sizes in both themes, and put the images in front of
  Peter. Use whenever a layout, colour, copy-placement or theme call is
  Peter's to make, or he asks to "see it", "show me", "before/after",
  "screenshot", "what does it look like on a phone", or to compare variants.
  Also use to check your own web change visually before asking for a merge.
---

# Render a before/after for Peter

Peter decides layout and design calls from pictures, not prose. This skill
produces one paired image per size × theme and a changed-pixel count for each,
so you can tell him where to look, and say plainly when nothing changed.

Scripts live next to this file: `render.js` (serve a tree, screenshot it) and
`compose.py` (pair the shots, count the change). Work in the session scratchpad
(`$S` below); never write probes or output into `tools/profiling/` or the repo.

## Steps

1. **Pick the two sides.** Usually *before* = `origin/master`, *after* = the
   working tree. Variants of one idea (P1–P6 style) are several *after* labels.
2. **Build each side with `build_site.py`.** ⚠️ Raw `web/` is NOT what readers
   see: it renders as the full build with no Beta badge. The public tree is
   `_site/index.html`, the specialist build `_site/dev-build-full/index.html`.
   ```bash
   S=<scratchpad>/rc; mkdir -p $S/before-src
   git archive origin/master web | tar -x -C $S/before-src
   .venv/bin/python scripts/build_site.py --src $S/before-src/web --out $S/before
   .venv/bin/python scripts/build_site.py --src web --out $S/after
   ```
3. **Render both, one at a time** (never alongside a verify run; this 4-core
   box manufactures timing and render failures under load):
   ```bash
   export NODE_PATH=/home/opc/edmonton-tax-viz/tools/profiling/node_modules
   R=.claude/skills/render-compare
   node $R/render.js --root $S/before --out $S/shots --label before [options]
   node $R/render.js --root $S/after  --out $S/shots --label after  [options]
   ```
   Options: `--page dev-build-full/index.html` for the full build;
   `--size 360x780,800x900,1280x800` (default); `--theme dark,light` (default);
   `--hash 'view=development&window=3yr'` for any state the link format carries
   (keys: `docs/CONTROLS_MATRIX.md` §8); `--js '<statements>'` for state it
   doesn't (open a panel, click a control), run after the page is ready;
   `--settle 1500` ms before the shot; `--touch auto|on|off` (auto = touch
   below 641 px, the phone breakpoint). Each line of output is JSON per shot:
   check `ready: true` and `errors: []`. About 15 s per shot.
4. **Compose and read the result yourself first:**
   `.venv/bin/python $R/compose.py $S/shots before after "<one-line caption>"`.
   Each pair prints `changed px` (pixels moved > 40 levels) and the box they
   sit in. **Two renders of the same tree differ by ≤ 7 px**, so a pair near
   that is "no change". Read every `compare_*.png` before sending; a pair that
   should differ and doesn't means the state never reached the page (bad hash
   key, `--js` ran before its target existed).
5. **Send it.** `SendUserFile` with the compare images that carry the
   decision, not all of them, and one line each naming what to look at
   ("360 light: the badge now clears the legend's last line"). If the call
   is between variants, label them as `COPY_DECISIONS.md` / the TODO item does.

## Pick sizes from the problem

- Phone: 360×780 (the narrowest layout tested; `verify-millrates` checks it),
  390×844 for a common phone.
- Breakpoint edges: 640 and 641 (the phone/desktop CSS seam,
  `docs/MOBILE_USABILITY.md`), and both ends of any band a finding names
  (light-mode F2 is 641–~930).
- Desktop: 1280×800. At that size only 2 counties draw at HOME.

## What the render cannot tell you

- **Text is too wide.** This box has none of the fonts in the page's CSS
  stack (only the shipped map-name face loads), so headless UI text reads
  ~15–20% wider than on Peter's laptop. A label that wraps or collides here may fit there. Never size CSS
  from these widths, and say so when a collision is the point of the image.
- **Colour is close but not exact.** It's software GL (SwiftShader), so
  judge contrast from the CSS values, not from sampled pixels.
- The first-visit guide never opens under automation (`navigator.webdriver`),
  so shots show the map as a returning reader sees it.

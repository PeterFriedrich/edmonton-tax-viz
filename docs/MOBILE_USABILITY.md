# Mobile Usability

Working doc for making the Edmonton revenue-per-acre viz usable on phones.
Everything here is split into **CONFIRMED** (verified by code-read or an actual
render) vs **NEEDS CONFIRMATION** (plausible but unverified — do NOT act on these
as fact; the last two sessions both burned time on unchecked premises). Update
the split as items get verified.

---

## 1. Architecture: what can be separated, what can't

The app is a single `web/index.html` (~3,200 lines), all inline CSS + JS, one
deck.gl / MapLibre canvas. There are **zero `@media` queries today** and the
viewport meta is already correct (`width=device-width, initial-scale=1`).

**Two layers, opposite answers to "can I separate mobile from desktop?":**

| Layer | Separable? | Seam |
|---|---|---|
| The map render (deck.gl layers, colours, heights, spike grid, data logic) | **No — shared** | none; it's one WebGL canvas. Touch pan/zoom/pitch already work via deck.gl. Anything about *what's drawn* hits both platforms by construction. |
| UI chrome (panels, control pods, legend, title, sizing, positioning) | **Yes — clean** | a `@media (max-width: …)` block appended to the END of `<style>`. Every rule inside fires only on small screens; the whole existing stylesheet stays the desktop baseline, untouched. Nothing in the media block can affect desktop. |
| Touch-specific interaction (tap/dismiss/gesture tuning) | **Yes — clean** | a JS branch guarded by `matchMedia('(pointer: coarse)')` — additive, desktop untouched. |

**Takeaway:** the rendering is genuinely shared, but ~all real mobile-usability
work (see §3) lives on the isolatable chrome/interaction side, so it can be done
with near-zero risk to the tuned desktop experience.

---

## 2. Current state — CONFIRMED (render pass, iPhone-13-class 390×844, touch)

Ran `tools/profiling/shot-mobile.js` (Playwright, 390×844, `isMobile`+`hasTouch`).

- **THE problem: the top third is an unreadable pile-up.** The title + multi-line
  blurb (left-anchored, `#title` spans top 20→196 px, right edge 382) and all six
  right-anchored control pods (`#coloradj` t20, `#toggle` t58, `#palette` t96,
  `#lens` t134, `#views` t172, `#layers` t210) occupy the same narrow band and
  render on top of each other. On desktop these clear each other because the
  window is wide; at 390 px they collide. This is the headline fix.
- **Wide pods clip off the LEFT edge** (not the right — they're `right:22px`
  anchored, so content grows leftward past 0): `#views` left = −107, `#coloradj`
  left = −51. The view-picker row (Ratio/Uses/Development/Infill/Glass) is the
  widest.
- **What's FINE:** the map itself renders correctly; the bottom-left `#legend`
  (top 751→822) is readable and clear of everything; MapLibre attribution sits
  clean bottom-right.

Screenshots: `mobile-default.png` (git-ignored artifact; regenerate via the tool).

## 2b. Current state — NEEDS CONFIRMATION

- **Tap-to-inspect (tooltips):** Peter observes on a **real device** that tapping
  a neighbourhood shows the tooltip — consistent with the mechanism (`getTooltip:
  tooltipFor`, deck.gl hover-pick; a tap produces a pick). **Treat as working.**
  The headless harness's synthetic `touchscreen.tap` did NOT produce a tooltip
  element — i.e. **the emulator is a weak oracle for touch interactions; the real
  device is authoritative.** Do device testing for anything touch-behavioural.
- Does the tooltip **dismiss** cleanly (tap empty space / another hood), or get
  "stuck" showing the last pick? (built-in deck tooltips can stick on touch) —
  unverified, real-device only.
- Tap-target size on the small pod buttons (`padding: 4–7px`) vs the ~44 px
  touch-target guideline — unmeasured.
- Pinch-zoom / two-finger pitch feel; whether page-zoom vs map-zoom conflict —
  unverified.
- Landscape orientation — not tested (portrait only so far).
- Legend bar fixed 200 px width, title `max-width:360px` — reflow behaviour on
  <360 px devices unverified.

---

## 3. Quick-pass plan (chrome layout first — highest impact, lowest risk)

Ordered; each step is independently shippable and desktop-safe.

1. **Establish the seam.** Append one `@media (max-width: 640px) { … }` block at
   the end of `<style>`. Nothing above it changes. All mobile rules live here.
2. **Fix the top-third collision (the headline).** Inside the media block, give
   the control pods a coherent small-screen layout instead of the desktop
   absolute-offset stack. Candidate approaches (decide when we get there):
   - collapse the pods into a single scrollable/stacked column, OR
   - a bottom sheet / hamburger that holds the controls, keeping the map clear.
   Also shrink/relocate the `#title` blurb (it's the biggest space hog) — likely
   collapse the long blurb to just the `<h1>` on mobile, with details on tap.
3. **Stop the left-edge clip** on `#views` / `#coloradj` (wrap or shrink the
   widest rows so nothing renders at negative left).
4. **Re-render + eyeball** with `shot-mobile.js` after each step; then hand Peter
   a real-device check for the touch-behaviour items in §2b (harness can't judge
   those).

**Not in the quick pass** (needs its own decision): tap-to-dismiss tooltip
tuning, touch-target resizing, landscape. Confirm they're actually problems on a
real device before building.

---

## 4. Tooling

- `tools/profiling/shot-mobile.js` — mobile-emulation render + panel-overflow
  report + tap probe. Run against a local server (`python3 -m http.server 8931`
  from `web/`), then `node tools/profiling/shot-mobile.js`. **Layout oracle only
  — not authoritative for touch interaction** (see §2b).

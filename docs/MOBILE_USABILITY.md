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

Re-run **2026-07-24 against the merged S65 regroup** (5-view `#controls` flex
column) via `tools/profiling/shot-mobile.js` (Playwright, 390×844, `isMobile`+
`hasTouch`), default **Money** view. The prior 7-view observations are superseded
(the pod ids + geometry changed). Screenshot `mobile-default.png` inspected.

- **What the regroup fixed for free: the pods no longer overlap *each other*.**
  The old desktop absolute-offset stack is gone; `#controls` is now a flex column,
  so the visible pods lay out in vertical sequence with no mutual collision:
  `#views` t20–48, `#toggle` t56–87, `#layers`(+`#moneydetail`) t95–206,
  `#coloradj` t214–242, `#lens` t250–278, `#a11y` t286–314. Structure-before-mobile
  paid off here.
- **THE remaining problem: the control column sits ON TOP of the title blurb.**
  `#title` (h1 + multi-line blurb) spans left 22→right 382, **top 20→196** — i.e.
  the full width of the top third. `#controls` occupies **top 20→314** over the
  same band. So in the render the blurb text shows *through* the gaps between the
  control buttons — the top third reads as an unreadable pile-up, just
  title-vs-controls now instead of pod-vs-pod. **The blurb is the space hog;
  collapsing it to just the `<h1>` on mobile (details on tap) clears most of this.**
  This is the headline fix.
- **Left-edge clip persists on the widest pods** (`right:`-anchored, content grows
  leftward past 0): `#controls` and `#coloradj` render at **left −51**, `#toggle`
  at **−10** — visible as the clipped "…r: sqrt scaling" label. *Improvement:*
  `#views` now fits (left 17) — the 7→5 view reduction fixed the worst offender,
  which used to sit at −107.
- **What's FINE:** the map renders correctly; `#legend` (bottom-left, left 22→304,
  top 751→822) is clear of everything; MapLibre attribution clean bottom-right;
  the per-view groups correctly hide in Money (`#devdetail`/`#devmode`/`#devmetric`/
  `#devwindow` `display:none`, `#palette` popover closed, `#banner` none).
- **Tap probe still returns no tooltip element** — unchanged; the emulator remains
  a weak oracle for touch (§2b). Real-device tap-to-inspect is authoritative.

Screenshots: `mobile-default.png` / `mobile-after-tap.png` (git-ignored artifacts;
regenerate via the tool). Probe id list updated to the merged control structure.

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
2. **Collapse the title blurb (the headline — biggest single win).** Post-regroup
   the pods already stack cleanly among themselves (§2); the remaining top-third
   mess is the full-width `#title` blurb (top 20→196) *under* the `#controls`
   column. Inside the media block, collapse the long blurb to just the `<h1>` on
   mobile (details on tap/expand). This alone clears most of the pile-up because
   the controls no longer need to fight the blurb for the top third.
   - **Still open (decide here):** whether the flex column is enough as-is, or the
     controls should move into a bottom sheet / hamburger to free the map. The
     regroup's clean vertical stack makes "column is fine" more viable than the old
     7-view pile-up did — but the column still runs top 20→314, so a collapsed/
     scrollable container may still be worth it. Decide against the refreshed render.
3. **Stop the left-edge clip.** `#controls`/`#coloradj` render at left −51, `#toggle`
   at −10 (`#views` now fits). Wrap or shrink the widest rows so nothing renders at
   negative left.
4. **Re-render + eyeball** with `shot-mobile.js` after each step; then hand Peter
   a real-device check for the touch-behaviour items in §2b (harness can't judge
   those).

**Open UX concern — the `#views` bar under-reads as the primary control** (Peter,
2026-07-24, looking at the move-1 render). `#views` (Money · Services · Ratio ·
Development) is *the* top-level control — the thing users act on first — but it
renders (a) too small relative to the secondary pods below it (same font/weight as
a metric toggle), and (b) "far away" up at the very top, so it doesn't read as the
primary switch. This is the hierarchy question the **move-2 fork feeds into**: a
bottom-sheet would let the view-picker sit prominently on the always-visible
collapsed bar (native pattern) rather than as a small strip at the top. Likely
applies to desktop too, not just phone. NOT yet actioned — recorded for the move-2
decision. (Interacts with: Uses pulled to full-only 2026-07-24, so public `#views`
is now 4 buttons, `DECISIONS.md`.)

**Not in the quick pass** (needs its own decision): tap-to-dismiss tooltip
tuning, touch-target resizing, landscape. Confirm they're actually problems on a
real device before building.

**Handled structurally, not by CSS:** the Development **grid checkbox → spike
picker** nesting is a weak small-screen affordance (Peter flagged, 2026-07-23).
Rather than restyle it for phone, the regroup pass collapses it into one 3-way
"Detail" selector (Neighbourhood / 100 m grid — activity / Stock age) — see
`docs/CONTROLS_MATRIX.md` §7 + `DECISIONS.md`. Structure-before-mobile: the CSS
pass inherits the flattened control, no phone-specific reveal logic needed.

---

## 4. Tooling

- `tools/profiling/shot-mobile.js` — mobile-emulation render + panel-overflow
  report + tap probe. Run against a local server (`python3 -m http.server 8931`
  from `web/`), then `node tools/profiling/shot-mobile.js`. **Layout oracle only
  — not authoritative for touch interaction** (see §2b).

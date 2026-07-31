# Mobile Usability

Working doc for making the Edmonton revenue-per-acre viz usable on phones.
Everything here is split into **CONFIRMED** (verified by code-read or an actual
render) vs **NEEDS CONFIRMATION** (plausible but unverified — do NOT act on these
as fact; the last two sessions both burned time on unchecked premises). Update
the split as items get verified.

---

## 1. Architecture: what can be separated, what can't

The app is `web/index.html` (~3,600 lines of markup + JS) plus
**`web/styles.css` (~400 lines — extracted 2026-07-29, all CSS lives there
now)**, one deck.gl / MapLibre canvas. The viewport meta is already correct
(`width=device-width, initial-scale=1`).

**The phone seam is `@media (max-width: 640px)` at the END of `web/styles.css`**
(one block; steps 1–2 of §3 shipped into it, plus the temporal bottom sheet).
It was inline in `index.html` until the CSS extraction — anything below that says
`<style>` means that file.

⚠️ **There are now TWO seams, and they answer different questions (2026-07-31).**
The block above is about **how much screen there is**; a second
`@media (hover: none)` block immediately before it is about **what is pointing at
the screen**. Put a rule in the hover seam when the reason is the *finger*: the
touch-only peek card (`#peek`) exists because a finger cannot hover, and the
enlarged 44px `#temporal-close` is needed on an 800px touch tablet and wrong for
a mouse in a 400px-wide desktop window. Width is the wrong test for both. The JS
side uses the matching `noHover()` helper, not a width check.

**One measured lesson from the seam, worth having before the next rule
(2026-07-29):** the history panel's desktop background is `rgba(12,12,20,0.92)`,
the value every reading surface here shares. As a **bottom sheet** it sits over
the legend and both bottom-right pods, and at 0.92 their labels ("Data &
Methods", "$50k+", the MapLibre attribution) read straight *through* its own
text — it needed 0.985. **0.92 is enough over the map; it is not enough over
other chrome**, and on a phone almost anything full-width lands on other chrome.
`#about-menu`'s comment records the first half of this lesson; this is the second.

**Two layers, opposite answers to "can I separate mobile from desktop?":**

| Layer | Separable? | Seam |
|---|---|---|
| The map render (deck.gl layers, colours, heights, spike grid, data logic) | **No — shared** | none; it's one WebGL canvas. Touch pan/zoom/pitch already work via deck.gl. Anything about *what's drawn* hits both platforms by construction. |
| UI chrome (panels, control pods, legend, title, sizing, positioning) | **Yes — clean** | the `@media (max-width: 640px)` block at the END of `web/styles.css`. Every rule inside fires only on small screens; the whole existing stylesheet stays the desktop baseline, untouched. Nothing in the media block can affect desktop. |
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
  `#coloradj` t214–242, `#lens` t250–278 (`#lens` removed 2026-07-26),
  `#a11y` t286–314. Structure-before-mobile
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
  at **−10** — visible as the clipped "…r: sqrt scaling" label. *Improvements:*
  `#views` now fits (left 17) — the 7→5 view reduction fixed the worst offender,
  which used to sit at −107. **`#coloradj` is FIXED as of 2026-07-25**: dropping
  its state caption (folded into the button label, 417px → 169px) moved it from
  left −51 to **left 177**, fully on screen at 390px — measured, not inferred.
  The `@media` rule that used to hide the caption on phones went with it. The
  `#controls` −51 figure predates that change; re-shoot before acting on it.
- **⚠️ CORRECTION (2026-07-25, later the same day): `#botleft` was NOT "clear of
  everything" — its invisible hit box was not.** The "no collision" note below
  was screenshot-confirmed, and a screenshot can only see *paint*. The wrapper
  carried no `pointer-events: none`, so its box — as wide as the `#legend` inside
  it — reached across a 390px screen to the bottom-right pods and **intercepted
  clicks meant for them** (it blocked the new Sources credit button outright),
  besides stealing map drags in that corner at every viewport. Separately,
  everything on the map sits at `z-index: 1`, so `#botleft` *painted through* a
  tall bottom-right popover. Both fixed 2026-07-25 (`DECISIONS.md`). **Lesson for
  this doc: "no collision" claims need a hit test (`page.click()` /
  `elementFromPoint`), not a screenshot** — overlap you can't see is still
  overlap.
- **⚠️ SECOND CORRECTION (same day): the bottom band is genuinely tight — treat
  any new anchored pod as a width budget, not a label.** A `Data: City of
  Edmonton Open Data · 2025` button measured **294px** and landed on top of
  `#legend` (which reaches x=304 at 390px, set by its longest line, *not* by the
  200px gradient bar). Fixed by shortening the label **and** bounding `#botleft`
  to `calc(100vw - 175px)` so that line wraps — either alone was insufficient.
  Current clearance is **9px** at 390 and 360px, asserted by geometry in
  `verify-about.js`. **Anything else added to either bottom corner has to be
  measured against that 9px, at both widths.** Related: on phones the mobile
  convention for this kind of chrome is a *short* label or a bare ⓘ that expands
  — see `docs/UI.md` "What other maps actually do".
- **What's FINE:** the map renders correctly; the bottom-left `#botleft` cluster
  (three stacked rows: the `#compass` arrows+needle added 2026-07-25, the Center
  2D / Center 3D `#viewbtns` row added 2026-07-24, then `#legend`) is clear of
  everything — all three rows fit within a 390px phone with no clip and no
  collision with the bottom-right Display popover or attribution
  (screenshot-confirmed 2026-07-25). The compass arrows also give phones a
  **one-finger way to rotate**, which the two-finger twist (competing with
  pinch-zoom) did not; MapLibre attribution clean bottom-right;
  the per-view groups correctly hide in Money (`#devdetail`/`#devmode`/`#devmetric`/
  `#devwindow` `display:none`, `#palette` popover closed, `#banner` none).
- **Tap probe still returns no tooltip element** — unchanged; the emulator remains
  a weak oracle for touch (§2b). Real-device tap-to-inspect is authoritative.

Screenshots: `mobile-default.png` / `mobile-after-tap.png` (git-ignored artifacts;
regenerate via the tool). Probe id list updated to the merged control structure.

**Chrome coverage, measured 2026-07-27** (sum of the visible chrome rects over
the viewport area, ignoring mutual overlap, default Money view):
**45.1% at 390×844** against **27.3% at 1440×900**. This is the first hard
number behind "the panels cover much more of a phone screen" and it confirms
the §3 priority order: the blurb collapse is worth more on mobile than any
amount of tuning downstream of it.

Consequence found while fixing the label sweep to dodge that chrome
(`docs/UI.md` "Labels dodge the chrome"): with ~45% of the canvas spoken for,
map labels on a phone are **genuinely scarce** — the cull is correct, but the
labels it removes were unreadable, not surplus. Two real collisions in the
before-shot: THE ORCHARDS AT ELLERSLIE painted across the compass buttons, and
EDMONTON SOUTH EAST straight through the legend, obscuring the `$50k+` scale
label. **Label density on mobile is not a label problem — it is the panel-size
problem**, so revisit it only after the blurb collapse lands.

## 2b. Current state — NEEDS CONFIRMATION

- **The hover tooltip fired on TOUCH and ran off the right edge — CONFIRMED ON
  DEVICE 2026-07-31, fixed same day.** Peter, asked whether a tooltip box
  appeared as well as the peek card: **yes, both.** deck's `getTooltip` is
  driven by a **hover pick**, and a tap synthesises one through the
  compatibility mouse event, so the full `.tip` box drew on top of the peek
  card, positioned at the finger, **left 195 → right 517 on a 390px viewport**
  (127px off-screen, text cut mid-word). Fixed by returning `null` from
  `tooltipFor` under `noHover()`; the card carries the same `primaryRow` line,
  so nothing is lost. Regression net: `verify-peek.js` asserts no `.tip` exists
  after a touch tap.
  - ⚠️ **Two lessons, both about how it was missed for a whole session.**
    **(1)** The S81 claim "on a phone the `.deck-tooltip` node never exists at
    all" was *true and too narrow* — the app renders its **own** `.tip` via
    `className`, and only deck's built-in was checked. **(2)** It was found by
    **eye, in a screenshot**. Every assertion passed, and `shot-mobile.js`'s
    id-based overflow table **structurally could not** see it, because `.tip`
    has no id. That script now sweeps for overflow generically.

- **Double-tap zoom on the chrome (fix shipped 2026-07-27) — CONFIRMED ON DEVICE
  2026-07-27.** Peter, on a phone: *"double tap on phone no longer zooms in for
  the buttons, only the map."* That confirms **both halves** of the design — the
  chrome no longer hijacks the gesture, and the map deliberately still does.
  Original report was accidental page zoom, "for sure common with the rotation
  buttons, but also just by accident on this UI". Mechanism: iOS Safari keeps
  double-tap-to-zoom even on a `width=device-width` viewport, and nothing set
  `touch-action`. Fixed with `touch-action: manipulation` on the chrome roots
  **and** the controls (`DECISIONS.md` 2026-07-27); the map canvas deliberately
  keeps the gesture. **Headless Chromium cannot reproduce the iOS behaviour**,
  so `verify-controls-clickable.js` asserts the *mechanism* (55/55 controls
  carry the property, `#map` does not) and NOT the outcome — the device check
  is what closed it, per the tooltip precedent below.
  - **Still unconfirmed: pinch zoom.** The fix deliberately avoids
    `user-scalable=no` (which would fail WCAG 1.4.4), so pinch should be
    unaffected, but nobody has actually pinched. One gesture to settle it.
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

> **STATUS 2026-07-31 — steps 1, 2 AND 3 are all closed. Do not re-plan them.**
> Steps 1-2 shipped in `0089eba` ("mobile chrome move 1") and Peter confirmed
> the collapse on device. **Step 3 (the left-edge clip) was closed as NOT
> REPRODUCIBLE, with no code change** — see the step itself. The only thing left
> in this section is the *open question* inside step 2 (bottom sheet or not),
> which is a decision for Peter against the CURRENT render, not a build item.
> This note exists because the list below reads as a forward plan and a session
> mistook it for one.

1. ~~**Establish the seam.**~~ **DONE.** One `@media (max-width: 640px) { … }`
   block at the end of `<style>`. Nothing above it changes; all mobile rules
   live there.
2. ~~**Collapse the title blurb (the headline — biggest single win).**~~
   **DONE** — `#title` shows only the `<h1>` on mobile and taps open the blurb
   as a card (`#title.expanded`). Original reasoning kept below; the *open
   question* at the end is still open. Post-regroup
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
3. ~~**Stop the left-edge clip.**~~ **CLOSED 2026-07-31 as NOT REPRODUCIBLE —
   no code change.** The S74 symptom (`#controls`/`#coloradj` at left −51,
   `#toggle` at −10) does not occur on current master. Re-measured at 390×844
   with `hasTouch`/`isMobile`, in **both builds**, across **every visible view**,
   with the Options pod **unfolded**: `#controls` 8→382, `#views` 22→382,
   `#toggle` 103→382, and the pod rows (`#coloradj`/`#layers`/`#moneymode`/
   `#chgwindow`) 177→371. Nothing at negative left, nothing off the right.
   ⚠️ **Two traps make a naive pass lie, and both are worth keeping:**
   **(a)** `#optpanel` is `.folded` by default at ≤640px, so its rows have **no
   layout box** and report `0,0` — the folded state *cannot* show the clip, and
   reads as "fixed" for the wrong reason. Unfold first.
   **(b)** The public build keeps full-only controls in the DOM but **hidden**,
   so selecting by presence hangs Playwright's `click()`; filter on visibility.
   Headless Chromium also measures text **wider** than the real `-apple-system`
   stack, so a no-clip verdict there **errs safe**.
   ✅ **`tools/profiling/shot-mobile.js` was fixed for this job (2026-07-31).**
   Its id list is now the page's own `CHROME_IDS` (read live from the page, so
   chrome added later is picked up) plus the rows `CHROME_IDS` deliberately
   omits; it honours its URL argument; and the tap probe looks for `#peek`.
   ⚠️ **An id list can only ever see chrome that HAS an id** — the worst
   overflow on the page is `div.tip`, which has none, so the script now also
   sweeps for overflow generically. Read that section, not just the id table.
4. **Re-render + eyeball** with `shot-mobile.js` after each step; then hand Peter
   a real-device check for the touch-behaviour items in §2b (harness can't judge
   those).

**UX concern — the `#views` bar under-reads as the primary control** (Peter,
2026-07-24, looking at the move-1 render). `#views` (Money · Services · Ratio ·
Development) is *the* top-level control — the thing users act on first — but it
rendered (a) too small relative to the secondary pods below it (same font/weight as
a metric toggle), and (b) "far away" up at the very top, so it didn't read as the
primary switch.

- **(a) SIZE — fixed 2026-07-25.** `#views` is now the largest type in the stack
  (**14px / 9px 18px**, up from 11.5px / 6px 12px — the metric bar is 12.5px and
  the modifiers 11.5px), so the visual weight matches the tier. Phones scale it
  back to **12.5px / 7px 11px** in the `@media` block: at 14px the four public
  views no longer fit one 390px row, and wrapping the primary control costs more
  than the extra size buys. Measured after: one row at 390px for both the 4-view
  public and 5-view full builds, no left clip. **The phone scale-back was
  reviewed and LOCKED 2026-07-26** (Peter) — it is a deliberate choice, not an
  unfinished edge: 12.5px still out-ranks the 11.5px modifiers, so Tier-1
  primacy still reads on a phone. `DECISIONS.md` 2026-07-26.
- **(b) POSITION — still open.** It's still a strip at the very top; that's the
  hierarchy question the **move-2 fork feeds into** (a bottom-sheet would let the
  view-picker sit on the always-visible collapsed bar). Applies to desktop too.

(Interacts with: Uses pulled to full-only 2026-07-24, so public `#views`
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
  report + tap probe. Serve `web/` (quirk q), then
  `node tools/profiling/shot-mobile.js [url]` — **the URL argument works as of
  2026-07-31; before that it was accepted and silently ignored** in favour of a
  hardcoded port 8931. **Layout oracle only — not authoritative for touch
  interaction** (see §2b). Reports the id table, the post-tap `#peek` box, and
  a generic overflow sweep that catches unidentified chrome like `div.tip`.
- `tools/profiling/verify-peek.js` — the touch gesture net (**25 checks**,
  desktop + 390×844). ⚠️ **Budget 900s, not 400.** Measured **419s** standalone
  on 2026-07-31, up from the ~150s recorded at S81; a `timeout 420` killed it
  mid-gesture and the crash (`Target page … has been closed`) reads exactly like
  a logic failure. **The cause was not isolated** — 4 checks were added the same
  day, so do not assume it is the box. ⚠️ **The only script in the suite that
  drives a REAL pointer at the
  map**; the other 26 call `temporalClick()`/`openTemporal()` directly in JS,
  which is why single-tap-opens-everything went unnoticed through the whole
  temporal lens build. If you are testing a *gesture*, a JS call proves nothing —
  the gate lives between the gesture and those functions.

⚠️ **Driving real taps has three traps, all measured 2026-07-31, and each one
looks exactly like the feature being broken:**
1. **Deck renders its picking buffer on demand, and under headless SwiftShader
   that pass is too slow for a click's synchronous pick** — bare taps registered
   **2 of 4**, versus **4 of 4** when a `pickObject` was issued first to warm it.
   Warm before every map gesture. This is a software-GL artifact of the harness,
   **not** something a device with hardware GL does — do not "fix" the app for it.
2. **A pixel must pick the same hood across a ring around it, not merely pick
   something.** Click-time picking rounds device pixels differently from a manual
   `pickObject`, so a pixel on a polygon *edge* reports hood A and delivers hood
   B. The west edge at the default zoom is river-valley slivers with no safe
   interior — start from the middle of the map.
3. **A touch tap can deliver the handler TWICE** (touch event + compatibility
   mouse event), so any toggle driven by a tap fires at random. Make touch paths
   idempotent instead of counting events.

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

> **⚠️ 2026-08-06 — THE FIRST TOUCH-ONLY REGRESSION TO REACH PRODUCTION, and
> the lesson is about where a view rule gets written, not about layout.**
> Gating the assessment-history panel out of the Services lens was written into
> `temporalFor()`, the shared **data** accessor. **The peek card gates on the
> same function**, and because §2b's confirmed fix suppresses `.tip` on touch,
> that card is **the only per-hood readout a phone has** — so Services went to
> *no tooltip and no card*: tapping a neighbourhood returned nothing at all.
> Desktop was completely unaffected, which is why it read as fine.
> - **Nothing in the verify suite caught it.** The suite covers the card
>   (`verify-peek.js`) and covers Services (`verify-services.js`), but had no
>   case for **the card in a view with no panel** — a per-view × per-surface
>   combination, which is exactly the gap `CONTROLS_MATRIX.md` exists to make
>   visible. `verify-peek.js` now owns that case and is falsified against the
>   broken build.
> - **The standing rule this produces:** any change that can stop `#peek`
>   opening is a **mobile-outage** change, not a cosmetic one. Desktop keeps its
>   tooltip and shows nothing wrong. Test it on `hasTouch` before believing it.
> - ⚠️ **The harder half was the deliberate opt-in** (`panelByChoice`): it
>   routes a tap *past* the card straight to pinning, so a fix verified from a
>   fresh load still left the tap dead once the user had opted in. A touch check
>   that only ever runs from a clean state is not covering touch.

> **2026-08-02 — two changes that landed on the phone without needing a phone
> form, and one that was a phone bug all along.**
> - **The change lens moved onto the map surface.** `#moneymode` (Current |
>   Change over time) left the Options panel to become `#toggle`'s row 2 under
>   **Value**. Reaching it on a phone was *unfold Options → find "Lens" → tap*;
>   it is now *Value → Change*, both on the map. The pod still fits **one row at
>   390px** (measured `180,97 202x55`). **Nothing was added to the default
>   render** — row 2 is exclusive with the revenue cuts.
> - **The revenue panel reuses the existing bottom sheet.** On Money's revenue
>   metrics `#temporal` shows the zone-revenue breakdown instead of the
>   assessment chart. Because it is the *same element*, the phone form,
>   dismissals and `#hoodmode` behaviour came for free — measured at 390×844 the
>   sheet renders 6 rows, bar `display:flex`, `8..382` of 390, bottom 836/844.
>   ⚠️ The colour bar reuses `.mixbar`, whose rule was scoped `.tip`/`#peek-read`
>   — **borrowing markup without its CSS collapses it to nothing visible**, the
>   second occurrence of that trap.
> - ⚠️ **The Display-popover overlap was NOT desktop-only**, though it was
>   reported and carried as a generic UI bug. Measured identically at **1440×900,
>   390×844 AND 360×780** (22px), because both pod offsets are fixed pixels. The
>   bottom-right column is one of the few places where **a fixed-offset stack
>   behaves the same at every width** — so a phone measurement adds nothing there,
>   unlike everywhere else in this document.

> **2026-08-01 — the mill-rate pod's phone form: the answer was NOT to place a
> pod, it was not to have one.** Shipped desktop-first, then Peter: *"no rates
> show on mobile"* → *"stacked, like bullet points almost, top left, where the
> description bubble would be, then folded in when you open the bubble"* → after
> seeing a standalone card built to that description: ***"i don't like the
> independent mill rates panel. folding it into the tax revenue blurb is fine."***
> The rates are now **re-parented into `#title`** at this seam: they open and
> close with the description card and add **nothing** to the default render.
>
> The intermediate build is worth keeping because everything it had to solve
> **stopped being a question** once the pod lived in the blurb:
> - ⚠️ **"Under the title" is not a phone location.** Measured at 390×844,
>   `#title` collapsed is 20–43 but `#controls` owns **58–197** — the same fact
>   that made `#temporal` a bottom sheet here. A desktop anchor needs a
>   *different anchor* on a phone, not a different offset. The standalone form
>   hung off `#controls`; the folded form needs no anchor at all.
> - ⚠️ **Bare text over the map does not survive the phone.** Desktop chrome sits
>   in a corner over dark map; a phone's map fills the screen, so the standalone
>   pod landed on the downtown prisms and 10.5px muted text on bright yellow was
>   unreadable (seen in a screenshot, not predicted). It needed its own card
>   background. Inside the blurb there already is one.
> - ⚠️ **A yield must be scoped to where the contention is.**
>   `#temporal.open ~ #millrates` shipped ungated with a comment saying it was
>   "desktop-only in effect" — reasoning about the LAYOUT (the panel is a bottom
>   sheet on a phone, so they never overlap) and not about the SELECTOR, which
>   matched everywhere. Switching the readout to **panel mode** blanked the rates
>   on a phone with nothing contending. It is desktop-only by construction now
>   (a child of `#title` is not `#temporal`'s sibling), and
>   `verify-millrates.js` asserts the property directly so it holds however a
>   future form achieves it.
>
> **The general shape:** on a phone, ask whether the thing needs to be its own
> surface before asking where to put it. Three separate problems here were all
> artifacts of it being one.


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

**Chrome coverage — RE-MEASURED 2026-08-01. ⚠️ THE 45.1% FIGURE WAS INFLATED AND
DROVE THE BACKLOG FOR SIX SESSIONS.** The 2026-07-27 method summed the visible
chrome rects *ignoring mutual overlap*, and the chrome **nests**: `#controls`
contains `#views`, `#toggle`, `#optpanel` and `#layers`, and `#botleft` contains
`#legend`, so containers were counted two and three times. Both numbers below,
default Money view — `sum` is the old comparable method, `union` counts each
pixel once (2px grid sample):

> **RE-MEASURED AGAIN 2026-08-04, per view.** The default reproduced to the
> decimal (**27.9%**), so the method is stable and the movement below is real.
> ⚠️ **But the 54.3% was attached to a state that has since shrunk, and the
> ">half the screen" state was never the one the doc named.** `#moneymode` left
> the Options panel for `#toggle` row 2 on **2026-08-02 — one day after the
> 08-01 measurement** — so Money unfolded lost a row and is now **47.9%, under
> half.** The only >50% states are **Services** and **Development**, which had
> never been measured.

| state | 390×844 | 1440×900 |
|---|---|---|
| **default** (Options folded on phone) | sum 37.9% · **union 27.9%** | sum 28.5% · **union 20.3%** |
| **Money UNFOLDED** | sum 78.5% · **union 47.9%** | 20.3% (never folds) |
| **Services UNFOLDED** *(full only)* | sum 112.7% · **union 53.1%** | **20.0%** |
| **Development UNFOLDED** | sum 114.1% · **union 52.7%** | **27.4%** |
| **Ratio UNFOLDED** *(full only)* | **union 37.4%** | 15.2% |
| **Uses UNFOLDED** *(full only)* | **union 31.6%** | 12.1% |
| default + peek card open | sum 53.2% · **union 34.5%** | n/a (touch-only) |
| ⚠️ **worst PUBLIC state** — Development unfolded **+ peek open** | **union 52.3%** | n/a |

**What this changes.** The honest phone-vs-desktop gap in the default state is
**27.9% vs 20.3% — about 7 points, not the ~18 the old pair implied.** Part of
the drop 45.1 → 37.9 is real (the blurb collapse); the rest of the way to 27.9
is the method correcting its own double counting. **The default phone render is
not the problem.**

⚠️ **THE PUBLIC BUILD CANNOT REACH THE WORST STATE AT ALL.** Services and Ratio
are full-only since 2026-07-28 (`|| !FULL_BUILD`, `web/index.html` — the
`applyView` data-presence gate), so **public `#views` = Money · Development**.
A public phone user's worst reachable state is **52.3%**, and only by unfolding
Options *and* tapping a neighbourhood — both deliberate acts, and the peek card
is the answer to the tap. Rendered and eyeballed at that state: nothing clips,
nothing overlaps, the middle ~40% of the map stays clear.

**This is what closed the bottom-sheet question — see §3.** Any future coverage
claim should quote the union, name the state **and name the view**; a
single-view figure is what let the wrong state carry the backlog.

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
  `tooltipFor` under `noHover()`. Regression net: `verify-peek.js` asserts no
  `.tip` exists after a touch tap.
  - ⚠️ **"the card carries the same `primaryRow` line, so nothing is lost" was
    WRONG, and this entry said it for one day.** `.tip` was the only *multi-row*
    readout a phone had, so suppressing it left every lens showing a single
    line — Services dropped from six rows to one, Uses lost its composition bar
    outright. Reported by Peter the next morning (*"when I click on stuff on
    mobile now the pop up doesn't appear"* — the *popup*, i.e. the readout, not
    the card, which he confirmed he could still see). Fixed 2026-08-01 by having
    `openPeek` borrow `viewTooltip(info, false)` instead of `primaryRow`.
    **The suppression was right; the replacement was too thin.** A fix that
    removes a surface has to account for everything that surface carried, not
    just the row you were looking at when you removed it.
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

> **STATUS 2026-08-04 — THIS WHOLE SECTION IS CLOSED. Do not re-plan it.**
> Steps 1-2 shipped in `0089eba` ("mobile chrome move 1") and Peter confirmed
> the collapse on device. **Step 3 (the left-edge clip) was closed as NOT
> REPRODUCIBLE, with no code change** — see the step itself. **The last open
> item, the bottom-sheet question in step 2, was CLOSED 2026-08-04: the control
> column stays as-is, no bottom sheet, no hamburger** (Peter, against the
> re-measured §2 table; `DECISIONS.md`).
> This note exists because the list below reads as a forward plan and a session
> mistook it for one — **it is a record, not a queue.**

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
   - ~~**Still open (decide here):** whether the flex column is enough as-is, or
     the controls should move into a bottom sheet / hamburger to free the map.~~
     ✅ **CLOSED 2026-08-04 — THE COLUMN IS FINE AS-IS. No bottom sheet, no
     hamburger, no code change** (Peter, against the re-measured §2 table).
     The reasoning, so it is not re-opened on the old numbers:
     - The state that made this a priority, **Money unfolded at 54.3%, is now
       47.9%** — `#moneymode` moved to `#toggle` on 2026-08-02.
     - The remaining >50% states (**Services 53.1%, Development 52.7%**) are
       **transient and user-initiated** — you reach them only by unfolding
       Options, and they fold away again. The **default** render, which is what
       a phone user actually meets, is **27.9%**.
     - **The public build cannot reach the worst state** (Services/Ratio are
       full-only); its ceiling is 52.3%, rendered clean.
     - Against that, a bottom sheet is a refactor of **shared desktop+mobile
       DOM** (`CONTROLS_MATRIX.md`: grouping drives both), i.e. real desktop
       regression risk to fix a state the user can dismiss.
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
- **(b) POSITION — still open, but it no longer has a vehicle.** It's still a
  strip at the very top. ⚠️ **This used to say the "move-2 fork feeds into" it —
  a bottom sheet would have let the view-picker sit on an always-visible
  collapsed bar. That fork was refused 2026-08-04**, so if position is ever
  worth changing it now needs its own proposal. Applies to desktop too, and
  nobody has reported it since 2026-07-24.

(Interacts with: Uses pulled to full-only 2026-07-24, then **Services and Ratio
pulled too on 2026-07-28** — so ⚠️ **public `#views` is TWO buttons, Money ·
Development**, not the four this line used to claim. Corrected 2026-08-04 after
measuring the live build; the gate is `|| !FULL_BUILD` in `applyView`.
`DECISIONS.md`.)

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
- ⚠️ **SPLIT THE GESTURE FROM THE CONTENT — it is the difference between 7
  minutes and 40 seconds.** `verify-peek.js` is slow because a real tap needs the
  picking dance (warm-up, ±8px ring-stable targets, an empty-pixel scan). When
  the question is *what does the card SAY in each lens*, that machinery buys
  nothing: switch the view and call `openPeek(f.properties)` directly, then read
  `#peek-read` and screenshot. Used on 2026-08-01 to check five lenses plus the
  public build in one pass. **This is not a licence to test gestures that way** —
  §3's standing finding is that calling the handler directly proves nothing about
  the gesture, and `verify-peek.js` remains the only script that drives a real
  pointer at the map. Use the direct call for *rendering*, the real pointer for
  *behaviour*.
- ⚠️ **A throwaway script in `/tmp` needs
  `NODE_PATH=…/tools/profiling/node_modules`** — Playwright is installed there,
  not at the repo root, and `require('playwright')` fails from anywhere else.
  And use a bare `state`, never `window.state`: a top-level `const` lives in the
  global lexical environment and is not a property of `window` (quirk ss). Both
  cost a cycle each on 2026-08-01.
- `tools/profiling/verify-peek.js` — the touch gesture net (**27 checks
  measured** 2026-08-01, up from 25, desktop + 390×844). **Budget ~150s.**
  It ran **437s** until 2026-08-04, when its empty-map-pixel scan stopped hunting
  with `pickObject` and started deriving the pixel from projected geometry
  (**2,474 picks → 1**); it is now **94s**. ⚠️ **A timeout that fires mid-gesture
  crashes it with `Target page … has been closed`, which reads exactly like a
  logic failure** — that is what a `timeout 420` did on 2026-07-31, back when
  900s was the honest budget. ⚠️ **The only script in the suite that
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

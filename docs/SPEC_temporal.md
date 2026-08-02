# SPEC — Temporal lens: assessment over time, per neighbourhood

**Status 2026-07-29: ✅ COMPLETE AND SHIPPED IN `/full/`. All four phases done.**
The last open item — the pinned panel's design — was settled 2026-07-29 (§2), so
§7 is empty and nothing in this spec is pending. `tools/profiling/verify-temporal.js`
(38 checks) is the regression net; read §2 before changing the panel and §0
before touching anything that reads the historical file.
Peter, 2026-07-28: *"what I actually want is pop up graphs for the assessment of
each neighborhood… you mouse over and get a line graph of the assessment value
over time, for that hood."*

Companion docs: `data/DATA.md` §0 (the source + its defect), `docs/ANALYSIS_BACKLOG.md`
(the Downtown finding), `docs/ARCHITECTURE.md` (module conventions — **read before
writing any module**), `docs/CONTROLS_MATRIX.md` §2 (where a lens leaks).

---

## 1. What it is

A per-neighbourhood time series of assessed value, 2012–2025, surfaced on the
map: a **sparkline in the hover tooltip** as the glance, and a **click-to-pin
panel** as the readable version.

**Home: `/full/` only** (Peter, 2026-07-28 — *"we'd prototype this in full for
now"*). It already carries the work-in-progress badge, so an unfinished lens
arrives labelled. Gate with `|| !FULL_BUILD` beside the data guard, the
established idiom. **The public build is locked at two views and lenses return
one at a time after launch** (`DECISIONS.md` 2026-07-28) — this one is not a
candidate for that queue until Phase 0 closes.

## 2. Why a hover tooltip is not the whole answer

> ⚠️ **READ FIRST — `#temporal` IS NO LONGER THE ASSESSMENT-HISTORY PANEL IN
> EVERY LENS (changed 2026-08-01).** Everything in this section describes what
> the panel shows **under Value** — Current and Change over time. On Money's
> **revenue** metrics the same element shows the hood's **zone-revenue
> breakdown** instead (Peter: *"for revenue I want the panel to just be the top
> contributing zones by percent of hood revenue"*). The history is not lost: it
> moved to Value, which is what it actually describes.
>
> One element, two modes — `openTemporal` branches to `renderHistory` or
> `renderRevenueMix`. A sibling panel was rejected because `#temporal` already
> owns the three dismissals, the `CHROME_IDS` label-sweep exemption, the phone
> bottom-sheet form, `#hoodmode` and the peek card's commit path.
>
> **Consequences for anyone editing this section:**
> - The **three surfaces that advertise the panel** are lens-dependent now and
>   must stay in step: `#peek-go`, `#temporal-hint`, and the tooltip's invite
>   (`click to pin` ⇄ `click for the revenue mix`). A teaser for the wrong panel
>   is the failure mode.
> - **A pinned panel must re-render when the lens changes** — `syncPinnedPanel`,
>   called from `applyMetric`, `applyView`, `applyHoodMode` and once at init. A
>   revenue breakdown left under a value map is a silent-correctness failure.
> - `verify-temporal.js` **selects Value on every page it opens.** That is a
>   change of lens, not a relaxation; `verify-revenue-panel.js` owns the other
>   mode.
> - **The two rendering invariants below still apply in full** — they govern the
>   history chart, which is untouched.
> - ⚠️ **NEVER PIN A LIVE-YEAR NUMBER AS A LITERAL IN A CHECK** (2026-08-02).
>   `verify-temporal.js` used to assert Downtown's current share, commercial
>   share and assessed value as equalities; the 2026-08-01 refresh moved the
>   live slice and reddened 5 checks with nothing wrong. The live year is
>   sourced from the current roll and **genuinely moves week to week** — §0.3's
>   guard refuses to band it for exactly that reason, so a literal here
>   contradicts the guard. Live-year assertions are **derived from the loaded
>   series and compared against the rendered strings**; only the frozen
>   historical anchors (2012 5.09%, peak 5.55% in 2016) stay pinned, and those
>   are what prove the archive half of the splice held. Compare parsed numbers
>   with a one-display-ulp tolerance — building the expectation with the page's
>   own formatter would hide a formatter bug.

Mechanically a sparkline is trivial: `tooltipFor` already returns an HTML string,
and 14 points is one inline `<svg><polyline>` — no library, no dependency.

But a hover tooltip **vanishes on mouse-out, cannot be studied, and does not
exist on touch at all**, and the Money tooltip already carries 3–4 rows. So the
sparkline is the teaser and the pinned panel is the home.

### The panel's design — SETTLED 2026-07-29

⚠️ **Decided on the merits, not asked** — like the split above. Cheap to reverse;
say so if it is re-opened.

| choice | why |
|---|---|
| **Home: the left column under `#title`** (`top: 210px`) | The one region no chrome claims, so pinning a panel can never bury a control. The title's box was **measured** at 176–179px across all five views (the blurb wraps to ~8 lines at 360px), not estimated — a first pass at 128px overlapped it. `verify-temporal.js` asserts the clearance against `#title`, `#botleft` and `#controls`, so a longer blurb fails loudly instead of overlapping. |
| **Three dismissals: the ×, Escape, or a second click on the pinned hood** | Touch needs a visible target; a keyboard user needs Escape *more* than for the popovers, because this panel is opened by clicking the **map** and so has no button to un-press. |
| **Clicking ANOTHER hood re-pins; an empty-map click is INERT** | Pin-then-browse is the point of the panel. And a *pinned* surface should take a deliberate dismissal — closing on empty-space clicks would let it vanish on the tail of a map drag. |
| **The sparkline rides EVERY view's tooltip**, appended in one wrapper rather than in the six per-view branches | A hood's assessment history is a fact about the neighbourhood, not about the lens you happen to be in — a teaser nobody sees in the view they are in is not a teaser. One wrapper is also a smaller change than six edits that must then stay in step. |
| **A `#hoodmode` toggle chooses where the detail lives, and panel mode REDUCES the hover to the view's headline number** (2026-07-30, Peter) | *"I don't want both the panel and pop up appearing at the same time"* → *"reduce the popup to just the primary metric once you go panel."* **Reduce, not suppress**: the tooltip is the only thing carrying the view's own number, so suppressing it would make panel mode blind in every view and hurt exactly the hood-to-hood browsing the panel exists for. The sparkline and the `click to pin` hint drop out too (the panel already draws the chart). ⚠️ **The reduction is per-view explicit, NOT "row 0"** — services' rows lead with road metres whichever service drives the ramp, so a positional rule would print road supply under a stormwater map; services reads `state.svcDriver`. Full write-up: `docs/UI.md` (2026-07-30), `CONTROLS_MATRIX.md` §3. |
| **The tooltip row carries `click to pin`** | Click-to-pin is undiscoverable otherwise — the same reason the compass exists as visible buttons instead of relying on drag-rotate. |
| **TOUCH: a tap PEEKS, and a second tap on the resulting card commits** (2026-07-31, Peter) | *"i actually want … the panel on mobile to be harder to activate."* A finger cannot hover, so the desktop two-stage gesture (hover to preview → click to commit) **collapsed into the single tap that opens the whole panel** — measured, not assumed. `#peek` restores the missing stage: it carries the same headline `primaryRow` produces for panel mode, and **the second tap lands on a big card rather than on the small polygon that opened it** (Google Maps, Apple Maps and Zillow all go pin → card → sheet). ⚠️ **Gated on `(hover: none)`, NOT on width** — the missing stage is a property of the *pointer*, so it must apply on a touch tablet and must not apply in a narrow desktop window. ⚠️ **The gate is armed on EVERY tap — REVISED the same day, see the row below.** ⚠️ **Every touch interaction here is IDEMPOTENT by design** — a touch tap can deliver `temporalClick` twice (touch event + compatibility mouse event), measured 2026-07-31, so re-peeking the shown hood is a no-op and retap-to-unpin is restricted to pointers. A toggle would have fired at random. |
| **The touch gate stays armed on EVERY tap; only `#hoodmode-btn` disarms it** (2026-07-31, Peter — **revises the row above, same day**) | *"can we keep that behaviour consistent … unless they go and explicitly find that option to keep it open."* The original clause tested `state.hoodMode !== "panel"`, but **committing a peek card is what SETS `hoodMode` to `"panel"`** — so one commit bought permanent one-tap pinning and the stray-tap problem returned from the second hood on. The test is now **`panelByChoice`**, set only by a deliberate press of `#hoodmode-btn`, which separates the mode a user *fell into* from the one they *asked for*. **Tapping a different hood CLOSES the panel** rather than swapping its contents, so the card is never competing with a stale panel above it; an empty-map tap still dismisses only the card. ⚠️ **The lesson is the shape of the bug, not the rule:** the gate keyed off a state that the gated action itself set, so it disarmed itself on first use. |
| **NO hover tooltip on touch — `tooltipFor` returns null under `(hover: none)`** (2026-07-31, CONFIRMED on device) | deck's `getTooltip` runs off a **hover pick**, and a tap synthesises one via the compatibility mouse event, so the full `.tip` box rendered **on top of the peek card**, at the finger, **127px off the right edge** of a 390px screen. ⚠️ **"the card carries the same `primaryRow` line, so nothing is lost" was WRONG, and stood here for one day — see the row below.** ⚠️ **An S81 premise was true but too narrow** — `.deck-tooltip` really never exists on a phone, but the app renders its **own** `.tip` via `className`, which nobody checked. ⚠️ **Found by eye in a screenshot**; every assertion passed, and an id-based overflow table cannot see `.tip` because it has no id. |
| **The card carries the LENS'S FULL READOUT, not its headline** (2026-08-01, Peter — **completes the row above**) | *"when I click on stuff on mobile now the pop up doesn't appear."* Suppressing `.tip` was correct, but it was the only **multi-row** readout a phone had, so every lens collapsed to one line — Services six rows → one, Uses lost its composition bar entirely. `openPeek` now renders `viewTooltip(info, false)`: the same rows the mouse gets, minus the heading `#peek-name` already prints. ⚠️ **This STRENGTHENS the "one definition" rule rather than dropping it** — the shared definition moves from `primaryRow` to `viewTooltip`'s body, so the two surfaces cannot drift in *any* lens instead of only in their headline. The sparkline and *click to pin* hint are deliberately not borrowed: `#peek-go` already invites the panel and the panel draws that chart full-size. ⚠️ **A borrowed body needs its borrowed CSS** — `.mixbar` was scoped `.tip .mixbar` and would have lost `display:flex`, collapsing the Uses bar to nothing visible. ⚠️ **KNOWN AND ACCEPTED: the change lens's card is still ONE LINE** (`+0.16% / yr of its share (13 yr)`, measured 2026-08-01). Not an oversight and deliberately NOT special-cased: that view's body is thin *because* the wrapper was assumed to supply the `% of city base` endpoints, and on touch the panel one tap away supplies them instead. Special-casing it would put wrapper content in the card for one view only. **RULED by Peter, 2026-08-01: leave it.** |
| **`#hoodmode-btn` CONFIRMS a panel you fell into; the label has THREE states** (2026-08-01, Peter — **revises the same-day "honest toggle" note**) | *"change button name and first press to mean yes, keep it open."* Arriving via the peek card sets panel mode with `panelByChoice = false`, so the button already read *"Readout: panel"* and one press turned the mode straight **off** — opting in to sticky one-tap pinning cost **two** presses, on the device where presses are dearest. Now three-way: `popup → panel ✓`, fallen-into `panel → panel ✓` (confirm), `panel ✓ → popup`. ⚠️ **The third label state is load-bearing, not decoration** — without the tick, the mode a user *fell into* and the mode they *asked for* look identical on the button while behaving differently on the very next tap, which is the same class of bug as the S82 self-disarming gate. ⚠️ `applyHoodMode`'s early return learned exactly one exception (re-entering a mode is a no-op *unless* confirming); the body is idempotent for that case, so it re-runs rather than growing a second path. |
| **The card is dismissed by tapping empty map — the OPPOSITE of the pinned panel's rule two rows up** | Deliberate, not an inconsistency. That rule protects a surface you *asked for* from a stray tap or the tail of a drag; this is a cheap preview that costs one tap to bring back, and tapping away is how the same card is dismissed on Google and Apple Maps. |
| **The × is doubled to ≥44px on touch** (2026-07-31, Peter) | *"the x on the panel needs to be twice as big so you can hit it on mobile."* Measured at **20.3 × 21** — comfortable for a cursor and **less than half** the 44px Apple HIG minimum (Material asks 48). Now 44.5 × 44, with `#temporal-name`'s padding widened to match so the hood name never runs under it. Same `(hover: none)` seam, same reason: the pointer changed, not the screen. |
| **Phone: a bottom sheet, near-opaque (0.985)** | Its desktop home is where the control column lives at ≤640px, so staying there would bury `#views`. It covers the legend and both bottom-right pods, which is acceptable in a way covering a *control* is not: it is opened by a deliberate tap and closed by one. **The opacity is not cosmetic** — at the desktop 0.92 those pods' labels read straight *through* the panel's own text. Same lesson as `#about-menu`, one step further: 0.92 is enough over the map, not over other chrome. |

**Two rendering invariants, both of which fail silently** (this is the part worth
re-reading before any edit):

1. **2024 is absent and must LOOK absent.** x is scaled from the **year value**,
   never the array index, and the line is drawn as **runs split at every gap** —
   so 2023→2025 spans twice an ordinary step and no stroke bridges the hole.
   Index positioning would draw it as a normal step; one polyline would bridge
   it; **neither is visible to the eye** on a 13-point series, which is why
   `verify-temporal.js` *measures* the ratio. The band covers the **missing year
   only** (half-step bounds) — shading the whole 2023→2025 run would claim 2023
   and 2025 are missing too. The break is **derived from the year steps**, not
   from a hard-coded `2024`, so January's roll-forward (§0.4) needs no edit here.
2. **The y axis does NOT start at zero, so both endpoints are labelled.** Most
   hoods are well under 1% of the base; zero-basing would flatten 406 of these
   to a straight line and show nothing. Scaling to the series' own range is what
   makes the shape legible, and printing the min and max is what keeps that
   honest. The labels get their **own left gutter** — at `x=0` the max label
   landed on the line, because 2012 is near Downtown's maximum. The sparkline
   cannot carry labels at 28px, so its muted row prints first → last instead.

## 3. Data source

`qi6a-xuwt` — Property Assessment Data (Historical), 2012–2025, 5.5M rows,
carries `neighbourhood_name` natively. **Full 443-hood × 14-year aggregate is one
server-side `$group` query: ~5,600 rows, ~3 s, under 100 kB reshaped** — roughly
1% of the current 7.7 MB payload. Full schema, quirks and the `$limit` trap in
`data/DATA.md` §0.

---

## 4. Phase 0 — THE DATA GATE (blocking)

**`qi6a-xuwt`'s 2024 and 2025 slices are proven incomplete.** Measured
account-by-account 2026-07-28: **2,448 accounts worth $2.93B, across 188
neighbourhoods**, existed in the 2023 slice *and* exist in the current roll, yet
are absent from the 2025 slice. Whole multi-unit buildings vanish together —
Downtown holds 53%, but Magrath Heights is missing 17% of its accounts and
Glenora 15%. **The series cannot be drawn until this is handled.** Full evidence:
`data/DATA.md` §0.

### 0.1 The defect map — ✅ DONE 2026-07-28

`tools/audit_historical_roll_gaps.py`, run against all 14 years. **The defect is
a single event beginning in 2024, not systemic decay. Twelve of fourteen years
are sound.**

| year | roll | defect | rate |
|---|---|---|---|
| 2012 | 337,298 | *untestable* | — |
| 2013–2017 | 346k–389k | 0–2 each | 0.00% |
| **2018** | 396,159 | **14** | 0.00% |
| 2019–2023 | 402k–426k | 0–8 each | 0.00% |
| **2024** | 426,913 | **2,322** | **0.54%** |
| **2025** | 431,706 | **131** *(incremental)* | 0.03% |

**Read the last two rows carefully.** Each year is tested against **N−1**, so the
figures are **incremental, not cumulative**: an account already missing in 2024
cannot be flagged again in 2025. Cumulatively, **~2,448 accounts are missing from
the 2025 slice** — 2,317 of them dropped in 2024 and never returned, plus 131
new. One event, two slices.

**Two detectors, and the first one alone would have lied.** The tool runs both
and reports the union:

- **A — self-audit:** present in N−1 *and* N+1, absent from N. No external source
  needed; catches properties demolished since. **Blind to any dropout that never
  returns.** It reported **5** defects for 2024 where the true figure is 2,321 —
  exactly the failure mode this dataset has. *A run showing ~0 for recent years
  has not shown them clean.*
- **B — current-roll control:** present in N−1 *and* in `q7d6-ambg`, absent from
  N. A property that existed before and exists today cannot legitimately be
  missing in between. Blind to since-demolished properties, which is why A stays.

### 0.2 What this means for the build

- **2012–2023 are usable.** Now tested with the detector that can actually see
  this failure mode, not just the self-audit.
- **2025 is repairable** — splice the current roll, which is complete.
- **2024 is the only irreparable year.** There is no current-roll equivalent for
  it, and the 2,322 missing accounts have no recoverable 2024 value.

**2024 IS OMITTED — decided 2026-07-28 (Peter).** The series is 2012–2023 from
the historical file plus 2025 spliced from the current roll, with an honest gap
at 2024 and the reason stated on hover. **Do not interpolate** — smoothing a
known hole is the failure this project's guard culture exists to prevent.

**This reverses the recommendation this section carried when it was written**
(balanced panel), and the reversal is the reasoning worth keeping:

- **Share-of-base is self-normalizing per year.** Numerator and denominator come
  from the *same* slice, so "what share of Edmonton's base was hood X in year N"
  is well-defined on each year's own complete roll. A constant account universe
  is not what the metric needs — a *complete* one per year is. New towers
  entering Downtown genuinely raise its share; that is the story, not an
  artifact, and a fixed panel would answer the stranger question "what share
  would Downtown be if we pretended these 2,448 properties never existed."
- **The panel trades twelve good years for one broken one.** It would punch the
  same $2.93B hole (53% of it Downtown) into twelve slices that are clean.
- **Flag and uncertainty-band both fail at the display grain** (§8, trap 1). A
  known-incomplete marker or a band is invisible at sparkline size, so the glance
  shows a wrong number regardless of how the pinned panel is annotated. That is
  the same class of error as pinning a per-point maximum that never reaches a
  100 m cell.

Rejected, for the record: **flag** (2), **balanced panel** (3), **uncertainty
band** (4).

### 0.3 Exit criteria

**✅ PHASE 0 IS CLOSED (2026-07-28).** All four criteria met:

| criterion | status |
|---|---|
| defect map across all 14 years | ✅ `tools/audit_historical_roll_gaps.py`, §0.1 |
| 2024 has a decided treatment | ✅ omitted, §0.2 |
| the splice is implemented and tested | ✅ `src/load_temporal.py`, 21 tests |
| a guard refuses to publish a failing year | ✅ `scripts/check_temporal_years.py`, 12 tests, wired into `refresh.yml` |

**The splice must not quietly become a 14-year loop.** 2024 is omitted by
decision, so the year list is deliberately non-contiguous — the guard asserts
that absence rather than treating it as a failure. `publishable_years()` owns the
rule and `structural_checks` enforces it in both directions: a missing year fails,
**and so does an unexpectedly present one**.

### 0.4 The January trap — found while building the guard, and closed

A plain "omit 2024" rule is **not sufficient**, and the reason is worth keeping:

- The current roll covers exactly **one** year. 2025 is publishable *because* it
  is the live year, not because its historical slice is sound — that slice is
  missing 131 accounts.
- So when the roll advances to 2026, **2025 loses its only complete source** and
  a naive splice would quietly fall back to the defective historical copy —
  re-acquiring the defect on a year that renders correctly today, with nothing in
  the pipeline saying a word. Exactly how the original defect survived two
  publication cycles.
- Closed by separating `HISTORICAL_DEFECT_YEARS` (measured: 2024, 2025) from the
  omitted set (derived per live year). Today 2024 is omitted; from January, 2024
  **and 2025** are.

**✅ CLOSED 2026-07-28 — the archive.** `data/temporal_archive.json`, written by
`load_temporal.write_archive`, captures the live year on **every** pipeline run
and is committed by `refresh.yml`. ~74 kB/year against a 7.7 MB payload.

Three rules make it safe:

1. **Freeze.** Only the live year is ever written. A year already captured is
   never rewritten, because once the roll advances we no longer hold a complete
   source for it — any rewrite could only be a silent downgrade.
2. **Capture everything, use it selectively.** Every live year is captured
   (which years turn out defective is not knowable in advance — the whole lesson
   of this dataset), but the archive only **wins** for years in
   `HISTORICAL_DEFECT_YEARS`. Preferring a capture for a year the historical file
   gets right would mix vintages: the roll carries titles created after
   publication (~8,200 accounts today), so that year would read measured-later
   than its neighbours and put a step in the series that is an artifact of
   sourcing, not of Edmonton.
3. **Automatic.** It runs on ordinary weekly runs, not as a January chore — a
   step that must be performed once, at a date months away, is a step that does
   not happen.

Verified by simulating the roll-forward: with the archive, live-2026 publishes
2012–2023 + **2025** + 2026 and 2025 is served `source="archive"`; without it,
2025 is gone. The guard fails if an archived year is ever served from the
historical file instead.

---

## 5. Phases 1–4 — the build (ordinary work, once the gate passes)

| phase | deliverable | notes |
|---|---|---|
| ~~**1**~~ ✅ | ~~`src/` module → hood × year table~~ **DONE 2026-07-28** — `src/load_temporal.py`. Unmatched names are flagged + reported and **kept in the denominator** (share-of-base means an unrenderable hood is still real value). | `ARCHITECTURE.md` conventions: independently runnable, configurable paths, structured output. **No silent drops** — 443 historical hood names will not align cleanly with today's boundaries; route through the `check_unmatched_names.py` policy. |
| ~~**2**~~ ✅ | ~~compact JSON → `web/data/`~~ **DONE 2026-07-28** — `export_temporal_web` → `web/data/temporal.json`, **406 hoods × 13 years, 89.2 kB** (budget 100 kB; ~41 kB gzipped). Integer-scaled: shares in ppm, values in **$1k units** — measured, not chosen by taste ($0.1M would put the smallest hood out by 74%). **The 2024 gap rides in the `years` array, so plot against year values, never the array index.** |
| ~~**3**~~ ✅ | ~~render in `/full/`~~ **DONE 2026-07-29** — sparkline in `tooltipFor` (via a wrapper over the per-view `viewTooltip`), plus the `#temporal` click-to-pin panel. Design settled in §2. `#temporal` is in `CHROME_IDS`, so the label sweep dodges it. Gated `\|\| !FULL_BUILD` beside a defensive fetch: no file ⇒ no lens, everything else still works. | **`web/data/temporal.json` ships to the PUBLIC root even though the public build never fetches it** — `/full/` is `index.html` alone under `<base href="../" />`, so `./data/temporal.json` resolves to the root copy. Verified in the *built* tree (public root: zero requests; `/full/`: 200, no 4xx), not assumed — the same failure shape as the `styles.css` 404 risk. |
| ~~**4**~~ ✅ | ~~guard + `refresh.yml` wiring~~ **DONE 2026-07-28** (landed early, with Phase 0) — `scripts/check_temporal_years.py`. | the anchor-band idiom of `check_value_anchors.py`: bands not equalities, direction-aware, missing inputs skip. Must sit **before** the status-manifest step, or a failure bumps the heartbeat and goes invisible. |

---

## 6. Locked decisions

| decision | rationale |
|---|---|
| **Normalize as share of the citywide assessment base — NOT CPI-deflated dollars** | The mill rate is a **residual** (levy ÷ total base), so a citywide revaluation is fiscally neutral; a hood's burden moves only when its assessment diverges from the city average. CPI-deflating answers a purchasing-power question, not a tax-share one. Share-of-base is unit-free, needs no deflator and no vintage to maintain. |
| **Reserve constant dollars for raw $/acre levels across years** | The one place a deflator is legitimate. And on the cost side later, city inputs track a **Municipal Price Index**, not CPI — CPI there is the wrong index, not merely imprecise. |
| **Name the denominator in the UI** | Downtown is **3.22% of the total base** but **9.30% of the commercial base** (2025). Public reporting quotes the second kind. Publish 3.22% beside an article saying 5.2% and the project looks wrong when it is not. Showing both is probably right. |
| **Framing is descriptive only** | Share-of-base line + the sourced driver (office vacancy). No "downtown is dying", no "the rest of the city subsidizes downtown". The reader draws the conclusion. |
| **`/full/` only, for now** | See §1. |
| **Do NOT use the `NONRES MUNICIPAL` class** | 1–2 accounts; its share swings 30–53% on noise. |
| **The metric is ASSESSED VALUE, not revenue** (2026-07-28) | Value reaches **2012**; revenue needs historical mill rates (`pwis-wc4c`, 2014 onward) so it would start 2014 *and* inherit every class-differential caveat. Two years of series and a whole caveat class, for a number that moves with the same shape — the mill rate is a residual, so revenue is value times a factor council chose. Revenue as a second panel line stays available later. |
| **The SPARKLINE plots share of the TOTAL base; the pinned panel ALSO states the commercial-base share** (2026-07-28) | Satisfies "name the denominator" above without putting two lines in a 14-point sparkline, which is past what that form carries. The commercial figure is what public reporting quotes (CBC/council ~5.2%), so it has to be reachable — but as a labelled number, not a second series. |
| **No `$/acre` line — share only** (2026-07-28) | The one place a deflator would be legitimate (row 2 of this table), deliberately not taken yet. It would cost a CPI series *and* a stated justification for dividing 14 years of moving boundaries by a **current** area. Share-of-base needs no deflator, no area assumption, no vintage — so Phase 0 is the only thing in front of the build. |
| **2024 is OMITTED** (2026-07-28) | Full reasoning in §0.2, including why this reversed the balanced-panel recommendation. |

## 6b. Round 2 — the change lens (SHIPPED 2026-07-30)

The lens in §1–§6 answers **one hood at a time**. Round 2 asks the same data for
**all 406 at once**: *how fast did each neighbourhood's share of the assessment
base move?* Peter, 2026-07-30: *"what I want is like, timelines options, for how
much each hood has changed on average over time… and spike chloro map
eventually."*

**Where it lives.** A **sub-mode of the Money view** (`#moneymode`: Current /
Change over time), not a sixth `#views` button — Peter's call. Internally it is
the view `"change"`, exactly the shape `glass` and `infill` already use: a
render-mode whose parent's `#views` button stays active. Its window picker
(`#chgwindow`: Since 2012 / Since 2019) follows the `#devwindow` idiom.
**PUBLIC as of 2026-07-31** (promoted from `/full/`-only — `DECISIONS.md`
2026-07-31). It was *doubly* gated on `FULL_BUILD` **and** a loaded
`temporal.json`; the build flag is gone and **the data gate remains**, which is
the half that actually matters — the controls still cannot offer a lens whose
data is absent, and both builds now degrade identically if the file is missing.

**No pipeline work.** Derived client-side from the already-loaded
`temporal.json`. Switching windows recomputes from a per-window clamp cache and
**never refetches**.

### The metric, and the two things measurement changed

| decision | rationale |
|---|---|
| **Relative change in share-of-base** (Peter, from the §10 gate) | pp change is defined everywhere but does not separate — median hood −0.032 pp against Downtown −1.791 pp. See `DECISIONS.md` 2026-07-30. |
| ⚠️ **COMPOUND, not arithmetic** — `(last/first)**(1/years) - 1` | **Measured during the build, and it reversed the obvious implementation.** The arithmetic form `(last/first - 1)/years` is **unbounded above** (observed max **+2,076%/yr**, from hoods emerging off a near-zero 2012 base) while bounded below at −7.7%/yr. Its p95 arms come out **108× apart** (+485%/yr gaining vs 4.5%/yr losing), so a diverging ramp would be owned by a handful of new subdivisions and every ordinary hood would sit invisibly at the dark centre. Compounding bounds it (max **+54%/yr**, arms **6×** apart) and is near-symmetric under doubling/halving, which is what a diverging map needs. It is also simply what *"average annual change"* **means** for a quantity that compounds. |
| ⚠️ **BOTH degenerate endpoints are holes, not numbers** | The 45 no-2012-baseline hoods were known from the gate. **The mirror case was not**: one hood (`MILL WOODS GOLF COURSE`) *ends* at zero share, where the compound rate evaluates to exactly −1 and printed **`-100.00% / yr`** — arithmetically true, descriptively false (it did not shed 100% every year; it fell out of the base once). Both ends are now off-scale grey with distinct reasons. |
| **Flat choropleth, never spikes** (Peter's call) | A prism cannot have negative height and hoods moved both ways. Reuses `infillColorAt` — the in-repo precedent for a signed metric — teal = gained share, orange = lost. Per-arm p95 clamps, like `infillStats`, because even compounded the arms are ~6× apart. |
| **Endpoints, not a fitted slope** | rho **+0.959** over all 406 (`ANALYSIS_BACKLOG.md` §10). A hump needs a *second* number — peak value + peak year, which the pinned panel already gives. |

### ⚠️ Two invariants that fail silently here

1. **ANNUALISE OVER YEARS ELAPSED, NEVER OBSERVED INTERVALS.** The 2024 gap
   makes them differ — the long window spans **13 years** but holds only **12
   intervals** — so annualising over intervals inflates every hood's rate ~8%
   (Downtown −3.28%/yr vs −3.55%/yr) with **nothing on screen looking wrong**.
   Same class as index-vs-year positioning in the chart (§2). `verify-change.js`
   asserts it **first**, and recomputes from the raw served file so the app
   cannot satisfy the check by agreeing with itself.
2. **The grey hoods must never read as set-aside land.** They are its opposite:
   new-growth areas that held none of the assessable base in the first year,
   which is *why* no relative change exists for them. The hover names the year
   (`No 2012 baseline — held none of the assessment base that year`) and the
   legend swatch says the same. Reading them as protected land inverts the story
   the map exists to carry.

**Also caught in build, and worth keeping:** the change tooltip originally
printed the endpoint pair itself, which `tooltipFor` then printed *again* in the
shared sparkline footer — the same "two dense blocks competing" objection that
produced the panel-mode reduction. The change hover is now **one line**; the
footer carries the endpoints.

Regression net: **`tools/profiling/verify-change.js`, 36 checks.**

## 7. Open decisions

**None — all four closed 2026-07-28 (Peter).** Metric, denominator, per-acre and
the 2024 treatment are now rows in §6. The settled first cut is exactly the one
§7 suggested: **share of citywide base · value not revenue · total not per-acre ·
2024 omitted.**

What remains before Phase 1 is *work*, not decisions: the splice and the guard
(§0.3).

## 8. Traps already paid for

- **Validate at the display grain.** Recorded in `FINDINGS_lot_dedupe.md` §4.3
  and re-learned twice since. A per-point maximum that never survives to a
  100 m cell is not a fact about the map.
- **Aggregates can be confidently wrong.** This lens's own finding was misread
  **twice** from aggregates — a class-level split said "80% genuine
  revaluation", a value-of-vanished-accounts sum said "98% vanishing" — and the
  account-level join produced the opposite answer both times. **When a series
  has a cliff, join at the entity level and check a second source for the same
  period before interpreting the shape.**
- **A cause named in a handoff is a hypothesis.** Reproduce the symptom *and*
  re-measure the stated cause before acting on a backlog item.
- **The two datasets disagree on column names** — historical uses
  `neighbourhood_name`, the current roll uses `neighbourhood`. And Socrata's
  default page size is 1,000: always pass `$limit` or results silently truncate.

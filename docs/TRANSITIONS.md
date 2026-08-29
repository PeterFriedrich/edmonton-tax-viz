# TRANSITIONS — when to animate between map states

Reference for adding a metric, a lens, or a control that swaps what the map
draws. **Nothing here is implemented yet** (2026-08-29): the map hard-cuts on
every swap, and the only motion on the page is chrome (`transition: background
0.12s` on the buttons, the loading overlay's 350ms fade). This doc exists so the
first transition that ships is argued rather than defaulted.

Naming follows the standing docs (`UI.md` is the build log, `CONTROLS_MATRIX.md`
is the state space); this is the rule set.

---

## 0. The principle

**Animation implies a relationship. Only animate where that implication is
true.** Heer & Robertson, *Animated Transitions in Statistical Data Graphics*
(IEEE InfoVis 2007), is the source: motion preserves **object constancy** — the
reader's belief that "this prism is that neighbourhood" survives the movement —
and it is worth having exactly when identity does persist. Where the *meaning*
of the encoding changes underneath, motion asserts a continuity that does not
exist.

This is the same class of rule the project already applies to numbers: an
unnamed denominator makes a correct figure read as wrong (`SPEC_temporal.md`
§6), and the institutional band refuses to draw a value it cannot support
(`DECISIONS.md`, 2026-08-18). A tween between two unrelated quantities is that
failure in the time dimension.

### The halfway-frame test

**Pause the animation midway. Does that in-between state mean anything real?**
If yes, animate. If no, cut or cross-fade. Every rule below is a corollary, and
when a new case is not covered, this is the test to run.

---

## 1. The rules

**1. Tween when identity persists and only the value changes.** Same
neighbourhoods, same metric, same unit — the extrusions *are* the same objects,
so a height tween is honest. The halfway frame is a real intermediate value.

**2. Cut or cross-fade when the encoding's meaning changes.** A different
quantity on a different scale has no real path between the two endpoints.
Cross-fade opacity out/in with an **independent height reset** — never
interpolate height or position between mismatched values. The halfway frame of
a dollars→counts tween is a number in no unit at all.

**3. Same unit, different metric — decide on whether a real quantitative
relationship connects them**, not on the shared axis. A shared scale makes a
tween *legible*, not *true*. Where one metric is a component of the other
(subset ↔ superset), the relationship is real and a tween is honest. Where two
metrics merely happen to be denominated the same way, cross-fade.

**4. Filtering, sorting and re-aggregating the SAME metric are always safe to
animate.** The classic object-constancy case. The reader's mental model
survives, and the halfway frame is a real partial state.

**5. Encoding-only changes (ramp, colour adjust) are always safe**, and are
colour-only by construction — no geometry moves.

---

## 2. Applied to our controls

| swap | rule | verdict |
|---|---|---|
| Ramp / `#coloradj` | 5 | **Tween** (colour). Same data, same geometry. |
| Revenue ⇄ Residential $ ⇄ Non-res $ | 3 | **Tween.** See below — these are subsets, not neighbours. |
| Revenue/Residential/Non-res → **Value** | 2 | **Cross-fade.** Different quantity, 55× scale. |
| Per acre ⇄ per lot acre | 3 | **Flag.** The genuine gray area here — see below. |
| View swap (Money → Services → Uses …) | 2 | **Cut.** Different lenses, different geometry entirely. |
| A future year stepper | 1 | **Tween — but read §4 first.** |

### The three revenue metrics are subsets, and that settles rule 3 for them

`revenue_per_acre`, `res_revenue_per_acre` and `nonres_revenue_per_acre` share
`elevationScale: 0.033` **deliberately**, so the bars read as comparable subsets
of the total — the code says so at each config, and `DECISIONS.md` (2026-07-16,
2026-08-01) locks residential and non-residential as decompositions of the levy,
not independent measures. So this is not the "merely both in dollars" case rule
3 warns about: residential dollars *are* part of total dollars. The halfway
frame is a real intermediate share. **Tween.**

`value_per_acre` is the opposite case despite also being dollars — assessed
**stock** vs annual **levy flow**, on `elevationScale: 0.0006`. Nothing connects
them. Cross-fade.

### The denominator toggle is the real gray area

Same numerator, same geometry, different denominator. Object constancy is
perfect, which argues rule 4 — but the halfway frame is a height computed
against *neither* neighbourhood acres nor lot acres, i.e. no denominator that
exists. Unresolved, and mechanically blocked anyway (§5). Cross-fade if forced
to choose today.

### Any future non-dollar metric cross-fades

A metric whose unit is not municipal levy dollars — counts, rates, indices,
anything of the kind — **cross-fades with an independent height reset**, never a
direct height tween. There is no real quantity connecting dollars to a count,
so every frame in between would be meaningless. This is the default for new
metrics; rule 3's tween is the exception that has to be argued.

---

## 3. Cross-fading in practice

Rule 2 says cross-fade. This is what that means concretely, and it is the side
of the rule most likely to be got subtly wrong.

### Height resets instantly. Only opacity moves.

**Never fade opacity and tween height at the same time.** The eye still tracks
"this prism grew into that one" underneath a fade — the same false relationship
a direct tween asserts, just harder to notice and therefore worse. The incoming
stack must already stand at its **final** height as it fades in.

This costs nothing today only because height cannot animate here at all (§5).
That is an accident of the engine, not a guarantee — the rule is written down so
it survives the day someone lifts that constraint.

### The three forms, in order of how unrelated the lenses are

1. **Simultaneous** — old fades out while new fades in. Fastest, feels
   responsive. Muddy at the midpoint, because both stacks are semi-visible at
   once. ⚠️ **That midpoint is at its worst here**: every lens draws the *same*
   406 neighbourhood polygons, so a simultaneous fade overlaps two translucent
   copies of one geometry at different heights, not two different-looking maps.
   Reserve it for genuinely adjacent lenses.
2. **Sequential** (fade out → brief hold → fade in) — **the default for lens
   switching.** The empty beat makes the "these are different things" boundary
   explicit. A lens switch is a deliberate context change, not a data stream, so
   the small latency cost buys the right reading. A continuous control (a time
   slider) would want form 1 instead.
3. **Fade through a neutral beat** — dip to a flat, uniform hood plane, then
   rise into the new metric. Strongest possible "no relationship" signal, and
   overkill for most swaps. Reach for it only if readers are actually misreading
   cross-fades as continuity. ⚠️ Note this is **not** a dip to parcels — the
   analysis unit is the neighbourhood by locked decision (`DECISIONS.md`,
   Phase 1). The neutral plane already exists as `GLASS_PLANE_COLOR`, drawn by
   `dev-neutral-plane` and `glass-plane`, so this form is cheaper here than it
   would normally be.

### Land the UI signal with the fade, not before it

Pair the visual cross-fade with the labelling change — legend, title, blurb — so
they land at the **same moment**. The mode switch reads clearly when the words
confirm "context changed" exactly as the layer does.

⚠️ **Today they would not.** A lens swap rewrites the title, blurb, legend label
and legend endpoints from the `METRICS` config synchronously on click. Add a
250ms fade and the copy would assert a new context a quarter-second before the
map showed one — the labelling would be describing a map still fading out.
Whatever drives the fade has to drive the copy swap too.

### ⚠️ This is not a props change — what it actually costs

Measured 2026-08-29 against the vendored build, because the obvious
implementation does not exist:

- **`opacity` is NOT a transitionable deck.gl prop here.** The bundle does carry
  `uniformTransitions` machinery, so grepping for it is misleading — but **no
  numeric uniform prop opts in** (`opacity` and `elevationScale` both lack the
  flag; every `transition: true` in the build is on an accessor-backed
  attribute). So a fade cannot be declared. It must be driven — a rAF/timer loop
  stepping opacity and re-issuing `setProps({ layers })` — or done by animating
  the **alpha inside `getFillColor`**, which *is* attribute-backed and does
  transition. The second is free but per-layer, and covers no `PathLayer` or
  `TextLayer` without its own `getColor`.
- **Both stacks have to be alive during the fade.** `buildLayers()` returns only
  the current view's stack, and ~20 sites call
  `overlay.setProps({ layers: buildLayers() })`, so the outgoing layers are
  removed the instant the swap lands. Cross-fading means returning a union for
  the duration.
- **⚠️ A naive union collides on ids.** `hoodHoverLayer()` (`hood-hover`) and
  `labelLayer()` (`hood-labels`) are in nearly every view's stack, so both
  halves of the fade would carry the same layer ids. The shared chrome has to be
  hoisted out of the fade and issued once.
- **⚠️ The outgoing stack must be made unpickable.** An **alpha-0 fill still
  picks in deck.gl** — measured in this repo, not assumed (see the
  `deviationBandLayers` comment in `web/index.html`). A fading-out lens would
  otherwise keep answering hovers, and a tooltip from the lens you just left is
  a silent-correctness failure, not a cosmetic one.

---

## 4. ⚠️ A year tween must not bridge the gap

The most likely future rule-1 case is a year stepper on the assessment series,
and it carries a trap specific to this project.

**The published series is 2012–2023 + 2026 — deliberately non-contiguous, two
years wide.** 2024 and 2025 are both omitted by decision (`SPEC_temporal.md`
§0), and `DECISIONS.md` (2026-07-29) locks the invariant that **2024 must LOOK
absent**: the sparkline scales x from the *year value*, never the array index,
and draws the line as runs split at every gap so no stroke bridges the hole.

A naive year tween would animate straight through 2024–2025, rendering two full
years of smooth motion across data that does not exist — destroying, in the
map, the exact thing the chart is built to preserve. **Step across the gap;
never tween across it.** The gap is derived from the year steps rather than
hard-coded, so the same derivation is available to any stepper.

(For the record: "revenue 2023 → 2024" is the natural way to describe rule 1,
and it is the one pair in this repo that cannot be drawn.)

---

## 5. ⚠️ What the engine will and will not do

Rules are useless if the renderer cannot honour them. Measured 2026-08-29 on
deck.gl 9.0.38 (`web/vendor/`, which does include `AttributeTransitionManager`):

- **Colour transitions are nearly free.** `metric-extrusion` keeps a stable
  layer id across every Money swap and already declares `updateTriggers` for
  `getFillColor`/`getElevation`, so a `transitions: { getFillColor: 250 }` prop
  is the whole change. Same for `getColor` on `top-edges`.
- **⚠️ Height transitions are NOT currently available, for two independent
  reasons.** `elevationScale` is a layer *uniform*, and **no numeric uniform
  prop opts into transitions in this build** — the bundle carries
  `uniformTransitions` machinery, but every `transition: true` in it sits on an
  accessor-backed attribute, so `elevationScale` (and `opacity`, §3) cannot be
  interpolated. A Revenue→Value swap would collapse the scene 55× instantly
  while the raw values slid underneath. And `top-edges` is a
  `PathLayer` whose *data* is rebuilt by `topRings()` at the new heights, so the
  roof outlines would snap while the prisms were still moving. Both are fixable
  by baking the scale into `getElevation` and setting `elevationScale: 1`, but
  that also touches label lift in `labelLayer` — it is a render-path change, not
  a prop.
- **⚠️ Motion costs the verify suite.** ~8 `verify-*.js` and ~20 `shot-*.js`
  scripts sample pixels immediately after a click and would capture
  mid-transition frames. Any transition ships with a settle wait in those
  scripts (`tools/profiling/`).
- **`prefers-reduced-motion` is already honoured** in `web/styles.css` for the
  overlay and spinner. Every new transition extends that block. Not optional.

---

## 6. Adding a metric — the checklist

1. Is the new metric a **component** of an existing one, in the same unit? → may
   tween. Anything else → cross-fade with an independent height reset.
2. Run the **halfway-frame test** and write the answer into the metric's config
   comment, so the next person inherits the reasoning rather than the verdict.
3. If it tweens on height, confirm `elevationScale` is **identical** to the
   metric it tweens from. If not, §5 applies and it cross-fades regardless of
   what rule 1–5 says.
4. Extend the `prefers-reduced-motion` block.
5. Add a settle wait to any `shot-*`/`verify-*` script that clicks the control.

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
| A future year stepper | 1 | **Tween — but read §3 first.** |

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
exists. Unresolved, and mechanically blocked anyway (§4). Cross-fade if forced
to choose today.

### Any future non-dollar metric cross-fades

A metric whose unit is not municipal levy dollars — counts, rates, indices,
anything of the kind — **cross-fades with an independent height reset**, never a
direct height tween. There is no real quantity connecting dollars to a count,
so every frame in between would be meaningless. This is the default for new
metrics; rule 3's tween is the exception that has to be argued.

---

## 3. ⚠️ A year tween must not bridge the gap

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

## 4. ⚠️ What the engine will and will not do

Rules are useless if the renderer cannot honour them. Measured 2026-08-29 on
deck.gl 9.0.38 (`web/vendor/`, which does include `AttributeTransitionManager`):

- **Colour transitions are nearly free.** `metric-extrusion` keeps a stable
  layer id across every Money swap and already declares `updateTriggers` for
  `getFillColor`/`getElevation`, so a `transitions: { getFillColor: 250 }` prop
  is the whole change. Same for `getColor` on `top-edges`.
- **⚠️ Height transitions are NOT currently available, for two independent
  reasons.** `elevationScale` is a layer *uniform*, not a per-vertex attribute,
  so deck.gl cannot interpolate it — a Revenue→Value swap would collapse the
  scene 55× instantly while the raw values slid underneath. And `top-edges` is a
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

## 5. Adding a metric — the checklist

1. Is the new metric a **component** of an existing one, in the same unit? → may
   tween. Anything else → cross-fade with an independent height reset.
2. Run the **halfway-frame test** and write the answer into the metric's config
   comment, so the next person inherits the reasoning rather than the verdict.
3. If it tweens on height, confirm `elevationScale` is **identical** to the
   metric it tweens from. If not, §4 applies and it cross-fades regardless of
   what rule 1–5 says.
4. Extend the `prefers-reduced-motion` block.
5. Add a settle wait to any `shot-*`/`verify-*` script that clicks the control.

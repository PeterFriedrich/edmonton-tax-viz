# PROPOSAL — the lens registry

**Status: PROPOSED, not approved. Nothing built.** Written 2026-09-05 (S140,
Opus 5) at Peter's ask, after the architecture audit
(`docs/FINDINGS_frontend_architecture_verdict.md`) named this as the one
refactor with a real payoff — and as the third re-open trigger on the
`DECISIONS.md` 2026-09-05 "stay one file" decision.

⚠️ **This buys maintainability, not a single user-visible change.** Every step
is verified by the render being *identical*. That is the honest pitch; judge it
on that.

⚠️ **Do not start this and the fix-in-place PR at once.** That PR (tail banners,
named `boot()`, `type="module"` + shim) is small, verifiable and unrelated. Land
it first so a regression here has a clean baseline behind it.

---

## 1. The problem, measured

**Adding or changing a lens means editing 28 symbols that branch on lens
identity.** Measured 2026-09-05 over `web/index.html` (`state.view === "…"` /
`v === "…"` comparisons, via `tools/codemap.py`'s own extractor):

| symbol | branches | lines | what it decides |
|---|---:|---:|---|
| `applyView` | **50** | 244 | everything: control visibility, async fetches, chrome, order |
| `refreshLegend` | 8 | 248 | the legend |
| `buildViewLayers` | 8 | 303 | the deck.gl layer stack |
| `viewTooltip` | 7 | 338 | hover/tap content |
| `primaryRow` | 7 | 81 | the tooltip's headline row |
| `legendGradient` | 6 | 79 | the ramp |
| `syncDevControls`, `syncPrismRow`, `labelZ`, `syncColorAdjust`, `revenueLens`, … | 1–4 each | — | 22 more |

The top six hold ~86 of the ~100 branches; the tail is 22 symbols with one or
two each — which is worse, not better, because those are the ones nobody
remembers to update.

**The project already knows this and has written the checklist down** — in the
`the Lab` banner comment:

> TO ADD AN EXPERIMENT: write its view the way any other view is written (a
> branch in `buildViewLayers`, `primaryRow`, `viewTooltip`, `refreshLegend`, and
> a `VIEWS` entry), then add one line here.

That comment names **five** places. The real number is 28. A checklist that
undercounts by 5× is the defect, and it is why "lens work touches everything"
is the felt experience of this file.

⚠️ **Note where these live.** `applyView` and `refreshLegend` sit under the
*"citywide budget panel (EXPERIMENTAL, full build only)"* banner, and
`viewTooltip`/`primaryRow` under *"Money's revenue panel"*. The dispatchers are
filed under the panels that happened to be written around them. The
fix-in-place PR's truthful banners partly address this; this proposal addresses
why it happened.

## 2. What already exists — and works

`VIEWS` (lines 1241–1345) **is already a registry**: one entry per lens with
`title`, `blurb`, `opacity`, and `indBlurb` for development's industrial cut.
`applyView` already consults it (`VIEWS[v].opacity`, `VIEWS[v].blurb`).

**So this is not a new pattern — it is finishing one the project chose and
proved.** The proposal is to move the remaining per-lens decisions into the
same table, field by field, and delete each branch as its field lands.

## 3. The constraint that shapes the design

⚠️ **`applyView` is not a switch. It is an ordered pipeline, and the order is
load-bearing.** Three invariants, each documented in the code because each was
a shipped bug:

1. **Chrome before layers.** `#title` text *and* `refreshLegend()` must be final
   before `buildLayers()`, because the label sweep measures their live bounding
   rects to cull labels. Getting this wrong twice: `SPRUCE GROVE` painted into
   Development's taller blurb; `DEVON` painted over by Uses' taller legend
   (fixed 2026-08-08).
2. **Control sync after the await.** `syncAmenityControls` must run *downstream*
   of `await ensureGridData()` — it reads column flags that do not exist until
   the grid file lands, and running first hides the rows permanently.
3. **Re-entrancy.** Every `await` is followed by `if (state.view !== v) return;`
   — four of them. A user switching views mid-fetch must not have the outgoing
   lens finish rendering over the incoming one.

**Therefore: NOT `lens.render()`.** A registry where each lens owns its own
orchestration would let a lens reorder those phases, and the failure is silent —
a label painted under chrome, not an exception. **The kernel keeps the phase
sequence. Lenses contribute data and pure functions to named phases, and never
call each other or the map.**

## 4. The design

`applyView` becomes an explicit, readable phase list (~40 lines instead of 244),
each phase consulting the registry:

| phase | kernel does | registry field |
|---|---|---|
| A commit | `state.view = v`, `#views` button | `parentBtn` (glass→money, infill→development) |
| B controls | show/hide panel sections | `controls: { layers, denom, prism, … }` — declarative booleans/predicates |
| C ensure | `await`, then the re-entrancy guard | `ensure: async () => …` (roads, zoning, grid, dev grid) |
| D chrome | write `#title-h` / `#title-p` | `title()`, `blurb()` — thunks, so metric/denominator-driven views stay dynamic |
| E legend | call it | `legend()` / `gradient()` |
| F layers | `overlay.setProps` | `layers()` |
| G post | colorAdjust, pinned panel, peek | `postSync` (rare) |
| — tooltip | `viewTooltip` shell | `tooltip(p)`, `primaryRow(p)` |

A lens entry ends up as one object — and adding a lens becomes **one entry plus
one `#views` button**, which is what the Lab comment always claimed.

## 5. Migration order — pure fields first, orchestration last

Each step is **independently shippable, independently revertable, and verified
by an identical render.** Ordered by rising risk:

1. **`title()` / `blurb()`** — kills `applyView`'s two ternary chains (~14
   branches). Purely textual; the existing `VIEWS` already holds the static half.
2. **`legend()` / `gradient()`** — `legendGradient`'s 6 branches, self-contained.
3. **`layers()`** — `buildViewLayers`' 8 branches. Mechanical: each
   `if (state.view === X) { … return [...] }` becomes `VIEWS[X].layers()`.
4. **`tooltip()` / `primaryRow()`** — 14 branches across two symbols.
5. **`controls`** — the show/hide pile. ⚠️ **Highest risk and last of the
   visible work:** it is shared DOM, so per `docs/CONTROLS_MATRIX.md` it drives
   **desktop and mobile together**. Read that doc before touching it.
6. **`ensure()`** — the async phase. The `await` and the re-entrancy guard stay
   in the kernel; only the fetch body moves.

Then, and only then, delete the dead branches from the 22-symbol tail.

## 6. Verification

Same discipline as stage 1 (the CSS extraction), which is the precedent for
"large mechanical move, verified by identity":

- **Per step:** the 65 `tools/profiling` scripts, **run one at a time** (this
  box manufactures failures under concurrency), plus pixel-identical screenshots
  vs master at 1440px and 390px, **both builds** (`?build=public` and `/full/`).
- ⚠️ **Known gap, from the audit (findings §5):** the harness verifies *that the
  page still works*, not *that the seam is right*. It cannot catch a lens
  reading another lens's state. Steps 1–4 are mechanical enough that identity is
  a real check; **step 5 is where a reviewer is required, not a script.**
- `tests/test_codemap.py` and the `PostToolUse` hook keep `CODEMAP.md` honest as
  ranges move — no manual step.

## 7. What it unlocks

- **The add-a-lens checklist becomes true**, and the Lab comment can be corrected
  to match reality instead of undercounting by 5×.
- **Per-lens ES modules fall out for free.** Once a lens is one object with no
  peer references, `export const money = { … }` is a file move, not a refactor.
  This is exactly the third re-open trigger recorded in `DECISIONS.md`
  2026-09-05 — so **this proposal is the only route by which the split becomes
  the right call**, and it earns that on its own merits first.

## 8. Risks, honestly

- **No user-visible payoff.** Every step's success criterion is "nothing
  changed." If the appetite isn't there, that is a legitimate no.
- **It is not small.** Six steps across ~1,300 lines of dispatcher, one PR each.
  Stage 1 moved CSS with *zero* coupling; this moves code with real coupling.
- **Step 5 touches shared desktop/mobile DOM** — the one place the audit found
  actual shipped regressions (three cross-lens leaks, all in shared gates).
- **Half-done is worse than not started**: a registry consulted by some phases
  and bypassed by others is harder to reason about than 28 honest branches. If
  it starts, steps 1–4 should land.

## 9. What I am NOT proposing

The file split (decided against, `DECISIONS.md` 2026-09-05), a bundler or
framework (Level 1, SOUND), touching `state` (already read-only against every
lens), or any change to the pipeline, data contract or CI.

## 10. The decision

**Peter's call, and it is a yes/no on appetite, not on technique:** is ~six PRs
of identical-render refactoring worth a true add-a-lens checklist and a free
split later?

- **Yes** → land the fix-in-place PR first, then step 1 alone, and re-judge on
  the real diff before committing to 2–6.
- **No** → say so and I will log it, so this is not re-proposed each time a lens
  edit touches five files. The 28-branch measurement stays useful either way:
  it belongs in the Lab comment as the corrected checklist.

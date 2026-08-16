# Controls & Lens Combinations — current state

Authoritative **snapshot** of every view × control combination as the app
actually behaves today (rewritten 2026-07-25 against `web/index.html`, with every
row **probed on the live site in both builds** — not inferred from reading). This
is the map to reason about **regrouping** the controls (desktop grouping is
shared DOM → it drives the mobile layout too; see `docs/MOBILE_USABILITY.md`).

- This doc = the current *state space* (what shows when, what gates what, what's
  still odd).
- `docs/LENS_INVENTORY.md` = the user-facing *catalogue* (what each lens is, what
  it offers, combination counts). Same source, different question.
- `docs/UI.md` = the chronological *build log* (why each feature was built).
- §5 holds what's still weird **after** the regroup; §7 is the locked decision
  record for the regroup itself.

---

> **Out of scope for this matrix — view-independent camera chrome.** The
> bottom-left **Center 2D / Center 3D** framing buttons (`#botleft`/`#viewbtns`,
> added 2026-07-24) and the **compass row** above them (`#compass`: `#rot-ccw` /
> `#tonorth` / `#rot-cw`, added 2026-07-25) move the *camera*, not the data — they
> show in every view and gate nothing, so they sit outside the tier system below.
> See `docs/UI.md` "Camera framing buttons" + "Compass with rotation arrows" and
> `DECISIONS.md` 2026-07-24 / 2026-07-25.

## 1. The three tiers

Every control is one of three tiers, and since the regroup the **on-screen stack
follows that order** — set with CSS `order:` on `#controls`, not DOM order
(`web/index.html` L36–38):

- **Tier 1 — WHAT am I looking at** (the view): `#views`, `order: 1`. Also the
  largest type on screen since 2026-07-25 (14px, vs 12.5px `#toggle` and 11.5px
  modifiers) so the rendering matches the tier — it previously tied for smallest.
- **Tier 2 — WHICH variant** of the current view: `#toggle` (`order: 2`, Money's
  metric picker) plus everything in `#layers`. **`#toggle` is itself two-level
  since 2026-07-26** — a quantity row (Revenue | Value) with a second row nested
  under whichever quantity is selected. It is the only control that nests
  *within* a tier, and it is not a new tier.
  **Since 2026-08-01 BOTH quantities have a row 2, and they are different kinds
  of thing:**
  - **Revenue → `#revcut`** (Total | Residential | Non-residential): genuine
    *subsets*, mirroring the data (`levy == res + nonres + farmland`).
  - **Value → `#moneymode`** (Current | Change over time): two *lenses* on the
    same quantity, not a decomposition. It sits here because the change lens
    measures movement in each hood's share of the **assessment base** — the
    value side. In the Options panel it was offered under Revenue too, where it
    read a column Revenue does not own.

  Exactly one row 2 is visible at a time; `syncMetricButtons` owns both.
- **Tier 3 — HOW it's drawn** (presentation modifiers): `#coloradj` — the only
  one left since `#lens` was removed 2026-07-26.
- **Out of the tier flow:** the `#a11y` **Display** popover (colour ramp +
  neighbourhood labels + the river/ring-road reference layer), bottom-right.
  This popover is where **view-independent map furniture** lives — controls that
  apply identically in every view. That is the test for putting something here
  rather than in the Options panel, whose contents are per-view.
  ⚠️ **`#a11y` and `#about` are a STACK in one bottom-right column** (`bottom:
  40px` and `68px`, both buttons 26px), and both menus open **upward into the
  same strip** — which is why opening either closes the other. `#a11y-menu`'s
  offset is `calc(200% + 8px)`, clearing **the pod above it**, not just its own
  button: anchored to its own top it sat 23px inside the Data & Methods button
  (fixed 2026-08-02). **Anything added to this column has to clear the whole
  stack**, and a z-index bump is the wrong tool — it buries a control instead of
  clearing it, and made the button unclickable when tried.

**Tiers 2 and 3 both live inside the foldable Options panel** (`#optpanel`,
`order: 3`): a header button `#opt-fold` toggles `#opt-body`, which **stacks**
`#layers` (the T2 sections) above `#coloradj` (the sole T3 pod). It was a
two-column row until 2026-07-26 — removing `#lens` emptied the T3 column, so the
`#opt-pres` wrapper went with it and `#coloradj` moved to the panel's BOTTOM
(presentation reads last, after the data controls it modifies). The panel got
much narrower as a result: **398px → 216px at 1440px.** It **defaults folded on
≤640px** and unfolded on desktop. So on a phone the whole of T2/T3 is one tap
away and only `#views` + `#toggle` are on the map.

---

## 2. Tier 1 — the views (`#views`)

**The decided 5-view target is what's built and live.** Two of the original
seven became modes of another view rather than top-level entries:

| `#views` button | Internal view name(s) | Notes |
|---|---|---|
| **Money** *(default)* | `money`, **`glass`**, **`change`** | `glass` = the "100 m grid" `#moneydetail` mode. **`change`** (2026-07-30) = the "Change over time" `#moneymode` lens — share-of-base movement, a flat diverging choropleth; **public as of 2026-07-31**. The Money button stays active in both. |
| **Development** | `development`, **`infill`** | Moved to **second, next to Money** (2026-07-27, Peter). `infill` = the full-only "Infill opportunity" `#devmode` lens; the Development button stays active in it. |
| **Services** 🔒 | `services` | Full build only — **LOCKED for release 2026-07-28**. |
| **Ratio** 🔒 | `ratio` | Full build only — **LOCKED for release 2026-07-28**. |
| **Uses** 🔒 | `uses` | Full build only — **LOCKED for release 2026-07-28** (was provisional 07-24). |
| **Lab** 🔒 `beta` | `deviation` *(+ future experiments)* | **NEW 2026-08-11.** Full build only, and it is a **CONTAINER, not a lens** — the `#views` button opens whichever experiment was last active (`state.lab`), and the registry `LAB_EXPERIMENTS` is the list. Carries a `beta` tag in the button itself. First and only experiment today: `deviation` ("vs peer average" — per **developed** acre, and its population follows the cut: Total scores all 358 developed hoods, Residential only the 226 residential ones, Non-residential only the 132 others. 2026-08-12). ⚠️ **9 institutional hoods draw NO prism at all** (15 until 2026-08-15, when share stopped deciding the geometry — see `docs/SPEC_revenue.md` "The consequence tier") — replaced by two white outlines (levied / exempt) that assert no value; the outline is achromatic **by rule**, since a tinted band leans toward a pole the lens exists to abstain from. A ≥25%-institutional hood that does NOT clear the consequence cut keeps its bar and gets the caveat in words. 2026-08-12, narrowed 2026-08-15. |

So **public `#views` = 2 buttons** (Money · Development); **`/full/` = 6**.
Verified in both builds 2026-07-28; the Lab re-verified 2026-08-11
(`verify-deviation.js` asserts the public row is still exactly
`money,development`).

⚠️ **The Lab is the first `#views` entry that is not a lens**, and that
distinction is load-bearing rather than pedantic:
- **Its experiments keep their OWN state.** `deviation` reads `state.labCut`,
  never Money's `state.metric`. It first shipped as a `#moneymode` button where
  those were one variable, and entering from the Value map would have averaged
  **assessed value** and printed it under a title saying *Revenue*
  (`DECISIONS.md` 2026-08-11, second entry).
- **Its own `#layers` sections**: `#labpick` (the experiment picker, hidden
  until there are 2+ — the services-radio rule) and `#labcut` (the deviation
  experiment's revenue cut, the Lab's own copy of Money's three cuts).
- **`#toggle` is HIDDEN in the Lab**, unlike `change`/`glass` which keep it.
- **Adding an experiment is one line** in `LAB_EXPERIMENTS` plus its view
  branches; no chrome work for the second one.

**This is the release shape (Peter, 2026-07-28): "2 views is fine for release,
lock it in. We'll add the other stuff later, like one lens at a time."** The
three provisional tags are settled — none is pending a re-decision. Post-launch
the pulled lenses come back **one at a time**, each as its own deliberate
release, not as a batch un-pull.

**Build visibility (public vs specialist) — FINALIZED 2026-07-23 (§7 +
`DECISIONS.md`).** The two-build split tags each lens `public | full`; this was
the same decision surface as regrouping, resolved together in the "organize the
lenses" pass.

| Lens / control | Public build | Specialist (`/full/`) |
|---|:---:|:---:|
| Money (incl. the 100 m grid mode) | ✅ | ✅ |
| **Development** — units + permits, Detail selector | ✅ | ✅ |
| **Services** view | ❌ _(locked 2026-07-28)_ | ✅ |
| **Ratio** view | ❌ _(locked 2026-07-28)_ | ✅ |
| **Uses** view (dominant zoned land use) | ❌ _(locked 2026-07-28)_ | ✅ |
| **Infill** lens on Development | ❌ | ✅ |
| **Assessment-history panel + hover sparkline + `#hoodmode`** | ✅ _(promoted 2026-07-31)_ | ✅ | _(⚠️ **Services has its own panel as of 2026-08-10** — cost against revenue, not history. `#hoodmode` is offered there again; the sparkline is not, it belongs to the history data)_ |
| **Change over time** lens on Money (`#moneymode` / `#chgwindow`) | ✅ _(promoted 2026-07-31)_ | ✅ |
| **Lab** view + every experiment in it (`#labpick` / `#labcut`) | ❌ _(2026-08-11 — unfinished by definition)_ | ✅ `beta` |
| **`#peek`, the touch-only peek card** | ✅ | ✅ | _(gated on `(hover: none)`, not on build — invisible to every mouse in both)_ |
| **Industrial** metric on Development | ❌ | ✅ |
| Money tooltip's **road m/acre + $/road metre** rows | ❌ _(went with Ratio, 2026-07-28)_ | ✅ |
| Data & Methods: modelled-services caveat, road/fire/transit source credits | ❌ _(went with Services, 2026-07-28)_ | ✅ |
| Deep data-detail (validation ratios, modeling quirks, methods-heavy blurbs) | trimmed to honest labels | ✅ full |
| Money's **Residential / Non-residential** revenue cuts | ✅ *(data-gated only)* | ✅ |

Full-only *modes/metrics inside a public view* (Infill, Industrial) are
`BUILD`-flag-gated at the control level — `|| !FULL_BUILD` sits next to their
data guard, so nothing is stripped from the file.

⚠️ **The Lab gates DIFFERENTLY, and on purpose: at the `#views` button, in the
one-time `if (!FULL_BUILD)` block near the top of the script — not beside a data
guard.** It has no data dependency (its experiments read columns the public
build also carries), so there is nothing else that would keep the button off
the published page. **A future experiment that needs its own data still gates
its data the usual way; the container gate is separate from and additional to
that.**

**The split moves in BOTH directions, and the 2026-07-31 promotion is the
worked example.** `DECISIONS.md` 2026-07-22 locks the two-build *mechanism*; the
*content* split is a per-control tag decided here and revisable (Uses was tagged
full-only "provisional… may return to public"; Transit **amended** an earlier
release-scope lock). Promoting the temporal + change lenses cost three
`FULL_BUILD` conjuncts and no pipeline work, because nothing is stripped —
`temporal.json` already shipped to the public root and the controls were only
hidden. ⚠️ **Promoting has a mirror of the pull-residue problem below:** the
lens's *caveats* must travel with it. The 2024 omission note and the
"NOT set-aside land" legend copy were already written, and
`verify-temporal.js` now asserts the public build **states** the omission — a
visible gap with no explanation reads as broken data.

**Pulling a view is not finished when its button is hidden.** The 2026-07-28
Services/Ratio pull had to chase two residues: Ratio's headline number was on the
*default* view's tooltip, and the Data & Methods pod warned about layers only
those views carried. Before tagging a lens full-only, grep for its columns
outside its own view arm — `tooltipFor`, the about copy, and the legend are the
three places a lens leaks.

---

## 3. Tier 3 — modifier pods

| Pod | Buttons | Actually bites in | Everywhere else |
|---|---|---|---|
| `#coloradj` | `Colour: sqrt scaling` / `Colour: linear` (the label **is** the state) | **Money** — both detail modes | **HIDDEN** (`display:none`, 2026-07-26 — was greyed) |
| `#toggle` (T2, listed here for the comparison) | **two rows**: `Revenue \| Value` over either `Total \| Residential \| Non-residential` (under Revenue) or `Current \| Change over time` (under Value, 2026-08-01) | **Money** — both detail modes, **and the Change lens**, which it hosts the way out of | **HIDDEN** (regroup, 2026-07-23 — was live-but-inert) |
| `#palette`, `Labels` | 3 ramps; hood names on/off | — | moved into the `#a11y` **Display** popover; apply everywhere (palette is n/a in Uses' categorical legend) |
| `#reference-on` (2026-07-27) | `Landmarks & nearby places` on/off — river, ring road, **and the 7 regional place names** | **every view** — `buildLayers()` BRACKETS `buildViewLayers()` (river under, ring road over), so no view can miss it; the place names go into the shared label pool, which every view already composes | never hidden. **Default ON**, unlike `Labels` — with no basemap tiles it is the only orientation cue, so it should not need hunting for |
| `#budget-pod` 🔒 (2026-08-16) | `City budget` `beta` — opens/closes `#budget` | **no view** — it modifies nothing on the map. It opens a citywide readout that is **independent of view, metric and denominator**, so it is the first pod here that never "bites in" anywhere | never hidden in `/full/`, **desktop and phone**; **hidden entirely** in the public build. Two forms: left-column pod on desktop, **bottom sheet ≤640px** (`DECISIONS.md` 2026-08-16), with a phone-only `×` since a sheet is nowhere near its opener |

⚠️ **`#budget-pod` does not fit the tier model, and that is the honest place for
it** (2026-08-16). Every other control here answers *what* is drawn, *which* cut,
or *how* it is painted. This one opens a separate readout and touches the map not
at all — the figures are citywide branch budgets with no neighbourhood dimension.
It sits in `#controls` for proximity, not because it is a map control, and it is
deliberately **not** in `#views`: it is not a lens (`DECISIONS.md` 2026-08-16).
If a second view-independent readout ever appears, these two want their own
group rather than a fourth tier.

**The one control that gates part of another control's layer** (2026-07-27):
`#reference-on` and `Labels` both feed the single `hood-labels` TextLayer, each
gating its own class of anchor via `labelPool()`. This is deliberate — one
layer means one declutter sweep, so a place name and a hood name can never
overlap — but it is the only place in the app where two checkboxes co-own a
layer, and the layer is now gated on **the pool being non-empty** rather than
on `state.labels`. Anything that reasons "labels off ⇒ no text layer" is wrong
as of this date. Regional names win collisions via an explicit `prio`, because
the sweep's existing priority key is polygon area and a Point has none.

**`#hoodmode` — where a hood's detail appears (2026-07-30).** Tier 3, and the
newest pod: `Readout: popup` / `Readout: panel` / `Readout: panel ✓`
(**three** states as of 2026-08-01 — the tick means the panel was *asked for*
rather than fallen into via a peek card, and it is the only state that earns
one-tap pinning on touch, so the button is **not** a plain toggle there:
a fallen-into panel takes one press to KEEP and a second to leave),
label-is-the-state like
`#coloradj` and sitting directly **above** it (moved 2026-07-31 — `#coloradj`
must stay the panel's last child; `verify-coloradj.js` asserts it, and adding a
pod after it went unnoticed for two sessions). **PUBLIC as of 2026-07-31** (was
full-build only), and **hidden until `web/data/temporal.json` loads** — with no
panel to switch to, the control would offer a mode that does not exist.

⚠️ **Hidden in SERVICES 2026-08-06, OFFERED AGAIN 2026-08-10** — the lens now has
its own panel (cost against revenue, `SPEC_services.md` "Hood panel"). The data
gate was never the only gate and still is not: both conditions live in
`syncHoodModePod()` (`temporalData && hoodPanelLens()`), so the reveal and the
per-view rule cannot drift apart, and `applyHoodMode` refuses panel mode wherever
`hoodPanelLens()` is false. **What changed is the view test, not the structure**:
`hoodPanelLens()` is now `!serviceLens() || state.hasSvcCost`, so Services keeps
the 2026-08-06 behaviour on a geojson predating the cost columns rather than
advertising a panel that would open empty. Rationale for both moves:
`DECISIONS.md` 2026-08-06 and 2026-08-10.

⚠️ **The panel's CONTENT is now three-way, not two** (`openTemporal`): service
cost, revenue mix, assessment history — tested in that order, first match wins.

It is the one control that changes **what the tooltip contains**: in panel mode
a view's hover collapses to its **headline number only**, and the temporal
sparkline + "click to pin" hint drop out. ⚠️ **That reduction is per-view
explicit, NOT "row 0" of the tooltip** — services' rows lead with road metres
whenever roads are present regardless of which service drives the ramp, so a
positional rule would print road supply under a stormwater-coloured map.
Services' headline reads `state.svcDriver` (still true wherever `primaryRow` is
used — the peek card uses it too).

⚠️ **The reduction is itself gated on the view having a panel (2026-08-06).**
It is a TRADE — tooltip detail for a panel that carries it — so where no panel
opens it is not a reduction, it is a deletion. In Services the hover stays full
even when `state.hoodMode` is still `"panel"` from another view.

**`#temporal`, the pinned hood panel (2026-07-29), is the surface it governs** —
and it is no longer tier-less. ⚠️ **It is no longer the assessment-history panel
in every lens (2026-08-01): on Money's REVENUE metrics it shows the hood's
zone-revenue breakdown instead**, and the history belongs to Value, which is what
it describes. One element, two modes (`renderHistory` / `renderRevenueMix`), so
the three dismissals and the phone bottom-sheet form are shared rather than
duplicated. **Three surfaces advertise it and all three follow the lens:**
`#peek-go`, `#temporal-hint`, and the tooltip's invite. ⚠️ **It no longer
appears in every view (2026-08-06): SERVICES has no panel** — it is getting a
service-specific one — so there it is taken off screen entirely rather than
left on its empty prompt, and all three advertisements go with it (`#peek-go`
hides; the map click and the card's commit are inert). An empty panel whose
prompt still says *"click a neighbourhood to see its assessment history"* over a
lens where clicking does nothing is the same class of lie the per-lens prompt
text exists to prevent. It is in **both builds** (public as of 2026-07-31), and
is still the only surface openable by clicking **the map itself**. It is
in `CHROME_IDS`, so the label sweep dodges it while open. Three dismissals with
deliberately different scopes: the **×** clears the pinned hood (content),
**Escape** and **`#hoodmode`** leave the mode. Design and the two rendering
invariants: `SPEC_temporal.md` §2.

**`#peek`, the touch-only peek card (2026-07-31), is the stage BEFORE it.** Not
a control and not a tier — a readout, and the only surface in the app whose
existence is decided by the **pointer** rather than by the view, the build or the
data. On `(hover: none)` a map tap opens this card instead of the panel, and the
card's own tap commits; everywhere else it never displays. It is in `CHROME_IDS`
alongside `#temporal`. **It shows the view's FULL readout** (2026-08-01) — the
same rows `viewTooltip` gives a mouse, minus the heading it prints itself — so
the view × sub-metric state space above governs the card's contents exactly as it
governs the hover's. Before that it showed the headline only, which on touch
(where `.tip` is suppressed) left a phone one line per lens.

⚠️ **IT MUST OPEN IN EVERY VIEW, INCLUDING THE ONES WITH NO PANEL BEHIND IT.**
Because `.tip` is suppressed on touch, this card is the **only per-hood readout
a phone has** — so anything that stops it opening does not degrade the lens, it
*deletes* it. That shipped to production on 2026-08-06: the Services history-panel
gate was written into `temporalFor()`, the shared **data** accessor, which the
card also tests, and tapping a neighbourhood in Services returned nothing at all.
**Panel-ness is a property of the VIEW (`hoodPanelLens()`); having history is a
property of the DATA (`temporalFor()`) — never conflate them.** Where there is
no panel the card still opens, `#peek-go` hides, and its own tap is a plain
dismissal. ⚠️ Note the harder half: the **deliberate opt-in** (`panelByChoice`)
normally routes a tap past the card straight to pinning, so views with no panel
must take the card path *regardless of the opt-in* or the tap dies on an inert
pointer path. `verify-peek.js` covers the whole case and is falsified against
the broken build. ⚠️ **Two of its rules deliberately invert `#temporal`'s**
and should not be "made consistent": an empty-map tap **dismisses** the card
(the panel is inert there — that rule protects a surface you asked for), and
re-tapping the shown hood is a **no-op** rather than a toggle, because a touch
tap can fire the handler twice. `#temporal`'s **×** is also enlarged to 44px on
the same seam. Full reasoning: `SPEC_temporal.md` §2, `MOBILE_USABILITY.md` §1.

**`#millrates`, the mill-rate pod (2026-08-01), is a READ-ONLY surface with the
narrowest gate in the app** — Money **and** a revenue cut, i.e. it is the only
chrome keyed on the `#revcut` row's *existence* rather than on a view. It is not
a control: nothing in it is clickable, and it changes only which of its three
rates is lit. It is in `CHROME_IDS`. Two rules make it unlike every other pod:
- **It has no fixed position.** `top` is read from `#title`'s measured box each
  time, because the blurb is 60px taller on the residential and non-residential
  cuts (196 → 256) and 140-499px across the app as a whole. Every other pod in
  this column uses a constant, and ⚠️ **`#temporal`'s constant is wrong in five
  states because of it** (TODO.md).
- **It yields.** With `#temporal` open the column cannot hold both at laptop
  heights, so the pod hides — via a CSS sibling selector rather than a JS toggle,
  so the two cannot both think they own the slot. This is the reverse of `#peek`,
  which the panel *replaces*; here the panel simply wins. **Desktop-only in
  effect:** on a phone the panel is a bottom sheet, so the two never contend.

⚠️ **It is the only surface that changes PARENT across the two seams, and on a
phone it is not a surface at all.** On desktop it floats in the free left column
under `#title`. At ≤640px it is **re-parented into `#title`** and becomes part of
the description blurb — it opens and closes with that card and adds nothing to
the default render (Peter, 2026-08-01: *"i don't like the independent mill rates
panel. folding it into the tax revenue blurb is fine"*). One phone-only rendering
rule survives: the rates render **stacked, one per row**, because the desktop
one-liner wraps at 360px and breaks between a class and its number.
⚠️ **The desktop yield is desktop-only BY CONSTRUCTION** — a child of `#title` is
not `#temporal`'s sibling — not by media query; it shipped ungated once and
blanked the rates in phone panel mode. `verify-millrates.js` covers all of this
at 390 and 360, including that the rates survive panel mode.

**All the inconsistencies in this table are now fixed.** `#toggle` used to stay
live but inert outside Money (resolved by the regroup — old combo C), `#lens`
used to grey out (resolved 2026-07-25, then the control was **removed entirely**
2026-07-26), and `#coloradj` stopped greying on 2026-07-26. **Nothing greys any
more.** With `#lens` gone, `#coloradj` is a direct child of `#opt-body`, so
hiding it takes its own row with it — no column-collapse step is needed.

The hide came from a live bug report ("the highlight residential button doesn't
work"): greyed `#4a4a5e` on a dark panel reads as *broken*, not *unavailable*,
and Money's **100 m grid** mode drops the lens *without leaving the Money view*,
so the control looked dead in place.

---

## 4. Tier 2 — per-view controls (in `#layers`)

Each row shows only in its view(s), and only when the underlying data columns
exist (the data-gate flags). `#layers` itself is hidden unless the current view
has at least one section to show.

| View / mode | Controls shown | Data-gate | Dynamic rules |
|---|---|---|---|
| **Money → Neighbourhood** | `#moneydetail` (Neighbourhood / 100 m grid); `#denom` headed **"Denominator"** | `#moneydetail` unconditional; `#denom` on `hasHoodLot` | `#coloradj` live (bottom of the panel); **`#toggle` shows exactly one row 2** — `#revcut`'s 3 cuts under Revenue, `#moneymode`'s Current / Change over time under Value (moved out of this panel 2026-08-01), the latter gated on `temporalData` |
| **Money → 100 m grid** (`glass`) | same `#moneydetail`; `#denom` **relabelled "Spike denominator"** | `gridData.hasLot` | **no `#prism-row`** — opacity fixed at 60%, re-applied on entry (2026-07-25); `#coloradj` stays live; `#revcut` still offered (the grid carries the cut columns, `col >= 0` fallback). `#moneymode` still appears under Value, but the lens toggle returns to the **prisms**, never here — Glass is a Detail choice |
| **Money → Change over time** (`change`) | `#chgwindow` (**Since 2012 / Since 2019**) — the section's only member since `#moneymode` left, so the "Window" header now stands alone | `temporalData` — **public as of 2026-07-31**; was doubly gated, and the surviving data gate is the one that matters: the toggle can never offer a lens whose data is absent | **no `#moneydetail`** (no change grid), **no `#denom`**, **`#coloradj` inert** (its own per-arm diverging clamp, like Infill). ⚠️ **`#toggle` STAYS VISIBLE here** (changed 2026-08-01) — it hosts the lens toggle, so hiding it would strand you in the lens. Value reads lit because the metric *is* share of the assessment base. Picking **Revenue** leaves the lens (Revenue owns no change lens); leaving via `Current` lands on the **prisms**, never Glass |
| **Services** | `#services` — **10 rows in 3 captioned groups** (2026-08-03): **Transportation** (Roads · Transit · Bike — *supply*), **Transportation cost — operating** (Roads cost · Transit cost · Bike cost — *dollars*) and **Other services** (Stormwater · Fire · Water/sewer · Service cost). Each row = on/off checkbox + a "colour" driver radio | rows self-gate on their columns; **captions self-gate on their rows** | radios appear only when **≥2** are checked; the driver always names a *checked* service (unchecking it hands the ramp on); fire/transit draw their dots and bike/transit their lines whenever checked, driver or not. ⚠️ **The group captions are LABELS — they gate nothing, carry no inputs, and a caption whose every row is hidden hides itself.** Grouping is shared DOM, so it drives desktop AND mobile. ⚠️ **The cost group is a SEPARATE caption on purpose:** its rows are dollars on an *operating* basis while the group above is supply, and **Roads cost is the same metres as Other services' Service cost on a different basis (~10.8× apart)** — the caption is where that distinction is visible in the panel. ⚠️ **`transport_cost_ops_per_acre` ships as a COLUMN with NO ROW** (90.8% transit at the median — `DECISIONS.md` 2026-08-03); do not add one without re-opening that call. Measured at 390/360/320 px with all 10 rows visible: no clip, no overflow, 178–235px clearance |
| **Ratio** | `#ratio-denom` (Per road metre / Per fire event / Per service $); `#prism-row` opacity slider, default 5% | `hasFire \|\| hasSvcCost` (else roads-only, control hidden) | **the only view that also shows the `#prism-hd` "Money plane" header** |
| **Uses** 🔒 | `#uses-prisms` (Height = share zoned residential); `#prism-row` while prisms on, default 35% | — | legend swaps to categorical |
| **Development → Housing built** | `#devmode` 🔒 (Housing built / Infill opportunity); `#devmetric` (Dwelling units / Permits / Industrial 🔒); `#devwindow` (**Last 3 yr / Last 5 yr / Since 2009** — shortest to longest, **`Since 2009` is the default**); `#devdetail` (Neighbourhood / **100 m grid — activity, the default**); `#prism-row` while the grid is active (50%) | `FULL_BUILD && hasInfill`; `hasPermitsPerAcre`; `hasDevWindow`, `hasLongWindow`; `devGridOfferable()` | **see below** |
| **Development → Infill** 🔒 | `#devmode`; `#devmetric` (**Industrial hidden**); `#devwindow` | same as Development | **no `#devdetail`** (no infill grid), no slider; entering with Industrial selected **silently resets to units** |

🔒 = full build only.

### Development's dynamic gating

- `#devdetail` — the **2-way Detail selector**. Shipped 3-way (decision #7,
  §7) replacing the old `#dev-grid` checkbox + `#devspike` picker; the third
  option, Stock age, was **withdrawn 2026-07-27** (`DECISIONS.md`). Offered whenever
  the grid file loaded **and** the metric isn't Industrial (`devGridOfferable =
  !!devGridData && !devIndustrial()`). The long "Since 2009" window **is**
  offerable (its own grid, PR #80). Industrial is the only choropleth-only metric.
- **Metric and Window now apply in both Detail modes.** They were suppressed
  only while Stock age was up; with it gone, nothing in this view hides them.

---

## 5. Weird combos — what's still open after the regroup

The regroup (§7) closed most of the original list; the resolved ones are kept at
the bottom as a record, **still under their original letters** — older references
elsewhere (`DECISIONS.md` says "§5.G", "§5.A/B", "§5.F") point at those. The
still-open items below are **numbered** so the two sets can't be confused.

**1. ~~`#coloradj` greys where its two neighbours hide.~~ RESOLVED 2026-07-26 —
it hides too.** `Colour: sqrt scaling` was the last pod still greying. Nothing in
the panel greys any more.

**2. ~~Money → 100 m grid has a hole in the Options panel.~~ RESOLVED 2026-07-26,
then made moot the same day.** The hole was first closed by collapsing the T3
column; hours later `#lens` was removed outright, which emptied that column
permanently. `#opt-pres` and its `syncPresColumn` helper are both **gone** —
`#coloradj` is now a direct child of `#opt-body` and takes its own row when it
hides. The two-column Options layout is gone with them.

**3. ~~Stock age still morphs the Development panel~~ — CLOSED 2026-07-27.**
The option was withdrawn, so nothing in Development hides Metric + Window any
more. The panel no longer reshuffles on a Detail change.

**4. Two separate "what do I divide by?" controls.** `#denom` (acres; Money, both
modes) and `#ratio-denom` (Ratio) are conceptually siblings but live apart, and
`#denom` still relabels itself ("Denominator" ↔ "Spike denominator") by mode.
**Untouched by the regroup.**

**5. Industrial silently self-resets.** In `/full/`, entering Infill with
Industrial selected drops the metric back to units without saying so. The public
build can't hit this (Industrial isn't there), which is why it survived — but a
silent state change is still a silent state change.

**6. ~~Stock age is arguably a lens wearing a Detail costume~~ — CLOSED
2026-07-27,** by removal rather than by relocation. It was the assessed standing
stock's median construction year — not permit activity at all — sitting in
Development's Detail selector only because that is where the 100 m grid
machinery lives. **The complaint was right, and worth remembering in the same
shape it was written:** if a control ignores the pickers around it, it is
probably a lens, not a detail mode. Industrial (old F, below) is the surviving
instance.

**7. `#views` position on mobile** — a thin strip at the very top, which is the
other half of the "under-reads as the primary control" concern. The *size* half
was fixed 2026-07-25. ⚠️ **The position fork it was waiting on (move-2 /
bottom-sheet) was REFUSED 2026-08-04** — the control column stays a stack — so
this has no vehicle and needs its own proposal if revisited.
`MOBILE_USABILITY.md` §3.

### Resolved by the regroup (record)

| Old | Was | Resolved by |
|---|---|---|
| **A** | "Year built" buried under the Detail checkbox — the whole stock-age lens invisible until you found an unrelated tick-box | The 3-way `#devdetail` (decision #7) |
| **B** | Choosing "Year built" morphed the panel unannounced | Same — now an explicit mode choice (residue → §5.3) |
| **C** | `#toggle` stayed live but inert in 5 of 7 views | `#toggle` is Money-scoped and **hides** (decision #5) |
| **E** | "Residential" meant two things in two pods (`Residential $` vs `Residential only`) | Renamed → **Highlight residential** (decision #6); both now Money-scoped and adjacent |
| **F** | Industrial, a Development-only choropleth metric, hidden inside `#devmetric` | Tagged full-only (decision #8) — public Development is units + permits, both grid-capable (residue → §5.5) |
| **G** | Glass double-duty'd Money's controls while being its own top-level view | Glass → Money's `#moneydetail` mode (decision #1) |

---

## 6. Discrepancy found while mapping (RESOLVED 2026-07-26)

A comment claimed the long "Since 2009" window is choropleth-only ("the Detail
toggle hides for either"). That was **stale** — PR #80 made the long window
first-class with its own grid; `devGridOfferable = !!devGridData &&
!devIndustrial()` excludes **only** Industrial.

The claim appeared in **three** sibling comments. The 2026-07-22 fix caught one
and was recorded here as done, which is how the other two survived another four
days — a reminder to grep for the *claim*, not fix the line you happened to
open. All three now agree (`devGridOfferable`, `syncDevChrome` and
`applyDevWindow`, corrected 2026-07-26 in PR #96).

**Behaviour was correct throughout — these were comments only.** The substantive
point they obscured is worth keeping: `syncDevChrome` still has to run on a
window switch, just for the title/blurb/legend and the per-window scale, *not* to
flip the Detail toggle.

---

## 7. Regrouping decisions (locked — BUILT 2026-07-23, MERGED & LIVE)

The running output of the "organize the lenses" pass. All eight were built in one
reflow on 2026-07-23 (branch `regroup-build-s65`) and are **now on master and
live** on both builds. The as-built map: `#views` = 5 (4 public); Glass = Money
`#moneydetail` mode (internal view unchanged); Infill = full-only `#devmode` on
Development; Industrial = full-only `#devmetric`; palette + Labels = the `#a11y`
"Display" popover; grid+spike = the `#devdetail` 3-way selector; `Highlight
residential` = the collapsed `#lens`. Table kept as the decision record; §2–§5
above describe the result. Mirrored in `DECISIONS.md`.

| When | Decision | Resolved |
|---|---|---|
| 2026-07-22 | **Glass → a render-mode of Money, not a top-level view.** `#views` drops 7→6; Glass becomes a grid/translucent toggle inside Money (it already reuses Money's `#toggle` + `#coloradj` + denominator). | old §5.C, §5.D, §5.G |
| 2026-07-23 | **Infill → a full-only mode of Development, not a top-level view.** `#views` drops 6→5. Shares `#devmetric`/`#devwindow` already. Unlike Glass, Infill does NOT share Development's build tag: Development is public, Infill is full-only → the toggle appears ONLY in `/full/` (`BUILD`-gated at the control level). | old §5.F-adjacent, §2 |
| 2026-07-23 | **`#palette` moves off the always-visible top chrome into an accessibility menu** — NOT deleted (Cividis is the CVD-safe ramp; deleting it = an a11y regression). Default stays **Inferno**, applied without opening the menu. Drops one T3 pod off the top stack. | old §3 |
| 2026-07-23 | **`Labels` also moves into the accessibility menu** — a display aid, same home. Leaves `#lens` holding only the Money/Ratio-scoped fade, so it collapses to a single toggle. | old §3 |
| 2026-07-23 | **Top stack reorders to tier order: View → Variant → Presentation.** ① `#views` (T1); ② `#toggle` (T2, Money's metric picker); ③ `#optpanel` (T2 `#layers` + T3 `#coloradj`/`#lens`); ④ accessibility button, out of the tier flow. Consequence: **`#toggle` becomes Money-scoped** and stops floating live-but-inert. | old §5.A, §5.C |
| 2026-07-23 | **`Residential only` → "Highlight residential"** — kills the name clash with the `Residential $` metric. Intent-first label. **Label-only — no mechanics, no scope change.** | old §5.E |
| 2026-07-23 | **Development's `#dev-grid` checkbox + `#devspike` picker collapse into ONE 3-way "Detail" selector**: **① Neighbourhood** · **② 100 m grid — activity** · **③ Stock age**. Metric + Window apply to ①/②; ③ hides them as an EXPLICIT mode choice. Motivated by phone usability — a nested checkbox reveal is a weak tap target (structure-before-mobile). | old §5.A, §5.B |
| 2026-07-23 | **Industrial tagged full-only** — it's choropleth-only, so in public it would leave the new Detail selector with two dead options. **Public Development is airtight: units + permits, both grid-capable.** | old §5.F, §2 |

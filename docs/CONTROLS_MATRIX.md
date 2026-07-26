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
  since 2026-07-26** — a quantity row (Revenue | Value) with a revenue-cut row
  (Total | Residential | Non-residential) nested under it. It is the only control
  that nests *within* a tier; the nesting mirrors the data (`levy == res + nonres
  + farmland`), so it is not a new tier.
- **Tier 3 — HOW it's drawn** (presentation modifiers): `#coloradj` — the only
  one left since `#lens` was removed 2026-07-26.
- **Out of the tier flow:** the `#a11y` **Display** popover (colour ramp +
  neighbourhood labels), bottom-right.

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
| **Money** *(default)* | `money`, **`glass`** | `glass` = the "100 m grid" `#moneydetail` mode. The Money button stays active in it. |
| **Services** | `services` | |
| **Ratio** | `ratio` | |
| **Uses** 🔒 | `uses` | Full build only (2026-07-24, provisional). |
| **Development** | `development`, **`infill`** | `infill` = the full-only "Infill opportunity" `#devmode` lens. The Development button stays active in it. |

So **public `#views` = 4 buttons** (Money · Services · Ratio · Development);
**`/full/` = 5**. Verified live in both builds 2026-07-25.

**Build visibility (public vs specialist) — FINALIZED 2026-07-23 (§7 +
`DECISIONS.md`).** The two-build split tags each lens `public | full`; this was
the same decision surface as regrouping, resolved together in the "organize the
lenses" pass.

| Lens / control | Public build | Specialist (`/full/`) |
|---|:---:|:---:|
| Money (incl. the 100 m grid mode) · Services · Ratio | ✅ | ✅ |
| **Development** — units + permits, Detail selector | ✅ | ✅ |
| **Uses** view (dominant zoned land use) | ❌ _(provisional, 2026-07-24)_ | ✅ |
| **Infill** lens on Development | ❌ | ✅ |
| **Industrial** metric on Development | ❌ | ✅ |
| Deep data-detail (validation ratios, modeling quirks, methods-heavy blurbs) | trimmed to honest labels | ✅ full |
| Money's **Residential $ / Non-res $** metrics | ✅ *(data-gated only)* | ✅ |

Full-only *modes/metrics inside a public view* (Infill, Industrial) are
`BUILD`-flag-gated at the control level — `|| !FULL_BUILD` sits next to their
data guard, so nothing is stripped from the file.

---

## 3. Tier 3 — modifier pods

| Pod | Buttons | Actually bites in | Everywhere else |
|---|---|---|---|
| `#coloradj` | `Colour: sqrt scaling` / `Colour: linear` (the label **is** the state) | **Money** — both detail modes | **HIDDEN** (`display:none`, 2026-07-26 — was greyed) |
| `#toggle` (T2, listed here for the comparison) | **two rows**: `Revenue \| Value` over `Total \| Residential \| Non-residential` (2026-07-26) | **Money** — both detail modes | **HIDDEN** (regroup, 2026-07-23 — was live-but-inert) |
| `#palette`, `Labels` | 3 ramps; hood names on/off | — | moved into the `#a11y` **Display** popover; apply everywhere (palette is n/a in Uses' categorical legend) |

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
| **Money → Neighbourhood** | `#moneydetail` (Neighbourhood / 100 m grid); `#denom` headed **"Denominator"** | `#moneydetail` unconditional; `#denom` on `hasHoodLot` | `#coloradj` live (bottom of the panel); `#revcut` (in `#toggle`, on the map) offers the 3 revenue cuts |
| **Money → 100 m grid** (`glass`) | same `#moneydetail`; `#denom` **relabelled "Spike denominator"** | `gridData.hasLot` | **no `#prism-row`** — opacity fixed at 60%, re-applied on entry (2026-07-25); `#coloradj` stays live; `#revcut` still offered (the grid carries the cut columns, `col >= 0` fallback) |
| **Services** | `#services` — 6 rows: Roads · Stormwater · Fire · Water/sewer · Transit · Service cost. Each = on/off checkbox + a "colour" driver radio | rows self-gate on their columns | radios appear only when **≥2** are checked; the driver always names a *checked* service (unchecking it hands the ramp on); fire/transit draw their dots whenever checked, driver or not |
| **Ratio** | `#ratio-denom` (Per road metre / Per fire event / Per service $); `#prism-row` opacity slider, default 5% | `hasFire \|\| hasSvcCost` (else roads-only, control hidden) | **the only view that also shows the `#prism-hd` "Money plane" header** |
| **Uses** 🔒 | `#uses-prisms` (Height = share zoned residential); `#prism-row` while prisms on, default 35% | — | legend swaps to categorical |
| **Development → Housing built** | `#devmode` 🔒 (Housing built / Infill opportunity); `#devmetric` (Dwelling units / Permits / Industrial 🔒); `#devwindow` (Last 5 yr / Last 3 yr / Since 2009); `#devdetail` (Neighbourhood / 100 m grid — activity / Stock age); `#prism-row` while the grid is active | `FULL_BUILD && hasInfill`; `hasPermitsPerAcre`; `hasDevWindow`, `hasLongWindow`; `devGridOfferable()`, `devAgeCol()` | **see below** |
| **Development → Infill** 🔒 | `#devmode`; `#devmetric` (**Industrial hidden**); `#devwindow` | same as Development | **no `#devdetail`** (no infill grid), no slider; entering with Industrial selected **silently resets to units** |

🔒 = full build only.

### Development's dynamic gating

- `#devdetail` — the **one 3-way Detail selector** that replaced the old
  `#dev-grid` checkbox + `#devspike` picker (decision #7, §7). Offered whenever
  the grid file loaded **and** the metric isn't Industrial (`devGridOfferable =
  !!devGridData && !devIndustrial()`). The long "Since 2009" window **is**
  offerable (its own grid, PR #80). Industrial is the only choropleth-only metric.
- The **Stock age** option additionally needs the year column (`devAgeCol() >= 0`);
  older grid files hide just that button and keep the other two.
- Selecting **Stock age** hides `#devmetric` and `#devwindow` (a stock snapshot
  has no permit metric or window) — now an **explicit mode choice** rather than
  the old surprise morph. See §5.3.

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

**3. Stock age still morphs the Development panel** — choosing it hides Metric +
Window. Now *chosen* rather than stumbled into (old B was worse: the picker
only appeared after ticking an unrelated checkbox), and the option's tooltip says
"Hides Metric + Window". Kept on the list because the panel still reshuffles;
downgraded from a defect to a known cost.

**4. Two separate "what do I divide by?" controls.** `#denom` (acres; Money, both
modes) and `#ratio-denom` (Ratio) are conceptually siblings but live apart, and
`#denom` still relabels itself ("Denominator" ↔ "Spike denominator") by mode.
**Untouched by the regroup.**

**5. Industrial silently self-resets.** In `/full/`, entering Infill with
Industrial selected drops the metric back to units without saying so. The public
build can't hit this (Industrial isn't there), which is why it survived — but a
silent state change is still a silent state change.

**6. Stock age is arguably a lens wearing a Detail costume.** It's the assessed
standing stock's median construction year — not permit activity at all, and it
ignores Metric and Window. It sits inside Development's Detail selector because
that's where the 100 m grid machinery is. Same shape as the old Industrial
complaint (old F, below), and worth revisiting if Development ever gets crowded.

**7. `#views` position on mobile** — a thin strip at the very top, which is the
other half of the "under-reads as the primary control" concern. The *size* half
was fixed 2026-07-25; the position fork (move-2 / bottom-sheet) is
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
open. All three now agree (`devGridOfferable` at ~L1700, `syncDevChrome` and
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

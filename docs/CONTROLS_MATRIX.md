# Controls & Lens Combinations — current state

Authoritative **snapshot** of every view × control combination as the app
actually behaves today (verified against `web/index.html`, 2026-07-22). This is
the map to reason about **regrouping** the controls (desktop grouping is shared
DOM → it drives the mobile layout too; see `docs/MOBILE_USABILITY.md`).

- This doc = the current *state space* (what shows when, what gates what).
- `docs/UI.md` = the chronological *build log* (why each feature was built).
- The flagged "weird combos" in §5 are the **unpack/move candidates** — not yet
  decided; they feed the regrouping decision.

---

## 1. The three tiers

Every control is one of three tiers. The current on-screen stack does **not**
follow this order (see §5.A):

- **Tier 1 — WHAT am I looking at** (the view/mode): `#views`.
- **Tier 2 — WHICH variant** of the current view (view-scoped sub-metrics):
  live in `#layers`, plus the special-cased `#toggle`.
- **Tier 3 — HOW it's drawn** (presentation modifiers): `#coloradj`, `#palette`,
  `#lens`.

---

## 2. Tier 1 — the views (`#views`)

**Built today (7):** `Money · Services · Ratio · Uses · Development · Infill · Glass`
**Decided target (5, §7):** `Money · Services · Ratio · Uses · Development`
— Glass → a mode of Money; Infill → a full-only mode of Development. §3–§5 below
still describe the **built** 7-view state (this doc is a current-state snapshot);
§7 holds the decided-but-unbuilt regroup.

**Build visibility (public vs specialist) — FINALIZED 2026-07-23 (§7 +
`DECISIONS.md`).** The two-build split tags each lens `public | full`; this was
the same decision surface as regrouping, resolved together in the "organize the
lenses" pass.

| Lens / control | Public build | Specialist (`/full/`) |
|---|:---:|:---:|
| Money (incl. Glass grid mode) · Services · Ratio · Uses | ✅ | ✅ |
| **Development** — units + permits, Detail selector | ✅ | ✅ |
| **Infill** mode on Development | ❌ | ✅ |
| **Industrial** metric on Development | ❌ | ✅ |
| Deep data-detail (validation ratios, modeling quirks, methods-heavy blurbs) | trimmed to honest labels | ✅ full |

Full-only *modes/metrics inside a public view* (Infill, Industrial on the public
Development view) are `BUILD`-flag-gated at the control level — the two-build
mechanism handles exactly this.

---

## 3. Tier 3 — modifier pods (rendered "always visible" at the top)

| Pod | Buttons | Actually bites in | In every other view |
|---|---|---|---|
| `#coloradj` | `Colour: sqrt scaling` (on/off) | **Money, Glass** | **greyed/disabled** (`.disabled`) |
| `#toggle` | `Revenue · Value · Residential $ · Non-res $` | **Money, Glass** | **stays fully live but silently inert** — records state, changes nothing visible (early-return in `applyMetric`) |
| `#palette` | `Inferno · Glow · Cividis` | all gradient views | applies (n/a in Uses' categorical legend) |
| `#lens` → `Residential only` | fade non-res hoods | **Money, Ratio** | **disabled** |
| `#lens` → `Labels` | hood name labels | **all views** | applies |

Note the inconsistency already visible here: three of these are Money/Glass- or
Money/Ratio-only, but only `#coloradj` and `Residential only` **grey out** when
they don't apply — `#toggle` does not. See §5.C.

---

## 4. Tier 2 — per-view controls (in `#layers`)

Each row shows only in its view(s), and only when the underlying data columns
exist (the data-gate flags). `#layers` itself is hidden unless the current view
has at least one section to show.

| View | Controls shown | Data-gate | Dynamic rules |
|---|---|---|---|
| **Money** | `#denom` (Ground / Lot acres) | `hasHoodLot` | — |
| **Services** | `#services` — 6 rows: Roads · Stormwater · Fire · Water/sewer · Transit · Service cost. Each = on/off checkbox + a "colour" driver radio that appears only when **≥2** services are on | rows self-gate on their columns | exactly one service drives the ramp; others render neutral |
| **Ratio** | `#ratio-denom` (Per road metre / Per fire event / Per service $); `#prism-row` opacity slider | `hasFire \|\| hasSvcCost` (else roads-only, control hidden) | — |
| **Uses** | `#uses-prisms` (Height = share zoned residential); `#prism-row` when prisms on | — | legend swaps to categorical |
| **Development** | `#devmetric` (Dwelling units / Permits / Industrial); `#devwindow` (Last 5 yr / Last 3 yr / Since 2009); `#dev-grid` **Detail = 100 m grid**; `#devspike` (New homes / Year built); `#prism-row` when grid active | `hasPermitsPerAcre`, `hasDevWindow`, `hasIndPermits`, `devGridData`, `devAgeCol` | **see §5.A/B — the gnarly one** |
| **Infill** | `#devmetric` (Dwelling units / Permits — **Industrial hidden**); `#devwindow` | same as Dev | entering Infill with Industrial selected **silently resets to units** |
| **Glass** | `#denom` relabelled **"Spike denominator"** (Ground / Lot); `#prism-row` opacity; **also uses `#toggle` metric + `#coloradj`** | `gridData.hasLot` | Glass = "Money, translucent, grid-denominated" |

### Development's dynamic gating (the tangle)

- `#dev-grid` (Detail / 100 m grid) is **offerable** whenever the grid file
  loaded **and** the metric isn't Industrial (`devGridOfferable = !!devGridData
  && !devIndustrial()`). The long "Since 2009" window **is** offerable (it has
  its own grid — PR #80). Industrial is the only choropleth-only metric.
- `#devspike` (New homes / Year built) shows **only when the 100 m grid is ON**
  (`devGridActive()`) and the age column loaded → **§5.A**.
- Selecting **Year built** sets `ageUp`, which **hides `#devmetric` and
  `#devwindow`** (a stock snapshot has no permit metric/window) → **§5.B**.

---

## 5. Weird combos — unpack/move candidates

The reason for this doc. None decided; these feed the regrouping pass.

**A. "Year built" is buried under the Detail checkbox.** The New-homes-vs-Year-
built picker (`#devspike`) only appears *after* you tick "100 m grid". So the
entire stock-age lens is invisible until you find an unrelated checkbox. And
"New homes" (the default) just re-labels what the choropleth already shows — the
picker's real payload is "reveal Year built." **This is the one Peter flagged.**

**B. Choosing "Year built" morphs the panel** — Metric + Window pickers vanish.
Combined with A, the Development panel reshuffles a lot as you poke it.

**C. `#toggle` stays live but inert in 5 of 7 views.** Revenue/Value/Residential
$/Non-res $ only bite in Money + Glass, yet the pod stays fully interactive in
Services/Ratio/Uses/Development/Infill — flipping it there changes nothing
visible. `#coloradj` (same Money/Glass scope) greys out; `#toggle` doesn't.
Inconsistent + misleading.

**D. Two separate "what do I divide by?" controls.** `#denom` (acres; Money +
Glass) and `#ratio-denom` (Ratio) are conceptually siblings but live apart, and
`#denom` even relabels itself ("Denominator" ↔ "Spike denominator") by view.

**E. "Residential" means two different things in two pods.** `Residential $`
(a metric in `#toggle`) vs `Residential only` (a fade lens in `#lens`) — similar
names, unrelated mechanics; the metric's tooltip already has to disclaim the
confusion.

**F. Industrial is a Development-only metric hidden inside `#devmetric`** and
silently self-resets on entering Infill. It's arguably a different lens wearing
a sub-metric costume.

**G. Glass double-duties Money's controls** (`#toggle` metric + `#coloradj` +
denominator) while being its own top-level view — worth asking whether it's a
view or a render-mode of Money.

---

## 7. Regrouping decisions (locked — BUILT 2026-07-23, branch `regroup-build-s65`)

The running output of the "organize the lenses" pass. Each locked a piece of the
regrouped structure; **all eight were built in one reflow on 2026-07-23** (branch
`regroup-build-s65`, not yet on master — merge gated on the two-build deploy
plumbing so the public root isn't shipped the `full` default). The as-built map:
`#views` = 5; Glass = Money `#moneydetail` toggle (internal view unchanged);
Infill = full-only `#devmode` on Development; Industrial = full-only `#devmetric`;
palette + Labels = the `#a11y` "Display" popover; grid+spike = the `#devdetail`
3-way selector; `Highlight residential` = the collapsed `#lens`. Table kept as the
decision record. Mirror to `DECISIONS.md`.

| When | Decision | Resolves |
|---|---|---|
| 2026-07-22 | **Glass → a render-mode of Money, not a top-level view.** `#views` drops 7→6; Glass becomes a grid/translucent toggle inside Money (it already reuses Money's `#toggle` + `#coloradj` + denominator). | §5.C, §5.D, §5.G |
| 2026-07-23 | **Infill → a full-only mode of Development, not a top-level view.** `#views` drops 6→5 (Money · Services · Ratio · Uses · Development). Shares `#devmetric`/`#devwindow` already. Unlike Glass, Infill does NOT share Development's build tag: Development is public, Infill is full-only → the Infill toggle appears ONLY in the `/full/` build (`BUILD`-flag-gated at the control level). Public build's Development = activity only; specialist's = activity + Infill toggle. | §5.F-adjacent, two-build tag surface (§2) |
| 2026-07-23 | **`#palette` (Inferno · Glow · Cividis) moves off the always-visible top chrome into an accessibility menu/button** — NOT deleted (Cividis is the colour-vision-deficiency-safe ramp; deleting it = an a11y regression). Default stays **Inferno**, applied without opening the menu; the picker is one tap away for those who need it. Drops one T3 pod off the top stack. The a11y menu is the natural future home for other display-aid toggles (e.g. `Labels`, any high-contrast option). | §3 (`#palette` row) |
| 2026-07-23 | **`Labels` (hood-name labels) also moves into the accessibility menu** — a display/legibility aid, same home as palette. Leaves `#lens` holding only `Residential only` (a Money/Ratio-scoped fade), so `#lens` collapses from a multi-option pod to a single toggle. | §3 (`#lens` rows) |
| 2026-07-23 | **Top stack reorders to tier order: View → Variant → Presentation** (fixes §5.A tier scramble). Top→bottom: ① `#views` (T1); ② per-view variants (T2) — `#layers` + `#toggle` (now Money's metric picker); ③ presentation (T3) — `#coloradj` + `Residential only`; ④ accessibility button (palette, labels), out of the tier flow. Two consequences: **`#toggle` becomes Money-scoped** (lives in Money's variant group → stops floating live-but-inert over other views = **combo C resolved**); **`#coloradj`** likewise Money-only in ③ (already greys today). | §5.A, §5.C |
| 2026-07-23 | **`Residential only` fade lens renamed → "Highlight residential"** — kills the §5.E name clash with the `Residential $` metric (both now Money-scoped and adjacent). Intent-first label; the control fades non-residential hoods. **Label-only — no mechanics, no scope change.** `Residential $` metric keeps its name (the `$` disambiguates; pairs with `Non-res $`). | §5.E |
| 2026-07-23 | **Development's `#dev-grid` checkbox + `#devspike` picker collapse into ONE 3-way "Detail" selector** — siblings, no progressive-disclosure-by-checkbox: **① Neighbourhood** (choropleth, default) · **② 100 m grid — activity** (today's "New homes" spikes) · **③ Stock age** (today's buried "Year built"). Metric + Window apply to ①/②; ③ hides Metric+Window as an EXPLICIT mode choice (defuses the surprise morph). Motivated by phone usability — the nested checkbox reveal is a weak tap target on small screens; flattening to one radio row is what mobile wants (structure-before-mobile: fix the shape here, mobile CSS inherits it). Resolves combos **A** (Year built no longer buried) + **B** (morph is now chosen, not surprising). | §5.A, §5.B; `docs/MOBILE_USABILITY.md` |
| 2026-07-23 | **Industrial (`#devmetric`) tagged full-only** — pulled out of the *public* Development panel (joins Infill as a `/full/`-only Dev extra). Rationale: Industrial is choropleth-only (no 100 m grid, no stock age), so in public it would leave the new 3-way Detail selector (decision #7) with two dead options; removing it makes **public Development airtight — units + permits only, both grid-capable, Detail selector never has a dead option.** `/full/` keeps Industrial as a metric (pinning Detail to Neighbourhood is fine in the specialist build). Resolves combo **F**. | §5.F, two-build tag surface (§2) |

---

## 6. Discrepancy found while mapping (fixed)

The comment at `web/index.html` ~L2952 claimed the long "Since 2009" window is
choropleth-only ("the Detail toggle hides for either"). That's **stale** — PR #80
made the long window first-class with its own grid; `devGridOfferable` excludes
only Industrial. Comment corrected 2026-07-22 to match the code. (No behaviour
change — the code was already correct.)

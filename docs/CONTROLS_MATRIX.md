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

## 2. Tier 1 — the seven views (`#views`)

`Money · Services · Ratio · Uses · Development · Infill · Glass`

**Build visibility (public vs specialist).** The two-build split (DECISIONS
2026-07-22; `docs/PLAN_public_release.md` §2a) tags each lens `public | full`.
This is the **same decision surface as regrouping** — finalize both in the
"organize the lenses" pass, not separately. Provisional tags:

| View | Public build | Specialist (`/full/`) |
|---|:---:|:---:|
| Money · Services · Ratio · Uses · Glass | ✅ | ✅ |
| **Development** | ✅ (moved public, Peter 2026-07-22) | ✅ |
| **Infill** | ❌ | ✅ |
| Deep data-detail (validation ratios, modeling quirks, methods-heavy blurbs) | trimmed to honest labels | ✅ full |

Sub-metrics inherit their view's tag unless split out during regrouping (e.g. if
Industrial leaves Development, it gets its own tag then).

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

## 7. Regrouping decisions (locked, not yet built)

The running output of the "organize the lenses" pass. Each locks a piece of the
regrouped structure; the code edit is deferred to ONE "build once" pass after the
whole regroup settles (don't reflow `index.html` twice). Mirror to `DECISIONS.md`.

| When | Decision | Resolves |
|---|---|---|
| 2026-07-22 | **Glass → a render-mode of Money, not a top-level view.** `#views` drops 7→6; Glass becomes a grid/translucent toggle inside Money (it already reuses Money's `#toggle` + `#coloradj` + denominator). | §5.C, §5.D, §5.G |
| 2026-07-23 | **Infill → a full-only mode of Development, not a top-level view.** `#views` drops 6→5 (Money · Services · Ratio · Uses · Development). Shares `#devmetric`/`#devwindow` already. Unlike Glass, Infill does NOT share Development's build tag: Development is public, Infill is full-only → the Infill toggle appears ONLY in the `/full/` build (`BUILD`-flag-gated at the control level). Public build's Development = activity only; specialist's = activity + Infill toggle. | §5.F-adjacent, two-build tag surface (§2) |

---

## 6. Discrepancy found while mapping (fixed)

The comment at `web/index.html` ~L2952 claimed the long "Since 2009" window is
choropleth-only ("the Detail toggle hides for either"). That's **stale** — PR #80
made the long window first-class with its own grid; `devGridOfferable` excludes
only Industrial. Comment corrected 2026-07-22 to match the code. (No behaviour
change — the code was already correct.)

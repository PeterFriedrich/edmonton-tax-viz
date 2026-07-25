# Lens Inventory — everything that currently exists in the map

_Regenerated 2026-07-25 from the control wiring in `web/index.html` — `#views`,
`#toggle`, `#layers` and its per-view sections, `#coloradj`, `#lens`, the `#a11y`
"Display" popover, and the `applyView`/`syncDevControls`/`syncColorAdjust`
visibility gates. This is the "what can the user actually do" catalogue; for the
*why* see `SPEC_*.md` + `docs/UI.md`, and for the control **state space** (tiers,
what gates what, open oddities) see `docs/CONTROLS_MATRIX.md`._

**This replaces the pre-regroup 7-view catalogue.** The regroup shipped
2026-07-23: Glass became a Money render-mode, Infill a Development lens, palette
and Labels moved into the Display popover, and Development's grid checkbox +
spike picker collapsed into one 3-way Detail selector.

---

## Two builds

The same `index.html` ships twice; a deploy step rewrites `DEFAULT_BUILD`
(`BUILD` / `FULL_BUILD`, ~L532–539). Append `?build=public` or `?build=full` to
override for testing.

| | Public root | Specialist `/full/` |
|---|---|---|
| Views | Money · Services · Ratio · **Development** | + **Uses** |
| Development extras | — | **Infill opportunity** lens · **Industrial** metric |

Everything else is identical. Full-only pieces are hidden at the control level
(`|| !FULL_BUILD` next to their data guard), not stripped from the file.

## Global chrome (every view)

| Control | Options | Notes |
|---|---|---|
| **Display** popover (`#a11y`) | **Colour ramp**: Inferno · Glow · Cividis · **Neighbourhood labels** on/off | Off the top stack since the regroup. Cividis is the CVD-safe ramp; default Inferno applies without opening the menu. Labels auto-declutter and multiply on zoom. |
| **Compass** (`#compass`) | rotate ccw · needle · rotate cw | Camera only. Arrows walk to the next 30° detent; the needle snaps north-up **in place** (bearing only). |
| **Center 2D / Center 3D** | — | Camera only. Reframes the whole city (contrast with the needle). |

Camera chrome gates nothing and shows everywhere — it sits outside the tier
system in `CONTROLS_MATRIX.md`.

## Modifier pods — and the three ways they handle "doesn't apply here"

| Pod | Bites in | Everywhere else |
|---|---|---|
| `#toggle` — Revenue · Value · Residential $ · Non-res $ | Money (both detail modes) | **HIDDEN** (`display:none`) — Money-scoped since the regroup |
| `#lens` — **Highlight residential** | Money → Neighbourhood, Ratio | **HIDDEN** + `disabled` (2026-07-25; greyed read as *broken*) |
| `#coloradj` — `Colour: sqrt scaling` / `Colour: linear` | Money (both detail modes) | **GREYED** (`.disabled`) — the remaining inconsistency; see below |

The button label **is** the state readout for `#coloradj` (no caption since
2026-07-25). ⚠️ **Open decision:** `#coloradj` still greys where `#lens` now
hides, so the two pods in the same column behave differently — in Development you
get a lone dim "Colour: sqrt scaling". Tracked in `TODO.md` + `DECISIONS.md`
2026-07-25; decide as a pair.

> ⚠️ **Highlight residential** (a *fade lens* on ≥50% residential zoned area) is
> **not** the **Residential $** metric (residential-class tax dollars). Different
> features; they compose in Money. The rename killed the older "Residential only"
> name clash but the two still sit adjacent.

---

## The 4 (public) / 5 (full) views

### 1. Money *(default)*
The revenue/value prisms — the money plane.
- **Metric** (`#toggle`): **Revenue** ($/acre) · **Value** (assessed $/acre) ·
  **Residential $** (residential-class tax $/acre — a subset of Revenue) ·
  **Non-res $** (non-residential-rate tax $/acre — the complement). The last two
  are column-guarded (hidden on older data), **not** build-gated: public gets all
  four.
- **Detail** (`#moneydetail`): **Neighbourhood** (solid hood prisms, default) ·
  **100 m grid** — internally the `glass` view: translucent grid-cell spikes over
  a neutral hood plane. Offered unconditionally (graceful fallback if the grid
  file is missing).
- **Denominator** (`#denom`): **Ground acres** (whole footprint, default) · **Lot
  acres** (parcel land owned). Header relabels to **"Spike denominator"** in the
  100 m grid mode. Gated on `hasHoodLot` (hood) / `gridData.hasLot` (grid).
- `#coloradj` **live in both** detail modes. `#lens` **live in Neighbourhood
  only** — grid cells carry no residential flag, so it hides when you switch to
  100 m grid *without leaving Money*. (That in-place disappearance is exactly the
  case that made greying-out read as broken.)
- **100 m grid has NO opacity slider** (2026-07-25) — translucency is fixed at
  60% and re-applied on every entry, so a detour through Ratio (5%) can't strand
  it. The blurb no longer mentions a slider.
- Tooltip always shows "**N% of revenue is residential**" (all four metrics).
- **Combinations:** 32 in Neighbourhood (4 metrics × 2 denom × lens × sqrt) + 16
  in 100 m grid (no lens) = **48**.

### 2. Services
City services on the ground — each service is its own toggleable layer; one
drives the colour ramp.
- **Service checkboxes** (independent on/off): **Roads** (m/acre) ·
  **Stormwater** (modeled $/acre) · **Fire** (events/acre/yr) · **Water/sewer**
  (modeled $/acre) · **Transit** (stop-events/acre/day) · **Service cost**
  (modeled roads+fire $/acre). Each row self-gates on its column.
- **Colour driver** radios appear only when **≥2 services are checked** (the
  choice has to be real). Invariant: the driver always names a *checked* service;
  unchecking it hands the ramp to the next one.
- Fire and Transit draw station dots / LRT lines whenever checked, driver or not.
- `#toggle`, `#lens` hidden; `#coloradj` greyed.
- **Combinations:** 63 non-empty checkbox subsets × the driver choice within each.

### 3. Ratio
Ghost prisms of revenue-per-unit over the neutral road network.
- **Ratio denominator** (`#ratio-denom`): **Per road metre** (default) · **Per
  fire event** · **Per service $** (a coverage multiple — reads ≫1× because only
  two services are measured). Shown only when the data offers a real choice
  (`hasFire || hasSvcCost`); roads-only data hides it.
- **Prism-opacity slider** (`#prism-row`, default 5%) — this is the one view that
  also shows the "Money plane" header.
- `#lens` **live**. `#toggle` hidden, `#coloradj` greyed.
- **Combinations:** 3 denominators × lens = **6** core (× slider, continuous).

### 4. Development
New building activity per acre from issued permits.
- **Lens** (`#devmode`, **full build only**, needs `hasInfill`): **Housing
  built** (default) · **Infill opportunity** — internally the `infill` view.
  Shown in both so you can toggle back. Public build never sees this row.
- **Metric** (`#devmetric`, needs `hasPermitsPerAcre`): **Dwelling units**
  (supply) · **Permits** (project density) · **Industrial** (400-series permits
  per acre — **full only**, choropleth-only, and **hidden inside Infill**, where
  the metric silently resets to units).
- **Window** (`#devwindow`): **Last 5 yr** (2021–2025) · **Last 3 yr**
  (2023–2025) · **Since 2009** (whole record). Each gated on its columns.
- **Detail** (`#devdetail`, Housing-built only, needs the dev-grid file and a
  non-Industrial metric): **Neighbourhood** (choropleth, default) · **100 m grid
  — activity** (geocoded permit spikes) · **Stock age** (median construction year
  per cell; gated on the year column). **Stock age hides Metric + Window** — an
  explicit mode choice, not a surprise morph.
- The prism slider shows while the 100 m grid is active.
- Set-aside greenfield land renders in **full colour** here, unlike every other
  lens — that undeveloped land is where much new building lands.
- `#toggle`, `#lens` hidden; `#coloradj` greyed.
- **Combinations:** full = **22** (Housing 16 + Infill 6); public = **13**.

#### Infill opportunity (Development's second lens, full only)
Suitability × activity **mismatch** — one signed diverging metric. Teal =
suitable but quiet (opportunity); orange = building where there's less room
(pressure). Suitability is the inverse of built FAR.
- Shares **Metric** (units · permits — no Industrial) and **Window**; here they
  drive the *activity* side of the mismatch.
- No Detail selector (no infill grid). Per-arm p95 colour clamps; the teal end is
  residential-only — a low-FAR industrial parcel is structurally underused, not
  an infill opportunity, and can still read as pressure.

### 5. Uses *(full build only — provisional, 2026-07-24)*
Each neighbourhood's dominant **zoned land use** (what it's designated for, not
what it yields), over the 2024 Zoning Bylaw geometry.
- **Residential prisms** toggle: height = share of zoned land that is
  residential. The opacity slider (default 35%) appears while they're on.
- Categorical colour legend, not a gradient — the palette ramp is n/a here.
- `#toggle`, `#lens` hidden; `#coloradj` greyed.
- **Combinations:** prisms on/off = **2**.

---

## Quick "what combines with what" matrix

| View | `#toggle` metric | Acre denom | Detail | Ratio denom | Dev metric/window | Service layers | Opacity slider | `#lens` | `#coloradj` |
|---|---|---|---|---|---|---|---|---|---|
| **Money** — Neighbourhood | ✅ 4 | ✅ 2 | ✅ 2 | — | — | — | — | ✅ | ✅ |
| **Money** — 100 m grid | ✅ 4 | ✅ 2 | ✅ 2 | — | — | — | ✖ fixed 60% | ✖ | ✅ |
| **Services** | ✖ | — | — | — | — | ✅ 6 | — | ✖ | ⊘ |
| **Ratio** | ✖ | — | — | ✅ 3 | — | — | ✅ 5% | ✅ | ⊘ |
| **Development** — Housing | ✖ | — | ✅ 3 | — | ✅ 3 × 3 | — | ✅ in grid | ✖ | ⊘ |
| **Development** — Infill 🔒 | ✖ | — | — | — | ✅ 2 × 3 | — | — | ✖ | ⊘ |
| **Uses** 🔒 | ✖ | — | — | — | — | — | ✅ 35% w/ prisms | ✖ | ⊘ |

✅ present and live · ✖ **hidden** · ⊘ **present but greyed** · — not applicable ·
🔒 full build only. Display popover (3 ramps + labels) and the camera chrome apply
in every view.

---

## Where to look in the code

| Thing | Anchor in `web/index.html` |
|---|---|
| Build flag | `DEFAULT_BUILD` / `BUILD` / `FULL_BUILD` ~L532–539 |
| Per-view chrome + defaults | `VIEWS` L933–~1002 (`opacity` is the per-view slider default) |
| Control DOM | `#toggle` L327, `#views` L334, `#coloradj` L346 / `#lens` L349, `#layers` sections L353–459, `#a11y` L461, `#botleft` L477 |
| Visibility gating | `applyView` L3086–~3245 (`prisms`, `moneyDetailShow`, `prismSlider`, `lensApplies`, `denomShow`, `ratioDenomShow`, `devGridShow`) |
| Development gating | `syncDevControls` ~L2984–3020 (`ageUp` hides metric+window; `devmodeShow`) |
| Colour-scaling pod | `syncColorAdjust` ~L2647 |
| Services driver rule | `syncServiceControls` ~L3274 |
| Data-column guards | ~L3470–3548 (each `state.hasX` + the button it hides) |

Verify coverage: `tools/profiling/verify-lens-visibility.js` (lens + colour pod
per view), `verify-glass-no-slider.js` (Money → 100 m grid), `verify-compass.js`
(camera chrome), `verify-controls-clickable.js` (run after any control CSS
change). All from the repo root.

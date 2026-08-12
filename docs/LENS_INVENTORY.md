# Lens Inventory — everything that currently exists in the map

_Regenerated 2026-07-25 from the control wiring in `web/index.html` — `#views`,
`#toggle`, `#layers` and its per-view sections, `#coloradj`, the `#a11y`
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
| Views | Money · **Development** | + **Services · Ratio · Uses · Lab** `beta` |
| Development extras | — | **Infill opportunity** lens · **Industrial** metric |
| Lab experiments | — | **vs city average** (`deviation`) |

⚠️ **The Views row was STALE and is corrected 2026-08-11 (measured, not
inferred):** it listed Services and Ratio as public, but both were pulled to
full-only on **2026-07-28** (`CONTROLS_MATRIX.md` §2, `DECISIONS.md`), three
days after this file was last regenerated. Probed in the running public build:
`#views` offers exactly `money, development`. ⚠️ **The rest of this file has
NOT been re-probed since 2026-07-25** — treat per-view detail below as
possibly-stale and re-generate from the code before relying on it.

Everything else is identical. Full-only pieces are hidden at the control level
(`|| !FULL_BUILD` next to their data guard), not stripped from the file.

## Global chrome (every view)

| Control | Options | Notes |
|---|---|---|
| **Display** popover (`#a11y`) | **Colour ramp**: Inferno · Glow · Cividis · **Neighbourhood labels** on/off · **Landmarks & nearby places** on/off (2026-07-27) | Off the top stack since the regroup. Cividis is the CVD-safe ramp; default Inferno applies without opening the menu. Labels auto-declutter and multiply on zoom. The reference set (North Saskatchewan River + Anthony Henday + 7 regional place names) defaults **ON** — with no basemap tiles it is the map's only orientation cue. One checkbox, three things: river under the data, ring road over it, and the place names inside the shared label layer — which the **Neighbourhood labels** box co-owns, each gating its own class, so either can be on alone. |
| **Compass** (`#compass`) | rotate ccw · needle · rotate cw | Camera only. Arrows walk to the next 30° detent; the needle snaps north-up **in place** (bearing only). |
| **Center 2D / Center 3D** | — | Camera only. Reframes the whole city (contrast with the needle). |

Camera chrome gates nothing and shows everywhere — it sits outside the tier
system in `CONTROLS_MATRIX.md`.

## Modifier pods — and the three ways they handle "doesn't apply here"

| Pod | Bites in | Everywhere else |
|---|---|---|
| `#toggle` — **two rows**: Revenue \| Value, with Total \| Residential \| Non-residential nested under Revenue (2026-07-26) | Money (both detail modes) | **HIDDEN** (`display:none`) — Money-scoped since the regroup |
| `#coloradj` — `Colour: sqrt scaling` / `Colour: linear` | Money (both detail modes) | **HIDDEN** + `disabled` (2026-07-26; greyed read as *broken*) |

The button label **is** the state readout for `#coloradj` (no caption since
2026-07-25), and **nothing greys any more** — it hides where it doesn't apply.

> **`#lens` (Highlight residential) was REMOVED 2026-07-26.** It faded
> neighbourhoods below 50% residential zoned area — a *binary* cut, which the
> continuous alternatives now do better: the **Residential** revenue cut in
> `#toggle` shows residential dollars directly, and every tooltip already carries
> `X% of revenue is residential`. Its removal also emptied `#opt-pres`, so that
> wrapper is gone and `#coloradj` moved to the bottom of the Options panel.
> `DECISIONS.md` 2026-07-26.

---

## The 2 (public) / 6 (full) views

### 1. Money *(default)*
The revenue/value prisms — the money plane.
- **Metric** (`#toggle`) — **two levels since 2026-07-26.** Row 1 is the
  *quantity*: **Revenue** ($/acre) · **Value** (assessed $/acre). Row 2, shown
  only under Revenue, is *which classes*: **Total** (default) · **Residential**
  (houses, condos, apartments) · **Non-residential** (commercial + industrial
  rate slices).
  - The nesting is the data's own shape: `levy == res + nonres + farmland`
    (`DECISIONS.md` 2026-07-18), so the cuts are genuine subsets of Total. They
    do **not** sum to it exactly — farmland is a small separate class.
  - **Value is a leaf** and the row hides under it: the pipeline emits no
    res/nonres decomposition of assessed value.
  - The two cuts stay column-guarded (hidden on older data files, and the whole
    row collapses if neither exists), **not** build-gated: public gets all four
    combinations. Still 4 reachable metrics — this regrouped them, it did not
    add or remove any.
- **Detail** (`#moneydetail`): **Neighbourhood** (solid hood prisms, default) ·
  **100 m grid** — internally the `glass` view: translucent grid-cell spikes over
  a neutral hood plane. Offered unconditionally (graceful fallback if the grid
  file is missing).
- **Denominator** (`#denom`): **Ground acres** (whole footprint, default) · **Lot
  acres** (parcel land owned). Header relabels to **"Spike denominator"** in the
  100 m grid mode. Gated on `hasHoodLot` (hood) / `gridData.hasLot` (grid).
- `#coloradj` **live in both** detail modes.
- **100 m grid has NO opacity slider** (2026-07-25) — translucency is fixed at
  60% and re-applied on every entry, so a detour through Ratio (5%) can't strand
  it. The blurb no longer mentions a slider.
- Tooltip always shows "**N% of revenue is residential**" (all four metrics).
- **Combinations:** 16 in Neighbourhood (4 metrics × 2 denom × sqrt) + 16 in
  100 m grid (same three) = **32**. _Was 48 until 2026-07-26; removing the
  residential lens dropped a ×2 factor from the Neighbourhood mode._

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
- `#toggle` and `#coloradj` both hidden — the Options panel holds only `#layers`.
- **Hood panel (2026-08-10):** clicking a hood shows its revenue per acre against
  each service cost, **grouped by basis and with no total** — two locked no-sum
  rules make a single cost figure impossible (`SPEC_services.md` "Hood panel").
  This is the lens's own panel, not the assessment history, which stays gated out.
- **Combinations:** 63 non-empty checkbox subsets × the driver choice within each.

### 3. Ratio
Ghost prisms of revenue-per-unit over the neutral road network.
- **Ratio denominator** (`#ratio-denom`): **Per road metre** (default) · **Per
  fire event** · **Per service $** (a coverage multiple — reads ≫1× because only
  two services are measured). Shown only when the data offers a real choice
  (`hasFire || hasSvcCost`); roads-only data hides it.
- **Prism-opacity slider** (`#prism-row`, default 5%) — this is the one view that
  also shows the "Money plane" header.
- `#toggle` and `#coloradj` hidden — the Options panel holds only `#layers`.
- **Combinations:** **3** denominators (× slider, continuous). _Was 6 until
  2026-07-26 — the residential lens was the other factor._

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
  — activity** (geocoded permit spikes). A third option, **Stock age**, shipped
  2026-07-17 and was **withdrawn 2026-07-27** (`DECISIONS.md`); Metric and
  Window now apply in both modes.
- The prism slider shows while the 100 m grid is active; the spikes **default to
  50%** (`VIEWS.development.opacity`, 2026-07-27) so the hood plane reads
  through them.
- Set-aside greenfield land renders in **full colour** here, unlike every other
  lens — that undeveloped land is where much new building lands.
- `#toggle` and `#coloradj` both hidden — the Options panel holds only `#layers`.
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
- `#toggle` and `#coloradj` both hidden — the Options panel holds only `#layers`.
- **Combinations:** prisms on/off = **2**.

---

### 6. Lab *(full build only, `beta` — NEW 2026-08-11)*

**A container, not a lens.** The `#views` button opens whichever experiment was
last active (`state.lab`); `LAB_EXPERIMENTS` is the registry. Hidden entirely in
the public build by the one-time `if (!FULL_BUILD)` block, which is a *different*
gate from the `|| !FULL_BUILD` pattern the other full-only pieces use — the Lab
has no data dependency, so nothing else would keep it off the published page.

| Control | Options | Notes |
|---|---|---|
| `#labpick` | one button per experiment | **Hidden while there is only one** — a chooser with one option is not a choice (the `syncServiceControls` rule). Rendered from the registry, so adding an experiment needs no markup. |
| `#labcut` | Total · Residential · Non-residential | The **Lab's own** copy of Money's revenue cuts, driving `state.labCut`. ⚠️ **Deliberately not shared with `#revcut`** — see below. |

`#toggle` (Money's metric pod) is **hidden** in the Lab, unlike `change` and
`glass` which keep it.

#### vs city average (`deviation`)

Each hood's revenue per acre re-centred on the citywide average
(**$14,049/acre**, Σ`total_revenue` ÷ Σ acres from the served features — never
an external total). **Extruded, and the deficit half extrudes BELOW the ground
plane** — the only lens that does; height is true to scale on Money's own
`elevationScale`, so a bar is comparable to the same hood's bar on the Revenue
map. Colour is the diverging `infillColorAt` ramp at a per-arm p95 clamp.

⚠️ **Not a cost-of-service comparison, and must never be named as one** (no
"COSA", no "cost of service" in code, columns, filenames or copy).
`verify-deviation.js` greps the rendered copy for both.

⚠️ **It reads `state.labCut`, NEVER `state.metric`.** It first shipped as a
`#moneymode` button where those were one variable; entering from the Value map
would have averaged assessed value and printed it under a "Revenue" title.

## Quick "what combines with what" matrix

| View | `#toggle` metric | Acre denom | Detail | Ratio denom | Dev metric/window | Service layers | Opacity slider | `#coloradj` |
|---|---|---|---|---|---|---|---|---|
| **Money** — Neighbourhood | ✅ 4 | ✅ 2 | ✅ 2 | — | — | — | — | ✅ |
| **Money** — 100 m grid | ✅ 4 | ✅ 2 | ✅ 2 | — | — | — | ✖ fixed 60% | ✅ |
| **Services** | ✖ | — | — | — | — | ✅ 6 | — | ✖ |
| **Ratio** | ✖ | — | — | ✅ 3 | — | — | ✅ 5% | ✖ |
| **Development** — Housing | ✖ | — | ✅ 3 | — | ✅ 3 × 3 | — | ✅ in grid | ✖ |
| **Development** — Infill 🔒 | ✖ | — | — | — | ✅ 2 × 3 | — | — | ✖ |
| **Uses** 🔒 | ✖ | — | — | — | — | — | ✅ 35% w/ prisms | ✖ |

✅ present and live · ✖ **hidden** · — not applicable · 🔒 full build only.
Display popover (3 ramps + labels + the river/ring-road reference layer) and
the camera chrome apply in every view.
**There is no "present but greyed" state left** — the last one (`#coloradj`)
became a hide on 2026-07-26. The `#lens` column is gone from this table because
the control was removed the same day.

---

## Where to look in the code

**Grep for the symbol, not the line number.** These anchors carried line numbers
until 2026-07-26, when they went stale twice in a single day (the metric regroup
and the lens removal both shifted `web/index.html` by ~200 lines). Symbols are
greppable and cannot rot silently, so that is all this table records now.

| Thing | Anchor in `web/index.html` (grep it) |
|---|---|
| Build flag | `DEFAULT_BUILD` / `BUILD` / `FULL_BUILD` |
| Per-view chrome + defaults | `const VIEWS` (`opacity` is the per-view slider default) |
| Control DOM | `#toggle` (`#metric-row` + `#revcut`), `#views`, `#layers` sections, then `#coloradj` LAST inside `#opt-body`, `#a11y`, `#botleft` |
| Visibility gating | `function applyView` — `prisms`, `moneyDetailShow`, `prismSlider`, `denomShow`, `ratioDenomShow`, `devGridShow` (`lensApplies` is GONE — lens removed 2026-07-26) |
| Metric picker (2 levels) | `REV_CUTS`, `isRevenue`, `lastRevCut`, `syncMetricButtons` |
| Development gating | `syncDevControls` (`ageUp` hides metric+window; `devmodeShow`) |
| Colour-scaling pod | `syncColorAdjust` |
| Services driver rule | `syncServiceControls` |
| Data-column guards | `state.hasResRevenue` / `hasNonresRevenue` / `hasHoodLot` / … (each paired with the button it hides) |

Verify coverage: `tools/profiling/verify-coloradj.js` (the colour pod per view;
replaced `verify-lens-visibility.js` when the lens was removed),
`verify-money-metric-group.js` (the two-level metric picker),
`verify-glass-no-slider.js` (Money → 100 m grid), `verify-compass.js` (camera
chrome), `verify-controls-clickable.js` (run after any control CSS change). All
from the repo root.

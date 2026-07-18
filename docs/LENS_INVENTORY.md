# Lens Inventory — everything that currently exists in the map

_Generated 2026-07-16 from the live control wiring in `web/index.html`
(`#views`, `#toggle`, `#lens`, `#palette`, `#coloradj`, and the per-view
`#layers` sections). This is the "what can the user actually do" catalogue —
for the *why* and methodology see the SPEC_*.md docs and `docs/UI.md`._

## Global controls (every view)

| Control | Options | Notes |
|---|---|---|
| **Palette** | Inferno · Glow · Cividis | Colour ramp; applies to any coloured layer. |
| **Labels** | on / off | Neighbourhood names; auto-declutter, more appear on zoom. |

## Colour scaling & the residential fade lens (view-scoped)

| Control | Where it's LIVE | Where it's OFF/disabled |
|---|---|---|
| **Colour: sqrt scaling** (on = spread across ramp / off = linear+clamp) | Money, Glass | Disabled in Services, Ratio, Uses, Development, Infill (colour there is driven by a fixed scale, not the money metric) |
| **Residential only** lens (fades non-residential hoods; re-clamps to the residential subset) | Money, Ratio | Disabled in Services, Uses, Glass, Development, Infill |

> ⚠️ "Residential only" (a **fade lens** on the zoned-area threshold
> `is_residential`, ≥50% residential zoned area) is **not** the same as the
> **Residential $** money metric (residential-class tax *dollars*). Different
> features; they can compose in the Money view.

---

## The 7 views and their controls

### 1. Money  *(default)*
The revenue/value prisms — the money plane.
- **Metric** (`#toggle`): **Revenue** ($/acre) · **Value** (assessed $/acre) · **Residential $** (residential-class tax $/acre — a subset of Revenue) · **Non-res $** (non-residential-rate tax $/acre — the complement of Residential $; commercial + industrial land). *The two decomposition metrics are column-guarded — hidden on older data files.*
- **Denominator**: **Ground acres** (whole footprint — default) · **Lot acres** (parcel land owned — land productivity). *Shown only when the data carries the lot-acre columns.*
- Colour-sqrt toggle: **live**. Residential fade lens: **live**.
- Tooltip always shows "**N% of revenue is residential**" (all four metrics).
- **Combinations:** 4 metrics × 2 denominators × (lens on/off) × (sqrt on/off) = up to **32** core states.

### 2. Services
City services on the ground — each service is its **own toggleable layer**; one drives the colour ramp.
- **Service checkboxes** (independent on/off): **Roads** (metres/acre) · **Stormwater** (modeled charge/acre) · **Fire** (dispatched events/acre) · **Water** (modeled charge/acre) · **Transit** (scheduled departures/acre) · **Service cost** (modeled roads+fire $/acre)
- **Colour driver** (radio, one of the *checked* services): picks which layer colours the ground.
- Each checkbox hides itself if its column is absent from the data.
- Residential lens & sqrt toggle: **disabled**.

### 3. Ratio
Ghost prisms of revenue-per-unit over the neutral road network.
- **Ratio denominator**: **Per road metre** (revenue ÷ city-maintained road m — default) · **Per fire event** (revenue ÷ dispatched event) · **Per service $** (revenue ÷ modeled roads+fire cost — a coverage multiple, reads ≫1× because only 2 services are measured)
- Picker shown only when the data offers a real choice (fire and/or service-cost column present); roads-only data hides it.
- Prism-opacity slider. Residential fade lens: **live**. sqrt toggle: disabled.

### 4. Uses
Each neighbourhood's dominant **zoned land use** (what it's designated for, not what it yields).
- **Residential prisms** toggle (on/off): optional prisms showing each hood's residential share.
- Categorical colour legend (not a gradient). Residential lens & sqrt: **disabled**.

### 5. Development
New dwelling activity per acre from issued building permits — where the city is actually growing.
- **Sub-metric**: **Dwelling units** (per acre — housing supply) · **Permits** (per acre — project density) · **Industrial** (new 400-series industrial permits per acre — count only; a hood-level choropleth, no detail grid). *Permits shown when the permit-per-acre column is present; Industrial when `ind_permits_per_acre` is present.*
- **Window**: **Last 5 yr** (2021–2025 — structural) · **Last 3 yr** (2023–2025 — recent). *Shown when the `_3yr` columns are present.*
- **Detail grid** toggle (on/off): 100 m detail cells. *Shown when `dev_grid.json` loaded; **hidden while Industrial is selected** (no industrial cells).*
- Residential lens & sqrt: **disabled**.

### 6. Infill
Suitability × activity **mismatch** — one signed diverging metric (teal = suitable but quiet / opportunity; orange = building where less suitable / pressure).
- **Sub-metric** (units · permits) and **Window** (5yr · 3yr): same two pickers as Development — here they drive the *activity* side of the mismatch. *Industrial is NOT offered here (an industrial permit isn't residential infill — the button hides and the metric resets to a residential column on entering this view).*
- Per-arm p95 colour clamps; opportunity (teal) end is residential-only (non-residential hoods barred from teal, kept on orange).
- Residential lens & sqrt: **disabled**.

### 7. Glass
Translucent metric prisms over a neutral neighbourhood plane (hover the ground for numbers).
- **Metric** (same `#toggle`): Revenue · Value · Residential $ · Non-res $ *(all render 100 m cells; the decomposition metrics fall back to hood prisms on older grid files)*
- **Spike denominator**: Ground acres · Lot acres. *Shown when the grid file carries the lot-acre columns.*
- Colour-sqrt toggle: **live**. Residential lens: **disabled**.

---

## Quick "what combines with what" matrix

| View | Metric toggle | Denominator | Ratio denom | Dev metric/window | Service layers | Res-fade lens | sqrt |
|---|---|---|---|---|---|---|---|
| Money | ✅ 4 | ✅ 2 | — | — | — | ✅ | ✅ |
| Services | — | — | — | — | ✅ 6 | ✖ | ✖ |
| Ratio | — | — | ✅ 3 | — | — | ✅ | ✖ |
| Uses | — | — | — | — | — | ✖ | ✖ |
| Development | — | — | — | ✅ 3 metric × 2 win (+grid; industrial=choropleth) | — | ✖ | ✖ |
| Infill | — | — | — | ✅ 2×2 | — | ✖ | ✖ |
| Glass | ✅ 4 | ✅ 2 | — | — | — | ✖ | ✅ |

Palette (3 ramps) and Labels apply in every view. "—" = control not present; "✖" = present in UI but disabled in that view.

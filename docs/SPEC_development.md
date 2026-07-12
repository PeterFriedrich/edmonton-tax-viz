# Scope: Development & Infill Lens family

**Status:** PLAN (2026-07-12). No code built yet. This doc specs a new lens
family — where building is actually happening, whether it's happening in the
*right* places, and how that lines up against the city's cost to serve. It is
the direct, permit-based answer to the question `FINDINGS_growth_servicing.md`
could only proxy with **median building-stock age** (a hood's `year_built`
median, which infill drags around and which is not the same as current activity).

Three lenses, built one minimal cut at a time so each can be *seen* before the
next is designed (Peter, 2026-07-12: "start with a single of each just to see
them"):

| | Lens | Answers | Phase |
|---|---|---|---|
| **A** | Building Activity | where are new homes actually being built now | 1 (first) |
| **B** | Suitability × Activity | is building happening where it *should* (and where it shouldn't) | 2 |
| **C** | Activity vs City Service Cost | what does the city pay to service where growth is going | 3 / future |

---

## Why

Every existing lens describes the roll as it stands *today* (revenue, services,
utilities per acre). None shows **change** — the flow of new dwellings onto the
land. The growth-servicing findings (`FINDINGS_growth_servicing.md`) approached
this through median `year_built` per hood, and flagged its own core limitation:
"Era = median building stock age, not plat date; heavy-infill mature hoods
drift later." Building permits remove that proxy — they are the dated, located,
counted record of construction itself. This lens family turns that record into
the map, and eventually sets it against the cost side the project already
models.

---

## Data

### Primary — General Building Permits (`24uj-dj8v`)

**Source:** Edmonton Open Data (Socrata), `https://data.edmonton.ca/resource/24uj-dj8v.json`.
**Verified 2026-07-12:** 243,324 rows, `issue_date` 2009-01-05 → 2026-07-09
(current, refreshed on the city's cadence). Reachable from the Oracle box
(`data.edmonton.ca` is; `edmonton.ca` is not).

Columns we use (schema confirmed live):

| field | type | use |
|---|---|---|
| `issue_date`, `year`, `month_number` | date/num | window filter, recency |
| `work_type` | text | **new-vs-alteration split** — see vocab below |
| `building_type` | text | **residential-type filter** — see vocab below |
| `units_added` | number | **dwelling units created** (the activity numerator) |
| `construction_value` | number | private $ value of the work — **available, NOT used** in Lens C (Peter chose city service cost); reserved for a possible future "private capital in" view |
| `floor_area` | number | secondary intensity measure |
| `neighbourhood` | text | **join key** to `neighbourhood_name` (UPPERCASE, matches our format) |
| `neighbourhood_numberr` | text | numeric hood id (backup join key; note the doubled `r` in the real field name) |
| `zoning` | text | permit-time zone (context / suitability input) |
| `latitude`, `longitude`, `geometry_point` | num/point | per-permit location (kept for a possible future point layer; **Lens A is choropleth**, so not needed for phase 1) |

**`work_type` vocab (live counts 2026-07-12, top values):** `(01) New`
(54,184) + `(01) Building - New` (46,391) = the **new-construction set**;
`(07) Add Suites to Single Dwelling` (3,064) = infill densification
(secondary/garden suites); `(03) Interior/Exterior Alterations`, `(02) Addition`,
`(99) Demolition` (9,756), etc. = not new dwellings. ~60k rows have a null/blank
`work_type` — **count and report** them (do not silently include or drop); most
predate consistent coding. Follow the project's explicit-dictionary rule
(DECISIONS 2026-06-29): hand-map the `work_type` codes we treat as "new",
warn on any unseen code, never prefix-match.

**`building_type` vocab (top values):** `Single Detached House (110)` (148,133),
`Detached Garage (010)` (21,140 — **exclude**, not a dwelling), `Semi-Detached
House (210)` (19,659), `Row House (330)` (7,090), `Apartments (310)` (1,908),
plus commercial types (Office/Retail/Warehouse/Restaurant). The **residential
dwelling set** = Single Detached + Semi-Detached + Row House + Apartments
(+ Duplex/other residential codes if present); garages and commercial excluded.
Hand-mapped dictionary, warn-on-unseen, same rule.

### Join & name discipline

Permit `neighbourhood` is UPPERCASE and matches `neighbourhood_name` format
(spot-checked 2026-07-12). **491 distinct** permit hood names vs our **406**
boundary hoods — the surplus is "AREA"-suffixed greenfield names (`CHAPPELLE
AREA`, `THE ORCHARDS AT ELLERSLIE`) and retired/renamed hoods. This is a **new
join**, so it needs the project's no-silent-drops treatment
(`scripts/check_unmatched_names.py` philosophy, T3c) — **but activity is not the
money path**: an unmatched permit hood contributes 0 activity (a visibly blank
hood), not a silently wrong dollar figure. So the guard here is **warn-not-fail**
(log unmatched permit-side names + their unit totals; don't break CI). A name
map for the recurring "AREA" suffixes is the first build task.

### Companion datasets (Lens B / future, not phase 1)

Discovered 2026-07-12, catalogued here so we don't re-hunt:

| id | name | possible use |
|---|---|---|
| `2ccn-pwtu` | Development Permits | upstream of building permits (approvals pipeline) |
| `vd42-umu2` | Mature Neighbourhood Reinvestment | direct "infill in mature areas" signal for Lens B suitability |
| `aq5q-em8z` | Infill Compliance Team Data | infill-specific activity |
| `uz9h-ceya` | Secondary Suites (Completed Permits) | densification (garden/secondary suites) |
| `25sf-z8zd`, `8t7s-6vwq` | Residential Building Permits 2009–2015 | historical snapshots (superseded by `24uj-dj8v`'s full range) |

**DATA.md gets a full entry when the Lens A loader is built** — data details
live here in the spec until then (the project keeps DATA.md for live-pipeline
sources).

---

## Lens A — Building Activity (choropleth) — PHASE 1

**Decision (Peter, 2026-07-12): neighbourhood choropleth**, not a point layer —
same look as the revenue/services lenses, least new render code. (Per-permit
lat/long is retained in the data for a possible future point/heatmap variant,
but not built now.)

**Metric:** `new_dwelling_units_per_acre` = Σ `units_added` per hood
(filtered to new-construction `work_type` ∩ residential `building_type`) ÷
boundary acres (EPSG:3400, the one project denominator), over a **rolling
window**. Secondary sub-metric option: **permit count per acre** (activity
regardless of unit count). Window default **last 5 full calendar years** —
*open decision* (see below); pinned, not auto-rolling-with-partial-year, per the
fire-lens precedent (DECISIONS 2026-07-05).

**⚠️ Set-aside mask — the headline tension (open decision, must resolve before
build):** the top activity hoods verified 2026-07-12 (KESWICK 3,139 units,
CHAPPELLE AREA 2,789, THE ORCHARDS 2,755, EDGEMONT, SECORD, GRIESBACH,
ROSENTHAL) are exactly the greenfield hoods the **set-aside overlay greys out**
on every other lens — they read near-zero *revenue* per acre because they're
≥90% not-yet-developed land. Reusing that mask here would **grey out the entire
story of the activity lens.** Lens A almost certainly must **override / invert
the set-aside treatment** (show greenfield growth hoods in full colour; the
undeveloped land IS where the units are landing). Exact handling is a locked-in
decision to make with Peter before building — it is the single biggest design
call in this lens.

**Computation (new module `src/load_permits.py` → column into
`join_and_calculate`):**
1. Download `24uj-dj8v` (Socrata full-export discipline from DATA.md §1:
   post-download count vs. server `count(*)`, atomic `.part` write).
2. Filter: `work_type` ∈ new-set (dict), `building_type` ∈ residential-set
   (dict), `issue_date` in window; report null-`work_type` and dropped rows.
3. Group by `neighbourhood`, Σ `units_added` (and count), name-normalize +
   warn-not-fail unmatched (above).
4. Merge onto the hood frame with `validate="m:1"` (NEW-1 discipline) → new
   columns `new_units_<window>`, `new_units_per_acre_<window>`.
5. Web: register a new choropleth metric in the lens/views control
   (`web/index.html`, same pattern as the services metrics ~line 332+), diverging
   or sequential palette per `dataviz` skill; tooltip line `new homes / acre`
   (escaped via the `esc()` helper, S3).

**First-cut "just to see it":** one metric (`new_units_per_acre`, 5-yr window),
choropleth, set-aside overridden. Ship, look, iterate.

---

## Lens B — Suitability × Activity mismatch — PHASE 2

**Decision (Peter, 2026-07-12): activity-adjusted, shown both ways.** Not a
static suitability score — the interesting thing is the **mismatch** between how
suitable a hood is for infill and how much is actually being built there:

- **Opportunity view:** high suitability, **low** activity → suitable but quiet
  (where infill *should* go but isn't).
- **Flipped / pressure view:** **low** suitability, high activity → "which less
  suitable areas are getting more built" (Peter's words) — building landing
  where servicing/fit is weaker.

Peter: "possibly as separate but just flipped of course" → implement as **one
signed diverging metric** (e.g. `z(suitability) − z(activity)`: positive = quiet
opportunity, negative = building-in-less-suitable), with the two views being the
two ends of the same diverging scale — plus optionally the two one-sided
choropleths.

**Base suitability score (the open design work):** a composite of ingredients we
can already compute, *pick ONE simple proxy for the first cut* and refine:
- **Serviced/mature** — infrastructure already sunk (mature-area proxy: older
  median `year_built`, or the `vd42-umu2` Mature Neighbourhood overlay).
- **Underused** — room to add: low improvement-to-land value ratio and/or larger
  median lot (assessment + `dkk9-cj3x` `lot_size`).
- **Zoning headroom** — zoned density minus built density (what the bylaw already
  permits vs what exists).

Base-suitability weighting/definition is **open** — do not lock until Lens A is
visible and we can eyeball the activity distribution against candidate scores.

---

## Lens C — Activity vs City Service Cost — PHASE 3 / FUTURE

**Decision (Peter, 2026-07-12): city service cost**, reusing the project's
modeled service columns (road m/acre, storm $/acre, water $/acre, fire ev/acre),
or the **V2 unit-cost composite** ($/acre in real dollars — laptop-gated, needs
published unit costs; `SPEC_utilities.md` decision 3, `FINDINGS_growth_servicing.md`
§6.2/§8). Sets **where new building is going** (Lens A) against **what the city
pays to service that land** — the two-ledger idiom of `FINDINGS_growth_servicing.md`
made spatial.

**`construction_value` (private builder cost) is explicitly NOT this lens**
(Peter's call) — noted in Data as a reserved field for a possible separate
"private capital in" view, never merged into the city-cost story (money-flow
honesty, same rule as DECISIONS 2026-07-10).

Depends on Lens A shipping and (for true dollars) the V2 unit-cost work.

---

## Locked decisions (2026-07-12) — mirror into DECISIONS.md

1. **Activity lens = neighbourhood choropleth** (new dwelling units per acre),
   not a per-permit point layer — reuses the existing render, points retained
   in data for a future variant.
2. **Infill lens = suitability × activity mismatch, shown both ways** (suitable-
   but-quiet AND less-suitable-but-building) — a signed diverging metric, not a
   static suitability score.
3. **Combined lens cost side = modeled city service cost** (reuse service
   columns / V2 unit costs), NOT permit `construction_value`.

## Methodology decisions still to settle (open — resolve at build time)

- **Set-aside handling for Lens A** (the headline tension above) — override /
  invert so greenfield growth hoods show. *Highest priority; blocks the build.*
- **Activity window** — 5 full years default? single latest year? cumulative
  since 2009? (fire-lens precedent: pinned, not partial-year auto-roll.)
- **Metric numerator** — `units_added` (dwellings) vs permit count vs
  `construction_value`-weighted vs `floor_area`. Default `units_added`.
- **Null-`work_type` rows** (~60k) — report count; decide include/exclude
  (default exclude, warn).
- **Lens B base-suitability definition + weighting** — pick one proxy first.
- Whether the "AREA"-suffix greenfield names get a maintained name map or are
  accepted as a documented unmatched set.

## Build order

1. **Lens A minimal** — `src/load_permits.py` + name map + `join_and_calculate`
   column + one choropleth metric + set-aside override. Verify (headless), ship,
   look. Add the DATA.md entry at this point.
2. **Lens A polish** — window/metric toggles, sub-metrics, tooltip.
3. **Lens B** — base suitability proxy + signed mismatch metric + two views.
4. **Lens C** — reuse service-cost columns (or V2) against Lens A.

## Cross-refs

- `FINDINGS_growth_servicing.md` — the median-age proxy this replaces; the two-
  ledger framing Lens C makes spatial; ASP/IIMP greenfield context.
- `SPEC_services.md` — the lens/metric + web-toggle pattern Lens A mirrors.
- `SPEC_utilities.md` decision 3 / V2 unit costs — Lens C cost side.
- `data/DATA.md` §1–2 — Socrata download discipline; `dkk9-cj3x` `year_built`/
  `lot_size` inputs for Lens B suitability.
- `scripts/check_unmatched_names.py` (T3c) — the name-guard philosophy the
  permit join extends (warn-not-fail, activity side).
- `docs/PARCEL_LEVEL_OPPORTUNITIES.md` — permits are point-located; a parcel-
  level activity map is the finer-grained future once parcel geometry is available.

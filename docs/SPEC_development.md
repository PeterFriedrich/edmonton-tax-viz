# Scope: Development & Infill Lens family

**Status:** Lens A **BUILT + shipped** (2026-07-12, branch
`feat/dev-lens-a-building-activity`); Lens B/C still PLAN. This doc specs a new
lens family — where building is actually happening, whether it's happening in the
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
**Verified 2026-07-12:** 243,371 rows, `issue_date` 2009-01-05 → 2026-07-09
(current, refreshed on the city's cadence). Reachable from the Oracle box
(`data.edmonton.ca` is; `edmonton.ca` is not).

**"Same data, different cuts" — verified 2026-07-12.** The portal lists eight
building/development-permit datasets, but the `rowsUpdatedAt` timestamps prove
there are only TWO source tables: all six building-permit views (this
`24uj-dj8v`, plus `itki-s8y9` Map Search — identical 243,371 row count —
`jsf3-5dv2` Commercial Final, `537d-t4az` Permitted Projects, `uep4-4w4g`
Permits >$1M, `ramb-ihnk` Activity) share one timestamp; both development-permit
views (`2ccn-pwtu`, `66ut-y7w2` Map Search) share another. The rest are saved
filters/map views we can't control. **We pull `24uj-dj8v` (tabular API) and do
our own filtering — ignore the derived views.**

**`occupancy_granted_date` variant (field confirmed 2026-07-12, NOT built).**
The schema carries `occupancy_granted_date` — a *completed-builds* cut vs. our
*issued-permits* cut. Caveat that gates it: the city only populates it for
residential finalized on/after Jan 1 2022 and non-residential on/after Jan 1
2024, so it is fine for a "recently completed" leading/lagging distinction but
**useless for historical totals** (pre-2022 completions are blank). A future
optional Lens-A toggle, not the base metric.

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

**`building_type` vocab (top values):** `Single Detached House (110)` (148,170),
`Detached Garage (010)` (21,140 — **exclude**, not a dwelling), `Semi-Detached
House (210)` (19,660), `Row House (330)` (7,093), `Apartments (310)` (1,908),
plus commercial types (Office/Retail/Warehouse/Restaurant). The **residential
dwelling set** = Single Detached + Semi-Detached/Duplex + Row House + Apartment
+ Mobile Home. **The live vocab (71 distinct values, 2026-07-12) carries many
spelling variants of each** — `Apartments (310)`/`Apartment (310)`/`Apartment
Condos (315)`/`Apartment Condo (315)`; `Row House (330)`/`Row Houses (330)`/
`Row House Condo (335)`; `Semi-Detached House (210)`/`Semi Detached House (210)`/
`Semi Detached House` (no code)/`Duplex (210)`/`Semi-Detached Condo (215)`;
`Single Detached House (110)`/`Single House (110)`/`Single Detached Condo (115)`/
`Backyard House (110)` (a new garden/secondary dwelling — counted). `Mixed Use
(522)` is commercial-coded and ambiguous on unit count — **excluded** from the
first cut. Every variant is enumerated explicitly in `src/load_permits.py`
(`RESIDENTIAL_BUILDING_TYPES`), never prefix-matched on the `(NNN)` code;
garages and commercial excluded. Hand-mapped dictionary, warn-on-unseen.

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

**DATA.md entry added 2026-07-12** (Lens A loader built) — see DATA.md
§"Building Permits" for the live-pipeline source record.

---

## Lens A — Building Activity (choropleth) — PHASE 1

**Decision (Peter, 2026-07-12): neighbourhood choropleth**, not a point layer —
same look as the revenue/services lenses, least new render code. (Per-permit
lat/long is retained in the data for a possible future point/heatmap variant,
but not built now.)

**Metric (BUILT):** `new_units_per_acre` = Σ `units_added` per hood
(filtered to new-construction `work_type` ∩ residential `building_type`) ÷
boundary acres (EPSG:3400, the one project denominator), over the pinned window.
The loader also carries `new_dwelling_units` (window total) and
`new_dwelling_permits` (count) into the slim file for the tooltip. **Window
LOCKED (Peter, 2026-07-12): the last 5 full calendar years (2021–2025)**,
summed — `PERMIT_YEARS` in `main.py`, pinned (a drift guard hard-errors if a
window year has zero permits), not auto-rolling-with-partial-year, per the
fire-lens precedent (DECISIONS 2026-07-05). Permit-count-per-acre is a possible
future sub-metric (the count already ships); not a toggle in the first cut.

**✅ Set-aside mask — LOCKED (Peter, 2026-07-12): full override, coloured.** On
Lens A the mask greys nothing — every hood is coloured by its activity value,
greenfield included; a hood's set-aside status still shows in the tooltip.
Implemented as a dedicated `developmentPlaneLayer` with no `is_set_aside` grey
branch and a `devScale` clamp computed over ALL hoods (`web/index.html`).

**Empirical footnote (measured on the real join, 2026-07-12):** the "headline
tension" turned out largely moot for *current* data. The set-aside flag is
`set_aside_frac ≥ 0.90`, and the growth hoods sit far below it (KESWICK 0.19,
CHAPPELLE 0.27, SECORD 0.11, GRIESBACH 0.10) — they've developed enough to render
on-scale already. Only **6 tiny set-aside hoods carry any activity, 43 units of
59,696 citywide (0.07%)**. The override is still the correct semantic choice and
future-proofs newly-platted greenfield (which starts ≥90% undeveloped AND high
activity), but its present visual impact is negligible.

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

**Base suitability score — LOCKED 2026-07-13 (Peter): built floor-area ratio
(FAR), the "underused / room to add" proxy.** `far` = Σ building floor area
(`Total Gross Area`, `dkk9-cj3x`) ÷ deduped lot area per hood — computed in
`build_hood_lot_acres` on the same eligible-point dedupe as the lot-acre
denominator (floor area summed per unit, land counted once per point). **Low FAR
= underused = suitable.** The other candidates considered and rejected for the
first cut:
- **Serviced/mature** (median `year_built`, or the `vd42-umu2` overlay) — its
  mismatch mostly re-derives the greenfield-vs-infill / median-age story this
  lens moves beyond; `vd42-umu2` also needs a new download.
- **Underused via value** (low value/lot-acre) — cheapest (already on the
  geojson) but conflates "underused" with "low land value" (a high-value
  downtown lot reads as un-suitable). *Note: the assessment roll has only a
  single `Assessed Value` — NO land/improvement split — so the classic teardown
  improvement-to-land ratio is unavailable.*
- **Zoning headroom** (zoned density − built density) — needs a zoning→max-density
  lookup table; a refinement, not a first cut.

**Architecture:** the pipeline emits the raw `far` ingredient only; the web
computes the signed diverging mismatch **`z(suitability) − z(activity)` =
`−(z(far) + z(activity))`** live in the `Infill` view, so it responds to the
existing units/permits × 5yr/3yr Lens-A toggles for free. Both terms are
standardised over the SAME included population; the score is clamped
symmetrically at p95 of `|score|` and rendered on a dark-centred diverging ramp
(teal = positive/opportunity, orange = negative/pressure, near-background centre
= a matched/unremarkable hood). POSITIVE = suitable-but-quiet, NEGATIVE =
building-where-less-suitable.

**Low-FAR exclusion — SHIPPED as: exclude `is_set_aside` hoods (grey, off the
z population), consistent with every money/services view.** This removes the 48
River Valley / Anthony Henday greenfield-fringe hoods (FAR ≈ 0 parkland/
undeveloped, not infill opportunities) and leaves 358 in the scale. `is_residential`
was REJECTED as the filter — it also drops DOWNTOWN, the key dense/pressure case.

**Residual caveat (documented, refine later):** low FAR conflates two things —
a *mature underused infill site* and a *brand-new empty suburb still being built
out*. So a few non-set-aside developing/edge hoods still read too strong: at the
extreme EVERGREEN (a mostly-vacated floodplain mobile-home park, FAR ≈ 0, zero
activity) tops the opportunity end, and new-growth suburbs like KINGLET GARDENS
(low FAR because new, high current activity) land in "pressure". The pressure
extreme is the trustworthy read — DOWNTOWN (high FAR = little room, still
building) is the #1 pressure hood, which is the genuinely useful signal. The
blurb frames the whole view as *relative and exploratory, not a target*. A future
refinement (a maturity gate, or zoning-headroom suitability) would clean the
opportunity end.

**Build status (2026-07-13):** ✅ backend `far` column DONE — `load_property_info`
loads `gross_area`, `build_hood_lot_acres` emits `far`, `join_and_calculate`
carries it into the geojson + SLIM (unsuppressed by the LOW_PARCEL_FRAC guard;
`far` is a density ratio, not a per-lot-acre dollar figure); +7 tests (318
green). ✅ **web `Infill` view DONE** — diverging mismatch plane, gated on `far`,
reuses the units/permits × 5yr/3yr pickers for the activity side, set-aside
excluded; `verify-infill.js` 34/34 green. ⏳ REMAINING (optional refinement):
the maturity/zoning-headroom cleanup of the opportunity end; the one-sided
choropleth toggles (Peter's "possibly as separate" — the single diverging map
already shows both ends).

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

## Methodology decisions — Lens A SETTLED (2026-07-12), Lens B/C open

Lens A build-time decisions, now LOCKED:
- **Set-aside handling** — ✅ full override, coloured (Peter, 2026-07-12); see
  the Lens A section. Empirically low-impact but semantically correct.
- **Activity window** — ✅ last 5 full years (2021–2025) is the pinned base,
  drift-guarded. A **3yr recent window (2023–2025)** now ships alongside as a
  `#devwindow` toggle (2026-07-13): a second pinned aggregation
  (`PERMIT_YEARS_RECENT` in `main.py`) emits `_3yr`-suffixed columns; the base
  columns stay unsuffixed. Both windows apply to both metrics (units/permits).
- **Metric numerator** — ✅ `units_added` (dwellings) is the default choropleth.
  A **permit-count-per-acre sub-metric** now ships alongside (2026-07-13): the
  `#devmetric` picker in the layers panel swaps the plane/scale/legend/tooltip to
  `new_permits_per_acre` (project density — one large apartment is many units on
  one permit; many single houses are many permits). ABBOTTSFIELD is the extreme:
  248 units from 2 permits.
- **Null-`work_type` rows** — ✅ excluded, count reported (in-window ~41k of the
  ~60k are null/blank; INFO-logged each load). Same for null `building_type`.
- **"AREA"-suffix greenfield names** — ✅ resolved via the shared
  `NAME_CORRECTIONS` (CHAPPELLE AREA → CHAPPELLE etc.); no permit-local map
  needed. Warn-not-fail; the only straggler is `GLENORA, ROSSLYN` (1 unit).

Still open (Lens C):
- **Lens B** — ✅ COMPLETE 2026-07-13: built-FAR suitability + `Infill` diverging
  view (set-aside excluded). Only optional refinements remain (see Lens B section).
- **Lens A polish** — ✅ permit-count-per-acre sub-metric toggle DONE
  (2026-07-13); ✅ window toggle DONE (2026-07-13) — a 5yr (base, 2021–2025) vs
  3yr (recent, 2023–2025) activity-window picker, both metrics; remaining: the
  `occupancy_granted_date` completed-builds variant (Data note above).

## Build order

1. **Lens A minimal** — ✅ DONE 2026-07-12 (`feat/dev-lens-a-building-activity`):
   `src/load_permits.py` + `join_and_calculate` column + one choropleth metric +
   set-aside override + `verify-development.js` (25/25) + DATA.md entry.
2. **Lens A polish** — ✅ permit-count sub-metric picker DONE 2026-07-13
   (`new_permits_per_acre` + `#devmetric` control); ✅ window toggle DONE
   2026-07-13 (`_3yr` columns + `#devwindow` 5yr/3yr control,
   verify-development.js 40/40); remaining: the occupancy completed-builds variant.
3. **Lens B** — ✅ DONE 2026-07-13: suitability proxy (built FAR) + backend `far`
   column + web `Infill` diverging view (`z(suitability)−z(activity)`, set-aside
   excluded, verify-infill.js 34/34). Optional future refinement: maturity gate
   on the opportunity end; one-sided choropleth toggles.
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

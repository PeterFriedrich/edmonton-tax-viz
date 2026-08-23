# Scope: Development & Infill Lens family

> **UI regroup BUILT 2026-07-23 (branch `regroup-build-s65`, not yet on master) —
> `docs/CONTROLS_MATRIX.md` §7, `DECISIONS.md`.** This family's *chrome* changed:
> **Infill** is now a *full-only mode of Development* (the `#devmode` Housing/Infill
> toggle, not a `#views` button); **Industrial** is a *full-only `#devmetric`*; and
> the grid checkbox + "Spikes" picker became **one `#devdetail` "Detail"
> selector** (Neighbourhood / 100 m grid — activity). It shipped 3-way; the
> third option, **Stock age, was withdrawn 2026-07-27** — the whole
> "Stock-age spikes" section below is retained as a record of what was built
> and why, but describes a feature that is **no longer in the UI**. Some UI prose
> below (§ "Spikes" picker naming, etc.) still describes the pre-regroup wording —
> the underlying analysis/columns are unchanged, only the controls moved.

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
standardised over the SAME included population; each arm of the score is
clamped at its own p95 (per-arm scaling, 2026-07-14 — see the block below) and
rendered on a dark-centred diverging ramp
(teal = positive/opportunity, orange = negative/pressure, near-background centre
= a matched/unremarkable hood). POSITIVE = suitable-but-quiet, NEGATIVE =
building-where-less-suitable.

**Low-FAR exclusion — SHIPPED as: exclude `is_set_aside` hoods (grey, off the
z population), consistent with every money/services view.** This removes the 48
River Valley / Anthony Henday greenfield-fringe hoods (FAR ≈ 0 parkland/
undeveloped, not infill opportunities) and leaves 358 in the scale. `is_residential`
was REJECTED as the filter — it also drops DOWNTOWN, the key dense/pressure case.

**Opportunity-end cleanup — SHIPPED as an ASYMMETRIC RESIDENTIAL GATE
(2026-07-13, web-only).** The original worry was that low FAR conflates a *mature
underused infill site* with a *brand-new empty suburb still being built out* — so
a "maturity gate" (median `year_built` threshold) was planned. **A prototype
against the live data showed that gate does NOT work:** the opportunity-end
pollution is not new suburbs but *non-residential land* — industrial parks and
river-valley/highway fringe whose low FAR is *structural*, not opportunity — and
those hoods span every decade (1958–2024), so age can't separate them. Of the
opportunity top-30, 13 were `frac_industrial > 0.5` and only 3 were residential;
a median-year gate removed just ~2 of them. New suburbs are *not* the problem:
their high activity already pushes them to the pressure side (KINGLET GARDENS,
median 2023, reads as pressure, not opportunity).

So the fix is a **land-use filter, applied asymmetrically:** a hood that is
`is_residential === false` is **barred from the OPPORTUNITY (teal) end** — if its
signed score is positive it renders off-scale grey — but is **kept on the
PRESSURE (orange) end and in the z-scoring population.** This resolves the earlier
`is_residential` rejection: the whole-scale filter was rejected because it drops
DOWNTOWN, but DOWNTOWN sits on the *pressure* end (FAR 3.37 drives it), never the
opportunity end, so the asymmetric gate keeps it. The pressure end is therefore
**unchanged** (same z population, same clamp, DOWNTOWN still #1). The opportunity
end now surfaces genuine mature residential infill candidates (CANOSSA,
HOMESTEADER, STEINHAUER, MENISA, WELLINGTON, MCLEOD, ROSSLYN, CAPILANO — all
established, low FAR, near-zero recent activity). EVERGREEN (residential-zoned,
vacated floodplain) legitimately stays teal.

⚠️ **AMENDED 2026-08-22 — EVERGREEN is now OFF THE SCALE, and the gate was doing
a second job nobody had written down.** Measured while testing whether this lens
survives the 100 m grid: `gross_area` is null/zero on ~6.2% of rows, the pipeline
summed it with `NaN → 0`, and **69 in-scale hoods have >50% of their eligible rows
missing it** — so their `far` was understated and pushed toward the teal end. The
lens was nonetheless CLEAN, because **only 2 of those 69 are residential and the
asymmetric gate bars the other 67 from the opportunity end anyway.** The gate has
therefore been absorbing a *data-completeness* gap as well as the land-use one
argued for above — which is precisely the job it cannot do per cell, where
`is_residential`'s equivalent is often measured on a single property.
`build_hood_lot_acres` now emits `far = null` where no eligible row records a
floor area, so EVERGREEN (4 eligible rows, none with `gross_area`) renders grey
"no infill data" instead of saturating the teal endpoint. Its teal was never a
measurement. Full numbers: `docs/FINDINGS_infill_granularity.md`. `is_residential` and `far` are both
already in the geojson, so **no new pipeline column was needed** (the planned
`median_year_built` backend work was avoided). The blurb frames the whole view as
*relative and exploratory, not a target*.

**Build status (2026-07-13):** ✅ backend `far` column DONE — `load_property_info`
loads `gross_area`, `build_hood_lot_acres` emits `far`, `join_and_calculate`
carries it into the geojson + SLIM (unsuppressed by the LOW_PARCEL_FRAC guard;
`far` is a density ratio, not a per-lot-acre dollar figure); +7 tests (318
green). ✅ **web `Infill` view DONE** — diverging mismatch plane, gated on `far`,
reuses the units/permits × 5yr/3yr pickers for the activity side, set-aside
excluded. ✅ **asymmetric residential opportunity gate DONE** (web-only,
`infillOppSuppressed`); `verify-infill.js` 44/44 green. ⏳ REMAINING (optional,
low priority): the one-sided choropleth toggles (Peter's "possibly as separate" —
the single diverging map already shows both ends).

**✅ PER-ARM SCALING DONE (2026-07-14, Fable — closes the S48-audit reopening).**
The S48 decision audit found the mismatch score is *structurally asymmetric*: the
suitability term `−z(far)` is capped at **+0.97** (far ≥ 0, so `z(far) ≥ −0.97`),
while the activity term `−z(activity)` is unbounded below (activity max z = +6.16).
On the shipped `units × 5yr` data the score ranges **−12.03 … +1.51**, so the old
single **symmetric** p95 clamp of `|score|` (**3.04**) let 18 hoods saturate the
orange (pressure) arm but **zero** hoods reach even half-saturation on the teal
(opportunity) arm — the legend's full-teal endpoint was *unreachable by
construction*, and the median hood score (+0.435) sat almost exactly on the +0.5
"opportunity" verdict threshold. **Shipped fix (web-only):** each arm clamps at
its *own* p95 — `clampPos` = p95 of positive scores (≈ 1.49 on units × 5yr),
`clampNeg` = p95 of `|negative scores|` (≈ 4.34) — in `infillStats`/`infillT`;
the tooltip verdict branches on clamped `t` at **±0.4** (`INFILL_VERDICT_T`,
chosen off the shipped data: ~25% of the teal arm / ~31% of the orange arm read
as verdicts on the default column, and the median hood at t ≈ 0.29 sits clear of
the cut). The teal endpoint now saturates (EVERGREEN, WESTVIEW VILLAGE — ⚠️ EVERGREEN went OFF the scale 2026-08-22, see the amendment above; WESTVIEW VILLAGE still saturates); the
pressure ordering is unchanged (DOWNTOWN still #1). Nothing else about Lens B
changed. Locked in `docs/DECISIONS.md` (2026-07-14); implementation brief was
`docs/FABLE_infill_perarm_scaling.md`. Deploy: web-only → live on the next
`refresh.yml` run (Peter's trigger).

**Balance validation (2026-07-22) — the lens is NOT density-dominated.** A natural
question is whether the mismatch just restates FAR (existing density). It doesn't:
on the live data (358 included hoods, `units × 5yr`) the score correlates **+0.79
with the suitability term (`−z(far)`) AND +0.79 with the activity term** — equally,
because both are standardised over the same population. The two inputs are
near-independent (corr(FAR, activity) = **+0.24**), so the score is a genuine
two-signal gap between *how underbuilt the land is* (stock) and *how much building
is happening* (flow), not one variable wearing two hats. Recorded in
`ANALYSIS_BACKLOG.md` §9.

**Round-2 audit caveats (recorded 2026-07-17; dispositions from the S56 delta
audit — `session-summary/2026-07-16.md` §2.D, ledger row in
`docs/AUDIT_LEDGER.md`).** Four properties of Lens B that are deliberate but
were previously undocumented:

- *Denominator mismatch (D2, was S48 L1) — disclosed, not fixed.* The two
  z-scored terms use different land bases: FAR ÷ deduped **lot** acres
  (parks/ravines absent from the roll don't dilute it) vs activity ÷
  **boundary** acres (ravines fully dilute it), so a half-ravine hood leans
  teal by boundary geometry alone. The S56 flip test (activity ÷ lot acres =
  `act/parcel_frac`, n=358) measured the bias as immaterial: Spearman ρ
  0.9965; top-15 overlap 15/15 (teal) and 14/15 (orange); 5/251 verdict-band
  flips, all band-edge hoods at `parcel_frac` 0.51–0.80, none of them ravine
  hoods (visible <50%-parcel hoods move ≤ Δt 0.08). A pipeline denominator
  switch was rejected — it buys nothing at this materiality.
- *z-population compression (D5, was L5) — maintainer note.* The 132
  teal-barred non-residential hoods stay in the z-scoring population
  (removing them would re-rank the pressure arm and drop DOWNTOWN's anchor);
  the cost is that visible teal *intensity* is compressed ~2× (far std 0.249
  with them vs 0.120 residential-only). Teal is therefore **ordinal, not
  cardinal** — ranks are stable (14/15 top-15 overlap res-only), but "how
  teal" understates the residential-only contrast. Deliberate trade.
- *Suite conversions excluded (D3, was L6) — DISCLOSE-ONLY.* Work types
  (07)/(08)/(09) (suite additions + non-res-to-res conversions) are outside
  `NEW_WORK_TYPES`, so Lens B's activity term misses densify-by-suite. S56
  measured it: 51 in-window rows / **544 units = 0.9%** of the 62,978-unit
  Lens A numerator, 81% of it in DOWNTOWN (teal-barred anyway) + INGLEWOOD
  (already orange; counterfactual moves it −0.45 → −0.61). **Zero hoods**
  would flip verdict today. Adding suites to Lens B's activity (fork option
  ii) would fork its numerator from Lens A for no visible change — rejected.
  The blurb carries the disclosure clause. **Revisit if the suite share
  grows** — (08)/(09) are policy-encouraged.
- *Verdict grammar (D4, was L0) — descriptive since 2026-07-17.* The tooltip
  verdicts no longer pronounce recommendations ("Suitable but quiet — infill
  opportunity" → "Room to add, quiet lately"; "Building where less suitable —
  pressure" → "More building than room suggests"; "Balanced — activity ≈
  suitability" → "Activity ≈ room"). The thresholds were already principled
  (clamped t ± 0.4); this closes the copy half of the S48 L0 CONDITIONAL. The
  residual risk — the map being cited as build-here advice regardless — is
  accepted; the blurb's "not a target or a recommendation" line stays.

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
  A **long "Since 2009" window (2009–2025)** joins the toggle (2026-07-21,
  "Lens A long window") — the cumulative *density-added-over-the-era* cut that
  reproduces the inspiration lens's 2009–2023 "homes added" map. `PERMIT_YEARS_LONG`
  emits `_long`-suffixed columns; it is **anchored** (start fixed at
  `PERMIT_START_YEAR = 2009`, end DERIVED from `PERMIT_YEARS[-1]`, so the January
  bump extends it — no separate pin). A **first-class window** (2026-07-22): it
  drives both the hood choropleth and its own 100 m detail grid (`units_long`
  cells). The geocoding lag is on the NEWEST permits, not the oldest (2009–2023 at
  95–98%, 2025 ~72%), so the long grid is the *best*-covered of the three (84% of
  units on the grid vs 79%/71% for 5yr/3yr) — an earlier cut wrongly made it
  choropleth-only on a sparse-early-geocoding assumption the data disproved.
  Applies to all three metrics (units/permits/industrial). Citywide: ~160k units
  2009–2025 vs ~60k (5yr) / ~39k (3yr).
- **Metric numerator** — ✅ `units_added` (dwellings) is the default choropleth.
  A **permit-count-per-acre sub-metric** now ships alongside (2026-07-13): the
  `#devmetric` picker in the layers panel swaps the plane/scale/legend/tooltip to
  `new_permits_per_acre` (project density — one large apartment is many units on
  one permit; many single houses are many permits). ABBOTTSFIELD is the extreme:
  248 units from 2 permits. A **third `#devmetric` option "Industrial"** ships
  (2026-07-18, SPEC_industrial.md A3): new industrial (400-series `building_type`)
  permits per acre, count only — a Development-view choropleth, reset away on
  entering Infill (an industrial permit isn't residential infill). ⚠️ **It was
  choropleth-only until 2026-08-18**, when it gained 100 m detail cells; those
  cells are measured in **deflated construction value**, not permit count,
  because counts are too sparse to form a surface (89% of cells hold one
  permit) and a bigger cell does not fix it. See SPEC_industrial.md A3 +
  DATA.md §10.
- **Null-`work_type` rows** — ✅ excluded, count reported (in-window ~41k of the
  ~60k are null/blank; INFO-logged each load). Same for null `building_type`.
- **"AREA"-suffix greenfield names** — ✅ resolved via the shared
  `NAME_CORRECTIONS` (CHAPPELLE AREA → CHAPPELLE etc.); no permit-local map
  needed. Warn-not-fail; the only straggler is `GLENORA, ROSSLYN` (1 unit).

Still open (Lens C):
- **Lens B** — ✅ COMPLETE 2026-07-13: built-FAR suitability + `Infill` diverging
  view (set-aside excluded) + asymmetric residential opportunity gate. Only the
  optional one-sided choropleth toggles remain (see Lens B section).
- **Lens A polish** — ✅ permit-count-per-acre sub-metric toggle DONE
  (2026-07-13); ✅ window toggle DONE (2026-07-13) — a 5yr (base, 2021–2025) vs
  3yr (recent, 2023–2025) activity-window picker, both metrics; ✅ 100 m detail
  grid DONE (2026-07-15, "Lens A detail grid" below); remaining: the
  `occupancy_granted_date` completed-builds variant (Data note above).

### Lens A detail grid (as built 2026-07-15)

Peter's call: fine-grain rendering ships as a **layers-panel toggle inside the
Development view, not a new view button** — deliberately, as the pattern probe
for possibly migrating other lenses to this style later. Toggling "100 m grid
(permit points)" swaps the choropleth for the **Glass composition**: a
uniformly NEUTRAL hood plane (the set-aside override stands — nothing greys;
hover/tooltip stay on the hood) under `GridCellLayer` spikes of geocoded
permits binned into the same EPSG:3400 100 m cells as the Glass grid
(`load_permits.export_dev_grid` → `web/data/dev_grid.json`, ~4.1k cells,
0.13 MB). Height is **linear** in the active column (units|permits × 5yr|3yr —
the two existing pickers keep driving it), peak 2,500 m at the max cell (447
units); colour is sqrt at a per-column p97.5 clamp (the choropleth's locked
transform). Legend flips to "per 100 m cell"; the opacity slider opens while
the grid is up.

**Geocode-lag disclosure (the honesty condition for this layer).** Cells hold
only geocoded permits; coordinates lag on the newest permits (~1–2% missing
2021–2023, but 994 permits in 2024 and 3,564 in 2025 at build time —
DATA.md §10). On the 5yr window that is 47,125 of 59,697 units on the grid
(~21% not yet mapped; 3yr ~29%). The export writes per-window `coverage` into
the JSON and the blurb computes the percentage from the file — the disclosure
cannot go stale against the data it describes. Ungeocoded permits still count
in the hood choropleth/tooltips; positions are never faked (no hood-centroid
fallback). The toggle stays hidden on older data files without
`dev_grid.json`. `verify-development.js` 54/54.

### Stock-age spikes on the detail grid (added 2026-07-17, **WITHDRAWN 2026-07-27**)

> **This feature is no longer in the UI.** Peter's call — it "wasn't
> working well as an option" — see `DECISIONS.md` 2026-07-27. The
> `median_year_built` column is still produced by `export_value_grid.py`
> and still ships in `value_grid.json`, so the analysis below is
> reusable; only the presentation was removed. Kept because the scaling
> work (`FINDINGS_stock_age_spike_scaling.md`) is the durable part.

Peter's call: a second spike source for the detail grid — **"Spikes" picker
(New homes | Year built)**, shown only while the grid is up. "Year built"
swaps the permit cells for the **median construction year of each 100 m
cell's assessed buildings** — the whole standing stock (418k of 439k roll
rows carry `year_built`, DATA.md § 2), not the permit window, so it answers
"when was this fabric built" beside Lens A's "where is building happening
now". Design decisions:

- **Data rides in `value_grid.json`** (`median_year_built`, appended last),
  not `dev_grid.json` — the age layer needs the whole-roll cell population
  (~34.7k cells), which the permit file doesn't have. One shared fetch with
  the Glass view (`ensureGridData`); the picker appears when the file lands
  with the column, stays hidden on older files.
- **Height = recency, linear in year off the p2.5 floor** shared with colour
  (revised 2026-07-21, DECISIONS): the true minimum is a lone pre-war outlier
  (2026: 1904, while p1 is already 1944), so baselining at the true oldest
  cell floated the whole stock ~40 yr off the floor and every spike read
  uniformly tall (median cell at 68 % of peak). Baselining at p2.5 drops the
  median to ~48 % and lets new-build tower. The **top is never clamped** —
  the newest cell still hits full peak (heights-never-percentile-*clamped*
  rule holds); only the floor moves up, so the oldest ~2.5 % sit flat. NOT a
  power curve (the 2026-06-25 no-power decision stands).
  See `FINDINGS_stock_age_spike_scaling.md`. Peak-parity with the permit
  spikes (2,500 m at the newest cell).
- **Colour = the same sequential ramp, LINEAR in year** (year is an interval
  scale — sqrt is meaningless, so the locked sqrt-colour transform does not
  apply and the legend says "linear colour"). Ramp-top **yellow = newest**;
  low anchor clamps at p2.5 (the p97.5 convention's bottom-end sibling — a
  lone 1880s cell must not stretch the ramp) — now **also the height floor**,
  so height and colour share one anchor. Anchors and the blurb's
  cell-coverage counts compute from the file, so they can't go stale.
- **Cells with no known year are ABSENT (`null`), never year-0**; the median
  is row-weighted, which neutralizes the condo duplication regimes (repeated
  identical years median to themselves).
- **The Metric/Window pickers hide while the age spikes are up** — they
  select the activity column, and a visible control that does nothing would
  be a small lie. Verdict/gating unaffected: this is display only, distinct
  from the REJECTED median-age *gate* for Lens B (DECISIONS 2026-07-13 —
  age couldn't separate industrial from suburbs; here age is the signal
  itself, not a filter).

~~`verify-age-spikes.js`~~ (deleted 2026-07-27 with the feature) covered the guard, layer swap, linear height/colour
recomputes, null-cell absence, picker hiding, and the shared-fetch Glass
regression.

## Amenity distance — BUILT 2026-08-23 (pipeline; UI filter still to come)

Peter, 2026-08-22: *"one of the affectors i wanted was like, distance of each
block from lrt stations, and schools, for each property."* Shipped as **two
per-cell attributes on the 100 m grid**, `dist_lrt_m` and `dist_school_m`.

⚠️ **They are NOT terms in the Infill score, by decision** (`DECISIONS.md`
2026-08-22). Proximity is a *desirability* input, not an *underused* input;
folding it into `−(z(far) + z(activity))` would turn a descriptive metric into
a weighted index whose weights nothing can falsify. As attributes they answer
the question directly ("show me the quiet-opportunity cells within 600 m of
LRT") and stay independent of whether the score itself ever re-grains.

**What is locked**
| | |
|---|---|
| Distance basis | **Road-network**, never straight-line — euclidean is 55% false-positive at a 600 m band (`FINDINGS_infill_granularity.md` §5) |
| Graph | `centerline_type == "Road"` only; railways excluded as a **correctness** filter (they let a walk travel the LRT track to the LRT station) |
| Per-cell statistic | **Median** of the cell's properties, not the minimum — one corner property must not make a whole cell read as served |
| LRT station set | The **30** parents with a street entrance, not the 33 served parents and not the 58 `location_type == 1` stops |
| Schools | Both public boards, **catchment schools only** (19 city-wide/specialized programs excluded); private/charter/francophone are absent from the source |
| Missing | `null`, never a large sentinel — 0.1% of properties reach no amenity over the graph |

**What is still open**
- **The UI filter has not been built.** The columns ship; nothing reads them yet.
  A control needs a home in the existing grouping (`CONTROLS_MATRIX.md`) and the
  band values (600 m? 800 m? the window picker?) are a Peter call.
- **The band is a judgement, not a discovery.** 600 m is the TOD walkshed
  convention and puts **554 cells (1.6%)** in scope; 800 m of a school covers
  **37.8%**. Neither number falls out of a cliff in the data.
- **Distance is not in the score and should stay out** unless that decision is
  deliberately revisited — see the DECISIONS row before proposing it.

## Build order

1. **Lens A minimal** — ✅ DONE 2026-07-12 (`feat/dev-lens-a-building-activity`):
   `src/load_permits.py` + `join_and_calculate` column + one choropleth metric +
   set-aside override + `verify-development.js` (25/25) + DATA.md entry.
2. **Lens A polish** — ✅ permit-count sub-metric picker DONE 2026-07-13
   (`new_permits_per_acre` + `#devmetric` control); ✅ window toggle DONE
   2026-07-13 (`_3yr` columns + `#devwindow` 5yr/3yr control,
   verify-development.js 40/40); ✅ 100 m detail grid DONE 2026-07-15
   (layers-panel toggle → glass composition, geocode-coverage disclosure —
   "Lens A detail grid" above; verify-development.js 54/54); remaining: the
   occupancy completed-builds variant.
3. **Lens B** — ✅ DONE 2026-07-13: suitability proxy (built FAR) + backend `far`
   column + web `Infill` diverging view (`z(suitability)−z(activity)`, set-aside
   excluded) + asymmetric residential opportunity gate (`infillOppSuppressed`;
   non-residential land barred from the teal end, kept on pressure/orange +
   in-population), verify-infill.js 41/41. Optional future: one-sided choropleth
   toggles.
4. **Lens C** — reuse service-cost columns (or V2) against Lens A.
5. **Amenity distance** — ✅ pipeline DONE 2026-08-23 (`feat/amenity-distance`):
   `src/load_schools.py` + `src/amenity_distance.py` +
   `load_transit.derive_lrt_stations` + `dist_lrt_m`/`dist_school_m` on the
   value grid. **The UI filter is NOT built** — see "Amenity distance" above.

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

## Entry defaults changed (2026-07-27, Peter)

The view **sits second in `#views`, next to Money**, and opens on:

| Control | Was | Now |
|---|---|---|
| `#devmetric` | Dwelling units | Dwelling units *(unchanged)* |
| `#devwindow` | Last 5 yr (2021–2025) | **Since 2009** (2009–2025) |
| `#devdetail` | Neighbourhood choropleth | **100 m grid — activity** |
| `#prism-row` | inherited (100% fresh, 5% via Ratio) | 50% *(set 2026-07-26)* |

`#devwindow` button order also changed from `5yr, 3yr, long` to **`3yr, 5yr,
long`** — shortest to longest, which is what it always should have read as.

**What this means for anyone reading the code:** the choropleth is no longer
what the view opens on. `verify-development.js` now selects
Neighbourhood + 5yr **explicitly** before its choropleth assertions rather than
relying on the entry defaults — the implicit dependency is exactly what broke
that suite when the defaults moved, and being explicit means the next change
cannot break it the same way. Same reasoning applies to any new test here.

Two latent ordering bugs surfaced with the grid as the default; both are fixed,
and both were of the shape *chrome read before it was final* — see
`DECISIONS.md` 2026-07-27. The durable one: `applyView` wrote the title/blurb
**after** `buildLayers()`, and the label sweep measures the title's live
bounding rect, so it culled against the outgoing view's (shorter) blurb.

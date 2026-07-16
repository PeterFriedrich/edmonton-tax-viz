# Scope: Utility Cost Lenses — five candidate services

**Status: SPEC'd 2026-07-05; Lens 1 (stormwater) pipeline BUILT same day**
(Peter's call: "stormwater first") on `feature/stormwater-lens` — see the
as-built block in Lens 1. Lenses 2–4 remain candidates, nothing built.
Method source: `docs/utility_cost_estimation_lens_methods.md` (verified
2025/2026 tariffs, formulas, and dataset IDs — cited below as "Methods §X";
tariff numbers live THERE, not here, so an annual rate re-pull touches one
doc). This spec maps those methods onto this project's pipeline: what each
lens would measure, which inputs we already have, and the open decisions to
settle with Peter before building anything.

These are **services** in the `SPEC_services.md` sense (cost/consumption
side; roads was the first). Any one of them is a "second service" and
therefore triggers the standing UI decision: the Roads view generalizes to a
Services view with per-service checkboxes, and "total services" gets defined
(TODO.md "More service layers").

## Why

Roads measure consumption as a physical quantity (metres per acre). The
utility lenses measure it in **dollars under the utilities' own tariff
structures** — and the tariffs are public, so the dollars are computable
without any cost model of our own. Two of the five signals are genuinely
**land-driven** (the framework's native axis, Methods §G):

- **Stormwater** is billed per m² of parcel scaled by a zone-based runoff
  coefficient — an area × intensity formula written directly into bylaw.
- **Fixed connection charges** (water/sanitary daily charges by meter size,
  electricity/gas daily customer charges) approximate the per-connection
  cost of linear infrastructure, independent of consumption.

The volumetric parts (m³, kWh, GJ) are demand-driven and rest on citywide
consumption proxies — weaker land signal, lower fidelity. The lenses are
tiered accordingly.

## Money-flow honesty (read before designing any display)

Property tax levy (our revenue metric) and utility charges are **different
money flows**. Water/sanitary/stormwater bills go to EPCOR under
performance-based regulation; electricity and gas delivery charges go to
EDTI/ATCO under AUC regulation. None of that is City tax revenue, and none
of it is funded BY the levy. Two consequences:

1. A "does revenue cover cost" ratio dividing the **levy** by **modeled
   utility charges** would compare unrelated flows — never build that
   silently. The honest framings: utility-charge intensity as a
   consumption/cost-allocation proxy (like `road_m_per_acre`), or modeled
   utility revenue vs modeled utility cost *within* the same utility.
2. The **franchise fees ARE City revenue** (electricity Local Access Fee =
   17.65% of forecast distribution revenue; gas Rider A = 35% of gross
   delivery revenue — Methods §D–E). A modeled per-hood franchise-fee line
   is a legitimate *revenue* column — but it is **modeled, not billed**, and
   must stay a separate column, never merged into the assessment-roll levy.

Everything these lenses output is labeled **modeled** (Methods, Caveats).
The stormwater case is special: because the tariff itself is the utility's
area-based cost allocation (validated within ±5% of cost of service by the
2024 HDR study, Methods §C), modeled billing ≈ allocated cost by
construction. For the others, modeled billing is a charge estimate, not a
cost estimate.

## Fidelity tiers

| Tier | Lens | Formula basis | Weakest input |
|---|---|---|---|
| 1 | Stormwater | Bylaw-native A × I × R × rate | zone-null rows; condo area apportionment |
| 2 | Water + sanitary | Verified tariffs, fixed + volumetric | meter size (assumed by class); 14.3 m³/mo proxy |
| 3 | Electricity, gas | Verified tariffs + franchise % | per-household kWh/GJ proxies; dwelling counts |

---

## Lens 1 — Stormwater (Tier 1, recommended first)

**AS BUILT (v1 pipeline, 2026-07-05, `feature/stormwater-lens`):**
`src/load_stormwater.py` (per-point A×I×R, `ZONE_RUNOFF` explicit dict with
[bylaw]/[aligned] provenance tiers) + `data/stormwater_rates.json`
(year-keyed 2025 monthly / 2026 daily rates, hard-error on a missing year
like mill rates) + `STORM_COLUMNS` merge in `join_and_calculate`
(`storm_charge_per_acre` on boundary acres) + `main.py` wiring
(`--skip-stormwater`; rides the existing property-info + zoning inputs).
19 new tests (182 green). Real-data run (2025 rate): **287,103 of 287,163
points modeled** — zone from own column 282,654, spatial fallback 4,508,
1 unresolved; 56 lot-ineligible + 3 on legacy zone codes (US/CSC/RSL,
DATA.md §2) excluded + reported. **Citywide modeled $240.4M/yr on 577 km²
eligible lot area.** Ranking sanity passes: industrial hoods top
($2.7–2.9k/acre), river valley / ravines / golf bottom ($0–140/acre),
residential between (Riverdale $842, Westmount $1,537, Downtown $1,645).
PEMBINA is #1 per-acre — the known lot-bound outlier, consistent.
**As-built caveats (on top of the modeled-not-billed framing):**
- **Serviced-area assumption:** the model charges every roll parcel at its
  zone's R; EPCOR presumably does not bill parcels outside the drainage
  service area. The annexed/rural fringe is material — EDMONTON ENERGY AND
  TECHNOLOGY PARK alone models $11.9M/yr (5% of citywide) on 50 km² of
  mostly-undeveloped land whose EET zones are assigned industrial R.
  **VALIDATED 2026-07-07** (`docs/FINDINGS_utility_validation.md`):
  modeled $240.4M vs EPCOR published $141.1M forecast revenue 2025F
  (1.70×); residential slice 1.11×; notyet+never zone categories carry
  $49.8M of largely unbilled land ($190.5M excluding them, 1.35×).
  DECIDED (Peter, 2026-07-07): citywide claims report BOTH totals —
  shipped as `UNBILLED_CATEGORIES` in `load_stormwater` (log line +
  `.attrs`); per-hood outputs unchanged. FINDINGS §3.
- **DISPLAYED as of 2026-07-05** (`feature/services-view`, decision 2):
  `storm_charge_per_acre` joined `SLIM_COLUMNS` and rides the main hood
  GeoJSON; the Services view (the Roads view generalized to per-service
  checkboxes) renders it as a flat hood plane — linear colour, clamp p97.5
  of non-set-aside hoods (≈ $2,700 on 2025 data), set-asides grey, legend
  labeled "Modeled". Full display detail: `docs/UI.md` "Services views".
- The AG runoff ambiguity below is coded as 0.1 with a VERIFY comment.

**Metric:** modeled annual stormwater charge per hood (and per acre) =
`Σ over properties ( lot_area_m² × I × R(zone, lot_area) ) × rate × 365`.
I = 1.0 default; R from the runoff-coefficient table keyed to Bylaw 20001
zone codes with the <450/>450 m² residential and <700/>700 m² DC splits;
rate $0.00327/m²/day effective 2026-04-01 (formula + full R table:
Methods §C).

**Inputs — all already in the pipeline** (this is why it's first):

- `lot_size` from `dkk9-cj3x` (m², city-provided). Multi-unit apportionment
  is EXACTLY the solved dedupe problem: the bylaw bills condo area as
  per-unit shares of the lot (Methods §C), and the shipped repeat-aware rule
  (`docs/FINDINGS_lot_dedupe.md`; `SHARE_MAX_M2`) reconstructs per-point
  eligible area on the same principle. Reuse `_point_lot_stats`; the 56
  ineligible majority-null points get excluded + REPORTED, same as the
  lot-acre metric.
- `zoning` from `dkk9-cj3x` — per-property zone code, **current Bylaw 20001
  vocabulary** (probe 2026-07-05: RS 146,567 / RSF 98,606 dominant; 78
  distinct base codes; DATA.md §2). Coverage: **98.2% of non-null rows use
  base codes directly in the R table**; the remainder are special-area codes
  (GLDF, PLD, SLD, BRH, …) that need explicit R assignments — same
  hand-assigned-dict philosophy as `ZONE_CATEGORY`, and the bylaw itself
  says unlisted zones map to the closest-aligned zone (EWSI discretion), so
  a judgment dict is faithful to how it's actually billed. Flag every
  assignment; unknown codes warn loudly.
- **Zone-null fallback:** 35.71% of rows (157,030) have null `zoning`.
  Fallback = point-in-polygon of the property lat/long against the zoning
  layer we already download (`fixa-tstc`). Report how many rows each path
  resolves; rows failing both are excluded + reported, never silent.
  **Trap (Methods §H): never source zone codes from the historical layer
  `67p2-r285`** — it carries old Bylaw 12800 codes that mismatch the R
  table.

**Refinements, deliberately NOT v1:** SIAP intensity reductions via the LID
Inventory (`3xir-jjpa`) — v1 uses I = 1.0 everywhere and reports how many
parcels the LID layer flags, without applying reductions. True impervious
area (vs zone-average R) is parcel-geometry-gated →
`PARCEL_LEVEL_OPPORTUNITIES.md` P6.

**Validation:** citywide modeled total vs EPCOR's published stormwater
revenue (order-of-magnitude sanity); per-hood modeled charge per acre
should track imperviousness intuition (industrial > commercial >
residential > river valley). A physical-bound-style guard like
`check_lot_acre_bounds` (eligible lot acres ≤ hood acres) comes free from
the dedupe reuse.

## Lens 2 — Water + sanitary/wastewater (Tier 2)

**Metric:** modeled annual water + sanitary + wastewater-treatment charge
per hood = fixed daily charges by meter size × 365 + volumetric rates ×
consumption proxy (residential 14.3 m³/month/household; formulas + block
schedules: Methods §A–B).

**Inputs and their honesty ranking:**
- Fixed charges need **meter size, which is not public** — assumed by
  land-use class (15 mm single-family default; larger for multi-res /
  commercial, inferable from `dkk9-cj3x` `total_gross_area` and unit
  counts). This is the lens's central modeled assumption.
- Volumetric charges need **household counts** — the residential-record
  count per hood (assessment CSV; condo units are individual records) is
  already the planned household proxy for ANALYSIS_BACKLOG 4. Multi-res
  uses the declining-block schedule (opposite shape to residential —
  Methods §A).
- Methods §A mentions an EPCOR hexagon water-usage open dataset for spatial
  calibration — **dataset ID unverified; locate before relying on it.**

**Note:** the fixed-charge component (per-connection, meter-sized) is the
land-relevant signal; the volumetric component mostly re-plots household
counts. Consider publishing the two as separate columns so the display can
show the connection-cost signal alone.

### Lens 2 as built (2026-07-07 — decisions locked with Peter 2026-07-06)

- **Scope: residential + multi-res only** (locked): RESIDENTIAL and
  MA DERELICT RESIDENTIAL rows are households, OTHER RESIDENTIAL rows are
  multi-res buildings; COMMERCIAL/FARMLAND/rest excluded + counted (~23.5k
  rows — verified rates exist but no consumption benchmark).
- **Two columns, colour by TOTAL** (locked): `water_charge_per_acre` drives
  the plane, `water_fixed_per_acre` ships alongside for the tooltip split.
- **Module:** `src/load_water.py`; rates in `data/water_rates.json`
  (April 2026 schedule; only the four meter sizes verified for BOTH water
  and sanitary — 15/25/100/300 mm; Public Fire Protection charge EXCLUDED,
  only its 15mm rate is verified). Tariff vintage pinned separately from
  the roll year (`WATER_RATE_YEAR` in main.py — a forward-looking modeled
  bill, unlike mill rates).
- **Connections:** household rows grouped by exact roll point (one condo
  tower = one connection); OTHER RESIDENTIAL units estimated from gross
  floor area (m², confirmed) at 90 m²/unit — the lens's weakest input
  (1,018 of 4,353 buildings lack floor area and are excluded + counted).
  Meter size assumed from unit-count bands (`_meter_size_mm`).
- **First real run:** 268,489 connections / 551,831 modeled households →
  352 hoods, **citywide $588.1M/yr ($133.9M fixed + $454.2M volumetric)**,
  ≈ $89/household/month. The household count runs ~20% above the census
  dwelling stock — the floor-area→units estimate is the suspected
  overcount; volumetric impact bounded (~4% of the total).
  **VALIDATED 2026-07-07** (`docs/FINDINGS_utility_validation.md`):
  $588.1M vs ≈$467M published at matching res+multi-res scope (≈1.26×,
  range 1.17–1.30 — the water utility's res+MR class split is derived to
  ~80% from EPCOR's by-class counts, §2.2, not read off a revenue schedule);
  connection count 13% UNDER EPCOR accounts (268,489 vs 308,389), so the
  excess is per-connection (households/consumption), not count.
- **Colour: LINEAR** (FINDINGS §6.6) — clamp/median 2.2× (storm territory);
  the raw skew (+3.4) lives in the p97.5-clamped tail; sqrt over-corrects.

## Lens 3 — Electricity distribution + Local Access Fee (Tier 3)

**Metric:** modeled annual distribution charge per hood (EDTI DAS-R:
$0.69953/day + $0.01712/kWh at ~7,200 kWh/yr/household — Methods §D), plus
**`laf_revenue` = 17.65% of modeled distribution revenue as a modeled CITY
revenue column** (separate from the levy — see Money-flow honesty).
Commercial classes have their own DAS schedules (Methods §D).

## Lens 4 — Natural gas distribution + franchise fee (Tier 3)

**Metric:** modeled annual delivery charge per hood (ATCO Gas North Low
Use: $0.997/day + ~$2.50/GJ all-in variable at ~110–120 GJ/yr/household —
Methods §E), plus **`gas_franchise_revenue` = 35% of gross delivery
revenue as a modeled CITY revenue column.**

**Tier-3 caveat (both):** the volumetric bulk of these charges scales with
household counts and citywide consumption proxies — as a map they largely
re-plot dwelling density. Their distinct value is the **franchise-fee
revenue lines** (real City revenue keyed to utility activity) and the
per-connection fixed charges. If that value doesn't justify a lens, the
franchise lines could ship as columns without a display layer. Methods §G's
pitfall applies: never let a per-household cost allocation masquerade as a
land-driven cost signal.

### Lens 3+4 as built — franchise COLUMNS ONLY (2026-07-07 — decided with Peter)

Built electricity + gas together as one module, **columns only, no display
layer** (the "ship as columns" option above — Peter's call, given the
collinearity below).

- **Scope: residential only**, and the **SAME dwelling model as the water
  lens** — `load_water.build_connections` was extracted as a shared helper so
  the two lenses cannot disagree on the household count (551,831). Each
  dwelling is billed as its own electricity + gas meter (per-dwelling, unlike
  water's shared building connection). Commercial excluded (no consumption
  proxy — same reason as water).
- **COLLINEAR WITH DWELLING COUNT (the headline caveat):** the consumption
  proxy is flat per dwelling (7,200 kWh/yr, 115 GJ/yr), so every per-hood
  column is `dwellings × a constant`. As a map it re-plots dwelling density
  and nothing more — hence no display layer. `dwelling_count` ships as its own
  column so the collinearity is explicit, not buried in a dollar figure. The
  distinct spatial signal (commercial load) is out of scope.
- **Module:** `src/load_franchise.py`; rates in `data/franchise_rates.json`
  (EDTI DAS-R Jan 2025 + ATCO Gas North Jan 2026; `FRANCHISE_RATE_YEAR` in
  main.py). Columns carried on the full frame (`FRANCHISE_COLUMNS`) but NOT in
  `SLIM_COLUMNS` and no per-acre derived — no display yet. `--skip-franchise`.
- **First real run:** 551,831 dwellings → 352 hoods. **Modeled City revenue:
  electricity LAF (17.65%) $36.9M/yr + gas franchise (35%) $125.7M/yr =
  $162.6M/yr** (modeled distribution $208.9M, gas delivery $359.3M).
- **Known underestimate:** modeled LAF is $5.57/mo/dwelling vs the City's
  published ~$8.33/mo (2026) — the fee is levied on EDTI's FULL distribution
  revenue (riders/pass-throughs), not the base customer+energy schedule
  modeled here (~⅓ low). Documented in the rates JSON + FINDINGS §5; per-hood
  shape unaffected (linear in dwellings). Gas franchise base follows Methods
  §E (all riders in the delivery base × 35%); Rider B property-tax rider
  excluded (a tax pass-through, not a franchise fee).
- **VALIDATED 2026-07-07 vs the City's audited franchise-fee line**
  (2024 Financial Annual Report, Note 24; FINDINGS §5.1): combined elec+gas
  modeled $162.6M (residential) vs $175.9M City actual = **0.92×**, but that
  masks two offsetting errors — **gas 1.32× over** (Rider T in the 35% base;
  excl → 1.00× — Peter parked the Rider-T call, TODO), **elec 0.46× under**
  (the LAF floor; real EDTI distribution base is 2.19× modeled). Line-by-line
  is the honest read; the combined near-match is coincidental cancellation.

---

## Shared machinery (whichever lens goes first)

- **New module per lens** (`src/load_stormwater.py` etc.), mirroring
  `load_roads.py` / `load_zoning.py`: load → explicit dicts → per-hood
  columns; per-hood columns merge in `join_and_calculate` (left join,
  graceful when absent); `main.py` `--skip-*` flags; no silent drops —
  every excluded row/point counted + reported.
- **Rates live in a small versioned JSON** (like `mill_rates.json`) with
  effective dates and source citations, not hard-coded in modules. Utility
  rates reset annually (water/wastewater Apr 1; electricity/gas Jan 1 —
  Methods, Caveats); annualize daily charges by day count. A rate-vintage
  field joins `status.json` if a lens becomes a CI-refreshed output.
- **Aggregation grain:** per-property computation, aggregated to hood
  (and optionally to the 100 m grid — stormwater per-point charges bin the
  same way the Glass grid does, with the same point-vs-parcel caveats).
- **Every output column is prefixed/documented as modeled** (`modeled_`
  prefix or equivalent — decide once, apply to all lenses).

## Recommended build order

Methods (Recommendations) stages 1–3 map onto: **stormwater first** (Tier 1
fidelity, zero new data), water/sanitary second, electricity/gas (or just
their franchise-revenue columns) third. Stage 4 (PBR rate escalation for
forward-year projection) and Stage 5 (lifecycle/developer-capital
accounting) are NOT lens builds — Stage 4 is deferred until a lens exists
and a projection is wanted; Stage 5 is an analysis question →
ANALYSIS_BACKLOG 5.

## Open decisions — settle with Peter before building (fire-lens protocol)

1. **Go/no-go and which lens first.** Recommended: stormwater (bylaw-native
   formula, inputs already loaded, reuses the dedupe machinery).
2. **Display shape — DECIDED 2026-07-05 (Peter): (a).** Per-hood
   ground-plane layer ($/acre/yr, sequential ramp, MODELED label) in the
   Services-view generalization, which was decided the same day: the Roads
   view becomes a "Services" view with per-service checkboxes (Roads,
   Stormwater, later Fire). Decided jointly with the fire lens (its design
   is also settled — TODO.md) so the Services UI is designed once.
   Rejected: (b) grid-cell variant alongside Glass (bigger build, per-cell
   modeled-vs-billed labeling harder); (c) pipeline-only (lens invisible).
3. **Does modeled utility $ enter "total services"? — DECIDED 2026-07-10
   (Peter): NO, staged design.** The trigger ("two dollar services exist")
   fired with storm + water built — but they are the wrong dollars: both
   are modeled **EPCOR** charges, and the Money-flow honesty rule above
   already forbids dividing the levy by them (they are recovered from
   ratepayers; adding them to both sides of a ratio would cancel). Only
   LEVY-FUNDED services may sit under the levy, and the two we measure
   (roads, fire) are physical. Staged answer:
   - **V1 (built 2026-07-10): the Ratio view's denominator is a per-service
     PICKER** — revenue per road metre | per fire event ("Ratio
     denominator" control, `web/index.html` `RATIO_DENOMS`). Fire floor
     0.005 events/acre/yr + log colour: `FINDINGS_revenue_scale.md` §6.7.
   - **V2 (metric BUILT 2026-07-15; display open):** one combined
     "modeled city service cost per acre" = road metres × published roadway
     O&M+renewal $/m/yr + fire events × (Fire Rescue operating budget ÷
     citywide annual dispatches). Unit costs become a manual, reviewed
     input (`city_unit_costs.json`, the mill-rates pattern), labeled
     MODELED and "roads + fire only" — never "total city cost" (police/
     parks/transit unmeasured). The fire term is a demand *allocation* of
     a mostly-fixed budget — carry that caveat.
     As built: unit costs sourced 2026-07-15 (laptop, DATA.md §13); the
     pipeline half landed the same day — `join_and_calculate.load_unit_costs`
     + `unit_costs` arg → `svc_cost_per_acre` in `SLIM_COLUMNS` (per-event $
     = budget ÷ the fire frame's citywide kept-event sum, pre-join; requires
     BOTH roads + fire, warn+skip otherwise).
     **Display — DECIDED 2026-07-16 (Peter): BOTH placements, staged.**
     - *(a) Services-view checkbox — BUILT 2026-07-16.* A 6th per-service
       row, "Service cost (roads+fire) — modeled $/acre", on the shared
       `svc-plane` (SERVICES `servicecost`, sqrt colour — fire-dominated
       skew). Its blurb + legend carry the "roads + fire only, never total
       city cost" and fixed-budget-allocation caveats; the tooltip adds a
       `svc_cost_per_acre` row. Column-guarded like the other service rows,
       so the checkbox hides on data files that predate the column (it lands
       on the first refresh after the metric PR). `verify-services.js` +
       `shot-services.js` extended.
     - *(b) Ratio-view coverage denominator — FOLLOW-ON, not yet built.*
       Levy revenue ÷ modeled service cost (a "does the tax cover roads+fire"
       coverage map). Money-flow-honest here because roads+fire ARE
       levy-funded (unlike storm/water). Reopens V1's per-service-only ratio
       as a combined option; heavier caveat copy. Peter's staged plan is to
       ship (a) first, then (b).
4. **Franchise-fee revenue columns:** ship with the electricity/gas lenses,
   earlier as standalone columns, or not at all? Recommended: only with
   their lenses — a modeled revenue line without its cost context invites
   misreading.
5. **Branch point — DECIDED 2026-07-05 (Peter):** merge the
   `feature/stormwater-lens` pipeline PR as-is first (nothing served
   changes; CI green suffices), then the Services-view UI + stormwater
   display on a fresh branch off master. Future lenses: new branch off
   master each.

## Out of scope (this spec)

- Forward-year rate projection (PBR I−X escalation, Methods §F).
- Lifecycle renewal / developer-contributed-capital accounting and the
  growth cost-recovery question (SSTC pause, off-site levies, BILD case
  study) — analysis, not a lens: ANALYSIS_BACKLOG 5. Advocacy-sourced
  figures on any side are labeled as such there (neutral-tone rule).
- True parcel-geometry imperviousness (PARCEL_LEVEL_OPPORTUNITIES P6).
- Per-parcel "your bill" outputs — everything here is modeled at
  aggregate grain; no output should read as a billing reconstruction for
  a specific address.

## Cross-refs

- Method source + all tariff numbers: `docs/utility_cost_estimation_lens_methods.md`.
- Services-lens architecture + second-service UI trigger: `docs/SPEC_services.md`, TODO.md "More service layers".
- Lot-size dedupe rule reused by stormwater: `docs/FINDINGS_lot_dedupe.md`, `src/export_value_grid.py`.
- `dkk9-cj3x` columns + zoning-coverage probe numbers: `data/DATA.md` §2.
- Zoning layer for the zone-null fallback: `data/DATA.md` §5 (`fixa-tstc`).
- Growth cost-recovery analysis: `docs/ANALYSIS_BACKLOG.md` item 5.
- Parcel-geometry upgrade path: `docs/PARCEL_LEVEL_OPPORTUNITIES.md` P6.

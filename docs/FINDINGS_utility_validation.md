# Findings — Utility Lens Validation vs EPCOR Published Revenue

**Date:** 2026-07-07 (Session 19). Closes the TODO validation item for
Lens 1 (stormwater) and Lens 2 (water + sanitary); §5 covers the Lens 3
(electricity/gas franchise) totals + caveats (build 2026-07-07), and §5.1
closes it against the City's audited franchise-fee line (2026-07-07).
**Verdict up front: order-of-magnitude PASS for both lenses.** The
residential slice of the stormwater model lands within ~11% of what EPCOR
actually bills; the citywide excess is localized and explained (unbilled
future/rural/parks land, I = 1.0 everywhere, judgment-tier runoff
coefficients on commercial/industrial).

## 0. Sources (all public, fetched 2026-07-07)

1. **EPCOR Water Services 2025–2027 Wastewater PBR Application**
   (May 31, 2024, 235 pp) — epcor.com `supporting-documents/
   2025-2027-wastewater-pbr-application.pdf`. Key tables:
   - Table 20.2-1 (p. 173): sanitary + stormwater forecast revenue and
     revenue requirement by customer class, 2025–2027.
   - Table 20.1.3.4-1 (p. 172): 2024 test-year stormwater present revenue
     $121.7M vs allocated cost $141.7M.
   - Table 12.4-1 (p. 109): wastewater treatment 2024 present revenue by
     class.
   - Table 4.8.1-1 / 4.8.1-3 (pp. 61–63): customer counts and stormwater
     equivalent units (SEUs) by class.
   - Table 21.3.2-2 (p. 179): stormwater rate +31.2% (2025), +6.2%/yr
     (2026–27); sanitary −7.0%/−2.0%/−2.0% (rebalancing).
2. **EWS 2024 PBR Progress Report** (Utility Committee deck) —
   pub-edmonton.escribemeetings.com DocumentId=263222, p. 7:
   2024 **actual** revenue — In-City Water $254.9M, Wastewater Treatment
   $137.9M, Wastewater Collection $278.2M (EWS total $671.0M).
3. **City of Edmonton 2024 Financial Annual Report** (audited consolidated
   financial statements) — edmonton.ca `2024FinancialAnnualReport.pdf`,
   **Note 24 "Utility Franchise Agreement Fees"** (pg 105), disclosed under
   AR 313/2000. Franchise fee revenue by utility, in $000
   (Budget / 2024 actual / 2023 actual):
   - ATCO Gas and Pipelines — **Gas**: 93,713 / **95,167** / 88,759
   - EPCOR Distribution — **Power**: 80,780 / **80,780** / 76,418
   - EPCOR Water Services — Water: 18,993 / 21,280 / 19,237
   - EPCOR Water Services — Drainage: 12,704 / 13,781 / 11,682
   - EPCOR Water Services — Wastewater: 10,637 / 11,429 / 10,748
   - **Total franchise fees: 216,827 / 222,437 / 206,844.**
   (Fetched from edmonton.ca on Peter's laptop, 2026-07-07 — the box that
   built Lens 3 could not reach edmonton.ca; that blocker is now cleared.)

The in-city **Water** PBR application (2022–2026 term) lives on
edmonton.ca, which this box cannot reach (curl exit 000; WebFetch 404 on
the `public-files` paths) — the water-utility class split below is
therefore an estimate, flagged as such.

## 1. Stormwater (Lens 1) — modeled $240.4M/yr at 2025 rates

| Comparison | Modeled | EPCOR published | Ratio |
|---|---|---|---|
| Citywide, all roll parcels | $240.4M | $141.1M forecast revenue 2025F ($147.4M revenue requirement) | **1.70×** |
| Excl. 48 set-aside hoods | $207.3M | same | 1.47× |
| Excl. `notyet` + `never` zone categories | $190.6M | same | 1.35× |
| Residential (`res` category) | $94.4M | $85.2M (residential $77.6M + multi-res $7.6M, 2025F) | **1.11×** |
| Everything non-res (ind+com+inst+mix+dc) | $96.1M | $55.9M (commercial class, 2025F) | 1.72× |

Context figures: 2024 actual stormwater present revenue $121.7M;
published trajectory $141.1M (2025F) → $159.5M (2026F) → $175.0M (2027F)
as the +31.2%/+6.2%/+6.2% rebasing lands.

**Physical cross-check (rate-independent):** EPCOR's 2025F billed base is
1.618B annual SEUs ≈ **134.8M m²-equivalent** (monthly average). The
model's `Σ A×I×R` ≈ **216M m²-equivalent** → 1.60×, consistent with the
revenue ratio (residual vs 1.70× is the part-year April rate change).

**Model split by zone category** (one-off rerun of the `load_stormwater`
per-point pipeline grouped by `ZONE_CATEGORY` instead of hood; reproduces
$240.4M exactly):

| Category | $M/yr | Share | Points |
|---|---|---|---|
| res | 94.4 | 39.3% | 263,377 |
| ind | 54.5 | 22.7% | 5,250 |
| notyet | 36.0 | 15.0% | 2,447 |
| dc | 14.9 | 6.2% | 7,878 |
| inst | 14.5 | 6.0% | 1,360 |
| never | 13.8 | 5.8% | 3,154 |
| com | 9.2 | 3.8% | 1,286 |
| mix | 3.0 | 1.2% | 2,351 |

**Where the 1.70× lives:**
1. **Unbilled land, ~21% of the modeled total**: `notyet` ($36.0M —
   future/rural/reserve, largely outside the drainage service area;
   EETP alone $11.6M) + `never` ($13.8M — river valley/parks; EPCOR only
   started billing rec sites/cemeteries/golf in 2025, ~$1.7M total).
2. **Non-res overshoot (~$40M)**: model uses I = 1.0 everywhere; real
   multi-res/commercial get Development Intensity Factor reductions via
   the Intensity Adjustment Program (retention ponds etc.). Plus the
   [aligned]-tier judgment R assignments and serviced-industrial fringe.
3. **Residential is nearly right (1.11×)** — the bylaw-tier R codes and
   the repeat-aware dedupe carry the bulk of the parcels and match
   EPCOR's billed base closely. Residual ~11%: vacant/unbilled parcels,
   the <4% SEU reduction EPCOR applied in the Bylaw-20001 R update, DIF.

## 2. Water + sanitary (Lens 2) — modeled $588.1M/yr at 2026 rates, residential + multi-res scope

Model components = water + sanitary collection + wastewater treatment
(fixed + volumetric). Published comparators at matching scope
(residential + multi-res):

| Component | Published res+MR | Source quality |
|---|---|---|
| Sanitary collection (2026F) | $135.4M ($106.0M res + $29.4M multi-res) | sourced (Table 20.2-1) |
| Wastewater treatment | $108.2M in 2024 ($83.8M single-family + $24.4M multi-res); ~ $115M by 2026 | sourced 2024 (Table 12.4-1); 2026 escalated |
| In-city water | 2024 actual $254.9M **all classes**; res+MR share est. ~70% → ~$190M at 2026 rates | share ESTIMATED (water PBR class split unreachable, §0) |
| **Total** | **≈ $440M (range $420–470M)** | |

**Ratio: modeled / published ≈ 1.33× (range 1.25–1.40×).** Same
hundred-million band → order-of-magnitude PASS.

**Count cross-check:** EPCOR 2026F accounts = 304,511 residential +
3,878 multi-res = **308,389** vs the model's **268,489 connections**
(~13% UNDER). So the dollar excess is per-connection (households per
connection, consumption proxy), not connection count.

**Where the ~1.3× lives (all model-side inflators, direction consistent):**
1. **Modeled households 551,831 run ~20% over census dwellings** — the
   `M2_GROSS_PER_UNIT = 90` floor-area→units estimate for OTHER
   RESIDENTIAL. **Sensitivity check DONE 2026-07-07** (see §2.1 below):
   the assumption moves household *count* a lot but citywide *dollars*
   very little (~±5% across a 70–120 m²/unit sweep), so it is NOT where
   the ~1.3× gap lives.
2. **Consumption proxy 14.3 m³/mo** vs EPCOR's actual 2023 average of
   13.8 m³/mo and a four-decade declining trend (PBR p. 63) — ~+4%.
3. **Occupancy**: the model bills every roll household; EPCOR bills
   active accounts (vacancy excluded).
4. **Rate vintage**: full 365 days at April-2026 tariffs vs EPCOR years
   blending 3 months of prior rates — ~+2–3%.
5. Meter-size band assumptions drive the $133.9M fixed component
   (unvalidated separately; no published fixed/volumetric split found).

### 2.1 `M2_GROSS_PER_UNIT` sensitivity (DONE 2026-07-07)

Swept the multi-res floor-area→units divisor across 70–120 m²/unit
(baseline 90) via `tools/sensitivity_m2_per_unit.py`, on real regenerated
data. The parameter only estimates OTHER RESIDENTIAL unit counts; nothing
else in the model touches it.

| m²/unit | connections | households | vs census* | citywide $/yr | Δ vs 90 |
|--------:|------------:|-----------:|-----------:|--------------:|--------:|
| 70  | 268,489 | 591,898 | 1.29× | $622.0M | +5.8% |
| 80  | 268,489 | 569,323 | 1.24× | $602.8M | +2.5% |
| **90** | **268,489** | **551,831** | **1.20×** | **$588.1M** | **baseline** |
| 100 | 268,489 | 537,878 | 1.17× | $576.5M | −2.0% |
| 110 | 268,489 | 526,466 | 1.14× | $567.4M | −3.5% |
| 120 | 268,489 | 516,885 | 1.12× | $559.1M | −4.9% |

\* census anchor ≈ 459,859 (= 551,831 / 1.20, implied by §2.1's ~20%).

**Findings:**
- **Connection count is invariant** (268,489 everywhere) — the divisor
  never touches the 13%-under-EPCOR connection count. Confirms the gap is
  per-connection, not count.
- **Households are highly sensitive** (~75k / ±7% span across the sweep)
  but **dollars are not** (~±5%). Multi-res units bill on the declining
  volumetric block and share a building's fixed meter charge, so marginal
  estimated units are cheap — the household overcount is mostly harmless
  to the modeled revenue. This confirms the earlier "~4% of total" bound.
- **Reconciling the count to census would require m²/unit well above 120**
  (extrapolating, ~145+), and even then citywide $ falls only ~7–8% — far
  short of closing the ~1.33× vs EPCOR. **The 90 baseline stands**; the
  gap is per-connection (consumption proxy + occupancy + rate vintage,
  items 2–4 above), not this assumption.

## 3. Set-aside / unbilled-land decision — DECIDED: report BOTH (Peter, 2026-07-07)

The bracket was quantified from the options below, and Peter picked the
recommendation: **any citywide stormwater claim states both the
all-parcels total AND the total excluding `notyet` + `never` zones.**
- All-parcels $240.4M labeled MODELED — honest but 1.7× billed reality.
- Exclude set-aside hoods → $207.3M (hood-level cut, coarse; not used).
- Exclude `notyet` + `never` zone categories → **$190.5M** (zone-level
  cut, sharper: it tracks EPCOR's actual billing boundary better and is
  computable per-point inside `load_stormwater`).

Shipped same day: `UNBILLED_CATEGORIES = ("notyet", "never")` in
`src/load_stormwater.py`; the module's log line reports both totals and
the returned frame's `.attrs` carries `storm_citywide_annual` /
`storm_billable_annual`. Per-hood outputs (and therefore the map) are
unchanged — this is reporting, not modeling. Real-data run: citywide
$240.4M / billable $190.5M, 5,601 unbilled points.

## 4. Methodological gotcha (recorded for future validators)

Recovering hood totals as `per_acre × area` from
`web/data/neighbourhood_value_per_acre.geojson` geometry **understates
totals ~15%**: the web geometry carries a display setback (inward buffer)
plus simplification (`join_and_calculate.write_slim_geojson`). Use
`load_boundaries()` full-res `area_acres` joined by `neighbourhood_name`
instead — that reproduces the pipeline totals exactly ($240.4M / $588.1M).

## 5. Electricity/gas franchise (Lens 3) — modeled $162.6M/yr City revenue, residential

Built 2026-07-07 as **columns only** (SPEC_utilities "Lens 3+4 as built").
Modeled City-revenue lines, residential scope, on the SAME 551,831-dwelling
model as Lens 2 (shared `build_connections`):

| Line | Rate | Modeled $/yr |
|---|---|---|
| Electricity distribution (EDTI DAS-R) | $0.69953/day + $0.01712/kWh @ 7,200 kWh | $208.9M |
| **Electricity Local Access Fee** | **17.65% of distribution** | **$36.9M** |
| Gas delivery (ATCO Gas North + Riders T/L) | $0.997/day + $2.497/GJ @ 115 GJ | $359.3M |
| **Gas franchise fee (Rider A)** | **35% of delivery** | **$125.7M** |
| **Combined City franchise revenue** | | **$162.6M** |

**Collinearity (the defining caveat):** the proxy is flat per dwelling, so
every per-hood column is `dwellings × constant` — the map would re-plot
dwelling density, nothing more. Hence columns only, and `dwelling_count`
ships explicitly. This is the SPEC's Tier-3 caveat made concrete.

**Known underestimate — modeled LAF ~⅓ low.** Modeled electricity LAF is
**$5.57/mo/dwelling vs the City's published ~$8.33/mo** (2026, Methods §D).
The 17.65% fee is levied on EDTI's FULL forecast distribution revenue
(riders, pass-throughs, adjustments), not the base customer+energy schedule
modeled here. A transparent underestimate; correcting it would scale the LAF
line up ~1.5× (≈$55M residential) but not change the per-hood shape.

### 5.1 Cross-check vs the City's audited franchise-fee line (DONE 2026-07-07)

Closed against **Note 24 of the 2024 Financial Annual Report** (§0 source 3),
now that edmonton.ca is reachable. City actual 2024 franchise revenue:
**Gas (ATCO) $95.2M**, **Power (EPCOR Distribution) $80.8M** → **combined
electricity + gas $175.9M** (all-sector; residential + commercial + industrial).

| Line | Modeled (residential) | City actual 2024 (all-sector) | Ratio |
|---|---|---|---|
| Gas franchise (Rider A 35%) | $125.7M | $95.2M | **1.32×** |
| Electricity Local Access Fee | $36.9M | $80.8M | **0.46×** |
| **Combined elec + gas** | **$162.6M** | **$175.9M** | **0.92×** |

**The combined 0.92× is a coincidence of two offsetting errors, not a clean
pass.** Read the two lines separately:

- **Gas overshoots (1.32×) — a residential-only model should not exceed the
  all-sector actual.** The cause is almost certainly the **transmission
  Rider T** ($1.357/GJ, the largest variable component): our 35% is levied on
  a delivery base that includes it. Excluding Rider T drops modeled gas to
  **$95.6M ≈ 1.00× actual**. That near-exact landing is itself a caution —
  residential-only matching an all-sector figure implies either residential
  dominates Edmonton's gas-franchise base or the 115 GJ/dwelling proxy runs
  high — so **excluding Rider T is a strong candidate correction, not proven.**
  Flagged for a decision (see TODO); the rates JSON already isolates
  `gas_rider_t_per_gj` so the change is one line.
- **Electricity undershoots (0.46×) — confirms and sharpens the known "~⅓ low"
  caveat.** Actual $80.8M ÷ 17.65% implies a real EDTI distribution base of
  **$457.7M**, 2.19× our modeled $208.9M. The gap is the base+energy schedule
  missing riders/pass-throughs AND commercial/industrial customers (residential
  scope). The LAF line is a documented floor, not an estimate of the true fee.

**Net:** the modeled City franchise revenue is the right order of magnitude
(0.92× combined), but the honest read is line-by-line — gas is high (Rider T),
electricity is a residential-only floor. Both errors are understood and point
the same way the caveats predicted.

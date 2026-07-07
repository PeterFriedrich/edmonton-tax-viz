# Findings — Utility Lens Validation vs EPCOR Published Revenue

**Date:** 2026-07-07 (Session 19). Closes the TODO validation item for
Lens 1 (stormwater) and Lens 2 (water + sanitary).
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
   RESIDENTIAL (SPEC bound: ~4% of total, but the sensitivity check is
   still open — see TODO follow-up).
2. **Consumption proxy 14.3 m³/mo** vs EPCOR's actual 2023 average of
   13.8 m³/mo and a four-decade declining trend (PBR p. 63) — ~+4%.
3. **Occupancy**: the model bills every roll household; EPCOR bills
   active accounts (vacancy excluded).
4. **Rate vintage**: full 365 days at April-2026 tariffs vs EPCOR years
   blending 3 months of prior rates — ~+2–3%.
5. Meter-size band assumptions drive the $133.9M fixed component
   (unvalidated separately; no published fixed/volumetric split found).

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

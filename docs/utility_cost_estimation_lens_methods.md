# Parcel-Level Utility Cost-of-Service Modeling for Edmonton: An Implementation Guide for a Revenue-per-Acre / Value-per-Acre Fiscal Tool

## TL;DR
- **All five Edmonton utilities can be reconstructed at the parcel level from official 2025/2026 tariffs plus Edmonton open data, but only stormwater has a truly parcel-native formula (Area × Intensity × Runoff Coefficient × $0.00327/m²/day) written directly into bylaw; water, wastewater, electricity, and gas must be modeled via meter-size fixed charges plus consumption-proxy volumetric charges because per-parcel meter reads are not public.**
- **Methodologically, keep the headline metric land/area-driven: stormwater (area-based) and the electricity Local Access Fee (now a franchise fee = 17.65% of forecast distribution revenue since March 17, 2025) are the cleanest cost/revenue signals; avoid per-capita allocation entirely and treat density as a cost-side variable, consistent with Urban3/Strong Towns value-per-acre practice.**
- **The BILD "developers already paid" argument is real for upfront capital but incomplete: a defensible cost-of-service model must separate developer-contributed assets from the lifecycle renewal + operating liabilities the City/EPCOR inherit — evidenced by the paused (May 13, 2024) Sanitary Sewer Trunk Charge and Edmonton's comparatively low off-site levies, which show general ratepayers cross-subsidizing new suburban trunk infrastructure.**

## Key Findings

### 1. Stormwater is the only utility with a bylaw-native parcel formula
EPCOR Wastewater Services Bylaw 20865 defines the daily stormwater charge as **A × I × R × Rate**, where A = parcel area (m²), I = Development Intensity Factor (default 1.0), R = runoff coefficient keyed to Zoning Bylaw 20001 zone codes, and Rate = **$0.00327/m²/day effective April 1, 2026** (verified on EPCOR's rate page; the prior rate was $0.092750/month effective April 1, 2025, before the monthly-to-daily transition). This is directly computable from a zoning layer and parcel geometry with zero consumption data required.

### 2. Water, wastewater, and sanitary use meter-size fixed charges + volumetric rates
Effective April 1, 2026 (EPCOR transitioned these from monthly to **daily** fixed charges):
- **Residential water consumption:** $2.5258/m³ (0–10 m³), $2.7593/m³ (10.1–35 m³), $3.4873/m³ (>35 m³).
- **Water fixed daily service charge** (15mm meter): $0.5359/day; scales up by meter size to $90.4715/day (300mm).
- **Wastewater treatment:** $1.3020/m³ (all consumption) + $0.2269/day fixed.
- **Sanitary (sewer collection):** $1.27331/m³ residential variable + fixed daily charge by meter size ($0.3625/day at 15mm).
- **Typical residential consumption benchmark:** per EPCOR's Wastewater Collection Rates FAQ, "a typical residential Edmonton household used 14.3 cubic metres (14,300 litres) of water per month in 2025" — this is the key proxy when meter reads are unavailable.

### 3. Electricity distribution (EDTI) is AUC-regulated with a clean per-parcel structure
EDTI residential Distribution Access Service (DAS-R, effective Jan 1, 2025): **Customer Charge $0.69953/day + Energy Charge $0.01712/kWh** (distribution only). The **Local Access Fee / franchise fee is now 17.65% of forecast distribution revenue** (Bylaw 20959, effective March 17, 2025). Per City of Edmonton Public Notice Bylaw 21163, this was "an increase from the prior agreement's converted percentage equivalent of 15.3 per cent," and "the average monthly franchise fee for an average residential customer is forecast to increase from approximately $6.66 in 2024 to $7.94 in 2025." This is both a cost driver and a direct municipal revenue line.

### 4. Natural gas distribution (ATCO Gas North) delivery rates
ATCO Gas North "Low Use" residential delivery service (effective Jan 1, 2026, Decision 30301-D01-2025): **Fixed Charge $0.997/day + Variable Charge $1.049/GJ**, plus Rider T transmission $1.357/GJ and Rider L load-balancing $0.091/GJ debit (May–Dec 2026). Edmonton's natural gas franchise fee (Rider A) is **35.00%** of gross delivery revenue (effective Jan 1, 2019). Typical residential gas consumption ~110–120 GJ/year with strong seasonal swing (~3 GJ summer to ~23 GJ winter per month per UCA profiles).

### 5. Consumption proxies (essential — no per-parcel meter data is public)
- Water/sanitary: 14.3 m³/household/month (2025); per-capita 176 L/c/d residential (2019), with EPCOR's design standard reduced to 160 L/c/d for neighbourhood-level planning.
- Electricity: ~7,200 kWh/household/year (600 kWh/month).
- Natural gas: ~110–120 GJ/household/year.

## Details

### A. POTABLE WATER (EPCOR Water Services Inc / EWSI)

**Regulator & currency:** City of Edmonton regulates EWSI under Performance-Based Regulation. Water PBR plan approved 2022, runs to March 31, 2027. Rates below effective **April 1, 2026**.

**Verified 2026 tariff (residential):**
- Consumption (inclining block): $2.5258/m³ (0–10 m³); $2.7593/m³ (10.1–35 m³); $3.4873/m³ (>35 m³).
- Fixed daily service charge by meter size: 15mm $0.5359; 20mm $0.8042; 25mm $1.3401; 40mm $2.6798; 50mm $4.2875; 100mm $13.3996; 300mm $90.4715.
- Public Fire Protection charge also scales by meter size (15mm $0.0963/day).
- **Multi-residential** consumption: $2.3842/m³ (0–100 m³); $1.9949/m³ (100.1–1000 m³); $1.6484/m³ (>1000 m³) — declining block, opposite of the residential inclining block.

**Computable parcel formula (annual $):**
```
annual_water = 365 * fixed_daily[meter_size]
             + 12 * sum_over_blocks(monthly_m3 proxy, block_rates)
# monthly_m3 residential proxy = 14.3 (2025 EPCOR benchmark)
# meter_size proxy: 15mm for single-family; larger for multi-res/commercial by units/floor area
```

**Proxy guidance:** Where no meter read exists, use 14.3 m³/month for single-family. For multi-family, scale by dwelling units × per-unit consumption (per-capita 160 L/c/d design standard × household size, or use EPCOR's hexagon water-usage open dataset for spatial calibration). Meter size is the dominant fixed-cost driver and must be inferred from building type/size.

**Flag:** Meter size is not in open parcel data; it must be assumed by land-use class. This is a modeled assumption, not a verified per-parcel value.

### B. WASTEWATER / SANITARY (EPCOR; Gold Bar Wastewater Treatment Plant)

**Currency:** Wastewater PBR plan (2025–2027, Bylaw 20865) approved by City Council Feb 4, 2025, effective April 1, 2025; rates below effective April 1, 2026.

**Verified 2026 tariff (residential):**
- Wastewater treatment: $1.3020/m³ + $0.2269/day fixed.
- Sanitary collection: $1.27331/m³ + fixed daily by meter size (15mm $0.3625; 25mm $1.0150; 100mm $10.3248; 300mm $77.3296).
- Both variable charges are billed on **metered water consumption** (no separate wastewater meter). If no meter, charges default to Bylaw 20865 provisions.

**Computable formula:**
```
annual_sanitary = 365*(ww_fixed_daily + san_fixed_daily[meter_size])
                + 12 * monthly_m3 * (1.3020 + 1.27331)
```

**Capital cost structure (for reconstructing true asset-delivery cost):** Per EPCOR's 2025–2027 Wastewater PBR Application, "planned capital investments for Wastewater Collection ... is expected to be $687.9 million, and for Wastewater Treatment ... $199.8 million" (≈$887.7M combined). Capital structure: **60% debt / 40% equity**; 2027 debt cost rate 4.07%; the application recommends increasing "return on equity (ROE) for Wastewater Collection to a fair equity return of 10.8%" (ramped: 9.0% in 2025, 9.9% in 2026, 10.8% in 2027), though Bylaw 20865 as approved Feb 4, 2025 set an allowed ROE of 10.50% for the term — for a WACC of ~6.76%. This return-on-rate-base is what makes utility-delivered infrastructure genuinely costly versus developer-contributed mains.

### C. STORMWATER / DRAINAGE (EPCOR Drainage; Bylaw 20865)

**Verified formula (bylaw-native):** Daily stormwater charge = **A × I × R × Rate**
- **A** = parcel area in m² (for multi-unit, proportion of lot per unit).
- **I** = Development Intensity Factor, **default 1.0**; reduced only via Stormwater Intensity Adjustment Program (SIAP) application (commercial and multi-family RM/RL only).
- **R** = runoff coefficient by Zoning Bylaw 20001 zone.
- **Rate = $0.00327/m²/day (effective April 1, 2026)** — EPCOR's rate page states "The stormwater utility rate — the daily rate as of April 1, 2026 is $0.00327."

**Verified runoff coefficient table (New Zoning Bylaw 20001 zones, effective April 1, 2025):**
| R | New zone codes |
|---|---|
| 0.1 | AG |
| 0.2 | A, AG, NA, RR, RVSA |
| 0.3 | PS, PSN |
| 0.4 | FD |
| 0.5 | AJ, RS/RSF >450m² |
| 0.55 | PU, RM/RSM >450m², RS/RSF <450m², UF, DC <700m² |
| 0.6 | RL, RM/RSM <450m², UI, DC >700m² |
| 0.65 | CN, MUN |
| 0.75 | BE, CB, CG, IH, IM, MU |
| 0.9 | (mapped high-runoff commercial/industrial) |
| 0.95 | (highest-runoff commercial) |

Note: runoff coefficients differ by lot size for residential (<450m² vs >450m²) and DC zones (<700m² vs >700m²). Zones not in the table default (at EWSI discretion) to the closest-aligned zone.

**Computable formula:**
```
annual_stormwater = 365 * area_m2 * I * R_lookup(zone_code, area_m2) * 0.00327
# I = 1.0 default; apply SIAP reduction only if modeling a specific credited parcel
```

**Condo/multi-family handling:** Area is apportioned per unit (building lot area × unit share). SIAP reductions are available to commercial and RM/RL multi-family that install Low Impact Development (LID); the LID Inventory open dataset (3xir-jjpa; map view xjna-dgrc) can flag credited parcels.

**Cost-allocation note:** The 2024 HDR cost-of-service study explicitly states stormwater cost is "a function of a parcel's impervious area and intensity of development/runoff coefficient" — validating the area-driven approach. The study shifted revenue so sanitary decreased and stormwater increased (each within 5% of cost of service; previously sanitary over-collected ~16% and stormwater under-collected ~16%). Effective April 1, 2025, EPCOR also began billing previously unbilled stormwater-only properties (City recreation sites, cemeteries, golf courses), adding ~$1.7M in City stormwater billing.

### D. ELECTRICITY DISTRIBUTION (EDTI, AUC-regulated)

**Verified 2025 DAS tariff (Decision 29293-D01-2024, effective Jan 1, 2025):**
- Residential (DAS-R): Customer Charge $0.69953/day + Energy Charge $0.01712/kWh.
- Commercial <50 kVA (DAS-SC): $0.61346/day + $0.03207/kWh.
- Commercial 50–150 kVA (DAS-MC): $1.87271/day + demand $0.26066/kVA/day.
- 2026 interim rates approved (Decision 30298-D01-2025); a typical 600 kWh/month household sees ~$2.52/month total-bill increase in 2026 (+1.2%).

**Local Access Fee / franchise fee:** Historically Edmonton uniquely used a consumption-based (¢/kWh) LAF (e.g., 0.72¢/kWh in 2015). As of March 17, 2025 (Bylaw 20959 / AUC Decision 29644-D01-2025), the fee is **17.65% of forecast distribution revenue** (note: EDTI's application discussed a 17.65% aggregate, and the AUC directed the fee be applied to "forecast" rather than "actual" revenue). Average residential monthly franchise fee: ~$6.66 (2024) → ~$7.94 (2025) → ~$8.33 (2026). This is a direct municipal revenue driver and a proxy for localized distribution load.

**Computable formula:**
```
annual_elec_distribution = 365 * cust_charge_daily + annual_kWh * energy_charge_kWh
annual_LAF_revenue = 0.1765 * annual_elec_distribution   # municipal revenue
# annual_kWh residential proxy = 7,200
```

### E. NATURAL GAS DISTRIBUTION (ATCO Gas North, AUC-regulated)

**Verified 2026 tariff (Low Use residential, ≤1,200 GJ/yr):**
- Fixed Charge $0.997/day + Variable Charge $1.049/GJ (effective Jan 1, 2026, Decision 30301-D01-2025).
- Rider T transmission $1.357/GJ (Decision 30329-D01-2025); Rider L load-balancing $0.091/GJ debit (May–Dec 2026).
- **Edmonton gas franchise fee (Rider A): 35.00%** of gross delivery revenue (effective Jan 1, 2019); Rider B municipal property tax rider 5.60% (effective Feb 1, 2026).

**Computable formula:**
```
annual_gas_delivery = 365 * 0.997 + annual_GJ * (1.049 + 1.357 + 0.091)
# annual_GJ residential proxy = 110-120, with seasonal split ~3 GJ summer / ~23 GJ winter month
annual_gas_franchise_revenue = 0.35 * gross_delivery_charges
```

### F. PBR RATE-PROJECTION MECHANICS (for forward rate modeling)

**EPCOR water/wastewater PBR:** Rates escalate by **I − X** where I = weighted average of Alberta Average Hourly Earnings (AHE) and CPI, X = efficiency factor. Capital funded via K-factor (Type 1 trackers) and K-bar (Type 2 formula-based). Y factors = flow-through costs; Z factors = exogenous events.

**EDTI electricity PBR3 (2024–2028, Decision 27388-D01-2023):** I factor = Alberta Fixed Weighted Index labour price index, **60% labour / 40% non-labour weighting**, forecast-and-true-up. **TFP growth factor 0.1%**, plus X-factor benefit-sharing premium of 0.3% (aggregate X ~0.4%; for K-bar calculation purposes X = 0.1% as it excludes the benefit-sharing premium). K-factor/K-bar capital, Y/Z factors as above.

```
rate_next_year = rate_this_year * (1 + I - X) + K_adjustment + Y + Z
```

### G. METHODOLOGICAL BEST PRACTICE: keep the metric land-driven

The value-per-acre / revenue-per-acre framework (Urban3, Strong Towns) deliberately normalizes by **land area**, not population, because dense/walkable development "uses just a few dozen yards of street and sidewalk and pipe while generating tons of revenue" (Strong Towns' canonical Asheville example: a downtown building generated $634,000/acre in property tax vs. a Walmart's $6,500/acre). Density belongs on the **cost side** (more units served per linear meter of main lowers per-parcel infrastructure cost), never folded into revenue. Urban3's own cost-of-service work (e.g., Edmond, OK) explicitly separates "per acre cost for infrastructure operations—water, sewer, and electric" from population-based services (fire, police).

**Recommended costing method per utility:**

| Utility | Recommended method | Required parcel inputs | Primary data source | Verification status |
|---|---|---|---|---|
| Stormwater | **Area-driven (ideal)** — A×I×R×rate | Parcel area, zone code | Bylaw 20865; zoning fixa-tstc; AltaLIS parcels | Verified formula + rate |
| Water | Connection + consumption proxy | Meter size (assumed), land-use | EPCOR 2026 rates; 14.3 m³/mo | Verified rates; proxy consumption |
| Sanitary/WW | Connection + consumption proxy | Meter size (assumed), land-use | EPCOR 2026 rates | Verified rates; proxy consumption |
| Electricity | Connection + consumption proxy; LAF as revenue | Land-use, ~7,200 kWh/yr | EDTI DAS-R; Bylaw 20959 | Verified rates + 17.65% fee |
| Natural gas | Connection + consumption proxy; 35% franchise as revenue | Land-use, ~110–120 GJ/yr | ATCO Gas North; Rider A | Verified rates + 35% fee |

**Pitfall to flag and stress-test:** Any method that allocates utility cost by per-capita or dwelling-count-only allocation will (a) penalize dense parcels that are actually cheaper to serve per unit of land, and (b) reward sprawl by hiding the linear-infrastructure cost. The Halifax Regional Municipality greenfield/cost-of-services work and Hemson's Ottawa and Vancouver development-charge studies allocate growth-related underground servicing on a **per-hectare / area basis**, corroborating the area-driven approach.

### H. EDMONTON OPEN DATA — dataset verification

- **Parcel geometry is RESTRICTED.** As of Nov 1, 2021, the City no longer provides land parcel boundary polygons; these are licensed via Alberta Data Partnerships (ADP) / AltaLIS. Open alternatives: Parcel Addresses (point centroids: ut27-nrpn, vzn8-xges, dwy4-xicg), assessment-roll lot areas, or building-footprint proxies. This is the single biggest data blocker for the area-driven stormwater module and should be resolved first.
- **Zoning: use current Zoning Bylaw Geographical Data (fixa-tstc)** and its Map View (ruwn-htv8) — these reflect Bylaw 20001 and carry the current zone codes used in the runoff-coefficient table. **Do NOT use "Zoning Bylaw Map - History" (67p2-r285)**, which is a stale/historical layer keyed to old Bylaw 12800 zone codes (RF1, CB1, etc.); pulling it into a residential-only filter would misclassify runoff coefficients and mismatch the current-zone R-table above.
- **Drainage datasets:** Drainage Pipe Segments (bh8y-pn5j), Drainage Map View Pipe Segments (irc5-87br), Drainage Map View Outfall (efaq-9jrb) — useful for network/asset and catchment context but **not** for per-parcel billing (they describe infrastructure, not tariff inputs).
- **Low Impact Development Inventory (3xir-jjpa; map view xjna-dgrc)** — flags SIAP-eligible/credited parcels for the I-factor reduction.

### I. COUNTER-NARRATIVE: BILD Urban Growth Case Study and cross-subsidization

**The BILD case:** BILD Edmonton Metro's Urban Growth Case Study (Heritage Valley + Windermere, SW Edmonton) reports, per VP Lindsey Butterfield, that "over $3.2 billion will be invested by the private sector … $2.4 billion of that is in road infrastructure alone," and "the area is expected to contribute approximately $309 million annually in property tax revenue" at full build-out (~171,000 residents), versus the City "currently collect[ing] over $163 million dollars annually from Heritage Valley and Windermere." City O&M is ~$14M/year roadways + $9.7M/year parks; BILD projects a ~$60M/year net surplus extrapolated across the study area.

**Correct cost-of-service treatment:** The "developers already paid" claim is valid for **upfront capital** (roads and utility mains dedicated to the City on completion). But it omits the **long-tail lifecycle liability**: once assets transfer, the City/EPCOR inherit renewal (the wastewater PBR return-on-rate-base at ~10.5–10.8% ROE on ~$888M of planned capital shows how expensive asset ownership is) plus perpetual O&M. Edmonton's Capital Investment Outlook confirms the scale of this inherited liability: as reported by Taproot Edmonton (Jan 26, 2026), the city "will be able to spend about $11 billion on both renewal and growth projects in the next 10 years, leaving a funding shortfall of $10 billion," and even directing all funding to renewal would meet "only 39% of the ideal renewal investment." A defensible model books developer capital as a one-time contribution (avoided cost) but still charges the parcel its share of lifecycle renewal + operating cost.

**Evidence of cross-subsidization:**
- **Off-site levies** are comparatively low: the Desjardins June 2026 development-fee study notes Edmonton "applies a suite of targeted instruments rather than a comprehensive charge," while Calgary applies single-detached infill water/wastewater charges "set at $9,328 per unit and broader per-hectare fees for greenfield development" — a signal that Edmonton recovers less of growth's servicing cost upfront than several peers.
- **Sanitary Sewer Trunk Charge PAUSED May 13, 2024** (SSSF Oversight Committee), including Expansion Assessment charges, during the SSSF Transformation project. The 2024 SSTC residential rate was $1,764/principal dwelling ($1,259/unit for new apartments). Per the City's SSSF Program page, "as of the end of 2024, approximately $361 million has been spent on deep sanitary trunk construction through the SSSF," with only $4.9M spent and $17.3M in revenue collected in 2024. With SSTC paused, new suburban trunk infrastructure is currently funded from the general SSSF/ratepayer base rather than fully from growth — direct evidence that growth is not fully self-funding its trunk servicing.

## Recommendations

**Stage 1 — Build the stormwater module first (highest fidelity, lowest data risk aside from parcel geometry).** Implement `A × I × R × 0.00327 × 365`. Join current zoning (fixa-tstc) to AltaLIS parcel polygons; hard-code the verified runoff-coefficient table with the <450m²/>450m² and DC <700m²/>700m² splits; default I=1.0. **Threshold to change approach:** if you cannot license AltaLIS polygons, fall back to assessment-roll lot areas or building-footprint proxies and flag output as estimated.

**Stage 2 — Add water/sanitary using meter-size fixed charges + 14.3 m³/month proxy.** Build a meter-size lookup keyed to land-use class (15mm single-family default). Model multi-residential with the declining-block water schedule and per-unit consumption.

**Stage 3 — Add electricity (7,200 kWh/yr) and gas (110–120 GJ/yr) delivery, and compute the LAF (17.65% of distribution revenue) and gas franchise fee (35% of gross delivery revenue) as municipal revenue lines.** These close the loop between cost and the revenue-per-acre metric.

**Stage 4 — Layer PBR escalation** (`rate × (1 + I − X) + K + Y + Z`) for forward-year projections; document I/X assumptions (electricity aggregate X≈0.4%, K-bar X=0.1%; water/wastewater I from AHE+CPI blend).

**Stage 5 — Book developer capital correctly.** Represent developer-contributed assets as avoided upfront capital, but always charge each parcel its lifecycle-renewal + O&M share (use the PBR return-on-rate-base logic and the $10B renewal-gap context). Surface the SSTC pause and low off-site levies as explicit cross-subsidy flags in the tool's output.

**Thresholds/benchmarks that change these recommendations:** New PBR decisions (water PBR expires March 31, 2027; the next filing will reset base rates); resumption of the SSTC after the SSSF Transformation project concludes; any change to the 17.65% electricity or 35% gas franchise fee percentages; and annual rate resets (re-pull before each production run).

## Caveats
- **Verified official figures:** all tariff rates cited (water/wastewater/sanitary/stormwater effective April 1, 2026; EDTI DAS effective Jan 1, 2025; ATCO Gas North effective Jan 1/May 1, 2026), the stormwater formula and $0.00327/m²/day rate, the runoff-coefficient table, the 17.65% electricity and 35% gas franchise fees, the ~$888M ($687.9M + $199.8M) wastewater capital plan and 60/40 debt-equity split with ~10.5–10.8% ROE, the SSTC pause date and 2024 rates, the $361M deep-trunk spend, and the $10B/11B infrastructure renewal-gap figures.
- **Reasonable estimates/proxies (require assumption):** meter-size-by-land-use mapping (not in open data); per-parcel consumption (uses citywide/household benchmarks); apportionment of multi-unit stormwater area; household size for per-capita conversions. Any parcel-level output built on these should be labeled "modeled," not "billed."
- **Currency:** utility rates reset annually — water/wastewater on April 1, electricity/gas on Jan 1. The daily-rate transition (April 1, 2026) means annualization should multiply daily charges by the actual day count, not 12×monthly.
- **Parcel geometry licensing (AltaLIS) is the key open-data constraint** and may require a paid license or an assessment-roll/footprint fallback.
- The BILD figures are advocacy-sourced projections (net surplus, full build-out revenue) and should be presented as such, not as realized outcomes; the counter-analysis (lifecycle liability, SSTC pause) is the appropriate corrective framing for a neutral fiscal tool.
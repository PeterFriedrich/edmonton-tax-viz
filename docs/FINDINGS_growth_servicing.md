# Findings — Growth Servicing Cost Recovery: Two Ledgers

**Date:** 2026-07-10. `ANALYSIS_BACKLOG.md` item 5, **auto half** (the by-hand
half — SSTC resumption tracking, reading the BILD study and Capital Investment
Outlook primary documents — remains open and is laptop-gated). Reproducible via
`tools/analyze_growth_servicing.py` (run from the repo root against the
standing `data/raw/` inputs and the served `web/data/` GeoJSON).

**Framing rule.** This document presents **two ledgers side by side** — the
development industry's revenue/upfront-capital ledger and the
inherited-liability ledger — per the neutral-tone rule: surface the data,
attribute the claims, no verdict language. Both external framings cited here
carry advocacy weighting (source citations: `docs/
utility_cost_estimation_lens_methods.md` §I); everything quoted from them is
labeled as a claim, not adopted as fact.

## 1. The question

BILD Edmonton Metro's Urban Growth Case Study (Heritage Valley + Windermere,
SW Edmonton) argues new growth is fiscally net-positive: per the study, over
$3.2B in private capital is invested upfront (~$2.4B of it roads), the City
"currently collect[s] over $163 million" annually from the area, and it is
projected to contribute ~$309M/yr in property tax at full build-out (~171,000
residents), against City O&M of ~$14M/yr roadways + $9.7M/yr parks. The
counter-consideration: once developer-built assets transfer, the City/EPCOR
carry lifecycle renewal and O&M in perpetuity — against a documented ~$10B
ten-year infrastructure renewal shortfall — and trunk-servicing cost recovery
is currently reduced (Sanitary Sewer Trunk Charge paused since 2024-05-13).
What can Edmonton's own data say about either side?

## 2. Method

- **Unit:** neighbourhood (406 served hoods; 48 set-aside excluded from
  distribution stats, matching the views; 358 kept).
- **Era bands** over each hood's **median `year_built`** (`dkk9-cj3x`,
  cleaned to 1870–2026): pre-1970 / 1970–89 / 1990–2009 / 2010+. This is
  median *building-stock* age, not plat date — infill pulls mature hoods'
  medians later (a pre-1950 band holds only 2 hoods, hence pre-1970 as the
  finest "mature grid" band). 349 kept hoods have a banded median (9 lack
  `year_built` data — counted, dropped).
- **Dwelling denominators, both models** (convention from
  `FINDINGS_land_use_diversity.md`): residential-record count (**rec** —
  condo units are individual records) and the water lens's
  `build_connections` unit model (**bc**). Per-dwelling medians are computed
  over hoods with ≥ 100 residential records (278 hoods; 71 excluded,
  counted).
- **Columns:** municipal levy (mill rates, municipal share only — no
  education requisition), within-boundary road centreline metres, modeled
  EPCOR stormwater and water/wastewater charges, fire-rescue dispatches/yr.
- **Construction caveat on the modeled utility columns:** they are functions
  of built form, not observed billing. The water model is ~per-connection/
  per-unit by construction, so water $/dwelling is nearly constant across
  eras *by design*; the stormwater model is area × runoff coefficient, so
  storm $/acre mostly tracks zoning mix. Era differences in these columns
  describe built form, not utility behaviour.

## 3. What Edmonton's data shows, by era

### 3.1 Per acre (medians, 349 hoods)

| era | n | levy $/ac | road m/ac | storm $/ac | water $/ac | fire ev/ac | developed frac |
|---|---|---|---|---|---|---|---|
| pre-1970 | 75 | 17,512 | 47 | 1,432 | 6,805 | 0.81 | 0.90 |
| 1970–89 | 120 | 17,389 | 35 | 1,559 | 6,355 | 0.60 | 0.90 |
| 1990–2009 | 93 | 23,951 | 32 | 1,654 | 7,624 | 0.50 | 0.90 |
| 2010+ | 61 | 20,759 | 23 | 1,533 | 6,561 | 0.28 | 0.75 |

### 3.2 Per dwelling (medians, 278 hoods with ≥ 100 res records)

| era | n | levy $/dw (rec) | (bc) | road m/dw (rec) | (bc) | storm $/dw | fire ev/1k dw |
|---|---|---|---|---|---|---|---|
| pre-1970 | 73 | 4,707 | 3,490 | 13.0 | 10.0 | 400 | 221 |
| 1970–89 | 86 | 3,905 | 2,904 | 8.9 | 6.8 | 359 | 155 |
| 1990–2009 | 68 | 4,340 | 3,736 | 7.0 | 6.2 | 298 | 103 |
| 2010+ | 51 | 4,473 | 3,928 | 6.4 | 5.4 | 363 | 70 |

Three observations, robust to both dwelling models:

1. **Road supply per dwelling falls with newness — roughly halving from the
   mature grid to post-2010 greenfield** (13.0 → 6.4 m/dw record proxy;
   10.0 → 5.4 bc; r(median year_built, road m/dw) = −0.53 rec / −0.34 bc).
   Within their own boundaries, new greenfield hoods carry *less* local road
   per dwelling than the pre-1970 grid, not more. (What this measures — and
   does not — is in §6.)
2. **Fire-rescue demand per dwelling falls steeply with newness** (221 →
   70 events/1k dwellings/yr, a ~3× gradient). Dispatch demand concentrates
   in older building stock; the data does not distinguish the candidate
   mechanisms (stock condition, demographics, medical/social call mix,
   non-residential draws inside mature hoods).
3. **Levy per dwelling is roughly flat across eras** (medians $3.9–4.7k rec;
   $2.9–3.9k bc, with 2010+ the highest bc band). New-suburb dwellings
   contribute about what mature-hood dwellings contribute, today, per unit.

### 3.3 Build-out sensitivity

Growth hoods mid-build could carry roads ahead of dwellings (roads are built
first). Splitting the 2010+ band by remaining undeveloped zoned share:
near-built-out (`frac_notyet` < 0.10, n=27) median road/dw **6.3** m, levy/dw
$4,579; mid-build (n=24) road/dw **6.5** m, levy/dw $4,437. The road-supply
gradient is not a mid-build artifact.

Per-*acre* levy in the 2010+ band is depressed by unfinished land (developed
frac 0.75 vs 0.90 elsewhere). Renormalized to **levy per developed acre**, the
two post-1990 bands lead: 27,778 (1990–2009) and **27,978** (2010+) vs 20,863
(pre-1970) and 20,603 (1970–89). At the neighbourhood scale, the newer bands
out-earn the mature bands per developed acre on today's roll.

## 4. Ledger A — the revenue / upfront-capital side

The claims (BILD Urban Growth Case Study, attributed; methods doc §I): $3.2B
private upfront capital in Heritage Valley + Windermere ($2.4B roads); >$163M
currently collected; ~$309M/yr projected at full build-out (~171k residents).
The projections are **full-build-out figures, not realized outcomes**.

Our current-roll totals for the same two planning areas (20 hoods,
best-effort ASP membership — §6):

| | Heritage Valley (15 hoods) | Windermere (5 hoods) | Combined |
|---|---|---|---|
| area (acres) | 5,536 | 3,734 | 9,270 |
| municipal levy /yr | $115.1M | $96.3M | **$211.4M** |
| levy $/acre | — | — | 22,809 |
| dwellings (rec / bc) | 19,425 / 32,754 | 17,475 / 19,427 | 36,900 / 52,181 |
| road (m; m/dw bc) | 141,130 | 111,131 | 252,261 (4.8) |
| modeled storm /yr | $8.2M | $5.6M | $13.7M |
| modeled water /yr | $43.5M | $27.9M | $71.4M |
| fire events /yr | 1,996 | 808 | 2,804 |
| zoned land not yet developed | 17% | 15% | ~16% |

Data-side observations:

- The combined **$211M/yr municipal levy today** is 7.8% of the citywide
  $2.70B roll, from an area still ~16% undeveloped. It already exceeds the
  study's ">$163M currently" figure — consistent in direction with the
  study's build-out trajectory, though the study's collection figure, date,
  and exact area boundary are not verifiable from here (by-hand half).
- Combined levy per acre (22,809) runs above the kept-hood citywide median
  (19,081); per developed acre the area's era bands are the strongest in
  §3.3.
- On the *within-boundary* servicing columns we measure, the area's 4.8 road
  m/dwelling (bc) is well below the mature-grid median (10.0).

## 5. Ledger B — the inherited-liability side

The counter-framing (methods doc §I, attributed): developer capital is real
but **one-time**; on transfer the City/EPCOR inherit perpetual O&M plus
lifecycle renewal. Edmonton's Capital Investment Outlook (as reported by
Taproot Edmonton, 2026-01-26) puts the ten-year renewal+growth funding
envelope at ~$11B against a ~$10B shortfall, with full funding meeting "only
39% of the ideal renewal investment." The wastewater PBR's return-on-rate-base
(~10.5–10.8% ROE on ~$888M planned capital) illustrates the carrying cost of
asset ownership.

What our data adds to that ledger:

- **Every road metre in §4 is inherited liability at transfer.** The 252 km
  of road inside Heritage Valley + Windermere is new stock added to the
  renewal backlog's denominator — the per-dwelling figure being *lower* than
  the mature grid's bounds the *rate* at which growth adds local-road
  liability per household, but does not make the addition zero, and the
  mature grid's own 13 m/dwelling is the stock whose renewal the $10B
  shortfall already fails to fund.
- **Trunk and arterial infrastructure is not in our road column at all**
  (§6): the deep sanitary trunks, arterial roads, and recreation/fire/transit
  facilities that serve growth sit outside or across hood boundaries. The
  documented cost-recovery facts on that layer, attributed:
  - **Sanitary Sewer Trunk Charge paused 2024-05-13** (2024 rate:
    $1,764/principal dwelling; $1,259/unit new apartments). ~$361M spent on
    deep trunk construction through the SSSF to end-2024; in 2024, $4.9M
    spent vs $17.3M collected. While paused, new trunk servicing draws on
    the general SSSF/ratepayer base rather than fully on growth — a
    measurable cross-subsidy channel until the SSTC resumes.
  - **Off-site levies are structured as targeted instruments, low relative
    to peers** (Desjardins June 2026 development-fee study: Calgary applies
    $9,328/unit single-detached infill water/wastewater charges plus
    per-hectare greenfield fees; Edmonton applies "a suite of targeted
    instruments rather than a comprehensive charge").
- The City-side O&M figures inside the BILD study (~$14M/yr roadways,
  ~$9.7M/yr parks) are **partial**: no lifecycle renewal, no utility side,
  no fire/police/transit/library operating draw. Our fire column gives one
  measured operating-demand line the study omits: 2,804 dispatches/yr in the
  area today (rising with occupancy), even at the lowest per-dwelling rate
  of any era band.

## 6. What this data cannot say (read before quoting either ledger)

1. **Road metres are within-boundary centreline metres.** Arterials on hood
   edges, the Henday, interchange capacity, and everything downstream
   (trunks, plants, stations) serve growth but are not attributed to growth
   hoods here. "New hoods have less road per dwelling" is a statement about
   *local internal* streets only — the layer developers typically build and
   dedicate — not about growth's citywide infrastructure draw.
2. **Levy is not cost.** A flat levy/dwelling across eras says nothing about
   whether the *cost* to serve those dwellings is flat; we measure two
   physical demand proxies (road supply, fire dispatches) and two modeled
   EPCOR charges, not City operating cost. The V2 "modeled city service cost
   per acre" work (SPEC_utilities decision 3, laptop-gated unit costs) is
   the upgrade path.
3. **Modeled utility charges are built-form functions** (§2), not billing
   records; per-dwelling water is ~constant by construction.
4. **Build-out projections vs current roll:** BILD's $309M is a projection;
   our $211M is today's roll under 2025 municipal rates. The two are not the
   same quantity and neither validates the other.
5. **ASP memberships are best-effort** (compiled from ASP neighbourhood
   lists; edmonton.ca unreachable from this box — re-verify against the ASP
   documents in a laptop session before external use). River-valley/ravine
   hoods are excluded as parkland.
6. **Era = median building stock age**, not plat date; heavy-infill mature
   hoods drift later.

## 7. The three IIMP greenfield areas (Decoteau / Horse Hill / Riverview)

Current totals — these areas are almost entirely pre-build-out (their anchor
hoods are set-aside "Future / Rural / Reserve"; flagged inline), so this is
the *starting line* the IIMP's 39-year pro forma runs from, not a
performance read:

| | Decoteau (2) | Horse Hill (3) | Riverview (4) | Combined |
|---|---|---|---|---|
| area (acres) | 3,644 | 6,426 | 5,012 | 15,083 |
| municipal levy /yr | $5.6M | $12.7M | $17.1M | $35.3M ($2,340/ac) |
| dwellings (rec) | 1,203 | 1,014 | 4,650 | 6,867 |
| zoned land not yet developed | 91% | 79% | 63% | — |
| set-aside members | DECOTEAU | RURAL NE HORSE HILL | RIVERVIEW AREA | |

Combined they hold 15,083 acres — 1.6× the Heritage Valley + Windermere
footprint — currently yielding $35.3M/yr municipal levy (~1.3% of the
citywide roll). Whatever trajectory these areas follow, the two ledgers above
are the frame: upfront developer capital and rising levy on one side;
transferred local assets, trunk servicing, and operating demand on the other.
The IIMP's own capital/debt figures for these areas are `ANALYSIS_BACKLOG`
item 6 (primary-source hunt, by hand).

## 8. Open follow-ups

- **By-hand half of item 5:** track SSTC resumption (SSSF Transformation)
  and off-site levy changes; read the BILD study and Capital Investment
  Outlook primary documents before quoting beyond the methods doc's
  citations. Laptop-gated.
- **V2 unit costs** (roadway O&M+renewal $/m/yr; Fire Rescue budget ÷
  citywide dispatches) would convert §3's physical columns into a modeled
  cost ledger — the direct upgrade to §6.2. Laptop-gated (TODO.md, "More
  service layers").
- Re-verify ASP hood memberships (§6.5).

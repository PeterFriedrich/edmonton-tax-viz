# FINDINGS — the roads lens end to end: centrelines → road metres per hood → $/acre panel

**Run:** 2026-09-28, S202, **Opus 5.5**, effort `xhigh`. ⚠️ **Same model family as
the authors** of every change audited (#535, #548, #580 were Opus 5.5), so this is a
different session, not an independent reader.
**Target:** the whole road chain on today's served data, folding in ledger item 13's
roads half (#535 boundary-road equal split, #548 roads-notebook fixes) and the open
`TODO.md` item tying the evidence notebooks' rates to `data/city_unit_costs.json`.
**Re-run note:** the rate and basis levels were audited by S142, S149 (Fable), S172
(Fable) and S187. They are **carried, not re-run** (§0). The delta since them is the
1 m floor (#520), the equal split (#535), the ranked Services panel (#580) and the
rewritten blurbs (S199 audited those).
**Hinge fact, checked first:** the 2026-09-28 scheduled refresh (run 36451039239, started 16:26 UTC,
green, commit `eed5555`) is the **first served file carrying the equal split**; the
09-21 file predates both the floor and the split. Every "served" figure below is
`eed5555`.
**Data:** fresh `9j8t-zm52` roads (62,254,912 bytes) and `65fr-66s6` boundaries
(byte-identical to local `data/raw/`), both fetched 2026-09-28 into the scratchpad,
so the rebuild uses the same feed vintage CI used today.
**Grounding read in full first:** DECISIONS rows 2026-07-01 (metric basis), 2026-09-02
(Services public), 2026-09-09 ×2 (class drift, `unknown`), 2026-09-21 (road floor),
2026-09-22 ×2 (allocation superseded → equal split); ledger rows S142, S149, S172,
S187 ×2; `FINDINGS_sliver_floors.md` §1; the external boundary-road replies in
`/home/opc/research/edmonton-tax-viz/road_cost/`.

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Publish roads supply + cost on the public build | **carried SOUND** (S149). Nothing since reopens it; #580 removed the panel's tax comparison, which narrows the claims. |
| L1 | Collector + local City centreline metres per hood acre as the metric basis | **carried CONDITIONAL** (S149). Not re-run. |
| L2 | Allocation to hoods: overlay, 1 m floor, equal split of boundary road | **CONDITIONAL**: sound between two published hoods; it halves road that fronts only one side. §1 |
| L3 | Is the served length what the pipeline says? (conservation, double count, reproduction) | **PASS** §2 |
| L4 | Rates → cost columns; evidence-notebook rates ↔ config | **PASS served / WARN tie** §3 |
| L5 | Map colour, ranked panel | **PASS**, two INFO notes §4 |
| L6 | Does anything watch the road columns between refreshes? | **WARN**: no, and today 45 hoods moved > 5% with no signal §5 |

## §0 — What was carried and why

S149 settled L0/L1 and the operating-rate unit (lane-km, stated not converted,
DECISIONS 2026-09-08). S172 cross-read the 50-year life (Fable). S187 re-verified
both rate notebooks' transcriptions. I found no new evidence against any of them. So
the audit spent its budget on the length side, which had changed twice in a week and
had never been reproduced end to end from raw.

## §1 — L2: the equal split is right between two developed hoods, and halves road that fronts only one

**What the split does, reproduced on today's feed:**
- 1,349 pieces and 94.2 km are split, 13 of them three-way; 0.8 km on the outer edge stays whole.
- Citywide metric length is **3,655.374 km with and without the split**, identical to the metre.
- 24 published (not set-aside) hoods move by more than 5% and 6 by more than 10%. The decision row said 24 and 7 on the 09-03 feed; the one-hood difference is vintage.
- The biggest movers: GAINER INDUSTRIAL +21.6%, MAPLE RIDGE −21.3%, UNIVERSITY OF ALBERTA FARM +19.0%, CPR IRVINE +15.9%, MORIN INDUSTRIAL +13.2%, WILSON INDUSTRIAL −11.2%.
- No hood crosses from zero.

**Where the split length went (gross km handed across a boundary):**

| from → to | km |
|---|---|
| published → published | 35.5 |
| set-aside → published | 6.9 |
| published → set-aside | 4.5 |
| set-aside → set-aside | 0.1 |
| published → unserved (LEWIS FARMS) | 0.012 |

Set-aside hoods are **net losers (4.5 − 6.9 = −2.4 km)**. The noise had parked edge road in
ravines and rural hoods, and the split handed half of it back. The split is an
improvement over the overlay on every hood I traced.

**The finding.** 22.9 km of edge road lies between a published hood and a set-aside
one, and the equal split gives the set-aside side half of it. The decision's reason
for an equal split is an asset split between **two frontage owners** (Oshawa–Whitby).
It does not cover a road whose other side is a ravine. The research reply the
decision drew on said the opposite for this residual: *"simple centreline/frontage
assignment is uncontroversial"* (`boundary_road_reply2_2026-09-22.md` l.33). That
case was never sized.

**Sized here:** under a variant where a set-aside sharer takes no share,

| Variant | Published hoods moved | > 5% | > 2% | km returned |
|---|---|---|---|---|
| every set-aside neighbour | 60 | 7 | 19 | 11.5 |
| River Valley / Parks neighbours only | 53 | 5 | 15 | 9.0 |

Biggest movers under the variants:
- **every set-aside neighbour:** MARQUIS +14.3%, ARGYLL +9.2%, VIRGINIA PARK +7.8%, CROMDALE +7.3%, CROSSROADS +6.0%.
- **River Valley / Parks only:** ARGYLL, VIRGINIA PARK, CROMDALE, RUNDLE HEIGHTS +5.8%, LANSDOWNE +5.7%.

**Why the variant is narrowed to River Valley.** "Set-aside" is a proxy for "fronts
nothing". It holds for the 23 River Valley / Parks neighbours: residential share is
≤ 2.7% and revenue is ≤ $1.4M/yr on each. It is weak for the Future / Rural ones:
RURAL NORTH EAST HORSE HILL carries $3.5M/yr on 85% parcelled land, and farm parcels
front roads. MARQUIS's +14.3% comes entirely from two Rural NE neighbours, so it is
the least trustworthy number in the table.

**Recommendation: Peter's call, not a fix.**
- **(a)** Record it as a sized limitation (DATA.md roads quirks).
- **(b)** A River Valley / Parks sharer gets no share. This is a one-line filter on `rings` in `split_boundary_pieces`, and needs a test pair differing only in the neighbour's set-aside reason.
- ⚠️ **Plumbing cost of (b):** the set-aside reason is computed in `join_and_calculate`, *downstream* of `load_roads`. (b) needs that reason upstream, or a named list, so it is a small data-contract change.
- A true frontage rule needs parcels and is out of proportion to 9 km.

## §2 — L3: served length reproduces from raw; no double count

- **Reproduction.** `load_roads` on today's feed, divided by `load_boundaries` acres, matches served `road_m_per_acre` on all 406 hoods. The max error is 4.95e-5, which is the 3-dp rounding, and no hood is off by more than 0.001.
- **Conservation.**
  - 5,025.0 km of City road goes in.
  - 5,010.8 km is assigned and 14.2 km (0.28%) lies outside every polygon.
  - The floor drops 751 pieces, 203.5 m, and zeroes exactly KENDAL and WESTVIEW VILLAGE.
  - The split is exact. The published total is 12 m short of the metric total: LEWIS FARMS is unserved, as the decision row states.
- **Double count, which conservation cannot see.**
  - The boundary polygons overlap in two places, 12.9 m² and 11.6 m², and carry **0 m** of metric road.
  - Only **one** geometry lands in two hoods, and it has zero length.
  - So a line lying exactly on a shared edge is not duplicated by `gpd.overlay` on this data.
- **The split's tests fail correctly.**
  - With the split disabled in `load_roads`, the 4 roads tests go red by name: both noise-side parametrizations, conservation and export-v consistency.
  - With a leaking split (`/ (k+1)`), those 4 plus the bike test go red, and `test_boundary_split_conserves_metric_length` reds on its sum assertion.
  - Tree restored by `git checkout` and verified clean; there were no uncommitted edits to lose.
- **WARN (guard-blind, low):**
  - `_prepare_segments`' conservation guard computes `unassigned = before − after` and warns only when that is > 5%. A double count makes `after` larger, so `unassigned` *shrinks*, and the guard can only ever look healthier under it.
  - Today's direct check is clean, and the split's own conservation test covers the split.
  - Remedy: a warning when `after > before`, or the §5 notebook invariant.

## §3 — L4: rates

- **Served cost columns.** `cost_roads_life_per_acre / road_m_per_acre` = 49.99976–50.00024 and `cost_roads_ops_per_acre / road_m_per_acre` = 9.31993–9.32006 across all 406 hoods. That is the configured $50 and $9.32, with only rounding error.
- **Evidence notebooks live.** `recheck_evidence_notebooks.py --only roads_lifecycle_rate roads_operating_rate` gives ✅ 45 and ✅ 22 invariants, so #548's pins hold on today's sources.
- **WARN: the tie is literal to literal, confirmed.**
  - `roads_lifecycle_rate.py:253` checks `SHIPPED == 50.0` and `roads_operating_rate.py:271` checks `SHIPPED == 9.32`. Neither reads `city_unit_costs.json`.
  - A config change (plus its pinning test) leaves both notebooks green while they justify the old number.
  - The notebooks are standalone **by design** (`EVIDENCE_NOTEBOOKS.md`), so don't make them import. Remedy: a `tests/` check that extracts each notebook's `check(SHIPPED == X)` literal and asserts it equals the config value.
  - Both are still unpublished, which caps the exposure.
- **WARN (claim, low):** `city_unit_costs.json` `roadway_renewal.why_the_renewal_half_alone` still says *"beside roadway_ops' $4.635/m/yr"* in the present tense. The rate is $9.32 since 2026-09-06.

## §4 — L5: surfaces

- **Map colour.** `roads.geojson` `v` matches served `road_m_per_acre` on every drawn hood, within 0.055 (1-dp rounding), so the web path carries the split. INFO: HERITAGE VALLEY AREA (15.7 m) and YELLOWHEAD CORRIDOR WEST (33.5 m) have a published value and no drawn road, because every part is under the 20 m display floor. That is cosmetic.
- **Ranked panel.** `svcRank` counts strictly-greater values plus 1, which is standard competition ranking, so ties share a rank. INFO: the "of 406" denominator includes the 48 set-aside hoods the map greys. They all sit at the bottom (none in the top 50), so a published hood's rank moves by 0 at the median and at most 43. It is true as stated and consistent with the function's comment, so no change is proposed.
- The panel note ("about five times … the lane-kilometre denominator widens") matches 50 / 9.32 = 5.4 and the 2026-09-08 decision.

## §5 — L6: nothing watches the road columns between refreshes

- **This week's served diff (09-21 → 09-28):**
  - 315 hoods changed, 131 by > 1%, 45 by > 5% and 19 by > 10%.
  - Decomposed: **42 of the 45 are the split alone**. The others are KENDAL and WESTVIEW VILLAGE, which the floor zeroed, and YELLOWHEAD CORRIDOR WEST (0.12 m/acre, vintage plus split).
  - Every move is explained. **But it was explained here, by hand.**
- **What reads a road column today:**
  - `check_revenue_deltas` reads revenue only.
  - `check_served_columns` checks schema and all-null.
  - `02_methods` asserts `road_km > 0`.
  - A boundary redraw or a feed defect that moved road length would publish silently.
- **Remedy: the open `TODO.md` roads verified notebook**, with these measured invariants:
  - citywide metric km inside a band (3,655.4 today);
  - split conserves exactly;
  - served = rebuild to 1e-3;
  - map `v` = served to 0.06;
  - cost ÷ length = config rate;
  - `road_m_unknown` = 0;
  - outside-boundary share < 1% (0.28% today).
- It can run on CI: `03_assumptions` already calls `load_roads` on the runner and went green today.

## What this run got wrong

1. **I told Peter the split had "probably never reached served data".** That was based on a `gh run list` at 16:23 UTC, three minutes before the scheduled refresh started. The refresh ran at 16:26 and carried it. The claim was a negative drawn from an absence ("no run since 09-21") on a job GitHub runs late; the prior three had started at 13:57–14:50. It was corrected within the session, before any finding rested on it.
2. **My first live run of the two notebooks reported "✅ 0 ❌ 0 ❓ 0 — RAN OK".** That is a vacuous green: the notebooks render through `display(Markdown)`, which my `redirect_stdout` never captured. The real result (45 and 22 held) came from the project's own runner. Had I stopped at the first run, §3 would have cited a check that checked nothing.
3. **§1's variant uses "set-aside" as a proxy for "fronts nothing"**, the proxy-guard class. I measured where the proxy breaks (the Rural NE hoods) and narrowed the recommendation, but I did not test frontage against parcels. MARQUIS's +14.3% should not be quoted as a real understatement.
4. **My first net-flow script got the net wrong twice.** It printed *"into unserved: 0.0 km"* while the gross table beside it showed 12 m going to LEWIS FARMS, and *"net into set-aside −2.1 km"* where the gross table gives 4.538 − 6.916 = **−2.378 km**. Both came from a `reindex`/`fillna` chain that mishandled hoods present on only one side of the subtraction. §1 now uses the gross table's arithmetic. Only the sign was ever load-bearing, and it survives.

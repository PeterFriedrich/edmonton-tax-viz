# Findings — Condo `lot_size` Dedupe Heuristic for the Lot-Acre Denominator

Captured 2026-07-05 while designing the lot-acre denominator variant for the
Glass-view grid spikes (TODO.md PRIORITY item). Sources: local snapshots
`data/raw/Property_Info__Current_Calendar_Year_.csv` (439,685 rows, `lot_size`
in m²) joined to `data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv`
on `Account Number` (100% match), plus `data/raw/neighbourhoods.geojson`
boundary acres. Numbers are from those snapshots and will shift on re-download.
Probe scripts were session-scoped (scratchpad); every number here is
reproducible from the two CSVs with pandas groupbys on `(Latitude, Longitude)`.

Purpose: document the empirical shape of the condo `lot_size` inconsistency and
the validation behind the chosen dedupe rule, so the lot-acre metric's
denominator is auditable rather than asserted. Context: DATA.md §2 (the quirk),
TODO.md (the build item), `src/export_value_grid.py` (the ground-acre metric
this variant complements).

## 1. Why a dedupe rule is needed at all

The true Urban3 metric is dollars per **parcel** acre. The only parcel-area
field in the open data is `dkk9-cj3x` `lot_size` — and each account carries one
lat/long point regardless of lot size, so a per-cell lot-acre denominator means
summing `lot_size` over the accounts at each point. At multi-unit points
(condos, towers, manufactured-home communities) that sum is unsafe: `lot_size`
is sometimes the whole parcel duplicated onto every unit (summing overcounts),
sometimes per-unit apportioned shares (summing is correct), sometimes null/zero
(summing undercounts). No flag distinguishes the regimes.

## 2. Scale of the problem

Grouping all 439,685 accounts by exact `(lat, lon)` gives **287,163 points**;
**3,002 are multi-unit**, holding 155,524 rows (35.4% of accounts) and $31.7B
assessed (13.3% of the roll). Regime breakdown at multi-unit points
(0 treated as null throughout):

| regime | points | rows | assessed value |
|---|---|---|---|
| multi-value, no nulls (apportioned-ish) | 2,457 | 146,471 | $29.3B |
| one distinct value, no nulls (duplicated parcel OR identical shares) | 502 | 1,959 | $0.9B |
| multi-value with some nulls | 16 | 4,109 | $1.1B |
| one value with some nulls | 7 | 286 | $0.1B |
| all null | 20 | 2,699 | $0.2B |

Almost all the money sits in the multi-value regime; the ambiguous one-value
regime is small ($1.0B).

## 3. The rule: sum of DISTINCT positive `lot_size` values per point

Per point: `lot_acres = unique(lot_size > 0).sum() / 4046.86`.

- **Duplicated-parcel regime:** every unit repeats the parcel size → distinct
  collapses to one value → correct.
- **Apportioned regime:** per-unit shares differ → distinct keeps them all →
  correct. Where shares legitimately repeat (identical units), distinct
  undercounts — measured small (§4.3).
- **Null rows** contribute nothing; points with no usable value at all get no
  lot-acre denominator (§5).

## 4. Validation

### 4.1 Physical bound: hood lot acres must fit inside the hood

Deduped lot acres summed per neighbourhood, divided by boundary acres, over the
398 hoods with assessed property: **median 0.65, p95 0.87, and 397 of 398 land
below 1.0** — consistent with private lots covering roughly two-thirds of a
neighbourhood (the rest being roads, parks, easements). The one violation is
PEMBINA (§4.4). Citywide the deduped total is 139,821 lot acres against a
~264,000-acre city footprint (which includes roads, the river valley, and
non-assessed land) — plausible.

### 4.2 The known anchor cases flip correctly

Under $/lot-acre, the top downtown tower (10220 104 Avenue NW: $621M on
1.01 lot acres → $612M/lot-acre) beats West Edmonton Mall ($1,285M on
107.14 lot acres → $12M/lot-acre) by ~50× — the inversion that motivated the
variant, now confirmed by the full top-15 table rather than two hand-checked
cells. Other top-value points land at sane magnitudes: University of Alberta
holdings $26–55M/lot-acre, Kingsway Mall $5.4M, Southgate-area $9.1M.

### 4.3 Collision risk (identical shares collapsing) is negligible

1,917 of 2,473 multi-value points contain at least one repeated value; naive
sum-all vs distinct-sum differs by 2,769 acres citywide (7,123 vs 4,354 at
those points). The direction of truth per point is unknowable without a parcel
fabric, but the one-value points where "identical shares" is the *likely*
reading (lot_max < 100 m² — implausibly small for a multi-unit parcel) number
just **9 points / $0.02B**. The physical-bound test (§4.1) shows distinct-sum
does not systematically overcount; accepting a possible undercount of a few
hundred acres spread over ~1,900 points (~1.4 ac/point) is the documented
trade.

### 4.4 Known outlier: PEMBINA (ratio 1.41 — flag, don't block)

The only hood whose deduped lot acres (198.8) exceed its boundary acres
(141.3). Two contributors: a 619-unit point at 13005 140 Avenue NW claiming
95.9 lot acres (reads like a manufactured-home community where per-pad values
may not be cleanly apportioned), and several 5–16-acre single-account lots
along 137 Avenue whose deeded `lot_size` likely extends past the hood boundary
(the field is city-supplied, not clipped to neighbourhood polygons). One hood
of 398; the validation check should report it, not fail on it.

## 5. Exclusion list: majority-null multi-unit points

Points where most units have null `lot_size` produce *understated* lot acres →
*overstated* $/lot-acre → fake needles, the exact artifact the variant exists
to remove. Measured: **10 points** with >50 units and majority-null lot_size,
$1.07B total (0.45% of roll). Worst case: 10310 102 Street NW (Downtown) —
1,290 units, 1,280 nulls; its 10 surviving values sum to a fake 2.7-acre lot
under a $779M complex ($287M/lot-acre needle, which would be #2 citywide).
Also in the list: 2518 West Port Road NW (Westview Village, 1,059 units all
null — the DATA.md §2 example), the Maple Ridge and Evergreen manufactured-home
points, 14105 West Block Drive NW (Glenora).

Rule: a point is **lot-acre-ineligible** when it has >1 unit and >50% null
`lot_size` (the 52 all-null points, $0.37B / 0.16% of roll, fall out
automatically). Ineligible points are excluded from the lot-acre metric and
their count + value reported at export time — no silent drops.

## 6. Resulting heuristic (for `export_value_grid`'s lot-acre variant)

1. Group accounts by exact `(lat, lon)`; treat `lot_size <= 0` as null.
2. Per point: lot acres = sum of DISTINCT positive `lot_size` values ÷ 4046.86.
3. Points with >1 unit and >50% null `lot_size` are ineligible — excluded from
   the lot-acre metric, count + value REPORTED.
4. Pipeline validation check: per-hood deduped lot acres ÷ boundary acres ≤ 1.0
   for all hoods except a committed known-outlier list (currently PEMBINA);
   report any new violation loudly (it means the dedupe broke or the data
   regime changed).
5. Validate the exported lot-acre grid against the ground-acre version before
   offering it in the UI (TODO.md).

## Open questions

- Display: does lot-acre replace ground-acre as the Glass grid's height metric,
  or ship as a toggle beside it? (Undecided as of 2026-07-05.)
- The PEMBINA mechanism (boundary-straddling `lot_size`) presumably also
  shaves accuracy in hoods that stayed under 1.0 — invisible to the bound test.
  A parcel-fabric cross-check is not possible with open data (AltaLIS transfer,
  DATA.md §2); accepted.
- Manufactured-home communities appear on both sides (PEMBINA overcounts,
  Maple Ridge/Evergreen are null). If they ever matter analytically, they may
  deserve their own regime.

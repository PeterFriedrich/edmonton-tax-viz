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

## 3. The rule: repeat-aware dedupe (REVISED 2026-07-05, same day)

> The first draft of this doc proposed a plain sum-of-DISTINCT-values per
> point. Cell-level validation (§4.3) showed that rule fails at
> identically-apportioned townhouse complexes — it collapses hundreds of
> legitimate identical shares to one, manufacturing $1B+/lot-acre needles
> worse than the WEM artifact it exists to fix. The shipped rule:

Per point, group the positive `lot_size` values; a value repeated k times
contributes:

- **k × value** when the value is share-sized (`< SHARE_MAX_M2 = 1000 m²`) —
  identical apportioned shares are real land per unit (the townhouse regime);
- **value once** when parcel-sized (`>= 1000 m²`) — a large value repeated
  across units reads as the parcel duplicated (the duplication guard).

`lot_acres = Σ contributions / 4046.86`. Null rows contribute nothing; points
with no usable value at all get no lot-acre denominator (§5). Implemented as
`_point_lot_stats` in `src/export_value_grid.py`.

## 4. Validation

### 4.1 Physical bound: hood lot acres must fit inside the hood

Deduped lot acres summed per neighbourhood, divided by boundary acres:
**median 0.69, p95 0.87, and 405 of 406 land below 1.0** (repeat-aware rule;
the plain distinct-sum draft gave median 0.65 — the bound test does NOT
discriminate between rule variants, §4.3 does) — consistent with private lots
covering roughly two-thirds of a neighbourhood (the rest being roads, parks,
easements). The one violation is PEMBINA (§4.4). Citywide totals (~140k lot
acres against a ~264,000-acre city footprint including roads, the river
valley, and non-assessed land) are plausible under every candidate rule.
Enforced in the pipeline as `check_lot_acre_bounds` (raises on any new
violation; PEMBINA committed in `KNOWN_BOUND_OUTLIERS`).

### 4.2 The known anchor cases flip correctly

Under $/lot-acre, the top downtown tower (10220 104 Avenue NW: $621M on
1.01 lot acres → $612M/lot-acre) beats West Edmonton Mall ($1,285M on
107.14 lot acres → $12M/lot-acre) by ~50× — the inversion that motivated the
variant, now confirmed by the full top-15 table rather than two hand-checked
cells. Other top-value points land at sane magnitudes: University of Alberta
holdings $26–55M/lot-acre, Kingsway Mall $5.4M, Southgate-area $9.1M.

### 4.3 The townhouse failure that forced the revision (found 2026-07-05, same day)

The first-draft assessment ("identical shares collapsing is negligible —
2,769 acres citywide, 9 suspect one-value points / $0.02B") was correct in
*acres* and wrong in the *display metric*. Spot-checking the exported grid's
top $/lot-acre cells found townhouse complexes where hundreds of units carry
identical apportioned shares — KAMEYOSEK (309 accounts, $42M, shares of
33.643 m² collapsing to a deduped 0.04 acres), SOUTH TERWILLEGAR (171
accounts at 149.547 m²), CALLINGWOOD SOUTH (71 accounts at ~105–114 m²).
Distinct-sum gave them up to **$1.2B value/lot-acre** — fake needles 2× worse
than the WEM artifact the metric exists to remove. Lesson recorded: a
citywide-aggregate error bound says nothing about a per-cell display metric;
validate at the display grain.

Rule-variant comparison (per-hood bound + worst townhouse-hood cell +
citywide top-3):

| rule | hood bound | townhouse max | citywide top 3 |
|---|---|---|---|
| distinct-sum | median 0.65, 1 hood > 1 | $1,209M/lot-ac | CALLINGWOOD S., KAMEYOSEK, DOWNTOWN |
| repeat-aware (T=500) | median 0.69, 1 hood > 1 | $37.7M | DOWNTOWN $612M / $149M / $143M |
| repeat-aware (T=1000) | identical | identical | identical |
| repeat-aware (T=2000) | identical | identical | identical |
| never dedupe | identical | identical | identical |

Two conclusions: (1) the repeat-aware rule is **insensitive to the threshold**
from 500–2000 m² — 1000 m² is committed as `SHARE_MAX_M2`; (2) "never dedupe"
behaves identically today, i.e. parcel-sized values duplicated across many
units barely exist in the current data — the ≥1000 m² dedupe is kept as a
cheap guard in case that regime appears in a future refresh. Residual known
bias: apportioned shares exclude common property, so complex-heavy cells
overstate $/lot-acre somewhat (a 309-townhouse complex on ~2.5 deduped acres
is denser than physically likely). Not correctable from open data; the
ground-acre metric remains available for comparison.

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
`lot_size`, or no usable `lot_size` at all. As built, that's **56 points /
4,307 rows / $1.23B (0.52% of roll)**, excluded from the lot-acre numerator
AND denominator and reported at export time — no silent drops. (Their dollars
stay in the ground-acre metric.)

## 6. Shipped heuristic (`src/export_value_grid.py`, built 2026-07-05)

1. Group accounts by exact `(lat, lon)`; treat `lot_size <= 0` as null.
2. Per point: repeat-aware dedupe (§3) — repeated values < `SHARE_MAX_M2`
   (1000 m²) count per unit, repeated values ≥ it count once.
3. Points with >1 unit and >50% null `lot_size`, or no usable `lot_size`, are
   ineligible — excluded from the lot-acre numerator AND denominator, count +
   value REPORTED (§5).
4. Pipeline validation check (`check_lot_acre_bounds`, wired in `main.py`):
   per-hood deduped lot acres ÷ boundary acres ≤ 1.0 for all hoods except
   `KNOWN_BOUND_OUTLIERS` (currently PEMBINA); RAISES on any new violation
   (it means the dedupe broke or the data regime changed).
5. Exported-grid validation vs ground-acre (run 2026-07-05): 34,675 cells, 28
   (0.1%) without a lot-acre value; revenue/lot-acre median $28.0k, p97.5
   $105k vs ground-acre median $18.0k, p97.5 $144k; top-10 lot-acre cells are
   all Downtown CBD; WEM $12.6M ground → $290k lot; 79% of cells read higher
   under lot-acre (lots exclude streets), consistent with the denominators'
   meanings.

## Open questions

- ~~Display: replace ground-acre or toggle?~~ **DECIDED (Peter, 2026-07-05):
  toggle — both denominators viewable in the Glass view.**
- The PEMBINA mechanism (boundary-straddling `lot_size`) presumably also
  shaves accuracy in hoods that stayed under 1.0 — invisible to the bound test.
  A parcel-fabric cross-check is not possible with open data (AltaLIS transfer,
  DATA.md §2); accepted.
- Manufactured-home communities appear on both sides (PEMBINA overcounts,
  Maple Ridge/Evergreen are null). If they ever matter analytically, they may
  deserve their own regime.

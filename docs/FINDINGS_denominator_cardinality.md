# Findings — record-to-parcel cardinality & the ground-acre vs lot-acre denominator

_Investigated 2026-07-08 (pre-launch lens audit). Reproduce:
`.venv/bin/python tools/audit_cardinality_denominators.py` (real roll in
`data/raw/`, gitignored). Value-based — mill rates only rescale within class, so
the denominator conclusions hold for `revenue_per_acre` too. Sibling of
`FINDINGS_lot_dedupe.md` (the grid/Glass-view lot-acre work this reuses)._

## Question

The launch audit asked whether the two known record-to-parcel cardinality
distortions — **WEM** (many records → one parcel, numerator-inflating) and
**condos** (shared lot area duplicated across unit records, denominator-inflating)
— corrupt the **first (neighbourhood) lens**, and whether a parcel/lot-acre
denominator should be offered there. Answered with the real roll.

## Verdict

1. **The neighbourhood lens is immune to both bugs — structurally and
   empirically.** It is NOT distorted; no fix is needed for the first lens.
2. **The condo denominator bug is tiny even where it could bite** (0.1% citywide;
   worst hood +12%) — the "condos duplicate the full lot" premise is largely false
   in this dataset (lot_size is mostly null/apportioned at condo points, not
   duplicated), and the shipped `SHARE_MAX_M2` dedupe already neutralises it.
3. **A lot-acre neighbourhood lens is a legitimate editorial choice, not a bug
   fix.** It systematically boosts park/river-valley hoods (median ×2.47 for the
   51 hoods that are <55% parcel land) — the Urban3-analogous "productivity of the
   developable land" framing — and needs a low-parcel-fraction guard.

## How the first lens is built (why it's immune)

`join_and_calculate.py`: `value_per_acre = total_assessed_value / area_acres`,
`revenue_per_acre = total_revenue / area_acres`.
- **Numerator** = `groupby(neighbourhood).sum()` of every assessment account's
  value/levy (`aggregate_by_neighbourhood.py`). One row = one legally-titled,
  separately-levied account. It **never joins to parcel geometry.**
- **Denominator** = `area_acres`, the boundary polygon area
  (`load_boundaries.py`, `geometry.area / SQ_M_PER_ACRE`). It **never reads
  `lot_size` or unit records.**

The two cardinality bugs only distort *per-parcel / per-point* metrics (the grid),
where value and area are matched at parcel granularity. The neighbourhood lens
matches a roll-summed numerator to a geometry-derived denominator — two different
bases — so parcel-level cardinality cannot enter their ratio.

## Q1 — WEM numerator (the premise is inverted)

- **439,635 accounts → 287,123 distinct points.** Only **1.0%** of points carry
  >1 account (2,996 points).
- **WEM is a *single* $1,285.1M account on one point** (Summerlea) — not "multiple
  records on one parcel." It is a **grid needle** (one value ÷ one 100 m cell,
  `FINDINGS_lot_dedupe.md`), not a neighbourhood-numerator problem. At the hood
  level it is simply Summerlea's largest single account, summed once.
- The genuinely multi-account points are **condo/townhouse stacks**: Downtown
  1,290 accts ($779M tower), South Terwillegar 1,152, Westview Village 1,059.
- **119,306 rows share an identical (point, value) with another row =
  $16.6B = 6.98% of the $237.5B roll.** These are *legitimately distinct titled
  units* (identical condo units), each separately levied — summing them is the
  correct neighbourhood tax base, NOT double-counting.

**→ No cardinality double-count reaches the neighbourhood numerator.**

## Q2 — condo denominator inflation (small, localized, already handled)

If one *naively* summed `lot_size` per hood as a denominator:

- **Citywide raw vs deduped lot-acres: 142,237 vs 142,161 — 0.1% overcount.**
- Worst hoods: River Valley Walterdale **+12%**, Poundmaker Industrial +9%,
  Callingwood South +6%, Callaghan +3%, Hazeldean +2%; everything else ≤1%.

`lot_size` at condo points is mostly null/apportioned, not duplicated-full (see
`DATA.md §2`). The `SHARE_MAX_M2 = 1000 m²` repeat-aware dedupe closes even the
small residual. The condo denominator bug is real but minor — and only matters at
all if you *build* a lot-acre denominator (below); it never touches ground-acre.

## Q5 — ground-acre vs lot-acre: what ground includes that lot excludes

- **Parcel land = 74% of citywide ground area** (deduped parcel 142,161 ac vs
  boundary 193,263 ac). Ground-acre includes ~26% non-parcel land — roads, alleys,
  parks, ROW, river valley.
- Per-hood parcel/ground fraction: **median 69%, IQR 63–76%, range 0–147%.**
  (147% = Pembina, `lot_size` summing past the polygon — a known lot-data
  artifact, already in the grid's `KNOWN_BOUND_OUTLIERS`.)

Ground-acre answers "value per acre of neighbourhood"; lot-acre answers "value per
acre of *developable parcel*". Neither is more correct — they answer different
questions. **Ground-acre is NOT Urban3 lineage** (audit Q6): Urban3 divides total
parcel value by total *parcel* area, i.e. their denominator is closer to lot-acre.
Ground-acre is this project's own addition, justified on cardinality-robustness
(it can't be corrupted by the record-to-parcel bugs), not Urban3 continuity.

## The decision: does a lot-acre neighbourhood lens change the story?

**Yes, systematically.** Spearman rank corr ground↔lot = **0.959**, but
**134/406 hoods move >20 ranks and 35 move >50** — and the movement is patterned:

| Direction | Hood | $/ground-ac | $/lot-ac | boost | parcel % |
|---|---|---|---|---|---|
| Rise | Rossdale | $1.33M | $3.73M | **×2.8** | 34% |
| Rise | Virginia Park | $1.45M | $3.64M | ×2.5 | 40% |
| Rise | Riverdale | $1.84M | $4.49M | ×2.4 | 41% |
| Rise | Westwood | $1.73M | $3.66M | ×2.1 | 47% |
| Rise | McCauley | $1.87M | $3.68M | ×2.0 | 51% |
| Fall | Pembina | $2.54M | $1.73M | ×0.7 | 147% |
| Fall | Mill Woods Town Centre | $2.22M | $2.69M | ×1.2 | 75% |

- **51 hoods are <55% parcel land (park/ROW/river-valley-heavy); their median
  $/acre boost under lot-acre is ×2.47, vs ×1.41 for the rest.** Ground-acre
  quietly penalises them for green space they can't build on; lot-acre credits
  only their developable land. This is the substantive reason to offer the lens.

**Gotcha — near-zero-parcel hoods explode.** Mill Woods Golf Course (0% parcel)
goes $0k → $1,204k/ac, a ×6,960 artifact of dividing by a sliver. A neighbourhood
lot-acre lens **needs a low-parcel-fraction guard** (floor the denominator or
suppress hoods below ~15% parcel to an "n/a" grey, same spirit as set-aside), plus
the existing `KNOWN_BOUND_OUTLIERS` handling for the >100% (Pembina) tail.

## Worked case study — University of Alberta (exempt-institutional hood)

The rise examples above are all park/river-valley hoods. **U of A is a distinct
category the toggle also serves: an exempt-institutional hood**, where the lift
comes not from parks but from tax-exempt campus/hospital land that is *absent from
the roll entirely* (verified — the exempt health-sciences addresses 11220 & 11350
83 Ave return 0 rows; consistent with `data/DATA.md` 2026-06-29: exempt
institutional land is excluded from the taxable roll, not flagged/zeroed).

| Metric | Value |
|---|---|
| Taxable accounts | 47 ($2.242B assessed; 88% non-res / 12% *Other* Residential; top-5 = 76%) |
| Boundary polygon | 295.2 acres |
| Taxable lot footprint (deduped, 45 eligible pts) | 147.5 acres = **50.0% parcel** |
| $/ground-acre (polygon denom) | $7.60M |
| $/lot-acre (taxable-footprint denom) | $15.20M (**×2.0**) |

Two points this case pins down:

- **Guard-PASS test.** At 50% parcel it sits well above the ~15% guard and renders
  cleanly — the complement to the Mill Woods Golf Course 0% *fail* case above. Good
  regression fixture for the guard when the toggle is built.
- **The toggle is honest here but not complete.** Lot-acre correctly counts only
  tax-paying land (exempt parcels are off-roll, so they leave the denominator
  automatically) → the ×2.0 is a *true* intensity, not an artifact. But it still
  cannot show the deeper U-of-A story: the exempt half of the polygon consumes
  roads/fire/transit and yields zero municipal revenue. That free-riding is a
  **cost/services-lens** question (see `docs/SPEC_services.md`), not something
  either revenue denominator surfaces.

## Recommendation

- **Do NOT** "fix" the first lens — there is nothing to fix; it is robust by
  construction.
- **Build a lot-acre denominator as a TOGGLE on the neighbourhood lens** (mirroring
  the Glass view's "Ground acres | Lot acres"), because it reshuffles 35 hoods by
  >50 ranks in an interpretable, park-crediting way. Frame it honestly as "value
  per developable parcel acre (Urban3-analogous)", ground-acre as the
  cardinality-robust default. Reuses `load_property_info` + `SHARE_MAX_M2` dedupe;
  adds a hood-level parcel-fraction guard.
- **Methodology-note language** (audit Q6/Q7): correct any "ground-acre =
  Urban3-standard/gross-area" claim; document condo handling as an industry-wide
  open problem (independent Urban3 replications *excluded* condos entirely — this
  project's dedupe is an improvement over exclusion).

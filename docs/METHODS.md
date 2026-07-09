# Methods

How the numbers on [the map](https://peterfriedrich.github.io/edmonton-tax-viz/)
are made — in one place, written for a reader checking the work rather than
building it. Every figure here is reproducible from open data with the code in
this repository; deeper detail lives in the linked `FINDINGS_*` documents, each
of which names the script that regenerates its numbers.

## 1. The core metric: municipal revenue (or assessed value) per acre

**Numerator.** Each of Edmonton's ~440,000 assessment accounts (open dataset
`q7d6-ambg`) carries an assessed value and up to three tax classes with
percentage apportionment. Per account:

```
levy = Σ over classes  assessed_value × (class % / 100) × (mill rate / 1000)
```

using the City's published municipal mill rates (`pwis-wc4c`; 2025: Residential
7.6254, Other Residential 8.3116, Non Residential 24.2229 per $1,000).
**Municipal levy only** — the provincial education levy is excluded because the
project measures City fiscal capacity, not household tax burden. Citywide 2025
municipal levy computed this way ≈ $2.67B. Accounts sum by neighbourhood; the
map's toggle shows either this revenue or raw assessed value (the
[Urban3](https://www.urbanthree.com/)/Strong Towns convention). The gap between
the two views is exactly Edmonton's class-differential mill rates — non-res
land taxed ≈ 3.2× residential per dollar of value. (`docs/SPEC_revenue.md`)

**Denominator — two, on purpose.** A toggle offers:

- **Ground acres** (default): the neighbourhood boundary polygon's area
  (`65fr-66s6`), which includes roads, parks, and rights-of-way (~26% of the
  city's land). Chosen as the default because it is *structurally immune* to
  parcel-record inconsistencies — it never reads a lot-size field.
- **Lot acres**: the deduplicated area of titled lots (`dkk9-cj3x`
  `lot_size`) — the denominator closest to Urban3's own method, a "revenue per
  acre of private land" view. Neighbourhoods where titled lots cover under 15%
  of the boundary are greyed out rather than shown (a near-zero denominator
  would explode the ratio; e.g. a golf-course neighbourhood at ×6,960).

Lineage note: Urban3's published method divides by *parcel* acres, so the
lot-acre mode is the comparable one; the ground-acre default is this project's
own robustness-motivated addition, not borrowed methodology.
(`docs/FINDINGS_denominator_cardinality.md`)

## 2. The two hard cases, worked openly

Anyone spot-checking this map will land on the same two places we audited
first, so here is what the data actually does there.

**West Edmonton Mall.** WEM is a *single* $1.285B assessment account pinned to
one coordinate. At the neighbourhood level it is simply Summerlea's largest
account, summed once — no distortion. On the 100 m grid (Glass view) one point
÷ one cell makes it the city's tallest needle under ground acres
($12.6M levy/acre); switch the denominator to lot acres and its 107-acre lot
brings it to ~$290k/acre — while the top downtown tower ($621M on ~1 lot acre)
correctly beats it ~50×. The toggle exists exactly so both readings are
visible: dollars-per-map-cell and dollars-per-acre-of-land.

**Condominiums.** Many taxable units share one lot, and the open data's
`lot_size` field encodes that inconsistently — sometimes the whole parcel
duplicated onto every unit, sometimes real per-unit shares, sometimes null.
This is an industry-wide problem; independent Urban3-style replications have
typically *excluded* condos entirely, deleting dense high-value land from
their maps. We instead apply a repeat-aware rule (`SHARE_MAX_M2`): repeated
values under 1,000 m² count per unit (genuine apportioned shares — the
townhouse regime), repeated values at or above it count once (parcel
duplicated). The rule is insensitive to that threshold from 500–2,000 m².
Points that are majority-null (56 points, $1.23B, 0.52% of the roll) are
excluded from the lot-acre view *and reported* — never silently dropped; their
dollars remain in the ground-acre view. A pipeline check asserts each
neighbourhood's deduped lot acres fit inside its boundary (one known
exception, Pembina, is documented). (`docs/FINDINGS_lot_dedupe.md`)

The neighbourhood-level metric is structurally immune to both cases: its
numerator never joins parcel geometry and its denominator never reads
`lot_size`. Verified empirically as well as structurally.
(`docs/FINDINGS_denominator_cardinality.md`)

## 3. Grey neighbourhoods: the set-aside layer

48 of 406 neighbourhoods render neutral grey, not low-red. These are places
where ≥ 90% of the land is zoned river valley / natural area / parks
("never-taxable") or future-development / agricultural reserve ("not yet") —
determined by overlaying the Zoning Bylaw geometry (`fixa-tstc`) on the
boundaries. Painting them as "low revenue" would be true arithmetic but a
false story; greying them says *this land is not on the taxable roll by
design*. The rule keys off zoning, so as fringe land is rezoned and develops
it automatically rejoins the colour scale on a later refresh.
(`docs/FINDINGS_revenue_scale.md`)

**Standing caveat:** tax-exempt institutions (universities, hospitals, crown
land) are *absent from the assessment roll*, not listed at zero — so
revenue/acre genuinely understates neighbourhoods holding them, and no flag in
the roll can mark it. We measure the effect instead: institutional-proxy
zoning carrying no taxable account, per neighbourhood
(`docs/FINDINGS_exempt_institutional.md` — 20 neighbourhoods ≥ 10% untaxed
institutional land; the University of Alberta area is the worked example).

## 4. The Glass view (100 m grid)

Sub-neighbourhood detail: each account's dollars binned into 100 m cells
(~35,000), prism height = dollars in cell ÷ cell acres, with the same
ground/lot-acre toggle as above. Pure point binning — no interpolation, no
spreading — so a cell shows exactly the accounts pinned inside it.

## 5. The cost side (Services view)

Revenue alone is half the fiscal story. Each service layer is a *supply* or
*modeled cost* per acre; none of them alters the revenue numbers.

- **Roads** — metres of city-maintained **collector + local** road centreline
  per acre (`9j8t-zm52`; 3,644 km in-metric). Arterials are computed but
  excluded: they are shared city-wide infrastructure that happens to run along
  neighbourhood edges, and alleys and provincial highways are out. This is the
  strongest cost lens methodologically — road length is the dominant driver of
  recurring surface-infrastructure cost, and it is measured, not modeled. The
  **Ratio view** divides: revenue per road-metre. (`docs/SPEC_services.md`)
- **Stormwater (modeled)** — EPCOR's own bylaw formula, area × intensity ×
  runoff coefficient, applied to every roll parcel at 2025 rates. Citywide
  $240.4M as modeled — deliberately reported alongside $190.5M when land
  EPCOR does not yet bill (future/rural/river-valley zones) is excluded.
  Validation against EPCOR's published figures: the residential slice lands
  within ~11% of billed reality; the citywide excess is localized and
  explained. (`docs/SPEC_utilities.md`, `docs/FINDINGS_utility_validation.md`)
- **Fire rescue (demand)** — emergency response events per acre per year,
  averaged over 2023–2025 (~88,000 events/yr, `7hsn-idqi`), with the 31
  station locations plotted. This is *service demand*, not response-time
  performance; medical calls are ~60% of events (a documented caveat, not a
  filter). Operational noise (alarm tests, moves) is excluded.
- **Water + sanitary (modeled)** — a per-connection model (meter-size fixed
  charges + block volumetric rates at April-2026 tariffs) over 268,489
  connections / ~552,000 modeled households; $588.1M/yr, ≈ 1.26× EPCOR's
  published residential + multi-res revenue, with the gap characterized
  component-by-component. (`docs/FINDINGS_utility_validation.md`)
- **Electricity/gas franchise fees** — modeled as data columns but *not*
  mapped: a flat per-dwelling proxy makes every map of them just a dwelling-
  density map. Included here for honesty about what was tried and why it
  isn't shown.

Every modeled dollar figure is labeled **modeled, not billed** in the app, and
each model is validated against published EPCOR / audited City figures to
order-of-magnitude or better before shipping.

## 6. Display honesty rules

- **Prism height is always linear.** No transform ever exaggerates height.
- Colour ramps may use sqrt (or log where noted) to spread a skewed
  distribution across the palette — and the app has a toggle to turn that
  off and see true-magnitude colour. Colour clamps sit near the 97.5th
  percentile; every transform choice is recorded with its skew test in
  `docs/FINDINGS_revenue_scale.md` §6.
- No silent data drops anywhere in the pipeline: unmatched, excluded, or
  suppressed records are counted and logged, and validation checks fail the
  build rather than degrade it.

## 7. Data sources

All open data, no GIS desktop software, Python only.

| Input | Edmonton Open Data ID | Notes |
|---|---|---|
| Property assessments | `q7d6-ambg` | ~440k accounts, live weekly feed, 2025 roll |
| Property information (lot sizes) | `dkk9-cj3x` | joins to assessments by account |
| Neighbourhood boundaries | `65fr-66s6` | 406 neighbourhoods |
| Tax rates | `pwis-wc4c` | municipal mill rates by class, 2014→ |
| Zoning Bylaw geometry | `fixa-tstc` | land-use categories, set-aside layer |
| Road network | `9j8t-zm52` | ~54k centreline segments |
| Fire response events / stations | `7hsn-idqi` / `b4y7-zhnz` | 2023–2025 |
| Utility tariffs | EPCOR bylaw schedules | year-pinned JSON in `data/` |

A weekly GitHub Action re-downloads everything, re-runs the full pipeline,
and redeploys — with guards that hold the last good data (and show a banner)
if the assessment year rolls over or a download is truncated.
(`docs/SPEC_deployment.md`)

## 8. Known limitations

1. **Exempt institutional land is invisible to the roll** (§3 caveat) — the
   biggest structural understatement, measured but not correctable.
2. **One coordinate per account** — a large property's dollars pin to a single
   point on the grid; the lot-acre denominator is the honest counterweight.
3. **Lot sizes are city-supplied, not clipped to neighbourhood boundaries** —
   one known bound violation (Pembina), reported not hidden.
4. **Utility figures are models** with stated assumptions (runoff intensity
   = 1.0, consumption proxies, occupancy) and published validation ratios;
   they are order-of-magnitude tools, not bills.
5. **Neighbourhood aggregation** smooths within-neighbourhood variation; the
   100 m grid view is the partial remedy, parcel-level analysis the future
   one (`docs/PARCEL_LEVEL_OPPORTUNITIES.md`).

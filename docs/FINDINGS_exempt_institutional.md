# Findings — Exempt-institutional hoods: where tax-exempt land dilutes the lens hardest

**Date:** 2026-07-09 (`ANALYSIS_BACKLOG.md` item 7, generalized out of the
University of Alberta hand-case in `FINDINGS_denominator_cardinality.md`).
Reproducible via `tools/audit_exempt_institutional.py` (repo root; reads the
served `web/data/neighbourhood_value_per_acre.geojson` for the canonical
published fields + `data/raw/` roll and zoning for the exempt-acre measure).
Value-based — the exemptions distort the value roll and the levy roll identically.

## The question

Some institutional land is on the taxable roll and some is not, so revenue/acre
and value/acre understate any neighbourhood holding a big exempt institution:
the numerator sees only the taxable slice, the denominator (polygon acres) sees
the whole thing. U of A was the worked example — $2.242B taxable on ~half its
polygon, the other half untaxed campus land. **Which other hoods have this
shape, and how do we tell genuine exempt-dilution apart from the things it looks
like** (low-value taxable land; park/river-valley)?

⚠️ **PREMISE CORRECTED 2026-08-07 — THE NUMBERS BELOW ARE UNAFFECTED; RE-RUN AND
CONFIRMED.** This section used to open with *"is **absent from the taxable roll
entirely** — not flagged, not zeroed, simply never appears (`data/DATA.md`,
2026-06-29)"*. That is **false as a blanket claim**: every major hospital is on
the roll (Royal Alexandra $273.8M, Misericordia $247.8M, Grey Nuns $196.9M) and
so is the U of A campus, while the Alberta Legislature genuinely is not. In
total **2,254 parcels on UI/UF/AJ/PU zoning carry $5.6B of assessed value** — see
`data/DATA.md` "Tax-exempt flag".

**The findings survive because the method never used that premise.** §"Method"
*measures* the taxable footprint sitting on institutional zoning and subtracts
it, rather than assuming institutional land is absent — so land that IS taxed is
counted as taxed and correctly excluded from `exempt_inst_acres`. Re-run
2026-08-07 against the same inputs reproduces every published figure exactly
(U of A: 145 exempt acres of 253 institutional, ×2.0 lift, $15.2M/lot-acre,
$2.242B taxable on 47 accounts). **Only the motivating sentence was wrong.**

## Method — measure exempt land, don't guess it

No exempt boolean exists, so exempt-institutional land is **measured** as
institutional-proxy zoning that carries no taxable account:

1. **Institutional zoning acres by code.** Overlay the four institutional-proxy
   base zone codes (`data/DATA.md` line ~308) on the neighbourhood boundaries,
   kept split by code because the code *is* the mechanism:
   - `UI` — Urban Institution (university / school / hospital)
   - `AJ` — Alternative Jurisdiction (federal / provincial crown land)
   - `PU` — Public Utility (treatment plants, pipeline/utility ROW, stormwater)
   - `UF` — Urban Facilities (civic — arenas, rec/expo grounds)
2. **Taxable footprint sitting on it.** Spatial-join the deduped taxable lot
   footprint (the shipped `SHARE_MAX_M2` dedupe, `_point_lot_stats`) onto those
   polygons — how much of the institutional land actually carries a taxed account.
3. **exempt_inst_acres = institutional acres − taxable footprint on them**
   (floored at 0); `exempt_inst_frac` = that ÷ polygon acres. Rank by frac
   ("bites hardest" is fractional — how much it distorts the per-acre number).

This measurement is what separates the three look-alikes the audit had to keep
apart: exempt-dilution has **large institutional zoning, almost none taxed**;
low-value institutional land is **taxed** (small exempt_inst); park/river-valley
off-roll land **isn't institutional at all** (near-zero institutional acres).

## Verdict up front

1. **U of A is not alone, but it is the extreme high-value case.** 20 non-set-aside
   hoods carry institutional-zoned land that is ≥10 % of their polygon *and*
   untaxed. Only a handful pair that with high taxable value density — U of A is
   the standout ($15.2M/lot-acre, ×2.0 lift).
2. **The exempt footprint is mostly NOT "university/hospital" zoning.** Citywide
   the institutional-proxy land is **PU 4,774 ac + AJ 1,870 ac + UF 1,819 ac**,
   with **UI only 205 ac**. The big exempt dilutions come from **provincial/federal
   crown land (AJ)** and **utility land (PU)**, not the classic `UI` institution
   code. U of A's campus is 100 % `AJ` (provincial), not `UI`.
3. **The lot-acre toggle gives these hoods an honest lift; the services lens is
   where the exempt half actually shows up.** Lot-acre correctly counts only the
   taxable land, so the ×-lift is a *true* intensity — but the exempt acres still
   consume roads/fire/transit at zero municipal revenue, which only the cost side
   (`docs/SPEC_services.md`) can surface. Same conclusion as the U of A case,
   now generalized.

## Ranked list — exempt-institutional hoods (≥10 % of polygon, untaxed)

`boost` = value-per-lot-acre ÷ value-per-acre (the lot-acre toggle's lift).

| Hood | exempt % | exempt ac | inst ac | parcel % | boost | $/lot-ac | code | mechanism |
|---|--:|--:|--:|--:|--:|--:|:--:|---|
| Poundmaker Industrial | 65 % | 106 | 113 | 29 % | ×3.5 | $1.5M | PU | utility / infrastructure |
| **University of Alberta** | 49 % | 145 | 253 | 50 % | ×2.0 | **$15.2M** | AJ | provincial crown |
| Edmonton Northlands | 43 % | 79 | 160 | 51 % | ×2.0 | $2.2M | UF | civic (expo/Coliseum) |
| McArthur Industrial | 24 % | 34 | 50 | 69 % | ×1.4 | $1.2M | AJ | provincial/federal |
| Westwood | 21 % | 50 | 55 | 47 % | ×2.1 | $3.7M | UF | civic |
| Yellowhead Corridor West | 20 % | 58 | 276 | 87 % | ×1.2 | $0.3M | AJ | provincial/federal |
| CPR Irvine | 20 % | 32 | 66 | 74 % | ×1.4 | $1.2M | AJ | provincial/federal |
| Woodcroft | 18 % | 58 | 97 | 59 % | ×1.7 | $2.7M | UF | civic |
| West Meadowlark Park | 17 % | 48 | 56 | 54 % | ×1.9 | $3.0M | UF | civic |
| Kennedale Industrial | 17 % | 56 | 80 | 49 % | ×2.1 | $1.5M | PU | utility |
| McCauley | 17 % | 62 | 76 | 51 % | ×2.0 | $3.7M | UF | civic + inner-city missions |
| Ambleside | 17 % | 129 | 166 | 65 % | ×1.5 | $3.8M | PU | utility (stormwater/ROW) |
| University of Alberta Farm | 13 % | 99 | 726 | 85 % | ×1.2 | $0.3M | AJ | mostly **taxed** farmland |
| Blatchford Area | 11 % | 80 | 195 | 30 % | ×3.3 | $2.3M | UI | redevelopment (in flux) |

(Full 20 in the tool output; the tail is more PU/utility hoods — Rossdale,
Strathcona Junction, Davies, South Edmonton Common.)

## Typology — three mechanisms, kept separate

- **Genuine exempt-dilution (the U-of-A pattern).** Large institutional zoning,
  little of it taxed, real value on the taxable slice → honest lot-acre lift, big
  services-lens gap. **University of Alberta** ($15.2M/lot-ac, 145 exempt ac, all
  provincial `AJ`) is the archetype and by far the highest-value. **Edmonton
  Northlands** (79 exempt ac of city civic `UF` — the Coliseum/expo grounds) is
  the clean second: a large city-owned exempt block inside an otherwise-taxable
  hood. Westwood, McCauley, West Meadowlark, Woodcroft are lower-value versions
  (civic `UF` land — schools, rec centres — plus, for McCauley, the inner-city
  mission/social-agency belt).
- **Utility/infrastructure corridors (`PU`).** The largest exempt bucket citywide.
  **Poundmaker Industrial** tops the whole ranking (106 exempt ac, 65 % of the
  polygon) but it is EPCOR/utility land at low taxable value ($1.5M/lot-ac), not a
  civic institution — a *different* dilution than U of A. `PU` also sweeps in
  stormwater ponds and pipeline ROW (Ambleside, Kennedale), which behave more like
  set-aside than "institution." Read `PU`-dominant hoods as utility land, not
  campuses.
- **Low-value institutional land that is ON the roll (not exempt).** **U of A Farm**
  is the trap the audit had to avoid: 726 ac of `AJ` zoning but 85 % on the taxable
  roll (as cheap farmland) → only 99 exempt ac and ×1.2 lift. **Yellowhead
  Corridor West** is the same shape (276 inst ac, 87 % taxed). These are
  high-footprint/low-value, *not* high-value/low-footprint — do not conflate with
  the U-of-A mechanism.

## Contrast — park/river hoods are a different story (item 1, not this)

The hoods with the *biggest* lot-acre boosts are mostly river-valley, and the
measurement correctly rejects them as exempt-institutional: **Riverdale** (×2.4,
1 inst ac, 0 % exempt), **Cloverdale** (×2.5, 0 inst ac), **River Valley Gold Bar**
(×2.9, 0 % exempt), **Virginia Park** (×2.5, 6 % exempt). Their off-roll land is
parkland/river the polygon can't build on — the park-crediting story already told
in `FINDINGS_denominator_cardinality.md`, not exempt-institutional dilution.

## Caveats / shelf life

- **The exempt-acre measure is a proxy, tending to over-count.** It subtracts only
  the deduped *lot footprint* of taxable points that fall inside institutional
  polygons (centroid-`within`), not their building coverage, so a leased taxable
  pad on institutional land removes less than its true area. Treat `exempt_inst_ac`
  as an upper-ish bound and a **ranking** signal, not a cadastral figure.
- **`PU` is broad.** It spans genuine utility plants, pipeline ROW, and stormwater
  ponds/greenway ponds. Only `UI`/`AJ`/`UF` map cleanly to "institution"; a `PU`
  hood may be diluted by ponds rather than a campus. The `code`/`mechanism`
  columns carry this distinction — use them.
- **Zoning is permitted-not-built and coarsens over time** (2024 bylaw collapse).
  Parcel-level assessment remains the better "what's actually there" source
  (`PARCEL_LEVEL_OPPORTUNITIES.md`); the AJ/PU/UI/UF proxy is the best available
  without it.

## Feeds

- **Lot-acre toggle framing (Money view).** These hoods are the honest-lift
  category alongside the park/river hoods; U of A / Northlands are the exemplars.
- **Services lens (`docs/SPEC_services.md`).** The exempt-acre figures are the
  cost-side free-riding estimate — serviced land yielding zero municipal revenue.
  When the roads/fire/transit cost lenses land, cross `exempt_inst_acres` against
  the per-hood servicing supply for the "who is subsidised" story.
- Related: item 1 (outlier tails — the park/river contrast set lives there), the
  shipped lot-acre findings (`FINDINGS_denominator_cardinality.md`).

# Scope: True Revenue Per Acre (next phase)

**Status: SCOPED, not started.** Captures what's needed to turn the current
*assessed-value*-per-acre metric into an actual *tax-revenue*-per-acre metric.

## Why

The project is titled "Revenue Per Acre" but currently computes
`value_per_acre = total_assessed_value / area_acres` — **assessed value, not
revenue**. No mill rate is applied (see `join_and_calculate.py`). Assessed value
is a *proxy* for revenue and a biased one: Edmonton's non-residential mill rate
is higher than residential, so value-per-acre understates the revenue pull of
commercial/industrial land relative to housing. True revenue/acre applies the
per-class tax rate.

## Methodology check — RESOLVED 2026-06-28

Confirmed how comparable projects define the metric (web research, sources below):

- **Strong Towns** (canonical how-to): primary metric is **assessed value per
  acre**, explicitly does *not* apply mill rates; tax liability is offered only
  as a secondary analysis.
- **Urban3 / Joe Minicozzi** (originators of the 3D value-per-acre map — our
  closest analog): **taxable assessed value per acre**.
- Some derivative practitioners apply the rate → revenue/acre
  (`(assessed value × tax rate) / acres`), but this is the minority/stricter form.

**So the current metric (assessed value/acre) IS the common convention — it
matches Urban3 directly. A rename alone would be legitimate.**

**The deciding insight:** applying a *uniform* city-wide rate is just scaling
every parcel by the same constant → an identical-looking map, only the legend
units change. The map only changes shape if **rates differ by class**. Edmonton's
do, substantially (see external data below: non-res ≈ 2–3× residential). So the
real payoff of the revenue phase is capturing the **class differential**, which
re-ranks neighbourhoods (commercial/industrial rises relative to residential) —
a genuinely new signal, not a unit change.

**Decision: build the real computation, keep BOTH metrics as a toggle.** Keep
assessed value/acre (the Urban3 convention, comparable to every other VPA map)
*and* add revenue/acre using class-differential municipal mill rates. The gap
between the two maps reflects the effect of Edmonton's class-differential mill
rates. This also resolves the exempt question (below): Urban3/Strong Towns
use *taxable* value, so exempt parcels shouldn't inflate either metric — exclude/
separate under value, $0 under revenue (the two treatments converge).

Sources:
- Strong Towns, "Value Per Acre Analysis: A How-To For Beginners" —
  https://www.strongtowns.org/journal/2018-10-19-value-per-acre-analysis-a-how-to-for-beginners
- Urban3 methodology (taxable value per acre, 3D) — https://www.urbanthree.com/
- Urban Prosperity Network, value-per-acre how-to (the apply-the-rate variant) —
  https://urbanprosperity.net/how-to-calculate-and-visualize-value-per-acre-in-your-city

## Data we already have

The raw assessment CSV (`Property_Assessment_Data__Current_Calendar_Year_.csv`)
**already carries the class fields** — they're currently dropped in
`load_assessment.py` (values per `DATA.md`):

- `Tax Class` — clean 4-value field: **Residential, Non Residential, Other
  Residential, Farmland**. This maps directly to the City's published mill-rate
  classes — **use it as the rate join key** (cleaner than `Assessment Class 1`,
  which has messier values like COMMERCIAL / MA DERELICT RESIDENTIAL).
- `Assessment Class 1/2/3` + `Assessment Class % 1/2/3` — per-class apportionment
  for split-class parcels.

So split-class parcels can be handled correctly from existing data. Note the
exempt proxy already in use: `Assessment Class 1 == 'NONRES MUNICIPAL/RES
EDUCATION'` (3 rows, flagged `is_exempt` on load) — see exempt decision below.

## Data we still need (external)

- **Edmonton municipal mill rates by tax class**, for the **same year** as the
  assessment dataset. Published annually by the City (tax rate bylaw). Must cover
  the four `Tax Class` values present: Residential, Non Residential, Other
  Residential, Farmland.
  - **Partial data gathered 2026-06-28:** 2024 *residential* municipal rate
    ≈ **0.0076648** (~7.66 mills); residential & farmland share the same rate.
    Non-residential is materially higher (Alberta Municipal Affairs cites
    Edmonton non-res ≈ 21 mills vs the residential figure — but that mixed/total
    number may include education; **get the exact municipal-only non-res rate
    from the 2024 City tax rate bylaw before computing**). Differential confirmed
    at ~2–3×, which is the whole point (see Methodology check). Still need: exact
    municipal non-res rate, and the "Other Residential" rate, for the year that
    matches the assessment dataset.
- Decide: **municipal mill rate only** (revenue *to the city*) vs **municipal +
  education/provincial** (total property tax). Municipal-only is the cleaner
  "city revenue" story; pick one and document it.

## Computation

Per property, summing over its (up to 3) classes:

```
levy = Σ_class  assessed_value × (class_% / 100) × (mill_rate[class] / 1000)
```

Then aggregate `levy` by neighbourhood → `total_revenue`, and
`revenue_per_acre = total_revenue / area_acres`.

## Code changes

- **`load_assessment.py`** — stop dropping `Assessment Class N` + `% N` (and/or
  `Tax Class`); carry them through.
- **New module `src/apply_tax_rates.py`** (independently runnable, per project
  rule) — map class → mill rate, compute per-property `levy`, handling
  split-class apportionment. Mill rates from a small config/data file keyed by
  year + class (with source + year recorded), not hardcoded.
- **`aggregate_by_neighbourhood.py`** — sum `levy` → `total_revenue` (keep
  `total_assessed_value` too if we want both layers).
- **`join_and_calculate.py`** — add `revenue_per_acre`; decide whether it
  replaces `value_per_acre` or sits alongside it (a toggle in the web map could
  show value vs revenue).
- **Tests** for the new module: rate mapping, split-class apportionment, and the
  exempt → $0 case below.
- **Rename** docs/titles once revenue is real (or drop the rename if we decide
  assessed value is the chosen metric — see "Verify first").

## Methodology decisions to settle

- **Municipal-only vs total tax** (above).
- **Tax-exempt properties.** Currently flagged + included (correct for an
  *assessed value* analysis). Under a *revenue* framing they generate **$0**, so
  they'd legitimately pull a neighbourhood's revenue/acre down. This is a real
  treatment change, not a bug — decide and document.
- **Year alignment.** Mill rate year must match the assessment year; the dataset
  is "Current Calendar Year", so pin both.
- **Keep both metrics?** Showing assessed-value/acre and revenue/acre side by
  side is itself informative (the gap *is* the mill-rate story). Possible web
  toggle.

## Cross-refs

- Current metric definition: `ARCHITECTURE.md` (join_and_calculate) + `DATA.md`.
- Tax-exempt current handling: `ARCHITECTURE.md` Key Decisions table.

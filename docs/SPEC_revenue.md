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

## Verify first (methodology check)

Before building: **confirm how comparable projects define the metric.** Strong
Towns / Urban3-style "value per acre" maps often use **taxable assessed value**
as the headline (i.e. our current metric is a common, defensible variant), while
the stricter "revenue" version applies the levy. Decide whether we're matching
the common convention or going stricter — this determines whether (2) is a
rename or a real new computation. *(Peter is checking reference projects.)*

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

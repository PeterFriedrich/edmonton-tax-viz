# Parcel-Level Opportunities

Future work whose value is **gated on parcel-level information** — i.e. analyses that
the current neighbourhood-level unit of aggregation limits, distorts, or can only
approximate. Collected separately from `ANALYSIS_BACKLOG.md` because the blocker here
is a **unit-of-analysis** choice, not a method: these items get materially better (or
only become possible) when we compute at the parcel and aggregate up, rather than
aggregating first.

_Started 2026-07-01._

## Why this is its own axis

The project deliberately aggregates to the neighbourhood (see `DATA.md` §2, Architecture
Decision — Phase 1). That choice is what forces the **land-use set-aside** machinery:
neighbourhood-level aggregation needs *explicit* categorization of non-developable land
that a parcel-level approach (e.g. Urban3, `FINDINGS_revenue_scale.md` §7) handles
**implicitly** — you just include/exclude parcels by their actual status. Several
backlog items are really the same limitation resurfacing, so they belong together.

## What parcel data we already have vs. would need

- **Available in the source datasets** (per-property / per-parcel, currently aggregated
  away by the pipeline): the assessment roll `q7d6-ambg` (per-property value, class,
  exempt flag) and the property-info dataset `dkk9-cj3x` (lot size, zoning, year built).
- **Would need acquiring / more work:** true parcel *geometry* (lot polygons) for a
  real parcel-level map; a clean parcel↔neighbourhood spatial join; confirming the
  assessment roll's coverage of non-taxable parcels (known gap — exempt institutional
  land is absent from the roll entirely, `FINDINGS_revenue_scale.md` §4–5).

---

## Opportunities

### P1. Replace / validate the set-aside with true parcel inclusion
The set-aside (`is_set_aside`, zoning-composition ≥0.90) is a **proxy** for "this land
isn't in the taxable comparison." At parcel level you'd exclude non-taxable /
non-developable parcels directly and aggregate the rest — no threshold, no zoning-share
approximation. Would both **validate** the current set-aside list and remove the
0.90-threshold judgment call. Cross-ref: `SPEC_revenue.md`, `DATA.md` §5.

### P2. Kill the low-acre-denominator artifact (ANALYSIS_BACKLOG item 1)
Neighbourhood revenue/acre can be spiked by a single large-value parcel in a small hood.
Computing revenue/acre **per parcel** and aggregating (or reporting the distribution
within a hood, not just the mean) removes the artifact and sharpens the outlier audit.

### P3. Mixed-use disambiguation without guessing (ANALYSIS_BACKLOG item 1)
Today `nonres` lumps commercial / industrial / mixed, and a hood's character is inferred
from zoning-composition fractions. At parcel level each parcel carries its actual
assessment class and use — so mixed-use and the outskirts high-performers can be
resolved from what each parcel *is*, not from a neighbourhood-level zoning share.

### P4. Richer ML feature matrix (ANALYSIS_BACKLOG item 2)
Per-parcel features (value, lot size, year built, class, frontage) give far more signal
than neighbourhood aggregates, and allow modelling at the parcel then aggregating — or
predicting parcel value and studying residuals. The neighbourhood matrix is a
lossy summary of this.

### P5. Urban3-style true parcel revenue/acre map (the gold standard)
The parcel-level 3D revenue/acre map is the method this project approximates at the
neighbourhood scale (`FINDINGS_revenue_scale.md` §7). A genuine parcel map is the
natural "Phase 3" once parcel geometry + a clean spatial join are in hand — and it
would make P1–P4 fall out for free.

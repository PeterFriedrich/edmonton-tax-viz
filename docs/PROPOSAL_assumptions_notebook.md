# Proposal: `03_assumptions` verified notebook

**Status: APPROVED and BUILT 2026-09-28 (S201): new notebook, gating.** Rows as built differ slightly: the excluded-permit-types row was dropped, and the roll-zoning row sizes non-res levy. It adds
a gate to the weekly publish, which is a CI behaviour change.

## Why
`02_methods` explains how each number is built. Its "Known limitations" list
names the biggest assumptions but gives **no size** for any of them, and it
has no coverage of the public Development and Change lenses (Methods F3/F4).
A reader can't tell which assumption moves 0.7% of the levy and which moves 30%
of the homes.

## What
A new `notebooks/verified/03_assumptions.py`. `tools/run_verified_notebooks.py`
globs `*.py`, so the workflow file needs no edit.
- **Not self-contained**, like `01`/`02`: it imports the pipeline and reads the
  week's served data plus `data/raw`. Only the evidence notebooks
  (`docs/EVIDENCE_NOTEBOOKS.md`) must stand alone.
- **One table per public lens.** Each row has the **assumption**, **what it
  touches** (share of levy, land, homes or records, recomputed weekly), the
  **direction** of the bias, and **where it's argued** (a DECISIONS/FINDINGS
  pointer, never restated).
- The same two rules as `01`/`02`: **no hand-typed number**, and **invariants
  asserted, not values**. It never fails because a share moved. It fails only
  when a row can't be computed, or when two measures of the same thing
  disagree.
- A sentence in `02_methods` §8 links to it, so the limitations list stops
  being the only place.

## Rows, ranked by today's size (measured 2026-09-28 unless noted)
| lens | assumption | size today | source |
|---|---|---|---|
| Development | homes on the grid are the geocoded ones only | **30%** of 3-year units, 21% of 5-year, 16% since 2009, off-grid | served `dev_grid.json` coverage |
| Money (non-res cut) | exempt-candidate zoning is levied as billed | **16.4%** of non-res levy | raw roll + spatial zoning (findings §6) |
| Money (total) | same | **8.1%** of total levy | served `rev_frac_exempt` |
| Money (lot acres) | the lot denominator is City lot size, not clipped | median hood is 69% parcelled land | served `parcel_frac` |
| Money / Glass | the roll's own zoning field is ignored in favour of spatial zoning | the roll field is blank on 36% of parcels, 17.7% of non-res levy | raw (findings §6) |
| Change over time | 2024 and 2025 are omitted | 2 of 15 years; the non-contiguous gap | `SPEC_temporal.md` §0 |
| Money | set-aside hoods are greyed, off the scale | 48 hoods, **0.7%** of levy | served |
| Glass | one coordinate per account | levy share on accounts whose lot is bigger than a cell | raw Property Info `lot_size` |
| Roads | arterials are left out of road metres | share of centreline metres | raw `roads.geojson` |
| Development | the residential building-type list excludes conversions | share of permits excluded | raw permits |
| Money | class %s that don't sum to 100 are billed as stated | 80 properties | pipeline log |

The table's order is by size, so it is **computed, not typed**: the notebook
sorts it.

## Invariants (the gate)
- Every row computes: no NaN, and the share is in [0, 1].
- Development coverage recomputed from `dev_grid.json` cells equals the
  served `coverage` block.
- The exempt-candidate total from served `rev_frac_exempt × total_revenue`
  agrees with the raw-roll recomputation within rounding.

## Cost and risk
- Adds one spatial join to the weekly run, about 1–2 min on the runner. The
  raw-roll rows need `data/raw`, which the refresh already downloads.
- A new gate means a new way for the refresh to go red. Mitigation: only
  structural invariants, and every one falsified by mutation before merge.

## Decision for Peter
1. Approve a new notebook (vs. a section appended to `02_methods`, which is
   already 487 lines).
2. Approve it gating the publish like `01`/`02`. The alternative is to render
   it without gating, which is cheaper but is the "guard on a channel nobody
   reads" pattern.

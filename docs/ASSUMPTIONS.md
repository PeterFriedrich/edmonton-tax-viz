# Assumptions index

One line per premise a published number rests on that no guard proves. This is
an index, not an argument: each row points at the place that holds the
evidence, and the reasoning stays there. Sizes are not typed here. The ones
that can be recomputed are sized weekly by
`notebooks/verified/03_assumptions.py` (rendered as `03_assumptions.html`),
and this file says "03" for those.

**Status:** **VERIFIED** — a named test or invariant proves it. **SUPPORTED** —
evidence agrees, nothing re-checks it. **UNVERIFIED** — never checked.
**ACCEPTED** — known to be off by a measured amount, and used anyway.

**Build:** *public* reaches the public map; *full* is the specialist build only.

`tests/test_assumptions_index.py` fails when a sizing row is added to
`03_assumptions.py`, or a cost rate in `data/city_unit_costs.json` is marked
anything but ESTABLISHED, without a row here. It also fails when a file path in
this table stops existing. Section citations to `.md` files are checked by
`scripts/check_doc_citations.py`.

## Sized weekly (03_assumptions)

| # | Lens (as 03 names it) | Premise | Status | Size | Build | Evidence |
|---|---|---|---|---|---|---|
| A1 | Money (non-residential) | levy on exempt-candidate zoning is counted as paid | ACCEPTED | 03 | public | FINDINGS_blurb_claims.md §6 |
| A2 | Money (total) | the same premise, against the total levy | ACCEPTED | 03 | public | FINDINGS_exempt_institutional.md |
| A3 | Money / Glass | zone shares come from the bylaw map; the roll's own zoning field is often blank | ACCEPTED | 03 | public | FINDINGS_blurb_claims.md §6 |
| A4 | Money (lot acres) | the lot-acre denominator leaves out roads and unparcelled land | ACCEPTED | 03 | public | Methods §1 (`notebooks/verified/02_methods.py`) |
| A5 | Money | set-aside neighbourhoods are greyed, not ranked | ACCEPTED | 03 | public | FINDINGS_revenue_scale.md |
| A6 | Glass | one point per account, though a lot can be bigger than a grid cell | ACCEPTED | 03 | public | Methods §4 (`notebooks/verified/02_methods.py`) |
| A7 | Money | class percentages that don't sum to 100 are billed as stated | ACCEPTED | 03 | public | `src/apply_tax_rates.py` |
| A8 | Change over time | roll years 2024 and 2025 are omitted | ACCEPTED | 03 | public | SPEC_temporal.md §0 |
| A9 | Roads | arterial roads are left out of road metres | ACCEPTED | 03 | public | DECISIONS.md 2026-07-01 |
| A10 | Development (grid) | homes permitted with no location are off the grid | ACCEPTED | 03 | public | FINDINGS_blurb_claims.md F4 |

## Not sized by 03

| # | Premise | Status | Size | Build | Evidence |
|---|---|---|---|---|---|
| B1 | 2025+ Farmland municipal rate = Residential (no Farmland rate published since 2025; equal every year 2014–2024) | SUPPORTED | low (farmland parcel count in DATA.md §4) | public | `data/mill_rates.json` `_assumed`; DATA.md §4 |
| B2 | `bikeway_ops` source denominator: per what kind of km is unknown | UNVERIFIED | unknown | full | `data/city_unit_costs.json` `bikeway_ops`; DATA.md §13 |
| B3 | `bikeway_capital` source denominator: route-km or lane-km is unstated | UNVERIFIED | unknown | full | `data/city_unit_costs.json` `bikeway_capital`; DATA.md §13 |
| B4 | The road snow rate is blended over a network that includes arterials, so the local-road term is likely a little high | ACCEPTED | unmeasured; direction known (high) | public | DATA.md §13 |
| B5 | The bike snow rate is blended over a network that is mostly not bikeway | ACCEPTED | unmeasured | full | DATA.md §13 |
| B6 | Bike replacement value uses the future facility mix against the existing stock, so it likely understates | ACCEPTED | unmeasured; direction known (low) | full | DATA.md §13 |
| B7 | Utility figures are models, not bills | SUPPORTED | validation ratios | full | FINDINGS_utility_validation.md |

## Not indexed yet

- **Fire, transit, stormwater and water** (full build) have no sized rows in 03.
  Their premises live in DATA.md and the FINDINGS files.
- **`[unverifiable]` rows in DECISIONS.md** are decisions, not premises, and
  stay there. Add one here only if a published number rests on it.
- **DATA_ISSUES.md** holds upstream defects. One belongs here only once a number
  we publish rests on working around it (A8 is one).

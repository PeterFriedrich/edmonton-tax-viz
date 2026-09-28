# Proposal: per-cut exempt share (F1 root, F2's missing bands)

**Status: PROPOSED 2026-09-28 (S201). No code until Peter approves.** It changes
the served schema (a data contract), so CLAUDE.md requires the plan first.
Evidence: `docs/FINDINGS_blurb_claims.md` F1, F2 and §6.

## The defect

`rev_frac_exempt` (hood) and `exempt_frac` (grid) are shares of the **total**
levy. Every band, caveat and exempt endpoint reads them on the Residential and
Non-residential cuts too.
- **Non-residential:** 165 non-set-aside hoods have ≥25% of their non-res levy
  on exempt-candidate zoning. **144** of them fall under the gate, which tests the
  total share, so they get no band and no caveat (§6). ASPEN GARDENS: 9% of
  total levy, 100% of its non-res figure.
- **Residential:** the reverse. A hood's share can be mostly non-res levy that
  does not exist on this cut. F1's interim `c[col] > 0` filter hides the worst
  case (the $0 cells), but the base height and the certain/uncertain split
  still use the total share.

## What changes

### 1. Pipeline: two new served columns in each artifact, and the old one kept
| artifact | existing | new |
|---|---|---|
| `neighbourhood_value_per_acre.geojson` | `rev_frac_exempt` | `rev_frac_exempt_res`, `rev_frac_exempt_nonres` |
| `value_grid.json`, `value_grid_50.json` | `exempt_frac` | `exempt_frac_res`, `exempt_frac_nonres` |

- **No new join.** `apply_tax_rates` already writes `res_levy`/`nonres_levy` per
  parcel, and `main.py` already has the spatial `zone_codes` (§6: spatial is
  the right instrument).
- Add `exempt_res_levy` and `exempt_nonres_levy` next to `exempt_levy`:
  `exempt_candidate_levy` applied to each class levy.
- Numerator and denominator are the **same class**, so the share runs 0–1 on its
  own cut. It's NaN where the cut's levy is 0, by the same rule as today.
- A share is denominator-independent, so one pair serves both ground and lot
  acres, as `exempt_frac` does now.
- **Payload:** one grid column costs about 141 KB raw at 100 m and 374 KB at
  50 m. It is about 95% zero/null and gzips small; measure it in the PR. The
  new columns go into `data/expected_columns.json`, which
  `scripts/check_served_columns.py` reads.

### 2. Front end: `exemptFrac` follows the cut its consumer is drawing
One accessor, `exemptFrac(p, cut)`, maps `revenue_per_acre` → total,
`res_revenue_per_acre` → `_res` and `nonres_revenue_per_acre` → `_nonres`. It
falls back to the total column when the new one is absent, so the front end can
ship before the refresh does.

| consumer | reads cut from | change |
|---|---|---|
| Money: `instShiftMoney`, `instBandedMoney`, band elevations, tooltip range + caveat | `state.metric` | follows the cut |
| Glass: `glassInstCells`, base height | `gridColKey()` | follows the cut. The F1 `> 0` filter becomes redundant (a $0 cell has a null share), so delete it |
| Deviation: `isUncertain`, `deviationRateExempt`, `avgExempt`, tooltip | `state.labCut` | follows the cut |
| Ratio: `instBandedRatio`, bands, tooltip | none | **stays on total**: its numerator is total revenue |

### 3. Wording
On a subset cut the caveat row says *"N% of its non-residential revenue is on
institutionally-zoned land"* (or residential). Today it says "of revenue",
which is true only on Total. This is a COPY_DECISIONS row and Peter's call.

## Decisions for Peter

1. **Approve the schema:** two new columns per artifact, keeping the total one.
   The alternative, replacing `exempt_frac` with a per-cut triple, breaks the
   graceful fallback and every existing reader at once.
2. **Accept the visual consequence before the build.** On Non-residential, up to
   144 more hoods gain the caveat. Only the subset that also clears
   `INST_CONSEQUENCE_MIN` gets the outlined band. I'll measure both counts on
   the served data in PR 1 and bring them back before PR 2 renders anything.
3. **Caveat wording** on subset cuts (§3).

## Build order and guards
- **PR 1, pipeline:** add the columns. Tests:
  - `exempt_share_by_neighbourhood` has no unit test today. Add one whose
    fixture differs **only** in tax class, so a class-blind share fails.
  - Add the grid equivalent in `tests/test_export_value_grid.py`.
  - Update `expected_columns.json`.
  - The front end is untouched and reads the old column until the weekly
    refresh publishes the new ones.
- **PR 2, front end, after the refresh lands:**
  - Add the accessor and the consumer changes.
  - `verify-glass-inst.js` / `verify-inst-caveat.js`: assert that on
    Non-residential a hood like ASPEN GARDENS carries the caveat, and that on
    Residential no flagged cell has a null per-cut share.
  - `verify-blurbs.js`: the azure count recomputes from `exempt_frac_res`.
  - Falsify each by reverting the accessor to the total column.
- **Then** add a DECISIONS row citing those tests, and revisit F2's provisional
  "business, industry and institutions" wording.

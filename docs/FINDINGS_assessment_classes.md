# Findings — Assessment Class Structure

Captured 2026-06-28 while scoping the revenue phase. Source: local snapshot
`data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv` (2025 data,
439,769 rows). Numbers below are from that snapshot and will shift on re-download.

Purpose: record what the per-parcel class fields actually contain, so the levy
computation is built on verified structure rather than assumption. Tagged for a
later notebook pass (see "To visualize" at the end).

## The two class vocabularies

The CSV describes a parcel's tax class in **two different vocabularies**:

- **`Tax Class`** (col 9) — a clean 4-value field that matches the mill-rate
  table keys exactly. One value per parcel.
- **`Assessment Class 1/2/3`** (cols 11–13) with **`Assessment Class % 1/2/3`**
  (cols 14–16) — a finer, *split-capable* description using different labels. A
  parcel can carry up to three weighted class slices.

### `Tax Class` distribution

| Tax Class | Rows |
|---|---|
| Residential | 411,563 |
| Non Residential | 23,341 |
| Other Residential | 4,356 |
| Farmland | 509 |

### `Assessment Class 1` distribution

| Assessment Class 1 | Rows |
|---|---|
| RESIDENTIAL | 411,563 |
| COMMERCIAL | 23,054 |
| OTHER RESIDENTIAL | 4,356 |
| FARMLAND | 509 |
| MA DERELICT RESIDENTIAL | 284 |
| NONRES MUNICIPAL/RES EDUCATION | 3 |

Note `COMMERCIAL` is the label that bills under the `Non Residential` mill rate —
the core vocabulary mismatch.

**Update (2026-07-02, from the live feed):** a re-download surfaced a new label
`DESIGNATED IND PROPERTIES` (**1 row**) not present in the 2026-06-28 snapshot —
Designated Industrial Property (provincially-assessed plants / linear / machinery).
Its own `Tax Class` field reads `Non Residential`, so it's mapped there for the
municipal levy (the only rate this project applies). This was caught by the
pipeline's no-silent-drop guard (`apply_tax_rates` hard-fails on an unmapped
label), not by chance — see the deployment dry-run in `session-summary/2026-07-01.md`.

## Label → mill-rate class map

Every label that appears across `Assessment Class 1/2/3`, mapped to its
mill-rate class:

| Assessment Class label | → Mill-rate class | Note |
|---|---|---|
| `RESIDENTIAL` | Residential | |
| `COMMERCIAL` | Non Residential | vocabulary mismatch |
| `OTHER RESIDENTIAL` | Other Residential | |
| `FARMLAND` | Farmland | |
| `MA DERELICT RESIDENTIAL` | Non Residential | all 284 rows have `Tax Class = Non Residential` |
| `DESIGNATED IND PROPERTIES` | Non Residential | new in the live feed (2026-07-02, 1 row); its `Tax Class` reads Non Residential |
| `NONRES MUNICIPAL/RES EDUCATION` | *exempt → $0* | the existing `EXEMPT_CLASS` |

This map is exhaustive for the current snapshot — the labels appearing in the
2nd and 3rd slots are a subset of those above (no surprise vocabulary):

- Class 2 labels: COMMERCIAL (392), RESIDENTIAL (373), FARMLAND (225),
  OTHER RESIDENTIAL (103), MA DERELICT RESIDENTIAL (1)
- Class 3 labels: FARMLAND (136), RESIDENTIAL (91), COMMERCIAL (52),
  OTHER RESIDENTIAL (6), NONRES MUNICIPAL/RES EDUCATION (1)

## Two structural facts that simplify the levy computation

1. **`map(Assessment Class 1)` equals `Tax Class` in 100% of rows** (0
   mismatches across all 439,769). The primary class slice carries no
   information beyond `Tax Class`; the only additional content in the
   `Assessment Class` columns is the split slices (2/3) and the finer labels
   (`MA DERELICT RESIDENTIAL`, `NONRES MUNICIPAL/RES EDUCATION`).

2. **Split-class is rare:** 1,094 rows have a 2nd class (~0.25%), 286 have a 3rd
   (~0.065%). The remaining ~99.75% are single-class.

Because of fact 1, a single unified formula covers every parcel — no
special-casing of splits:

```
levy = assessed_value × Σ_{i=1..3} (pct_i / 100) × rate[ map(Class_i) ]
```

where `rate[exempt] = 0`. For a single-class parcel, `pct_1 = 100` and
`Class_2/3` are NaN, so it collapses to `assessed_value × rate[Tax Class]`.

## Open checks (verify in code, flag — no silent drops)

- Confirm `% 1 + % 2 + % 3 ≈ 100` per row; flag and report any that don't sum.
- Confirm no label appears that isn't in the map above (guard against a future
  re-download introducing a new class).

## To visualize (notebook later)

- Value share vs. levy share by class — the value→revenue reweighting that is
  the project thesis (per-class % of total assessed value vs. % of total
  municipal levy). **Partially SHIPPED 2026-07-16 as the residential-revenue
  decomposition** (`res_levy` → the "Residential $" Money metric + per-hood
  share tooltip; residential-class = 52.6% of the citywide 2025 levy —
  DATA.md §4). The full per-class notebook cut is still open.
- Distribution of split-class parcels — where they are, how much value they
  carry, how much the apportionment moves their levy vs. a flat `Tax Class` rate.
- Per-neighbourhood exempt share, to identify the exempt-heavy neighbourhoods
  that will legitimately read low on revenue/acre.

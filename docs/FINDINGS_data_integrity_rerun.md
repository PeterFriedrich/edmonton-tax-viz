# Data-integrity re-run on current data — 2026-11-03 (S239)

**Re-run of the 2026-07-01 full pass** (`docs/FINDINGS_data_integrity_audit.md`),
instrument `docs/DATA_INTEGRITY.md`, family (b) correctness. `AUDIT_LEDGER.md`
never-audited #6. Model: Opus 5.5.

**Data:** a fresh pull on 2026-11-03 of `q7d6-ambg` (439,825 rows), `dkk9-cj3x`
(439,825), `65fr-66s6` (407) and `fixa-tstc` (11,551), all count-checked
against the server. It went into the session scratchpad, not `data/raw/`, which
the report worktree shares. It was compared with the served
`web/data/*.json`/`.geojson` from the 2026-11-02 refresh (`b83f877`).

**Delta since 07-01, so the scope is not a repeat.** T2 (roll year), T4
(cardinality, S74), T7 (colour, S215/S221) and T8 (membership, S126) have each
had their own audit since. The ledger named four joints that came after 07-01:
the lot-acre columns, the `res_levy` decomposition, the value/res grids and the
services join. The services cost lens itself had four audits (S142, S149, S187,
S202), so its join was covered here through the zero-fill check (§3). The
name-join "who reads the warning" question belongs to candidate #8; this run
only checked today's unmatched set.

## Bottom line

**The published money numbers can be trusted on today's data. Nothing is
blocking.** An independent re-derivation from the raw roll matches every served
money column on all 406 rendered hoods to within 5×10⁻⁶. It uses its own levy
loop, its own join and its own projected areas, and shares only two pieces of
hand data: `NAME_CORRECTIONS` and the rate values. Both of those were checked
separately (§1, §2). The highest-leverage hardening is not in the money path. It
is the reader question on the eight warn-only zero-fills (§3), and that is
candidate #8's.

## 1. T1 — class → rate mapping, 2026 roll — **CONFIRMED-correct**

- The first-slot label agrees with the parcel's own `Tax Class` for every
  label/class pair on the roll. The only mismatch is 2 rows: the exempt label
  under `Tax Class` "Non Residential". They are billed $0 by design.

  | label | Tax Class | rows | value |
  |---|---|---:|---:|
  | RESIDENTIAL | Residential | 411,635 | $162.9B |
  | COMMERCIAL | Non Residential | 22,950 | $52.6B |
  | OTHER RESIDENTIAL | Other Residential | 4,402 | $23.9B |
  | FARMLAND | Farmland | 511 | $0.06B |
  | DERELICT RESIDENTIAL | Non Residential | 270 | $0.08B |
  | DESIGNATED IND PROPERTIES | Non Residential | 1 | $0.02B |
  | NONRES MUNICIPAL/RES EDUCATION | Non Residential | 2 | $0.004B |

- Slots 2 and 3 carry only labels that are already mapped.
- The 2026 rate values are checked against `pwis-wc4c` every month by the digest
  (all 15 matched on 2026-11-01, issue #770). This run did not re-check them.
- The "class % ≠ 100" warning fires on **80 rows**. Every one is source rounding
  (85–99%, median 99%, none at 0%). They leave **$9.4M of value** unbilled,
  roughly **$0.2M of levy**, which is 0.008% of the $2.791B total. Billing
  as-stated is the right call. The warning goes to an unread log, but its
  ceiling is immaterial.

## 2. T3 (today's set only) + T4 — **CONFIRMED-correct**

- **Unmatched names:** OLIVER ($500) on the assessment side and LEWIS FARMS (no
  parcels carry the name) on the boundary side. That is exactly what `DATA.md`
  §"Name Matching" expects, so 406 of 407 boundaries render.
- **Every `NAME_CORRECTIONS` target re-checked by spatial containment on today's
  roll** (07-01 recorded containment for two of the ten). Each is the right hood: 86–100% of the
  source name's value lies inside the target polygon. The spillovers are the
  documented ones (LEWIS FARMS INDUSTRIAL → 3 points in LEWIS FARMS; RIVER VALLEY
  WINDEMERE → 4 in WINDERMERE; ANTHONY HENDAY SOUTHEAST → 5 in SAKAW/ASTER). The
  City's own `Neighbourhood` field decides which hood a parcel belongs to, not
  geometry; that has always been the rule.
- **Independent re-derivation vs served file**, 406 hoods. Max relative
  difference and count over 0.1%:

  | column | max rel | > 0.1% |
  |---|---:|---:|
  | `value_per_acre` | 4.2e-6 | 0 |
  | `revenue_per_acre` | 4.6e-6 | 0 |
  | `total_revenue` | 4.2e-6 | 0 |
  | `res_revenue_per_acre` | 4.7e-6 | 0 |
  | `nonres_revenue_per_acre` | 4.6e-6 | 0 |

  Citywide levy: served $2,791,060,264 against $2,791,060,786 re-derived.
  Agreement this tight also shows the roll did not change materially between
  the 11-02 refresh and the 11-03 pull.
- **`res_levy` decomposition:** residential plus non-residential is 99.98% of the
  levy. The remainder is Farmland's own rate class, as `apply_tax_rates`
  documents.

## 3. Joints added after 07-01

**Lot-acre columns — CONFIRMED-consistent.** `build_hood_lot_acres` on the fresh
pull reproduces the served `parcel_frac` and `value_per_lot_acre` to within
5×10⁻⁶. The 7 served nulls are the `LOW_PARCEL_FRAC` suppression. The bound
check passes (1 over 1.0, the known PEMBINA). 59 lot-ineligible points ($1.23B)
are logged and left out of numerator and denominator alike. **One lat/long point
spans two hoods** (104 rows, $25.1M, OLIVER/WÎHKWÊNTÔWIN). There, lot area goes
to the point's first hood while dollars follow each row's own hood. The OLIVER
side is the $500 straggler, so the effect is immaterial. The heuristic itself
was audited in S74.

**Value grids (100 m and 50 m) — CONFIRMED-conserving.** From the served files,
Σ cell value × cell acres = **$239.572B**, the raw roll total to the dollar, and
Σ levy matches the hood file to within 1.8×10⁻⁷. There are no negative cells and
no cell where residential exceeds total. The code guards conservation of value
only. Levy uses the same `groupby`, so binning cannot drop levy without dropping
value, and the value guard covers the shared mechanism.

**Services join (zero-fill) — CONFIRMED on today's data, warn-only by design.**
`join_and_calculate.py` left-joins eight per-hood frames and
`fillna(0.0)`s the misses: permits, roads, bike, stormwater, fire, transit,
water, franchise. Each logs a warning, and none fails. So a name drift in one
loader would publish as a plausible zero. **Today every published zero is
real:**

- Roads, 8 zeros: only WESTVIEW VILLAGE is residential (private manufactured-home
  roads, `FINDINGS_revenue_scale.md`).
- Fire, 5 zeros: the zero-event hoods listed in `FINDINGS_revenue_scale.md`.
- Water, 55 zeros: all non-residential, matching the residential-only scope.
- Stormwater: 0 zeros.
- Transit, 54 zeros: checked directly, not from the docs. CAMERON HEIGHTS,
  DONSDALE, TRUMPETER AREA, MARQUIS and RIVER'S EDGE have **0 scheduled
  fixed-route stops** (control: GLENORA 9 of 9). These are on-demand zones,
  which `DATA.md` documents as missing from GTFS.

Whether anyone reads those eight warnings is candidate #8's question, and it is
left there.

## 4. T5 — CRS — **CONFIRMED-correct**

Every `.area`/`.length`/`.buffer(d≠0)`/`.simplify` in `src/` and
`scripts/build_*` runs on EPSG:3400 (`PROJECTED_CRS`, `_ALBERTA_CRS`,
`SETBACK_CRS`, `AREA_CRS`, `WORKING_EPSG` all = 3400, checked). The 4326
uses are export reprojection, `revenue_by_zone`'s point-in-polygon join (no
metric math) and `buffer(0)` validity repair. Nothing uses EPSG:26911.

## 5. T2, T6 — covered elsewhere, wiring confirmed

- **T2:** `check_roll_year_against_fir.py`, `check_year_alignment.py`,
  `check_unmatched_names.py` and `check_value_anchors.py` all run in
  `refresh.yml`. The last three refreshes (10-19, 10-26, 11-02) are green. The
  brief's "if the only defense is a human remembering…" is no longer true.
- **T6:** the one live defect, `RTCC` unclassified (THE UPLANDS 2.7%), was caught
  by the monthly digest and fixed the same day in #776. The default is `other`,
  not the brief's `nonres`.

## 6. Completeness pass

- **`is_exempt` feeds no number.** `load_assessment` computes, documents and
  returns it, and no pipeline code in `src/`, `scripts/` or `main.py` reads it.
  It is **not unread**, though: `tests/test_load_assessment.py` asserts on it,
  other test fixtures carry it, and it shows as a column in the dataframe preview
  on the published `web/verified/01_money_lens.html`. Deleting it is still the
  project's preference for obsolete code. It touches a published page's table
  and two tests, so it is a TODO item, not a quiet cleanup.
- **The brief has drifted** (`claim`): `ASSESSMENT_YEAR = 2025`,
  `DEFAULT_CATEGORY = "nonres"`, "three known-unresolved" names (one remains),
  T2's "only defense is a human", and stale line numbers. Fixed in this PR with
  a dated status block at the top of `DATA_INTEGRITY.md`, not a rewrite, because
  the ranked targets are still the right ones.
- Every `errors="coerce"` and `fillna` in `src/` was read. The money-path ones
  (`apply_tax_rates` empty slot → 0, `export_value_grid` eligibility) are correct
  as written. The rest sit on permit, transit and fire inputs that their own
  audits cover.

## What this run got wrong

- **The first re-derivation was less independent than its framing.** It reused
  `NAME_CORRECTIONS` and the same rate constants, so a correction pointing at the
  wrong hood would have matched on both sides and passed. That was caught before
  writing up, and closed with the containment check in §2. It covers all ten
  entries; 07-01 recorded containment for two.
- **The transit-zero PASS was first written on documentation alone.** "These
  hoods really have no transit" is a negative claim, the riskiest shape in this
  repo. It was re-checked against GTFS stops with a positive control before it
  went into §3.
- **A confident negative, wrong on the first draft.** §6 first said nothing
  reads `is_exempt`, from a grep of `src/`, `scripts/` and `main.py` only. A
  wider grep, run before committing, found it asserted in a test and printed on a
  published notebook page. The claim it supports, that it feeds no number, still
  holds. "Nothing reads it" did not.
- **Smaller:** the first script pointed at `data/raw/boundaries.geojson`, which
  doesn't exist (the file is `neighbourhoods.geojson`), and a GTFS read without
  `dtype=str` crashed. Neither reached a result.

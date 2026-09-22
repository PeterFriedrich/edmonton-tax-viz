# FINDINGS — the road + bike sliver floors (#491, #520), audited

**Run:** 2026-09-22, S187, **Opus 5.5**, effort `high`. `docs/AUDIT_LEDGER.md`
S173–S186 backlog item #1. ⚠️ **Same model family as the author (Opus 5)** — a
different model, not an independent one.
**Target:** `MIN_PIECE_M = 1.0` in `src/load_bike.py` (DECISIONS 2026-09-20) and
`src/load_roads.py` (DECISIONS 2026-09-21), the asymmetry class they were fixing
(a floor on the display path, none on the metric path), and every surface that
divides by a road/bike column.
**Grounding read in full first:** DECISIONS rows 2026-09-20 (bike), 2026-09-20
(S7 per-unit), 2026-09-21 (roads); `SPEC_services.md` §Computation + Guards; S184
handoff §2b.
**Data:** local `data/raw/` (2026-09-03) for the overlay; the served
`web/data/neighbourhood_value_per_acre.geojson` (CI build after #520) for every
published figure. The local overlay reproduces S184's **32,469** metric pieces
exactly, and local vs served `road_m_per_acre` agree to the third digit on the
hoods spot-checked.

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Should sub-metre overlay crumbs be removed from the metric at all? | **SOUND** |
| L1 | Is *piece length* the right test for "boundary artefact"? | **CONDITIONAL** — the floor is right about what it removes, but the mechanism behind the crumbs moves 470× more length and has no treatment. §1 |
| L2 | Is 1.0 m the right value, and metric-groups-only the right scope? | **SOUND** — reproduced |
| L3 | Does the display-floor-only asymmetry recur in another `src/load_*.py`? | **PASS** |
| L4 | Does any surface divide by an unfloored road/bike column? | **FAIL (full build only)** — the `$ revenue / road metre` tooltip. §2 |
| L5 | Code/comments | **WARN** — two comments now false. §3 |

## §1 — L1: boundary-running road is allocated by digitizing noise, and the floor only catches its dust

The crumbs `MIN_PIECE_M` removes are the tail of a bigger mechanism. Where a
neighbourhood boundary is drawn **on** a road centreline, `gpd.overlay` hands the
road to whichever side it falls on in the low decimals. Measured over collector +
local pieces lying wholly within 2 m of their own hood's boundary:

- **95.2 km of metric road (2.6%) runs along a boundary.** 99.8% of that length
  is in pieces ≥ 1 m, so the floor removes **0.2 km** of it. Pieces run up to
  785 m. At 0.5 m tolerance it is 51 km; at 5 m, 123 km.
- **It is noise, not a systematic offset.** The median offset of those pieces
  (≥ 20 m long) from the boundary is **0.2 m** (p10 0.05, p90 0.73). The
  boundary *is* the centreline.
- **It lands lopsided.** Across the 367 hood pairs that share such road, the
  heavier side holds **70%** of the length, weighted by length.
- **Sensitivity.** Splitting each pair's shared length 50/50 instead of taking
  what the overlay decided moves **25 published, not-set-aside hoods by > 5%**
  and **7 by > 10%** in `road_m_per_acre`, so the same share moves the two roads
  cost columns. Examples: GAINER INDUSTRIAL +21.7%, MAPLE RIDGE −21.3%,
  UNIVERSITY OF ALBERTA FARM +19.0%, CPR IRVINE +15.9%, MORIN INDUSTRIAL +13.2%,
  WILSON INDUSTRIAL −11.2%, STARLING +10.5%. None crosses the Ratio lens's 5 m/acre
  floor. **MAPLE RIDGE's entire published road figure** (0.56 m/acre, $27.78/acre
  lifecycle) is 94.5 m of boundary-running road.
- **Bike:** 2.5 km (0.25%) along boundaries, 92% one-sided; 11 hoods > 5%. Smaller
  because routes rarely trace boundaries.

⚠️ **The 50/50 split is a convention, not ground truth.** Nothing here shows the
current allocation is *wrong*. The metric is literally "road inside this
polygon", and a road *on* the line is ambiguous under that definition. What is
shown is that the published number for those hoods depends on sub-metre
digitizing noise, by the amounts above.

**This was already accepted. Its stated grounds don't hold.**
`SPEC_services.md` §Guards accepts *"the residual noise in v1"* on two claims:

1. *"collectors can still trace boundaries occasionally"*. Measured:
   **collector 5.8% (53.3 km)** and **local 1.5% (41.9 km)** of their length
   runs along a boundary, against arterial 9.3% (126.6 km). Arterials are the
   plurality, but metric road is **43%** of all boundary-running road.
   "Occasionally" was never measured.
2. *"the conservation check bounds the damage"*. **It cannot.** Conservation
   compares citywide length before and after the overlay. Moving a metre from
   one hood to its neighbour leaves that total unchanged, so the check is blind
   to exactly this error. This is `check-where-the-value-can-be-wrong` again.

The spec also says to *"note it as a known limitation"*. It appears nowhere else:
not in `data/DATA.md` Known Quirks for the roads source, and not on any reader
surface.

**Sharpest argument against this finding:** the effect is concentrated in
atypical hoods (industrial, river valley, Henday, university lands). The
residential core moves 5–7% at most (DELTON, ARGYLL, SHERWOOD, CROMDALE), and 2.6%
of citywide length is small next to the $/m rate's own uncertainty. It is a
sensitivity, not a defect. **What would change the verdict to SOUND:** record the
caveat with these sizes (DATA.md Known Quirks + the SPEC line corrected), or adopt
an explicit rule for boundary-on-centreline road (split, or assign by a stated
tie-break). That is Peter's call, not an audit fix.

## §2 — L4: the `$ revenue / road metre` tooltip still divides by what the Ratio lens rejects

`web/index.html`, Money tooltip, `FULL_BUILD` branch:

```js
if (FULL_BUILD && p.road_m_per_acre > 0 && p.revenue_per_acre != null) {
  const perM = p.revenue_per_acre / p.road_m_per_acre;
```

The Ratio lens computes **the same quotient** but gates it through `ratioKept`:
`p[d.col] >= d.floor` (5 m/acre, commented *"below this the ratio is an
artifact"*) **and** `!p.is_set_aside`. The tooltip applies neither. #520 fixed the
two hoods whose input was a crumb and left the surface asymmetric. S184's own row
names the asymmetry (*"the exposure was the one surface with no floor"*), and the
surface still has none.

Served file, today:

- **15 hoods that are NOT set aside** sit below the 5 m/acre floor and print a
  figure. The top two are **YELLOWHEAD CORRIDOR WEST, $53,309 / road metre**, the
  highest in the city and 3× DOWNTOWN's $14,069, on 37 m of road (13 stubs of
  roads crossing a corridor strip, longest 8.5 m), and **HERITAGE VALLEY AREA,
  $13,238**, on 16.4 m (7 stubs, longest 3.3 m). Both pieces sets clear the 1 m
  floor. Length was never the problem for these.
- **43 set-aside hoods** also print the row.

Exposure is `/dev-build-full/` only, so this is not the public build. **Fix
(proposed, not applied):** gate the row on the Ratio lens's own predicate —
`RATIO_DENOMS.roads.floor` and `!p.is_set_aside` — so the two surfaces cannot
disagree. Guard it in `verify-smoke.js` next to §C9/§C10 by asserting the row
appears only where `ratioKept` holds.

Other division sites checked: `res_revenue_per_acre / revenue_per_acre`
(bounded share, `> 0` guarded, `<1%` floor) **PASS**. `ratioOf` (gated by
`ratioKept`) **PASS**. `deviationRate = rate / devAcreFrac(p)` **PASS**: the
divisor is floored by construction, because `is_set_aside` fires at
`SET_ASIDE_THRESHOLD = 0.90` and the kept maximum is 0.896 (RIVER VALLEY GOLD
BAR), a ×9.6 ceiling that the 2026-08-12 decision chose on purpose.

## §3 — L3 / L5

- **L3 PASS.** Only `load_roads` and `load_bike` overlay *lines*. `load_zoning`'s
  overlay yields area **fractions** normalised per hood, and its crumbs, like
  GAINER INDUSTRIAL's `set_aside_frac` 1.2e-05, are never used as a divisor
  except through the 0.90-floored `devAcreFrac`. Point-in-polygon `sjoin`s
  (stormwater, transit, `revenue_by_zone`) produce no pieces.
- **L5 WARN, two false comments:**
  - `export_roads_web`: *"The colour driver: the same metric join_and_calculate
    publishes."* It is computed from the raw overlay **without** `MIN_PIECE_M`.
    The rounded `v` differs by 0.1 m/acre in 8 hoods. That is immaterial, but
    the sentence is false.
  - `RATIO_DENOMS` comment cites *"WESTVIEW VILLAGE, $1.3M/m on a near-zero road
    base"* as a current artefact. Since #520 Westview is 0 m. The live example
    is now YELLOWHEAD CORRIDOR WEST.

## Reproduction

Scripts were run from the session scratchpad. The method, in enough detail to
rewrite them:

1. `load_roads._prepare_segments('data/raw/roads.geojson', load_boundaries(...))`,
   then keep `group in {collector, local}` (32,469 pieces).
2. Along-boundary means `piece.within(hood.boundary.buffer(tol))`, with tol
   0.5 / 2 / 5 m. Offset is the mean distance of 11 interpolated points to the
   boundary.
3. For the neighbour, `sjoin(predicate="within")` of along pieces against the
   other hoods' buffered boundaries. Per pair, sum the length on each side. The
   50/50 counterfactual moves each pair to half-half and recomputes per acre.
4. Join to the served file on `neighbourhood_name`, filter
   `~is_set_aside & road_m_per_acre > 0`.
5. Tooltip: served `revenue_per_acre / road_m_per_acre` where
   `road_m_per_acre > 0`, split by `< 5` and by `is_set_aside`.

## What this run got wrong

- **I nearly published LEWIS FARMS as the headline L1 case.** It showed 143 m of
  road, 100% along-boundary, 5.38 m/acre, just above the Ratio floor. It is **not
  served**: DATA.md documents it as the one empty hood. It came from the local
  boundary file and was caught only by joining to the served file. The same trap
  is waiting for anyone who measures on `data/raw/` alone.
- **The one-sidedness count overstates.** "207 of 367 pairs ≥ 90% one-sided"
  counts short perpendicular stubs that end within 2 m of a boundary as
  "along". Those pairs total only 16.6 km. The 70% length-weighted figure is
  the honest headline, and the doc uses it.
- **The 2 m containment test is a proxy.** A road genuinely 1–2 m inside a
  boundary counts as "along". The 0.2 m median offset says that is rare, but it
  is not zero, and the tol sweep (51 / 95 / 123 km) shows the headline depends
  on tol.
- **L4 is code-read plus the served file, not rendered.** No full-build
  screenshot or verify run was taken. The condition is unambiguous in the source,
  but "prints" means "the code prints it given this data", not "seen".
- **The overlay is on 2026-09-03 raw data**, 18 days older than the served
  build. Piece counts reproduce, so the network had not materially changed, but
  per-hood L1 sizes can differ slightly from what a fresh build would give.

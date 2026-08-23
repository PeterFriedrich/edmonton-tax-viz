# Findings — Can the Infill lens move from the neighbourhood to the 100 m grid?

Captured 2026-08-22 (S115) answering Peter's question: *"shouldn't we actually
have it more granular? like either the 100m grid, or some alternative. one of
the affectors i wanted was like, distance of each block from lrt stations, and
schools, for each property, then it would get filled into each spike."*

Sources: local snapshots `data/raw/Property_Info__Current_Calendar_Year_.csv`
(439,685 rows, 100% geocoded), `data/raw/building_permits.csv`,
`data/raw/roads.geojson` (53,720 features), `data/raw/gtfs_*.csv`, and the
served `web/data/dev_grid.json` / `value_grid.json`. Numbers are from those
snapshots and will shift on re-download. Probe scripts were session-scoped
(scratchpad); every figure below is reproducible with pandas groupbys on the
EPSG:3400 cell index `floor(x / 100)`, reusing `export_value_grid._point_lot_stats`
and `load_permits.NEW_WORK_TYPES` / `RESIDENTIAL_BUILDING_TYPES` so the cell
population matches the pipeline's (34,658 cells here vs 34,666 shipped, 0.02%).

**Verdict in one line: the ACTIVITY half re-grains cleanly with a kernel; the
SUITABILITY half does not, because at 100 m `far == 0` means "no data" far more
often than it means "nothing built".** Straight-line distance to transit is
separately unusable and must be network distance.

## 1. Why the question is not just "run the same code on smaller polygons"

The shipped lens (`SPEC_development.md` Lens B) is a signed diverging score
`−(z(far) + z(activity))` over 358 in-scale neighbourhoods, computed live in the
browser. Both ingredients already exist per cell, in files that already share
cell geometry — `export_dev_grid` bins to the same EPSG:3400 grid as
`export_value_grid`, deliberately. So the re-graining looked like a join.

It is not, because **three of the lens's guards are properties of the
neighbourhood as a unit**, not of the metric:

- `is_set_aside` (zoning composition ≥ 0.90) has no per-cell equivalent;
- the **asymmetric residential gate** (`is_residential === false` barred from the
  teal end) is what keeps industrial parks and river-valley fringe out of the
  opportunity end — and it is measured per hood;
- the per-arm p95 clamps and the ±0.4 verdict cut are calibrated over 358 hoods.

## 2. The activity term — SOLVED by a kernel

Share of the 34,658 in-population cells carrying **non-zero** activity, where
the kernel is a disc of the given radius centred on each cell:

| radius | cells in kernel | `units` 5yr | `units` 3yr | `units` long |
|---|---|---|---|---|
| **0 m (the cell itself)** | 1 | **11.8%** | **7.3%** | 28.1% |
| 100 m | 5 | 26.7% | 19.6% | 44.5% |
| 200 m | 13 | 38.8% | 31.0% | 56.3% |
| 300 m | 29 | 50.4% | 42.4% | 67.3% |
| 400 m | 49 | 58.8% | 50.8% | 74.8% |
| **600 m** | 113 | **73.0%** | 65.8% | 85.5% |
| 800 m | 197 | 81.8% | 76.4% | 90.2% |
| 1000 m | 317 | 87.9% | 84.5% | 92.4% |
| 1500 m | 709 | 94.5% | 92.9% | 95.6% |

⚠️ **At cell grain with no kernel the default column is 88% zeros.** Standardising
that is meaningless: for 88% of cells the score would collapse to `−z(far)` plus
a constant, and the lens would silently become an inverted-FAR map still
labelled "mismatch". The hood unit hides this — essentially every hood has
*some* activity, so `z(activity)` is a genuine continuous variable there.

The curve has no cliff, so the radius is a judgement rather than a discovery.
600 m clears the degeneracy on the default column and coincides with the
conventional TOD walkshed; 800 m is what the 3yr window needs.

**Decision taken 2026-08-22 (Peter): kernel/radius activity, not a longer
window and not abandoning the cell grain.**

## 3. The suitability term — NOT solved at 100 m

### 3.1 The cells are thin, and the opportunity tail is the thinnest part

Distinct property points per cell: median 8, but **22.9% of cells hold exactly
one** and 33.0% hold ≤ 3.

The bottom-5% FAR band — i.e. *the entire opportunity end of the scale*:

| | opportunity tail | all cells |
|---|---|---|
| median points per cell | **1** | 8 |
| share with ≤ 3 points | **90.9%** | 32.9% |
| share `f_res > 0.5` | **11.8%** | — |
| share `f_ind > 0.5` | **44.7%** | — |

At hood grain the same pollution exists but is bounded — the S48-era prototype
found 13 of the opportunity top-30 were `frac_industrial > 0.5`. At cell grain
it is nearly half of the whole tail.

### 3.2 ⚠️ `far == 0` is a DATA GAP, and it is 16% of cells

`gross_area` is null or zero on **6.25% of eligible rows** citywide (`DATA.md`
already records ~6.2%). The pipeline sums it with `NaN → 0`, so a cell whose
properties all lack the field emits `far = 0.0` — **indistinguishable from a cell
with genuinely nothing built on it.**

Cells by FAR band against the share of their own properties missing `gross_area`:

| FAR band | cells | share of all | median % missing `gross_area` | median points |
|---|---|---|---|---|
| **exactly 0** | 5,616 | **16.2%** | **100.0%** | 1 |
| (0, .02] | 975 | 2.8% | 0.0% | 1 |
| (.02, .05] | 683 | 2.0% | 0.0% | 2 |
| (.05, .10] | 903 | 2.6% | 11.1% | 3 |
| (.10, .20] | 7,010 | 20.2% | 0.0% | 9 |
| (.20, .40] | 12,305 | 35.5% | 0.0% | 10 |
| > .40 | 7,166 | 20.7% | 0.0% | 10 |

Within the in-scale population, **3,964 cells (12.4%) have `far == 0` AND zero
activity — every one of them ties at the identical maximum opportunity score.**
60% of the `far == 0` cells are industrial; the top hoods holding them are
SOUTHEAST (ANNEXED) INDUSTRIAL, WINTERBURN INDUSTRIAL AREA EAST, MISTATIM
INDUSTRIAL, CLOVER BAR AREA.

The next band up is **not** a data gap (median 0% missing) — those are single
large-lot parcels: one property, a big lot, a small building. Real, but that is
"land awaiting assembly", not "a mature area with room to add a suite".

### 3.3 What a prototype actually surfaces

Score prototyped at a 600 m kernel with a set-aside proxy, the residential gate
re-expressed per cell (`f_res > 0.5` required for the teal end) and a
`n_points >= 4` thinness floor (which drops 27% of the in-scale population):
the top of the opportunity end is entirely `far == 0`/near-zero cells in
GOODRIDGE CORNERS, STILLWATER, RIVER'S EDGE, SUDER GREENS — subdivided but
unbuilt suburban land, arriving with an unbreakable tie.

⚠️ `SPEC_development.md` Lens B explicitly considered and dismissed this
confound: *"New suburbs are not the problem: their high activity already pushes
them to the pressure side."* **That protection is an artifact of averaging ~400
properties per hood and does not survive the re-graining.**

## 4. The shipped hood lens is CLEAN — and the reason is undocumented

Because §3.2 is a property of the data rather than of the grid, the obvious
follow-up is whether it biases the live map. It does not, but only just:

| threshold | in-scale hoods above it | of which RESIDENTIAL (not barred from teal) |
|---|---|---|
| > 25% of rows missing `gross_area` | 87 | **3** |
| > 50% | 69 | **2** |
| > 80% | 38 | **1** |

The two residential survivors at >50% are EVERGREEN (4 eligible rows; already
documented in Lens B as legitimately teal) and MAPLE RIDGE (3 rows).

⚠️ **The asymmetric residential gate is therefore absorbing a data-completeness
gap, not only a land-use one** — 85 of the 87 affected hoods are non-residential
and barred from the opportunity end for an unrelated stated reason. That is
load-bearing behaviour the spec does not claim, and it is exactly the job the
gate **cannot** do per-cell, where "residential fraction" is often measured on a
single point.

**No live defect. No change made to the shipped lens.**

## 5. ⚠️ Straight-line distance to LRT is unusable — it must be network distance

Method: a routable graph built from `data/raw/roads.geojson` (186,931 nodes /
206,836 edges, 99.5% reachable), one multi-source Dijkstra from the 33
GTFS-derived LRT stations (max station snap 108 m), against 3,982 randomly
sampled properties.

⚠️ **Correction, 2026-08-23 — this probe graph was built from ALL centrelines,
including 2,117 RAILWAY rows** (186,931 nodes is the unfiltered count). A walk
could therefore travel *along the LRT track itself* to reach an LRT station.
That biases network distance DOWNWARD, toward euclidean, so the false-positive
rates below are if anything **understated** — the conclusion holds and the
direction is safe. The shipped graph (`src/amenity_distance.py`) keeps only
`centerline_type == "Road"`: 163,841 nodes, and better connected at 99.83%.
Re-measured on the shipped graph over all 439,245 reachable properties, the
network/euclidean ratio median is **1.36** against this sample's 1.35.

| band | euclidean says in-band | network says in-band | euclidean's FALSE POSITIVES |
|---|---|---|---|
| 400 m | 192 | 62 | **68%** |
| 600 m | 357 | 161 | **55%** |
| 800 m | 504 | 262 | **48%** |
| 1000 m | 637 | 380 | **40%** |

Network/euclidean ratio: median **1.35**, p90 1.67, p99 2.55, max **7.90**;
21.7% of properties are at least 1.5× further by road than by line.

A straight-line 600 m transit filter would be **wrong more than half the time it
says yes**, which is the direction that matters — it manufactures transit-adjacent
opportunity that is not reachable. The river valley and the rail/freeway
corridors are the mechanism. Network distance costs one Dijkstra over data
already in the repo, so there is no reason to ship the euclidean version.

### ⚠️ The GTFS station set needs a membership pass before it is used
Deriving stations from the 3 light-rail routes (`route_type_descr` =
*Tram, Streetcar, Light rail*) → trips → `stop_times` → `parent_station` yields
**33 parents from 130 served stop_ids**. That set includes things that are not
passenger stations — `Heath Sciences Tail Track`, `Kathleen Andrews Platform`,
`DL Macdonald Platform` (bus garages / tail track). ⚠️ This is the `T8` shape
(`DATA_INTEGRITY.md`): the names look right, so check what the members **are**.

## 6. Data available today (no acquisition blocker)

- **LRT stations** — derivable from the GTFS already in `data/raw/`, no new
  download. Note the membership caveat above. The 58 `location_type == 1` stops
  are *not* the answer: that set mixes LRT stations with bus transit centres.
- **Schools** — two live Socrata datasets, probed 2026-08-22:
  `996c-239n` *EPSB School Locations* (225 rows, `Last-Modified` 2026-04-22) and
  `gfxq-u8uu` *Edmonton Catholic Schools (Current)* (97 rows, 2026-05-04). Both
  carry `latitude`/`longitude` and a grade level, so "nearest elementary" stays
  answerable. Not yet in `download_data.py`.
- **Per-property distances** are cheap at this scale (439,685 points × 322
  schools) and are the right grain: compute per property, aggregate to the cell,
  rather than measuring from the cell centroid.

## 6a. ⚠️ The fix shipped 2026-08-22 handles TOTAL absence, NOT partial

`build_hood_lot_acres` now emits `far = null` where **no** eligible row records a
floor area (16 of 410 hoods on the local snapshot; 12 were already set-aside
grey). Re-scoring the shipped population before/after:

| | in scale | clampPos | top of the teal arm |
|---|---|---|---|
| before | 358 | 0.765 | EVERGREEN 1.51, WESTVIEW VILLAGE 1.49, MAPLE RIDGE 1.46 |
| after | 348 | 0.774 | WESTVIEW VILLAGE 1.50, MAPLE RIDGE 1.47, CANOSSA 0.98 |

EVERGREEN leaves the scale (its teal was never a measurement — 4 eligible rows,
none with a floor area); WESTVIEW VILLAGE still saturates and becomes #1; MCLEOD
joins the saturating set. The ordering is otherwise unchanged.

⚠️ **A hood that is PARTLY missing still has an understated `far`, and one of
them is #2 on the teal arm.** MAPLE RIDGE records a floor area on only ~33% of
its eligible rows, so its FAR is understated by roughly 3× and it keeps a
near-saturating opportunity score. The null fix cannot reach this case — there is
a usable value, it is just built from a third of the rows. Options not taken: a
coverage threshold (null the hood below X% recorded) or a coverage-scaled FAR
(divide by the recorded share). **Both need a decision about what fraction is
enough, and neither should be guessed** — the same shape as the 0.90 set-aside
threshold. Open in `docs/ANALYSIS_BACKLOG.md` §12.

## 7. What this implies for build order

1. ✅ **DONE 2026-08-22 — `gross_area` absence is now explicit.** A unit with no
   recorded floor area emits `null`, not `0` (§6a). ⚠️ Partial coverage is
   **still** unhandled and still biases toward opportunity.
2. ✅ **DONE 2026-08-23 — the distances ship as per-cell attributes.**
   `dist_lrt_m` / `dist_school_m` on `value_grid.json`, cell median, Lens B
   untouched. ⚠️ **No UI reads them yet.** Distances (network, both amenity
   sets) are **independent of the score** and
   **Decision taken 2026-08-22 (Peter): attributes and a filter, NOT a weighted
   term in the suitability score** — proximity is a desirability input, not an
   "underused" input, and folding it in would turn a descriptive metric into a
   weighted index whose weights nothing can falsify.
3. The cell-grain **score** is gated on (1) plus per-cell replacements for the
   set-aside exclusion and the residential gate. On today's numbers, shipping it
   without those would put a teal opportunity end in front of readers that is
   ~16% missing-data cells.

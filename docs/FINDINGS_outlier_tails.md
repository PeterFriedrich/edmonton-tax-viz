# Findings — Performance tails vs land-use classification (outlier audit)

**Date:** 2026-07-09 (`ANALYSIS_BACKLOG.md` item 1). Reproducible via
`tools/audit_outlier_tails.py` (repo root; reads the served
`web/data/neighbourhood_value_per_acre.geojson` for the canonical published
fields, the `data/raw/` roll + zoning for counts / dominant zone, and
`data/dc_use_by_hood.csv` for item 3's resolved DC use split). Both the
revenue/acre and value/acre tails are surfaced; set-aside hoods (48) are excluded
from the ranked comparison (off-scale by design, matching the colour treatment),
leaving **358 hoods** ranked.

## The question

Two observations put the `res` / `com` / `ind` / `mix` / `dc` / `inst` / set-aside
classification (`src/load_zoning.py`) on trial:

1. Several of the **highest** revenue/acre and value/acre performers sit out on
   the city **outskirts** — counterintuitive; you'd expect the core to dominate.
   Suspicion: they're mixed-use (folded into `nonres`) or otherwise in a bucket
   that doesn't match what's on the ground.
2. There's a cluster of **weak** performers **inside the non-residential group**
   that also needs explaining.

A top performer in the wrong bucket, or a systematic weak-performer pattern in
`nonres`, would mean the categories need refining (e.g. a mixed-use split). The
audit annotates each tail with composition (served `frac_*` + the resolved DC use
split), the dominant base zone code + its bylaw description, a downtown-anchored
distance band, and a thin-denominator check (account count + the single largest
account's share of hood value) so an artifact is separable from a real performer.

## Verdict

**The classification holds up. Neither tail is a misclassification artifact — both
resolve into genuine land-use and denominator effects, and the mixed-use split the
item floated is *not* warranted.** Specifically:

- The outskirts-high-performer surprise is **real but benign**: it is big-box DC
  power centres, genuine industrial, and *dense new-suburb residential* — none of
  them thin-denominator artifacts.
- The weak-non-res cluster is **low-intensity heavy industrial on very large
  acreages** plus the **exempt/institutional roll gap** (already item 7) plus
  **annexed-but-unbuilt agricultural land** — all correctly low, none miscoded.
- **Thin-denominator artifacts exist only in the bottom tail**, never the top, so
  the revenue/acre and value/acre *leaders* are trustworthy at face value.

## 1. The top tail is not artifact-driven

The top 15 by revenue/acre are led by **Downtown** (248.8k/ac; core; com/mix/inst)
and **University of Alberta** (171.7k/ac; the exempt-institutional case, item 7),
then a mix of core high-density residential (Wîhkwêntôwin, Garneau, Strathcona)
and DC-dominant power centres further out. Crucially, **every** top-15 hood has
either thousands of accounts or a low single-account share — the largest top-share
in the top 15 is U of A's 26 % (47 accounts), and that is the genuine
$2.242B-on-half-its-polygon exempt case, not a one-parcel spike. **No top performer
is a small-hood / one-dominant-parcel artifact.** The value/acre top tail tells the
same story (Downtown 13.7M, Wîhkwêntôwin 9.9M, Garneau 8.8M, U of A 7.6M).

## 2. The outskirts high performers resolve into three legitimate groups

Filtering to top-quartile revenue/acre sitting **> 9 km** from the downtown
centroid returns ~30 hoods, all of which fall into one of three real categories —
not one is a miscoded core-type hood:

- **Big-box DC power centres** — South Edmonton Common (DC80), Mill Woods Town
  Centre (DC75), and (just inside the 9 km cut) Summerlea (DC63), Calgary Trail
  South (DC66), Place LaRue (DC75). Item 3's DC use split resolves these to
  **commercial** (`frac_dc_com` 58–80 %), so "DC" here is not opaque — it is
  power-centre retail, exactly as the 2026-07-03 use-mix note predicted. Their
  low single-account share (7–23 %) confirms real multi-tenant retail, not a spike.
- **Genuine industrial** — Sunwapta (IM/CB, ind38 com31), Edmiston (IM, ind97),
  White (IM, ind88): annexed light/heavy industrial correctly in `ind`.
- **Dense new-suburb residential** — Walker, Secord, Summerside, Laurel,
  Rutherford, Allard, McConachie, Keswick, etc. (RSF, res 60–80 %), each with
  **thousands of accounts and a 1–3 % top-account share.** These are legitimately
  productive per acre because modern suburbs pack many small-lot dwellings; the
  low top-share is the proof they are not denominator artifacts.

The surprise is therefore explained without touching the classification: the
outskirts *can* out-produce mid-ring hoods when they are new dense subdivisions or
regional retail, and the audit's location + thin-denom columns make that legible.

## 3. The weak non-residential cluster is genuine low-intensity land, not miscoding

The bottom value/acre tail is dominated by **agricultural (`AG`/`A`) zoning in
annexed-but-unbuilt outskirts** (Marquis, Meltwater, River's Edge, Kendal,
Goodridge Corners, …) and river-valley `A`-zone hoods — land that simply is not
developed yet, correctly reading near-zero. Within the non-residential group
proper, the weak performers separate cleanly:

- **Low-intensity heavy industrial on very large acreages** — Clover Bar Area
  (IM, ind50, **4,765 ac**), Maple Ridge Industrial (IM, ind52), Crossroads
  (ind46, 1,352 ac). Big footprints of low-value-per-acre heavy/annexed industrial;
  the bucket is right, the intensity is genuinely low.
- **Exempt / institutional roll-gap hoods** — Yellowhead Corridor West (AJ,
  inst95, 7 accounts, 83 % top-share) and University of Alberta Farm (AJ, inst98,
  14 accounts, 86 % top-share, low-value farmland *on* the roll). These are the
  item-7 exempt-institutional mechanisms surfacing on the value lens; not a
  classification error, and cross-referenced there.

No systematic "weak performer stuck in `nonres`" pattern appears that a category
change would fix — the com/ind/mix/dc split introduced 2026-07-03 already did that
work.

## 4. No mixed-use misclassification — the split is not warranted

Every hood with `frac_mixed > 0` carries mix as a **minority fraction** (the true
`MU`/`RMU`-type mixed zones total ~317 ac citywide, ~1 % of nonres — confirmed
again here), and the DC-dominant hoods are the power centres already resolved to
commercial by item 3. Nothing in either tail is a mixed-use hood masquerading in
the wrong bucket. The 2026-07-03 hypothesis — that mixed-use might drive the
outskirts surprise — is **rejected**: DC power-centre retail and dense new
residential drive it instead. A dedicated `mixed` category split would not change
any tail.

## 5. Thin-denominator artifacts — bottom tail only

Applying a strict artifact test (single account ≥ 50 % of hood value **and**
≤ 50 accounts) returns **6 hoods, all in the bottom tail**: Yellowhead Corridor
West, U of A Farm, Anthony Henday Mistatim, Heritage Valley Area (2 accounts,
100 % top-share), Kendal, River Valley Kendal. These are exempt/annexed/undeveloped
land where one account trivially dominates a near-empty roll — expected, and they
already read as low performers. **The top tail contains none of them**, so the
per-acre *leaders* need no denominator asterisk.

## Caveats

- **Distance is centroid-to-centroid** from the Downtown hood centroid (EPSG:3400);
  bands (core < 4 km, outskirts > 9 km) are a coarse location signal, not a travel
  metric. Large annexed hoods have centroids that pull their distance outward.
- **Dominant zone code** is the single largest base zone by overlaid area — a
  useful one-line label, but a hood can be genuinely multi-code (the composition
  column carries the rest). The bylaw `description` is the modal one per code.
- This is the **auto** half of item 1. The **by-hand** half — satellite / bylaw
  spot-checks of individual surfaced outliers — is left to a laptop session; this
  doc's per-hood annotations are the running start for it.

## Feeds

- Confirms the `res`/`com`/`ind`/`mix`/`dc`/`inst` split is fiscally sound — no
  build-side refactor of `load_zoning.py` categories is called for.
- The exempt/institutional weak-non-res hoods (Yellowhead Corridor West, U of A
  Farm) cross-reference `FINDINGS_exempt_institutional.md` (item 7).
- The annotated tails (composition + density + top-share) are a ready feature set
  for item 2 (ML feature importance) once `scikit-learn` lands in the env.

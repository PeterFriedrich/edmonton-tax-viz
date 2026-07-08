# Findings — Land-Use Diversity vs Fiscal Productivity and Servicing Burden

**Date:** 2026-07-07. First deconfounded pass in Session 22 (`ANALYSIS_BACKLOG.md`
item 4); **updated Session 24** to fold in the resolved Direct Control land-uses
(`ANALYSIS_BACKLOG.md` item 3) and re-admit the previously-dropped high-`frac_dc`
hoods. Reproducible via `tools/analyze_land_use_diversity.py` (run from the repo
root against the standing `data/raw/` inputs, the served `web/data/` GeoJSON, and
`data/dc_use_by_hood.csv`).

**Verdict up front.** Tested in Edmonton's own data, at the neighbourhood
scale:

1. **Fiscal productivity — supported, secondary.** Land-use diversity is
   associated with higher **revenue per acre**, and the association survives
   controlling for building-stock age, density, and lot size (partial
   r = **+0.27**, n = 299). But density is by far the dominant driver of
   revenue/acre (r = +0.66); diversity is a real but smaller *independent*
   contributor on top of it.
2. **Servicing burden — not supported.** Diversity shows **no** relationship
   with **road metres per dwelling** (raw r = −0.04, partial r = −0.03). The
   eye-catching negative correlation with road *per acre* (−0.38) is
   built-form confounding — older, denser hoods have more road per acre
   regardless of use mix. Divide by dwellings instead of acres and the
   apparent servicing benefit disappears.

The headline the data will not support is "mixed-use neighbourhoods need less
road per household." At comparable age and density they do not, in Edmonton.
**Resolving the Direct Control land that the first pass had to drop, and
re-admitting 8 hoods, does not change either verdict** (§2.1).

## 1. Method

**Diversity index.** Normalized Shannon evenness over renormalized *developed*
zoned-area shares — residential, commercial, industrial, mixed, institutional
(the `frac_*` shares are exported per hood by the use-mix pipeline,
`src/load_zoning.py`):

    H = −Σ pᵢ ln pᵢ  /  ln(k),   k = 5 developed categories, pᵢ renormalized to sum to 1

0 = single-use, 1 = perfectly even across the five. `frac_never` / `frac_notyet`
are excluded (river-valley / undeveloped land would otherwise read as
"diverse"). Set-aside hoods are excluded throughout (off the fiscal comparison,
matching the views).

**DC resolution (Session 24).** `frac_dc` (Direct Control) is bespoke per-site
bylaws with no single claimable use. The first pass treated it as *unknown* and
dropped every hood with `frac_dc ≥ 0.30` (14 hoods) — otherwise single-use power
centres like SOUTH EDMONTON COMMON (81 % DC) would score as "diverse."
`ANALYSIS_BACKLOG` item 3 has since classified each DC provision's use from its
bylaw **Purpose statement** (918 provisions → `tools/dc_use_labels.py` →
`data/dc_inferred_use.csv`, QA'd against the live pages), then area-weighted
those up to neighbourhoods (`tools/rollup_dc_uses.py` → `data/dc_use_by_hood.csv`,
splitting each hood's `frac_dc` into `frac_dc_res/_com/_ind/_mix/_inst/_unknown`
and reconstructing the authoritative `frac_dc` **exactly**, max|Δ| = 0.0000). The
resolved shares are now **folded into** the developed categories
(`frac_commercial += frac_dc_com`, etc.), and the exclusion rule changes from
`frac_dc ≥ 0.30` to **`frac_dc_unknown ≥ 0.10`**: a hood is dropped only when its
*unresolved* DC is large. **92 %** of citywide DC mass resolves to a use; the
10 % residual is legacy parcels carrying no bylaw page in the City's open-data
layer (`url = "legacy"`) plus ~20 unpublished/inaccessible provision pages
(§2.1).

**Metrics.**
- **revenue per acre** and **road m per acre** — from the served hood GeoJSON.
- **road per dwelling** = (road m/acre × hood acres) ÷ dwellings. Hood acres
  come from `load_boundaries()` full-resolution polygons, **not** derived from
  the slim web GeoJSON (that understates ~15 % — see
  `FINDINGS_utility_validation.md` §4). Dwellings from **two** denominators
  (see §3.2).

**Confounders (controls).**
- **Age** = 2026 − median `year_built` per hood (`dkk9-cj3x`).
- **Density** = dwellings ÷ hood acres.
- **Lot size** = median `lot_size` per hood (`dkk9-cj3x`, m²).

Partial correlations regress each control out of both variables (OLS residuals,
`numpy.linalg.lstsq`) and correlate the residuals. (`scipy`/`statsmodels` are
not project dependencies; a formal regression with p-values is a later step —
significance here is read off n: at n ≈ 299, |r| > ~0.113 is p < 0.05.)

## 2. Data and join (no silent drops)

- **358** developed, non-set-aside hoods carry a diversity index; **358/358**
  match the DC-use rollup.
- **0** boundary-acres mismatches (clean join on normalized hood name).
- **52** hoods have no RESIDENTIAL assessment records — all pure
  industrial/commercial (ALBERTA PARK INDUSTRIAL, CALGARY TRAIL NORTH, …);
  correctly excluded from the per-dwelling test (they have no dwellings).
- **9** hoods have no median `year_built` (new/undeveloped areas).
- **Analysis set: n = 299** (developed, `frac_dc_unknown` < 0.10, complete
  controls).
- H across the set: min 0.00, median **0.24**, max 0.89. Edmonton is mostly
  single-use residential; genuinely mixed hoods (Downtown and the mixed-use
  cores) are the tail, not the norm.

### 2.1 DC re-admission (Session 24)

Folding the resolved DC uses in and switching to the `frac_dc_unknown` rule
changes the analysis set from the pre-resolution **n = 293** to **n = 299**:

- **Re-admitted (8)** — previously `frac_dc ≥ 0.30`, DC now resolved *and* the
  hood has residential controls: CHARLESWORTH, EBBERS, EMPIRE PARK, KINOKAMAU
  PLAINS AREA, MILL WOODS TOWN CENTRE, SOUTH EDMONTON COMMON, SUMMERLEA, TERRA
  LOSA. (The other 6 previously-dropped hoods stay out: MCCAULEY and STRATHCONA
  JUNCTION still exceed the unknown trap; PLACE LARUE, CALGARY TRAIL SOUTH,
  HERITAGE VALLEY AREA and LEWIS FARMS BUSINESS EMPLOYMENT are all-non-residential
  and fail the per-dwelling controls regardless.)
- **Newly excluded (2)** — `frac_dc < 0.30` so they were in the old set, but a
  large `legacy` DC parcel with no bylaw page pushes `frac_dc_unknown ≥ 0.10`:
  CROMDALE, ROSSDALE.
- Folding DC in shifts individual-hood H by **0.039 on average** — small. The
  headline correlations move within rounding (§3), so the first pass's verdicts
  were **not** an artifact of dropping DC land.
- **Honest residual.** MCCAULEY is the clearest unresolved case: ~43 % of its DC
  is three old bare-"DC" parcels the City's open data tags `url = "legacy"` with
  no agreement number and no page — genuinely unclassifiable from the available
  data, not a scrape failure. One large `legacy` parcel *was* hand-resolved:
  SUMMERLEA's 50-ha parcel is geometrically coincident with the West Edmonton
  Mall DC (`dc2-1198`), so it inherits `mix` (documented in
  `tools/rollup_dc_uses.py`).

## 3. Results

### 3.1 Pearson correlation matrix (n = 299)

|            |    H | rev/ac | road/ac | road/dw | density |  age | lot |
|------------|-----:|-------:|--------:|--------:|--------:|-----:|----:|
| **H**      | 1.00 |  +0.35 |  −0.38  |  −0.04  |  +0.22  | −0.37| +0.02|
| rev/acre   |      |   1.00 |  +0.07  |  +0.01  |  **+0.66** | −0.07| −0.09|
| road/acre  |      |        |   1.00  |  −0.24  |  +0.23  | **+0.54**| −0.21|
| road/dwell |      |        |         |   1.00  |  −0.17  | −0.06| +0.02|

Two confounds are visible directly: revenue/acre is driven by **density**
(+0.66), and road/acre is driven by **age** (+0.54). Diversity correlates with
both age (−0.37, mixed hoods skew *newer*) and density (+0.22) — which is why
its raw correlations need deconfounding.

### 3.2 Servicing burden — the null, under two denominators

Road per dwelling was computed with both a simple proxy and the full model, to
be sure the null is not a denominator artifact:

| dwelling denominator | H vs road/dwell (raw) | partial |
|---|---:|---:|
| RESIDENTIAL record count (per-unit rows) | −0.03 | −0.02 |
| `build_connections` model (551,831 citywide) | −0.04 | −0.03 |

The two denominators rank hoods almost identically (**r = 0.996**), and the
connection model captures ~33 % more dwellings (apartment units the record
count misses, concentrated in exactly the mixed/dense hoods) — yet the
correlation with diversity stays at zero either way. **The null is robust.**

### 3.3 Fiscal productivity — real but secondary

| relationship | raw r | partial r (age, density, lot) |
|---|---:|---:|
| H vs **revenue/acre** | +0.35 | **+0.27** |
| H vs road/acre (built-form, *not* servicing) | −0.38 | −0.31 |
| H vs **road/dwelling** (servicing) | −0.04 | −0.03 |

Revenue/acre vs diversity is the one relationship that *survives* controls
(+0.27). Diversity adds fiscal productivity beyond what density alone explains
— but density (+0.66) remains the primary lever.

### 3.4 Stratified comparison (high- vs low-diversity within era × density)

Split by building era (pre-1950 / 1950–80 / post-1980) × density tercile, and
compare the above- vs below-median-diversity hoods within each cell (medians):

- **Revenue/acre:** high-diversity hoods match or exceed low-diversity in
  **5 of 6** populated cells (e.g. post-1980 high-density $28,364 vs $25,350) —
  consistent with §3.3. The one exception is post-1980 *low*-density ($12,257 vs
  $15,839), a thin, land-extensive band.
- **Road/dwelling:** no robust direction — high-diversity medians run at or
  slightly below low-diversity in most cells (e.g. post-1980 mid 6.0 vs 8.3) but
  the differences are small and the pooled partial correlation is a null (−0.03).
  Consistent with the §3.2 null; the stratified lean is within noise.

## 4. Limitations

- **Zoned, not built, mix.** The 2024 bylaw's broad zones understate
  fine-grained mix (a residential zone can permit small-scale commercial), and
  zoning is permitted-not-built. Neighbourhood-scale *zoned* mix is what this
  measures. This now includes the DC land, classified from each provision's
  stated Purpose — still an intended-use signal, not a built-form audit.
- **Correlational, no p-values yet.** Partial correlations control three
  confounders linearly; they are not a full model. A regression / random-forest
  permutation-importance pass (folding diversity into item 2's feature matrix)
  is the natural next step, and would put confidence intervals on +0.27.
- **DC classification is Purpose-statement inference.** Each DC use is read from
  the bylaw's Purpose text (res/com/ind/mix/inst), QA'd on a 32-page sample plus
  a corpus-wide audit (~2–3 % boundary-case error, concentrated in medium-
  confidence mixed-use calls). The ~8 % still-unresolved DC mass is carried as a
  distinct `frac_dc_unknown` and drives the two exclusions in §2.1 — never
  silently folded into a use.
- **`inst` sensitivity.** Dropping institutional land from the index weakens the
  (already-not-the-servicing-metric) road/acre correlation toward zero but
  leaves the revenue/acre relationship intact — the fiscal-productivity finding
  does not hinge on how institutional land is treated.

## 5. Reproduce

    python tools/dc_use_labels.py        # -> data/dc_inferred_use.csv (DC use labels)
    python tools/rollup_dc_uses.py       # -> data/dc_use_by_hood.csv  (frac_dc split by use)
    python tools/analyze_land_use_diversity.py

Inputs: `web/data/neighbourhood_value_per_acre.geojson`,
`data/raw/neighbourhoods.geojson`,
`data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv`,
`data/raw/Property_Info__Current_Calendar_Year_.csv`,
`data/raw/zoning.geojson` (for the rollup). A notebook version (scatters
coloured by era, for `notebooks/exploration/`) is deferred.

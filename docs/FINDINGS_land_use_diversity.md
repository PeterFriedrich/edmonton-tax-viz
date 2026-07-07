# Findings — Land-Use Diversity vs Fiscal Productivity and Servicing Burden

**Date:** 2026-07-07 (Session 22). Closes the first deconfounded pass of
`ANALYSIS_BACKLOG.md` item 4. Reproducible via
`tools/analyze_land_use_diversity.py` (run from the repo root against the
standing `data/raw/` inputs + the served `web/data/` GeoJSON).

**Verdict up front.** Tested in Edmonton's own data, at the neighbourhood
scale:

1. **Fiscal productivity — supported, secondary.** Land-use diversity is
   associated with higher **revenue per acre**, and the association survives
   controlling for building-stock age, density, and lot size (partial
   r = **+0.27**, n = 293). But density is by far the dominant driver of
   revenue/acre (r = +0.71); diversity is a real but smaller *independent*
   contributor on top of it.
2. **Servicing burden — not supported.** Diversity shows **no** relationship
   with **road metres per dwelling** (raw r = −0.03, partial r = −0.02). The
   eye-catching negative correlation with road *per acre* (−0.36) is
   built-form confounding — older, denser hoods have more road per acre
   regardless of use mix. Divide by dwellings instead of acres and the
   apparent servicing benefit disappears.

The headline the data will not support is "mixed-use neighbourhoods need less
road per household." At comparable age and density they do not, in Edmonton.

## 1. Method

**Diversity index.** Normalized Shannon evenness over renormalized *developed*
zoned-area shares — residential, commercial, industrial, mixed, institutional
(the nine `frac_*` shares are exported per hood by the use-mix pipeline,
`src/load_zoning.py`):

    H = −Σ pᵢ ln pᵢ  /  ln(k),   k = 5 developed categories, pᵢ renormalized to sum to 1

0 = single-use, 1 = perfectly even across the five. `frac_never` / `frac_notyet`
are excluded (river-valley / undeveloped land would otherwise read as
"diverse"). **The DC trap:** `frac_dc` (Direct Control) is *unknown* use, not
mixed use — treating it as a category makes single-use power centres like SOUTH
EDMONTON COMMON (81 % DC) score as diverse, so hoods with `frac_dc ≥ 0.30` are
flagged low-confidence and dropped from the analysis set (14 hoods). Set-aside
hoods are excluded throughout (off the fiscal comparison, matching the views).

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
significance here is read off n: at n ≈ 293, |r| > ~0.115 is p < 0.05.)

## 2. Data and join (no silent drops)

- **358** developed, non-set-aside hoods carry a diversity index.
- **0** boundary-acres mismatches (clean join on normalized hood name).
- **52** hoods have no RESIDENTIAL assessment records — all pure
  industrial/commercial (ALBERTA PARK INDUSTRIAL, CALGARY TRAIL NORTH, …);
  correctly excluded from the per-dwelling test (they have no dwellings).
- **9** hoods have no median `year_built` (new/undeveloped areas).
- **Analysis set: n = 293** (developed, `frac_dc` < 0.30, complete controls).
- H across the set: min 0.00, median **0.20**, max 0.87. Edmonton is mostly
  single-use residential; genuinely mixed hoods (Downtown, McCauley, Blatchford,
  Baranow) are the tail, not the norm.

## 3. Results

### 3.1 Pearson correlation matrix (n = 293)

|            |    H | rev/ac | road/ac | road/dw | density |  age | lot |
|------------|-----:|-------:|--------:|--------:|--------:|-----:|----:|
| **H**      | 1.00 |  +0.33 |  −0.36  |  −0.03  |  +0.20  | −0.34| +0.04|
| rev/acre   |      |   1.00 |  +0.12  |  −0.00  |  **+0.71** | −0.07| −0.09|
| road/acre  |      |        |   1.00  |  −0.24  |  +0.24  | **+0.54**| −0.21|
| road/dwell |      |        |         |   1.00  |  −0.16  | −0.06| +0.02|

Two confounds are visible directly: revenue/acre is driven by **density**
(+0.71), and road/acre is driven by **age** (+0.54). Diversity correlates with
both age (−0.34, mixed hoods skew *newer*) and density (+0.20) — which is why
its raw correlations need deconfounding.

### 3.2 Servicing burden — the null, under two denominators

Road per dwelling was computed with both a simple proxy and the full model, to
be sure the null is not a denominator artifact:

| dwelling denominator | dwellings (set) | H vs road/dwell (raw) | partial |
|---|---:|---:|---:|
| RESIDENTIAL record count (per-unit rows) | — | −0.02 | −0.005 |
| `build_connections` model (551,831 citywide) | — | −0.03 | −0.015 |

The two denominators rank hoods almost identically (**r = 0.996**), and the
connection model captures ~33 % more dwellings (apartment units the record
count misses, concentrated in exactly the mixed/dense hoods) — yet the
correlation with diversity stays at zero either way. **The null is robust.**

### 3.3 Fiscal productivity — real but secondary

| relationship | raw r | partial r (age, density, lot) |
|---|---:|---:|
| H vs **revenue/acre** | +0.33 | **+0.27** |
| H vs road/acre (built-form, *not* servicing) | −0.36 | −0.30 |
| H vs **road/dwelling** (servicing) | −0.03 | −0.02 |

Revenue/acre vs diversity is the one relationship that *survives* controls
(+0.27). Diversity adds fiscal productivity beyond what density alone explains
— but density (+0.71) remains the primary lever.

### 3.4 Stratified comparison (high- vs low-diversity within era × density)

Split by building era (pre-1950 / 1950–80 / post-1980) × density tercile, and
compare the above- vs below-median-diversity hoods within each cell (medians):

- **Revenue/acre:** high-diversity hoods match or exceed low-diversity in
  **every** populated cell (e.g. post-1980 high-density $27,983 vs $23,632) —
  consistent with §3.3.
- **Road/dwelling:** no consistent direction — high-diversity is sometimes
  slightly higher, sometimes lower, within noise (e.g. post-1980 high-density
  4.6 vs 4.6; 1950–80 mid 9.1 vs 7.6). Consistent with the §3.2 null.

## 4. Limitations

- **Zoned, not built, mix.** The 2024 bylaw's broad zones understate
  fine-grained mix (a residential zone can permit small-scale commercial), and
  zoning is permitted-not-built. Neighbourhood-scale *zoned* mix is what this
  measures.
- **Correlational, no p-values yet.** Partial correlations control three
  confounders linearly; they are not a full model. A regression / random-forest
  permutation-importance pass (folding diversity into item 2's feature matrix)
  is the natural next step, and would put confidence intervals on +0.27.
- **DC land is dropped, not resolved.** 14 high-`frac_dc` hoods are excluded.
  Running the DC provision scrape (item 3) to resolve their real uses would let
  them back in and materially upgrade the index.
- **`inst` sensitivity.** Dropping institutional land from the index weakens the
  (already-not-the-servicing-metric) road/acre correlation toward zero but
  leaves the revenue/acre relationship intact — the fiscal-productivity finding
  does not hinge on how institutional land is treated.

## 5. Reproduce

    python tools/analyze_land_use_diversity.py

Inputs: `web/data/neighbourhood_value_per_acre.geojson`,
`data/raw/neighbourhoods.geojson`,
`data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv`,
`data/raw/Property_Info__Current_Calendar_Year_.csv`. A notebook version
(scatters coloured by era, for `notebooks/exploration/`) is deferred.

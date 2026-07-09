# Findings — What drives revenue/value per acre? (ML feature importance)

**Date:** 2026-07-09 (`ANALYSIS_BACKLOG.md` item 2). Reproducible via
`tools/ml_feature_importance.py` (repo root; reads the served
`web/data/neighbourhood_value_per_acre.geojson` for the canonical published
fields, the `data/raw/` roll for account counts + class mix, boundaries for area
+ distance, and property-info `dkk9-cj3x` for built-form medians). Runs in
~10 min on the Oracle box (repeated RF fits + held-out permutation importance).

Random-forest regressions predict a neighbourhood's `revenue_per_acre` and
`value_per_acre` (log10) from its structural characteristics; **held-out
permutation importance** — averaged over 25 repeated train/test splits — is the
headline driver ranking. Set-aside hoods (48) are excluded (off-scale by design,
matching the views); a further 16 are dropped for a missing feature (no
`year_built`/`lot_size` medians, or an all-set-aside developed share leaving `H`
undefined), leaving **342 hoods** in the model. No silent drops — the tool prints
every exclusion.

## Verdict

**Fiscal productivity per acre is overwhelmingly a built-form *density* story, not
a land-use *mix* story.** Two density proxies — road metres per acre and parcels
per acre — carry essentially all the predictive signal. The six land-use
composition fractions and the land-use diversity index are near-zero in held-out
permutation importance. This is the full-multivariate confirmation of item 4's
partial-correlation result (density +0.66 vs diversity +0.27 against revenue/acre):
with everything in one model, **density dominates and diversity all but vanishes.**

The models are genuinely predictive out-of-fold, so the ranking is not noise:

| Target | Feature set | Held-out R² (mean ± sd) |
|---|---|---|
| `revenue_per_acre` | structural (14) | **0.567** ± 0.173 |
| `revenue_per_acre` | + class mix (15) | 0.591 ± 0.166 |
| `value_per_acre` | structural (14) | **0.706** ± 0.123 |
| `value_per_acre` | + class mix (15) | 0.707 ± 0.126 |

Value/acre is more predictable from structure than revenue/acre — revenue adds
mill-rate/class-mix variation on top of the assessment.

## The driver ranking (held-out permutation importance)

**`revenue_per_acre`, structural features:**

| # | Feature | perm. importance | (impurity) |
|---|---|---|---|
| 1 | `road_m_per_acre` | **0.777** | 0.509 |
| 2 | `parcels_per_acre` | **0.124** | 0.110 |
| 3 | `frac_industrial` | 0.061 | 0.047 |
| 4 | `frac_dc` | 0.037 | 0.050 |
| 5 | `frac_residential` | 0.029 | 0.032 |
| … | `age`, `dist_km`, `med_lot` | 0.014–0.017 | |
| — | `H` (diversity), `frac_commercial`, `frac_inst`, `top_acct_share` | ≈ 0 / negative | |

**`value_per_acre`, structural features:** same shape — `road_m_per_acre`
(0.588) and `parcels_per_acre` (0.266) first and second by a wide margin, then
`age` (0.031) and `dist_km` (0.019); every composition frac and `H` are ≈ 0.

Three read-outs:

1. **Density is the driver, in two correlated guises.** `road_m_per_acre` and
   `parcels_per_acre` are both built-form-intensity measures (finely subdivided,
   well-connected land packs more assessed value — and more billable frontage —
   per acre). `road_m_per_acre` is the sharper single proxy and takes most of the
   importance; it is collinear with `frac_residential` (+0.77) and is itself the
   roads-servicing cost metric, so read the two density features as **one
   correlated group** carrying the model, not as two independent effects.
2. **Land-use composition is a minor, not a major, lever.** The only composition
   signals that survive are a modest revenue/acre lift from **industrial** and
   **DC (power-centre)** land — consistent with item 1's finding that the
   top performers are big-box DC and genuine industry. `frac_commercial` and
   `frac_inst` are ≈ 0; the mixed-use fraction is ≈ 0, echoing item 1's rejection
   of a mixed-use split.
3. **Diversity `H` is null once density is controlled.** Its held-out importance
   is 0.002 (revenue) / −0.001 (value) — the diversity–productivity correlation
   item 4 measured is absorbed by density in the joint model.

## Class mix matters for *revenue*, not *value*

Adding the value-weighted **non-residential share** of the roll (`nonres_value_share`):

- **Revenue/acre:** it jumps to the #2 driver (perm. importance 0.218) and lifts
  R² 0.567 → 0.591. Non-residential land bills at a higher mill rate, so its share
  drives *revenue* per acre directly.
- **Value/acre:** it is negligible (0.013) and R² is unchanged. *Assessed value*
  gets no mill-rate multiplier, so the class mix barely moves it.

This clean split is a sanity check that the models are picking up real mechanism,
not artifact. (`nonres_value_share` is derived from the same assessed dollars as
the target, so its importance is *partly* mechanical — reported as a labelled
contrast, kept out of the primary structural model. See caveats.)

## Classification: the tails are highly separable

Top- vs bottom-tercile of `revenue_per_acre` (middle third dropped; 114 vs 114),
RandomForest classifier, held-out **ROC-AUC = 0.967** ± 0.013. Permutation
importance leads with **`parcels_per_acre`** (0.072), then `frac_industrial`,
`frac_dc`, `dist_km`, `road_m_per_acre`. The near-perfect AUC means a hood's
tail membership is almost fully determined by its structure — the quantified
version of item 1's verdict that **the tails are genuine, not artifacts** (and
`top_acct_share`, the thin-denominator concentration signal, has ≈ 0 importance
across every model — one-dominant-parcel spikes are not a general driver).

## Caveats

- **Correlated importance splits.** Permutation importance divides across
  collinear features (flagged pairs: `road_m_per_acre`↔`frac_residential` +0.77,
  `parcels_per_acre`↔`med_lot` −0.70, `age`↔`dist_km` −0.68, `frac_inst`↔`H`
  +0.64), and the six `frac_*` shares are compositional (sum ≈ 1) — dependent by
  construction. The density group's true joint importance is understated by any
  single-feature number; treat the ranking as a grouped signal.
- **`road_m_per_acre` is a near-restatement of density and a cost-side metric.**
  It is a legitimate exogenous built-form feature (street length per acre, not
  derived from assessed dollars), but "roads per acre predicts revenue per acre"
  is a *density correlation*, not a causal claim that roads generate revenue.
- **`nonres_value_share` is semi-mechanical** vs the revenue target (same dollars)
  — hence the separate structural / +class-mix models; the headline drivers come
  from the structural-only model.
- **Neighbourhood n ≈ 342, correlational, one snapshot.** RF R² of 0.57–0.71 is
  solid for cross-sectional municipal data but this is association, not causation,
  on a single assessment year. Permutation importance is held-out (test-fold), so
  it reflects predictive value, not in-sample fit.
- **Zoning is permitted-not-built**, and the composition fractions inherit the
  2024-bylaw coarsening (`FINDINGS_land_use_diversity.md`) — a real reason
  composition may under-perform density here.

## Feeds

- **Item 1 (outlier tails):** quantifies why the tails are genuine (AUC 0.97) and
  ranks the same industrial/DC composition signal item 1 read by hand.
- **Item 4 (land-use diversity):** upgrades the partial-correlation pass to a full
  multivariate model — density dominates, diversity is null in the joint fit.
- **Services lens (`SPEC_services.md`):** that revenue/acre tracks `road_m_per_acre`
  so tightly is the revenue side of the roads cost-vs-revenue story — dense hoods
  pay more *and* carry more road; the per-acre efficiency question is whether the
  revenue lift outpaces the servicing cost (the lens will answer directly).

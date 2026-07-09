"""Machine-learning feature importance (ANALYSIS_BACKLOG item 2): what drives a
neighbourhood's revenue/value per acre?

Fits random-forest regressions to predict `revenue_per_acre` and `value_per_acre`
from each hood's structural characteristics, and extracts a data-driven ranking of
what most explains fiscal performance. Complements item 1 (`audit_outlier_tails.py`
eyeballs the tails) and item 4 (`analyze_land_use_diversity.py` isolates the mix
effect) — this quantifies the drivers across ALL neighbourhoods at once.

Method notes the item pins down:
  * PERMUTATION importance (held-out) is the headline, NOT the impurity-based
    `feature_importances_` (biased toward high-cardinality / continuous features).
    Impurity is printed alongside only as a contrast.
  * Importance + test R^2 are averaged over repeated train/test splits (n~350 is
    small; a single split is noisy). Permutation importance is computed on the
    TEST fold each split, so it reflects held-out predictive value, not fit.
  * Collinearity is reported up front: the zoning composition fractions are
    compositional (sum ~1), so importance splits across correlated features — RF
    tolerates it but the ranking must be read as a correlated-group signal.
  * Two feature sets: a STRUCTURAL model (physical land / built-form / location —
    all exogenous to the assessed dollars), then a contrast that adds the
    assessment-class value mix (semi-mechanical vs the target — see caveats).
  * A top-vs-bottom-tercile CLASSIFICATION variant aligns with item 1's tails.

Set-aside hoods are excluded (off-scale by design, matching the views); every
drop is counted, no silent loss. Canonical per-hood fields are read from the
SERVED GeoJSON so the ranking matches the live map exactly.

Reproduce (repo root, standing pipeline inputs in data/raw/, served GeoJSON in
web/data/):
    .venv/bin/python tools/ml_feature_importance.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, "src")
sys.path.insert(0, "tools")

from load_assessment import load_assessment  # noqa: E402
from load_boundaries import load_boundaries  # noqa: E402
from audit_outlier_tails import location, roll_stats  # noqa: E402  (reused annotators)
from analyze_land_use_diversity import entropy_norm  # noqa: E402  (normalized Shannon)

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor  # noqa: E402
from sklearn.inspection import permutation_importance  # noqa: E402
from sklearn.metrics import roc_auc_score  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402

SERVED = "web/data/neighbourhood_value_per_acre.geojson"
ASSESS = "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
BOUND = "data/raw/neighbourhoods.geojson"
PINFO = "data/raw/Property_Info__Current_Calendar_Year_.csv"

CURRENT_YEAR = 2026
# Developed shares the diversity index is computed over (dc excluded — unknown
# use, not mixed; never/notyet excluded — they make river hoods read as diverse).
DEV = ["frac_residential", "frac_commercial", "frac_industrial", "frac_mixed", "frac_inst"]

# Structural features: physical land composition, built form, and location — all
# exogenous to the assessed dollars we predict.
STRUCTURAL = [
    "frac_residential", "frac_commercial", "frac_industrial",
    "frac_mixed", "frac_dc", "frac_inst",
    "H",                # land-use diversity (normalized Shannon over DEV)
    "parcels_per_acre", "area_acres", "med_lot", "age",
    "road_m_per_acre",  # built-form / grid intensity
    "dist_km",          # distance from the downtown centroid
    "top_acct_share",   # value concentration (one-dominant-parcel signal)
]
# Added only in the contrast model — derived from the same assessed dollars as the
# target, so its importance is partly mechanical (see the FINDINGS caveats).
CLASS_MIX = ["nonres_value_share"]

N_SPLITS = 25          # repeated train/test splits (small n -> average them)
TEST_SIZE = 0.25
N_REPEATS = 10         # permutation repeats per split


def norm(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.upper()


def served_full() -> pd.DataFrame:
    """All published per-hood fields (canonical — matches the live map)."""
    with open(SERVED) as fh:
        gj = json.load(fh)
    return pd.DataFrame([f["properties"] for f in gj["features"]])


def build_matrix() -> pd.DataFrame:
    """Assemble the per-neighbourhood feature matrix + targets. No silent drops:
    the set-aside exclusion and any missing-feature rows are counted by main()."""
    served = served_full()
    served["neighbourhood_name"] = served["neighbourhood_name"].pipe(norm)
    served["H"] = served.apply(lambda r: entropy_norm(r.to_dict(), DEV) or np.nan, axis=1)

    a = load_assessment(ASSESS)
    boundaries = load_boundaries(BOUND)

    # Density / built-form and value-concentration annotators (reuse item 1).
    rs = roll_stats(a)                              # n_accounts, total_value, top_acct_share
    loc = location(boundaries)[["neighbourhood_name", "dist_km"]]
    acres = boundaries[["neighbourhood_name", "area_acres"]]

    # Assessment-class mix: value-weighted Non-Residential share of the roll.
    tot = a.groupby("neighbourhood_name")["assessed_value"].sum()
    nonres = (a[a["tax_class"] == "Non Residential"]
              .groupby("neighbourhood_name")["assessed_value"].sum())
    class_mix = (nonres.reindex(tot.index, fill_value=0.0) / tot).rename("nonres_value_share")

    # Built-form medians from the property-info dataset (dkk9-cj3x).
    pi = pd.read_csv(PINFO, usecols=["Neighbourhood", "year_built", "lot_size"], low_memory=False)
    pi["neighbourhood_name"] = norm(pi["Neighbourhood"])
    pi["year_built"] = pd.to_numeric(pi["year_built"], errors="coerce")
    pi.loc[(pi["year_built"] < 1870) | (pi["year_built"] > CURRENT_YEAR), "year_built"] = np.nan
    pi["lot_size"] = pd.to_numeric(pi["lot_size"], errors="coerce")
    info = pi.groupby("neighbourhood_name").agg(med_year=("year_built", "median"),
                                                med_lot=("lot_size", "median"))

    df = (served
          .merge(acres, on="neighbourhood_name", how="left")
          .merge(rs, on="neighbourhood_name", how="left")
          .merge(loc, on="neighbourhood_name", how="left")
          .merge(class_mix, left_on="neighbourhood_name", right_index=True, how="left")
          .merge(info, on="neighbourhood_name", how="left"))

    df["parcels_per_acre"] = df["n_accounts"] / df["area_acres"]
    df["age"] = CURRENT_YEAR - df["med_year"]
    return df


def _fit_repeated(X: np.ndarray, y: np.ndarray, seeds: range):
    """Repeated train/test RF regression. Returns (test R^2s, held-out permutation
    importances, impurity importances) stacked over splits."""
    r2, perm, imp = [], [], []
    for seed in seeds:
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=TEST_SIZE, random_state=seed)
        rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=2,
                                   random_state=seed, n_jobs=-1)
        rf.fit(Xtr, ytr)
        r2.append(rf.score(Xte, yte))
        pi = permutation_importance(rf, Xte, yte, n_repeats=N_REPEATS,
                                    random_state=seed, n_jobs=-1)
        perm.append(pi.importances_mean)
        imp.append(rf.feature_importances_)
    return np.array(r2), np.array(perm), np.array(imp)


def run_regression(df: pd.DataFrame, target: str, feats: list[str], label: str) -> None:
    X = df[feats].to_numpy(float)
    y = np.log10(df[target].to_numpy(float))     # right-skewed target -> log10
    r2, perm, imp = _fit_repeated(X, y, range(N_SPLITS))

    print("\n" + "=" * 74)
    print(f"{label}: predict log10({target})   n={len(df)}  feats={len(feats)}")
    print("=" * 74)
    print(f"held-out R^2 over {N_SPLITS} splits: "
          f"mean={r2.mean():+.3f}  sd={r2.std():.3f}  "
          f"[{np.percentile(r2, 10):+.3f}, {np.percentile(r2, 90):+.3f}]")

    order = np.argsort(perm.mean(0))[::-1]
    print(f"\n{'feature':<20}{'perm_imp':>12}{'sd':>8}   {'impurity':>10}")
    print("-" * 54)
    for i in order:
        print(f"{feats[i]:<20}{perm.mean(0)[i]:>12.4f}{perm.std(0)[i]:>8.4f}   "
              f"{imp.mean(0)[i]:>10.3f}")
    print("(perm_imp = held-out permutation importance, the headline; impurity = "
          "biased RF default, contrast only)")


def run_classification(df: pd.DataFrame, target: str, feats: list[str]) -> None:
    """Top- vs bottom-tercile of the target (drops the middle) — item 1's tail
    framing, quantified. Reports held-out ROC-AUC + permutation importance."""
    q = df[target].quantile([1 / 3, 2 / 3]).to_numpy()
    lab = pd.Series(np.where(df[target] >= q[1], 1,
                             np.where(df[target] <= q[0], 0, -1)), index=df.index)
    sub = df[lab != -1]
    y = lab[lab != -1].to_numpy()
    X = sub[feats].to_numpy(float)

    aucs, perms = [], []
    for seed in range(N_SPLITS):
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=TEST_SIZE,
                                              random_state=seed, stratify=y)
        clf = RandomForestClassifier(n_estimators=400, min_samples_leaf=2,
                                     random_state=seed, n_jobs=-1)
        clf.fit(Xtr, ytr)
        aucs.append(roc_auc_score(yte, clf.predict_proba(Xte)[:, 1]))
        pi = permutation_importance(clf, Xte, yte, n_repeats=N_REPEATS,
                                    scoring="roc_auc", random_state=seed, n_jobs=-1)
        perms.append(pi.importances_mean)
    aucs, perms = np.array(aucs), np.array(perms)

    print("\n" + "=" * 74)
    print(f"CLASSIFICATION: top vs bottom tercile of {target}   "
          f"n={len(sub)} ({int((y == 1).sum())} top / {int((y == 0).sum())} bottom)")
    print("=" * 74)
    print(f"held-out ROC-AUC over {N_SPLITS} splits: mean={aucs.mean():.3f}  sd={aucs.std():.3f}")
    order = np.argsort(perms.mean(0))[::-1]
    print(f"\n{'feature':<20}{'perm_imp(AUC)':>14}{'sd':>8}")
    print("-" * 42)
    for i in order:
        print(f"{feats[i]:<20}{perms.mean(0)[i]:>14.4f}{perms.std(0)[i]:>8.4f}")


def collinearity(df: pd.DataFrame, feats: list[str]) -> None:
    print("\n" + "=" * 74)
    print("COLLINEARITY — |Spearman| >= 0.60 feature pairs (importance splits across these)")
    print("=" * 74)
    corr = df[feats].corr(method="spearman").to_numpy()
    flagged = False
    for i in range(len(feats)):
        for j in range(i + 1, len(feats)):
            if abs(corr[i, j]) >= 0.60:
                print(f"  {feats[i]:<20} {feats[j]:<20} r={corr[i, j]:+.2f}")
                flagged = True
    if not flagged:
        print("  (none >= 0.60)")
    print("  NB the six frac_* shares are compositional (sum ~1) — dependent by "
          "construction even below 0.60.")


def main() -> None:
    if not Path(SERVED).exists():
        raise SystemExit(f"missing {SERVED} — run the pipeline / refresh first")
    df = build_matrix()

    n_total = len(df)
    n_setaside = int(df["is_set_aside"].astype(bool).sum())
    active = df[~df["is_set_aside"].astype(bool)].copy()

    all_feats = STRUCTURAL + CLASS_MIX
    need = all_feats + ["revenue_per_acre", "value_per_acre"]
    before = len(active)
    model_df = active.dropna(subset=need).copy()
    model_df = model_df[(model_df["revenue_per_acre"] > 0) & (model_df["value_per_acre"] > 0)]
    dropped = active[~active["neighbourhood_name"].isin(model_df["neighbourhood_name"])]

    print("=" * 74)
    print("FEATURE MATRIX")
    print("=" * 74)
    print(f"{n_total} hoods total | {n_setaside} set-aside excluded | "
          f"{before} active | {len(model_df)} complete-case in the model")
    if len(dropped):
        print(f"dropped for missing feature/target ({len(dropped)}): "
              f"{', '.join(sorted(dropped['neighbourhood_name'])[:12])}"
              f"{' …' if len(dropped) > 12 else ''}")
        for col in need:
            miss = dropped[col].isna().sum() if col in dropped else 0
            if miss:
                print(f"    {col}: {miss} missing")

    collinearity(model_df, STRUCTURAL)

    for target in ["revenue_per_acre", "value_per_acre"]:
        run_regression(model_df, target, STRUCTURAL, "STRUCTURAL")
        run_regression(model_df, target, STRUCTURAL + CLASS_MIX, "STRUCTURAL + class-mix")
    run_classification(model_df, "revenue_per_acre", STRUCTURAL)


if __name__ == "__main__":
    main()

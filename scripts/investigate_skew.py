"""
Investigation: colour-transform skew test on the set-aside-excluded taxable set.

Reproduces the numbers in docs/FINDINGS_revenue_scale.md §6. The §3 skew test
originally proved a two-population mixture by trimming the near-zero tail *by
revenue* (circular, diagnostic-only). This script re-runs it the defensible way —
splitting by the independent zoning category (is_set_aside from load_zoning) — to
decide the colour transform.

Reads the exported web GeoJSON (web/data/neighbourhood_value_per_acre.geojson),
which already carries revenue_per_acre / value_per_acre / is_set_aside, so it
reproduces from a committed artifact without re-running the whole pipeline. Run
`python main.py --skip-png` first if the GeoJSON is stale.

Usage:
    python scripts/investigate_skew.py
    # or, in a notebook:
    #   from scripts.investigate_skew import skew_table, load_metrics
    #   skew_table(load_metrics())

Key result (2026-07-01): excluding the 48 set-aside neighbourhoods does NOT yield
a log-normal taxable core — log-skew goes from -2.16 to -4.19 (worse), because the
mixed 0.55-0.90 band (kept on-scale by design) still holds near-zero-revenue hoods.
=> log over-corrects; sqrt is the transform. See FINDINGS §6.

Roads addendum (2026-07-01, services lens): road_m_per_acre is already
near-symmetric RAW (biased skew -0.29 all / -0.43 excl set-aside; the metric is
physically bounded ~0-60 m/acre, max/median 1.84x). sqrt (-0.92) and log (-3.0)
both over-correct. => LINEAR colour for road_m_per_acre. See FINDINGS §6.3.
"""

import json

import numpy as np
import pandas as pd

GEOJSON = "web/data/neighbourhood_value_per_acre.geojson"
METRICS = ["revenue_per_acre", "value_per_acre", "road_m_per_acre"]


def biased_skew(s) -> float:
    """Population (biased) skewness — matches the estimator used in FINDINGS §3.

    NumPy/pandas default differ (pandas .skew() is bias-corrected); the published
    table uses the biased form, so pin it here for exact reproduction.
    """
    s = np.asarray(s, dtype=float)
    m = s.mean()
    sd = s.std(ddof=0)
    return float(((s - m) ** 3).mean() / sd ** 3)


def load_metrics(path: str = GEOJSON) -> pd.DataFrame:
    """Load the per-neighbourhood metrics table from the exported web GeoJSON."""
    with open(path) as fh:
        gj = json.load(fh)
    return pd.DataFrame([f["properties"] for f in gj["features"]])


def _row(label: str, series: pd.Series) -> dict:
    s = series.dropna()
    s = s[s > 0]  # log/sqrt need positive support; drops nothing here (all > 0)
    return {
        "set": label,
        "n": len(s),
        "raw": round(biased_skew(s), 2),
        "sqrt": round(biased_skew(np.sqrt(s)), 2),
        "log": round(biased_skew(np.log(s)), 2),
    }


def skew_table(df: pd.DataFrame) -> pd.DataFrame:
    """Raw / sqrt / log biased-skew for all vs set-aside-excluded, per metric."""
    excl = df.loc[~df["is_set_aside"].astype(bool)]
    rows = []
    for col in METRICS:
        rows.append({"metric": col, **_row("all", df[col])})
        rows.append({"metric": col, **_row("excl set-aside", excl[col])})
    return pd.DataFrame(rows)


def lowest_kept(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """Lowest-revenue neighbourhoods still ON the scale (not set aside).

    These are the mixed 0.55-0.90 band that keeps the taxable distribution mixed.
    """
    excl = df.loc[~df["is_set_aside"].astype(bool)]
    cols = ["neighbourhood_name", "revenue_per_acre", "set_aside_frac"]
    return excl.nsmallest(n, "revenue_per_acre")[cols].reset_index(drop=True)


if __name__ == "__main__":
    df = load_metrics()
    n_set_aside = int(df["is_set_aside"].astype(bool).sum())
    print(f"n = {len(df)} neighbourhoods; {n_set_aside} set aside (is_set_aside)\n")

    print("Biased skewness (matches FINDINGS §3 estimator):")
    print(skew_table(df).to_string(index=False))

    print("\nLowest-revenue hoods still on the scale (mixed 0.55-0.90 band):")
    print(lowest_kept(df).to_string(index=False))

    print(
        "\nReading: log over-corrects on the excluded set (revenue -4.19), so the "
        "taxable core is NOT log-normal at the 0.90 threshold. sqrt stays well-behaved "
        "(revenue 1.55, value 0.21). => sqrt is the colour transform. See FINDINGS §6."
    )

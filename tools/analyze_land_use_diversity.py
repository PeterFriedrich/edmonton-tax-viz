"""Land-use diversity index vs fiscal productivity and servicing burden.

ANALYSIS_BACKLOG.md item 4, first deconfounded pass (2026-07-07). Computes a
per-neighbourhood normalized-Shannon land-use diversity index over developed
zoned-area shares, then tests two relationships in Edmonton's own data:

  1. revenue_per_acre vs diversity   — fiscal productivity
  2. road per dwelling vs diversity  — servicing burden (the one to lean into)

against confounders (built-form age, density, lot size). Reports the raw
correlation matrix, partial correlations (controls regressed out via OLS
residuals), and a stratified high- vs low-diversity comparison within
era x density bands. No silent drops: unmatched / excluded hoods are counted.

Results are documented in docs/FINDINGS_land_use_diversity.md. Run from the
repo root with the standing pipeline inputs in data/raw/ and the served
GeoJSON in web/data/:

    python tools/analyze_land_use_diversity.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, "src")
from load_boundaries import load_boundaries  # noqa: E402
from load_water import build_connections  # noqa: E402

GEO = "web/data/neighbourhood_value_per_acre.geojson"
BOUNDARIES = "data/raw/neighbourhoods.geojson"
ASSESS = "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
PINFO = "data/raw/Property_Info__Current_Calendar_Year_.csv"
DC_USE = "data/dc_use_by_hood.csv"  # tools/rollup_dc_uses.py: frac_dc split by inferred use

# Developed zoned-use shares the entropy is computed over. never/notyet are
# excluded (they make river-valley hoods read as "diverse").
#
# DC (Direct Control) land was previously *unknown* use and high-frac_dc hoods
# were dropped (DC_TRAP). ANALYSIS_BACKLOG item 3 resolved each DC provision's
# use (Purpose-statement classification -> data/dc_use_by_hood.csv), so we now
# FOLD the resolved DC shares into the developed categories and re-admit hoods
# whose DC is mostly resolved. Only the still-unresolved DC share
# (frac_dc_unknown: legacy parcels with no bylaw page + a few unlabelled) stays
# out, and a hood is excluded when that residual is large (UNKNOWN_TRAP).
DEV = ["frac_residential", "frac_commercial", "frac_industrial", "frac_mixed", "frac_inst"]
# (DEV category, resolved-DC column that feeds it).
DC_FOLD = [("frac_residential", "frac_dc_res"), ("frac_commercial", "frac_dc_com"),
           ("frac_industrial", "frac_dc_ind"), ("frac_mixed", "frac_dc_mix"),
           ("frac_inst", "frac_dc_inst")]
UNKNOWN_TRAP = 0.10  # frac_dc_unknown >= this => still low-confidence, excluded
CURRENT_YEAR = 2026


def norm(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.upper()


def entropy_norm(props: dict, cats: list[str]) -> float | None:
    """Normalized Shannon evenness (0..1) over renormalized developed shares."""
    vals = [max(0.0, props.get(c, 0.0) or 0.0) for c in cats]
    tot = sum(vals)
    if tot <= 0:
        return None
    p = [v / tot for v in vals]
    h = -sum(x * math.log(x) for x in p if x > 0)
    return h / math.log(len(cats))


def _resid(y: np.ndarray, controls: np.ndarray) -> np.ndarray:
    x = np.column_stack([np.ones(len(controls)), controls])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    return y - x @ beta


def partial_corr(df: pd.DataFrame, a: str, b: str, ctrl: list[str]) -> float:
    c = np.column_stack([df[k].to_numpy(float) for k in ctrl])
    return float(np.corrcoef(_resid(df[a].to_numpy(float), c),
                             _resid(df[b].to_numpy(float), c))[0, 1])


def build_frame() -> pd.DataFrame:
    # Resolved DC-use shares per hood (fold into the developed categories).
    dcu = pd.read_csv(DC_USE)
    dcu["name"] = norm(dcu["neighbourhood_name"])
    dc_by_name = dcu.set_index("name")

    gj = json.load(open(GEO))
    rows = []
    for f in gj["features"]:
        p = f["properties"]
        if p.get("is_set_aside"):
            continue
        name = p["neighbourhood_name"]
        # Base (pre-resolution) developed shares, DC excluded entirely.
        h_base = entropy_norm(p, DEV)
        # Augmented: fold each hood's resolved DC-use shares into DEV.
        aug = {c: (p.get(c, 0.0) or 0.0) for c in DEV}
        dc_unknown = 0.0
        if name.upper() in dc_by_name.index:
            r = dc_by_name.loc[name.upper()]
            for dev_col, dc_col in DC_FOLD:
                aug[dev_col] += float(r.get(dc_col, 0.0) or 0.0)
            dc_unknown = float(r.get("frac_dc_unknown", 0.0) or 0.0)
        h = entropy_norm(aug, DEV)
        if h is None:
            continue
        rows.append(dict(name=name, H=h, H_base=h_base,
                         rev_acre=p.get("revenue_per_acre"),
                         road_acre=p.get("road_m_per_acre"),
                         dc=p.get("frac_dc", 0.0) or 0.0,
                         dc_unknown=dc_unknown))
    g = pd.DataFrame(rows)
    print(f"developed hoods (GeoJSON, non-set-aside): {len(g)}")
    matched = g["name"].str.upper().isin(dc_by_name.index)
    print(f"  DC-use rollup matched: {int(matched.sum())}/{len(g)} hoods")

    acres = load_boundaries(BOUNDARIES)[["neighbourhood_name", "area_acres"]]

    a = pd.read_csv(ASSESS, usecols=["Neighbourhood", "Assessment Class 1"], low_memory=False)
    a["name"] = norm(a["Neighbourhood"])
    res = a[a["Assessment Class 1"] == "RESIDENTIAL"].groupby("name").size().rename("res_count")

    conns = build_connections(ASSESS, PINFO)
    dwell = conns.groupby("neighbourhood_name")["units"].sum().rename("dwell_bc")
    print(f"build_connections dwelling model: {conns['units'].sum():,.0f} dwellings, {dwell.size} hoods")

    pi = pd.read_csv(PINFO, usecols=["Neighbourhood", "year_built", "lot_size"], low_memory=False)
    pi["name"] = norm(pi["Neighbourhood"])
    pi["year_built"] = pd.to_numeric(pi["year_built"], errors="coerce")
    pi.loc[(pi["year_built"] < 1870) | (pi["year_built"] > CURRENT_YEAR), "year_built"] = np.nan
    pi["lot_size"] = pd.to_numeric(pi["lot_size"], errors="coerce")
    info = pi.groupby("name").agg(med_year=("year_built", "median"), med_lot=("lot_size", "median"))

    df = (g.merge(acres, left_on="name", right_on="neighbourhood_name", how="left")
            .merge(res, on="name", how="left")
            .merge(dwell, left_on="name", right_index=True, how="left")
            .merge(info, on="name", how="left"))

    print(f"  no boundary-acres match: {df['area_acres'].isna().sum()}")
    print(f"  no residential records : {df['res_count'].isna().sum()} (industrial/commercial hoods)")
    print(f"  no median year_built   : {df['med_year'].isna().sum()}")

    df["road_total_m"] = df["road_acre"] * df["area_acres"]
    df["rpd_rec"] = df["road_total_m"] / df["res_count"]      # road per dwelling (record proxy)
    df["rpd_bc"] = df["road_total_m"] / df["dwell_bc"]        # road per dwelling (connection model)
    df["density"] = df["res_count"] / df["area_acres"]
    df["dens_bc"] = df["dwell_bc"] / df["area_acres"]
    df["age"] = CURRENT_YEAR - df["med_year"]
    return df


def main() -> None:
    if not Path(GEO).exists():
        raise SystemExit(f"missing {GEO} — run the pipeline / refresh first")
    df = build_frame()

    need = ["H", "rev_acre", "road_acre", "rpd_rec", "rpd_bc",
            "density", "dens_bc", "age", "med_lot"]
    complete = df.dropna(subset=need)
    complete = complete[np.isfinite(complete["rpd_rec"]) & np.isfinite(complete["rpd_bc"])]

    # New analysis set: fold resolved DC in, exclude only hoods whose UNRESOLVED
    # DC share is large. Replaces the old frac_dc>=0.30 DC_TRAP.
    c = complete[complete["dc_unknown"] < UNKNOWN_TRAP].copy()
    # For comparison: the pre-resolution set (old DC_TRAP) with pre-resolution H.
    old = complete[complete["dc"] < 0.30]
    readmitted = c[c["dc"] >= 0.30]
    newly_excluded = complete[(complete["dc"] < 0.30) & (complete["dc_unknown"] >= UNKNOWN_TRAP)]
    print(f"\nanalysis set (fold resolved DC; excl frac_dc_unknown>={UNKNOWN_TRAP}): n={len(c)}")
    print(f"  pre-resolution set (frac_dc<0.30): n={len(old)}")
    print(f"  re-admitted (was frac_dc>=0.30, DC now resolved): n={len(readmitted)}: "
          f"{', '.join(sorted(readmitted['name']))}")
    print(f"  newly excluded (frac_dc_unknown>={UNKNOWN_TRAP}): n={len(newly_excluded)}: "
          f"{', '.join(sorted(newly_excluded['name']))}")
    print(f"  mean |H - H_base| over set: {(c['H'] - c['H_base']).abs().mean():.3f} "
          f"(DC-fold shifts the index)")
    print(f"H distribution: min={c['H'].min():.2f} median={c['H'].median():.2f} max={c['H'].max():.2f}")

    var = ["H", "rev_acre", "road_acre", "rpd_bc", "dens_bc", "age", "med_lot"]
    m = c[var].to_numpy(float)
    print("\n=== Pearson correlation matrix ===")
    print("            " + "".join(f"{v[:8]:>9s}" for v in var))
    for i, v in enumerate(var):
        print(f"{v[:11]:11s} " + "".join(f"{np.corrcoef(m[:, i], m[:, j])[0, 1]:+9.2f}"
                                         for j in range(len(var))))

    ctrl = ["age", "dens_bc", "med_lot"]
    print(f"\n=== Partial correlations with H, controlling for {ctrl} ===")
    for tgt, lab in [("rev_acre", "revenue / acre"), ("road_acre", "road m / acre"),
                     ("rpd_rec", "road / dwelling (record proxy)"),
                     ("rpd_bc", "road / dwelling (connection model)")]:
        raw = float(np.corrcoef(c["H"], c[tgt])[0, 1])
        par = partial_corr(c, "H", tgt, ctrl)
        print(f"  H vs {lab:34s}  raw r={raw:+.3f}   partial r={par:+.3f}")
    print(f"\n  corr(record proxy, connection model) = {np.corrcoef(c['rpd_rec'], c['rpd_bc'])[0,1]:+.3f}")

    c = c.copy()
    c["era"] = pd.cut(c["med_year"], [0, 1950, 1980, 2100],
                      labels=["pre-1950", "1950-80", "post-1980"])
    c["dens_q"] = pd.qcut(c["dens_bc"], 3, labels=["low", "mid", "high"])
    hi = c["H"] >= c["H"].median()
    print("\n=== Stratified: high-H vs low-H within era x density (medians) ===")
    print(f"{'era':10s}{'dens':6s}{'nHi':>4s}{'nLo':>4s}  "
          f"{'road/dw Hi':>11s}{'Lo':>8s}  {'rev/ac Hi':>11s}{'Lo':>10s}")
    for era in ["pre-1950", "1950-80", "post-1980"]:
        for dq in ["low", "mid", "high"]:
            cell = c[(c["era"] == era) & (c["dens_q"] == dq)]
            ch = cell[hi.reindex(cell.index, fill_value=False)]
            cl = cell[~hi.reindex(cell.index, fill_value=False)]
            if len(ch) < 2 or len(cl) < 2:
                continue
            print(f"{era:10s}{dq:6s}{len(ch):4d}{len(cl):4d}  "
                  f"{ch['rpd_bc'].median():11.1f}{cl['rpd_bc'].median():8.1f}  "
                  f"{ch['rev_acre'].median():11.0f}{cl['rev_acre'].median():10.0f}")


if __name__ == "__main__":
    main()

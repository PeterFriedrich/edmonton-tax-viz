"""Audit (ANALYSIS_BACKLOG item 1): do the performance tails match the land-use
classification?

The observation the item records: several of the highest revenue/acre and
value/acre performers sit out on the city OUTSKIRTS (counterintuitive — you'd
expect the core to dominate), and there's a cluster of WEAK performers inside the
non-residential group. The classification (`load_zoning.py`'s res/com/ind/mix/dc/
inst split) is what's on trial: a top performer in the wrong bucket, or a
systematic weak-performer pattern, would mean the categories need refining.

This is the AUTO half — it surfaces the tails, each row annotated so the by-hand
eyeball (satellite / bylaw spot-check) has a running start:
  * composition   — the served frac_* shares (res/com/ind/mix/dc/inst) + the
                    resolved DC use split (item 3's dc_use_by_hood.csv) so a
                    DC-dominant power centre reads as commercial, not "unknown".
  * dominant zone — the actual dominant base zone code + its bylaw description,
                    overlaid from the zoning GeoJSON (finer than the category).
  * location      — distance of the hood centroid from the DOWNTOWN centroid, and
                    a core / mid / outskirts band — the outskirts-surprise signal.
  * thin-denom    — area_acres, account count, and the single largest account's
                    share of hood value: a tiny hood with one dominant parcel
                    spikes revenue/acre as an artifact, not a real performer.

Set-aside hoods are excluded from the ranked tails (off-scale by design, matching
the colour treatment) but counted. Canonical per-hood fields are read from the
SERVED GeoJSON so the ranking matches the live map exactly.

Value-based + revenue-based tails both shown. Reproduce:
  .venv/bin/python tools/audit_outlier_tails.py
"""
import json
import logging
import sys

import geopandas as gpd
import pandas as pd

sys.path.insert(0, "src")
from load_assessment import load_assessment
from load_boundaries import load_boundaries
from load_zoning import _load_categorized
from export_value_grid import SQ_M_PER_ACRE

logging.basicConfig(level=logging.WARNING)

SERVED = "web/data/neighbourhood_value_per_acre.geojson"
ASSESS = "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
BOUND = "data/raw/neighbourhoods.geojson"
ZONING = "data/raw/zoning.geojson"
DC_USE = "data/dc_use_by_hood.csv"

N = 15  # tail depth
# Distance bands from the downtown centroid (km) — Edmonton is ~30km across.
CORE_KM = 4.0
OUTSKIRTS_KM = 9.0


def served_hoods() -> pd.DataFrame:
    """Canonical published per-hood fields (matches the live map exactly)."""
    with open(SERVED) as fh:
        gj = json.load(fh)
    df = pd.DataFrame([f["properties"] for f in gj["features"]])
    keep = [
        "neighbourhood_name", "revenue_per_acre", "value_per_acre",
        "revenue_per_lot_acre", "value_per_lot_acre", "parcel_frac",
        "is_set_aside", "is_residential", "set_aside_frac",
        "frac_residential", "frac_commercial", "frac_industrial",
        "frac_mixed", "frac_dc", "frac_inst",
    ]
    return df[keep]


def dominant_zone(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Per-hood dominant base zone code + bylaw description, by overlaid area.

    Uses the base zone code (first `zoning` token) directly — finer than the
    collapsed category — so 'the wrong bucket' is legible at the code level."""
    zoning = _load_categorized(ZONING)  # cleaned geometry, EPSG:3400
    zoning["code"] = zoning["zoning"].fillna("").str.split().str[0]
    # One representative description per code (modal, for the annotation).
    desc = (
        zoning.dropna(subset=["description"])
        .groupby("code")["description"]
        .agg(lambda s: s.mode().iat[0] if not s.mode().empty else s.iat[0])
    )

    if boundaries.crs is None or boundaries.crs.to_epsg() != 3400:
        raise ValueError(f"boundaries must be EPSG:3400 (got {boundaries.crs})")
    overlay = gpd.overlay(
        boundaries[["neighbourhood_name", "geometry"]],
        zoning[["code", "category", "geometry"]],
        how="intersection", keep_geom_type=True,
    )
    overlay["acres"] = overlay.geometry.area / SQ_M_PER_ACRE
    by = overlay.groupby(["neighbourhood_name", "code", "category"])["acres"].sum().reset_index()
    idx = by.groupby("neighbourhood_name")["acres"].idxmax()
    dom = by.loc[idx, ["neighbourhood_name", "code", "category"]].rename(
        columns={"code": "dom_code", "category": "dom_category"}
    )
    dom["dom_desc"] = dom["dom_code"].map(desc).fillna("")
    return dom.reset_index(drop=True)


def roll_stats(a: pd.DataFrame) -> pd.DataFrame:
    """Per-hood account count, total value, and the single largest account's
    share of hood value (the one-dominant-parcel artifact signal)."""
    g = a.groupby("neighbourhood_name")["assessed_value"]
    return pd.DataFrame({
        "n_accounts": g.size(),
        "total_value": g.sum(),
        "top_acct_share": g.max() / g.sum(),
    }).reset_index()


def location(boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Distance (km) of each hood centroid from the DOWNTOWN hood centroid."""
    cent = boundaries[["neighbourhood_name"]].copy()
    cent["geometry"] = boundaries.geometry.centroid  # EPSG:3400 metres
    cent = gpd.GeoDataFrame(cent, crs="EPSG:3400")
    dt = cent.loc[cent["neighbourhood_name"] == "DOWNTOWN", "geometry"]
    if dt.empty:
        raise ValueError("no DOWNTOWN hood to anchor the distance signal")
    origin = dt.iloc[0]
    cent["dist_km"] = cent.geometry.distance(origin) / 1000.0
    cent["band"] = pd.cut(
        cent["dist_km"], [-1, CORE_KM, OUTSKIRTS_KM, 1e9],
        labels=["core", "mid", "outskirts"],
    )
    return cent[["neighbourhood_name", "dist_km", "band"]]


def comp(r) -> str:
    """One-line composition tag: dominant served category fracs, >=15%."""
    parts = {
        "res": r.frac_residential, "com": r.frac_commercial,
        "ind": r.frac_industrial, "mix": r.frac_mixed,
        "dc": r.frac_dc, "inst": r.frac_inst,
    }
    top = sorted((v, k) for k, v in parts.items() if v >= 0.15)
    return " ".join(f"{k}{int(v*100)}" for v, k in reversed(top)) or "-"


def _print_tail(title: str, rows: pd.DataFrame, metric: str) -> None:
    print("\n" + "=" * 118)
    print(title)
    print("=" * 118)
    print(f'{"hood":<26}{metric[:11]:>12}{"parc%":>6}{"dist":>6}{"band":>10}'
          f'{"acres":>7}{"accts":>7}{"top%":>6}  {"domZone":<9}composition')
    for _, r in rows.iterrows():
        val = r[metric]
        vs = f"{val/1e6:>11.2f}M" if "value" in metric else f"{val:>12,.0f}"
        print(f'{r.neighbourhood_name[:25]:<26}{vs}{r.parcel_frac*100:>6.0f}'
              f'{r.dist_km:>6.1f}{str(r.band):>10}{r.area_acres:>7.0f}'
              f'{int(r.n_accounts):>7}{r.top_acct_share*100:>6.0f}  '
              f'{r.dom_code:<9}{r.composition}')


def main() -> None:
    served = served_hoods()
    a = load_assessment(ASSESS)
    boundaries = load_boundaries(BOUND)

    df = (
        served
        .merge(boundaries[["neighbourhood_name", "area_acres"]], on="neighbourhood_name", how="left")
        .merge(dominant_zone(boundaries), on="neighbourhood_name", how="left")
        .merge(roll_stats(a), on="neighbourhood_name", how="left")
        .merge(location(boundaries), on="neighbourhood_name", how="left")
        .merge(pd.read_csv(DC_USE).drop(columns=["frac_dc"]), on="neighbourhood_name", how="left")
    )
    df["composition"] = df.apply(comp, axis=1)
    df["dom_code"] = df["dom_code"].fillna("-")

    # Fiscal comparison excludes set-aside hoods (off-scale by design).
    active = df[~df["is_set_aside"].astype(bool)].copy()
    n_setaside = int(df["is_set_aside"].astype(bool).sum())
    ranked = active[active["revenue_per_acre"].notna()]

    print(f"{len(df)} hoods total | {n_setaside} set-aside excluded | "
          f"{len(ranked)} in the ranked comparison")
    print(f"downtown-anchored bands: core <{CORE_KM:g}km, outskirts >{OUTSKIRTS_KM:g}km")

    for metric, label in [("revenue_per_acre", "REVENUE/ACRE"),
                          ("value_per_acre", "VALUE/ACRE")]:
        srt = ranked.sort_values(metric, ascending=False)
        _print_tail(f"TOP {N} by {label}  (are the leaders in the expected bucket / location?)",
                    srt.head(N), metric)
        _print_tail(f"BOTTOM {N} by {label}  (weak performers — esp. inside non-residential)",
                    srt.tail(N).iloc[::-1], metric)

    # --- the item's explicit flags ------------------------------------------------
    print("\n" + "=" * 118)
    print("OUTSKIRTS HIGH PERFORMERS — top-quartile revenue/acre sitting >{:g}km out"
          .format(OUTSKIRTS_KM))
    print("(the item's central surprise: genuine annexed industrial/logistics, or thin-denom artifact?)")
    print("=" * 118)
    q75 = ranked["revenue_per_acre"].quantile(0.75)
    out = ranked[(ranked["dist_km"] > OUTSKIRTS_KM) & (ranked["revenue_per_acre"] >= q75)]
    for _, r in out.sort_values("revenue_per_acre", ascending=False).iterrows():
        print(f'{r.neighbourhood_name[:25]:<26} rev/ac {r.revenue_per_acre:>10,.0f}  '
              f'{r.dist_km:>4.1f}km  {r.area_acres:>6.0f}ac  {int(r.n_accounts):>5} accts  '
              f'top {r.top_acct_share*100:>3.0f}%  {r.dom_code:<8}{r.composition}')

    print("\n" + "=" * 118)
    print("MIXED-USE / DC-DOMINANT SUSPECTS — frac_mixed>0 or DC-dominant (power centres)")
    print("(item: prime suspects for the outskirts surprise; DC use split resolves what DC actually is)")
    print("=" * 118)
    susp = ranked[(ranked["frac_mixed"] > 0) | (ranked["frac_dc"] >= 0.15)].copy()
    susp = susp.sort_values("revenue_per_acre", ascending=False)
    for _, r in susp.head(20).iterrows():
        dc = ""
        if r.frac_dc >= 0.15 and pd.notna(r.get("frac_dc_com")):
            dc = (f"  DC->[com{int(r.frac_dc_com*100)} res{int(r.frac_dc_res*100)} "
                  f"ind{int(r.frac_dc_ind*100)} mix{int(r.frac_dc_mix*100)} "
                  f"unk{int(r.frac_dc_unknown*100)}]")
        print(f'{r.neighbourhood_name[:25]:<26} rev/ac {r.revenue_per_acre:>10,.0f}  '
              f'{str(r.band):>9}  mix{int(r.frac_mixed*100)} dc{int(r.frac_dc*100)}  '
              f'{r.dom_code:<8}{r.composition}{dc}')

    print("\n" + "=" * 118)
    print("THIN-DENOMINATOR ARTIFACTS — small hoods where ONE account dominates value")
    print("(a single large parcel in a small hood spikes revenue/acre; not a real 'performer')")
    print("=" * 118)
    thin = ranked[(ranked["top_acct_share"] >= 0.5) & (ranked["n_accounts"] <= 50)]
    for _, r in thin.sort_values("revenue_per_acre", ascending=False).iterrows():
        print(f'{r.neighbourhood_name[:25]:<26} rev/ac {r.revenue_per_acre:>10,.0f}  '
              f'{r.area_acres:>6.0f}ac  {int(r.n_accounts):>4} accts  '
              f'top acct {r.top_acct_share*100:>3.0f}%  {r.dom_code:<8}{r.composition}')


if __name__ == "__main__":
    main()

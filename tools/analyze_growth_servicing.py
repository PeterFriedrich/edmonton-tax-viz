"""Growth servicing cost recovery — growth areas vs mature neighbourhoods.

ANALYSIS_BACKLOG.md item 5 (auto half), 2026-07-10. The development-industry
framing (BILD Edmonton Metro, Heritage Valley + Windermere case study) is that
growth is fiscally net-positive: developers fund upfront capital, the area
contributes large property-tax revenue at build-out. The counter-consideration
is the long-tail liability the City/EPCOR inherit once assets transfer
(lifecycle renewal + O&M). This script computes what Edmonton's own data can
say about either side, at the neighbourhood scale:

  1. Era bands (median year_built) x the fiscal + servicing columns we
     publish: levy, road supply, modeled storm/water charges, fire demand —
     per acre AND per dwelling.
  2. Build-out sensitivity: growth hoods mid-build carry roads ahead of
     dwellings, so the post-2010 band is split by remaining undeveloped share.
  3. Named-area ledgers: Heritage Valley + Windermere (the BILD study area)
     and the three IIMP greenfield areas (Decoteau / Horse Hill / Riverview)
     as current totals.

Neutral-tone rule: this surfaces data and attributes claims; verdict language
belongs nowhere in the output. Results are documented in
docs/FINDINGS_growth_servicing.md. Run from the repo root:

    python tools/analyze_growth_servicing.py

No silent drops: set-aside, unmatched, and low-count hoods are counted when
excluded.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "src")
from load_boundaries import load_boundaries  # noqa: E402
from load_water import build_connections  # noqa: E402

GEO = "web/data/neighbourhood_value_per_acre.geojson"
BOUNDARIES = "data/raw/neighbourhoods.geojson"
ASSESS = "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
PINFO = "data/raw/Property_Info__Current_Calendar_Year_.csv"

CURRENT_YEAR = 2026
# Per-dwelling stats are only meaningful where dwellings exist in number;
# hoods under this residential-record count are excluded from per-dwelling
# medians (counted, not silent).
MIN_RES_RECORDS = 100

# Era bands over the hood's median year_built. NOTE: this is median BUILDING
# STOCK age, not plat date — infill pulls mature hoods' medians later, so a
# pre-1950 band holds only 2 hoods; pre-1970 is the finest useful "mature
# grid" band.
ERA_EDGES = [1800, 1970, 1990, 2010, CURRENT_YEAR + 1]
ERA_LABELS = ["pre-1970", "1970-89", "1990-2009", "2010+"]

# Named planning areas, compiled from ASP neighbourhood lists (best-effort —
# memberships should be re-verified against the ASP documents themselves;
# edmonton.ca is unreachable from this box). River-valley / ravine hoods
# (BLACKMUD CREEK RAVINE, RIVER VALLEY KESWICK/WINDERMERE) are deliberately
# absent: parkland, not the serviced study area.
AREAS = {
    "Heritage Valley": [
        "ALLARD", "BLACKMUD CREEK", "CALLAGHAN", "CASHMAN", "CAVANAGH",
        "CHAPPELLE", "DESROCHERS AREA", "GRAYDON HILL", "HAYS RIDGE AREA",
        "HERITAGE VALLEY AREA", "HERITAGE VALLEY TOWN CENTRE", "MACEWAN",
        "PAISLEY", "RICHFORD", "RUTHERFORD",
    ],
    "Windermere": [
        "AMBLESIDE", "GLENRIDDING HEIGHTS", "GLENRIDDING RAVINE", "KESWICK",
        "WINDERMERE",
    ],
    "Decoteau (IIMP)": ["DECOTEAU", "ASTER"],
    "Horse Hill (IIMP)": ["MARQUIS", "GORMAN", "RURAL NORTH EAST HORSE HILL"],
    "Riverview (IIMP)": [
        "RIVERVIEW AREA", "RIVER'S EDGE", "THE UPLANDS", "STILLWATER",
    ],
}


def norm(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.upper()


def build_frame() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (kept frame for era stats, full frame incl. set-aside for area totals)."""
    gj = json.load(open(GEO))
    rows = []
    for f in gj["features"]:
        p = f["properties"]
        rows.append(dict(
            name=p["neighbourhood_name"],
            set_aside=bool(p.get("is_set_aside")),
            set_aside_reason=p.get("set_aside_reason") or "",
            rev_acre=p.get("revenue_per_acre"),
            road_acre=p.get("road_m_per_acre"),
            storm_acre=p.get("storm_charge_per_acre"),
            water_acre=(p.get("water_charge_per_acre") or 0.0)
                       + (p.get("water_fixed_per_acre") or 0.0),
            fire_acre=p.get("fire_events_per_acre"),
            frac_notyet=p.get("frac_notyet", 0.0) or 0.0,
            frac_never=p.get("frac_never", 0.0) or 0.0,
            frac_res=p.get("frac_residential", 0.0) or 0.0,
        ))
    g = pd.DataFrame(rows)
    print(f"hoods in served GeoJSON: {len(g)} "
          f"(set-aside: {int(g['set_aside'].sum())})")

    acres = load_boundaries(BOUNDARIES)[["neighbourhood_name", "area_acres"]]
    acres["name"] = norm(acres["neighbourhood_name"])
    g["key"] = norm(g["name"])
    g = g.merge(acres[["name", "area_acres"]], left_on="key", right_on="name",
                how="left", suffixes=("", "_b"))
    print(f"  boundary-acres matched: {int(g['area_acres'].notna().sum())}/{len(g)}")

    a = pd.read_csv(ASSESS, usecols=["Neighbourhood", "Assessment Class 1"],
                    low_memory=False)
    a["name"] = norm(a["Neighbourhood"])
    res = (a[a["Assessment Class 1"] == "RESIDENTIAL"]
           .groupby("name").size().rename("res_count"))

    conns = build_connections(ASSESS, PINFO)
    dwell = conns.groupby("neighbourhood_name")["units"].sum().rename("dwell_bc")
    print(f"build_connections dwelling model: {conns['units'].sum():,.0f} dwellings")

    pi = pd.read_csv(PINFO, usecols=["Neighbourhood", "year_built"],
                     low_memory=False)
    pi["name"] = norm(pi["Neighbourhood"])
    pi["year_built"] = pd.to_numeric(pi["year_built"], errors="coerce")
    pi.loc[(pi["year_built"] < 1870) | (pi["year_built"] > CURRENT_YEAR),
           "year_built"] = np.nan
    med_year = pi.groupby("name")["year_built"].median().rename("med_year")

    g = (g.set_index("key")
          .join(res).join(dwell).join(med_year)
          .reset_index(drop=True))
    g["res_count"] = g["res_count"].fillna(0).astype(int)

    # Totals (levy etc. were published per boundary acre; multiply back).
    for col, tot in [("rev_acre", "levy_total"), ("road_acre", "road_total_m"),
                     ("storm_acre", "storm_total"), ("water_acre", "water_total"),
                     ("fire_acre", "fire_total")]:
        g[tot] = g[col] * g["area_acres"]

    # Per-dwelling metrics on both dwelling models (record proxy + connection
    # model — FINDINGS_land_use_diversity showed conclusions should be robust
    # to both).
    for d in ["res_count", "dwell_bc"]:
        sfx = "_rec" if d == "res_count" else "_bc"
        g["levy_dw" + sfx] = g["levy_total"] / g[d]
        g["road_dw" + sfx] = g["road_total_m"] / g[d]
        g["storm_dw" + sfx] = g["storm_total"] / g[d]
        g["fire_kdw" + sfx] = 1000 * g["fire_total"] / g[d]

    g["developed_frac"] = 1.0 - g["frac_never"] - g["frac_notyet"]
    g["era"] = pd.cut(g["med_year"], bins=ERA_EDGES, labels=ERA_LABELS,
                      right=False)

    kept = g[~g["set_aside"]].copy()
    print(f"kept for era stats (non-set-aside): {len(kept)}; "
          f"no median year_built: {int(kept['med_year'].isna().sum())}")
    return kept, g


def med_table(df: pd.DataFrame, cols: list[tuple[str, str, str]],
              title: str) -> None:
    print(f"\n=== {title} ===")
    hdr = f"{'era':>10}{'n':>5}" + "".join(f"{lbl:>{w}}" for _, lbl, w in
                                           [(c, l, int(w)) for c, l, w in cols])
    print(hdr)
    for era in ERA_LABELS:
        c = df[df["era"] == era]
        if not len(c):
            continue
        line = f"{era:>10}{len(c):>5}"
        for col, _lbl, w in cols:
            v = c[col].median()
            line += f"{v:>{int(w)},.0f}" if abs(v) >= 10 else f"{v:>{int(w)}.2f}"
        print(line)


def area_ledger(full: pd.DataFrame) -> None:
    print("\n=== Named-area ledgers (current totals; incl. set-aside members, flagged) ===")
    idx = full.set_index(norm(full["name"]))
    for area, members in AREAS.items():
        missing = [m for m in members if m not in idx.index]
        sub = idx.loc[[m for m in members if m in idx.index]]
        sa = sub[sub["set_aside"]]
        print(f"\n{area}: {len(sub)} hoods"
              + (f"  [MISSING from data: {missing}]" if missing else "")
              + (f"  [set-aside members: {list(sa.index)}]" if len(sa) else ""))
        acres = sub["area_acres"].sum()
        print(f"  area           : {acres:>12,.0f} acres")
        print(f"  municipal levy : ${sub['levy_total'].sum():>12,.0f} /yr")
        print(f"  dwellings      : {sub['res_count'].sum():>12,.0f} (record proxy)"
              f"   {sub['dwell_bc'].sum():>10,.0f} (connection model)")
        print(f"  road           : {sub['road_total_m'].sum():>12,.0f} m"
              f"   ({sub['road_total_m'].sum() / max(sub['dwell_bc'].sum(), 1):.1f} m/dwelling)")
        print(f"  modeled storm  : ${sub['storm_total'].sum():>12,.0f} /yr (EPCOR-billed)")
        print(f"  modeled water  : ${sub['water_total'].sum():>12,.0f} /yr (EPCOR-billed)")
        print(f"  fire events    : {sub['fire_total'].sum():>12,.1f} /yr")
        print(f"  undeveloped    : {(sub['frac_notyet'] * sub['area_acres']).sum() / max(acres, 1):>12.0%} of zoned land still 'not yet developed'")


def main() -> None:
    kept, full = build_frame()

    era = kept[kept["era"].notna()].copy()
    print(f"\nera-banded hoods: {len(era)} "
          f"(dropped for missing year_built: {len(kept) - len(era)})")

    med_table(era, [
        ("rev_acre", "levy$/ac", 10), ("road_acre", "road m/ac", 11),
        ("storm_acre", "storm$/ac", 11), ("water_acre", "water$/ac", 11),
        ("fire_acre", "fire/ac", 9), ("developed_frac", "dev frac", 10),
    ], "Per-ACRE medians by era band (all kept hoods)")

    dw = era[era["res_count"] >= MIN_RES_RECORDS].copy()
    print(f"\nper-dwelling subset: res_count >= {MIN_RES_RECORDS} -> {len(dw)} hoods "
          f"(excluded: {len(era) - len(dw)})")
    med_table(dw, [
        ("levy_dw_rec", "levy$/dw", 10), ("levy_dw_bc", "(bc)", 9),
        ("road_dw_rec", "road m/dw", 11), ("road_dw_bc", "(bc)", 9),
        ("storm_dw_rec", "storm$/dw", 11), ("fire_kdw_rec", "fire/kdw", 10),
    ], "Per-DWELLING medians by era band (record proxy + connection model)")

    # Build-out sensitivity: mid-build hoods carry roads (built first) ahead
    # of dwellings; split the growth band by remaining undeveloped share.
    g10 = dw[dw["era"] == "2010+"]
    for lbl, c in [("2010+ near-built-out (notyet < 0.10)", g10[g10["frac_notyet"] < 0.10]),
                   ("2010+ mid-build     (notyet >= 0.10)", g10[g10["frac_notyet"] >= 0.10])]:
        if len(c):
            print(f"\n{lbl}: n={len(c)}  road m/dw (rec) median="
                  f"{c['road_dw_rec'].median():.1f}  levy $/dw median="
                  f"{c['levy_dw_rec'].median():,.0f}  levy $/ac median="
                  f"{c['rev_acre'].median():,.0f}")

    # Levy per DEVELOPED acre — growth hoods' low levy/acre is partly just
    # unfinished land; renormalizing by developed share is the fair check.
    era_dev = era[era["developed_frac"] > 0.2].copy()
    era_dev["rev_dev_acre"] = era_dev["rev_acre"] / era_dev["developed_frac"]
    med_table(era_dev, [
        ("rev_acre", "levy$/ac", 10), ("rev_dev_acre", "levy$/devac", 13),
    ], "Levy per developed acre (developed_frac > 0.2)")

    # Simple age gradients for the doc.
    ok = dw.dropna(subset=["med_year", "road_dw_rec", "road_dw_bc"])
    r_rec = np.corrcoef(ok["med_year"], ok["road_dw_rec"])[0, 1]
    r_bc = np.corrcoef(ok["med_year"], ok["road_dw_bc"])[0, 1]
    print(f"\nr(median year_built, road m/dwelling): record proxy {r_rec:+.2f}, "
          f"connection model {r_bc:+.2f}  (n={len(ok)})")

    area_ledger(full)


if __name__ == "__main__":
    main()

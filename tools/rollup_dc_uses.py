#!/usr/bin/env python3
"""Roll the inferred DC land-uses up to neighbourhoods (ANALYSIS_BACKLOG item 3, step 5).

Splits each neighbourhood's authoritative ``frac_dc`` (Direct Control share of
total zoned area) into per-use sub-shares ``frac_dc_res / _com / _ind / _mix /
_inst / _unknown``, area-weighted, using the SAME overlay + denominator as
``src/load_zoning.load_zoning`` — so the sub-shares sum exactly to ``frac_dc``
and are directly comparable to ``frac_residential`` etc.

Method: reuse ``load_zoning._load_categorized`` (identical code→category dict,
CRS, geometry cleaning) and ``load_boundaries``; relabel each ``dc`` polygon's
category to ``dc_<use>`` via its ``url`` → slug → ``data/dc_inferred_use.csv``
label; overlay against neighbourhood boundaries; piece-area fractions of total
zoned area per hood. DC polygons whose slug has no label (the 20 failed
fetches — access-denied nodes + one bad URL) roll up to ``dc_unknown`` and are
counted, never silently dropped (CLAUDE.md).

The split is kept SEPARATE from the authoritative ``frac_dc`` — never folded
in. Re-admission into the diversity index (step 6) is a downstream decision.

    python tools/rollup_dc_uses.py    # -> data/dc_use_by_hood.csv
"""
import csv
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from load_boundaries import load_boundaries          # noqa: E402
from load_zoning import _load_categorized            # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("rollup_dc_uses")

ROOT = Path(__file__).resolve().parent.parent
ZONING = ROOT / "data" / "raw" / "zoning.geojson"
BOUNDARIES = ROOT / "data" / "raw" / "neighbourhoods.geojson"
WEB_GEO = ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson"
LABELS = ROOT / "data" / "dc_inferred_use.csv"
OUT = ROOT / "data" / "dc_use_by_hood.csv"

USES = ("res", "com", "ind", "mix", "inst", "unknown")
DC_COLS = [f"frac_dc_{u}" for u in USES]


def _slug(url):
    return urlparse(url).path.rstrip("/").split("/")[-1] if isinstance(url, str) and url else None


def main():
    labels = {r["slug"]: r["use"] for r in csv.DictReader(open(LABELS))}

    zoning = _load_categorized(str(ZONING))          # EPSG:3400, category, all cols
    is_dc = zoning["category"] == "dc"
    slugs = zoning.loc[is_dc, "url"].map(_slug)
    uses = slugs.map(labels).fillna("unknown")       # unlabeled DC polygons -> unknown
    n_unlabeled = int((slugs.map(labels).isna() & is_dc).sum())
    if n_unlabeled:
        missing = sorted(set(slugs[slugs.map(labels).isna()].dropna()))
        logger.warning("%d DC polygons have no use label -> dc_unknown: %s",
                       n_unlabeled, missing)

    # Subcategory: dc polygons become dc_<use>; everything else keeps its category.
    zoning["subcat"] = zoning["category"]
    zoning.loc[is_dc, "subcat"] = "dc_" + uses

    boundaries = load_boundaries(str(BOUNDARIES))     # EPSG:3400
    overlay = gpd.overlay(
        boundaries[["neighbourhood_name", "geometry"]],
        zoning[["subcat", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )
    overlay["piece_area"] = overlay.geometry.area

    by = (overlay.groupby(["neighbourhood_name", "subcat"])["piece_area"]
          .sum().unstack(fill_value=0.0))
    totals = by.sum(axis=1)                           # total zoned area per hood
    fracs = by.div(totals, axis=0)

    out = pd.DataFrame(index=fracs.index)
    for u in USES:
        col = f"dc_{u}"
        out[f"frac_dc_{u}"] = fracs[col] if col in fracs.columns else 0.0
    out["frac_dc"] = out[DC_COLS].sum(axis=1)         # reconstructed; == pipeline frac_dc
    out = out.reset_index()

    # Sanity: reconstructed frac_dc must match the served pipeline value.
    import json
    web = json.load(open(WEB_GEO))
    web_dc = {f["properties"]["neighbourhood_name"]: (f["properties"].get("frac_dc") or 0.0)
              for f in web["features"]}
    out["_web_frac_dc"] = out["neighbourhood_name"].map(web_dc)
    cmp = out.dropna(subset=["_web_frac_dc"])
    diff = (cmp["frac_dc"] - cmp["_web_frac_dc"]).abs()
    logger.info("frac_dc reconstruction vs served: max|Δ|=%.4f mean|Δ|=%.5f over %d hoods",
                diff.max(), diff.mean(), len(cmp))
    worst = cmp.loc[diff.sort_values(ascending=False).index[:5]]
    for _, r in worst.iterrows():
        logger.info("   %-28s recon=%.3f served=%.3f", r["neighbourhood_name"],
                    r["frac_dc"], r["_web_frac_dc"])

    out = out.drop(columns=["_web_frac_dc"])
    out = out[["neighbourhood_name", "frac_dc"] + DC_COLS].sort_values("frac_dc", ascending=False)
    out.to_csv(OUT, index=False)
    logger.info("Wrote %d hoods -> %s", len(out), OUT.relative_to(ROOT))

    resolved = out[["frac_dc_res", "frac_dc_com", "frac_dc_ind", "frac_dc_mix",
                    "frac_dc_inst"]].sum().sum()
    unk = out["frac_dc_unknown"].sum()
    logger.info("Citywide DC frac mass: resolved=%.2f unknown=%.2f (%.0f%% resolved)",
                resolved, unk, 100 * resolved / (resolved + unk) if resolved + unk else 0)


if __name__ == "__main__":
    main()

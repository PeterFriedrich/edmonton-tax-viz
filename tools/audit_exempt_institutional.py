"""Audit (ANALYSIS_BACKLOG item 7): where does tax-exempt institutional land
dilute the neighbourhood revenue/value lens hardest?

Generalizes the University of Alberta hand-case (FINDINGS_denominator_cardinality.md):
U of A carries $2.242B taxable value on ~half its polygon, the other half being
institutional land that carries no taxable account.

⚠️ This docstring used to say that exempt land is "ABSENT from the taxable roll
entirely (DATA.md 2026-06-29)". That claim is RETRACTED — hospitals and the U of A
campus ARE on the roll; $5.6B of assessed value sits on UI/UF/AJ/PU zoning (see
DATA.md "Tax-exempt flag", corrected 2026-08-07). ⚠️ **The measurement below is
unaffected and its outputs are unchanged** (re-run 2026-08-07, every figure in
FINDINGS_exempt_institutional.md reproduced exactly) — because it MEASURES the
taxable footprint rather than assuming there is none, land that is taxed gets
counted as taxed. Do not "fix" the method on account of the retraction.

No exempt boolean exists, so we MEASURE exempt-institutional land as institutional-
proxy zoning that carries NO taxable account:

  1. Institutional zoning  — base zone codes UI/UF/AJ/PU (Urban Institution /
     Urban Facilities / Alternative Jurisdiction / Public Utility, DATA.md
     line ~308), overlaid on boundaries for institutional ACRES BY CODE per hood.
     The code split names the mechanism the item says NOT to conflate:
        UI -> university / school / hospital     AJ -> federal / provincial land
        PU -> utility / infrastructure corridor  UF -> civic urban facilities
  2. Taxable footprint ON that land — spatial-join the deduped taxable lot
     footprint (the shipped SHARE_MAX_M2 dedupe, _point_lot_stats) onto the
     institutional polygons. Institutional acres MINUS the taxable footprint
     sitting on them  =  exempt_inst_acres  (the honest exempt measure).

This separation is what distinguishes the three mechanisms the item flags:
  * EXEMPT-DILUTION (U of A): large institutional zoning, almost none taxed
    -> big exempt_inst_acres; the lot-acre toggle gives an honest lift AND the
    services lens carries the free-riding cost.
  * low-value institutional ON the roll (U of A Farm): institutional land that
    IS taxed (as cheap farmland) -> small exempt_inst_acres.
  * park / river-valley (McCauley, Virginia Park): off-roll land that is NOT
    institutional -> small exempt_inst_acres even though the lot-acre boost is
    large (that boost is item 1 / the lot-acre findings' territory, not this).

Canonical per-hood published fields (value_per_acre, parcel_frac, ...) are read
from the SERVED GeoJSON so the ranking matches the live map exactly; the roll +
zoning supply the exempt-acre measure and absolute figures.

Value-based (no mill rates) — exemptions distort the value roll and the levy roll
identically. Reproduce:  .venv/bin/python tools/audit_exempt_institutional.py
"""
import json
import logging
import sys

import geopandas as gpd
import pandas as pd

sys.path.insert(0, "src")
from load_assessment import load_assessment
from load_boundaries import load_boundaries
from load_property_info import load_property_info
from load_zoning import _load_categorized
from export_value_grid import _point_lot_stats, build_hood_lot_acres, SQ_M_PER_ACRE

logging.basicConfig(level=logging.WARNING)

SERVED = "web/data/neighbourhood_value_per_acre.geojson"
ASSESS = "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
PINFO = "data/raw/Property_Info__Current_Calendar_Year_.csv"
BOUND = "data/raw/neighbourhoods.geojson"
ZONING = "data/raw/zoning.geojson"

# Institutional-proxy base zone codes (DATA.md line ~308) + on-the-ground meaning.
INST_CODES = {
    "UI": "university / school / hospital",
    "AJ": "federal / provincial jurisdiction",
    "PU": "public utility / infrastructure",
    "UF": "urban civic facilities",
}
# Minimum exempt-institutional share of polygon to be called an exempt hood.
EXEMPT_FRAC_MIN = 0.10


def served_hoods() -> pd.DataFrame:
    """Canonical published per-hood fields (matches the live map exactly)."""
    with open(SERVED) as fh:
        gj = json.load(fh)
    df = pd.DataFrame([f["properties"] for f in gj["features"]])
    return df[[
        "neighbourhood_name", "value_per_acre", "value_per_lot_acre",
        "parcel_frac", "frac_inst", "set_aside_frac", "is_set_aside",
    ]]


def institutional_zoning(boundaries: gpd.GeoDataFrame):
    """Return (per-hood inst acres by code, dissolved inst polygons) in EPSG:3400.

    Uses the base zone code (first `zoning` token) directly rather than the
    collapsed `inst` category, so the dominant-code mechanism label survives."""
    zoning = _load_categorized(ZONING)  # cleaned geometry, EPSG:3400
    zoning["code"] = zoning["zoning"].fillna("").str.split().str[0]
    inst = zoning[zoning["code"].isin(INST_CODES)][["code", "geometry"]].copy()

    if boundaries.crs is None or boundaries.crs.to_epsg() != 3400:
        raise ValueError(f"boundaries must be EPSG:3400 (got {boundaries.crs})")

    overlay = gpd.overlay(
        boundaries[["neighbourhood_name", "geometry"]], inst,
        how="intersection", keep_geom_type=True,
    )
    overlay["acres"] = overlay.geometry.area / SQ_M_PER_ACRE
    by_code = (
        overlay.groupby(["neighbourhood_name", "code"])["acres"].sum()
        .unstack(fill_value=0.0)
    )
    for c in INST_CODES:
        if c not in by_code.columns:
            by_code[c] = 0.0
    by_code = by_code[list(INST_CODES)]
    by_code["inst_acres"] = by_code.sum(axis=1)
    by_code["dominant_inst_code"] = by_code[list(INST_CODES)].idxmax(axis=1)
    by_code.loc[by_code["inst_acres"] == 0, "dominant_inst_code"] = ""
    return by_code.reset_index(), inst


def taxable_footprint_on_institutional(grid_input, inst_polys) -> pd.DataFrame:
    """Deduped taxable lot footprint (acres) that sits ON institutional zoning,
    per hood. Spatial-joins each eligible taxable POINT to the institutional
    polygons and sums its deduped lot_m2."""
    pts = grid_input.loc[
        grid_input["latitude"].notna() & grid_input["longitude"].notna()
    ]
    per_point = _point_lot_stats(pts[["latitude", "longitude", "lot_size"]])
    hood = pts.groupby(["latitude", "longitude"], sort=False)["neighbourhood_name"].first()
    per_point = per_point.merge(
        hood.rename("neighbourhood_name").reset_index(),
        on=["latitude", "longitude"],
    )
    elig = per_point[per_point["eligible"]].copy()

    gpts = gpd.GeoDataFrame(
        elig,
        geometry=gpd.points_from_xy(elig["longitude"], elig["latitude"]),
        crs="EPSG:4326",
    ).to_crs(epsg=3400)

    inst_union = gpd.GeoDataFrame(geometry=[inst_polys.union_all()], crs="EPSG:3400")
    on_inst = gpts.sjoin(inst_union, how="inner", predicate="within")
    tax = (
        on_inst.groupby("neighbourhood_name")["lot_m2"].sum() / SQ_M_PER_ACRE
    ).rename("taxable_inst_acres")
    return tax.reset_index()


def main() -> None:
    served = served_hoods()

    a = load_assessment(ASSESS)
    pinfo = load_property_info(PINFO)
    grid_input = a.merge(pinfo, on="account_number", how="left")

    boundaries = load_boundaries(BOUND)  # EPSG:3400, area_acres
    area = boundaries[["neighbourhood_name", "area_acres"]]
    inst_by_code, inst_polys = institutional_zoning(boundaries)
    tax_on_inst = taxable_footprint_on_institutional(grid_input, inst_polys)
    hood_lot = build_hood_lot_acres(grid_input)[["neighbourhood_name", "lot_acres_eligible"]]
    roll = a.groupby("neighbourhood_name").agg(
        total_value=("assessed_value", "sum"),
        n_accounts=("assessed_value", "size"),
    ).reset_index()

    df = (
        served
        .merge(area, on="neighbourhood_name", how="left")
        .merge(inst_by_code, on="neighbourhood_name", how="left")
        .merge(tax_on_inst, on="neighbourhood_name", how="left")
        .merge(hood_lot, on="neighbourhood_name", how="left")
        .merge(roll, on="neighbourhood_name", how="left")
    )
    df["inst_acres"] = df["inst_acres"].fillna(0.0)
    df["taxable_inst_acres"] = df["taxable_inst_acres"].fillna(0.0)

    # --- the honest exempt-institutional measure --------------------------------
    df["exempt_inst_acres"] = (df["inst_acres"] - df["taxable_inst_acres"]).clip(lower=0)
    df["exempt_inst_frac"] = df["exempt_inst_acres"] / df["area_acres"]
    df["lot_boost"] = df["value_per_lot_acre"] / df["value_per_acre"]

    def mechanism(r) -> str:
        code = r["dominant_inst_code"]
        return {"UI": "university/school/hospital", "AJ": "federal/provincial",
                "PU": "utility/infrastructure", "UF": "civic facilities"}.get(code, "-")

    df["mechanism"] = df.apply(mechanism, axis=1)

    # ---- report ----------------------------------------------------------------
    exempt = df[
        (df["exempt_inst_frac"] >= EXEMPT_FRAC_MIN) & (~df["is_set_aside"].astype(bool))
    ].sort_values("exempt_inst_frac", ascending=False)

    print("=" * 104)
    print("EXEMPT-INSTITUTIONAL HOODS — institutional zoning (UI/UF/AJ/PU) carrying NO taxable")
    print(f"account, >= {EXEMPT_FRAC_MIN:.0%} of the polygon. Ranked by exempt_inst_frac.")
    print("exempt_inst_acres = institutional-zoned acres  -  taxable footprint sitting on them.")
    print("=" * 104)
    print(f'{"hood":<28}{"exmpt%":>7}{"exAcre":>7}{"instAc":>7}{"parc%":>6}'
          f'{"boost":>6}{"$/lotac":>8}{"code":>5}  mechanism')
    for _, r in exempt.iterrows():
        print(f'{r.neighbourhood_name[:27]:<28}{r.exempt_inst_frac*100:>7.0f}'
              f'{r.exempt_inst_acres:>7.0f}{r.inst_acres:>7.0f}{r.parcel_frac*100:>6.0f}'
              f'{r.lot_boost:>6.2f}{r.value_per_lot_acre/1e6:>8.2f}'
              f'{r.dominant_inst_code:>5}  {r.mechanism}')

    print("\n--- top exempt-institutional hoods, with absolutes ---")
    for _, r in exempt.head(12).iterrows():
        print(f'{r.neighbourhood_name}: ${r.total_value/1e9:.3f}B taxable on '
              f'{int(r.n_accounts)} accts | polygon {r.area_acres:.0f}ac, inst zoning '
              f'{r.inst_acres:.0f}ac of which ~{r.exempt_inst_acres:.0f}ac untaxed '
              f'(exempt) | $/ground {r.value_per_acre/1e6:.1f}M -> $/lot '
              f'{r.value_per_lot_acre/1e6:.1f}M (x{r.lot_boost:.1f}) | {r.mechanism}')

    # Contrast set: high lot-boost hoods that are NOT exempt-institutional (park).
    print("\n--- for contrast: big lot-acre boost but NOT exempt-institutional (park/river) ---")
    park = df[
        (df["lot_boost"] >= 2.0) & (df["exempt_inst_frac"] < EXEMPT_FRAC_MIN)
        & (~df["is_set_aside"].astype(bool))
    ].sort_values("lot_boost", ascending=False).head(8)
    for _, r in park.iterrows():
        print(f'{r.neighbourhood_name[:27]:<28} boost x{r.lot_boost:.1f}  '
              f'parcel {r.parcel_frac*100:.0f}%  exempt_inst {r.exempt_inst_frac*100:.0f}%  '
              f'inst {r.inst_acres:.0f}ac')


if __name__ == "__main__":
    main()

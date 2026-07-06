"""Modeled stormwater charge per neighbourhood (utility lens #1).

Implements the Bylaw 20865 daily stormwater charge — ``A x I x R x rate`` —
per property POINT from the property-info CSV (``dkk9-cj3x``), then
aggregates to neighbourhoods. Design + open decisions: docs/SPEC_utilities.md
Lens 1; tariff source docs/utility_cost_estimation_lens_methods.md §C.

**Everything here is MODELED (bylaw formula applied to open data), not
billed.** Known limitation shared with the revenue metrics: the roll omits
exempt institutional land entirely, so hood totals understate wherever
exempt land dominates.

- **A** — parcel area per point: rows grouped by exact lat/long and deduped
  with ``export_value_grid._point_lot_stats`` (the repeat-aware condo rule of
  docs/FINDINGS_lot_dedupe.md — which is the bylaw's own per-unit
  apportionment read back). Majority-null multi-unit points are ineligible,
  excluded + reported.
- **I** — Development Intensity Factor, default 1.0 (SIAP/LID credits out of
  scope v1).
- **R** — runoff coefficient from the explicit ``ZONE_RUNOFF`` dict below
  (verified bylaw-table rows marked; special-area codes assigned by
  closest-aligned zone, the bylaw's own rule for unlisted zones), with the
  lot-size splits applied against the point's deduped area.
- **rate** — from ``data/stormwater_rates.json``, year-keyed like
  ``mill_rates.json`` (rates reset each April 1; the year must match the
  assessment roll year, same rule as mill rates).

Zone resolution order (each path's count reported, no silent drops):
row's own ``zoning`` column → modal zone among rows at the same point →
point-in-polygon against the ``fixa-tstc`` zoning polygons → unresolved
(excluded + reported). Never use the stale historical layer ``67p2-r285``
(old bylaw codes — DATA.md §5 / SPEC_utilities.md).
"""

import json
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd

from export_value_grid import _point_lot_stats
from load_assessment import NAME_CORRECTIONS

logger = logging.getLogger(__name__)

# --- Runoff coefficients (R) ------------------------------------------------
# Lot-size split rows: (threshold_m2, r_below, r_at_or_above), evaluated
# against the point's deduped parcel area. Note the direction REVERSES
# between residential (smaller lot -> higher R: denser coverage) and DC
# (larger site -> higher R).
_R_LOW_RES = (450.0, 0.55, 0.50)   # RS/RSF bylaw row: <450 m2 -> 0.55, else 0.50
_R_MID_RES = (450.0, 0.60, 0.55)   # RM/RSM bylaw row: <450 m2 -> 0.60, else 0.55
_R_DC = (700.0, 0.55, 0.60)        # DC bylaw row:     <700 m2 -> 0.55, else 0.60

# Every base zone code hand-assigned (same philosophy as ZONE_CATEGORY in
# load_zoning.py — no prefix heuristics; unknown codes warn loudly and are
# excluded + reported, never guessed). Two provenance tiers:
#   [bylaw]   — directly in the Bylaw 20865 runoff table (Methods §C)
#   [aligned] — special-area code mapped to its closest-aligned zone, the
#               bylaw's own rule for zones not in the table (EWSI discretion);
#               alignment chosen from the code's ZONE_CATEGORY + description.
ZONE_RUNOFF = {
    # --- [bylaw] verified table rows ---------------------------------------
    # VERIFY: the source table lists AG at both 0.1 (own row) and 0.2 (grouped
    # row); the dedicated row is taken. Check against Bylaw 20865 Schedule 1
    # before any production claim — few billed parcels are AG, impact is low.
    "AG": 0.1,
    "A": 0.2, "NA": 0.2, "RR": 0.2, "RVSA": 0.2,
    "PS": 0.3, "PSN": 0.3,
    "FD": 0.4,
    "AJ": 0.5,
    "RS": _R_LOW_RES, "RSF": _R_LOW_RES,
    "PU": 0.55, "UF": 0.55,
    "RM": _R_MID_RES, "RSM": _R_MID_RES,
    "DC": _R_DC, "DC1": _R_DC, "DC2": _R_DC,
    "RL": 0.6, "UI": 0.6,
    "CN": 0.65, "MUN": 0.65,
    "BE": 0.75, "CB": 0.75, "CG": 0.75, "IH": 0.75, "IM": 0.75, "MU": 0.75,

    # --- [aligned] never: river valley / natural / parks -------------------
    "A1": 0.2, "A2": 0.2, "A3": 0.2, "A4": 0.2, "A5": 0.2, "A6": 0.2,
    "A7": 0.2, "NSRVES": 0.2,          # river-valley special areas -> A
    "BP": 0.3,                         # Blatchford Parks -> PS

    # --- [aligned] notyet: rural fringe / reserve ---------------------------
    "AES": 0.1,                        # Agricultural Edmonton South -> AG
    "RCES": 0.2, "RAES": 0.2,          # country/acreage residential -> RR
    "EETC": 0.75, "EETIM": 0.75, "EETM": 0.75, "EETL": 0.75,  # EET industrial -> IM/IH
    "EETR": 0.4,                       # EET Industrial Reserve -> FD

    # --- [aligned] institutional --------------------------------------------
    # (PU/UF/UI/AJ are bylaw rows above; no special-area inst codes exist)

    # --- [aligned] residential: low-density -> RS/RSF split ----------------
    "GLD": _R_LOW_RES, "GLDF": _R_LOW_RES, "SLD": _R_LOW_RES,
    "PLD": _R_LOW_RES, "CCSD": _R_LOW_RES, "CCLD": _R_LOW_RES,

    # --- [aligned] residential: row housing -> RM/RSM split ----------------
    "GRH": _R_MID_RES, "BRH": _R_MID_RES, "SRH": _R_MID_RES,
    "SRA": _R_MID_RES, "PRH": _R_MID_RES, "RVRH": _R_MID_RES,

    # --- [aligned] residential: apartment / medium-high -> RL --------------
    "GLRA": 0.6, "GMRA": 0.6, "BLMR": 0.6, "BMR": 0.6, "ALA": 0.6,
    "CCMD": 0.6, "CCHD": 0.6, "HDR": 0.6, "RMU": 0.6,
    "RTCR": 0.6, "RTCMR": 0.6,

    # --- [aligned] commercial: neighbourhood-scale -> CN --------------------
    "CCNC": 0.65,

    # --- [aligned] commercial: general / downtown / centres -> CB/CG -------
    "CCA": 0.75, "JAMSC": 0.75, "AED": 0.75, "MED": 0.75, "MRC": 0.75,
    "ASC": 0.75, "AUVC": 0.75, "ECB": 0.75, "TC-C": 0.75, "UC3ES": 0.75,

    # --- [aligned] industrial -> IM/IH --------------------------------------
    "EIB": 0.75, "EIM": 0.75, "ILES": 0.75, "IBES": 0.75,

    # --- [aligned] mixed: neighbourhood main-street / village -> MUN -------
    "MMS": 0.65, "CMUV": 0.65, "GVC": 0.65, "TC-MU": 0.65,

    # --- [aligned] mixed: downtown / major -> MU ----------------------------
    "CMU": 0.75, "HA": 0.75, "UW": 0.75, "MMUT": 0.75,
    "CPMU": 0.75, "CPT": 0.75, "RCRM": 0.75, "RCRL": 0.75,

    # --- [aligned] direct control variants -> DC split ----------------------
    "DC/INDES": _R_DC,
}

# Annualization factor by the rate's published unit.
_ANNUAL_FACTOR = {"m2_day": 365.0, "m2_month": 12.0}

# Project CRS for anything metric (per project rule: set explicitly).
_ALBERTA_CRS = "EPSG:3400"


def load_stormwater_rate(rates_json: str | Path, year: int) -> tuple[float, float]:
    """Return (annual_rate_per_m2, intensity_default) for ``year``.

    Hard-errors on a missing year — silently modeling one year's charges
    against another year's roll is the mill-rate desync bug all over again.
    """
    with open(rates_json, encoding="utf-8") as f:
        rates = json.load(f)
    entry = rates["years"].get(str(year))
    if entry is None:
        raise ValueError(
            f"no stormwater rate for {year} in {rates_json} — "
            f"available: {sorted(rates['years'])}"
        )
    factor = _ANNUAL_FACTOR.get(entry["per"])
    if factor is None:
        raise ValueError(f"unknown rate unit {entry['per']!r} in {rates_json}")
    return entry["rate"] * factor, rates.get("intensity_default", 1.0)


def runoff_coefficient(zone: str, area_m2: float) -> float | None:
    """R for a base zone code, applying the lot-size splits; None if unknown."""
    spec = ZONE_RUNOFF.get(zone)
    if spec is None:
        return None
    if isinstance(spec, tuple):
        threshold, below, at_or_above = spec
        return below if area_m2 < threshold else at_or_above
    return spec


def _base_zone(zoning: pd.Series) -> pd.Series:
    """First whitespace token, uppercased — strips height/overlay suffixes."""
    return zoning.astype("string").str.strip().str.split().str[0].str.upper()


def _fallback_zones(points: pd.DataFrame, zoning_gdf: gpd.GeoDataFrame) -> pd.Series:
    """Resolve zone codes for points via point-in-polygon (EPSG:3400).

    ``points`` needs latitude/longitude; ``zoning_gdf`` needs a ``zoning``
    column and polygon geometry (the fixa-tstc layer). Returns a Series of
    base zone codes indexed like ``points`` (NaN where no polygon contains
    the point). Multiple containing polygons (overlaps/slivers): first match
    wins.
    """
    pts = gpd.GeoDataFrame(
        index=points.index,
        geometry=gpd.points_from_xy(points["longitude"], points["latitude"]),
        crs="EPSG:4326",
    ).to_crs(_ALBERTA_CRS)

    zones = zoning_gdf[["zoning", "geometry"]].copy()
    if zones.crs is None:
        zones = zones.set_crs("EPSG:4326")
    zones = zones.to_crs(_ALBERTA_CRS)
    zones["zoning"] = _base_zone(zones["zoning"])

    hits = gpd.sjoin(pts, zones, how="left", predicate="within")
    # De-duplicate points that fall in overlapping polygons.
    hits = hits[~hits.index.duplicated(keep="first")]
    return hits["zoning"].reindex(points.index)


def load_stormwater(
    property_info_csv: str | Path,
    rates_json: str | Path,
    year: int,
    zoning_geojson: str | Path | None = None,
) -> pd.DataFrame:
    """Model the annual stormwater charge per neighbourhood.

    Returns a DataFrame keyed by ``neighbourhood_name``:
        storm_lot_m2         float  sum of eligible deduped parcel area
        storm_effective_m2   float  sum of A x I x R (rate-independent)
        storm_charge_annual  float  modeled $/year at the ``year`` rate

    ``zoning_geojson`` (fixa-tstc) enables the point-in-polygon fallback for
    zone-null points; when None/absent those points stay unresolved (still
    counted + reported, never silent).
    """
    annual_rate, intensity = load_stormwater_rate(rates_json, year)

    df = pd.read_csv(
        property_info_csv,
        usecols=["zoning", "lot_size", "Latitude", "Longitude", "Neighbourhood"],
        low_memory=False,
    ).rename(columns={
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Neighbourhood": "neighbourhood_name",
    })
    df["lot_size"] = pd.to_numeric(df["lot_size"], errors="coerce")
    df["zone"] = _base_zone(df["zoning"])
    df["neighbourhood_name"] = (
        df["neighbourhood_name"].astype("string").str.strip().str.upper()
        .replace(NAME_CORRECTIONS)
    )

    no_coords = df["latitude"].isna() | df["longitude"].isna()
    if no_coords.any():
        logger.warning(
            "%d rows have null coordinates — excluded from the stormwater model",
            int(no_coords.sum()),
        )
    rows = df.loc[~no_coords]

    # --- A: deduped parcel area per point (FINDINGS_lot_dedupe heuristic) ---
    per_point = _point_lot_stats(rows)

    # --- zone per point: modal own-column zone, then spatial fallback -------
    own = (
        rows.dropna(subset=["zone"])
        .groupby(["latitude", "longitude"], sort=False)["zone"]
        .agg(lambda s: s.mode().iloc[0])
    )
    per_point = per_point.merge(
        own.rename("zone").reset_index(), on=["latitude", "longitude"], how="left"
    )
    n_own = per_point["zone"].notna().sum()

    unresolved = per_point["zone"].isna()
    n_fallback = 0
    if unresolved.any() and zoning_geojson is not None and Path(zoning_geojson).exists():
        zoning_gdf = gpd.read_file(zoning_geojson)
        fb = _fallback_zones(per_point.loc[unresolved], zoning_gdf)
        per_point.loc[unresolved, "zone"] = fb
        n_fallback = int(per_point.loc[unresolved.index[unresolved], "zone"].notna().sum())
    elif unresolved.any() and zoning_geojson is not None:
        logger.warning(
            "Zoning file not found (%s) — no spatial fallback for %d zone-less points",
            zoning_geojson, int(unresolved.sum()),
        )

    # --- R per point (lot-size splits against the deduped area) -------------
    per_point["r"] = [
        runoff_coefficient(z, a) if pd.notna(z) else None
        for z, a in zip(per_point["zone"], per_point["lot_m2"])
    ]

    unknown = per_point["zone"].notna() & per_point["r"].isna()
    if unknown.any():
        counts = per_point.loc[unknown, "zone"].value_counts()
        logger.warning(
            "%d points carry zone codes with NO runoff assignment — excluded "
            "+ reported (extend ZONE_RUNOFF):\n  %s",
            int(unknown.sum()),
            "\n  ".join(f"{z}: {n}" for z, n in counts.items()),
        )

    modeled = per_point["eligible"] & per_point["r"].notna()
    excluded = per_point.loc[~modeled]
    if len(excluded):
        logger.warning(
            "Stormwater model excludes %d of %d points (%d lot-ineligible, "
            "%d zone-unresolved, %d zone-unassigned) carrying %.0f km2 of "
            "raw lot area — reported, not modeled",
            len(excluded), len(per_point),
            int((~per_point["eligible"]).sum()),
            int(per_point["zone"].isna().sum()),
            int(unknown.sum()),
            excluded["lot_m2"].sum() / 1e6,
        )

    pts = per_point.loc[modeled].copy()
    pts["effective_m2"] = pts["lot_m2"] * intensity * pts["r"]

    # --- hood per point, then aggregate --------------------------------------
    hood_of_point = (
        rows.groupby(["latitude", "longitude"], sort=False)["neighbourhood_name"].first()
    )
    pts = pts.merge(
        hood_of_point.rename("neighbourhood_name").reset_index(),
        on=["latitude", "longitude"],
    )

    out = (
        pts.groupby("neighbourhood_name", as_index=False)
        .agg(storm_lot_m2=("lot_m2", "sum"), storm_effective_m2=("effective_m2", "sum"))
    )
    out["storm_charge_annual"] = out["storm_effective_m2"] * annual_rate

    logger.info(
        "Stormwater model (year %d rate): %d points modeled (%d zone from own "
        "column, %d from spatial fallback) -> %d hoods, citywide $%.1fM/yr "
        "on %.0f km2 eligible lot area",
        year, len(pts), int(n_own), n_fallback, len(out),
        out["storm_charge_annual"].sum() / 1e6,
        out["storm_lot_m2"].sum() / 1e6,
    )
    return out

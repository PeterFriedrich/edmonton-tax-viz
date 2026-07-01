"""Land-use layer: overlay the Zoning Bylaw polygons on neighbourhood boundaries
to derive each neighbourhood's set-aside share (never + not-yet land).

See docs/SPEC_revenue.md (Update 2026-06-29), docs/ARCHITECTURE.md §load_zoning,
and data/DATA.md §5. Categorization is an EXPLICIT code→category dict (95 base
codes confirmed 2026-06-30) — never keyword/prefix heuristics.
"""

import logging

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)

# Threshold above which a neighbourhood is set aside (SPEC_revenue.md 2026-06-29).
SET_ASIDE_THRESHOLD = 0.90

# ---------------------------------------------------------------------------
# Explicit zone-code → land-use category dictionary.
#
# Keyed on the FIRST whitespace token of the `zoning` field (height/overlay
# suffixes like "RM h16" are dropped). Categories:
#   never  — permanently non-taxable: River Valley / Natural Areas / Parks
#   notyet — undeveloped holding land: Future Dev / rural fringe / industrial reserve
#   inst   — institutional proxy (UI/UF/AJ/PU); STAYS on the scale, tracked separately
#   dev    — developed (residential/commercial/industrial/mixed); stays on the scale
#
# set-aside = never + notyet.  dev + inst stay on the colour scale.
# Cross-checked against each row's `url` bylaw section (DATA.md §5).
# ---------------------------------------------------------------------------
ZONE_CATEGORY = {
    # --- never: River Valley / Natural / Parks ---------------------------------
    "A": "never",        # River Valley
    "A1": "never",       # Fort Edmonton Park Special Area
    "A2": "never",       # Muttart Conservatory Special Area
    "A3": "never",       # Louise McKinney Riverfront Special Area
    "A4": "never",       # Edmonton Valley Zoo Special Area
    "A5": "never",       # Buena Vista Park Special Area
    "A6": "never",       # River Crossing Special Area
    "A7": "never",       # William Hawrelak Park Zone
    "NA": "never",       # Natural Areas
    "NSRVES": "never",   # North Saskatchewan River Valley Edmonton South
    "PS": "never",       # Parks and Services
    "PSN": "never",      # Neighbourhood Parks and Services
    "BP": "never",       # Blatchford Parks

    # --- notyet: Future / rural fringe / industrial reserve --------------------
    "FD": "notyet",      # Future Urban Development
    "AG": "notyet",      # Agriculture Zone
    "RR": "notyet",      # Rural Residential
    "AES": "notyet",     # Agricultural Edmonton South
    "RCES": "notyet",    # Country Residential Edmonton South
    "RAES": "notyet",    # Acreage Residential Edmonton South
    "EETC": "notyet",    # Edmonton Energy & Technology Park — Chemical Cluster
    "EETIM": "notyet",   # Edmonton Energy & Technology Park — Medium Industrial
    "EETM": "notyet",    # Edmonton Energy & Technology Park — Manufacturing
    "EETL": "notyet",    # Edmonton Energy & Technology Park — Logistics
    "EETR": "notyet",    # Edmonton Energy & Technology Park — Industrial Reserve

    # --- inst: institutional proxy (stays on scale) ---------------------------
    "PU": "inst",        # Public Utility
    "UF": "inst",        # Urban Facilities
    "UI": "inst",        # Urban Institution
    "AJ": "inst",        # Alternative Jurisdiction

    # --- dev: developed (everything else) -------------------------------------
    # Standard residential
    "RSF": "dev", "RM": "dev", "RS": "dev", "RSM": "dev", "RL": "dev",
    "HDR": "dev", "RMU": "dev",
    # Commercial / mixed use / business
    "CN": "dev", "CG": "dev", "CB": "dev", "CCA": "dev", "CMU": "dev",
    "MU": "dev", "MUN": "dev", "BE": "dev", "JAMSC": "dev", "AED": "dev",
    "HA": "dev",
    # Industrial
    "IM": "dev", "IH": "dev", "UW": "dev",
    # Direct Control — default to developed (DATA.md §5 rule)
    "DC": "dev", "DC1": "dev", "DC2": "dev", "DC/INDES": "dev",
    # Griesbach special area
    "GLDF": "dev", "GRH": "dev", "GLRA": "dev", "GMRA": "dev", "GLD": "dev",
    "GVC": "dev",
    # Blatchford special area
    "BLMR": "dev", "BRH": "dev", "BMR": "dev",
    # Stillwater special area
    "SRH": "dev", "SLD": "dev", "SRA": "dev",
    # Paisley special area
    "PLD": "dev", "PRH": "dev",
    # Riverview special area
    "RVRH": "dev", "RTCMR": "dev", "RTCR": "dev",
    # Ambleside special area
    "ALA": "dev", "ASC": "dev", "AUVC": "dev",
    # Clareview Campus special area
    "CCSD": "dev", "CCMD": "dev", "CCLD": "dev", "CCHD": "dev", "CCNC": "dev",
    # Marquis special area
    "MRC": "dev", "MMUT": "dev", "MED": "dev", "MMS": "dev",
    # Century Park special area
    "CPMU": "dev", "CPT": "dev",
    # River Crossing (developed portions)
    "RCRM": "dev", "RCRL": "dev",
    # Town Center / other special areas
    "TC-MU": "dev", "TC-C": "dev", "CMUV": "dev",
    # Ellerslie / Edmonton South industrial & commercial (rezoned = developed)
    "EIB": "dev", "EIM": "dev", "ECB": "dev", "ILES": "dev", "IBES": "dev",
    "UC3ES": "dev",
}

# never + notyet make up the set-aside share.
SET_ASIDE_CATEGORIES = ("never", "notyet")

# Unknown codes default here (conservative — won't wrongly hide land). Flagged.
DEFAULT_CATEGORY = "dev"

# Human-readable dominant-reason labels for the tooltip.
REASON_LABELS = {
    "never": "River Valley / Natural / Parks",
    "notyet": "Future / Rural / Reserve",
}


def _categorize(zoning_series: pd.Series) -> pd.Series:
    """Map the `zoning` field to a land-use category via the explicit dict.

    Parses the first whitespace token as the base code, then looks it up.
    Unmatched codes are flagged (no silent drops) and default to developed.
    """
    base = zoning_series.fillna("").str.split().str[0]
    category = base.map(ZONE_CATEGORY)

    unmatched = category.isna()
    if unmatched.any():
        missing = sorted(base[unmatched].unique())
        logger.warning(
            "Unmatched zone codes (defaulting to %r): %s",
            DEFAULT_CATEGORY,
            missing,
        )
        category = category.fillna(DEFAULT_CATEGORY)

    return category


def _clean_geometry(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """buffer(0) to fix invalid polygons; drop empty and non-polygonal parts.

    Raw municipal zoning polygons are invalid/mixed-dimension and make GEOS
    overlay raise (DATA.md §5).
    """
    before = len(gdf)
    gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notna()].copy()
    gdf["geometry"] = gdf.geometry.buffer(0)
    gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    gdf = gdf[~gdf.geometry.is_empty]
    dropped = before - len(gdf)
    if dropped:
        logger.info("Dropped %d empty/non-polygonal zoning features after cleaning", dropped)
    return gdf


def load_zoning(zoning_path: str, boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Overlay zoning on neighbourhood boundaries → per-neighbourhood set-aside share.

    Parameters
    ----------
    zoning_path : str
        Path to the zoning GeoJSON (`fixa-tstc`, see DATA.md §5).
    boundaries : gpd.GeoDataFrame
        Output of load_boundaries — MUST carry projected geometry (EPSG:3400)
        and a `neighbourhood_name` column.

    Returns
    -------
    pd.DataFrame keyed by `neighbourhood_name` with columns:
        frac_never, frac_notyet, frac_dev, frac_inst — land-use composition
        set_aside_frac  — never + notyet share (0–1)
        is_set_aside    — set_aside_frac >= SET_ASIDE_THRESHOLD
        set_aside_reason — dominant set-aside category label (tooltip); "" if not set aside
    """
    zoning = gpd.read_file(zoning_path)
    logger.info("Loaded %d zoning features (input CRS: %s)", len(zoning), zoning.crs)

    if zoning.crs is None:
        logger.warning("Zoning CRS missing — assuming EPSG:4326 per DATA.md §5")
        zoning = zoning.set_crs(epsg=4326)
    zoning = zoning.to_crs(epsg=3400)

    zoning = _clean_geometry(zoning)
    zoning["category"] = _categorize(zoning["zoning"])

    # Keep only what the overlay needs.
    zoning = zoning[["category", "geometry"]]

    if boundaries.crs is None or boundaries.crs.to_epsg() != 3400:
        raise ValueError(
            f"boundaries must be projected to EPSG:3400 before overlay (got {boundaries.crs})"
        )

    overlay = gpd.overlay(
        boundaries[["neighbourhood_name", "geometry"]],
        zoning,
        how="intersection",
        keep_geom_type=True,
    )
    overlay["piece_area"] = overlay.geometry.area

    # Fractions are relative to the total ZONED area within each neighbourhood
    # (robust to boundary/zoning edge misalignment — pieces sum to 1 per hood).
    by_cat = (
        overlay.groupby(["neighbourhood_name", "category"])["piece_area"]
        .sum()
        .unstack(fill_value=0.0)
    )
    for cat in ("never", "notyet", "dev", "inst"):
        if cat not in by_cat.columns:
            by_cat[cat] = 0.0

    totals = by_cat[["never", "notyet", "dev", "inst"]].sum(axis=1)
    fracs = by_cat[["never", "notyet", "dev", "inst"]].div(totals, axis=0)

    result = pd.DataFrame(
        {
            "frac_never": fracs["never"],
            "frac_notyet": fracs["notyet"],
            "frac_dev": fracs["dev"],
            "frac_inst": fracs["inst"],
        }
    )
    result["set_aside_frac"] = result["frac_never"] + result["frac_notyet"]
    result["is_set_aside"] = result["set_aside_frac"] >= SET_ASIDE_THRESHOLD

    # Dominant set-aside reason for the tooltip (only meaningful when set aside).
    dominant = result[["frac_never", "frac_notyet"]].idxmax(axis=1).map(
        {"frac_never": REASON_LABELS["never"], "frac_notyet": REASON_LABELS["notyet"]}
    )
    result["set_aside_reason"] = dominant.where(result["is_set_aside"], "")

    result = result.reset_index()

    logger.info(
        "Zoning overlay: %d neighbourhoods, %d set aside (>= %.2f)",
        len(result),
        int(result["is_set_aside"].sum()),
        SET_ASIDE_THRESHOLD,
    )
    return result

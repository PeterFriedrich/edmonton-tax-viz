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

# Threshold above which a neighbourhood is flagged residential (residential-only
# lens). Share of total ZONED area, consistent with the other fractions. Display
# filter only — orthogonal to is_set_aside (a set-aside hood cannot also clear this,
# since the fractions sum to 1 and 0.90 + 0.50 > 1).
RESIDENTIAL_THRESHOLD = 0.50

# ---------------------------------------------------------------------------
# Explicit zone-code → land-use category dictionary.
#
# Keyed on the FIRST whitespace token of the `zoning` field (height/overlay
# suffixes like "RM h16" are dropped). Categories:
#   never  — permanently non-taxable: River Valley / Natural Areas / Parks
#   notyet — undeveloped holding land: Future Dev / rural fringe / industrial reserve
#   inst   — institutional proxy (UI/UF/AJ/PU); STAYS on the scale, tracked separately
#   res    — developed, primary permitted use is housing; stays on the scale
#   com    — developed commercial / retail / entertainment; stays on the scale
#   ind    — developed industrial / warehousing / business employment; stays on scale
#   mix    — developed mixed use (purpose statement blends res + com ± inst)
#   dc     — Direct Control: bespoke per-site bylaws, no single use claimable
#   other  — unknown codes only (DEFAULT_CATEGORY); stays on scale, flagged loudly
#
# res + the nonres group = the old "dev" bucket (split 2026-07-01 for the
# residential lens; nonres split again com/ind/mix/dc 2026-07-03 for the use-mix
# view). Classification is by each code's authoritative `description`; ambiguous
# names resolved from the bylaw page's purpose statement (the `url` field) —
# e.g. UW "Urban Warehouse" is a downtown mixed-use zone, NOT warehousing, and
# BE "Business Employment" sits in the bylaw's industrial-zones part.
# set-aside = never + notyet.  Everything else stays on the colour scale.
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

    # --- res: developed, primary use is housing -------------------------------
    # Standard residential
    "RSF": "res",        # Small Scale Flex Residential
    "RS": "res",         # Small Scale Residential
    "RSM": "res",        # Small-Medium Scale Transition Residential
    "RM": "res",         # Medium Scale Residential
    "RL": "res",         # Large Scale Residential
    "HDR": "res",        # High Density Residential
    "RMU": "res",        # Residential Mixed Use (primary use residential)
    # Griesbach special area — housing
    "GLD": "res",        # Griesbach Low Density Residential
    "GLDF": "res",       # Griesbach Low Density Residential Flex
    "GLRA": "res",       # Griesbach Low Rise Apartment
    "GMRA": "res",       # Griesbach Medium Rise Apartment
    "GRH": "res",        # Griesbach Row Housing
    # Blatchford special area — housing
    "BLMR": "res",       # Blatchford Low to Medium Rise Residential
    "BMR": "res",        # Blatchford Medium Rise Residential
    "BRH": "res",        # Blatchford Row Housing
    # Stillwater special area — housing
    "SLD": "res",        # Stillwater Low Density Residential
    "SRA": "res",        # Stillwater Rear Attached Housing
    "SRH": "res",        # Stillwater Row Housing
    # Paisley special area — housing
    "PLD": "res",        # Paisley Low Density
    "PRH": "res",        # Paisley Row Housing
    # Riverview special area — housing
    "RVRH": "res",       # Riverview Row Housing
    "RTCR": "res",       # Riverview Town Centre Residential
    "RTCMR": "res",      # Riverview Town Centre Medium Rise Residential
    # Ambleside special area — housing
    "ALA": "res",        # Ambleside Low Rise Apartment
    # Clareview Campus special area — housing
    "CCSD": "res",       # Clareview Campus Single Detached Residential
    "CCLD": "res",       # Clareview Campus Low Density Residential
    "CCMD": "res",       # Clareview Campus Medium Density Residential
    "CCHD": "res",       # Clareview Campus High Density Residential

    # --- com: commercial / retail / entertainment -----------------------------
    "CN": "com",         # Neighbourhood Commercial
    "CG": "com",         # General Commercial
    "CB": "com",         # Business Commercial
    "CCA": "com",        # Core Commercial Arts Zone (downtown)
    "JAMSC": "com",      # Jasper Avenue Main Street Commercial Zone (downtown)
    "AED": "com",        # Arena and Entertainment District Zone (downtown)
    "MED": "com",        # Marquis Entertainment District
    "MRC": "com",        # Marquis Retail Centre Zone
    "ASC": "com",        # Ambleside Shopping Centre
    "AUVC": "com",       # Ambleside Urban Village Commercial
    "CCNC": "com",       # Clareview Campus Neighbourhood Commercial
    "ECB": "com",        # Ellerslie Commercial Business Zone
    "TC-C": "com",       # Town Center Commercial (Heritage Valley)
    "UC3ES": "com",      # Urban Commercial 3 Edmonton South

    # --- ind: industrial / warehousing / business employment ------------------
    "IM": "ind",         # Medium Industrial
    "IH": "ind",         # Heavy Industrial
    "BE": "ind",         # Business Employment (bylaw part-2 industrial-zones)
    "EIB": "ind",        # Ellerslie Industrial Business Zone
    "EIM": "ind",        # Ellerslie Medium Industrial Zone
    "ILES": "ind",       # Light Industrial Edmonton South
    "IBES": "ind",       # Industrial Business Edmonton South

    # --- mix: mixed use (bylaw purpose blends res + commercial ± inst) --------
    "MU": "mix",         # Mixed Use
    "MUN": "mix",        # Neighbourhood Mixed Use
    "CMU": "mix",        # Commercial Mixed Use (downtown)
    "HA": "mix",         # Heritage Area (downtown; purpose = res + com + community)
    "UW": "mix",         # Urban Warehouse (downtown; purpose = mixed, NOT warehousing)
    "MMS": "mix",        # Marquis Main Street (ground-floor retail, res/office above)
    "MMUT": "mix",       # Marquis Mixed Use Transition Zone
    "CMUV": "mix",       # Central McDougall Urban Village
    "GVC": "mix",        # Griesbach Village Centre (businesses + residences + inst)
    "CPMU": "mix",       # Century Park Mixed Use Zone
    "CPT": "mix",        # Century Park Transition Zone (legacy TOD)
    "TC-MU": "mix",      # Town Center Mixed Use (Heritage Valley)
    "RCRM": "mix",       # River Crossing Medium Scale Zone (redevelopment)
    "RCRL": "mix",       # River Crossing Large Scale Zone (redevelopment)

    # --- dc: Direct Control — bespoke site-specific bylaws --------------------
    "DC": "dc",          # Direct Control
    "DC1": "dc",         # Direct Development Control Provision
    "DC2": "dc",         # Site Specific Development Control Provision
    "DC/INDES": "dc",    # Direct Control / Industrial District Edmonton South
}

# All land-use categories, in output order.
CATEGORIES = ("never", "notyet", "inst", "res", "com", "ind", "mix", "dc", "other")

# never + notyet make up the set-aside share.
SET_ASIDE_CATEGORIES = ("never", "notyet")

# The non-residential developed group (the pre-split "nonres" bucket) — summed
# into frac_nonres for continuity with docs/analyses that reference it.
NONRES_CATEGORIES = ("com", "ind", "mix", "dc", "other")

# Unknown codes default here (conservative — keeps land on the scale, does NOT
# claim it as residential or any specific non-residential use). Flagged.
DEFAULT_CATEGORY = "other"

# Human-readable dominant-reason labels for the tooltip.
REASON_LABELS = {
    "never": "River Valley / Natural / Parks",
    "notyet": "Future / Rural / Reserve",
}


def _categorize(zoning_series: pd.Series) -> pd.Series:
    """Map the `zoning` field to a land-use category via the explicit dict.

    Parses the first whitespace token as the base code, then looks it up.
    Unmatched codes are flagged (no silent drops) and default to "other" —
    on the scale, claimed as no specific use.
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
        frac_never, frac_notyet, frac_inst, frac_residential, frac_commercial,
        frac_industrial, frac_mixed, frac_dc, frac_other
                        — land-use composition (shares of total zoned area; sum to 1)
        frac_nonres     — commercial + industrial + mixed + dc + other (the
                          pre-split bucket, kept for continuity)
        set_aside_frac  — never + notyet share (0–1)
        is_set_aside    — set_aside_frac >= SET_ASIDE_THRESHOLD
        set_aside_reason — dominant set-aside category label (tooltip); "" if not set aside
        is_residential  — frac_residential >= RESIDENTIAL_THRESHOLD (display filter,
                          orthogonal to is_set_aside)
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
    for cat in CATEGORIES:
        if cat not in by_cat.columns:
            by_cat[cat] = 0.0

    cols = list(CATEGORIES)
    totals = by_cat[cols].sum(axis=1)
    fracs = by_cat[cols].div(totals, axis=0)

    result = pd.DataFrame(
        {
            "frac_never": fracs["never"],
            "frac_notyet": fracs["notyet"],
            "frac_inst": fracs["inst"],
            "frac_residential": fracs["res"],
            "frac_commercial": fracs["com"],
            "frac_industrial": fracs["ind"],
            "frac_mixed": fracs["mix"],
            "frac_dc": fracs["dc"],
            "frac_other": fracs["other"],
        }
    )
    # Pre-split bucket, kept for continuity (docs/ANALYSIS_BACKLOG reference it).
    result["frac_nonres"] = sum(fracs[c] for c in NONRES_CATEGORIES)
    result["set_aside_frac"] = result["frac_never"] + result["frac_notyet"]
    result["is_set_aside"] = result["set_aside_frac"] >= SET_ASIDE_THRESHOLD

    # Dominant set-aside reason for the tooltip (only meaningful when set aside).
    dominant = result[["frac_never", "frac_notyet"]].idxmax(axis=1).map(
        {"frac_never": REASON_LABELS["never"], "frac_notyet": REASON_LABELS["notyet"]}
    )
    result["set_aside_reason"] = dominant.where(result["is_set_aside"], "")

    # Residential-only lens flag (display filter, orthogonal to is_set_aside).
    result["is_residential"] = result["frac_residential"] >= RESIDENTIAL_THRESHOLD

    result = result.reset_index()

    logger.info(
        "Zoning overlay: %d neighbourhoods, %d set aside (>= %.2f), %d residential (>= %.2f)",
        len(result),
        int(result["is_set_aside"].sum()),
        SET_ASIDE_THRESHOLD,
        int(result["is_residential"].sum()),
        RESIDENTIAL_THRESHOLD,
    )
    return result

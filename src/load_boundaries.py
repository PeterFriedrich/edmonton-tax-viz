import logging

import geopandas as gpd

logger = logging.getLogger(__name__)

# The exact international acre. ⚠️ Was 4046.856422 (truncated) until
# 2026-09-07, disagreeing with export_value_grid.py's 4046.8564224 in the
# 11th significant figure — no published number moved (the largest
# revenue_per_acre shifts $0.000025), but two definitions of one constant
# is one too many. Pinned as a LITERAL in tests/test_load_boundaries.py:
# it was previously unpinned and could be HALVED with 784 tests green
# (docs/FINDINGS_vacuous_guards.md V2).
SQ_M_PER_ACRE = 4046.8564224


def load_boundaries(path: str) -> gpd.GeoDataFrame:
    """Load neighbourhood boundary GeoJSON, reproject, and compute area_acres."""
    gdf = gpd.read_file(path)
    logger.info("Loaded %d boundary features (input CRS: %s)", len(gdf), gdf.crs)

    gdf = gdf.to_crs(epsg=3400)

    gdf["area_acres"] = gdf.geometry.area / SQ_M_PER_ACRE
    gdf["neighbourhood_name"] = gdf["name"].str.strip().str.upper()

    logger.info(
        "area_acres range: %.1f – %.1f",
        gdf["area_acres"].min(),
        gdf["area_acres"].max(),
    )

    return gdf[["neighbourhood_name", "geometry", "area_acres"]]

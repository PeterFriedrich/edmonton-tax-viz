import logging

import geopandas as gpd

logger = logging.getLogger(__name__)

SQ_M_PER_ACRE = 4046.856422


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

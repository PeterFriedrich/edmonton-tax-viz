import logging

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)


def join_and_calculate(
    assessment: pd.DataFrame,
    boundaries: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Left join boundaries → assessment, flag unmatched rows, compute value_per_acre.

    Assessment names are expected to be corrected and aggregated already
    (NAME_CORRECTIONS is applied upstream in load_assessment.py). The three
    unresolved cases (OLIVER, HERITAGE VALLEY TOWN CENTRE AREA,
    LEWIS FARMS INDUSTRIAL) surface here as unmatched warnings.
    """
    agg = assessment

    boundary_names = set(boundaries["neighbourhood_name"])
    unmatched_assessment = sorted(set(agg["neighbourhood_name"]) - boundary_names)
    if unmatched_assessment:
        logger.warning(
            "%d assessment neighbourhood(s) with no boundary match (excluded from map):\n  %s",
            len(unmatched_assessment),
            "\n  ".join(unmatched_assessment),
        )

    joined = boundaries.merge(agg, on="neighbourhood_name", how="left")

    no_assessment = joined[joined["total_assessed_value"].isna()]
    if len(no_assessment):
        logger.warning(
            "%d boundary neighbourhood(s) with no assessment data:\n  %s",
            len(no_assessment),
            "\n  ".join(sorted(no_assessment["neighbourhood_name"])),
        )

    zero_area = joined["area_acres"] == 0
    if zero_area.any():
        logger.warning(
            "%d neighbourhood(s) with zero area_acres — value_per_acre will be NaN:\n  %s",
            zero_area.sum(),
            "\n  ".join(sorted(joined[zero_area]["neighbourhood_name"])),
        )

    joined["value_per_acre"] = (
        joined["total_assessed_value"] / joined["area_acres"].replace(0, float("nan"))
    )

    logger.info(
        "Joined %d boundary neighbourhoods; %d with value_per_acre calculated",
        len(joined),
        joined["value_per_acre"].notna().sum(),
    )

    return joined[["neighbourhood_name", "total_assessed_value", "area_acres", "value_per_acre", "geometry"]]


# Columns the web client actually consumes. Everything else is dropped to keep
# the GeoJSON the browser downloads small.
SLIM_COLUMNS = ["neighbourhood_name", "value_per_acre", "geometry"]


def export_geojson(
    result: gpd.GeoDataFrame,
    output_path: str,
    crs: str = "EPSG:4326",
) -> gpd.GeoDataFrame:
    """Write a slim GeoJSON of the join result for the Phase 2 web map.

    Keeps only the columns the deck.gl layer needs (SLIM_COLUMNS) and reprojects
    to ``crs`` (default EPSG:4326 — MapLibre/deck.gl expect lon/lat geometry; the
    join result is in projected EPSG:3400 for area math). Rows with no
    value_per_acre cannot be rendered (null elevation), so they are dropped — but
    the count is logged, never silently discarded.

    Returns the slim GeoDataFrame that was written.
    """
    slim = result[SLIM_COLUMNS]

    missing = slim["value_per_acre"].isna()
    if missing.any():
        logger.warning(
            "Dropping %d neighbourhood(s) with no value_per_acre from GeoJSON export:\n  %s",
            missing.sum(),
            "\n  ".join(sorted(slim[missing]["neighbourhood_name"])),
        )
    slim = slim[~missing]

    if slim.crs is None:
        raise ValueError("result GeoDataFrame has no CRS set; cannot reproject for export")
    slim = slim.to_crs(crs)

    slim.to_file(output_path, driver="GeoJSON")
    logger.info("Wrote slim GeoJSON (%d features, %s) to %s", len(slim), crs, output_path)

    return slim

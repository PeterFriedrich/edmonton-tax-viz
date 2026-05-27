import logging

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)

# Assessment name → boundary name. See data/DATA.md "Name Matching" for the
# three unresolved cases (OLIVER, HERITAGE VALLEY TOWN CENTRE AREA,
# LEWIS FARMS INDUSTRIAL) that will be flagged as unmatched.
NAME_CORRECTIONS = {
    "ANTHONY HENDAY SOUTHEAST":        "ANTHONY HENDAY SOUTH EAST",
    "CHAPPELLE AREA":                   "CHAPPELLE",
    "EDMONTON RESEARCH AND DEVEL PARK": "EDMONTON RESEARCH AND DEVELOPMENT PARK",
    "PLACE LA RUE":                     "PLACE LARUE",
    "RAPPERSWIL":                       "RAPPERSWILL",
    "RIVER VALLEY WINDEMERE":           "RIVER VALLEY WINDERMERE",
    "SOUTHEAST (ANNEXED) INDUSTRIAL":   "SOUTHEAST INDUSTRIAL",
    "WESTBROOK ESTATE":                 "WESTBROOK ESTATES",
}


def join_and_calculate(
    assessment: pd.DataFrame,
    boundaries: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Left join boundaries → assessment, flag unmatched rows, compute value_per_acre."""
    agg = assessment.copy()
    agg["neighbourhood_name"] = agg["neighbourhood_name"].replace(NAME_CORRECTIONS)

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

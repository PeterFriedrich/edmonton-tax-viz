import logging

import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_by_neighbourhood(df: pd.DataFrame) -> pd.DataFrame:
    """Sum assessed values by neighbourhood.

    Returns a DataFrame with columns:
        neighbourhood_name      str
        total_assessed_value    float
    """
    aggregated = (
        df.groupby("neighbourhood_name", as_index=False)["assessed_value"]
        .sum()
        .rename(columns={"assessed_value": "total_assessed_value"})
    )

    logger.info("Aggregated %d properties into %d neighbourhoods", len(df), len(aggregated))

    return aggregated

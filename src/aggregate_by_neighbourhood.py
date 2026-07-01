import logging

import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_by_neighbourhood(df: pd.DataFrame) -> pd.DataFrame:
    """Sum assessed values (and levy, if present) by neighbourhood.

    Returns a DataFrame with columns:
        neighbourhood_name      str
        total_assessed_value    float
        total_revenue           float   only if ``levy`` is present (revenue phase)

    ``levy`` is summed into ``total_revenue`` only when apply_tax_rates.py has run
    upstream, so the Phase 1 value-only path is unaffected.
    """
    agg_spec = {"assessed_value": "sum"}
    if "levy" in df.columns:
        agg_spec["levy"] = "sum"

    aggregated = (
        df.groupby("neighbourhood_name", as_index=False)
        .agg(agg_spec)
        .rename(columns={"assessed_value": "total_assessed_value", "levy": "total_revenue"})
    )

    logger.info("Aggregated %d properties into %d neighbourhoods", len(df), len(aggregated))

    return aggregated

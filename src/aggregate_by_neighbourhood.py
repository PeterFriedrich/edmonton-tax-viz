import logging

import pandas as pd

logger = logging.getLogger(__name__)


def aggregate_by_neighbourhood(df: pd.DataFrame) -> pd.DataFrame:
    """Sum assessed values (and levy, if present) by neighbourhood.

    Returns a DataFrame with columns:
        neighbourhood_name      str
        total_assessed_value    float
        total_revenue           float   only if ``levy`` is present (revenue phase)
        total_res_revenue       float   only if ``res_levy`` is present — the
                                        residential-class subset of total_revenue
        total_nonres_revenue    float   only if ``nonres_levy`` is present — the
                                        non-res-rate subset of total_revenue

    ``levy`` is summed into ``total_revenue`` only when apply_tax_rates.py has run
    upstream, so the Phase 1 value-only path is unaffected; ``res_levy`` →
    ``total_res_revenue`` and ``nonres_levy`` → ``total_nonres_revenue`` follow
    the same conditional pattern.
    """
    agg_spec = {"assessed_value": "sum"}
    if "levy" in df.columns:
        agg_spec["levy"] = "sum"
    if "res_levy" in df.columns:
        agg_spec["res_levy"] = "sum"
    if "nonres_levy" in df.columns:
        agg_spec["nonres_levy"] = "sum"

    aggregated = (
        df.groupby("neighbourhood_name", as_index=False)
        .agg(agg_spec)
        .rename(columns={
            "assessed_value": "total_assessed_value",
            "levy": "total_revenue",
            "res_levy": "total_res_revenue",
            "nonres_levy": "total_nonres_revenue",
        })
    )

    logger.info("Aggregated %d properties into %d neighbourhoods", len(df), len(aggregated))

    return aggregated

import logging

import geopandas as gpd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def plot_choropleth(gdf: gpd.GeoDataFrame, output_path: str) -> None:
    """Render value_per_acre choropleth and save to output_path."""
    plottable = gdf[gdf["value_per_acre"].notna()].copy()
    skipped = len(gdf) - len(plottable)
    if skipped:
        logger.warning("%d neighbourhood(s) with no value_per_acre omitted from map", skipped)

    fig, ax = plt.subplots(1, 1, figsize=(14, 12))

    plottable.plot(
        column="value_per_acre",
        ax=ax,
        cmap="YlOrRd",
        legend=True,
        legend_kwds={"label": "Assessed value per acre (CAD)", "shrink": 0.6},
        missing_kwds={"color": "lightgrey", "label": "No data"},
    )

    ax.set_title("Edmonton — Assessed Value per Acre by Neighbourhood", fontsize=14, pad=12)
    ax.set_axis_off()

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    logger.info("Saved choropleth to %s", output_path)

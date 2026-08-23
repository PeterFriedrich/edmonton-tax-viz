"""Network distance from every property to the nearest amenity, over the road graph.

Feeds the grid's ``dist_lrt_m`` / ``dist_school_m`` columns (SPEC_development.md
"Amenity distance"). One multi-source Dijkstra per amenity set, on a routable
graph built from the Road Network centrelines already in ``data/raw/``.

**Why not straight-line distance.** Measured 2026-08-22
(docs/FINDINGS_infill_granularity.md §5): a 600 m euclidean band around LRT is
wrong **55% of the time it says yes**, and 68% at 400 m. The river valley and
the rail/freeway corridors are the mechanism, and the error runs in the
direction that matters — it manufactures transit-adjacent opportunity nobody
can walk to. Network distance costs one Dijkstra over data we already hold.

**⚠️ Railways are excluded from the graph, and that is a correctness filter,
not a tidy-up.** ``centerline_type`` splits the file into Road (39,515), Alley
(12,088) and Railway (2,117). Routing over railway centrelines lets a walk
travel *along the LRT track itself* to reach an LRT station — a shortcut no
pedestrian has. Dropping alleys and railways also leaves the graph BETTER
connected, not worse: 163,841 nodes at 99.83% in one component, against
186,931 at 99.45% for the unfiltered file (measured 2026-08-23).

``responsible_party`` is deliberately NOT filtered, unlike load_roads. That
filter exists there because the services lens measures what the City must
maintain; here a provincial or private road is still a road somebody walks
along, and excluding it would carve holes in the graph.

**⚠️ This is a road-centreline proxy for a walk, not a walkshed.** Sidewalks,
river-valley trails, shared-use paths and pedestrian bridges are not in the
source, so a block whose real route is a footpath reads as further away than it
is. Distances are honest as *road* distances and should be described that way.
"""

import logging
from dataclasses import dataclass

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from pyproj import Transformer
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree

logger = logging.getLogger(__name__)

# Alberta 10-TM Forest — the project's metric CRS, set explicitly before any
# distance math (project rule).
PROJECTED_CRS = "EPSG:3400"
_TO_ALBERTA = Transformer.from_crs(4326, 3400, always_xy=True)

# Centreline rows that carry a walkable route. Explicit include set, not an
# exclude list: a new centerline_type value should be reviewed before it can
# route a pedestrian (the ZONE_CATEGORY philosophy).
WALKABLE_CENTERLINE_TYPES = ("Road",)

# Two graph vertices closer together than this are the same place. 0.1 m is far
# below the precision of anything downstream and keeps digitizing noise from
# splitting an intersection into two unconnected nodes.
NODE_SNAP_M = 0.1

# scipy's sparse graph routines read a stored 0 as "no edge", so every weight
# has to be strictly positive. 1 mm is inert at the metre scale we report.
MIN_EDGE_M = 1e-3

# A point this far from any centreline is reported. It is not dropped and not
# clamped — the snap length is included in its distance, so the number stays
# correct; the log exists because a cluster of them means the graph is missing
# roads, not that the properties are remote.
FAR_SNAP_WARN_M = 500.0


@dataclass(frozen=True)
class RoadGraph:
    """A routable undirected road graph in ``PROJECTED_CRS``."""

    node_xy: np.ndarray  # (n, 2) node coordinates, metres
    edges: csr_matrix    # (n, n) upper-triangular-ish weights, metres
    tree: cKDTree        # spatial index over node_xy, for snapping

    @property
    def n_nodes(self) -> int:
        return len(self.node_xy)


def build_road_graph(roads_path: str) -> RoadGraph:
    """Build the routable graph from a Road Network centreline GeoJSON.

    Every centreline vertex becomes a node and every consecutive vertex pair an
    undirected edge weighted by its length, so the graph carries curve geometry
    rather than only intersection-to-intersection straight lines.
    """
    gdf = gpd.read_file(roads_path)
    if "centerline_type" not in gdf.columns:
        raise ValueError(
            f"expected column 'centerline_type' not in {roads_path} — headers: "
            f"{list(gdf.columns)}"
        )
    kept = gdf[gdf["centerline_type"].isin(WALKABLE_CENTERLINE_TYPES)]
    dropped = gdf["centerline_type"].loc[~gdf.index.isin(kept.index)].value_counts()
    if kept.empty:
        raise ValueError(
            f"no {WALKABLE_CENTERLINE_TYPES} centrelines in {roads_path} — "
            f"found {sorted(set(gdf['centerline_type'].dropna()))}"
        )
    logger.info(
        "Road graph input: %d walkable centrelines; excluded %s",
        len(kept), ", ".join(f"{k} {v}" for k, v in dropped.items()) or "none",
    )

    parts = kept.to_crs(PROJECTED_CRS).explode(index_parts=False, ignore_index=True)
    xy, part_idx = shapely.get_coordinates(parts.geometry.values, return_index=True)
    # Consecutive coordinate pairs are an edge only WITHIN one part — the pair
    # that straddles two parts joins the end of one street to the start of an
    # unrelated one.
    within = part_idx[:-1] == part_idx[1:]
    seg_a, seg_b = xy[:-1][within], xy[1:][within]

    quantized = np.round(np.vstack([seg_a, seg_b]) / NODE_SNAP_M).astype(np.int64)
    _, inverse = np.unique(quantized, axis=0, return_inverse=True)
    inverse = inverse.ravel()
    ia, ib = inverse[: len(seg_a)], inverse[len(seg_a) :]
    node_xy = np.empty((int(inverse.max()) + 1, 2))
    node_xy[ia] = seg_a
    node_xy[ib] = seg_b

    length = np.hypot(seg_a[:, 0] - seg_b[:, 0], seg_a[:, 1] - seg_b[:, 1])
    real = ia != ib  # a zero-length segment (repeated vertex) is not an edge
    n = len(node_xy)
    # Duplicate (i, j) pairs SUM in a coo->csr conversion, and a doubled weight
    # would silently lengthen every route through it — parallel edges collapse
    # to the shortest instead.
    edges = _min_duplicates(ia[real], ib[real], np.maximum(length[real], MIN_EDGE_M), n)

    n_comp, labels = connected_components(edges, directed=False)
    largest = np.bincount(labels).max()
    logger.info(
        "Road graph: %d nodes, %d edges, %d components, %.2f%% in the largest",
        n, int(real.sum()), n_comp, 100 * largest / n,
    )
    return RoadGraph(node_xy=node_xy, edges=edges, tree=cKDTree(node_xy))


def _min_duplicates(ia: np.ndarray, ib: np.ndarray, w: np.ndarray, n: int) -> csr_matrix:
    """CSR of ``w`` keyed by (ia, ib), keeping the MINIMUM of duplicate pairs."""
    key = ia.astype(np.int64) * n + ib
    order = np.lexsort((w, key))
    key, w = key[order], w[order]
    first = np.ones(len(key), dtype=bool)
    first[1:] = key[1:] != key[:-1]
    key, w = key[first], w[first]
    return coo_matrix((w, (key // n, key % n)), shape=(n, n)).tocsr()


def _snap(graph: RoadGraph, lon: np.ndarray, lat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Nearest graph node per lon/lat point, with the offset to reach it (metres)."""
    x, y = _TO_ALBERTA.transform(np.asarray(lon, dtype=float), np.asarray(lat, dtype=float))
    offset, node = graph.tree.query(np.column_stack([x, y]))
    return node, offset


def network_distance_m(
    graph: RoadGraph,
    points: pd.DataFrame,
    amenities: pd.DataFrame,
    label: str,
) -> np.ndarray:
    """Road-network metres from each row of ``points`` to its nearest amenity.

    Both frames need ``latitude``/``longitude``. Returns a float array aligned to
    ``points``; ``NaN`` where no amenity is reachable (a disconnected fragment of
    the graph) — never a sentinel large number, which would read downstream as a
    real "far away".

    Both snap offsets are INCLUDED: the amenity's walk to the network and the
    property's walk from it. A station 90 m off the nearest centreline is 90 m
    away from a property standing on that centreline, not 0 m.
    """
    if amenities.empty:
        raise ValueError(f"{label}: no amenity points to measure to")
    a_node, a_offset = _snap(graph, amenities["longitude"], amenities["latitude"])
    far = a_offset > FAR_SNAP_WARN_M
    if far.any():
        logger.warning(
            "%s: %d amenity point(s) sit >%.0f m from any road (max %.0f m) — "
            "their offset is included, but check the graph covers that area",
            label, int(far.sum()), FAR_SNAP_WARN_M, float(a_offset.max()),
        )

    # One virtual source joined to every snapped amenity by its own offset turns
    # "nearest of many, each with its own head start" into a single Dijkstra.
    # min_only=True cannot do this: it would ignore the per-amenity offsets.
    n = graph.n_nodes
    src_w = np.maximum(a_offset, MIN_EDGE_M)
    order = np.argsort(src_w)
    a_node, src_w = a_node[order], src_w[order]
    # Two amenities can snap to the same node; sorted by offset, the first
    # occurrence is the shorter head start, and summing them would be wrong.
    _, keep = np.unique(a_node, return_index=True)
    base = graph.edges.tocoo()
    aug = coo_matrix(
        (
            np.concatenate([base.data, src_w[keep]]),
            (
                np.concatenate([base.row, np.full(len(keep), n)]),
                np.concatenate([base.col, a_node[keep]]),
            ),
        ),
        shape=(n + 1, n + 1),
    ).tocsr()

    dist_from_source = dijkstra(aug, directed=False, indices=n)[:n]

    p_node, p_offset = _snap(graph, points["longitude"], points["latitude"])
    far_p = p_offset > FAR_SNAP_WARN_M
    if far_p.any():
        logger.warning(
            "%s: %d point(s) sit >%.0f m from any road (max %.0f m) — offset "
            "included in the distance",
            label, int(far_p.sum()), FAR_SNAP_WARN_M, float(p_offset.max()),
        )
    out = dist_from_source[p_node] + p_offset
    unreachable = ~np.isfinite(out)
    if unreachable.any():
        logger.warning(
            "%s: %d of %d point(s) cannot reach any amenity over the road graph "
            "— emitted as null, not as a large number",
            label, int(unreachable.sum()), len(out),
        )
    out = np.where(unreachable, np.nan, out)
    finite = out[np.isfinite(out)]
    if len(finite):
        logger.info(
            "%s: median %.0f m, p90 %.0f m, max %.0f m over %d point(s) "
            "to %d amenity point(s)",
            label, float(np.median(finite)), float(np.percentile(finite, 90)),
            float(finite.max()), len(finite), len(amenities),
        )
    return out

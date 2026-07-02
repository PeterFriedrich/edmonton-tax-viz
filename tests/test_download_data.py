"""Tests for scripts/download_data.py — the Socrata $limit truncation check.

Socrata truncates silently at $limit (returns exactly that many features, no
error), so check_not_truncated must fail loudly at count == limit and pass
below it. Tests write small temp GeoJSON files; no network.
"""

import json
import sys

import pytest

sys.path.insert(0, "scripts")
from download_data import SOURCES, check_not_truncated, feature_count


def _geojson(tmp_path, n_features):
    p = tmp_path / "data.geojson"
    fc = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"i": i}, "geometry": None}
            for i in range(n_features)
        ],
    }
    p.write_text(json.dumps(fc))
    return p


def test_feature_count(tmp_path):
    assert feature_count(_geojson(tmp_path, 7)) == 7


def test_feature_count_empty(tmp_path):
    assert feature_count(_geojson(tmp_path, 0)) == 0


def test_under_limit_passes_and_returns_count(tmp_path):
    p = _geojson(tmp_path, 42)
    assert check_not_truncated("test", p, limit=100) == 42


def test_at_limit_raises(tmp_path):
    p = _geojson(tmp_path, 100)
    with pytest.raises(RuntimeError, match="truncated"):
        check_not_truncated("test", p, limit=100)


def test_error_names_the_source(tmp_path):
    p = _geojson(tmp_path, 5)
    with pytest.raises(RuntimeError, match="zoning"):
        check_not_truncated("zoning", p, limit=5)


def test_sources_limits_match_urls():
    """The declared 'limit' must equal the URL's $limit or the check is a lie."""
    for name, src in SOURCES.items():
        if "limit" in src:
            assert f"$limit={src['limit']}" in src["url"], name
        else:
            # No limit declared -> must be a full-export endpoint, not $limit'd.
            assert "$limit" not in src["url"], name

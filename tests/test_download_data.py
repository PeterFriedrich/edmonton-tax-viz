"""Tests for scripts/download_data.py — the two-tier truncation guard.

Tier 1: Socrata truncates silently at $limit (returns exactly that many
features, no error), so check_not_truncated must fail loudly at
count == limit and pass below it.
Tier 2: the post-download count must equal the live server count(*) —
catches truncation by any limit that isn't ours. Mismatch fails hard;
an unavailable server count only warns (soft-fail).

Tests write small temp files and monkeypatch the network; no real HTTP.
"""

import json
import sys

import pytest

sys.path.insert(0, "scripts")
import download_data
from download_data import (
    SOURCES,
    check_not_truncated,
    csv_record_count,
    feature_count,
    verify_download,
)


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


# --- local counting ---------------------------------------------------------


def test_feature_count(tmp_path):
    assert feature_count(_geojson(tmp_path, 7)) == 7


def test_feature_count_empty(tmp_path):
    assert feature_count(_geojson(tmp_path, 0)) == 0


def test_csv_record_count_excludes_header(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("a,b\n1,2\n3,4\n")
    assert csv_record_count(p) == 2


def test_csv_record_count_handles_quoted_newlines(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text('a,b\n1,"two\nlines"\n3,4\n')
    assert csv_record_count(p) == 2  # naive line counting would say 3


def test_csv_record_count_header_only(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("a,b\n")
    assert csv_record_count(p) == 0


# --- tier 1: our $limit -----------------------------------------------------


def test_under_limit_passes():
    check_not_truncated("test", 42, limit=100)  # no raise


def test_at_limit_raises():
    with pytest.raises(RuntimeError, match="truncated"):
        check_not_truncated("test", 100, limit=100)


def test_error_names_the_source():
    with pytest.raises(RuntimeError, match="zoning"):
        check_not_truncated("zoning", 5, limit=5)


# --- tier 2: server count(*) cross-check ------------------------------------


def _src(tmp_path, n, limit=None, count_url="http://x/count"):
    src = {"dest": _geojson(tmp_path, n)}
    if limit is not None:
        src["limit"] = limit
    if count_url is not None:
        src["count_url"] = count_url
    return src


def test_verify_passes_when_counts_match(tmp_path, monkeypatch):
    monkeypatch.setattr(download_data, "server_count", lambda url: 10)
    verify_download("test", _src(tmp_path, 10, limit=100))  # no raise


def test_verify_fails_on_server_mismatch(tmp_path, monkeypatch):
    """Server has more rows than we got — truncation by a limit that isn't ours."""
    monkeypatch.setattr(download_data, "server_count", lambda url: 50000)
    with pytest.raises(RuntimeError, match="server reports 50000"):
        verify_download("test", _src(tmp_path, 10, limit=100))


def test_verify_soft_fails_when_server_count_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(download_data, "server_count", lambda url: None)
    verify_download("test", _src(tmp_path, 10, limit=100))  # warn only, no raise


def test_verify_limit_check_runs_before_server_check(tmp_path, monkeypatch):
    """At our $limit it must fail even if the server count is unavailable."""
    monkeypatch.setattr(download_data, "server_count", lambda url: None)
    with pytest.raises(RuntimeError, match="truncated"):
        verify_download("test", _src(tmp_path, 100, limit=100))


def test_verify_csv_source_uses_record_count(tmp_path, monkeypatch):
    p = tmp_path / "data.csv"
    p.write_text("a,b\n1,2\n3,4\n")
    monkeypatch.setattr(download_data, "server_count", lambda url: 2)
    verify_download("assessment", {"dest": p, "count_url": "http://x"})  # no raise
    monkeypatch.setattr(download_data, "server_count", lambda url: 3)
    with pytest.raises(RuntimeError, match="server reports 3"):
        verify_download("assessment", {"dest": p, "count_url": "http://x"})


# --- SOURCES config invariants ----------------------------------------------


def test_sources_limits_match_urls():
    """The declared 'limit' must equal the URL's $limit or the check is a lie."""
    for name, src in SOURCES.items():
        if "limit" in src:
            assert f"$limit={src['limit']}" in src["url"], name
        else:
            # No limit declared -> must be a full-export endpoint, not $limit'd.
            assert "$limit" not in src["url"], name


def test_all_sources_have_count_url():
    for name, src in SOURCES.items():
        assert "count_url" in src, name
        assert "$select=count(*)" in src["count_url"], name

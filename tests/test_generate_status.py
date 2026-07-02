"""Tests for scripts/generate_status.py — the status manifest / heartbeat logic.

The interesting behaviour is in build_status(): the two-timestamp split
(generated only bumps on real content change; last_checked bumps every run) and
the banner preserve/set/clear rules. Everything keys off a content hash of the
GeoJSON, so tests write a small temp file and vary its bytes.
"""

import sys

sys.path.insert(0, "scripts")
from generate_status import _SENTINEL, build_status, content_hash, load_prior


def _geojson(tmp_path, text="{}"):
    p = tmp_path / "data.geojson"
    p.write_text(text)
    return p


def _build(gj, prior, **kw):
    defaults = dict(
        geojson=gj, prior=prior, today="2026-07-01",
        data_year=2025, rate_year=2025, zoning_year=2024,
    )
    defaults.update(kw)
    return build_status(**defaults)


def test_first_run_generates_today(tmp_path):
    """No prior manifest → generated and last_checked both today; banner null."""
    gj = _geojson(tmp_path)
    s = _build(gj, prior={})
    assert s["generated"] == "2026-07-01"
    assert s["last_checked"] == "2026-07-01"
    assert s["banner"] is None
    assert s["data_year"] == 2025 and s["rate_year"] == 2025 and s["zoning_year"] == 2024
    assert s["_geojson_sha256"] == content_hash(gj)


def test_unchanged_data_preserves_generated(tmp_path):
    """Same content hash as prior → generated keeps the old date, heartbeat moves."""
    gj = _geojson(tmp_path, '{"a":1}')
    prior = {"generated": "2025-01-15", "_geojson_sha256": content_hash(gj)}
    s = _build(gj, prior=prior, today="2026-07-01")
    assert s["generated"] == "2025-01-15"       # unchanged data → not bumped
    assert s["last_checked"] == "2026-07-01"     # heartbeat always moves


def test_changed_data_bumps_generated(tmp_path):
    """Content hash differs from prior → generated bumps to today."""
    gj = _geojson(tmp_path, '{"a":2}')
    prior = {"generated": "2025-01-15", "_geojson_sha256": "stale-hash"}
    s = _build(gj, prior=prior, today="2026-07-01")
    assert s["generated"] == "2026-07-01"


def test_banner_preserved_by_default(tmp_path):
    """banner=_SENTINEL (flag not passed) → keep whatever the prior had."""
    gj = _geojson(tmp_path)
    prior = {"banner": "Holding — 2026 rates pending", "_geojson_sha256": content_hash(gj)}
    s = _build(gj, prior=prior, banner=_SENTINEL)
    assert s["banner"] == "Holding — 2026 rates pending"


def test_banner_set(tmp_path):
    gj = _geojson(tmp_path)
    s = _build(gj, prior={}, banner="New notice")
    assert s["banner"] == "New notice"


def test_banner_cleared(tmp_path):
    """Explicit None clears a prior banner (the --clear-banner path)."""
    gj = _geojson(tmp_path)
    prior = {"banner": "old", "_geojson_sha256": content_hash(gj)}
    s = _build(gj, prior=prior, banner=None)
    assert s["banner"] is None


def test_load_prior_missing_and_corrupt(tmp_path):
    """Absent file → {}; unreadable/corrupt JSON → {} (fresh), never raises."""
    assert load_prior(tmp_path / "nope.json") == {}
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert load_prior(bad) == {}

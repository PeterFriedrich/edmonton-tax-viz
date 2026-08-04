"""Tests for scripts/generate_status.py — the status manifest / heartbeat logic.

The interesting behaviour is in build_status(): the two-timestamp split
(generated only bumps on real content change; last_checked bumps every run) and
the banner preserve/set/clear rules. Everything keys off a content hash of the
GeoJSON, so tests write a small temp file and vary its bytes.
"""

import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, "scripts")
from generate_status import (
    _SENTINEL,
    DISPLAY_RATE_CLASSES,
    MILL_RATES,
    ROOT,
    build_status,
    content_hash,
    load_prior,
    municipal_rates,
)


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


# ---- municipal_rates: the frontend's mill-rate pod ---------------------------

def _rates_file(tmp_path, year="2025", extra=None):
    rates = {
        "Residential": {"municipal": 7.0, "education": 2.0},
        "Other Residential": {"municipal": 8.0, "education": 2.0},
        "Non Residential": {"municipal": 24.0, "education": 4.0},
    }
    rates.update(extra or {})
    p = tmp_path / "mill_rates.json"
    p.write_text(json.dumps({"rates": {year: rates}}))
    return p


def test_municipal_rates_publishes_the_three_display_classes(tmp_path):
    """Municipal rate only, in display order — education is provincial, excluded."""
    r = municipal_rates(_rates_file(tmp_path), 2025)
    assert [c["name"] for c in r["classes"]] == DISPLAY_RATE_CLASSES
    assert [c["rate"] for c in r["classes"]] == [7.0, 8.0, 24.0]
    assert r["assumed"] == []


def test_municipal_rates_reports_assumed_classes(tmp_path):
    """An _assumed marker in the source surfaces as data, not as UI copy.

    2025 Farmland is inferred (no row published), and the caveat the pod prints
    must disappear on its own the year a real row appears.
    """
    p = _rates_file(tmp_path, extra={"Farmland": {"municipal": 7.0, "_assumed": "why"}})
    assert municipal_rates(p, 2025)["assumed"] == ["Farmland"]


def test_municipal_rates_missing_display_class_raises(tmp_path):
    """A dropped class must fail loudly — a pod short one rate reads as fact."""
    p = _rates_file(tmp_path)
    data = json.loads(p.read_text())
    del data["rates"]["2025"]["Non Residential"]
    p.write_text(json.dumps(data))
    with pytest.raises(KeyError, match="Non Residential"):
        municipal_rates(p, 2025)


def test_municipal_rates_absent_year_degrades_to_none(tmp_path):
    """No rates for the year → None, so the pod simply never shows."""
    assert municipal_rates(_rates_file(tmp_path), 2099) is None
    assert municipal_rates(tmp_path / "nope.json", 2025) is None


def test_build_status_carries_the_rates(tmp_path):
    s = _build(_geojson(tmp_path), prior={}, rates_path=_rates_file(tmp_path))
    assert s["municipal_rates"]["classes"][0]["rate"] == 7.0


def test_committed_status_matches_the_rate_source():
    """web/data/status.json is hand-maintained between refreshes — keep it honest.

    The pod ships before the next auto-refresh regenerates the manifest, so the
    committed copy must already equal what the generator would write.
    """
    committed = json.loads((ROOT / "web/data/status.json").read_text())
    assert committed["municipal_rates"] == municipal_rates(MILL_RATES, committed["rate_year"])


# ---- budget_context: the Data & Methods pod's citywide scale section ---------
# Mirrors municipal_rates: values only, degrades to None, validates loudly.

def _budget_file(tmp_path, total=1000, cats=None):
    p = tmp_path / "budget.json"
    p.write_text(json.dumps({
        "total_operating_budget": {"value": total, "year": 2025},
        "categories": cats if cats is not None else [
            {"key": "transit", "label": "Transit", "value": 120},
            {"key": "roads", "label": "Roads", "value": 30, "derived_component": "maintenance"},
        ],
    }))
    return p


def test_budget_context_publishes_values_and_total():
    from generate_status import budget_context

    b = budget_context()
    assert b["total"] == 3_845_555_000
    keys = [c["key"] for c in b["categories"]]
    assert keys == ["transit", "roads", "active_transport", "sidewalks"]


def test_budget_context_publishes_no_share_or_ratio(tmp_path):
    """⚠️ The manifest must carry dollars only.

    A precomputed share can drift out of agreement with the value it came from —
    which is exactly how the source research shipped 'transit is ~15x roads'
    when it is 9.2x. The UI divides by total itself.
    """
    from generate_status import budget_context

    b = budget_context(_budget_file(tmp_path))
    for c in b["categories"]:
        assert set(c) == {"key", "label", "value", "derived"}
    assert not any(k in b for k in ("shares", "ratios", "percentages"))


def test_budget_context_flags_the_derived_category(tmp_path):
    from generate_status import budget_context

    b = budget_context(_budget_file(tmp_path))
    assert {c["key"]: c["derived"] for c in b["categories"]} == {"transit": False, "roads": True}


def test_budget_context_missing_file_degrades_to_none(tmp_path):
    from generate_status import budget_context

    assert budget_context(tmp_path / "nope.json") is None


def test_budget_context_malformed_degrades_to_none(tmp_path):
    from generate_status import budget_context

    bad = tmp_path / "budget.json"
    bad.write_text("{not json")
    assert budget_context(bad) is None


def test_budget_context_category_exceeding_total_raises(tmp_path):
    """A category bigger than the whole budget is a decimal-place slip."""
    from generate_status import budget_context

    p = _budget_file(tmp_path, total=100, cats=[{"key": "transit", "label": "T", "value": 200}])
    with pytest.raises(ValueError, match="exceed"):
        budget_context(p)


def test_budget_context_nonpositive_value_raises(tmp_path):
    from generate_status import budget_context

    p = _budget_file(tmp_path, cats=[{"key": "transit", "label": "T", "value": 0}])
    with pytest.raises(ValueError, match="bad value"):
        budget_context(p)


def test_committed_budget_file_components_reconcile():
    """Each category's components must sum to the value the pod prints."""
    data = json.loads(Path("data/city_budget_context.json").read_text())
    for c in data["categories"]:
        if "components" in c:
            assert sum(c["components"].values()) == c["value"], c["key"]


def test_committed_budget_file_shares_are_what_we_claim():
    """Pins the four shares the pod renders, so a hand edit to the JSON that
    changes the story fails here rather than shipping quietly."""
    data = json.loads(Path("data/city_budget_context.json").read_text())
    total = data["total_operating_budget"]["value"]
    got = {c["key"]: round(100 * c["value"] / total, 2) for c in data["categories"]}
    assert got == {"transit": 12.18, "roads": 1.33, "active_transport": 0.79, "sidewalks": 0.15}

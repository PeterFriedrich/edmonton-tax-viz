"""Tests for scripts/export_budget_ranked.py (ranked branch operating budget).

No network: the four fetch helpers are monkeypatched, and ``build()`` — which
holds the classification and every guard — is exercised on hand-built category
mixes. The guards are the point of the module, so most of these assert that a
malformed source is REFUSED rather than published.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import export_budget_ranked as e  # noqa: E402


# A branch that buys people and things, and one that only moves money.
SERVICE_MIX = {"Personnel": 100.0, "Materials, Goods and Supplies": 20.0}
FINANCING_MIX = {"Tax-supported Debt Charges": 500.0, "Pay As You Go Funding": 50.0}


def wire(monkeypatch, by_branch, *, years=(2025, 2026), total=None):
    """Point the module's four fetch helpers at fixtures instead of Socrata."""
    if total is None:
        total = sum(sum(c.values()) for c in by_branch.values())
    monkeypatch.setattr(e, "available_years", lambda: list(years))
    monkeypatch.setattr(e, "branch_categories", lambda y, f: by_branch)
    monkeypatch.setattr(e, "fund_total", lambda y, f: total)
    monkeypatch.setattr(e, "source_vintage", lambda: {
        "dataset_id": e.DATASET_ID, "rows_updated_at": "2026-06-05",
    })


def test_splits_by_category_mix_not_by_branch_name(monkeypatch):
    wire(monkeypatch, {
        "Police Service": SERVICE_MIX,
        "Capital Project Financing": FINANCING_MIX,
    })
    out = e.build(2026)
    assert [r["branch"] for r in out["services"]] == ["Police Service"]
    assert [r["branch"] for r in out["other"]] == ["Capital Project Financing"]


def test_a_renamed_financing_branch_still_classifies_as_other(monkeypatch):
    """The budget tree gets re-cut (DATA.md §17). A name list would break here."""
    wire(monkeypatch, {
        "Police Service": SERVICE_MIX,
        "Corporate Financing and Capital Funding": FINANCING_MIX,  # invented name
    })
    out = e.build(2026)
    assert [r["branch"] for r in out["other"]] == ["Corporate Financing and Capital Funding"]


def test_a_branch_with_any_service_dollars_is_a_service(monkeypatch):
    """One service category is enough — grant-funded branches still deliver."""
    wire(monkeypatch, {
        "Public Library": {"External Services": 75.0, "Transfer to Reserves": 5.0},
        "Capital Project Financing": FINANCING_MIX,
    })
    out = e.build(2026)
    assert [r["branch"] for r in out["services"]] == ["Public Library"]


def test_transfer_to_reserves_does_not_strip_a_service_branch(monkeypatch):
    """`Transfer to Reserves` spans 11 branches incl. Police — classifying by
    category rather than by branch would have removed dollars from services."""
    wire(monkeypatch, {
        "Police Service": {**SERVICE_MIX, "Transfer to Reserves": 14.0},
        "Capital Project Financing": FINANCING_MIX,
    })
    out = e.build(2026)
    police = next(r for r in out["services"] if r["branch"] == "Police Service")
    assert police["budget"] == pytest.approx(134.0)


def test_each_block_is_ranked_descending(monkeypatch):
    wire(monkeypatch, {
        "Small Service": {"Personnel": 1.0},
        "Big Service": {"Personnel": 900.0},
        "Small Other": {"Pay As You Go Funding": 2.0},
        "Big Other": {"Tax-supported Debt Charges": 700.0},
    })
    out = e.build(2026)
    assert [r["branch"] for r in out["services"]] == ["Big Service", "Small Service"]
    assert [r["branch"] for r in out["other"]] == ["Big Other", "Small Other"]


def test_totals_reconcile_with_the_independently_queried_fund_total(monkeypatch):
    wire(monkeypatch, {"A": SERVICE_MIX, "B": FINANCING_MIX})
    out = e.build(2026)
    assert out["services_total"] + out["other_total"] == pytest.approx(out["total"])


def test_publishes_no_share_or_ratio(monkeypatch):
    """Shares are computed in the front end, so the two can never disagree —
    the same rule city_budget_context.json follows."""
    wire(monkeypatch, {"A": SERVICE_MIX, "B": FINANCING_MIX})
    out = e.build(2026)
    for row in out["services"] + out["other"]:
        assert set(row) == {"branch", "budget"}
    blob = repr(out).lower()
    assert "share" not in blob and "percent" not in blob


# ---- the guards: a malformed source must be refused, not published ----------

def test_dropped_branch_fails_reconciliation(monkeypatch):
    """A paging cutoff or a lost branch shows up here and nowhere else."""
    wire(monkeypatch, {"A": SERVICE_MIX, "B": FINANCING_MIX}, total=99_999.0)
    with pytest.raises(SystemExit, match="do not reconcile"):
        e.build(2026)


def test_negative_branch_total_is_refused(monkeypatch):
    wire(monkeypatch, {"A": SERVICE_MIX, "Odd": {"Intra-municipal Recoveries": -5.0}})
    with pytest.raises(SystemExit, match="negative branch totals"):
        e.build(2026)


def test_classification_collapse_is_refused(monkeypatch):
    """If the category vocabulary is re-cut, every branch lands on one side."""
    wire(monkeypatch, {"A": SERVICE_MIX, "B": {"Personnel": 5.0}})
    with pytest.raises(SystemExit, match="classification collapsed"):
        e.build(2026)


def test_unknown_year_is_refused(monkeypatch):
    wire(monkeypatch, {"A": SERVICE_MIX, "B": FINANCING_MIX})
    with pytest.raises(SystemExit, match="not in"):
        e.build(1999)


def test_empty_source_is_refused(monkeypatch):
    wire(monkeypatch, {}, total=0.0)
    with pytest.raises(SystemExit, match="no rows"):
        e.build(2026)

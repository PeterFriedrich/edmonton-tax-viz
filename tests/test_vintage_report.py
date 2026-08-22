"""Tests for the monthly vintage digest (scripts/vintage_report.py).

The digest's whole value is that it goes RED when something has gone stale, so
these tests are mostly falsification: each check is driven into its ACTION path
with a fixture and asserted to fire. An all-green report that cannot go red is
worse than no report, because it reads as reassurance.

The two network-backed checks are exercised through injected fixtures rather
than live calls — CI must not depend on Socrata being up to test our own logic.
"""
import datetime as dt
import json

import pytest

from scripts import vintage_report as vr


@pytest.fixture
def pinned(monkeypatch):
    """Pin main.py's years to a known state; return the pinned assessment year."""
    import main
    monkeypatch.setattr(main, "ASSESSMENT_YEAR", 2025)
    monkeypatch.setattr(main, "FIRE_YEARS", (2023, 2024, 2025))
    monkeypatch.setattr(main, "PERMIT_YEARS", (2021, 2022, 2023, 2024, 2025))
    monkeypatch.setattr(main, "PERMIT_YEARS_RECENT", (2023, 2024, 2025))
    return 2025


def _write(tmp_path, name, payload):
    p = tmp_path / name
    p.write_text(json.dumps(payload))
    return p


# --- mill rates -------------------------------------------------------------

def test_mill_rates_flags_a_newer_published_year(pinned, tmp_path, monkeypatch):
    """The case this whole script was written for: rates published before the roll."""
    monkeypatch.setattr(vr, "MILL_RATES", _write(tmp_path, "m.json", {"rates": {"2025": {}}}))
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp([{"tax_year": "2025"}, {"tax_year": "2026"}]))
    status, _, detail = vr.check_mill_rates()
    assert status == vr.ACTION
    assert "2026" in detail


def test_mill_rates_ignores_unheld_history(pinned, tmp_path, monkeypatch):
    """The file deliberately carries no history — 2014-2024 must not read as work."""
    monkeypatch.setattr(vr, "MILL_RATES",
                        _write(tmp_path, "m.json", {"rates": {"2025": {}, "2026": {}}}))
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp([{"tax_year": str(y)}
                                                   for y in range(2014, 2027)]))
    status, _, _ = vr.check_mill_rates()
    assert status == vr.OK


def test_mill_rates_flags_a_missing_pinned_year(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "MILL_RATES", _write(tmp_path, "m.json", {"rates": {"2019": {}}}))
    status, _, detail = vr.check_mill_rates()
    assert status == vr.ACTION
    assert "no 2025 block" in detail


def test_mill_rates_network_failure_is_unknown_not_action(pinned, tmp_path, monkeypatch):
    """A guard must not manufacture an alarm out of an unreachable source."""
    monkeypatch.setattr(vr, "MILL_RATES", _write(tmp_path, "m.json", {"rates": {"2025": {}}}))
    monkeypatch.setattr(vr.requests, "get", _boom)
    status, _, _ = vr.check_mill_rates()
    assert status == vr.UNKNOWN


# --- the local-state checks -------------------------------------------------

def test_stormwater_flags_a_missing_pinned_year(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "STORMWATER_RATES", _write(tmp_path, "s.json", {"years": {"2019": {}}}))
    assert vr.check_stormwater()[0] == vr.ACTION


def test_stormwater_ok_when_pinned_year_present(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "STORMWATER_RATES",
                        _write(tmp_path, "s.json", {"years": {"2025": {}, "2026": {}}}))
    assert vr.check_stormwater()[0] == vr.OK


def test_temporal_archive_flags_an_uncaptured_live_year(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "TEMPORAL_ARCHIVE", _write(tmp_path, "a.json", {"years": {"2019": {}}}))
    assert vr.check_temporal_archive()[0] == vr.ACTION


def test_banner_flags_a_live_banner(tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "STATUS_JSON", _write(tmp_path, "st.json", {"banner": "Showing 2025 …"}))
    status, _, detail = vr.check_banner()
    assert status == vr.ACTION
    assert "Showing 2025" in detail


def test_banner_ok_when_null(tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "STATUS_JSON", _write(tmp_path, "st.json", {"banner": None}))
    assert vr.check_banner()[0] == vr.OK


# --- the January pins -------------------------------------------------------

def test_window_pins_ok_before_the_roll(pinned):
    """During 2026, windows ending 2025 are current — 2026 is not a full year yet."""
    assert vr.check_window_pins(today=dt.date(2026, 8, 6))[0] == vr.OK


def test_window_pins_fire_once_the_year_completes(pinned):
    status, _, detail = vr.check_window_pins(today=dt.date(2027, 1, 15))
    assert status == vr.ACTION
    for name in ("FIRE_YEARS", "PERMIT_YEARS", "PERMIT_YEARS_RECENT"):
        assert name in detail


def test_year_constants_flag_drift(monkeypatch):
    """RUNBOOK §1 step 6: these are separate constants and forgetting them is silent."""
    import main
    monkeypatch.setattr(main, "ASSESSMENT_YEAR", 2026)  # generate_status still says 2025
    status, _, detail = vr.check_year_constants()
    assert status == vr.ACTION
    assert "DATA_YEAR" in detail


# --- rendering --------------------------------------------------------------

def test_render_leads_with_action_items():
    results = [(vr.OK, "fine", "d"), (vr.ACTION, "broken", "d"), (vr.OK, "also fine", "d")]
    body, n = vr.render(results, today=dt.date(2026, 8, 6))
    assert n == 1
    assert "1 item(s) need attention" in body
    # ACTION rows sort to the top so the digest is skimmable in a notification.
    assert body.index("broken") < body.index("fine")


def test_render_says_so_when_all_green():
    body, n = vr.render([(vr.OK, "a", "d")], today=dt.date(2026, 8, 6))
    assert n == 0
    assert "Nothing needs attention" in body


def test_a_raising_check_does_not_kill_the_digest(monkeypatch):
    monkeypatch.setattr(vr, "CHECKS", (_boom_check, lambda: (vr.OK, "fine", "d")))
    results = vr.run_all()
    assert len(results) == 2
    assert vr.UNKNOWN in [r[0] for r in results]


_CAP_HEADER = ("fiscal_year,service,branch,profile_id,profile,"
               "fund_type,fund,approved\n")
_CAP_BODY = ("2023,Roads,Infrastructure Delivery,23-40-9033,Ottewell,"
             "Grants,Fed,100.00\n"
             "2024,Roads,Infrastructure Delivery,CM-25-0000,Renewal,"
             "Reserves,Res,250.00\n")
_CAP = _CAP_HEADER + _CAP_BODY


class _FakeTextResp:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


def _cap_local(monkeypatch, tmp_path, text):
    f = tmp_path / "capital_budget.csv"
    f.write_text(text)
    monkeypatch.setattr(vr, "CAPITAL_BUDGET", f)


def test_capital_budget_ok_when_upstream_matches(monkeypatch, tmp_path):
    _cap_local(monkeypatch, tmp_path, _CAP)
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(_CAP))
    status, _, detail = vr.check_capital_budget()
    assert status == vr.OK
    assert "2 rows" in detail.replace(",", "")


def test_capital_budget_fires_when_upstream_moves(monkeypatch, tmp_path):
    _cap_local(monkeypatch, tmp_path, _CAP)
    moved = _CAP + ("2027,Roads,Infrastructure Delivery,27-00-0001,New,"
                    "Grants,Fed,500.00\n")
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(moved))
    status, _, detail = vr.check_capital_budget()
    assert status == vr.ACTION
    assert "+1" in detail and "+500" in detail


def test_capital_budget_ignores_row_order(monkeypatch, tmp_path):
    """⚠️ The endpoint is generated per request behind no-cache, so a server-side
    reorder must NOT read as a budget change. Hashing raw bytes would."""
    _cap_local(monkeypatch, tmp_path, _CAP)
    lines = _CAP_BODY.splitlines()
    reordered = _CAP_HEADER + "\n".join(reversed(lines)) + "\n"
    assert reordered != _CAP
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(reordered))
    assert vr.check_capital_budget()[0] == vr.OK


def test_capital_budget_unreachable_is_unknown_not_action(monkeypatch, tmp_path):
    """A guard must never manufacture an alarm out of an unreachable source."""
    _cap_local(monkeypatch, tmp_path, _CAP)
    monkeypatch.setattr(vr.requests, "get", _boom)
    assert vr.check_capital_budget()[0] == vr.UNKNOWN


def test_capital_budget_wrong_shape_is_unknown(monkeypatch, tmp_path):
    """A 404 HTML page parses as CSV without raising — the header check catches it."""
    _cap_local(monkeypatch, tmp_path, _CAP)
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeTextResp("<!DOCTYPE html><html>404"))
    assert vr.check_capital_budget()[0] == vr.UNKNOWN


def test_capital_budget_missing_local_copy_is_unknown(monkeypatch, tmp_path):
    monkeypatch.setattr(vr, "CAPITAL_BUDGET", tmp_path / "absent.csv")
    assert vr.check_capital_budget()[0] == vr.UNKNOWN


def test_committed_capital_budget_parses():
    """The real committed file must satisfy the fingerprint's own header contract."""
    n, total, digest = vr._capital_fingerprint(vr.CAPITAL_BUDGET.read_text())
    assert n > 1000
    assert total > 1e9
    assert len(digest) == 64


class _FakeResp:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def _boom(*a, **k):
    raise RuntimeError("network down")


def _boom_check():
    raise RuntimeError("this check is broken")

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
    # Any year generate_status.py's DATA_YEAR/RATE_YEAR do NOT carry. Kept
    # relative to the real pin so the 2026 roll (or the next one) can't make
    # this assert a no-drift case again, which is how it broke on 2026-08-25.
    monkeypatch.setattr(main, "ASSESSMENT_YEAR", main.ASSESSMENT_YEAR + 1)
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


# --- archived years measure as filed ----------------------------------------
#
# The sibling check (check_temporal_archive) confirms the live year was
# CAPTURED and was green throughout the 2026-07-28 defect, because the capture
# did happen — it just captured the wrong year. These tests drive the
# correctness half, so a mislabelled entry cannot go quiet the same way.

def _archive(tmp_path, years):
    """years: {year: residential_base}. Shape matches temporal_archive.json."""
    payload = {"years": {
        str(y): {"SOME HOOD": {"RESIDENTIAL": [100, base]}}
        for y, base in years.items()
    }}
    return _write(tmp_path, "arch.json", payload)


def _fir(tmp_path, years):
    """A FIR tax-base file shaped as filed_bases() reads it: years -> assessment."""
    return _write(tmp_path, "fir.json", {
        "years": {str(y): {"assessment": {"residential": v}} for y, v in years.items()}
    })


def test_archived_year_measuring_as_another_year_fires(tmp_path, monkeypatch):
    """The exact 2026-07-28 defect: the 2026 roll filed under the label 2025."""
    fir = _fir(tmp_path, {2025: 148_130_000_000, 2026: 160_370_000_000})
    monkeypatch.setattr(vr, "FIR_TAX_BASE", fir)
    # Filed as 2025, but the value is unmistakably the 2026 base.
    monkeypatch.setattr(vr, "TEMPORAL_ARCHIVE",
                        _archive(tmp_path, {2025: 162_255_000_000}))
    status, _, detail = vr.check_temporal_archive_year()
    assert status == vr.ACTION
    assert "2026 roll" in detail


def test_archived_year_matching_its_label_is_ok(tmp_path, monkeypatch):
    fir = _fir(tmp_path, {2025: 148_130_000_000, 2026: 160_370_000_000})
    monkeypatch.setattr(vr, "FIR_TAX_BASE", fir)
    monkeypatch.setattr(vr, "TEMPORAL_ARCHIVE",
                        _archive(tmp_path, {2026: 162_264_000_000}))
    status, _, detail = vr.check_temporal_archive_year()
    assert status == vr.OK
    # A green over ONE year must carry its own caveat — a bare tick reads far
    # stronger than a population of 1 supports.
    assert "thin population" in detail


def test_archived_year_outside_fir_range_is_named_never_counted(tmp_path, monkeypatch):
    """An unverifiable year silently reading as verified is the defect's own shape."""
    fir = _fir(tmp_path, {2025: 148_130_000_000, 2026: 160_370_000_000})
    monkeypatch.setattr(vr, "FIR_TAX_BASE", fir)
    monkeypatch.setattr(vr, "TEMPORAL_ARCHIVE",
                        _archive(tmp_path, {2031: 200_000_000_000}))
    status, _, detail = vr.check_temporal_archive_year()
    assert status == vr.UNKNOWN
    assert "NOT CHECKED" in detail and "2031" in detail


# --- the roll-year check must not cry wolf on stale metadata ----------------

def test_stale_coverage_string_is_unknown_not_action(pinned, monkeypatch):
    """⚠️ REGRESSION. Edmonton's `Period of Coverage` sat a year stale through the
    whole 2026 roll. This check compared `detected == pinned` itself, bypassing
    check_alignment()'s stale-metadata downgrade (DECISIONS.md 2026-08-25), so it
    reported "roll has moved to 2025, pin is still 2026" — telling Peter to redo a
    year-roll already done, once a month, in the only channel that reaches him.
    """
    import main
    monkeypatch.setattr(main, "ASSESSMENT_YEAR", dt.date.today().year)
    monkeypatch.setattr(vr, "parse_coverage_year", None, raising=False)
    monkeypatch.setattr(
        vr.requests, "get",
        lambda *a, **k: type("R", (), {"json": lambda self: {"metadata": {"custom_fields": {
            "Time Frame": {"Period of Coverage":
                           f"{dt.date.today().year - 1}-01-01 to "
                           f"{dt.date.today().year - 1}-12-31"}}}}})(),
    )
    status, _, detail = vr.check_assessment_roll()
    assert status == vr.UNKNOWN, f"stale metadata must not fire an ACTION: {detail}"
    assert "not being kept current" in detail


def test_both_archive_checks_are_registered():
    """⚠️ The digest is wired by MEMBERSHIP, not by a workflow step — so this list
    is the whole wiring, and dropping a name from it is silent. Both archive
    checks must be here: `check_temporal_archive` (was the year CAPTURED) and
    `check_temporal_archive_year` (does a captured year MEASURE as its label).
    The first was green throughout the defect the second exists to catch.
    """
    assert vr.check_temporal_archive in vr.CHECKS
    assert vr.check_temporal_archive_year in vr.CHECKS


# --- unclassified zoning ----------------------------------------------------

def _served(tmp_path, rows):
    return _write(tmp_path, "served.geojson", {"features": [
        {"properties": {"neighbourhood_name": n, "frac_other": v}} for n, v in rows]})


def test_unclassified_zoning_ok_when_everything_classifies(tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "SERVED_GEOJSON",
                        _served(tmp_path, [("A", 0.0), ("B", 0.0)]))
    status, _, detail = vr.check_unclassified_zoning()
    assert status == vr.OK
    assert "2 hoods" in detail


def test_unclassified_zoning_fires_and_names_the_worst(tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "SERVED_GEOJSON",
                        _served(tmp_path, [("A", 0.0), ("B", 0.02), ("C", 0.31)]))
    status, _, detail = vr.check_unclassified_zoning()
    assert status == vr.ACTION
    assert "1 of 3 hoods" not in detail and "2 of 3 hoods" in detail
    assert detail.index("C 31.0%") < detail.index("B 2.0%")  # worst first
    assert "ZONE_CATEGORY" in detail


def test_unclassified_zoning_treats_missing_column_as_zero(tmp_path, monkeypatch):
    """A pre-frac_other served file must not fire — absence is not a defect."""
    monkeypatch.setattr(vr, "SERVED_GEOJSON", _write(
        tmp_path, "served.geojson", {"features": [{"properties": {}}]}))
    assert vr.check_unclassified_zoning()[0] == vr.OK


def test_unclassified_zoning_check_is_registered():
    """Membership IS the wiring — see test_both_archive_checks_are_registered."""
    assert vr.check_unclassified_zoning in vr.CHECKS

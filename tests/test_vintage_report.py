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

import requests

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
    # ⚠️ Named BOTH, and derived, not typed: this asserted only `"DATA_YEAR" in
    # detail`, so dropping RATE_YEAR from the check's own tuple was green (S147
    # audit run 2, R4(2)). Reading the names off generate_status also means a
    # renamed constant reds here rather than passing on a stale literal.
    import scripts.generate_status as gs
    for name in ("DATA_YEAR", "RATE_YEAR"):
        assert hasattr(gs, name)
        assert name in detail, f"{name} drifted but the digest does not name it"


def test_year_constants_ok_when_all_three_agree(pinned, monkeypatch):
    """The opposite direction. Without it, a check hard-wired to ACTION passes
    the test above — the vacuity the sibling assertions in this suite exist for.

    ⚠️ `ZONING_YEAR` is deliberately NOT in this comparison: it is the bylaw
    year, not the roll year (`tests/test_generate_status.py`
    `test_zoning_year_is_the_bylaw_year_and_does_not_track_the_roll`, and
    `vr.check_zoning_bylaw` for the upstream half).

    ⚠️ Read the constants off `scripts.generate_status`, which is the module the
    check imports. `sys.path` carries BOTH `.` and `scripts/`, so `import
    generate_status` and `import scripts.generate_status` are two DIFFERENT
    module objects — monkeypatching the first would not touch what the check
    reads, and the patch would silently do nothing.
    """
    import main
    from scripts.generate_status import DATA_YEAR, RATE_YEAR
    assert DATA_YEAR == RATE_YEAR, "this test's premise; the drift case is above"
    monkeypatch.setattr(main, "ASSESSMENT_YEAR", DATA_YEAR)
    status, _, detail = vr.check_year_constants()
    assert status == vr.OK
    assert str(DATA_YEAR) in detail


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
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status

    def json(self):
        return self._payload

    def raise_for_status(self):
        """Present so a check that calls it is testable. An HTTP error must reach
        the check as an exception — i.e. UNKNOWN — not as a parsed error body."""
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")


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


# --- zoning bylaw -----------------------------------------------------------
#
# ⚠️ The subject is `status.json`'s published `zoning 2024`, which nothing
# measured (S147 audit run 2, R4(2)). There is no year field upstream to read:
# the bylaw's identity is its ZONE-CODE VOCABULARY, and `ZONE_CATEGORY` is this
# project's record of which bylaw it read. The pin on the constant itself lives
# in `tests/test_generate_status.py`.


def _zoning_rows(codes):
    return _FakeResp([{"zoning": c} for c in codes])


def _status(tmp_path, monkeypatch, year=2024):
    monkeypatch.setattr(vr, "STATUS_JSON", _write(tmp_path, "status.json",
                                                  {"zoning_year": year}))


def test_zoning_bylaw_ok_when_the_vocabulary_is_the_one_we_mapped(tmp_path, monkeypatch):
    from src.load_zoning import ZONE_CATEGORY
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _zoning_rows(sorted(ZONE_CATEGORY)))
    status, _, detail = vr.check_zoning_bylaw()
    assert status == vr.OK
    assert "2024" in detail


def test_zoning_bylaw_reads_the_base_code_not_the_suffixed_string(tmp_path, monkeypatch):
    """Upstream appends height/overlay suffixes (`RM h16`) and `load_zoning`
    keys on the first token. Splitting differently would report all 95 codes as
    unknown on a completely normal file."""
    from src.load_zoning import ZONE_CATEGORY
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _zoning_rows([f"{c} h16" for c in ZONE_CATEGORY]))
    assert vr.check_zoning_bylaw()[0] == vr.OK


def test_zoning_bylaw_flags_a_code_that_is_new_upstream(tmp_path, monkeypatch):
    from src.load_zoning import ZONE_CATEGORY
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _zoning_rows(list(ZONE_CATEGORY) + ["ZZQ"]))
    status, _, detail = vr.check_zoning_bylaw()
    assert status == vr.ACTION
    assert "ZZQ" in detail


def test_zoning_bylaw_flags_a_mapped_code_that_vanished(tmp_path, monkeypatch):
    """⚠️ The direction `check_unclassified_zoning` cannot see at all — it reads
    `frac_other` on the served file, and a code that DISAPPEARS contributes no
    unclassified area. Half of what a bylaw rename looks like."""
    from src.load_zoning import ZONE_CATEGORY
    _status(tmp_path, monkeypatch)
    kept = sorted(ZONE_CATEGORY)
    dropped = kept.pop()
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _zoning_rows(kept))
    status, _, detail = vr.check_zoning_bylaw()
    assert status == vr.ACTION
    assert dropped in detail and "GONE" in detail


def test_zoning_bylaw_says_the_constant_does_not_follow_the_roll(tmp_path, monkeypatch):
    """The digest must not invite the January bump it exists to prevent."""
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _zoning_rows(["RS", "ZZQ"]))
    _, _, detail = vr.check_zoning_bylaw()
    assert "ASSESSMENT_YEAR" in detail and "never" in detail


def test_zoning_bylaw_network_failure_is_unknown_not_action(tmp_path, monkeypatch):
    """A guard must not manufacture a bylaw change out of an unreachable source."""
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get", _boom)
    status, _, detail = vr.check_zoning_bylaw()
    assert status == vr.UNKNOWN
    assert "2024" in detail


def test_zoning_bylaw_empty_response_is_unknown_not_a_wholesale_rename(tmp_path, monkeypatch):
    """⚠️ The failure that would cry wolf hardest: a shape change empties every
    `zoning` field, and a naive set difference then reports all 95 mapped codes
    GONE — a bylaw replacement, from nothing but a renamed column."""
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _zoning_rows([""] * 40))
    assert vr.check_zoning_bylaw()[0] == vr.UNKNOWN


def test_zoning_bylaw_check_is_registered():
    """The digest is wired by MEMBERSHIP; dropping a name from CHECKS is silent."""
    assert vr.check_zoning_bylaw in vr.CHECKS


def test_zoning_bylaw_http_error_is_unknown_not_action(tmp_path, monkeypatch):
    _status(tmp_path, monkeypatch)
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp([{"zoning": "RS"}], status=503))
    assert vr.check_zoning_bylaw()[0] == vr.UNKNOWN


# --- road class vocabulary --------------------------------------------------
#
# ⚠️ The sibling failure to check_zoning_bylaw's, with one difference that
# matters: zoning's unmapped codes land in `frac_other` and are VISIBLE on the
# served file, while an unmapped road code is charged as `local` and is visible
# nowhere. `_classify` fails OPEN. The only prior signal was a log warning that
# had been firing on every run, unread, for two months.
#
# ⚠️ `test_every_alley_prefixed_code_is_the_alley_group` in test_load_roads.py
# must NOT be quoted as covering this: it iterates the keys that are PRESENT,
# so a missing key makes it vacuously true (measured 2026-09-09).

def _class_rows(codes, unclassed=0):
    """Socrata `$group` shape: one row per distinct value, `count_1` as a string."""
    rows = [{"functional_class_code": c, "count_1": "10"} for c in codes]
    if unclassed:
        rows.append({"functional_class_code": None, "count_1": str(unclassed)})
    return _FakeResp(rows)


def test_road_classes_ok_when_the_vocabulary_is_the_one_we_mapped(monkeypatch):
    from src.load_roads import CLASS_GROUP
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _class_rows(sorted(CLASS_GROUP)))
    status, _, detail = vr.check_road_classes()
    assert status == vr.OK
    assert str(len(CLASS_GROUP)) in detail


def test_road_classes_queries_the_population_the_classifier_actually_sees(monkeypatch):
    """⚠️ The defect this check exists for lives in a FILTERED subset. Measured
    2026-09-09: the unfiltered feed carries a 16th value (null, the Alley +
    Railway rows) that `_classify` never receives, so an unfiltered query
    reports drift in codes the classifier cannot reach. Asserting on the
    constants — not on the literal strings — also fails if a row filter moves
    and the check's population stops following it."""
    from src.load_roads import CENTERLINE_TYPE, CLASS_GROUP, RESPONSIBLE_PARTY
    seen = {}

    def _capture(*a, **k):
        seen.update(k.get("params") or {})
        return _class_rows(sorted(CLASS_GROUP))

    monkeypatch.setattr(vr.requests, "get", _capture)
    vr.check_road_classes()
    where = seen["$where"]
    assert f"centerline_type='{CENTERLINE_TYPE}'" in where
    assert f"responsible_party_description='{RESPONSIBLE_PARTY}'" in where
    assert seen["$group"] == "functional_class_code"


def test_road_classes_flags_a_code_that_is_new_upstream(monkeypatch):
    """`Alley-Commercial`, replayed: the exact event nothing detected."""
    from src.load_roads import CLASS_GROUP
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _class_rows(list(CLASS_GROUP) + ["Alley-Industrial"]))
    status, _, detail = vr.check_road_classes()
    assert status == vr.ACTION
    assert "Alley-Industrial" in detail and "UNMAPPED" in detail


def test_road_classes_says_an_unmapped_code_is_charged_not_dropped(monkeypatch):
    """⚠️ The half a reader gets backwards. `no silent data drops` reads as "the
    length went missing"; fail-open means the opposite — it is IN road_m_total,
    on the charged side. The digest must say which."""
    from src.load_roads import CLASS_GROUP, DEFAULT_GROUP
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _class_rows(list(CLASS_GROUP) + ["Alley-Industrial"]))
    _, _, detail = vr.check_road_classes()
    assert DEFAULT_GROUP in detail and "CHARGED" in detail


def test_road_classes_flags_a_mapped_code_that_vanished(monkeypatch):
    """Half of what a wholesale re-lettering looks like, and invisible from the
    served file — an absent code contributes no unclassified length."""
    from src.load_roads import CLASS_GROUP
    kept = sorted(CLASS_GROUP)
    dropped = kept.pop()
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _class_rows(kept))
    status, _, detail = vr.check_road_classes()
    assert status == vr.ACTION
    assert dropped in detail and "GONE" in detail


def test_road_classes_flags_an_unclassed_row_separately_from_a_new_code(monkeypatch):
    """A City road with a NULL class is a different defect from a new code — the
    fix is upstream, not a `CLASS_GROUP` entry — but it is charged as `local`
    the same way. Folding it into the new-code message would send the reader to
    the wrong place."""
    from src.load_roads import CLASS_GROUP
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _class_rows(sorted(CLASS_GROUP), unclassed=7))
    status, _, detail = vr.check_road_classes()
    assert status == vr.ACTION
    assert "7 row(s) carry NO" in detail
    assert "UNMAPPED" not in detail and "GONE" not in detail


def test_road_classes_empty_vocabulary_is_unknown_not_a_wholesale_rename(monkeypatch):
    """⚠️ The failure that would cry wolf hardest, and it must beat the null
    count to the return. A renamed/emptied column yields ONE null group; a naive
    reading reports every mapped code GONE *and* every city road unclassed —
    two alarms, both manufactured out of a shape change."""
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _class_rows([], unclassed=49000))
    status, _, detail = vr.check_road_classes()
    assert status == vr.UNKNOWN
    assert "GONE" not in detail


def test_road_classes_network_failure_is_unknown_not_action(monkeypatch):
    monkeypatch.setattr(vr.requests, "get", _boom)
    assert vr.check_road_classes()[0] == vr.UNKNOWN


def test_road_classes_http_error_is_unknown_not_action(monkeypatch):
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp([{"functional_class_code": "Local-Residential",
                                                    "count_1": "1"}], status=503))
    assert vr.check_road_classes()[0] == vr.UNKNOWN


def test_road_classes_check_is_registered():
    """The digest is wired by MEMBERSHIP; dropping a name from CHECKS is silent."""
    assert vr.check_road_classes in vr.CHECKS


# --- TODO branch refs (the mechanical half of backlog staleness) -------------
#
# Added 2026-09-16 after a hand sample of 15 open items untouched >60 days found
# 7 stale (47%). Two were this exact shape, and the scan then found a third the
# sample had missed. These tests drive every branch of it, because the check's
# whole value is going red.

class _FakeProc:
    def __init__(self, stdout="", returncode=0, stderr=""):
        self.stdout, self.returncode, self.stderr = stdout, returncode, stderr


def _remote(*branches):
    return "\n".join(f"abc123\trefs/heads/{b}" for b in branches)


def _todo(monkeypatch, tmp_path, text, remote=_remote("master", "feature/live")):
    (tmp_path / "TODO.md").write_text(text)
    monkeypatch.setattr(vr, "TODO_MD", tmp_path / "TODO.md")
    monkeypatch.setattr(vr.subprocess, "run", lambda *a, **k: _FakeProc(remote))
    return vr.check_todo_branch_refs()


def test_todo_branch_fires_on_a_deleted_branch(monkeypatch, tmp_path):
    status, _, detail = _todo(
        monkeypatch, tmp_path,
        "- [ ] **Stormwater** — v1 built on `feature/stormwater-lens` (unmerged).\n")
    assert status == vr.ACTION
    assert "feature/stormwater-lens" in detail and "line 1" in detail


def test_todo_branch_ok_when_the_branch_is_live(monkeypatch, tmp_path):
    assert _todo(monkeypatch, tmp_path,
                 "- [ ] Work in progress on `feature/live`.\n")[0] == vr.OK


def test_todo_branch_ignores_closed_items(monkeypatch, tmp_path):
    """A finished item naming its long-deleted branch is history, not a live claim."""
    assert _todo(monkeypatch, tmp_path,
                 "- [x] ~~Shipped~~ on `feature/gone-forever`.\n")[0] == vr.OK


def test_todo_branch_ignores_a_name_already_marked_stale(monkeypatch, tmp_path):
    """Correcting an item quotes the dead branch. Without this the fix re-flags
    itself forever — hit for real on TODO.md L2791, 2026-09-16."""
    assert _todo(monkeypatch, tmp_path,
                 '- [ ] **Utility lenses.**\n'
                 '  ⚠️ **"unmerged on `feature/stormwater-lens`" is STALE (corrected\n'
                 '  2026-09-16): it is on master and the branch is gone.**\n')[0] == vr.OK


def test_todo_branch_does_not_flag_doc_paths(monkeypatch, tmp_path):
    """`docs/` is excluded by design: measured 2026-09-16 it gave 64 hits, all of
    them doc PATHS. This is the false-positive case that would kill the check."""
    assert _todo(monkeypatch, tmp_path,
                 "- [ ] See `docs/DATA_ISSUES.md` and `docs/SPEC_services.md`.\n")[0] == vr.OK


def test_todo_branch_does_not_flag_file_paths_under_a_branchy_prefix(monkeypatch, tmp_path):
    assert _todo(monkeypatch, tmp_path,
                 "- [ ] Touch `scripts/check_cost_copy.py` and `src/load_roads.py`.\n")[0] == vr.OK


def test_todo_branch_scans_sub_items(monkeypatch, tmp_path):
    """The two real finds were both sub-items, not top-level ones."""
    status, _, detail = _todo(
        monkeypatch, tmp_path,
        "- [ ] **Parent epic.**\n  - [ ] child, see `feature/dead-branch`.\n")
    assert status == vr.ACTION and "line 2" in detail


def test_todo_branch_unknown_when_git_fails(monkeypatch, tmp_path):
    """Unreachable is UNKNOWN, never ACTION — the digest's standing rule."""
    (tmp_path / "TODO.md").write_text("- [ ] `feature/x`\n")
    monkeypatch.setattr(vr, "TODO_MD", tmp_path / "TODO.md")
    monkeypatch.setattr(vr.subprocess, "run",
                        lambda *a, **k: _FakeProc("", returncode=128, stderr="no remote"))
    assert vr.check_todo_branch_refs()[0] == vr.UNKNOWN


def test_todo_branch_empty_remote_is_unknown_not_all_stale(monkeypatch, tmp_path):
    """An empty branch list must not read as 'every reference is dead'."""
    assert _todo(monkeypatch, tmp_path, "- [ ] `feature/x`\n", remote="")[0] == vr.UNKNOWN


def test_todo_branch_unknown_without_a_todo_file(monkeypatch, tmp_path):
    monkeypatch.setattr(vr, "TODO_MD", tmp_path / "nope.md")
    assert vr.check_todo_branch_refs()[0] == vr.UNKNOWN


def test_todo_branch_is_registered_in_the_digest():
    assert vr.check_todo_branch_refs in vr.CHECKS


# --- budget pod manifest ----------------------------------------------------
#
# The gap these close: `city_budget_context.json` is hand-maintained and feeds
# published dollars on all 18 About-panel surfaces, and nothing recurring read
# it. Every test here drives a check into ACTION — an all-green manifest guard
# that cannot go red is the failure mode this project keeps re-learning.

_OPS_HEADER = ("budget_year,fund_type,department,branch,program,category,"
               "account_type,budget\n")


def _ops_row(year, program, budget, fund="Tax Supported"):
    return f"{year},{fund},Dept,Branch,{program},Materials,Expenses,{budget}\n"


def _ops_csv(rows=(), pod_year=2025):
    """The two pinned FY2017 lines plus the FY2025 snow program, at their real values."""
    base = (_ops_row(2017, "Roadway Maintenance", 65671000)
            + _ops_row(2017, "Snow and Ice Control", 63709000)
            + _ops_row(2025, "OPS/PARS - Snow and Ice Control", 67553815)
            + _ops_row(pod_year, "Something Else", 3845555000 - 67553815))
    return _OPS_HEADER + base + "".join(rows)


_POD = {
    "total_operating_budget": {"year": 2025, "value": 3845555000},
    "categories": [
        {"key": "roads", "components": {"maintenance": 65671000,
                                        "snow_and_ice_control": 36850000}},
        {"key": "active_transport", "components": {"snow_and_ice_control": 30150000}},
    ],
}


def _pod_local(monkeypatch, tmp_path, payload=None):
    f = tmp_path / "city_budget_context.json"
    f.write_text(json.dumps(payload or _POD))
    monkeypatch.setattr(vr, "BUDGET_CONTEXT", f)


def test_budget_context_ok_when_nothing_moved(monkeypatch, tmp_path):
    _pod_local(monkeypatch, tmp_path)
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(_ops_csv()))
    status, _, detail = vr.check_budget_context()
    assert status == vr.OK
    assert "99.2%" in detail


def test_budget_context_flags_a_newer_fiscal_year(monkeypatch, tmp_path):
    """The live case on 2026-09-17: FY2026 published, pod still on FY2025."""
    _pod_local(monkeypatch, tmp_path)
    csv_text = _ops_csv(rows=[_ops_row(2026, "Something Else", 4045178891)])
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(csv_text))
    status, _, detail = vr.check_budget_context()
    assert status == vr.ACTION
    assert "FY2026" in detail and "FY2025" in detail
    # It must say re-confirm, not "bump the year" — the vintage is a decision.
    assert "do not bump the year alone" in detail


def test_budget_context_flags_a_moved_pinned_program(monkeypatch, tmp_path):
    _pod_local(monkeypatch, tmp_path)
    moved = _OPS_HEADER + (
        _ops_row(2017, "Roadway Maintenance", 70000000)
        + _ops_row(2017, "Snow and Ice Control", 63709000)
        + _ops_row(2025, "OPS/PARS - Snow and Ice Control", 67553815))
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(moved))
    status, _, detail = vr.check_budget_context()
    assert status == vr.ACTION
    assert "Roadway Maintenance" in detail and "+4,329,000" in detail


def test_budget_context_ignores_a_renamed_program_in_other_years(monkeypatch, tmp_path):
    """⚠️ The era trap `DATA.md` §17 documents, as a test.

    `Roadway Maintenance` is FY2017-only and `Snow and Ice Control` FY2017-only;
    both are renamed from FY2018. A check that followed the NAME across years
    would read the rename as a budget cut and file an ACTION every month forever.
    """
    _pod_local(monkeypatch, tmp_path)
    renamed = _ops_csv(rows=[
        _ops_row(2018, "OPS/PARS - Infrastructure Maintenance", 49700000),
        _ops_row(2026, "OPS/PARS - Mobility Infrastructure Services", 76950000),
    ])
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(renamed))
    # FY2026 present, so the year half fires; the PROGRAM half must not.
    _, _, detail = vr.check_budget_context()
    assert "Roadway Maintenance" not in detail
    assert "Snow and Ice Control` FY2017" not in detail


def test_budget_context_flags_a_drifted_snow_cross_check(monkeypatch, tmp_path):
    """The snow components are Taproot's, corroborated against the portal at 99.2%."""
    pod = json.loads(json.dumps(_POD))
    pod["categories"][0]["components"]["snow_and_ice_control"] = 10_000_000
    _pod_local(monkeypatch, tmp_path, pod)
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(_ops_csv()))
    status, _, detail = vr.check_budget_context()
    assert status == vr.ACTION
    assert "snow cross-check drifted" in detail


def test_budget_context_flags_a_vanished_snow_program(monkeypatch, tmp_path):
    """A third re-cut of the tree must say so, not divide by zero."""
    _pod_local(monkeypatch, tmp_path)
    gone = _OPS_HEADER + _ops_row(2017, "Roadway Maintenance", 65671000) \
        + _ops_row(2017, "Snow and Ice Control", 63709000)
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeTextResp(gone))
    status, _, detail = vr.check_budget_context()
    assert status == vr.ACTION
    assert "returned nothing" in detail


def test_budget_context_counts_only_tax_supported(monkeypatch, tmp_path):
    """Utilities and Enterprise/CRL are the wrong denominator (`DATA.md` §17)."""
    _pod_local(monkeypatch, tmp_path)
    with_other_funds = _ops_csv(rows=[
        _ops_row(2027, "Water", 500000000, fund="Utilities"),
        _ops_row(2028, "CRL", 100000000, fund="Enterprise/CRL"),
    ])
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeTextResp(with_other_funds))
    status, _, detail = vr.check_budget_context()
    assert status == vr.OK, detail   # FY2027/28 are not tax-supported, so not "newer"


def test_budget_context_unreachable_is_unknown_not_action(monkeypatch, tmp_path):
    _pod_local(monkeypatch, tmp_path)
    monkeypatch.setattr(vr.requests, "get", _boom)
    assert vr.check_budget_context()[0] == vr.UNKNOWN


def test_budget_context_wrong_shape_is_unknown(monkeypatch, tmp_path):
    """A 404 HTML page parses as CSV without raising."""
    _pod_local(monkeypatch, tmp_path)
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeTextResp("<!DOCTYPE html><html>404"))
    assert vr.check_budget_context()[0] == vr.UNKNOWN


def test_budget_context_missing_local_file_is_unknown(monkeypatch, tmp_path):
    monkeypatch.setattr(vr, "BUDGET_CONTEXT", tmp_path / "absent.json")
    assert vr.check_budget_context()[0] == vr.UNKNOWN


def test_committed_budget_context_has_what_the_check_reads():
    """The real file must carry the keys the check pins, or it silently reads 0."""
    local = json.loads(vr.BUDGET_CONTEXT.read_text())
    assert int(local["total_operating_budget"]["year"]) > 2000
    comp = {c["key"]: c.get("components", {}) for c in local["categories"]}
    assert comp["roads"]["snow_and_ice_control"] > 0
    assert comp["active_transport"]["snow_and_ice_control"] > 0
    assert comp["roads"]["maintenance"] == vr.PINNED_PROGRAMS[("Roadway Maintenance", 2017)]


def test_budget_context_is_registered_in_the_digest():
    assert vr.check_budget_context in vr.CHECKS


# --- mill rate VALUES -------------------------------------------------------

def _rate_rows(year, municipal):
    return [{"tax_year": str(year), "assessment_class": "Residential",
             "tax_rate_type": "Municipal",
             "amount_per_1_000_of_assessed_value": str(municipal)}]


def test_mill_rate_values_flag_a_republished_rate(pinned, tmp_path, monkeypatch):
    """⚠️ THE GAP: `check_mill_rates` compares YEARS, so this passes it silently."""
    monkeypatch.setattr(vr, "MILL_RATES", _write(
        tmp_path, "m.json", {"rates": {"2025": {"Residential": {"municipal": 7.6254}}}}))
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp(_rate_rows(2025, 7.9999)))
    status, _, detail = vr.check_mill_rate_values()
    assert status == vr.ACTION
    assert "7.6254" in detail and "7.9999" in detail


def test_mill_rate_values_ok_when_they_match(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "MILL_RATES", _write(
        tmp_path, "m.json", {"rates": {"2025": {"Residential": {"municipal": 7.6254}}}}))
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp(_rate_rows(2025, 7.6254)))
    assert vr.check_mill_rate_values()[0] == vr.OK


def test_mill_rate_values_skip_underscore_notes(pinned, tmp_path, monkeypatch):
    """`_assumed` records a DERIVED value; there is nothing upstream to compare."""
    monkeypatch.setattr(vr, "MILL_RATES", _write(tmp_path, "m.json", {"rates": {"2025": {
        "Farmland": {"municipal": 7.6254, "_assumed": "set = Residential"}}}}))
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp(_rate_rows(2025, 7.6254)))
    status, _, detail = vr.check_mill_rate_values()
    assert status == vr.OK
    assert "_assumed" not in detail.replace("`_assumed` note", "")


def test_mill_rate_values_report_a_class_with_nothing_published(pinned, tmp_path,
                                                               monkeypatch):
    monkeypatch.setattr(vr, "MILL_RATES", _write(tmp_path, "m.json", {"rates": {"2025": {
        "Farmland": {"municipal": 7.6254}}}}))
    monkeypatch.setattr(vr.requests, "get",
                        lambda *a, **k: _FakeResp(_rate_rows(2025, 7.6254)))
    status, _, detail = vr.check_mill_rate_values()
    assert status == vr.OK
    assert "Farmland municipal" in detail


def test_mill_rate_values_ignore_other_years(pinned, tmp_path, monkeypatch):
    """A 2024 rate that disagrees is not this check's business — we bill one year."""
    monkeypatch.setattr(vr, "MILL_RATES", _write(
        tmp_path, "m.json", {"rates": {"2025": {"Residential": {"municipal": 7.6254}}}}))
    monkeypatch.setattr(vr.requests, "get", lambda *a, **k: _FakeResp(
        _rate_rows(2025, 7.6254) + _rate_rows(2024, 1.1111)))
    assert vr.check_mill_rate_values()[0] == vr.OK


def test_mill_rate_values_network_failure_is_unknown(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "MILL_RATES", _write(
        tmp_path, "m.json", {"rates": {"2025": {"Residential": {"municipal": 7.6254}}}}))
    monkeypatch.setattr(vr.requests, "get", _boom)
    assert vr.check_mill_rate_values()[0] == vr.UNKNOWN


def test_mill_rate_values_missing_pinned_block_is_unknown(pinned, tmp_path, monkeypatch):
    monkeypatch.setattr(vr, "MILL_RATES", _write(tmp_path, "m.json", {"rates": {"2019": {}}}))
    assert vr.check_mill_rate_values()[0] == vr.UNKNOWN


def test_mill_rate_values_is_registered_in_the_digest():
    assert vr.check_mill_rate_values in vr.CHECKS

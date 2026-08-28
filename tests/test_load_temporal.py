"""Tests for the temporal splice (src/load_temporal.py).

The splice's whole job is to keep two things straight that the data does not:
which years are publishable at all, and which hood a 14-year-old row belongs to
today. So the tests that matter are the year-selection rules (including the
January roll-forward, which is the trap a naive "omit 2024" implementation
walks into) and the name/denominator handling.

All fixtures synthetic, per the project's testing convention.
"""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.load_temporal import (  # noqa: E402
    COMMERCIAL_CLASSES,
    VALUE_UNIT,
    export_temporal_web,
    HISTORICAL_DEFECT_ACCOUNTS,
    HISTORICAL_DEFECT_YEARS,
    TEMPORAL_NAME_CORRECTIONS,
    build_temporal_table,
    current_roll_aggregate,
    load_archive,
    load_historical_aggregate,
    write_archive,
    normalize_hood,
    omitted_years,
    publishable_years,
    _year_summary,
)


def _long(rows):
    """rows: (year, hood, class, n_accounts, value) — the internal long shape."""
    return pd.DataFrame(
        rows, columns=["year", "neighbourhood_name", "mill_class", "n_accounts", "assessed_value"]
    )


def _two_source_fixture(live_year=2025):
    """A minimal history + a live roll, one commercial and one residential hood."""
    hist = _long([
        (y, h, c, n, v)
        for y in (2022, 2023, 2024, 2025)
        for h, c, n, v in (
            ("ALPHA", "RESIDENTIAL", 10, 1000.0),
            ("BETA", "COMMERCIAL", 5, 3000.0),
        )
    ])
    cur = _long([
        (live_year, "ALPHA", "RESIDENTIAL", 12, 1200.0),
        (live_year, "BETA", "COMMERCIAL", 6, 3600.0),
    ])
    return hist, cur


# --- year selection: the decision, and the trap ------------------------------

def test_2024_is_omitted():
    years = publishable_years(2025)
    assert 2024 not in years
    assert omitted_years(2025) == (2024,)


def test_published_years_are_deliberately_non_contiguous():
    years = publishable_years(2025)
    assert years[:12] == tuple(range(2012, 2024))
    assert years[-1] == 2025
    # The gap is the decision. If this ever becomes a plain range, someone
    # "fixed" it and republished a year with 2,322 missing accounts.
    assert years != tuple(range(2012, 2026))


def test_live_year_is_published_even_though_its_historical_slice_is_defective():
    # 2025 is in HISTORICAL_DEFECT_YEARS, but the current roll covers it.
    assert 2025 in HISTORICAL_DEFECT_YEARS
    assert 2025 in publishable_years(2025)


def test_january_roll_forward_drops_2025_instead_of_silently_republishing_it():
    """THE TRAP. Once the roll advances, 2025 has no complete source again."""
    assert 2025 in publishable_years(2025)      # live: repaired by the roll
    assert 2025 not in publishable_years(2026)  # no longer live: unrepairable
    assert omitted_years(2026) == (2024, 2025)


def test_a_clean_year_after_the_defect_window_stays_published():
    # 2026 is not a known-defective year, so once history covers it, it stays
    # published even after 2027 becomes live.
    assert 2026 in publishable_years(2027)


# --- name handling -----------------------------------------------------------

def test_oliver_is_carried_forward_as_the_renamed_hood():
    """Without this the series shows a 12,000-account hood vanishing in 2025."""
    assert TEMPORAL_NAME_CORRECTIONS["OLIVER"] == "WÎHKWÊNTÔWIN"
    out = normalize_hood(pd.Series(["OLIVER", " oliver ", "WÎHKWÊNTÔWIN"]))
    assert list(out) == ["WÎHKWÊNTÔWIN"] * 3


def test_shared_pipeline_corrections_still_apply():
    # NAME_CORRECTIONS layer, not the temporal one.
    assert normalize_hood(pd.Series(["CHAPPELLE AREA"]))[0] == "CHAPPELLE"


def test_rename_produces_one_continuous_series_not_two_broken_ones():
    hist = _long([(y, "OLIVER", "RESIDENTIAL", 100, 500.0) for y in (2022, 2023)])
    cur = _long([(2025, "WÎHKWÊNTÔWIN", "RESIDENTIAL", 110, 600.0)])
    table, _ = build_temporal_table(hist, cur, 2025)
    assert set(table["neighbourhood_name"]) == {"WÎHKWÊNTÔWIN"}
    assert sorted(table["year"]) == [2022, 2023, 2025]


# --- the splice itself -------------------------------------------------------

def test_live_year_comes_from_the_roll_and_the_historical_copy_is_discarded():
    hist, cur = _two_source_fixture()
    table, _ = build_temporal_table(hist, cur, 2025)
    live = table[table["year"] == 2025]
    assert set(live["source"]) == {"current_roll"}
    # 12 from the roll, not the historical slice's 10.
    assert int(live[live["neighbourhood_name"] == "ALPHA"]["n_accounts"].iloc[0]) == 12


def test_defective_year_is_absent_from_the_output_entirely():
    hist, cur = _two_source_fixture()
    table, stats = build_temporal_table(hist, cur, 2025)
    assert 2024 not in set(table["year"])
    assert stats["omitted_years"] == (2024,)


def test_missing_live_year_in_the_roll_raises_rather_than_publishing_a_gap():
    hist, cur = _two_source_fixture()
    with pytest.raises(ValueError, match="carries no rows for live_year"):
        build_temporal_table(hist, cur.assign(year=2099), 2025)


# --- shares and the denominator ----------------------------------------------

def test_shares_sum_to_one_per_year():
    hist, cur = _two_source_fixture()
    table, _ = build_temporal_table(hist, cur, 2025)
    for _, grp in table.groupby("year"):
        assert grp["share_of_total_base"].sum() == pytest.approx(1.0)


def test_commercial_share_uses_only_the_commercial_class():
    hist, cur = _two_source_fixture()
    table, _ = build_temporal_table(hist, cur, 2025)
    row = table[(table["neighbourhood_name"] == "BETA") & (table["year"] == 2023)].iloc[0]
    # BETA is the only commercial hood, so it is the entire commercial base.
    assert row["share_of_commercial_base"] == pytest.approx(1.0)
    alpha = table[(table["neighbourhood_name"] == "ALPHA") & (table["year"] == 2023)].iloc[0]
    assert alpha["share_of_commercial_base"] == pytest.approx(0.0)
    assert "COMMERCIAL" in COMMERCIAL_CLASSES


def test_commercial_share_is_null_not_zero_when_a_year_has_no_commercial_base():
    hist = _long([(y, "ALPHA", "RESIDENTIAL", 10, 1000.0) for y in (2023,)])
    cur = _long([(2025, "ALPHA", "RESIDENTIAL", 11, 1100.0)])
    table, _ = build_temporal_table(hist, cur, 2025)
    assert table["share_of_commercial_base"].isna().all()


def test_unmatched_hoods_stay_in_the_denominator():
    """An unmatched name is a hood that will not render — not a dropped dollar.

    Excluding it from the base would silently inflate every other hood's share.
    """
    hist, cur = _two_source_fixture()
    table, stats = build_temporal_table(hist, cur, 2025, boundary_names={"ALPHA"})
    assert stats["unmatched_hoods"] == ["BETA"]
    assert not table[table["neighbourhood_name"] == "BETA"]["matched_boundary"].any()
    # BETA is 3000 of 4000 in 2023 and still counts toward the base.
    alpha = table[(table["neighbourhood_name"] == "ALPHA") & (table["year"] == 2023)].iloc[0]
    assert alpha["share_of_total_base"] == pytest.approx(0.25)


def test_unmatched_value_fraction_is_reported():
    hist, cur = _two_source_fixture()
    _, stats = build_temporal_table(hist, cur, 2025, boundary_names={"ALPHA"})
    assert stats["unmatched_value_frac"] > 0.5  # BETA carries most of the value


# --- loaders -----------------------------------------------------------------

def test_historical_loader_rejects_a_file_missing_its_aggregate_columns(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("assessment_year,neighbourhood_name\n2012,ALPHA\n")
    with pytest.raises(ValueError, match="missing expected column"):
        load_historical_aggregate(p)


def test_current_roll_aggregate_sums_per_property_rows():
    assessment = pd.DataFrame({
        "neighbourhood_name": ["ALPHA", "ALPHA", "BETA"],
        "assessment_class_1": ["RESIDENTIAL", "RESIDENTIAL", "COMMERCIAL"],
        "assessed_value": [100.0, 200.0, 50.0],
    })
    out = current_roll_aggregate(assessment, 2025)
    alpha = out[out["neighbourhood_name"] == "ALPHA"].iloc[0]
    assert int(alpha["n_accounts"]) == 2
    assert alpha["assessed_value"] == pytest.approx(300.0)


# --- reporting ---------------------------------------------------------------

def test_year_summary_makes_the_gap_visible():
    assert _year_summary([2012, 2013, 2014, 2025]) == "2012-2014, 2025"
    assert _year_summary([2020]) == "2020"


# --- the archive: surviving the roll-forward ---------------------------------

def test_archive_lets_a_defect_year_survive_the_roll_forward():
    """THE POINT OF THE ARCHIVE. Without it, 2025 is lost each January."""
    hist = _long([(y, "ALPHA", "RESIDENTIAL", 10, 1000.0) for y in (2023, 2025, 2026)])
    cur = _long([(2026, "ALPHA", "RESIDENTIAL", 14, 1400.0)])
    captured = _long([(2025, "ALPHA", "RESIDENTIAL", 12, 1200.0)])

    lost, _ = build_temporal_table(hist, cur, 2026, archive=None)
    assert 2025 not in set(lost["year"])

    kept, stats = build_temporal_table(hist, cur, 2026, archive=captured)
    assert 2025 in set(kept["year"])
    assert stats["archived_years"] == (2025,)
    row = kept[kept["year"] == 2025].iloc[0]
    assert row["source"] == "archive"
    # The captured 12, not the defective historical slice's 10.
    assert int(row["n_accounts"]) == 12


def test_archive_does_not_override_a_year_the_historical_file_gets_right():
    """Mixing vintages would put an artifact step in the series."""
    hist = _long([(y, "ALPHA", "RESIDENTIAL", 10, 1000.0) for y in (2022, 2023, 2026)])
    cur = _long([(2026, "ALPHA", "RESIDENTIAL", 14, 1400.0)])
    captured = _long([(2022, "ALPHA", "RESIDENTIAL", 99, 9900.0)])  # a clean year
    table, stats = build_temporal_table(hist, cur, 2026, archive=captured)
    assert stats["archived_years"] == ()
    row = table[table["year"] == 2022].iloc[0]
    assert row["source"] == "historical" and int(row["n_accounts"]) == 10


def test_write_archive_freezes_years_that_are_no_longer_live(tmp_path):
    """A frozen year must never be rewritten — we no longer hold a full source."""
    p = tmp_path / "arch.json"
    write_archive(p, _long([(2025, "ALPHA", "RESIDENTIAL", 12, 1200.0)]), 2025)
    # The roll moves on; 2025 must survive untouched.
    summary = write_archive(p, _long([(2026, "ALPHA", "RESIDENTIAL", 20, 2000.0)]), 2026)
    assert summary["frozen_years"] == (2025,)
    back = load_archive(p)
    assert int(back[back["year"] == 2025]["n_accounts"].iloc[0]) == 12
    assert int(back[back["year"] == 2026]["n_accounts"].iloc[0]) == 20


def test_write_archive_refreshes_the_year_while_it_is_still_live(tmp_path):
    p = tmp_path / "arch.json"
    write_archive(p, _long([(2025, "ALPHA", "RESIDENTIAL", 12, 1200.0)]), 2025)
    write_archive(p, _long([(2025, "ALPHA", "RESIDENTIAL", 13, 1300.0)]), 2025)
    back = load_archive(p)
    assert int(back[back["year"] == 2025]["n_accounts"].iloc[0]) == 13


def test_a_stale_pin_cannot_overwrite_a_confirmed_year(tmp_path):
    """THE 2025 DEFECT, in one test. Audit 2026-08-28 F1.

    The freeze protects OTHER years; the pinned year is reassigned every run so
    the live capture can improve. When the pin goes stale that same line writes
    the NEXT roll over a CORRECT archived year — which is how the real 2025 was
    lost. A capture that cannot prove it is the pinned year must not destroy one
    that did.
    """
    p = tmp_path / "arch.json"
    write_archive(p, _long([(2026, "ALPHA", "RESIDENTIAL", 20, 2000.0)]), 2026,
                  confirmed=True)
    # The roll advances to 2027; nobody bumps the pin. The frame therefore
    # carries the 2027 roll under the 2026 label, exactly as main.py would.
    summary = write_archive(p, _long([(2026, "ALPHA", "RESIDENTIAL", 99, 9999.0)]), 2026,
                            confirmed=False)

    assert summary["archived_year"] is None and summary["refused_year"] == 2026
    back = load_archive(p)
    assert int(back[back["year"] == 2026]["n_accounts"].iloc[0]) == 20
    assert float(back[back["year"] == 2026]["assessed_value"].iloc[0]) == 2000.0


def test_an_unconfirmed_capture_is_still_written_when_nothing_is_at_risk(tmp_path):
    """Refusing to capture at all would REINTRODUCE the loss.

    Alberta files FIR months after Edmonton rolls, so a correctly pinned January
    capture is unprovable for most of the year. The data is irreplaceable; only
    the label was ever wrong. Keep the data, refuse the overwrite.
    """
    p = tmp_path / "arch.json"
    summary = write_archive(p, _long([(2027, "ALPHA", "RESIDENTIAL", 7, 700.0)]), 2027,
                            confirmed=False)
    assert summary["archived_year"] == 2027
    back = load_archive(p)
    assert int(back[back["year"] == 2027]["n_accounts"].iloc[0]) == 7

    # ...and it keeps improving week to week while it stays unproven.
    write_archive(p, _long([(2027, "ALPHA", "RESIDENTIAL", 8, 800.0)]), 2027, confirmed=False)
    back = load_archive(p)
    assert int(back[back["year"] == 2027]["n_accounts"].iloc[0]) == 8


def test_confirmation_upgrades_an_unproven_year_once_fir_lands(tmp_path):
    p = tmp_path / "arch.json"
    write_archive(p, _long([(2027, "ALPHA", "RESIDENTIAL", 7, 700.0)]), 2027, confirmed=False)
    write_archive(p, _long([(2027, "ALPHA", "RESIDENTIAL", 9, 900.0)]), 2027, confirmed=True)
    assert json.loads(p.read_text())["_year_confirmed"]["2027"] is True
    # ...and from then on it is protected.
    summary = write_archive(p, _long([(2027, "ALPHA", "RESIDENTIAL", 1, 1.0)]), 2027,
                            confirmed=False)
    assert summary["refused_year"] == 2027


def test_write_archive_refuses_when_there_is_nothing_to_capture(tmp_path):
    with pytest.raises(ValueError, match="nothing to archive"):
        write_archive(tmp_path / "a.json", _long([(2024, "A", "RESIDENTIAL", 1, 1.0)]), 2025)


def test_missing_archive_file_is_not_an_error(tmp_path):
    assert load_archive(tmp_path / "absent.json").empty


def test_archive_round_trips_hood_names_with_diacritics(tmp_path):
    p = tmp_path / "arch.json"
    write_archive(p, _long([(2025, "WÎHKWÊNTÔWIN", "RESIDENTIAL", 12, 1200.0)]), 2025)
    assert load_archive(p)["neighbourhood_name"].iloc[0] == "WÎHKWÊNTÔWIN"


# --- the web export ----------------------------------------------------------

def _exported(tmp_path, **kw):
    hist, cur = _two_source_fixture()
    table, _ = build_temporal_table(hist, cur, 2025, **kw)
    p = tmp_path / "temporal.json"
    stats = export_temporal_web(table, p)
    return json.loads(p.read_text()), stats


def test_export_carries_the_year_axis_including_the_gap(tmp_path):
    payload, _ = _exported(tmp_path)
    assert payload["years"] == [2022, 2023, 2025]
    # The renderer must plot against these values, not array indices.
    assert 2024 not in payload["years"]


def test_export_ships_the_defect_counts_so_the_note_is_not_a_literal(tmp_path):
    """The load-bearing test for the single-source rule.

    The published note and `verify-temporal.js` each used to carry their own copy
    of this figure (2,322 against 2,448) and disagreed for weeks with every check
    green. Both now read this field, so it has to be here and it has to cover
    every defective year -- an omitted year with no entry renders as the vaguer
    "incomplete for that year" fallback instead of the count.
    """
    payload, _ = _exported(tmp_path)
    assert payload["defect_accounts"] == {
        str(y): n for y, n in sorted(HISTORICAL_DEFECT_ACCOUNTS.items())
    }
    for year in HISTORICAL_DEFECT_YEARS:
        assert str(year) in payload["defect_accounts"]
    # The gap in `years` is what the note looks up, so every gap must resolve.
    gaps = [
        y for y in range(payload["years"][0], payload["years"][-1] + 1)
        if y not in payload["years"]
    ]
    assert gaps, "fixture must exercise a gap year"
    assert all(str(y) in payload["defect_accounts"] for y in gaps)


def test_defect_counts_are_incremental_and_must_not_be_summed():
    """Pins the trap: 2,322 + 131 = 2,453, but the real shortfall is 2,448.

    The counts are per-year increments against N-1, and 5 of 2024's missing
    accounts returned in 2025 (SPEC_temporal.md section 0.1). Both consumers --
    the panel note and verify-temporal.js -- state a SINGLE year's count or fall
    back to wording with no number, precisely so neither can publish this sum.
    If someone later "simplifies" that to a total, this test says why not.
    """
    assert sum(HISTORICAL_DEFECT_ACCOUNTS.values()) == 2453
    assert HISTORICAL_DEFECT_ACCOUNTS[2024] == 2322
    # The documented cumulative figure is NOT the sum, and that is the point.
    assert sum(HISTORICAL_DEFECT_ACCOUNTS.values()) != 2448


def test_export_series_are_index_aligned_to_years(tmp_path):
    payload, _ = _exported(tmp_path)
    for series in payload["hoods"]["ALPHA"]:
        assert len(series) == len(payload["years"])


def test_export_scales_shares_and_values_to_integers(tmp_path):
    payload, _ = _exported(tmp_path)
    shares, values, _ = payload["hoods"]["ALPHA"]
    assert all(isinstance(v, int) for v in shares + values)
    # ALPHA is 1000 of 4000 in 2022 -> 0.25 -> 250000 ppm.
    assert shares[0] == 250_000
    assert values[0] == 1000 // VALUE_UNIT or values[0] == round(1000 / VALUE_UNIT)


def test_export_omits_hoods_that_cannot_be_rendered(tmp_path):
    payload, stats = _exported(tmp_path, boundary_names={"ALPHA"})
    assert set(payload["hoods"]) == {"ALPHA"}
    assert stats["hoods"] == 1


def test_exported_shares_stay_shares_of_the_WHOLE_city(tmp_path):
    """Dropping unrenderable hoods must not renormalize the remainder."""
    payload, _ = _exported(tmp_path, boundary_names={"ALPHA"})
    shares = payload["hoods"]["ALPHA"][0]
    # Still 0.25 of the citywide base, not 1.0 of the surviving hoods.
    assert shares[0] == 250_000


def test_export_writes_zero_not_null_for_a_missing_commercial_base(tmp_path):
    hist = _long([(y, "ALPHA", "RESIDENTIAL", 10, 1000.0) for y in (2022, 2023)])
    cur = _long([(2025, "ALPHA", "RESIDENTIAL", 11, 1100.0)])
    table, _ = build_temporal_table(hist, cur, 2025)
    p = tmp_path / "t.json"
    export_temporal_web(table, p)
    assert json.loads(p.read_text())["hoods"]["ALPHA"][2] == [0, 0, 0]


def test_export_pads_a_hood_missing_a_year_rather_than_shifting_its_series(tmp_path):
    """A short series would silently slide left against the shared year axis."""
    hist = _long([
        (2022, "ALPHA", "RESIDENTIAL", 10, 1000.0),
        (2023, "ALPHA", "RESIDENTIAL", 10, 1000.0),
        (2023, "BETA", "RESIDENTIAL", 10, 1000.0),   # BETA has no 2022
    ])
    cur = _long([
        (2025, "ALPHA", "RESIDENTIAL", 11, 1100.0),
        (2025, "BETA", "RESIDENTIAL", 11, 1100.0),
    ])
    table, _ = build_temporal_table(hist, cur, 2025)
    p = tmp_path / "t.json"
    export_temporal_web(table, p)
    payload = json.loads(p.read_text())
    assert payload["years"] == [2022, 2023, 2025]
    assert len(payload["hoods"]["BETA"][0]) == 3
    assert payload["hoods"]["BETA"][0][0] == 0        # padded, not shifted
    assert payload["hoods"]["BETA"][0][1] > 0


def test_export_stays_inside_the_spec_budget(tmp_path):
    """SPEC_temporal.md phase 2: under 100 kB pre-gzip."""
    payload, stats = _exported(tmp_path)
    assert stats["bytes"] < 100 * 1024

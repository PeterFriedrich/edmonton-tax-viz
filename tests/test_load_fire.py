import json
import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_fire import (
    DISPATCH_COLUMN_CANDIDATES,
    NOISE_GROUPS,
    export_fire_stations_web,
    load_fire_events,
)

YEARS = (2023, 2024, 2025)


# Real-file shape: event_type_group carries two-letter codes; the long-name
# vocabulary the filter matches lives in event_description.
_CODES = {"MEDICAL": "MD", "FIRE": "FR", "TRAINING/MAINTENANCE": "TM",
          "COMMUNITY EVENT": "CM", "PRE-INCIDENT PLANNING": "PP"}


def _row(when="2024-06-01T12:00:00", group="MEDICAL", hood="ALPHA"):
    return {
        "dispatch_datetime": when,
        "event_type_group": None if group in (None, "") else _CODES.get(group, "ZZ"),
        "event_description": group,
        "neighbourhood_name": hood,
        # extra column proves the loader slims by usecols
        "response_code": "D",
    }


def _write_events(tmp_path, rows):
    p = tmp_path / "fire_response.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def _window_rows(hood="ALPHA", group="MEDICAL"):
    """One event in each window year — the minimum valid window coverage."""
    return [_row(when=f"{y}-03-01T00:00:00", group=group, hood=hood) for y in YEARS]


# --- load_fire_events --------------------------------------------------------

def test_counts_averaged_over_window(tmp_path):
    # ALPHA: 3 events in 2023, 0 in 2024, 0 in 2025 -> 1.0/yr.
    # BETA: one per year -> 1.0/yr (also keeps every window year non-empty).
    rows = [_row(when="2023-05-01T00:00:00", hood="ALPHA")] * 3 + _window_rows("BETA")
    out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"ALPHA", "BETA"}
    assert out.set_index("neighbourhood_name")["fire_events_per_year"]["ALPHA"] == pytest.approx(1.0)
    assert out.set_index("neighbourhood_name")["fire_events_per_year"]["BETA"] == pytest.approx(1.0)


def test_events_outside_window_excluded(tmp_path):
    rows = _window_rows() + [
        _row(when="2011-01-01T00:00:00", hood="OLD"),
        _row(when="2026-01-01T00:00:00", hood="PARTIAL"),
    ]
    out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"ALPHA"}


def test_noise_groups_excluded_and_reported(tmp_path, caplog):
    rows = _window_rows()
    rows += [_row(group=g) for g in sorted(NOISE_GROUPS)]
    with caplog.at_level("INFO"):
        out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(1.0)  # noise not counted
    assert "operational-noise" in caplog.text
    assert "TRAINING/MAINTENANCE" in caplog.text


def test_null_group_excluded_and_counted(tmp_path, caplog):
    rows = _window_rows() + [_row(group=None), _row(group="")]
    with caplog.at_level("WARNING"):
        out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(1.0)
    assert "null event group" in caplog.text


def test_code_only_rows_kept_via_fallback(tmp_path, caplog):
    # A code with no description (the real DR/86/FP/HO case) is a real
    # dispatch — kept under the bare code, loudly.
    row = _row(group=None)
    row["event_type_group"] = "DR"
    rows = _window_rows() + [row]
    with caplog.at_level("WARNING"):
        out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(4 / 3)
    assert "bare code" in caplog.text
    assert "DR" in caplog.text


def test_unknown_group_kept_and_logged(tmp_path, caplog):
    rows = _window_rows() + [_row(group="ZOMBIE OUTBREAK")]
    with caplog.at_level("WARNING"):
        out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    # 4 kept events / 3 years
    assert out["fire_events_per_year"].sum() == pytest.approx(4 / 3)
    assert "ZOMBIE OUTBREAK" in caplog.text


def test_medical_share_logged(tmp_path, caplog):
    rows = _window_rows(group="MEDICAL") + [_row(group="FIRE")]
    with caplog.at_level("INFO"):
        load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert "MEDICAL 75%" in caplog.text


def test_hood_normalized_and_corrected(tmp_path):
    # strip + uppercase + NAME_CORRECTIONS (PLACE LA RUE -> PLACE LARUE)
    rows = [
        _row(when="2023-01-01T00:00:00", hood="  place la rue "),
        _row(when="2024-01-01T00:00:00", hood="PLACE LARUE"),
        _row(when="2025-01-01T00:00:00", hood="PLACE LARUE"),
    ]
    out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert list(out["neighbourhood_name"]) == ["PLACE LARUE"]
    assert out["fire_events_per_year"].iloc[0] == pytest.approx(1.0)


def test_fire_specific_hood_corrections(tmp_path):
    # FIRE_NAME_CORRECTIONS layers on top of the shared dict: the fire CSV
    # still says OLIVER for the renamed WÎHKWÊNTÔWIN boundary, and the
    # "AREA" names collapse into their boundary hoods (summed, not dupes).
    rows = [
        _row(when="2023-01-01T00:00:00", hood="OLIVER"),
        _row(when="2024-01-01T00:00:00", hood="WÎHKWÊNTÔWIN"),
        _row(when="2025-01-01T00:00:00", hood="keswick area"),
        _row(when="2025-06-01T00:00:00", hood="KESWICK"),
    ]
    out = load_fire_events(_write_events(tmp_path, rows), YEARS).set_index("neighbourhood_name")
    assert set(out.index) == {"WÎHKWÊNTÔWIN", "KESWICK"}
    assert out["fire_events_per_year"]["WÎHKWÊNTÔWIN"] == pytest.approx(2 / 3)
    assert out["fire_events_per_year"]["KESWICK"] == pytest.approx(2 / 3)


def test_null_hood_excluded_and_counted(tmp_path, caplog):
    rows = _window_rows() + [_row(hood=None)]
    with caplog.at_level("WARNING"):
        out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(1.0)
    assert "no neighbourhood_name" in caplog.text


def test_empty_window_year_raises(tmp_path):
    # Nothing in 2025 -> hard error naming the year.
    rows = [
        _row(when="2023-01-01T00:00:00"),
        _row(when="2024-01-01T00:00:00"),
    ]
    with pytest.raises(ValueError, match="2025"):
        load_fire_events(_write_events(tmp_path, rows), YEARS)


def test_unparseable_dates_reported(tmp_path, caplog):
    rows = _window_rows() + [_row(when="not a date")]
    with caplog.at_level("WARNING"):
        out = load_fire_events(_write_events(tmp_path, rows), YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(1.0)
    assert "unparseable" in caplog.text


def test_dispatch_column_candidates_resolve(tmp_path):
    # Any candidate spelling works; an unresolvable header fails LOUD with
    # the file's real headers in the message.
    rows = pd.DataFrame(_window_rows()).rename(
        columns={"dispatch_datetime": "dispatched_datetime"})
    p = tmp_path / "fire_response.csv"
    rows.to_csv(p, index=False)
    out = load_fire_events(p, YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(1.0)


def test_missing_dispatch_column_errors_with_headers(tmp_path):
    rows = pd.DataFrame(_window_rows()).rename(
        columns={"dispatch_datetime": "mystery_time"})
    p = tmp_path / "fire_response.csv"
    rows.to_csv(p, index=False)
    with pytest.raises(ValueError, match="mystery_time"):
        load_fire_events(p, YEARS)
    assert "mystery_time" not in DISPATCH_COLUMN_CANDIDATES


def test_missing_group_column_errors(tmp_path):
    rows = pd.DataFrame(_window_rows()).drop(columns=["event_type_group"])
    p = tmp_path / "fire_response.csv"
    rows.to_csv(p, index=False)
    with pytest.raises(ValueError, match="event_type_group"):
        load_fire_events(p, YEARS)


def test_empty_years_raises(tmp_path):
    with pytest.raises(ValueError, match="empty"):
        load_fire_events(_write_events(tmp_path, _window_rows()), ())


# --- export_fire_stations_web -------------------------------------------------

def _write_stations(tmp_path, df):
    p = tmp_path / "fire_stations.csv"
    df.to_csv(p, index=False)
    return p


def test_stations_export_shape(tmp_path):
    p = _write_stations(tmp_path, pd.DataFrame([
        {"station_number": 1, "address": "A", "latitude": 53.5, "longitude": -113.5},
        {"station_number": 2, "address": "B", "latitude": 53.6, "longitude": -113.6},
    ]))
    out = tmp_path / "fire_stations.json"
    n = export_fire_stations_web(p, out)
    assert n == 2
    data = json.loads(out.read_text())
    assert data["stations"][0] == [-113.5, 53.5, "1"]
    assert data["stations"][1][1] == 53.6


def test_stations_null_coords_dropped_and_reported(tmp_path, caplog):
    p = _write_stations(tmp_path, pd.DataFrame([
        {"station_number": 1, "latitude": 53.5, "longitude": -113.5},
        {"station_number": 2, "latitude": None, "longitude": -113.6},
    ]))
    out = tmp_path / "fire_stations.json"
    with caplog.at_level("WARNING"):
        n = export_fire_stations_web(p, out)
    assert n == 1
    assert "null coordinates" in caplog.text


def test_stations_missing_coords_column_errors(tmp_path):
    p = _write_stations(tmp_path, pd.DataFrame([{"station_number": 1, "address": "A"}]))
    with pytest.raises(ValueError, match="latitude"):
        export_fire_stations_web(p, tmp_path / "out.json")


def test_stations_all_null_coords_errors(tmp_path):
    p = _write_stations(tmp_path, pd.DataFrame([
        {"station_number": 1, "latitude": None, "longitude": None},
    ]))
    with pytest.raises(ValueError, match="no stations"):
        export_fire_stations_web(p, tmp_path / "out.json")


def test_stations_label_optional(tmp_path, caplog):
    p = _write_stations(tmp_path, pd.DataFrame([
        {"latitude": 53.5, "longitude": -113.5},
    ]))
    out = tmp_path / "fire_stations.json"
    with caplog.at_level("WARNING"):
        export_fire_stations_web(p, out)
    assert json.loads(out.read_text())["stations"][0][2] == ""
    assert "unlabelled" in caplog.text


def test_dispatch_column_substring_fallback(tmp_path, caplog):
    # A header outside the candidate list but containing "dispatch" resolves
    # as the single unambiguous match — loudly, so the name gets pinned.
    rows = pd.DataFrame(_window_rows()).rename(
        columns={"dispatch_datetime": "evt_dispatch_stamp"})
    p = tmp_path / "fire_response.csv"
    rows.to_csv(p, index=False)
    with caplog.at_level("WARNING"):
        out = load_fire_events(p, YEARS)
    assert out["fire_events_per_year"].sum() == pytest.approx(1.0)
    assert "evt_dispatch_stamp" in caplog.text


def test_dispatch_column_not_datetime_errors(tmp_path):
    # Resolving a column that doesn't parse as datetimes at all must fail
    # loud, not silently produce an empty window.
    rows = pd.DataFrame(_window_rows())
    rows["dispatch_datetime"] = "banana"
    p = tmp_path / "fire_response.csv"
    rows.to_csv(p, index=False)
    with pytest.raises(ValueError, match="does not parse"):
        load_fire_events(p, YEARS)

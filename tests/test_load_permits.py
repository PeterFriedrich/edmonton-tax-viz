import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_permits import (
    INDUSTRIAL_BUILDING_TYPES,
    KNOWN_BUILDING_TYPES,
    KNOWN_WORK_TYPES,
    NEW_WORK_TYPES,
    RESIDENTIAL_BUILDING_TYPES,
    load_permits,
)

YEARS = (2021, 2022, 2023, 2024, 2025)


def _row(year=2023, work_type="(01) New",
         building_type="Single Detached House (110)", units_added=1,
         neighbourhood="ALPHA"):
    return {
        "year": year,
        # extra columns prove the loader slims via usecols
        "issue_date": f"{year}-06-01T00:00:00",
        "work_type": work_type,
        "building_type": building_type,
        "units_added": units_added,
        "neighbourhood": neighbourhood,
    }


def _write(tmp_path, rows):
    p = tmp_path / "building_permits.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def _window_rows(hood="ALPHA", units=1):
    """One valid new-residential permit in each window year — the minimum
    coverage that keeps the drift guard satisfied."""
    return [_row(year=y, neighbourhood=hood, units_added=units) for y in YEARS]


def _series(out, col="new_dwelling_units"):
    return out.set_index("neighbourhood_name")[col]


# --- aggregation -------------------------------------------------------------

def test_sums_units_and_counts_permits(tmp_path):
    # ALPHA: 3 permits, 5 units total, all in 2021. BETA: one/year keeps every
    # window year non-empty (drift guard) — 5 permits, 5 units.
    rows = [
        _row(year=2021, neighbourhood="ALPHA", units_added=2),
        _row(year=2021, neighbourhood="ALPHA", units_added=2),
        _row(year=2021, neighbourhood="ALPHA", units_added=1),
    ] + _window_rows("BETA")
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"ALPHA", "BETA"}
    assert _series(out, "new_dwelling_units")["ALPHA"] == pytest.approx(5.0)
    assert _series(out, "new_dwelling_permits")["ALPHA"] == 3
    assert _series(out, "new_dwelling_units")["BETA"] == pytest.approx(5.0)
    assert _series(out, "new_dwelling_permits")["BETA"] == 5


def test_apartment_units_exceed_permit_count(tmp_path):
    # A single apartment permit can add many dwellings — units != permits.
    rows = _window_rows("BETA") + [
        _row(year=2022, neighbourhood="TOWER",
             building_type="Apartments (310)", units_added=120),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert _series(out, "new_dwelling_units")["TOWER"] == pytest.approx(120.0)
    assert _series(out, "new_dwelling_permits")["TOWER"] == 1


# --- filters -----------------------------------------------------------------

def test_non_new_work_type_excluded(tmp_path):
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="ADD", work_type="(02) Addition"),
        _row(year=2023, neighbourhood="SUITE", work_type="(07) Add Suites to Single Dwelling"),
        _row(year=2023, neighbourhood="DEMO", work_type="(99) Demolition"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"BETA"}


def test_non_residential_building_type_excluded(tmp_path):
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="GARAGE", building_type="Detached Garage (010)"),
        _row(year=2023, neighbourhood="OFFICE", building_type="Office Buildings (520)"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"BETA"}


def test_residential_spelling_variants_all_counted(tmp_path):
    # The vocab carries many spellings of the same dwelling category; every
    # enumerated variant must be counted, not just the canonical one.
    variants = [
        "Single House (110)", "Backyard House (110)", "Duplex (210)",
        "Semi Detached House", "Row Houses (330)", "Apartment Condos (315)",
        "Mobile Home (130)",
    ]
    rows = _window_rows("BETA")
    for i, bt in enumerate(variants):
        rows.append(_row(year=2023, neighbourhood=f"V{i}", building_type=bt))
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"BETA"} | {f"V{i}" for i in range(len(variants))}


# --- window ------------------------------------------------------------------

def test_out_of_window_excluded(tmp_path):
    rows = _window_rows("BETA") + [
        _row(year=2015, neighbourhood="OLD"),
        _row(year=2026, neighbourhood="PARTIAL"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"BETA"}


def test_empty_window_year_raises_drift_guard(tmp_path):
    # No permits in 2025 -> the pinned window is stale / data drifted.
    rows = [_row(year=y, neighbourhood="BETA") for y in (2021, 2022, 2023, 2024)]
    with pytest.raises(ValueError, match="window year 2025 has ZERO permits"):
        load_permits(_write(tmp_path, rows), YEARS)


def test_empty_years_raises(tmp_path):
    with pytest.raises(ValueError, match="years window is empty"):
        load_permits(_write(tmp_path, _window_rows()), ())


# --- warn-on-unseen ----------------------------------------------------------

def test_unseen_work_type_warns_and_excluded(tmp_path, caplog):
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="WEIRD", work_type="(42) Teleporter"),
    ]
    with caplog.at_level("WARNING"):
        out = load_permits(_write(tmp_path, rows), YEARS)
    assert "WEIRD" not in set(out["neighbourhood_name"])
    assert any("KNOWN_WORK_TYPES" in r.message and "(42) Teleporter" in str(r.args)
               for r in caplog.records)


def test_unseen_building_type_warns_and_excluded(tmp_path, caplog):
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="WEIRD", building_type="Spaceport (777)"),
    ]
    with caplog.at_level("WARNING"):
        out = load_permits(_write(tmp_path, rows), YEARS)
    assert "WEIRD" not in set(out["neighbourhood_name"])
    assert any("KNOWN_BUILDING_TYPES" in r.message for r in caplog.records)


def test_known_non_new_type_does_not_warn(tmp_path, caplog):
    # A known-but-excluded work_type is silently filtered, not warned about.
    rows = _window_rows("BETA") + [_row(year=2023, work_type="(99) Demolition")]
    with caplog.at_level("WARNING"):
        load_permits(_write(tmp_path, rows), YEARS)
    assert not any("KNOWN_WORK_TYPES" in r.message for r in caplog.records)


# --- name handling -----------------------------------------------------------

def test_name_correction_merges_area_suffix(tmp_path):
    # CHAPPELLE AREA -> CHAPPELLE (shared NAME_CORRECTIONS) so the two collapse
    # into one hood with summed units.
    rows = [
        _row(year=2021, neighbourhood="CHAPPELLE AREA", units_added=3),
        _row(year=2022, neighbourhood="CHAPPELLE", units_added=2),
        _row(year=2023, neighbourhood="CHAPPELLE", units_added=1),
        _row(year=2024, neighbourhood="CHAPPELLE", units_added=1),
        _row(year=2025, neighbourhood="CHAPPELLE", units_added=1),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"CHAPPELLE"}
    assert _series(out)["CHAPPELLE"] == pytest.approx(8.0)


def test_blank_neighbourhood_excluded(tmp_path):
    rows = _window_rows("BETA") + [_row(year=2023, neighbourhood="", units_added=9)]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert set(out["neighbourhood_name"]) == {"BETA"}


# --- robustness --------------------------------------------------------------

def test_non_numeric_units_treated_as_zero(tmp_path):
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="NULLU", units_added="not a number"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    # NULLU is kept (new + residential) but contributes 0 units, 1 permit.
    assert _series(out, "new_dwelling_units")["NULLU"] == pytest.approx(0.0)
    assert _series(out, "new_dwelling_permits")["NULLU"] == 1


def test_missing_required_column_raises(tmp_path):
    df = pd.DataFrame(_window_rows()).drop(columns=["units_added"])
    p = tmp_path / "building_permits.csv"
    df.to_csv(p, index=False)
    with pytest.raises(ValueError, match="units_added"):
        load_permits(p, YEARS)


def test_no_kept_rows_raises(tmp_path):
    # Everything filtered out (all garages) -> loud failure, not empty frame.
    rows = [_row(year=y, building_type="Detached Garage (010)") for y in YEARS]
    with pytest.raises(ValueError, match="no new residential permits"):
        load_permits(_write(tmp_path, rows), YEARS)


# --- dictionary invariants ---------------------------------------------------

def test_new_work_types_subset_of_known():
    assert NEW_WORK_TYPES <= KNOWN_WORK_TYPES


def test_residential_subset_of_known_building_types():
    assert RESIDENTIAL_BUILDING_TYPES <= KNOWN_BUILDING_TYPES


# --- export_dev_grid (100 m detail layer) -------------------------------------

from load_permits import export_dev_grid  # noqa: E402

# Two WGS84 points ~30 m apart (same 100 m cell) and one ~1 km away.
LAT_A, LON_A = 53.5461, -113.4938
LAT_B, LON_B = 53.54615, -113.4942
LAT_FAR, LON_FAR = 53.5561, -113.4938


def _grow(year=2023, lat=LAT_A, lon=LON_A, **kw):
    r = _row(year=year, **kw)
    r["latitude"] = lat
    r["longitude"] = lon
    return r


def _geo_window_rows():
    return [_grow(year=y) for y in YEARS]


def _read(out):
    import json
    return json.loads(out.read_text())


def test_dev_grid_bins_nearby_points_into_one_cell(tmp_path):
    rows = _geo_window_rows() + [
        _grow(year=2023, lat=LAT_B, lon=LON_B, units_added=3),
        _grow(year=2023, lat=LAT_FAR, lon=LON_FAR, units_added=7),
    ]
    out = tmp_path / "dev_grid.json"
    export_dev_grid(_write(tmp_path, rows), out, YEARS)
    payload = _read(out)
    assert payload["columns"] == ["lon", "lat", "units", "permits"]
    assert payload["cell_m"] == 100.0
    cells = {tuple(c[:2]): c[2:] for c in payload["cells"]}
    assert len(cells) == 2  # A+B share a cell; FAR is its own
    assert sorted(v[0] for v in cells.values()) == [7, 8]  # units: 5+3, 7


def test_dev_grid_3yr_columns_and_window_split(tmp_path):
    rows = _geo_window_rows()  # one unit per year 2021-2025 at the same point
    out = tmp_path / "dev_grid.json"
    export_dev_grid(_write(tmp_path, rows), out, YEARS, years_recent=(2023, 2024, 2025))
    payload = _read(out)
    assert payload["columns"] == ["lon", "lat", "units", "permits",
                                  "units_3yr", "permits_3yr"]
    (cell,) = payload["cells"]
    assert cell[2:] == [5, 5, 3, 3]


def test_dev_grid_reports_geocode_coverage(tmp_path):
    rows = _geo_window_rows() + [
        {**_row(year=2025, units_added=10), "latitude": None, "longitude": None},
    ]
    out = tmp_path / "dev_grid.json"
    stats = export_dev_grid(_write(tmp_path, rows), out, YEARS)
    cov = _read(out)["coverage"]["5yr"]
    assert cov == {"units": 15, "units_geocoded": 5,
                   "permits": 6, "permits_geocoded": 5}
    assert stats["coverage"]["5yr"] == cov
    # the ungeocoded permit contributes NO cell
    assert sum(c[2] for c in _read(out)["cells"]) == 5


def test_dev_grid_excludes_non_new_and_non_residential(tmp_path):
    rows = _geo_window_rows() + [
        _grow(year=2023, work_type="(03) Interior Alterations", units_added=50),
        _grow(year=2023, building_type="Detached Garage (010)", units_added=50),
    ]
    out = tmp_path / "dev_grid.json"
    export_dev_grid(_write(tmp_path, rows), out, YEARS)
    assert sum(c[2] for c in _read(out)["cells"]) == 5


def test_dev_grid_missing_latlong_columns_raises(tmp_path):
    p = _write(tmp_path, _window_rows())  # no latitude/longitude columns
    with pytest.raises(ValueError, match="lat/long"):
        export_dev_grid(p, tmp_path / "dev_grid.json", YEARS)


def test_dev_grid_no_kept_rows_raises(tmp_path):
    rows = [_grow(year=2023, work_type="(03) Interior Alterations")]
    with pytest.raises(ValueError, match="no new residential"):
        export_dev_grid(_write(tmp_path, rows), tmp_path / "g.json", (2023,))


# --- industrial permit velocity (SPEC_industrial.md A3) ----------------------

def test_industrial_permits_counted_separately(tmp_path):
    # New industrial permits land in ind_permits (count), NOT new_dwelling_units.
    rows = _window_rows("BETA") + [
        _row(year=2022, neighbourhood="INDPARK",
             building_type="Storage Buildings, Warehouses (460)", units_added=0),
        _row(year=2023, neighbourhood="INDPARK",
             building_type="Manufacturing Buildings (430)", units_added=0),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    ind = out.set_index("neighbourhood_name")
    assert ind.loc["INDPARK", "ind_permits"] == 2
    # Industrial adds no dwelling units and no residential permits.
    assert ind.loc["INDPARK", "new_dwelling_units"] == pytest.approx(0.0)
    assert ind.loc["INDPARK", "new_dwelling_permits"] == pytest.approx(0.0)
    # A residential-only hood carries a true 0 industrial count.
    assert ind.loc["BETA", "ind_permits"] == pytest.approx(0.0)


def test_industrial_and_residential_coexist_in_one_hood(tmp_path):
    rows = _window_rows("MIXED") + [
        _row(year=2022, neighbourhood="MIXED",
             building_type="Utility Buildings (480)"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    row = out.set_index("neighbourhood_name").loc["MIXED"]
    assert row["new_dwelling_permits"] == 5        # the residential window rows
    assert row["ind_permits"] == 1                 # the one industrial permit


def test_industrial_requires_new_work_type(tmp_path):
    # An alteration to an industrial building is not new construction.
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="INDPARK",
             work_type="(03) Interior Alterations",
             building_type="Manufacturing Buildings (430)"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert "INDPARK" not in set(out["neighbourhood_name"])


def test_parkade_490_not_industrial(tmp_path):
    # Parkade shares code (490) with Engineering but is NOT industrial — the
    # enumeration is by full string, so it must not be counted.
    rows = _window_rows("BETA") + [
        _row(year=2023, neighbourhood="PARK", building_type="Parkade (490)"),
    ]
    out = load_permits(_write(tmp_path, rows), YEARS)
    assert "PARK" not in set(out["neighbourhood_name"])  # neither res nor ind


def test_industrial_set_disjoint_from_residential():
    assert not (INDUSTRIAL_BUILDING_TYPES & RESIDENTIAL_BUILDING_TYPES)
    assert INDUSTRIAL_BUILDING_TYPES <= KNOWN_BUILDING_TYPES

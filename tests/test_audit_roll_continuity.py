"""Tests for tools/audit_roll_continuity.py.

The whole audit rests on one decision: match parcels by POSITION with a
tolerance, not by any identifier. Both halves of that are load-bearing and
neither is obvious from reading the code:

  * with too small a tolerance, every renumbered parcel reads as a dropout —
    coordinates drift up to ~2m across a renumbering, so an exact match on
    rounded lat/lon reports the four hospitals as missing. That is the exact
    false positive the audit exists to avoid.
  * with no tolerance limit at all, ``sjoin_nearest`` matches every parcel to
    *something* and the audit finds nothing, ever.

So the tests pin the behaviour at both edges using the real observed drift.
Network fetching is not tested — it is a thin Socrata pager, and the audit is
validated end-to-end against known-answer cases (the four renumbered hospitals
must match; see the tool's docstring).
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from audit_roll_continuity import to_points, unmatched  # noqa: E402

# Misericordia, historical vs current. ~0.7m apart across the renumbering.
MISERICORDIA_HIST = (53.52170884084244, -113.61159282909364)
MISERICORDIA_CUR = (53.52170991953645, -113.6115817586859)


def _roll(*rows):
    """rows of (account, lat, lon, value) -> the frame to_points() expects."""
    return pd.DataFrame(
        [{"account_number": a, "latitude": lat, "longitude": lon,
          "assessed_value": v, "house_number": "1", "street_name": "X",
          "neighbourhood_name": "H"} for a, lat, lon, v in rows]
    )


def test_renumbered_parcel_matches_despite_coordinate_drift():
    """The case the audit exists for: same building, new account, ~0.7m moved."""
    hist = to_points(_roll(("10095840", *MISERICORDIA_HIST, 250_236_500)))
    cur = to_points(_roll(("11495573", *MISERICORDIA_CUR, 247_780_500)))
    assert unmatched(hist, cur, 5.0).empty


def test_a_genuinely_absent_parcel_is_reported():
    hist = to_points(_roll(("10095840", *MISERICORDIA_HIST, 250_236_500)))
    cur = to_points(_roll(("999", 53.6, -113.4, 1_000)))   # ~10km away
    gone = unmatched(hist, cur, 5.0)
    assert list(gone["account_number"]) == ["10095840"]


def test_tolerance_too_tight_manufactures_the_false_positive():
    """Falsification: at 0.1m the real drift reads as a dropout.

    This is what an exact / rounded-coordinate join would do, and it is why the
    tolerance exists. If someone tightens it, this test says what breaks.
    """
    hist = to_points(_roll(("10095840", *MISERICORDIA_HIST, 250_236_500)))
    cur = to_points(_roll(("11495573", *MISERICORDIA_CUR, 247_780_500)))
    assert len(unmatched(hist, cur, 0.1)) == 1


def test_each_historical_parcel_is_counted_once():
    """sjoin_nearest can emit several rows per left row on ties.

    Two current parcels equidistant from one historical point must not turn one
    parcel into two — that would inflate both the count and the value at risk.
    """
    hist = to_points(_roll(("A", 53.5, -113.5, 1_000_000)))
    cur = to_points(_roll(("B", 53.500001, -113.5, 1), ("C", 53.499999, -113.5, 1)))
    assert unmatched(hist, cur, 50.0).empty
    far = to_points(_roll(("B", 53.6, -113.5, 1), ("C", 53.4, -113.5, 1)))
    assert len(unmatched(hist, far, 5.0)) == 1


def test_rows_without_coordinates_are_dropped_not_matched():
    """A parcel with no position cannot be matched and must not read as a dropout."""
    df = _roll(("A", 53.5, -113.5, 1_000_000))
    df.loc[1] = {"account_number": "B", "latitude": None, "longitude": None,
                 "assessed_value": 5_000, "house_number": "2",
                 "street_name": "Y", "neighbourhood_name": "H"}
    pts = to_points(df)
    assert list(pts["account_number"]) == ["A"]


@pytest.mark.parametrize("value,expected", [("250236500", 250_236_500.0), ("", None)])
def test_assessed_value_is_coerced_from_socrata_strings(value, expected):
    """Socrata returns numbers as text; the value column must be numeric."""
    df = _roll(("A", 53.5, -113.5, value))
    got = to_points(df)["assessed_value"].iloc[0]
    assert (got == expected) if expected is not None else pd.isna(got)

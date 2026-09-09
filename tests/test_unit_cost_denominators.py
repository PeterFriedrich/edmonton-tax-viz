"""Every rate in ``data/city_unit_costs.json`` must declare WHAT ITS PUBLISHER'S
DENOMINATOR COUNTS.

⚠️ Why this file exists. A rate can be wrong in three ways: its PROVENANCE, its
VINTAGE, and its DENOMINATOR. The JSON carried fields and guards for the first
two and nothing for the third, and ``roadway_ops`` shipped for a year as dollars
per LANE-km multiplied by CENTRELINE metres (S149). The existing ``units`` key
did not catch it because it describes what *we* compute, never what the *City's*
figure was per.

⚠️ THE POINT IS THE QUESTION, NOT THE ANSWER. ``UNKNOWN`` / ``UNEXAMINED`` are
legal and currently the majority. These tests deliberately do NOT require a
resolved unit — requiring one would just get the field filled in with guesses,
which is the failure this is meant to prevent.
"""
import json
from pathlib import Path

import pytest

UNIT_COSTS = Path(__file__).resolve().parents[1] / "data" / "city_unit_costs.json"

VALID_UNITS = {"lane-km", "centreline-km", "route-km", "not-a-length-rate", "UNKNOWN"}
VALID_CONFIDENCE = {"ESTABLISHED", "ASSUMED", "UNEXAMINED", "N/A"}


@pytest.fixture(scope="module")
def costs():
    with open(UNIT_COSTS, encoding="utf-8") as f:
        return json.load(f)


def rate_blocks(costs):
    """Every real block — the leading underscore keys are prose preamble."""
    return {k: v for k, v in costs.items() if not k.startswith("_")}


def test_there_are_rate_blocks_to_check(costs):
    """Guard the guard: an empty selection would make every test below vacuous."""
    assert len(rate_blocks(costs)) >= 7


def test_every_rate_block_declares_a_source_denominator(costs):
    missing = [k for k, v in rate_blocks(costs).items() if "source_denominator" not in v]
    assert not missing, (
        f"blocks with no source_denominator: {missing}. A new rate must answer "
        "what its publisher's denominator counts — 'UNKNOWN'/'UNEXAMINED' is a "
        "legal answer, silence is not."
    )


@pytest.mark.parametrize("field,valid", [("unit", VALID_UNITS), ("confidence", VALID_CONFIDENCE)])
def test_source_denominator_uses_the_closed_vocabulary(costs, field, valid):
    bad = {
        k: v["source_denominator"].get(field)
        for k, v in rate_blocks(costs).items()
        if v.get("source_denominator", {}).get(field) not in valid
    }
    assert not bad, f"{field} outside {sorted(valid)}: {bad}"


def test_every_source_denominator_says_why(costs):
    """A bare label is not the deliverable — the reasoning is."""
    thin = {
        k: len(v["source_denominator"].get("why", ""))
        for k, v in rate_blocks(costs).items()
        if len(v.get("source_denominator", {}).get("why", "")) < 80
    }
    assert not thin, f"source_denominator.why too thin to be useful: {thin}"


def test_not_a_length_rate_and_na_agree(costs):
    """The two fields cannot disagree about whether a length denominator exists."""
    for k, v in rate_blocks(costs).items():
        sd = v["source_denominator"]
        assert (sd["unit"] == "not-a-length-rate") == (sd["confidence"] == "N/A"), (
            f"{k}: unit={sd['unit']!r} and confidence={sd['confidence']!r} disagree "
            "about whether this is a per-length rate"
        )


def test_roadway_ops_is_pinned_to_lane_km(costs):
    """⚠️ The S149 finding itself. This is the one unit that IS established, and
    the whole floor framing rests on it — if this flips, the published caveat,
    the ~2.5-3x lifecycle gap and the send-back brief's Q1 all need re-reading."""
    sd = costs["roadway_ops"]["source_denominator"]
    assert sd["unit"] == "lane-km"
    assert sd["confidence"] == "ESTABLISHED"


def test_the_two_lifecycle_blocks_share_one_unconfirmed_denominator(costs):
    """⚠️ roadway_renewal IS the $1.9M half of roadway_om_renewal, so they must
    never drift apart on this. Both are unconfirmed pending Q1(a) bullet 2, and
    resolving it resolves both."""
    a = costs["roadway_om_renewal"]["source_denominator"]
    b = costs["roadway_renewal"]["source_denominator"]
    assert a["unit"] == b["unit"] == "UNKNOWN"
    assert a["confidence"] == b["confidence"] == "ASSUMED"

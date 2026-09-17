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


def test_the_two_lifecycle_blocks_share_one_denominator(costs):
    """⚠️ roadway_renewal IS the $1.9M half of roadway_om_renewal, so they must
    never drift apart on this. Both were unconfirmed pending Q1(a) bullet 2;
    that resolved to centreline on 2026-09-17 and resolved both together, as
    predicted. The invariant the test protects is the AGREEMENT, not the value —
    a future re-reading must move both blocks or neither."""
    a = costs["roadway_om_renewal"]["source_denominator"]
    b = costs["roadway_renewal"]["source_denominator"]
    assert a["unit"] == b["unit"] == "centreline-km"
    assert a["confidence"] == b["confidence"] == "ESTABLISHED"


def test_the_two_road_figures_do_not_share_a_denominator(costs):
    """⚠️ THE TRAP THIS FILE EXISTS FOR, now that the lifecycle side is resolved.
    This file carries two City road per-km figures on GENUINELY DIFFERENT units:
    the Development Impact lifecycle figures are centreline-km, the ~11,000 km
    snow-and-ice inventory behind roadway_ops is lane-km. The tidy-looking error
    is to "harmonize" them. Falsified by name: if these two ever read the same,
    someone has propagated one resolution across both."""
    lifecycle = costs["roadway_om_renewal"]["source_denominator"]["unit"]
    operating = costs["roadway_ops"]["source_denominator"]["unit"]
    assert lifecycle == "centreline-km"
    assert operating == "lane-km"
    assert lifecycle != operating, (
        "the lifecycle and operating road rates now claim the same denominator — "
        "they are different City figures and were established separately"
    )


def test_development_impact_figures_reconcile_to_the_pages_own_total(costs):
    """⚠️ THE CHECK THAT PINS THE CENTRELINE READING, and the reason it is not
    just an assertion of what we already believed.

    The source page states its own lifecycle total — "about $4 million. Or about
    2.5 times the initial capital investment" — and the three component figures
    stored here sum to it exactly. That is what makes them ONE single-street
    scenario rather than a mix of bases: a lane-km reading would have to explain
    why a two-lane street's components still add to the page's one-street total.

    Guards the stored figures, not the prose: change any component and this
    fails, which is the point (the $1,285/km road-maintenance figure went a year
    unchallenged because nothing tied it to anything else)."""
    pub = costs["roadway_om_renewal"]["source"]["published_figures_per_km_neighbourhood_road"]
    capital = pub["initial_capital"]
    om = pub["operate_and_maintain"]
    renewal = pub["renew_and_replace"]

    assert (capital, om, renewal) == (1_500_000, 600_000, 1_900_000)
    assert capital + om + renewal == 4_000_000, "no longer reconciles to the page's stated ~$4M total"
    # The page rounds "about 2.5 times"; the exact ratio is 2.67. Anything outside
    # this band means a component moved and the page's own framing no longer holds.
    assert 2.5 <= (capital + om + renewal) / capital <= 2.7

    # The shipped rate is that bundle, minus capital, over the 50-year life.
    assert (om + renewal) / 50 / 1000 == costs["roadway_om_renewal"]["value"] == 50
    assert renewal / 50 / 1000 == costs["roadway_renewal"]["value"] == 38

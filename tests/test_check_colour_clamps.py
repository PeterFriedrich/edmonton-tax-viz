"""Tests for scripts/check_colour_clamps.py (the money colour-clamp guard).

⚠️ The load-bearing test is ``test_catches_the_clamp_at_5000_hole``: it
reconstructs the exact vacuity the 2026-09-15 published-numbers audit found —
the verify scripts pin the legend STRING, so the clamp could be moved to $5,000
with the legend still reading ``$50k+`` and every check would stay green.

⚠️ The drift half (check B) is green on the real file today (4.5%, inside the
1–6% band, by Peter's decision to keep the literal). A guard that has never been
shown to go red is not evidence of anything, so it is falsified here by moving
the data under a fixed clamp in BOTH directions.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_colour_clamps import (  # noqa: E402
    BAND,
    EXIT_DRIFT,
    EXIT_OK,
    check_legend_agreement,
    main,
    measure_drift,
    parse_legend_money,
    parse_metrics,
)

REPO = Path(__file__).resolve().parent.parent


def _html(tmp_path: Path, *blocks: str) -> Path:
    """A minimal METRICS block at the real file's indentation (6 spaces)."""
    p = tmp_path / "index.html"
    p.write_text("    const METRICS = {\n" + "\n".join(blocks) + "\n    };\n")
    return p


def _metric(key: str, legend: str, clamp: str, blurb: str = "") -> str:
    return (
        f"      {key}: {{\n"
        f'        blurb: "{blurb}",\n'
        f'        legendMin: "$0",\n'
        f'        legendMax: "{legend}",\n'
        f"        colorClamp: {clamp},\n"
        f"      }},"
    )


def _geojson(tmp_path: Path, values, key="revenue_per_acre", set_aside=()) -> Path:
    feats = [
        {"properties": {"neighbourhood_name": f"H{i}", key: v, "is_set_aside": False}}
        for i, v in enumerate(values)
    ]
    feats += [
        {"properties": {"neighbourhood_name": f"S{i}", key: v, "is_set_aside": True}}
        for i, v in enumerate(set_aside)
    ]
    p = tmp_path / "hoods.geojson"
    p.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    return p


# --- check A: the hole the audit found ---------------------------------------

def test_catches_the_clamp_at_5000_hole(tmp_path):
    """The audit's words: the existing guards 'would pass with the clamp at $5,000'."""
    html = _html(tmp_path, _metric("revenue_per_acre", "$50k+", "5_000"))
    failures = check_legend_agreement(parse_metrics(html))
    assert len(failures) == 1
    assert "legend says '$50k+'" in failures[0] and "5,000" in failures[0]


def test_agreeing_pair_passes(tmp_path):
    html = _html(tmp_path, _metric("revenue_per_acre", "$50k+", "50_000"))
    assert check_legend_agreement(parse_metrics(html)) == []


def test_moving_only_the_legend_fails(tmp_path):
    """The other direction: re-labelling without re-anchoring the ramp."""
    html = _html(tmp_path, _metric("revenue_per_acre", "$57k+", "50_000"))
    assert len(check_legend_agreement(parse_metrics(html))) == 1


def test_moving_both_together_passes(tmp_path):
    html = _html(tmp_path, _metric("revenue_per_acre", "$57k+", "57_000"))
    assert check_legend_agreement(parse_metrics(html)) == []


@pytest.mark.parametrize("legend,expected", [
    ("$50k+", 50_000), ("$30k+", 30_000), ("$4M+", 4_000_000),
    ("$1.5M+", 1_500_000), ("$0", 0),
])
def test_legend_money_parsing(legend, expected):
    assert parse_legend_money(legend) == expected


def test_unparseable_legend_is_a_failure_not_a_pass(tmp_path):
    """A legend nothing can decode must not read as agreement."""
    html = _html(tmp_path, _metric("revenue_per_acre", "lots", "50_000"))
    failures = check_legend_agreement(parse_metrics(html))
    assert len(failures) == 1 and "not a money literal" in failures[0]


# --- the parser ---------------------------------------------------------------

def test_blurb_dollar_figures_do_not_pair_with_the_wrong_metric(tmp_path):
    """METRICS blurbs are full of `$` figures and braces; a greedy regex over the
    block silently pairs one metric's legend with another's clamp."""
    html = _html(
        tmp_path,
        _metric("revenue_per_acre", "$50k+", "50_000", blurb="costs $50 per metre per year"),
        _metric("value_per_acre", "$4M+", "4_000_000", blurb="about $1,900,000 to renew"),
    )
    m = parse_metrics(html)
    assert m["revenue_per_acre"]["clamp"] == 50_000
    assert m["value_per_acre"]["clamp"] == 4_000_000


def test_blocks_without_both_fields_are_not_money_metrics(tmp_path):
    html = _html(
        tmp_path,
        _metric("revenue_per_acre", "$50k+", "50_000"),
        "      roads: {\n        label: \"Roads\",\n      },",
    )
    assert set(parse_metrics(html)) == {"revenue_per_acre"}


def test_parses_the_real_file():
    """The four money metrics, and only those."""
    m = parse_metrics(REPO / "web" / "index.html")
    assert set(m) == {"revenue_per_acre", "res_revenue_per_acre",
                      "nonres_revenue_per_acre", "value_per_acre"}
    assert m["revenue_per_acre"]["clamp"] == 50_000


def test_the_real_file_agrees():
    assert check_legend_agreement(parse_metrics(REPO / "web" / "index.html")) == []


# --- check B: falsified in both directions ------------------------------------

CLAMP_HTML = ("revenue_per_acre", "$50k+", "50_000")


def _drift(tmp_path, values, set_aside=()):
    html = _html(tmp_path, _metric(*CLAMP_HTML))
    geo = _geojson(tmp_path, values, set_aside=set_aside)
    return measure_drift(parse_metrics(html), geo)[0]


def test_in_band_is_not_flagged(tmp_path):
    """97 hoods under the clamp, 3 over = 3.0%."""
    row = _drift(tmp_path, [10_000] * 97 + [60_000] * 3)
    assert row["share"] == 3.0 and not row["flagged"]


def test_too_many_saturating_is_flagged(tmp_path):
    """The data rises under a fixed clamp — the top band stops discriminating."""
    row = _drift(tmp_path, [10_000] * 90 + [60_000] * 10)
    assert row["share"] == 10.0 and row["flagged"]


def test_too_few_saturating_is_flagged(tmp_path):
    """The other direction: a clamp far above the distribution wastes the ramp."""
    row = _drift(tmp_path, [10_000] * 100)
    assert row["share"] == 0.0 and row["flagged"]


def test_band_edges(tmp_path):
    assert _drift(tmp_path, [10_000] * 994 + [60_000] * 6)["flagged"]       # 0.6% < floor
    assert not _drift(tmp_path, [10_000] * 990 + [60_000] * 10)["flagged"]  # 1.0% == floor
    assert not _drift(tmp_path, [10_000] * 940 + [60_000] * 60)["flagged"]  # 6.0% == ceiling
    assert _drift(tmp_path, [10_000] * 939 + [60_000] * 61)["flagged"]      # 6.1%


def test_set_aside_hoods_are_excluded_and_it_matters(tmp_path):
    """Including grey hoods dilutes the share toward zero, so the guard would read
    healthy while the ramp saturates. 10 of 100 live = 10% (flagged); with 100
    set-aside hoods folded in it would read 5% and pass."""
    row = _drift(tmp_path, [10_000] * 90 + [60_000] * 10, set_aside=[0] * 100)
    assert row["n"] == 100 and row["share"] == 10.0 and row["flagged"]


def test_the_real_file_is_in_band_today(tmp_path):
    """Records Peter's 2026-09-16 decision as a measurement: 4.5% is accepted, so
    the band contains it. If this starts failing, the clamp moved or the data did."""
    rows = measure_drift(parse_metrics(REPO / "web" / "index.html"),
                         REPO / "web" / "data" / "neighbourhood_value_per_acre.geojson")
    rev = next(r for r in rows if r["metric"] == "revenue_per_acre")
    assert rev["saturating"] == 16 and 4.0 < rev["share"] < 5.0
    assert BAND[0] <= rev["share"] <= BAND[1] and not rev["flagged"]


# --- exit codes ---------------------------------------------------------------

def test_drift_never_changes_the_exit_code(tmp_path, capsys):
    """B reports; it must never block the weekly publish."""
    html = _html(tmp_path, _metric(*CLAMP_HTML))
    geo = _geojson(tmp_path, [10_000] * 50 + [60_000] * 50)  # 50% saturating
    assert main(["--html", str(html), "--geojson", str(geo)]) == EXIT_OK
    assert "50.0%" in capsys.readouterr().out


def test_legend_disagreement_blocks(tmp_path):
    html = _html(tmp_path, _metric("revenue_per_acre", "$50k+", "5_000"))
    geo = _geojson(tmp_path, [10_000] * 100)
    assert main(["--html", str(html), "--geojson", str(geo)]) == EXIT_DRIFT


def test_missing_metrics_block_fails_rather_than_passing_empty(tmp_path):
    """If METRICS moves or is renamed, the guard must not report an all-clear
    over zero metrics."""
    empty = tmp_path / "index.html"
    empty.write_text("<html></html>")
    assert main(["--html", str(empty), "--legend-only"]) == EXIT_DRIFT


def test_legend_only_needs_no_data(tmp_path):
    html = _html(tmp_path, _metric(*CLAMP_HTML))
    assert main(["--html", str(html), "--geojson", str(tmp_path / "nope.geojson"),
                 "--legend-only"]) == EXIT_OK

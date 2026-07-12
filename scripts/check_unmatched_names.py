"""Unmatched-name guard: fail CI loud when the assessment money-path name join drifts.

The data-integrity audit's §4 / second-run T3c follow-on: neighbourhood names are
the join key between the assessment roll and the boundary polygons, and the
pipeline handles a mismatch by *warning* and dropping the row (CLAUDE.md "no
silent data drops" — but a warning in a weekly unattended CI log is effectively
silent). On a public auto-refreshing site, a NEW unmatched name means real
assessed value has silently vanished from the map. This guard converts that from
warn-silent to fail-loud.

It compares the LIVE money-path unmatched sets against a committed baseline
(``data/expected_unmatched.json``):

  * ``assessment_not_in_boundaries`` — assessment neighbourhood names with no
    boundary polygon. These DROP DOLLARS from the map. A NEW name here is the
    dangerous case → the guard FAILS (exit 5).
  * ``boundaries_not_in_assessment`` — boundary polygons with no assessment rows
    (rendered n/a grey). A new name here shows a blank hood, not wrong money → a
    warning, still tracked in the baseline so the count is intentional.

Both baselines are also treated as exact sets: a name that USED to be unmatched
and now matches (a mapping got fixed upstream) is reported as a warning asking
for a baseline update — benign, so it does NOT fail the build (we only hard-fail
on the silent-data-loss direction, so a legitimate fix never reds the weekly
refresh unexpectedly).

Runs in CI (refresh.yml) after download, before regeneration: a hard failure
stops the build before deploy, so the last good data keeps serving and the owner
is notified. Names are compared post-correction/aggregation (load_assessment
applies NAME_CORRECTIONS and the zero-value drop first — which is why SPUR LINES,
$0, never reaches this join and is correctly absent from the baseline).

Outcomes (exit codes; 2 is argparse's):
  0  ok    — live sets equal the baseline (or differ only by resolved names).
  5  drift — a NEW assessment name has no boundary (silent dollar loss). FAIL.

When ``GITHUB_OUTPUT`` is set (CI), writes ``result=`` and the added/removed
name lists for the workflow/log.

Usage:
    python scripts/check_unmatched_names.py                       # live data/raw + baseline
    python scripts/check_unmatched_names.py --assessment-csv a.csv --boundaries-geojson b.geojson
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ASSESSMENT_CSV = ROOT / "data" / "raw" / "Property_Assessment_Data__Current_Calendar_Year_.csv"
DEFAULT_BOUNDARIES_GEOJSON = ROOT / "data" / "raw" / "neighbourhoods.geojson"
DEFAULT_BASELINE = ROOT / "data" / "expected_unmatched.json"

EXIT_OK = 0
EXIT_DRIFT = 5


def compute_unmatched(assessment_names: set[str], boundary_names: set[str]) -> dict[str, set[str]]:
    """The two money-path unmatched sets, given the post-correction name sets."""
    return {
        "assessment_not_in_boundaries": assessment_names - boundary_names,
        "boundaries_not_in_assessment": boundary_names - assessment_names,
    }


def compare_to_baseline(
    live: dict[str, set[str]], expected: dict[str, set[str]]
) -> tuple[str, dict[str, dict[str, set[str]]]]:
    """Compare live unmatched sets to the baseline.

    Returns ``(result, detail)``. ``result`` is ``"ok"`` when nothing new dropped
    out (added assessment-side names are the only hard failure), else ``"drift"``.
    ``detail`` maps each set name to ``{"added": ..., "removed": ...}`` so the
    caller can report exactly what moved.
    """
    detail: dict[str, dict[str, set[str]]] = {}
    for key in ("assessment_not_in_boundaries", "boundaries_not_in_assessment"):
        live_set = live.get(key, set())
        exp_set = expected.get(key, set())
        detail[key] = {"added": live_set - exp_set, "removed": exp_set - live_set}

    # Hard failure ONLY on new assessment names with no boundary (silent dollar
    # loss). Everything else — resolved names, or a new n/a-grey boundary hole —
    # is a warning that asks for a baseline update but does not red the build.
    dropped_dollars = detail["assessment_not_in_boundaries"]["added"]
    return ("drift" if dropped_dollars else "ok"), detail


def _load_baseline(path: Path) -> dict[str, set[str]]:
    """Read the committed baseline; each set is stored as a {name: reason} map."""
    raw = json.loads(path.read_text())
    return {
        "assessment_not_in_boundaries": set(raw.get("assessment_not_in_boundaries", {})),
        "boundaries_not_in_assessment": set(raw.get("boundaries_not_in_assessment", {})),
    }


def _load_live_names(assessment_csv: Path, boundaries_geojson: Path) -> dict[str, set[str]]:
    """Run the real loaders so names go through NAME_CORRECTIONS + the zero drop."""
    sys.path.insert(0, str(ROOT / "src"))
    from load_assessment import load_assessment  # noqa: PLC0415 — heavy import, only when needed
    from load_boundaries import load_boundaries  # noqa: PLC0415

    assessment = load_assessment(str(assessment_csv))
    boundaries = load_boundaries(str(boundaries_geojson))
    return compute_unmatched(
        set(assessment["neighbourhood_name"]),
        set(boundaries["neighbourhood_name"]),
    )


def _write_github_output(**kv: object) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def _fmt(names: set[str]) -> str:
    return ", ".join(sorted(names)) if names else "(none)"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--assessment-csv", type=Path, default=DEFAULT_ASSESSMENT_CSV)
    p.add_argument("--boundaries-geojson", type=Path, default=DEFAULT_BOUNDARIES_GEOJSON)
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    expected = _load_baseline(args.baseline)
    live = _load_live_names(args.assessment_csv, args.boundaries_geojson)
    result, detail = compare_to_baseline(live, expected)

    a = detail["assessment_not_in_boundaries"]
    b = detail["boundaries_not_in_assessment"]

    # Benign, exit-0 warnings: resolved names (baseline now stale) + new n/a holes.
    if a["removed"] or b["removed"]:
        logger.warning(
            "Resolved name(s) now matching (update data/expected_unmatched.json): "
            "assessment-side [%s], boundary-side [%s]",
            _fmt(a["removed"]), _fmt(b["removed"]),
        )
    if b["added"]:
        logger.warning(
            "NEW boundary neighbourhood(s) with no assessment data (rendered n/a grey; "
            "update the baseline if intentional): %s",
            _fmt(b["added"]),
        )

    if result == "drift":
        logger.error(
            "NAME DRIFT — %d assessment neighbourhood(s) newly have no boundary match, "
            "so their assessed value is silently dropped from the map: %s\n"
            "Investigate (spatial containment via the assessment lat/lon is the decisive "
            "test — DATA.md 'Name Matching'); add a NAME_CORRECTIONS entry or, if truly "
            "immaterial+intentional, add the name to data/expected_unmatched.json.",
            len(a["added"]), _fmt(a["added"]),
        )
        _write_github_output(
            result="drift",
            added_assessment=_fmt(a["added"]),
            added_boundary=_fmt(b["added"]),
        )
        return EXIT_DRIFT

    logger.info(
        "Unmatched-name guard OK: assessment-side unmatched %s; boundary-side unmatched %s "
        "(both match the committed baseline).",
        _fmt(live["assessment_not_in_boundaries"]),
        _fmt(live["boundaries_not_in_assessment"]),
    )
    _write_github_output(result="ok")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

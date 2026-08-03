"""Schema guard: fail CI loud when a column disappears from the served GeoJSON.

Every lens in ``web/index.html`` self-gates on its own column — a services row
hides itself when its column is absent, a tooltip row is omitted rather than
printed as NaN, a view button is removed when its metric is missing. That
degradation is deliberate and correct (it is what lets a new column ship a week
before its data does), but it means **a silently dropped column looks exactly
like a feature that was never built**. No error, no NaN, no banner: the lens
simply is not there, and the site publishes without it.

``verify-smoke.js`` cannot close this. Everything it asserts is derived from the
served file itself, so when a column vanishes the check vanishes with it (its B7
comment says so, and B5 documents the same limit for temporal.json). Catching a
disappearance needs *memory of what was there last week*, which is what the
committed baseline in ``data/expected_columns.json`` provides.

This is the schema half of the guard family, not the value half:

  * ``check_value_anchors.py`` pins the cardinality REGIME in numeric bands.
  * ``check_unmatched_names.py`` pins which names are allowed to go unmatched.
  * this one pins WHICH COLUMNS EXIST — a list, not a measurement, so it moves
    only when someone changes the pipeline on purpose. A schema baseline cannot
    cry wolf at the January reassessment the way a value baseline can.

Direction policy matches ``check_unmatched_names.py``:

  * a baselined column MISSING, or present on only SOME features → FAIL. Both
    are the drop this guard exists for; partial presence additionally means the
    join lost rows.
  * a NEW column not in the baseline → warn and ask for a re-pin, never red.
    Columns get added constantly here and a guard that blocks the publish on
    every new metric would be turned off within a month.

⚠️ ON THE DEGRADED GROUND-ACRE-ONLY MODE. ``main.py`` drops the
``*_per_lot_acre`` family when the property-info CSV is absent, and
``check_value_anchors.py`` deliberately SKIPS in that case. This guard does not:
that mode is legitimate for a local run but not for a publish, and skipping is
precisely how a site would go out silently missing a metric. In CI the CSV is
fetched by ``download_data.py``, so reaching that state already means the
download half-failed — worth stopping the publish over. Re-pin only when the
removal is intended.

Outcomes (exit codes; 2 is argparse's):
  0  ok    — every baselined column present on every feature.
  5  drift — a column vanished or went partial. FAIL.

Runs in CI (refresh.yml) AFTER regeneration, so it sees the file the site is
about to serve. Re-pin with ``--write-baseline`` when a change is intentional.

Usage:
    python scripts/check_served_columns.py                    # live geojson + baseline
    python scripts/check_served_columns.py --write-baseline   # re-pin after an intended change
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GEOJSON = ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson"
DEFAULT_BASELINE = ROOT / "data" / "expected_columns.json"

EXIT_OK = 0
EXIT_DRIFT = 5


def column_presence(features: list[dict]) -> dict[str, int]:
    """Map every column seen anywhere to the number of features carrying it.

    Counts KEY PRESENCE, not non-null values. A null is a legitimate "no value
    for this neighbourhood" — the four ``*_per_lot_acre`` columns are null on
    the seven set-aside hoods by design — whereas a missing key means the
    pipeline never wrote the column for that row. Same distinction B6/B7 draw
    in ``verify-smoke.js``, so the two guards answer the same question.
    """
    counts: dict[str, int] = {}
    for feature in features:
        for column in feature.get("properties", {}):
            counts[column] = counts.get(column, 0) + 1
    return counts


def compare_to_baseline(
    counts: dict[str, int], total: int, baseline: list[str]
) -> tuple[list[str], list[str], list[str]]:
    """Split the served schema against the committed one.

    Returns ``(missing, partial, added)``. ``missing`` and ``partial`` are the
    failing directions; ``added`` is benign and only asks for a re-pin.
    """
    missing = sorted(c for c in baseline if c not in counts)
    partial = sorted(c for c in baseline if 0 < counts.get(c, 0) < total)
    added = sorted(c for c in counts if c not in baseline)
    return missing, partial, added


def _write_github_output(**kv: object) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--geojson", type=Path, default=DEFAULT_GEOJSON)
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument(
        "--write-baseline",
        action="store_true",
        help="overwrite the baseline with the live schema (use when a change is intended)",
    )
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    # Deliberately NOT a skip. An absent served geojson means the pipeline did
    # not produce the file the whole site reads; there is no degraded reading of
    # that worth publishing past.
    if not args.geojson.exists():
        logger.error("Served GeoJSON not found: %s", args.geojson)
        _write_github_output(result="drift", missing="<no served geojson>")
        return EXIT_DRIFT

    features = json.loads(args.geojson.read_text()).get("features", [])
    if not features:
        logger.error("Served GeoJSON %s carries no features.", args.geojson)
        _write_github_output(result="drift", missing="<no features>")
        return EXIT_DRIFT

    counts = column_presence(features)
    total = len(features)

    if args.write_baseline:
        payload = {
            "_note": (
                "Columns the served neighbourhood GeoJSON must carry "
                "(scripts/check_served_columns.py). A list, not a measurement: "
                "it changes only when the pipeline changes on purpose. Removing "
                "an entry is how you retire a column deliberately."
            ),
            "columns": sorted(counts),
        }
        args.baseline.write_text(json.dumps(payload, indent=2) + "\n")
        logger.info("Wrote baseline %s with %d columns.", args.baseline, len(counts))
        return EXIT_OK

    baseline = json.loads(args.baseline.read_text())["columns"]
    missing, partial, added = compare_to_baseline(counts, total, baseline)

    for column in added:
        logger.warning(
            "  %-28s NEW — not in the baseline (re-pin with --write-baseline)", column
        )
    for column in partial:
        logger.error(
            "  %-28s PARTIAL — on %d of %d features", column, counts[column], total
        )
    for column in missing:
        logger.error("  %-28s MISSING — gone from every feature", column)

    if missing or partial:
        logger.error(
            "SERVED-COLUMN DRIFT — %d missing, %d partial, out of %d baselined "
            "columns on %d features.\n"
            "Every lens self-gates on its own column, so this does NOT crash the "
            "site: the affected rows and views simply disappear and the publish "
            "looks clean. Do NOT re-pin the baseline to make this pass — find why "
            "the column stopped being written (a renamed source field, a join that "
            "dropped rows, a loader that returned early). Re-pin only once the "
            "removal is understood AND intended.",
            len(missing), len(partial), len(baseline), total,
        )
        _write_github_output(
            result="drift", missing=",".join(missing), partial=",".join(partial)
        )
        return EXIT_DRIFT

    logger.info(
        "Served-column guard OK: all %d baselined columns present on all %d features%s.",
        len(baseline), total, f" ({len(added)} new, unpinned)" if added else "",
    )
    _write_github_output(result="ok")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

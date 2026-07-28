"""Value-anchor guard: fail CI loud when the record-to-parcel cardinality regime shifts.

The two known cardinality distortions — WEM-style needles (huge value on one
point) and condo shared-lot duplication — are handled today by the repeat-aware
dedupe in ``export_value_grid._point_lot_stats`` (``SHARE_MAX_M2``). But
``docs/FINDINGS_lot_dedupe.md`` §4.3 records something that makes those guards
fragile in a specific way: **the dedupe is currently a no-op.** "Never dedupe"
produces identical output, because parcel-sized lot values repeated across units
barely exist in the present data. The threshold is insurance calibrated against
a regime that is not here yet.

So the risk is not the bug returning; it is the *data regime* shifting under a
heuristic nobody is watching — most plausibly at the January year-roll
(``docs/RUNBOOK.md``). Nothing in the pipeline would say a word: the numbers
would simply drift, and ``check_lot_acre_bounds`` only catches gross physical
violations (hood lot acres exceeding hood acres), not a needle coming back.

This guard pins the *regime*, not the dollars. Assessed values move every year
on reassessment, so equality checks would cry wolf each January; every anchor is
therefore a band, and the ranking/ratio anchors are expressed as multiples that
survive a uniform revaluation.

Anchors (see ``data/expected_value_anchors.json`` for the committed bands):

  * ``dup_parcel_points`` / ``dup_parcel_value_frac`` — points where a lot value
    >= SHARE_MAX_M2 repeats across units, i.e. the duplicated-parcel regime the
    dedupe exists to catch. THE PRIMARY CANARY: growth here means the dedupe has
    become load-bearing and its threshold needs re-validating.
  * ``dedupe_effect_pct`` — how much raw lot-acre summing overcounts vs deduped.
    ~0.05% today; a jump is the same regime shift seen from the area side.
  * ``ineligible_points`` / ``ineligible_value_frac`` — majority-null multi-unit
    points dropped from the lot-acre metric entirely. Growth = more value
    silently leaving the denominator.
  * ``lot_needle_ratio`` — top cell $/lot-acre divided by the 99.9th percentile,
    read from the EXPORTED grid. A needle is by definition one cell towering
    over the body of the distribution, so this detects the failure mode itself
    (WEM-style or the §4.3 fake-townhouse kind) without naming a parcel, and it
    survives reassessment because it is a ratio.

    **Measured at CELL grain, deliberately.** The obvious point-grain version
    (max $/lot-acre per lat/long point) is anchored to noise: a Westmount point
    holds $0.9M on a sub-milliacre lot = $3,478M/lot-acre, four times the real
    top. It never reaches the map — at 100 m cells it pools with its neighbours,
    and the exported top cells are the Downtown tower's 612/149/143 — so pinning
    it would have failed the build over an artifact nobody can see. This is
    ``FINDINGS_lot_dedupe.md`` §4.3's own lesson: validate at the display grain.

Outcomes (exit codes; 2 is argparse's):
  0  ok    — every anchor inside its committed band.
  5  drift — an anchor moved in the DANGEROUS direction. FAIL.

Anchors moving in the benign direction (fewer ineligible points, a stronger
inversion) warn and ask for a baseline update, but never red the build — same
policy as ``check_unmatched_names.py``.

Runs in CI (refresh.yml) AFTER regeneration, so it sees the roll the site is
about to serve. Regenerate the baseline with ``--write-baseline`` when a move is
understood and intentional.

Usage:
    python scripts/check_value_anchors.py                    # live data/raw + baseline
    python scripts/check_value_anchors.py --write-baseline   # re-pin after an understood move
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ASSESSMENT_CSV = ROOT / "data" / "raw" / "Property_Assessment_Data__Current_Calendar_Year_.csv"
DEFAULT_PROPERTY_INFO_CSV = ROOT / "data" / "raw" / "Property_Info__Current_Calendar_Year_.csv"
DEFAULT_BASELINE = ROOT / "data" / "expected_value_anchors.json"
DEFAULT_GRID_JSON = ROOT / "web" / "data" / "value_grid.json"

EXIT_OK = 0
EXIT_DRIFT = 5

# Which direction is dangerous for each anchor. Every anchor today fails "high"
# — each is a distortion whose growth is the bad news. "low" is supported so an
# anchor whose collapse is the failure can be added without reworking this.
DANGER = {
    "dup_parcel_points": "high",
    "dup_parcel_value_frac": "high",
    "dedupe_effect_pct": "high",
    "ineligible_points": "high",
    "ineligible_value_frac": "high",
    "lot_needle_ratio": "high",
}

# Percentile the top cell is measured against in lot_needle_ratio. High enough
# to sit in the real body of the distribution, robust to a single artifact.
NEEDLE_PCTILE = 99.9


def compute_anchors(df: pd.DataFrame) -> dict[str, float]:
    """Regime anchors for a merged assessment + property-info frame.

    Expects ``latitude``/``longitude``/``assessed_value`` (load_assessment) and
    ``lot_size`` (load_property_info). Reuses the SHIPPED dedupe heuristic via
    ``_point_lot_stats`` so the guard tracks the real rule rather than a copy of
    it — if the heuristic changes, these anchors move with it by construction.
    """
    sys.path.insert(0, str(ROOT / "src"))
    from export_value_grid import (  # noqa: PLC0415 — heavy import, only when needed
        SHARE_MAX_M2,
        _point_lot_stats,
    )

    pts = df[["latitude", "longitude", "assessed_value", "lot_size"]].dropna(
        subset=["latitude", "longitude"]
    )
    stats = _point_lot_stats(pts)

    lot = pts["lot_size"].where(pts["lot_size"] > 0)
    total_value = float(pts["assessed_value"].sum())

    # Duplicated-parcel regime: a parcel-sized value repeated across units at one
    # point. This is exactly what the >= SHARE_MAX_M2 branch of the dedupe eats,
    # so its size tells us whether that branch is doing any work at all.
    repeats = (
        pts.assign(_lot=lot)
        .dropna(subset=["_lot"])
        .groupby(["latitude", "longitude", "_lot"], sort=False)
        .size()
        .rename("k")
        .reset_index()
    )
    dup = repeats[(repeats["k"] > 1) & (repeats["_lot"] >= SHARE_MAX_M2)]
    dup_points = dup[["latitude", "longitude"]].drop_duplicates()

    value_by_point = pts.groupby(["latitude", "longitude"], sort=False)["assessed_value"].sum()
    dup_value = float(
        value_by_point.reindex(
            pd.MultiIndex.from_frame(dup_points), fill_value=0.0
        ).sum()
    )

    # Area side of the same question: raw summing vs the deduped contribution.
    raw_lot_m2 = float(lot.sum())
    dedup_lot_m2 = float(stats["lot_m2"].sum())
    dedupe_effect_pct = (
        (raw_lot_m2 - dedup_lot_m2) / dedup_lot_m2 * 100.0 if dedup_lot_m2 else 0.0
    )

    ineligible = stats[~stats["eligible"]]
    inel_value = float(
        value_by_point.reindex(
            pd.MultiIndex.from_frame(ineligible[["latitude", "longitude"]]), fill_value=0.0
        ).sum()
    )

    return {
        "dup_parcel_points": float(len(dup_points)),
        "dup_parcel_value_frac": dup_value / total_value if total_value else 0.0,
        "dedupe_effect_pct": dedupe_effect_pct,
        "ineligible_points": float(len(ineligible)),
        "ineligible_value_frac": inel_value / total_value if total_value else 0.0,
    }


def compute_needle_ratio(grid: dict, column: str = "value_per_lot_acre") -> float:
    """Top cell over the ``NEEDLE_PCTILE`` cell, from an exported value grid.

    Takes the parsed ``value_grid.json`` (``columns`` + ``cells``) rather than
    recomputing, so the guard measures the artifact the site actually serves.
    """
    idx = grid["columns"].index(column)
    vals = sorted(c[idx] for c in grid["cells"] if c[idx] is not None)
    if not vals:
        raise ValueError(f"no non-null {column} cells in the grid")
    body = float(np.percentile(vals, NEEDLE_PCTILE))
    return float(vals[-1]) / body if body else float("inf")


def compare_to_baseline(
    live: dict[str, float], baseline: dict[str, dict[str, float]]
) -> tuple[str, dict[str, dict]]:
    """Compare live anchors to the committed bands.

    Returns ``(result, detail)``. ``result`` is ``"drift"`` only when an anchor
    left its band in the DANGEROUS direction (``DANGER``); the benign side is
    reported so the baseline can be re-pinned, but does not fail the build.
    """
    detail: dict[str, dict] = {}
    dangerous = False
    for key, value in live.items():
        band = baseline.get(key)
        if band is None:
            detail[key] = {"value": value, "status": "unpinned"}
            continue
        lo, hi = float(band["min"]), float(band["max"])
        if value < lo:
            status = "drift" if DANGER.get(key) == "low" else "benign"
        elif value > hi:
            status = "drift" if DANGER.get(key) == "high" else "benign"
        else:
            status = "ok"
        dangerous = dangerous or status == "drift"
        detail[key] = {"value": value, "min": lo, "max": hi, "status": status}
    return ("drift" if dangerous else "ok"), detail


def _load_live(assessment_csv: Path, property_info_csv: Path) -> pd.DataFrame:
    """Run the real loaders so the guard sees exactly what the pipeline sees."""
    sys.path.insert(0, str(ROOT / "src"))
    from load_assessment import load_assessment  # noqa: PLC0415
    from load_property_info import load_property_info  # noqa: PLC0415

    assessment = load_assessment(str(assessment_csv))
    info = load_property_info(str(property_info_csv))
    return assessment.merge(info, on="account_number", how="left")


def _write_github_output(**kv: object) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def _band(value: float, tol: float) -> dict[str, float]:
    """A +/- ``tol`` fractional band around ``value``, floored sanely at zero."""
    span = abs(value) * tol
    return {"min": round(max(0.0, value - span), 6), "max": round(value + span, 6)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--assessment-csv", type=Path, default=DEFAULT_ASSESSMENT_CSV)
    p.add_argument("--property-info-csv", type=Path, default=DEFAULT_PROPERTY_INFO_CSV)
    p.add_argument("--grid-json", type=Path, default=DEFAULT_GRID_JSON)
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument(
        "--write-baseline",
        action="store_true",
        help="recompute and overwrite the baseline bands (use when a move is understood)",
    )
    p.add_argument(
        "--tolerance",
        type=float,
        default=0.5,
        help="fractional half-width of generated bands with --write-baseline (default 0.5)",
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

    # main.py degrades to ground-acre only when the property-info CSV is absent
    # (and then the grid carries no lot-acre column at all). That is a handled
    # condition, not a regime shift — skip rather than invent a hard failure the
    # pipeline deliberately avoids. The dollars path is guarded separately by
    # check_unmatched_names.py.
    for missing, what in ((args.assessment_csv, "assessment CSV"),
                          (args.property_info_csv, "property-info CSV"),
                          (args.grid_json, "exported value grid")):
        if not missing.exists():
            logger.warning(
                "SKIPPING value-anchor guard — %s not found (%s). The lot-acre "
                "metric degrades to ground-acre only; nothing to anchor.",
                what, missing,
            )
            _write_github_output(result="skipped")
            return EXIT_OK

    grid = json.loads(args.grid_json.read_text())
    if "value_per_lot_acre" not in grid.get("columns", []):
        logger.warning(
            "SKIPPING value-anchor guard — the exported grid has no "
            "value_per_lot_acre column, so the pipeline ran ground-acre only."
        )
        _write_github_output(result="skipped")
        return EXIT_OK

    df = _load_live(args.assessment_csv, args.property_info_csv)
    live = compute_anchors(df)
    live["lot_needle_ratio"] = compute_needle_ratio(grid)

    if args.write_baseline:
        payload = {
            "_note": (
                "Regime anchors for the record-to-parcel cardinality guard "
                "(scripts/check_value_anchors.py). Bands, not equalities: assessed "
                "values move every reassessment. See docs/FINDINGS_lot_dedupe.md and "
                "docs/FINDINGS_denominator_cardinality.md."
            ),
            **{k: _band(v, args.tolerance) for k, v in live.items()},
        }
        args.baseline.write_text(json.dumps(payload, indent=2) + "\n")
        logger.info("Wrote baseline %s from live data: %s", args.baseline, live)
        return EXIT_OK

    baseline = json.loads(args.baseline.read_text())
    result, detail = compare_to_baseline(live, baseline)

    for key, d in sorted(detail.items()):
        if d["status"] == "ok":
            logger.info("  %-24s %.6g  (band %.6g-%.6g)", key, d["value"], d["min"], d["max"])
        elif d["status"] == "unpinned":
            logger.warning("  %-24s %.6g  NOT PINNED — add it to the baseline", key, d["value"])
        elif d["status"] == "benign":
            logger.warning(
                "  %-24s %.6g  outside band %.6g-%.6g in the BENIGN direction "
                "(re-pin with --write-baseline if this is the new normal)",
                key, d["value"], d["min"], d["max"],
            )
        else:
            logger.error(
                "  %-24s %.6g  outside band %.6g-%.6g — DANGEROUS direction",
                key, d["value"], d["min"], d["max"],
            )

    if result == "drift":
        moved = [k for k, d in detail.items() if d["status"] == "drift"]
        logger.error(
            "VALUE-ANCHOR DRIFT — %d anchor(s) moved dangerously: %s\n"
            "This means the record-to-parcel cardinality regime changed, so the "
            "repeat-aware dedupe (SHARE_MAX_M2) and the lot-acre denominator may no "
            "longer be calibrated. Do NOT re-pin the baseline until the cause is "
            "understood: re-run tools/audit_cardinality_denominators.py and check "
            "docs/FINDINGS_lot_dedupe.md §3-§5 against the new data.",
            len(moved), ", ".join(sorted(moved)),
        )
        _write_github_output(result="drift", moved=",".join(sorted(moved)))
        return EXIT_DRIFT

    logger.info("Value-anchor guard OK: all %d anchors inside their committed bands.", len(detail))
    _write_github_output(result="ok")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

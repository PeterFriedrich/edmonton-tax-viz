"""Permit-name guard: file an issue when a NEW permit neighbourhood name misses the boundaries.

The permit name join is warn-not-fail by decision (an unmatched permit hood is a
blank or low hood, not a dropped dollar), so its only signal was a build-log
warning. On 2026-11-10 that let a City respelling go unseen: 15 of the 16
``CHAPPELLE AREA, HERITAGE VALLEY AREA`` rows became ``CHAPPELLE, HERITAGE VALLEY
AREA``, the correction key stopped matching them, and CHAPPELLE shipped 28 units
low. ⚠️ A guard on correction keys that match no row would have MISSED it: one
row kept the old spelling, so the key never died. What did move was the
unmatched set (14 names / 537 units → 15 / 565), so this guard watches that set.

It runs the real ``load_permits`` over the since-2009 window (every published
permit window is inside it) and compares the names with no boundary polygon
against the ``permits_not_in_boundaries`` baseline in
``data/expected_unmatched.json``. Names come from the residential AND industrial
aggregates, so an industrial-only name is covered too.

  * a NEW name → ``flagged=<n>`` and a markdown report; CI files an issue.
    Someone has to decide where those units go (a ``PERMIT_NAME_CORRECTIONS``
    key, or the baseline if it straddles hoods by decision).
  * a name that LEFT the set → a log warning only: the baseline is stale, and
    nothing is wrong on the site.

Always exits 0 — this signal is never allowed to block the publish.

Usage:
    python scripts/check_permit_names.py                      # live data/raw + baseline
    python scripts/check_permit_names.py --report out.md      # write the issue body
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PERMITS_CSV = ROOT / "data" / "raw" / "building_permits.csv"
DEFAULT_BOUNDARIES_GEOJSON = ROOT / "data" / "raw" / "neighbourhoods.geojson"
DEFAULT_BASELINE = ROOT / "data" / "expected_unmatched.json"
BASELINE_KEY = "permits_not_in_boundaries"


def unmatched_permits(permits: pd.DataFrame, boundary_names: set[str]) -> pd.DataFrame:
    """Rows of the ``load_permits`` output whose hood has no boundary polygon."""
    return permits.loc[~permits["neighbourhood_name"].isin(boundary_names)]


def compare_to_baseline(live: set[str], expected: set[str]) -> tuple[set[str], set[str]]:
    """``(added, removed)``: names new to the unmatched set, and names that left it."""
    return live - expected, expected - live


def render(added: pd.DataFrame) -> str:
    """Markdown body for the GitHub issue."""
    lines = [
        "The weekly refresh found permit neighbourhood name(s) that match no "
        "boundary polygon and are not in the `permits_not_in_boundaries` baseline "
        "(`data/expected_unmatched.json`). Their permits are counted citywide but "
        "placed in no neighbourhood, so the hood they belong to reads low.",
        "",
        "**Nothing is blocked**: the refresh published normally.",
        "",
        "| Name | Units since 2009 | Residential permits | Industrial permits |",
        "|---|---|---|---|",
    ]
    for r in added.sort_values("new_dwelling_units", ascending=False).itertuples():
        ind = getattr(r, "ind_permits", 0)
        lines.append(
            f"| `{r.neighbourhood_name}` | {r.new_dwelling_units:,.0f} | "
            f"{r.new_dwelling_permits:,.0f} | {0 if pd.isna(ind) else int(ind):,} |"
        )
    lines += [
        "",
        "**Triage:** `docs/RUNBOOK.md` §0f. In short: a respelling of a name "
        "already corrected, or a list that resolves to one hood, gets a "
        "`PERMIT_NAME_CORRECTIONS` key (`src/load_permits.py`). A list that "
        "straddles two or more hoods goes into the baseline with its reason. "
        "Close this issue when the PR lands.",
    ]
    return "\n".join(lines) + "\n"


def _load_live(permits_csv: Path, boundaries_geojson: Path) -> tuple[pd.DataFrame, set[str]]:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))
    import main  # noqa: PLC0415 — heavy import; main.py owns the window pins
    from load_boundaries import load_boundaries  # noqa: PLC0415
    from load_permits import load_permits  # noqa: PLC0415

    permits = load_permits(str(permits_csv), main.PERMIT_YEARS_LONG)
    boundaries = load_boundaries(str(boundaries_geojson))
    return permits, set(boundaries["neighbourhood_name"])


def _write_github_output(**kv: object) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--permits-csv", type=Path, default=DEFAULT_PERMITS_CSV)
    p.add_argument("--boundaries-geojson", type=Path, default=DEFAULT_BOUNDARIES_GEOJSON)
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument("--report", type=Path, help="write the markdown issue body here")
    args = p.parse_args(argv)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)s: %(message)s")

    expected = set(json.loads(args.baseline.read_text()).get(BASELINE_KEY, {}))
    permits, boundary_names = _load_live(args.permits_csv, args.boundaries_geojson)
    unmatched = unmatched_permits(permits, boundary_names)
    added, removed = compare_to_baseline(set(unmatched["neighbourhood_name"]), expected)

    if removed:
        logger.warning(
            "Permit name(s) left the unmatched set (remove from %s in %s): %s",
            BASELINE_KEY, args.baseline.name, ", ".join(sorted(removed)),
        )
    if not added:
        logger.info("Permit-name guard OK: %d unmatched names, all in the baseline.", len(unmatched))
        _write_github_output(flagged=0)
        return 0

    new_rows = unmatched.loc[unmatched["neighbourhood_name"].isin(added)]
    report = render(new_rows)
    logger.warning("NEW unmatched permit name(s): %s", ", ".join(sorted(added)))
    if args.report:
        args.report.write_text(report)
    # Plain text: the names are the City's strings and the title passes through a shell.
    title = f"⚠️ New unmatched permit name — {' | '.join(sorted(added))}"
    _write_github_output(flagged=len(added), title=title)
    return 0


if __name__ == "__main__":
    sys.exit(main())

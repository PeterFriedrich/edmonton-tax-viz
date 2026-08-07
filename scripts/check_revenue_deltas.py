"""Magnitude guard: notice when ONE neighbourhood's revenue moves a lot.

Every other guard in this family is a citywide aggregate or a schema check, and
that is the hole this fills. On 2026-08-03 ``WEST MEADOWLARK PARK``'s
``total_revenue`` went $4.63M -> $10.63M (+130%) in a single auto-refresh. The
run was GREEN: nothing failed, no email, and the doubled number served on the
live map for four days until it was found by hand while diffing two git
revisions for an unrelated reason.

Nothing could have caught it. ``check_value_anchors.py`` is the closest and it
pins the record-to-parcel CARDINALITY regime — dedup ratios over the whole roll,
which one arriving parcel cannot move. Citywide the event was +0.22%. The
failure was per-neighbourhood, and no guard looked there.

Direction policy: this one only ever WARNS.

  * ``check_served_columns.py`` / ``check_unmatched_names.py`` fail the publish,
    because a dropped column or a broken join is never legitimate.
  * a neighbourhood's revenue doubling often IS legitimate — a large parcel
    completes, a reassessment lands. There is no threshold that separates "real"
    from "wrong" without a human looking, so blocking the publish would red the
    weekly refresh on good data and be switched off within a month. This reports
    and exits 0. ALWAYS. The refresh commits and deploys either way.

⚠️ THE THRESHOLD IS TWO CONDITIONS AND BOTH ARE LOAD-BEARING. Percentage alone
cries wolf: small edge neighbourhoods swing hard on a few completed houses.
Measured over every auto-refresh that has ever changed this file:

    2026-07-20   117 hoods moved   worst CANON RIDGE      +3.1%   +$67K
    2026-07-27   155 hoods moved   worst ALCES           +12.7%  +$501K
    2026-08-03    77 hoods moved   worst WEST MEADOWLARK +129.7%  +$6,001,962
                                   next-largest that run  -1.2%  -$102K

ALCES is why ``MIN_ABS_DOLLARS`` exists — it clears 10% on ordinary churn and is
half a million dollars. The pair fires on exactly ONE event in all recorded
history, with a ~100x margin to the next-largest mover in the same run. Widen
before narrowing: a guard nobody believes is worse than no guard.

The baseline is the PREVIOUS COMMITTED version of the served file
(``git show HEAD:<path>``), already in the checkout — no pinned JSON to re-pin,
no new data, no new dependency. That is deliberate: the question is "what
changed since the last publish", which git already answers, and a pinned
baseline would need re-pinning after every legitimate move.

Also reported, because it is free and it is what cracked the West Meadowlark
case in minutes: the largest ``rev_frac_*`` shift on each flagged hood. There
``rev_frac_inst`` went 0.059 -> 0.590, which pointed straight at an institutional
parcel (a UF-zoned $247.8M account that had not been on the taxable roll before)
instead of a generic "something moved".

Outcomes (exit codes; 2 is argparse's):
  0  always — flagged or not. Prints the report; sets ``flagged`` for CI.

Runs in CI (refresh.yml) AFTER regeneration and BEFORE the commit, so it
compares the artifact about to be served against the one currently served. When
it flags, the workflow files a GitHub issue so the notification email arrives —
same channel as ``vintage-digest.yml``, and for the same reason: a warning in a
green run reaches nobody.

Usage:
    python scripts/check_revenue_deltas.py                  # vs git HEAD
    python scripts/check_revenue_deltas.py --before old.geojson --after new.geojson
    python scripts/check_revenue_deltas.py --report out.md  # write the issue body
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GEOJSON = ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson"

# Both must hold for a hood to be flagged — see the docstring's measurements.
MIN_PCT = 10.0
MIN_ABS_DOLLARS = 1_000_000.0

METRIC = "total_revenue"
NAME_KEY = "neighbourhood_name"

EXIT_OK = 0


def load_features(path: Path) -> dict[str, dict]:
    """Map neighbourhood name -> properties, from a served GeoJSON on disk."""
    payload = json.loads(path.read_text())
    return {
        f["properties"][NAME_KEY]: f["properties"] for f in payload.get("features", [])
    }


def load_committed(path: Path, rev: str = "HEAD") -> dict[str, dict] | None:
    """Same, from the version of ``path`` committed at ``rev``.

    Returns None when the file is not in that commit at all — a first publish,
    or a fresh clone with no history for it. That is "nothing to compare
    against", not a fault, and the caller reports it as a skip.
    """
    rel = path.resolve().relative_to(ROOT)
    proc = subprocess.run(
        ["git", "show", f"{rev}:{rel.as_posix()}"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if proc.returncode != 0:
        return None
    payload = json.loads(proc.stdout)
    return {
        f["properties"][NAME_KEY]: f["properties"] for f in payload.get("features", [])
    }


def biggest_frac_shift(before: dict, after: dict) -> tuple[str, float, float] | None:
    """Largest absolute move among the ``rev_frac_*`` composition columns.

    The revenue-mix fingerprint of whatever caused the delta. A jump in
    ``rev_frac_inst`` means institutional value arrived; ``rev_frac_commercial``
    means a commercial reassessment; no shift at all means the hood scaled
    uniformly, which reads as a rate change rather than a parcel event.
    """
    best = None
    for key, old in before.items():
        if not key.startswith("rev_frac_"):
            continue
        new = after.get(key)
        if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
            continue
        if best is None or abs(new - old) > abs(best[2] - best[1]):
            best = (key, float(old), float(new))
    return best


def compare(
    before: dict[str, dict],
    after: dict[str, dict],
    min_pct: float = MIN_PCT,
    min_abs: float = MIN_ABS_DOLLARS,
) -> tuple[list[dict], list[str], list[str]]:
    """Split the two served files into (flagged movers, appeared, disappeared).

    A hood is flagged only when BOTH thresholds are cleared. Hoods entering or
    leaving the file are reported unconditionally — there is no percentage to
    compute, and either direction is worth a human look on a file whose feature
    count has been 406 for its whole recorded history.
    """
    flagged = []
    for name, old_props in before.items():
        new_props = after.get(name)
        if new_props is None:
            continue
        old = old_props.get(METRIC)
        new = new_props.get(METRIC)
        if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
            continue
        if old <= 0:
            continue
        delta = float(new) - float(old)
        pct = delta / float(old) * 100.0
        if abs(pct) >= min_pct and abs(delta) >= min_abs:
            flagged.append(
                {
                    "name": name,
                    "before": float(old),
                    "after": float(new),
                    "delta": delta,
                    "pct": pct,
                    "frac_shift": biggest_frac_shift(old_props, new_props),
                }
            )
    flagged.sort(key=lambda r: -abs(r["delta"]))
    appeared = sorted(n for n in after if n not in before)
    disappeared = sorted(n for n in before if n not in after)
    return flagged, appeared, disappeared


def render(
    flagged: list[dict], appeared: list[str], disappeared: list[str], total: int
) -> str:
    """Markdown body for the GitHub issue (and the console report)."""
    lines = [
        "## Large per-neighbourhood revenue change in this refresh",
        "",
        f"`{METRIC}` moved by **≥{MIN_PCT:.0f}% AND ≥${MIN_ABS_DOLLARS:,.0f}** "
        f"in {len(flagged)} of {total} neighbourhoods.",
        "",
        "⚠️ **This is a heads-up, not a failure.** The refresh committed and "
        "deployed normally — a hood's revenue doubling is often legitimate (a "
        "large parcel completes, a reassessment lands). It needs a human to say "
        "which this is.",
        "",
    ]
    if flagged:
        lines += [
            "| neighbourhood | before | after | change | revenue mix |",
            "|---|---|---|---|---|",
        ]
        for r in flagged:
            shift = r["frac_shift"]
            mix = (
                f"`{shift[0]}` {shift[1]:.3f} → {shift[2]:.3f}"
                if shift and abs(shift[2] - shift[1]) >= 0.01
                else "unchanged (scaled uniformly)"
            )
            lines.append(
                f"| **{r['name']}** | ${r['before']:,.0f} | ${r['after']:,.0f} "
                f"| **{r['pct']:+.1f}%** (${r['delta']:+,.0f}) | {mix} |"
            )
        lines.append("")
    if appeared:
        lines += [f"**Neighbourhoods that APPEARED:** {', '.join(appeared)}", ""]
    if disappeared:
        lines += [f"**Neighbourhoods that DISAPPEARED:** {', '.join(disappeared)}", ""]
    lines += [
        "### How to investigate",
        "",
        "A shift in `rev_frac_inst` / `rev_frac_commercial` means value of that "
        "class arrived or left, so start on the roll:",
        "",
        "```",
        "# the parcels now in the hood, largest first",
        "curl -s 'https://data.edmonton.ca/resource/q7d6-ambg.json' \\",
        "  --data-urlencode \"\\$where=upper(neighbourhood)='<HOOD>'\" \\",
        "  --data-urlencode '$order=assessed_value::number DESC' \\",
        "  --data-urlencode '$limit=10' -G",
        "```",
        "",
        "Then diff against the previous served file to confirm the size of the "
        "move and rule out a transfer from a neighbouring hood:",
        "",
        "```",
        "git diff HEAD~1 -- web/data/neighbourhood_value_per_acre.geojson",
        "```",
        "",
        "Precedent: `WEST MEADOWLARK PARK` +130% on 2026-08-03 — one new "
        "$247.8M UF-zoned account on the taxable roll, taxed at the "
        "Non-Residential rate. See `docs/TODO_archive.md`.",
    ]
    return "\n".join(lines) + "\n"


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
    p.add_argument(
        "--before",
        type=Path,
        help="baseline GeoJSON on disk (default: the --geojson path at git HEAD)",
    )
    p.add_argument("--after", type=Path, help="alias for --geojson")
    p.add_argument("--rev", default="HEAD", help="git rev for the baseline")
    p.add_argument("--min-pct", type=float, default=MIN_PCT)
    p.add_argument("--min-abs", type=float, default=MIN_ABS_DOLLARS)
    p.add_argument("--report", type=Path, help="write the markdown report here")
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    after_path = args.after or args.geojson
    if not after_path.exists():
        # Unlike the schema guard this does not fail: an absent file is already
        # a hard failure in the steps above, and this one must never be the
        # reason a publish stops.
        logger.warning("No served GeoJSON at %s — nothing to compare.", after_path)
        _write_github_output(flagged="0")
        return EXIT_OK

    after = load_features(after_path)
    before = (
        load_features(args.before)
        if args.before
        else load_committed(after_path, args.rev)
    )
    if before is None:
        logger.info(
            "No committed %s at %s — first publish, nothing to compare against.",
            after_path.name, args.rev,
        )
        _write_github_output(flagged="0")
        return EXIT_OK

    flagged, appeared, disappeared = compare(
        before, after, args.min_pct, args.min_abs
    )

    if not (flagged or appeared or disappeared):
        logger.info(
            "Revenue-delta guard OK: no neighbourhood moved ≥%.0f%% and ≥$%s "
            "across %d neighbourhoods.",
            args.min_pct, f"{args.min_abs:,.0f}", len(after),
        )
        _write_github_output(flagged="0")
        return EXIT_OK

    for r in flagged:
        logger.warning(
            "  %-32s $%s -> $%s  (%+.1f%%, $%s)",
            r["name"], f"{r['before']:,.0f}", f"{r['after']:,.0f}",
            r["pct"], f"{r['delta']:+,.0f}",
        )
    for name in appeared:
        logger.warning("  %-32s APPEARED", name)
    for name in disappeared:
        logger.warning("  %-32s DISAPPEARED", name)

    report = render(flagged, appeared, disappeared, len(after))
    if args.report:
        args.report.write_text(report)

    logger.warning(
        "BIG REVENUE DELTA — %d neighbourhood(s) moved ≥%.0f%% and ≥$%s. "
        "NOT a failure: the refresh publishes anyway. A hood's revenue can "
        "legitimately double when a large parcel completes. Investigate which "
        "this is; see the report for how.",
        len(flagged), args.min_pct, f"{args.min_abs:,.0f}",
    )
    _write_github_output(
        flagged=str(len(flagged) + len(appeared) + len(disappeared)),
        title=f"⚠️ Big revenue delta — {flagged[0]['name'] if flagged else 'membership change'}",
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

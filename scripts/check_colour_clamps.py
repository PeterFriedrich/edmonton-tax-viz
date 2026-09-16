"""Money colour-clamp guard: the legend must mean what the clamp does, and drift
must be loud.

``METRICS`` in ``web/index.html`` carries, per money metric, a hand-set
``colorClamp`` (where the colour ramp saturates) and a hand-typed ``legendMax``
string (what the reader is told it saturates at). Two different failures live
there, and they need different answers:

**A — the legend and the clamp disagree (FAILS, merge gate).** The existing
verify scripts pin the legend STRING (``verify-res-revenue.js``,
``verify-smoke.js`` grep for ``$30k+`` / ``$4M+``), which is the presence kind of
guard: the 2026-09-15 published-numbers audit found they **would pass with the
clamp at $5,000** while the legend still said ``$50k+``. Then every colour on the
map means something other than what the legend says, and nothing is red. This is
fully decidable offline from one file, so it blocks a merge.

**B — the clamp has drifted away from the distribution it was set from (WARNS).**
Each ``colorClamp`` was hand-set near p97.5 of the served values, i.e. ~2.5% of
neighbourhoods saturating. Assessments rise; the clamp does not. Measured
2026-09-16 over the 358 non-set-aside hoods:

    revenue_per_acre        $50,000  p97.5 $57,412  sits at p95.5  16 hoods (4.5%)
    res_revenue_per_acre    $30,000  p97.5 $29,268  sits at p97.8   7 hoods (2.2%)
    nonres_revenue_per_acre $50,000  p97.5 $50,261  sits at p97.2  10 hoods (2.8%)
    value_per_acre       $4,000,000  p97.5 $4,028,947 sits at p97.2 10 hoods (2.8%)

⚠️ **Drift is NOT a defect and this check must never block the publish.** A
literal clamp is deliberate — the ground-acre neighbourhood view is the landing
surface, and a scale that silently re-anchors every week means two visits to the
site are not comparable. Peter's call, 2026-09-16: keep the literal, make the
drift loud. So B reports EVERY run (the table above, recomputed) and flags only
outside ``BAND`` — the signal is "come and re-decide", not "this is wrong".

⚠️ **The band CONTAINS today's 4.5%, deliberately, and that is not vacuity.**
Peter accepted 4.5% when he chose the literal; a band that excluded it would red
the gate to force a decision he has already made. What B catches is the NEXT
move. It is falsified in ``tests/test_check_colour_clamps.py`` by moving the data
under a fixed clamp in both directions — a guard never shown to go red is not
evidence of anything.

⚠️ **B's population is the 358 hoods the colour scale actually runs over** —
``is_set_aside`` hoods are grey and off the scale, so including them dilutes the
saturating share toward zero and the guard reads healthy while the ramp saturates.
Measured both ways 2026-09-16: 4.5% over 358 live hoods, 3.9% over all 406.

Not covered here: the LOT-acre and GRID scales, which already self-anchor to a
live ``quantile(vals, 0.975)`` and render their legend from it
(``moneyScale`` / ``gridScale``) — they cannot drift apart by construction.

Outcomes (exit codes; 2 is argparse's):
  0  ok    — A passes; B is reported, flagged or not (B NEVER changes the code).
  7  drift — A failed: a legend string does not match its clamp.

Usage:
    python scripts/check_colour_clamps.py                 # A + B
    python scripts/check_colour_clamps.py --legend-only   # A (no data needed)
    python scripts/check_colour_clamps.py --report out.md # B's issue body
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HTML = ROOT / "web" / "index.html"
DEFAULT_GEOJSON = ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson"

EXIT_OK = 0
EXIT_DRIFT = 7

NAME_KEY = "neighbourhood_name"

# Share of live (non-set-aside) hoods sitting at or above the clamp. The design
# intent is ~2.5% (a p97.5 clamp). Outside this, the legend's top band no longer
# means what it was set to mean and the literal is worth re-deciding.
BAND = (1.0, 6.0)

# `colorClamp: 50_000,` / `legendMax: "$50k+",` inside a `metric_key: {` block.
METRIC_BLOCK = re.compile(r"^\s{6}([a-z_]+):\s*\{\s*$")
LEGEND_MAX = re.compile(r"^\s*legendMax:\s*\"([^\"]+)\"")
COLOR_CLAMP = re.compile(r"^\s*colorClamp:\s*([0-9_]+)")

SUFFIX = {"": 1, "k": 1_000, "m": 1_000_000, "b": 1_000_000_000}


def parse_legend_money(text: str) -> float | None:
    """``"$50k+"`` -> 50000.0. None when the string is not a money literal."""
    m = re.fullmatch(r"\$([0-9]+(?:\.[0-9]+)?)([kMB]?)\+?", text.strip())
    if not m:
        return None
    return float(m.group(1)) * SUFFIX[m.group(2).lower()]


def parse_metrics(html_path: Path) -> dict[str, dict]:
    """Per money metric: its ``legendMax`` string and its ``colorClamp`` number.

    Read line-wise rather than with one big regex over the file: ``METRICS``
    holds multi-line blurbs full of ``$`` figures and braces, and a greedy
    pattern across them silently pairs a legend with another metric's clamp.
    """
    out: dict[str, dict] = {}
    current: str | None = None
    for line in html_path.read_text(errors="ignore").splitlines():
        block = METRIC_BLOCK.match(line)
        if block:
            current = block.group(1)
            continue
        if current is None:
            continue
        if m := LEGEND_MAX.match(line):
            out.setdefault(current, {})["legend_max"] = m.group(1)
        elif m := COLOR_CLAMP.match(line):
            out.setdefault(current, {})["clamp"] = float(m.group(1).replace("_", ""))
    # A metric block without BOTH is not a money metric (services, dev lenses).
    return {k: v for k, v in out.items() if {"legend_max", "clamp"} <= v.keys()}


def check_legend_agreement(metrics: dict[str, dict]) -> list[str]:
    """Check A. The reader's label must decode to the number the ramp uses."""
    failures = []
    for key, m in sorted(metrics.items()):
        stated = parse_legend_money(m["legend_max"])
        if stated is None:
            failures.append(
                f"{key}: legendMax {m['legend_max']!r} is not a money literal, so "
                f"nothing can check it against colorClamp {m['clamp']:,.0f}"
            )
        elif stated != m["clamp"]:
            failures.append(
                f"{key}: legend says {m['legend_max']!r} (= {stated:,.0f}) but "
                f"colorClamp is {m['clamp']:,.0f} — every colour on the map means "
                f"something other than what the legend says"
            )
    return failures


def live_values(geojson_path: Path, key: str) -> list[float]:
    """The values the colour ramp actually runs over: set-aside hoods are grey
    and off the scale, so they are not part of the population."""
    payload = json.loads(geojson_path.read_text())
    out = []
    for feat in payload.get("features", []):
        p = feat.get("properties", {})
        if p.get("is_set_aside"):
            continue
        v = p.get(key)
        if isinstance(v, (int, float)) and v > 0:
            out.append(float(v))
    return sorted(out)


def _quantile(sorted_vals: list[float], q: float) -> float:
    """Linear-interpolated quantile, matching the front end's ``quantile()``."""
    if not sorted_vals:
        return float("nan")
    pos = (len(sorted_vals) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def measure_drift(metrics: dict[str, dict], geojson_path: Path) -> list[dict]:
    """Check B. Per metric: where the clamp sits in today's distribution."""
    rows = []
    for key, m in sorted(metrics.items()):
        vals = live_values(geojson_path, key)
        if not vals:
            continue
        clamp = m["clamp"]
        saturating = sum(1 for v in vals if v >= clamp)
        share = 100.0 * saturating / len(vals)
        below = sum(1 for v in vals if v < clamp)
        rows.append({
            "metric": key,
            "legend_max": m["legend_max"],
            "clamp": clamp,
            "n": len(vals),
            "p975": _quantile(vals, 0.975),
            "saturating": saturating,
            "share": share,
            "sits_at": 100.0 * below / len(vals),
            "flagged": not (BAND[0] <= share <= BAND[1]),
        })
    return rows


def format_report(rows: list[dict]) -> str:
    lines = [
        "| metric | legend | clamp | p97.5 today | clamp sits at | saturating |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        mark = " ⚠️" if r["flagged"] else ""
        lines.append(
            f"| `{r['metric']}` | {r['legend_max']} | ${r['clamp']:,.0f} | "
            f"${r['p975']:,.0f} | p{r['sits_at']:.1f} | "
            f"{r['saturating']} of {r['n']} ({r['share']:.1f}%){mark} |"
        )
    flagged = [r for r in rows if r["flagged"]]
    if flagged:
        names = ", ".join(f"`{r['metric']}`" for r in flagged)
        lines += [
            "",
            f"**Outside the {BAND[0]}–{BAND[1]}% band: {names}.**",
            "",
            "The clamp is a deliberate literal so the ground-acre scale is stable "
            "across refreshes (`DECISIONS.md` 2026-09-16), so this is not a defect "
            "and nothing is blocked — it is the signal to re-decide the literal. "
            "Raising it to today's p97.5 restores ~2.5% saturating; leaving it "
            "widens the top band. Both legend string and `colorClamp` move together "
            "or check A fails.",
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
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--html", type=Path, default=DEFAULT_HTML)
    p.add_argument("--geojson", type=Path, default=DEFAULT_GEOJSON)
    p.add_argument("--legend-only", action="store_true", help="check A only")
    p.add_argument("--report", type=Path, help="write B's table here (issue body)")
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=args.log_level, format="%(levelname)s %(message)s")

    metrics = parse_metrics(args.html)
    if not metrics:
        logger.error("No money metrics found in %s — has METRICS moved?", args.html)
        return EXIT_DRIFT

    failures = check_legend_agreement(metrics)
    for f in failures:
        logger.error("LEGEND/CLAMP DISAGREE  %s", f)
    if failures:
        logger.error("%d legend/clamp disagreement(s) — see above", len(failures))
        return EXIT_DRIFT
    logger.info("Legend/clamp agreement OK: %d money metrics", len(metrics))

    if args.legend_only:
        return EXIT_OK

    rows = measure_drift(metrics, args.geojson)
    report = format_report(rows)
    print(report, end="")
    if args.report:
        args.report.write_text(report)

    flagged = [r for r in rows if r["flagged"]]
    _write_github_output(
        flagged=len(flagged),
        title=(f"⚠️ Colour clamp drifted — {flagged[0]['metric']}" if flagged else ""),
    )
    if flagged:
        # Never a non-zero exit: drift is a re-decide signal, not a defect. The
        # issue filed from CI is what makes it reach a reader (CLAUDE.md: a
        # warning in a green run reaches nobody).
        logger.warning("%d clamp(s) outside the %.1f–%.1f%% band — reported, not blocked",
                       len(flagged), *BAND)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

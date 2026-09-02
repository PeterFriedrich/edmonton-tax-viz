"""Copy guard: fail loud when a blurb quotes a unit cost the pipeline no longer uses.

Every modelled-cost lens states its rate in prose — "$1,285 per kilometre to
maintain", "$50 per metre per year", "$436.6 million". Those literals live in
``web/index.html``; the rates that actually colour the map live in
``data/city_unit_costs.json``. **Nothing otherwise ties the two together.**

That matters because the whole design intent of keeping rates in a JSON file is
that improving one is a single-value edit: change ``roadway_om_renewal.value``
and the next refresh recomputes every hood. The map is then correct and the
sentence under it is stale — a wrong number presented with full confidence,
which is this project's characteristic failure mode rather than an unlikely one.
The road rates are actively expected to move (the published $600k/km lifecycle
O&M and the $1,285/km operating maintenance figure are ~2.6x apart on what look
like the same quantity, and that is unresolved), so this is not a hypothetical.

⚠️ THIS GUARD CHECKS PROSE, NOT ARITHMETIC. It cannot tell you a rate is *right*
— only that the map and the caption are quoting the SAME rate. Sourcing lives in
``city_unit_costs.json``'s own ``source`` blocks and in ``data/DATA.md`` §13.

Direction policy differs from the schema guards on purpose: **any mismatch is a
FAIL**, with no warn-and-re-pin side. A new rate with no matching copy is not a
"new column" that can wait a week — it is already on the map, and the caption is
already wrong. There is nothing to defer.

Outcomes (exit codes; 2 is argparse's):
  0  ok    — every rate the copy quotes matches the file the pipeline reads.
  5  drift — a quoted rate no longer matches. FAIL.

Usage:
    python scripts/check_cost_copy.py
    python scripts/check_cost_copy.py --html web/index.html --costs data/city_unit_costs.json
"""

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger("check_cost_copy")

REPO = Path(__file__).resolve().parent.parent
DEFAULT_HTML = REPO / "web" / "index.html"
DEFAULT_COSTS = REPO / "data" / "city_unit_costs.json"


def _money(value: float) -> str:
    """$1285.0 -> "$1,285" — the form the blurbs write whole-dollar rates in."""
    return f"${value:,.0f}"


def _millions(value: float) -> str:
    """436605000 -> "$436.6 million" — the form used for budget-scale figures."""
    return f"${value / 1e6:.1f} million"


# Explicit claim table, in the project's explicit-dict style: one row per rate a
# blurb states in words. `path` walks city_unit_costs.json; `fmt` renders the
# value the way the copy writes it; `label` names the sentence for the error.
#
# ⚠️ ADD A ROW WHENEVER A BLURB QUOTES A NEW RATE. A quoted rate with no row here
# is exactly the drift this guard exists to catch, and it cannot detect its own
# omission — the copy simply goes unchecked, silently.
CLAIMS = [
    {
        "label": "Roads cost (lifecycle) — the $/road-metre/yr rate",
        "path": ["roadway_om_renewal", "value"],
        "fmt": lambda v: f"${v:,.0f} per metre per year",
    },
    {
        "label": "Roads cost (operating) — maintenance $/km/yr",
        "path": ["roadway_ops", "components_per_km_per_year", "maintenance"],
        "fmt": _money,
    },
    {
        "label": "Roads cost (operating) — snow and ice $/km/yr",
        "path": ["roadway_ops", "components_per_km_per_year", "snow_and_ice_control"],
        "fmt": _money,
    },
    {
        "label": "Bike cost (operating) — maintenance $/km/yr",
        "path": ["bikeway_ops", "components_per_km_per_year", "maintenance"],
        "fmt": _money,
    },
    {
        "label": "Bike cost (operating) — snow and ice $/km/yr",
        "path": ["bikeway_ops", "components_per_km_per_year", "snow_and_ice_control"],
        "fmt": _money,
    },
    {
        "label": "Transit cost — the ETS bus+LRT gross operating budget",
        "path": ["transit_ets", "operating_budget_gross_annual"],
        "fmt": _millions,
    },
]


def _dig(data: dict, path: list[str], source: Path):
    node = data
    for key in path:
        try:
            node = node[key]
        except (KeyError, TypeError) as e:
            raise KeyError(
                f"{source}: no such unit-cost field {'.'.join(path)} ({e})"
            ) from e
    return node


def check(html_path: Path, costs_path: Path) -> list[str]:
    """Return a list of failure messages; empty means every quoted rate matches."""
    html = html_path.read_text(encoding="utf-8")
    costs = json.loads(costs_path.read_text(encoding="utf-8"))

    failures = []
    for claim in CLAIMS:
        value = _dig(costs, claim["path"], costs_path)
        expected = claim["fmt"](float(value))
        if expected in html:
            logger.info("ok    %-58s %s", claim["label"], expected)
        else:
            failures.append(
                f"{claim['label']}: {costs_path.name} says "
                f"{'.'.join(claim['path'])} = {value}, so the copy should quote "
                f'"{expected}" — no such text in {html_path.name}. '
                "Either the rate changed and the blurb was not updated, or the "
                "blurb rephrased the number into a form this guard cannot see "
                "(in which case fix the wording, not this script)."
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--costs", type=Path, default=DEFAULT_COSTS)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    for path in (args.html, args.costs):
        if not path.exists():
            logger.error("MISSING %s — cannot check cost copy", path)
            return 5

    failures = check(args.html, args.costs)
    if failures:
        logger.error("\nCOST COPY DRIFT — %d quoted rate(s) no longer match:\n", len(failures))
        for msg in failures:
            logger.error("  * %s\n", msg)
        return 5

    logger.info("\nOK — all %d quoted rates match %s", len(CLAIMS), args.costs.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())

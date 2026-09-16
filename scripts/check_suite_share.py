#!/usr/bin/env python3
"""Suite-share guard: fail loud when the Infill blurb's excluded-conversions
percentage no longer matches what the permits data says.

The Infill blurb (Lens B) discloses what its activity term leaves out:

    "... new construction only; secondary-suite and non-res-to-residential
     conversions (~0.9% of units 2021-25) are excluded."

That ``0.9%`` is a **measured** figure, not a rate read from a config file.
S56 derived it on 2026-07-16 (``docs/SPEC_development.md`` D3: 51 in-window
rows / 544 units against a 62,978-unit Lens A numerator) and it was typed into
the copy. Nothing has recomputed it since.

⚠️ **THIS IS A PUBLIC NUMBER WITH NO CHECK.** The 2026-09-15 published-numbers
audit (``docs/FINDINGS_published_numbers.md`` §4, L2) moved it to ``9.0%`` — a
ten-fold overstatement on the live Development panel — and **892 tests passed**.

Two different things can make the sentence wrong, and this guard catches both
because it re-derives rather than compares strings:

  1. **The copy is edited** (L2's falsification) — a typo or a careless edit.
  2. **The share moves under the copy.** ``SPEC_development.md`` D3 says so in
     as many words: *"Revisit if the suite share grows — (08)/(09) are
     policy-encouraged."* The exclusion is only defensible while it is small,
     so the number drifting is a finding about the LENS, not just stale prose.
     Re-measured 2026-09-16: 544 units / 62,970, i.e. the Lens A denominator
     had already moved 8 units since July.

⚠️ **IT NEEDS ``data/raw/building_permits.csv``, WHICH IS GITIGNORED.** So it
runs in the refresh workflow, where the raw pull exists — NOT in ``tests.yml``.
A missing input is a hard FAIL (exit 4), never a quiet pass: a guard that goes
green when its data is absent is the vacuous kind this project keeps catching
(``docs/FINDINGS_vacuous_guards.md``). ``tests/test_check_suite_share.py``
covers the logic on a fixture so CI still exercises it.

Scope, inherited deliberately: the haystack is ``check_cost_copy``'s
reader-visible text, whose comment-blindness is itself the fix for a falsified
vacuous guard (V1, 2026-09-07). Importing it rather than re-implementing means
one hardened extractor, not two that can drift apart.

Outcomes (exit codes; 2 is argparse's):
  0  ok      — the copy states the share the permits data currently shows.
  4  input   — a required input is missing. FAIL, loudly.
  5  drift   — the copy and the data disagree. FAIL.

Usage::

    python scripts/check_suite_share.py
    python scripts/check_suite_share.py --permits data/raw/building_permits.csv
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from check_cost_copy import _blurb_texts, _visible_html_text  # noqa: E402
from load_permits import NEW_WORK_TYPES  # noqa: E402

logger = logging.getLogger("check_suite_share")

REPO = Path(__file__).resolve().parent.parent
DEFAULT_HTML = REPO / "web" / "index.html"
DEFAULT_PERMITS = REPO / "data" / "raw" / "building_permits.csv"

# The work types the Infill activity term excludes and the blurb discloses.
# ⚠️ These are the (07)/(08)/(09) codes as spelled in the live vocabulary — the
# same strings `load_permits.KNOWN_WORK_TYPES` carries. A vocabulary change that
# renames one would drop it silently from the numerator and shrink the share, so
# the guard asserts each is still a known value before trusting the arithmetic.
SUITE_WORK_TYPES = frozenset({
    "(07) Add Suites to Single Dwelling",
    "(08) Add Suites to Multi-Dwelling",
    "(09) Convert Non-Res to Residential",
})

# The sentence the guard reads, e.g. "~0.9% of units". The percentage is the
# only part that moves; the surrounding words are pinned so a rewrite that drops
# the disclosure entirely is a FAIL rather than a silent pass.
_CLAIM_RE = re.compile(r"~\s*(\d+(?:\.\d+)?)\s*%\s*of\s*units")


def suite_share(permits: pd.DataFrame, years) -> tuple[float, int, int, int]:
    """(share_pct, suite_units, lens_a_units, suite_rows) over ``years``.

    The denominator is Lens A's numerator — units added by genuinely-new
    construction — because that is what the blurb's "% of units" compares to.
    Using all permits instead would understate the share several-fold.
    """
    work = permits["work_type"].astype("string").str.strip()
    in_window = permits["year"].isin(list(years))

    unknown = SUITE_WORK_TYPES - set(work.dropna().unique())
    if unknown:
        raise SystemExit(
            f"[suite-share] work_type vocabulary no longer contains "
            f"{sorted(unknown)} — the disclosed share would silently shrink. "
            f"Reconcile against load_permits.KNOWN_WORK_TYPES before re-pinning."
        )

    suite = permits[in_window & work.isin(SUITE_WORK_TYPES)]
    lens_a = permits[in_window & work.isin(NEW_WORK_TYPES)]["units_added"].sum()
    if lens_a <= 0:
        raise SystemExit(
            "[suite-share] Lens A numerator is zero over the window — the year "
            "pin is wrong or the permits pull is broken. Refusing to divide."
        )
    suite_units = suite["units_added"].sum()
    return 100.0 * suite_units / lens_a, int(suite_units), int(lens_a), len(suite)


def stated_share(html: str) -> float | None:
    """The percentage the reader-visible copy states, or None if absent."""
    haystack = " ".join(_blurb_texts(html)) + " " + _visible_html_text(html)
    m = _CLAIM_RE.search(haystack)
    return float(m.group(1)) if m else None


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--html", type=Path, default=DEFAULT_HTML)
    ap.add_argument("--permits", type=Path, default=DEFAULT_PERMITS)
    ap.add_argument("--years", type=int, nargs="+", default=None,
                    help="override the permit window (default: main.PERMIT_YEARS)")
    args = ap.parse_args(argv)

    for path in (args.html, args.permits):
        if not path.exists():
            logger.error(
                "[suite-share] FAIL missing input: %s\n"
                "  This guard re-derives from the raw permits pull, so it runs in "
                "the refresh workflow, not tests.yml. It fails rather than passing "
                "quietly, because a guard that goes green without its data is worse "
                "than no guard.", path)
            return 4

    years = args.years
    if years is None:
        sys.path.insert(0, str(REPO))
        from main import PERMIT_YEARS
        years = PERMIT_YEARS

    permits = pd.read_csv(args.permits, low_memory=False)
    share, suite_units, lens_a, rows = suite_share(permits, years)
    stated = stated_share(args.html.read_text())

    window = f"{min(years)}-{max(years)}"
    if stated is None:
        logger.error(
            "[suite-share] FAIL the Infill blurb no longer discloses the excluded "
            "share at all.\n  Expected a phrase like '~%.1f%% of units'. The "
            "exclusion is only defensible while it is disclosed (SPEC_development.md "
            "D3); removing the sentence is a decision, not an edit.", share)
        return 5

    if round(stated, 1) != round(share, 1):
        logger.error(
            "[suite-share] FAIL copy says ~%.1f%%, permits say %.2f%% (%s)\n"
            "  %d suite units (%d rows, work types (07)/(08)/(09)) against a "
            "%d-unit Lens A numerator.\n"
            "  If the DATA moved: SPEC_development.md D3 says revisit the "
            "exclusion, not just the sentence — the D3 counterfactual "
            "('zero hoods would flip verdict') was measured at 0.9%% and does "
            "not carry forward on its own.\n"
            "  If the COPY moved: restore it to ~%.1f%%.",
            stated, share, window, suite_units, rows, lens_a, share)
        return 5

    logger.info(
        "[suite-share] ok: copy ~%.1f%% matches permits %.2f%% (%s; %d units / %d)",
        stated, share, window, suite_units, lens_a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Re-run the standalone notebooks against live sources and report what moved.

WHY THIS EXISTS. ``notebooks/standalone/`` holds two kinds of document, and
both carry invariants that are meant to keep PASSING:

* **evidence reports** — each one documents a defect in somebody else's
  published data, and its invariants are written to fail *when the publisher
  fixes it* (``docs/EVIDENCE_NOTEBOOKS.md``);
* **justification notebooks** — each one defends a number this project ships,
  and its invariants fail when a source moves under that number.

Nothing re-ran either kind on a schedule. Measured 2026-09-21: four of the five
published evidence pages had not touched a live source since **2026-08-29**,
while their files carried an mtime of the previous day — a cosmetic re-render
of stored outputs had made three-week-old evidence look current. If the City
had quietly backfilled the 2024 assessment slice in that window, nothing here
would have noticed; the detector was well built and had no trigger. That is the
same shape as the ``_classify`` warning that logged to an unread file for ~70
days, one level up.

⚠️ **A FAILURE HERE IS NOT NECESSARILY BAD NEWS.** For an evidence report the
most likely cause is the publisher fixing the defect, which is the outcome the
report was written to produce — but it also means the published page now makes
a claim that is no longer true and must be pulled or re-dated. Triage in
``docs/RUNBOOK.md`` §0e.

⚠️ **"COULD NOT CHECK" IS LOUDER THAN "SOMETHING MOVED", and is reported
separately.** A notebook that cannot fetch its sources has not verified
anything, and a dead source URL is itself a finding about a page that cites it.
This repo has the failure in its history the other way round — a guard that
could not read its baseline was reported like a guard that read it and found
nothing.

REPORT-ONLY. Runs notebooks that read the network and write nothing; it touches
no data file and no branch.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STANDALONE = REPO / "notebooks" / "standalone"

PASS, MOVED, UNCHECKABLE = "pass", "moved", "uncheckable"

# The two species, kept apart because a failure MEANS something different in
# each. Names are module stems in notebooks/standalone/.
EVIDENCE = (
    "roll_year_metadata",
    "historical_2024_gap",
    "exemption_uncertainty",
    "school_coverage_gap",
    "permit_neighbourhood_list",
)
JUSTIFICATION = (
    "roads_lifecycle_rate",
    "roads_operating_rate",
)

# A notebook that fails its own invariants raises AssertionError from its last
# cell and exits 1. Anything else non-zero (ImportError, a 404 escaping the
# fetch helper, a timeout) means the run never got far enough to judge.
ASSERTION_MARKER = "AssertionError"

# Generous: these fetch multi-MB PDFs and page through Socrata.
PER_NOTEBOOK_TIMEOUT = 1500


def run_one(stem, python=sys.executable, timeout=PER_NOTEBOOK_TIMEOUT):
    """Execute one notebook as a plain script. Returns (status, detail)."""
    path = STANDALONE / f"{stem}.py"
    if not path.exists():
        return UNCHECKABLE, f"`{path.relative_to(REPO)}` does not exist"

    try:
        proc = subprocess.run(
            [python, str(path)],
            capture_output=True, text=True, timeout=timeout, cwd=str(STANDALONE),
        )
    except subprocess.TimeoutExpired:
        return UNCHECKABLE, f"timed out after {timeout}s — sources unreachable or slow"

    out = f"{proc.stdout}\n{proc.stderr}"
    n_pass = out.count("[PASS]")
    n_fail = out.count("[FAIL]")

    if proc.returncode == 0:
        # ⚠️ Exit 0 alone does not mean the invariants ran — a notebook that
        # printed nothing would also exit 0. Require evidence that checks fired.
        if n_pass == 0:
            return UNCHECKABLE, "exited 0 but recorded no invariants — did it run?"
        return PASS, f"{n_pass} invariant(s) held"

    if ASSERTION_MARKER in out:
        failed = [ln.strip() for ln in out.splitlines() if "[FAIL]" in ln]
        detail = "; ".join(failed)[:600] or f"{n_fail} invariant(s) failed"
        return MOVED, f"**{n_fail} of {n_pass + n_fail} flipped** — {detail}"

    tail = " ".join(proc.stderr.strip().splitlines()[-3:])[:400]
    return UNCHECKABLE, f"exit {proc.returncode}, no invariant verdict — {tail}"


def run_all(only=None, python=sys.executable):
    results = []
    for species, stems in (("evidence", EVIDENCE), ("justification", JUSTIFICATION)):
        for stem in stems:
            if only and stem not in only:
                continue
            status, detail = run_one(stem, python=python)
            results.append((species, stem, status, detail))
    return results


def render(results, today=None):
    today = today or dt.date.today()
    moved = [r for r in results if r[2] == MOVED]
    unchecked = [r for r in results if r[2] == UNCHECKABLE]

    if unchecked and moved:
        head = (f"**{len(moved)} notebook(s) moved and {len(unchecked)} could not be "
                f"checked.** Read the uncheckable ones first — they verified nothing.")
    elif unchecked:
        head = (f"⚠️ **{len(unchecked)} notebook(s) COULD NOT BE CHECKED.** This is not "
                f"a clean bill of health: nothing was verified for them.")
    elif moved:
        head = (f"⚠️ **{len(moved)} notebook(s) no longer hold.** For an evidence "
                f"report the likely cause is the publisher FIXING the defect — good "
                f"news that still makes the published page wrong until it is pulled "
                f"or re-dated.")
    else:
        head = ("**Everything still holds.** Every documented defect is still present "
                "upstream and every shipped rate's sources still read as transcribed.")

    icon = {PASS: "✅", MOVED: "⚠️", UNCHECKABLE: "❓"}
    lines = [
        f"Evidence recheck — {today.isoformat()}",
        "",
        head,
        "",
        "| | Notebook | Kind | Detail |",
        "|---|---|---|---|",
    ]
    order = {UNCHECKABLE: 0, MOVED: 1, PASS: 2}
    for species, stem, status, detail in sorted(results, key=lambda r: order[r[2]]):
        lines.append(f"| {icon[status]} | `{stem}` | {species} | {detail} |")

    lines += [
        "",
        "**What a ⚠️ means, by kind.** *evidence* — the defect this report "
        "documents may have been fixed upstream; confirm, then pull or re-date "
        "the published page at `web/notebooks/` and update "
        "`docs/DATA_ISSUES.md`. *justification* — a source moved under a rate "
        "this project ships on a public map; re-read it before the next refresh.",
        "",
        "**A ❓ is the louder result.** The notebook verified nothing. A source "
        "that will not fetch is itself a finding about a page that cites it.",
        "",
        "---",
        "*Generated monthly by `.github/workflows/evidence-recheck.yml` "
        "(`scripts/recheck_evidence_notebooks.py`). Report-only — it changes "
        "nothing. Triage: `docs/RUNBOOK.md` §0e. Close this issue once you've "
        "acted, or immediately if it's all green.*",
    ]
    return "\n".join(lines), len(moved), len(unchecked)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--only", nargs="*", help="run only these notebook stems")
    p.add_argument("--python", default=sys.executable,
                   help="interpreter to run the notebooks with")
    args = p.parse_args(argv)

    # Notebooks run with cwd set to their own directory, so a relative
    # interpreter path (`.venv/bin/python`, the way this repo is usually
    # driven) would resolve against the wrong directory and raise
    # FileNotFoundError before any notebook ran.
    python = args.python
    if os.sep in python and not os.path.isabs(python):
        python = os.path.abspath(python)

    results = run_all(only=args.only, python=python)

    if args.json:
        print(json.dumps([{"species": s, "notebook": n, "status": st, "detail": d}
                          for s, n, st, d in results], indent=2))
        return 0

    body, n_moved, n_unchecked = render(results)
    print(body)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        today = dt.date.today().isoformat()
        if n_unchecked:
            title = f"⚠️ Evidence recheck could not run — {n_unchecked} notebook(s)"
        elif n_moved:
            title = f"⚠️ Evidence invariant flipped — {n_moved} notebook(s)"
        else:
            title = f"✅ Evidence recheck — {today}"
        with open(out, "a") as f:
            f.write(f"moved_count={n_moved}\n")
            f.write(f"unchecked_count={n_unchecked}\n")
            f.write(f"title={title}\n")

    # Exit 0 regardless — the ISSUE is the output, not the exit code. A non-zero
    # exit here would mean this script crashed, which is a different problem.
    return 0


if __name__ == "__main__":
    sys.exit(main())

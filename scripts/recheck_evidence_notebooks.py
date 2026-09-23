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
import re
import subprocess
import sys
import tempfile
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

# All seven finished cold in under 2 min combined (2026-09-23). ⚠️ Seven of
# these must fit inside the workflow's `timeout-minutes: 60`, or a third hung
# notebook gets the job killed with no issue filed — which is what the old
# 1500 s cap allowed.
PER_NOTEBOOK_TIMEOUT = 420

# The notebooks cache their downloads beside themselves and re-read them when
# present, with no freshness check. Pointing these at a fresh directory is what
# makes a hand run on a machine with warm caches a LIVE check, as CI's is.
CACHE_ENV_VARS = ("EXEMPTION_NB_DATA", "HISTORICAL_GAP_DATA", "ROLL_YEAR_DATA")

# Exceptions that mean the source could not be reached. Anything else escaping
# a notebook means the data arrived in a shape the code did not expect — which
# for an evidence report is often the publisher's FIX (an IndexError on a year
# that now exists, a KeyError on a column that was added), not a dead source.
NETWORK_EXC = re.compile(
    r"URLError|HTTPError|ConnectionError|ConnectTimeout|ReadTimeout|Timeout|"
    r"SSLError|RemoteDisconnected|IncompleteRead|socket\.gaierror|gaierror|"
    r"ProtocolError|MaxRetryError|ChunkedEncodingError")
EXC_LINE = re.compile(r"^([A-Za-z_][\w.]*(?:Error|Exception|Timeout|gaierror))\b")


def _claims(out, tag):
    """The distinct claim lines carrying `tag`, in order.

    ⚠️ Deduplicated because two notebooks print every verdict twice — once in
    `check()` and again in their closing summary — which reported 101
    invariants as 118 and one flip as "2 of 12". Two different invariants with
    byte-identical text would collapse into one; a notebook should not have
    those anyway.
    """
    return list(dict.fromkeys(ln.strip() for ln in out.splitlines() if tag in ln))


def _exception(stderr):
    for ln in reversed(stderr.strip().splitlines()):
        m = EXC_LINE.match(ln.strip())
        if m:
            return m.group(1)
    return None


def run_one(stem, python=sys.executable, timeout=PER_NOTEBOOK_TIMEOUT):
    """Execute one notebook as a plain script. Returns (status, detail)."""
    path = STANDALONE / f"{stem}.py"
    if not path.exists():
        return UNCHECKABLE, f"`{path.relative_to(REPO)}` does not exist"

    with tempfile.TemporaryDirectory(prefix=f"recheck-{stem}-") as cache:
        env = {**os.environ, **{v: os.path.join(cache, v.lower()) for v in CACHE_ENV_VARS}}
        try:
            proc = subprocess.run(
                [python, str(path)],
                capture_output=True, text=True, timeout=timeout,
                cwd=str(STANDALONE), env=env,
            )
        except subprocess.TimeoutExpired:
            return UNCHECKABLE, (f"**network** — timed out after {timeout}s, "
                                 "sources unreachable or slow")

    out = f"{proc.stdout}\n{proc.stderr}"
    passed, failed = _claims(out, "[PASS]"), _claims(out, "[FAIL]")
    n_pass, n_fail = len(passed), len(failed)

    if proc.returncode == 0:
        # ⚠️ Exit 0 alone does not mean the invariants ran — a notebook that
        # printed nothing would also exit 0. Require evidence that checks fired.
        if n_pass == 0:
            return UNCHECKABLE, "exited 0 but recorded no invariants — did it run?"
        return PASS, f"{n_pass} invariant(s) held"

    if ASSERTION_MARKER in out:
        detail = "; ".join(failed)[:600] or f"{n_fail} invariant(s) failed"
        return MOVED, f"**{n_fail} of {n_pass + n_fail} flipped** — {detail}"

    tail = " ".join(proc.stderr.strip().splitlines()[-3:])[:400]
    exc = _exception(proc.stderr)
    if exc and NETWORK_EXC.search(exc):
        kind = f"**network** (`{exc}`) — a source did not answer"
    elif exc:
        kind = (f"**data shape** (`{exc}`) — a source answered with something the "
                "notebook did not expect; for an evidence report that can be the FIX")
    else:
        kind = f"exit {proc.returncode}, no exception named"
    # Verdicts that fired before the crash are evidence too — keep them.
    before = f" Flipped before the crash: {'; '.join(failed)[:300]}." if failed else ""
    return UNCHECKABLE, f"{kind}, no invariant verdict.{before} — {tail}"


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
        "**A ❓ is the louder result.** The notebook verified nothing. A "
        "**network** ❓ is a source that will not fetch — itself a finding about "
        "a page that cites it. A **data shape** ❓ means a source answered in a "
        "form the notebook did not expect; on an *evidence* report that can be "
        "the publisher's fix, so read the notebook before hunting for a dead URL.",
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

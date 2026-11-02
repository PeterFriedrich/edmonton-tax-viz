#!/usr/bin/env python3
"""Execute the verified-pipeline notebooks and render them to HTML.

Each notebook under ``notebooks/verified/`` is a jupytext percent-format ``.py``
file that imports the real ``src/`` modules, displays computed figures, and
asserts invariants. Executing them is how the documentation stays current: the
prose is authored, every number is recomputed from the data in front of it.

Exit codes:
    0   every notebook executed and every invariant held
    1   at least one notebook failed (its log names which invariant)

A failing notebook produces no HTML — nbconvert fails closed rather than
publishing figures from a run that did not finish. The captured log is written
next to the output so CI can surface the traceback without re-running.

A full run (no ``--only``) that succeeds also writes ``REPORT_FIGURES.md``: the
values each notebook declared for a ``docs/REPORT_CLAIMS.md`` row marked live,
as the page states them, for checking the written report against.

    python tools/run_verified_notebooks.py --out-dir _verified
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inject_notebook_mobile_css import inject  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "notebooks" / "verified"


def build(source: Path, out_dir: Path, timeout: int, figures: bool = True) -> tuple[bool, float, Path]:
    """Convert one percent-format .py to .ipynb, execute it, render HTML."""
    ipynb = out_dir / (source.stem + ".ipynb")
    log_path = out_dir / (source.stem + ".log")

    # jupytext only rewrites the container; nothing is executed at this stage.
    convert = subprocess.run(
        [sys.executable, "-m", "jupytext", "--to", "ipynb", str(source), "-o", str(ipynb)],
        capture_output=True,
        text=True,
    )
    if convert.returncode != 0:
        log_path.write_text(convert.stdout + convert.stderr)
        return False, 0.0, log_path

    # The kernel's cwd is the notebook's directory, which is the build dir and
    # not the repo — so the root is passed explicitly rather than searched for.
    env = {**os.environ, "EDMONTON_REPO_ROOT": str(ROOT)}
    if figures:
        env["REPORT_FIGURES_DIR"] = str(out_dir.resolve())

    started = time.monotonic()
    run = subprocess.run(
        [
            sys.executable, "-m", "nbconvert",
            "--to", "html",
            "--execute", str(ipynb),
            "--output-dir", str(out_dir),
            f"--ExecutePreprocessor.timeout={timeout}",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    elapsed = time.monotonic() - started

    log_path.write_text(run.stdout + run.stderr)
    ipynb.unlink(missing_ok=True)  # intermediate; the .py and the .html are the artifacts

    # nbconvert's lab template clips code lines and wide tables on a phone
    # instead of scrolling them. This render path is weekly and automated, so
    # the fix has to live here — patching the committed HTML lasts until the
    # next refresh. Measured 2026-09-21 on the published page: -428px of code
    # and -1458px of output at 390px wide.
    if run.returncode == 0:
        html = out_dir / (source.stem + ".html")
        if html.exists():
            inject(html)

    return run.returncode == 0, elapsed, log_path


def render_report_figures(out_dir: Path, status: dict) -> str:
    """One table of every notebook's declared report figures; consumes the JSON."""
    rows = []
    for f in sorted(out_dir.glob("*.figures.json")):
        page = f.name.removesuffix(".figures.json")
        for rid, values in json.loads(f.read_text()).items():
            rows += [(rid, label, value, page) for label, value in values]
        f.unlink()
    order = lambda r: (re.match(r"[A-Z]+", r[0]).group(), int(re.search(r"\d+", r[0]).group()))
    lines = [
        "# Report figures (weekly-live values)",
        "",
        # No run date or commit: the file changes only when a figure or the served data
        # does, so a change to it (and the handoff's "press Sync") means something.
        f"From the served data generated {status.get('generated')} "
        f"(roll year {status.get('data_year')}, rate year {status.get('rate_year')}), "
        f"by `tools/run_verified_notebooks.py`.",
        "",
        "Each value is quoted as its verified notebook states it this week. The claims "
        "are in `docs/REPORT_CLAIMS.md`; a row marked live has its number here, not there.",
        "",
        "| id | figure | value | page |",
        "|---|---|---|---|",
    ]
    lines += [f"| {r} | {label} | {value} | `{page}` |" for r, label, value, page in sorted(rows, key=order)]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out-dir", type=Path, default=ROOT / "_verified")
    p.add_argument("--timeout", type=int, default=1800, help="per-cell execution timeout (seconds)")
    p.add_argument("--only", help="run just the notebook whose stem matches this")
    args = p.parse_args(argv)

    sources = sorted(SOURCE_DIR.glob("*.py"))
    if args.only:
        sources = [s for s in sources if args.only in s.stem]
    if not sources:
        print(f"ERROR: no notebooks found in {SOURCE_DIR}", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for stale in args.out_dir.glob("*.figures.json"):
        stale.unlink()
    failures = []

    for source in sources:
        print(f"--- {source.name}", flush=True)
        ok, elapsed, log_path = build(source, args.out_dir, args.timeout, figures=not args.only)
        if ok:
            print(f"    OK   {elapsed:5.1f}s  -> {args.out_dir / (source.stem + '.html')}")
        else:
            failures.append(source.name)
            print(f"    FAIL {elapsed:5.1f}s  see {log_path}")
            # Surface the reason inline; CI logs are the only thing many readers see.
            tail = log_path.read_text().strip().splitlines()[-15:]
            for line in tail:
                print(f"      | {line}")

    print(f"\n{len(sources) - len(failures)}/{len(sources)} notebooks executed cleanly")
    if failures:
        print(f"FAILED: {', '.join(failures)}", file=sys.stderr)
        # The committed REPORT_FIGURES.md stays last week's; don't leave half a set.
        for f in args.out_dir.glob("*.figures.json"):
            f.unlink()
        return 1
    # A partial run would publish a table missing whole pages' figures.
    if not args.only:
        status = json.loads((ROOT / "web" / "data" / "status.json").read_text())
        out = args.out_dir / "REPORT_FIGURES.md"
        out.write_text(render_report_figures(args.out_dir, status))
        print(f"report figures -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

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

    python tools/run_verified_notebooks.py --out-dir _verified
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "notebooks" / "verified"


def build(source: Path, out_dir: Path, timeout: int) -> tuple[bool, float, Path]:
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
    return run.returncode == 0, elapsed, log_path


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
    failures = []

    for source in sources:
        print(f"--- {source.name}", flush=True)
        ok, elapsed, log_path = build(source, args.out_dir, args.timeout)
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
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

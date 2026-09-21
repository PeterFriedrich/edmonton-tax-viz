"""The retrieval report must not let two instrument regimes be compared.

The PostToolUse hook logged only the `Read`/`Grep`/`Glob` TOOLS until
2026-09-21, so every doc consulted through `bash grep`, `sed` or `cat` was
invisible — measured that day, one ordinary session consulted 8 tracked docs and
logged 0 of them. Widening the hook to `Bash` fixes the undercount going
forward and thereby creates a worse hazard: the same table now holds counts
produced by two different instruments, and a doc whose count rises across the
change looks more-read when nothing about the reading changed.

The `~2026-09-30` readout is the thing this protects, and its decision rule is
"a doc never opened before an action is a prune candidate" — so a count read
without the regime warning can delete a doc that was being used all along.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "retrieval_report.py"
SPANS = "WINDOW SPANS"


def _log(tmp_path, stamps_and_tools):
    """A log whose rows differ ONLY in date and tool — nothing else varies."""
    path = tmp_path / "log.jsonl"
    with path.open("w") as fh:
        for stamp, tool in stamps_and_tools:
            fh.write(json.dumps({
                "t": stamp, "tool": tool, "path": "docs/DECISIONS.md",
                "q": None, "cwd": str(ROOT), "sid": "s1",
            }) + "\n")
    return path


def _run(log_path):
    out = subprocess.run(
        [sys.executable, str(TOOL), "--log", str(log_path)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert out.returncode == 0, out.stderr
    return out.stdout


def test_window_spanning_the_widening_is_flagged(tmp_path):
    log = _log(tmp_path, [
        ("2026-09-18T10:00:00Z", "Read"),
        ("2026-09-22T10:00:00Z", "Bash"),
    ])
    out = _run(log)
    assert SPANS in out, "a window straddling the hook change printed no warning"
    assert "1 of 2 calls predate it" in out


def test_a_window_entirely_after_the_widening_is_not_flagged(tmp_path):
    """Differs from the case above ONLY in the first row's date."""
    log = _log(tmp_path, [
        ("2026-09-21T10:00:00Z", "Read"),
        ("2026-09-22T10:00:00Z", "Bash"),
    ])
    assert SPANS not in _run(log), "warned about a window with nothing to compare"


def test_a_window_entirely_before_the_widening_is_not_flagged(tmp_path):
    log = _log(tmp_path, [
        ("2026-09-16T10:00:00Z", "Read"),
        ("2026-09-18T10:00:00Z", "Read"),
    ])
    assert SPANS not in _run(log)


def test_the_never_opened_caveat_no_longer_claims_bash_is_invisible(tmp_path):
    """The old wording is now false and would suppress a real prune candidate.

    Bash reads ARE captured — but only when the command names the file, so the
    caveat has to state the narrower residual blind spot instead of the old
    blanket one.
    """
    out = _run(_log(tmp_path, [("2026-09-22T10:00:00Z", "Bash")]))
    assert "NAMES the file" in out
    assert "grep -rn x docs/" in out

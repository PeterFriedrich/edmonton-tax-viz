"""What has landed since the newest handoff — the evidence a session-end nag lacks.

`CLAUDE.md` requires a written record in `session-summary/` before context is
lost, and six places say so: three `CLAUDE.md` lines, the `PreCompact` hook, the
`SessionEnd` hook, and the audit skill's Step 5. **The rule was never
under-supplied.** What was missing is that the two hooks fired the same sentence
whether eight PRs had landed or none — *"if you did substantive work, reconcile
TODO.md and run /handoff"* — so they could not distinguish a session that owed a
handoff from one that did not, and a warning that always fires is one you learn
to skim. That is this project's named failure mode (`_classify`, ~70 days into a
log nobody read), applied to its own session ritual.

So this replaces the instruction with the measurement: **commits touching
substantive paths that landed after the newest handoff's own last commit**, plus
uncommitted work in those paths. When nothing is owed it prints NOTHING, which is
what makes the message worth reading when it appears.

⚠️ **Silence here is not "the handoff is complete", only "no code has moved since
it was last committed."** A handoff can be present and wrong, and no diff can see
that. It answers *is there unrecorded work*, not *is the record good*.

⚠️ **Fails silent, always.** It runs at session end and on compaction, where
anything it prints competes with the user's own output and a traceback would be
noise at the worst moment. No git, no repo, a detached HEAD, a shallow clone with
no history for the handoff file — every one of them exits 0 saying nothing. It
can never be the reason a session ends badly.

Usage:
    python scripts/handoff_gap.py                 # plain text, or nothing
    python scripts/handoff_gap.py --json          # SessionEnd hook shape
    python scripts/handoff_gap.py --json-compact   # PreCompact hook shape
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parent.parent
SUMMARIES = ROOT / "session-summary"

# Work that belongs in a handoff. `docs/` is deliberately OUT: a docs-only change
# is usually the handoff itself, or a DECISIONS row that is already its own
# record, and counting it would make the message fire after every commit — which
# is the always-on nag this replaces.
SUBSTANTIVE = ("src", "tests", "tools", "scripts", "web", ".github", "main.py")


def _git(*args):
    """stdout, or None on any failure at all. See the module docstring."""
    try:
        # NOT capture_output=/text=: both are Python 3.7+, and the fallback
        # interpreter here is 3.6.8. They raise TypeError, which the handler
        # below swallows — so the hook would print NOTHING, for ever, while
        # looking healthy. Caught only by running it under python3 (2026-09-16).
        proc = subprocess.run(
            ["git"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, cwd=str(ROOT), timeout=15,
        )
    except Exception:  # noqa: BLE001 — a hook must never raise
        return None
    return proc.stdout if proc.returncode == 0 else None


def newest_handoff():
    try:
        files = sorted(SUMMARIES.glob("*.md"))
    except OSError:
        return None
    return files[-1] if files else None


def gap():
    # type: () -> Optional[Dict[str, object]]
    """``{handoff, commits, dirty}`` when something is unrecorded, else None.

    ⚠️ Comment-style type hints and `typing` imports, not `str | None`: this
    runs from a hook whose fallback interpreter is the system `python3`, which
    is **3.6.8** on this box. `retrieval_report.py` has the modern form and is
    `.venv`-only because of it — a report can demand an interpreter, a hook
    cannot."""
    handoff = newest_handoff()
    if handoff is None:
        return None

    rel = handoff.relative_to(ROOT).as_posix()
    last = _git("log", "-1", "--format=%H", "--", rel)
    if not last or not last.strip():
        return None  # never committed, or no history for it (shallow clone)

    # --no-merges: a merge commit restates its branch's changes, and counting
    # both reports every PR twice.
    out = _git("log", "--no-merges", "--format=%h %s",
               f"{last.strip()}..HEAD", "--", *SUBSTANTIVE)
    if out is None:
        return None
    commits = [ln for ln in out.strip().split("\n") if ln]

    status = _git("status", "--porcelain", "--", *SUBSTANTIVE)
    dirty = len([ln for ln in (status or "").strip().split("\n") if ln])

    if not commits and not dirty:
        return None
    return {"handoff": handoff.name, "commits": commits, "dirty": dirty}


def message(g):
    bits = []
    if g["commits"]:
        bits.append(f"{len(g['commits'])} commit(s) touching "
                    f"{'/'.join(SUBSTANTIVE[:4])}/…")
    if g["dirty"]:
        bits.append(f"{g['dirty']} uncommitted file(s) in those paths")
    what = " and ".join(bits)
    lines = [
        f"⚠️ {what} landed after `session-summary/{g['handoff']}` was last "
        f"committed — that handoff records none of it.",
    ]
    for c in g["commits"][:5]:
        lines.append(f"    {c}")
    if len(g["commits"]) > 5:
        lines.append(f"    …+{len(g['commits']) - 5} more")
    lines.append("Append to that file (same session) or write a new one, then "
                 "reconcile TODO.md. CLAUDE.md requires the record before the "
                 "context is gone.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="SessionEnd hook shape")
    ap.add_argument("--json-compact", action="store_true", help="PreCompact hook shape")
    args = ap.parse_args(argv)

    try:
        g = gap()
    except Exception:  # noqa: BLE001 — belt and braces; a hook must never raise
        return 0
    if g is None:
        return 0  # nothing owed: say nothing, so the message means something

    text = message(g)
    if args.json_compact:
        print(json.dumps({
            "suppressOutput": True,
            "systemMessage": text,
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "additionalContext": text,
            },
        }))
    elif args.json:
        print(json.dumps({"systemMessage": text}))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

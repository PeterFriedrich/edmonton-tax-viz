"""Guards on the LOADED PATH — what every session is told to read before it works.

`CLAUDE.md` names the files a session must open: itself, `TODO.md`, the latest
handoff, the auto-memory index. Measured 2026-09-16 that is **292 KB**, and the
handoff pile is 4% of it — the number the decision to keep one file per session
rests on (`DECISIONS.md` 2026-09-16, rec #4 of the doc-apparatus review).

⚠️ **That 4% is true only while the archive discipline holds, and until this file
nothing enforced it.** `CLAUDE.md` says *"keep the 3 most recent at top level,
archive older"* — a rule with a reader and no check, which is this project's
standing failure mode (`_classify` warned into a log for ~70 days). A lapse is
silent and compounding: nobody notices the 4th file, and the decision stops being
the decision in effect.

Lives in `tests/` rather than as a `scripts/check_*.py` because it needs no CLI,
no report and no exit code of its own — it is a repo invariant, and pytest
already runs on the merge gate. Same shape as `test_ci_workflows.py`.
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUMMARIES = REPO / "session-summary"

# CLAUDE.md, "Token Efficiency": read only the latest, keep the 3 most recent.
MAX_LIVE = 3


def _live() -> list[str]:
    return sorted(p.name for p in SUMMARIES.glob("*.md"))


def _archived() -> list[str]:
    return sorted(p.name for p in (SUMMARIES / "archive").glob("*.md"))


def test_at_most_three_handoffs_at_top_level():
    live = _live()
    assert len(live) <= MAX_LIVE, (
        f"{len(live)} handoffs at session-summary/ top level, max {MAX_LIVE} "
        f"(CLAUDE.md). Move the oldest into session-summary/archive/ in this same "
        f"PR — `git mv session-summary/{live[0]} session-summary/archive/`. "
        f"Archiving is not deletion: the files stay, out of the loaded path."
    )


def test_the_live_handoffs_are_the_most_recent_ones():
    """Not just three — the three NEWEST. Filenames are date-prefixed, so every
    archived name must sort before every live one. Catches archiving the wrong
    end, which passes the count test while leaving a stale file in the path a
    session is told to read."""
    live, archived = _live(), _archived()
    if not live or not archived:
        return
    assert archived[-1] < live[0], (
        f"session-summary/archive/{archived[-1]} is newer than the live "
        f"{live[0]} — the wrong end was archived. The top-level files must be "
        f"the {MAX_LIVE} most recent."
    )


def test_archive_is_where_the_history_actually_is():
    """A floor under the two tests above: if the archive were empty, both would
    pass over a repo that had DELETED its history instead of moving it."""
    assert len(_archived()) > len(_live())

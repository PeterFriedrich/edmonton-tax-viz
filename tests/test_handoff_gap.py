"""Tests for scripts/handoff_gap.py (the session-end handoff-gap measurement).

⚠️ Two tests carry the design, and both are about NOT firing:
``test_docs_only_commits_do_not_fire`` and ``test_nothing_owed_prints_nothing``.
The thing this replaces was a hook that printed the same sentence every session
whether work had landed or not; if this fires unconditionally too, it is the same
nag with extra machinery. Silence is the feature.

The rest drive the fail-silent contract — a hook that raises at session end is
noise at the worst possible moment.
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import handoff_gap as hg  # noqa: E402


def _run(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True,
                   capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A real git repo — the script shells out, so a fake would test nothing."""
    _run(tmp_path, "init", "-q", "-b", "main")
    _run(tmp_path, "config", "user.email", "t@example.com")
    _run(tmp_path, "config", "user.name", "T")
    (tmp_path / "session-summary").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "session-summary" / "2026-09-16-s1.md").write_text("# handoff\n")
    _run(tmp_path, "add", "-A")
    _run(tmp_path, "commit", "-qm", "handoff")
    monkeypatch.setattr(hg, "ROOT", tmp_path)
    monkeypatch.setattr(hg, "SUMMARIES", tmp_path / "session-summary")
    return tmp_path


def _commit(repo, path, text="x", msg="work"):
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    _run(repo, "add", "-A")
    _run(repo, "commit", "-qm", msg)


# --- the two that carry the design -------------------------------------------

def test_nothing_owed_prints_nothing(repo, capsys):
    """The handoff is the newest thing: silence, exit 0."""
    assert hg.gap() is None
    assert hg.main([]) == 0
    assert capsys.readouterr().out == ""


def test_docs_only_commits_do_not_fire(repo):
    """A DECISIONS row or a doc edit is already its own record. Counting docs/
    would make this fire after nearly every commit — the always-on nag again."""
    _commit(repo, "docs/DECISIONS.md", msg="docs: a row")
    assert hg.gap() is None


# --- it fires when work is genuinely unrecorded --------------------------------

def test_fires_on_a_substantive_commit(repo):
    _commit(repo, "src/load_x.py", msg="feat: a lens")
    g = hg.gap()
    assert g is not None and len(g["commits"]) == 1
    assert "feat: a lens" in g["commits"][0]
    assert "records none of it" in hg.message(g)


def test_fires_on_uncommitted_work_alone(repo):
    """Unrecorded and unpushed is the worse case, not a lesser one."""
    (repo / "src" / "wip.py").write_text("x")
    g = hg.gap()
    assert g is not None and g["dirty"] == 1 and g["commits"] == []
    assert "uncommitted" in hg.message(g)


def test_counts_only_commits_after_the_handoff(repo):
    """Work recorded by the handoff must not be re-reported forever."""
    _commit(repo, "src/a.py", msg="before")
    (repo / "session-summary" / "2026-09-17-s2.md").write_text("# newer\n")
    _run(repo, "add", "-A")
    _run(repo, "commit", "-qm", "handoff 2")
    assert hg.gap() is None
    _commit(repo, "src/b.py", msg="after")
    g = hg.gap()
    assert len(g["commits"]) == 1 and "after" in g["commits"][0]
    assert g["handoff"] == "2026-09-17-s2.md"


def test_merge_commits_are_not_double_counted(repo):
    """A merge restates its branch's changes; counting both reports every PR twice."""
    _run(repo, "checkout", "-q", "-b", "feat")
    _commit(repo, "src/f.py", msg="feat: thing")
    _run(repo, "checkout", "-q", "main")
    _run(repo, "merge", "-q", "--no-ff", "feat", "-m", "Merge pull request #1")
    g = hg.gap()
    assert len(g["commits"]) == 1, g["commits"]


# --- fail-silent contract -----------------------------------------------------

def test_no_handoff_files_is_silent(repo):
    for p in (repo / "session-summary").glob("*.md"):
        p.unlink()
    assert hg.gap() is None


def test_uncommitted_handoff_is_silent(repo, tmp_path):
    """No history for the file (never committed, or a shallow clone) — the
    comparison has no footing, so it says nothing rather than guessing."""
    (repo / "session-summary" / "2026-12-31-s9.md").write_text("# new\n")
    _commit(repo, "src/a.py", msg="work")
    assert hg.gap() is None


def test_not_a_git_repo_is_silent(tmp_path, monkeypatch):
    (tmp_path / "session-summary").mkdir()
    (tmp_path / "session-summary" / "h.md").write_text("x")
    monkeypatch.setattr(hg, "ROOT", tmp_path)
    monkeypatch.setattr(hg, "SUMMARIES", tmp_path / "session-summary")
    assert hg.gap() is None
    assert hg.main([]) == 0


def test_git_missing_is_silent(repo, monkeypatch):
    def boom(*a, **k):
        raise FileNotFoundError("git")
    monkeypatch.setattr(hg.subprocess, "run", boom)
    assert hg.gap() is None
    assert hg.main([]) == 0


def test_main_never_raises_even_if_gap_explodes(repo, monkeypatch, capsys):
    monkeypatch.setattr(hg, "gap", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    assert hg.main([]) == 0
    assert capsys.readouterr().out == ""


# --- hook output CHANNELS ------------------------------------------------------
#
# ⚠️ These replace two tests that pinned the JSON *shape* on SessionEnd and
# PreCompact — both shapes were well-formed and both events throw the JSON away
# (`docs/FINDINGS_guard_burst.md` §2). A shape test cannot see that. What each
# event actually reads, per the hooks reference:
#
#   SessionEnd    JSON discarded; "Shows stderr to user only"  -> stderr, no JSON
#   SessionStart  additionalContext reaches Claude, systemMessage the user
#   PreCompact    JSON discarded; only surface is exit 2, which BLOCKS -> unusable

def test_session_end_writes_to_stderr_and_emits_no_json(repo, capsys):
    _commit(repo, "src/a.py", msg="work")
    hg.main(["--session-end"])
    captured = capsys.readouterr()
    assert "records none of it" in captured.err
    assert captured.out == "", (
        "SessionEnd discards JSON output fields; anything on stdout is thrown "
        "away. stderr is the only surface that event has."
    )


def test_session_start_carries_the_gap_in_additional_context(repo, capsys):
    import json
    _commit(repo, "src/a.py", msg="work")
    hg.main(["--session-start"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    assert "records none of it" in payload["hookSpecificOutput"]["additionalContext"]
    assert "records none of it" in payload["systemMessage"]


def test_session_start_message_does_not_claim_the_same_session(repo, capsys):
    """At SessionStart the gap belongs to a context that is already gone, so the
    end-of-session wording ("append to that file (same session)") is wrong.

    ⚠️ Asserts on what `main(["--session-start"])` actually EMITS, not on
    `message(g, at_start=True)`. The first cut called the helper directly and
    stayed green when the mutation flipped `main`'s call site back to the
    end-of-session wording — `check-where-the-value-can-be-wrong`, committed
    inside the fix for exactly that class, and caught only by mutating it."""
    import json
    _commit(repo, "src/a.py", msg="work")
    hg.main(["--session-start"])
    emitted = json.loads(capsys.readouterr().out)["hookSpecificOutput"]["additionalContext"]
    assert "same session" not in emitted, emitted
    assert "out of context now" in emitted

    hg.main(["--session-end"])
    assert "same session" in capsys.readouterr().err


def test_no_hook_can_block_compaction_or_a_session(repo, capsys):
    """Every mode exits 0. PreCompact's only surface was exit 2, which blocks
    compaction — and on an auto-compact recovering from a context-limit error a
    block fails the request. This script promises it can never end a session
    badly, so it must never hand any event a blocking exit code."""
    _commit(repo, "src/a.py", msg="work")
    for argv in ([], ["--session-start"], ["--session-end"]):
        assert hg.main(argv) == 0, argv
        capsys.readouterr()


def test_long_commit_lists_are_truncated(repo):
    for i in range(9):
        _commit(repo, f"src/f{i}.py", msg=f"work {i}")
    msg = hg.message(hg.gap())
    assert "+4 more" in msg


# --- the fallback interpreter must actually work ------------------------------
#
# The hook prefers `.venv/bin/python` and falls back to the system `python3`,
# which is **3.6.8** on this box. `capture_output=`/`text=` are 3.7+ and raise
# TypeError, which this module's fail-silent handler swallows — so the fallback
# printed NOTHING for ever while looking healthy. A vacuous fallback is worse
# than none, because it reads as working.

def test_source_uses_no_python37_only_subprocess_kwargs():
    # Comment lines are skipped: the fix's own comment NAMES the banned kwargs to
    # explain why they are banned. Mention vs use — the same distinction
    # check_doc_citations.py draws for quoted citations.
    src = "\n".join(
        ln for ln in Path(hg.__file__).read_text().split("\n")
        if not ln.strip().startswith("#")
    )
    for kw in ("capture_output=", "text=True"):
        assert kw not in src, (
            f"{kw} is Python 3.7+; the hook's fallback interpreter is 3.6.8 and "
            f"the failure is SILENT. Use stdout=/stderr=PIPE + universal_newlines."
        )


def test_it_runs_under_the_system_python3(repo):
    """Not just importable — actually produces the report under the fallback."""
    py3 = "/usr/bin/python3"
    if not Path(py3).exists():
        pytest.skip("no system python3 to check the fallback against")
    _commit(repo, "src/a.py", msg="feat: work")
    out = subprocess.run(
        [py3, "-c",
         "import sys;sys.path.insert(0,%r);import handoff_gap as h;"
         "h.ROOT=__import__('pathlib').Path(%r);h.SUMMARIES=h.ROOT/'session-summary';"
         "sys.exit(h.main([]))" % (str(Path(hg.__file__).parent), str(repo))],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
    )
    assert out.returncode == 0, out.stderr
    assert "records none of it" in out.stdout, out.stderr


# --- the wiring IS the feature -------------------------------------------------
#
# Same reasoning as test_ci_workflows.py: a measurement nothing invokes is a
# script, not a guard. settings.json is hand-edited, and a dropped hook is
# invisible — the session simply ends quietly, which is what it does when nothing
# is owed.

def _hook_commands(event):
    import json
    settings = json.loads((Path(hg.__file__).parents[1] / ".claude" / "settings.json").read_text())
    return " ".join(h["command"] for entry in settings["hooks"].get(event, [])
                    for h in entry["hooks"])


def test_both_hooks_invoke_the_gap_script():
    for event, flag in (("SessionStart", "--session-start"), ("SessionEnd", "--session-end")):
        joined = _hook_commands(event)
        assert "handoff_gap.py" in joined, f"{event} no longer runs the gap script"
        assert flag in joined, f"{event} must pass {flag}"
        assert "python3" in joined, f"{event} needs the no-venv fallback"


def test_the_session_end_hook_does_not_discard_its_own_channel():
    """⚠️ The defect this whole rewiring came from. SessionEnd shows stderr and
    discards everything else, so `2>/dev/null` on that hook silences the guard
    completely — while the hook, the script and every shape test stay green."""
    joined = _hook_commands("SessionEnd")
    assert "2>/dev/null" not in joined.split("handoff_gap.py")[-1], (
        "the SessionEnd hook is redirecting stderr away, which is the only "
        "surface that event has — the guard would reach nobody"
    )


def test_no_precompact_hook_runs_the_gap_script():
    """PreCompact discards systemMessage/continue, has no additionalContext, and
    sends exit-0 stdout to the debug log. Its only surface is exit 2 = block
    compaction, which this script may never use. Wiring it there is vacuous."""
    assert "handoff_gap.py" not in _hook_commands("PreCompact"), (
        "PreCompact cannot surface an informational message; SessionStart "
        "(source 'compact') is where that signal lands now"
    )


def test_hooks_do_not_reintroduce_the_unconditional_nag():
    """The old hooks echoed a fixed sentence every session. If that string comes
    back, the measurement has been bypassed and the nag is live again."""
    import json
    settings = (Path(hg.__file__).parents[1] / ".claude" / "settings.json").read_text()
    assert "if you did substantive work" not in settings

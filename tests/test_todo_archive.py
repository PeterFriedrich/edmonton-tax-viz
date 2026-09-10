"""Tests for tools/todo_archive.py.

The tool rewrites TODO.md, the file every session reads first, so a wrong split
is silent: text vanishes from the backlog into an archive nobody reads. On
2026-09-10 closing one 39-line item took 66 lines with it — the item's span ran
to the next checkbox, so a `_Last reconciled_` block and a `###` heading rode
along. These pin that an item ends at the first unindented non-item line, and
that a run adds no blank lines of its own.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import todo_archive  # noqa: E402

TODO_TEXT = """\
# TODO

## Open work

_Last reconciled: preamble note._

- [ ] **Open one.**
  body of open one

- [x] **Closed one — DONE 2026-09-10.**
  body of closed one

  - indented child after a blank line

_Last reconciled: a note that belongs to no item._

### A heading that must stay put

Paragraph under the heading.

- [ ] **Open two.**
  body of open two

## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- **An older done line.**
"""

ARCHIVE_TEXT = """\
# TODO — archive of CLOSED items

---

- [x] **Previously archived.**
"""


@pytest.fixture
def run(tmp_path, monkeypatch):
    todo, archive = tmp_path / "TODO.md", tmp_path / "TODO_archive.md"
    todo.write_text(TODO_TEXT, encoding="utf-8")
    archive.write_text(ARCHIVE_TEXT, encoding="utf-8")
    monkeypatch.setattr(todo_archive, "TODO", todo)
    monkeypatch.setattr(todo_archive, "ARCHIVE", archive)
    assert todo_archive.main() == 0
    return todo.read_text(encoding="utf-8"), archive.read_text(encoding="utf-8")


def test_text_after_a_closed_item_stays_in_todo(run):
    todo, archive = run
    for kept in ("_Last reconciled: a note that belongs to no item._",
                 "### A heading that must stay put",
                 "Paragraph under the heading."):
        assert kept in todo
        assert kept not in archive


def test_closed_item_moves_whole_including_blank_separated_children(run):
    todo, archive = run
    assert "body of closed one" in archive
    assert "indented child after a blank line" in archive
    assert "body of closed one" not in todo


def test_open_items_and_text_keep_their_order(run):
    todo, _ = run
    order = ["preamble note", "Open one.", "belongs to no item", "A heading",
             "Paragraph under", "Open two."]
    positions = [todo.index(s) for s in order]
    assert positions == sorted(positions)


def test_a_run_adds_no_blank_lines(run):
    todo, _ = run
    assert "\n\n\n" not in todo
    assert "## Open work\n\n_Last reconciled: preamble note._" in todo

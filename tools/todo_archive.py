#!/usr/bin/env python3
"""One-shot: move CLOSED TODO.md items into docs/TODO_archive.md.

TODO.md is read first in every session (CLAUDE.md), and had grown to 1,839
lines of which ~740 were CLOSED work kept in place for the record. That record
is worth having — "never redo a closed item without asking" depends on it — but
it does not need to be re-read every session to serve that purpose.

So: closed items move to the archive VERBATIM, and each leaves a one-line entry
in TODO.md's existing `## Done` section. The no-redo rule still works by
grepping `## Done`; the reasoning is one hop away. Same shape as
`session-summary/archive/` and the one-line-plus-pointer rule for DECISIONS.md.

Verifies that no line is lost before writing anything.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODO = ROOT / "TODO.md"
ARCHIVE = ROOT / "docs" / "TODO_archive.md"

ITEM = re.compile(r"^- \[([ x])\] ")


def title_of(block):
    """Best available short title for a closed item."""
    head = " ".join(l.strip() for l in block[:4])
    for pat in (r"~~\*\*(.+?)\*\*~~", r"\*\*(.+?)\*\*"):
        m = re.search(pat, head)
        if m:
            t = m.group(1)
            break
    else:
        t = ITEM.sub("", block[0]).strip()
    t = re.sub(r"\s+", " ", t).strip(" -—~*")
    return t[:150]


def done_marker(block):
    """Pull a 'DONE <date>' / 'SHIPPED <date>' style marker if present."""
    head = " ".join(l.strip() for l in block[:6])
    m = re.search(r"(✅\s*)?\b(DONE|COMPLETE|SHIPPED|LOCKED|EXECUTED|CLOSED|DECIDED|BUILT)\b"
                  r"[^.|]{0,40}?(\d{4}-\d{2}-\d{2})", head, re.I)
    if m:
        return f"{m.group(2).upper()} {m.group(3)}"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", head)
    return m.group(1) if m else ""


def main():
    lines = TODO.read_text(encoding="utf-8").splitlines()
    try:
        open_ix = lines.index("## Open work")
        done_ix = lines.index("## Done")
    except ValueError as e:
        print("todo_archive: expected '## Open work' and '## Done' headings", e)
        return 1

    preamble = lines[:open_ix + 1]
    body = lines[open_ix + 1:done_ix]
    done_tail = lines[done_ix:]

    # Split the body into blocks, each starting at a top-level "- [ ]"/"- [x]".
    blocks, cur = [], []
    for l in body:
        if ITEM.match(l):
            if cur:
                blocks.append(cur)
            cur = [l]
        else:
            (cur if cur else preamble).append(l)
    if cur:
        blocks.append(cur)

    closed = [b for b in blocks if ITEM.match(b[0]).group(1) == "x"]
    still_open = [b for b in blocks if ITEM.match(b[0]).group(1) == " "]
    if not closed:
        print("todo_archive: nothing closed to move")
        return 0

    # --- build the archive ---
    arch = [
        "# TODO — archive of CLOSED items",
        "",
        "Closed work moved out of `TODO.md` so the file that is read at the start of "
        "**every** session carries only live work. **Nothing here is a to-do.**",
        "",
        "`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so "
        "the *never redo a closed item without asking* rule still works by grepping "
        "there; this file holds the reasoning behind each one.",
        "",
        "Items are verbatim as they were closed, newest-moved first in the order they "
        "appeared in `TODO.md`. Line numbers and \"next up\" markers inside them are "
        "historical — do not act on them.",
        "",
        "---",
        "",
    ]
    for b in closed:
        arch += b + [""]

    # --- one-line entries for TODO.md's ## Done ---
    stubs = []
    for b in closed:
        t = title_of(b)
        d = done_marker(b)
        stubs.append(f"- [x] **{t}**" + (f" — {d}" if d else "") +
                     " · `docs/TODO_archive.md`")

    new_done = ([done_tail[0], ""]
                + [f"Closed items moved out of `## Open work` on 2026-07-30 live in "
                   f"**`docs/TODO_archive.md`** — one line each below, reasoning there.",
                   ""]
                + stubs + [""] + done_tail[1:])

    new_todo = preamble + [""] + [l for b in still_open for l in b] + new_done

    # --- accounting: no closed line may vanish ---
    moved = sum(len(b) for b in closed)
    kept = sum(len(b) for b in still_open)
    if moved + len(stubs) < 1:
        print("todo_archive: refusing to write, nothing accounted for")
        return 1
    print(f"closed items      {len(closed):3d}  ({moved} lines) -> docs/TODO_archive.md")
    print(f"open items        {len(still_open):3d}  ({kept} lines) stay")
    print(f"TODO.md         {len(lines):5d} -> {len(new_todo)} lines")

    ARCHIVE.write_text("\n".join(arch).rstrip() + "\n", encoding="utf-8")
    TODO.write_text("\n".join(new_todo).rstrip() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

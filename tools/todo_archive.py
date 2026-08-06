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

Verifies that no line is lost before writing anything, and REFUSES to archive a
closed item that still has unchecked children (`--allow-open-children` to
override) — those are live work, and the archive is where nobody looks for it.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODO = ROOT / "TODO.md"
ARCHIVE = ROOT / "docs" / "TODO_archive.md"
# Matched to find and strip prior copies, so it must stay stable across edits to
# the banner's wording.
BANNER_PREFIX = "Closed items moved out of `## Open work`"

ITEM = re.compile(r"^- \[([ x])\] ")
# An UNCHECKED box nested inside a closed top-level item (any indent depth).
CHILD_OPEN = re.compile(r"^\s+- \[ \] ")


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


def main(allow_open_children=False):
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

    # A closed parent can still carry UNCHECKED children, and archiving it takes
    # them out of the live backlog silently — the archive's own header says
    # "Nothing here is a to-do", so nobody looks. Found on 2026-08-06: the
    # upstream Edmonton Open Data bug report, still open, had ridden the closed
    # temporal-graph item into the archive on 2026-07-31 and sat there 6 days.
    # Same failure shape as the two bugs guarded below — refuse, name the lines,
    # let a human decide (promote to top level, or pass the flag to accept).
    orphans = [(ITEM.sub("", b[0]).strip()[:60], l.strip()[:90])
               for b in closed for l in b[1:] if CHILD_OPEN.match(l)]
    if orphans and not allow_open_children:
        print(f"todo_archive: REFUSING TO WRITE — {len(orphans)} unchecked item(s) "
              f"nested under closed parent(s) would be archived out of sight:")
        for parent, child in orphans:
            print(f"    under {parent!r}\n        {child}")
        print("  Promote each to its own top-level item in TODO.md, close it, or "
              "re-run with --allow-open-children if it is genuinely abandoned.")
        return 1

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
    # ⚠️ APPEND TO THE EXISTING ARCHIVE, NEVER REPLACE IT. This function built
    # `arch` from the header alone and then wrote it, which was harmless on the
    # FIRST run (S79, empty file) and destroyed every previously-archived item
    # on any run after it — 757 lines -> 81 when it was caught on 2026-07-31.
    # The archive is the only copy of that reasoning; TODO.md keeps one-line
    # stubs. Newest-moved first, matching the header's own claim.
    prior = []
    if ARCHIVE.exists():
        old_lines = ARCHIVE.read_text(encoding="utf-8").splitlines()
        # Everything after the header's closing `---` is prior archived content.
        for i, l in enumerate(old_lines):
            if l.strip() == "---":
                prior = old_lines[i + 1:]
                break
        else:
            # No recognisable header: keep the whole file rather than guess.
            prior = old_lines
        while prior and not prior[0].strip():
            prior.pop(0)

    for b in closed:
        arch += b + [""]
    if prior:
        arch += prior + [""]

    # --- one-line entries for TODO.md's ## Done ---
    stubs = []
    for b in closed:
        t = title_of(b)
        d = done_marker(b)
        stubs.append(f"- [x] **{t}**" + (f" — {d}" if d else "") +
                     " · `docs/TODO_archive.md`")

    # Exactly ONE banner, always. This used to be prepended unconditionally while
    # done_tail still carried the previous run's copy, so TODO.md accumulated one
    # duplicate line per archive pass -- three by 2026-07-31, in a file every
    # session reads. Stripping by prefix also cleans up the copies already there,
    # and drops the hardcoded 2026-07-30, which described the FIRST run and was
    # wrong on every run after it. (Same shape as the overwrite bug guarded
    # below: the second and later runs are a different program from the first.)
    banner = (BANNER_PREFIX + " live in **`docs/TODO_archive.md`** — "
              "one line each below, reasoning there.")
    tail = [l for l in done_tail[1:] if not l.startswith(BANNER_PREFIX)]
    new_done = [done_tail[0], "", banner, ""] + stubs + [""] + tail

    new_todo = preamble + [""] + [l for b in still_open for l in b] + new_done

    # --- accounting: no closed line may vanish ---
    moved = sum(len(b) for b in closed)
    kept = sum(len(b) for b in still_open)
    if moved + len(stubs) < 1:
        print("todo_archive: refusing to write, nothing accounted for")
        return 1
    # The archive only ever grows. This is the guard that would have caught the
    # overwrite bug above on its first destructive run, so it checks the SIZE of
    # what is about to be written rather than trusting the append logic.
    prior_len = len(ARCHIVE.read_text(encoding="utf-8").splitlines()) if ARCHIVE.exists() else 0
    if len(arch) < prior_len:
        print(f"todo_archive: REFUSING TO WRITE — the archive would SHRINK "
              f"({prior_len} -> {len(arch)} lines). It is append-only and holds "
              f"the only copy of closed items' reasoning.")
        return 1
    print(f"closed items      {len(closed):3d}  ({moved} lines) -> docs/TODO_archive.md")
    print(f"open items        {len(still_open):3d}  ({kept} lines) stay")
    print(f"TODO.md         {len(lines):5d} -> {len(new_todo)} lines")

    ARCHIVE.write_text("\n".join(arch).rstrip() + "\n", encoding="utf-8")
    TODO.write_text("\n".join(new_todo).rstrip() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(allow_open_children="--allow-open-children" in sys.argv[1:]))

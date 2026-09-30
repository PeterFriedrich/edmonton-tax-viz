"""Project brief for Claude web, generated from the repo so it cannot drift.

Claude web (a claude.ai chat or Project) sees only what it is given. Without a
brief, every research prompt re-writes a "my situation" block and a "don't
recommend back" list by hand, and both go stale. This builds one from the files
the repo already maintains:

  - the ``## Project`` paragraph and the doc map of ``CLAUDE.md``;
  - ``docs/SCOPE.md``, the one hand-kept input ("out of scope / don't recommend");
  - the stack, from ``requirements-ci.txt`` (the direct pins; ``requirements.txt``
    is a 118-line freeze whose JupyterLab tree would bury them);
  - live rows of ``docs/DECISIONS.md`` (struck or SUPERSEDED rows left out),
    each cut to its first sentence plus its first rejected-alternative sentence;
  - open items of ``TODO.md``;
  - the "Status at a glance" table of ``docs/DATA_ISSUES.md``;
  - the reply format a research answer must end with (``docs/CLAUDE_WEB.md``).

``--write`` commits ``docs/BRIEF.md`` and a claude.ai Project syncs it through
the GitHub integration (setup in ``docs/CLAUDE_WEB.md``). Ported by hand from
``cc-data-project-template``, with one deliberate difference: **no merge-gate
staleness test.** TODO.md and DECISIONS.md change in most PRs here (189 and 107
commits in 2026-09), so a gate would put a BRIEF.md diff in nearly every PR and
conflicts between open ones. ``/handoff`` regenerates it instead, so master's
copy is at most one session stale; the Project only refreshes when Sync is
pressed anyway.

The output carries no date or commit SHA on purpose: it must be a pure function
of the source files, or ``--check`` would report stale on every commit.

Exit codes: 0 ok; 6 ``--check`` found ``docs/BRIEF.md`` stale or missing.

Usage:
    python scripts/make_brief.py            # print to stdout
    python scripts/make_brief.py --write    # (re)write docs/BRIEF.md
    python scripts/make_brief.py --check    # exit 6 if docs/BRIEF.md is stale
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEF = "docs/BRIEF.md"

EXIT_OK = 0
EXIT_FAIL = 6

# Summaries are cut here: the brief orients, the full text is in the repo. The
# decisions log would otherwise fill the brief (330 live rows, 469 KB uncut).
ITEM_CHARS = 280
DECISION_CHARS = 200
REJECTED_CHARS = 200

# A sentence ends at . ! or ? (optionally closing a **bold** span) followed by
# space — but not after an abbreviation: "St. Albert" would otherwise cut a
# summary to "St.". Fixed-width lookbehinds, one per abbreviation.
_ABBR = "".join(rf"(?<!\b{re.escape(a)})" for a in ("St.", "e.g.", "i.e.", "vs.", "No."))
SENTENCE_END = re.compile(rf"(?:(?<=[.!?]){_ABBR}|(?<=[.!?]\*\*))\s+")
# The row's alternatives are what a reviewer most needs, to stop recommending
# them back; 79 rows phrase them as "Rejected".
REJECTED = re.compile(r"(?<!-)\b(?:[Rr]ejected|[Rr]efused|[Nn]ot chosen)\b")

ITEM = re.compile(r"^- \[( |x)\] ")
DEAD_ROW = re.compile(r"^\W*~~|\b(?:SUPERSEDED|RETRACTED|REVERSED)\s+\d{4}-\d{2}-\d{2}")

REPLY_FORMAT = """\
End your reply with these fenced tables — one row per item, `-` for an empty
cell. They map onto the repo's own ledgers, so a row can be pasted, not
rewritten. Leave a table out if it has no rows.

```
TODO | why | source
```

```
DECISION | rationale | test that would protect it, or [unverifiable]
```

```
CLAIM-CHECK | claim this brief makes, or the repo seems to assume | evidence for or against
```

Don't recommend anything listed under "Out of scope" or already a locked
decision, unless you are arguing that it should be reopened — then say so in
the DECISION table."""


def _read(root: Path, rel: str) -> str:
    p = root / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _section(md: str, heading: str) -> str:
    """Body under ``## heading`` up to the next ``## `` heading."""
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", md, re.M | re.S)
    return m.group(1).strip() if m else ""


def _cells(line: str) -> list[str]:
    # Unescaped pipes only, as in check_decisions_log.parse_rows.
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def _table_rows(md: str) -> list[list[str]]:
    """Data rows of every markdown table in ``md``, header and rule skipped."""
    rows, in_table = [], False
    for line in md.splitlines():
        if not line.startswith("|"):
            in_table = False
            continue
        if not in_table:
            in_table = True  # header row
            continue
        if re.match(r"^\|\s*:?-{3,}", line):
            continue
        rows.append(_cells(line))
    return rows


def _clip(text: str, cap: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= cap else text[:cap].rsplit(" ", 1)[0] + " …"


def project(root: Path) -> str:
    return _section(_read(root, "CLAUDE.md"), "Project") or "(no `## Project` section in CLAUDE.md)"


def doc_map(root: Path) -> list[str]:
    """One line per Key Files entry: the path and its first clause."""
    out = []
    for line in _section(_read(root, "CLAUDE.md"), "Key Files").splitlines():
        m = re.match(r"^- (`[^`]+`)\s+—\s+(.*)", line)
        if m:
            first = re.split(r"(?<=[.!?])\s|\s—\s", m.group(2), maxsplit=1)[0]
            out.append(f"- {m.group(1)} — {first.rstrip('.')}")
    return out


def scope(root: Path) -> str:
    md = _read(root, "docs/SCOPE.md")
    body = _section(md, "Out of scope") if md else ""
    return body or "(none recorded — add `docs/SCOPE.md`)"


def stack(root: Path) -> list[str]:
    out = []
    reqs = _read(root, "requirements-ci.txt") or _read(root, "requirements.txt")
    for line in reqs.splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(f"- {line}")
    pkg = _read(root, "package.json")
    if pkg:
        data = json.loads(pkg)
        for key in ("dependencies", "devDependencies"):
            for name, ver in sorted(data.get(key, {}).items()):
                out.append(f"- {name} {ver}" + (" (dev)" if key == "devDependencies" else ""))
    return out


def decisions(root: Path) -> list[str]:
    out = []
    for cells in _table_rows(_read(root, "docs/DECISIONS.md")):
        if len(cells) < 2 or DEAD_ROW.search(cells[1]):
            continue
        sentences = SENTENCE_END.split(cells[1])
        line = f"- **{cells[0]}** — {_clip(sentences[0], DECISION_CHARS)}"
        rejected = next((s for s in sentences[1:] if REJECTED.search(s)), None)
        if rejected:
            line += f" … {_clip(rejected, REJECTED_CHARS)}"
        out.append(line)
    return out


def open_items(root: Path) -> list[str]:
    """Top-level ``- [ ]`` items under ``## Open work`` (continuation lines
    joined), with the ``###`` groupings kept."""
    out, item = [], None

    def flush():
        if item is not None:
            out.append(f"- {_clip(' '.join(item), ITEM_CHARS)}")

    for line in _section(_read(root, "TODO.md"), "Open work").splitlines():
        m = ITEM.match(line)
        if m or line.startswith("### "):
            flush()
            item = None
            if line.startswith("### "):
                out.append(f"\n**{line[4:].strip()}**")
            elif m.group(1) == " ":
                item = [ITEM.sub("", line)]
        elif item is not None and line.startswith("  ") and not line.lstrip().startswith("- ["):
            item.append(line.strip())
    flush()
    return out


def data_issues(root: Path) -> list[str]:
    out = []
    glance = _section(_read(root, "docs/DATA_ISSUES.md"), "Status at a glance")
    for cells in _table_rows(glance):
        # # | issue | evidence | report text | status
        if len(cells) == 5:
            out.append(f"- #{cells[0]} {cells[1]} — status: {cells[4]}")
    return out


def build(root: Path = ROOT) -> str:
    def block(title: str, lines: list[str], empty: str) -> str:
        body = "\n".join(lines).strip() if lines else empty
        return f"## {title}\n\n{body}\n"

    parts = [
        "# Project brief\n",
        "<!-- GENERATED by scripts/make_brief.py — do not edit. /handoff regenerates it\n"
        "     with `python scripts/make_brief.py --write`. -->\n",
        "For a Claude web chat: this is the project as its repo records it. The repo\n"
        "is the source of truth; where this brief and your own assumptions differ,\n"
        "the brief wins.\n",
        f"## What it is\n\n{project(root)}\n",
        f"## Out of scope — don't recommend back\n\n{scope(root)}\n",
        block("Stack", stack(root), "(no requirements.txt / package.json entries)"),
        block("Locked decisions", decisions(root), "(none yet)"),
        block("Open work", open_items(root), "(none)"),
        # An empty result is reported as what it is, not as "no defects".
        block("Known upstream data defects", data_issues(root),
              "(no rows in the \"Status at a glance\" table of `docs/DATA_ISSUES.md`)"),
        block("Where things live", doc_map(root), "(no Key Files list in CLAUDE.md)"),
        f"## Reply format\n\n{REPLY_FORMAT}\n",
    ]
    return "\n".join(parts)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = p.add_mutually_exclusive_group()
    g.add_argument("--write", action="store_true", help=f"write {BRIEF}")
    g.add_argument("--check", action="store_true", help=f"exit {EXIT_FAIL} if {BRIEF} is stale")
    p.add_argument("--root", type=Path, default=ROOT)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    text = build(args.root)
    target = args.root / BRIEF
    if args.write:
        target.write_text(text, encoding="utf-8")
        print(f"wrote {BRIEF}")
    elif args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != text:
            print(f"{BRIEF} is stale or missing — run: python scripts/make_brief.py --write",
                  file=sys.stderr)
            return EXIT_FAIL
    else:
        sys.stdout.write(text)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

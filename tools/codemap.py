#!/usr/bin/env python3
"""Emit docs/CODEMAP.md — a symbol index for the big single-file front end.

Why this exists: `web/index.html` is ~7,300 lines holding the whole app, so a
session that needs `refreshLegend` has no way to find it except scanning. That
scanning is the dominant context cost of a front-end session (S79). This gives
every symbol a line range and a one-line purpose, so you can jump straight to a
40-line slice instead of paging through 60-line windows hunting for it.

Line numbers here go stale on the next edit BY DESIGN — regenerate, don't cite.
The handoff convention (symbols, not line numbers) still holds for prose; this
file is the lookup table that makes it navigable.

    python tools/codemap.py            # write docs/CODEMAP.md
    python tools/codemap.py --check    # exit 1 if stale (for CI, if wanted)
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "CODEMAP.md"

# A symbol worth indexing: a function declaration, or a top-level const that
# holds an arrow function or a config object. Plain scalar consts are noise.
SYMBOL = re.compile(
    r"^(?P<indent>\s*)(?:async\s+)?(?:function\s+(?P<fn>\w+)"
    r"|const\s+(?P<const>[A-Za-z_]\w*)\s*=\s*(?P<rhs>.*))"
)
ID_ATTR = re.compile(r'\bid="([\w-]+)"')
# The file's own section banners: `// --- title -------`. Grouping by them beats
# one flat 250-row table — you usually know the AREA before the symbol.
BANNER = re.compile(r"^\s*//\s*-{2,}\s*(?P<title>.+?)\s*-{3,}\s*$")


def leading_comment(lines, i):
    """First line of the comment block directly above line i, if any."""
    j = i - 1
    block = []
    while j >= 0:
        s = lines[j].strip()
        if s.startswith("//"):
            block.append(s[2:].strip())
            j -= 1
        elif not s and block:
            break
        else:
            break
    if not block:
        return ""
    # block is bottom-up; the FIRST line of the comment is the topic sentence.
    text = block[-1]
    text = re.sub(r"\s+", " ", text).strip(" -—*")
    return text[:120]


def interesting_const(rhs):
    """Keep arrow functions and structured config; drop scalar constants."""
    rhs = rhs.strip()
    if "=>" in rhs:
        return True
    return rhs.startswith("{") or rhs.startswith("[")


def collect(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = []
    section = "(top)"
    for i, line in enumerate(lines):
        b = BANNER.match(line)
        if b:
            section = b.group("title").strip()
            continue
        m = SYMBOL.match(line)
        if not m:
            continue
        # TOP LEVEL ONLY (indent 4 in this file). Indexing body-level `const`s
        # does not merely add noise — it TRUNCATES the enclosing symbol's range,
        # because a range runs to the next indexed line. changeFor read as
        # "1697-1699" until this was tightened.
        if len(m.group("indent")) > 4:
            continue
        name = m.group("fn")
        if not name:
            name = m.group("const")
            if not interesting_const(m.group("rhs") or ""):
                continue
        hits.append({"name": name, "line": i + 1, "section": section,
                     "why": leading_comment(lines, i)})
    # End of each symbol = the line before the next one starts.
    for a, b in zip(hits, hits[1:]):
        a["end"] = b["line"] - 1
    if hits:
        hits[-1]["end"] = len(lines)
    return hits, lines


def element_ids(lines):
    """Element ids in markup order — the control surface, by name."""
    out = []
    seen = set()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("//"):
            continue
        for m in ID_ATTR.finditer(line):
            if m.group(1) not in seen:
                seen.add(m.group(1))
                out.append((m.group(1), i + 1))
    return out


def render():
    src = ROOT / "web" / "index.html"
    hits, lines = collect(src)
    ids = element_ids(lines)
    L = [
        "# CODEMAP — `web/index.html`",
        "",
        "**Generated — do not hand-edit.** `python tools/codemap.py`",
        "",
        "`web/index.html` is a single ~{:,}-line file holding the whole front end. "
        "This is the lookup table for it: jump to a symbol's range instead of "
        "scanning. **Line numbers go stale on the next edit — regenerate rather "
        "than citing them.** Prose should still name symbols, not lines.".format(len(lines)),
        "",
        "## Symbols ({} indexed)".format(len(hits)),
        "",
        "Grouped by the file's own `// --- section ---` banners, in file order.",
    ]
    last = None
    for h in hits:
        if h["section"] != last:
            last = h["section"]
            L += ["", "### {}".format(last), "",
                  "| symbol | lines | what it does |", "|---|---|---|"]
        why = h["why"].replace("|", "\\|")
        L.append("| `{}` | {}–{} | {} |".format(h["name"], h["line"], h["end"], why))
    L += [
        "",
        "## Element ids ({}) — the control surface".format(len(ids)),
        "",
        "| id | line |",
        "|---|---|",
    ]
    L += ["| `#{}` | {} |".format(i, n) for i, n in ids]
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if CODEMAP.md is out of date")
    args = ap.parse_args()
    new = render()
    if args.check:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != new:
            print("codemap: docs/CODEMAP.md is STALE — run python tools/codemap.py")
            return 1
        print("codemap: up to date")
        return 0
    OUT.write_text(new, encoding="utf-8")
    print("codemap: wrote {}".format(OUT.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

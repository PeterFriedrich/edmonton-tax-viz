"""Guards for the generated symbol index (tools/codemap.py -> docs/CODEMAP.md).

The map exists so a session can jump to a symbol's line range instead of
scanning a ~4,250-line file. Both ways it can fail are SILENT — it keeps
looking fine while quietly ceasing to help:

  1. **Stale.** Symbols move on every edit, so a map generated two commits ago
     sends you to the wrong slice. Nothing errors; you just search anyway and
     the map has cost more than it saved.
  2. **Blind.** The extractor is a regex, not a JS parser. It currently catches
     100% of function declarations, but only because the file has a consistent
     house style — a function written in a shape the regex does not match would
     be missing from the map with no warning at all.

The second is the one worth a test: it converts "it happens to catch
everything" into "it is required to catch everything".
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import codemap  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "web" / "index.html"
MAP = REPO / "docs" / "CODEMAP.md"

FUNC_DECL = re.compile(r"^\s*(?:async\s+)?function (\w+)")


def test_codemap_is_not_stale():
    """docs/CODEMAP.md must match what tools/codemap.py emits today."""
    assert MAP.exists(), "docs/CODEMAP.md is missing — run: python tools/codemap.py"
    assert MAP.read_text(encoding="utf-8") == codemap.render(), (
        "docs/CODEMAP.md is STALE — its line numbers no longer match "
        "web/index.html. Regenerate with:  python tools/codemap.py"
    )


def test_codemap_indexes_every_function_declaration():
    """No function may be missing from the map.

    The extractor is a regex; this is what stops it silently going blind if the
    file's style drifts (a nested declaration, an unusual indent, a generator).
    If this fails, fix tools/codemap.py's SYMBOL pattern — do not delete the
    assertion, the map's whole value is being complete.
    """
    declared = {m.group(1) for m in
                (FUNC_DECL.match(l) for l in SRC.read_text(encoding="utf-8").splitlines())
                if m}
    indexed = set(re.findall(r"^\| `(\w+)`", MAP.read_text(encoding="utf-8"), re.M))
    missing = sorted(declared - indexed)
    assert not missing, (
        f"{len(missing)} function(s) declared in web/index.html but absent from "
        f"docs/CODEMAP.md: {missing[:10]} — tools/codemap.py's SYMBOL regex "
        f"missed them."
    )


def test_codemap_line_ranges_are_ordered_and_in_bounds():
    """A range that runs backwards or past EOF means the parser lost its place."""
    n_lines = len(SRC.read_text(encoding="utf-8").splitlines())
    rows = re.findall(r"^\| `\w+` \| (\d+)–(\d+) \|", MAP.read_text(encoding="utf-8"), re.M)
    assert rows, "no symbol rows parsed out of docs/CODEMAP.md"
    for start, end in rows:
        start, end = int(start), int(end)
        assert start <= end, f"range runs backwards: {start}–{end}"
        assert end <= n_lines, f"range {start}–{end} runs past EOF ({n_lines})"

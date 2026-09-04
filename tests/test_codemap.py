"""Guards for the generated symbol index (tools/codemap.py -> docs/CODEMAP.md).

These test the EXTRACTOR against the current source, never the committed
`docs/CODEMAP.md`. That distinction is the whole design of this file.

**There is deliberately no "is the committed map stale?" test.** One was written
2026-07-30 and removed the same day: `pytest` is refresh.yml's *"guard before
regenerating"* step, so a failing test stops the weekly data refresh outright —
no download, no regen, no deploy. Letting a **documentation artifact** halt the
data pipeline because someone edited `web/index.html` without re-running a
generator is wildly disproportionate to the harm (a stale map degrades
*gracefully*: line numbers shift by the size of the edit, and a 20-line drift
inside a 178-line range still lands you in the right function).

Staleness is handled by **regenerating on use** — `python tools/codemap.py`
takes 40ms, so a session runs it when it starts and after editing the file.
See `docs/TOKEN_EFFICIENCY.md` rule 5.

What IS worth guarding is the extractor going **blind**: it is a regex, not a JS
parser, and it currently catches 100% of function declarations only because the
file has a consistent house style. A function written in an unmatched shape
would vanish from the map with no warning. These tests convert "happens to catch
everything" into "required to catch everything", and they cannot be tripped by
the committed file being out of date.
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


def test_extractor_indexes_every_function_declaration():
    """No function may be missing from a FRESHLY GENERATED map.

    This is the one that matters: it stops the regex silently going blind if the
    file's style drifts (a nested declaration, an unusual indent, a generator).
    If it fails, fix tools/codemap.py's SYMBOL pattern — do not delete the
    assertion, completeness is the map's whole value.
    """
    declared = {m.group(1) for m in
                (FUNC_DECL.match(l) for l in SRC.read_text(encoding="utf-8").splitlines())
                if m}
    indexed = set(re.findall(r"^\| `(\w+)`", codemap.render(), re.M))
    missing = sorted(declared - indexed)
    assert not missing, (
        f"{len(missing)} function(s) declared in web/index.html but NOT extracted "
        f"by tools/codemap.py: {missing[:10]} — its SYMBOL regex missed them."
    )


def test_extractor_line_ranges_are_ordered_and_in_bounds():
    """A range that runs backwards or past EOF means the parser lost its place."""
    n_lines = len(SRC.read_text(encoding="utf-8").splitlines())
    rows = re.findall(r"^\| `\w+` \| (\d+)–(\d+) \|", codemap.render(), re.M)
    assert rows, "tools/codemap.py extracted no symbols at all"
    for start, end in rows:
        start, end = int(start), int(end)
        assert start <= end, f"range runs backwards: {start}–{end}"
        assert end <= n_lines, f"range {start}–{end} runs past EOF ({n_lines})"


def test_committed_map_exists_and_parses():
    """The committed map must be present and shaped like a map.

    Deliberately does NOT compare it to a fresh render — see the module
    docstring. Being out of date is fine; being absent or malformed is not.
    """
    assert MAP.exists(), "docs/CODEMAP.md is missing — run: python tools/codemap.py"
    rows = re.findall(r"^\| `\w+` \| \d+–\d+ \|", MAP.read_text(encoding="utf-8"), re.M)
    assert len(rows) > 50, f"docs/CODEMAP.md has only {len(rows)} symbol rows"


def test_reference_graph_ignores_property_access():
    """`foo.state` must NOT count as a reference to the symbol `state`.

    Without the no-dot lookbehind, every `props.state`-shaped access inflates
    the in-degree of a common name — and in-degree is the number the front-end
    refactor decision reads to find the shared kernel. A graph that silently
    counted property access would make an ordinary symbol look load-bearing.

    ⚠️ Asserted from CALLER's edges, not `state`'s own: `reference_graph`
    strips self-references, so a fixture where `state` is the only symbol
    cannot fail this no matter what the regex does.
    """
    def graph(body_line):
        hits = [{"name": "state", "line": 1, "section": "s", "why": "", "end": 1},
                {"name": "caller", "line": 2, "section": "s", "why": "", "end": 3}]
        lines = ["const state = {};", "const caller = () => {", body_line]
        return codemap.reference_graph(hits, lines)["caller"]

    assert graph("  return state.view;") == {"state"}, "a real reference was missed"
    assert graph("  return foo.state;") == set(), "property access counted as a reference"


def test_reference_graph_is_not_degenerate_on_the_real_file():
    """A blind graph (all-empty, or everything referencing everything) is the
    failure this catches — it would look fine in the rendered table."""
    hits, lines = codemap.collect(SRC)
    edges = codemap.reference_graph(hits, lines)
    total = sum(len(v) for v in edges.values())
    assert total > 100, f"only {total} edges — the identifier regex went blind"
    assert total < len(hits) ** 2 / 4, f"{total} edges is implausibly dense"
    assert any(edges[h["name"]] for h in hits), "no symbol references any other"

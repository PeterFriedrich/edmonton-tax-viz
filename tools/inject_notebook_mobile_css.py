"""Make the published evidence notebooks' code cells readable on a phone.

nbconvert's lab template lays the input area out as `display: table-cell` with
`overflow: hidden` and no scrollable element inside it, so a code line wider
than the viewport is CLIPPED, not scrolled — unreachable on any narrow screen.
Measured 2026-09-20: 54 of 54 code cells across the five published reports lost
up to 561px at 390px wide, while none were clipped at 1280px.

Wrapping is the fix rather than a scroller because `overflow-x` on a
`display: table-cell` box is unreliable, and a nested horizontal scroll region
is a poor affordance on touch. The `overflow-x: auto` below is only a backstop
for a token too long to wrap.

Idempotent: re-running replaces the marked block rather than stacking copies.
Run after rendering a notebook to `web/notebooks/` (see docs/EVIDENCE_NOTEBOOKS.md).
"""

import argparse
import pathlib
import re
import sys

START = "<!-- mobile-code-wrap: injected by tools/inject_notebook_mobile_css.py -->"
END = "<!-- /mobile-code-wrap -->"

BLOCK = f"""{START}
<style>
/* Long code lines are clipped, not scrolled, by the lab template's
   table-cell input area. Wrap them instead. A hanging indent would mark
   continuations, but the whole cell is one <pre>, so text-indent reaches
   only its first line — it cost width and marked nothing. */
.jp-InputArea-editor {{
  overflow-x: auto;
}}
.jp-InputArea-editor .highlight pre,
.jp-InputArea-editor pre {{
  white-space: pre-wrap;
  overflow-wrap: break-word;
}}
</style>
{END}"""

PATTERN = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)


def inject(path: pathlib.Path) -> str:
    html = path.read_text(encoding="utf-8")
    if PATTERN.search(html):
        updated = PATTERN.sub(BLOCK, html)
        action = "unchanged" if updated == html else "refreshed"
    else:
        if "</head>" not in html:
            return "SKIPPED — no </head>"
        updated = html.replace("</head>", BLOCK + "\n</head>", 1)
        action = "injected"
    if updated != html:
        path.write_text(updated, encoding="utf-8")
    return action


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dir",
        type=pathlib.Path,
        default=pathlib.Path("web/notebooks"),
        help="directory of rendered notebook HTML (default: web/notebooks)",
    )
    args = ap.parse_args()

    targets = sorted(p for p in args.dir.glob("*.html") if p.name != "index.html")
    if not targets:
        print(f"no rendered notebooks in {args.dir}", file=sys.stderr)
        return 1
    for p in targets:
        print(f"{p}: {inject(p)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

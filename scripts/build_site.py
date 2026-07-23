#!/usr/bin/env python3
"""Emit the two-build GitHub Pages tree from web/ (docs/PLAN_public_release.md §2a).

ONE hand-edited source (``web/index.html``) carries a ``DEFAULT_BUILD`` literal
and gates every full-only control on ``BUILD === "full"``. This step fans it out
into the single Pages artifact:

  <out>/            PUBLIC build (curated). The whole web/ tree — shared data/ +
                    vendor/ — with index.html's DEFAULT_BUILD rewritten to
                    "public". This is the site root, the advertised URL.
  <out>/full/       SPECIALIST build (everything). index.html ONLY, with a
                    ``<base href="../">`` so its relative asset URLs (./data/...,
                    vendor/...) resolve to the ROOT's shared data/ + vendor/ — no
                    duplication of the multi-MB GeoJSON. DEFAULT_BUILD stays
                    "full", and a visible work-in-progress badge is injected (the
                    mitigation for /full/ being discoverable-but-unlisted, not
                    access-controlled — PLAN_public_release.md §2a).

No data download or regeneration happens here: it is a pure code-shaping step, so
it lives on the CODE deploy path. Run it before actions/upload-pages-artifact in
BOTH deploy.yml and refresh.yml (factor once, don't inline twice), uploading
<out> instead of web/.

  python scripts/build_site.py --src web --out _site
"""
import argparse
import re
import shutil
from pathlib import Path

# Fixed WIP badge for the specialist build. pointer-events:none so it never
# eats a map click; bottom-centre keeps clear of the legend (bottom-left) and
# the MapLibre attribution (bottom-right).
WIP_BADGE = (
    '<div id="wip-badge" style="position:fixed;left:50%;bottom:10px;'
    'transform:translateX(-50%);z-index:9999;pointer-events:none;'
    "font:600 11px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;"
    'color:#f3e2b0;background:rgba(40,30,12,0.92);border:1px solid #6b5a2a;'
    'border-radius:5px;padding:4px 10px;">'
    'Specialist build — work in progress</div>'
)

BUILD_RE = re.compile(r'const DEFAULT_BUILD = "(?:public|full)";')


def set_default_build(html: str, mode: str) -> str:
    """Rewrite the single DEFAULT_BUILD literal; fail loudly if it drifted."""
    assert mode in ("public", "full")
    html2, n = BUILD_RE.subn(f'const DEFAULT_BUILD = "{mode}";', html)
    if n != 1:
        raise SystemExit(
            f"build_site: expected exactly 1 DEFAULT_BUILD literal in index.html, "
            f"found {n} — did the source change? (looked for the "
            f'`const DEFAULT_BUILD = \"...\";` line)'
        )
    return html2


def build(src: Path, out: Path) -> None:
    if not (src / "index.html").is_file():
        raise SystemExit(f"build_site: {src}/index.html not found")
    if out.exists():
        shutil.rmtree(out)

    # Root = PUBLIC: copy the whole tree, then flip index.html's default.
    shutil.copytree(src, out)
    root_index = out / "index.html"
    root_index.write_text(set_default_build(root_index.read_text(), "public"))

    # /full/ = SPECIALIST: index.html only, sharing the root's data/ + vendor/
    # via <base>. The base MUST precede the vendor <link>/<script> it rewrites,
    # so inject it immediately after <head>.
    full_html = set_default_build((src / "index.html").read_text(), "full")
    if "<base " in full_html:
        raise SystemExit("build_site: source already carries a <base> tag — "
                         "the /full/ share-root injection assumes none")
    if full_html.count("<head>") != 1 or full_html.count("</body>") != 1:
        raise SystemExit("build_site: expected exactly one <head> and one </body>")
    full_html = full_html.replace("<head>", '<head>\n  <base href="../" />', 1)
    full_html = full_html.replace("</body>", f"  {WIP_BADGE}\n</body>", 1)
    full_dir = out / "full"
    full_dir.mkdir()
    (full_dir / "index.html").write_text(full_html)

    print(f"build_site: wrote {out}/ (public) + {out}/full/ (specialist)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Emit the two-build Pages tree.")
    ap.add_argument("--src", default="web", type=Path, help="source web/ dir")
    ap.add_argument("--out", default="_site", type=Path, help="output artifact dir")
    args = ap.parse_args()
    build(args.src, args.out)


if __name__ == "__main__":
    main()

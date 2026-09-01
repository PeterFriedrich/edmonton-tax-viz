#!/usr/bin/env python3
"""Emit the two-build GitHub Pages tree from web/ (docs/PLAN_public_release.md §2a).

ONE hand-edited source (``web/index.html``) carries a ``DEFAULT_BUILD`` literal
and gates every full-only control on ``BUILD === "full"``. This step fans it out
into the single Pages artifact:

  <out>/            PUBLIC build (curated). The whole web/ tree — shared data/ +
                    vendor/ — with index.html's DEFAULT_BUILD rewritten to
                    "public". This is the site root, the advertised URL. Carries
                    a "Beta build" badge.
  <out>/full/       SPECIALIST build (everything). index.html ONLY, with a
                    ``<base href="../">`` so its relative asset URLs (./data/...,
                    vendor/...) resolve to the ROOT's shared data/ + vendor/ — no
                    duplication of the multi-MB GeoJSON. DEFAULT_BUILD stays
                    "full", and its badge names the build as well as the beta
                    status (the mitigation for /full/ being discoverable-but-
                    unlisted, not access-controlled — PLAN_public_release.md §2a).

No data download or regeneration happens here: it is a pure code-shaping step, so
it lives on the CODE deploy path. Run it before actions/upload-pages-artifact in
BOTH deploy.yml and refresh.yml (factor once, don't inline twice), uploading
<out> instead of web/.

  python scripts/build_site.py --src web --out _site
"""
import argparse
import datetime as dt
import hashlib
import os
import re
import shutil
import subprocess
from pathlib import Path

# WIP badge, one per build with its own label. pointer-events:none so it never
# eats a map click; bottom-centre keeps clear of the legend (bottom-left) and
# the MapLibre attribution (bottom-right).
BADGE_LABELS = {
    "public": "Beta build — work in progress",
    "full": "Specialist build (beta) — work in progress",
}


def wip_badge(label: str) -> str:
    return (
        '<div id="wip-badge" style="position:fixed;left:50%;bottom:10px;'
        'transform:translateX(-50%);z-index:9999;pointer-events:none;'
        "font:600 11px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;"
        'color:#f3e2b0;background:rgba(40,30,12,0.92);border:1px solid #6b5a2a;'
        'border-radius:5px;padding:4px 10px;">'
        f'{label}</div>'
    )


def inject_badge(html: str, mode: str) -> str:
    """Insert the build's badge before the document's own </body>.

    The LAST </body> is the document's; the first is only the same tag when
    nothing below quotes it in a string (web/index.html is nearly all script).
    """
    body_end = html.rfind("</body>")
    if body_end < 0:
        raise SystemExit("build_site: no </body> in the source")
    return html[:body_end] + f"  {wip_badge(BADGE_LABELS[mode])}\n" + html[body_end:]

BUILD_RE = re.compile(r'const DEFAULT_BUILD = "(?:public|full)";')
STYLES_RE = re.compile(r'href="styles\.css"')
STAMP_RE = re.compile(r'const BUILD_STAMP = "[^"]*";')


def build_stamp() -> str:
    """Short commit + UTC date identifying the deployed CODE.

    Env first, git second: in CI ``GITHUB_SHA`` is authoritative and always set,
    while ``git rev-parse`` on an Actions checkout can describe something other
    than the commit being deployed. Locally there is no env var and git is the
    only source.

    ⚠️ Falls back to ``"dev"`` rather than raising. This runs on the deploy path,
    and a missing git binary is not a reason to refuse to publish a working
    site — the same fail-open reasoning as the pre-push hook. "dev" on screen is
    honest about not being a released build; a crashed deploy would not be.
    """
    sha = os.environ.get("GITHUB_SHA", "")
    if not sha:
        try:
            sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True, text=True, timeout=10, check=True,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return "dev"
    if not sha:
        return "dev"
    return f"{sha[:7]} · {dt.datetime.now(dt.timezone.utc):%Y-%m-%d}"


def set_build_stamp(html: str, stamp: str) -> str:
    """Rewrite the single BUILD_STAMP literal; fail loudly if it drifted."""
    if '"' in stamp:
        raise SystemExit(f"build_site: refusing to inject a quote in the stamp: {stamp!r}")
    html2, n = STAMP_RE.subn(f'const BUILD_STAMP = "{stamp}";', html)
    if n != 1:
        raise SystemExit(
            f"build_site: expected exactly 1 BUILD_STAMP literal in index.html, "
            f"found {n} — did the source change? (looked for the "
            f'`const BUILD_STAMP = \"...\";` line)'
        )
    return html2


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


def css_token(css: Path) -> str:
    """Version token for the stylesheet link: 8 hex of its content hash.

    Content hash rather than the commit sha deliberately — a sha changes on every
    deploy, including ones that never touched the CSS, so it would discard a
    working browser cache for nothing. It also needs no git at build time.
    """
    return hashlib.sha256(css.read_bytes()).hexdigest()[:8]


def cache_bust(html: str, token: str) -> str:
    """Stamp the stylesheet link with ?v=<token>; fail loudly if it drifted.

    ``styles.css`` split out of ``index.html`` on 2026-07-29, so a CSS-only change
    now ships in a file with its own cache lifetime and can render stale against a
    fresh page — a deploy that looks half-shipped (RUNBOOK.md §3c). Note this only
    covers stale CSS under fresh HTML: a browser holding index.html itself stale
    holds this query with it.
    """
    html2, n = STYLES_RE.subn(f'href="styles.css?v={token}"', html)
    if n != 1:
        raise SystemExit(
            f'build_site: expected exactly 1 `href="styles.css"` link in '
            f"index.html, found {n} — did the source change?"
        )
    return html2


def build(src: Path, out: Path) -> None:
    if not (src / "index.html").is_file():
        raise SystemExit(f"build_site: {src}/index.html not found")
    if not (src / "styles.css").is_file():
        raise SystemExit(f"build_site: {src}/styles.css not found")
    if out.exists():
        shutil.rmtree(out)

    # Both builds get the SAME token — /full/ resolves styles.css through its
    # <base href="../" />, so it reads the root's copy of the very file hashed.
    token = css_token(src / "styles.css")
    # ONE stamp for both copies: they are the same commit, emitted in the same
    # run. Computed once so a midnight-crossing build cannot date them apart.
    stamp = build_stamp()

    # Root = PUBLIC: copy the whole tree, then flip index.html's default.
    shutil.copytree(src, out)
    root_index = out / "index.html"
    root_index.write_text(
        inject_badge(
            cache_bust(
                set_build_stamp(set_default_build(root_index.read_text(), "public"), stamp),
                token,
            ),
            "public",
        )
    )

    # /full/ = SPECIALIST: index.html only, sharing the root's data/ + vendor/
    # via <base>. The base MUST precede the vendor <link>/<script> it rewrites,
    # so inject it immediately after <head>.
    full_html = cache_bust(
        set_build_stamp(
            set_default_build((src / "index.html").read_text(), "full"), stamp
        ),
        token,
    )
    # ⚠️ THESE CHECKS ARE SCOPED TO THE <head> SLICE ON PURPOSE — an unscoped
    # `"<base " in full_html` failed a green deploy on PR #117, because a single
    # COMMENT mentioning the tag, ~289,000 characters below </head>, reads
    # identically to a competing <base> element. web/index.html is ~4,250 lines
    # and nearly all of it is script below the head, so any whole-file substring
    # test here is a false-positive generator, not a guard.
    head_end = full_html.find("</head>")
    if head_end < 0:
        raise SystemExit("build_site: no </head> in the source")
    head = full_html[:head_end]
    if "<base " in head:
        raise SystemExit("build_site: source already carries a <base> tag — "
                         "the /full/ share-root injection assumes none")
    if head.count("<head>") != 1:
        raise SystemExit("build_site: expected exactly one <head>")
    full_html = full_html.replace("<head>", '<head>\n  <base href="../" />', 1)
    full_html = inject_badge(full_html, "full")
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

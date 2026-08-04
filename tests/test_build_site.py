"""Guards for the two-build Pages emit (scripts/build_site.py).

The one that matters for CI: if web/index.html's ``DEFAULT_BUILD`` literal ever
drifts (renamed/removed), the emit must FAIL loudly rather than silently ship a
single-mode site — so refresh.yml's pytest gate catches it before deploy.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, "scripts")
import build_site  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def test_source_has_exactly_one_default_build_literal():
    """The real web/index.html must carry the literal the deploy step rewrites."""
    html = (REPO / "web" / "index.html").read_text()
    assert len(build_site.BUILD_RE.findall(html)) == 1


def test_set_default_build_flips_the_literal():
    src = 'x\nconst DEFAULT_BUILD = "full";\ny'
    assert 'const DEFAULT_BUILD = "public";' in build_site.set_default_build(src, "public")
    assert 'const DEFAULT_BUILD = "full";' in build_site.set_default_build(src, "full")


def test_set_default_build_fails_on_drift():
    with pytest.raises(SystemExit):
        build_site.set_default_build("no literal here", "public")


def test_source_has_exactly_one_bustable_stylesheet_link():
    """The real web/index.html must carry the link the deploy step stamps."""
    html = (REPO / "web" / "index.html").read_text()
    assert len(build_site.STYLES_RE.findall(html)) == 1


def test_cache_bust_fails_on_drift():
    with pytest.raises(SystemExit):
        build_site.cache_bust('<link href="other.css" rel="stylesheet" />', "abc12345")


def test_build_emits_both_copies(tmp_path):
    src = tmp_path / "web"
    (src / "data").mkdir(parents=True)
    (src / "vendor").mkdir()
    (src / "data" / "x.json").write_text("{}")
    (src / "styles.css").write_text("#map { color: red }")
    (src / "index.html").write_text(
        '<head>\n<script src="vendor/a.js"></script>\n'
        '<link href="styles.css" rel="stylesheet" />\n</head>\n'
        '<body><script>const DEFAULT_BUILD = "full";</script></body>'
    )
    out = tmp_path / "_site"
    build_site.build(src, out)

    root = (out / "index.html").read_text()
    full = (out / "full" / "index.html").read_text()
    # Root = public, shares the tree; /full/ = specialist, base-href to root,
    # WIP badge, and NOT a duplicated data/ dir.
    assert 'const DEFAULT_BUILD = "public";' in root
    assert (out / "data" / "x.json").is_file()
    assert 'const DEFAULT_BUILD = "full";' in full
    assert '<base href="../" />' in full
    assert "work in progress" in full.lower()
    assert not (out / "full" / "data").exists()

    # Both copies carry the SAME token, and it is the source CSS's own hash —
    # /full/ reads the root's styles.css through its <base>, so a divergent
    # token there would point at a file that never gets that name.
    token = build_site.css_token(src / "styles.css")
    assert f'href="styles.css?v={token}"' in root
    assert f'href="styles.css?v={token}"' in full


def test_css_token_tracks_content_not_the_deploy(tmp_path):
    """Same bytes ⇒ same token, so an unrelated deploy keeps the cached CSS."""
    a, b = tmp_path / "a.css", tmp_path / "b.css"
    a.write_text("#map { color: red }")
    b.write_text("#map { color: red }")
    assert build_site.css_token(a) == build_site.css_token(b)
    b.write_text("#map { color: blue }")
    assert build_site.css_token(a) != build_site.css_token(b)


def test_build_rejects_source_with_existing_base(tmp_path):
    src = tmp_path / "web"
    src.mkdir()
    # styles.css must exist or this raises for the wrong reason and passes vacuously.
    (src / "styles.css").write_text("#map { color: red }")
    (src / "index.html").write_text(
        '<head><base href="/"><link href="styles.css" rel="stylesheet" /></head>'
        '<body><script>const DEFAULT_BUILD = "full";</script></body>'
    )
    with pytest.raises(SystemExit):
        build_site.build(src, tmp_path / "_site")


def test_build_ignores_head_markup_quoted_below_the_head(tmp_path):
    """A COMMENT is not a tag. This shape failed a green deploy on PR #117.

    The guards above are about the <head> the injection targets, but they used
    to substring-search the whole 290KB file — where ~4,200 of 4,250 lines are
    script. A `<base ` or `</body>` mentioned in a comment or a JS string down
    there is not markup, and must not fail the build.
    """
    src = tmp_path / "web"
    src.mkdir()
    (src / "styles.css").write_text("#map { color: red }")
    (src / "index.html").write_text(
        '<head><link href="styles.css" rel="stylesheet" /></head>\n'
        '<body><script>const DEFAULT_BUILD = "full";\n'
        '// /full/ gets a <base href="../"> injected after <head> at build time\n'
        'const tpl = "</body>";\n'
        "</script></body>"
    )
    out = tmp_path / "_site"
    build_site.build(src, out)

    full = (out / "full" / "index.html").read_text()
    head, _, body = full.partition("</head>")
    # Injected into the real head, exactly once, and the prose left alone.
    assert '<base href="../" />' in head
    assert full.count('<base href="../" />') == 1
    assert '<base href="../">' in body
    # The badge goes before the document's own </body>, not the quoted one.
    assert body.index("work in progress") > body.index('const tpl = "</body>"')

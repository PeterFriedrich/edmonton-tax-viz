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


def test_build_emits_both_copies(tmp_path):
    src = tmp_path / "web"
    (src / "data").mkdir(parents=True)
    (src / "vendor").mkdir()
    (src / "data" / "x.json").write_text("{}")
    (src / "index.html").write_text(
        '<head>\n<script src="vendor/a.js"></script>\n</head>\n'
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


def test_build_rejects_source_with_existing_base(tmp_path):
    src = tmp_path / "web"
    src.mkdir()
    (src / "index.html").write_text(
        '<head><base href="/"></head><body>'
        '<script>const DEFAULT_BUILD = "full";</script></body>'
    )
    with pytest.raises(SystemExit):
        build_site.build(src, tmp_path / "_site")

"""The MIT grant must not silently swallow data that is not ours to license.

`LICENSE` carves three things out of the MIT grant: the prose (CC BY), the
open-government data, and the vendored third-party libraries. Carve-out 2 is
the one that rots. It names `data/` and `web/data/` because those are where
OGL-derived files live *today*; a fourth location arriving later is an ordinary
thing to do and nothing about adding it prompts anyone to reopen the licence.
The failure is silent and it runs the wrong way — the repo would be asserting
MIT over City of Edmonton data.

So the carve-out list is read out of `LICENSE` itself rather than restated
here. There is one source of truth: add a data directory without declaring it
and this fails; declare it and it passes.

This does NOT check the licence is the right licence, or that the OGL
attribution text is correct — `verify-about.js` pins the prescribed statement
on the live site, which is where compliance is actually owed.
"""

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# Formats that are unambiguously a data payload. `.json` is deliberately absent:
# the repo uses it for config and expectations (`expected_columns.json`) as well
# as for data, so it cannot be classified by extension alone.
DATA_SUFFIXES = {".csv", ".geojson", ".gpkg", ".shp", ".parquet", ".topojson"}

# The carve-out blocks quote their paths as an indented bare-path block.
CARVE_OUT_PATH = re.compile(r"^ {4}([A-Za-z][\w./-]*/?)\s*$", re.M)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return out.stdout.splitlines()


@pytest.fixture(scope="module")
def licence_text() -> str:
    path = ROOT / "LICENSE"
    assert path.is_file(), "LICENSE is missing — the repo is public and needs one"
    return path.read_text()


def test_docs_licence_exists():
    """Carve-out 1 points at LICENSE-docs; a dangling pointer grants nothing."""
    path = ROOT / "LICENSE-docs"
    assert path.is_file(), "LICENSE references LICENSE-docs, which does not exist"
    assert "CC BY 4.0" in path.read_text()


def test_licence_declares_the_data_directories(licence_text):
    """Guard the guard: if the path block stops parsing, the real check below
    silently passes on an empty carve-out list."""
    declared = set(CARVE_OUT_PATH.findall(licence_text))
    assert {"data/", "web/data/"} <= declared, (
        "LICENSE no longer declares the known data directories — the carve-out "
        f"block may have been reformatted. Parsed: {sorted(declared)}"
    )


def test_no_data_file_outside_the_carve_out(licence_text):
    declared = tuple(sorted(CARVE_OUT_PATH.findall(licence_text)))

    escaped = [
        f
        for f in tracked_files()
        if Path(f).suffix.lower() in DATA_SUFFIXES and not f.startswith(declared)
    ]

    assert not escaped, (
        "Data-shaped files are committed outside every path LICENSE carves out "
        "of the MIT grant, so the repo is claiming MIT over them:\n  "
        + "\n  ".join(escaped)
        + "\n\nIf these derive from open-government data, add their directory to "
        "carve-out 2 in LICENSE. If they are genuinely ours, add them to the "
        "MIT-covered list and say so here."
    )

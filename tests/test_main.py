"""Tests for the pipeline entrypoint.

main.py is glue over already-tested modules, so these tests deliberately cover
only what isn't tested elsewhere: that the canonical web-export parameters stay
pinned (the whole reason main.py exists) and that the CLI wires paths/skip flags
through correctly. The per-module logic is covered by the other test files.
"""

import sys
from pathlib import Path

# main.py lives at the repo root, not in src/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import main


def test_canonical_export_params_pinned():
    # These values are documented in docs/PERFORMANCE.md and baked into the
    # served map geometry. Changing them changes what every viewer downloads,
    # so a change here should be deliberate enough to also update this test.
    assert main.SETBACK_M == 45.0
    assert main.SIMPLIFY_TOLERANCE_M == 10.0


def test_parse_args_defaults():
    args = main.parse_args([])
    assert args.assessment_csv == main.ASSESSMENT_CSV
    assert args.boundaries_geojson == main.BOUNDARIES_GEOJSON
    assert args.png_out == main.PNG_OUT
    assert args.geojson_out == main.GEOJSON_OUT
    assert args.setback_m == main.SETBACK_M
    assert args.simplify_tolerance_m == main.SIMPLIFY_TOLERANCE_M
    assert args.skip_png is False
    assert args.skip_geojson is False


def _capture_run(monkeypatch):
    calls = {}
    monkeypatch.setattr(main, "run", lambda **kw: calls.update(kw))
    return calls


def test_skip_png_passes_none(monkeypatch):
    calls = _capture_run(monkeypatch)
    main.main(["--skip-png"])
    assert calls["png_out"] is None
    assert calls["geojson_out"] == main.GEOJSON_OUT


def test_skip_geojson_passes_none(monkeypatch):
    calls = _capture_run(monkeypatch)
    main.main(["--skip-geojson"])
    assert calls["geojson_out"] is None
    assert calls["png_out"] == main.PNG_OUT


def test_skip_property_info_passes_none(monkeypatch):
    calls = _capture_run(monkeypatch)
    main.main(["--skip-property-info"])
    assert calls["property_info_csv"] is None
    main.main([])
    assert calls["property_info_csv"] == main.PROPERTY_INFO_CSV


def test_path_overrides_flow_through(monkeypatch):
    calls = _capture_run(monkeypatch)
    main.main(["--assessment-csv", "/tmp/a.csv", "--simplify-tolerance-m", "3.5"])
    assert calls["assessment_csv"] == Path("/tmp/a.csv")
    assert calls["simplify_tolerance_m"] == 3.5

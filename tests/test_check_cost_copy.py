import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from check_cost_copy import CLAIMS, check, prose

REPO = Path(__file__).resolve().parent.parent

# Every claim is evaluated on every run, so the fixture has to be complete.
# Values are the real ones, which keeps the expected strings recognisable:
# 50 / 9.32 rounds to 5, so the words claim reads "five times".
COSTS = {
    "roadway_om_renewal": {"value": 50},
    "roadway_ops": {
        "value": 9.32,
        "components_per_km_per_year": {"maintenance": 5970, "snow_and_ice_control": 3350},
    },
    "bikeway_ops": {
        "components_per_km_per_year": {"maintenance": 178, "snow_and_ice_control": 20100},
    },
    "transit_ets": {"operating_budget_gross_annual": 436_600_000},
}
ROADS_MAINTENANCE = "$5,970"
LIFECYCLE = "$50 per metre per year"


def _check(tmp_path, body, figure):
    """Does the guard fail on `figure` specifically, given `body` as the page?

    Keyed on the expected string rather than the claim label because two rows
    are called "maintenance" — roads and bike — and a substring filter would
    silently match the wrong one.
    """
    html = tmp_path / "index.html"
    html.write_text(body, encoding="utf-8")
    costs = tmp_path / "city_unit_costs.json"
    costs.write_text(json.dumps(COSTS), encoding="utf-8")
    return [f for f in check(html, costs) if f'"{figure}"' in f]


def test_the_fixture_still_produces_the_figures_these_tests_key_on():
    # Without this, renaming a claim or changing a rate would leave every test
    # below passing vacuously — the defect class this file exists for.
    expected = {c["expect"](COSTS) for c in CLAIMS}
    assert {ROADS_MAINTENANCE, LIFECYCLE} <= expected


# ── V1: the falsification, verbatim ─────────────────────────────────────────
# docs/FINDINGS_vacuous_guards.md V1. Reproduced 2026-09-07 against the real
# file: the roads blurb reverted to the retired $1,285 and one ordinary-looking
# comment carrying $5,970 kept all 7 rates green, while the public build showed
# a rate the project had retired the day before.

FALSIFICATION = """
  <script>
      // Maintenance is $5,970 per km (2017 program basis).
      roadscost: {
        blurb: "modeled annual operating cost per acre — $1,285 per " +
               "kilometre to maintain.",
      },
  </script>
"""


def test_a_comment_does_not_satisfy_the_guard(tmp_path):
    assert _check(tmp_path, FALSIFICATION, ROADS_MAINTENANCE)


def test_an_html_comment_does_not_satisfy_the_guard(tmp_path):
    body = "<!-- maintenance is $5,970 per km --><p>$1,285 per kilometre</p>"
    assert _check(tmp_path, body, ROADS_MAINTENANCE)


def test_a_block_comment_does_not_satisfy_the_guard(tmp_path):
    body = "<script>/* maintenance is $5,970 */</script><p>$1,285</p>"
    assert _check(tmp_path, body, ROADS_MAINTENANCE)


def test_a_blurb_key_named_inside_a_comment_does_not_satisfy_the_guard(tmp_path):
    # `// ... blurb: ...` prose appears three times in the real file, so the
    # scan must not treat a commented key as a declaration.
    assert _check(tmp_path, '<script>// blurb: "$5,970 per kilometre"</script>', ROADS_MAINTENANCE)


def test_an_attribute_value_does_not_satisfy_the_guard(tmp_path):
    assert _check(tmp_path, '<p data-rate="$5,970">the rate</p>', ROADS_MAINTENANCE)


# ── The passing side: copy a reader actually sees ───────────────────────────

def test_visible_html_text_satisfies_the_guard(tmp_path):
    body = '<p id="about-modelled-roads">$5,970 per <b>kilometre</b> to maintain.</p>'
    assert not _check(tmp_path, body, ROADS_MAINTENANCE)


def test_a_blurb_literal_satisfies_the_guard(tmp_path):
    assert not _check(tmp_path, '<script>\n        blurb: "$5,970 per km",\n</script>', ROADS_MAINTENANCE)


def test_a_figure_split_across_concatenated_literals_is_found(tmp_path):
    # The lifecycle rate is written `"... $50 per metre " + "per year, ..."`,
    # so the join must be seamless or that claim goes unchecked.
    body = '<script>\n        blurb: "costs $50 per metre " +\n               "per year today",\n</script>'
    assert not _check(tmp_path, body, LIFECYCLE)


def test_a_null_blurb_is_skipped_without_swallowing_the_next_one(tmp_path):
    body = ('<script>\n        blurb: null, // denominator-driven\n'
            '        label: "Ratio",\n        blurb: "$5,970 per km",\n</script>')
    assert not _check(tmp_path, body, ROADS_MAINTENANCE)


def test_two_blurbs_abutting_do_not_manufacture_a_match(tmp_path):
    body = '<script>\n        blurb: "$5,",\n        blurb: "970 per km",\n</script>'
    assert _check(tmp_path, body, ROADS_MAINTENANCE)


# ── The real files ──────────────────────────────────────────────────────────

# Comments in web/index.html, asserted present in the raw file so that the
# absence check below cannot pass because the wording drifted.
REAL_COMMENTS = ["Strict mode rather than", "Transportation cost, OPERATING basis"]


def test_the_shipped_copy_matches_the_shipped_rates():
    assert check(REPO / "web" / "index.html", REPO / "data" / "city_unit_costs.json") == []


def test_the_real_prose_keeps_the_copy_and_drops_the_comments():
    html = (REPO / "web" / "index.html").read_text(encoding="utf-8")
    haystack = prose(html)
    assert "$5,970 per kilometre to maintain" in haystack
    assert "Both road cost layers are modelled" in haystack
    for comment in REAL_COMMENTS:
        assert comment in html, f"comment probe {comment!r} no longer in the file"
        assert comment not in haystack

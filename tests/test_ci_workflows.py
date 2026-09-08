"""Guards on CI wiring itself — membership IS the wiring, so pin the membership.

Audit 2026-08-28 F3 (`docs/FINDINGS_proxy_guards.md`): `pytest` used to exist in
exactly one place, a weekly cron, with no `pull_request` workflow and no branch
protection — so nothing measured the merged state and a green suite in a PR body
was a claim about the author's laptop. These tests fail if that state returns.
"""
import importlib
import re
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO / ".github" / "workflows"


def _load(name):
    return yaml.safe_load((WORKFLOWS / name).read_text())


def _triggers(workflow):
    """`on:` parses as the YAML 1.1 boolean True, not the string."""
    return workflow.get(True) or workflow.get("on") or {}


def _run_steps(workflow):
    return [s.get("run", "") for job in workflow["jobs"].values() for s in job["steps"]]


def test_the_merge_gate_runs_the_suite_on_pull_requests_and_master():
    """A gate that only runs on one of the two lets the other in unmeasured."""
    wf = _load("tests.yml")
    triggers = _triggers(wf)
    assert "pull_request" in triggers
    assert "master" in triggers["push"]["branches"]
    assert any("pytest" in r for r in _run_steps(wf))


def test_the_merge_gate_needs_no_secrets_or_network():
    """It must not be able to go red for reasons unrelated to the change.

    A merge gate that flakes on an upstream outage is one people learn to
    ignore, which is worse than no gate. Both commands read committed files
    only, so nothing here may reference a secret.
    """
    raw = (WORKFLOWS / "tests.yml").read_text()
    assert "secrets." not in raw


def test_the_weekly_refresh_still_runs_the_suite_itself():
    """The merge gate does NOT replace it — they gate different things.

    tests.yml gates the CHANGE. refresh.yml's own step gates the weekly DATA
    PUBLISH, running before download + regeneration so a broken suite holds the
    data path rather than corrupting it. Deleting either re-opens a hole, and
    the tempting cleanup after adding tests.yml is to drop the "duplicate".
    """
    assert any("pytest" in r for r in _run_steps(_load("refresh.yml")))


# --- every guard step, not just pytest ---------------------------------------
# docs/FINDINGS_vacuous_guards_r2.md R2. The tests above pin pytest's membership
# in two workflows — 2 of the ~14 guard steps across the three. Deleting the
# cost-copy step from the merge gate left all 800 tests green, and "membership
# IS the wiring" applies to every one of them.

def _runs(name):
    return "\n".join(_run_steps(_load(name)))


def test_the_merge_gate_runs_both_offline_guards():
    """A rate change is a code edit: refresh.yml would only catch it days later,
    on a site already serving the stale caption."""
    runs = _runs("tests.yml")
    assert "python -m pytest tests/" in runs
    assert "scripts/check_doc_citations.py" in runs
    assert "scripts/check_cost_copy.py" in runs


def test_the_weekly_refresh_runs_every_data_guard():
    """Each of these gates a different failure the refresh can publish silently;
    the list is the one refresh.yml's own step names describe."""
    runs = _runs("refresh.yml")
    for guard in (
        "scripts/check_unmatched_names.py",      # a broken join drops dollars
        "scripts/check_year_alignment.py",       # roll/rate vintage
        "scripts/check_roll_year_against_fir.py",
        "scripts/check_value_anchors.py",        # cardinality regime
        "scripts/check_served_columns.py",       # a dropped column
        "scripts/check_revenue_deltas.py",       # one hood moving hard
        "scripts/check_temporal_years.py",       # a year failing its control
        "tools/run_verified_notebooks.py",
    ):
        assert guard in runs, f"{guard} is no longer wired into refresh.yml"


def test_the_monthly_digest_runs_the_report_that_carries_the_checks():
    """`vintage_report.CHECKS` is how check_temporal_archive_year.py is wired —
    its filename appears in no workflow, which is what made an audit call it
    unwired 11 days after it shipped (FINDINGS_vacuous_guards V3, withdrawn)."""
    assert "scripts/vintage_report.py" in _runs("vintage-digest.yml")


@pytest.mark.parametrize("workflow", ["refresh.yml", "deploy.yml"])
def test_the_smoke_gate_sits_between_the_build_and_the_upload(workflow):
    """Position is the point: a red gate here leaves the live site serving the
    PREVIOUS good data instead of publishing a broken render. A smoke step that
    ran after the upload would be a report, not a gate.

    ⚠️ BOTH PUBLISHING WORKFLOWS. refresh.yml gates the DATA path; deploy.yml
    gates the CODE path — the one that changes the rendering — and had this same
    seam standing empty until 2026-09-08 (audit run 2, V3 sharpened).
    """
    steps = [s for job in _load(workflow)["jobs"].values() for s in job["steps"]]
    smoke = next(i for i, s in enumerate(steps) if "verify-smoke.js" in s.get("run", ""))
    upload = next(
        i for i, s in enumerate(steps)
        if "upload-pages-artifact" in s.get("uses", "")
    )
    assert smoke < upload, "the smoke gate must run before the artifact is uploaded"
    assert upload - smoke == 1, "a step was inserted between the gate and the upload"


@pytest.mark.parametrize("workflow", ["refresh.yml", "deploy.yml"])
def test_the_smoke_gate_covers_both_builds(workflow):
    """Both builds share one GeoJSON but not one UI, so a check run against only
    the dev server passes on full-only states the public root does not have."""
    run = next(r for r in _run_steps(_load(workflow)) if "verify-smoke.js" in r)
    assert run.count("verify-smoke.js") == 2
    assert "/full/index.html" in run


# --- the exit codes the workflow branches on ---------------------------------
# R2, one level down: refresh.yml maps the two year guards with LITERAL case
# labels while the scripts define EXIT_HOLD/EXIT_INCONCLUSIVE. Mutating
# EXIT_HOLD 3 -> 6 is green today; in CI a genuine hold would then fall through
# to `*) exit $code` — a hard failure with no banner and no hold state written,
# instead of the designed keep-last-good-plus-banner.

def _case_labels(run):
    """The numeric labels of a `case $code in ... esac` block."""
    return {int(m.group(1)) for m in re.finditer(r"^\s*(\d+)\)", run, re.M)}


@pytest.mark.parametrize("script,module", [
    ("check_year_alignment.py", "check_year_alignment"),
    ("check_roll_year_against_fir.py", "check_roll_year_against_fir"),
])
def test_the_refresh_case_labels_match_the_scripts_exit_codes(script, module):
    sys.path.insert(0, str(REPO / "scripts"))
    mod = importlib.import_module(module)
    # The two scripts name their success code differently; `or` is wrong here
    # because the value is 0.
    ok = getattr(mod, "EXIT_OK", getattr(mod, "EXIT_ALIGNED", None))
    run = next(r for r in _run_steps(_load("refresh.yml")) if script in r)
    assert _case_labels(run) == {ok, mod.EXIT_HOLD, mod.EXIT_INCONCLUSIVE}

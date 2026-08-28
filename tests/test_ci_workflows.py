"""Guards on CI wiring itself — membership IS the wiring, so pin the membership.

Audit 2026-08-28 F3 (`docs/FINDINGS_proxy_guards.md`): `pytest` used to exist in
exactly one place, a weekly cron, with no `pull_request` workflow and no branch
protection — so nothing measured the merged state and a green suite in a PR body
was a claim about the author's laptop. These tests fail if that state returns.
"""
from pathlib import Path

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

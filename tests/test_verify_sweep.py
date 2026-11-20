"""scripts/verify_sweep.py: the weekly sweep's shard split, parse and verdict.

The failure this guards is a sweep that reads green while it checked less than
it says: a shard that died, a script no shard picked up, a retry that hid a
real red, or a result line attributed to the wrong script.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import verify_sweep as vs  # noqa: E402

# The shapes verify.js prints (its results loop): status, two spaces, the name
# padded to 34, the counts, and on a red the failures indented eight spaces.
OK = "ok    verify-smoke.js                       41 checks  12s\n\n1 script(s), 41 checks — all green\n"
RED = ("FAIL  verify-smoke.js                       41 checks  12s  (2 failed, exit 1)\n"
       "        FAIL  A9 city mask drawn\n"
       "        FAIL  B2 legend reads $50k+\n"
       "\n1 script(s), 41 checks — 1 SCRIPT(S) FAILED\n")
SKIP = "skip  verify-blurbs.js                       0 checks  3s  (PARTIAL — ran 0 checks: full build)\n"


def test_shards_cover_every_script_exactly_once():
    for build in vs.BUILDS:
        scripts = vs.scripts_for(build)
        shards = [vs.shard_of(scripts, i, vs.SHARDS) for i in range(vs.SHARDS)]
        flat = [s for sh in shards for s in sh]
        assert sorted(flat) == scripts, build
        assert len(flat) == len(set(flat)), build


def test_exclusions_match_the_plan():
    public, full = vs.scripts_for("public"), vs.scripts_for("full")
    assert "verify-url-state.js" not in public + full
    assert "verify-theme.js" in public and "verify-theme.js" not in full
    assert "verify-blurbs.js" in public and "verify-blurbs.js" not in full
    assert "verify-smoke.js" in public and "verify-smoke.js" in full


def test_parse_reads_status_and_failures():
    assert vs.parse(OK, "verify-smoke.js") == ("ok", [])
    status, detail = vs.parse(RED, "verify-smoke.js")
    assert status == "red"
    assert detail == ["FAIL  A9 city mask drawn", "FAIL  B2 legend reads $50k+"]
    assert vs.parse(SKIP, "verify-blurbs.js")[0] == "skip"


def test_parse_never_credits_another_scripts_green():
    status, detail = vs.parse(OK, "verify-theme.js")
    assert status == "red"
    assert "no result line" in detail[0]


def test_parse_of_a_crash_is_red():
    status, _ = vs.parse("--serve failed: http.server exited early (code 1)\n", "verify-smoke.js")
    assert status == "red"


def test_a_retry_that_stays_red_is_red_not_flaky():
    red, ok = {"status": "red"}, {"status": "ok"}
    assert vs.final_status([red, red]) == "red"
    assert vs.final_status([red, ok]) == "flaky"
    assert vs.final_status([ok]) == "ok"


def _write(tmp_path, rows):
    (tmp_path / "r.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return vs.load(tmp_path)


def _all(status="ok"):
    return [{"build": b, "script": s, "status": status,
             "attempts": [{"status": status, "secs": 1, "detail": []}]}
            for b in vs.BUILDS for s in vs.scripts_for(b)]


def test_every_script_ok_is_green(tmp_path):
    kind, title, missing, reds, flaky, total = vs.summarise(_write(tmp_path, _all()))
    assert (kind, missing, reds, flaky) == ("green", [], [], [])
    assert str(total) in title


def test_one_missing_result_is_broken_even_when_the_rest_are_green(tmp_path):
    rows = _all()[1:]
    kind, title, missing, *_ = vs.summarise(_write(tmp_path, rows))
    assert kind == "broken"
    assert len(missing) == 1
    assert title.startswith("⚠️ Verify sweep could not run")


def test_no_results_at_all_is_broken(tmp_path):
    kind, *_ = vs.summarise(vs.load(tmp_path))
    assert kind == "broken"


def test_one_red_outranks_flaky(tmp_path):
    rows = _all()
    rows[0]["status"] = "red"
    rows[1]["status"] = "flaky"
    kind, title, _, reds, flaky, _ = vs.summarise(_write(tmp_path, rows))
    assert kind == "red" and len(reds) == 1 and len(flaky) == 1
    assert title == "⚠️ Verify sweep — 1 red, 1 flaky"


def test_flaky_only(tmp_path):
    rows = _all()
    rows[2]["status"] = "flaky"
    kind, *_ = vs.summarise(_write(tmp_path, rows))
    assert kind == "flaky"


def test_body_names_the_red_script_its_build_and_hint(tmp_path):
    rows = _all()
    r = next(x for x in rows if x["script"] == "verify-services-panel.js" and x["build"] == "full")
    r["status"] = "red"
    r["attempts"] = [{"status": "red", "secs": 1, "detail": ["FAIL  the floor fires | got 0"]}] * 2
    kind, _, missing, reds, flaky, total = vs.summarise(_write(tmp_path, rows))
    text = vs.body(kind, missing, reds, flaky, total, "https://x/run/1", "abcdef1234")
    assert "| full | `verify-services-panel.js` | data shape" in text
    assert "the floor fires \\| got 0" in text
    assert "`abcdef1`" in text

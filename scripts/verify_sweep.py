"""The weekly verify sweep on GitHub Actions (`.github/workflows/verify-sweep.yml`).

Two subcommands, one per job:

    run     one matrix shard: every verify script whose index in the sorted list
            is `shard` mod `of`, each through `tools/profiling/verify.js --serve`
            on its own, retried once when red. Writes one JSON line per script.
    report  reads every shard's lines, compares them with the scripts that should
            have run, and writes the issue title and body.

Why it exists: the full sweep's job is drift detection (`docs/FINDINGS_verify_
selection.md` §4). Its stale reds come from refreshes and copy merges whatever
the PR is, and before this they sat unnoticed for days because nothing ran it.

Statuses, worst first: `missing` (no result: a shard died, or the matrix and
`--of` disagree), `red` (red twice), `flaky` (red, then green alone), `ok`,
`skip` (verify.js's own skip, e.g. a deliberate refusal).

⚠️ The parse reads verify.js's result line. If verify.js changes that format,
every script reads as "no result line" and the sweep goes red everywhere. That
is the loud direction on purpose: a format change can never read as green.

Stdlib only, so the runner's system python3 is enough.

    python3 scripts/verify_sweep.py run --build public --shard 0 --of 8 --site _site --out r.jsonl
    python3 scripts/verify_sweep.py report --results results --body report.md
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILING = ROOT / "tools" / "profiling"
SHARDS = 8
TIMEOUT_S = 900

BUILDS = {"public": "index.html", "full": "dev-build-full/index.html"}
# url-state is a required check on every web/ PR already (tests.yml). theme
# checks BOTH builds from the site root, so it runs once, under public. blurbs
# refuses the full build by design (deploy.yml runs it on public).
EXCLUDE = {
    "public": {"verify-url-state.js"},
    "full": {"verify-url-state.js", "verify-theme.js", "verify-blurbs.js"},
}

# What a red has meant before (FINDINGS_verify_selection §1, §4b). A hint, not
# a verdict: every red still gets reproduced on a built tree.
HINTS = {
    "verify-services-panel.js": "data shape: a floor that stopped firing is a prompt to re-measure, maybe a real data change",
    "verify-deviation.js": "data shape: the inverted / zero-crossing bands or the surplus arm moved; re-measure",
    "verify-about.js": "external host: a link target answered 404/410",
    "verify-loading-overlay.js": "runner timing: the 250 / 8000 / 40 ms bounds are calibrated for the runner",
}
DEFAULT_HINT = "stale expectation or real page bug: reproduce on a built tree"

RESULT = re.compile(r"^(FAIL|skip|ok  )  (verify-\S+\.js) ")
STATUS = {"FAIL": "red", "skip": "skip", "ok  ": "ok"}


def scripts_for(build):
    names = sorted(p.name for p in PROFILING.glob("verify-*.js"))
    return [n for n in names if n not in EXCLUDE[build]]


def shard_of(scripts, shard, of):
    return [s for i, s in enumerate(scripts) if i % of == shard]


def parse(output, script):
    """(status, detail lines) for `script` from one verify.js run's output."""
    lines = output.splitlines()
    for i, line in enumerate(lines):
        m = RESULT.match(line)
        if not m or m.group(2) != script:
            continue
        detail = []
        for nxt in lines[i + 1:]:
            if not nxt.startswith("        "):
                break
            detail.append(nxt.strip())
        return STATUS[m.group(1)], detail
    tail = [l for l in lines if l.strip()][-6:]
    return "red", ["verify.js gave no result line for this script"] + tail


def run_once(build, script, site):
    cmd = ["node", str(PROFILING / "verify.js"), "--serve", site,
           "--page", BUILDS[build], "--jobs", "1", script]
    started = time.time()
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=TIMEOUT_S)
        out = p.stdout + p.stderr
        print(out, flush=True)
        status, detail = parse(out, script)
    except subprocess.TimeoutExpired:
        status, detail = "red", [f"timed out after {TIMEOUT_S} s"]
    return {"status": status, "secs": round(time.time() - started), "detail": detail}


def final_status(attempts):
    if attempts[0]["status"] != "red":
        return attempts[0]["status"]
    return "red" if attempts[-1]["status"] == "red" else "flaky"


def cmd_run(a):
    scripts = shard_of(scripts_for(a.build), a.shard, a.of)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    reds = 0
    with open(a.out, "w") as f:
        for script in scripts:
            attempts = [run_once(a.build, script, a.site)]
            if attempts[0]["status"] == "red":
                print(f"--- {script} red; re-running once ---", flush=True)
                attempts.append(run_once(a.build, script, a.site))
            status = final_status(attempts)
            reds += status == "red"
            f.write(json.dumps({"build": a.build, "script": script,
                                "status": status, "attempts": attempts}) + "\n")
            f.flush()
    print(f"{len(scripts)} script(s) in {a.build} shard {a.shard}/{a.of}, {reds} red")
    return 1 if reds else 0


def load(results_dir):
    got = {}
    for p in sorted(Path(results_dir).glob("**/*.jsonl")):
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                got[(r["build"], r["script"])] = r
    return got


def summarise(got):
    """kind, title and the counts behind them."""
    expected = {(b, s) for b in BUILDS for s in scripts_for(b)}
    missing = sorted(expected - got.keys())
    rows = [got[k] for k in sorted(expected & got.keys())]
    reds = [r for r in rows if r["status"] == "red"]
    flaky = [r for r in rows if r["status"] == "flaky"]
    total = len(expected)
    if missing:
        kind = "broken"
        title = f"⚠️ Verify sweep could not run — {len(missing)} of {total} scripts have no result"
    elif reds:
        kind = "red"
        title = f"⚠️ Verify sweep — {len(reds)} red" + (f", {len(flaky)} flaky" if flaky else "")
    elif flaky:
        kind = "flaky"
        title = f"Verify sweep — {len(flaky)} flaky, none red"
    else:
        kind = "green"
        title = f"Verify sweep — all {total} green"
    return kind, title, missing, reds, flaky, total


def body(kind, missing, reds, flaky, total, run_url, sha):
    out = [f"Weekly verify sweep on `{sha[:7]}`: {total} script runs over both builds. "
           f"[Run log]({run_url}). Triage: `docs/RUNBOOK.md` §0g.", ""]
    if missing:
        out += ["## No result (the sweep itself broke)", "",
                "A shard died in setup, or the matrix and `--of` disagree. "
                "Nothing below covers these scripts.", ""]
        out += [f"- `{b}` `{s}`" for b, s in missing] + [""]
    if reds:
        out += ["## Red twice", "", "| Build | Script | Hint | First failures |", "|---|---|---|---|"]
        for r in reds:
            fails = "<br>".join(d.replace("|", "\\|") for d in r["attempts"][-1]["detail"][:5])
            out.append(f"| {r['build']} | `{r['script']}` | {HINTS.get(r['script'], DEFAULT_HINT)} | {fails} |")
        out.append("")
    if flaky:
        out += ["## Flaky (red, then green alone)", ""]
        for r in flaky:
            first = r["attempts"][0]["detail"][:1]
            out.append(f"- `{r['build']}` `{r['script']}`" + (f": {first[0]}" if first else ""))
        out.append("")
    if kind == "green":
        out += ["Every script green on both builds.", ""]
    out += ["Reproduce one: `python3 scripts/build_site.py --src web --out <dir>`, then "
            "`node tools/profiling/verify.js --serve <dir> [--page dev-build-full/index.html] --jobs 1 <script>`."]
    return "\n".join(out) + "\n"


def cmd_report(a):
    kind, title, missing, reds, flaky, total = summarise(load(a.results))
    run_url = "{}/{}/actions/runs/{}".format(
        os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
        os.environ.get("GITHUB_REPOSITORY", "?"), os.environ.get("GITHUB_RUN_ID", "?"))
    sha = os.environ.get("GITHUB_SHA") or subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    Path(a.body).write_text(body(kind, missing, reds, flaky, total, run_url, sha or "unknown"))
    if a.github_output:
        with open(a.github_output, "a") as f:
            f.write(f"kind={kind}\ntitle={title}\n")
    print(kind, title)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--build", choices=BUILDS, required=True)
    r.add_argument("--shard", type=int, required=True)
    r.add_argument("--of", type=int, default=SHARDS)
    r.add_argument("--site", required=True)
    r.add_argument("--out", required=True)
    p = sub.add_parser("report")
    p.add_argument("--results", required=True)
    p.add_argument("--body", required=True)
    p.add_argument("--github-output")
    a = ap.parse_args(argv)
    return cmd_run(a) if a.cmd == "run" else cmd_report(a)


if __name__ == "__main__":
    sys.exit(main())

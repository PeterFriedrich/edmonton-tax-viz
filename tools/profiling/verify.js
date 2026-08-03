// Quiet runner for the verify suite.
//
// Why a RUNNER rather than a --quiet flag in each script: the verify scripts
// (31 as of 2026-08-03, auto-discovered below) all work and all differ slightly
// in how they print. Editing every one of them to add a flag is one chance per
// script to break a passing test to save output. This wraps them instead —
// nothing existing changes, and a gate run goes from ~120 lines of PASS to one
// line per script.
//
// Classification does NOT trust the "ALL CHECKS PASSED" banner (five scripts
// never print it — RUNBOOK quirk (u)). It counts /^FAIL/ lines and the exit
// code, and reports either.
//
//   node tools/profiling/verify.js <url>                  # every script
//   node tools/profiling/verify.js <url> change temporal  # substring filter
//   node tools/profiling/verify.js <url> --jobs 3         # force concurrency
//   node tools/profiling/verify.js <url> -v               # show PASS lines too
//
// ⚠️ The whole suite exceeds the 10-minute Bash cap (quirk (t)). Filter, or
// raise the caller's timeout — this runner does not shorten the work, only the
// output.
const { spawn } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");

const args = process.argv.slice(2);
const verbose = args.includes("-v") || args.includes("--verbose");
const jobsIx = args.indexOf("--jobs");

// ⚠️ THE DEFAULT IS DERIVED FROM CORE COUNT, AND IT USED TO BE A HARDCODED 3
// THAT THIS BOX CANNOT SUPPORT. Measured 2026-08-03 on the 4-core Oracle ARM
// box: ONE verify script draws ~275% CPU — 2.75 of 4 cores — because the
// scripts run headless Chromium on SwiftShader, where all rasterisation and
// every deck.gl picking-buffer readback is software. So 3-up demanded ~8 cores
// from 4: measured cpu_sum 385-400% (every core pegged) and load average 8.2.
//
// What that cost, on the same three scripts:
//   --jobs 3  ~509s wall, 2 of 3 FAILED
//   --jobs 2  ~505s wall, 1 of 3 FAILED
//   --jobs 1   615s wall, ALL GREEN
//
// ⚠️ Parallelism was buying ~17% of wall time in exchange for determinism —
// a bad trade, and worse than it looks: a real regression is indistinguishable
// from the contention flake, so a red batch had to be re-run alone before it
// meant anything (quirk (mmm)). The scripts had already accreted workarounds
// for this in their own code (see verify-peek.js's picking-buffer re-send,
// which names "the 3-up runner" explicitly) — the runner default was the cause
// nobody went back to. The wall time is dominated by ONE script regardless:
// verify-peek spends ~437s of the 615s software-picking a pixel grid.
//
// Divisor is 3, not 2.75, so the estimate stays conservative on a box whose
// cores are slower than this one's. `--jobs N` still forces any value.
const jobs = jobsIx >= 0
  ? Math.max(1, parseInt(args[jobsIx + 1], 10) || 1)
  : Math.max(1, Math.floor((os.cpus().length || 1) / 3));
const rest = args.filter((a, i) =>
  !a.startsWith("-") && !(jobsIx >= 0 && i === jobsIx + 1));
const url = rest[0];
const filters = rest.slice(1);

if (!url) {
  console.error("usage: node tools/profiling/verify.js <url> [name-filter...]");
  process.exit(2);
}

const dir = __dirname;
const scripts = fs.readdirSync(dir)
  .filter(f => /^verify-.*\.js$/.test(f))
  .filter(f => !filters.length || filters.some(s => f.includes(s)))
  .sort();

if (!scripts.length) {
  console.error("no verify scripts matched: " + filters.join(", "));
  process.exit(2);
}

const run = script => new Promise(resolve => {
  const started = Date.now();
  const p = spawn("node", [path.join(dir, script), url], { cwd: path.join(dir, "..", "..") });
  let out = "";
  p.stdout.on("data", d => { out += d; });
  p.stderr.on("data", d => { out += d; });
  p.on("close", code => {
    const lines = out.split("\n");
    const fails = lines.filter(l => /^FAIL/.test(l));
    const passes = lines.filter(l => /^PASS/.test(l));
    // A script that crashed before printing anything is a failure even with no
    // FAIL lines — exit code is the backstop, not the banner.
    const bad = fails.length > 0 || code !== 0;
    resolve({ script, bad, fails, passes, code, out,
              secs: ((Date.now() - started) / 1000).toFixed(0) });
  });
});

(async () => {
  const results = [];
  const queue = scripts.slice();
  const workers = Array.from({ length: Math.min(jobs, queue.length) }, async () => {
    while (queue.length) results.push(await run(queue.shift()));
  });
  await Promise.all(workers);
  results.sort((a, b) => a.script.localeCompare(b.script));

  for (const r of results) {
    const n = r.passes.length + r.fails.length;
    console.log(`${r.bad ? "FAIL" : "ok  "}  ${r.script.padEnd(34)} ` +
                `${String(n).padStart(3)} checks  ${r.secs}s` +
                (r.bad ? `  (${r.fails.length} failed, exit ${r.code})` : ""));
    if (r.bad) {
      // Show the failures themselves — the whole point of running it.
      for (const f of r.fails) console.log("        " + f);
      if (!r.fails.length) console.log("        " + r.out.trim().split("\n").slice(-6).join("\n        "));
    }
    if (verbose) for (const p of r.passes) console.log("        " + p);
  }

  const bad = results.filter(r => r.bad);
  const checks = results.reduce((a, r) => a + r.passes.length + r.fails.length, 0);
  console.log(`\n${results.length} script(s), ${checks} checks — ` +
              (bad.length ? `${bad.length} SCRIPT(S) FAILED` : "all green"));
  process.exit(bad.length ? 1 : 0);
})();

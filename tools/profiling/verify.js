// Quiet runner for the verify suite.
//
// Why a RUNNER rather than a --quiet flag in each script: the verify scripts
// (32 as of 2026-08-03, auto-discovered below) all work and all differ slightly
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
//   node tools/profiling/verify.js --serve web smoke      # serve a root itself
//   node tools/profiling/verify.js --serve /tmp/_site --page dev-build-full/index.html
//
// --serve <root> replaces <url>: it starts http.server on a free port, refuses
// to run unless the served page is byte-identical to the file on disk, and
// kills the server by its own pid on the way out. It exists because the
// by-hand version (start, find the port, check the root, kill) was 324 calls
// in 60 sessions, and its kill step was usually `pkill -f`, which matches its
// own shell (docs/FINDINGS_dev_velocity.md §7).
//
// ⚠️ The whole suite exceeds the 10-minute Bash cap (quirk (t)). Filter, or
// raise the caller's timeout — this runner does not shorten the work, only the
// output.
const { spawn } = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");

const args = process.argv.slice(2);
const verbose = args.includes("-v") || args.includes("--verbose");
const jobsIx = args.indexOf("--jobs");
const serveIx = args.indexOf("--serve");
const pageIx = args.indexOf("--page");

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
// nobody went back to. The wall time was dominated by ONE script regardless:
// verify-peek spent ~437s of the 615s software-picking a pixel grid, until its
// empty-pixel scan was derived from geometry instead on 2026-08-04 (437s → 94s).
//
// Divisor is 3, not 2.75, so the estimate stays conservative on a box whose
// cores are slower than this one's. `--jobs N` still forces any value.
const jobs = jobsIx >= 0
  ? Math.max(1, parseInt(args[jobsIx + 1], 10) || 1)
  : Math.max(1, Math.floor((os.cpus().length || 1) / 3));
const valueOf = ix => (ix >= 0 ? args[ix + 1] : undefined);
const rest = args.filter((a, i) =>
  !a.startsWith("-") && ![jobsIx, serveIx, pageIx].some(ix => ix >= 0 && i === ix + 1));
const serveRoot = valueOf(serveIx);
const page = valueOf(pageIx) || "index.html";
let url = serveIx >= 0 ? undefined : rest[0];
const filters = serveIx >= 0 ? rest : rest.slice(1);

if (serveIx >= 0 ? !serveRoot || serveRoot.startsWith("-") : !url) {
  console.error("usage: node tools/profiling/verify.js <url> [name-filter...]\n" +
                "       node tools/profiling/verify.js --serve <root> [--page <path>] [name-filter...]");
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

// fast-teardown.js gives each page its own browser process and kills it on
// close — graceful close was deferring GPU teardown into the next page (31% of
// the suite). Appended, so a caller's own NODE_OPTIONS survive.
const env = { ...process.env, NODE_OPTIONS:
  `${process.env.NODE_OPTIONS || ""} --require ${path.join(dir, "fast-teardown.js")}`.trim() };

const run = script => new Promise(resolve => {
  const started = Date.now();
  const p = spawn("node", [path.join(dir, script), url], { cwd: path.join(dir, "..", ".."), env });
  let out = "";
  p.stdout.on("data", d => { out += d; });
  p.stderr.on("data", d => { out += d; });
  p.on("close", code => {
    const lines = out.split("\n");
    const fails = lines.filter(l => /^FAIL/.test(l));
    // `ok  ` is verify-url-state, -glass-cell and -grid-loading's pass line;
    // without it they read "0 checks" when green.
    const passes = lines.filter(l => /^(PASS|ok  )/.test(l));
    // verify-blurbs refuses the full build with a FAIL on purpose, because on
    // the deploy gate a refusal must be red. Here it was a red on every
    // full-build sweep. Reporting it as a skip is safe: deploy.yml calls the
    // script directly, never through this runner.
    const skipped = fails.length === 1 && /^FAIL\s+PARTIAL — ran 0 checks:/.test(fails[0]);
    // A script that crashed before printing anything is a failure even with no
    // FAIL lines — exit code is the backstop, not the banner.
    const bad = !skipped && (fails.length > 0 || code !== 0);
    resolve({ script, bad, skipped, fails, passes, code, out,
              secs: ((Date.now() - started) / 1000).toFixed(0) });
  });
});

const md5 = buf => crypto.createHash("md5").update(buf).digest("hex");

// Resolves to the page URL once the server answers with the file on disk.
// The md5 comparison is the point: a server that failed to bind leaves an
// OLDER one answering from another directory, and every check then passes or
// fails against the wrong tree. Port 0 makes that collision impossible here,
// and the comparison is what proves it.
const serve = () => new Promise((resolve, reject) => {
  const root = path.resolve(serveRoot);
  const file = path.join(root, page);
  if (!fs.existsSync(file)) return reject(new Error(`${file} does not exist`));
  // System python3 on the Oracle box is 3.6, whose http.server wedges under
  // these scripts; the project venv is used when there is one.
  const venv = path.join(dir, "..", "..", ".venv", "bin", "python");
  const server = spawn(fs.existsSync(venv) ? venv : "python3",
    ["-u", "-m", "http.server", "0", "--bind", "127.0.0.1", "--directory", root],
    { stdio: ["ignore", "pipe", "pipe"] });
  process.on("exit", () => server.kill());
  for (const sig of ["SIGINT", "SIGTERM"]) process.on(sig, () => process.exit(130));
  let banner = "";
  const timer = setTimeout(() => reject(new Error("http.server printed no port within 15s: " + banner)), 15000);
  server.on("exit", code => reject(new Error(`http.server exited early (code ${code}): ${banner}`)));
  const onData = async d => {
    banner += d;
    const m = banner.match(/port (\d+)/);
    if (!m) return;
    server.stdout.off("data", onData);
    clearTimeout(timer);
    const pageUrl = `http://127.0.0.1:${m[1]}/${page}`;
    try {
      const served = Buffer.from(await (await fetch(pageUrl)).arrayBuffer());
      if (md5(served) !== md5(fs.readFileSync(file))) {
        return reject(new Error(`${pageUrl} is not serving ${file} (md5 differs)`));
      }
      console.log(`serving ${root} at ${pageUrl} (pid ${server.pid}, md5 matches disk)`);
      resolve(pageUrl);
    } catch (e) { reject(e); }
  };
  server.stdout.on("data", onData);
  server.stderr.on("data", d => { banner += d; });
});

(async () => {
  if (serveIx >= 0) {
    try { url = await serve(); }
    catch (e) { console.error("--serve failed: " + e.message); process.exit(2); }
  }
  const results = [];
  const queue = scripts.slice();
  const workers = Array.from({ length: Math.min(jobs, queue.length) }, async () => {
    while (queue.length) results.push(await run(queue.shift()));
  });
  await Promise.all(workers);
  results.sort((a, b) => a.script.localeCompare(b.script));

  for (const r of results) {
    const n = r.skipped ? 0 : r.passes.length + r.fails.length;
    console.log(`${r.bad ? "FAIL" : r.skipped ? "skip" : "ok  "}  ${r.script.padEnd(34)} ` +
                `${String(n).padStart(3)} checks  ${r.secs}s` +
                (r.bad ? `  (${r.fails.length} failed, exit ${r.code})` : "") +
                (r.skipped ? `  (${r.fails[0].replace(/^FAIL\s+/, "")})` : ""));
    if (r.bad) {
      // Show the failures themselves — the whole point of running it.
      for (const f of r.fails) console.log("        " + f);
      if (!r.fails.length) console.log("        " + r.out.trim().split("\n").slice(-6).join("\n        "));
    }
    if (verbose) for (const p of r.passes) console.log("        " + p);
  }

  const bad = results.filter(r => r.bad);
  const skips = results.filter(r => r.skipped).length;
  const checks = results.reduce((a, r) => a + (r.skipped ? 0 : r.passes.length + r.fails.length), 0);
  console.log(`\n${results.length} script(s), ${checks} checks — ` +
              (bad.length ? `${bad.length} SCRIPT(S) FAILED` : "all green") +
              (skips ? `, ${skips} skipped` : ""));
  process.exit(bad.length ? 1 : 0);
})();

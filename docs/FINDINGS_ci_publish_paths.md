# Findings — the CI behaviour changes, audited from their live runs (queue item 7)

**Run:** 2026-10-05, S215, Opus 5.5, `xhigh`. ⚠️ Same model family as the
builders (#521, #523, #569, #578 were all Opus 5.5).
**Target:** `docs/AUDIT_LEDGER.md` queue item 7: #521 (`/dev-build-full/` move +
`build_site.py`), #523 (`refresh.yml` rebase-and-retry), and the two gates the
item later absorbed, #569 (`verify-blurbs.js` gates `deploy.yml`) and #578
(verified notebooks gate `refresh.yml`). The brief said to audit the log, not
the YAML alone.
**Instrument:** `edmonton-audit` decision stack. Logs of refresh runs
35634413769 (2026-09-21 dispatch), 36451039239 (2026-09-28 schedule) and
37343456450 (2026-10-05, red). Deploy run 37140648807. The last 100 `deploy.yml`
runs (back to 2026-08-16) and 60 `refresh.yml` runs, intersected by time. Live
HTTP status of the served paths. GitHub's concurrency documentation and the
`actions/checkout` README, read from the source pages.

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Should each behaviour exist? | **SOUND** for all four. Each answers a measured failure (DECISIONS 2026-09-21 ×2, 2026-09-24 ×2). |
| L1 | Did each work in its first live runs? | **SOUND** for #521, #569, #578. **CONDITIONAL** for #523: never exercised in production. |
| L2 | Do the two publish paths interact safely? | **WARN.** Two latent ordering defects, F1 and F2. Neither has fired. |

### L1 evidence

- **#521:** live `/full/` returns **404** and `/dev-build-full/` returns
  **200** (2026-10-05). Both successful refreshes since the move ran
  `verify-smoke.js` against `/dev-build-full/index.html`, and every check passed.
- **#569:** deploy 37140648807 (2026-10-03) ran `rules: 150 states … PASS
  (longest 398 chars)` and `wiring: … 23 changes` PASS. All 100 deploys since
  2026-08-16 are green.
- **#578:** the 2026-09-28 refresh printed `3/3 notebooks executed cleanly`.
  The data commit `eed5555` carries `web/verified/0{1,2,3}_*.html`, and
  `/verified/02_methods.html` serves 200. `04_roads_lens` (#607) merged 81 minutes
  after that run; its first scheduled run was today's, which died earlier, at
  regen (queue item 16 stays open).
- **#523:** neither successful run since 2026-09-21 logged
  `push rejected`. Both pushed first time (`b4d9464..9d46704`,
  `96c1429..eed5555`, `Bypassed rule violations` as expected). The retry path
  is proven only by the five throwaway-repo scenarios recorded in DECISIONS
  2026-09-21. That is good evidence, and it is still not a production run.

## F1 — a code deploy queued behind a refresh republishes LAST WEEK's data

**Mechanism (documented behaviour, unreproduced here):**
1. A `web/**` PR merges while `refresh.yml` is between its checkout and its
   push (~8–10 min). `deploy.yml` fires for that commit, call it S, and waits
   in the shared `refresh-map-data` group.
2. The refresh pushes its data commit D on top of S, rebasing if needed (#523
   makes this path succeed where it used to fail). It deploys new data.
3. The pending deploy then runs. `deploy.yml`'s checkout has no `ref:`, and
   `actions/checkout` *"defaults to the reference or SHA for that event"* — S,
   which does not contain D. It builds `_site` from S's `web/data` and
   `web/verified` and **deploys last week's data over this week's.**
4. Nothing repairs it until the next `web/**` push or the next Monday. D
   touches only excluded paths, so it never triggers a deploy of its own.

**What reaches the public:** last week's numbers, with last week's `status.json`.
So the page stays internally consistent and is just a week stale. The
`Big revenue delta` issue would describe data the site is not showing. Git is
correct throughout; only Pages regresses.

**Why it isn't covered:** DECISIONS 2026-07-22 says the shared group means
*"code + data deploys never race"*. The group stops them deploying **at once**;
it does nothing about **order**, and queueing is what lets the stale one go
last. #523 made the precondition more reachable: before it, a merge landing
mid-refresh killed the refresh instead.

**Exposure:** 0 of the last 100 deploys overlapped a refresh. The window is the
checkout→push span of one run a week, and the scheduled run now fires at
14:00–17:00 UTC (O1), 08:00–11:00 in Edmonton. Manual dispatches, which
DECISIONS 2026-09-21 calls *"usually run while someone is actively merging"*,
are the likely trigger.

**✅ Built 2026-10-05 (S216).** **Remedy (CI change → Peter):** `deploy.yml`'s checkout gets `ref: master`,
so a deploy publishes the branch tip as it is when the run starts, not as it was
at trigger time. A later deploy then never carries older data than an earlier
one. Plus a `test_ci_workflows.py` assertion on that line.

## F2 — a pending refresh can be CANCELLED by a later code push

GitHub: *"By default, any existing `pending` job or workflow in the same
concurrency group will be canceled and the new queued job or workflow will take
its place"*. `queue: single` is the default, and neither workflow sets `queue`.

**Scenario:** a deploy is running (~2 min) when the cron fires, so the refresh
is pending. A second `web/**` push lands, and its deploy **replaces the pending
refresh.** A scheduled run is not retried, so that week's refresh and heartbeat
are lost silently. Two lost weeks in a row raise the staleness banner.
`deploy.yml`'s comment (*"queue behind an in-flight refresh rather than aborting
it"*) describes only the in-progress case.

**Exposure:** smaller than F1's, because it needs two pushes inside one ~2-minute
deploy at the moment the cron fires. Never observed: the one `cancelled`
refresh on record (2026-07-13) ran 30 min 20 s, which is a `timeout-minutes: 30`
kill, not a replacement.

**✅ Built 2026-10-05 (S216).** **Remedy (CI change → Peter):** `queue: max` on both workflows' `concurrency`
blocks. This is documented, and it is compatible with `cancel-in-progress: false`
(only the `true` combination is rejected).

## Observations (not findings)

- **O1 — the "Monday 08:00 UTC" cron has fired 6–9 hours late since
  September.** Trigger times: 07-06 12:03, 08-17 08:39, 09-07 13:57, 09-21 14:49,
  09-28 16:26, 10-05 16:46. Today's late firing is why the run read the City's
  15:00 UTC GTFS reload at all (`DATA_ISSUES.md` §8). A run before 14:58 UTC would have
  read the previous load, which the 09-28 run read without error. No action: the cron comment already says
  "best-effort". The workflow comment's *Monday 08:00* is just no longer what
  happens.
- **O2 — a 0-row download passes `download_data.py`.** The count guard
  compares local rows to the server's `count(*)`, and 0 = 0. Today the transit
  loader caught it. Whether every other loader fails loud on an empty source,
  rather than publishing a zero lens, is unmeasured → new queue item 18.

## What this run got wrong

- **I wrote an unverified counterfactual into `DATA_ISSUES.md` §8 an hour before
  this audit, and published it.** It said that without the guard *"every service
  weighs 0 and the transit lens would read zero everywhere"*. I never ran it. The
  code shows only that with no weekday dates `n_weekday_dates` is 0, so the mean
  has no denominator. What it would then publish (zeros, NaN or an error) is
  still unrun, and the corrected sentence (this PR) claims no more than that. It is the confident-negative shape the skill
  warns about, in an upstream-facing document.
- **My first framing of F1, while working, said the exposure window was the whole refresh job.**
  Only checkout→push counts. A code push after the data commit lands produces a
  deploy whose SHA contains that commit, so it is harmless. That makes the
  window about 8–10 min, not 12.
- **F1 and F2 are mechanism findings with no reproduction.** Both rest on
  documented GitHub behaviour plus the YAML, and the run history shows 0
  occurrences. A real race on a throwaway repo was not staged. If GitHub's
  checkout resolved `github.sha` to the branch tip at run time, F1 would be
  wrong, and the README sentence quoted above is the whole basis for saying it
  does not.

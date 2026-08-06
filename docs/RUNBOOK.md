# Runbook — live-site operations

What to do when the unattended pipeline needs a human. Distinct from
`docs/SPEC_deployment.md` (how the automation is designed): this is the
checklist you open when the weekly run fails, the site shows a banner, or a
new year rolls.

**What runs unattended:** `.github/workflows/refresh.yml`, Mondays 08:00 UTC
(+ manual `workflow_dispatch`): tests → download → unmatched-name check →
year-alignment check → `main.py --skip-png` → commit `web/data/` → deploy
`web/` to Pages.
**Failure is safe by default** — any failed run leaves the site serving the
last committed data. Nothing here is ever a same-day emergency.

**Two deploy paths (don't confuse them):** `refresh.yml` is the DATA path above.
`.github/workflows/deploy.yml` is the CODE path — it fires on any push to
`master` that touches site code (`web/**`, minus `web/data/**`) and just
re-uploads the committed `web/` tree to Pages (no download, no regen; ~seconds).
So a UI/button edit ships on push; a data change ships on the weekly run. Both
share the `refresh-map-data` concurrency group, so they never deploy at once.
If a code push didn't update the site, first check the deploy.yml run (not
refresh.yml); if only data is stale, that's refresh.yml.

- Live site: https://peterfriedrich.github.io/edmonton-tax-viz/
- Runs: https://github.com/PeterFriedrich/edmonton-tax-viz/actions
- What's being served right now: `web/data/status.json` (`data_year`,
  `generated`, `banner`, GeoJSON SHA-256)

---

## 1. The January year roll (the recurring one)

**Symptom:** the site shows a "Showing 2025 data —…" banner, and the weekly
run logs `::warning::YEAR MISMATCH — holding window`. This is the designed
hold state (`scripts/check_year_alignment.py` exit 3): Edmonton rolled the
assessment feed to the new year and CI is refusing to apply stale mill rates.
The site keeps serving last year's data and is fully functional — take your
time.

**Checklist (in order):**

1. **Wait for the City to publish the new year's municipal mill rates**
   (`pwis-wc4c`) — typically spring, after the budget. The hold can last
   months by design.
   - ⚠️ **That ordering is NOT guaranteed, and for 2026 it inverted:** the City
     published 2026 rates on **2026-04-29**, months *before* the 2026 roll.
     **Check `data/mill_rates.json` before assuming you have to wait** —
     **2026 is already pre-staged there** (added 2026-08-06, every published
     value verified against the live API), so the 2027-January roll should be a
     same-day clear, not a months-long banner. Pre-staging is safe: rates are
     year-keyed and nothing reads a year that isn't pinned.
2. **Add the new year's block to `data/mill_rates.json`** — a manual,
   *reviewed* step (deliberately never auto-fetched; see DATA.md §4 for the
   vocabulary bridge and known quirks). **Skip if already pre-staged** — just
   re-verify the block against the live source before relying on it.
   - ⚠️ **Since 2026-08-01 this file is also what the site DISPLAYS.**
     `generate_status.py` copies the year's municipal rates into
     `status.json` → the mill-rate pod. Two consequences: the three display
     classes (`DISPLAY_RATE_CLASSES`) must all be present or the generator
     **raises** rather than shipping a pod short one rate; and if the new year
     publishes a real **Farmland** row, add it **without** an `_assumed` key —
     that retires the "Farmland rate assumed" caveat on screen automatically.
     `tests/test_generate_status.py` fails if the committed manifest and this
     file disagree.
3. **Bump `ASSESSMENT_YEAR` in `main.py`** — the single source of truth the
   year-alignment check reads.
4. **Bump the pinned activity windows in `main.py`** — `FIRE_YEARS`,
   `PERMIT_YEARS` (5yr, Development lens A base), and `PERMIT_YEARS_RECENT` (3yr,
   the window-toggle recent cut): drop the oldest year, add the newest
   *completed* calendar year (pinned so a partial year is never averaged/summed
   in; a stale pin hard-errors via the drift guard, so this can't be missed
   silently). All three roll together. **`PERMIT_YEARS_LONG` (the "Since 2009"
   window) needs NO edit** — it is DERIVED from `PERMIT_YEARS`' last year
   (`range(2009, PERMIT_YEARS[-1] + 1)`), so bumping `PERMIT_YEARS` extends it
   automatically; its 2009 start never moves.
5. **Confirm `data/stormwater_rates.json` has the new year** — stormwater
   rates are year-keyed and must match the roll year, same rule as mill rates.
6. **Bump `DATA_YEAR` / `RATE_YEAR` in `scripts/generate_status.py`** —
   ⚠️ these are *separate constants* from main.py's pin; forget them and
   `status.json` (and the site's vintage display) silently misreports the
   year. Bump `ZONING_YEAR` only when the zoning bylaw vintage changes.
7. **Leave `WATER_RATE_YEAR` / `FRANCHISE_RATE_YEAR` alone** unless new
   verified tariff schedules have been added to `data/water_rates.json` /
   `data/franchise_rates.json` — these are forward-looking modeled bills,
   deliberately independent of the roll year. When they do bump, the
   legend/blurb year in `web/index.html` rides along (see main.py comments).
8. **Re-pin the temporal baseline: `python scripts/check_temporal_years.py
   --write-baseline`** (`docs/SPEC_temporal.md` §0.3). The baseline pins settled
   historical years and deliberately **excludes whatever year was live when it
   was written**. After the roll, last year is no longer live, is not in the
   baseline, and the guard reports it `not pinned` — a **warning, not a
   failure**, by design. Re-pinning closes it. ⚠️ **Read the guard's output
   BEFORE re-pinning, never after**: `--write-baseline` overwrites the bands
   with whatever the data now says, so re-pinning first would erase the very
   drift the guard exists to show you.
   - **The archive needs NO action.** `refresh.yml` captures the live year on
     every run and freezes it automatically once the roll moves on
     (`src/load_temporal.write_archive`) — deliberately, because a step
     performed once at a date months away is a step that does not happen. **Do
     confirm `data/temporal_archive.json` gained last year's entry** before the
     roll: the current roll covers exactly one year, so a year not captured in
     time is unrecoverable.
   - **If the guard HARD-FAILS (exit 5) on a settled year losing accounts, do
     NOT re-pin.** That is the 2024 defect recurring. Re-run
     `tools/audit_historical_roll_gaps.py`, and if confirmed add the year to
     `HISTORICAL_DEFECT_YEARS` in `src/load_temporal.py` — which drops it from
     the published series unless the archive already holds it.
9. **Run `pytest tests/ -q`, commit, push**, then trigger the workflow
   ("Run workflow" on refresh.yml) and confirm it regenerates + deploys.
10. **Clear the banner:** `python scripts/generate_status.py --clear-banner`,
   commit, push. ⚠️ The banner is *preserved* across runs unless explicitly
   cleared (by design, so a manual notice isn't wiped by the heartbeat) — the
   realigned weekly run will NOT clear it for you. Note: the banner change
   reaches the live site on the next workflow run's deploy, not on push.

## 2. The weekly run failed (red X email)

Triage by which step failed, in the run log:

- **"Run tests"** — a real regression or an environment/dependency change;
  the site is unaffected. Reproduce locally (`.venv/bin/python -m pytest
  tests/ -q`), fix before next Monday if convenient.
- **"Download source data"** — usually a portal blip; re-run the workflow.
  Persistent patterns:
  - *Timeout on one source* — Socrata generates large GeoJSON server-side
    before sending byte one; raise that source's per-source `timeout` in
    `scripts/download_data.py` `SOURCES` (precedent: roads → 900 s).
  - *"features == $limit … truncated"* — the dataset outgrew our `$limit`;
    raise BOTH the `$limit` in the URL and the matching `limit` field.
  - *"downloaded N but server reports M"* — incomplete download; re-run. If
    it persists, the portal itself is misbehaving — wait it out.
- **"Check unmatched names"** (exit 5, `scripts/check_unmatched_names.py`) — a
  NEW assessment neighbourhood name has no boundary polygon, so its assessed
  value would silently drop off the map. The build stops *before* regen, so the
  site keeps serving last-good data. The error names the drifted neighbourhood.
  Fix: find where it should map (spatial containment via the assessment lat/lon
  is the decisive test — DATA.md "Name Matching") and either add a
  `NAME_CORRECTIONS` entry (`src/load_assessment.py`) or, if the value is truly
  immaterial and deliberately unmapped (the OLIVER precedent), add the name to
  `data/expected_unmatched.json` with a reason. A boundary-side hole or a
  resolved name is only a warning (exit 0) asking for the same baseline update.
- **"Check cardinality value anchors"** (exit 5, `scripts/check_value_anchors.py`)
  — the record-to-parcel *regime* moved: a duplicated-parcel condo regime
  appearing, more value dropping out as lot-acre-ineligible, or a needle
  returning to the top of the exported grid. This runs **after** regen and stops
  the commit, so the site keeps serving last-good data. The error names which
  anchors moved. **Do not just re-pin the baseline** — that silences the alarm
  without answering it. Diagnose first: re-run
  `tools/audit_cardinality_denominators.py` (needs the real roll) and check the
  new numbers against `docs/FINDINGS_lot_dedupe.md` §3–§5; `SHARE_MAX_M2` was
  calibrated on a regime where the dedupe is a no-op, so if
  `dup_parcel_points` grew, the threshold itself needs re-validating. Once the
  move is understood and intentional, re-pin with
  `python scripts/check_value_anchors.py --write-baseline` and commit
  `data/expected_value_anchors.json`. Moves in the benign direction (fewer
  ineligible points, a flatter distribution) only warn. **The January year-roll
  is the most likely trigger** — see §1.
- **"Check served columns"** (exit 5, `scripts/check_served_columns.py`) — a
  column the site serves **disappeared**, or landed on only some neighbourhoods.
  Runs after regen, before the commit, so the site keeps serving last-good data.
  The error names each column as `MISSING` (gone from every feature) or
  `PARTIAL` (on *n* of 406 — that additionally means a join dropped rows).
  ⚠️ **This is the one guard whose failure you would otherwise never see.**
  Every lens self-gates on its own column, so the affected row, view or tooltip
  line just *isn't there* — no error, no NaN, no banner, and the publish looks
  clean. That is why it fails hard on something as undramatic as a missing key.
  **Do not re-pin to make it pass.** ⚠️ **Check the "Download source data" step
  first — it is the most likely cause.** Every lens in `main.py` skips with a
  `logger.warning` when its raw file is absent (roads, bike, fire, transit,
  permits, zoning, property-info, unit costs), and the run then continues and
  publishes *without* that lens. So one dataset failing to download silently
  removes a whole layer from the site, and this guard is what turns that back
  into a red build. Otherwise: a renamed source field, a loader returning early,
  a join losing rows, or a `main.py` flag that stopped being passed. Only once
  the removal is understood
  **and** intended, re-pin with
  `python scripts/check_served_columns.py --write-baseline` and commit
  `data/expected_columns.json`. A **new** column only warns, so adding a metric
  never blocks the publish — re-pin at your convenience.
- **"Run verified notebooks"** (exit 1, `tools/run_verified_notebooks.py`,
  added 2026-08-05) — an invariant inside `notebooks/verified/01_money_lens.py`
  failed: the pipeline, re-run independently in notebook form, disagrees with
  itself. Runs after regen, before the commit, so the site (and the last
  published `web/verified/01_money_lens.html`, `docs/VERIFICATION.md`) keeps
  serving last-good. Take this one seriously — unlike the UI-facing guards
  below, it's a second, differently-shaped recomputation of the exact numbers
  the site is about to publish, not a rendering check. The log names which
  check failed (`tools/run_verified_notebooks.py` tails it on failure);
  cross-reference against the assertion in the notebook source. Reproduce
  locally: `.venv/bin/python tools/run_verified_notebooks.py --out-dir
  /tmp/_verified` and open the HTML.
- **"Check temporal years"** (exit 5, `scripts/check_temporal_years.py`) — the
  assessment *time series* failed a control. Like the guards above it runs before
  the status manifest, so the heartbeat stays unbumped and the site serves
  last-good data. The error lists every failed check by name; the three that
  matter:
  - **`years: UNEXPECTEDLY PRESENT [2024]`** — a year we omit *by decision*
    (`DECISIONS.md` 2026-07-28) reached the series. Something republished a slice
    known to be missing 2,322 accounts. Do not "fix" the gap; find what changed.
  - **`<year>.n_accounts … a settled year LOST …`** — the 2024 defect recurring
    on a different year. **Do NOT re-pin.** Re-run
    `tools/audit_historical_roll_gaps.py` (~20 min, the exact account-level
    control), and if confirmed add the year to `HISTORICAL_DEFECT_YEARS` in
    `src/load_temporal.py`.
  - **`archive: <year> … the captured copy is not being used`** — the archive
    holds a year but the defective historical slice is being served instead.
    Check `data/temporal_archive.json` is present and committed.

  Benign moves (a settled year *gaining*, an unpinned year) only warn. **The
  January year-roll is the expected trigger for the "not pinned" warning** — §1
  step 8.
- **"Regenerate web GeoJSON"** — read the traceback; the loaders hard-error
  deliberately on upstream schema drift rather than publishing wrong numbers.
  Usual fixes are extending an explicit mapping: `ZONE_CATEGORY`
  (load_zoning), the functional-class dict (load_roads), `ZONE_RUNOFF`
  (load_stormwater), `DISPATCH_COLUMN_CANDIDATES` (load_fire), the class
  bridge in apply_tax_rates. Never switch these to prefix/keyword matching
  (locked decision — see DECISIONS.md).
- **"Smoke-check the built render"** (exit 1, `tools/profiling/verify-smoke.js`,
  added 2026-08-02) — the regenerated data reaches the page, but the page does
  something wrong with it. ⚠️ **This is the only step that looks at the RENDER**;
  every guard above it checks the data. It runs **after** the data commit and
  **before** `upload-pages-artifact`, so the commit has landed but **the live
  site keeps serving the previous good render** — the failure direction is safe.
  Read the failing check's letter:
  - **A*** (4xx, failed request, console error, page exception) — a served file
    is missing or the page threw. Usually a file that regen did not write.
  - **B*** (shape) — a column the page reads is **absent**. `B6` names the
    column and how many features lack it; `B4` does the same for the land-use
    fractions. This is the *silent* one: `viewTooltip` guards each row with
    `!= null`, so a dropped column **omits the row** rather than printing NaN,
    and nothing else in the suite would see it.
  - **C*** (garbage) — `NaN` / `undefined` reached rendered text, or a lens
    rendered no readout at all. The check names the offending neighbourhoods.
  - **D*** (provenance) — the mill-rate pod disagrees with `status.json`, or
    the banner does not match the manifest.
  ⚠️ **Do not "fix" this by relaxing the check.** Nothing in it is pinned to a
  data value — every assertion is an invariant or is derived from the served
  file — so it **cannot** go red merely because the numbers moved. A red here
  means the render and the data genuinely disagree. Reproduce locally against
  the built tree:
  ```bash
  python scripts/build_site.py --src web --out /tmp/_site
  .venv/bin/python -m http.server 8931 --directory /tmp/_site &
  node tools/profiling/verify-smoke.js http://localhost:8931/index.html
  node tools/profiling/verify-smoke.js http://localhost:8931/full/index.html
  ```
- **Commit/deploy steps** — transient GitHub issues; re-run.

**Loud warnings worth a look even on green runs:** unknown zone / road-class
codes (hand-assign to the dicts), new fire `event_type_group` values (kept in
by design, logged), the year-check "inconclusive" warning (metadata fetch
failed; fine once, investigate if it repeats).

## 3. The schedule went to sleep

GitHub auto-disables cron workflows after 60 days without repo activity. The
heartbeat commit is what normally prevents this, but commits pushed with the
default `GITHUB_TOKEN` don't reliably reset the timer (SPEC_deployment
"Staying awake").

**How you find out (2026-07-26).** You no longer have to notice. The site
raises its own banner when `status.json`'s `last_checked` is more than
**14 days** old — two missed weekly runs. That check runs in the browser off
the manifest's age, so it fires no matter *why* the pipeline stopped: disabled
schedule, expired token, broken workflow, or a run that never got to the commit
step. A banner the backend set (e.g. the year-alignment hold) always wins over
it.

**Recovery:** Actions tab → "Refresh map data" → Enable workflow → Run
workflow. The banner clears itself on the next successful run — there is no
`--clear-banner` to remember, because nothing ever wrote it down.

### The heartbeat token (`HEARTBEAT_TOKEN`)

`refresh.yml` checks out with `secrets.HEARTBEAT_TOKEN` when it exists and
falls back to `github.token` when it doesn't, so the workflow runs either way —
the secret is an *upgrade*, not a dependency. A push authenticated by a PAT
counts as repo activity; one by `GITHUB_TOKEN` may not.

To create or rotate it: GitHub → Settings → Developer settings →
**Fine-grained tokens** → repo access limited to `edmonton-tax-viz`, repository
permission **Contents: Read and write** (nothing else). Add it at repo →
Settings → Secrets and variables → Actions → `HEARTBEAT_TOKEN`.

**Fine-grained tokens expire (366 days max), and that is fine here.** When it
lapses the push fails and the whole run goes red — GitHub emails you about a
failed scheduled workflow, and the staleness banner appears within 14 days as
the backstop. The failure is loud by construction: the commit step deliberately
does *not* use `git push || true`, because that form reports green while the
heartbeat quietly dies.

## 3b. ⚠️ NEVER commit a locally regenerated `web/data` (added 2026-08-01)

**`python main.py` on a dev box rebuilds the map from whatever is in
`data/raw/` — which is almost certainly older than what the site is serving.**
The committed `web/data/*.geojson` comes from the `refresh.yml` auto-refresh,
which **downloads fresh data on every run**. A local box does not.

Measured 2026-08-01 on the Oracle server: local `data/raw/` dated **2026-07-06**
against a committed geojson from the **2026-07-27** refresh. A run intended only
to ADD columns changed **1,896 pre-existing values** across 406 features —
`revenue_per_acre`, `value_per_lot_acre` and friends all shifted ~0.2%. Committing
that would have silently rolled the published numbers back three weeks, with no
banner and nothing in `status.json` to say so.

**Rules:**
- Pipeline code changes ship as **code only**. The columns/values appear on the
  site when `refresh.yml` next runs, which is the only thing that should ever
  write `web/data`.
- To see your change locally, regenerate to a throwaway path:
  `python main.py --skip-png --geojson-out /tmp/x.geojson`.
- If the data genuinely *should* roll, run `scripts/download_data.py` first and
  say so explicitly in the commit — don't let a vintage change ride along inside
  a feature PR.
- **After a pipeline change merges, expect the new columns to be ABSENT from the
  served file until the next refresh.** Any UI reading them must degrade cleanly
  in that window (the house pattern for optional data). To end that window
  early instead of waiting out the weekly cron, see **§3d**.
- `git status --short web/data/` before committing is the cheap check.

## 3c. "The change didn't ship" — check the browser cache BEFORE the deploy
(added 2026-08-01)

Peter, on the phone after a deploy: *"i'm still not seeing the mill rates on
mobile… i can see it when i open it in a private window on my phone. but it's
refusing to show on normal safari."*

**A private window rendering the change while the normal one does not is a cache
result, full stop** — it is the fastest disambiguation available and worth asking
for first. `web/styles.css` was extracted from `index.html` in 2026-07-29, so a
CSS-only change now ships in a **separate file with its own cache lifetime**, and
a phone can hold a stale stylesheet against a fresh page. That is exactly the
shape that makes a change look half-deployed.

**Triage order, cheapest first:**
1. `gh run list --workflow=deploy.yml --limit 3` — did it deploy at all? ⚠️ A
   data-only change produces **no run** (`deploy.yml` excludes `web/data/**`).
2. `curl -s <site>/styles.css | grep <your new rule>` — is the change actually
   served? This distinguishes "not deployed" from "not seen" in one command.
3. Private/incognito window on the affected device.
4. Only then look for a device-specific bug.

Headers as of 2026-08-01: `index.html` and `styles.css` both come back
`cache-control: max-age=600` with matching `last-modified`, so the intended
window is 10 minutes — the observed Safari behaviour was longer.

**The stylesheet link is cache-busted since 2026-08-02.** `scripts/build_site.py`
stamps it `styles.css?v=<8 hex of the file's content hash>` in both builds, so a
CSS change lands under a URL the browser has never seen. The token is a **content
hash, not the commit sha** — an unrelated deploy leaves it alone and the cached
copy stays good.
⚠️ **This does NOT make every "didn't ship" report a non-cache report.** It covers
stale CSS under *fresh* HTML — the shape above. A browser holding `index.html`
itself stale holds the old query string with it and sees the old CSS by
construction, and `index.html` cannot bust itself. **So step 3 still earns its
place**; what changed is that a *correctly reloaded page* can no longer pair with
an old stylesheet.

To read the token being served: `curl -s <site>/index.html | grep -o 'styles.css?v=[a-f0-9]*'`.
If it matches your local `python -c "import hashlib;print(hashlib.sha256(open('web/styles.css','rb').read()).hexdigest()[:8])"`,
the deployed CSS is your CSS.

## 3d. Publishing a data-side feature WITHOUT waiting for Monday
(added 2026-08-04)

§3b's last bullet says the new columns are absent "until the next refresh" —
which is true, but the cron is weekly and that wait can be up to **six days**.
**Dispatching `refresh.yml` by hand is the supported way to close it**, and is
the right call when work is *gated on the data existing* rather than on the
calendar.

```bash
gh workflow run refresh.yml --ref master
gh run list --workflow=refresh.yml --limit 1
```

Done 2026-08-04 (run `30909649645`): three items carried **S89 → S91** behind
the Monday cron closed in one run, and the served-column guard got its
**first-ever CI execution** as a side effect.

**Why this is safe, and what would make it unsafe:**
- `refresh.yml` **downloads fresh data every run** and **commits only if the
  data actually changed** — git is the change detector. Re-running it is
  idempotent, not destructive.
- ⚠️ It is safe *because it runs the whole guard chain*. This is **not** a
  licence to hand-run the pieces. In particular, **never hand-run
  `generate_status.py` and commit it** — it stamps `last_checked` with a
  freshness check that never happened, and the staleness banner reads that
  field.
- ⚠️ It **deploys to the live site.** Confirm the code it will publish is
  already merged and verified.

**Expect 10–20 minutes, not ~9.** The 2026-08-04 dispatch took **20m00s** and
the 2026-08-05 one **13m10s**, against the scheduled runs' ~9m30s; the variable
part is *"Install the verify harness"* (npm + Playwright Chromium) before the
pre-publish smoke gate, which is cache-dependent and so swings by ~7 minutes
between runs. **A run sitting at that step is downloading a browser, not hung**
— the data steps are already green by then. **Budget a monitor for 25 minutes
regardless**; finishing early is the good case. Step-level progress:

```bash
gh api repos/PeterFriedrich/edmonton-tax-viz/actions/runs/<id>/jobs \
  -q '.jobs[] | .steps[] | "\(.number). \(.name) — \(.status)/\(.conclusion // "-")"'
```

That view is worth knowing: it showed *"Commit regenerated data + heartbeat"*
already green while the run still had eight steps to go, so the data was
confirmed published well before the run finished.

**Afterwards**, if the run shipped new columns:
`.venv/bin/python scripts/check_served_columns.py --write-baseline`.
⚠️ **Bare `python` on the Oracle box is the system interpreter and cannot run
that script** (`dict[str, int]` → `TypeError: 'type' object is not
subscriptable`). The procedures write bare `python` after a `source
.venv/bin/activate` that is easy to skip.

## 4. Wrong numbers suspected on the live site

1. Check `web/data/status.json` — vintage + `generated` date + GeoJSON hash
   tell you exactly what's being served.
2. For a systematic check, `docs/DATA_INTEGRITY.md` is the audit brief
   (system map + ranked joints); the `edmonton-audit` skill goes deep on one
   target.
3. **Known gap — no deploy-without-regenerate path.** Every deploy comes from
   a fresh download + regeneration; `git revert` of a bad auto-refresh commit
   doesn't reach the live site until a workflow run, and that run re-downloads.
   If *upstream data itself* goes bad (beyond what the year hold covers), the
   honest stopgap is: disable the schedule (Actions UI), set a banner
   (`generate_status.py --banner "..."` — but note it also only deploys with
   a run), and fix forward. A deploy-only workflow would close this gap if it
   ever bites for real.

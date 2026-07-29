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
2. **Add the new year's block to `data/mill_rates.json`** — a manual,
   *reviewed* step (deliberately never auto-fetched; see DATA.md §4 for the
   vocabulary bridge and known quirks).
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

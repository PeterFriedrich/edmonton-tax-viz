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
8. **Run `pytest tests/ -q`, commit, push**, then trigger the workflow
   ("Run workflow" on refresh.yml) and confirm it regenerates + deploys.
9. **Clear the banner:** `python scripts/generate_status.py --clear-banner`,
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
heartbeat commit normally prevents this, but `GITHUB_TOKEN` commits don't
always reset the timer (SPEC_deployment "Staying awake"). If `last_checked`
in status.json goes stale > 1 week: Actions tab → "Refresh map data" →
Enable workflow → Run workflow.

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

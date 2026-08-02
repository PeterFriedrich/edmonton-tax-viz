# Scope: Automated Backend + Static Deployment

**Status: LIVE (2026-07-01/02).** The site is deployed and auto-refreshing at
**https://peterfriedrich.github.io/edmonton-tax-viz/**. A **scheduled GitHub
Action** (`.github/workflows/refresh.yml`) regenerates the map data and publishes
it to a fully static **GitHub Pages** frontend; no always-on server. Built &
verified in production: `scripts/download_data.py` (fetch all three inputs),
`scripts/generate_status.py` (→ `web/data/status.json`), the frontend banner in
`web/index.html`, the workflow, and `requirements-ci.txt`. **Bootstrap done**
(Pages enabled with `build_type: workflow` via API; first run green end-to-end).
Action versions on node24 majors (checkout v7 / setup-python v6 / upload-pages-
artifact v5 / deploy-pages v5). **Remaining: deferred follow-ons only** — auto
year-detection + mismatch banner, per-year archives, and the 60-day heartbeat
watch. This doc is the agreed design; the sub-sections below note where reality
now differs.

## The key fact this is built around

**Everything that matters here updates at most once a year.** The Edmonton
assessment dataset rolls its assessment year annually; the mill-rate dataset
(`pwis-wc4c`) publishes new rates annually. The Socrata feed updates weekly, but
those intra-year edits don't meaningfully move a neighbourhood-level
value/revenue-per-acre map. So the system is optimized for **rare data changes**,
not real-time freshness — which is exactly what a periodic batch job suits.

## Core decision: push, not pull

**DECIDED: the backend regenerates and commits static data into the repo; the
frontend never calls a backend at runtime.**

GitHub Pages serves *only* files committed to the repo — there is no external
store it can read. So the data (GeoJSON) must live in the repo as committed
files, and the backend's job ends by committing them. The alternative — a live
frontend→server fetch — would couple every page load to a server being up,
reachable, and CORS-configured, to serve a file that's identical for months. All
downside.

With the commit-and-publish model:
- The site is **100% static** (HTML + committed GeoJSON), served by GitHub's CDN.
- No CORS, no backend latency, no uptime coupling, no server to maintain.
- It fits what already exists: `web/data/neighbourhood_value_per_acre.geojson` is
  already a committed file. We're only automating *who* regenerates and commits
  it, and *when*.

## Two deploy paths: data vs. code (2026-07-22)

The pipeline was originally the *only* way anything reached the live site — so a
pure code change (moving a button, restyling, building a lens on
already-committed data) could only ship by running the full weekly pipeline
(download all ~750 MB + regenerate). That fused two unrelated triggers.

They're now split:

| Workflow | Fires on | Does | Cost |
|---|---|---|---|
| `refresh.yml` (DATA) | weekly cron + `workflow_dispatch` | download → regen `web/data/` → commit → **`build_site` → deploy** | full pipeline (~min) |
| `deploy.yml` (CODE) | push to `master` touching `web/**` (excl. `web/data/**`) + `workflow_dispatch` | **`build_site` → re-upload** committed `web/` to Pages | ~seconds |

(Both paths run `scripts/build_site.py` before the Pages upload — see the
**Two-build emit** section below.)

**Why this is safe and needs no data step:** `web/data/*.geojson` is *committed*
(the data-bot commits it each refresh), so the last-good data is already on disk
for any code deploy — nothing to fetch, nothing to regenerate. The path filter
excludes `web/data/**` so the bot's data commit doesn't double-deploy (its own
refresh run already deployed it). Both workflows share the `refresh-map-data`
concurrency group (`cancel-in-progress: false`), so a code deploy queues behind
an in-flight refresh instead of racing it on Pages.

**What still needs a data run:** only a lens that requires a *brand-new* dataset.
Even then it's `download_data.py --only <source>` + that one loader + commit —
not all 15. **Selective/partial regen** (teaching `main.py` which datasets a
given change actually needs, so even data runs skip untouched sources) is a
harder, separate refinement and is explicitly **deferred** — the cheap
change-signal exists (`rowsUpdatedAt` per dataset in Socrata view metadata; e.g.
roads was static 2+ months while permits/fire change daily), but acting on it
needs raw-file caching across CI runs. Not built.

## Two-build emit: public root + /full/ specialist (2026-07-23)

Neither workflow uploads `web/` directly any more. Both run
`scripts/build_site.py --src web --out _site` immediately before
`upload-pages-artifact` (factored once, not inlined twice), and upload `_site/`.
That one step fans the site out into **two builds inside a single Pages
artifact**:

| Path in artifact | Build | Contents |
|---|---|---|
| `_site/` (root) | **PUBLIC** (curated) | whole `web/` tree, shared `data/` + `vendor/`, `DEFAULT_BUILD` rewritten to `"public"`. The advertised URL. |
| `_site/full/` | **SPECIALIST** (everything) | `index.html` only, `DEFAULT_BUILD` `"full"`, `<base href="../">` so its relative asset URLs resolve to the root's shared `data/` + `vendor/`, plus an injected WIP badge. Discoverable-but-unlisted; linked from the README. |

**One source of truth.** There is one hand-edited file, `web/index.html`, carrying
a single `const DEFAULT_BUILD = "public|full";` literal. The public and full
outputs are byte-identical *except* that literal (plus the `<base>` tag and WIP
badge injected into full). So:

- **Both builds regenerate on every deploy, from the same source** — code push or
  weekly data refresh, doesn't matter. They *cannot* drift: any change to
  `web/index.html` lands in both automatically.
- **Data is shared, not duplicated.** `/full/` reaches the root's `data/` +
  `vendor/` via `<base href="../">` — one copy of the multi-MB GeoJSON on disk, so
  the two builds can never disagree about data.

**The flag discipline (the thing that bites you if you forget).** To make a control
specialist-only, gate it on `BUILD === "full"` (`FULL_BUILD`) in `web/index.html`.
Public then hides it; `/full/` shows it. **The default is *public*:** anything you
add and *don't* explicitly gate on `FULL_BUILD` appears on the public root. The
failure mode is therefore **"a specialist control leaked to public,"** not "the
builds drifted." When adding a control, the one question to ask is *does this
belong in public?* — if not, flag it `full`.

**Guardrails** (these catch the *other* class of mistake):

- `set_default_build` (`build_site.py`) fails the build loudly if the
  `DEFAULT_BUILD` literal isn't found *exactly once* — a refactor that renames or
  removes it breaks the deploy instead of silently shipping the wrong default.
- `tests/test_build_site.py` runs in `refresh.yml`'s pytest gate and guards the
  emitted shape (root hides full-only controls, `/full/` carries them, no GeoJSON
  duplication, the source literal exists).

Rationale for the split (curated public root vs. discoverable `/full/`) and the
per-control tag table live in `docs/PLAN_public_release.md` §2a and
`docs/CONTROLS_MATRIX.md` §2; this section is the *operational* how-it-deploys view.

## Backend: a scheduled GitHub Action (primary)

**DECIDED: the backend is a scheduled GitHub Action, not a dedicated server.**
Because the data has to end up in the repo anyway, GitHub's own runners can do
the whole job for free — no VM to maintain, no deploy key, no "is the server up"
question.

```
   Edmonton Open Data (Socrata)
   ├─ assessment (q7d6-ambg) ─┐
   └─ tax rates (pwis-wc4c)   │  download
                              ▼
   Scheduled GitHub Action ── run main.py ──▶ regenerate web/data/*.geojson
                              │  commit (if changed) + deploy
                              ▼
   GitHub repo ──▶ GitHub Pages (static, CDN) ──▶ visitors
```

An Action is a YAML workflow in `.github/workflows/`. On a cron trigger, GitHub
boots a fresh Ubuntu VM, runs the steps, and destroys it. Sketch:

```yaml
name: Refresh map data
on:
  schedule:
    - cron: '0 8 * * 1'        # weekly, Mon 08:00 UTC (cron is UTC + best-effort)
  workflow_dispatch: {}          # manual "run now" button

permissions:
  contents: write                # commit regenerated data back to the repo
  pages: write                   # deploy to Pages
  id-token: write                # required by the Pages deploy action

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: python scripts/download_data.py     # pull Socrata data
      - run: python main.py                       # regenerate web/data/*.geojson
      - run: |                                     # commit only if changed
          git config user.name  "data-bot"
          git config user.email "bot@users.noreply.github.com"
          git add web/data
          git commit -m "Auto-refresh map data" || echo "no changes"
          git push
      # then deploy web/ to Pages (upload-pages-artifact + deploy-pages)
```

That is the entire backend.

**What the runner can/can't do (the edges):**
- It's a real VM — installs any pip/apt deps, can run Docker, headless Chromium,
  heavy parallel compute. The pipeline's deps (geopandas/shapely/pandas/
  matplotlib) install cleanly on `ubuntu-latest`.
- **Ephemeral:** destroyed at job end; no state persists except what's committed.
- **Capped at 6 hours/job.** Fine for a batch job; can't host anything 24/7.
- **No stable IP** — it can't *be* a server something connects to.
- **Public-repo Actions minutes are free** (private repos: 2,000 min/month free —
  this job is minutes per run either way).
- ToS note: Actions is for repo-related automation; building this project's data
  is squarely legitimate use.

### Backend flow

1. **Regenerate.** Download the raw assessment data + matching-year mill rates,
   run `main.py` → PNG + `web/data/*.geojson` at the canonical params (setback
   45 m, simplify 10 m).
2. **Commit if changed.** `git add web/data && git commit || true && git push`.
   The commit only lands if output actually changed, so **git is the change
   detector** — a redundant run pushes nothing.
3. **Emit the two builds.** `scripts/build_site.py --src web --out _site` — the
   shared code-shaping step (`deploy.yml` runs the same one). It also stamps the
   stylesheet link with a content-hash cache-buster (2026-08-02, `RUNBOOK.md` §3c).
4. **Gate on the RENDER** (added 2026-08-02). `tools/profiling/verify-smoke.js`
   drives the built tree in headless Chromium, **both builds**, and fails the run
   *before* the artifact is uploaded — so a red check leaves the live site
   serving the previous good render. ⚠️ **This is the only step on this path that
   looks at the rendered page.** Every other guard checks the DATA, and this
   workflow regenerates *and* deploys in one run, so without it a data change
   could alter what the site shows with nothing on fire. ⚠️ **Every assertion in
   it is an invariant or is derived from the served file, never a pinned data
   value** — a literal would go red on each legitimate refresh
   (`verify-temporal.js` did exactly that on 2026-08-01), and a check that cries
   wolf gets ignored. Triage: `RUNBOOK.md` §2.
5. **Deploy.** Publish the emitted tree to Pages via the official Pages actions
   (`upload-pages-artifact` + `deploy-pages`). This removes any "Pages can't
   serve a subfolder" problem — no `gh-pages` branch or `/docs` move needed.

**Auth:** the workflow's built-in `GITHUB_TOKEN` (via `permissions:` above)
covers both committing to this repo and deploying Pages — **no deploy key or PAT
needed for the core flow.** (One exception under "stay-awake" below.)

### Staying awake (the 60-day pause)

Scheduled workflows are auto-disabled after **60 days of no repo activity**. Since
annual data may not change for months, the run should write a **heartbeat** — bump
a `last_checked` timestamp in the status manifest (below) every run and commit it.
That commit is repo activity and keeps the schedule alive, *and* it's genuinely
useful frontend metadata (two birds).

Wrinkle: commits made with the default `GITHUB_TOKEN` are sometimes reported *not*
to reset the inactivity timer (GitHub suppresses some automation-triggered
events). If that proves true in practice, make the heartbeat commit with a small
repo-scoped **PAT** instead, or just re-enable the workflow if it ever sleeps.

**As built (2026-07-26) — belt and braces, because prevention alone can't be
trusted.** The wrinkle above was taken as a given rather than waited on:

1. **Prevention.** `refresh.yml` checks out with
   `${{ secrets.HEARTBEAT_TOKEN || github.token }}` — a fine-grained,
   contents:write, this-repo-only PAT when present, silently the old behaviour
   when not (forks, or a revoked token, still work). A PAT push *does* trigger
   workflows, unlike `GITHUB_TOKEN`; that is safe only because the commit step
   stages `web/data` **only** and `deploy.yml` excludes `web/data/**`. Widening
   what gets staged would start a deploy loop.
2. **Detection.** Prevention has its own silent failure — the PAT expires (366
   days max), and so does any other assumption about why the pipeline is alive.
   So the frontend ages `last_checked` itself and raises the banner past
   `STALE_DAYS = 14` (two missed weekly runs). This needs no server, no secret
   and nothing to renew, and it covers *every* cause of stoppage rather than the
   one the PAT addresses. A backend-set banner outranks it.
3. **No green-but-broken.** The commit step's `git push || echo "Nothing to
   push."` was replaced with an explicit `git diff --cached --quiet` test. The
   `||` form swallowed auth failures as well as no-ops, which would have let an
   expired PAT report success while the heartbeat stopped — the exact failure
   this section exists to prevent.

The design principle worth keeping: **the thing that detects the outage must not
be the thing that can go out.** That is why detection lives in the browser.

## Year alignment

The assessment year lives only in the dataset metadata (see `DATA.md`), and mill
rates must match that year. The rate fetch should **auto-detect the assessment
year from the assessment dataset metadata** and pull the matching `pwis-wc4c`
rates, so the two can never silently desync.

**When the years can't be aligned (graceful degradation, not a hard fail):** rates
can lag the assessment roll by months — e.g. the 2026 assessment is published but
2026 municipal rates aren't out yet. In that window the job must **not** compute a
mismatched-year map. Instead:
- **Keep serving last year's committed data** (already in the repo — the site
  stays fully functional on the previous year).
- **Set a banner** in the status manifest, e.g. *"Showing 2025 data — the 2026
  assessment is out but Edmonton's 2026 municipal tax rates aren't published yet.
  The map updates automatically once they are."*
- Log/alert so we know it's in the holding state.

So in that window only the banner updates; the data waits for matching rates.

**Zoning is a third refreshed input (added 2026-06-29).** The land-use set-aside
(`src/load_zoning.py`, see `SPEC_revenue.md`) keys off the zoning layer (`fixa-tstc`),
NOT off revenue — so it only stays correct if zoning is re-pulled each cycle. As
fringe land develops, the city rezones it (Future/Agricultural → residential), its
set-aside fraction drops below 0.90, and it auto-rejoins the colour scale on the next
run. If zoning is snapshotted once and never refreshed, developing neighbourhoods get
wrongly greyed for years. So: **pull zoning alongside assessment + mill rates, and
record its vintage** (add `zoning_year` to `status.json`). Zoning has no hard
year-alignment constraint with assessment (it's stable land-use, not a tax rate), but
its vintage should be visible for provenance.

## Frontend (GitHub Pages, static)

Serves `web/` + the committed GeoJSON. No runtime backend. CDN deps (MapLibre,
deck.gl via unpkg) load client-side and need only the visitor's internet.

**Status manifest + banner.** A small committed JSON file (`web/data/status.json`)
records what the site is showing, doubles as the heartbeat, and carries an
optional banner. The frontend fetches it on load and, if `banner` is non-null,
renders a maintenance-style notice above the map. Example:

```json
{
  "data_year": 2025,
  "rate_year": 2025,
  "zoning_year": 2024,
  "generated": "2026-06-28",
  "last_checked": "2026-06-28",
  "banner": null
}
```

`last_checked` is bumped every run (the heartbeat); `generated` changes only when
the data actually changes; `banner` is set during the holding window or for any
maintenance notice — settable by the backend with no frontend deploy. (Banner
styling is a UI concern — see `docs/UI.md`.)

## Decisions settled (2026-07-01, as built)

1. **Change-detection strategy — DECIDED (b): re-run on schedule, `git diff` gates
   the push.** Dead simple; the redundant download is free on the runner. Poll-
   Socrata-metadata (a) can be added later if desired.
2. **Cron cadence — DECIDED: weekly** (`0 8 * * 1`, Mon 08:00 UTC). Overkill for
   annual data but cheap, and bounds staleness to a week when the new year drops.
3. **Heartbeat auth — DECIDED: `GITHUB_TOKEN`.** If the schedule ever auto-disables
   after 60 days, add a repo-scoped PAT for the heartbeat commit (tracked in TODO).

(Also decided by the Action model: Pages-serves-`web/` → the Pages deploy action;
backend auth → built-in `GITHUB_TOKEN`; commit-data-to-repo → yes, also enables the
archive + heartbeat.)

**As-built notes vs. this design:**
- `status.json` carries a `_geojson_sha256` field (not in the example above) as the
  content-change detector so `generated` bumps only on real data change,
  independent of git.
- **`municipal_rates` added 2026-08-01** — the mill rates the revenue map is
  billed at, for the frontend's mill-rate pod:

  ```json
  "municipal_rates": {
    "unit": "per $1,000 assessed",
    "classes": [{"name": "Residential", "rate": 7.6254}, …],
    "assumed": ["Farmland"]
  }
  ```

  Municipal rate only — every figure on the site is the municipal levy, and the
  education levy is provincial. Derived from `data/mill_rates.json` (the manual,
  reviewed input) rather than restated, so the year-roll has one source. `assumed`
  names classes whose rate that year was **inferred, not published** (2025
  Farmland), which is what lets the UI's caveat stop printing on its own the year
  a real row appears instead of becoming a stale literal. Degrades to `null` if
  the rates file is unreadable; the pod simply never shows. ⚠️ Because
  `generate_status.py` only runs during a refresh, a rate change committed by
  hand must be written into **both** files — `tests/test_generate_status.py`
  asserts the committed manifest equals what the generator would produce.
- **Year-alignment GUARD built 2026-07-01** (`scripts/check_year_alignment.py`,
  wired into `refresh.yml` between download and regen; see
  `docs/FINDINGS_data_integrity_audit.md` §3). It detects the roll year from
  Socrata metadata (`Period of Coverage`) and compares it to the pinned
  `ASSESSMENT_YEAR` + the years in `mill_rates.json`. Aligned → proceed;
  mismatch → **holding window exactly as designed above**: regen is skipped,
  the last committed data keeps serving, the banner is auto-set, and the run
  gets a `::warning::` annotation. Metadata unreachable → proceed as aligned
  (the guard adds no new fragility), with a warning.
  **Recovery is still manual** (by design — rates are a reviewed input): bump
  `ASSESSMENT_YEAR` in `main.py`, add the year to `mill_rates.json`, update
  `generate_status.py` year constants, and **clear the banner**
  (`generate_status.py --clear-banner` — aligned runs preserve it otherwise).
- What remains a follow-on from the original design: **auto-fetching** the
  matching `pwis-wc4c` rates for a newly detected year (the guard detects and
  holds; it does not self-heal).
- Mill rates are **not** fetched by `download_data.py` (they live in the committed
  `data/mill_rates.json`); refreshing them for a new year stays a manual, reviewed
  step.

## Future work: multi-year data / archiving

Not in initial scope, but the architecture should not preclude it. Pages storage
is a non-constraint: the served GeoJSON is ~0.5 MB/year against a 1 GB site limit,
so a multi-decade archive is trivial (the real ceiling is the ~100 GB/month
bandwidth soft limit ≈ 200k loads/month). Multiple years would enable a **year
selector** in the UI, pairing with the value↔revenue toggle.

Two independent paths:
- **Forward archiving (free — decide now).** The Action already regenerates each
  year's data. If it writes **per-year files** (`web/data/2025.geojson`, …) and
  **keeps rather than overwrites** them, an archive accumulates automatically.
  Recommendation: archive from day one even if the UI shows only the latest at
  first — years not captured can't be recovered from the current-year feed.
- **Backfill (a real task — future).** Historical assessed values ARE available:
  - **`qi6a-xuwt` — "Property Assessment Data (Historical)"**, coverage **2012–
    2025**, updated annually, has an explicit **`assessment_year`** column, plus
    `lot_size` / `zoning` / `year_built`.
    Endpoint: `https://data.edmonton.ca/resource/qi6a-xuwt.json`.
  - Caveats for a *revenue* backfill: (1) it exposes `mill_class_1/2/3` (the messy
    COMMERCIAL/etc. values) but **not** the clean `Tax Class` join key we use —
    needs a class→rate mapping step. (2) Mill rates (`pwis-wc4c`) only go back to
    **2014**, so 2012–2013 would be **value-only** (no revenue layer).
  - When this work starts, promote the dataset details into `data/DATA.md`.

## Alternative backend: a dedicated server (e.g. Oracle Cloud free VM)

Kept as an option, **not** the plan. A persistent VM running the same pipeline on
cron + `git push` would also work. Choose it only if you later need something the
Action can't do:

| | Scheduled GitHub Action (chosen) | Dedicated VM (Oracle free tier) |
|---|---|---|
| Infra to maintain | none | VM, OS, cron, env |
| Cost | free (public repo) | free tier |
| RAM for ~80 MB CSV + geopandas | ~16 GB runner — fine | up to 24 GB ARM — fine |
| State between runs | none (commit is the state) | persistent disk |
| Max run length | 6 h/job | unbounded |
| Stable IP / can host a service | no | yes |
| Best when | periodic batch (this project) | a live API/daemon, heavy/long compute, or reusing the box |

If a live backend is ever needed (e.g. on-the-fly queries, parcel-level data too
big to precompute), revisit this.

## Open questions / risks

- **Runner deps** — confirm geopandas/shapely install cleanly on `ubuntu-latest`
  (pip wheels normally suffice; add `apt-get` for GDAL only if a wheel needs it).
- **Reproducibility** — keep `requirements.txt` (or an env file) authoritative so
  the runner recreates the environment exactly.
- **First-run bootstrap** — one-time manual step: enable Pages in repo Settings
  (source = GitHub Actions) and run the workflow once via `workflow_dispatch`.
- **Heartbeat reliability** — see the `GITHUB_TOKEN` wrinkle above.

## Cross-refs

- Operations (January year-roll checklist, failure triage): `docs/RUNBOOK.md`.
- Pipeline entrypoint + canonical export params: `main.py`, `docs/PERFORMANCE.md`.
- Data sources, dataset IDs, and the metadata-only assessment year: `data/DATA.md`.
- Revenue phase (adds the mill-rate fetch this automation must also run):
  `docs/SPEC_revenue.md`.
- Intended Pages URL: `peterfriedrich.github.io/edmonton-tax-viz`.

# Project Planning & Audit — Edmonton Revenue-Per-Acre Fiscal Analysis

Filled out by: Claude Code, reviewed by Peter
Date: 2026-08-05 (S95)

> Answers below are concrete and cite actual files/lines, not generic
> pipeline-hygiene answers. Where something isn't decided or isn't
> implemented, that's stated plainly rather than skipped. ⚠️ marks a
> silent-failure risk or a real gap. This doc is a **point-in-time snapshot**
> — like `docs/AUDIT_LEDGER.md` rows, it can go stale; re-verify before
> trusting an old answer.
>
> Most of the individual answers here already live in dedicated docs
> (`docs/ARCHITECTURE.md`, `data/DATA.md`, `docs/DATA_INTEGRITY.md`,
> `docs/security-audit.md`, `docs/AUDIT_LEDGER.md`). What this doc adds is
> putting them all in one place, in the order a planning/audit review wants
> them, so gaps between docs become visible.

---

## Phase 1 — Requirements

**Datasets ingested, and cadence.** All from Edmonton Open Data (Socrata),
fetched by `scripts/download_data.py`, run weekly by `.github/workflows/refresh.yml`
(`cron: '0 8 * * 1'`, Monday 08:00 UTC — Socrata's own update cadence for these
sources is not itself pinned or checked, see ⚠️ below). Current sources
(`data/DATA.md` §1–15):

| # | Dataset | Socrata ID | Update cadence assumed |
|---|---|---|---|
| 1 | Property Assessment (current) | `q7d6-ambg` | annual roll, checked weekly |
| 2 | Property Info (lot size/zoning/year built) | `dkk9-cj3x` | annual roll |
| 3 | Neighbourhood Boundaries | `65fr-66s6` | rarely changes |
| 4 | Property & Education Tax Rates | `pwis-wc4c` | annual (Council-set) |
| 5 | Zoning Bylaw Geographical Data | `fixa-tstc` | infrequent |
| 6 | Road Network | `9j8t-zm52` | infrequent |
| 7 | Fire Response Events | `7hsn-idqi` | rolling/live |
| 8 | Fire Stations | `b4y7-zhnz` | rare |
| 9 | ETS GTFS Static Feed | (transit portal) | seasonal (signup-boundary steps) |
| 10 | Building Permits | `24uj-dj8v` | rolling/live |
| 11 | Alberta FIR Debt Series | (province, non-Socrata file) | annual |
| 12 | Off-Site Levy Fire-Hall Catchments | — | rare |
| 13 | City Service Unit Costs | hand-curated JSON, audited against `budget.edmonton.ca` (S94) | annual budget cycle |
| 14 | Geographic Reference Layers | OSM Overpass (not Edmonton Open Data) | static |
| 15 | Bike Routes | (transportation portal) | infrequent |
| — | Property Assessment (**Historical**) | `qi6a-xuwt` | **catalogued, NOT wired into `download_data.py`** — DATA.md §0 |

⚠️ **No source dataset's own "last updated" metadata is cross-checked against
the pull cadence**, except the one case that burned the project already: roll
year (`scripts/check_year_alignment.py`, T2 below). A silent schema or content
change on any of the other 14 datasets between weekly pulls has no
freshness/version check of its own — the guards that exist (`check_unmatched_names.py`,
`check_value_anchors.py`, `check_served_columns.py`) catch specific *symptoms*
of drift, not drift in general.

**What "up to date" means to a viewer — surfaced, not silently assumed.**
`web/data/status.json` carries `last_checked` (bumped every run, a heartbeat)
and an optional `banner`. The front end (`web/index.html:5024-5031`) computes
its own staleness fallback: if `last_checked` is ≥14 days old (`STALE_DAYS`),
it shows *"Automatic updates may have stopped — data last checked ... The map
still works; the figures are as of that date."* A backend-set banner (e.g. the
year-alignment hold) always takes precedence over the staleness fallback.
Every path that can't determine staleness (missing/garbled date, a future
date) returns *no* warning rather than a false one — deliberately, per the
inline comment, "not manufacture a warning about data that is fine."

**Who this is for.** Not personal/portfolio-only: `docs/PLAN_public_release.md`
records a 2026-07-09 decision to open the tool to "a wider public audience,"
on the existing GitHub Pages deployment with no new hosting/engineering. The
project's own stated rigor bar (`docs/DATA_INTEGRITY.md` §0): *"This is a
public civic analysis; methodology errors will be scrutinized."* — full
production rigor applies, not portfolio-piece rigor.

---

## Phase 2 — Actors & Data Access

**Who/what writes data.** Exactly one path: the scheduled `refresh.yml`
GitHub Action (weekly cron + manual `workflow_dispatch`), which downloads,
regenerates, and commits `web/data/**` + `web/verified/**` +
`data/temporal_archive.json` back to `master` using a bot identity
(`data-bot <41898282+github-actions[bot]@users.noreply.github.com>`). No other
writer exists — no runtime backend, no admin panel, no manual data-edit path
other than a human committing directly (as happened once this session, see
the S95 handoff — docs-only, not a data write).

**Credentials.** Exactly one secret in use: `HEARTBEAT_TOKEN`
(`.github/workflows/refresh.yml:43`), a repo-scoped PAT used only so the
weekly commit registers as "activity" and GitHub doesn't auto-disable the cron
after 60 days of silence (`github.token` pushes don't reliably count). It has
`contents:write` on this repo only, per the file's own comment, and **falls
back to `github.token` if absent/revoked** — the workflow degrades gracefully
rather than failing hard on a missing secret. No Socrata **app token** is used
anywhere (`grep -rn "APP_TOKEN\|X-App-Token"` — zero hits) — all Socrata pulls
are anonymous/unauthenticated. No Mapbox/basemap API key either (MapLibre
against keyless vector tiles). `docs/security-audit.md`'s Data Handling
checklist (verified 2026-07-09) separately confirms nothing in `data/raw/`,
`data/processed/`, or `output/` is tracked in git (all three gitignored), so
there's no plaintext-credential-in-history risk to check beyond the one PAT,
which lives only in repo Secrets.

⚠️ **Anonymous Socrata calls are subject to Socrata's public per-IP throttle**
(no app token raises that ceiling). `download_data.py` has generic
retry-with-linear-backoff on *any* download exception
(`download_with_retry`, 3 attempts) — this incidentally covers a 429, but
there's no explicit `Retry-After` handling or rate-limit-specific backoff. At
current weekly-cadence, low-request-count usage this is very unlikely to bite,
but it's not designed for it, only accidentally resilient to it.

---

## Phase 3 — Architecture

**End-to-end, one paragraph.** `scripts/download_data.py` pulls ~15 Socrata/OSM
sources into `data/raw/` (gitignored) with atomic per-file writes
(stream to a `.part` sibling, then `Path.replace()` — a crash mid-download
can't leave a truncated file `main.py` would read as complete). `main.py`
wires independently-runnable `src/` modules: load → normalize/join →
apply tax rates → aggregate by neighbourhood → compute per-acre metrics →
export slim GeoJSON/JSON to `web/data/`. Everything runs at **build time**
inside the CI job; the deployed artifact is static files only — no live
backend (`docs/security-audit.md` Scope update). `scripts/build_site.py`
fans `web/` into a two-build `_site/` (public root + `/full/` specialist);
`deploy.yml` publishes that to GitHub Pages.

**Last-known-good vs. direct overwrite.** Not a direct overwrite — there is a
staged, ordered guard sequence *before* anything is committed, all inside the
same `refresh.yml` job:
1. `check_unmatched_names.py` — new neighbourhood-name drift → **fail** (exit 5).
2. `check_year_alignment.py` — roll-year vs. pinned rate year → **hold** (exit 3: skip regen entirely, keep serving last-committed data + set a banner) or inconclusive-proceed (exit 4).
3. `main.py --skip-png` regenerates `web/data/*` — but only `if: steps.yearcheck.outputs.result != 'hold'`.
4. `check_value_anchors.py` (numeric bands) and `check_served_columns.py` (schema baseline) — **after** regeneration, judging the freshly-written artifact.
5. `run_verified_notebooks.py` — re-runs the real pipeline independently and asserts invariants.
6. `check_temporal_years.py --write-archive`.
7. Only *then*: commit + push.
8. `build_site.py`, then `verify-smoke.js` against the actual rendered `_site/` (both builds) — **gates `upload-pages-artifact`**, so a red render check leaves the previous good deploy live even though the data commit already landed.

A hard failure at any guard stops the job before the commit step runs (default
GitHub Actions `if: success()` on unguarded steps) — so no partially-regenerated
`web/data/` tree can reach `master`. This answers Phase 6's atomicity question
too; see there.

**Hosting/infra decisions.** GitHub Pages only — no CDN/object-storage choice
was ever in play for this project (`docs/PLAN_public_release.md` §2: *"no new
hosting, no new engineering"*, decided 2026-07-09). Two-build split
(public root + `/full/`) shares one `web/data/` tree; no separate database,
no serverless functions, no third-party analytics service.

**Known architectural debt.**
- ⚠️ Bikeway lifecycle capital rate still has no service-life figure Edmonton
  publishes (`TODO.md` open item) — a genuine data gap, not a code shortcut.
- Services-panel mobile confirmation is CONFIRMED for layout/overflow but
  **NOT CONFIRMED** for real touch interaction — verify scripts drive `.click()`,
  which bypasses `pointer-events` (a standing caveat, `docs/MOBILE_USABILITY.md`).
- ~~`ineligible_points`/`ineligible_value_frac` cardinality is tracked at ~72%
  of its guard band~~ — **RESOLVED 2026-09-03: there was no drift.** The trend
  was one step with an interpolated midpoint, it reverted on 2026-08-10, and
  the ~72%/83% readings came from a stale local `data/raw/`. `DECISIONS.md`
  2026-09-03. ⚠️ The debt it leaves is a different one, below.
- ⚠️ **No committed baseline in this repo ties its numbers to the run that
  produced them, except `expected_value_anchors.json` (since 2026-09-03).**
  `expected_columns.json`, `expected_temporal_years.json` and the
  `city_unit_costs.json` rates are the same shape — a pinned value whose
  provenance is a prose comment — and none was checked for the interpolated or
  stale-sourced row found in the anchors' own history.
- Historical assessment dataset (`qi6a-xuwt`) is catalogued but unused; 2024
  is a **known, deliberately-omitted** gap in the temporal lens (`SPEC_temporal.md`
  §0) — this is a documented decision, not an unnoticed hole.

---

## Phase 4 — Slices (per dataset)

Full detail lives in `data/DATA.md` (one numbered section per dataset, each
with its own "Known Quirks"). Condensed:

| Dataset | Ingest | Transform | Render | Special case |
|---|---|---|---|---|
| Assessment (`q7d6-ambg`) | ✅ | ✅ | ✅ | Condo units share one land parcel (expected); 46 zero-value rows dropped+logged; roll year is metadata-only |
| Property Info (`dkk9-cj3x`) | ✅ | ✅ | ✅ | No parcel polygons (Edmonton moved GIS to AltaLIS 2021) — point/centroid only |
| Neighbourhood Boundaries (`65fr-66s6`) | ✅ | ✅ | ✅ | 407 features; 1 assessment-side straggler (`OLIVER`, $500, deliberately unmapped), 1 boundary-side no-data (`LEWIS FARMS`) |
| Tax Rates (`pwis-wc4c`) | ✅ | ✅ | ✅ (mill-rate pod) | 2025 Farmland rate is an **assumption**, flagged live on the front end via `_assumed` key |
| Zoning (`fixa-tstc`) | ✅ | ✅ | ✅ | Geometry needs `buffer(0)` clean before overlay; categorization is an explicit 95-code dict, never keyword-matched |
| Road Network (`9j8t-zm52`) | ✅ | ✅ | ✅ | Null `functional_class_code` == alley+railway exactly; a new null defaults to `local` with a loud warning |
| Fire Events (`7hsn-idqi`) | ✅ | ✅ | ✅ | 57% medical-call share is an interpretive trap, caveated in UI copy by locked decision; hard-errors on a zero-row window year |
| Fire Stations (`b4y7-zhnz`) | ✅ | ✅ | ✅ | Context dots only |
| GTFS transit feed | ✅ | ✅ | ✅ | Snapshot of *current signup only* — no ridership data exists anywhere on the portal (probed, confirmed absent) |
| Building Permits (`24uj-dj8v`) | ✅ | ✅ | ✅ | 6 other portal datasets are saved views over the same source — deliberately ignored to avoid double-pulling |
| FIR Debt Series | ✅ | ✅ | not yet (lens unbuilt) | One historical unit slip (Strathcona County 2013, $000s) already caught + guarded |
| Off-Site Levy Catchments | ✅ | ✅ | ✅ | Boundaries are **advisory** per the bylaw itself — must be labelled approximated, not authoritative |
| City Service Unit Costs | hand-curated | ✅ | ✅ | 3 of 4 manually-entered figures independently verified against the City's budget portal (S94); one was wrong ~5× and has been corrected |
| Geographic Reference Layers (OSM) | ✅ | ✅ | ✅ | Overpass requires form-encoded POST + a named `User-Agent` or it 406s |
| Bike Routes | ✅ | ✅ | ✅ | — |
| Historical Assessment (`qi6a-xuwt`) | ❌ not wired into `download_data.py` | audit-only (`notebooks/exploration/03_historical_roll_gap.ipynb`) | ❌ | Known 2024 completeness defect (S75); confirmed **not** in the shipped pipeline |

---

## Phase 5 — Implementation Order / Consistency

**Same order every time?** Yes — `main.py` wires every module through one
fixed sequence (load → apply rates → aggregate → join/calculate → export),
and every dataset added since Phase 1 has slotted into that same shape
(`src/load_<name>.py` + `export_<name>_web` pattern — roads, bike, fire,
transit, permits all follow it). No dataset has its own bespoke pipeline
shape.

**Shared/generic code and blast radius.** The highest-leverage shared modules:
- `src/join_and_calculate.py` — the single join point (assessment × boundaries
  × zoning) computing both public metrics (`value_per_acre`, `revenue_per_acre`).
  A bug here is the single biggest blast radius in the codebase: it can be
  silently wrong for **every neighbourhood at once**, which is exactly why
  `docs/DATA_INTEGRITY.md` T3/T4/T5 rank it highest.
- `src/aggregate_by_neighbourhood.py` — one `groupby().sum()` that every
  revenue/value figure passes through.
- `scripts/generate_status.py` — feeds `status.json`, now also the source of
  truth for the on-screen mill-rate pod (`web/index.html`) since 2026-08-01;
  a bug here could show wrong rates without touching the map layer at all.
- `check_value_anchors.py` / `check_served_columns.py` — the two guards that
  would have to *also* be wrong for a shared-code bug to reach production
  undetected.

---

## Phase 6 — Testing (negative / silent-failure focus)

**Schema drift.** `src/load_assessment.py:53-66` renames raw Socrata column
names to internal ones via a dict; a **renamed** source column is a no-op
rename, and the subsequent `return df[[...]]` column-select then raises
`KeyError` on the missing internal name — **loud, not silent.** A **type**
change (e.g., a numeric field becomes a string) is caught similarly:
`.astype(float)` (`load_assessment.py:84`) raises on non-numeric content.
So the specific failure mode the template asks about — Socrata silently
renaming/retyping a field — already fails loudly here, confirming
`DATA_INTEGRITY.md`'s framing that residual risk is in *semantic* correctness
(right column, wrong meaning) rather than structural drift.

**Partial/mid-run failure.** Two layers: (1) `scripts/download_data.py`'s
`download()` writes to a `.part` sibling and only `Path.replace()`s it onto
the real destination on success — a truncated network stream can never look
like a complete raw file. (2) At the CI-job level, every regeneration/guard
step after "Download source data" runs unconditionally-on-success; the
"Commit regenerated data" step has **no `if:`**, so GitHub Actions' default
(`if: success()`) means a crash anywhere in `main.py` or a guard stops the
job *before* the commit step ever runs. **Net: a half-written `web/data/`
tree cannot reach `master`.** ⚠️ One caveat: `src/join_and_calculate.py:1077`
(`slim.to_file(output_path, driver="GeoJSON")`) writes the *served* files
directly, not via a temp-then-rename — but since a crash mid-`main.py` already
prevents the commit step from running (above), this only matters for a
process that crashes *after* every file finishes writing but *some other way*
still reaches git add, which doesn't happen in the current job shape. Not
exploitable today; would become one if the commit step's `if:` condition were
ever loosened.

**Neighbourhood matching.** Covered in depth in `docs/DATA_INTEGRITY.md` T3 —
LEFT join, warn-not-fail on unmatched names, `NAME_CORRECTIONS` dict
(`src/load_assessment.py:19-30`). ⚠️ Genuinely warn-only *in code*, but as of
2026-07-01 it also has a **committed baseline + hard CI fail** on any new
drift: `scripts/check_unmatched_names.py` against `data/expected_unmatched.json`
— so the residual risk this phase worries about (a warning scrolling past
unnoticed) is closed for the specific case of a *new* mismatch; it's open only
for a mismatch that's silently mapped *wrong* (T3(b) in `DATA_INTEGRITY.md`,
never fully audited).

**Field disambiguation (assessment vs. levy vs. revenue).** `Tax Class`
(clean 4-value field) is the sole join key to `mill_rates.json`
(`src/apply_tax_rates.py`); the parallel `Assessment Class 1/2/3` fields use a
*different* vocabulary and are used only for split-class apportionment (~0.25%
of rows). `docs/FINDINGS_assessment_classes.md` documents the full label→rate-class
map and confirms `Assessment Class 1` matches `Tax Class` in 100% of rows.
Tests exist (`tests/` — 564 passing as of last run) but this phase's specific
ask — "is there a test confirming the *right* field is used where expected" —
is answered by the FINDINGS doc's audit trail rather than a named unit test
asserting the join-key choice itself; ⚠️ worth flagging as thin if that
specific regression (accidentally joining on `Assessment Class 1` instead of
`Tax Class`) is a scenario worth a dedicated test.

**Double-counting.** `docs/DATA_INTEGRITY.md` T4 + the dedicated
S74/S86-era cardinality audits (`docs/FINDINGS_denominator_cardinality.md`,
`tools/audit_cardinality_denominators.py`) both concluded the neighbourhood
lens is **structurally immune**: the numerator sums one row per account (no
parcel-geometry join to double-count against), and multi-unit condos are
*separately assessed* accounts, so summing them is correct, not a duplicate.
Re-verified 2026-07-28 (S74) against a live snapshot — still holds.

**Null handling.** `load_assessment.py:76-82` drops null/zero
`assessed_value` rows explicitly, with a logged count (`logger.info`, not
silent). `src/join_and_calculate.py` similarly logs zero/NaN-area
neighbourhood drops at export. Nulls are **excluded**, never silently coerced
to a real-looking zero, in the paths audited so far.

**Rerun safety / idempotency.** No `datetime.now()`/`random`/`uuid` calls
found anywhere in `src/`, `main.py`, or the export scripts (checked) — output
is a pure function of input, so two runs against identical source data
produce byte-identical `web/data/*` (this is exactly what let the S86 audit
diff two refreshes cell-by-cell and prove "the data moved, the splice did
not"). The **one** intentionally-non-idempotent field is `status.json`'s
`last_checked`/`generated` heartbeat timestamps — by design, not a bug. ⚠️ Not
independently verified by a dedicated idempotency *test* (e.g., "run main.py
twice on frozen input, diff the outputs") — the S86 finding is empirical
evidence from one real refresh, not a standing regression test.

---

## Phase 7 — Review

**Explicit audit history exists and is tracked**, not ad hoc: `docs/AUDIT_LEDGER.md`
lists every executed audit run with date, scope, instrument, verdict, and what
remains outstanding. As of this snapshot: a full data-integrity pass
(2026-07-01, 5 bugs found and closed), pre-launch cardinality audit
(2026-07-08/09, structurally clean), a security + architecture audit
(2026-07-09, 1 Medium + informational findings, mostly resolved), two rounds
of a development/infill lens decision-stack audit (S48/S56), historical-data
completeness audits (S74, S75), a render-vs-data diff audit (S86), and a
manual-input verification audit against an independent budget source (S94,
caught a real ~5× error, corrected).

**Never independently reviewed (per `AUDIT_LEDGER.md`'s own "Never audited"
list, still current as of this doc unless noted):**
1. **Services/cost lens decision stack** — has build-time verification, never
   a top-down decision audit like the development lenses got. Ranked the
   ledger's own "biggest unaudited public claim surface."
2. **Residential-revenue metric + Glass grid columns** decisions (class
   composition, MA DERELICT exclusion, real-zero convention) — pipeline
   verified green, decisions themselves unaudited.
3. **Debt lens data series** — anchor-checked at build, no independent pass
   (low urgency, lens itself unbuilt).
4. ~~Refresh workflow end-to-end failure modes (operational logic, not
   supply chain)~~ — ⚠️ **this ledger entry is stale.** It's dated before the
   render-gate (`verify-smoke.js` in `refresh.yml`, closed 2026-08-02) and
   the schema-baseline guard (`check_served_columns.py`, closed 2026-08-03)
   existed. Those two close a real chunk of what that line worried about; the
   HOLD-path/banner-state logic and the January year-roll procedure itself
   are still un-adversarially-tested.
5. **Data-integrity RE-RUN on current schema** — the 2026-07-01 pass predates
   lot-acre columns, res_levy decomposition, value/res grids, and the
   services join.

---

## Phase 8 — Deploy & Observability

**How a silently-wrong number would be noticed.** Multiple independent layers,
in the order they'd actually catch something, from most to least automated:
1. `check_unmatched_names.py` / `check_year_alignment.py` / `check_value_anchors.py`
   / `check_served_columns.py` — each targets one *specific known* prior
   failure mode (see Phase 3's guard sequence). These fail the build loudly.
2. `run_verified_notebooks.py` — an independent re-derivation of the same
   numbers via a differently-shaped code path, asserting invariants.
3. `verify-smoke.js` — gates the actual rendered `_site/`, invariant-only
   (never a pinned value, deliberately, so it doesn't cry wolf on legitimate
   weekly data movement).
4. Below all of that: **a wrong number that isn't any of the above's named
   failure mode would currently only be caught by a human looking at the map
   and noticing it looks off** — same honest answer this template is designed
   to surface. The whole audit history in Phase 7 exists because that's true;
   each closed finding started as "a human noticed something."

**Run-level logging/summary.** Scattered, not centralized: individual modules
log row counts at key steps (`aggregate_by_neighbourhood.py:44` — "Aggregated
%d properties into %d neighbourhoods"; multiple `logger.info`/`logger.warning`
calls in `join_and_calculate.py` for drops/unmatched counts — 150 log calls
across `src/` total). ⚠️ There is **no single run-summary artifact** (e.g. a
committed `run_report.json` with before/after row counts, "X% dropped vs last
run") that a human or a script could scan without reading CI logs line by
line. The closest thing to "noise complaints dropped 90% since last run" is
`check_value_anchors.py`'s banded numeric checks — but those are pinned bands
on ~a handful of anchor values, not a general drop-detector across every
metric.

**Propagation lag.** GitHub Pages deploy lag (documented as a known quantity,
not measured fresh here) — `deploy.yml` runs after `refresh.yml`'s commit in
the same job graph; typical GitHub Pages propagation is on the order of
1-2 minutes. Not flagged anywhere as a live problem for this project's
cadence (weekly data, not real-time) — a consistency gap here would only
matter for someone hitting the site in the exact window between commit and
deploy completion, low-stakes for a weekly-refresh civic map.

---

## Summary — Top Risks

Ranked by (a) how silent the failure would be and (b) how much it would
matter, **not** by ease of fixing:

1. **A semantically-wrong-but-present mapping or column.** Every hard guard
   in this pipeline (`check_unmatched_names.py`, `check_value_anchors.py`,
   `check_served_columns.py`, class-mapping raise) catches *absence* or
   *out-of-band* values — none of them can tell a *present, plausible, wrong*
   value from a correct one. This is `DATA_INTEGRITY.md`'s own framing (§0)
   and remains the single highest-leverage residual risk: a new
   `ASSESSMENT_CLASS_TO_RATE_CLASS` entry, a new `NAME_CORRECTIONS` mapping,
   or a manually-curated cost figure (per S94, this already happened once —
   the roads figure was 5× wrong and lived on the public site until caught)
   pointed at a defensible-looking but incorrect target would ship clean.

2. **No general run-level drift summary.** Every guard targets a *named*
   prior failure. A genuinely novel failure mode — one nobody has hit yet —
   has no generic "row counts moved more than expected" tripwire; it falls
   through to "a human notices the map looks wrong" (Phase 8). Low cost to
   add (a committed before/after row-count + top-line-metric diff, informational
   not blocking), currently absent.

3. **The Services/cost lens decision stack has never had a top-down audit**
   (Phase 7, item 1) — it's the largest shipped public-claim surface that has
   only ever been build-verified, never decision-audited the way the
   development/infill lenses were (S48/S56). If a bad decision is baked in
   anywhere, this is the least-checked place it could be.

4. **Idempotency and mid-run atomicity are structurally true but not
   regression-tested.** The current guarantees (no `datetime.now()`/random
   anywhere; CI's default `if: success()` step-gating) hold *today* by the
   shape of the code, not by an explicit test that would catch a future
   change quietly breaking either property (e.g., someone adding a
   `continue-on-error: true` to a step, or a timestamp creeping into an
   export). Cheap to convert into a real test; currently only true by
   inspection.

5. **`AUDIT_LEDGER.md`'s own "Never audited" list can itself drift stale** —
   confirmed this session (item 4, the refresh-workflow line, was already
   half-resolved by two later fixes the ledger row didn't reflect). Not a
   pipeline risk, but a process one: the audit-coverage map needs the same
   "verify before trusting" discipline this project applies to everything
   else. Worth a line update in `AUDIT_LEDGER.md` itself as a follow-up.

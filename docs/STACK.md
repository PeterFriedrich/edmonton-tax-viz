# STACK — what this project is built out of

One page, current as of **2026-09-05**. Answers "what am I working with?" without
reading four other docs. **Versions here are the pinned ones**, not ranges —
if a number here disagrees with `requirements*.txt` or `web/vendor/README.md`,
those files are right and this is stale.

Related: `docs/ARCHITECTURE.md` (module interfaces + data flow — the *how*),
`docs/SPEC_deployment.md` (deploy design), `docs/security-audit.md` (supply
chain), `docs/PERFORMANCE.md` (render + boot cost).

---

## 1. The shape of it

**A Python batch pipeline that writes static files, and a single-file web map
that reads them.** No server, no database, no API of our own, no build step for
the front end. GitHub Actions runs the pipeline on a schedule and pushes the
result to GitHub Pages.

```
Socrata (data.edmonton.ca)  →  src/*.py  →  web/data/*.{geojson,json}  →  web/index.html
        raw CSV/JSON            pandas +        static artifacts            deck.gl + maplibre
                                geopandas
```

---

## 2. Python — the pipeline

**Python 3.12.13**, in `.venv/`. ⚠️ **The system `python` is 3.6.8** — always
invoke `.venv/bin/python` explicitly; a bare `python` will fail on modern syntax.

| package | version | role |
|---|---|---|
| `pandas` | 3.0.3 | every table |
| `geopandas` | 1.1.3 | spatial joins, dissolves, area |
| `shapely` | 2.1.2 | geometry ops (`buffer(0)` repair) |
| `pyogrio` | 0.12.1 | GeoJSON/shapefile I/O |
| `pyproj` | 3.7.2 | reprojection |
| `numpy` | 2.4.6 | numerics |
| `scipy` | 1.18.0 | spatial indexing / stats |
| `matplotlib` | 3.10.9 | Phase 1 static choropleths only |
| `requests` | 2.34.2 | Socrata fetches |
| `pytest` | 9.0.3 | tests |

⚠️ **`EPSG:3400` (NAD83 / Alberta 10-TM Forest) is the metric CRS everywhere.**
Set it explicitly before any `.area` call — `EPSG:4326` areas are degrees², which
produce wrong numbers and no error. `EPSG:26911` is a valid metric CRS but is
**not** used here and counts as an inconsistency if it appears.

### Two requirements files, and they are not interchangeable

- **`requirements.txt`** — the authoritative full-environment freeze (~130 pins),
  including JupyterLab for local exploration.
- **`requirements-ci.txt`** — the slim runner set. ⚠️ **Bump both in lockstep
  when a pipeline dependency changes**; the CI file re-pins the same versions
  rather than resolving its own.

⚠️ **`scikit-learn` (1.9.0) is in the freeze but deliberately NOT in CI.** It is
used by exactly one exploratory tool (`tools/ml_feature_importance.py`), never by
the pipeline. **Nothing in `src/`, `scripts/` or `main.py` may import it** — that
would break the scheduled refresh, and no test would catch it locally.

---

## 3. Front end — deliberately frameworkless

**No React, no bundler, no npm install to serve the site, no transpile step.**

- `web/index.html` — **~424 KB, ~7,345 lines**, hand-edited, markup + all the JS.
  Navigate it via `docs/CODEMAP.md` (generated symbol index, auto-refreshed by a
  `PostToolUse` hook) rather than scanning.
- `web/styles.css` — ~52 KB, all CSS (extracted 2026-07-29).

### Vendored, not CDN-loaded

| file | package | version |
|---|---|---|
| `web/vendor/deck.gl-9.0.38.min.js` | deck.gl | 9.0.38 |
| `web/vendor/maplibre-gl-4.7.1.js` | maplibre-gl | 4.7.1 |
| `web/vendor/maplibre-gl-4.7.1.css` | maplibre-gl | 4.7.1 |

⚠️ **Vendoring is a security decision, not a convenience one** (`security-audit.md`
S1): every displayed dollar figure executes through these libraries, so a
compromised CDN could silently alter civic numbers. SHA-256s are recorded in
`web/vendor/README.md` and were cross-verified against two independent CDNs.
**Never point a `<script src>` back at a CDN without SRI.**

**No basemap tiles** — the map draws on a flat dark backdrop, so the page has no
runtime third-party network dependency at all.

### The one build step

`scripts/build_site.py` fans the single hand-edited `web/index.html` into the
two-build Pages tree: `/` (public, curated) and `/full/` (specialist,
everything), by rewriting a `DEFAULT_BUILD` literal. ⚠️ It is **not** in the
served tree, so `deploy.yml` lists it explicitly as a trigger path.

---

## 4. Data sources

All Edmonton Open Data (Socrata, `data.edmonton.ca`), fetched over HTTPS at run
time — the pipeline does **not** read `data/raw/` for the audit tools.

| resource | what |
|---|---|
| `q7d6-ambg` | Property Assessment Data — current year (the live roll) |
| `qi6a-xuwt` | Property Assessment Data — historical, 2012–2025 |
| plus | property info, zoning, roads, permits, fire, GTFS transit, bike, schools |

Full per-source detail, column names and quirks: **`data/DATA.md`** — read it
before touching any data file. Known upstream defects: `docs/DATA_ISSUES.md`.

⚠️ **HTTPS from the Oracle box needs `certifi`** — the system CA bundle is stale
and missing post-2021 roots, so a "host unreachable"/000 here is usually local:

```bash
REQUESTS_CA_BUNDLE=$(.venv/bin/python -m certifi) .venv/bin/python <script>
```

---

## 5. Testing

**Two independent harnesses.**

- **pytest** — 45 test files, **784 tests**, ~11 s. Tiers and what each can see:
  `docs/ARCHITECTURE.md` §Testing.
- **Playwright + Chromium** — `tools/profiling/`, **65 JS scripts** (`verify-*`
  assert behaviour, `shot-*` capture screenshots). Node **v20.20.2**,
  `playwright ^1.61.1`.

⚠️ **Playwright is installed only in `tools/profiling/node_modules`** — a script
in `/tmp` cannot `require('playwright')`. Put the script in that directory.

⚠️ **Run verify scripts ONE AT A TIME.** Concurrent runs manufacture failures on
this 4-core box and corrupt every timing. Check `ps aux | grep -c "[c]hrome"` and
`/proc/loadavg` before trusting a red or a number.

⚠️ **This box has no GPU** — `ANGLE (… SwiftShader driver)`, software WebGL. Use
it for A/B comparison only; never read an absolute render or boot timing off it
(`docs/PERFORMANCE.md`).

Doc integrity has its own guard: `scripts/check_doc_citations.py`.

---

## 6. Notebooks

`jupytext` 1.19.5 + `nbconvert` 7.17.1 + `ipykernel` 7.2.0. Sources are `.py`
(jupytext light format), not `.ipynb`, so they diff cleanly.

- **`notebooks/verified/`** — gate the weekly publish; run in `refresh.yml`.
  See `docs/VERIFICATION.md`.
- **`notebooks/standalone/`** — the published evidence reports behind
  `docs/DATA_ISSUES.md`. See `docs/EVIDENCE_NOTEBOOKS.md`. ⚠️ Nothing re-runs
  these on a schedule, by decision (`DECISIONS.md` 2026-08-29).

---

## 7. CI/CD — four GitHub Actions workflows

| workflow | trigger | does |
|---|---|---|
| `tests.yml` | every PR + push to `master` | pytest, plus the two **static repo guards** that need no network — `check_doc_citations.py` and `check_cost_copy.py` (blurb rates vs `city_unit_costs.json`). **The required check is the job id `test`**, not the workflow name |
| `deploy.yml` | push to `master` touching site code | rebuild + deploy Pages. Excludes `web/data/**` (the refresh run already deployed it) |
| `refresh.yml` | weekly, Mon 08:00 UTC + manual | download → `main.py` → guards → verified notebooks → commit data → deploy |
| `vintage-digest.yml` | monthly, 1st at 14:00 UTC | files the vintage/pin digest issue. `RUNBOOK.md` §0 |

**Hosting: GitHub Pages.** Static artifact, gzipped by Pages,
`cache-control: max-age=600`.

⚠️ **`master` is branch-protected** (since 2026-08-29). Force-push and deletion
are blocked as a side effect. ⚠️ **A failed deploy after a `web/**` merge is
silent** — check `gh run list`.

---

## 8. Repo layout

| path | count | what |
|---|---|---|
| `src/` | 22 modules | the pipeline; each independently runnable |
| `scripts/` | 25 | guards, site build, status generation |
| `tools/` | 16 py + 65 js | audits + the headless harness |
| `tests/` | 45 files | pytest |
| `docs/` | 61 | specs, findings, decisions, runbook |
| `web/` | — | the served site |
| `data/raw/`, `data/processed/` | — | local snapshots; **never `Read` these** (`docs/TOKEN_EFFICIENCY.md`) |

---

## 9. What this project deliberately does NOT use

Recorded so nobody proposes them as improvements without reopening a decision.

- **No GIS desktop software** (QGIS/ArcGIS) — Python-only, by project rule.
- **No database** — static files are the interface.
- **No front-end framework, and no JS toolchain in the publish path** — one
  hand-edited HTML file. ⚠️ **The ES-module split was DECIDED AGAINST on
  2026-09-05** (`DECISIONS.md`; `docs/FINDINGS_frontend_architecture_verdict.md`):
  the file stays one file, with three re-open triggers — do not re-propose it on
  size alone. `scripts/build_site.py` is a build step (stdlib, no JS); a bundler
  is what the rule forbids.
- **No CDN at runtime** — see §3.
- **No CSS preprocessor**, no TypeScript. A **read-only** JS checker in
  `tests.yml` (`tsc --checkJs --noEmit` or eslint — emits nothing to `_site/`)
  is **allowed since 2026-09-05** (`DECISIONS.md`) but **not yet installed**;
  S1 constrains what executes on the page, not what reads the source.

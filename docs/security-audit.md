# Security Audit: Edmonton Revenue Per Acre

Post-implementation review checklist for a Python data pipeline producing a static map from public data. Scope is appropriate for the threat model: a local analysis tool with no web exposure, no auth, and no private data.

> **Scope update (2026-07-09 audit):** the paragraph above is Phase-1 vintage. The
> project now has a public surface: a weekly GitHub Action
> (`.github/workflows/refresh.yml`) downloads the open-data inputs, runs
> `main.py --skip-png`, commits the regenerated static files under `web/data/`,
> and deploys `web/` to GitHub Pages. **All Python executes at build time** —
> the deployed site is static files only; there is no live service, endpoint,
> or runtime backend anywhere. The expanded surface is therefore: (1) what the
> published static output contains, (2) the CI workflow's supply chain and
> write permissions, (3) the browser page's own dependencies and rendering of
> data-derived strings, and (4) ingest integrity (bad source data becoming
> published "fact"). Findings for that surface are in the
> **Findings — 2026-07-09** section below.

---

## Threat Model

| Asset | Risk | Likelihood |
|-------|------|------------|
| Raw assessment CSV | Contains property owner info if not stripped | Medium |
| Output map | Aggregated by neighbourhood — low sensitivity | Low |
| Pipeline code | Runs locally, no network exposure | Low |
| Dependencies | Supply chain risk via PyPI | Medium |

This is not a web app. There is no auth surface, no database, and no user-supplied input at runtime. The main risks are data handling (what ends up in processed files or logs) and dependency integrity.

*(2026-07-09: see Scope update above — "no web exposure" no longer holds for the
Pages site + CI, though "no runtime input / no auth surface" still does.)*

---

## Checklist

Verified 2026-07-09 (full-repo audit pass; evidence inline).

### Data Handling

- [x] **No PII in processed outputs** — published files verified aggregate-only:
  `web/data/neighbourhood_value_per_acre.geojson` carries exactly the 24
  neighbourhood-level `SLIM_COLUMNS` props; `value_grid.json` is 100 m cell sums;
  `roads.geojson`/`zoning.geojson` carry `n/t/v` / `u` display props only;
  `fire_stations.json` is 31 public station points. `data/processed/` is empty +
  gitignored. Raw address columns (house/street) are dropped at
  `load_assessment.py`'s explicit column select (src/load_assessment.py:86-92);
  the source dataset has no owner-name field.
- [x] **No PII logged to stdout** — all flagging paths log counts and
  neighbourhood names only (e.g. src/load_assessment.py:74,81;
  src/join_and_calculate.py:160-165; export drop-list logs hood names,
  src/join_and_calculate.py:514-520). No module logs individual records,
  account numbers, or coordinates.
- [x] **`data/raw/` is in `.gitignore`** — `.gitignore:30` (`data/raw/*` with a
  `.gitkeep` exception); `git ls-files` confirms nothing under `data/raw/` is
  tracked.
- [x] **`output/` is in `.gitignore`** — `.gitignore:34`.
- [x] **`data/processed/` is in `.gitignore`** — `.gitignore:32`.

### Dependency Integrity

- [x] **`requirements.txt` pins exact versions** — every line in both
  `requirements.txt` (full dev freeze) and `requirements-ci.txt` (the 9-package
  set the publishing workflow installs) is `==`-pinned.
- [x] **Dependencies are from well-known maintainers** — CI set is
  geopandas/shapely/pandas/numpy/matplotlib/pyogrio/pyproj/requests/pytest, all
  mainstream. The dev freeze adds the standard Jupyter toolchain; no unfamiliar
  packages.
- [x] **No `pip install` in code** — grep of `src/`, `scripts/`, `main.py`,
  `tests/` is clean.
- [x] **`pip-audit` run (2026-07-09)** — `requirements-ci.txt`: **no known
  vulnerabilities** (this is the set that runs in the publishing pipeline).
  `requirements.txt` (local dev only): 11 known vulnerabilities in 5 packages,
  all in the notebook toolchain, none in the publish path — see finding S5.

### File Path Handling

- [x] **No path traversal risk** — all input/output paths are constants at the
  top of `main.py` (main.py:49-65) or argparse `Path` defaults; the CI workflow
  invokes `python main.py --skip-png` with no external path input. No path is
  built from data-file contents.
- [x] **No shell execution** — grep for `subprocess|os.system|eval(|exec(|__import__`
  across `src/`, `scripts/`, `main.py`, `tests/` is clean.
- [x] **Output directory is created safely** — `pathlib.Path.mkdir(parents=True,
  exist_ok=True)` (main.py:236,240; scripts/download_data.py:198).

### Code Quality (Security-Relevant)

- [x] **No `pickle` usage** — grep clean; intermediates are CSV/GeoJSON/JSON only.
- [x] **No `eval` or `exec`** — grep clean (Python). The web page uses no
  `eval`/`new Function`; its two `innerHTML` legend writes use hardcoded
  strings only (web/index.html:1520,1563) — but see finding S3 for the tooltip.
- [x] **Exception handling doesn't swallow errors silently** — no bare
  `except: pass` anywhere. The three broad `except Exception` blocks are
  deliberate, documented soft-fails that log and degrade
  (scripts/download_data.py:155,230,269; scripts/check_year_alignment.py:158);
  data-shape errors in the pipeline itself raise (e.g. unmapped tax class,
  src/apply_tax_rates.py:64,80).

---

## Findings — 2026-07-09 (Phase-2 public surface)

Full-repo pass against the checklist above plus the build-time/static-site
surface. Ranked by severity. Per the session brief these are logged, not fixed.

### S1 (Medium) — CDN scripts loaded without subresource integrity
`web/index.html:8-10` loads `maplibre-gl@4.7.1` (JS + CSS) and
`deck.gl@9.0.38` from unpkg.com with pinned versions but **no `integrity`
attributes** (`grep -c integrity= web/index.html` → 0). The entire page —
including every displayed dollar figure — runs through these libraries, so a
compromised CDN or package release could silently alter the civic numbers the
site presents, which is exactly the harm class this project cares about.
**Suggested fix:** add SRI hashes + `crossorigin="anonymous"`, or better,
vendor the three files into `web/vendor/` (repo already commits ~5 MB of data;
this removes the third-party runtime dependency entirely and makes the site
fully self-contained on Pages).

**RESOLVED 2026-07-12.** Vendored all three files into `web/vendor/`
(`maplibre-gl-4.7.1.{js,css}`, `deck.gl-9.0.38.min.js`) and pointed
`web/index.html` at the local copies — no CDN `<script src>` remains
(`grep -cE 'unpkg|jsdelivr' web/index.html` → 0). Downloaded from unpkg and
cross-verified byte-for-byte against jsdelivr (two independent CDNs, identical
SHA-256); provenance + hashes recorded in `web/vendor/README.md`. The basemap
style is `sources: {}` (a solid background, no external tiles), so the live site
now has **zero external runtime dependencies**. Headless-verified: the map still
renders (`verify-transit.js` 24/24 against the vendored build).

### S2 (Low) — previously-scrubbed content still present in tree + history
Content the project owner scrubbed from the repo on 2026-07-09 (see
`session-summary/2026-07-09.md` §B) is still present in two places: the same
handoff's own verbatim quote (§B first bullet), and the pre-scrub commit
`da86117`, permanently reachable in public history via merge `5cf3d24`. The
handoff already records the history residual as known/low-stakes; the verbatim
quote in the handoff itself appears to be an oversight of the same scrub.
**Suggested fix:** reword that quoted line in the committed handoff (content
change is the owner's call, per the standing rule; not applied by this audit).
Rewriting public history for `da86117` remains the owner's decision —
previously judged low-stakes.

### S3 (Low) — data-derived strings interpolated into tooltip HTML unescaped
`web/index.html:1349` builds tooltip HTML with
`` `<b>${p.neighbourhood_name}</b>` `` (plus `set_aside_reason` at :1393,1411)
via deck.gl's `html:` tooltip. These strings originate in the upstream
open-data portal and flow to the page through the weekly auto-refresh — so a
vandalized/compromised upstream neighbourhood name containing markup would
execute in visitors' browsers. Impact is bounded (static site: no cookies,
auth, or storage to steal — defacement/redirect risk), and the value would
also have to survive the pipeline's normalization, but it is a genuine
untrusted-data → HTML sink on a public site. **Suggested fix:** one small
escape helper (`&<>"'` entity replacement) applied to the two data-derived
strings in `tooltipFor`.
**RESOLVED (2026-07-12):** added an `esc()` helper (`&<>"'` → entities) just
above `tooltipFor` in `web/index.html`; applied to both data-derived strings —
`neighbourhood_name` (the `name` prefix) and `set_aside_reason` (its two sites).
Every other tooltip interpolation is a formatted number or code-defined config
label, not upstream data. Headless verify (`verify-transit.js`) 24/24 green.

### S4 (Low) — workflow actions pinned by mutable tag, not commit SHA
`refresh.yml` pins `actions/checkout@v7`, `setup-python@v6`,
`upload-pages-artifact@v5`, `deploy-pages@v5` by tag. Tags are mutable; the
job holds `contents: write` + `id-token: write` + `pages: write`, so a
compromised action could push to master and publish to the site. This is the
standard supply-chain hardening gap, not an observed weakness — the
permissions block is otherwise least-privilege, concurrency is guarded, and
the banner output is passed via `env:` (no expression-injection sink).
**Suggested fix:** pin each action to its full commit SHA (comment the tag
alongside); GitHub's Dependabot keeps SHA pins updated.
**RESOLVED (2026-07-12):** all four actions in `refresh.yml` now pinned to full
commit SHA with the release version in a trailing comment —
`actions/checkout@9c091bb…` (v7.0.0), `setup-python@ece7cb06…` (v6.3.0),
`upload-pages-artifact@fc324d35…` (v5.0.0), `deploy-pages@cd2ce8fc…` (v5.0.0).
SHAs resolved via the GitHub API at pin time. A `github-actions` Dependabot
config to auto-bump the pins was left out deliberately (it opens recurring PRs —
owner's call); bump the pins by hand when an action releases a new version.

### S5 (Low) — known CVEs in the local dev freeze (not the publish path)
`pip-audit -r requirements.txt --no-deps` (2026-07-09): 11 known
vulnerabilities in 5 packages — `tornado 6.5.5` (4, fix 6.5.6/6.5.7),
`bleach 6.3.0` (3, fix 6.4.0), `soupsieve 2.8.3` (2, fix 2.8.4),
`jupyter-server 2.18.2` (fix 2.20.0), `jupyterlab 4.5.7` (fix 4.5.9). All are
in the Jupyter/notebook toolchain used only for local exploration;
**`requirements-ci.txt` — the set installed by the publishing workflow — is
clean.** **Suggested fix:** bump those five pins next time the dev env is
touched; consider adding a `pip-audit -r requirements-ci.txt` step to
`refresh.yml` so the publish path stays continuously checked.

**RESOLVED (2026-07-12, P2.3c):** bumped all five pins in `requirements.txt`
(`tornado→6.5.7`, `bleach→6.4.0`, `soupsieve→2.8.4`, `jupyter_server→2.20.0`,
`jupyterlab→4.5.9`). A fresh `pip-audit` at fix time surfaced a sixth, newer
CVE in the same dev-only toolchain — `mistune 3.2.1` (CVE-2026-49851) — bumped
to `3.3.0` as well. `pip-audit -r requirements.txt --no-deps` now reports **no
known vulnerabilities**. Added a **non-blocking** `pip-audit -r requirements-ci.txt`
step to `refresh.yml` (after "Install dependencies") so the publish path stays
continuously checked; kept `continue-on-error: true` so a future CVE surfaces as
a workflow warning without halting the unattended data refresh (drop that flag
to make it a hard deploy gate).

### S6 (Informational) — dev-environment details in committed docs
Committed session summaries (`session-summary/*.md`) and `CLAUDE.md` reference
absolute dev-box paths (`/home/opc/...`) and the hosting box's identity
("Oracle box"). No credentials, hostnames, or addresses are exposed, and the
box serves nothing for this project (the site is on GitHub Pages), so this is
noted for awareness only. If session summaries keep accumulating in a public
repo, treat them as public-facing text when writing them.

### Verified strengths (ingest / data-integrity, brief §2)
The "could a bad source file silently corrupt published numbers" surface is
the best-defended part of the repo — recorded so it isn't re-audited from
scratch:
- **Download integrity:** HTTPS to `data.edmonton.ca` only; atomic `.part`
  temp-file writes (no truncated file readable as complete,
  scripts/download_data.py:204-211); dual truncation guards — own-`$limit`
  check + live `count(*)` cross-check, mismatch fails hard
  (scripts/download_data.py:160-193).
- **Year alignment:** `check_year_alignment.py` compares Socrata metadata year
  vs the `ASSESSMENT_YEAR` pin vs `mill_rates.json`; mismatch → CI **holds**
  (keeps serving last committed data, sets visitor-facing banner) rather than
  publishing wrong-rate revenue numbers (refresh.yml:52-78).
- **Tests gate regeneration:** `pytest` runs before download/regen in CI
  (refresh.yml:41-42).
- **In-pipeline guards:** hard error on unmapped tax class
  (src/apply_tax_rates.py:80), conservation guards (roads overlay totals, grid
  cell sums), lot-acre physical-bound check that raises on new violations
  (src/export_value_grid.py:303), no-silent-drop logging throughout.
- **Provenance:** `web/data/status.json` publishes data/rate/zoning years,
  generation date, and the served GeoJSON's SHA-256.

**Accepted risks (deliberate, documented):** the `count(*)` cross-check and
the year-alignment metadata fetch both fail SOFT (warn + proceed) so the
guards can't take the pipeline down — availability-over-strictness tradeoffs
recorded in their docstrings.

---

## Audit Prompts for AI-Assisted Review

Use these prompts with Claude to get a focused security review after implementation is complete.

### Prompt 1: Data exposure check
```
Read all files in src/ and tests/. Identify any place where individual property 
records, owner names, or addresses could appear in stdout, log output, or 
processed files. The pipeline should only surface neighbourhood-level aggregates 
in its outputs — flag any deviation.
```

### Prompt 2: Dependency review
```
Read requirements.txt. For each dependency: confirm it is a well-known package 
with active maintenance, flag any unpinned versions, and note if any package has 
known CVEs. Suggest running pip-audit if not already in the workflow.
```

### Prompt 3: File path and shell safety
```
Read all files in src/ and main.py. Check for: path traversal risks (paths 
constructed from external input), any subprocess or os.system calls, any eval 
or exec calls, and any use of pickle for intermediate file storage. Report 
findings with file and line number.
```

### Prompt 4: Full pipeline audit
```
Read ARCHITECTURE.md, then read all files in src/. For each module, verify that 
its implementation matches its documented contract (inputs, outputs, 
responsibilities, "does not" boundaries). Flag any module that does something 
outside its documented scope, particularly any that touch the filesystem, 
network, or shell unexpectedly.
```

---

## Notes

- This checklist is scoped to Phase 1 (local static pipeline). A web-facing version would require a significantly expanded audit covering OWASP Top 10, content security policy, and rate limiting. *(2026-07-09: the web-facing surface now exists and is covered by the Findings section above — note that OWASP Top 10 / rate limiting largely don't apply to a static Pages site with no endpoints; CSP would still be a reasonable hardening add-on alongside S1.)*
- Property assessment data from Edmonton Open Data is public, but the raw CSV may include fields not needed for this analysis (owner name, mailing address). Strip these columns in `load_assessment.py` and confirm they are absent from all downstream outputs. *(2026-07-09: verified — explicit column select at src/load_assessment.py:86-92; no owner-name field exists in the source.)*

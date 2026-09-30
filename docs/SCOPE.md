# SCOPE — what this project deliberately does not do

The one hand-kept input to the Claude web brief (`scripts/make_brief.py`, setup
in `docs/CLAUDE_WEB.md`). Everything else in the brief is generated from files
the repo already maintains; this is the list an outside reviewer can't derive —
ideas that were considered and turned down, so they stop coming back as
recommendations.

One bullet each: **the thing**, then why not, and a pointer if a decision row
or doc holds the argument. A turned-down idea that has a locked decision needs
no bullet here — the brief already carries `docs/DECISIONS.md`.

Seeded 2026-09-30 from `docs/STACK.md` §9; add to it when an idea is turned down.

## Out of scope

- **GIS desktop software** (QGIS/ArcGIS) — Python-only, by project rule.
- **A database** — static files are the interface.
- **A front-end framework, bundler or JS toolchain in the publish path** — one hand-edited HTML file; the ES-module split was decided against on 2026-09-05 (`docs/FINDINGS_frontend_architecture_verdict.md`), don't re-propose it on size alone.
- **A CDN at runtime** — `docs/STACK.md` §3.
- **A CSS preprocessor or TypeScript** — a read-only JS checker in CI is allowed, nothing that emits to the site.
- **Parcel-level output** — the unit is the neighbourhood; parcel polygons are licensed, not open data (`docs/PARCEL_LEVEL_OPPORTUNITIES.md`).
- **Regional comparison (St. Albert, Strathcona, other municipalities)** — moved to the sibling repo `alberta-regional-viz`.

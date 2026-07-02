# Claude Instructions

## Project
Edmonton revenue-per-acre fiscal analysis. Python-only, no GIS software.

## Key Files
- `TODO.md` — living backlog: the authoritative list of what's left. Read it to know what to work on; update it in place as items open/close. Session summaries narrate *what happened*; TODO.md owns *what's left*.
- `docs/SPEC_phase1.md` — what we're building and why
- `docs/SPEC_services.md` — services lens (cost side; roads first): metric, filters, locked decisions, build order
- `docs/ARCHITECTURE.md` — module interfaces, data flow, testing approach. **Read before writing any module.**
- `data/DATA.md` — data source details, column names, known quirks. **Read before touching any data files. Update if you discover anything new.**
- `docs/TOKEN_EFFICIENCY.md` — context/token hygiene (what NOT to read raw, session-summary archiving). **Read before bulk-reading data or summaries.**
- `docs/ANALYSIS_BACKLOG.md` — analytical questions/investigations to run later (auto + by-hand). Distinct from TODO.md (build work) and FINDINGS_*.md (conclusions).
- `docs/PARCEL_LEVEL_OPPORTUNITIES.md` — future work gated on parcel-level data (finer than the neighbourhood unit); the set-aside machinery exists because we aggregate to neighbourhood.
- `docs/DATA_INTEGRITY.md` — standalone audit brief for checking the numbers are *right* (silent-correctness, not crashes). Point a model here for a full data-integrity pass: system map + ranked, pre-verified joints. Complements the `edmonton-audit` skill (which goes deep on ONE target).
- `session-summary/` — session handoff notes. Read the latest before starting work; older ones live in `session-summary/archive/` (don't bulk-read them).

## Token Efficiency
- **Never `Read` raw `.geojson`/`.csv` data files** — the zoning GeoJSON alone is ~2.3M tokens. Inspect via a small python/geopandas summary instead. See `docs/TOKEN_EFFICIENCY.md`.
- Read only the **latest** session summary; keep the 3 most recent at top level, archive older.

## Session Management
- Always run `/handoff` before `/clear` — never wipe context without a written record in `session-summary/`

## Code Style
- Keep processing steps as separate, independently runnable modules in `src/`
- No silent data drops — flag unmatched or missing records explicitly
- Always set CRS explicitly before any area calculation

## Deployment Horizon
- Configurable paths over hardcoded ones
- Structured output over print statements for logging
- Clean module boundaries so rendering can be swapped out later

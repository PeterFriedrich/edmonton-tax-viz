# Claude Instructions

## Project
Edmonton revenue-per-acre fiscal analysis. Python-only, no GIS software.

## Development Pipeline

Work follows this sequence — do not skip steps:

1. **Spec** (`SPEC_phase1.md`) — what to build and why
2. **Architecture** (`ARCHITECTURE.md`) — module contracts, data flow, key decisions
3. **Implementation** — one module at a time, in data flow order
4. **Tests** — per module in `tests/`, using synthetic data only
5. **Security audit** (`docs/security-audit.md`) — post-implementation review checklist

See `CONTRIBUTING.md` for the full contributor guide including AI-assisted workflow notes.

## Key Files
- `SPEC_phase1.md` — what we're building and why
- `ARCHITECTURE.md` — module interfaces, data flow, testing approach. **Read before writing any module.**
- `CONTRIBUTING.md` — full dev pipeline, AI workflow notes, project structure
- `docs/security-audit.md` — post-implementation security checklist and audit prompts
- `data/DATA.md` — data source details, column names, known quirks. **Read before touching any data files. Update if you discover anything new.**

## Code Style
- Keep processing steps as separate, independently runnable modules in `src/`
- No silent data drops — flag unmatched or missing records explicitly
- Always set CRS explicitly before any area calculation

## Data
Raw data files are not committed. See `data/DATA.md` for what to expect and where to get it.

# Claude Instructions

## Project
Edmonton revenue-per-acre fiscal analysis. Python-only, no GIS software.

## Key Files
- `docs/SPEC_phase1.md` — what we're building and why
- `docs/ARCHITECTURE.md` — module interfaces, data flow, testing approach. **Read before writing any module.**
- `data/DATA.md` — data source details, column names, known quirks. **Read before touching any data files. Update if you discover anything new.**
- `session-summary/` — session handoff notes. Read the latest before starting work.

## Code Style
- Keep processing steps as separate, independently runnable modules in `src/`
- No silent data drops — flag unmatched or missing records explicitly
- Always set CRS explicitly before any area calculation

## Deployment Horizon
- Configurable paths over hardcoded ones
- Structured output over print statements for logging
- Clean module boundaries so rendering can be swapped out later

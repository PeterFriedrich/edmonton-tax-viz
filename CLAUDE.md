# Claude Instructions

## Project
Edmonton revenue-per-acre fiscal analysis. Python-only, no GIS software.

## Key Files
- `SPEC_phase1.md` — what we're building and why
- `data/DATA.md` — data source details, column names, known quirks. **Read before touching any data files. Update if you discover anything new.**

## Code Style
- Keep processing steps as separate, independently runnable modules in `src/`
- No silent data drops — flag unmatched or missing records explicitly
- Always set CRS explicitly before any area calculation

## Data
Raw data files are not committed. See `data/DATA.md` for what to expect and where to get it.

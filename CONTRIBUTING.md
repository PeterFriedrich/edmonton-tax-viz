# Contributing

## Overview

This is a Python data pipeline that produces a static choropleth map of Edmonton assessed value per acre by neighbourhood. All inputs are publicly available; no GIS software is required.

---

## Development Pipeline

Work follows this sequence. Do not skip steps — each one informs the next.

| Step | Artifact | Purpose |
|------|----------|---------|
| 1. Spec | `docs/SPEC_phase1.md` | Defines what to build, inputs/outputs, and acceptance criteria |
| 2. Architecture | `docs/ARCHITECTURE.md` | Defines module contracts, data flow, and key technical decisions |
| 3. Implementation | `src/*.py` | One module at a time, in data flow order |
| 4. Tests | `tests/*.py` | Per module, using synthetic data only |
| 5. Security audit | `docs/security-audit.md` | Post-implementation review checklist |

For new phases, start at step 1 and write a new spec before touching any code.

### AI-assisted workflow

This project uses Claude Code (Claude Sonnet) as a coding assistant. The pipeline above was designed to work well with AI assistance:

- **Spec first** — a written spec gives the AI unambiguous scope. Without it, the AI will fill gaps with assumptions.
- **Architecture before implementation** — the architecture doc defines module interfaces explicitly. This prevents the AI from making different design decisions across separate conversations.
- **One module at a time** — ask the AI to implement one module, review it, then move to the next. Batching modules increases the chance of cross-module inconsistencies.
- **Tests alongside each module** — ask for tests immediately after each module, while the design intent is still fresh in context.
- **CLAUDE.md is the AI's working memory** — if you establish a convention, add it there so it persists across sessions.

---

## Getting Started

### Prerequisites

- Python 3.10+
- `pip install -r requirements.txt`

### Data

Raw data files are not committed. See `data/DATA.md` for sources and download instructions.

Expected files before running:

```
data/raw/property_assessment.csv
data/raw/neighbourhoods.geojson   # or .shp
```

### Running

```bash
python main.py
```

Output is written to `output/edmonton_value_per_acre.png`.

Each processing step can also be run and inspected independently:

```bash
python -c "from src.load_assessment import load_assessment; print(load_assessment('data/raw/property_assessment.csv').head())"
```

### Running Tests

```bash
pytest tests/
```

Tests use synthetic data only — no real data files needed.

---

## Code Conventions

- **One file per processing step** in `src/` — each module is independently runnable
- **No silent data drops** — flag unmatched or missing records explicitly to stdout (count + examples)
- **CRS before area** — always set and reproject CRS explicitly before any area calculation; never assume input CRS is suitable
- **No hardcoded paths** — file paths are constants defined at the top of `main.py`, passed down as arguments
- **No analysis logic in `plot_choropleth.py`** — rendering only

---

## Project Structure

```
/
├── data/
│   ├── raw/                  # Downloaded inputs — not committed
│   ├── processed/            # Intermediate outputs from each step
│   └── DATA.md               # Source details, column names, known quirks
├── docs/
│   └── security-audit.md     # Post-implementation security review
├── src/
│   ├── load_assessment.py
│   ├── aggregate_by_neighbourhood.py
│   ├── load_boundaries.py
│   ├── join_and_calculate.py
│   └── plot_choropleth.py
├── tests/
│   └── test_*.py
├── output/                   # Final map image(s) — not committed
├── main.py
├── requirements.txt
├── SPEC_phase1.md
├── ARCHITECTURE.md
├── CLAUDE.md
└── README.md
```

# Analysis Backlog

Analytical questions and investigations to run later — distinct from `TODO.md`
(which owns *build* work) and the `FINDINGS_*.md` docs (which record *conclusions*).
An item graduates out of here when it's either built (→ TODO) or answered (→ FINDINGS).
Each entry notes whether the work is **auto** (a script/query surfacing candidates)
or **by hand** (human eyeballing / spot-check), since most need both.

Items whose value is gated on **parcel-level** data (finer than our neighbourhood unit)
live in `PARCEL_LEVEL_OPPORTUNITIES.md` — several items below have a parcel-level angle
noted there.

_Started 2026-07-01._

---

## 1. Do the performance tails match the land-use classification? (outlier audit)

**Observation.** Some of the highest revenue/acre performers sit well out on the
city **outskirts**, which is counterintuitive — you'd expect the core to dominate.
Suspicion: several are **mixed-use** (currently classified `nonres`) or otherwise
sit in a category that doesn't match what's actually there. Conversely, there's a
cluster of **weak performers inside the non-residential group** that also needs
explaining. Both tails need assessing, and the classification is what's on trial.

**Why it matters.** Validates the `res`/`nonres`/`inst`/set-aside split (`load_zoning.py`)
against real fiscal behaviour. A top performer in the wrong bucket, or a systematic
weak-performer pattern in `nonres`, would mean the categories need refining (e.g.
mixed-use may deserve its own treatment rather than folding into `nonres`).

**Approach — auto:**
- Surface **top-N and bottom-N** by `revenue_per_acre` *and* `value_per_acre`, each
  row annotated with: zoning composition (`frac_residential`/`frac_nonres`/`frac_inst`/
  `set_aside_frac`), dominant zone code(s) + description, `is_set_aside`/`is_residential`,
  and a location signal (distance from centre / core-vs-outskirts).
- Flag likely **mixed-use** hoods explicitly (MU/MUN/CMU/RMU and DC sites) — they're
  the prime suspects for the outskirts-high-performer surprise.
- Look for a **low-acre denominator** effect: a single large-value parcel in a small
  neighbourhood can spike revenue/acre. Check parcel count / area per top performer.

**Approach — by hand:**
- Eyeball the surfaced top + bottom outliers; spot-check their zoning codes and `url`
  bylaw section against what's actually on the ground (satellite / known landmarks).
- Confirm whether outskirts top performers are genuine (annexed industrial, big-box,
  logistics) or artifacts (tiny-acre hoods, one dominant parcel).

**Possible outcomes / follow-ups:**
- A mixed-use category split (`nonres` → `commercial` / `industrial` / `mixed`), if
  mixed-use behaves distinctly. (Would be a TODO build item.)
- A findings note on what actually drives the outskirts high performers.

---

## 2. Machine learning — feature importance (what drives revenue/value per acre?)

**Goal.** Fit models (primarily **random forest**) to predict a neighbourhood's
`revenue_per_acre` (and/or `value_per_acre`) from its characteristics, and extract
**feature importance** — a data-driven ranking of what most explains fiscal
performance. Complements item 1: item 1 eyeballs the tails; this quantifies the
drivers across all neighbourhoods.

**Candidate features** (assemble a neighbourhood-level matrix):
- Land-use composition — `frac_residential` / `frac_nonres` / `frac_inst` /
  `set_aside_frac` (already computed in `load_zoning.py`, but currently dropped before
  output — see prerequisite).
- Density / built form — parcel count, area_acres, parcels-per-acre, median lot size,
  median year built (property-info dataset `dkk9-cj3x`).
- Assessment-class mix — value / levy share by class (see `FINDINGS_assessment_classes.md`).
- Location — distance from centre, ward / district.

**Method notes:**
- Start with RF regression; also try classification (top-vs-bottom performer) to align
  with item 1's tail framing.
- **Prefer permutation importance (and/or SHAP) over impurity-based importance** —
  the default RF `feature_importances_` is biased toward high-cardinality / continuous
  features. Flagged so the first cut doesn't mislead.
- Watch collinearity (composition fractions sum to 1 → linearly dependent; drop one or
  use it deliberately). RF tolerates it but importance splits across correlated features.
- Decide up front whether **set-aside hoods are excluded** (they're off-scale by
  design — probably exclude, matching the colour treatment).

**Prerequisites / blockers:**
- **Feature matrix doesn't exist yet.** `join_and_calculate` emits only a slim column
  set; the per-category fracs + density/class features would need assembling (a small
  export step, or a notebook that re-joins from the source frames).
- **`scikit-learn` not installed** in the `edmonton-tax` env (scipy isn't either —
  numpy-only today). Adding it is the first setup step.
- Notebook lives in `notebooks/exploration/`; per global CLAUDE.md use the Jupyter MCP
  tools, not NotebookEdit.

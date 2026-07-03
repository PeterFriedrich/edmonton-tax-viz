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

**Update 2026-07-03 (from the use-mix view build).** The `nonres` split landed
ahead of this audit: `com` / `ind` / `mix` / `dc` (Direct Control as its own
category — 24% of nonres area; ambiguous codes resolved from bylaw purpose
statements, DATA.md §5). Two composition facts already surfaced:
- **The 8 DC-dominant neighbourhoods are largely the big-box power centres:**
  South Edmonton Common, Terra Losa, Mill Woods Town Centre, Calgary Trail
  South, Summerlea, Place LaRue — plus McCauley and Strathcona Junction. DC
  zoning, not the standard commercial zones, is where the power-centre retail
  sits — so when this audit annotates the top/bottom performers, `frac_dc` is
  the column to watch alongside `frac_commercial`, and the "likely mixed-use"
  suspect list should include DC-dominant hoods explicitly.
- **No neighbourhood is mixed-dominant** (the true mixed-use zones total ~317
  acres citywide, ~1% of nonres) — if mixed-use drives outliers it will show
  as a minority fraction, not as dominance; use `frac_mixed > 0` rather than
  a dominance test when flagging suspects.

---

## 2. Machine learning — feature importance (what drives revenue/value per acre?)

**Goal.** Fit models (primarily **random forest**) to predict a neighbourhood's
`revenue_per_acre` (and/or `value_per_acre`) from its characteristics, and extract
**feature importance** — a data-driven ranking of what most explains fiscal
performance. Complements item 1: item 1 eyeballs the tails; this quantifies the
drivers across all neighbourhoods.

**Candidate features** (assemble a neighbourhood-level matrix):
- Land-use composition — the full 9-fraction breakdown (`frac_residential` /
  `frac_commercial` / `frac_industrial` / `frac_mixed` / `frac_dc` / `frac_inst` /
  `set_aside_frac` …) — exported end-to-end since 2026-07-03 (use-mix view pipeline).
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

---

## 3. Direct Control provision scrape — what does the DC land actually permit?

_Added 2026-07-03, out of the use-mix view build._

**Observation.** The `dc` category (24% of nonres area) is honest but opaque by
construction — Direct Control means a bespoke per-site bylaw, so `load_zoning.py`
claims no single use for it. But the zoning dataset's `url` field points at the
**per-provision** bylaw page for each DC site (`dc-20932`, `dc1-19431`, `dc2-277`,
… ~1,070 polygons), and each page lists that specific site's permitted uses. The
information we discard exists — one HTTP request per site away. Item 1 just made
this concrete: the 8 DC-dominant neighbourhoods are the big-box power centres.

**Why it matters.** Site-level use classification for the DC bucket would let the
item 1 audit distinguish "DC = power-centre retail" from "DC = residential tower"
from "DC = legacy industrial" — currently all invisible inside `frac_dc`.

**Approach — auto:**
- Collect the distinct DC `url` values from the zoning GeoJSON (dedupe: many
  polygons share a provision); fetch each bylaw page politely (cache to disk,
  rate-limit — it's a city web app, not a bulk API).
- Extract the purpose statement + listed/permitted uses per provision; classify
  each site into com / ind / res / mix (extraction is unstructured text →
  LLM/heuristic, so it inherits a QA burden).
- **Keep scraped classifications in separate columns** (e.g. `dc_inferred_use`,
  per-hood `frac_dc_com`-style rollups) — never silently folded into the
  bylaw-authoritative zoning categories. The honest `frac_dc` stays as-is.

**Approach — by hand:**
- Verify a random sample (~30 provisions) of the extracted classifications
  against the pages before trusting any rollup.
- Spot-check the 8 DC-dominant hoods first — highest leverage for item 1.

**Caveats / shelf life:**
- Scrape fragility: page structure can change; re-runs should diff against the
  cached corpus rather than re-classify from scratch.
- The 2024 bylaw renewal collapsed the standard zones into fewer, broader ones —
  zoning-based inference is getting coarser in general. Legacy DC1/DC2
  provisions, however, persist until sites redevelop, so this per-site detail
  has a long shelf life; expect the DC corpus to shrink slowly, not vanish.
- Zoning (including DC provisions) says *permitted*, not *built* — parcel-level
  assessment remains the better "what's actually there" source
  (`PARCEL_LEVEL_OPPORTUNITIES.md`).

---

## 4. Land-use diversity index — does mix correlate with fiscal productivity and servicing burden?

_Added 2026-07-03 (Peter's direction, from a design discussion). Depends on the
use-mix pipeline (shipped — the nine `frac_*` shares are exported end-to-end)._

**Goal.** Compute a per-neighbourhood **land-use diversity index** (normalized
Shannon entropy over zoned-area shares) as an independent variable, then test
two relationships **in Edmonton's own data** rather than citing other cities'
findings:

1. `revenue_per_acre` vs diversity — does mix correlate with fiscal productivity?
2. **Road supply per household vs diversity** — does mix correlate with lower
   servicing burden? This is the one to lean into: if mixed-use hoods show
   measurably less road per household than single-use ones *at comparable
   density and era*, that's an Edmonton-specific, self-supporting result.
   Framed as a hypothesis test; report whichever direction the data shows.

**Index design (decide before computing):**
- H = −Σ pᵢ ln pᵢ, normalized by ln(k) → 0–1.
- **Renormalize over developed shares only** (res / com / ind / mix / inst) —
  including never/notyet makes river-valley hoods read as "diverse".
  Sensitivity-check with and without `inst`.
- **The DC trap:** `frac_dc` is *unknown* use, not mixed use. Treating dc as its
  own category makes SOUTH EDMONTON COMMON (81% DC, a single-use power centre)
  score as diverse. Either exclude dc + flag high-`frac_dc` hoods as
  low-confidence, or run item 3 (DC provision scrape) first and use the
  resolved uses. **Item 3 materially upgrades this item.**
- Limitation to state: the 2024 bylaw's broad zones understate fine-grained mix
  (a residential zone can permit small-scale commercial within it), and zoning
  is permitted-not-built. Neighbourhood-scale zoned mix is what we can measure.

**Denominator work (the "per household" piece):**
- We publish road **per acre**; the servicing-burden test wants per *household*.
  No household dataset is loaded, but the assessment CSV already gives a serviceable
  proxy: **count of residential property records per hood** (condo units are
  individual records, so this approximates dwelling units). Zero new data needed
  for a first pass; a municipal/federal census dwelling count is the upgrade.

**Confounders (explicit ask — age, density, lot size):**
- **Age:** median `year_built` from the property-info dataset `dkk9-cj3x`
  (DATA.md §2 — documented but NOT yet fetched by `scripts/download_data.py`;
  adding it needs the standard `$limit`/truncation guard, ~440k rows via SODA).
- **Density:** residential-record count per acre (from data already loaded).
- **Lot size:** median `lot_size` from `dkk9-cj3x` (city-provided, m²; ~0.6% null).
- **Strategy:** (a) report the correlation matrix among mix / age / density /
  lot size FIRST — in Edmonton, mature gridded hoods are plausibly old AND
  mixed AND small-lot at once, and if mix≈age is near-collinear at n≈250–360
  the honest finding is "not separable at this n", not a forced estimate;
  (b) stratified comparison: diversity-high vs -low *within* era bands
  (pre-1950 / 1950–80 / post-1980) × density terciles, shown as small
  multiples; (c) regression / RF permutation importance with the controls in —
  this folds into item 2's feature matrix (entropy becomes a feature there).
- Set-aside hoods excluded (off the fiscal comparison, matching the views).

**Sequencing note:** a first-pass scatter (revenue/acre vs H, road-per-unit vs
H, coloured by era once `dkk9-cj3x` lands) is a notebook exercise on top of the
already-served GeoJSON + assessment CSV. The deconfounded version needs the
`dkk9-cj3x` download step first.

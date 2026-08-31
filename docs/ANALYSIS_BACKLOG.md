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

**DONE 2026-07-09 — see `docs/FINDINGS_outlier_tails.md`; reproducible via
`tools/audit_outlier_tails.py`.** Surfaced top/bottom-15 by revenue/acre AND
value/acre (358 hoods, 48 set-aside excluded), each annotated with composition
(served `frac_*` + item 3's resolved DC use split), dominant base zone code +
bylaw description, a downtown-anchored distance band, and a thin-denominator check
(account count + largest-account share). **Verdict: the classification holds up —
no build-side refactor of `load_zoning.py` categories warranted.** (1) The
outskirts-high-performer surprise is real but benign — big-box DC power centres
(resolved to commercial by item 3), genuine industrial, and *dense new-suburb
residential* (thousands of small accounts, 1–3 % top-share → not artifacts). (2)
The weak-non-res cluster is low-intensity heavy industrial on very large acreages
(Clover Bar 4,765 ac, ind50) + the exempt/institutional roll gap (Yellowhead
Corridor West, U of A Farm — item 7) + annexed-unbuilt `AG` land; all correctly
low, none miscoded. (3) The floated **mixed-use split is rejected** — mix is a
minority fraction everywhere. (4) Thin-denom artifacts appear only in the *bottom*
tail, so the per-acre leaders are trustworthy at face value. The annotated tails
are a ready feature set for item 2.

<details><summary>Original item (kept for provenance)</summary>

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
  row annotated with: zoning composition (`frac_residential`/`frac_commercial`/`frac_industrial`/
  `frac_mixed`/`frac_dc`/`frac_inst`/
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

</details>

---

## 2. Machine learning — feature importance (what drives revenue/value per acre?)

**DONE 2026-07-09 — see `docs/FINDINGS_feature_importance.md`; reproducible via
`tools/ml_feature_importance.py`.** Random-forest regressions (held-out
permutation importance, averaged over 25 train/test splits; 342 hoods, set-aside
excluded) predict `revenue_per_acre` (held-out R²=0.57) and `value_per_acre`
(R²=0.71). **Verdict: fiscal productivity per acre is a built-form DENSITY story,
not a land-use MIX story.** Two density proxies — `road_m_per_acre` (perm. imp.
0.78/0.59) and `parcels_per_acre` (0.12/0.27) — carry essentially all the signal;
the six `frac_*` composition shares and the diversity index `H` are ≈ 0 in
held-out importance (the full-multivariate confirmation of item 4's density≫diversity
partial-correlation result). The only surviving composition signal is a modest
revenue/acre lift from industrial + DC power-centre land (matches item 1). Adding
assessment-class mix: `nonres_value_share` is a clean #2 for *revenue*/acre
(mill-rate effect) but negligible for *value*/acre. A top-vs-bottom-tercile
classifier separates the tails at **AUC 0.97**, quantifying item 1's "the tails
are genuine" (and `top_acct_share` — the thin-denominator signal — is ≈ 0
everywhere). Feeds items 1 + 4 and the services-lens cost-vs-revenue story.

<details><summary>Original item (kept for provenance)</summary>

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
- ~~**`scikit-learn` not installed**~~ **DONE 2026-07-09** — `scikit-learn==1.9.0`
  + `scipy==1.18.0` installed into `.venv` and pinned in `requirements.txt` (NOT
  `requirements-ci.txt` — the refresh pipeline doesn't use them; exploration-only).
  The remaining blocker is the feature matrix (above).
- Notebook lives in `notebooks/exploration/`; per global CLAUDE.md use the Jupyter MCP
  tools, not NotebookEdit.

</details>

---

## 3. Direct Control provision scrape — what does the DC land actually permit?

_Added 2026-07-03, out of the use-mix view build._

**DONE 2026-07-07 (Sessions 22–24).** Full pipeline shipped end-to-end:
1. **Crawl** — `scripts/scrape_dc_provisions.py` (polite, resumable, cached to
   `data/raw/dc_provisions/`, gitignored, laptop-only). 918/938 pages cached;
   20 failed = 19 unpublished-node 403s + 1 bad URL.
2. **Extract** — `tools/extract_dc_uses.py` pulls each provision's Purpose
   statement → `data/dc_provisions_text.csv` (918 rows, 898 usable purposes).
3. **Classify** — `tools/dc_use_labels.py` holds the in-context (Claude)
   per-slug use judgments (res/com/ind/mix/inst/unknown), joins the text CSV,
   and emits `data/dc_inferred_use.csv` with a hard 918-slug coverage assert.
   Distribution: res 364, com 256, mix 139, inst 73, ind 57, unknown 29.
4. **QA** — 32-page spot-check vs the cached full pages (incl. the "Uses" list
   absent from the labelling input) + a corpus-wide `mix`-without-residential
   audit → 3 boundary fixes; ~2–3 % effective error, all medium/low-confidence.
5. **Rollup** — `tools/rollup_dc_uses.py` area-weight-splits each hood's
   authoritative `frac_dc` into `frac_dc_res/_com/_ind/_mix/_inst/_unknown`
   (`data/dc_use_by_hood.csv`), reusing `load_zoning`'s exact overlay so the
   reconstructed `frac_dc` matches the served value **exactly** (max|Δ|=0.0000).
   92 % of citywide DC mass resolves to a use.
6. **Re-analyze** — item 4's `analyze_land_use_diversity.py` folds the resolved
   shares into the DEV categories and re-admits 8 of the 14 dropped hoods; the
   headline correlations are unchanged (see item 4 + `FINDINGS_land_use_diversity.md`).

The residual 8 % unknown is legacy DC parcels the City's open data tags
`url = "legacy"` (no bylaw page) + the 20 failed fetches — carried as a distinct
`frac_dc_unknown`, never folded into a use. MCCAULEY (bare "DC" legacy parcels,
unidentifiable) and STRATHCONA JUNCTION stay excluded; SUMMERLEA's WEM `legacy`
parcel was hand-resolved (geometrically coincident with `dc2-1198`).
⚠️ The crawl only runs on Peter's laptop (`zoningbylaw.edmonton.ca` is
edmonton.ca, unreachable from the Oracle box); the offline steps 2–6 run anywhere
the gitignored HTML corpus is present.

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

**DONE 2026-07-07 (Session 22 first pass; Session 24 folded in the resolved DC
land) — see `docs/FINDINGS_land_use_diversity.md`; reproducible via
`tools/analyze_land_use_diversity.py`.** Result: (1) revenue/acre vs diversity
holds under controls (partial r +0.27, n=299) but is secondary to density
(+0.66); (2) **road-per-dwelling vs diversity is a null** (r ≈ −0.03, robust to
both the record-count and `build_connections` dwelling denominators) — the
road-per-*acre* correlation was age/density confounding, not a per-household
servicing benefit. **Session 24:** item 3's DC classification is now folded into
the DEV categories and 8 of the 14 dropped high-`frac_dc` hoods re-admitted (n
293→299); both verdicts are unchanged, so the DC trap was not hiding a different
story (FINDINGS §2.1). Remaining upgrades (open): formal regression + p-values /
RF importance (folds into item 2); the `notebooks/exploration/` scatter version.

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
  (DATA.md §2 — fetched by `scripts/download_data.py --only property_info`
  since 2026-07-04; the pipeline already loads its `lot_size` via
  `src/load_property_info.py` for the grid's lot-acre metric, and `year_built`
  is one usecols entry away).
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
`dkk9-cj3x` download step first (DONE 2026-07-04 — the file is a standing
pipeline input now).

---

## 5. Growth servicing cost recovery — who funds new trunk infrastructure, and what does the city inherit?

_Added 2026-07-05, out of the utility methods doc
(`docs/utility_cost_estimation_lens_methods.md` §I and Stage 5). Analysis, not
a lens build — the lens side is `docs/SPEC_utilities.md`._

**AUTO HALF DONE 2026-07-10 (Session 36) — see
`docs/FINDINGS_growth_servicing.md`; reproducible via
`tools/analyze_growth_servicing.py`.** Two-ledger result, era-banded by median
`year_built`: (1) road supply per dwelling *falls* with newness (mature grid
~13.0 m/dw → post-2010 ~6.4, robust to both dwelling models and to build-out
stage) and fire demand per dwelling falls ~3×, while levy per dwelling is
roughly flat and levy per *developed* acre is highest in the post-1990 bands;
(2) Heritage Valley + Windermere currently yield $211M/yr municipal levy
(7.8% of the citywide roll) at ~16% undeveloped — but within-boundary road
metres exclude arterials/trunks, and the documented cross-subsidy channels
(SSTC pause, low off-site levies) sit exactly on that unmeasured layer.
**The by-hand half stays OPEN (laptop):** SSTC-resumption tracking, reading
the BILD study + Capital Investment Outlook primary docs, re-verifying the
best-effort ASP hood memberships.

**Question.** Development-industry material (BILD Edmonton Metro's Urban
Growth Case Study: Heritage Valley + Windermere) argues new growth is
fiscally net-positive because developers fund upfront capital (~$3.2B
claimed) and the area will contribute ~$309M/yr in property tax at build-out.
The counter-consideration is the **long-tail liability**: once assets
transfer, the City/EPCOR carry lifecycle renewal + O&M (regulated
return-on-rate-base ~10.5–10.8% ROE on ~$888M of planned wastewater capital
alone; a documented ~$10B ten-year infrastructure renewal shortfall). What
can Edmonton's own data say about either side?

**Documented facts to anchor on (sourced in the methods doc — both the BILD
projections and the counter-framing carry advocacy weighting; label all of
it):**
- Sanitary Sewer Trunk Charge **paused 2024-05-13** (2024 rate was
  $1,764/principal dwelling); ~$361M spent on deep trunks through the SSSF
  to end-2024. While paused, new trunk servicing draws on the general
  SSSF/ratepayer base — a measurable cross-subsidy channel.
- Edmonton's off-site levies are structured as targeted instruments, low
  relative to peers (e.g. Calgary's per-unit infill water/wastewater charges
  + per-hectare greenfield fees).
- BILD's figures are **projections at full build-out**, not realized
  outcomes; City-side O&M figures in the same study (~$14M/yr roadways,
  ~$9.7M/yr parks) are partial (no renewal, no utility side).

**Approach — with our data (auto):**
- Per-hood levy (have) vs per-hood modeled utility charges + road supply
  (SPEC_utilities lenses when built) for the named growth areas vs mature
  hoods — an Edmonton-data version of the case study's revenue side, with
  the consumption side attached.
- Neighbourhood age (`year_built` medians, `dkk9-cj3x`) × road-per-household
  and (once built) stormwater-charge-per-acre: does new-greenfield servicing
  intensity differ from mature-grid intensity? Overlaps item 4's servicing-
  burden test; this item adds the growth-area framing.

**Approach — by hand:**
- Track SSTC resumption (SSSF Transformation project) and any off-site levy
  changes; each changes the cross-subsidy picture materially.
- Read the BILD study and the City's Capital Investment Outlook directly
  before quoting either beyond the methods doc's citations.

**Output:** a FINDINGS doc presenting both ledgers side by side — developer
upfront capital (avoided City cost) AND inherited lifecycle/renewal + O&M —
per the neutral-tone rule: surface the data, attribute the claims, no
verdict language.

---

## 6. IIMP capital & debt figures for Decoteau / Horse Hill / Riverview — source hunt

_Added 2026-07-08. The **research** half of the TODO build item "Decoteau / Horse
Hill / Riverview capital & debt annotation" (a citation/annotation layer, NOT a
lens). This item owns *finding + verifying the numbers*; TODO owns *surfacing
them in the map*. Close sibling of item 5 (same three growth areas, same capital
vs recurring-revenue question) — item 5 is the analytical ledger, this is the
primary-source dig behind one specific published model._

**DONE 2026-07-15 (laptop) — `docs/FINDINGS_iimp_growth_areas.md`.** Located +
verified the primary source (Report CR_2705, March 22 2016, + Attachment 1); every
brief figure confirmed against the actual tables (developer $3.806B, City/Province
$1.362B with full breakdown, ~$1.4B 50-yr shortfall — distinct from the capital
figure, area/pop/horizon stats). 2016$, projections at build-out, received for
information. Not superseded per-area by the 2026 CIO/OIO (citywide, not per-area).
Figures + citations ready for the TODO D2 annotation build.

**Question.** The City's IIMP (Integrated Infrastructure Management Plan) ran a
39-year capital pro forma on the three greenfield growth areas — developer
capital + muni/provincial capital (~$369M piece) + O&M + lifecycle renewal,
amortized vs projected tax revenue. We currently only have it **secondhand** (a
Gemini research summary in project files + 2016 Global News coverage). We want
the primary figures — developer capital, muni/provincial capital, build-out
horizon, revenue-vs-cost gap — with an explicit citation + "as of" date.

**Why it matters.** IIMP is the closest existing precedent to the **OIC**
(operating-impact-of-capital) accounting the City is introducing for the
**2027–2030 zero-based budget cycle** — a credibility anchor for the tool, and a
concrete capital/debt data point for three named hoods where citywide
capital-cost data at this fidelity doesn't exist.

**Approach — by hand (primary supersedes secondhand):**
- **PRIMARY target: the actual IIMP / "Fiscal Impacts of Growth" report.** Search
  council agenda/report archives (edmonton.ca, eScribe/insite) for "IIMP",
  "Fiscal Impacts of Growth", "Decoteau ASP", "Growth Related Analysis".
- Off-site levy bylaw + capital financing policy — how the ~$369M
  muni/provincial piece was financed (debt vs levy vs grant); that's the "debt"
  component specifically.
- City annual financial statements / debt management reports — actual
  debt-servicing cost + interest rates for the relevant financing period, IF we
  want real debt-service cost rather than just capital outlay.
- Infrastructure committee **mid-2026 OIC presentation** — check whether it
  re-presents/updates these three areas' figures under the new OIC framework; if
  so, cite that (current) version over the 2016 analysis.
- 2016 Global News coverage — secondary corroboration only; primary report
  supersedes it for exact figures.

**Blocker.** edmonton.ca / eScribe are **unreachable from the Oracle box** (curl
exit 000 — the Session-21 network policy); the source dig is **laptop-only**. See
`docs/REMOTE_VM.md` and the Session-21 handoff.

**Caveat / shelf life.** 2016-vintage figures may be superseded by the OIC
re-presentation — prefer the most current published version and date-stamp
whichever is used. Keep framing neutral/descriptive: state the IIMP's own
projected figures + horizon, attribute, don't editorialize.

**Output:** verified figures + citations feeding the TODO annotation build; a
short FINDINGS note if the numbers warrant one. Kept strictly separate from every
recurring-cost lens (different unit of analysis — multi-decade capital pro forma,
not the citywide recurring-cost map).


## 7. Exempt-institutional hoods — where does exempt-land dilution bite hardest?

**DONE 2026-07-09 — see `docs/FINDINGS_exempt_institutional.md`; reproducible via
`tools/audit_exempt_institutional.py`.** Measured (not guessed) exempt-institutional
land as institutional-proxy zoning (`UI/UF/AJ/PU`) carrying no taxable account:
overlay institutional acres by code, spatial-join the deduped taxable footprint onto
them, `exempt_inst_acres = inst acres − taxed footprint`. Results: (1) **20 hoods**
have ≥10 % of their polygon as untaxed institutional land; **U of A is the extreme
high-value case** ($15.2M/lot-ac, 145 exempt ac, ×2.0 lift) — Edmonton Northlands
(civic expo grounds) is the clean second. (2) The exempt footprint is mostly **NOT**
`UI` "university/hospital" zoning — citywide it's `PU` 4,774 ac + `AJ` 1,870 ac +
`UF` 1,819 ac vs `UI` only 205 ac; U of A's campus is 100 % `AJ` (provincial crown).
(3) The measurement cleanly separates the three look-alikes: genuine exempt-dilution
(U of A), utility corridors (`PU` — Poundmaker tops the raw ranking but is low-value
EPCOR land + stormwater ponds), and low-value institutional land that is ON the roll
(U of A Farm — 726 inst ac but 85 % taxed as farmland). Park/river hoods (Riverdale,
Cloverdale) correctly reject as ~0 % exempt despite big lot-acre boosts. Feeds the
lot-acre toggle framing + the services-lens free-riding estimate (`SPEC_services.md`).

<details><summary>Original item (kept for provenance)</summary>

_Added 2026-07-08, generalized out of the University of Alberta hand-analysis
(see `docs/FINDINGS_denominator_cardinality.md` worked case). U of A: $2.242B
taxable value on 47 accounts sitting on 147.5 of 295.2 polygon acres (50%
parcel), $/ground-acre $7.6M → $/lot-acre $15.2M (×2.0). The lift is driven by
tax-exempt campus/hospital land that is **absent from the taxable roll entirely**
(`data/DATA.md` 2026-06-29). U of A is unlikely to be alone._

**Question.** Which neighbourhoods are dominated by tax-exempt institutional land
(university, hospitals, Legislature, City/provincial property, large parks), and
therefore (a) get the biggest *honest* lift from the pending lot-acre
neighbourhood toggle, and (b) carry the biggest **services-lens gap** — serviced
land (roads/fire/transit) yielding zero municipal revenue?

**Why it matters.** These hoods behave in a way neither revenue denominator fully
tells: lot-acre makes their tax-paying intensity honest, but the exempt half is
invisible to a revenue lens and only shows as free-riding on the **cost/services**
side (`docs/SPEC_services.md`). Candidate set beyond U of A: University of Alberta
Farm (734ac, 14 accounts — but *low-value taxable* land, a different mechanism, do
not conflate), Legislature Grounds, the hospital-anchored hoods, downtown
government blocks.

**Approach.** No exempt boolean exists on the roll (exempt land is simply absent,
not flagged) — so proxy exempt share as **polygon acres − deduped taxable lot
footprint − road/ROW acres** per hood, rank hoods by low taxable-footprint
fraction, and cross-reference zoning `AJ/PU/UI/UF` (the exempt-proxy zones,
`data/DATA.md` §5, "Set-aside categories"). Separate genuine exempt-dilution
(U of A: high value,
low footprint) from low-value-land hoods (U of A Farm: high footprint, low value)
and from park/river-valley (already covered in item 1 / the lot-acre findings).

**Output:** a ranked list of exempt-institutional hoods + a FINDINGS note; feeds
both the lot-acre toggle framing and the services-lens cost-vs-revenue story.
Related: item 1 (outlier tails), the PRIORITY lot-acre toggle in `TODO.md`.

</details>

---

## 8. Regional non-residential assessment share — rebuild the published series from primary data

**Added 2026-07-18 (with the industrial/non-res lens family — `docs/SPEC_industrial.md` B1).**

**Observation.** Two published secondary figures for Edmonton's share of the
region's non-residential assessment base don't obviously reconcile: a 2016 city
report cited a decline from **76% → 72%** over the prior 15 years, while a
late-2024 industry publication cited a decline from a "record high" **72% in
2008-09 to 60% in 2022**. Candidate explanations: different denominators (which
municipalities count as "the region"), different valuation bases
(equalized vs raw), different class definitions (machinery & equipment,
linear property in or out).

**Why it matters.** The share series is the headline number for the regional
context lens (B1); citing either secondary figure without reconciliation would
import an unexplained contradiction into public copy. The project rule is to
rebuild from primary data and state what it shows.

**Approach — auto:** pull the FIR/SIR yearly workbooks (established
`fetch_fir_debt.py` idiom; zips back to 1994) + the equalized assessment XLSX
(2024–2026 verified on open.alberta.ca; check FIR/SIR or older editions for
pre-2024 equalized values) for Edmonton + Strathcona/Sturgeon/Parkland
counties + Leduc city/county; compute the share series under each candidate
definition (equalized vs raw, class in/out) and see which reproduces which
published figure. **By hand:** read the two secondary sources' own
methodology notes if recoverable; pick and document the definition the lens
will use.

**Output:** a FINDINGS note with the reconciled series + the definition
chosen for B1; feeds SPEC_industrial B1 copy.

---

## 9. Built-form intensity — surface it as its own map (units-per-permit and/or FAR)

**Where this came from.** The Development lens has two activity metrics (2026-07):
**Dwelling units** (homes) and **Permits** (construction events). They diverge
sharply by built form because a single-detached house = 1 permit = ~1 unit, while
an apartment tower = 1 permit = many units. Confirmed on the live data
(2009–2025, `units-per-permit` by hood): single-family suburbs sit at ~1.0–1.2
(Donsdale 1.0, Laurier Heights 1.1), apartment/tower nodes at 5–16 (Clareview
Town Centre 15.8, Heritage Valley TC 14.4, Garneau 11.3); citywide avg 2.06. So
the **Permits** map is essentially a single-family-lot-churn map (maxes out on the
sprawling edges — Chappelle 3,807 permits), while **Units** weights multi-family
more. The *ratio itself* is a built-form/intensity signal we don't surface.

**Two candidate metrics (neither built yet):**
- **units-per-permit** — a NEW column (`new_dwelling_units / new_dwelling_permits`
  per hood/window; the counts already ship). A *flow* intensity map of recent
  construction: low = single-family, high = multi-family. Guard the 0-permit
  denominator; decide the window(s).
- **FAR as a standalone view** — `far` (Σ floor area ÷ deduped lot area) is ALREADY
  computed per hood AND per 100 m cell (Glass grid), but is only surfaced *inside*
  the Infill lens as the suitability term — never shown raw. A *stock* intensity
  map: low FAR = single-family/vacant, high = dense multi-family/commercial.
  Low-effort to expose (data's there); would need its own legend/ramp + a caveat
  that FAR mixes in commercial floor area.

**FAR vs units-per-permit** are related but distinct: FAR = intensity of what's
STANDING (all eras, incl. commercial); units-per-permit = intensity of what's
being BUILT NOW (residential only). corr(FAR, new-unit-activity) is only +0.24 on
the current data — largely independent signals.

**Why it matters.** Both answer "how intensely is this land used/being built"
directly, which neither the units nor the permits map does on its own. FAR is the
cheaper win (already computed); units-per-permit is the more targeted recent-
construction cut. Decide whether either earns a view before building.

**Aside (validation, not a task):** the **Infill lens is NOT density-dominated** —
its score `z(inverse-FAR) − z(activity)` correlates **+0.79 with EACH** term on
the live data (358 hoods), i.e. existing-density and new-build contribute equally
(the two z-scores are standardised over the same population). Recorded here so a
future "is Infill just a FAR map?" question has its answer; see SPEC_development
Lens B.

---

## 10. Does per-hood CHANGE in share-of-base actually separate the 406 hoods? — ✅ RUN 2026-07-30. **THE GATE PARTLY FAILS, and the fix is a decision for Peter.**

**Executed against `web/data/temporal.json` (406 hoods × 13 years), 2026-07-30,
prompted by Peter: *"I've already seen some graphs that have like, a peak in the
middle. So straight average would be 0."* He is right, and measuring it turned up
three things that outrank the hump itself.**

### Finding 1 — ⚠️ A RELATIVE-CHANGE MAP IS UNDEFINED FOR 45 HOODS (11%), AND THEY ARE THE GROWTH AREAS

45 of 406 hoods have a **zero 2012 share**, so `last/first` does not exist for
them: Blatchford, Decoteau, Keswick, Glenridding Ravine, Graydon Hill, Rosenthal,
Stillwater, The Uplands, Edgemont, Cavanagh, the Anthony Henday ring segments and
several river-valley slivers. **These are precisely the neighbourhoods a
"how much has it changed" map most needs to show** — they went from nothing to
something, which is the largest change possible.

This **reverses the recommendation `TODO.md` carried** (relative as the headline).
Percentage-point change is defined for all 406.

Options, none free: (a) relative change, with the 45 drawn in the established
off-scale grey (`SET_ASIDE_COLOR` / the `infillOppSuppressed` idiom) and
explained; (b) percentage-point change, defined everywhere — but see Finding 3;
(c) relative change measured from each hood's **first non-zero year**, which is
defensible but silently puts a 3-year change and a 13-year change on the same
ramp. **(c) is the comparability trap this project keeps meeting; if it is taken,
the window must be stated per hood.**

### Finding 2 — the hump is REAL but NARROW, and drawdown does not fix it

Measuring the hump as how far the peak rises above the *higher* of the two
endpoints:

| hump | hoods | share |
|---|---|---|
| ~0 (monotone — the peak **is** an endpoint) | 257 | 71% |
| 1–5% (negligible) | 40 | 11% |
| 5–15% (visible arc) | 45 | 12% |
| **>15% (a real hump)** | **34** | **8%** |

So endpoint arithmetic describes ~71% of hoods honestly. For the 34 real humps it
does not — biggest are **RIVER VALLEY LAURIER** (+243% hump), **HERITAGE VALLEY
AREA** (+185%), **UNIVERSITY OF ALBERTA** (peak 2023, −44% to 2025), **SOUTH
EDMONTON COMMON** (peak 2019, −36%), **MAPLE RIDGE INDUSTRIAL** (net **+24%** yet
**−23%** off its 2020 peak).

**Spearman, all in pp so the comparison isn't confounded:**

| pair | rho | reading |
|---|---|---|
| net vs OLS slope, all 406 | **+0.959** | near-duplicates in aggregate |
| net vs OLS slope, **the 34 humps only** | **+0.719** | this is exactly Peter's point, quantified |
| net vs **peak drawdown** | **+0.919** | ⚠️ **drawdown is NOT a different ranking** — it does not solve the hump |
| net **relative** vs net **pp** | **+0.581** | genuinely different orderings; the pp/relative choice matters more than endpoint/slope |

**So the fix for a peaked series is NOT swapping in drawdown or a slope.** Both
rank almost identically to net change. A peaked hood needs a **second number**
(peak value + peak year), not a different single number — and the panel already
computes and shows exactly that (`peak share 5.55% in 2016`).

### Finding 3 — ⚠️ THE GATE FAILS FOR PERCENTAGE-POINT CHANGE: IT DOES NOT SEPARATE HOODS

| metric | p1 | p25 | median | p75 | p99 |
|---|---|---|---|---|---|
| net **pp** | −0.255 | −0.062 | **−0.032** | +0.001 | +0.835 |
| net **relative %** | — | −27.0 | **−20.7** | −10.2 | +253.3 |

The median hood moves **−0.032 pp**. Downtown moves **−1.791 pp** — about **56×**
the median. **15% of hoods (61 of 406) move less than 0.01 pp in thirteen years.**
A pp choropleth is therefore Downtown plus a handful of others blazing over ~380
hoods that are visually identical — **the exact failure this gate was written to
catch.** Relative change *does* spread (p25 −27%, median −21%, p95 +253%), which
is the tension with Finding 1: the measure that separates is the one that is
undefined for the growth hoods.

**A sqrt or rank/percentile transform of pp is the obvious third path** and is
already an in-repo idiom (`state.colorAdjust`, the locked sqrt colour scaling) —
but note it would be **presentation** rescaling of an unseparated metric, not a
fix to the metric, and the project's linear-elevation honesty choice is nearby.

### Finding 4 — two windows earn their keep

Long (2012→2025) vs short (2019→2025), both pp: **rho +0.734**, and the sign
**flips for 55 of 406 hoods (14%)**. So the short and long windows genuinely tell
different stories for a seventh of the city, and Peter's "timeline options" ask is
justified rather than decorative.

### Methodology note — two errors in the first pass, corrected

Recorded because both are easy to repeat: the first run compared a **relative**
net change against a **pp/year** slope and read the low correlation (+0.574) as
"endpoint and slope differ", when it was mostly the relative/pp difference — the
clean comparison is **+0.959**. And the script **pre-labelled its expected
conclusions** in the print statements, so the output asserted "near-duplicates"
and "genuinely different" beside numbers that said the opposite. Also 45 hoods
divided by zero and quietly produced `nan`, which poisoned every correlation in
the first run. **Compare like units, and don't print a conclusion you haven't
measured yet.**

---

## 10-original. The question as first framed (kept for the record)

**The question.** Peter wants "how much each hood has changed on average over
time" as a **map metric** with selectable windows (`TODO.md`). Before drawing
that map, answer the cheap prerequisite: **does the metric spread the hoods, or
does it put ~400 of them inside noise with a handful of Downtown-scale outliers
carrying the whole ramp?** A choropleth of a metric that doesn't separate is a
uniform map with three bright cells.

**Why it is cheap.** No new data. `web/data/temporal.json` is 406 hoods × 13
years, already built; this is a pandas histogram, not a pipeline.

**What to report, in this order:**
1. Distribution of **relative** change (2012→2025) and of **percentage-point**
   change. How many hoods fall inside ±1 pp? Inside ±10% relative?
2. **Do the two rank hoods differently?** Spearman between them. The pp measure
   structurally ranks by hood size (a hood at 0.05% cannot move 1 pp), so a high
   correlation would be the surprise, not the expectation.
3. **Endpoint vs OLS slope over the same window — Spearman.** If they agree,
   endpoint arithmetic is safe and far easier to explain; if they disagree, some
   hood's freak start year is setting its whole answer.
4. Same three for the **short window** (2019→2025), and whether short and long
   windows tell *different* stories — because if they don't, one picker option is
   enough and the "timeline options" ask collapses to a simpler feature.

⚠️ **Divide by YEARS ELAPSED (13), not observed intervals (12).** 2024 is omitted,
so the two differ and using intervals inflates every annual rate by ~8%. Same
trap as index-vs-year positioning in the sparkline; see `SPEC_temporal.md` §2.

⚠️ **Watch the renamed hood.** OLIVER → WÎHKWÊNTÔWIN carries ~12,000 accounts. It
is handled inside `build_temporal_table`, so the served file is already correct —
but any *fresh* analysis that re-derives from the raw historical file must apply
`TEMPORAL_NAME_CORRECTIONS` or it will report one hood collapsing to nothing and
another appearing from nowhere.

---

## Downtown's assessed value: real decline, but ~a third of the headline drop was a DATA DEFECT (NEW 2026-07-28, RESOLVED)

Surfaced while checking whether a per-neighbourhood assessment time series was
feasible. **Resolved the same day at the data layer.** Two intermediate readings
were recorded and both were wrong; the trail is kept because the *method* that
settled it is the reusable part.

### What it looked like, and why that was wrong

`qi6a-xuwt` alone says Downtown ran $7.30B (2012) -> **$10.28B (2016 peak)** ->
$7.09B (2025), with a violent $9.16B -> $7.30B single-year drop into 2024.

- **First reading (wrong):** split by `mill_class_1`, commercial fell 24% on
  only -60 accounts, so "~80% genuine revaluation, ~20% unexplained."
- **Second reading (also wrong):** the 1,359 accounts that vanished were worth
  $1.822B in 2023 -- ~98% of the drop -- so "almost all of it is the vanishing."
- **What settled it:** tracing the individual account numbers, then checking the
  same buildings against the **current roll**. Neither aggregate could have
  answered it; only the account-level join did.

### The finding

**The historical dataset's 2024 and 2025 slices are incomplete** (full evidence
in `data/DATA.md` §0). For assessment year **2025**, same year, same city:

| Downtown, 2025 | accounts | value |
|---|---|---|
| `q7d6-ambg` current roll (what we ship) | **11,216** | **$7.81B** |
| `qi6a-xuwt` historical 2025 slice | 10,307 | $7.09B |

Two ICE District towers (Stantec Tower and 10360 102 St, 571 accounts, ~$308M)
are present in 2023, **absent from both 2024 and 2025**, and **present again in
the current roll**. They were not demolished.

### The corrected trend -- still a real story, ~a third smaller

Using the historical dataset for 2023 and the **current roll** for 2025:

| | 2023 (hist) | 2025 (current roll) | change |
|---|---|---|---|
| COMMERCIAL | $6.32B / 822 | **$4.85B / 723** | **-$1.47B (-23%)** |
| RESIDENTIAL | $1.63B / 10,739 | $1.49B / 10,393 | -$0.14B (-9%) |
| OTHER RESIDENTIAL | $1.20B / 101 | **$1.46B / 97** | **+$0.26B (+22%)** |
| **total** | **$9.16B / 11,663** | **$7.81B / 11,216** | **-$1.35B (-14.7%)** |

- **The office-devaluation story SURVIVES and is essentially the whole story.**
  Commercial fell 23% on a near-stable account count -- the same buildings
  reassessed lower. That is now confirmed against the roll we ship, not just
  against the suspect historical file or press coverage.
- **But the magnitude was overstated.** Peak-to-2025 is **-24%**, not -31%; the
  2023->2025 fall is **-$1.35B**, not -$2.07B. Roughly a third of the apparent
  collapse was the 909-account hole.
- **`OTHER RESIDENTIAL` rose 22%** and was invisible in every earlier reading.

### Still open

1. ~~**How far back does the defect go?**~~ **ANSWERED 2026-07-28: not far.**
   2012-2023 are clean (0-14 accounts/yr); the defect is one dropout event in
   2024 plus 131 stragglers in 2025. `docs/SPEC_temporal.md` §0.1. The "every
   year needs a control total" instinct was right and became the guard.
2. ~~**Is the shortfall citywide or Downtown-shaped?**~~ **ANSWERED: both, and
   the ~8,000 was WRONG.** That figure was inferred from row counts of different
   vintages; most of the gap is new construction. Measured account-by-account:
   **2,448 accounts / $2.93B / 188 neighbourhoods.** Downtown holds 1,292 (53%)
   -- so it is genuinely Downtown-shaped -- but Magrath Heights loses 17% of its
   accounts and Glenora 15%, so it is not Downtown-only. **Cite 2,448, never
   8,000.**
3. **Worth reporting to Edmonton Open Data.** Two named towers missing from a
   published dataset is a concrete, reproducible bug report.
4. **Does any of this change a published claim?** Still unchecked -- the
   revenue-per-acre *ranking* may be perfectly stable regardless.
5. **Framing stays descriptive** (locked 2026-07-28): share-of-base line plus the
   sourced driver. No "downtown is dying", no "the rest of the city subsidizes
   downtown."

### The reusable lesson

**Two aggregate-level readings both looked convincing and both were wrong.** A
class-level split and a value-of-vanished-accounts sum each produced a coherent
story; the account-level join produced the opposite one. When a series has a
cliff, **join at the entity level and check a second source for the same period**
before interpreting the shape. This is `FINDINGS_lot_dedupe.md` §4.3's
"validate at the display grain" lesson wearing different clothes.

### The share-of-base denominator -- state it in the UI

Independent of the defect, and **it corrects an incoming claim** that the
publicly-quoted ~5.2% / 7.7% / 10.1% Downtown share figures "match the project's
existing figures." They do not match share of **total** assessed base:

| year | share of TOTAL base | share of COMMERCIAL base |
|---|---|---|
| 2021 | 5.08% | 13.32% |
| 2023 | 4.46% | 12.11% |
| 2025 | **3.22%** | **9.30%** |

_(both from the historical file, so both inherit the 2025 defect above -- the
ratio is less affected than the level, but recompute from the current roll
before publishing either.)_

The public figures sit in the **commercial** range, so they are almost certainly
a non-residential or levy share -- the levy is non-res-weighted by the class
differential this project already models. **Publish 3.22% beside an article
saying 5.2% and the project looks wrong when it is not.** Name the denominator in
the UI; showing the commercial share alongside is probably worth it, since that
is the series public discourse uses.

**Do NOT use the `NONRES MUNICIPAL` class for anything** -- it is 1-2 accounts and
its share swings 30-53% on noise.

---

## 11. The capital budget — a spatial layer we do not have (NEW 2026-08-21, SOURCED, not built)

**Auto + by hand.** Every dollar this project models is **operating**. The
capital side has never been in the repo, and it is the side that answers *"what
is the City committing to build here?"* — a different question from *"what does
this neighbourhood cost to run?"*

### The sources exist and are reachable from the Oracle box
Probed 2026-08-21. ⚠️ **The open data portal has NO capital sibling to
`da9s-v9j8`** — a domain search for approved budgets returns only the two
OPERATING feeds (`da9s-v9j8` expenses, `m84q-ghmu` revenues), `552h-hjwj`
Capital Projects, and a 2015 relic (`pdmi-3qjb` / `r993-376i`). The real capital
budget is on the **Open Budget portal** (§17's host), which was never probed
beyond `operating_budget.csv`:

| endpoint | rows | grain |
|---|---|---|
| `budget.edmonton.ca/api/capital_budget.csv` | **1,884** | `fiscal_year, service, branch, profile_id, profile, fund_type, fund, approved` — **the profile-level budget** |
| `budget.edmonton.ca/api/capital_projects.csv` | **399** | `profile_id` → description, phase, address, **lat/long** — joins to the above |
| `data.edmonton.ca` `552h-hjwj` | 214 | the `building.edmonton.ca` app feed: `neighbourhood`, `ward`, lat/long, `approved_budget_m`; only 4 asset types |

**Shape of `capital_budget.csv`:** FY2023–2037, **$11.51B** total, dense over the
**2023–2026 cycle ($9.22B)** with thin carry-forward tails (60 rows in 2027 → 1
in 2037). Top services: LRT Expansion $4.10B, Roads $1.48B, Recreation & Culture
$1.02B, Yellowhead Freeway Conversion $789M, Neighbourhoods $716M. Funding
splits by `fund_type` (Grants $4.60B, Tax-Supported Debt $3.50B, Reserves $1.23B,
PAYG $852M…) — so *who pays for it* is answerable, not just *what it costs*.

### Why it is interesting spatially
`capital_projects.csv` carries lat/long for 399 profiles and `552h-hjwj` carries
a `neighbourhood` string for 210 of 214. Either could put committed capital on
the map beside the operating cost the Services lens already shows.

⚠️ **MEASURED 2026-08-22 — and the binding constraint is NOT what it first
looked like.** `capital_budget.csv` and `capital_projects.csv` are the SAME
population, not different ones: **399 distinct `profile_id`s each, 397 shared**
(2 unmatched per side). The 1,884-vs-399 gap is a difference of GRAIN — the
budget repeats a profile across years and funds — not of coverage.

**The real limit is that only 104 of the 399 profiles carry a coordinate.**
Those 104 cover 831 of 1,884 budget rows and **$8.58B of $11.51B — 74.6% of the
dollars**. What falls out is partly non-spatial by nature (`LRV Replacements`
$240.5M, `Vehicle and Equipment Replacement` $119.6M) and partly linear
infrastructure a point could not honestly represent anyway
(`Yellowhead Trail - 156 Street to St Albert Trail` $103.9M,
`Metro Line LRT (NAIT - Blatchford) Extension` $111.1M).

⚠️ **So a point map would silently omit a quarter of the money, and would omit
it NON-RANDOMLY** — the fleet and the corridors, not a random 25%. Decide what
the unplaced quarter does before drawing anything; `552h-hjwj`'s `neighbourhood`
string (210 of 214) is a different and coarser handle on the same problem.

### ⚠️ New-vs-renewal is NOT a published field, and enumerating it is the T8 trap
There is no column separating new construction from renewal. A keyword pass over
`profile` (`renew|reconstruct|rehabilit|resurfac|overlay|replacement|preservation`)
across the three road-ish services for 2023–26 gives **$1,023M renewal /
$1,490M new, 27.3% of all capital** — but that is **exactly the
hand-enumeration shape `DATA_INTEGRITY.md` T8 exists to distrust**: a value-sum
over a name-matched set, no self-check, every member counting for its full
weight. Two profiles named `Transportation: … - Renewal` are explicit; the rest
are inferred from words like "Reconstruction". **Treat the split as indicative
only; do not publish a new-vs-renewal number sourced this way.**

### Cadence — ⚠️ NOT annual, and the endpoint gives NO freshness signal
The capital budget is a **four-year cycle** (this file is 2023–2026), moved
within-cycle by supplemental adjustments. ⚠️ **`capital_budget.csv` sends
`Cache-Control: no-cache` and a `Last-Modified` that merely echoes `Date`** — so
unlike Socrata's `rowsUpdatedAt` (§18), **there is no header to date the data
from.** Any staleness check must be content-based (hash the payload, diff the
row count / cycle totals), and any published figure must date itself from the
budget cycle rather than from the fetch.

**Prerequisite for any of this:** the manual reviewed-input pattern (§13, §16,
§18) — hand-fetch, eyeball the diff, commit. Never the weekly refresh.

---

## 12. Infill at 100 m + amenity proximity (NEW 2026-08-22, MEASURED, not built)

Full measurement write-up: `docs/FINDINGS_infill_granularity.md`. Locked calls:
`docs/DECISIONS.md` 2026-08-22 (×2). This section holds only what is still open.

**The question.** Peter: *"shouldn't we actually have it more granular? … one of
the affectors i wanted was like, distance of each block from lrt stations, and
schools, for each property, then it would get filled into each spike."*

**Settled by measurement, do not re-derive:**
- Activity at cell grain is **88% zeros** on the default column; a **600 m disc
  kernel** fixes it (73.0% non-zero). No cliff in the curve.
- **`far == 0` is 16.2% of cells and means missing `gross_area`** — 3,964 in-scale
  cells tie at the maximum opportunity score.
- **Euclidean distance to LRT is 55% false-positive at a 600 m band.** Use the
  road network.
- **Nothing here is blocked on data acquisition.** LRT stations derive from the
  GTFS in `data/raw/`; schools are `996c-239n` (225) + `gfxq-u8uu` (97).

✅ **DONE 2026-08-23 — the distances themselves ship** (`feat/amenity-distance`):
`dist_lrt_m` / `dist_school_m` as per-cell attributes on `value_grid.json`,
computed per property over a road graph and taken as the cell median.
✅ **DONE 2026-08-25 — the filter ships under Infill.** Infill had no 100 m grid
of its own, so this is what "housing" the thread there turned into: the
`#amenity` checkboxes draw over `infill-plane` as a translucent highlight (not
a metric, not a colour change to the hood score — `SPEC_development.md`
"Amenity distance"). ⚠️ **2026-08-26 — and ONLY under Infill**: the filter was
originally built in Money's Glass mode and 2026-08-25 widened the gate rather
than moving it, so both views offered it for a day; the Glass copy is now
removed (`DECISIONS.md` 2026-08-26). This is NOT the real per-cell Infill score
item 5 below still asks for; it is the cheapest correct placeholder pending
items 3 and 5. Band value is still a Peter call, unchanged (`TODO.md`).
⚠️ **One correction to the measurement above:** S115's probe graph included
railway centrelines, so its network distances could route along the LRT track.
The shipped graph excludes them; the 55% figure is if anything understated.

**Still open — in dependency order:**

1. ✅ **DONE 2026-08-22 — total absence of `gross_area` now emits `null`.**
   ⚠️ **PARTIAL coverage is still unhandled and is the live residual**: MAPLE
   RIDGE records a floor area on ~33% of its eligible rows, so its `far` is
   understated ~3× and it sits **#2 on the teal arm** of the shipped lens. A
   coverage threshold or a coverage-scaled FAR would reach it; **both need a
   "what fraction is enough" call, the same shape as the 0.90 set-aside
   threshold, and neither should be guessed.** See the findings §6a.
2. ✅ **DONE 2026-08-23 — the `T8` membership pass is paid, and the rule is
   STRUCTURAL.** A passenger station has a `location_type == 2` street entrance;
   exactly the 3 suspects have none, all 30 survivors have one. ⚠️ Trip counts
   could NOT have separated them (two tie exactly with Belvedere/Clareview at
   3,601 trips — they sit on the alignment). `DECISIONS.md` 2026-08-23.
3. **Per-cell replacements for `is_set_aside` and the asymmetric residential
   gate.** ⚠️ The gate is doing more work than the spec claims (it absorbs the
   `gross_area` gap), and per-cell its `f_res` is often measured on ONE point —
   so a naive port makes it weaker exactly where it matters most.
4. **The radius is a judgement, not a discovery.** 600 m clears the default
   column; the 3yr window wants 800 m. Whether the kernel radius should follow
   the window picker is undecided.
5. **What a 100 m infill spike should be HEIGHT-wise** is unasked. The shipped
   Infill view is a flat diverging plane, not spikes — Peter's "filled into each
   spike" implies an extrusion the lens has never had, and a signed diverging
   score has no natural height (which arm gets tall?).

## 13. The school amenity set is two boards out of five (NEW 2026-08-23, SOURCED, not built)

`dist_school_m` measures to **303 catchment schools** from EPSB + ECSD. Private,
charter and francophone (Conseil scolaire Centre-Nord) schools are **not in it**,
so the column overstates distance wherever one of those is nearest. Dataset facts
+ the three probes: `data/DATA.md` §20.

**Settled by probe 2026-08-23, do not re-derive:**
- **The property roll cannot answer it.** No field says what a building IS;
  `legal_description` is `Plan / Block / Lot`; **0 of 439,685 rows** mention
  "school".
- **Zoning cannot answer it either.** `US` — the zone schools nominally occupy —
  is on **one** parcel citywide, and `PS`/`PSN` (751/949) mean parks. Institutional
  land is hospitals, fire halls, worship and community leagues too.
- **Edmonton's portal has no such dataset.** The catalogue's `school` results are
  entirely EPSB/ECSD (locations, catchments, footprints, ward boundaries,
  historical vintages).
- **Alberta publishes lists that cover them — as PDFs**, not rows.

**Still open — and it is a JUDGEMENT, not a lookup:**
1. **Is a hand-built list worth its staleness?** Transcribing + geocoding the
   provincial PDFs is a few dozen points and `amenity_distance` takes any point
   frame, so the *work* is small. ⚠️ **The cost is that it would go stale
   SILENTLY** — the two board feeds re-download weekly and a manual list would
   not, so a school opening or closing keeps answering with the old geometry.
   That is the `archived-tables-still-answer` shape: reachable is not updated.
2. **If built, it needs the manual-reviewed-input treatment** (`DATA.md` §13/§16/
   §18 pattern): committed file, content-hash digest, a vintage row in
   `RUNBOOK.md` §0. Adding it as a quiet extra point set would be the worst of
   both — wider coverage, no freshness contract.
3. **The error direction is currently SAFE and would stay safe if left alone.**
   Missing schools means "further than you are", which under-claims proximity —
   the same direction as the node-snap and walk-proxy approximations. Closing the
   gap partially (say, private but not francophone) does not change that; it just
   moves the boundary.

## 14. A police cost driver — crime data exists, but not the kind this needs (NEW 2026-08-23, SOURCED, not built)

`SPEC_breakeven.md` §4a: **Police Service is $597.2M, the largest line in the
FY2025 register, with no spatial driver in hand.** Probed 2026-08-23 whether a
crime/incident dataset could supply one.

### The claim "OGC API - Records" is wrong — corrected for the record
A relayed claim said EPS's data was "accessible programmatically... through
OGC API - Records and GIS features." **OGC API - Records is a real but
different standard** (catalog/metadata discovery, not incident data). What
actually exists is a plain **Esri ArcGIS FeatureServer** — the same vendor
technology as this project's LRT/schools boundary layers, just a different API
shape than the Socrata `data.edmonton.ca` sources currently ingested.

### What's actually there
EPS's Community Safety Data Portal (`communitysafetydataportal.edmontonpolice.ca`)
is an ArcGIS Hub site (`data-eps1.hub.arcgis.com`). Confirmed live endpoints in
its service folder:

| service | what |
|---|---|
| `EPS_OCC_30DAY` | rolling 30-day window only — no use as a stable annual driver |
| `Historic_Occurrences_CSDP` | **the real one** — point geometry, Jan 2023 onward, ~293K incidents, 2,000 records/query (needs pagination) |
| `Neighborhoods`, `Ward Boundaries` | boundary layers also live in the same folder |

Fields on `Historic_Occurrences_CSDP`: `Reported_Date`, `Occurrence_Category`,
`Occurrence_Group`, `Occurrence_Type_Group`, `Intersection`. **No neighbourhood
or ward field** — same as schools/LRT, a point-to-polygon spatial join would be
needed, which this project already knows how to do.

### ⚠️ The publisher's own caveat undercuts the driver case, not just the join
Locations are **anonymized to the nearest intersection**, and EPS states why:
*"users should not rely on this data to assess safety or crime levels for
specific areas"* — high-foot-traffic areas report more incidents without
necessarily having more crime. That is the dataset's publisher warning against
the exact per-area comparison a police-cost driver would need. It does not
block the join technically; it means adopting this driver imports a
**documented, self-disclosed bias** into the largest line in the register,
which is a worse position than having no driver.

**Not a lookup — the same judgement `SPEC_breakeven.md` §4a already flags**:
allocating $597.2M by any spatial driver makes the driver choice do the
arguing. This finding doesn't resolve that; it closes off "find better data" as
the escape hatch. **PETER'S CALL**, same as before — population/dwelling
surfacing (`SPEC_breakeven.md` §4a Task 1b) remains the cheaper unblock if
police is to be reached at all.

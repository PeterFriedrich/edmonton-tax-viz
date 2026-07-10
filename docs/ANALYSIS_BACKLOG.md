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
`data/DATA.md` line ~308). Separate genuine exempt-dilution (U of A: high value,
low footprint) from low-value-land hoods (U of A Farm: high footprint, low value)
and from park/river-valley (already covered in item 1 / the lot-acre findings).

**Output:** a ranked list of exempt-institutional hoods + a FINDINGS note; feeds
both the lot-acre toggle framing and the services-lens cost-vs-revenue story.
Related: item 1 (outlier tails), the PRIORITY lot-acre toggle in `TODO.md`.

</details>

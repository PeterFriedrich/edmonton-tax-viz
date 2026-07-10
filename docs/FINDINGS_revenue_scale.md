# Findings — Revenue/Acre Distribution & Colour-Scale Choice

Captured 2026-06-29 while deciding how the web map should colour-encode
revenue-per-acre (and value-per-acre). Source: local snapshot
`data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv` (2025 data,
439,769 rows) and the derived `web/data/neighbourhood_value_per_acre.geojson`
(405 rendered neighbourhoods). Numbers below are from that snapshot and will
shift on re-download.

Purpose: record the empirical shape of the metric distributions and the reasoning
behind the colour transform, so the choice is documented and auditable rather than
asserted. Tagged for a later notebook pass (see "To visualize" at the end).

## 1. The problem: a hard colour clamp reads as a threshold

The map encodes magnitude two ways: **height** (raw value, linear) and **colour**
(a sequential ramp). Colour currently saturates at a fixed clamp — `$50,000` for
revenue/acre, `$4,000,000` for value/acre — so every neighbourhood at or above the
clamp shares the identical peak colour.

| metric | clamp | clamp percentile | # saturated | spread above clamp |
|---|---|---|---|---|
| revenue_per_acre | $50,000 | ~p97.3 | 11 of 405 | $50k → $250k (5×) |
| value_per_acre | $4,000,000 | ~p97.5 | 10 of 405 | $4M → $13.8M (3.4×) |

Two issues:
- The saturated cluster reads as a **meaningful threshold** ("these are the maxed-out
  ones") when it is only a display device. It is most visible on ramps with a
  distinct bright peak.
- The clamp is a **round number**, which reads as chosen rather than derived.

Height is *not* clamped, so true magnitude is still encoded honestly in height —
the plateau is a colour-channel artifact only.

## 2. Why a clamp exists at all: severe right skew

| metric | min | median | p90 | p99 | max | orders of magnitude |
|---|---|---|---|---|---|---|
| revenue_per_acre | $2 | $17,592 | $34,659 | $60,967 | $249,973 | 5.2 |
| value_per_acre | $173 | $1,733,540 | $3,109,480 | $5,231,534 | $13,782,602 | 4.9 |

Without a clamp, a linear colour scale to the true max would place the **median at
7%** of the revenue ramp (13% for value) — almost the whole city near-black, only
Downtown coloured. The clamp pulls the median up to ~35% (43% for value). It is a
legitimate response to skew; the *hard edge* is the problem, not the intent.

## 3. The distribution is a two-population mixture

Testing log-normality (a log-normal distribution has log-skew ≈ 0):

| metric | raw skew | log skew |
|---|---|---|
| revenue_per_acre | +5.83 | −2.16 |
| value_per_acre | +2.72 | −2.08 |

The log transform **over-corrects into left skew** — the signature of mixing two
populations. Re-running the skew on revenue as the near-zero tail is trimmed:

| trim below | n | raw skew | log skew |
|---|---|---|---|
| — (all) | 405 | 5.83 | −2.16 |
| $1,000 | 354 | 6.75 | −1.17 |
| **$2,000** | 348 | 6.90 | **−0.22**  ← ≈ log-normal |
| $5,000 | 339 | 7.08 | +0.71 |

Log-skew crosses ~0 once the bottom ~57 neighbourhoods are removed, while raw skew
*rises* (the top tail is untouched). That is a **log-normal taxable core plus a
separate near-zero spike** — two populations that should not share one continuous
colour scale.

> **Warning — circular definition.** The $2,000 trim above *proves the two-population
> structure exists*; it is **not** a production method. Defining a population by the
> low revenue you are trying to explain is circular and indefensible. The split must
> be by an independent category (see §4).

## 4. What the near-zero spike actually is (correction)

Initial assumption (carried in earlier handoffs): the spike is **tax-exempt land**
(Legislature, government campuses) reading low because the denominator is full
boundary area with a $0 exempt numerator. **The data does not support this.**

- **`is_exempt` flags 3 parcels citywide** (Assessment Class 1 == `NONRES
  MUNICIPAL/RES EDUCATION`), ~$0.01B total.
- **Every one of the 57 near-zero neighbourhoods has `exempt_share = 0.00`.** No
  neighbourhood citywide exceeds 0.5.
- The 46 rows dropped on load for $0/null assessed value are all
  RESIDENTIAL/COMMERCIAL/FARMLAND — no institutional land hiding there.

**Tax-exempt institutional land is absent from the taxable assessment roll
entirely** — not flagged, not zeroed, not dropped. It contributes nothing to the
numerator while its area still sits inside a neighbourhood's boundary denominator.

The spike is instead **low taxable coverage** — few taxable parcels over a large
boundary polygon:
- **55 of 57** have <200 parcels (many under 25).
- **20 of 57** are `RIVER VALLEY …` (natural area); others are golf courses,
  `ANTHONY HENDAY …` ring-road margins, energy parks, and undeveloped town centres.
- Examples: RIVER VALLEY KENDAL $2/acre (3 parcels); MILL WOODS GOLF COURSE $4/acre
  (2 parcels).

So the genuine split is **taxable-developed vs. low-coverage natural/undeveloped
land** — separable by land-use/coverage, *not* by exempt status.

## 5. Methodology caveat (record regardless of downstream choices)

Because exempt institutional land is absent from the roll, revenue/acre
**understates** any neighbourhood that contains large exempt institutions. This is a
limitation of the source, not a modelling choice, and should be disclosed.

The tax roll itself gives no way to detect which neighbourhoods those are. The
zoning layer (`src/load_zoning.py`) now provides a **partial** proxy: its
institutional codes — `UI` (Urban Institution), `UF` (Urban Facilities), `AJ`
(Alternative Jurisdiction), `PU` (Public Utility) — flag *where* exempt-roll
understatement is most likely to sit. This is a proxy only: zoning marks what a
parcel is *zoned for*, not its *tax status*, so the flag neither confirms exempt
land nor quantifies the understatement. These codes stay **on** the colour scale
(classified `inst`, not set aside); the flag is a caveat aid, not an exclusion.

## 6. Colour-transform options

Height stays **linear** throughout (the standing honesty choice — Downtown's spike
is the signal). The question is colour only.

| option | hard cap? | plateau? | fit to this data |
|---|---|---|---|
| linear + clamp (current) | yes | yes | compresses low end; round-number critique |
| percentile cap (e.g. p99 = $60,967) | yes | smaller (6 saturate) | defensible/mechanical, but still a hard edge |
| **sqrt, no cap** | no | no | tames +5.83 skew without exploding the near-zero floor; robust while the mixture is unsplit |
| log, no cap | no | no | **correct for the taxable core once split** (≈ log-normal); over-corrects on the *mixed* distribution |
| rank / quantile | no | no | fully smooth, but encodes order not amount |

**Decision logic:** split the low-coverage population out first (§4, by category).
Then re-run the §3 skew test on the **category-defined** taxable set. If it is
≈ log-normal (likely), use **log** for the taxable colour scale and display the
low-coverage set separately. If it stays mixed, **sqrt** is the no-set-aside
fallback.

### 6.1 Result — DECIDED: sqrt (2026-07-01)

Ran that test on the zoning-defined taxable set (`is_set_aside` from
`src/load_zoning.py`; 48 of 405 hoods set aside at the locked ≥0.90 threshold).
Reproduce with `scripts/investigate_skew.py` (biased skew, matching §3):

| set | metric | n | raw | sqrt | log |
|---|---|---|---|---|---|
| all | revenue_per_acre | 405 | 5.83 | **0.36** | −2.16 |
| **excl set-aside** | revenue_per_acre | 357 | 6.62 | **1.55** | **−4.19** |
| all | value_per_acre | 405 | 2.72 | **−0.35** | −2.08 |
| **excl set-aside** | value_per_acre | 357 | 3.54 | **0.21** | −3.88 |

**The taxable core is NOT log-normal at the 0.90 threshold — the opposite of the
§6 prediction.** Excluding the set-aside hoods pushes log-skew *further* negative
(revenue −2.16 → −4.19), because the exclusion removes only the ≥0.90 hoods while
the **mixed 0.55–0.90 band stays on the scale by design** and still holds
near-zero-revenue land. The dozen lowest-revenue kept hoods are all in that band —
RIVER VALLEY KENDAL $1.76/acre (set-aside 0.78), ANTHONY HENDAY MISTATIM $702
(0.86), RIVER VALLEY CAMERON $325 (0.66) — their tiny revenue dominates the left
log-tail. This is not a bug in the threshold: keeping underdeveloped-but-developed
land on the scale is the fiscal story (§SPEC_revenue). It just means a single
**log** scale over-corrects.

**sqrt** is well-behaved everywhere (|skew| ≤ 1.55 across every cut; 0.36 / −0.35
on the full set) — it tames the right skew without exploding the near-zero floor,
and does not assume a clean log-normal core that the data does not have. **Use sqrt
for colour.** Height stays linear regardless.

Candidate methodology statement:

> Colour encodes a square-root transform of the metric; height encodes the raw
> linear value. Natural/undeveloped set-aside neighbourhoods (zoning ≥90% never +
> not-yet) are shown in neutral grey, excluded from the colour-scale fit.
> Tax-exempt institutional land is absent from the source assessment roll, so
> revenue/acre understates neighbourhoods containing such land; these cannot be
> identified from the available data.

### 6.2 Residential-only rescale confirms the mill-rate skew lives in revenue (2026-07-01)

The residential-only lens (`web/index.html`, `is_residential` from
`load_zoning.py`) rescales colour to the p97.5 of just the 226 residential hoods.
That clamp lands very differently for the two metrics:

| metric | full-set clamp (≈p97.5) | residential-only clamp | shift |
|---|---|---|---|
| revenue_per_acre | $50,000 | **$36,784** | −26% |
| value_per_acre | $4,000,000 | **$3,881,318** | −3% |

Removing non-residential land drops the **revenue** ceiling by a quarter but leaves
the **value** ceiling almost untouched. This is empirical, neighbourhood-level
confirmation of what `SPEC_revenue.md` asserts only from the rate schedule: Edmonton's
non-residential mill rate is ≈ 3.2× residential, so commercial/industrial land drives
the high revenue/acre tail — but assessed *value*/acre is not class-differentiated, so
its residential range is essentially the whole-city range. The mill-rate skew is a
**revenue** phenomenon, exactly where theory places it. (This is also why the
residential lens visibly re-spreads the Revenue view but barely changes Value.)

### 6.3 Road supply is near-symmetric — DECIDED: linear colour (2026-07-01)

`road_m_per_acre` (services lens, `SPEC_services.md`: city-maintained
collector + local metres per boundary acre) ran through the same biased-skew
test as §6.1 (`scripts/investigate_skew.py`, roads now in `METRICS`):

| set | n | raw | sqrt | log |
|---|---|---|---|---|
| all | 400 | **−0.29** | −0.92 | −3.00 |
| excl set-aside | 357 | **−0.43** | −1.16 | −4.77 |

Raw is already the best-behaved by a wide margin — sqrt and log both
over-correct into the left tail. Unlike revenue (5+ orders of magnitude),
road supply is **physically bounded**: an acre only fits so much road
(observed 0–60.0 m/acre, median 32.6, max/median 1.84×). A bounded,
near-symmetric quantity needs no compression. **Colour for
`road_m_per_acre` is LINEAR** (same decision criterion as §6.1 — minimize
|skew| — opposite outcome). Clamp candidate ≈ p97.5 = 53 m/acre, per the
established convention. Height, as always, stays linear.

(The 6 zero-road hoods: 5 are set-aside — river valley / ring-road margins —
and render grey anyway; zeros sit honestly at the bottom of a linear ramp,
another reason no log.)

### 6.4 Revenue per road metre is ~log-normal — DECIDED: log colour (2026-07-02)

The ratio view's metric (`revenue_per_acre / road_m_per_acre` — acres cancel:
$ of municipal revenue per metre of city-maintained collector+local road) ran
through the same biased-skew test, computed from the web GeoJSON's two
published columns (no pipeline change; derivation is client-side too):

| set | n | median | p97.5 | max | raw | sqrt | log |
|---|---|---|---|---|---|---|---|
| all computable | 400 | $537 | $4,629 | $1,314,509 | 19.72 | 16.18 | **0.32** |
| excl set-aside | 357 | $568 | $5,468 | $1,314,509 | 18.62 | 15.48 | 2.74 |

The first log-transform metric in the project — a ratio of two positive
quantities coming out ~log-normal is the textbook case, and sqrt barely
dents a 19.7 skew. **Colour is LOG**, anchored between the kept subset's
p2.5 and p97.5 (computed at runtime in `web/index.html` `ratioScale()`,
≈ $264–$3,253 on 2026-07-02 data). Height, as always, stays linear.

**The denominator-artifact tail is real and must be floored, not clamped
away:** WESTVIEW VILLAGE's ratio is $1,314,509/m (next: KENDAL $96,132) —
near-zero road base, exactly the low-denominator artifact
`ANALYSIS_BACKLOG.md` item 1 anticipated. Hoods with `road_m_per_acre <
5` (`RATIO_ROAD_FLOOR`) render grey + flat ("insufficient road base"),
alongside the set-asides; the 6 zero-road hoods have no ratio at all and
fall under the same floor. The floor is display-only and tunable.

**Residential subset (2026-07-03, for the lens):** the kept residential
hoods' anchors are p2.5 ≈ $258 / p97.5 ≈ $916 / max $2,197 (n=223) vs the
full kept set's $264 / $3,253 / $18,025 (n=339). The floor barely moves but
the ceiling drops ~3.5× — the ratio's entire high tail sits on
non-residential land, the same mill-rate mechanism as §6.2 seen through the
road denominator. The lens therefore rescales the log colour anchors to the
residential kept subset (the ratio analogue of `residentialClampFor`);
height stays on the full-subset scale.

Urban3's value-per-acre work is **parcel-level** (e.g. the Asheville comparison: an
edge Walmart ≈ $6,500/acre vs. a downtown building ≈ $634,000/acre, ~100×). This
project is **neighbourhood-aggregate**, which structurally compresses the spread —
so a narrower range here is expected, not a weakness. Urban3 publishes no
methodology for handling the skew (the scaling lives inside an Esri/Blender
pipeline), so documenting the transform explicitly is a more auditable position,
not a deviation from a standard.

### 6.5 Fire demand is the most skewed metric yet — DECIDED: sqrt colour (2026-07-06)

`fire_events_per_acre` (SPEC_services "Fire lens"; shipped provisionally
linear because the build session had no data access) ran through the same
biased-skew test on the first real numbers (post-PR-#18 refresh, 406 hoods,
5 true zeros):

| set | n | median | p97.5 | max | raw | sqrt | log |
|---|---|---|---|---|---|---|---|
| all (positive) | 401 | 0.45 | — | 17.87 | 7.86 | **2.42** | −1.48 |
| excl set-aside | 354 | — | 2.96 | 17.87 | 7.58 | **2.70** | −1.48 |

Raw skew +7.86 beats revenue_per_acre's +5.83 — the worst in the project.
On the shipped scale (linear, clamp = p97.5 of non-set-aside = 2.96), the
clamp/median ratio is **5.8×** (storm's is ~1.8×, which is why storm stays
linear): the median hood sits at 17% of the ramp and **59% of hoods occupy
the bottom fifth** — the map reads as downtown-plus-uniform-void.
WÎHKWÊNTÔWIN at 3.5 events/acre and a 0.3 suburb render nearly alike.

**Log is rejected** on the §6.1 grounds: it over-corrects the mixed
distribution into left skew (−1.48; not a log-normal core), and fire has 5
true-zero hoods where log is undefined and would need an arbitrary floor.
**sqrt** puts the median at 42% of the ramp and drops the bottom-fifth
share to 11% — the same robust no-assumptions choice as the revenue/value
colour. Height: still no extrusion (flat plane); tooltip stays raw.

### 6.6 Water/sewer charge is storm-shaped — DECIDED: linear colour (2026-07-07)

`water_charge_per_acre` (SPEC_utilities Lens 2, first real run) through the
same test (406 hoods, 54 true zeros — hoods with no residential roll
records):

| set | n | median | p97.5 | max | raw | sqrt | log |
|---|---|---|---|---|---|---|---|
| all (positive) | 352 | 4,986 | — | 43,955 | 3.40 | −0.25 | −1.59 |
| excl set-aside | 316 | — | 12,164 | 43,955 | 3.89 | −0.24 | −2.59 |

Despite the raw +3.4, this is the storm case, not the fire case:
**clamp/median is 2.2×** (storm ~1.8×, fire 5.8×) — the skew lives entirely
in the p97.5-clamped tail. On the shipped scale, linear puts the median
hood at 44% of the ramp with 25% of hoods in the bottom fifth (healthy);
sqrt statistically over-corrects (−0.25) and pushes the on-ramp median to
67% — top-compressed. **Linear**, matching storm. Height: none (flat plane).

### 6.7 Revenue per fire event is the §6.4 case again — DECIDED: log colour + 0.005 floor (2026-07-10)

The Ratio view's second denominator (`revenue_per_acre / fire_events_per_acre`
— acres cancel: $ of municipal revenue per dispatched fire-department event;
SPEC_utilities decision 3's per-service picker) through the same biased-skew
test, computed from the web GeoJSON's two published columns (client-side
derivation, no pipeline change):

| set | n | median | p97.5 | max | raw | sqrt | log |
|---|---|---|---|---|---|---|---|
| all computable (events > 0) | 401 | $37,123 | $342,082 | $1,686,489 | 7.30 | 3.21 | −0.76 |
| kept (excl set-aside, floor) | 350 | $39,655 | $298,901 | $472,418 | 2.78 | 1.57 | **+0.13** |

The ratio-of-two-positive-quantities log-normal pattern of §6.4 holds:
**colour is LOG**, anchored between the kept subset's p2.5 and p97.5
(runtime `ratioScale()`, ≈ $7,092–$298,901 on 2026-07-09 data). Note the
contrast with §6.5: the fire *supply* metric rejected log (true zeros,
left over-correction), but the *ratio*'s floor removes the zeros by
construction and the kept core is cleanly log-normal. Height, as always,
stays linear (parity: the tallest kept hood matches the other views' peak).

**The denominator-artifact tail is real here too and gets the §6.4 floor
treatment:** four zero-event hoods (CROSSROADS, KENDAL, QUARRY RIDGE, RIVER
VALLEY KENDAL — no ratio at all) plus four annexed-fringe hoods below
0.005 events/acre/yr (MARQUIS 0.0011, MATTSON 0.0016, RIVER'S EDGE 0.0020,
ALCES 0.0024) whose ratios explode to $1.3–1.7M/event on a near-zero event
base. **Floor = 0.005 events/acre/yr** (≈ the kept subset's p2.5; the next
hood up, KINGLET GARDENS at 0.0149, is a genuinely developing suburb) —
greyed + flat ("too few fire events"), display-only and tunable
(`RATIO_DENOMS.fire.floor`).

**Residential subset (for the lens):** kept residential anchors are p2.5 ≈
$7,406 / p97.5 ≈ $101,413 / max $403,433 (n=226) vs the full kept set's
$7,092 / $298,901 / $472,418 (n=350). Same shape as §6.4: the floor barely
moves, the ceiling drops ~2.9× — the high tail is non-residential
(mill-rate mechanism, §6.2). The lens rescales the log colour anchors to
the residential kept subset; height stays on the full-subset scale.

Skew numbers here are reproducible headless via `scripts/investigate_skew.py`
(`skew_table` / `load_metrics` / `lowest_kept` are importable). The plots below are
the remaining visual confirmations:

- Histogram of revenue/acre and value/acre on linear vs. sqrt vs. log axes — show
  the plateau and the log over-correction directly.
- The two-population mixture: overlay the taxable core and the near-zero spike;
  mark where the log-skew crosses 0 as the tail is trimmed.
- Per-neighbourhood parcel count (coverage) vs. revenue/acre — confirm the spike is
  a coverage phenomenon.
- Map the 57 low-coverage neighbourhoods (River Valley / ring-road / undeveloped)
  to confirm they are land-use, not exempt, cases.

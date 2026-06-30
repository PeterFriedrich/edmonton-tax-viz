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
**understates** any neighbourhood that contains large exempt institutions, and the
data gives **no way to detect which neighbourhoods those are**. This is a limitation
of the source, not a modelling choice, and should be disclosed.

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

Candidate methodology statement:

> Colour encodes a square-root (or log, for the taxable core) transform of the
> metric across the full distribution; height encodes the raw linear value.
> Low-coverage natural/undeveloped neighbourhoods are displayed separately.
> Tax-exempt institutional land is absent from the source assessment roll, so
> revenue/acre understates neighbourhoods containing such land; these cannot be
> identified from the available data.

## 7. Context: Urban3

Urban3's value-per-acre work is **parcel-level** (e.g. the Asheville comparison: an
edge Walmart ≈ $6,500/acre vs. a downtown building ≈ $634,000/acre, ~100×). This
project is **neighbourhood-aggregate**, which structurally compresses the spread —
so a narrower range here is expected, not a weakness. Urban3 publishes no
methodology for handling the skew (the scaling lives inside an Esri/Blender
pipeline), so documenting the transform explicitly is a more auditable position,
not a deviation from a standard.

## To visualize (notebook later)

- Histogram of revenue/acre and value/acre on linear vs. sqrt vs. log axes — show
  the plateau and the log over-correction directly.
- The two-population mixture: overlay the taxable core and the near-zero spike;
  mark where the log-skew crosses 0 as the tail is trimmed.
- Per-neighbourhood parcel count (coverage) vs. revenue/acre — confirm the spike is
  a coverage phenomenon.
- Map the 57 low-coverage neighbourhoods (River Valley / ring-road / undeveloped)
  to confirm they are land-use, not exempt, cases.

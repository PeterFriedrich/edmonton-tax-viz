# Findings — Data-Integrity Audit (first run of the DATA_INTEGRITY brief)

Captured 2026-07-01, running `docs/DATA_INTEGRITY.md` end to end against the
live snapshot `data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv`
(439,685 rows at audit time) and the current `master` code. Numbers below are
from that snapshot and will shift on re-download.

Purpose: record the verdict on each of the brief's ranked targets (T1–T7) plus
what the completeness pass surfaced, so fixes can be applied and re-verified
against a written baseline. **Verdicts here are point-in-time; the brief is the
reusable instrument, this doc is one run's output.**

Method notes: verdicts follow the brief's evidence standard — actual lines read,
claims tested against live data where possible. Two checks went beyond code
reading: a spatial containment test (assessment lat/lon → boundary polygon) to
resolve the unmatched-name cases, and a duplicate-account scan for the
aggregation grain.

---

## Summary table

| # | Target | Verdict |
|---|---|---|
| T3 | Heritage Valley Town Centre value | **BUG (blocking)** — rendered at ~1/250th of real value |
| T3 | Lewis Farms Industrial | **BUG** — $106M dropped, boundary renders as a hole |
| T2 | Roll-year / rate vintage alignment | **BUG (latent)** — no guard anywhere |
| T3c | Unmatched-set visibility in CI | **BUG (process)** — warning-only |
| NEW | Socrata `$limit` truncation | **BUG (latent, low likelihood)** |
| T1 | Class → rate mapping | CONFIRMED-correct (municipal), 3 footnotes |
| T4 | Aggregation grain / denominator | CONFIRMED-correct |
| T5 | CRS end to end | CONFIRMED-correct |
| T6 | Zoning bucketing | CONFIRMED-correct |
| T7 | Frontend representation | CONFIRMED-correct |

---

## 1. BLOCKING — Heritage Valley Town Centre renders at ~1/250th of its value [T3]

**Verdict: BUG (blocking).** The one materially wrong number on the live map at
audit time.

**Evidence.** `src/load_assessment.py` `NAME_CORRECTIONS` (~ln 16) has no entry
for `HERITAGE VALLEY TOWN CENTRE AREA`. In the live snapshot:

| Assessment name | Rows | Assessed value |
|---|---|---|
| HERITAGE VALLEY TOWN CENTRE (matches boundary) | 15 | $2,253,500 |
| HERITAGE VALLEY TOWN CENTRE AREA (unmatched, dropped) | 946 | $570,417,000 |

Spatial containment test: **945 of the 946** unmatched properties fall inside
the HERITAGE VALLEY TOWN CENTRE boundary polygon (1 in adjacent Desrochers).

**Impact.** Because a *partial* match exists, the neighbourhood **renders** —
with value/revenue per acre understated ~250×. This is the exact
plausible-but-wrong failure mode the brief targets: not a visible hole, a
confident wrong number on a public map.

**Why it was missed.** DATA.md's "Name Matching" section lists this as one of
three known-unresolved unmatched names. What wasn't recognized is that the
boundary side also has a small direct match, so "unmatched = excluded from map"
(the assumed failure mode, visible) was actually "partially matched = rendered
wrong" (invisible).

**Fix.** Add to `NAME_CORRECTIONS`:
`"HERITAGE VALLEY TOWN CENTRE AREA": "HERITAGE VALLEY TOWN CENTRE"` — the same
pattern as the existing `CHAPPELLE AREA → CHAPPELLE` entry. Corrections apply
before aggregation, so the two name groups sum correctly.

## 2. Lewis Farms Industrial — $106M dropped, hole in the map [T3]

**Verdict: BUG.**

**Evidence.** `LEWIS FARMS INDUSTRIAL` (103 rows, $106,304,000) is unmatched
and dropped. The boundary hood `LEWIS FARMS BUSINESS EMPLOYMENT` has zero
assessment rows under its own name → `value_per_acre` NaN → dropped at export →
hole in the rendered map. Spatial test: **100 of 103** properties fall inside
LEWIS FARMS BUSINESS EMPLOYMENT (3 spill into adjacent LEWIS FARMS — boundary-
edge cases, same order of imprecision as the source's own neighbourhood labels).

**Fix.** `"LEWIS FARMS INDUSTRIAL": "LEWIS FARMS BUSINESS EMPLOYMENT"`.

**Also resolved.** `OLIVER` (1 remaining row, $500) sits inside
**WÎHKWÊNTÔWIN** — the 2024 rename. *(Correction, post-write-up: DATA.md
"Name Matching" records a deliberate, documented decision NOT to map this $500
straggler onto the $4.12B neighbourhood — respected; no entry added.)* With the
two material corrections applied, the expected unmatched set is **exactly the
OLIVER straggler** (useful as a CI assertion baseline — see §4).

## 3. Roll-year / mill-rate vintage: unguarded [T2]

**Verdict: BUG (latent).** The top forward-looking hazard; the only integrity
risk in the pipeline with **no guard at all**.

**Evidence.**
- `main.py` ~ln 57: `ASSESSMENT_YEAR = 2025` — hardcoded pin.
- The live CSV has **no year column** (verified against the snapshot's 19
  columns) — the roll vintage exists only in Socrata *metadata*.
- `data/mill_rates.json` contains only 2025.
- `scripts/generate_status.py` ~ln 45: `DATA_YEAR = 2025`, `RATE_YEAR = 2025` —
  constants, so after a roll even the provenance display would be wrong.
- Nothing anywhere compares downloaded-roll-year to the pin.

The dataset is named "Current Calendar Year": when Edmonton rolls the feed to
the 2026 roll, the weekly CI keeps running, applying 2025 rates to 2026
assessments. Every revenue number wrong; nothing crashes; `status.json` claims
2025 data.

**Fix direction** (per SPEC_deployment "Year alignment", still unbuilt): fetch
the Socrata metadata year in CI and hard-fail — or auto-set the maintenance
banner — when it differs from `ASSESSMENT_YEAR`. The banner machinery for the
holding window already exists (`generate_status.py --banner`).

## 4. Unmatched-set changes are warning-only in CI [T3c]

**Verdict: BUG (process).**

**Evidence.** `src/join_and_calculate.py` ~ln 40–56: unmatched names
`logger.warning(...)` and proceed. `.github/workflows/refresh.yml` runs pytest
(synthetic fixtures) before regenerating, but nothing asserts live-data match
counts. A new naming drift in an unwatched weekly run scrolls past unread —
finding #1 demonstrates the cost.

**Fix direction.** Commit the expected-unmatched list (empty once §1–§2 land)
and fail the CI build when the actual set differs. That converts this whole
finding class from warn-silent to fail-loud, matching the project rule.

## 5. Downloader trusts Socrata not to truncate [NEW, from completeness pass]

**Verdict: BUG (latent, low likelihood).**

**Evidence.** `scripts/download_data.py` `SOURCES`: boundaries fetched with
`$limit=500` (407 features today), zoning with `$limit=20000` (~11.5k). Socrata
truncates **silently** at `$limit`. The atomic `.part` write guards mid-stream
network failure, but a short server-side response is a complete, valid,
truncated file. Truncated boundaries = neighbourhoods silently vanish.

**Fix direction.** Post-download assertion: feature count strictly below the
`$limit` (and within tolerance of the expected count).

---

## Confirmed-correct targets

### T1 — Class → rate mapping (municipal)
All mapped rate classes exist in `mill_rates.json` 2025; the live feed has zero
unmapped labels; exempt → $0 is correct; `DESIGNATED IND PROPERTIES → Non
Residential` is consistent with those parcels' own `Tax Class`. Footnotes:

1. `MA DERELICT RESIDENTIAL → "Non Residential"` bills the identical municipal
   rate (24.2229) as the dedicated "Mature Area Derelict Residential" class, so
   no current impact — but their *education* rates differ (3.9762 vs 2.4366).
   Latent trap if `rate_type` ever changes from `"municipal"`. Mapping to the
   dedicated class would be more faithful.
2. Farmland 2025 municipal is a **documented assumption** (source stopped
   publishing a Farmland row; set = Residential, which held 2014–2024). Flagged
   in the JSON; 509 parcels, low impact.
3. 80 live rows have class percentages summing ≠ 100; billed as-stated with a
   warning — the intended conservative choice (normalizing would invent which
   class the missing share belongs to).

Also noted: `mill_rates.json` notes say hyphenated class-name variants are
"normalized on load", but `load_mill_rates` does no normalization. The failure
mode is a loud KeyError, so this is doc-vs-code divergence only.

### T4 — Aggregation grain / denominator
439,685 rows, 439,685 unique `Account Number`s, **zero duplicates** — the
groupby-sum cannot double-count. Condo units are separately assessed accounts
(summing is correct). `area_acres` = projected-m² / 4046.856422. Zero-area
neighbourhoods → NaN → dropped at export with names logged. Colour clamps are
fixed constants (`METRICS.colorClamp`), so export drops cannot skew the scale.

### T5 — CRS
Full sweep of `src/` + `main.py`: every `.area` / `.buffer` / `.simplify` runs
after `to_crs(3400)`; `load_zoning` raises if boundaries aren't EPSG:3400;
3400→4326 happens only at export (display); no EPSG:26911 anywhere. The one
soft spot — `load_zoning` *assumes* 4326 when the zoning file's CRS is missing —
is warned, documented (DATA.md §5), and correct for the source.

### T6 — Zoning bucketing
Unknown codes warn and default to `nonres` — stay on scale, never claimed
residential, never dropped. Fractions are shares of summed per-category area,
so they sum to 1 by construction; set-aside ∩ residential is impossible
(0.90 + 0.50 > 1). Degenerate zero-zoned-area case yields NaN fractions →
both flags False → conservative.

### T7 — Frontend
`scaleT` (sqrt of clamped ratio) is monotonic — a larger value can never render
dimmer; over-clamp values cap at the ramp top (capped, not hidden). The legend
samples `√p` in value space, so displayed colour matches rendered colour.
Elevation is strictly linear. `updateTriggers` include metric/ramp/lens, so no
stale accessor renders.

---

## Minor / cosmetic

- `data/DATA.md` row count (439,769, dated 2026-05-27) has drifted to 439,685 —
  the count is dated in the doc, so this is expected live-feed drift, not an
  error.
- `load_assessment` drops zero/null `assessed_value` rows at INFO level; those
  rows contribute $0 by construction, and the drop is logged.

---

## Bottom line

The pipeline's engineering integrity is solid — CRS, aggregation grain, rate
math, zoning bucketing, and frontend representation all confirmed correct. But
the published map carried **one materially wrong number at audit time**:
Heritage Valley Town Centre at ~1/250th of its real value ($2.25M rendered vs
$572.7M actual), fixable with one `NAME_CORRECTIONS` line, plus $106M
recoverable for Lewis Farms Business Employment. The single highest-leverage
hardening is the **year-alignment guard (§3)** — the weekly CI schedule makes
its eventual trigger a certainty, not a possibility.

**Status of fixes (updated 2026-07-01, same day):**
- **§1 + §2 FIXED** (PR #5): both `NAME_CORRECTIONS` entries added; export now
  406/407 boundaries. **Deployed and verified live**: HVTC $1,977,595/acre
  value, LFBE $656,128/acre. (OLIVER deliberately left unmapped per DATA.md —
  see §2 correction note.)
- **§3 FIXED** (PR #7): `scripts/check_year_alignment.py` + `refresh.yml`
  wiring. First production run took the aligned path correctly (regen ran,
  holding-banner step skipped). Auto-fetching new-year rates remains a
  follow-on (TODO).
- **§4 + §5 OPEN** — tracked in `TODO.md` "Data-integrity audit follow-ons".

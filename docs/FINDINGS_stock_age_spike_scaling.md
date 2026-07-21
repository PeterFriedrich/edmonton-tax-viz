# Findings — Stock-age spike heights read uniformly tall (baseline fix)

**Date:** 2026-07-21. Context: the Development view's **Spikes → Year built**
map (`median_year_built` per 100 m cell, `export_value_grid`; shipped
2026-07-17, DECISIONS). Observation from Peter: *every* spike reads tall, and
new-build areas don't stand out the way they should. Reproducible against the
served grid via the snippet in §1 (34,675 cells, 31,180 with a known year).

## The question

Height was `(year − lo) / span`, **baselined at the single oldest cell and
linear in year**, where `lo`/`hi`/`span` came from the true min/max cell. If
the oldest cell is a lone pre-war outlier, the whole distribution floats high
off the floor and the height range is wasted on a decade band nothing occupies
— so mature and new stock both read tall and fail to separate.

## Diagnosis — the baseline is a lone 1904 outlier

Median-year-built distribution over the 31,180 known-year cells:

| pctile | year |   | pctile | year |
|---|---|---|---|---|
| p0 (min) | **1904** | | p50 | 1986 |
| p1 | 1944 | | p75 | 2006 |
| p2.5 | **1950** | | p90 | 2017 |
| p5 | 1954 | | p95 | 2021 |
| p10 | 1958 | | p97.5 | 2023 |
| p25 | 1970 | | p100 | 2025 |

The floor (1904) is a genuine outlier: **p1 is already 1944**, so almost
nothing lives in the first ~40 years, yet that dead band ate the bottom third
of every spike. Under the old true-min baseline (span 1904→2025 = 121 yr):

| cell | year | height (old, base 1904) |
|---|---|---|
| p25 (mature) | 1970 | **55 % of peak** |
| p50 | 1986 | **68 %** |
| p75 | 2006 | 84 % |
| p90 (new-ish) | 2017 | 93 % |

A genuinely new build (2017) stood only ~1.4× taller than a 1970s
neighbourhood — everything read as "tall," new-build did not pop. Two causes
compound: **(1)** the dead 1904→1944 offset, and **(2)** linear-in-year gives
recency no extra emphasis.

## Options considered

1. **Raise the height baseline to a percentile (p2.5 = 1950)** — the anchor the
   *colour* ramp already uses (`AGE_COLOR_LO_Q`). Span collapses to 1950→2025 =
   75 yr; median drops 68 % → **48 %**, p25 → **27 %**; new-build towers. The
   oldest ~2.5 % of cells floor flat (they already read as the darkest colour).
   Mildest change: height simply adopts the colour anchor that already exists —
   no new honesty caveat, no nonlinear distortion of an interval scale.
2. **Convex (accelerating) height transform** — power > 1 on normalized height
   so recency accelerates. Delivers "new-build much higher," but reopens the
   2026-06-25 **"linear elevation, no power curve"** decision (super-linear
   exaggeration is unacceptable for scrutinised civic numbers) — held OPEN.
3. **Rank/percentile (histogram-equalization) height** — smoothest by
   construction, but destroys absolute-time proportionality (a decade in the
   sparse pre-war tail would look like a decade in the dense 2000s). Too much
   distortion for this project's honesty rules. Rejected.
4. **Clip to a narrative era window** (baseline at a chosen 1950/1960) — same
   mechanism as #1 but with a judgment-call anchor instead of a data-driven
   percentile. Percentile is more defensible and self-adjusting across refreshes.

## Verdict

**Ship #1: baseline the heights at the p2.5 colour anchor.** Height and colour
now share one floor (both `(year − p2.5) / (max − p2.5)`, one extruded, one into
the ramp) — the most honest possible pairing, and it fixes the root cause
(the dead pre-war offset) with no nonlinear transform. The heights-never-
percentile-*clamped* rule is preserved in spirit: the **top** is never clamped
(the newest cell still hits full peak); only the **floor** moves up to the same
p2.5 the colour ramp already anchored on, so the oldest 2.5 % sit flat rather
than each carrying a ~40-year constant offset. Spike emphasis beyond this (#2)
stays held under the 2026-06-25 no-power-curve decision.

## Feeds

- DECISIONS.md line (2026-07-21) refining the 2026-07-17 stock-age spike entry.
- `verify-age-spikes.js` updated: the height-baseline assertion now checks the
  p2.5 anchor (shared with colour) rather than the true oldest cell.
- Blurb + code comments in `web/index.html` (`ageGridLayer`, `devBlurb`).

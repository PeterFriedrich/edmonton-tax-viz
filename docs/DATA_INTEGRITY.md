# Data-Integrity Audit Brief

> **Who this is for.** A model pointed at this repo to check that the numbers on
> the map are *right* — not that the code is stylish or that it runs. Written to
> be read cold, without the rest of the session context.
>
> **Model note.** This brief assumes the reading model is doing **verification,
> not discovery** — the risk-ranking below was already done by a stronger model
> with this repo's history in view. Your job is to confirm or refute each claim
> against the actual code and data, in the given order. Do **not** treat the list
> as exhaustive of all bugs; treat it as "the places most likely to be silently
> wrong, ranked." A final "what did the ranking miss?" pass is part of the job
> (see [§4](#4-completeness-pass)).

---

## 0. What you are optimizing for

**Silent wrong numbers, not crashes.** A pipeline that throws is self-diagnosing —
someone sees red CI and fixes it. The expensive bug is the one that keeps running
and produces a *plausible-but-wrong* number: a neighbourhood billed at the wrong
mill rate, a parcel dropped from a total, a stale rate applied to a new roll year.
Nobody notices until the map is screenshotted and it's wrong in public. This is a
public civic analysis; methodology errors will be scrutinized.

So: **weight code style, performance, and crash-safety near zero. Weight
"could this quietly change a revenue or value number without failing?" near one.**

**The meta-shape of this codebase you must understand before auditing.** This
pipeline is *unusually* defensive: it converts most integrity risks into **loud
hard failures** on purpose (unmapped assessment class → `raise`; missing CRS →
`raise`; missing rate class → `raise`). That is deliberate — "no silent data
drops" is a project rule. **The consequence for you:** the guarded risks are
already loud, so your real target is the **residual set the guards cannot catch**:

- **(a) Semantic correctness a guard can't judge.** A guard checks that every
  assessment class *is mapped*; it cannot check the mapping is *right*. Is
  `DESIGNATED IND PROPERTIES → "Non Residential"` correct? Is each
  `NAME_CORRECTIONS` entry pointing at the *right* neighbourhood?
- **(b) Warn-not-fail paths.** Some mismatches only `logger.warning(...)` and keep
  going. In a **scheduled CI run nobody watches**, a warning scrolls past and the
  map silently loses a neighbourhood. Which mismatches warn instead of fail, and
  would a *change* in that warning be noticed?
- **(c) Config/vintage drift.** A hardcoded year or rate that was right once and
  silently isn't anymore.

Rank your scrutiny toward (a), (b), (c). That is where wrong-but-plausible lives.

---

## 1. The system, end to end

Build a mental model of the whole flow before touching any single file. Trace a
single parcel's assessed value from the API to a pixel.

```
Socrata Open Data API  (scripts/download_data.py — weekly GitHub Action)
  ├─ assessment CSV      q7d6-ambg   (one row per property account)
  ├─ neighbourhood polys 65fr-66s6   (407 boundaries)
  └─ zoning polygons     fixa-tstc   (~11.5k features)
        │
        ▼   src/  (each module independently runnable; main.py wires them)
  load_assessment      normalize + uppercase neighbourhood_name; NAME_CORRECTIONS
  apply_tax_rates      class label → rate class → mill rate → per-property levy
  aggregate_by_…       groupby(neighbourhood).sum(assessed_value, levy)
  load_boundaries      to_crs(EPSG:3400); area_acres from projected geometry
  load_zoning          overlay zoning on boundaries → set-aside / residential frac
  join_and_calculate   LEFT join boundaries←assessment(+zoning); value/revenue_per_acre
  export_geojson       slim cols; reproject 3400→4326; setback+simplify (display-only)
        │
        ▼
  web/data/*.geojson  +  web/data/status.json  (generate_status.py)
        │
        ▼   web/index.html  (MapLibre + deck.gl)
  sqrt colour scale, p97.5 clamp; set-aside → grey; residential-only lens
```

Two numbers reach the public: **value_per_acre** (`total_assessed_value / acres`)
and **revenue_per_acre** (`total_revenue / acres`, where revenue = municipal levy).
Everything below is "can either of those be silently wrong for some neighbourhood?"

Key reference docs to read as you go (don't take their word as proof — verify
against code): `docs/ARCHITECTURE.md`, `data/DATA.md`,
`docs/FINDINGS_assessment_classes.md`, `docs/FINDINGS_revenue_scale.md`.

---

## 2. How to run this audit

1. **Ground yourself first (cheap, ~one pass).** Read the flow above and skim the
   named modules until you can state, in your own words, where a parcel's value
   becomes a per-acre number. If your mental model disagrees with §1, resolve that
   before proceeding — a wrong mental model produces confident wrong findings.
2. **Then work the ranked targets in §3 in order.** For each: read the *actual
   lines*, not your assumptions about them. State a verdict.
3. **Stop-the-line rule.** If you CONFIRM a bug that changes a published number
   (targets T1–T4 especially), flag it **blocking** and say so loudly — don't bury
   it under lower-priority notes.
4. **Do the completeness pass in §4** before you finish.

Do not fix code as you go unless asked — this brief produces a *verdict and a
prioritized findings list*, and the human decides what to change.

---

## 3. Ranked verification targets

Each target is a **claim to confirm or refute**, not a resolved answer. For each,
give: `CONFIRMED-correct` / `BUG` / `UNCERTAIN`, the evidence (quote the line), and
"how would this show up on the map if it were wrong?"

### T1 — Assessment class → rate class mapping is *semantically* correct
`src/apply_tax_rates.py` — `ASSESSMENT_CLASS_TO_RATE_CLASS` (~ln 32).

The non-residential mill rate is ~3.2× residential (see FINDINGS §6.2), so a single
class mapped to the wrong side silently mis-scales that parcel's revenue — and the
guard (`_build_label_rate_lookup` raises on *unmapped* labels) cannot tell you a
*present* mapping is wrong.

**Verify:** (a) every value on the right-hand side exists as a class key in
`data/mill_rates.json` for the audited year; (b) each mapping is defensible against
the parcel's own `Tax Class` field and Edmonton's levy classes — scrutinize the
non-obvious ones: `MA DERELICT RESIDENTIAL → Non Residential`,
`DESIGNATED IND PROPERTIES → Non Residential`, and `EXEMPT_LABEL → None` ($0).
(c) The class-% "sum to <100" path (`~ln 125`) *warns and bills as-stated* rather
than normalizing — confirm that's the intended conservative choice and that the
warning count is something a human could actually see.

### T2 — Roll-year / mill-rate vintage alignment
`main.py` — `ASSESSMENT_YEAR = 2025` (~ln 57); `data/mill_rates.json`;
`scripts/generate_status.py` year constants.

This is the top **unguarded, silent** risk. The assessment coverage year lives in
Socrata *metadata*, not in the CSV rows — so a weekly re-download that rolls to a
new roll year will keep computing, applying the pinned **2025** rates to (say) 2026
assessments. Every revenue number would be wrong; nothing crashes.

**Verify:** is there anything that cross-checks the downloaded roll year against
the pinned `ASSESSMENT_YEAR` and the years present in `mill_rates.json`? If the
only defense is a human remembering to bump the pin, say so and rank it high — this
is the "biggest robustness gap" per the deployment notes, and worth confirming it's
still true rather than assuming.

### T3 — Neighbourhood name matching (warn-not-fail drop)
`src/join_and_calculate.py` (LEFT join ~ln 48, unmatched warnings ~ln 40–56);
`src/load_assessment.py` `NAME_CORRECTIONS` (~ln 16) + uppercase/strip normalize.

The join **warns** on unmatched neighbourhoods and keeps going — it does not fail.
Three cases are known-unresolved (OLIVER, HERITAGE VALLEY TOWN CENTRE AREA,
LEWIS FARMS INDUSTRIAL). The silent risk: in an unwatched CI run, a *new* naming
drift (a renamed/amalgamated/annexed neighbourhood) silently drops from the map and
the only trace is a warning line nobody reads.

**Verify:** (a) does the normalize step (uppercase + strip + `NAME_CORRECTIONS`)
still cover the current data, or has drift crept in? (b) is each `NAME_CORRECTIONS`
entry mapping to the *correct* target neighbourhood, not just to *a* match that
silences the warning? (c) is there any mechanism that would make a *change* in the
unmatched set visible (a committed expected-count, a CI assertion), or is it
warning-only? Recommend one if not.

### T4 — Aggregation: no double-count, correct denominator
`src/aggregate_by_neighbourhood.py` (groupby-sum); `src/join_and_calculate.py`
(`value_per_acre = total_assessed_value / area_acres`, zero-area → NaN ~ln 58–67).

**Verify:** (a) is the assessment file truly one row per account/parcel, so
`groupby.sum` can't double-count? Multi-unit condos are *separately assessed*
accounts (summing is correct); confirm there's no row-duplication or
multi-row-per-parcel that would inflate a total (check DATA.md + a spot count).
(b) area_acres comes from **projected** geometry (T5), summed value over true area —
confirm units line up (acres, not km²/degrees²). (c) zero/NaN-area neighbourhoods
become NaN then get dropped at export *with a logged count* — confirm the drop is
logged, not silent, and doesn't skew the colour-scale fit.

### T5 — CRS is projected (EPSG:3400) before every area calculation
`src/load_boundaries.py`, `src/load_zoning.py`, `src/join_and_calculate.py`
(`SETBACK_CRS = "EPSG:3400"`), export reproject to 4326.

Area computed in EPSG:4326 is in **degrees²** — wrong by orders of magnitude, no
error raised. This project standardizes on **EPSG:3400** (Alberta 10-TM). This is
largely guarded (export raises if `crs is None`), so this is a *confirm-correct*
pass more than a hunt.

**Verify:** every `.area` / `.buffer` / `.simplify` runs on 3400 geometry, never on
raw 4326; the 3400→4326 reproject happens *only* at export (display), after all
area math; no stray EPSG:26911 (UTM 11N) anywhere — the pipeline is 3400 end to end.

### T6 — Zoning set-aside / residential bucketing
`src/load_zoning.py` — `ZONE_CATEGORY` dict, `SET_ASIDE_THRESHOLD` (0.90),
`RESIDENTIAL_THRESHOLD` (0.50), `DEFAULT_CATEGORY = "nonres"`.

Mis-bucketing changes which neighbourhoods render grey (excluded from the scale) or
count as residential in the lens — a *display*-integrity risk more than a
dollar-value one, but still "wrong on the map."

**Verify:** unknown/new zoning codes default to `nonres` and **warn** (conservative:
stays on scale, never falsely claimed residential) — confirm no unknown code is
silently dropped. The set-aside denominator is *zoned* area within the hood (not
boundary area) — confirm fractions sum to 1 and a hood can't be both set-aside and
residential (0.90 + 0.50 > 1 by construction).

### T7 — Frontend can't misrepresent the underlying number
`web/index.html` — sqrt colour transform, p97.5 clamp, set-aside grey, residential
rescale; `web/data/status.json` provenance.

Colour = sqrt and height = linear are deliberate "honesty" choices; the clamp caps
the colour ramp at p97.5. This is presentation, not data — lowest rank — but confirm
the transform doesn't *invert or reorder* magnitude (a bigger number must never
render smaller/dimmer), and that clamped outliers are handled honestly (capped
colour, not hidden).

---

## 4. Completeness pass

Before finishing, spend one explicit pass asking **"what would this ranking miss?"**
Candidate blind spots to actively check, not assume:

- A silent-drop path in a module **not** listed above (e.g. `load_assessment`
  filtering rows, `plot_choropleth`, `download_data.py` partial-fetch handling).
- A guard that *looks* like it fails loudly but actually swallows (a bare `except`,
  a `.fillna(0)` that turns missing data into a real-looking zero).
- Any place a **warning** substitutes for a **failure** on something that changes a
  published number — same class of risk as T3, possibly elsewhere.
- Divergence between what a reference doc *claims* and what the code *does*
  (`DATA.md` row counts / column names, ARCHITECTURE data-flow claims).

Report anything found here as its own finding with a proposed rank relative to
T1–T7.

---

## 5. Output format

Lead with the ranked findings, most-dangerous first. Per finding:

```
### [Txx or NEW] <one-line claim>
Verdict:  BUG (blocking) | BUG | UNCERTAIN | CONFIRMED-correct
Evidence: <file:line + the actual quoted line(s)>
Impact:   <how a wrong value/label would show up on the map, and for whom>
Action:   <the specific check to add or line to change — or, if correct, what you
           confirmed and why it holds>
```

End with a one-paragraph bottom line: can the published numbers be trusted right
now, yes/no, and what's the single highest-leverage thing to harden.

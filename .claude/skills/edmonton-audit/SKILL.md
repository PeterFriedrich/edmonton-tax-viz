---
name: edmonton-audit
description: >
  Focused audit skill for the Edmonton revenue-per-acre fiscal analysis project.
  Use this whenever the user asks to audit, review, check, or QA their Python
  pipeline or project files. Picks ONE audit target per run — designed for
  Opus-class token budgets where doing everything at once is expensive and
  unfocused. Triggers on: "audit my code", "check the pipeline", "review my
  project", "what should I look at", "is this right", or any QA/review request
  in the context of this project.
---

# Edmonton Revenue-Per-Acre Audit Skill

## Purpose

This project is a public civic analysis — methodology errors will be scrutinized.
The goal of each audit run is a **single, deep, actionable verdict** on one aspect
of the pipeline. Do not attempt a broad sweep; pick one focus, go deep, produce
a clear pass/fail + specific fix if needed.

> **Related, but different job:** `docs/DATA_INTEGRITY.md` is a standalone,
> read-cold audit *brief* that maps the whole system and ranks the joints most
> likely to be silently wrong — use it to decide *where* the risk is (or hand it
> to another model for a broad verification sweep). This skill is the *deep dive*
> on ONE target once you've picked it. If you're asked "where should I look?",
> that doc's ranking (T1–T7) is a better starting point than a cold sweep here.

---

## Audit Targets (pick ONE per run)

Choose based on what the user asks, or — if they're just asking "what should I
check" — pick in this priority order:

1. **CRS correctness** — highest risk; silent wrong answers if broken
2. **Silent data drops** — second highest; undermines auditability
3. **Module independence** — architecture risk; harder to fix later
4. **Methodology** — is value/acre being calculated correctly
5. **DATA.md currency** — is the documentation lying about the data

---

## How to Run an Audit

### Step 1 — Identify the target

If the user hasn't specified, ask them to share the relevant file(s), then pick
the highest-priority target from the list above. Tell the user which one you're
auditing and why.

### Step 2 — Read the code carefully

Don't skim. You're looking for subtle bugs, not obvious ones. Read the actual
lines, not your assumptions about what they probably say.

### Step 3 — Deliver a verdict

Structure your output as:

```
## Audit: [Target Name]

**Verdict:** PASS / FAIL / WARN

**Finding:**
[One paragraph. What you found. Be specific — quote the actual line if there's
a bug. Don't hedge.]

**Fix (if needed):**
[Concrete code change or specific action required. If PASS, state what you
confirmed and why it's correct.]
```

---

## What to Look for by Target

### 1. CRS Correctness

The single most dangerous silent failure in this pipeline.

- Is `.to_crs()` called explicitly before any `.area` calculation?
- Is the target CRS a projected (metric) CRS — not WGS84 (EPSG:4326)?
  - EPSG:4326 areas are in degrees², not m² or km². This produces wrong numbers
    without an error.
  - This project standardizes on **EPSG:3400** (NAD83 / Alberta 10-TM Forest) —
    Alberta's province-wide single-zone standard. Use it everywhere.
  - Flag **EPSG:26911** (UTM Zone 11N) as an inconsistency if you find it.
    Although it's also a valid metric CRS, Edmonton (~113.5°W) sits at the
    eastern edge of Zone 11, so it carries more distortion here and breaks
    consistency with the rest of the pipeline. The pipeline should be 3400
    end to end.
- Is the CRS set once at load, or re-projected every time it's needed?
- Is there any place where area is calculated on the raw/joined GeoDataFrame
  before the explicit projection step?

**Common bug pattern to look for:**
```python
# WRONG — area in degrees²
gdf['area_km2'] = gdf.geometry.area / 1e6

# RIGHT — explicit projection first
gdf = gdf.to_crs(epsg=3400)
gdf['area_km2'] = gdf.geometry.area / 1e6
```

### 2. Silent Data Drops

The project spec requires unmatched records to be flagged, not silently dropped.

- Are neighbourhood names normalized before the join (case, whitespace, special chars)?
- After the join, is there an explicit check for unmatched rows?
- Are unmatched rows logged/printed with counts and examples — not just dropped?
- Is the total record count before and after the join printed or logged so drift
  is visible?

**What good looks like:**
```python
merged = assessment.merge(boundaries, on='neighbourhood', how='left')
unmatched = merged[merged.geometry.isna()]
if len(unmatched) > 0:
    print(f"WARNING: {len(unmatched)} records unmatched ({unmatched['neighbourhood'].nunique()} neighbourhoods)")
    print(unmatched['neighbourhood'].value_counts().head(10))
```

### 3. Module Independence

Each `src/` module should be runnable standalone (`python src/module.py`) without
requiring other modules to have been run first.

- Does each module define its own input/output paths (or accept them as args)?
- Does any module import state from another module at the top level?
- Does any module depend on a file that a previous module would have produced,
  without checking if that file exists first?
- Can you trace the data flow: raw CSV → joined GeoDataFrame → calculated field
  → output — with each step being a separate, independently invokable file?

### 4. Methodology

Is the core calculation correct for the stated purpose?

- **Value per acre**: `total_assessed_value / area_in_acres` — check units match
  (area in km² needs conversion; 1 km² = 247.105 acres)
- **Aggregation**: assessed values should be *summed* within a neighbourhood
  before dividing by area — not averaged
- **Property class exclusions**: are farmland or exempt properties being excluded?
  If so, is this documented and intentional?
- **Lot Size field**: if using the parcel-level `Lot Size` field instead of
  polygon area, is it clear which is being used and are the units consistent?
- **Neighbourhood area source**: is it from the polygon geometry (post-projection)
  or from the `Area SQKM` field in the Neighbourhoods dataset? Document which.

### 5. DATA.md Currency

Is the documentation telling the truth about the data?

- Do the column names listed match what's actually in the CSVs?
- Is the row count current?
- Are the neighbourhood name quirks (case, encoding, special characters) documented?
- Is the join match rate recorded (e.g. "312 of 318 neighbourhoods matched")?
- Are any exclusions (property classes, null values) documented with the reason?

If DATA.md is still a placeholder framework with no actual findings filled in,
flag this — it means either the data hasn't been pulled yet, or it has been pulled
but the doc hasn't been updated (which means knowledge is being lost between
Claude Code sessions).

---

## Escalation

If you find a FAIL on CRS or silent drops, flag it as **blocking** — the output
numbers cannot be trusted until it's fixed. Don't continue auditing other targets
in the same run; fix this first.

For WARN or architecture issues, list them and let the user decide order.

---

## Token discipline (Opus)

One target per run. If the user asks you to "audit everything," push back:
explain that a focused single-target audit on Opus is more useful than a shallow
pass over everything, and ask which target matters most right now or offer to
pick the highest-priority one.

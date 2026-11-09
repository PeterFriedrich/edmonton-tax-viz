# Fable Brief — is the modelled levy a fair "what properties pay the City"?

Read this in full before opening any code or any number. House pattern:
`docs/FABLE_AUDIT_development_lens.md` §0 (read that section first if you have
not). Written 2026-11-09 (S241, Opus 5.5) for a **Fable** run. It's the second
release brief, after `docs/FABLE_AUDIT_roads_release.md`.

**Why.** The first release is the public build as it stands (Peter,
2026-11-09). Its landing view says **"City property tax per acre: what each
neighbourhood's properties pay the City"**. That number is modelled as
assessment × the class mill rate, for every parcel on the roll. Against what
the City filed with the province (Alberta FIR Schedule MR, 2026), our total
reads **+11.0% (+$275M levy)**:
- residential matches to +1.2%;
- non-residential is +20.6%, and **96% of that sits on exempt-candidate
  zoning** (`AJ`/`UF`/`UI`/`PU`/`PS`).

This was investigated on 2026-08-25. Two premises were ACCEPTED (A1/A2 in
`docs/ASSUMPTIONS.md`), and `notebooks/verified/03_assumptions.py` sizes them
every week. Opus 5 and 5.5 did all of that, and Peter set the wording. **Your
job is the independent read:** is the headline sentence honest for a release,
given what is already known?

This session spends Fable usage. The investigation is written down. Don't
redo it; challenge what it concluded and what ships.

## §0 — The rule, and the scope

**Top-down, and an UNSOUND level moots everything beneath it.** For each
level, give:
- a verdict: **SOUND**, **CONDITIONAL** (with the caveat that must hold), or
  **UNSOUND**;
- the single sharpest argument against it;
- the evidence that would flip it.

**In scope:**
- the levy as the numerator of every public Money metric: total,
  residential, non-residential, and the Glass grid;
- the Ratio view's "City tax per road metre";
- the copy and caveats a reader sees about it.

**Out of scope:**
- The denominators: acres, lot acres.
- The roads cost side (that's the roads brief).
- The full-build-only lenses.

**No new exemption data exists.** Edmonton publishes no per-parcel exemption
status, and an open-data request was drafted
(`docs/DRAFT_open_data_request_exemption_status.md`). Judge what can honestly
be said **without** it. Don't propose a method that needs it as a release
remedy.

## §1 — Confirm the hinge first

Confirm with the file that proves it:
- **the served levy is assessment × mill rate on every roll parcel, with
  nothing removed for exemption.** Start in `src/` at the levy computation;
  `docs/SPEC_revenue.md` names it.
- **the FIR 2026 totals the gap is measured against are what
  `data/fir_tax_base.json` holds**, fetched by `scripts/fetch_fir_tax_base.py`.

Then confirm one apparent contradiction, because the levels below depend on
it:
- `docs/FINDINGS_exempt_institutional.md` describes exempt institutional land
  as **untaxed, absent from the taxable roll** (DECISIONS 2026-06-29 superseded
  `is_exempt` on that basis).
- The FIR comparison and A1/A2 say levy on exempt-candidate zoning **is
  counted as paid**.

Both can be true at once: some exempt parcels absent, others on the roll with
an assessment we bill. **Measure which, by parcel count and by dollars**, and
say which of the two documents a reader of the site is closer to.

## §2 — Ground yourself (this order, then stop reading)

1. `TODO.md` item "AN EXTERNAL LEVY ANCHOR EXISTS AFTER ALL — Alberta FIR
   Schedule MR": the whole investigation. Note its year-alignment correction.
2. `docs/FINDINGS_exempt_institutional.md`: verdict, typology, caveats.
3. `docs/ASSUMPTIONS.md` A1, A2.
4. `web/verified/03_assumptions.html`: this week's sizes.
5. `docs/DECISIONS.md` rows 2026-08-08: the "gross modelled, direction
   unknown" wording lock for the $125.4M figure.
6. Also in `docs/DECISIONS.md`: 2026-08-15 (the exemption caveat reaches the
   Money tooltip), 2026-08-16 (translucent banded prisms), 2026-08-19 (Glass
   `inst_frac`), 2026-08-25 (`EXEMPT_CANDIDATE_ZONES` includes `PS`).
7. `docs/PROPOSAL_per_cut_exempt_share.md` (PROPOSED, not built): the
   exempt-share bands read the TOTAL levy on the Residential and
   Non-residential cuts too.
8. `docs/COPY_DECISIONS.md` rows N1–N3 ("City tax", not "revenue").

## §3 — The decision stack (highest first)

### L0 — Can a modelled levy carry the sentence "what properties pay the City"?

The number is a model, not a bill. Citywide it is 11% above what the City
filed, and almost all of the excess sits in identifiable places.
- Is "pay" a claim the release can make, or is it "would pay at full
  taxation"?
- Peter locked "gross modelled, never revenue lost, direction unknown" for
  the $125.4M exempt figure (2026-08-08). Is the **landing headline** held to
  the same standard? Or does it assert, for the whole map, exactly what that
  lock forbids for one number?

### L1 — Is the residual small enough to ignore where it isn't flagged?

Residential is +1.2%, so the residential cut is essentially sound. The
non-residential excess concentrates on exempt-candidate zoning, which the map
already bands, translucent, on Money (15 hoods as of 2026-08-15; count them today).
- Is the banding enough to tell a reader that the number is overstated
  **there**?
- What's left unflagged? Measure it:
  - the 4% of the non-res gap outside the five zones;
  - the ~87% of the $4.00B "other residential" (apartment) gap on ordinary
    residential zoning, consistent with use-based exemptions (seniors',
    non-profit and social housing) that zoning cannot see;
  - the $1.90B residential residual.
- Which published hoods carry those, and by how much? A hood whose number is
  overstated with no band is the release risk.

### L2 — The bands themselves

- Hoods banded on Money (count them), with `inst_frac` cells on Glass.
- `EXEMPT_CANDIDATE_ZONES` includes `PS` (parks and services), which the
  map's `inst` category does not.
- The per-cut defect: bands read the total levy on the Residential and
  Non-residential cuts.

Does each band appear where the overstatement is, and only there? Is the
PROPOSED per-cut fix release-blocking or polish? Measure what the defect gets
wrong on the public cuts today.

### L3 — Communication

Check every public sentence that states or implies "paid" or "pays":
- the Money blurbs (total, residential, non-residential);
- the Ratio "City tax per road metre" blurb;
- the tooltip caveat, the panel headline ("$X in city property tax", N3);
- Data & Methods;
- the verified pages `01_money_lens` and `02_methods`.

For each, say whether it is true as worded under L0–L2's verdicts, and give
the smallest wording change that would make it true. Copy changes go through
`docs/COPY_DECISIONS.md`. Check its status column before proposing (row S9 is
there because a settled row was re-proposed).

### L4 — The external anchor as a standing check

The FIR comparison exists only as a TODO item. The carried proposal is a row
in `03_assumptions.py` that sizes our total against the FIR weekly.
- Is that the right instrument?
- What would it catch: a year drift, as on 2026-08-25? A new exemption
  class?
- What can it never catch? Proposal only; the build is a separate PR.

## §4 — Output

1. **`docs/FINDINGS_levy_as_revenue.md`:**
   - §0: the hinge and the contradiction, both measured;
   - §1: the verdict table L0–L4;
   - one section per level;
   - "What this leaves for Peter": each call before release, sized in hoods
     and dollars.
   - Mark every claim **measured** or **read**, and say which model ran.
2. **A row in `docs/AUDIT_LEDGER.md` "Executed audits"**; strike queue item 22.
3. **Release-blocking items into `TODO.md`** under
   `### Levy-as-revenue audit follow-ons (OPEN <date>, docs/FINDINGS_levy_as_revenue.md)`.
   Mark which block the release.
4. **No code, data or copy changes in this run.** A shipped number found
   **wrong** (not merely caveated) gets a ⚠️ `TODO.md` item at the top of
   that heading.

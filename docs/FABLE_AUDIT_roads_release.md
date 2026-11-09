# Fable Brief — the public ROADS lens, before the first release

Read this in full before opening any code or any number. House pattern:
`docs/FABLE_AUDIT_development_lens.md` §0 (read that section first if you have
not). Written 2026-11-09 (S241, Opus 5.5) for a **Fable** run.

**Why now, and why Fable.** Peter's first release is the current public build,
as it stands. On the roads side a reader sees four things (§1). Their last
cross-model read was **S172 (2026-09-18, Fable 5.1)**, and it covered only the
road-life sections. Everything after that was built **and** audited by Opus
alone:
- S187: the two rate notebooks, and the sliver floors.
- S188: the boundary-road equal split (#535), which moved served
  `road_m_per_acre`.
- S199: the public blurbs.
- S202: roads end to end.

Every one of those audits ran on the same model family as the author. Your
value is the independent read: the argument the authors didn't make against
themselves.

This session spends Fable usage. Don't re-derive what is written down. The
history is long and mostly settled; your job is to challenge whether what
ships is fit to **release**, not to re-run the earlier audits.

## §0 — The rule, and the scope

**Top-down, and an UNSOUND level moots everything beneath it.** For each
level, give:
- a verdict: **SOUND**, **CONDITIONAL** (with the caveat that must hold), or
  **UNSOUND**;
- the single sharpest argument against it;
- the evidence that would flip it.

**In scope:** the four public roads surfaces in §1, their rates, their metres,
their copy, and the levy comparison they are read against.

**Out of scope:**
- The full-build-only layers: stormwater, water, fire, transit, bike. The
  S142 fire UNSOUND is settled, and the composite that carried it is retired.
- Whether the levy itself is a fair "revenue" numerator. That is a separate
  brief: premises A1/A2 in `docs/ASSUMPTIONS.md`, the FIR +11% gap in the
  `TODO.md` item "AN EXTERNAL LEVY ANCHOR EXISTS AFTER ALL". Take the levy as
  given here.

**Never propose a replacement rate.** If a shipped rate is wrong, say so and by
how much. Every replacement this project has taken came from a named City
publication after a scoped question, never from an audit's arithmetic (same
rule as `FABLE_AUDIT_road_figures.md`).

## §1 — Confirm the hinge first

Before judging anything, confirm with the file that proves it: **the public
build shows exactly these roads surfaces, and no other Services layer.**

| Surface | Served column | Where |
|---|---|---|
| Services → Roads (supply) | `road_m_per_acre` | `SERVICES.roads`, `pub: true` |
| Services → Roads cost (operating, $9.32/m/yr) | `cost_roads_ops_per_acre` | `SERVICES.roadscost`, `pub: true` |
| Services → Roads cost — lifecycle ($50/m/yr) | `cost_roads_life_per_acre` | `SERVICES.roadslife`, `pub: true` |
| Ratio view: revenue per road metre | (check) | `#view=ratio`, public |

The `SERVICES` table and the public gate are in `web/index.html`. The gate is
`FULL_BUILD || SERVICES[...].pub`; look both up in `docs/CODEMAP.md`, don't
scan the file. Also confirm what the hood panel shows for each layer
(share of levy? $/acre?). If the table is wrong, stop and say so: the levels
below assume it.

## §2 — Ground yourself (this order, then stop reading)

1. `docs/FINDINGS_services_cost_lens_verdict.md` §1 (S142): the verdict table
   and its CONDITIONAL caveats. **Level 0 below asks whether those caveats were
   ever met.**
2. `docs/FINDINGS_road_figures_consolidation.md` (S149, Fable) and
   `docs/FINDINGS_road_life_crossread.md` (S172, Fable): the last two
   independent reads.
3. `docs/FINDINGS_roads_rate_notebooks.md` (S187), `docs/FINDINGS_sliver_floors.md`
   (S187), `docs/FINDINGS_roads_end_to_end.md` (S202): the Opus-only work since.
4. `data/city_unit_costs.json` → `roadway_ops`, `roadway_om_renewal`,
   `roadway_renewal`, `_two_bases`. Read the caveat fields; they carry the
   history.
5. `docs/DECISIONS.md` rows 2026-09-02 (roads back to public, both bases ship,
   the copy↔JSON guard), and the 2026-07-16 back-filled "magnitude, not
   break-even" row.
6. `docs/ASSUMPTIONS.md` A9 (arterials left out of the metres) and B4 (snow
   rate blended with arterials, direction known: high).
7. Open Peter's calls in `TODO.md`:
   - "the road service life is 50 years and the City page's base-case reading
     is 25";
   - "Roads end-to-end audit follow-ons (S202)": the set-aside boundary split;
   - "road-per-dwelling is a good DIAGNOSTIC and a bad MAP".

Primary sources are named in `city_unit_costs.json` `source` fields:
- the City page "Development Impact on Infrastructure";
- the 2017 roads-maintenance budget;
- the snow-and-ice figure.

**Re-fetch them and read them directly.** S172's rule: don't trust a
transcription, including ours. This box's CA bundle is stale, so fetch with
`certifi` if HTTPS fails.

## §3 — The decision stack (highest first)

### L0 — Should modelled road dollars per acre ship in a public release at all?

S142 called this CONDITIONAL: "on condition the constants are defensible; every
defect found so far has been a constant". Its L4 also named the caption's
missing 4.65× fact.
- Were S142's conditions met, or did the lens return to public (2026-09-02)
  with them open?
- A release is read by people who will quote one number. Is "modelled yearly
  cost of this neighbourhood's roads" a claim the evidence can carry, given
  that **one citywide rate times metres** is all it is? Or does the colour
  scale only restate `road_m_per_acre` with a dollar sign? Both cost layers are
  `rate × road_m_per_acre`, so their maps are the supply map rescaled.
  **Is a map that adds no spatial information beyond the supply layer worth its
  dollar framing?**

### L1 — Two bases, side by side, 5.4× apart (DECISIONS 2026-09-02)

Peter chose to ship both rather than pick one. The code comment says ~5.4× as
shipped and ~3.0× on one unit (the operating rate is per lane-km, applied to
centreline metres; `roads_operating_rate` §7).
- Does a reader get what they need to choose between them, or two numbers with
  no reason to prefer either?
- Is "operating = a floor" (the blurbNote) honest, given the lane-km ×
  centreline mismatch?
- Is the lifecycle basis's "not what the City spends here, nor a funding gap"
  enough to stop it being read as exactly that?

### L2 — The rates, against their primary sources

- **Operating, $9.32/m/yr** = $5,970 maintenance + $3,350 snow, per km per
  year:
  - two publications, two vintages, both citywide blends over ~11,000 km that
    include arterials, both per **lane**-km;
  - S187: the snow "corroboration" checks the total, not the 55% share that
    ships;
  - B4: the snow share runs high.
- **Lifecycle, $50/m/yr** = ($600k O&M + $1.9M renewal) per km over 50 years:
  - figures from **one** neighbourhood's published example;
  - the same City page gives the life as "usually 25, extended to 50 with
    proper maintenance". Peter took 50 on 2026-07-15; at 25 the rate is
    $100/m/yr. That's a denominator choice, still listed as Peter's call.
- For each: is the transcription right, is the unit right, and is the
  generalization (one neighbourhood's example, or a citywide blend, applied to
  every hood) defensible for a release? Size anything you find. Don't replace
  it.

### L3 — The metres

`road_m_per_acre` = collector + local centreline metres per acre:
- arterials are excluded (A9);
- road on a boundary is split equally between the hoods (#535), including into
  set-aside hoods (22.9 km; the S202 Peter's call);
- slivers are floored at `MIN_PIECE_M = 1.0`.

S202 reproduced the served column from raw to 5e-5 on all 406 hoods. **Don't
redo that.** Judge the choices:
- Is excluding arterials right for a per-hood cost? The blurb says every kind
  of development shares them.
- Is the equal split sound on a release map?
- Which published hoods do these choices move the most?

### L4 — The comparison the reader makes: road cost against the levy

The project's lock is **magnitude, not break-even** (DECISIONS 2026-07-16,
back-filled; no 1.0 line, never "pays its way"). S142 L3 found a panel that
presented break-even (100% saturation, amber when over) as an unrecorded
amendment of that lock.
- What does the hood panel show now for the two cost layers, and on the Ratio
  view?
- Does any public surface still invite a "covers its roads / doesn't" reading?
- Is "share of levy" (or whatever ships) a magnitude, or a break-even under
  another name?

### L5 — Communication: every public road sentence against the data

This covers:
- the four blurbs and blurbNotes (`SERVICES.roads/roadscost/roadslife`, the
  Ratio blurb);
- the hood panel's road rows;
- the roads part of Data & Methods;
- the public verified page `web/verified/04_roads_lens.html`
  (`notebooks/verified/04_roads_lens.py`).

`scripts/check_cost_copy.py` ties rates quoted in the copy to the JSON. It
checks **that the number matches, not that the sentence is true**. S199
checked the blurbs, Opus only. Re-check each claim. Two examples: "$5,970 per
lane-km of maintenance (the City's 2017 roads-maintenance budget)", and "one
lane is charged per street".

### L6 — Code: spot-check only

S202 is the reproduction. Run only what a finding above needs.

## §4 — Output

1. **`docs/FINDINGS_roads_release.md`:**
   - §0: the hinge confirmed, with the file;
   - §1: the verdict table, L0–L6, one line each;
   - one section per level;
   - a last section, "What this leaves for Peter", listing each call he must
     make before release and what it is worth (hoods moved, $ moved).
   - Mark every claim **measured** or **read**, and say which model ran.
2. **A row in `docs/AUDIT_LEDGER.md` "Executed audits"**, pointing at the
   findings doc.
3. **Release-blocking items into `TODO.md`** under a new heading
   `### Roads release audit follow-ons (OPEN <date>, docs/FINDINGS_roads_release.md)`.
   Mark which block the release and which don't.
4. **No code, data or copy changes in this run.** Remedies are proposals.
   Peter merges code PRs, and copy changes go through
   `docs/COPY_DECISIONS.md`. One exception: a shipped number found **wrong**
   (not merely contestable) gets a `TODO.md` item marked ⚠️ at the top of
   that heading.

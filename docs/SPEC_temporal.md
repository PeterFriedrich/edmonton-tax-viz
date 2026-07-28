# SPEC — Temporal lens: assessment over time, per neighbourhood

**Status 2026-07-28: SPEC'd, nothing built. Phase 0 is a hard gate.**
Peter, 2026-07-28: *"what I actually want is pop up graphs for the assessment of
each neighborhood… you mouse over and get a line graph of the assessment value
over time, for that hood."*

Companion docs: `data/DATA.md` §0 (the source + its defect), `docs/ANALYSIS_BACKLOG.md`
(the Downtown finding), `docs/ARCHITECTURE.md` (module conventions — **read before
writing any module**), `docs/CONTROLS_MATRIX.md` §2 (where a lens leaks).

---

## 1. What it is

A per-neighbourhood time series of assessed value, 2012–2025, surfaced on the
map: a **sparkline in the hover tooltip** as the glance, and a **click-to-pin
panel** as the readable version.

**Home: `/full/` only** (Peter, 2026-07-28 — *"we'd prototype this in full for
now"*). It already carries the work-in-progress badge, so an unfinished lens
arrives labelled. Gate with `|| !FULL_BUILD` beside the data guard, the
established idiom. **The public build is locked at two views and lenses return
one at a time after launch** (`DECISIONS.md` 2026-07-28) — this one is not a
candidate for that queue until Phase 0 closes.

## 2. Why a hover tooltip is not the whole answer

Mechanically a sparkline is trivial: `tooltipFor` already returns an HTML string,
and 14 points is one inline `<svg><polyline>` — no library, no dependency.

But a hover tooltip **vanishes on mouse-out, cannot be studied, and does not
exist on touch at all**, and the Money tooltip already carries 3–4 rows. So the
sparkline is the teaser and the pinned panel is the home. That split is decided;
the panel's design is not.

## 3. Data source

`qi6a-xuwt` — Property Assessment Data (Historical), 2012–2025, 5.5M rows,
carries `neighbourhood_name` natively. **Full 443-hood × 14-year aggregate is one
server-side `$group` query: ~5,600 rows, ~3 s, under 100 kB reshaped** — roughly
1% of the current 7.7 MB payload. Full schema, quirks and the `$limit` trap in
`data/DATA.md` §0.

---

## 4. Phase 0 — THE DATA GATE (blocking)

**`qi6a-xuwt`'s 2024 and 2025 slices are proven incomplete.** Measured
account-by-account 2026-07-28: **2,448 accounts worth $2.93B, across 188
neighbourhoods**, existed in the 2023 slice *and* exist in the current roll, yet
are absent from the 2025 slice. Whole multi-unit buildings vanish together —
Downtown holds 53%, but Magrath Heights is missing 17% of its accounts and
Glenora 15%. **The series cannot be drawn until this is handled.** Full evidence:
`data/DATA.md` §0.

### 0.1 Map the defect's full extent

**The dataset can audit itself — no external control needed for most of it.** An
account present in year N−1 **and** N+1 but absent in N is definitionally a
defect: buildings do not blink. Run that across all 14 years to get a per-year,
per-hood defect map. Only 2024/2025 are proven bad so far; **nobody has looked at
2012–2023.**

For the newest year the check is stronger still — reconcile against the **current
roll** (`q7d6-ambg`), which is independent and complete.

### 0.2 The 2024 hole has no fix — decide what to do about it

The splice (historical 2012–2023 + current roll for the live year) repairs 2025
because the current roll *is* 2025. **There is no current-roll equivalent for
2024.** So 2024 is defective with no replacement. Options, Peter's call:

- **omit 2024** — an honest gap in the line, with the reason stated on hover
- **show it flagged** — plotted but visually marked as known-incomplete
- **do not ship a 14-point series at all** — show 2012–2023 plus a separately
  labelled "current" point

**Do not interpolate across it.** Smoothing a known hole is the failure this
project's whole guard culture exists to prevent.

### 0.3 Exit criteria

Phase 0 is done when: the defect map exists for all 14 years; the splice is
implemented and tested; 2024 has a decided treatment; and a guard refuses to
publish a year that fails its control.

---

## 5. Phases 1–4 — the build (ordinary work, once the gate passes)

| phase | deliverable | notes |
|---|---|---|
| **1** | `src/` module → hood × year table | `ARCHITECTURE.md` conventions: independently runnable, configurable paths, structured output. **No silent drops** — 443 historical hood names will not align cleanly with today's boundaries; route through the `check_unmatched_names.py` policy. |
| **2** | compact JSON → `web/data/` | array-of-arrays, not verbose objects. Budget: under 100 kB pre-gzip. |
| **3** | render in `/full/` | sparkline in `tooltipFor`; click-to-pin panel. Chrome must be added to `CHROME_IDS` or the label sweep will paint names under it. |
| **4** | guard + `refresh.yml` wiring | the anchor-band idiom of `check_value_anchors.py`: bands not equalities, direction-aware, missing inputs skip. Must sit **before** the status-manifest step, or a failure bumps the heartbeat and goes invisible. |

---

## 6. Locked decisions

| decision | rationale |
|---|---|
| **Normalize as share of the citywide assessment base — NOT CPI-deflated dollars** | The mill rate is a **residual** (levy ÷ total base), so a citywide revaluation is fiscally neutral; a hood's burden moves only when its assessment diverges from the city average. CPI-deflating answers a purchasing-power question, not a tax-share one. Share-of-base is unit-free, needs no deflator and no vintage to maintain. |
| **Reserve constant dollars for raw $/acre levels across years** | The one place a deflator is legitimate. And on the cost side later, city inputs track a **Municipal Price Index**, not CPI — CPI there is the wrong index, not merely imprecise. |
| **Name the denominator in the UI** | Downtown is **3.22% of the total base** but **9.30% of the commercial base** (2025). Public reporting quotes the second kind. Publish 3.22% beside an article saying 5.2% and the project looks wrong when it is not. Showing both is probably right. |
| **Framing is descriptive only** | Share-of-base line + the sourced driver (office vacancy). No "downtown is dying", no "the rest of the city subsidizes downtown". The reader draws the conclusion. |
| **`/full/` only, for now** | See §1. |
| **Do NOT use the `NONRES MUNICIPAL` class** | 1–2 accounts; its share swings 30–53% on noise. |

## 7. Open decisions (Peter's)

1. **Metric — assessed value or revenue?** Value reaches 2012; revenue needs
   historical mill rates (`pwis-wc4c`, "2014 onward") so it starts **2014** and
   inherits every class-differential caveat.
2. **Denominator — share of total base, or of the commercial base?** Or both.
3. **Per-acre or total?** The project is per-acre throughout, but 14 years of
   moving boundaries divided by a *current* area needs a stated justification.
4. **2024 treatment** — see §4.2.

**Suggested first cut: share of citywide base · value not revenue · total not
per-acre.** It is the only combination needing no deflator, no area assumption
and no rate table — so Phase 0 is the only thing in front of it.

## 8. Traps already paid for

- **Validate at the display grain.** Recorded in `FINDINGS_lot_dedupe.md` §4.3
  and re-learned twice since. A per-point maximum that never survives to a
  100 m cell is not a fact about the map.
- **Aggregates can be confidently wrong.** This lens's own finding was misread
  **twice** from aggregates — a class-level split said "80% genuine
  revaluation", a value-of-vanished-accounts sum said "98% vanishing" — and the
  account-level join produced the opposite answer both times. **When a series
  has a cliff, join at the entity level and check a second source for the same
  period before interpreting the shape.**
- **A cause named in a handoff is a hypothesis.** Reproduce the symptom *and*
  re-measure the stated cause before acting on a backlog item.
- **The two datasets disagree on column names** — historical uses
  `neighbourhood_name`, the current roll uses `neighbourhood`. And Socrata's
  default page size is 1,000: always pass `$limit` or results silently truncate.

# DATA_ISSUES — defects in data we do not control, and what we've told the publisher

**What belongs here:** a defect in a source we consume — Edmonton Open Data,
Alberta FIR, GTFS — plus the evidence, what it breaks on our side, and
**whether anyone has been told**. One row per defect, newest first.

**What does NOT belong here:**

| this file | where it goes instead |
|---|---|
| how a source is shaped, its columns, its quirks | `data/DATA.md` |
| our own build work and backlog | `TODO.md` |
| a locked decision + its reasoning | `docs/DECISIONS.md` |
| an audit we ran over our own pipeline | `docs/AUDIT_LEDGER.md` |
| an analytical question to investigate | `docs/ANALYSIS_BACKLOG.md` |

⚠️ **The point of the file is the last column.** Findings that never leave the
repo were the standing failure mode here: the `qi6a-xuwt` dropout was measured
on 2026-07-31, and by 2026-08-06 it had been archived unsent as a sub-item of a
closed parent, invisible for six days. Status must be one of
**NOT SENT · SENT (date) · ACKNOWLEDGED (date) · FIXED (date) · WONTFIX**, and
"the artifact exists" is **not** sent.

---

## Status at a glance

⚠️ **This table is the authoritative send status.** `TODO.md` carries a tracker
item that mirrors it in one line each — if the two disagree, **this one is
right**, and the TODO is stale. Update here first.

**Nothing has been sent. Five issues, zero contact, as of 2026-08-27.** (Issue 2
is ours, not theirs — it was never a candidate to send, and it is now fixed.)

| # | issue | evidence | report text | status |
|---|---|---|---|---|
| 1 | `Period of Coverage` names the wrong year | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/roll-year-metadata.html) | ❌ not written | **NOT SENT** |
| 2 | archive's 2025 entry is the 2026 roll | — (ours, not theirs) | n/a | ✅ **FIXED 2026-08-27** |
| 3 | `qi6a-xuwt` drops 2,448 accounts | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/historical-2024-gap.html) | ❌ not written | **NOT SENT** |
| 4 | no per-parcel exemption status published | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/exemption-uncertainty.html) | ✅ `docs/DRAFT_open_data_request_exemption_status.md` | **NOT SENT** |
| 5 | 3 of 5 school boards absent from open data | ❌ none | ❌ not written | **NOT SENT** |

**Channel:** `opendata@edmonton.ca`, read from the portal footer 2026-08-25 —
primary source, not inference. Right channel for 1, 3, 4 and 5, all of which are
dataset/portal requests. **Assessment & Taxation Branch is the escalation if
Open Data bounces one**, not the first stop.

**Issue 4 is the only one with a written message.** Everything else has evidence
and no text. ⚠️ Sending is Peter's call in every case — it is outward-facing and
it speaks for the project.

⚠️ **Re-measure before quoting any figure below.** Several are derived against
the current roll, which moves weekly and rolled to 2026 in August. Each row says
when it was last measured.

---

## 1. `q7d6-ambg` — `Period of Coverage` names the wrong year, and has all year

**Status: NOT SENT.** Evidence published and linkable; the report text itself is
not written.
**Last measured: 2026-08-26** (every figure recomputed by the published run).

**Evidence:** `/notebooks/roll-year-metadata.html`
(source `notebooks/standalone/roll_year_metadata.py`). Standalone — live APIs
only, imports nothing from `src/`, **8/8 invariants pass**. Two independent
proofs by design: §2 uses **only Edmonton's own datasets** (the Historical
table's 2025 slice against the current roll), §3 uses **Alberta's FIR filings**,
so a reader who distrusts either source still has the other. ⚠️ The first
invariant flips when the City corrects the field, which is how the page reports
its own obsolescence.

**The defect.** The Socrata metadata on *Property Assessment Data (Current
Calendar Year)* reads:

```
Period of Coverage : 2025-01-01 to 2025-12-31
rowsUpdatedAt      : 2026-08-24
```

The rows were refreshed two days before that reading and the content is the
**2026** roll — Alberta FIR Schedule `MR(2)` puts Edmonton's filed residential
base at $148.1B for 2025 and $160.4B for 2026, and our measurement of the served
file is **$162.3B, +1.2% against 2026 and +9.5% against 2025**. The hand-
maintained coverage string has been a year stale for the whole 2026 roll.

**What it broke here — THREE times.** ⚠️ **This is the argument for sending it.**
One un-maintained metadata field has now produced three separate defects
downstream, in three different subsystems, over roughly a month — and each was
found by accident rather than by looking. All three are fixed on our side; the
field is not.

1. **The mill-rate pin sat a year stale.** `check_year_alignment.py` validated
   our `ASSESSMENT_YEAR` against this string; both said 2025, so it reported
   *aligned* and the pipeline billed a 2026 roll at 2025 rates — citywide levy
   understated **$69.5M (2.5%)**. Fixed 2026-08-25 by
   `scripts/check_roll_year_against_fir.py`, which measures parcels against FIR
   instead of reading anyone's metadata (`DECISIONS.md` 2026-08-25), and wired
   into `refresh.yml` 2026-08-26 so `python main.py` is gated on it.
2. **The temporal archive froze the 2026 roll under the label 2025** — issue 2
   below. ✅ Resolved 2026-08-27, but **the cost was permanent**: the phantom
   entry was deleted and the real 2025 turned out to be unrecoverable, so the
   published series lost a year (2012–2023 + 2026).
3. **The monthly digest was about to cry wolf, every month.**
   `vintage_report.check_assessment_roll` compared the coverage string against
   our pin *itself*, bypassing the stale-metadata downgrade
   `check_year_alignment.py` locked in 2026-08-25. With their field reading
   2025 and our pin correctly at 2026, it reported **"Roll has moved to 2025,
   pin is still 2026"** and told Peter to work the year-roll runbook for a roll
   already done — a false ⚠️ due to fire 2026-09-01, in the only channel here
   that reaches a human on a schedule. Fixed 2026-08-27 (PR #258) by routing
   through `check_alignment()`; now reports UNKNOWN and names the FIR guard as
   the authority. ⚠️ **Found while testing something else, not by looking** —
   the same way the other two surfaced.

**Why report it.** It costs Edmonton **one field edit**, and it is the kind of
defect no consumer can detect without an external anchor most consumers don't
have. The dataset is otherwise sound. ⚠️ **Cheapest of all five to fix and the
most expensive left unfixed** — see the three-defect list above. It is also the
only issue whose evidence page is live while it has never had a draft written.

---

## 2. Our own consequence of issue 1 — the temporal archive's 2025 entry is the 2026 roll

**Status: N/A (ours, not theirs). ✅ RESOLVED 2026-08-27.** Listed here because
it is a *direct consequence* of issue 1 and would be unreadable filed anywhere
else. **Last measured: 2026-08-26; fixed 2026-08-27** — see *The fix* at the
bottom of this row.

**What happened.** `src/load_temporal.write_archive` captures the live roll
under whatever `main.ASSESSMENT_YEAR` says, then **freezes** it — by design,
because once the roll advances we no longer hold a complete source for that
year (`SPEC_temporal.md` §0.4, the January trap). On **2026-07-28**
(commit `865159a`) the pin still said 2025 because of issue 1, so the archive
froze the **2026 roll under the label 2025**.

**The evidence**, three independent sources agreeing:

| source | 2025 | 2026 |
|---|---|---|
| historical table `qi6a-xuwt`, total assessed | **$220.07B** | absent |
| Alberta FIR, filed residential base | $148.13B | $160.37B (**+8.3%**) |
| `data/temporal_archive.json`, RESIDENTIAL | **$162.255B** | $162.264B |

Both archive entries best-fit FIR **2026** (+1.17% / +1.18%) and miss 2025 by
+9.5%. They are the same roll captured four weeks apart: 343 of 406 hoods are
byte-identical and the citywide total moves **+0.0021%**, against a historical
year-on-year range of −2.05% to +16.10%.

**What it breaks:**

- **The change lens** annualises over 14 elapsed years instead of 13 (and 7
  instead of 6 on the short window) while the numerator gained nothing —
  **diluting every hood's rate ~7% and ~14%**.
- **The assessment-history panel and sparkline** show a flat 2025→2026 plateau
  that never happened, and the real 2025 — a +8.3% revaluation year — is
  missing from every hood's curve.
- **`data/expected_temporal_years.json`'s 2025 anchor** ($237.2B–$239.6B) was
  pinned from the mislabelled capture, so the guard now enforces the wrong
  value and would reject the true $220.07B.
- **`CHG_WINDOW_LABEL`** is hardcoded `"2012–2025"` / `"2019–2025"`, so the
  legend prints an end year the arithmetic no longer uses.

**Detection, built 2026-08-26.** `scripts/check_temporal_archive_year.py`
checks every archived year's RESIDENTIAL total against FIR and asserts it
best-fits the year it is filed under. It exited 3 on the defective archive and
**exits 0 as of 2026-08-27**, so it is now safe to wire into a workflow.

### The fix — 2026-08-27

**The mislabelled entry was DELETED, not relabelled.** A correctly-labelled
`2026` entry already existed (the same roll, captured four weeks later and so
very slightly more complete), so relabelling would have collided with it;
342 of 406 hoods were byte-identical between the two and the citywide total
differs by **+0.0021%**. Deleting the phantom leaves the later capture, which is
the better copy of the only year either of them actually measures.

⚠️ **This does NOT restore a real 2025 — and that was the surprise.** 2025 is in
`HISTORICAL_DEFECT_YEARS`, so with no archive entry `publishable_years()` does
not fall back to the historical file; it **omits the year**. The published
series is now **2012–2023 + 2026**, with a **two-year hole**. That outcome
follows from already-locked policy rather than a new decision: the historical
2025 slice carries the *same* cumulative defect as 2024 (2,448 accounts /
$2.93B, 53% of it Downtown — issue 3), and `SPEC_temporal.md` §0.2 already
rejected publishing a slice with that hole when it omitted 2024.

**So the true cost of issue 1 is now clear: the real 2025 is gone for good.**
The archive existed precisely to capture 2025 before the roll advanced past it
(`SPEC_temporal.md` §0.4). It ran on time and captured the wrong year, because
the stale coverage string made the guard green. **A safety mechanism whose input
is unverified does not merely fail — it consumes its one chance to succeed.**

**What moved with it:**

- `data/temporal_archive.json` — the `2025` key removed; `2026` untouched.
- `web/data/temporal.json` — regenerated: 13 years, 406 hoods, 89.3 kB.
- `data/expected_temporal_years.json` — the 2025 anchor **removed**, with a note
  in `_note` forbidding a re-pin from the archive. It was dormant (the guard
  skips unpublished years) but pinned from the phantom, so it would have
  enforced $237.2B–$239.6B against a true $220.07B for anyone republishing 2025.
- `CHG_WINDOW_LABEL` → `"2012–2026"` / `"2019–2026"`, plus four other hardcoded
  `2012–2025` strings. ⚠️ Still hardcoded **on purpose** — a label that read the
  last year from the data would have silently renamed the phantom instead of
  exposing it.
- The tooltip's **hardcoded `"(2024 n/a)"`** is now derived from the year list.
  It would have understated a two-year hole with every check green — the panel
  note beside it was already derived for exactly this reason, and the teaser was
  the copy that got missed.
- `verify-temporal.js` (6 checks) and `verify-change.js` (3) rescaled from a
  one-year gap to a two-year one; year references derived where they were
  literals, so the next roll-forward does not redden them.

**⚠️ The `x is year-scaled` ratio-3.01 failure was NOT a rendering defect** —
the S121 handoff flagged it as possibly real and unexplained. With the phantom
2025 present, the detached run held **two** points and was stroked as a path, so
the measurement's `g circle`[0] fell through to the live-year marker at 2026 and
silently changed which element it was reading. The renderer was correct
throughout; the *measurement* had lost its subject.

---

## 3. `qi6a-xuwt` — 2,448 accounts vanish from the 2024/2025 historical slices

**Status: NOT SENT.** Artifact published and linkable; the report text itself is
not written.
**Last measured: 2026-08-26** (re-measured live; account counts reproduced
exactly, dollar figures moved because the control is the current roll).

**The defect.** The Historical Assessment roll drops accounts that exist both in
earlier slices and in the current roll: **5** by detector A, **2,321** by
detector B, **2,322** union, plus **131** more incremental in 2025 —
**2,448 cumulative** across **188 neighbourhoods**, Downtown worst at **1,292**.
The dataset's self-audit and the current-roll control **disagree by 464×**, which
is the single most useful sentence for the City. 11 of 13 testable years are
clean, so this is not a systemic export fault.

The loss is **building-shaped**: 2,448 accounts at **272 addresses**, with
**29 addresses losing every account they had** (969 total); the largest are
**309** and **261** units at 10310 / 10360 102 ST NW. ⚠️ Incidental find: one
Downtown address is published under **three spellings** (`102 STREET` /
`SSTREET` / `STSREET`), so that building actually loses **315**, not 309.

**Evidence:** `/notebooks/historical-2024-gap.html`
(source `notebooks/standalone/historical_2024_gap.py`). Standalone — live API
only, imports nothing from `src/`, every figure computed at run time, 6/6
invariants asserted. Includes a dozen real account numbers and the portal query,
so the report needs no re-run to be checkable.
⚠️ **Do not send `notebooks/exploration/03_historical_roll_gap.ipynb`** — the
superseded version.

**What it breaks here:** 2024 is omitted from the temporal lens by decision
(`SPEC_temporal.md` §0.2 — do not interpolate), and the published year list is
deliberately non-contiguous as a result.

---

## 4. No per-parcel exemption status is published anywhere

**Status: NOT SENT.** Request drafted at
`docs/DRAFT_open_data_request_exemption_status.md`; submission channel
confirmed as `opendata@edmonton.ca` (read from the live portal footer,
2026-08-25).
**Last measured: 2026-08-26.**

**The gap.** The roll flags **3 properties / $7.6M** as exempt — about **0.05%**
of what must actually be exempt. FIR shows the filed taxable base sitting
**~$15B below** the roll, and `MR(2)` is *proven* to be the taxable base
internally (assessment × rate reproduces the levy to −0.0000%). Five zone codes
account for **96%** of the non-residential gap.

**Why we cannot close it ourselves** — and this is what makes it a request
rather than an analysis:

- the candidate set is **shorter than the gap**, so errors run both ways;
- apartments are exempted **by use** under MGA s.362, invisible to zoning
  (**87%** of that gap sits on ordinary residential zoning);
- **a sum does not determine its terms** — demonstrated by constructing **two
  disjoint sets** (60 and 68 properties, zero overlap) that each hit the same
  $3.49B target to 100.0000%.

**Evidence:** `/notebooks/exemption-uncertainty.html`
(source `notebooks/standalone/exemption_uncertainty.py`, 11/11 invariants pass,
committed outputs from a cold-cache run that fetched all three sources live).

⚠️ **Do not put the $125.4M figure in the message** — see the TODO item.

---

## 5. Private, charter and francophone schools are absent from open data

**Status: NOT SENT.** No draft. Lowest priority of the five.
**Last measured: 2026-08-23.**

Two of five school boards publish catchment locations (`996c-239n`, 225 rows;
`gfxq-u8uu`, 97 rows). The rest are not in the open data at all, and the gap
**cannot be closed from data we hold** — probed three ways 2026-08-23
(`ANALYSIS_BACKLOG.md` §13). The amenity band's school set is therefore
incomplete by construction, which the control's tooltip states outright.

`amenity_distance` takes any point frame, so a published point set would drop
straight in. ⚠️ A hand-built list would be the `T8` hand-enumeration shape — a
value over a name-matched set with no self-check — and is not the answer.

---

## Possible issues — not yet confirmed, scoped, or clearly the publisher's fault

⚠️ **Nothing here is reportable as it stands.** These are candidates found by a
sweep of `data/DATA.md`, `docs/DECISIONS.md` and `docs/ANALYSIS_BACKLOG.md` on
2026-08-26 — real enough to record, not measured enough to send. Promote one to
a numbered issue above only after it has an artifact that reproduces it.

⚠️ **What was deliberately EXCLUDED from this list**, because it looks like a
defect and is not: **identifier churn.** Account numbers get renumbered
(0.15%–0.37%/yr, spiking to 0.91% in 2023→2024), addresses get re-addressed
(`WESTMOUNT SHOPPING CENTRE NW` no longer exists), neighbourhoods get renamed
(OLIVER → WÎHKWÊNTÔWIN moved 12,237 parcels). That is routine municipal
practice, `data/DATA.md` says so outright, and **a vanished account number is
not by itself a finding**. What would be a defect is a property absent from the
published roll *while still being assessed* — which is A below, and the reason
it is separated from the churn it hides inside.

### A. Properties go transiently absent from the published current roll

**⚠️ The single case is CONFIRMED; the population is not.** Now an active
`TODO.md` item — the one candidate here worth working.

Misericordia Community Hospital was continuously assessed 2012–2025 as account
`10095840` (~$200–260M, always WEST MEADOWLARK PARK), was renumbered to
`11495573`, and was **absent from `q7d6-ambg` entirely until 2026-08-03** —
during which the map understated that neighbourhood by **~$250M**. All four
major hospitals moved into a new `114955xx` block at the 2025 roll, and the old
numbers appear in **no year** of `qi6a-xuwt`.

`tools/audit_roll_continuity.py` (run 2026-08-07 against historical 2024) finds
**1,534 of 426,913 parcels — 0.36%, $1.62B assessed** — with no current match,
by position rather than by any of the three churning identifiers (across the
hospital renumbering the coordinates moved **under 2 m**).

⚠️ **Those 1,534 are candidates, not verdicts** — demolitions, subdivisions and
consolidations look identical to a dropout from the outside. That is exactly
what makes this unreportable today: we cannot yet say how many are real.

Same dataset as issue 1, so if it firms up it could ride along in that report
rather than needing its own.

### B. `building_type` is an uncontrolled vocabulary (building permits)

71 distinct values carrying multiple spellings of the same category —
`Apartments (310)` / `Apartment (310)` / `Apartment Condos (315)`;
`Row House (330)` / `Row Houses (330)`; `Semi Detached House` with no code at
all. We handle it by enumerating full strings (`RESIDENTIAL_BUILDING_TYPES`,
`INDUSTRIAL_BUILDING_TYPES`), never by prefix-matching.

Low severity and it costs us nothing today, but it is a genuine publisher-side
quality issue and the cheapest of these to write up. ⚠️ Any report would have
to enumerate what the variants ARE rather than name the categories — the
category-by-name shape is how parkades ended up classified as industrial
elsewhere in this project.

### C. No capital budget on the open data portal, and no freshness signal where it does live

The portal has **no capital sibling** to `da9s-v9j8`: a domain search returns
only the two OPERATING feeds (`da9s-v9j8` expenses, `m84q-ghmu` revenues),
`552h-hjwj` Capital Projects (a 214-row app feed), and a 2015 relic. Probed
2026-08-21 — do not go hunting for one again.

The real capital budget is on the **Open Budget portal**, which publishes **no
freshness header at all**: `Last-Modified` merely echoes `Date` behind
`Cache-Control: no-cache`. So unlike Socrata's `rowsUpdatedAt` there is nothing
to watch, and the committed file *is* the pin — `scripts/vintage_report.py`
fingerprints sorted content instead.

Two requests in one, which is why it is not yet drafted: publish capital
alongside operating, and expose a real last-modified. ⚠️ Also note the file has
quirks that are **not** defects: 1,884 rows over 399 `profile_id`s (not one row
per project) and 87 rows with negative `approved` (funding-source swaps).

### D. No published service life for bikeways or shared pathways

⚠️ **This is about BIKEWAYS, not roads** — roads have a published figure, and
the 25-vs-50-year question there is a judgment call on the City's own wording,
not a gap.

Searched 2026-08-04 across six sources: the Development Impact page (roads and
fire stations only), both Bike Plan PDFs, the 2025 Infrastructure Report, the
Infrastructure State-and-Condition / Inventory / Tools pages, and the 2023
Capital Asset Management Audit. None state one.

An availability gap rather than an error, same shape as issues 4 and 5. It is
the last input the bikeway cost side needs.

---

## Cross-refs

- `data/DATA.md` — what each source *is* (§0 historical roll, §11 FIR, §20
  schools + amenity distance, §21 the roll-year anchor)
- `docs/SPEC_temporal.md` §0 — the historical file's defect map and the omit
  decisions that follow from issue 3
- `docs/DECISIONS.md` 2026-08-25 — why a guard that reads a publisher's
  free-text metadata field is not measuring the data
- `docs/RUNBOOK.md` §1 — what to do when a roll-year guard holds the publish

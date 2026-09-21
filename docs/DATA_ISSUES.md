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

⚠️ **What each evidence notebook stands on — which datasets, both directions —
is inventoried in `docs/EVIDENCE_NOTEBOOKS.md`.** This file owns SEND STATUS;
that one owns what the evidence rests on.

## Status at a glance

⚠️ **This table is the authoritative send status.** `TODO.md` carries a tracker
item that mirrors it in one line each — if the two disagree, **this one is
right**, and the TODO is stale. Update here first.

**Nothing has been sent. Seven issues, zero contact, as of 2026-09-21.**
⚠️ **And every defect below was CHECKED still-present on 2026-09-21**, not
assumed: all five published evidence notebooks were re-executed against live
sources and their 51 invariants all held. They are re-run **monthly** from now
on (`.github/workflows/evidence-recheck.yml`, 15th of the month; RUNBOOK §0e),
so a silent upstream fix will surface here instead of waiting for someone to
think of re-running a notebook by hand. ⚠️ **Status in this table is still
changed by a HUMAN** — the recheck reports, it does not edit rows.
⚠️ **Issues 1 and 3–6 — all five of the previously sendable set — have BOTH
published evidence and drafted report text** (issue 6's landed 2026-09-17), so
**nothing among those five is blocked on work; the only thing left is the
decision to send.** ⚠️ **Issue 7 (new 2026-09-20) has NEITHER** — no notebook,
no draft — so "every sendable issue is ready" stopped being true on 2026-09-20
and this line is the only place that says so. (Issue 2 is ours, not theirs — it
was never a candidate to send, and it is now fixed.)

| # | issue | evidence | report text | status |
|---|---|---|---|---|
| 1 | `Period of Coverage` names the wrong year | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/roll-year-metadata.html) | ✅ `docs/DRAFT_bug_report_coverage_year.md` | **NOT SENT** |
| 2 | archive's 2025 entry is the 2026 roll | — (ours, not theirs) | n/a | ✅ **FIXED 2026-08-27** |
| 3 | `qi6a-xuwt` drops 2,448 accounts | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/historical-2024-gap.html) | ✅ `docs/DRAFT_bug_report_historical_dropout.md` | **NOT SENT** |
| 4 | no per-parcel exemption status published | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/exemption-uncertainty.html) | ✅ `docs/DRAFT_open_data_request_exemption_status.md` | **NOT SENT** |
| 5 | 3 of 5 school boards absent from open data | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/school-coverage-gap.html) | ✅ `docs/DRAFT_open_data_request_school_locations.md` | **NOT SENT** |
| 6 | `24uj-dj8v` `neighbourhood` holds a LIST of hoods | [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/permit-neighbourhood-list.html) | ✅ `docs/DRAFT_bug_report_permit_neighbourhood_list.md` | **NOT SENT** |
| 7 | `stt5-pzaa` frozen 2 annual cycles while its report kept publishing | ❌ none | ❌ none | **NOT SENT** |

**Channel:** `opendata@edmonton.ca`, read from the portal footer 2026-08-25 —
primary source, not inference. Right channel for 1, 3, 4 and 5, all of which are
dataset/portal requests. **Assessment & Taxation Branch is the escalation if
Open Data bounces one**, not the first stop.

**Issues 1 and 3–6 all have a written message.** ⚠️ **This line read "issue 6
does not" until 2026-09-20, and was wrong the day it was written** — the draft
landed at 14:52 on 2026-09-17, eight minutes after the prose claiming its
absence, and §6 below carried the same stale "No draft" for three days while
the table two rows up said ✅. **The table is authoritative; prose about the
table goes stale by the hour.** ⚠️ **Report text is no longer the blocker on any
of the five — the only thing between them and a send is Peter's decision.** All three new drafts re-verified their premises against the live portal on the day they were written (coverage string still wrong and it survived the 2026-09-14 refresh; `qi6a-xuwt` untouched since 2026-01-12 so the dropout stands; the school absence re-searched and still absent). ⚠️ **Issue 6's evidence gap CLOSED 2026-09-17** — it was the
one issue lacking a published notebook, which made "every remaining blocker is
report text" false between 2026-09-14 and 2026-09-17. It now has both. ⚠️ Sending is Peter's call in every case — it is outward-facing and
it speaks for the project.

⚠️ **Re-measure before quoting any figure below.** Several are derived against
the current roll, which moves weekly and rolled to 2026 in August. Each row says
when it was last measured.

---

## 1. `q7d6-ambg` — `Period of Coverage` names the wrong year, and has all year

**Status: NOT SENT.** Evidence published and linkable. **Report text written
2026-09-17: `docs/DRAFT_bug_report_coverage_year.md`** — premises re-verified live
that day, including the new fact that the field **survived the 2026-09-14
refresh**, so it is not maintained by the refresh.
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

**Status: NOT SENT.** Artifact published and linkable. **Report text written
2026-09-17: `docs/DRAFT_bug_report_historical_dropout.md`.** ⚠️ `rowsUpdatedAt`
confirmed still **2026-01-12** that day — the table has not moved since January,
so the defect stands and the account counts remain quotable.
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

**Status: NOT SENT.** **Draft written 2026-09-17:
`docs/DRAFT_open_data_request_school_locations.md`** — the absence re-searched
live that day and it still holds. Lowest priority of the five; send last.
**Last measured: 2026-08-29** (evidence notebook, live re-fetch).

**Evidence:** [published](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/school-coverage-gap.html)
— `notebooks/standalone/school_coverage_gap.py`, 4 of 4 invariants passed.
⚠️ **This one argues an ABSENCE, so it is built the opposite way round from the
other three:** it runs the catalogue searches that would DISPROVE the claim
(`private school`, `charter school`, `independent school`, `francophone`,
`Centre-Nord`) and shows they return no school point set for any missing
operator. Its invariants are written to **FAIL if the City publishes the
missing schools** — the outcome the report asks for. It establishes only that
the portal exposed no such dataset on the run date, not that the City holds
none internally.

Two of five school boards publish catchment locations (`996c-239n`, 225 rows;
`gfxq-u8uu`, 97 rows). The rest are not in the open data at all, and the gap
**cannot be closed from data we hold** — probed three ways 2026-08-23
(`ANALYSIS_BACKLOG.md` §13). The amenity band's school set is therefore
incomplete by construction, which the control's tooltip states outright.

`amenity_distance` takes any point frame, so a published point set would drop
straight in. ⚠️ A hand-built list would be the `T8` hand-enumeration shape — a
value over a name-matched set with no self-check — and is not the answer.

---

## 6. `24uj-dj8v` — the `neighbourhood` field sometimes holds a LIST of hoods

**Status: NOT SENT.** **Draft: `docs/DRAFT_bug_report_permit_neighbourhood_list.md`**
(written 2026-09-17; this line said "No draft" until 2026-09-20, three days after
the file existed). **Last measured: 2026-09-14** (S156, local re-derivation from
`data/raw/building_permits.csv`).

**Evidence:** ✅ **PUBLISHED 2026-09-17** —
[permit-neighbourhood-list.html](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/permit-neighbourhood-list.html)
(`notebooks/standalone/permit_neighbourhood_list.py`, **5 of 5 invariants**,
executed cold-cache against live APIs). Measured live that day: **547 of 246,402
rows, 0.22%** — reproducing the local figure in shape.

The permits dataset writes `neighbourhood` as a **comma-joined list** on some
rows — `OLIVER, WÎHKWÊNTÔWIN`, `THE HAMPTONS, GRANVILLE`,
`HOLLICK-KENYON, BRINTNELL, MILLER, BRINTNELL` — where every other hood-bearing
source we consume carries either a numeric id (`fire_response`, both Property
CSVs) or a single clean name (the historical aggregate). **546 raw rows, 92
distinct names, 0.22%** — and **92 of the 95 permit names that miss the boundary
file are this one pattern**, so it is essentially the entire name-join defect for
this dataset.

Three distinguishable causes are mixed into one field, which is what makes it a
publisher problem rather than a join problem on our side:
- **A rename carrying both names** — `OLIVER, WÎHKWÊNTÔWIN` (the 2024 rename,
  `data/DATA.md`). One hood, two labels.
- **The same hood written twice** — `RITCHIE, RITCHIE`,
  `SOUTH TERWILLEGAR, SOUTH TERWILLEGAR`. Pure duplication.
- **A permit genuinely spanning 2+ hoods** — `RUTHERFORD, HERITAGE VALLEY TOWN
  CENTRE`. Real information, in a field with no room for it.

**What it broke here:** the published since-2009 window silently dropped
**1,810 dwelling units (1.11% citywide)**, understating WÎHKWÊNTÔWIN by **68%**
(1,229 shown against 2,066) and SOUTH TERWILLEGAR by 45%. ⚠️ **It hid because
every affected row predates 2021** — the 5yr and 3yr windows lose 1 unit and 0,
so the module's "immaterial" note was true of the windows anyone had measured
and false of the one shipped 2026-07-21. 1,245 units across 8 unambiguous names
were corrected 2026-09-14; **565 across 15 names remain unattributed by
decision** (see `TODO.md` — a name correction cannot split a straddling permit,
and those rows are only 14.9% geocoded so geometry cannot either).

**What to ask for.** ⚠️ **THE ASK RECORDED HERE UNTIL 2026-09-17 WAS WRONG, and
would have been checkably wrong to the person receiving it.** It said to ask for
*"the numeric `neighbourhood_id` the City already publishes"* — but this dataset
**already carries one**, `neighbourhood_numberr`, and it is **comma-joined on
every one of the same 547 rows** (asserted as a notebook invariant). Asking a
publisher to publish a field they already publish costs a report its
credibility. **The corrected ask:** make the EXISTING id single-valued, and give
the genuine multi-hood permit somewhere to go (a repeated row per hood, or an
`additional_neighbourhoods` field). ⚠️ **The id is nonetheless strictly MORE
informative than the name**, which is this report's actual contribution:
checking each id for membership in `65fr-66s6` separates the three causes
mechanically, where names could only guess — **240 genuine straddles / 238
renames / 69 duplications, with 0 rows unclassified**. Retired ids (`1150`
OLIVER, `2310` GORMAN INDUSTRIAL WEST) are simply absent from the boundary file.
Minor, and worth one line in the report: the field name has a **typo**,
`numberr`. ⚠️ Worth pairing with the observation that
this dataset's `building_type` is also an uncontrolled vocabulary
(§B below) — same dataset, same class of problem.

---

## 7. `stt5-pzaa` — frozen two annual cycles while the report it comes from kept publishing

**Status: NOT SENT.** No notebook, no draft. **Last measured: 2026-09-20**
(S179, live against the Socrata API and `edmonton.ca` from the Oracle box).

**This closes a question `TODO.md` A2 carried unfiled for 13 sessions** — *is
`stt5-pzaa` retired, annual, or defective?* S166 measured that its rows had not
moved since 2025-02-19 but deliberately refused to write a row here, because a
table that stops updating may be a publisher defect **or** may simply be annual
or retired, and the three want different reports. **It is defective**, on the
publisher's own declared terms.

**Evidence — the dataset asserts it is current, and is not:**

- Its own Socrata `custom_fields` declare **`Update Frequency: Annually`,
  `Automated or Manual: Manual`**. There is **no deprecation signal of any
  kind**: `moderationStatus: None`, not hidden from the data catalogue, `flags`
  carries only routine values. ⚠️ The description's *"the City will no longer
  provide datasets…"* sentence is the **standard ADP/AltaLIS parcel-polygon
  boilerplate** appended across this portal, not a retirement notice — it reads
  like one to a keyword scan, which is why the text was checked.
- **Newest snapshot year is 2023.** Years 2016–2023, 393–487 parcels each,
  3,631 rows.
- `rowsUpdatedAt` = **2025-02-19**, 577 days at measurement. ⚠️ **All 3,631 rows
  carry the identical `:updated_at` second**, so that was a full
  truncate-and-replace; per-row load history is destroyed and **the API cannot
  say when any snapshot first appeared.** Do not try to date the 2023 load from
  it.
- ⚠️ **The program did not stop — only the open data did.** The City published
  `2023-Industrial-Land-Supply-Report.pdf` (PDF created 2024-09-17) and
  **`2024-Vacant-Industrial-Land-Report.pdf` (created 2025-12-17, ten months
  after the dataset's last touch)**, both HTTP 200 off
  `edmonton.ca/growthanalysis`. The 2025 edition 404s and is **not** late — on
  this cadence it is due ~Dec 2026.
- **The same defect hits `k8bn-rfq9` "Growth Monitoring Reports"**, which is the
  index *of those PDFs*: newest `year` is **2022**, last touched **2025-02-13**,
  six days before `stt5-pzaa`. One publication workflow, two frozen tables, one
  week apart — which is what makes this a workflow lapse rather than one broken
  table.
- Sibling `svsw-2ub7` "Vacant Land Inventory" (non-industrial) is frozen since
  **2021-06-21 — 1,916 days**, also declaring `Annually`. `parr-53tk` is a
  derived view of `stt5-pzaa` (`modifyingViewUid`), **not** independent
  corroboration.

**What it breaks here — and the staleness is the smaller half.**

A2 planned to compute industrial absorption from snapshot diffs. Two problems,
and the second is the dangerous one:

**(a)** Two annual cycles (2024, 2025) are simply absent, so any series built on
this ends in 2023, not today.

**(b)** ⚠️ **THE METHODOLOGY BROKE INSIDE THE MISSING GAP, AND THE BREAK IS
INVISIBLE FROM THE DATASET.** Footnote 4 of the 2024 report states that vacant
and reserved industrial land were **"previously combined (2020-2023)"** and are
now differentiated, and that the cycle newly includes industrial-zoned property
in mixed-use neighbourhoods, office and Direct Control zones, and underutilized
land. The dataset is the **old, combined** definition, confirmed by a stable
offset rather than assumed:

| year | `stt5-pzaa` Σ `area_ha` | the City's report | Δ |
|---|---|---|---|
| 2022 | 6,655.6 | 6,715 | 59.4 |
| 2023 | 6,628.5 | 6,687 | 58.5 |
| 2024 | **absent** | 6,990 total = 5,112 gross reserved + **1,878 net vacant** | — |

A ~59 ha constant offset across both years is the same series. **Continuing the
dataset's 6,628 ha with the 2024 report's "vacant" 1,878 ha shows a 72%
collapse that is entirely definitional** — and that is exactly the join a
reader, a reporter, or this project would make without reading footnote 4 of a
PDF that is not linked from the dataset.

**(c)** A2's own framing is "shovel-ready", and **footnote 1 of the 2024 report
says it "does not include data on shovel-ready lands."** The dataset's
`servicing` field is the only shovel-ready proxy either source offers — which
raises the dataset's value here rather than lowering it.

**What to ask for.** Refresh `stt5-pzaa` with 2024 (and 2025 when that edition
lands), **or** mark it retired if the 2024 split means it is being superseded —
the ask is not really about freshness, it is that **the metadata currently
asserts a live annual cadence, so a consumer who reads it is told the data is
current when it is two cycles behind.** If it is refreshed, ask for the
vacant/reserved split to be carried **as a column**, so the 2020–2023 rows stay
interpretable instead of silently changing meaning at the 2024 boundary. Same
ask for `k8bn-rfq9` — a four-column index of PDFs, cheap to fix, and currently
omitting two published editions. ⚠️ **One thing to raise in the City's favour,
because it may make the whole request moot:** the 2024 report quotes the 2024
Industrial Investment Action Plan (p.21) committing to *"establishing a vacant
land inventory data set"* — so a successor may already be planned, and the
right first question is whether this dataset is it.

**Channel:** `opendata@edmonton.ca` — portal dataset, same as 1, 3, 4 and 5.

⚠️ **Incidental, and it retires a blocker:** `docs/SPEC_industrial.md` recorded
these report PDFs as **"laptop-gated from the Oracle box."** All three
downloaded here over plain `curl` with the `certifi` bundle;
`www.edmonton.ca/growthanalysis` returns **200**. That claim was stale in the
same way the `budget.edmonton.ca` one was (S108) — **test the exact host, never
the domain.**

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

`tools/audit_roll_continuity.py` (re-run 2026-08-30 against historical 2024)
finds **1,457 of 426,913 parcels — 0.34%, $1.07B assessed** — with no current
match, by position rather than by any of the three churning identifiers.

⚠️ **This supersedes the 1,534 / $1.62B figure carried here from 2026-08-07.**
Position matched 1,578 as unmatched, but **121 of them ($592M — 35.6% of the
value) are still on the roll under the same account number**: recentroided past
the 5 m tolerance, not missing. The <2 m drift the tolerance was built on is a
four-hospital sample that does not generalize — these moved a median 58 m, up to
559 m. The tool now acquits them, and ⚠️ **widening the tolerance is the wrong
remedy**: it would trade a visible false positive for a silent false negative.

⚠️ **Those 1,457 are candidates, not verdicts, and the figure is an upper
bound** — demolitions, subdivisions and consolidations look identical to a
dropout from the outside, and a parcel that both renumbered *and* moved past the
tolerance is a false positive nothing here can see. That is exactly what makes
this unreportable today: we cannot yet say how many are real. The per-parcel
list is committed at `data/roll_continuity_candidates_2026-08-30.csv` so the
next observation can be diffed against it rather than compared as a bare count.

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

**⚠️ MEASURED CONSEQUENCE, 2026-09-18 — the missing freshness signal is no longer
hypothetical.** The feed appears to be **~3 months behind Council**, and nothing
about the response says so:

- On **2026-06-16** Council approved a **$126.6M (1.10%) net increase**, naming
  six newly funded projects (`edmonton.ca/city_government/budget-and-finances`).
- Fetched **2026-09-18**, the API is **byte-identical** to the copy committed
  **2026-08-22**, and its total is still **$11,510,831,000** —
  **$49,169,000 below** the **$11.56B** the City states on that page.
- **The strongest single indicator: the *"178 Street over Whitemud Drive Bridge"*
  rehabilitation, funded $16.0M in that adjustment, has NO profile in the feed at
  all** — zero rows on a `178` substring, in a file at profile grain covering
  FY2023–2037.

⚠️ **Stated as evidence, not proof, because the falsification attempt partly
succeeded.** Two of the six are ambiguous rather than absent — there IS a
*"New Transit Bus Garage"* profile at $365,109,000, which may or may not be the
*"Southeast Transit Bus Garage"* that received $66.0M, and a TACS Transformation
profile at $3,816,000 against a $1.3M award. **Only the 178 Street bridge is
cleanly missing.** So: most likely pre-adjustment, and **not confirmed**.

⚠️ **This is NOT a defect in `check_capital_budget`, and do not "fix" it there.**
That guard fingerprints sorted content and answers *"has the feed changed since
our pin"* — which is the right question for a re-fetch trigger, and it is
correctly reporting **Unchanged**, because the feed genuinely has not changed.
What no guard here can answer is *"does the feed still track the approved
budget"*, and **that is unanswerable by design while the publisher exposes no
vintage**. It is the reason the request above matters, one level up from
`guards-must-measure-data-not-metadata`: the metadata does not merely lie, it is
absent, so the only detector is a human noticing a Council decision is missing.

**Blast radius is small and should stay stated:** `capital_budget.csv` is read
only by `scripts/vintage_report.py`, not by the pipeline, so nothing the site
publishes moves on this. ⚠️ **It would matter immediately if any capital figure
were ever put on a served surface.**

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

### E. `lot_size` holds ownership SHARES, not square metres, for some records

**⚠️ CONFIRMED and exactly reproducible; NOT PROMOTED because it has no
published artifact yet** — the bar every numbered issue above clears.

Found 2026-09-01 by the Glass grid halving to 50 m, which stopped diluting it.
The needle cell is three WESTMOUNT records at identical coordinates — **commercial
storefronts**, 12203/12207/12211 107 Avenue NW, Tax Class Non-Residential
(`zoning` null), not condos as first recorded:

| account | assessed | `lot_size` |
|---|---|---|
| 4259396 | $469,500 | **0.505** |
| 4259412 | $185,500 | **0.218** |
| 4259420 | $204,500 | **0.277** |
| | $859,500 | **sum = 1.000** |

Three values summing to exactly 1.000 are **ownership shares of one parcel**,
recorded in a field whose every other row is square metres. The result is
$859,500 of assessment sitting on a nominal 1 m² lot — **$3.48B per lot-acre**,
79× the 99.9th-percentile cell.

Population, from `Property_Info__Current_Calendar_Year_.csv` (439,685 rows):

| `lot_size` band | rows | share |
|---|---|---|
| 0 < x < 1 m² | **7,984** | 1.82% |
| < 2 m² | 16,377 | 3.72% |
| < 5 m² | 27,990 | 6.37% |
| < 50 m² | 63,271 | 14.39% |

⚠️ **The share hypothesis is CONFIRMED for this parcel and NOT generalised** —
only 3 of 158 coordinate groups containing sub-1 m² lots sum to ~1.000, so
whatever produces the other 7,981 rows is unestablished and may be several
different things. **That gap is exactly what stops this being sendable.**

**What the other rows are — partial answer, 2026-09-02.** In the large towers
they are a **continuous graded series**: one 407-record point carries
0.279 / 0.558 / 0.837 / 1.394 / 1.952 / 5.02 … — integer multiples of a 0.279
base, i.e. per-unit apportioned shares scaled to *something*, straddling 1 m²
arbitrarily. So they are systematic, not junk, and the sub-1 m² population is
**not a clean defect boundary**: a record-level floor at 1 m² cuts one coherent
population in half. Measured cost of doing that: it cascades 66 points into
`majority_null` and drops **$1.43B (0.598% of city value)** to remove $859,500
— which is why the shipped rule is point-level and multi-record-only. Still
unestablished: what the shares are scaled *to*, and whether any point-total
recovers a true parcel area.

⚠️ ~~**It does NOT reach a reader.**~~ **FALSE — corrected 2026-09-02, found by
Peter using the live public site.** The claim checked two channels and missed
the third: `gridPickable: false` (can't click it) and the p97.5 colour clamp
(can't see it as colour) are both true, but **spike HEIGHT is not clamped**.
`gridScale` (`web/index.html`) anchors elevation on `vals[vals.length - 1]` —
the maximum cell — so the tallest cell is drawn at full height *by
construction*. This cell won that anchor, and every real cell was divided by
it: the p97.5 cell rendered at **0.249%** of full height on value/lot-acre and
**0.107%** on revenue/lot-acre. One needle over a flat plane, on the **public**
root (both `grid-fine` and `Lot acres` are ungated). Reachable via Money →
Revenue *or* Value → 50 m grid → Lot acres.

**Fixed 2026-09-02** — `MULTI_UNIT_MIN_LOT_M2` in `src/export_value_grid.py`:
a point holding **multiple** titled records whose total deduped lot area is
under 10 m² is not sitting on a real parcel, so it leaves the lot-acre metric
(ground-acre is untouched — the dollars are real, only the lot area is not).
Effect: `lot_needle_ratio` **79.01 → 13.93**, and the 50 m and 100 m grids now
**agree** (13.93 vs 12.82) where they differed 6× before — the divergence was
the artifact, not the resolution. Citywide cost: **4 changed fields, all
WESTMOUNT, all ≈0.05%** (`value_per_lot_acre`, `revenue_per_lot_acre`,
`nonres_revenue_per_lot_acre`, `far`).

⚠️ **The rule is restricted to multi-record points ON PURPOSE.** 381
single-record points hold genuinely tiny *real* parcels (median 8.4 m², median
value $500 — stalls, slivers) and produce unremarkable ratios; a floor that
caught them would delete real data for no gain. Insensitive to the exact cut
from 2–50 m² (one point throughout), so the threshold is not a tuning knob.

⚠️ **The dedupe rule is not at fault.** `FINDINGS_lot_dedupe.md` §3 contributes
`k × value` for repeats under `SHARE_MAX_M2 = 1000 m²` — correct for the
townhouse regime it was built for. These three values are *distinct* and each
appears once, so the rule passes them through untouched. **The inputs are
wrong, not the heuristic.**

To promote: a standalone notebook that reproduces the population from a live
fetch and settles what the other 7,981 rows are. `TODO.md` carries it.

---

### F. The Open Budget portal books FY2025's whole Neighbourhood Renewal line to program `Alley Renewal`

Found 2026-09-08 (S149 consolidation audit) on a fresh pull of
`budget.edmonton.ca/api/operating_budget.csv` (1,037,656 bytes). Branch
`Neighbourhood Renewal` is **$174,386,000 in each of FY2023–FY2026**. In
FY2023, FY2024 and FY2026 it is three rows — `Neighbourhood Renewal`
$158,106,000 + `Alley Renewal` $22,280,000 + `Less: Microsurfacing - City
Operations` −$6,000,000. In **FY2025 it is ONE row, program AND category
`Alley Renewal`, $174,386,000** — the whole levy labelled as alleys. The
total is right; the labelling is not. **Breaks here:** nothing served — the
line is not a pipeline input — but any per-program time series built from
the portal (`DATA.md` §17 already warns about renames) would show alley
renewal jumping 7.8× in 2025 and neighbourhood renewal vanishing. Same
publication as Socrata `da9s-v9j8`, so the Socrata copy presumably carries the
same row. **Not reported; not yet an artifact** — one `groupby` reproduces it
(`docs/FINDINGS_road_figures_consolidation.md` §6).

### G. The Snow & Ice annual report calls the same road inventory both "linear km" and "lane km"

Found 2026-09-10 (S154), re-reading a retrieval from the road-cost send-back
round. The City's *Snow and Ice Control Annual Report, Winter 2023-24*
(`edmonton.ca/sites/default/files/public-files/assets/PDF/Snow-Ice-Annual-Report_Winter2023-2024.pdf`,
28 pp.) says on **p4** *"The City maintains more than 12,000 **linear km** of
roadways and 500 km of active pathways"*, and on **p16** *"Distances are
represented in lane kilometres (lane km), which is a function of the length of
the street or bike route multiplied by the number of lanes"*. p13 repeats the
12,000 with no unit, as does the live *Winter Travel* page. **Magnitude says
p16 is right** — the City's own centreline feed holds ~6,340 km of roads +
alleys (`data/DATA.md` §6) — so p4 is the error. **Breaks here:** nothing
served (`roadway_ops` is already treated as lane-km), but it is the reason a
reporter's *"linear kilometres"* (Taproot 2025) looked sourced, and it makes
the unit unsettleable from wording alone. **Not reported; no artifact** — two
page quotes reproduce it. Channel if sent: `infrastructure@edmonton.ca`,
alongside the open Q1(a) question in `TODO.md` — **not** `opendata@`, since
this is a PDF report, not a dataset.

## Cross-refs

- `data/DATA.md` — what each source *is* (§0 historical roll, §11 FIR, §20
  schools + amenity distance, §21 the roll-year anchor)
- `docs/SPEC_temporal.md` §0 — the historical file's defect map and the omit
  decisions that follow from issue 3
- `docs/DECISIONS.md` 2026-08-25 — why a guard that reads a publisher's
  free-text metadata field is not measuring the data
- `docs/RUNBOOK.md` §1 — what to do when a roll-year guard holds the publish

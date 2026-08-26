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

⚠️ **Re-measure before quoting any figure below.** Several are derived against
the current roll, which moves weekly and rolled to 2026 in August. Each row says
when it was last measured.

---

## 1. `q7d6-ambg` — `Period of Coverage` names the wrong year, and has all year

**Status: NOT SENT.** No draft written.
**Last measured: 2026-08-26** (live metadata query).

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

**What it broke here — twice, and the second one is still broken:**

1. **The mill-rate pin sat a year stale.** `check_year_alignment.py` validated
   our `ASSESSMENT_YEAR` against this string; both said 2025, so it reported
   *aligned* and the pipeline billed a 2026 roll at 2025 rates — citywide levy
   understated **$69.5M (2.5%)**. Fixed 2026-08-25 by
   `scripts/check_roll_year_against_fir.py`, which measures parcels against FIR
   instead of reading anyone's metadata (`DECISIONS.md` 2026-08-25), and wired
   into `refresh.yml` 2026-08-26 so `python main.py` is gated on it.
2. **The temporal archive froze the 2026 roll under the label 2025** — issue 2
   below, unresolved.

**Why report it.** It costs Edmonton one field edit, and it is the kind of
defect no consumer can detect without an external anchor most consumers don't
have. The dataset is otherwise sound.

---

## 2. Our own consequence of issue 1 — the temporal archive's 2025 entry is the 2026 roll

**Status: N/A (ours, not theirs).** Listed here because it is a *direct
consequence* of issue 1 and would be unreadable filed anywhere else.
**Last measured: 2026-08-26.** Needs a decision — see the bottom of this row.

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
best-fits the year it is filed under. It exits 3 on today's archive. ⚠️ **Not
wired into any workflow yet** — it fails by design until the decision below is
made, so wiring it as a hold would stop the weekly publish.

**⚠️ OPEN — needs Peter's call.** The archive is frozen by design, so this is a
decision, not a rewrite. The options and what each costs are not yet written up.

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

## Cross-refs

- `data/DATA.md` — what each source *is* (§0 historical roll, §11 FIR, §20
  schools + amenity distance, §21 the roll-year anchor)
- `docs/SPEC_temporal.md` §0 — the historical file's defect map and the omit
  decisions that follow from issue 3
- `docs/DECISIONS.md` 2026-08-25 — why a guard that reads a publisher's
  free-text metadata field is not measuring the data
- `docs/RUNBOOK.md` §1 — what to do when a roll-year guard holds the publish

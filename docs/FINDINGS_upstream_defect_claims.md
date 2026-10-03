# FINDINGS — upstream-defect claims, before any is sent (ledger queue item 5)

**Run:** 2026-10-03, S214, Opus 5.5. Decision audit (L0–L3) over the six
publisher-facing issues in `docs/DATA_ISSUES.md` and the five drafts under
`docs/DRAFT_*`. ⚠️ Same model family that wrote the drafts.

**Why it gates sending:** a defect report to a publisher is outward-facing and
cannot be unsent. A wrong claim costs the project its credibility with the one
reader who can fix the data.

**Method — every claim re-measured live, not read off the drafts:**
- Socrata metadata (`/api/views/<id>.json`) for all 7 datasets named;
- SoQL aggregates on `q7d6-ambg`, `qi6a-xuwt`, `24uj-dj8v`;
- the Edmonton catalogue (Socrata discovery API) for issue 7's successor;
- the open.alberta.ca CKAN API for issues 4 and 5;
- `scripts/recheck_evidence_notebooks.py` cold-cache: **5 evidence notebooks,
  37 invariants, all ✅** (plus the 2 roads notebooks, 67 ✅).

---

## 1. Verdicts

| # | issue | L0 send at all? | L1 claim true today? | L2 message says only what the evidence supports? | verdict |
|---|---|---|---|---|---|
| 1 | `q7d6-ambg` coverage year | yes | ✅ still `2025-01-01 to 2025-12-31`; rows updated 2026-09-28 | ⚠️ misses the obvious rebuttal (F3) | **CONDITIONAL** — add one paragraph, then send |
| 3 | `qi6a-xuwt` dropout | yes | ✅ `rowsUpdatedAt` still 2026-01-12; notebook 6/6 live | ❌ attributes our detector to the City (F2) | **CONDITIONAL** — fix one paragraph, then send |
| 4 | exemption status | yes | ✅ no exempt column; 2025 manual still the newest edition | ✅ message; ⚠️ stale sender notes (F4) | **SOUND** (notes fixed here) |
| 5 | school locations | **no** | ✅ on Edmonton's portal; ❌ "nobody publishes it" | ❌ the premise is answered by Alberta (F1) | **UNSOUND — do not send** |
| 6 | permit neighbourhood list | yes | ✅ 546 of 247,162 rows; id comma-joined on all 546, 0 name-only | ✅ all four quoted examples exist | **SOUND** |
| 7 | `stt5-pzaa` frozen | n/a (no draft) | ✅ still 2025-02-19; `k8bn-rfq9` still 2025-02-13; no successor on the portal | — | **holds; not sendable until it has an artifact** |

Nothing here is a FAIL on a published number. **F1 is a public claim**:
the school evidence page says the provincial lists are PDFs.

---

## 2. Findings

### F1 (HIGH, public) — Alberta already publishes a machine-readable directory of every school, missing operators included

open.alberta.ca `alberta-education-schools-and-authorities` → *Alberta school
information report*, XLSX (`education.alberta.ca/media/1626669/authority_and_school.xlsx`).
The `Extract Date` column read **2026-10-02 08:00**, so it is regenerated daily.

- **2,687 schools province-wide; 450 with `School City` = Edmonton.**
- **Edmonton, by `Authority Type`:**
  - Public 227
  - Separate 101
  - Private School 54
  - ECS Private Operator 25
  - Provincial 20
  - Charter 11
  - Francophone 10 (9 under *The Greater North Central Francophone Education
    Region* = Centre-Nord)
  - Federal First Nations 2
- **Columns:** school code, name, street address, postal code, ECS/elementary/
  junior/senior flags, authority name and type. **No coordinates.**
- It corroborates the two board feeds: Public 227 here, against `996c-239n`'s
  225 rows.

**What this breaks.**
- **The draft request** (`DRAFT_open_data_request_school_locations.md`) asks
  Edmonton for a dataset and invites *"if the data sits with the province, that
  would be a useful answer"*. We now hold that answer. Sending it asks the City
  to research something we could have looked up. That is the same credibility
  class as issue 6's old ask, the one that asked for a field already published.
- **Three in-repo claims are wrong.** Each says the provincial lists are
  **PDFs** and not addressable rows:
  - `notebooks/standalone/school_coverage_gap.py` §4 — **on the published page**;
  - `data/DATA.md` §20;
  - `docs/ANALYSIS_BACKLOG.md` §13 (*"settled by probe, do not re-derive"*).
  The 2026-08-23 probe found the PDF lists and stopped. This XLSX sits in the
  same catalogue.
- **The evidence page's invariants still pass**, correctly, because they test
  Edmonton's portal only. Its scope sentence is what overreaches.

**What it does NOT break.** The narrow claim still holds: *Edmonton's portal
carries no point set for these operators*. The direction of our error is
unchanged (missing schools only make "nearest school" look further away).

**Remedy.**
- **Do not send issue 5.** It is left `NOT SENT` with a hold note in
  `DATA_ISSUES.md`.
- Correct `DATA.md` §20 and `ANALYSIS_BACKLOG.md` §13 (done here).
- The notebook text is the report session's (sent to it).
- ⚠️ **ANALYSIS_BACKLOG §13's staleness objection to a hand-built list no longer
  applies as stated.** This source has a daily `Extract Date`, which is a
  freshness signal. What is left is geocoding about 150 addresses. Whether to use
  it in `dist_school_m` is Peter's call; it is a new input, so propose first.

### F2 (MEDIUM, outward-facing) — the dropout message tells the City its own audit disagrees, but the "self-audit" is ours

The draft says: *"The dataset's own quality indicators don't appear to reflect
the loss — comparing its internal audit figures against the current roll, the
two disagree by a factor of several hundred."*

`qi6a-xuwt` publishes **no** quality indicator or audit figure. The notebook's
"self-audit" is **detector A**, which **we** built from the dataset alone
(absent in N, present in N−1 and N+1; `historical_2024_gap.py` §3). The 464× is
detector B 2,321 ÷ detector A 5. A City reader would look for an audit field
that does not exist.

**Fixed in the draft here.** It now says that a check using only the dataset's
own slices finds 5, while checking against the current roll finds 2,321.

**Also, LOW:** *"absent from the 2024 and 2025 slices"* fits about 2,317 of the
2,448. The notebook shows 131 accounts dropped in 2025 only. Reworded to
*"absent from the 2025 slice (nearly all of them from 2024 as well)"*.

### F3 (MEDIUM, outward-facing) — the coverage-year report invites a valuation-date reply and does not answer it

An Alberta roll for tax year N values property as of **July 1, N−1**. So a City
reader can reasonably answer *"2025 is the valuation year of the 2026 roll"*.
Neither the draft, the notebook nor `DATA_ISSUES.md` addresses it.

**It is answerable from the City's own data.** `qi6a-xuwt` labels its rolls
by roll year:
- its `assessment_year = 2025` RESIDENTIAL total is **$149.65B**, against FIR
  2025's **$148.1B** (+1.0%);
- the current resource reads **$162.55B**, against FIR 2026's **$160.4B**
  (+1.3%) and FIR 2025 (+9.7%).

So the sibling dataset calls the 2025 roll "2025", and `q7d6-ambg` calls the
2026 roll "2025". **The objection fails, but only if the message says so.**

**Fixed in the draft here** with one paragraph. The figures there are
re-measured 2026-10-03 (411,575 accounts, $162.5B).

### F4 (LOW, internal) — the exemption draft's sender notes are stale and contradict the channel rule

- The notes still say *"THE ONE THING STILL UNRESOLVED IS WHERE TO SEND IT"* and
  *"`edmonton.ca` is unreachable from the Oracle box"*. Both are false:
  - the channel was settled 2026-08-25 (`opendata@edmonton.ca`);
  - `edmonton.ca` returns 200 from this box with `certifi` (DATA_ISSUES §7).
- The message's `To:` line reads *Open Data / Assessment & Taxation Branch*,
  against DATA_ISSUES' rule that A&T is the escalation, not the first stop.

Fixed here.

### F5 (LOW, internal) — `DATA_ISSUES.md` §4 calls `NONRES MUNICIPAL/RES EDUCATION` an exemption flag

§4 says the roll *"flags 3 properties / $7.6M as exempt"*. That `mill_class_1`
value names a **split-rate** class (municipal at the non-residential rate,
education at the residential rate), not an exemption. Live:
- 2 accounts, $4.3M as `mill_class_1`;
- 1 account, $66.3M as `mill_class_3`.

The draft message never uses it, so nothing outward is wrong. The internal
record now says it is a proxy (done here). `data/DATA.md` already calls it a
"best proxy", and `is_exempt` in the pipeline is unaffected by this run.

---

## 3. What would change these verdicts

- **Issue 1:** a City statement that `Period of Coverage` is meant as the
  valuation year. That would make it a documentation request, not a bug. Asking
  is cheap, and the new paragraph does.
- **Issue 5:** if the provincial XLSX were found to omit a material share of
  Edmonton's private or charter schools against the PDF lists, the request
  would survive in a narrower form. Not checked; the count of 54 + 25 + 11 + 10
  looks complete for a city this size.
- **Issue 6:** the dataset refreshes daily, so 546 drifts. Re-measure on the
  send date (the draft already says so).

---

## 4. What this run got wrong

- **I first read the 2,322 + 131 = 2,453 vs 2,448 mismatch in `DATA_ISSUES.md`
  §3 as an arithmetic error to report.** The notebook explains it: 5 accounts
  dropped out and returned, and it shows the 2,453 − 2,448 difference on
  purpose. Not a finding.
- **The Wayback Machine check for the field's value during the 2025 roll
  failed.** CDX returned 504 twice and `[]` once. F3 therefore rests on the
  sibling dataset's convention, not on the field's own history. That is weaker
  than a snapshot showing the field read `2025` all through 2025.
- **I killed my own wait loop with `pkill -f`**, the exact hazard in memory
  (`pgrep-watchers-match-themselves`). No data was lost; the output file was
  intact.
- **F1's Edmonton count uses `School City`, a mailing field.** Schools with a
  St. Albert or Sherwood Park mailing city inside the boundary, or the reverse,
  are miscounted. That doesn't touch the finding, which is that the source
  exists. It does matter if the source is ever used.

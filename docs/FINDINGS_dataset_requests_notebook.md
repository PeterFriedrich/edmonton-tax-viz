# FINDINGS — the Dataset Requests notebook (`04_dataset_requests.py`, #538/#539)

**Run:** 2026-09-23, S190, Opus 5.5, `edmonton-audit` decision family.
⚠️ Opus 5.5 also wrote the notebook (S189), so this run is the same model and is **not independent**.
**Data:** live `a9w6-s3na`, 656 rows, same count as S189. The notebook was re-executed against it through a harness. All 9 invariants pass, and every printed figure matches the S189 handoff.
**Probes:** the scratch scripts were not kept. Each finding below names the exact rows, so any of them can be re-derived from the live table.

## Verdicts, top-down

| Level | Question | Verdict |
|---|---|---|
| L0 | Publish this as a background page at all? | **SOUND.** The data is public, and the page is framed as landscape rather than as a defect report. |
| L1 | Is the Dec-2023 re-reading right, i.e. is a migration-day stamp a move and not a refusal? | **SOUND** (§1) |
| L2 | Is "real refusals = 78" right? | **CONDITIONAL** (§2) |
| L3 | Topic heuristic (§4, §5b) | **CONDITIONAL.** Two regex bugs misfile 24 requests (§3). |
| L4 | §5a/§5b prose | **One FALSE sentence** (§4) |
| L5 | §5e catalogue estimate | **CONDITIONAL.** The date anchor is invalid for 57 of 152 rows (§5). |
| L6 | §6 duplicate check (the notebook's first job) | **CONDITIONAL.** The closest precedent for Issue 4 goes unmentioned (§6). |

## 1. The migration pairing is sound, and not by luck

- **127 = 127.** 127 old rows were stamped on 2023-12-12/13, and 127 tracker rows were created on those same days. Title matching pairs 126 of them.
- **One-to-one holds structurally.** Only two title keys occur more than twice in the whole table: `bikecounts` and `speedlimits`. Neither involves two migration-day rows, so no ambiguous merge was ever possible.
- **The two unpaired rows are not a missed pair.**
  - `ODR22-351` is a question about map data vs. Socrata, not a dataset request.
  - `8686q114n` is about mowed grass.
- **Only one old row matches a tracker row outside the migration days**, and it doesn't change any count. `ODR16-75` "Speed limits" (Completed 2019) matches `8686qhk00`, but that tracker row is paired with `ODR21-328`, not with `ODR16-75`.
- **The migration moved only the undecided subset.** The 78 unmoved refusals have status dates spread over 2016–2023, so they had already been refused when the migration ran. "Never decided" is therefore supported, not just "moved".
- **Caveat:** the table has no history, so a moved row's pre-migration status can't be seen directly. What supports "never decided" is that pattern of selection.

## 2. "78 real refusals" includes 16 made in a backlog sweep seven years late

- The notebook's §2b warns that `status_date` spikes are bulk edits. That check was **never applied to the refusal set itself.**
- Two such days are hiding in it:
  - **2023-09-19:** 12 refusals, plus 4 Completed rows, all requested in 2016. (A 13th refusal dated that day, `ODR23-373`, was a genuine next-day decision.)
  - **2023-06-07:** 5 refusals. All are 2016 water and wastewater requests (`ODR16-100`…`104`).
- **Effect on 2016:** of 2016's 40 "refused", 16 were declined in these sweeps roughly 7.5 years later. That is housekeeping, not a considered no. The median request-to-refusal lag across all 78 is only 0.24 years, so these sweeps stand out clearly.
- **Two further rows aren't really refusals:**
  - `ODR19-269` is titled `test`, with details `test`.
  - `ODR19-260`/`261`/`262` are one person's same-day asks for PDFs of City documents. They are refused requests, but not requests for data.
- **Fix:**
  - Split the sweeps out as a fifth fate: "closed in a backlog sweep".
  - Drop `test`.
  - Say what's left: about **61 decided refusals**. The 2.6× headline becomes about 3.3×. The direction holds, and the claim gets stronger.

## 3. Topic regexes: `\bbus` matches "business" and `tree` matches "street"

- **Transit is first in the list and wins every tie.** Its `\bbus` fires on "business" in **20 requests**, for example:
  - `ODR17-148` "Publish BIA data (Business Improvement Areas)"
  - `ODR16-108` "Travel Expenses for City Employees"
  - `ODR16-73` NAICS codes
- **Parks' unanchored `tree` fires on "street" 4 times**, for example `ODR16-106` "LED Streetlight Conversion" and `ODR22-339` "142 Street Roundabout".
- **With `\bbus(?:es)?\b` and `\btrees?\b`:**
  - 24 requests change topic.
  - **§4 Transit falls from 50 to 30.** 40% of the published Transit row was business-related text.
- Lesser hits, too few to matter: `\btax` on "taxis" (`ODR17-137`), and `river` on "driver" (`32x16xn`).

## 4. False sentence in §5a: "Utilities & drainage is the only topic in §5b with more refusals than completions"

- The notebook's own §5b table contradicts it. **Property, assessment & tax has 11 refused vs 10 completed** (12 vs 10 once the regexes are fixed). This is the topic this project cares most about.
- **The utilities 13 is also soft:**
  - 2 of the 13 are misfiled: `ODR16-38` EV charging, and `ODR16-58` picnic sites (it mentions water).
  - 5 are the 2023-06-07 sweep (§2).
  - "Gas and power mapping" is 3 rows, two of them identical `Gas utility mapping` requests filed the same minute.
- The honest statement is weaker: utilities and property both lean toward refusal, and the counts are small.

## 5. §5e anchors on a date that is bulk-stamped for 57 of 152 CLOSED rows

- **The estimate transfers a catch rate across two populations whose dates mean different things.**
  - The catch rate (30/80 = 38%) is measured on old `Completed` rows. None of the 80 shares its published date with 2 or more other rows, so those dates look like real publish dates.
  - On `CLOSED` rows, **57 of 152 close on a day shared with 2 or more other closes**, for example 16 on 2023-12-19 and 9 on 2025-12-31 (a year-end sweep). This is exactly the §1 point that the date on a CLOSED row means "date closed".
  - A ±45-day window around a bulk-close day says nothing about when an asset was created.
- **The estimate is therefore biased low**, on top of resting on 6 hits. Treat "~16 of 152 (~11%)" as a **floor**, not as an order-of-magnitude estimate.
- **The matching itself is clean.** I read all 30 Completed matches, and every one is the right asset (e.g. "Hens and Bees" → "Hens and Bees"). False positives are not the problem.
- **Code nit:** `~d.moved` on the CLOSED selection is a no-op, because only ODR rows are ever `moved`. It was probably meant to be `~d.reintake`. The 53 re-intake rows are included today; say whether that's intended.

## 6. §6 Issue 4 skips the precedent that most resembles our ask

- **`ODR23-363`** (2023-04-27) asked to add columns to *Property Assessment Data (Current Calendar Year)*: zoning, legal description, title ownership. It was **genuinely Rejected** on 2023-05-04. That was not a migration stamp.
- It appears in the Issue-4 context table, but the prose points the reader at `868ev4dbu` (NEW) and says to "be ready for a similar answer".
- Asking to add a tax-status column to `q7d6-ambg` is the same shape of request, and the last one was **refused in a week**. The prose should cite `ODR23-363` first.
- Minor: 2 of the context block's 13 rows are migration duplicates (`ODR19-233`/`8686qh18m`, `ODR19-245`/`8686qh3ah`), so there are 11 unique requests. Several of them, such as the 2023 release or the parcel polygons, aren't asks for new fields.

## 7. Prose numbers checked against the executed output

**Match:**
- header: 126 moved, 241 bulk-edit rows, 2.6×
- §5a:
  - 0.41/0.45/0.51 → 0.12/0.13
  - 2021 = 16 requests
  - "never decided > refused every year from 2017"
- §5b: utilities 13 vs 7
- §5c: 135 open, median 4.0 years, 59 asked 5+ years ago
- §5e: 30/80, 16/152
- §6: hit counts; the `8686qh58b` and `8686qhh84` statuses

**Wrong:** the §5a "only topic" sentence (§4 above).

**Not checkable from the notebook:** "only 11 of 111 [2016 rows] are hackathon captures". No cell computes it.

## What this run got wrong

- **I first counted 17 sweep refusals.** One of the 2023-09-19 rows, `ODR23-373`, was created the day before and is a real decision. Correct figure: 16.
- **I tried a date-shift null (±1–2 years) as a false-positive test for §5e.** It returned 1–11 CLOSED matches, which looked like "6 is noise". Shifted matches aren't false positives, though: an asset with the same name a year earlier is often the existing dataset the request was answered with. I dropped that argument and inspected the matches directly instead.
- **The §4 finding stands on the same heuristic it criticises.** The "Property 12 vs 10" count comes from my patched regexes, which were checked only for the two bugs above. The next-worst pattern could still misfile a few rows.
- **L1 is SOUND only by inference from selection** (§1 caveat). I have not seen a City statement describing the migration.

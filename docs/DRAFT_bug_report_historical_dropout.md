# DRAFT — Bug report: `qi6a-xuwt` drops 2,448 accounts from its 2024/2025 slices

**Status: DRAFT, NOT SENT.** Written 2026-09-17. Peter's to send, edit or discard.

**Channel:** `opendata@edmonton.ca` (portal footer, read 2026-08-25). Assessment
& Taxation is the escalation if Open Data bounces it, not the first stop.

⚠️ **Send separately from the `q7d6-ambg` coverage-year report.** Different
dataset, different defect.

---

## Claims, re-verified live 2026-09-17

| Claim | Status |
|---|---|
| `qi6a-xuwt` has not been updated since **2026-01-12** | ✅ **VERIFIED TODAY** (`rowsUpdatedAt` = 2026-01-12). **The defect is therefore still present** — nothing has been republished that could have fixed it. |
| Its `Period of Coverage` reads `2012 - 2025` | ✅ **VERIFIED TODAY** |
| 2,448 accounts cumulative, 188 neighbourhoods, Downtown worst at 1,292 | ⚠️ **Last measured 2026-08-26**, not re-run today. Account counts reproduced exactly on that run. Safe to quote because the historical table has not moved since January. |
| Self-audit vs current-roll control disagree by **464×** | ⚠️ Same provenance as above. **This is the single most useful sentence for the City** — it says the dataset's own quality check does not see the loss. |
| 11 of 13 testable years are clean | ⚠️ Same provenance. Important: it makes this a slice-specific fault, not a systemic export fault. |
| Building-shaped: 272 addresses, 29 losing every account (969 total) | ⚠️ Same provenance. Largest: 309 and 261 units at 10310 / 10360 102 ST NW. |
| Evidence page is live and linkable | ✅ `/notebooks/historical-2024-gap.html`, 6/6 invariants asserted, includes real account numbers and the portal query |

⚠️ **Do not send `notebooks/exploration/03_historical_roll_gap.ipynb`** — the
superseded version.

⚠️ **Re-run the notebook before sending.** The figures are three weeks old. The
historical table has not moved, but the *control* is the current roll, which
refreshes weekly — so the dollar figures drift even when the account counts do
not. Quote account counts, not dollars.

---

## Draft message

> **To:** City of Edmonton Open Data
> **Subject:** Data quality — accounts missing from the 2024 and 2025 slices of Historical Assessment (`qi6a-xuwt`)
>
> Hello,
>
> I've been using the *Historical (Property) Assessment* data (resource
> `qi6a-xuwt`) to look at assessment over time by neighbourhood, and I believe
> its 2024 and 2025 slices are missing a substantial number of accounts.
>
> **What I'm seeing.** Roughly **2,448 accounts** that appear both in earlier
> slices of the same dataset and in the current assessment roll are absent from
> the 2024 and 2025 slices. They span **188 neighbourhoods**, with Downtown
> worst affected at about **1,292 accounts**. Eleven of the thirteen testable
> years look clean, so this does not appear to be a systemic export problem —
> it looks specific to those two slices.
>
> **The loss is building-shaped, which may help locate the cause.** The missing
> accounts cluster at about **272 street addresses**, and **29 of those
> addresses lose every account they had** — 969 accounts in total. The two
> largest are roughly 309 and 261 units at 10310 and 10360 102 ST NW. That
> pattern looks more like whole multi-unit buildings failing to carry through an
> export step than like scattered record-level errors.
>
> **One thing I'd flag as possibly relevant:** at least one Downtown address
> appears in the data under three different spellings of the street name
> (`102 STREET`, `102 SSTREET`, `102 STSREET`). If address strings are used as a
> key anywhere in the pipeline that builds these slices, that could be part of
> it.
>
> **Why I'm reporting it rather than working around it.** The dataset's own
> quality indicators don't appear to reflect the loss — comparing its internal
> audit figures against the current roll, the two disagree by a factor of
> several hundred. So a user has no signal from within the data that anything is
> missing, and any per-neighbourhood time series built from these slices
> understates 2024 and 2025 without saying so.
>
> Full working, including specific account numbers and the portal queries to
> reproduce it, is here:
> https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/historical-2024-gap.html
>
> I'd be glad to hear if I've misunderstood how these slices are built — for
> instance if accounts are intentionally excluded under some condition I haven't
> accounted for.
>
> Thank you for your time.
>
> [name / contact]

---

## Notes for whoever sends this

- **The 464× sentence is deliberately softened** to "disagree by a factor of
  several hundred" in the message. The precise figure is in the linked notebook.
  Leading with a hard multiplier on *their* quality check reads as an accusation;
  the point is to get the slices fixed, not to grade their audit.
- **The three-spellings observation is offered as a hypothesis, not a diagnosis.**
  We do not know how the slices are built. Stated as a lead, which is useful;
  stated as the cause, it invites a correction that derails the report.
- **Quote account counts, not dollar figures.** The dollar control is the
  current roll and moves weekly.
- **Do not bundle the `Period of Coverage` issue into this**, even though this
  dataset also carries one (`2012 - 2025`). That is a different report and a
  different dataset.
- ⚠️ **Check `rowsUpdatedAt` before sending.** It has read 2026-01-12 since
  January. If the table has been republished, **re-measure first** — the defect
  may be gone, and a stale bug report is worse than none.

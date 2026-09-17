# DRAFT — Bug report: `Period of Coverage` on `q7d6-ambg` names the wrong year

**Status: DRAFT, NOT SENT.** Written 2026-09-17. Peter's to send, edit or discard.

**Channel:** `opendata@edmonton.ca` (portal footer, read 2026-08-25). Assessment
& Taxation is the escalation if Open Data bounces it, not the first stop.

⚠️ **Send this one separately from the `qi6a-xuwt` dropout report.** Different
dataset, different defect, different fix. Filing them together muddles both —
the same rule the exemption-status request already follows.

---

## Why this one is worth sending

It costs Edmonton **one field edit**, and it is the kind of defect no consumer
can detect without an external anchor most consumers don't have. The dataset is
otherwise sound. `DATA_ISSUES.md` §1 records three separate downstream defects it
caused here, in three different subsystems, over roughly a month — each found by
accident rather than by looking.

---

## Claims, re-verified live 2026-09-17

| Claim | Status |
|---|---|
| `Period of Coverage` reads `2025-01-01 to 2025-12-31` | ✅ **VERIFIED TODAY** from `https://data.edmonton.ca/api/views/q7d6-ambg.json` |
| `rowsUpdatedAt` is **2026-09-14** | ✅ **VERIFIED TODAY.** ⚠️ **New fact, stronger than the August measurement: the field survived a refresh three days ago.** It is not merely stale, it is not maintained by the refresh. |
| The served content is the **2026** roll | ✅ **RE-MEASURED TODAY.** Residential assessed base on the live resource is **$162,309,281,500** over 411,525 accounts — byte-identical to the 2026-08-26 measurement. |
| FIR `MR(2)` residential base: $148.1B (2025), $160.4B (2026) | ✅ Recorded in `DATA_ISSUES.md` §1 from Alberta FIR filings. Today's $162.3B is **+9.6% against 2025 and +1.2% against 2026**. |
| Evidence page is live and linkable | ✅ `/notebooks/roll-year-metadata.html`, 8/8 invariants pass, two independent proofs (Edmonton's own data; Alberta FIR) |

⚠️ **The evidence page reports its own obsolescence** — its first invariant flips
when the City corrects the field. Re-run it before sending if more than a few
weeks pass.

---

## Draft message

> **To:** City of Edmonton Open Data
> **Subject:** Metadata correction — Period of Coverage on Property Assessment Data (`q7d6-ambg`)
>
> Hello,
>
> I use the open assessment data regularly and I think one metadata field on
> *Property Assessment Data (Current Calendar Year)* (resource `q7d6-ambg`) is
> reporting the wrong year.
>
> **The field:** `Period of Coverage` currently reads `2025-01-01 to
> 2025-12-31`. As of today the resource's `rowsUpdatedAt` is 2026-09-14, and the
> content appears to be the 2026 roll rather than the 2025 one.
>
> **What suggests the content is 2026.** The residential assessed base on the
> live resource sums to about $162.3B across 411,525 accounts. Edmonton's
> filings with Alberta Municipal Affairs (Financial Information Return, Schedule
> MR(2)) put the residential base at roughly $148.1B for 2025 and $160.4B for
> 2026. The served file is about 9.6% above the 2025 figure and within about
> 1.2% of the 2026 one, which points fairly clearly at 2026.
>
> **Why it matters to data users.** The coverage string is the only statement in
> the dataset of which roll year the rows belong to. Anyone joining this data to
> a published mill rate has to pick a year, and this field is the natural thing
> to trust. Choosing the year it names produces a levy calculation that is
> internally consistent, looks correct, and is off by a full year of assessment
> growth — with nothing in the data to signal it. It appears the field is
> hand-maintained and did not move when the roll rolled; it also did not change
> in the 2026-09-14 refresh, so I don't think the refresh updates it.
>
> **The fix I am suggesting** is just correcting the field to the year the rows
> actually cover, and if possible including it in whatever updates
> `rowsUpdatedAt` so it can't drift again.
>
> Working notes and the full comparison are here, if useful:
> https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/roll-year-metadata.html
>
> If I've misread which roll this resource is meant to carry, I'd be glad to be
> corrected — that would be just as useful to me.
>
> Thank you for maintaining these datasets.
>
> [name / contact]

---

## Notes for whoever sends this

- **Lead with the field, not with our pipeline.** What Edmonton needs is the
  name of the field and the year it should say. Our three downstream defects are
  the reason *we* care; they are not their problem and don't belong in the note.
- **The FIR comparison is the load-bearing evidence** — it is the external
  anchor, and it is what makes the claim checkable on their end without trusting
  our arithmetic. Keep it.
- **Do not assert the field is hand-maintained as fact.** The message says "it
  appears" for a reason: we have observed that it did not change across a
  refresh, which is evidence, not confirmation of their process.
- **Re-measure the $162.3B before sending** if the roll has refreshed since
  2026-09-17. One query:
  `https://data.edmonton.ca/resource/q7d6-ambg.json?$query=SELECT tax_class, sum(assessed_value) GROUP BY tax_class`
- ⚠️ **If the field has been corrected by the time this is sent, do not send it.**
  Close the row in `DATA_ISSUES.md` as FIXED instead, and note the date.

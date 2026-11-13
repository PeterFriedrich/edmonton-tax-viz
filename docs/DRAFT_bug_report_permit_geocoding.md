# DRAFT — Bug report: `24uj-dj8v` stopped geocoding most new-construction permits around January 2025

**Status: DRAFT, NOT SENT.** Written 2026-11-13. Peter's to send, edit or discard.

**Channel:** `opendata@edmonton.ca` (portal footer, read 2026-08-25).

⚠️ **Send separately** from the issue 6 report (`DRAFT_bug_report_permit_neighbourhood_list.md`).
It's the same dataset but a different defect, and either can be fixed without the other.

---

## Claims, measured live 2026-11-13

Pulled from `24uj-dj8v` with `issue_date >= 2023-01-01`, filtered to the
pipeline's `NEW_WORK_TYPES` (`src/load_permits.py`). "Geocoded" means both
`latitude` and `longitude` are non-null.

| Claim | Status |
|---|---|
| New-construction permits were 94–99% geocoded every month from 2023-01 to 2024-03 | ✅ measured |
| The share fell through 2024: 76–89% from April to November, 66% in December, 51% in January 2025 | ✅ measured |
| Every month from 2025-02 to 2026-10 is 21–44% geocoded | ✅ measured (lowest 2026-04, 21.4%; highest 2025-08, 43.7%) |
| No age gradient: older months are not filling in | ✅ 2025-02 is 39.2%, 2026-10 is 31.4%. The 2024 and 2025 un-geocoded counts moved by −2 permits between 2026-07-14 and 2026-11-10 (`docs/FINDINGS_roads_release.md` §10 D1) |
| Since 2025-02: 6,433 of 9,367 new-construction permits have no coordinates, carrying 14,268 of 28,267 `units_added` | ✅ measured |
| The drop is concentrated on new construction | ✅ all permit types together: 96–97% in early 2024, 62–77% every month since 2025-02 |
| The un-geocoded rows still carry an address (6,433 of 6,433) and a neighbourhood (6,431) | ✅ measured, so the City has what geocoding needs |

**What the data cannot say:** whether the process changed around the turn of
2025 or a batch geocoding job has stopped running. The message asks; it does not
guess.

**No evidence notebook.** The message gives a one-line query the City can run
itself, so the claim stays checkable without one. If a notebook is wanted for
the monthly recheck, it would join `docs/EVIDENCE_NOTEBOOKS.md`.

---

## Draft message

> **To:** City of Edmonton Open Data
> **Subject:** General Building Permits (`24uj-dj8v`) — most permits since early 2025 have no coordinates
>
> Hello,
>
> I use the *General Building Permits* data (resource `24uj-dj8v`) to map new
> construction, and I've noticed that the `latitude` and `longitude` fields
> stopped being filled in for most permits around the start of 2025.
>
> **What I'm seeing.** For new-construction permits, coordinates are present
> on 94–99% of permits each month through March 2024. The share then falls:
> roughly 80% for most of 2024, 51% in January 2025, and between 21% and 44%
> in every month from February 2025 to October 2026. Since February 2025,
> about 6,400 of 9,400 new-construction permits have no coordinates. Other
> permit types dropped too, but less: all permits together went from about
> 97% to between 62% and 77%.
>
> **It doesn't look like a backlog clearing.** Permits from early 2025 are
> geocoded at about the same rate as last month's, and the counts for 2024
> and 2025 have barely changed since July. So it looks as though whatever
> used to add coordinates stopped running or changed, rather than running
> behind.
>
> **The rows aren't missing anything else.** Every one of them still has an
> address, and almost all have a neighbourhood, so neighbourhood-level totals
> are fine. Only maps and anything spatial below the neighbourhood are
> affected.
>
> This query counts new-construction permits with and without coordinates
> by issue month:
>
> `https://data.edmonton.ca/resource/24uj-dj8v.json?$select=date_trunc_ym(issue_date) AS month, count(*) AS permits, count(latitude) AS geocoded&$where=issue_date >= '2024-01-01' AND work_type in('(01) Building - New', '(01) New', '(01) New House')&$group=month&$order=month`
>
> (Without the `work_type` filter it shows the smaller drop across all
> permit types.)
>
> Could you tell me whether this is a known change, and whether coordinates
> are expected to be added for these permits? If geocoding has moved to a
> different dataset or process, a pointer to it would help just as much.
>
> Thank you for your time.
>
> [name / contact]

---

## Notes for whoever sends this

- **Re-run the query before sending.** If recent months are back above ~90%,
  don't send. Mark `DATA_ISSUES.md` §9 resolved upstream, and expect the
  Development grid coverage to jump on the next weekly refresh.
- The query in the message was run 2026-11-13 and reproduces the monthly
  figures above exactly. Its `work_type` list is `NEW_WORK_TYPES` from
  `src/load_permits.py`; if that set changes, update the query.
- **Keep the ask open-ended.** The data can't tell a process change from a
  stalled batch job, and guessing wrong costs the report credibility.

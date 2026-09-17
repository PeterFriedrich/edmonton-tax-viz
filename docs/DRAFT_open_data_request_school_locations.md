# DRAFT — Open Data request: publish school locations for the remaining operators

**Status: DRAFT, NOT SENT.** Written 2026-09-17. Peter's to send, edit or discard.

**Channel:** `opendata@edmonton.ca` (portal footer, read 2026-08-25).

⚠️ **This is a request, not a bug report.** It asserts no defect. Two school
boards publish locations and do so well; the ask is for the rest. Keep the tone
matched to that — the coverage-year and dropout reports are the ones that report
something broken.

**Lowest priority of the four.** Send it last, or fold it in only if a
conversation is already open.

---

## Claims, re-verified live 2026-09-17

| Claim | Status |
|---|---|
| EPSB locations published: `996c-239n`, **225 rows** | ✅ **VERIFIED TODAY** (`Edmonton Public School Board (EPSB)_School Locations`, updated 2026-04-22) |
| Catholic locations published: `gfxq-u8uu`, **97 rows** | ✅ **VERIFIED TODAY** (`Edmonton Catholic Schools (Current)`, updated 2026-05-04) |
| No point set for private, charter or francophone operators | ✅ **RE-RUN TODAY.** Catalogue searches for `private school`, `charter school`, `independent school`, `francophone`, `Centre-Nord` return **no school location dataset** for any missing operator. Hits are unrelated (Playgrounds, Insight Community surveys, a 2016 census residency table). |
| Evidence page is live and linkable | ✅ `/notebooks/school-coverage-gap.html`, 4/4 invariants pass |

⚠️ **This argues an ABSENCE, so it is built the opposite way round from the other
reports:** the notebook runs the searches that would *disprove* the claim, and
its invariants are written to **FAIL if the City publishes the missing schools** —
the outcome the request asks for. ⚠️ **It establishes only that the portal exposed
no such dataset on the run date, not that the City holds none internally.** Do
not let the message imply otherwise.

---

## Draft message

> **To:** City of Edmonton Open Data
> **Subject:** Dataset request — school locations for operators not currently published
>
> Hello,
>
> Edmonton publishes school locations for two of the city's school authorities —
> *Edmonton Public School Board (EPSB) School Locations* (`996c-239n`, 225
> records) and *Edmonton Catholic Schools* (`gfxq-u8uu`, 97 records). Both are
> clean and easy to work with, and I use them regularly.
>
> **The request:** a comparable point set for the remaining operators —
> independent and private schools, charter schools, and the francophone
> authority (Conseil scolaire Centre-Nord).
>
> **Why it matters for users of the data.** Any analysis that asks "how far is
> this address from a school" is currently answering "how far is it from a
> public or Catholic school," which is a different question. The gap is not
> visible in the data: the two published sets look complete on their own terms,
> so the natural way to use them silently under-counts schools — and it does so
> unevenly across the city, since the missing operators are not distributed the
> same way the published ones are. A user has no signal that anything is absent.
>
> I looked for these before asking. Catalogue searches for private, charter,
> independent and francophone schools return no location dataset for any of
> those operators, so as far as I can tell the portal does not currently carry
> one. If I have missed an existing source, I would genuinely rather be pointed
> at it than have new data created.
>
> **A minimal version would be sufficient.** Name, operator or authority, and a
> point or civic address per school would resolve it. Matching the shape of the
> two existing datasets would be ideal, since anything built on those would then
> accept it directly.
>
> I appreciate that these operators are not City bodies and that the City may
> not hold or be able to publish their locations — if that is the situation, and
> if you know whether the data sits with the province or with the authorities
> themselves, that would be a useful answer in itself.
>
> Working notes are here, if useful:
> https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/school-coverage-gap.html
>
> Thank you for the work that goes into the portal.
>
> [name / contact]

---

## Notes for whoever sends this

- **The last paragraph is doing real work — keep it.** These are not City
  schools, and the City may have no standing to publish their locations. Asking
  in a way that accepts "we can't, but here's who can" makes a useful reply
  possible instead of an awkward one.
- **Lead by naming what they already publish, and say it's good.** This is the
  only one of the four reports that asks for new work rather than a correction;
  the two existing datasets are the evidence the ask is reasonable.
- **Do not claim the City holds this data.** We know only that the portal does
  not expose it. The notebook is explicit about this and the message must stay
  inside it.
- **Do not offer to supply a hand-built list.** A name-matched set with no
  self-check is the `T8` hand-enumeration shape and is not the answer
  (`DATA_ISSUES.md` §5) — offering it invites exactly the wrong fix.
- **Re-run the catalogue searches before sending.** The claim is an absence, and
  an absence is the one kind of claim that can be falsified between writing and
  sending. `notebooks/standalone/school_coverage_gap.py`.

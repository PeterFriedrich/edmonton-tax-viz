# DRAFT — Bug report: `24uj-dj8v` puts a LIST of neighbourhoods in a one-neighbourhood field

**Status: DRAFT, NOT SENT.** Written 2026-09-17. Peter's to send, edit or discard.

**Channel:** `opendata@edmonton.ca` (portal footer, read 2026-08-25).

⚠️ **Send separately** from the `q7d6-ambg` coverage-year report and the
`qi6a-xuwt` dropout report. Different dataset, different defect.

---

## ⚠️ This report's ask CHANGED on 2026-09-17 — read this before sending

`DATA_ISSUES.md` §6 previously said to ask for *"the numeric `neighbourhood_id`
the City already publishes on `fire_response` and both Property CSVs, which
would remove the name join from this dataset entirely."*

**That ask was wrong, and it would have been checkably wrong to the person
receiving it.** The dataset **already carries** a numeric id —
`neighbourhood_numberr` — and it is **comma-joined on exactly the same rows**.
Asking Edmonton to publish a field they already publish is the kind of error
that costs a report its credibility.

**The corrected ask** is that the *existing* id be made single-valued, with the
genuine multi-neighbourhood case given somewhere to go. See "What to ask for"
below.

---

## Claims, measured live 2026-09-17

| Claim | Status |
|---|---|
| `neighbourhood` holds comma-joined lists | ✅ **547 of 246,402 rows (0.22%)**, measured live. Reproduces the 2026-09-14 in-repo figure of 546 exactly in shape; the dataset refreshed 2026-09-17. |
| `neighbourhood_numberr` is comma-joined on the same rows | ✅ **VERIFIED on all 547** — asserted as a notebook invariant |
| Every affected row carries an id | ✅ **0 rows with no id**, so the id-based classification covers the whole defect rather than a subset |
| Three distinct causes are present | ✅ **240 genuine straddles / 238 renames / 69 duplications** |
| Retired ids are absent from `65fr-66s6` | ✅ `1150` (OLIVER) and `2310` (GORMAN INDUSTRIAL WEST) are not in the 407-row boundary file; `1151` (WÎHKWÊNTÔWIN, effective 2024-10-30) is |
| The field name carries a typo | ✅ `numberr`, doubled final `r` |
| Evidence page | ✅ `/notebooks/permit-neighbourhood-list.html`, **5 of 5 invariants pass**, executed cold-cache 2026-09-17 |

**The classification rule** (this is the report's actual contribution — names
alone cannot do this):

| pattern in `neighbourhood_numberr` | meaning | rows | units_added |
|---|---|---|---|
| same id repeated (`5642, 5642`) | duplication | 69 | 383 |
| one retired + one live (`1150, 1151`) | a rename | 238 | 1,252 |
| two or more live ids (`3080, 4350`) | a genuine straddle | 240 | 537 |

⚠️ **Do not present those unit figures as "units lost".** They are the
`units_added` sitting on list-valued rows in the raw dataset. What our own
published window lost is a different measurement against a different denominator
(`DATA_ISSUES.md` §6). Conflating them would overstate the case.

---

## What we checked and did NOT find — keep this out of the message

Investigating this turned up **5,252 non-comma rows carrying a retired id**
(`CHAPPELLE AREA` 5,175 rows, `OLIVER` 75, `LEWIS FARMS INDUSTRIAL` 2). That
looked like a second and larger defect. **It is not one for us:**
`src/load_assessment.py`'s `NAME_CORRECTIONS` already maps all three, so nothing
is dropped on our side — and those three are exactly the three non-comma names
`DATA_ISSUES.md` §6 already records as missing the boundary file, found
independently from the id direction.

**It is arguably still a data-quality observation for the City** (a retired
designation persisting as the published value on 5,175 rows), but it is a
*different* claim from the list-valued field, it has no evidence page, and
bundling an unevidenced second complaint into a well-evidenced first one weakens
both. **Left out deliberately.** If it is ever worth raising, it needs its own
measurement and its own page.

---

## Draft message

> **To:** City of Edmonton Open Data
> **Subject:** Data quality — neighbourhood field holds multiple values on General Building Permits (`24uj-dj8v`)
>
> Hello,
>
> I use the *General Building Permits* data (resource `24uj-dj8v`) for
> neighbourhood-level analysis, and I've run into something in the
> neighbourhood fields that I think is worth flagging.
>
> **What I'm seeing.** On about 547 rows — roughly 0.22% of the dataset — the
> `neighbourhood` field holds a comma-joined *list* of neighbourhood names
> rather than a single name, for example `OLIVER, WÎHKWÊNTÔWIN`,
> `RITCHIE, RITCHIE` and `CANOSSA, NORWESTER INDUSTRIAL`. The companion field
> `neighbourhood_numberr` is comma-joined on the same rows, in the same order,
> so using the numeric id instead doesn't avoid it.
>
> **Why it's awkward for a consumer.** Joining either field to the
> neighbourhood boundary data (`65fr-66s6`) silently drops those rows — the
> join simply finds no match, with nothing to indicate that anything went
> missing. The share is small citywide, but the affected rows cluster in a few
> neighbourhoods, so a per-neighbourhood total can be off by a large fraction
> for a specific neighbourhood while the citywide figure looks fine.
>
> **Three different situations appear to be sharing one field**, which may
> matter for how you'd want to fix it:
>
> - a neighbourhood **rename** carrying both the old and new name — the
>   `OLIVER, WÎHKWÊNTÔWIN` case;
> - the **same neighbourhood written twice**, such as `RITCHIE, RITCHIE`, which
>   carries no extra information;
> - a permit that **genuinely spans two or more neighbourhoods**, such as
>   `CANOSSA, NORWESTER INDUSTRIAL` — real information, in a field with no room
>   for it.
>
> **The id field already distinguishes these**, which I thought was worth
> passing on. Checking each id against the boundary data separates the cases
> mechanically: two identical ids means duplication; one retired id plus one
> current id means a rename (`1150` is no longer in the boundary file, `1151`
> is); two current ids means a real multi-neighbourhood permit. On the rows I
> looked at this classified every one of them, with none left ambiguous.
>
> **What would help most**, in rough order:
>
> 1. Making `neighbourhood_numberr` single-valued, and the name field with it.
>    For the rename and duplication cases this looks unambiguous.
> 2. Somewhere for a genuine multi-neighbourhood permit to go — either one row
>    per neighbourhood, or a separate `additional_neighbourhoods` field.
> 3. A very minor one: the field name `neighbourhood_numberr` has a doubled `r`.
>    Harmless, but hard for a consumer to work around without hard-coding the
>    misspelling, and cheap to correct while the field is being looked at.
>
> Full working, with the row counts and the classification, is here:
> https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/permit-neighbourhood-list.html
>
> If the list-valued rows are intentional and I've misread what the field is
> meant to represent, I'd be glad to know — that would be useful in itself.
>
> Thank you for your time.
>
> [name / contact]

---

## Notes for whoever sends this

- ⚠️ **Do not repeat the old "publish a numeric id" ask.** It is already
  published. See the warning at the top — this is the one substantive way this
  draft departs from what `DATA_ISSUES.md` §6 said before 2026-09-17.
- **The typo is listed third and called minor on purpose.** Leading with it, or
  giving it equal weight, makes the whole report read as pedantry.
- **The classification rule is the part worth their attention** — it turns
  "your field is messy" into "here is a mechanical way to tell the three cases
  apart," which is a much easier thing to act on.
- **Don't quote the `units_added` figures as units lost.** See the warning above
  the table.
- **Keep the retired-id observation out** unless it gets its own evidence page.
- **Re-run the notebook before sending.** This dataset refreshes often — it
  updated on 2026-09-17, the day this was written — so the 547 will drift.
  ⚠️ **If the field has been made single-valued, do not send:** mark the issue
  FIXED in `DATA_ISSUES.md` and the report RESOLVED in `EVIDENCE_NOTEBOOKS.md`.
  The notebook's first three invariants are written to fail on that outcome, so
  a re-run tells you directly.

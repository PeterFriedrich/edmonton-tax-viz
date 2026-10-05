# Findings — Services ranked panel + Development zero-fill (queue item 14)

**Run:** 2026-10-05, S215, Opus 5.5, `xhigh`. ⚠️ Same model family as the
builder (#575, #580).
**Target:** `docs/AUDIT_LEDGER.md` queue item 14, the new public claims:
- *"Nth highest of 406"* (#580 `svcRank`, including ties);
- *"a utility charge paid to EPCOR, not a City cost"* (#580);
- the 44 Development hoods zero-filled by inference (#575 `devHistoryFor`).

**Instrument:** `edmonton-audit` decision stack.
- The served `neighbourhood_value_per_acre.geojson` and `dev_history.json`
  (CI refresh 2026-09-28).
- `data/raw/building_permits.csv` (local pull 2026-09-03; the unmatched names
  in question are all pre-2021, so vintage does not move them), filtered with
  `load_permits`' own vocabulary sets.
- A point-in-polygon of geocoded permits against the zero-filled hoods.
- A headless render of both builds calling `openTemporal` per hood; the
  quoted panel text below is what the browser printed.

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Should Services show ranked dollars, and Development speak for permit-less hoods? | **SOUND.** Peter's calls (DECISIONS 2026-09-24 ×2); not re-opened. |
| L1a | Is the rank right? | **SOUND.** Competition ranking (`count(x > v) + 1`) over non-null values; ordinal suffixes correct (11–13 → th). Public rows (roads family): n = 406, largest tie 8. |
| L1b | Is the EPCOR sentence right? | **SOUND, full build only** (storm/water are not `pub`). It restates `SPEC_utilities.md` "Money-flow honesty". |
| L1c | Is the zero-fill's "every one of them zero" right? | **SOUND in effect on the public build; the guard behind it is BLIND — F1.** Every geocoded permit that co-names a zero-filled public hood lies in the *other* hood. The one false "none" is on the full build (industrial, set-aside land). |
| L2 | Does each panel say only what its number supports? | **F2 (full build only):** a $0 water charge that is out of scope, not measured, is ranked and called a utility charge. |

## F1 — the zero-fill's confirmation reads the join it is meant to check

`devHistoryFor` zero-fills a hood with no `dev_history.json` row only when the
served `*_long` column is exactly 0. Its comment says this is *"so a name
mismatch still shows as missing rather than as 'none'"*. But the `_long` column
and `dev_history.json` come from the **same** permit→hood name join
(`load_permits` + `PERMIT_NAME_CORRECTIONS`). A permit whose `neighbourhood` is
one of the 15 deliberately unmatched multi-hood lists (565 units,
`load_permits.py` docstring, `DATA_ISSUES.md` issue 6) adds to **neither**, so
both read 0 and the check passes. It catches a mismatch between the two
*exports*. It does not catch a mismatch between the permits and the boundaries,
and that is the mismatch this dataset actually has.

**Measured on the lens's own rows** (new construction, 2009–2025). 3 of the 44
zero-filled hoods are named in an unmatched list:

| Hood | Build / sub-metric | Lens rows co-naming it | Geocoded rows fall in | Panel prints |
|---|---|---|---|---|
| HERITAGE VALLEY AREA (developed) | **public** / units | 26 permits, 46 units, 2010–11: `ALLARD, HERITAGE VALLEY AREA` 18 (0 geocoded); `CHAPPELLE AREA, HERITAGE VALLEY AREA` 8 (5 geocoded) | **CHAPPELLE, 5 of 5** | *"No new homes permitted here, 2009–2025 / 17 years of permit records, every one of them zero"* |
| ANTHONY HENDAY HORSE HILL (set-aside) | public / units | 1 permit, 2013 (`GORMAN, …`) | outside every polygon | same |
| RIVER VALLEY GLENORA (set-aside) | full / industrial | 1 industrial permit, 2010 (`RIVER VALLEY VICTORIA, RIVER VALLEY GLENORA`) | **RIVER VALLEY GLENORA** | *"No new industrial permits here … every one of them zero"* |

**So the public sentence holds on the evidence there is.** Every geocoded
co-named row lies in the other hood. That matches the containing-area-plus-hood
pattern `PILOT SOUND AREA WEST PORTION, MCCONACHIE` was corrected for. The 18
Allard rows are not geocoded and stay unknown. **The one false "none" is River
Valley Glenora's industrial row** (full build, set-aside land): a 2010
industrial permit geocoded inside that polygon.

**The finding is the guard, not the sentence.** The comment claims a protection
the code does not have, and it held here only because these list names happen
to mean "containing area, then the actual hood". A future list row naming two
peer hoods would print "every one of them zero" for both.

**Class:** `guard-blind` (an identity check: both sides read one join).
**Reach:** public none found. Full build: 1 hood, 1 permit, set-aside.

**Remedy (smallest first; Peter):**
1. Correct the comment to say what the check catches (an export mismatch) and
   what it cannot (an unmatched permit name).
2. **`CHAPPELLE AREA, HERITAGE VALLEY AREA` → CHAPPELLE** joins
   `PERMIT_NAME_CORRECTIONS` on the same footing as the Pilot Sound entry, with
   the 5-of-5 geocode as its evidence. That moves 8 permits / 28 units onto
   Chappelle. Its long-window total changes, so the change is Peter's.
3. Only if the open 15-name decision does not cover it: `export_dev_history`
   writes the hoods named in unmatched permit names, and `devHistoryFor` does not
   zero-fill those (data contract → proposal).

## F2 — full build: a $0 water charge that is out of scope, ranked as a charge

The water model is residential-only (DECISIONS 2026-07-06). 55 hoods carry
`water_charge_per_acre = 0`, 43 of them developed, mostly industrial and
commercial. The panel prints, for ALBERTA PARK INDUSTRIAL:

> WATER/SEWER · $0 modelled water+sewer / acre / yr (fixed $0) · **352nd highest
> of 406 neighbourhoods** · **A utility charge paid to EPCOR, not a City cost.**
> · Modelled, not billed.

The layer blurb discloses *"commercial properties are not modelled"*; the panel
does not. The $0 is "not modelled", not "charged nothing". The rank then places
an industrial park below every hood with any modelled residential charge. `svcRank`'s
comment says it ranks *"over the hoods that HAVE the column … so a service with
partial coverage reports a denominator it can support"*. The water column is
zero-filled, not null, outside its scope, so that protection never engages.

**Class:** `render`; **reach:** full build only.
**Remedy (Peter):** either null the column where a hood has no in-scope
residential rows (pipeline; check the map's colouring of the same 55 first), or
have the panel say *"Commercial properties are not modelled; no residential
water charge here"* with no rank when the hood has no in-scope rows.

## Observations (not findings)

- **Ranks include set-aside land; the colour scale does not.** All 48
  set-aside hoods are in every rank's denominator, and the public scale
  (`index.html` ~2031) filters them out. "Of 406 neighbourhoods" is literally
  true, and on the public roads rows no set-aside hood is in the top 10. On the
  full build's bike rows, 5 of the top 10 are set-aside (river-valley trails),
  so a developed hood can read "6th highest" behind five parks. Worth knowing if
  bike goes public.
- **Ties are competition-ranked and unannounced.** Every hood at 0 on bike
  reads "337th highest of 406" alongside 69 others (full only). The public
  maximum tie is 8 (road length 0). Not wrong, and not a defect at that size.

## What this run got wrong

- **My first cut of F1 counted raw permit rows of every type.** It said
  "EVERGREEN 39, HERITAGE VALLEY AREA 45 …, 11 hoods". Filtered to the lens's
  own rows (new construction, residential/industrial building types,
  2009–2025), it is **3 hoods**. The other eight drop out on the lens's own
  filters (work type, building type or window); which filter removes each was
  not broken down. Had the
  unfiltered count been written up, F1 would have overstated its reach almost
  fourfold.
- **I assumed the industrial sub-metric was public** and wrote the probe to
  click it on the public build; the click timed out because `offered()` hides
  it there. The River Valley Glenora half of F1 is full-only.
- **I drafted F1 as a public defect, then reversed it.** The first draft said
  the Heritage Valley rows *"are not geocoded"*, so the claim *"rests on an
  absence"*. I had checked only whether any geocoded row fell **inside** the
  zero-filled polygons, and none did. I never asked where the geocoded rows
  **were**. 8 of the 16 raw `CHAPPELLE AREA, HERITAGE VALLEY AREA` rows carry
  coordinates, and all 5 that are lens rows sit in Chappelle. "No point inside"
  had been read as "no points", which is the confident-negative shape again,
  caught before publishing. F1's public half is now **supported**, not
  overstated.

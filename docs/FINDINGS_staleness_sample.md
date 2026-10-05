# Findings — sampling staleness passes 7–8 (queue item 9)

**Run:** 2026-10-05, S215, Opus 5.5, `xhigh`. ⚠️ Same model family as the
passes. **Target:** `docs/STALENESS_LEDGER.md` rows 21–35 (passes 7–8, #498,
#499, #514). The brief: *"sample the verdicts, don't re-run the pass"*. One
pass-7 verdict was reversed within a day (row 25 → row 35).
**Instrument:** a re-check of 7 of the 15 rows against the tree and the live
sources today. The sample was chosen to cover each verdict kind (ACCURATE,
ACCURATE + caveat, CORRECTED, REVERSED) and both kinds of claim (code,
external).

## Verdict: SOUND — 7 of 7 sampled verdicts still hold; one resolved warning still read as live

| Row | Item | Verdict then | Re-checked 2026-10-05 |
|---|---|---|---|
| 21 | T3 `#revcut` does not reach the panel | ACCURATE | ✅ `revenueMix = p => REV_CATEGORIES.filter(c => p[c.col] > 0)…`: takes only `p`, reads no cut. The item is still open. |
| 22 | Retrieval logging | ACCURATE + caveat (Bash reads invisible) | ✅ the verdict held then; the **caveat was resolved 2026-09-21** (`4971a80`, Bash matcher added). Log today: **1,588 Bash / 411 Read entries since 09-21**. `TODO.md` recorded the widening; **this ledger's pass-7 warning paragraph did not**, and still told a reader not to prune until the matcher was widened. Fixed in this PR. |
| 23 | B2 regional mill rates | ACCURATE | ✅ the FIR page carries the workbook. It shows **both** `2026_Tax_Rates.xlsx` and `2026_tax_rates.xlsx`, so the row's *"casing slip"* note was unnecessary: the item's casing is on the page too. |
| 26 | Selective regen | CORRECTED (payoff falsified) | ✅ the verdict stands. Its supporting fact *"GTFS static 93–153 d"* aged today: all five GTFS tables reloaded 2026-10-05 for the fall signup. That is consistent with signup-cadence updates, not a contradiction; the optimisation is still worth little. |
| 27 | B3 industrial context map | CORRECTED (blocker gone) | ✅ `reference.geojson` holds 15 `t="boundary"` features, including the four counties and Industrial Heartland. |
| 33 | Income variable | ACCURATE | ✅ no `income` in `src/*.py`, `web/index.html` or `data/DATA.md`. |
| 35 | A4 re-check | REVERSED (blocker real) | ✅ `filestream.ashx?DocumentId=244141` → **403, `server: cloudflare`**, from this box today. |

## What this run got wrong

- **I went in expecting row 22's caveat to be a live defect.** The ledger
  paragraph reads that way, and I started measuring the log as if the matcher
  were still narrow. The 1,588 Bash entries showed the fix had landed 14 days
  earlier. That is the exact failure the ledger warns about (*"a verdict … belongs
  to a cohort of its own"*), and it came from reading the ledger as current. The
  sample caught it only because it re-measured instead of re-reading.
- **The sample is 7 of 15, chosen to span verdict kinds, not at random**, so
  "7 of 7 hold" is a coverage statement, not a rate. Rows 24, 28–32 and 34 were
  not re-checked.

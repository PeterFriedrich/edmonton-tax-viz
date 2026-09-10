# FINDINGS — the decisions index drifted from its own contract

**Run:** 2026-09-04 (S137) · **Target:** `docs/DECISIONS.md` · **Trigger:** incidental.
Measuring the Fable brief's reading list showed `DECISIONS.md` at **367 KB**, which is not
a size an index should reach.

**Verdict: the file no longer does what its header says it does, and the erosion was
gradual, unremarked, and is not confined to this file.** No decision is wrong; no number
served to the site is affected. This is a documentation-contract finding.

---

## 0. The claim I got wrong first, corrected

My opening read was that the file *"duplicates exactly the rationale its header says it
doesn't."* Measured against the docs each row points to, **that is false**: median 8-gram
overlap is **4%** (mean 6%; only 9 of 231 testable rows exceed 20%). The rows are original
prose, not copy-paste.

⚠️ **But the substantive claim survives in a form that matters more.** Of the distinctive
facts in the Decision column, **98.8% are recoverable elsewhere in the repo** (see §3). It
is *paraphrased* duplication — the same facts, rewritten. **No text-similarity check would
ever flag it, which is why it ran for four months.** The lesson generalizes: a
"duplicates nothing" rule enforced by eye, against prose that is reworded each time, is
not enforced at all.

## 1. The contract, and what holds

`DECISIONS.md`'s own header states it:

> Append-only, one line per locked decision: when, what, **the one-sentence why**
> (including what was rejected), and where the full reasoning lives. This file
> **duplicates no rationale** — it exists so a contributor can find where a decision is
> argued without reading every doc.

| predicate | result | measured |
|---|---|---|
| one line per decision | ✅ **holds** | 247 rows, all single-line |
| pointer to full reasoning | ✅ **holds** | ⚠️ ~~only **3** of 247 rows have an empty pointer~~ — **that 3 was a parse artifact (see §7): the naive splitter reports `L145`/`L146`/`L261`, all of which have FULL pointers. Correct answer: **1** (`L196`), which the old script's `len(c)<3` filter could not see.** |
| **"the one-sentence why"** | ❌ **13%** | 33 of 247 rows are one sentence; median **6**, max **19** |
| **"duplicates no rationale"** | ❌ **violated in substance** | 98.8% of distinctive facts exist elsewhere |

The Decision column alone is **321,920 bytes — 88% of the file.**

## 2. The drift is monotonic, and steep

Median Decision-cell length, by month of the decision:

| month | rows | median chars | max |
|---|---|---|---|
| 2026-05 | 3 | **138** | 149 |
| 2026-06 | 8 | 239 | 276 |
| 2026-07 | 105 | 557 | 2,889 |
| 2026-08 | 111 | 1,629 | 4,322 |
| 2026-09 | 19 | **2,219** | 3,417 |

**16× in four months.** The May rows are exactly what the header describes — one sentence,
one pointer:

> `| 2026-05 (Phase 1) | **Neighbourhood, not parcel, as the unit** — parcel boundary
> polygons are licensed (ADP/AltaLIS), not open data; roll points + boundary polygons are.
> | docs/PARCEL_LEVEL_OPPORTUNITIES.md, data/DATA.md |`

⚠️ **Nothing was ever decided to change this.** There is no `DECISIONS.md` line reopening
the format. It eroded one row at a time, each row individually defensible.

## 3. Sizing the remedy before proposing one

Per the house rule about counting what a fix actually touches: a trim back toward the
contract would **destroy information in 12 of 247 rows**.

Extracting distinctive facts (backticked identifiers, dollar figures, numbers with units)
from every row and testing each against the whole repo with `docs/DECISIONS.md` excluded:

- **1,295 distinctive facts; 16 (1.2%) exist only in `DECISIONS.md`.**
- Of those 16, four are notation artifacts (`styles-abc123.css` is an illustrative
  placeholder; `vintage_report.CHECKS` and `src/load_temporal.publishable_years` are dotted
  references to symbols that do exist). **The true rescue list is ~8 values:**

| row | value found nowhere else |
|---|---|
| L205 (2026-08-07) | `0.06%` |
| L223 (2026-08-11) | `$14,048.73/acre`, `$234,399` |
| L226/L227 (2026-08-12) | `258px`, `272px` |
| L245 (2026-08-22) | `$161.3M` |
| L258 (2026-08-25) | `$88,038,783/yr` |
| L287 (2026-09-01) | `152 ms`, `167 ms`, `319 ms` |

⚠️ **These must be rescued into their owning docs BEFORE any trim, not after.**

### Method corrections (both were mine, both mattered)

⚠️ **My first uniqueness pass reported 24 unique facts. It was inflated by ~50%** — comma
and trailing-punctuation variants defeated a raw substring test, so `$19,729` (in 4 other
files) and `$2,784,219,936` (in 3) read as unique. Re-run with `[,\s$]` stripped, it is 16.

⚠️ **My first corpus build could not have failed.** It excluded `DECISIONS.md` by
`str.replace()` of the whole file against concatenated `git grep` output — which, had the
line ordering differed at all, would have silently left the file inside its own corpus and
scored **every** fact as recoverable. Rebuilt via `git ls-files` with an explicit exclusion
and a falsification probe (the file's own header string must be absent from the corpus).
Same family as the two vacuous checks caught in S135/S136.

## 4. ⚠️ It is not confined to this file

`docs/AUDIT_LEDGER.md` opens with *"Rules (**mirror `DECISIONS.md`**): … one-line verdict +
pointer, **never duplicate findings or rationale here**."*

**Measured: 32 rows, median 1,941 chars, max 5,416, 72 KB.** The same drift, under a header
that names the same rule and points at the same file.

**The pattern is the finding.** Both files are pointer-style indexes whose value is being
small; both grew ~2 KB/row; both did so under an explicit written rule against it. Any
remedy that fixes only `DECISIONS.md` treats the instance and not the cause.

## 5. What is NOT established

- ~~**Whether the connective reasoning is recoverable.**~~ **MEASURED 2026-09-09
  (S152) — see §7. It is recoverable where a row points at a doc, and the DEFECT
  IS THE POINTER COLUMN, not the Decision column.**
- **Whether the contract or the practice should change.** Four months of authors chose the
  long form every time. That is evidence the file has become a genuinely useful decision
  *log*, in which case the honest fix is **rewriting the header to describe what it is**,
  not trimming 322 KB to match a header nobody has followed since June.

## 6. Reproduce

```bash
# contract compliance + the monthly drift table (§1, §2)
.venv/bin/python - <<'PY'
import re, statistics as st
rows=[]
for l in open('docs/DECISIONS.md'):
    if not l.startswith('|') or re.match(r'^\|\s*-{3,}', l): continue
    c=[x.strip() for x in re.split(r'(?<!\\\\)\\|', l.strip().strip('|'))]  # NOT .split('|') — see §7
    if len(c)<3 or c[0].lower()=='when': continue
    rows.append(c)
L=[len(c[1]) for c in rows]
print(len(rows), 'rows; median', int(st.median(L)), 'max', max(L))
PY
```

⚠️ **The splitter above was corrected 2026-09-09** — the original `.split('|')` broke on the five
rows carrying a pipe inside inline code and produced §1's wrong empty-pointer count. **The pointer is the
LAST field**, and a 2-field row (`L196`) has none and must not be silently dropped.

The uniqueness sweep (§3) is the longer script; rebuild the corpus with `git ls-files`,
exclude `docs/DECISIONS.md` **explicitly**, normalize with `re.sub(r'[,\s$]','',s.lower())`,
and **assert the file's own header string is absent from the corpus before trusting any
result** — without that probe the sweep cannot fail.

## 7. §5's open question, measured (2026-09-09, S152)

§5 said the *arguments* were unmeasured and that this decides trim-vs-rewrite. It
does, and the answer points at neither option.

**Read two of the longest rows against the doc they point at.** Both were **fully
recoverable, and the target was RICHER than the row**:

| row | pointer | verdict |
|---|---|---|
| L231 (3,174 ch) institutional consequence tier | `SPEC_revenue.md` "The consequence tier" | the whole argument is there — share-vs-consequence, all three over-selection counter-examples (RIVER VALLEY CAMERON 0 rank/0.02, EVERGREEN $87, U OF A FARM), **plus** the measure-on-the-ramp lesson, the fixed-transform reasoning and the inversion proof the row omits |
| L284 (3,252 ch) Glass cell as a third Detail button | `docs/UI.md` §"Glass cell size as a third Detail button" | Peter's verbatim ask **and all three reasons in the same order**, stated more fully than the row |

⚠️ **A PHRASE-ABSENCE TEST WOULD HAVE ANSWERED THIS BACKWARDS.** *"SHARE decides
the WORDS"* and *"inherits the right gating for free"* appear **nowhere** outside
`DECISIONS.md` — yet both arguments are fully present in the target, paraphrased.
§2's 4% n-gram overlap already predicted this: **the rows duplicate arguments
without duplicating wording, so any grep-based recoverability test is vacuous
here.** This had to be read.

**The at-risk set is the rows with nowhere to point, and it is small:**

⚠️ **THE FIRST THREE COUNTS PUBLISHED HERE WERE WRONG — MY PARSER WAS, AND IT
MANUFACTURED ONE OF THE EXAMPLES.** Corrected 2026-09-09 within the same session.
Rows in this table contain pipes **inside inline code** (`L62`, `L145`, `L146`,
`L196`, `L261`), so a naive `split("|")` scatters the Decision text across extra
fields and reads the WRONG field as the pointer. Successive parses gave **35, then
26, then 22** before the method was pinned down. **The pointer is the LAST field,
and `\|` must not be split on.**

| | first published | correct |
|---|---|---|
| total rows | 271 | **272** |
| no `.md` pointer | 35 | **23** |
| no pointer column at all | 3 (unnamed) | **1 — `L196` only** |
| long (>800 ch) among them | 19 | **18** |

⚠️ **The L146 example was BACKWARDS.** It was offered as a row with *no pointer*
whose reasoning I had located in `PLAN_public_release.md` — **the row already
pointed at `docs/PLAN_public_release.md` §2a and `docs/CONTROLS_MATRIX.md` §2.**
I was rediscovering what the row said. **Same family as §3's own two method
corrections and the vacuous checks of S135/S136: the instrument was broken in the
direction that confirmed the hypothesis.** `L145` and `L146` both have full
pointers; only `L196` (2026-08-04, the hand-dispatched refresh) genuinely has no
pointer column.

- **The surviving example holds:** `L153` (CSS extraction) points only at code,
  and its story is told in `UI.md`, `STACK.md`, `TOKEN_EFFICIENCY.md` and 7 more.
  **Evidence strength: phrase-presence only, not read end-to-end like L231/L284 —
  so 23 is an upper bound on rows whose reasoning is genuinely homeless.**
- ✅ **§1's "247 rows" is NOT a casualty — that one is real growth.** At the
  commit that added this doc (`0438954`, 2026-09-04) the corrected parser counts
  **248**; the file has since grown to **272 rows / 412 KB**. The 1-row gap is
  `L196`, which the old script drops.
- ⚠️ **§3's fact counts (1,295 facts / 16 unique) were NOT re-derived** and its
  sweep reads the same columns. Re-run them with the corrected splitter before
  acting on the trim's blast radius.

**So a THIRD option exists, and it is right under either of §5's two:** complete
the **pointer** column on the 23 no-`.md` rows (the 18 long ones first).
✅ **DONE 2026-09-09 (S152) — all 272 rows now carry a doc pointer, 0 remaining.**
Method: match each row to a doc **section heading**, preferring a heading carrying
the row's own date (`UI.md`'s sections are dated), then confirm the row's key
symbol appears in that doc. ⚠️ **Symbol-absence did NOT refute a candidate** —
per this section's own finding the docs paraphrase, so 8 of 23 landed on a doc
that never names the symbol (`RIVER_COLOR` appears only in the generated
`CODEMAP.md`); those were placed on heading semantics and re-checked by hand.
**`scripts/check_doc_citations.py` verified all 23 additions resolve** (guard OK
at its 2-warning baseline), which is the property the whole exercise was for. It is
append-only — which is what the file's own header says it is — non-destructive,
reversible, and it converts recoverability from luck into a property of the file.
It is also the **prerequisite a trim already needs**, so it is not a detour: after
it, the trim's blast radius is re-measurable and the ~8 orphaned values in §3 are
the only true rescues left.

**What is still NOT established:** whether the long form should be *blessed*
(§5's second bullet stands — four months of authors chose it every time). This
measurement says the long rows are **redundant**, not that they are **harmful**;
the cost is paid only by sessions that load the file, and §3's house rule about
sizing a remedy applies to the header rewrite too.

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
| pointer to full reasoning | ✅ **holds** | only **3** of 247 rows have an empty pointer |
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
    c=[x.strip() for x in l.strip().strip('|').split('|')]
    if len(c)<3 or c[0].lower()=='when': continue
    rows.append(c)
L=[len(c[1]) for c in rows]
print(len(rows), 'rows; median', int(st.median(L)), 'max', max(L))
PY
```

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

- **271 rows. 35 carry no `.md` pointer** (code-only or empty); **3 carry no
  pointer at all**; **19 of the 35 are long (>800 ch)** — July 5, Aug 10, Sep 4.
- ⚠️ **But two of those 19 spot-checked have their reasoning in a doc anyway,
  just unnamed:** L153 (CSS extraction) is told in `UI.md`, `STACK.md`,
  `TOKEN_EFFICIENCY.md` and 7 more; L146 (public build ships at two views —
  **no pointer at all**) is in `PLAN_public_release.md` and `CONTROLS_MATRIX.md`,
  Peter's *"2 views is fine"* quote included. **Evidence strength: these two are
  phrase-presence only, not read end-to-end like L231/L284 — the at-risk count
  is an upper bound of 19, probably much lower.**

**So a THIRD option exists, and it is right under either of §5's two:** complete
the **pointer** column on the 35 no-`.md` rows (the 19 long ones first). It is
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

# FINDINGS — is the modelled levy a fair "what properties pay the City"?

**Run:** 2026-11-10 (S244), **Fable 5.2** (`claude-fable-5-2`), from
`docs/FABLE_AUDIT_levy_as_revenue.md`. The investigation it challenges
(2026-08-25) and every weekly sizing since were Opus.

**Scope:** the numerator of every public Money metric and of the Ratio view,
the exempt-share bands, and the public sentences about them. Denominators, the
roads cost side and full-build lenses are out. No new exemption data exists and
no remedy here needs any.

**Every claim is tagged.** *(measured)* = computed this session from a fresh
2026-11-10 pull of the roll (`q7d6-ambg`, 439,825 rows) run through
`load_assessment` and `apply_tax_rates`, joined to `data/raw/zoning.geojson`
(2026-09-03 pull), and from the served
`web/data/neighbourhood_value_per_acre.geojson` (2026-11-09 refresh; 406
neighbourhoods, 48 set-aside, 358 published). *(read)* = taken from a repo
file or the code, not re-derived. The FIR figures are *(read)* from
`data/fir_tax_base.json`; the province's file was not re-fetched.

⚠️ **One reconciliation limit.** My zoning is nine weeks older than the served
file's. Citywide the exempt-candidate share agrees (8.03% mine, 8.05% served),
and 402 of 406 hoods agree to 0.0001. Four differ by 0.015–0.07 (Meyokumin
0.147 served vs 0.076, Mattson, Eaux Claires, Aster; none near the 0.25 gate).
Per-hood totals below use the served share; **per-cut shares are mine** and
carry that tolerance.

**Headline.** No level is UNSOUND. The model reads **+$282.0M, +11.2%** above
the levy the City filed for 2026, and the direction is not in doubt for the
aggregate: the model is over. "Pay" is true only as "at the City's published
rates, with nothing removed for exemption". **The app never states the size of
that gap, while a notebook published on the same site already calls it
"$14.95B on the roll that Edmonton does not tax"** (§0.4). **One set of
shipped numbers is wrong, not merely caveated:** the band, the caveat
percentage and the printed range on the Residential and Non-residential cuts
are computed from the total-levy share (§4, L2).

## 0. The hinge and the contradiction

### 0.1 The served levy is assessment × mill rate on every roll parcel

*(read, `src/apply_tax_rates.py`)* `levy = assessed value × Σ slot (pct/100) ×
(rate[class]/1000)`, municipal rate only. The only rate-0 class is
`NONRES MUNICIPAL/RES EDUCATION`. An unmapped class label is a hard error.

*(measured)* An independent loop over the raw CSV gives **$2,791,060,799**, the
pipeline's figure to the dollar, and the served file sums to $2,791,060,264.
What leaves the numerator:

| Removed | Rows | Assessed | Why |
|---|---|---|---|
| Zero-assessed rows | 54 of 439,825 | $0 | `load_assessment` drops null/zero value (28 on `RS`, 12 on `AG`; 3 on candidate zones) |
| Rate-0 slices | 3 | $7,602,150 | the exempt class label, 0.003% of the $239.57B roll |

So the hinge holds: nothing is removed for exemption except three slices.

*(read)* `data/fir_tax_base.json` 2026 holds a levy of **$2,509,075,991** on
$224.20B. It is the province's early `tax_rates.xlsx` release, fetched
2026-08-25: **a bylaw-time figure, fixed for the year.**

### 0.2 The gap today

*(measured)*

| Class | Roll (ours) | FIR | Gap, assessed | Gap, levy | On 08-25 |
|---|---|---|---|---|---|
| Residential | $162.938B | $160.373B | +$2.565B, **+1.6%** | +$19.9M | +1.2%, $1.90B |
| Other residential | $23.601B | $19.017B | +$4.583B, **+24.1%** | +$36.1M | $4.00B |
| Non-residential | $52.947B | $43.986B | +$8.961B, **+20.4%** | +$226.0M | +20.6%, $9.08B |
| **Total levy** | **$2,791.1M** | **$2,509.1M** | | **+$282.0M, +11.2%** | +$275.1M, +11.0% |

⚠️ **The two residential gaps grow through the year for a reason that is not
exemption.** Between the 2026-09-03 raw pull and today the roll gained $0.648B
of residential and $0.589B of other-residential assessment (294 new accounts,
2,082 changed) while non-residential moved −$0.027B. The FIR side does not
move. *(measured; the mechanism, in-year supplementary assessment, is
inferred.)* So part of the +1.6% and of the apartment gap is growth, not
exemption, and it will keep widening until the January roll.

*(measured)* FIR's "Other" bucket implies a rate of 8.2872, not the 8.2064
other-residential rate. The $1.54M difference is what **$90M** at the
non-residential rate would add, and the roll holds **$79.6M** of derelict
residential, which this pipeline bills at that rate. So "Other" is very likely
other residential plus derelict residential *(inferred)*. It moves $0.08B
between two rows of the table and changes no conclusion.

### 0.3 The contradiction: absent, or on the roll and billed?

Both, measured:

| | Parcels | Dollars | Acres |
|---|---|---|---|
| **On the roll and billed**, exempt-candidate zoning (`AJ UF UI PU PS`) | **3,332** | **$9.359B assessed, $224.2M levy** (8.03% of total, 16.4% of non-residential) | 13,667 (polygons holding ≥1 account) |
| **Absent**: candidate-zone polygons with no roll account | 569 polygons, 0 accounts | **$0, in our number and in FIR's** | 2,213 (13.9% of candidate acres) |

By zone, on the roll: `PS` 1,091 parcels / $87.7M; `AJ` 340 / $62.5M; `UF` 758
/ $49.2M; `UI` 39 / $16.4M; `PU` 1,104 / $8.3M.

**The reader of the site is closer to A1/A2 ("counted as paid"), and in
dollars entirely so.** Absent land puts nothing on the map and nothing in the
gap. Every dollar of the +11.2% is on a parcel that is on the roll.

*(measured)* Non-residential assessment on candidate zoning is **$8.667B,
96.7% of the $8.961B non-residential gap.** Read the other way: closing the gap
by exemption needs essentially **all** candidate-zoned non-residential
assessment to be untaxed. What is left over, $0.294B, is 0.66% of the $44.28B
ordinary non-residential base.

*(read)* `docs/FINDINGS_exempt_institutional.md` defines its measure as
institutional zoning *minus the footprint of roll accounts*, and calls the
on-roll land "taxed" and "taxable" throughout (e.g. "U of A $2.242B taxable on
47 accounts"). Its 2026-08-07 correction fixed the opening sentence only. The
retracted premise, **on the roll = taxed**, survives in the method's labels,
and FIR contradicts it for about $8.7B.

### 0.4 A third voice the brief did not list: the published notebook

*(read, `web/notebooks/exemption-uncertainty.html`, last run 2026-09-23; found
while checking a claim, not in the brief's §2 list.)* The project already
publishes the FIR comparison. The notebook says the filed base is the roll
minus "property the City assesses but does not tax", sizes it at **$14.95B**
("what the roll says we could tax, against what Edmonton says it did tax"),
and its §7 lists what it does not claim: no specific parcel, and that timing,
appeals and supplementary assessments are in the gap too.
`evidence-recheck.yml` re-runs it monthly.

So the brief's "the FIR comparison exists only as a TODO item" is not right,
and the contradiction has three sides, two of them public on one site:

| Where | What it says about on-roll institutional land |
|---|---|
| The app's landing sentence and blurbs | properties **pay** this |
| `/notebooks/exemption-uncertainty.html` | about $15B is assessed and **not taxed** |
| Tooltip caveat, mix note (locked 2026-08-08/15) | **not known** which way |

The notebook is linked from `web/notebooks/index.html` only. Nothing in
`web/index.html` or the verified pages points to it *(measured: no
`notebooks/` link in either)*. It gives assessed dollars, not what the gap
does to the map: the +11.2% is in `TODO.md` only.

## 1. Verdicts

| Level | Verdict | In one line |
|---|---|---|
| **L0** "pay" on a modelled levy | **CONDITIONAL** | True as "at published rates, nothing removed for exemption". As a bare "pay" it asserts for the whole map what the 2026-08-08 lock forbids for one number |
| **L1** the unflagged residual | **CONDITIONAL** | Residential is sound (+1.6%). Half the candidate levy, **$111.1M, sits in 295 published hoods with no flag**; 46 of them are 10–25% candidate |
| **L2** the bands | **CONDITIONAL** | Right on Total (6 hoods). **Wrong on both split cuts**: 16 of 20 Residential caveats are false, 142 Non-residential hoods that qualify get none, and printed range ends are off by up to 28× |
| **L3** communication | **CONDITIONAL** | About says "modelled, not billed"; the landing says "pay", one panel says "collected", and the published notebook says "does not tax". The app never gives the 11% |
| **L4** FIR as a standing check | **CONDITIONAL** | Right instrument for the aggregate, if it is per class, alarms on the non-residential residual and not the total, and holds on a year mismatch |

## 2. L0 — can a modelled levy carry "what properties pay the City"?

**Verdict: CONDITIONAL.** The claim the data supports is *would be billed at
the City's published rates*. For about 90% of the dollars that is also what is
levied, as far as FIR can tell. For the rest it is not.

- *(measured)* The City filed $2,509.1M; the map adds to $2,791.1M.
- *(read)* The About panel already says the true thing: "Revenue is modelled,
  not billed … not what any owner was charged." The landing sentence says the
  opposite verb about the same number.
- *(read, DECISIONS 2026-08-08)* The $125.4M figure is locked as "gross
  modelled", never revenue lost, direction unknown. **The headline is not held
  to that standard.** It takes a direction (paid in full) for every parcel. The
  lock stops one number from assuming *exempt*; nothing stops the map from
  assuming *paid*.
- ⚠️ **"Direction unknown" is itself stale for the aggregate.** It was locked
  17 days before the FIR anchor was found. Per parcel it is still unknown. For
  the city it is known: over. The TODO item and the published notebook (§0.4)
  say so; the tooltip caveat, the mix note and `02_methods` do not.
- *(measured)* What survives untouched: Downtown is #1 at either endpoint
  ($256,242 → $242,266 per acre), and Summerlea, Wîhkwêntôwin and Garneau
  barely move. The top of the ranking is not an artefact of exemption.

**Sharpest argument against this verdict (that it should be SOUND):** zone
coincidence is not parcel proof. The FIR file is an early release, FIR's
buckets are mapped by inference (§0.2), and other causes (how the City files
revitalization-levy areas, annexed land, appeals) were never ruled out. A
$8.667B / $8.961B match could be two unrelated numbers. *I do not think so:
the match is to 3.3% on a base of $53B and the same five zones carry it. But
it is inference.* That Alberta exempts hospitals, universities, schools and
Crown or municipal property is my recollection of the Municipal Government
Act, not verified this session.

**What would flip it.** To SOUND: per-parcel exemption status showing most
candidate-zoned accounts are taxed, or the province's final 2026 return
reporting taxable non-residential assessment within ~2% of the roll. To
UNSOUND: evidence the excess is not concentrated, for example the apartment gap
sitting in the top-ranked residential hoods.

## 3. L1 — is the residual small enough to ignore where it isn't flagged?

**Verdict: CONDITIONAL.** Yes for residential. Not everywhere for
non-residential, and the reader is never told the general fact.

Where the $282.0M excess sits *(measured)*:

| Part | Levy | Locatable? | Flag a reader sees |
|---|---|---|---|
| Non-res on candidate zoning (all classes $224.2M; non-res $218.6M) | ≈$218.6M | by zone | see next table |
| Non-res outside the five zones | ≈$7.4M ($0.294B) | no | none; 0.66% of base, ignorable |
| Other residential (apartments) off candidate zoning | ≈$33.4M ($4.073B, 88.9% of that gap) | **no** | none |
| Residential | $19.9M | no | none; +1.6%, partly in-year growth |

The $224.2M of candidate levy, by what the hood shows *(measured, served
share, Total cut)*:

| Tier | Hoods | Candidate levy |
|---|---|---|
| Banded, translucent, range printed | **6** | $71.4M |
| Caveat line in the tooltip, solid prism | **15** | $40.0M |
| **No flag at all** (published) | **295** | **$111.1M** |
| Set-aside (grey; 3 have a share ≥0.25) | 48 | $1.7M |

The brief's "15 hoods as of 2026-08-15" is the caveat tier. It is **21
published hoods** today, 6 of them banded.

**Unflagged hoods** *(measured)*: share 0–5% in 160 hoods ($25.2M); 5–10% in
88 ($51.3M); 10–15% in 27 ($17.7M); 15–20% in 16 ($14.0M); 20–25% in 3 ($2.9M:
Bellevue 24.8%, Baranow 24.3%, Overlanders 21.4%). **46 unflagged hoods are
≥10%, holding $34.6M.** At the exempt endpoint 32 unflagged hoods fall ≥10
ranks, 19 fall ≥20, the largest 45.

**Caveat-only hoods are drawn solid at the levied endpoint**, the one FIR says
is too high. Two are in the top ten:

| Hood | Share | Per acre, levied → exempt | Rank | Candidate levy |
|---|---|---|---|---|
| Spruce Avenue | 43% | $75,624 → $43,117 | 6 → 15 | $9.75M |
| Central McDougall | 54% | $68,879 → $31,963 | 7 → 48 | $10.94M |
| Cromdale | 30% | | 53 → 111 | |
| Heritage Valley Town Centre | 30% | | 82 → 153 | |
| McQueen | 41% | | 151 → 282 | |

They are not banded because both endpoints sit near the $50,000 colour clamp,
so the two prisms draw alike. That is DECISIONS 2026-08-16 working as designed;
this is its measured cost, not a defect.

**Apartments are the part no zone can find.** *(measured)* Off-candidate
other-residential levy is $189.5M. It is ≥25% of total levy in 15 published
hoods (Abbottsfield 46%, Boyle Street 44%, Ermineskin 42%, Inglewood 41%,
Garneau 38%, Wîhkwêntôwin 32%) and ≥10% in 84. If the 17.6% gap were spread
evenly it would be ≥5% of the hood total in 10 hoods and ≥2% in 71; on the
Residential cut ≥5% in 41 and ≥10% in 11. It is not spread evenly, and part of
it is growth (§0.2). ⚠️ The brief's reading, "consistent with use-based
exemptions", is weaker than it was: $0.589B of the $4.58B appeared in ten
weeks.

**Is the banding enough?** For the six worst hoods, yes: University of Alberta
(90%, rank 2 → 181, $47.3M) is translucent and prints a range. Below the gate
the map is silent, and nothing citywide tells a reader that institutional land
is billed at full rate anywhere.

**Sharpest argument against (that it should be SOUND):** an unflagged hood is
overstated by under 25% and usually under 10%, which is the size of other
limits the site accepts without a per-hood flag. A threshold has to sit
somewhere.

**What would flip it.** To SOUND: one public sentence carrying the citywide
size, so the unflagged remainder is disclosed in general. To UNSOUND: the
apartment excess proving concentrated in a few high-ranked hoods.

## 4. L2 — the bands themselves

**Verdict: CONDITIONAL. Sound on Total; wrong on the two split cuts.**

**Total cut** *(measured)*: 6 bands on ground acres and the same 6 on lot
acres (Edmonton Northlands, Tawa, University of Alberta, University of Alberta
Farm, Virginia Park, West Meadowlark Park). The code comment says six. Each is
where the overstatement is.

**`PS`** *(measured)*: the largest of the five zones, $87.7M on 1,091 parcels,
99% non-residential class. It is diffuse (top 20 accounts are 20% of its value;
median $237,500) and spread across suburban hoods (Heritage Valley Town Centre,
Silver Berry, Leger, Secord, Chappelle), which is where school and recreation
sites are *(inferred from location; the roll names no owner)*. Without `PS`
the candidate set would explain 58% of the non-residential gap, not 97%. It
belongs in the set. The tooltip calls all five "institutionally-zoned", which
is loose for parks and utilities but not false.

**Glass** *(measured)*: 1,334 of 34,674 cells are flagged (≥0.25). They hold
8.2% of grid revenue and **99.3% of candidate revenue**. The cell gate works.

**The per-cut defect** *(read: `exemptFrac = p => p.rev_frac_exempt` on every
cut; measured below, my zoning)*:

| | Residential cut | Non-residential cut |
|---|---|---|
| Hoods with a caveat today | 20 | 21 |
| …where the cut's own share is <25% (**false caveat**) | **16** (14 are <5%) | 0 |
| Hoods ≥25% on the cut's own share | 6 | **163** of 356 |
| …with no caveat (**missed**) | 2 (Lambton Industrial, South Edmonton Common; trivial dollars) | **142**, holding $62.6M candidate of $132.9M non-res levy (78 are ≥50%, 9 are ≥90%) |
| Bands today → bands on the cut's share | **2 → 0** | 6 → 9 (adds Hudson, Royal Gardens, Virginia Park) |

Printed range, low end, today vs the cut's own share:

| Cut | Hood | Printed | Correct | |
|---|---|---|---|---|
| Residential | West Meadowlark Park | **$2,567** to $10,342 | $9,631 | residential share is 7%, not 75%; should not band |
| Residential | University of Alberta | **$643** to $6,353 | $3,609 | 43%, not 90%; should not band |
| Non-residential | West Meadowlark Park | **$7,330** to $29,529 | $266 | 99%, not 75% |
| Non-residential | Tawa | **$17,513** to $41,433 | $10,693 | 74%, not 58% |
| Non-residential | Central McDougall | **$26,150** to $56,352 | $19,601 | 65%, not 54% |
| Non-residential | University of Alberta | **$17,405** to $172,048 | $14,438 | |

**These are shipped numbers that are wrong**, on public cuts, and the
"N% of revenue is on institutionally-zoned land" line under them quotes the
total share on a cut where it does not apply. `TODO.md` F1+F2 (S199) already
names the root and counted 165/144 on the Non-residential cut; today 163/142.
What is new here: the printed range ends, the false Residential caveats, and
that both Residential bands are spurious.

**Release-blocking or polish?** Blocking, in one of two forms, Peter's choice:
build `docs/PROPOSAL_per_cut_exempt_share.md` (a data-contract change, already
proposed 2026-09-28), or turn the band, range and caveat off on the split cuts
until it lands. The second is smaller and stops the wrong numbers, but leaves
the Non-residential cut with no per-hood flag.

⚠️ **A per-hood flag cannot carry the Non-residential cut anyway.** 163 of 356
hoods qualify, 46%, and the cut is +20.4% citywide. That is a property of the
cut, and it belongs in the blurb (L3), not in 163 tooltips.

**Sharpest argument against (that it is polish):** the split cuts are
secondary views, the wrong figure is the low end of a range labelled as
uncertain, and the fix has been waiting six weeks without anyone being misled
in a way they reported.

**What would flip it.** To SOUND: the per-cut columns shipped, or the split-cut
bands off. To UNSOUND: nothing short of the Total bands being wrong, and they
are not.

## 5. L3 — communication

**Verdict: CONDITIONAL.** Each sentence, under L0–L2. Statuses are from
`docs/COPY_DECISIONS.md`, **read before proposing**: N1–N6 and P1 are
**applied**, so every change below re-opens a settled row and is Peter's call.
They were settled on jargon ("levy" → "City tax"), not on this question.

| Surface | Wording *(read)* | True as worded? | Smallest change |
|---|---|---|---|
| Landing / loading blurb (N5, applied) | "What each neighbourhood pays the City in property tax, per acre." | Only at published rates. +11.2% citywide | Leave it short; put the qualifier in the Total blurb |
| Total blurb (P1, applied) | "…what each neighbourhood's properties pay the City, divided by its land area." | Same | Add: "at the City's published rates, with tax-exempt property not removed" |
| Residential blurb (P1) | "what houses, condos and apartment buildings pay the City…" | Yes, to +1.6% on houses and condos. Apartments are +24% and unlocatable | None needed |
| **Non-residential blurb (P1, provisional 2026-09-26)** | "what non-residential property (business, industry and institutions) pays the City…" | **Least true sentence on the site.** It names institutions as payers; the cut is +20.4% and 16.4% of it is on candidate zoning | "…(business, industry and institutions) is billed at published rates; exempt institutions are not removed" |
| Split-cut note (P3) | "A subset of Revenue, not all of what the land pays." | Yes | None |
| Ratio blurb (P1 roads) | "City tax per road metre: what each neighbourhood pays the City, divided by…" | Same as Total | Follows the Total blurb |
| **Panel headline (N4, applied)** | "City property tax collected here / $X per acre each year" | **No.** "Collected" is a cash claim; the model does not know billing, let alone collection. Shown on banded hoods too | Drop the verb: "City property tax here" |
| Set-aside ratio note | "The resulting city tax collected is too low for comparison." | Same verb | "The resulting city tax is too low…" |
| Tooltip caveat (locked 2026-08-15) | "N% of revenue is on institutionally-zoned land / the City does not publish which of it is tax-exempt" | True on Total. On the split cuts N is the wrong share (L2) | None on Total |
| Revenue-mix note | "Institutional and public land is on the roll and is counted above at published rates; the City does not publish which of it is tax-exempt." | **Yes. The model sentence for the rest** | None |
| Data & Methods (About) | "Revenue is modelled, not billed … not what any owner was charged." | Yes, and unsized | Add the size: "Citywide it is about 11% above the levy the City reported for 2026, mostly on institutional and public land" |
| `01_money_lens` | "flags tax-exempt rows without removing them" | Literally true, but the flag finds 3 slices ($7.6M). A reader takes it as "exempt rows are identified" | Say how few |
| `02_methods` §3 | "the error it causes runs both ways … not on the roll at all (the Legislature), which understates its neighbourhood" | **No.** Absent land pays nothing, so a paid-tax metric is right about it. This is the direction retracted 2026-08-08 | Delete "which understates its neighbourhood"; say the on-roll side is the only dollar error and the model is over |
| `02_methods` §8 | "some exempt land is billed on the map and some is missing from it" | Yes | None |

*(measured)* **"FIR", "Schedule MR" and "11%" appear nowhere in
`web/index.html` or the verified pages.** The gap is public only in the
evidence notebook (§0.4), in assessed dollars, unlinked from the app. A reader
who finds both pages is told "pay" by one and "does not tax" by the other.
The smallest fix is the About sentence above plus a link to the notebook.

`01_money_lens` and `02_methods` are generated from `notebooks/verified/`,
which the report session owns.

**Sharpest argument against (that the copy is SOUND):** "pay" was chosen on
purpose because "levy" made readers' eyes glaze, the About panel carries the
caveat, and every qualifier added to a first sentence costs readers.

**What would flip it.** To SOUND: the size stated once in the app and "collected"
gone. To UNSOUND: nothing in the copy is worse than L0 already says.

## 6. L4 — the FIR comparison as a standing check

**Verdict: CONDITIONAL.** A row in `03_assumptions.py` is a reasonable
instrument, and its first value is that it would put the number L3 says the
app lacks on a verified page, re-derived weekly. As a single total-vs-total
row it would mislead.

⚠️ **Part of a standing check already exists.** *(read)* The monthly evidence
recheck re-runs `exemption_uncertainty` (12 invariants, among them "every
class taxes LESS than the roll carries") and `roll-year-metadata` (the roll's
residential base must fit FIR 2026 within 5%; it read +1.2%). The second
already catches a year drift, and its failure opens an issue, a channel with a
reader. Neither reads the **pipeline's** levy: both recompute from their own
download. The row's job is the part they do not do: tie the *served* number to
FIR, and watch the residual.

What it needs *(proposal only; the build is a separate PR)*:

1. **Per class, not one total.** Residential and other residential drift up
   all year against a fixed FIR figure (§0.2: +$1.24B in ten weeks). A
   tolerance on the total would either fire every autumn or be set so wide it
   sees nothing.
2. **Alarm on the non-residential residual**: roll non-residential minus FIR
   non-residential minus candidate-zoned non-residential. Today $0.294B, 0.66%
   of base, and non-residential did not drift. A new exempt class, a class
   label mapped to the wrong rate, or a zone falling out of the candidate set
   shows here first.
3. **Print the FIR vintage** (year, resource name, fetch date) beside the
   number, and **hold, not compare, when roll year ≠ FIR year.**

What it would catch: a year drift like 2026-08-25's (already caught monthly,
above); a wrong mill rate (FIR's
implied rates check directly: 7.7419 and 25.2216 match); a class-mapping error;
a new exemption class, if it is larger than roughly $0.3B of assessment.

What it can never catch:
- **Where.** It is one number per class for the city.
- **Offsetting errors**: accounts missing from the roll against exempt land
  billed.
- **Anything from January until the province publishes the new year.** The
  2026 file was fetched in late August *(read)*, so for most of the year the
  row has no comparator and must hold.
- **Collections.** FIR is a levy at bylaw time, not cash, and not
  supplementary tax.
- **Its own input going stale.** `fir_tax_base.json` is a manually reviewed
  file. For 51 weeks of 52 the row re-measures roll drift against a number
  nobody has refreshed.

**Sharpest argument against (that it is the wrong instrument):** a weekly row
on an annual input is a guard that cannot change, on a page few read, which is
this project's standing failure mode. A one-line check in the monthly vintage
digest would reach a reader.

**What would flip it.** To SOUND: built as 1–3. To UNSOUND: the province
changing or dropping Schedule MR.

## 7. What this leaves for Peter

Sized in hoods and dollars. "Blocks" is my recommendation, not a decision.

| # | Call | Size | Blocks release? |
|---|---|---|---|
| 1 | ⚠️ **Split-cut bands print wrong numbers.** Build the per-cut share, or turn band, range and caveat off on Residential and Non-residential | Residential: 16 of 20 caveats false, 2 of 2 bands spurious, low ends off 3.8× and 5.6×. Non-residential: 142 hoods ($62.6M) uncaveated, 4 of 6 low ends off by 20% or more (up to 28×), 3 bands missing | **Yes** — a wrong shipped number |
| 2 | **State the gap in the app.** One sentence in About, a clause in the Total blurb, a link to the published notebook | +$282.0M, +11.2%; today the app says "pay" and the notebook says "does not tax" | **Yes** — it is what makes "pay" conditional and not false |
| 3 | **"Collected"** in the panel headline and the set-aside note | 2 strings; shown for all 358 hoods, including University of Alberta at $178,401 | Recommended; two words |
| 4 | **Non-residential blurb** names institutions as payers | The cut is +20.4% ($226.0M); 163 of 356 hoods are ≥25% candidate | Recommended; the row is already provisional |
| 5 | **Caveat-only hoods drawn solid at the levied endpoint** | 15 hoods, $40.0M; Spruce Avenue 6 → 15, Central McDougall 7 → 48 | No. A 2026-08-16 decision; re-open only if the top ten should not show them at full height |
| 6 | **Unflagged hoods at 10–25%** | 46 hoods, $34.6M; 32 would move ≥10 ranks. Dropping the gate to 0.10 would flag 67 of 358 | No, once #2 is said. A gate at 0.10 dilutes the flag |
| 7 | **"Direction unknown"** in the tooltip caveat and mix note, against a known aggregate direction | Wording locked 2026-08-08 and 08-15, before FIR | No. True per parcel |
| 8 | **`02_methods` "understates its neighbourhood"**, and `FINDINGS_exempt_institutional.md` calling on-roll land "taxed" | 1 public sentence; 1 internal doc | No. Report session's notebook |
| 9 | **FIR row in `03_assumptions.py`**, per class with the residual alarm (§6) | Ties the served levy to FIR weekly; the monthly recheck already covers year drift | No. Separate PR |
| 10 | **Apartments** | ≈$33.4M, not locatable; 15 hoods ≥25% apartment levy | No remedy without data. Note that part is in-year growth |

Nothing here needs exemption data. Items 1–4 are a pipeline column plus copy.

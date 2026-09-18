# Findings — The Roadway Service Life Implied by Edmonton's Audited Books

Captured 2026-09-17 (S170). **The first road service life this project has
obtained from a City source other than the one page the 25-vs-50 choice sits
on.** It does not settle that choice — see §4 — but it ends the situation where
the only life figures available were two readings of a single sentence.

Two findings, and the negative one came first:

1. **The City's Consolidated Financial Statements do NOT publish a roads
   service life.** Roadways are amortized inside a broad *Engineered structures*
   class at **7 to 100 years**, which cannot discriminate 25 from 50.
2. **But Schedule 1 puts the roadway system's gross cost and its annual
   amortization on separate lines, so an implied average life is derivable:
   36.4–38.0 years.** That is road-specific, City-published, and nobody had
   asked for it.

⚠️ **Both are `[DERIVED]` or `[PRIMARY]` from a document fetched and read in
this session, not relayed.** The ask went out as Q3(a) of the send-back brief and
a research round answered it; the reply flagged its own numbers as
*"NOT YET DIRECTLY VERIFIED … reconstructed from search-index snippets and a
research subagent."* Everything below was then re-taken from the PDF directly.
The reply turned out to be correct on both claims it marked solid **and** on the
range it marked unverified — recorded because the standing pattern in this
project is the opposite (`DECISIONS.md` 2026-08-03, 2026-09-03).

Source, fetched 2026-09-17, HTTP 200, 58 pages, 1,415,249 bytes:

- **City of Edmonton, Consolidated Financial Statements, FY2023** —
  `https://www.edmonton.ca/sites/default/files/public-files/FinancialAnnualReportConsolidatedFinancialStatements2023.pdf`
- ⚠️ **edmonton.ca is reachable from the Oracle box again.** `data/DATA.md` §13
  and the send-back brief both record it as 502/unreachable, which is why this
  was routed to an external round at all. **That note is stale** — the page
  behind the whole 25-vs-50 question was also re-read directly today.

## 1. The negative finding: Note 1 has no roads line

Note 1 (Significant Accounting Policies), *Non-Financial Assets → Tangible
Capital Assets*, p23 of the PDF, straight-line amortization:

| asset class | useful life |
|---|---|
| Land improvements | 20 to 50 years |
| Buildings | 10 to 60 years |
| Machinery and equipment | 3 to 50 years |
| Vehicles | 9 to 35 years |
| **Engineered structures** | **7 to 100 years** |

**Roadways are not a separate class.** *Engineered structures* also contains the
light rail transit system, the bus system, waste facilities and "other". The
label `Roadway system` appears only in **Schedule 1** (pp.79–80) and **Note 15**
(p107) as dollar balances, carrying no years.

⚠️ **A 7-to-100 range cannot discriminate 25 from 50.** As an answer to the
question that was asked, this source is exhausted: **nothing further to ask of
it.** That is a real answer and closes the Q3(a) ask.

## 2. The derivation Schedule 1 does support

Schedule 1 reports, per class, the opening and closing **gross cost** and the
**amortization expense for the year** — separately for `Roadway system`. Their
ratio is the average straight-line life implied by the City's own amortization:

> **implied average life = gross cost ÷ annual amortization expense**

FY2023, `Engineering structures: Roadway system` (thousands of dollars):

| quantity | value |
|---|---|
| gross cost, opening | $9,304,626 |
| gross cost, closing | $9,732,383 |
| amortization expense for the year | $255,893 |
| **implied average life** | **36.4 yrs (opening) – 38.0 yrs (closing)**, 37.2 on mean cost |

The three-way spread is just which cost base the year's charge is set against;
the stock grew 4.6% during the year. **Quote the range, not a point.**

## 3. Why the method is trustworthy here — it validates against the note it sits beside

The same ratio computed for every class must land inside that class's own
stated Note 1 range, and **all eight do**. This is the same shape of check that
made the Bike Plan Table 3 capital figures usable (`DECISIONS.md` 2026-08-04):
the document is made to audit itself.

| class | implied (open / mean / close) | Note 1 range | inside |
|---|---|---|---|
| Land improvements | 30.4 / 31.1 / 31.9 | 20–50 | ✅ |
| Buildings | 26.2 / 27.1 / 28.1 | 10–60 | ✅ |
| Vehicles | 20.1 / 21.0 / 22.0 | 9–35 | ✅ |
| Machinery and equipment | 13.7 / 14.0 / 14.4 | 3–50 | ✅ |
| **ENG: Roadway system** | **36.4 / 37.2 / 38.0** | 7–100 | ✅ |
| ENG: Light rail transit | 50.9 / 54.0 / 57.0 | 7–100 | ✅ |
| ENG: Waste | 58.2 / 58.2 / 58.3 | 7–100 | ✅ |
| ENG: Bus system | 28.3 / 28.7 / 29.1 | 7–100 | ✅ |

**The ordering is also the right shape**: light rail (54) outlives the roadway
system (37), which outlives the bus system (29), which outlives machinery (14).
A method that produced roads outliving LRT, or any class outside its own stated
band, would be measuring the arithmetic rather than the assets.

## 4. ⚠️ What it does NOT support — four limits, stated before anyone quotes 37

1. **It is an ACCOUNTING life, not an engineering service life.** Straight-line
   amortization allocates cost across periods; it is a policy choice, and the
   statements never use the words "service life". ⚠️ **This is the sidewalk
   *"amortized for 20 years"* trap one step over** — that turned out to be a
   local-improvement **tax levy term** and treating it as an asset life would
   have been a category error (`DECISIONS.md` 2026-08-04). **Do not call 37 "the
   City's road service life."**
2. **`Roadway system` is every road the City owns** — arterials, collectors,
   locals, alleys and the structures capitalized with them — not a
   neighbourhood street. It carries exactly the caveat the 2023 *Infrastructure
   State and Condition* 33-year figure carries, and for the same reason.
3. **It is an average over a stock of mixed vintages**, weighted by historical
   cost, and the identity `gross ÷ annual charge = life` is exact only for a
   stock in steady state. The 4.6% single-year growth is why §2 gives a range.
4. **Historical cost, not replacement cost.** Older metres sit in the numerator
   at the dollars of their build year, so the figure is not comparable to the
   $9.75B replacement value in the State-and-Condition report.

## 5. Where it leaves the 25-vs-50 call

**It does not settle it, and nothing external can** — the choice is between two
readings the City prints in a single sentence, and that sentence was re-verified
verbatim today (`city_unit_costs.json` → `roadway_om_renewal.✅_unit_resolved_2026_09_17`).

What changes is that the evidence is no longer one-sided:

| reading | source | class |
|---|---|---|
| 25 yrs | Development Impact page, base case | neighbourhood street |
| 50 yrs | Development Impact page, *"with proper maintenance"* — **shipped** | neighbourhood street |
| 33 yrs ⚠️ | 2023 Infrastructure State and Condition, p27 (expected life) | all roads — ⚠️ **row label in doubt**, see below |
| **36.4–38.0 yrs** | **audited Schedule 1, implied — this document** | all roads |
| **25.9 yrs** | **2020 Infrastructure State and Condition, Appendix A p31** | **collector + local — the population the site charges** |
| **60 yrs** | **City staffer via ConstructConnect / *Journal of Commerce*, 2016** — see §5a | **Neighbourhood Renewal reconstruction — also the right population** |

⚠️ **Added 2026-09-17, after this document was written: the 33 is in doubt and a
better figure exists.** The 2020 edition of that report puts **33 against the
*Goods and People Movement Portfolio*** (roads + bridges + active modes + LRT +
transit bus), while its **Roads row reads 24**. Our 33 may be a portfolio number
read as a roads number — flagged, not corrected, since the 2023 edition was not
re-obtained. More importantly the same 2020 table publishes expected asset life
**per road class** — Local 28, Collector 20, **25.9 lane-km weighted across
collector+local** — which is the first life figure on the right population
rather than a citywide aggregate. `docs/FINDINGS_road_class_inventory.md` §4–§5.

⚠️ **Both City-published *aggregates* land below the shipped 50**, and they were
produced by different mechanisms (an engineering condition assessment and an
accounting policy), which is worth more than two agreeing numbers from one
method. ⚠️ **But neither is a neighbourhood street**, and the site's rate is
calibrated to one — so this is a reason to state the choice in the methodology
note, not a reason to move the rate. ⚠️ **And the two figures that ARE on a
neighbourhood street disagree with each other by more than either disagrees with
50** — 25.9 (Appendix A, expected life) against 60 (§5a, reconstruction interval).
That is the tell that they are measuring different events, not competing
estimates of one.

⚠️ **Recorded against my own interest, deliberately** (`measurements-that-favour-me`):
this finding does **not** support the number the site currently ships, and it was
derived by the same session that verified the centreline unit in the shipped
rate's favour. Both were measured the same way; only one flatters the status quo.

**The counter-argument for 50, which is on the page itself and is not circular**
(unlike the 3% set-aside rule, demoted 2026-09-03): the $600k + $1.9M **is** the
*"proper maintenance and renewal"* the page says extends the life to 50.
Annualizing that bundle over 25 years charges the cost of the extension while
refusing to count the extension. See `TODO.md`'s service-life item.

## 5a. ⚠️ A City-attributed 60-year reconstruction life, on the right population

Added **2026-09-18 (S171)**. This is the only figure in §5's table that lands
**above** the shipped 50, and it is on the same population as the 25.9.

> *"The results of a complete reconstruction are expected to endure for **60
> years**, so long as preventative maintenance is carried out as scheduled — such
> as road **microsurfacing at 10 years and again at 40 years**, along with a
> **roadway overlay completed after 30 years**."*

- **ConstructConnect / *Journal of Commerce*, September 2016**, quoting the City
  on the **Neighbourhood Renewal** program:
  `https://canada.constructconnect.com/joc/news/infrastructure/2016/09/infrastructure-upgrades-forge-ahead-in-edmonton-1018310w`
- **Fetched and matched verbatim from this box 2026-09-18** (`certifi`; HTTP 200).
- ⚠️ **[SECONDARY]** — a trade publication quoting a named City staffer, not a
  City document. It is **not** primary, and it should not be quoted as though the
  City published it. What it is good for is the *structure*, which no primary
  source states as plainly.

**Why it matters more than its rank suggests.** It is the only source found that
states the **maintenance schedule and the resulting interval together**, and it
therefore explains the Development Impact page's sentence rather than competing
with it:

| event | interval | what happens |
|---|---:|---|
| surface treatment | 10 yr, 40 yr | microsurfacing |
| resurfacing | 30 yr | roadway overlay |
| **expected asset life** (Appendix A) | **~26 yr** | the structure is *due* — not the same as replaced |
| **full reconstruction** | **50–60 yr** | base rebuilt; the cycle restarts |

⚠️ **`road_m_per_acre` charges the whole bundle — capital + O&M + renewal — so
its denominator is the interval over which the bundle recurs**, which is the
reconstruction interval, not the resurfacing interval. On that reading the
shipped 50 is the conservative end of 50–60, and the 25.9 is a different
quantity rather than a competing answer.

⚠️ **Provenance, stated plainly.** This figure surfaced in the external research
round and sat in the send-back brief's Q3(b) as one of four *unverified* relayed
service lives; it was not used at the time. Two of the other three were also
spot-checked on 2026-09-18 and verify verbatim — **Calgary** *"A fully
reconstructed road can last up to 20 years"* (`calgary.ca`, primary), and
**Winnipeg**, whose regional-street asphalt is *"designed for 25 years"* with
rehabilitation *"expected to extend the service life … to 60"* — ⚠️ **the same
base-plus-maintained pair Edmonton prints**, from a second municipality. The
fourth (Alberta Transportation, 20 yr) is provincial highways, a different asset
class, and does not bear on this.

⚠️ **COUNTS IN FAVOUR OF THE SHIPPED NUMBER, AND WAS RETRIEVED BY A SESSION THAT
HAD ALREADY ARGUED FOR IT ONCE THAT DAY** (`measurements-that-favour-me`). The
quote is verbatim from a URL that returns 200 and the fetch is repeatable in §6's
terms; the *reading* built on it — that this is a different event from the 25.9
rather than a contradiction of it — is an argument, not a measurement. **Read
§4a of `docs/FINDINGS_road_class_inventory.md` together with this, and treat both
as wanting a cross-read.**

> ✅ **CROSS-READ 2026-09-18 (S172, Fable 5.1)** —
> `docs/FINDINGS_road_life_crossread.md` §4. Quote re-fetched verbatim; the
> two-events reading **holds** and is the only one under which the Development
> Impact page's own $1.5M / $600k / $1.9M are internally consistent. Three
> narrowings: (1) 60 is a **forward** claim about a road reconstructed to 2016
> standards on a full treatment schedule, not an interval the existing
> mean-age-38 stock has achieved — NRP exists because that stock did not last
> 60; (2) **Calgary's primary "a fully reconstructed road can last up to 20
> years" is filed above as verification and not weighed** — it is almost
> certainly a base life comparable to Edmonton's "usually 25", but that has to be
> said; (3) the schedule that buys the 60 costs more than the page's $1.9M
> (observed NRP reconstruction 1.66× it), so the 50-year *rate* is a floor even
> where the 50-year *life* is right.

## 6. Reproduction

Figures transcribed from Schedule 1, p79 of the FY2023 statements. The check in
§3 is the point — it runs offline and fails if any transcription is wrong.

```python
# class: (opening cost, closing cost, amortization expense, Note 1 stated range)
S1 = {
    'Land improvements':       (1_897_484, 1_987_563,  62_379, (20, 50)),
    'Buildings':               (3_704_948, 3_969_045, 141_361, (10, 60)),
    'Vehicles':                (1_485_937, 1_626_337,  74_000, (9, 35)),
    'Machinery and equipment': (1_037_305, 1_092_018,  75_923, (3, 50)),
    'ENG: Roadway system':     (9_304_626, 9_732_383, 255_893, (7, 100)),
    'ENG: Light rail transit': (1_866_680, 2_091_320,  36_660, (7, 100)),
    'ENG: Waste':              (  156_702,   156_839,   2_692, (7, 100)),
    'ENG: Bus system':         (  289_323,   297_697,  10_230, (7, 100)),
}
for k, (o, c, a, (lo, hi)) in S1.items():
    yrs = [o / a, ((o + c) / 2) / a, c / a]
    assert all(lo <= y <= hi for y in yrs), f'{k} falls outside its own Note 1 range'
    print(f'{k:<24}' + ''.join(f'{y:7.1f}' for y in yrs))
```

To re-fetch the source (edmonton.ca needs `certifi` from this box — the CA
bundle is stale, `oracle-box-stale-ca-bundle`):

```python
import requests, certifi, io
from pypdf import PdfReader
url = ('https://www.edmonton.ca/sites/default/files/public-files/'
       'FinancialAnnualReportConsolidatedFinancialStatements2023.pdf')
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=90, verify=certifi.where())
rd = PdfReader(io.BytesIO(r.content))          # Note 1 table p23, Schedule 1 p12
print(rd.pages[22].extract_text())
```

⚠️ **A later fiscal year is a different measurement, not a correction.** The
implied life moves with the stock's age mix and with any re-estimate of useful
lives. If FY2024 or FY2025 is added here, report it as a second year in a series
and say whether Note 1's ranges changed — do not overwrite this one.

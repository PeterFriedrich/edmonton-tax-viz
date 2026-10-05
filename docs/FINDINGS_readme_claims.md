# Findings — README public claims + licence (queue item 8)

**Run:** 2026-10-05, S215, Opus 5.5, `xhigh`. ⚠️ Same model family as the
authors of #486–#488, #490 and #500–#502.
**Target:** `README.md`, the public front door. Each sourced claim is checked
against its source, each claim about this repo against the repo today, and the
licence split against what is tracked. Then: do `tests/test_readme_claims.py`
and `tests/test_license.py` pin the claims that matter?
**Instrument:** `edmonton-audit` decision stack. Primary sources fetched on
2026-10-05:
- CBC (`datePublished` read from the page's JSON-LD);
- the Urban3 Lafayette case study;
- the Halifax 2005 PDF (text extracted, pp. 10–12, 18);
- CNU;
- Calgary Lens;
- the Smart Prosperity PDF and 2026 tax-rate coverage, via search.

The repo's own transcription of IIMP 2016 (`docs/FINDINGS_iimp_growth_areas.md`).
The live `q7d6-ambg` row count. The published notebook HTML under
`web/notebooks/`, and `git ls-files`.

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Should the README make comparative and sourced claims at all? | **SOUND.** It is the public front door, and the claims carry the motivation. |
| L1a | External claims true to their sources? | **SOUND, 9 of 9.** Table below. |
| L1b | Claims about this repo true today? | **WARN — F1, F2.** Two counts have drifted; one report is framed as a City defect after S214 knocked out its premise. |
| L2 | Licence split covers what is tracked? | **CONDITIONAL — F3.** City-derived rows sit in paths no scope names, so they fall under the MIT grant by default. The guard detects data by extension and cannot see them. |
| L3 | Do the guards pin what matters? | **SOUND for the claim that matters most** (break-even framing, falsified by its own self-test). **Nothing pins a count**, which is how F1 drifted. |

### L1a — every external claim, against its source

| README claim | Source read | Holds? |
|---|---|---|
| Sustainable Prosperity: costs exceed revenues by nearly $4B over 60 years across 17 planned developments | Smart Prosperity *Suburban Sprawl* (Oct 2013): *"Across just 17 of more than 40 new planned developments in Edmonton, costs … expected to exceed revenues by nearly $4 billion over the next 60 years"* | ✅ |
| 2016 analysis of Decoteau, Riverview and Horse Hills: $1.4B short over 50 years | IIMP 2016 Attachment 1, transcribed in `FINDINGS_iimp_growth_areas.md`: *"cumulative shortfall over the 50 year analysis period … in the order of $1.4 billion"* | ✅ (the City's name is "Horse **Hill**") |
| Edmonton raised property taxes by 6.9% | CBC / CTV, Dec 2025: 6.9% for **2026** | ✅ (undated "recently" will rot) |
| Ottawa: Hemson, $465/person/yr deficit vs $606 surplus; CBC 2021-09-29; Menard | CBC page: headline *"$465 per person per year"*, sub *"ends up ahead by $606 for high-density infill"*, *"Hemson Consulting Ltd. review"*, *"Coun. Shawn Menard asked city staff"*, `datePublished 2021-09-29` | ✅ |
| Lafayette: parcel-level, 2015 capital revenue vs 50-year cost of roads, "the first of its kind" | Urban3: *"This Cost of Service analysis was the first of its kind"*; *"Total capital revenue in 2015 … and the total 50 year cost of roads"* | ✅ |
| Halifax 2005: roads $1,053 (1.2 people/acre) vs $26 (92/acre), 40:1; all services $5,240 → $1,416, ~3.7:1 | PDF p.10 *"Pattern A is $1,053/year vs. $26/year in Pattern G"*; p.11 totals `$5,240 … $1,416`; p.12 *"1.2 people per (residential) acre"*; p.18 *"92 people per (residential) acre"* | ✅ (see O1) |
| Arlington: 33% of county tax base on 8% of land | CNU: *"generated 33 percent of the county tax base on only 8 percent of its land"* | ✅ |
| Calgary Lens: Pixeltree, 313 communities, 2026 roll, raw totals, includes the provincial education portion | calgarylens.ca: *"313 of 313 communities"*, Pixeltree, 2026 roll, totals not per-area, municipal + *"Alberta education mill rate (provincial portion)"* | ✅ |
| Notebook figures: 2,448 accounts / 188 hoods / 29 addresses; ~$15B exemption gap | Published pages: `2,448`, `neighbourhoods affected: 188`, `addresses losing EVERY account: 29`. Class gaps $1.963B + $4.005B + $8.978B + $0.006B = **$14.95B** | ✅ |

## F1 — two counts have drifted

- **"~448,000 property assessment records"** (Why Now). The live
  `q7d6-ambg` count is **439,696**. The Data sources list two sections down
  already says **~440,000**, so the README disagrees with itself.
- **"Six confirmed, five of them with a published, reproducible notebook"**
  (Data Problem §2). It went false on 2026-10-03,
  when S214 found issue 5's premise unsound (Alberta publishes the school
  list). It is **"six" again only by coincidence**, because issue 8 was added
  today (`DATA_ISSUES.md` §8, no notebook). The confirmed set with notebooks is
  now issues 1, 3, 4 and 6: **four**. "Five" is false either way.

**✅ Fixed 2026-10-05 (S216):** ~440,000, and the counts replaced by the pointer.
**Class:** `claim`, public. **Remedy (Peter; public copy):** fix both numbers,
or drop the counts for a pointer ("see `docs/DATA_ISSUES.md`"), which cannot
drift. F1 is what an unpinned count does. The 448k figure was right for an
earlier roll.

## F2 — the school page is listed as a City defect after S214 removed the premise

The Status section lists *"Edmonton's open data covers two school authorities,
not all of them"* under *"standalone, reproducible findings about **defects in
Edmonton's published open data**"*. The page was amended 2026-10-03: the
province publishes a daily spreadsheet of every school, with addresses. The
page itself now says *"the finding is unchanged"*, meaning the City's portal
does cover two authorities, so the page is not false. The README's framing of
it as a **defect** is what S214 F1 undercut. `DATA_ISSUES.md` holds issue 5 at
*"DO NOT SEND as drafted"* pending Peter (withdraw, or narrow to a request for
a geocoded version).

**Class:** `claim`, public. **Remedy:** follows Peter's issue-5 decision.
Withdraw → drop the bullet. Narrow → reframe it as a coverage note, not a
defect. Separately, the list omits the permit-neighbourhood-list page, which
*is* a confirmed defect (issue 6) with a published notebook.

## F3 — City-derived rows sit outside every licence scope

`LICENSE` grants MIT over *"the code and configuration in this repository"*
and carves out `docs/` etc. (CC BY), `data/` + `web/data/` (upstream terms) and
`web/vendor/`. Tracked paths that hold **City-derived records** but sit in no
carve-out:

- `output/historical_roll_gaps.json`: per-year **account IDs** from
  `qi6a-xuwt` (b11ccc3).
- `web/notebooks/*.html` (7) and `web/verified/*.html` (3): the published
  reports. Prose, plus tables of City rows; e.g. `historical-2024-gap.html`
  lists addresses with assessed values.
- `notebooks/` sources (24 files): code, and the findings prose of the
  published reports.

The README table names none of these. By the LICENSE's own structure,
everything not carved out is under the MIT grant. That is the exact failure
`test_license.py`'s docstring describes (*"the repo would be asserting MIT
over City of Edmonton data"*). The test cannot see it because it classifies by
extension: `.json` is excluded on purpose, and `.html` was never in the set.
The **prose** in those reports is also analysis, and the LICENSE's own
reasoning (*"a software licence says nothing useful about a findings
document"*) puts that under CC BY.

**Class:** `guard-blind` (the guard's population omits two payload shapes).
**Reach:** licence text only; no figure is wrong.
**Remedy (Peter; licensing is his):** add `output/`, `web/notebooks/` and
`web/verified/` to carve-out 2, or delete `output/historical_roll_gaps.json` if
it is obsolete. Say in carve-out 1 that the reports' prose is CC BY. Add the
paths to the README table, so `test_license`'s two-way README↔LICENSE-docs tie
covers them.

## Observations

- **O1 — Halifax 40:1 excludes curbs and sidewalks.** The $26 is "Roads (no
  curbs)"; Pattern G also carries $27 of curbs and sidewalks, and A carries $0.
  So roads + curbs is 1,053 : 53, about 20:1. The README follows the report's
  own sentence (p.10), so this is not a defect. It is a nuance the report also
  leaves out.
- **O2 — the 6.9% line is undated.** "Recently" is the 2026 budget. Next
  December it will be a year-old figure without saying so.

## What this run got wrong

- **I first read "Six confirmed" as false, then found it true.** It counts
  issue 8, which I added to `DATA_ISSUES.md` this morning. The README sentence
  was false from 2026-10-03 until #660 merged today, and is now right by
  accident: half of it (six) right for the wrong reason, the other half (five
  notebooks) still wrong. A count checked an hour earlier would have produced a
  different finding. That is F1's point, and it nearly became my error.
- **I nearly reported Halifax's 40:1 as inflated** on reading the Pattern G
  page, which shows roads at $53. That figure includes curbs and sidewalks. The
  report's own sentence uses $26, and the README matches it. Demoted to O1.
- **"Four lenses" briefly looked wrong**, because `verify-blurbs.js` counts
  `glass` and `change` states as public. Both are modes inside other views,
  not views. The public `#views` are Money, Development, Services and Ratio (Uses
  and Lab hidden), so the README is right.

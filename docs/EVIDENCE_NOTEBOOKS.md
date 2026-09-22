# Evidence notebooks — what each report rests on

Inventory of the **standalone evidence notebooks** (`notebooks/standalone/`):
what each one claims, which data it stands on, and where it is published.

⚠️ **This is not `docs/VERIFICATION.md`.** That file covers
`notebooks/verified/` — pipeline notebooks that run inside `refresh.yml` and
gate the weekly publish. **These are different artifacts with an opposite
purpose:** they are public-facing evidence for the defects in
`docs/DATA_ISSUES.md`, they run on demand, and nothing regenerates them.

**Why this file exists:** the reverse lookup was impossible. "Which reports
break if `q7d6-ambg` changes?" required opening all four, because the only
per-report data description was a prose caption in `web/notebooks/index.html`.

---

## The reports

| report | claims | source `.py` | published |
|---|---|---|---|
| **Roll year metadata** | The current roll is published under the wrong `Period of Coverage` year | `roll_year_metadata.py` | [roll-year-metadata.html](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/roll-year-metadata.html) |
| **Historical 2024 gap** | Whole buildings are missing from the 2024 slice of the Historical roll | `historical_2024_gap.py` | [historical-2024-gap.html](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/historical-2024-gap.html) |
| **Exemption uncertainty** | What public data can and cannot say about tax-exempt property | `exemption_uncertainty.py` | [exemption-uncertainty.html](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/exemption-uncertainty.html) |
| **School coverage gap** | Open data covers two school authorities, not all of them | `school_coverage_gap.py` | [school-coverage-gap.html](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/school-coverage-gap.html) |
| **Permit neighbourhood list** | The permits dataset puts several neighbourhoods in a one-neighbourhood field, in the name AND id columns | `permit_neighbourhood_list.py` | [permit-neighbourhood-list.html](https://peterfriedrich.github.io/edmonton-tax-viz/notebooks/permit-neighbourhood-list.html) |

| report | `DATA_ISSUES.md` | status | invariants | re-verified |
|---|---|---|---|---|
| Roll year metadata | issue **1** | **ACTIVE** | 8 of 8 | 2026-08-29 |
| Historical 2024 gap | issue **3** | **ACTIVE** | 6 of 6 | 2026-08-29 |
| Exemption uncertainty | issue **4** | **ACTIVE** | 11 of 11 | 2026-08-29 |
| School coverage gap | issue **5** | **ACTIVE** | 4 of 4 | 2026-08-29 |
| Permit neighbourhood list | issue **6** | **ACTIVE** | 5 of 5 | 2026-09-17 |

## ⚠️ They are re-run monthly now — and what the first run found

**Added 2026-09-21.** `.github/workflows/evidence-recheck.yml` re-executes
**every** notebook in `notebooks/standalone/` against live sources on the
**15th of each month** and files a GitHub issue
(`scripts/recheck_evidence_notebooks.py`; triage in `docs/RUNBOOK.md` §0e).
An issue is filed even when all-green, for the same reason the vintage digest
files one.

**Why it had to exist.** Until that date **nothing re-ran these at all** —
`refresh.yml` runs `notebooks/verified/`, a different directory doing a
different job. Measured 2026-09-21: four of the five published evidence pages
had not touched a live source since **2026-08-29**, while every file in
`web/notebooks/` carried an mtime of the previous day, because S180's
mobile-CSS pass had re-rendered stored outputs. ⚠️ **The files looked a day
old and the evidence was three weeks old** — a distinction nothing on the page
made, and the exact shape of *"updated on so-and-so"* standing in for
*"checked"*.

**The baseline, established the same day.** All seven notebooks re-executed
against live sources — **113 invariants, 113 holding**:

| notebook | kind | invariants |
|---|---|---|
| `roll_year_metadata` | evidence | 8 |
| `historical_2024_gap` | evidence | 12 |
| `exemption_uncertainty` | evidence | 22 |
| `school_coverage_gap` | evidence | 4 |
| `permit_neighbourhood_list` | evidence | 5 |
| `roads_lifecycle_rate` | justification | 40 |
| `roads_operating_rate` | justification | 22 |

⚠️ **Changed 2026-09-22 (S187, `docs/FINDINGS_roads_rate_notebooks.md`):**
`roads_lifecycle_rate` is now **45**, so the total is **118**. One duplicate
was dropped, the wrong "paved rose" claim was withdrawn, and 7 checks were added
that pin the hardcoded Schedule 1, Appendix A and Appendix B tables to the
fetched PDFs. Before that, 16 of its 40 were arithmetic on constants that could
not see a source change. `roads_operating_rate` stays at 22, but two of them
changed meaning: the snow check now says the 55% split is unverifiable, and the
program-separation check is now the intra-municipal charge mirror. The recheck
reports pass/fail per notebook and keeps no per-claim baseline, so the rewording
raises no alert.

⚠️ **So every documented defect is still present upstream as of 2026-09-21,
and no publisher has fixed anything.** That is unsurprising — `DATA_ISSUES.md`
records **zero reports sent** — but it had never actually been *checked*
before, only assumed.

⚠️ **The checker found a defect in the two newest notebooks on its first live
run.** Both roads notebooks reported their verdicts only through
`display()`, which renders as an opaque object repr outside a Jupyter kernel —
so run as scripts they reported **nothing** about their own invariants, and the
checker correctly refused to call that a pass rather than trusting exit 0. Both
now print in `check()`, the idiom the five evidence notebooks already used.
**A new notebook in this directory needs a printing `check()` or the recheck
cannot see it.**

⚠️ **"Re-verified" is the date the committed HTML was last executed, not a
freshness guarantee.** Nothing re-runs these on a schedule — chosen deliberately
(`DECISIONS.md` 2026-08-26). All four were re-executed 2026-08-29 and every
invariant still passed, so no finding here has yet been overtaken.

---

## ⚠️ A SECOND SPECIES lives in the same folder — justification notebooks

Added **2026-09-18 (S172)**. Everything above describes **defect reports**:
evidence that someone else's published data is wrong, each tied to a
`DATA_ISSUES.md` row, each with invariants written to **fail when the publisher
fixes it**. A second kind of notebook now sits beside them and **must not be
read against those rules**.

| notebook | claims | source `.py` | published |
|---|---|---|---|
| **Roads lifecycle rate** | Why this project's roads cost lens uses **$50 per road-metre per year** — the published figures, the centreline unit, the 50-year denominator, three independent cross-checks, and the one argument that had to be withdrawn | `roads_lifecycle_rate.py` | ⚠️ **NOT PUBLISHED** — Peter's call pending |
| **Roads operating rate** | Why the same lens's *other* column is **$9.32 per road-metre per year** — the two halves and their two vintages, the secondary source that earns its place by reconciling to the City's own programme total, the **lane-km unit defect that ships disclosed rather than corrected**, the offsetting arterial blend, and the 4.65× re-scope this project was forced into by its own split treatment | `roads_operating_rate.py` | ⚠️ **NOT PUBLISHED** — same call, still pending |

**How it differs, in the three ways that matter:**

1. **It defends OUR number, not someone else's defect.** There is no
   `DATA_ISSUES.md` row and there should not be one.
2. **Its invariants are meant to keep passing.** A defect report that keeps
   agreeing with itself after the fix is a failure; this one agreeing with
   itself means the sources still say what we transcribed. ⚠️ **A failure here
   means a transcription is wrong or a source moved** — both worth an alert,
   neither a success.
3. **It is not in `web/notebooks/index.html` and its HTML is not in `web/`.**
   Rendering it into that folder publishes it to GitHub Pages whether or not
   the index links it. **Do not move it there without Peter's say-so** — it was
   built "internal first, publish later" on his 2026-09-18 call.

⚠️ **The rule it DOES share, and the important one: it imports nothing from
`src/` and reads nothing from `data/`.** Every figure is fetched live from a
public URL at run time and checked against the transcription printed on the
page, so the notebook can be handed to a skeptic who has never seen this repo —
which is the whole point of a justification document. Two figures that cannot be
derived without the repo (the 3,654 km charged network; the observed NRP
reconstruction $/m) are labelled **[repo]** in place and cited rather than
asserted. **40 invariants, all passing as of 2026-09-18.** The operating
notebook follows the same rule, with the centreline km measured from
`data/raw/roads.geojson` and the 2020 class lane-km split labelled **[repo]**
and **[SECONDARY]** respectively. **22 invariants, all passing as of
2026-09-21.**

⚠️ **Their sources are PDFs, web pages and budget APIs, not Socrata**, so the
per-source tables below do not cover them. The lifecycle notebook stands on: the
*Development Impact on Infrastructure* page, the FY2023 Consolidated Financial
Statements, the 2020 and 2025 *Infrastructure State and Condition* reports,
`budget.edmonton.ca`'s **capital** budget API, and one trade-press article. The
operating notebook stands on: `budget.edmonton.ca`'s **operating** budget API,
the *Snow and Ice Control Annual Report Winter 2023-24* PDF, and one Taproot
article. ⚠️ **The 2020 report is fetched from the Internet Archive** — the City
no longer serves it and the current edition no longer publishes per-class asset
lives at all, so that snapshot is not replaceable.

⚠️ **The two notebooks share `budget.edmonton.ca` and must not be read as
corroborating each other through it** — one reads the capital budget, the other
the operating budget, and a portal outage takes out a section of each.

⚠️ **The operating notebook already caught its own source moving.** Its §9 pins
the `Parks & Roads Services` FY2026 branch total, and between
`FINDINGS_roadway_maintenance_rate.md`'s measurement (2026-09-05,
$307,325,053 → 1.2551×) and the notebook's first execution (2026-09-21,
$304,370,450 → 1.2431×) the portal revised it. Nothing shipped moved — the rate
is unescalated FY2017 — but **a document that had pinned the escalated figure
would now be wrong**, which is the case for invariants that keep passing.

---

## Lifecycle — these are SNAPSHOTS, not living documents

**A report is evidence that something was true on a date.** It is not maintained
toward the present, and it is not supposed to be. Every report states its own
two dates on its face — *first measured* and *re-executed* — because the
published HTML is the artifact that gets handed to someone, usually without the
index page that would otherwise date it.

⚠️ **Two of the four carried NO date at all until 2026-08-29.** A snapshot that
does not say what it is a snapshot of is the failure mode this section exists to
prevent.

### Status vocabulary

| status | meaning |
|---|---|
| **ACTIVE** | the defect stands; the report is current evidence |
| **RESOLVED** | the publisher fixed it — the report stays up as the record |
| **AMENDED** | the defect changed shape; same report, findings updated |
| **SUPERSEDED** | replaced by a different report; archived, not deleted |

### The three transitions

**1. They fix it → RESOLVED, and the report STAYS PUBLISHED.**
⚠️ **Do not delete or unpublish it.** It becomes the record that the issue was
found, reported and fixed — which is the only durable evidence the work
mattered. Mark it RESOLVED here, add a dated note at the top of the notebook
saying what changed, and update `DATA_ISSUES.md`. ⚠️ **The invariants will now
FAIL, and that is correct** — several are deliberately written to fail on the
fix. Do not "repair" them into passing; a report that keeps agreeing with itself
after being acted on is one nobody notices has succeeded.

**2. It morphs → AMENDED, same report.**
The defect is still there but has changed shape, or main-project work turned up
something that alters the premise. Update the notebook in place, re-execute,
and leave `FIRST_MEASURED` alone — it records when the finding was made, not
when it was last touched.

**3. It is replaced by a different bug → SUPERSEDED, archive and write a new
one.** When the finding is not the same finding any more, do not stretch the
old report to cover it. Move it to `notebooks/standalone/archive/` and its page
to `web/notebooks/archive/`, mark it SUPERSEDED **with a pointer to the report
that replaced it**, and write the new one fresh. ⚠️ **Archive, never delete** —
the same rule as `docs/TODO_archive.md`. A public URL that 404s is worse than
one that explains itself, and outreach may already have cited it.

⚠️ **Only transition 1 is detectable automatically** (the invariants flip).
Transitions 2 and 3 are human judgement, usually triggered by main-project work
rather than by the data — so the per-source table below is the tool: when a
source's understanding changes, check who depends on it.

---

## What each report stands on

**Read this direction to answer "what does this report need?"**

| report | Socrata (`data.edmonton.ca`) | other sources |
|---|---|---|
| Roll year metadata | `q7d6-ambg`, `qi6a-xuwt` | `open.alberta.ca` — FIR workbooks (~10 MB, cached) |
| Historical 2024 gap | `q7d6-ambg`, `qi6a-xuwt` | — |
| Exemption uncertainty | `q7d6-ambg`, `fixa-tstc` | `open.alberta.ca` — FIR |
| School coverage gap | `q7d6-ambg`, `996c-239n`, `gfxq-u8uu` | `api.us.socrata.com` — the **catalogue** API, not a dataset |
| Permit neighbourhood list | `24uj-dj8v`, `65fr-66s6`, `q7d6-ambg` | — |

**Read this direction to answer "if this source changes, what breaks?"**

| source | what it is | reports depending on it |
|---|---|---|
| `q7d6-ambg` | Property Assessment Data (Current Calendar Year) | ⚠️ **all four** |
| `qi6a-xuwt` | Property Assessment Data (Historical) | Roll year metadata, Historical 2024 gap |
| `fixa-tstc` | Zoning Bylaw Geographical Data | Exemption uncertainty |
| `996c-239n` | EPSB School Locations | School coverage gap |
| `gfxq-u8uu` | Edmonton Catholic Schools (Current) | School coverage gap |
| `24uj-dj8v` | General Building Permits | Permit neighbourhood list |
| `65fr-66s6` | Neighbourhood Boundaries | Permit neighbourhood list |
| `open.alberta.ca` | Financial Information Return workbooks | Roll year metadata, Exemption uncertainty |
| `api.us.socrata.com` | Socrata catalogue search | School coverage gap |

⚠️ **`q7d6-ambg` is a single point of failure for the whole evidence set** — all
five reports touch it. A schema change there does not just break one report — it
breaks every one, and because nothing runs them on a schedule, **it breaks them
silently.** The
school report is the most exposed: it asserts a property of that dataset's
*schema* (that it carries no land-use field), so a column being ADDED — the
outcome that report would welcome — makes its invariant fail rather than pass.

---

## The one that argues an absence

**School coverage gap is built the opposite way round from the other three** and
should not be "made consistent" with them.

The other three demonstrate a wrong value, which can be shown directly. That
one asserts a dataset **does not exist**, and no query returns that. So it
states what the missing dataset would look like, runs the catalogue searches
that would **find** it, and shows they come back empty.

⚠️ **Two of its invariants are written to FAIL when the City publishes the
missing schools** — the outcome the report asks for. A report that keeps
agreeing with itself after being acted on is one nobody notices has worked.
Do not "fix" those into passing.

---

## ⚠️ The duplicated helper block is DELIBERATE — do not extract it

Each notebook defines its own `check` / `_read` / `soda` / `show`. Measured
2026-08-29: **~219 of 2,080 lines, about 11%**, and `check` is byte-identical
in all four.

**This duplication is load-bearing.** `DECISIONS.md` 2026-08-26 locked that a
standalone notebook **imports nothing from `src/`**, so it can be handed to a
skeptic — or to the City — who has never seen this repo. A shared module
breaks precisely that property, which is the reports' whole purpose.

Reviewed and left alone 2026-08-29 on Peter's call, after measuring the drift:

- `check` — **identical** across all four
- `_read` — three variants differing **only in the timeout parameter** (600
  hardcoded / 600 default / 300 default)
- `soda`, `show` — two variants each, cosmetic

⚠️ **The overlap is HTTP boilerplate, not data loading.** Each report's actual
loading is genuinely different — Alberta XLSX workbooks, the catalogue API,
aggregate SoQL — so there is far less shared "loading and inspection" than the
helper names suggest. **Revisit only if a variant diverges behaviourally**, and
prefer a generated preamble over an imported module if it ever does, so the
published artifact stays self-contained.

---

## Adding a report

1. Write `notebooks/standalone/<name>.py` in jupytext percent format, matching
   the house pattern: self-contained, live public sources, a `CHECKS` list, and
   a final cell that raises `AssertionError` if any invariant fails.
2. Set `FIRST_MEASURED` to today and leave it alone forever after — it dates
   the FINDING, not the last edit. Execute it **cold-cache** so the committed outputs prove the notebook's own
   portability, then commit both the `.py` and the executed `.ipynb`.
3. Render to `web/notebooks/<name-with-dashes>.html` (underscores become
   dashes) and add an entry to that folder's hand-written `index.html`.
   ⚠️ **Then run `python tools/inject_notebook_mobile_css.py`.** nbconvert's
   stock template **clips** code lines wider than the viewport — no scroller,
   nothing to find. It is invisible at desktop width and total on a phone
   (measured 2026-09-20: 54 of 54 cells clipped at 390px, 0 at 1280px).
   `tests/test_notebook_mobile_css.py` fails if you skip it.
4. Update `docs/DATA_ISSUES.md` — **the status table there is authoritative for
   send status**, not this file.
5. Add rows to **both** tables above (status **ACTIVE**); the reverse lookup is
   the point.

⚠️ **Write invariants that fail when the publisher fixes the defect.** That is
the house style here, and it is what makes a report notice its own success.

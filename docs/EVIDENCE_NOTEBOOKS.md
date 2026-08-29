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

| report | `DATA_ISSUES.md` | status | invariants | re-verified |
|---|---|---|---|---|
| Roll year metadata | issue **1** | **ACTIVE** | 8 of 8 | 2026-08-29 |
| Historical 2024 gap | issue **3** | **ACTIVE** | 6 of 6 | 2026-08-29 |
| Exemption uncertainty | issue **4** | **ACTIVE** | 11 of 11 | 2026-08-29 |
| School coverage gap | issue **5** | **ACTIVE** | 4 of 4 | 2026-08-29 |

⚠️ **"Re-verified" is the date the committed HTML was last executed, not a
freshness guarantee.** Nothing re-runs these on a schedule — chosen deliberately
(`DECISIONS.md` 2026-08-26). All four were re-executed 2026-08-29 and every
invariant still passed, so no finding here has yet been overtaken.

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

**Read this direction to answer "if this source changes, what breaks?"**

| source | what it is | reports depending on it |
|---|---|---|
| `q7d6-ambg` | Property Assessment Data (Current Calendar Year) | ⚠️ **all four** |
| `qi6a-xuwt` | Property Assessment Data (Historical) | Roll year metadata, Historical 2024 gap |
| `fixa-tstc` | Zoning Bylaw Geographical Data | Exemption uncertainty |
| `996c-239n` | EPSB School Locations | School coverage gap |
| `gfxq-u8uu` | Edmonton Catholic Schools (Current) | School coverage gap |
| `open.alberta.ca` | Financial Information Return workbooks | Roll year metadata, Exemption uncertainty |
| `api.us.socrata.com` | Socrata catalogue search | School coverage gap |

⚠️ **`q7d6-ambg` is a single point of failure for the whole evidence set.** A
schema change there does not just break one report — it breaks every one, and
because nothing runs them on a schedule, **it breaks them silently.** The
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
4. Update `docs/DATA_ISSUES.md` — **the status table there is authoritative for
   send status**, not this file.
5. Add rows to **both** tables above (status **ACTIVE**); the reverse lookup is
   the point.

⚠️ **Write invariants that fail when the publisher fixes the defect.** That is
the house style here, and it is what makes a report notice its own success.

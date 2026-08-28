# FINDINGS — proxy readings, first class sweep (2026-08-28, S123)

Instrument: `docs/FABLE_AUDIT_proxy_guards.md`. Ledger row: 2026-08-28.
Scope: every guard, gate, workflow trigger and user-facing vintage string in
the repo, audited as a **set** for the shape five accidental finds shared.

**Headline: 3 UNSOUND, 1 CONDITIONAL, 1 SOUND. The two that matter were not
known, and one of them is the 2026-08-27 defect still live through a different
door.**

> ### Disposition — 2026-08-28, same day
> **F1 FIXED · F3 FIXED · F4 still open · F5 still open** (Peter: *"do f1 and
> f3"*). The fixes are recorded at the end of each finding below; the verdicts
> above are left as they were written, because a findings doc that edits its own
> history stops being evidence. ⚠️ **F1's fix deliberately departs from the
> remedy proposed here** — see its disposition for why "skip on inconclusive"
> would have reintroduced the loss.

---

## T1 — IRREVERSIBLE GATES — **UNSOUND**

### F1. The archive can still freeze the wrong year, and every instrument is blind at the same time

`src/load_temporal.write_archive(path, current, live_year)` labels its capture
with `live_year`, which is `main.ASSESSMENT_YEAR` — a **hand-bumped pin**. The
capture is permanent. This is the mechanism that destroyed 2025.

S122 deleted the bad entry. **It did not close the door.** Three things have to
hold for the door to be shut, and none does during the annual FIR-lag window:

**(a) The freeze rule does not protect the pinned year — it overwrites it.**
Reproduced against the real function on a temp file:

```
write_archive(p, frame(2026, 1_000.0), 2026)   -> years['2026'] = 1000.0   (correct capture)
write_archive(p, frame(2026, 9_999.0), 2026)   -> years['2026'] = 9999.0   (overwritten)
```

The docstring's *"a year already archived is never rewritten"* is true of
**other** years (`frozen` excludes `live_year`); the pinned year's entry is
reassigned unconditionally every run, by design, so the live year's snapshot
improves as the roll fills in. Under a **stale pin**, that same line writes the
*new* roll over a *correct* archived year, weekly, silently.

**(b) The FIR guard cannot detect the year that causes this.** `detect_year`
ranks our residential base against `filed_bases()` — years **Alberta has
filed**. Alberta files months after Edmonton rolls. Simulated against the real
anchor (`data/fir_tax_base.json`, 2023–2026) for a 2027 roll arriving before
FIR files 2027:

| next-year revaluation | `detect_year` | workflow outcome |
|---|---|---|
| +2.0% | **2026** | **ALIGNED — wrong year archived, guard confirms it** |
| +4.0% | **2026** | **ALIGNED — wrong year archived, guard confirms it** |
| +6.0% | `None` | inconclusive → warning → **proceeds, archives under the stale pin** |
| +8.3% | `None` | inconclusive → warning → **proceeds, archives under the stale pin** |
| +12.0% | `None` | inconclusive → warning → **proceeds, archives under the stale pin** |

**There is no revaluation rate at which the archive is protected.** Edmonton's
own filed history spans both branches (2024 **+2.40%** → the false-green branch;
2025 **+10.18%**, 2026 **+8.27%** → the inconclusive branch). ⚠️ **The ≤5% branch
is worse than the metadata era**, because the guard returns a confident green
rather than an unread string.

**(c) `refresh.yml` treats "cannot tell" as "proceed", for a step that cannot be
undone.** Exit 4 emits `::warning::` and leaves `result` un-`hold`, so
`check_temporal_years.py --write-archive` runs. That is **correct** for
regenerating `web/data` — recomputable output should not be held hostage to an
unpublished FIR year — and **wrong** for the freeze. The two share one gate,
and the gate was sized for the recomputable one.

**And the after-the-fact detector inherits the same blind spot.**
`check_temporal_archive_year` uses the same `detect_year` over the same
`filed_bases()`, so during the window it returns UNKNOWN or a false green for
precisely the entry that is wrong. Meanwhile `check_assessment_roll` correctly
reports ❓ (the coverage string is untrustworthy — locked 2026-08-25). **Every
instrument is silent at once, and for one reason: they all depend on somebody
else having published the new year.**

**Failure scenario, concrete:** January 2027, roll advances to 2027, pin not yet
bumped. The Monday refresh overwrites the good 2026 archive entry with 2027
data. Repeats weekly. The digest says ❓ and ✅. When FIR finally files 2027,
`check_temporal_archive_year` goes red — and 2026 is gone, because the roll
carries one year and 2026 is no longer it. **Identical to the 2025 loss, one
layer down.**

**Evidence that would change this verdict:** proof that FIR files before the roll
advances (the anchor's own history says otherwise), or that the pin cannot be
stale across a refresh (S119 records it stale for months).

### ✅ F1 — FIXED 2026-08-28, and NOT the way this doc proposed

The proposal above — *skip the capture on inconclusive* — **was wrong, and
writing it out is what showed why.** Alberta files FIR months after Edmonton
rolls, so "skip until proven" leaves the archive empty through the whole lag
window; a January where Alberta ran late would cost a year outright. **That is
the very loss this mechanism exists to prevent** — the remedy would have
re-opened the hole from the other side.

What shipped instead separates the two things that were conflated. **The data
is irreplaceable; only the label was ever wrong.** So:

- `write_archive(..., confirmed=)` takes whether the caller **measured** this
  capture to be `live_year`. It **always writes** — but it **refuses to
  overwrite an entry already recorded as confirmed** with an unconfirmed one.
  Unproven ≠ wrong; an unproven capture still keeps improving weekly, and is
  upgraded in place the moment FIR lands.
- `check_temporal_years._capture_measures_as()` measures the **frame about to be
  written** (not the CSV, not the pin, not a coverage string) and **reuses
  `detect_year`** rather than comparing locally — the S122 lesson that a
  duplicated comparison is a bypassed decision.
- `data/temporal_archive.json` gains `_year_confirmed`, backfilled from
  `check_temporal_archive_year.py`'s own re-derived verdict rather than
  asserted (`{"2026": true}`; the guard reports `+1.2%`, ok).

⚠️ **The regression test was falsified against the old logic on the DEFECT, not
the signature** — the pre-fix function was given the new keyword and left
otherwise untouched, and the test then fails on `assert (2026 is None)`, i.e.
on having archived where it should have refused.

**Verified end to end on the real roll**, not only by unit test:
`Archive year CONFIRMED: the capture measures as 2026 (residual +1.17%)`.
⚠️ That run also re-captured from this box's **older local CSV** and would have
committed a downgraded archive — restored, and worth knowing before anyone runs
`--write-archive` locally.

**What this does NOT fix:** if the pin is stale *and* the archived entry was
never confirmed, the overwrite still happens. Nothing today is in that state,
and protecting an unproven entry against another unproven one has no principled
winner.

---

## T2 — PUBLISH GATES — **SOUND, one stated proxy, one cleared**

All nine `CHECKS` members and all nine `scripts/check_*.py` classified. Every
one measures its subject except the two known, documented cases:

- `check_assessment_roll` reads the coverage string — **handled correctly**: it
  routes through `check_alignment()`, downgrades to ❓ and names
  `check_roll_year_against_fir.py` as the authority. A stated proxy, not a
  hidden one.
- `check_temporal_archive` answers *was it captured*, not *is it right* —
  already documented as such, with `check_temporal_archive_year` as its
  correctness sibling.

**Cleared, recorded so the next run does not re-litigate it:**
`export_budget_ranked.py`'s vintage reads Socrata's **`rowsUpdatedAt`**
(`2026-06-05`, agreeing with the committed `budget_ranked.json`). This is
platform-emitted on write, **not** hand-typed prose like `Period of Coverage` —
a different thing, correctly used. `check_capital_budget` is the model
implementation for the whole class: it explicitly refuses `Last-Modified`
because it merely echoes `Date`, and content-hashes the body instead.

---

## T3 — WIRING — **UNSOUND (two instances, one fixed)**

### F2. `deploy.yml` did not trigger on the script that shapes the artifact — FIXED

Found and fixed 2026-08-28 (PR #262) before this sweep began; counted here
because it is the instance that motivated it. The filter read *what lives under
`web/`* as a stand-in for *what changes the served artifact*, so a
`scripts/build_site.py` change merged green and deployed nothing.

**Swept for siblings: none.** `deploy.yml` is the only workflow with path
filters; `refresh.yml` and `vintage-digest.yml` are cron-only.

### F3. Nothing runs the test suite on a change — **UNSOUND, and new**

`pytest` appears in **exactly one place**: `refresh.yml`, a **weekly cron**
(Mondays 08:00 UTC). There is no `pull_request` workflow and no `push`
workflow that runs tests. `master` is **not protected** — the API returns
`Branch not protected`, so there are no required status checks.

Consequences:

- **`deploy.yml` publishes to the live site on every push to `master` with zero
  test execution.**
- "746 passed" in a PR body is a claim about the author's machine. Nothing
  measures the **merged** state — the exact substitution this class is about,
  and the one I made three times today without noticing.
- A test failure introduced on a Tuesday surfaces the following **Monday**, as
  a **held data refresh**: the symptom is a stale map, not a red check on the
  change that caused it.

**Honest mitigation, stated because it is real:** the placement inside
`refresh.yml` is correct — `pytest` runs *before* download and regeneration, so
a broken suite holds the data path rather than corrupting it. The gap is that
it is a **release gate, not a merge gate**. For a repo whose failures are
silent-correctness failures and whose guards live in `tests/`, a week of
unverified `master` is the wrong side of the trade.

### ✅ F3 — FIXED 2026-08-28

`.github/workflows/tests.yml`: `pytest tests/ -q` + `check_doc_citations.py` on
`pull_request` and `push: master`. Offline and secret-free by construction — a
merge gate that can go red because Socrata is down is one people learn to
ignore, which is worse than no gate; a test asserts no `secrets.` reference.

⚠️ **`refresh.yml`'s own pytest step stays, and a test pins that too.** They
gate different things — this one the change, that one the weekly data publish
(running before download + regeneration, so a broken suite holds the data path
rather than corrupting it). The tempting cleanup after adding a merge gate is
to delete the "duplicate".

⚠️ **STILL OPEN, and only Peter can do it: branch protection is OFF.** The gate
now *reports* on every PR, but with `master` unprotected nothing *blocks* a
merge on a red one. That is a repo-settings change, not a code change. Until it
is on, this converts a silent gap into a visible signal — which is most of the
value, but not all of it.

---

## T4 — DISPLAY — **UNSOUND**

### F4. Fifteen hardcoded activity-window labels, and the procedure that rolls them mentions none

`main.py` pins `FIRE_YEARS = (2023, 2024, 2025)`,
`PERMIT_YEARS = (2021…2025)`, `PERMIT_YEARS_RECENT = (2023, 2024, 2025)`.
Fifteen user-facing strings in `web/index.html` restate those ranges as
literals, none derived:

| what | sites |
|---|---|
| `DEV_WINDOW_LABEL` (one map → 5 render sites: tooltip, legend, peek card, two readouts) | 1907 + 4898, 4908, 5692, 5712 |
| `DEV_WINDOW_PHRASE` + its fallback | 1285, 1286, 1287, 1299 |
| window button tooltips | 230, 231, 232 |
| fire copy (`2023–2025`) | 316, 348, 767, 924, 5593 |
| lens title + blurb (`2021–2025`) | 1075, 1078, 1110 |

**All are correct today** — the pins have never rolled, because the project is
younger than one year-roll (`git log -S` puts both the pins and the labels at
their original commits). **They are scheduled to be wrong in January 2027.**

`docs/RUNBOOK.md` §1 step 4 walks the bump: three pins, plus the
construction-price deflator re-run, plus the note that `PERMIT_YEARS_LONG` is
derived and needs no edit. **It does not mention `web/index.html` at all.** The
digest's `check_window_pins` watches the *pins*; nothing watches the *labels*.
Step 4's reassurance that *"a stale pin hard-errors via the drift guard, so this
can't be missed silently"* is true of the pin and **false of all fifteen
strings** — they will silently label 2022–2026 data as 2021–2025.

⚠️ **This is the `(2024 n/a)` defect (S122) at 15× the size, and the same tell is
present: correctly-derived copy sits beside it.** Lines 6776–6778 read
`data_year` / `rate_year` / `zoning_year` straight from `status.json`.

**Why it is not a one-line fix:** `status.json` carries no activity window, so
the browser cannot derive these today. Closing it means `generate_status.py`
publishing the three windows — an **output-schema change**, so it is proposed,
not built. The cheap partial (a RUNBOOK line + a test pinning label against
pin) is also left for Peter, because a half-fix that makes step 4 look complete
is its own hazard.

---

## T5 — TESTS — **CONDITIONAL**

### F5. `test_refresh_workflow_gates_every_publish_step_on_both_guards` checks consistency, not coverage

Its body collects steps whose `if:` **already mentions** `yearcheck` and asserts
each also mentions `rollyear`. A new publish step with **no `if:` at all** is
invisible to it, while the name promises the opposite.

**CONDITIONAL rather than UNSOUND:** today's ungated steps (the data commit, the
site build) are ungated **deliberately** — both must run during a hold to ship
the banner — so coverage is correct right now and the test's weakness is
latent. Sound only while someone reads the workflow when adding a step.

---

## What this sweep did not cover

- `web/index.html` literals **other than** vintage/window strings (thresholds,
  counts, anchors) — the S102/S103/S104 citation sweeps covered the doc-backed
  subset; unbacked numeric literals remain unswept as a set.
- Front-end code paths: no `verify-*.js` script asserts a label against a
  served pin, and adding one was not attempted here.
- The 2026-08-25 stale-metadata downgrade is taken as given, not re-derived.

# Findings — the guard corpus's CHANNEL and TRIGGER layer (2026-09-16, S165, Opus 5)

**Instrument:** S164 §5.3, the "third-question sweep". Prior runs
(`FINDINGS_vacuous_guards.md`, `_r2.md`) asked **question 1 — does it fire on a
defect.** This run asks only:

- **Q2 — can the trigger actually occur on this repo?**
- **Q3 — does anyone read the output when it does?**

**Target scoping note.** The skill asks for one target. This one is a *layer*
(the channel-and-trigger seam across 13 `check_*.py`, 13 digest checks, 43
`verify-*.js`, 4 workflows) rather than one artefact — the same shape as
auditing CRS across every module. It is one pass, not a sweep of each guard.

⚠️ **Self-audit caveat, stated up front.** Opus 5 wrote several of these guards
and, earlier in this same session, reversed an S164 finding that had proposed
deleting one. `measurements-that-favour-me` applies. The one HIGH finding below
is therefore stated as a falsifiable mechanism with its own disconfirming
evidence named, and **one hypothesis I formed during the run is recorded as
FALSIFIED in §3** rather than dropped.

## 0. Verdict

| | |
|---|---|
| **HIGH — 1** | The authoritative roll-year guard's BLIND states have no reader, and one of them occurs **by construction every January** (§1) |
| **LOW — 1** | `refresh.yml`'s inconclusive message names the wrong cause, every week (§2) |
| **Swept clean** | §3 — including one hypothesis of mine that measured false |
| **Not covered** | §4 |

---

## 1. HIGH — the roll-year guard goes blind every January, and says so only into a log

### The guard, and why it is the authority

`check_roll_year_against_fir.py` measures our residential taxable base against
what Edmonton filed with Alberta (FIR Schedule MR). It is **the** roll-year
authority, and the repo says so in three places, because its sibling cannot do
the job: `check_year_alignment.py` reads Socrata's `Period of Coverage`, which
Edmonton has left reading **2025 through the entire 2026 roll**
(`DATA_ISSUES.md` issue 1), so that guard is **permanently `inconclusive` by
design**. Verified on the live run `34857405723` (2026-09-14, green):

```
##[warning]Year-alignment check inconclusive (metadata fetch/parse failed) — proceeding as aligned.
```

**What it is guarding is the most expensive defect this project has recorded:**
a roll that moved while `ASSESSMENT_YEAR` did not, billing a 2026 roll at 2025
rates — **~$69.5M understated (S119)**.

### Its three blind states, and what each emits

| blind state | exit | `refresh.yml` case block does | channel |
|---|---|---|---|
| roll CSV absent (`data/raw/…Current_Calendar_Year_.csv`) | `EXIT_OK` (0) | `0) ;;` — **nothing** | `logger.info` |
| FIR anchor absent (`data/fir_tax_base.json`) | `EXIT_OK` (0) | `0) ;;` — **nothing** | `logger.warning` |
| no FIR year fits | `EXIT_INCONCLUSIVE` (4) | `echo "::warning::…"` | Actions log |

**None of the three files an issue. All three publish.** In every case the
pipeline proceeds, commits, and deploys, and the run is **green**.

⚠️ Note the first two report **success**, not inconclusiveness — `result=skipped`
and exit 0. A guard that cannot measure is indistinguishable, at the workflow
level, from one that measured and was satisfied.

### Q2 — the trigger occurs, annually, and it is calculable

Not hypothetical and not rare. From `data/fir_tax_base.json` (fetched
2026-08-25), Edmonton's filed residential base grows:

| year | vs prior |
|---|---|
| 2024 | **+12.0%** |
| 2025 | **+9.6%** |
| 2026 | **+9.9%** |

And the guard's own thresholds are `MAX_PLAUSIBLE_RESIDUAL = 0.05` (5%) with
`MIN_SEPARATION = 0.03`.

**So when the roll rolls to 2027 in January, our measured base will sit ~10%
above FIR's 2026 filing — twice the 5% tolerance — and Alberta will not have
filed 2027 yet** (`RUNBOOK.md` §0: *"Alberta files FIR months after Edmonton
rolls"*; the anchor currently holds 2023–2026). No year fits. `detect_year`
returns `None`. **The guard returns INCONCLUSIVE in the first weeks of January,
every January, which is precisely the window it exists to cover.**

That is not a failure of the guard — going inconclusive there is *correct*
behaviour. The defect is that its correct answer reaches nobody.

### Q3 — and the one channel that does reach a human says "not an action"

The `::warning::` lands in the log of a **green** weekly run. That is the exact
channel `CLAUDE.md` names as *"this project's standing failure mode — a working
guard on a channel nobody reads"*, the one that let `_classify` warn about
`Alley-Commercial` on every pipeline run for ~70 days.

**It is worse than silence, because the digest actively stands the reader down.**
`vintage_report.check_assessment_roll` reports `❓ UNKNOWN` every month (correctly
— the Socrata string is untrusted) and tells Peter:

> The authority is `scripts/check_roll_year_against_fir.py` … **this digest
> cannot run it** (it needs the raw roll, which is not committed). **Not an
> action unless that guard disagrees.**

In January the guard does not *disagree* — it is **blind**, which the digest's
wording does not distinguish from agreement. So the monthly issue, the only
channel that emails a human, says stand down, while the authority it defers to
has gone dark and cannot be consulted from there. `data/raw/` holds only
`.gitkeep`, so the digest's inability to run it is structural, not incidental.

### The fix already exists in this repo, one file over

`check_revenue_deltas.py` hit the identical problem and solved it — its comment
is the argument for this finding, written by the project about itself:

> The direction policy still holds — this guard never stops a publish. But it
> must not report the all-clear it did not measure either, and **a warning
> inside a green run reaches nobody** (the whole reason the flagged path files
> an issue). So a fault goes out through that same channel.

It emits `flagged="fault"` with the title *"⚠️ Revenue-delta guard could not
read its baseline"*, and `CLAUDE.md` calls that *"the louder of the two"*.

**Proposed fix (not taken unasked — it changes CI behaviour):** give the
roll-year guard's three blind states the same escalation. A `roll-year-blind`
issue, **deduped like `clamp-drift`** rather than per-event like the delta
issue — a blind guard is a persistent *state* that recurs weekly until the FIR
anchor is refreshed, not a transient event. Then soften the digest row from
*"not an action unless that guard disagrees"* to distinguish **disagrees** from
**could not answer**.

**What would change this verdict:** evidence that a January inconclusive is
caught by something else before publish. I did not find one — `RUNBOOK.md` §1 is
a *manual* checklist a human opens, which is the thing a guard exists to stop
depending on.

---

## 2. LOW — the weekly warning names a cause that is not the cause

`refresh.yml`'s case block hardcodes one message for exit 4:

```
4) echo "::warning::Year-alignment check inconclusive (metadata fetch/parse failed) — proceeding as aligned." ;;
```

But `check_year_alignment.py` returns `EXIT_INCONCLUSIVE` from **two** branches:
a genuine fetch/parse failure (L175), and the `stale-metadata` branch (L184) —
where the fetch *succeeded* and the field is simply untrustworthy. The live
2026-09-14 run shows both lines, and they contradict each other:

```
WARNING: Year-alignment check INCONCLUSIVE — Socrata reports the roll as 2025 but it is 2026 …
##[warning]Year-alignment check inconclusive (metadata fetch/parse failed) — proceeding as aligned.
```

The second is false: nothing failed to fetch. **Low severity only because the
channel has no reader anyway** (§1) — but if §1's fix gives it one, this message
becomes actively misleading and should be fixed first. The script already prints
the right cause; the workflow should surface the script's message, not its own.

---

## 3. Swept clean — falsified, not assumed

- ⚠️ **MY OWN HYPOTHESIS, MEASURED FALSE.** On reading `refresh.yml` I believed
  the `hold` mechanism could not engage: nine steps gate on
  `steps.yearcheck.outputs.result != 'hold'`, and **no `$GITHUB_OUTPUT` write
  appears anywhere in the workflow**. That would have made every gate vacuously
  true and the banner path dead — a finding larger than §1. **It is wrong.** Both
  scripts write `GITHUB_OUTPUT` themselves (`_write_github_output`, 7 call sites
  across the two). Recorded because the sweep's whole subject is inferring a
  channel's existence from the wrong file.
- **`check_temporal_archive_year.py` appears in no workflow** — this looked like
  an unwired guard. It is wired through `vintage_report.CHECKS` (the digest), and
  `tests/test_ci_workflows.py:101` exists specifically to pin that wiring. Clean.
- **The `hold` → banner path has a real reader**: the live site. Not a log.
- **`check_suite_share.py`** has no `set +e`, so a non-zero exit fails the
  workflow and blocks the publish. Real channel.
- **Merge-gate guards** (`check_doc_citations`, `check_cost_copy`,
  `check_decisions_log`) block a PR — the reader is whoever cannot merge.
- **41 of 43 `verify-*.js` have no automated caller** (only `verify-smoke.js` and
  `verify-temporal.js`, in `refresh.yml`). **Not re-filed as new** — this is
  `FINDINGS_vacuous_guards.md` **V3**, already reported and sharpened in S146.
  The counts have moved since (V3 read 42 scripts / 1 in CI); the structure has
  not.

## 4. Not covered by this run

- The 13 digest checks were taken one level deep (registration in `CHECKS` +
  the issue channel), not per-check for Q2.
- `deploy.yml` and `tests.yml` were read for channels only.
- **Q1 (does it fire) was deliberately not asked** — that is the prior runs'
  ground, and nothing here re-measures their verdicts.
- No guard was mutated. This run reads wiring; it does not falsify detection.

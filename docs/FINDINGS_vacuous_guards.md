# Findings — checks that cannot fail (run 2026-09-07, S144)

Instrument: `docs/FABLE_AUDIT_vacuous_guards.md`. Ledger row: 2026-09-07.
Scope as the brief defines it: the guard/test estate and the wiring that runs
it — **not** the lenses.

**Two defects found, both reproduced by falsification. One structural gap. Three
tiers came back clean and are recorded as such.** ⚠️ **Two claims I formed
mid-run were WRONG and were dropped before publication** — §6 records them,
because an audit of unfalsifiable checks that does not falsify its own claims is
the joke telling itself.

---

## V1 — `check_cost_copy.py` can be satisfied by a code comment  (T1, HIGH)

**The check:** every rate a lens blurb states in prose must match
`data/city_unit_costs.json`. It runs on the **merge gate**, and it is the *only*
thing tying the map's rates to its captions.

**Why it cannot fail as intended:** it tests `expected in html` against the raw
file text. It has **no locality** — it constrains that the string exists
*somewhere* in a 7,300-line file, not that it appears in the copy a reader sees.
`web/index.html` is heavily commented by house style, so any comment mentioning
a rate satisfies the check permanently.

**Falsified 2026-09-07.** Reverted the roads blurb to the retired `$1,285` and
added one ordinary-looking comment containing `$5,970`:

```
ok    Roads cost (operating) — maintenance $/km/yr    $5,970
OK — all 7 quoted rates match city_unit_costs.json
```

**The guard passed while the public blurb displayed a rate the project retired
the day before.** ⚠️ This is not hypothetical: the 2026-09-06 re-scope added
several comments naming rates, and a `$5,970` in any of them would have disarmed
the check silently and permanently.

**Blast radius:** T1. A wrong public rate merges and `deploy.yml` publishes it
minutes later. This is the project's cardinal failure mode, and this guard is
the only thing standing in front of it.

**Fix:** strip comments before matching, and give the check locality — match
within the blurb string literals and the `#about-*` prose, not the whole file.
⚠️ **Add the falsification as a test** (`check_cost_copy` has **no test file at
all** — see §5), so the fix itself cannot rot back.

---

## V2 — the acre constant can be halved with all 784 tests green  (T5, HIGH)

**The property:** `SQ_M_PER_ACRE` converts every area in the project. Value per
acre is the headline published number.

**Falsified 2026-09-07.** `src/load_boundaries.py`, `4046.856422 → 2023.428211`
— **doubling every published per-acre figure**:

```
784 passed in 12.28s
```

A subtler `→ 4000.0` (1.2% error) is likewise green. **No test pins the
constant, and no test would notice it moving.**

**Why:** `tests/test_export_value_grid.py` does
`from export_value_grid import SQ_M_PER_ACRE` and then computes its **expected
values with it** — roughly forty assertions of the form
`f(SQ_M_PER_ACRE) == expected(SQ_M_PER_ACRE)`. Both sides move together. This is
the class in its purest form: the tests read the right constant, in a scope
where it cannot differ from itself.

⚠️ **`tests/test_load_roads.py` does it correctly** — it hardcodes
`4046.8564224` — which is why that module's conversion *is* pinned. The estate
already contains the fix; it was simply never applied here.

**Blast radius:** T5, but the *consequence* is T1-shaped — a silent multiplier
on the public headline metric.

**Fix:** one test asserting the literal
(`assert SQ_M_PER_ACRE == 4046.8564224`), in both modules that define it.

**Noted while there, not a defect:** the constant is defined **twice** with
different precision — `load_boundaries.py` `4046.856422` vs
`export_value_grid.py` `4046.8564224` (the exact international acre). The
difference is **9.9e-11 relative** and changes no published figure. It is
duplication worth removing, *not* a correctness problem, and is recorded that
way so a later reader does not inflate it.

---

## V3 — no browser check gates any merge  (T2/T4, structural)

Paired with the ledger's open item *"the verify scripts gate nothing"*, which
this run also corrects factually: the estate is **42 `verify-*.js`**, inside a
directory of 65 `.js` (42 verify + 17 shot + 6 misc). The "65 verify scripts"
phrasing conflates the two.

**What actually gates what:**

| gate | trigger | runs | browser check |
|---|---|---|---|
| `tests.yml` (`test`) | PR + master push | pytest, `check_doc_citations`, `check_cost_copy` | **none** |
| `deploy.yml` | master push → **publishes** | `build_site.py` | **none** |
| `refresh.yml` | weekly | pytest + 6 `check_*.py` | `verify-smoke.js`, **both builds** |

✅ **The merge gate itself is sound and I confirmed it** — branch protection
requires context `test`, which matches the job id in `tests.yml` and reports on
master. No PR merges without those three green.

⚠️ **But `test` contains no browser check.** **1 of 42** verify scripts runs in
CI, only in the weekly refresh. So a rendering regression merges and publishes,
and the earliest automated notice is **Sunday** — which is exactly how four
scripts sat red on master from 2026-09-02 until S140 noticed by hand.

Two further facts, reported without recommendation: `enforce_admins: false`
(an admin merge can bypass the required check) and `strict: false` (a PR need
not be current with master before merging).

**Also:** `scripts/check_temporal_archive_year.py` appears in **no workflow**.
Its 13 tests pass; nothing runs the guard itself.

---

## V4 — the early-exit class, and the data-vs-build trap inside it  (T4)

**14 early exits across 10 of the 42 scripts** leave the script's body unrun and
still `process.exit(0)`. ⚠️ **The literal `check(name, true)` in those branches
is not the defect** — it reports that a branch was taken. The defect is that the
script then prints a pass line and exits 0, **indistinguishable from a full
run**, which is §1's collapse of three states into one exit code.

**Measured against the PUBLIC build — which nothing has ever run them against:**

| script | exit | checks run |
|---|---|---|
| ⚠️ `verify-bike.js` | 0 | **3 of 37 (8%)** |
| ⚠️ `verify-transport-cost.js` | 0 | **5 of 29 (17%)** |
| ⚠️ `verify-transit.js` | **1** | 24/26 |
| ⚠️ `verify-ind-permits.js` | **1** | 25/26 |
| `verify-peek.js` | 0 | 33/38, **219 s** |
| 5 others | 0 | 84–96% |

**The two reds share one cause, and it is a defect this project has already
found once.** Their early-exit guards are **DATA**-gated, not **BUILD**-gated:

```js
// verify-transit.js — DATA
const hasTransit = ... f.properties.transit_dep_per_acre != null;
// verify-bike.js — BUILD (correct)
const bikeReachable = ... getComputedStyle(row).display !== 'none';
```

⚠️ **Both builds serve the same GeoJSON.** The column is present on the public
build, so a data-gated guard never fires there; the script falls through to
assert a row that the public build deliberately hides, and reds on a **correct**
build. `verify-ind-permits.js` fails identically ("industrial button shown …
when column present").

**This is precisely the trap S143 found in `hoodPanelLens()`** — gating on
`state.hasSvcCost`, a data flag, where the public build carries the column and
hides the UI. It was fixed in the app and **left unfixed in the harness**.

⚠️ **The sibling inconsistency is the sharpest single fact here:** the same
situation — a full-only service hidden on the public build — produces a **silent
pass in `verify-bike.js`** and a **failure in `verify-transit.js`**. Both are
wrong, in opposite directions, and neither is visible because nothing runs these
against the public build.

**Fix, in order:** (1) gate every early exit on a BUILD condition; (2) make the
scripts print `ran N of M` so a partial run cannot read as a full one; (3) run
the estate against **both** builds, which is the only reason these were found.

---

## §5 — Tiers that came back clean (falsified, not assumed)

- **`check_served_columns.py` — clean.** Five `test_main_fails_*` tests exercise
  the failure path directly (dropped column, half-written column, absent file,
  empty collection). ⚠️ My first keyword scan scored this guard `0` for
  negative-path coverage and was **wrong**; the finding is that the scan was
  crude, not that the guard is weak.
- **CRS on the boundary path — clean.** `3400 → 4326` reds
  `test_area_acres_not_in_degrees` and `test_reprojects_to_3400`, by name.
- **The committed unit-cost rates — clean.** Reverting the operating rate to the
  retired `4.635`, or the lifecycle rate to `25`, each reds the test that names
  it.
- **The four assert-less tests are NOT findings.** `test_under_limit_passes` and
  its three siblings assert *"does not raise"*, each marked `# no raise`, and
  they red if the call raises.
- ⚠️ **One real gap in an otherwise clean tier:** `SETBACK_CRS "EPSG:3400" →
  "EPSG:26911"` in `join_and_calculate.py` is **not caught** — the exact
  inconsistency the audit checklist tells auditors to flag. Lower severity than
  V2 (UTM 11N is a valid metric CRS, so areas stay areas), but unpinned.

---

## §6 — What this run got wrong

Recorded because the brief demands it of every run, and because both errors are
this class turned on the auditor.

1. ⚠️ **"`deploy.yml` gates nothing, so anything can ship."** Drafted, then
   checked: branch protection requires `test`, the context matches the job id,
   and it reports. **The merge gate works.** The true finding is narrower — that
   gate contains no *browser* check. Publishing the first version would have
   been a confident false alarm about the project's publish path.
2. ⚠️ **A regex that classified early-exit guards as DATA- or BUILD-gated
   returned `?` for most entries.** Its totals were **dropped, not published**;
   §V4 reports the three data-gated guards confirmed by reading them. An
   instrument that cannot demonstrate a negative is not evidence.
3. **`verify-peek.js` was recorded as a timeout and is not one** — 219 s against
   a 150 s cap I chose. My instrument, not the estate.

⚠️ **`pgrep -f <name>` matched this run's own tooling three times**, once
killing the shell that was about to write a sweep script (`pkill -9 -f
pubsweep.sh` matched the compound command containing that string). The class
under audit kept reappearing in the audit's own instruments — which is the
strongest available argument that it is systemic rather than a list of nine
mistakes.

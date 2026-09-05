# FINDINGS — Front-end architecture decision audit (the `web/index.html` question)

**Run 2026-09-05 (S140) against `docs/FABLE_AUDIT_frontend_architecture.md`.**
Container: `docs/PLAN_frontend_refactor.md`. This is the *output* of that brief:
one verdict per level, the sharpest argument, what to do instead, and the
evidence that would change it. `web/index.html` was not edited. `STACK.md` §9 and
`DECISIONS.md` were — but only *after* Peter made the three owner calls (§10),
not as part of the audit itself, per the brief's §4.

Every number below was either taken from the brief's §3/§3a as instructed, or
measured this session with the command shown. The brief was wrong in three
places, each corrected in §7 — read that section before quoting the brief again.

---

## 0. The precondition, confirmed

**GitHub Pages is not what forces the single file.** `.github/workflows/deploy.yml`
feeds Pages from `_site/`, a directory *produced by a build step*
(`python3 scripts/build_site.py --src web --out _site` →
`actions/upload-pages-artifact`). Any bundler's output would land in the same
directory by the same mechanism. The vendored 1.3 MB of deck.gl/maplibre already
proves Pages serves arbitrary static assets. The no-build rule is the *choice*
recorded in `STACK.md` §9 and `security-audit.md` S1 — and §1 below notes that
the rule as written is misnamed, because `build_site.py` *is* a build step.

## 1. Verdicts

| level | verdict | one line |
|---|---|---|
| **0** hand-written at all? | **SOUND** | Generators make the chart this project is not making; the "two standards" gap is static analysis, not tests, and it is addressed at Level 1 |
| **1** no-build + vendoring | **SOUND** | A bundler degrades the S1 posture and buys nothing here — but the rule is drawn **wider than S1 supports** (it forbids read-only checkers it never needed to) |
| **2** one file or modules? | **CONDITIONAL — stay one file** | The measured coupling does not justify a split; the two real defects (a lying navigation aid, sloppy mode) have 5- and 1-line fixes |
| **3** seams, if ever | banner-per-module **UNSOUND** (known); kernel/lens/panel **CONDITIONAL** | Lens↔lens coupling is 3%; the true seam problem is the three dispatchers, and a split without a lens registry moves files, not coupling |
| **4** guard coupling | **CONDITIONAL** | 7 files read the source, not 11; 3 of the 7 exist only because the page duplicates pipeline constants — a served manifest retires them, split or no split |
| **5** sequencing | (moot for a split; the Level-2 remedy is itself the zero-coupling first slice) | `<script type="module">` on the existing block is a zero-edit change to the JS; the coupling it breaks is **39 of 65** harness scripts, not 8 |
| **6** code correctness | one note | 6,748 lines of sloppy-mode JS; no duplicate top-level names today (376 declared, 376 distinct) |

**Highest level UNSOUND: none.** Nothing beneath is mooted; Level 2's verdict is
the decision.

---

## 2. Level 0 — hand-written: SOUND

**Sharpest argument against.** The data half is a reproducible pipeline with
784 tests, guards and pinned versions; the presentation half is a hand-edited
file with no types, no import graph and no static check. Two engineering
standards in one repo, and the untyped half is the one that prints the dollar
figures.

**Why it holds anyway.** The generator alternatives (Observable, Quarto,
Datasette, kepler.gl, Python templating) produce charts, tables and
config-driven maps. What this page is: nine lenses dispatched through
`applyView` (which names all nine, 54 times, in 244 lines), a revenue panel and a
budget panel that reach into the lenses (65 chrome→lens edges), an uncertainty
band with three sections of its own rendering rules, a label sweep, a
hover/touch seam, and a two-build gate. None of that is a config surface any
listed generator exposes; templating it from Python yields the same hand-written
JS under a `.j2` extension. And the "two standards" claim overstates the gap: the
65 Playwright scripts in `tools/profiling/` *are* the presentation half's test
suite, and they gate the weekly publish (`verify-smoke.js` in `refresh.yml`).
What the front end lacks is **static analysis**, and that is a Level-1 question.

**What I would do instead.** Nothing at this level.

**What would change the verdict.** A lens that is expressible as a kepler.gl (or
equivalent) config with no custom code. Test it on Money — the default lens —
before believing it; the revenue panel and the band are the parts that will not
fit.

## 3. Level 1 — no build step, vendoring: SOUND, with the rule's scope corrected

**Sharpest argument against.** The no-build rule forces the two-build fan-out to
work by regex-rewriting a JS literal inside a 424 KB file
(`build_site.py::set_default_build`), guarded by a hard-fail on "exactly one
match" — and that guard has already broken a deploy once when a *comment*
tripped the companion base-tag check (commit `2026-07-30 fix(web): a comment
tripped build_site's base-tag guard`). With a bundler that is an env var.

**Why it holds anyway.** The question the brief asks is whether a build step
*degrades the supply-chain posture S1 bought*, and the answer is yes: a bundler
replaces "three files with recorded SHA-256s, cross-verified against two CDNs"
with "whatever esbuild/vite emitted from a lockfile of transitive packages,
executing on a GitHub runner at publish time." It would buy the three things
bundlers exist for — npm dependencies, TS/JSX transpile, minification — and this
project has two dependencies (vendored), no TS/JSX, and page runtime is out of
scope. Cost: exactly what S1 paid to remove. Benefit: none the project has asked
for. The regex mechanism is the *price*, and it is a small one with a test
(`tests/test_build_site.py`) on it.

**The correction.** The rule is misnamed and over-scoped:

- *Misnamed:* `STACK.md` §3 itself calls `build_site.py` "the one build step".
  There is a build step; it is stdlib Python, and it does not execute anything
  on the page. The rule that S1 actually justifies is **"no JS toolchain in the
  publish path."**
- *Over-scoped:* `STACK.md` §9 records "no linter config in CI beyond the
  tests" under the same heading. S1 constrains **what executes on the page**. A
  type-checker or linter run in `tests.yml` (`tsc --checkJs --noEmit`, or
  eslint) reads the source and writes nothing to `_site/`; the served bytes are
  identical with or without it. The security argument is being used to forbid
  something it does not cover — and that something is the exact remedy for
  Level 0's "two standards" argument.

**What I would do instead.** Keep the rule for the publish path, rename it to
what it means, and make the read-only-checker question a separate decision.
**That decision is the owner's (brief §4 call (a)).** Note it *also* adds a
`node_modules` — under `tools/profiling/`, where one already exists for
Playwright, so the dev-side supply chain is not new.

**What would change the verdict.** A third runtime dependency the project cannot
vendor, or a decision to ship TypeScript. Neither is on the backlog.

## 4. Level 2 — one file or modules: CONDITIONAL, stay one file

This is the decision. Both sides, then the verdict.

### 4.1 The case for splitting, as sharp as the evidence allows

1. **The navigation aid lies about the most important 1,600 lines.** The brief
   knew the banners are in build order; it did not know how badly. `CODEMAP.md`
   attributes `applyView` (in-degree 13) and `refreshLegend` (14) — the view
   dispatcher and the legend dispatcher — to *"the citywide budget panel
   (EXPERIMENTAL, full build only)"*. Its last symbol row reads
   **`applySvcDriver` | 6808–7345** — a 538-line range for a ~13-line function,
   because the boot (`map.on("load", async () => …)` at line 6818, ~527 lines),
   **41 of the page's 43 `addEventListener` sites**, and all 10 capability
   flags are an anonymous callback with no indexed symbol. A reader who trusts
   the codemap looks for the boot and every control binding under an
   experimental full-only banner, and finds a row that names the wrong
   function. This is not new: at stage 1 (commit `a24aa91`) the same tail —
   1,555 lines — sat under *"temporal lens"*. **The last banner always absorbs
   the boot, whatever it is called.**
2. **Sloppy mode.** `grep -c "use strict" web/index.html` → 0. In a classic
   script, `typo = value` creates a global silently and a duplicate
   `function f` silently replaces the first. Neither is loud. (Today: 376
   top-level declarations, 376 distinct names — the second hazard has not fired
   yet.)
3. **Growth.** 3,305 → 6,748 JS lines in five weeks (brief §3b).

### 4.2 The case for staying, from the same measurements

1. **The lenses are already independent.** Classifying `CODEMAP`'s 852 edges by
   the section class of each endpoint (kernel = tunables/Lab/base map/loading
   overlay/reference layers; chrome = the two panels + services views; lens =
   the rest):

   | edge class | n | share |
   |---|---|---|
   | same section | 325 | 38% |
   | chrome → kernel | 206 | 24% |
   | kernel → kernel | 76 | 9% |
   | chrome → lens | 65 | 8% |
   | chrome → chrome | 57 | 7% |
   | lens → kernel | 53 | 6% |
   | **lens → lens** | **28** | **3%** |
   | kernel → chrome / kernel → lens / lens → chrome | 23 / 17 / 2 | 5% |

   Of the 28 lens→lens edges, **22 are inside the uncertainty-band trio**
   (*two tiers* ↔ *the same doubt* ↔ *institutional band*) plus deviation —
   one concern that happens to carry three banners. The lens layer would
   survive a file split cleanly, which is another way of saying **the file is
   not what couples it.** (Method: `tools/codemap.py`'s own `collect()` +
   `reference_graph()`, classified in a 30-line script; the regex-graph caveat
   in `CODEMAP.md` applies.)
2. **The growth is appended, not entangled.** Sections that existed at stage 1
   are flat or smaller: tunables 183→263, reference layers 652→804, services
   view 583→**307**, Infill 215→**130**, base map 197→**15**. The doubling is
   two panels (revenue 1,270; budget 1,601 incl. the boot tail) and four new
   lens sections. New things were added next to old things; old things did not
   grow around them.
3. **The public build runs almost none of the experimental code.** The whole
   6,748-line script executes **9 top-level statements** at load (3 tunables,
   2 loading overlay, 2 revenue panel, 2 budget-panel-section — one of which is
   the boot itself). Everything else is declarations. Experimental full-only
   code is inert in the public build unless it fails to *parse* — and a
   SyntaxError in one ES module fails the whole module graph exactly as it
   fails one script today. **Blast radius does not change with a split.**
4. **The regression record does not implicate the file.** Of 165 commits to
   `web/index.html`, 30 are fix/revert. Three are cross-lens leaks
   (`2026-08-05 the Services lens must not trigger the assessment-history
   panel`; `08-06 the panel gate also killed the card`; `08-16 the hover
   sparkline only rides where the click opens that chart`) — and all three are
   wrong conditions inside **shared dispatchers and gates**, which a module
   boundary would not have separated. Zero are name collisions or accidental
   cross-section references.
5. **The codemap is tested and self-refreshing** (`tests/test_codemap.py`, 5
   tests; the `PostToolUse` hook), and the S79 lesson ("one large slice, not
   many windows") already solved the navigation cost for the parts it indexes
   truthfully.

### 4.3 Verdict: CONDITIONAL — stay one file, on two conditions

The doubling is real, but *where the lines went* decides what it means: they
went to independent appended sections with 3% peer coupling, which are exactly
as navigable in one file as in nine. A split would move 6,748 lines through
39 harness scripts (§6), seven Python guards (§5) and the codemap generator to
put file boundaries around code whose actual coupling — the dispatchers — it
does not touch. Meanwhile the two defects that *are* measured have fixes that
fit in a single small PR:

- **Condition 1 — make the banners truthful.** Three new banners at the tail
  of the script (`// --- controls: wiring ---` before the `addEventListener`
  cluster, `// --- boot ---` at `map.on("load"`, `// --- capability flags ---`
  at line ~7130) and, so the codemap can index it, name the boot: `async
  function boot() {…}` + `map.on("load", boot)`. **This is the only change
  that fixes §4.1 item 1, and a split would not fix it** — modules cut on
  lying banners would carry the lie. Consider also re-titling the budget
  banner, which will then cover only the budget panel.
- **Condition 2 — `<script>` → `<script type="module">`.** The script body
  parses **unchanged** as an ES module (`node --check` on the extracted
  6,748 lines as `.mjs`: OK; no top-level `await`/`this`; no inline
  `on*=` handlers in the markup; no `window.*` assignments). One attribute
  buys strict mode (undeclared assignment → `ReferenceError`), module scope,
  and duplicate-declaration errors — §4.1 item 2, closed for free. ⚠️ **It
  needs one shim**, because module scope hides `state` et al. from the
  harness (§6): `window.__app = { state, applyView, buildLayers, METRICS,
  SERVICES, CHROME_IDS, FULL_BUILD, noHover }` — those eight names cover all
  39 scripts — and a one-line prefix change in each script's `page.evaluate`
  (or a `const {state} = window.__app` line). `node --check` tests parsing,
  not strict-mode *runtime* behaviour; the 65 scripts, run one at a time, are
  the verification. **If a split is ever taken, this is also its mandatory
  first step**, which is why Level 5 is moot rather than deferred.

**What would change the verdict to "split".** Any one of: (a) a second
concurrent author (merge conflicts concentrate in one path — a real cost this
single-author repo has never paid); (b) a regression traced to cross-section
name or scope interference (none in 165 commits); (c) the dispatchers refactored
into a lens registry (§5) — at which point per-lens modules fall out naturally
and the split is a consequence, not a project. Growth alone is **not** on this
list: another appended 3%-coupled panel is not a reason.

## 5. Level 3 — seams, if a split is ever taken: banners UNSOUND, kernel/lens/panel CONDITIONAL

Banner-per-module is already measured dead (brief). The concern-based cut the
brief proposes — kernel / lens layer builders / panels+chrome / reference layers
— **is the right shape** (the lens layer separates at 3%), with two findings the
brief did not have:

- **The dispatchers are the seam problem, not `state`.** `applyView` names
  every lens (glass 10, services 9, money 7, ratio 6, development 6, uses 5,
  infill 5, change 4, deviation 2 — 54 literals in 244 lines); `refreshLegend`
  branches on 8 views in 248 lines; `buildLayers` is the third. Adding a lens
  today edits all three plus the controls plus the markup. A split that leaves
  them as-is produces lens modules whose every addition still edits three
  kernel functions — files moved, coupling unchanged. The prerequisite for a
  split that *means* something is a **lens registry** (each lens exports
  `{ layers, legend, apply }`, the kernel iterates). That is a kernel refactor,
  larger than a file move, and the thing to decide *before* any split.
- **Ten lens-owned symbols are imported by peers** and would move to the
  kernel first: `exemptFrac` (5), `deviationStats` (4), `deviationRate` (3),
  `infillColorAt`, `isUncertain`, `devAcreFrac`, `inDeviationPop` (2 each),
  `DEVIATION_POP`, `deviationRateExempt`, `INST_OUTLINE_COLOR`.
- **24 edges reference a `const`/`let` declared later in the file.** Harmless
  in one script (all inside function bodies that run after boot); a TDZ hazard
  if modules are ever ordered by source position with a cycle.

`state` itself: the brief's §3a stands (re-verified S139, all eight escape
patterns zero) — `export const state` from a kernel module, imported read-only.

## 6. Level 4 — the guard coupling: CONDITIONAL

**The count was wrong, and the two files named as "scanning the HTML" split
one-and-one.** Measured by grep for a read (`read_text` / `open` /
`readFileSync`), not a mention:

| file | reads `web/index.html`? | what for |
|---|---|---|
| `scripts/build_site.py` | yes | `DEFAULT_BUILD` / `BUILD_STAMP` regex — the fan-out mechanism |
| `scripts/check_cost_copy.py` | yes | rates **in prose** vs `data/city_unit_costs.json` |
| `scripts/check_doc_citations.py` | yes | `.md` citations — any text file, indifferent to a split |
| `tools/codemap.py` | yes | banners + indent-4 declarations → `CODEMAP.md` |
| `tests/test_build_site.py` | yes | the literal exists exactly once |
| `tests/test_codemap.py` | yes | every declaration indexed |
| `tests/test_window_labels.py` | yes | `const WINDOWS = {…}` / `const CELLS = {…}` regexed vs `main.py` |
| `scripts/check_served_columns.py` | **no** — docstring only; it reads the GeoJSON + `expected_columns.json` | — |
| `scripts/build_reference_layers.py` | **no** — two comments | — |
| `deploy.yml` | path trigger is `web/**`, not the file | — |
| `refresh.yml` | **no `index.html` trigger at all** | — |

**7 readers, not 11.** Of the 7, `check_doc_citations` and the two `build_site`
files are indifferent or intrinsic. `codemap.py` + `test_codemap.py` are the
navigation aid and must move with any JS move (brief, correct).

**The finding, independent of the split:** the remaining two — plus
`tools/profiling/verify-staleness-banner.js`'s `STALE_DAYS` regex — **exist to
reconcile literals the page duplicates from the pipeline.** `WINDOWS`/`CELLS`
restate `main.py`'s pins; the cost prose restates `city_unit_costs.json`;
`STALE_DAYS` is pinned by text. `test_window_labels.py`'s own docstring says
why it exists: the page "restated the same ranges as literals and did not roll
with" the pipeline. The page already fetches `web/data/status.json` at boot.
**Serving `WINDOWS`, `CELLS` and the unit-cost values in that manifest (or a
sibling) and reading them at render lets the page stop carrying copies, and
the text-regex guards on the source go with them.** `check_cost_copy.py`
is the harder case — its prose is authored — but its *numbers* could be
interpolated from the manifest, which is what its docstring says the design
intent was ("a single-value edit"). ⚠️ This is a data-contract change and
needs a proposal (CLAUDE.md); it is logged here, not started.

## 7. Corrections to the brief (so it is not re-quoted wrong)

1. **"8 of 65 profiling scripts name `index.html`, 7 as a URL, so the JS harness
   is mostly not the risk"** — the coupling is by **scope**, not by filename.
   **39 of 65 scripts reach page-scope globals inside `page.evaluate`**
   (`state.` in 36 files, `applyView` 11, `METRICS` 8, `buildLayers` 5,
   `SERVICES` 5, `CHROME_IDS` 4, `FULL_BUILD` 4, `noHover` 1; 337 sites; 11 of
   the 39 *drive* the page by writing `state.` or calling `applyView`). Under
   `<script type="module">` — the first step of any split — all 39 break
   unless the page publishes a shim. There is no shared helper module in
   `tools/profiling/` to fix them in one place (`require('./…')` → 0 hits), so
   the fix is the page-side `window.__app` (§4.3).
   Method: `grep -lE '\b(state\.|applyView|METRICS|…)' tools/profiling/*.js`.
   ⚠️ **Credit where due, and a narrowing of this correction:**
   `docs/TOKEN_EFFICIENCY.md` "Files to watch" **already carried the qualitative
   claim** — *"every verify script calls bare globals inside `page.evaluate`;
   module scope is not global scope, so a split would break the whole test
   harness"* — so the *brief* missed this, the *repo* did not. What this session
   adds is the count (39/65, 337 sites), the eight-symbol shim list that fixes
   it, and the correction that it is **not** a blocker. (That paragraph's
   pointer, "RUNBOOK quirk (i)", was dangling; fixed in the same PR.) This is
   the S139 shape again: a fact recorded in one file and absent from the
   instrument built beside it.
2. **"11 Python/CI files read `web/index.html`"** — 7 read it; 2 mention it in
   comments; neither workflow names it (§6).
3. **"`check_cost_copy.py` and `check_served_columns.py` both scan the HTML"** —
   only the first does. `check_served_columns.py` reads the served GeoJSON and
   the committed baseline; its docstring mentions the HTML to explain *why*
   a dropped column is silent.

One thing the brief's §3a *did* get right that this session leaned on without
re-measuring: the `state` write surface. S139 re-ran the falsification (all
eight escapes zero) the day before; taken as given.

## 8. The recommendation, in one paragraph

**Stay one file. Record it as a decision with the three re-open triggers in
§4.3, so it is not re-asked at the next doubling.** First concrete step, one PR,
well under 30 lines of diff to `web/index.html`: add the three tail banners and
name the boot function (Condition 1 — regenerate `CODEMAP.md` and confirm
`applySvcDriver`'s range collapses to ~13 lines and `applyView` moves out of the
budget section), then flip `<script>` to `<script type="module">` with the
`window.__app` shim and update the 39 scripts' `page.evaluate` prefixes
(Condition 2 — run all 65 one at a time; pixel-compare 1440/390 against
master as stage 1 did). Separately and on its own timetable: the manifest
finding in §6, and the read-only-checker question in §3, both of which are the
owner's calls.

## 9. Not verifiable this session

- Whether the script body has **runtime** strict-mode violations (assignment to
  an undeclared name). `node --check` proves it parses as a module, not that
  it runs as one. The 65 verify scripts are the test; running them is the
  first PR's job, not this session's.
- Whether the 24 later-declared-`const` references would actually hit a TDZ
  under some module ordering — only matters if a split happens; not traced.
- Whether Peter (the human reader) uses `CODEMAP.md` at all, or only models do.
  If only models, the navigability half of the argument is about grep, and
  §4.1 item 1 is still the defect.

## 10. `DECISIONS.md` lines to reopen / add (by date; proposed, not made)

✅ **Made the same session (S140) after Peter's three calls: the checker is allowed, the standard gap is static analysis, and the decision is logged** — two `DECISIONS.md` rows dated 2026-09-05 and `STACK.md` §9 updated. The list below is what was proposed and what landed.

- **2026-07-29** — its closing sentence, *"Stage 2 … should wait until stage 1
  proves it helps."* The gate has been **passed**, not mooted: the
  `MOBILE_USABILITY.md` §3 work shipped into the extracted CSS seam
  (`0089eba`) and §3 was closed 2026-08-04. The deferral reason has expired
  and should be replaced by an explicit decision.
- **New line (2026-09-05, proposed):** *`web/index.html` stays one file; the
  split is not justified by measured coupling (lens↔lens 3% of 852 edges) and
  its two real defects are fixed in place (truthful tail banners + named boot;
  `type="module"` with a `window.__app` harness shim). Re-open only on: a
  second concurrent author, a regression traced to cross-section scope
  interference, or a lens-registry refactor of `applyView`/`refreshLegend`/
  `buildLayers`. Growth alone does not reopen it. →
  `docs/FINDINGS_frontend_architecture_verdict.md`.*
- **`STACK.md` §9** (via a decision, not a direct edit): split "no framework or
  bundler in the publish path" from "no linter in CI" — the second is not
  backed by S1 and is the owner's separate call.

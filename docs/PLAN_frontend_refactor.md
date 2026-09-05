# PLAN — Front-End Refactor (the `web/index.html` question)

**Status as of 2026-09-05: THE BRIEF HAS RUN (S140) — verdict is STAY ONE FILE, pending Peter's three calls.** Output: `docs/FINDINGS_frontend_architecture_verdict.md`. Steps 2–4 of §6 are what remain.

**Previous status (2026-09-04): NOTHING IS DECIDED.** This document is the container
for an initiative whose central decision has been deliberately handed to a Fable
session rather than made inline. It exists so that the next session — human or
model — can tell in one read what is settled, what is measured, what is merely
believed, and what it is *not allowed* to do yet.

⚠️ **Do not start refactoring from this document.** It records a pending
decision, not a plan of record. The one thing to do next is run the brief.

✅ **Unblocked 2026-09-05 (S139) and executed 2026-09-05 (S140).** The credit-gate note that stood here is history; see `session-summary/2026-09-05-s139.md` if it matters.

## 1. The question

`web/index.html` is a single hand-edited 7,345-line file holding the entire
front end — markup, all JS, no build step, libraries vendored as globals. Is
that still the right architecture, and if not, what replaces it and in what
order?

## 2. Why it was escalated rather than planned

Three reasons, all worth preserving:

1. **The status quo has a real case.** No build step, three files with recorded
   SHA-256s, no `node_modules`, nothing to trust at deploy time. That is a
   security posture (`security-audit.md` S1), not laziness, and a refactor that
   treats it as an obstacle has already lost the argument.
2. **The obvious plan is wrong** (§4), and it took a measurement to see that.
   A session that planned inline would likely have shipped it.
3. **It is a decision, not a task.** Levels 0–1 of the brief (should the front
   end be hand-written at all; may a build step exist) are the project owner's
   calls, and they moot everything under them.

## 3. Artifacts — read in this order

| artifact | what it carries |
|---|---|
| **`docs/FABLE_AUDIT_frontend_architecture.md`** | **The brief. The decision stack, Levels 0–6, and the reporting contract.** Start here. |
| `docs/CODEMAP.md` → *Dependency graph* | Generated. In-degree table + section self-containment — the evidence for Level 3. |
| `docs/STACK.md` §3, §9 | What the front end is built out of; §9 is the decision being reopened. |
| `docs/DECISIONS.md` **2026-07-29** | Stage 1 (CSS extraction) and the recorded reasoning for **not** taking stage 2. |
| `TODO.md` → *"STAGE 2 of the `web/index.html` split"* | The live item, re-measured 2026-09-04. |
| `docs/security-audit.md` S1 | Why the libraries are vendored — the constraint on Level 1. |
| `docs/SPEC_deployment.md` | The two-build fan-out that exists *because* there is no build step. |
| `docs/MOBILE_USABILITY.md` §1, §3 | The separation seam, and the work stage 2 was gated behind. |

⚠️ **One input is being sought before step 1 of §6 runs:**
`/home/opc/frontend_refactor_research_prompt.md` (**outside the repo**) is a
research prompt for an external web session, asking what established practice
says about *this class* of decision and — the valuable part — **what inputs a
decision like this normally needs that we appear to be missing**. It is
deliberately NOT asking that session to make the call, and it explicitly forbids
speculation about what a model "prefers", because that is the confabulation this
channel has produced before. **Grep before applying anything it returns.**

## 4. What is already measured (do not re-derive)

| fact | value | when |
|---|---|---|
| total / markup / JS | 7,345 · ~575 · **~6,748** lines | 2026-09-04 |
| section banners | **19** | " |
| indexed symbols · edges | 278 · **852** | " |
| **at stage 1 (2026-07-29)** | **3,305 JS lines, 9 banners** | `DECISIONS.md` |
| `state` in-degree | **110** (next: `buildLayers` 34, `METRICS` 16) | 2026-09-04 |
| `state` fields · accesses | **32** · 453 — **420 read / 33 write** | " |
| sections that WRITE `state` | **2** (controls, boot) — **lenses: 0** | " |
| full read of `web/index.html` | ~429 KB ≈ **107K tokens** (~$1.07 at Fable in-rate) | " |
| profiling scripts naming the file | **8 of 65** — **7** as a served **URL**, **1 reads the source** | " |
| Python/CI files reading the file | **11** | " |

Three findings follow, and each one closes a line of enquiry:

1. ⚠️ **The JS doubled in five weeks** (3,305 → 6,748) while banners went 9 → 19.
   **This is the strongest argument in the whole discussion and the only one
   that came from measurement rather than taste.** The 2026-07-29 deferral was
   decided when the file was half its current size.
2. ⚠️ **"`state` is a god object" was WRONG — retired by measurement 2026-09-04.**
   In-degree is 110 and every seam does cross it, but the coupling is
   **one-directional**: **453 accesses, 420 read / 33 write**, and the 33 writes
   are only **UI control handlers (22), the data fetch (1), and 10 capability
   flags derived from `state.data` at boot**. **No lens or layer section writes
   to it at all** — money, services, uses, infill, change, deviation, temporal,
   the uncertainty band and the reference layers are read-only against it,
   without exception. Verified by falsification: zero `Object.assign(state`,
   computed-key writes, `delete`, nested mutation, compound assignment, or
   `state` passed as an argument. **The writer/reader seam already exists in the
   code.** ⚠️ **This removes an argument against splitting; it supplies none
   for.** A read-mostly config object survives fine in one file too. Full
   measurement: the brief's **§3a**.
3. ⚠️ **BANNER-PER-MODULE IS A DEAD END.** The banners mark where someone
   started typing, not concerns: `money view (default)` — the **default lens** —
   has **1 symbol and 29 lines** under its banner, while
   `the citywide budget panel (EXPERIMENTAL)` has **35 symbols and 1,587**.
   Self-containment runs 27–44% for the large sections. Modules cut on these
   lines would mostly import each other.

## 4a. Reproducing the `state` measurement

Kept here rather than in the brief: the brief is loaded on every Fable
invocation and pays tokens for it, and the session needs the conclusion, not the
script.

```bash
cd /home/opc/edmonton-tax-viz
.venv/bin/python - <<'PY'
import re, collections
lines = open('web/index.html').read().split('\n')
acc = collections.Counter(); writes = []
for i, l in enumerate(lines, 1):
    acc.update(re.findall(r'\bstate\.([A-Za-z_$][\w$]*)', l))
    for m in re.finditer(r'\bstate\.([A-Za-z_$][\w$]*)\s*=(?!=)', l):
        writes.append((i, m.group(1)))
print(f'{len(acc)} fields, {sum(acc.values())} accesses, {len(writes)} writes')
# expect: 32 fields, 453 accesses, 33 writes
# ⚠️ THE FALSIFICATION IS THE POINT — the write count is only the whole mutation
# surface if all of these stay at zero. Assert, don't eyeball.
for name, p in {
    'Object.assign': r'Object\.assign\(\s*state\b',
    'computed key':  r'\bstate\[[^\]]+\]\s*=(?!=)',
    'delete':        r'\bdelete\s+state\.',
    'nested mutate': r'\bstate\.[\w$.]+\.(push|splice|pop|shift|unshift|sort|reverse)\(',
    'compound':      r'\bstate\.[\w$]+\s*(\+=|-=|\*=|\|\|=|\?\?=|&&=)',
    'incr/decr':     r'\bstate\.[\w$]+\s*(\+\+|--)|(\+\+|--)\s*state\.',
    'passed as arg': r'\(\s*state\s*[,)]',
    'destructured':  r'\{[^{}]*\}\s*=\s*state\b',
}.items():
    n = sum(1 for l in lines if re.search(p, l))
    print(f'  {name:14} {n}   {"OK" if n == 0 else "*** ESCAPE — recount ***"}')
PY
```

⚠️ **If any escape count goes non-zero, §4 finding 2 is void until re-measured.**
A single `Object.assign(state, …)` or one `f(state)` that mutates its argument
would turn the one-directional coupling back into a genuine god object, and the
read/write ratio would stop meaning what it means today.

## 5. Rules this initiative inherits

- ⚠️ **Do NOT justify a split on token savings.** Measured, false — the file is
  read in grep-located windows via `CODEMAP.md`, never end to end
  (`TOKEN_EFFICIENCY.md`). Justify on navigability, grep precision, blast radius
  or correctness, or not at all.
- ⚠️ **Page runtime is out of scope** — a separate, shelved item with its own
  measurements (`PERFORMANCE.md`). This is about the source.
- ⚠️ **GitHub Pages is not the constraint.** Pages serves arbitrary static
  files; a bundled build deploys to it normally. The no-build rule is a choice
  (`STACK.md` §9, `security-audit.md` S1). This is the most common wrong
  assumption made about this repo — several arguments collapse without it.
- **`DEFAULT_BUILD` must stay in `index.html`** — `scripts/build_site.py`
  regexes it there and hard-fails on anything but exactly one match.
- ⚠️ **`tools/codemap.py` must move with the JS.** It parses the banners out of
  this file to generate `CODEMAP.md`, which a `PostToolUse` hook regenerates and
  `CLAUDE.md` names as the way to navigate the front end. Split the JS without
  it and **the project's own navigation aid silently empties.**

## 6. Sequence

1. ✅ **DONE 2026-09-05 (S140)** — verdicts in `docs/FINDINGS_frontend_architecture_verdict.md`; the brief's §3 was corrected in three places (its §7). Launch recipe kept below for the record. ~~**Run the Fable session** against the brief.~~ Output: a verdict per level
   and one actionable recommendation. Launch it as:

   ```bash
   cd /home/opc/edmonton-tax-viz
   CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5-20251001 \
   CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 \
   claude --model claude-opus-5 --effort high --disallowed-tools Agent Task
   #  …read the handoff and orient on Opus, keeping it SHORT, then in-session:
   #  /model claude-fable-5-1
   ```

   ⚠️ **Launch ONCE and swap models in-session — do not start a second session
   for the Fable half.** `--disallowed-tools` and both env vars are **launch-time
   only**; a session started later without them has no subagent cap at all.
   `/model` and the effort pin both survive the swap.

   ⚠️ **Keep the Opus orientation phase short.** Everything in context when you
   swap is re-read on every subsequent Fable turn. Fable 5.1's $0.25/M cache read
   makes that cheap, not free.

   **`claude-fable-5-1`, not `claude-fable-5`** — identical $10/M in and $50/M
   out, but **$0.25/M cache read against Fable 5's $1.00** (catalog tiers
   `tier_10_50_cache_read_0_25` vs `tier_10_50`). This session re-reads a ~154 KB
   brief every turn; the cache read is the rate that matters.

   **`--effort high`, and it is a pin.** `high` is the model default (cost index
   1.0). `xhigh` is **1.74×** and `max` is **1.91×** — and what they buy is deeper
   visible reasoning, which the brief's §4 then tells the session to suppress.
   A launch-time `--effort` **pins** the level so an in-session `/effort` cannot
   quietly raise it; release it interactively if a level genuinely stalls.

   ⚠️ **The env vars are not decoration.** The brief's §4 says *"No subagents —
   single session"*, and until this line existed that rule was **enforced by
   prose only** — the same failure mode `FINDINGS_decisions_index_drift.md`
   documents for `DECISIONS.md`'s own header. `--disallowed-tools` is the
   enforcement; the two env vars are the cap if the tool is named differently in
   a future build. Verified against the CLI binary (2.1.258) on 2026-09-04:
   **`CLAUDE_CODE_SUBAGENT_MODEL` only sets a *default*** — an agent
   definition's `model:` and an explicit per-spawn `model` both override it —
   whereas **`_FORCE` removes the `model` parameter from the tool schema
   outright** and ignores agent-definition models. Only the second is a cap.
   ⚠️ **Do not move these into `.claude/settings.json`**: they would apply to
   every session in this repo and silently downgrade ordinary Explore/Plan
   fan-out to haiku. This is per-invocation on purpose.
   ⚠️ **Nothing is pinned by default** — there is no `.claude/agents/` or
   `~/.claude/agents/`, and both env vars are unset in the shell, so an
   unguarded Fable session's subagents would inherit **Fable**.
2. ☐ **Record the outcome as a `DECISIONS.md` line** — including *"stay as is"*,
   which is a legitimate result and should be logged as one so this is not
   reopened every quarter.
3. ☐ **Only then** plan execution: seams, order, and the smallest first slice
   that proves the seam. Stage 1 was chosen because it had zero coupling and
   could be verified by pixel-identical screenshots; find the equivalent.
4. ☐ Update `STACK.md` §9 and this file with what was decided.

⚠️ **Note the verification asymmetry before step 3:** 7 of the 8 `verify-*.js`
scripts reference the page by URL, so they keep passing across a split. They can
confirm a migration did not break the page; **they cannot detect a bad seam.**
⚠️ **The eighth inverts it.** `tools/profiling/verify-staleness-banner.js` reads
`web/index.html` off disk and regexes `const STALE_DAYS = (\d+);` out of the
source, so **it fails on any split that moves that literal** — loudly
(`process.exit(1)`), but on a *correct* migration. Carry it with the JS. It
belongs with §7's second open question: a guard asserting on the **text of the
artifact** rather than on the value.

## 7. Open questions the brief does not settle

- Whether the presentation half may run at a lower engineering standard than the
  pipeline half (no types, no build, no import graph, end-to-end tests only).
  This is a values question, not a technical one, and it is the owner's.
- Whether the guards that *scan rendered HTML* for copy and columns
  (`check_cost_copy.py`, `check_served_columns.py`) are reading the wrong
  artifact. That finding stands **whether or not** a split happens.

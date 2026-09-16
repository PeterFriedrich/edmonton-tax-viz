# Findings — the guard burst (`43b324d`…`adc5e49`), audited 2026-09-16 by Fable 5.1

**Brief:** `docs/FABLE_AUDIT_guard_burst.md`. **Read cold** — the L0/L1 view below
was formed from the diffs and the mutation battery before S162 §6–7 and S163 §2–3
were opened; §6 says where the two agree and where they do not.

**Target:** 14 PRs, four new guard scripts + one digest check + one guard
extension, ~950 test lines, written by Opus 5 in under two days.

## 0. Verdict in one table

The brief's rule — a failure at a level moots the ones below — applies **per
component**, not to the burst as a whole: three of the six pieces pass every level
they were taken to, one fails L0 on this repo's own facts, one has no confirmed
reader, one holds narrowly. **No line-level review (L4) was performed on any of
them** — the L1 evidence is red-then-green against real mutations, not a reading
of the ~950 test lines.

| piece | L0 exist? | L1 fires? | L2 reader? | L3 record matches? | verdict |
|---|---|---|---|---|---|
| `check_colour_clamps.py` A (legend = clamp, `tests.yml`) | ✅ closes a measured gap (S160 T3) | ✅ red 3 ways on real file | ✅ required check `test`, 14/14 PRs merged after it passed | ✅ | **KEEP** |
| `check_colour_clamps.py` B (drift, `refresh.yml` → issue) | ✅ 4.5% vs 2.5% design, measured | ✅ red both directions on real data | ⚠️ same channel as the digest (proven read) — but **no dedup; re-files weekly once flagged** | ✅ | **KEEP**, add dedup |
| `tests/test_loaded_path.py` | ⚠️ **not occurring** — 3 files live at every commit in the window; the hand rule was being kept | ✅ both invariants red | ✅ merge gate | ✅ | **KEEP** — 64 lines, no CI cost, guards a rule with no other check |
| `check_doc_citations.py` handoff extension | ✅ 6/8 citations dead when written (not re-measured, see §5) | ✅ red on a dead path, green on a live one | ✅ merge gate | ✅ | **KEEP** |
| `check_decisions_log.py` | ⚠️ narrow — a lint on a token, enforcing a **new** discipline; ½ of day-one rows opt out | ✅ rule 1 red/green (3 ways); rule 2 red on two real chains; one verb-class miss | ✅ merge gate | ⚠️ `CUTOFF` is a fixed date, not permanent — engages 2026-09-17 | **KEEP as a lint**, count the opt-outs |
| `check_todo_branch_refs` (digest) | ❌ **its trigger cannot occur on this repo** (§1) | ✅ red on a synthetic dead branch | ✅ digest | ❌ two docs state a premise the repo does not satisfy | **L0 FAIL** — give it an input or delete it |
| `handoff_gap.py` (hooks) | ✅ replaces a nag with a measurement; blind to 64% of commits by design | ✅ red/green under 3.6.8 and `.venv`; silent on docs-only, as designed | ❌ **SessionEnd output is discarded by the harness; PreCompact's `additionalContext` is not a documented field for that event** (§2) | ❌ `CLAUDE.md` and the DECISIONS row claim the hooks "name" the gap | **L2 FAIL** — the measurement works and reaches nobody confirmed |

The two failures are **the project's own named failure mode, shipped fresh by
the machinery built to prevent it**: a working guard on a channel nobody reads
(`handoff_gap`), and a working guard on an input that never arrives
(`check_todo_branch_refs`). Neither is a code defect. Every test passes.

## 1. `check_todo_branch_refs` — L0 FAIL: the branch it waits for is never deleted

**Its detection condition is "an open item names a branch no longer on origin",
and its stated cause is "the branch was merged and deleted".** Measured:

- `delete_branch_on_merge` on the repo: **false** (`gh api repos/…`).
- Merged PRs **#291–#436 (145 PRs): every head branch is still on origin.**
  147 heads live. The only branches gone are #286–#290 and older — the ones the
  one-off `chore/branch-prune` (#291, merged 2026-08-31) removed.
- Replaying the check on `TODO.md` at `43b324d` (the burst's own baseline): **7
  hits** (the row says 9), and **all seven are pre-prune relics** —
  `feature/phase2-web`, `feature/deployment`, `chore/node24-actions`,
  `feature/services-lens` (#8, July), `feature/stormwater-lens`,
  `feature/year-alignment-guard`, `fix/name-corrections-audit`. All were
  corrected in the same day's staleness passes; today it reads 0.
- Mutation G2: an open item claiming the clamp guard "sits unmerged on
  `fix/colour-clamp-guard`" (merged as #421 that afternoon) → **OK, not flagged.**
  That is exactly the stale shape the check was built for, and on this repo it
  is invisible, because the branch is still there.

So the guard's 9 hits were a **stock** of stale references that a single prune
had exposed, not a **flow** it can keep catching. Its expected hit rate from here
is zero until someone prunes branches again, which nothing does. `RUNBOOK.md` §0d
and the ACTION message both assert *"the branch was merged and deleted"* as the
cause — a premise this repo has not satisfied since 2026-08-31.

**Fix is one setting, not code.** Turning on *Automatically delete head branches*
gives the check a live input (every merge from then on) and retires the manual
prune. The pre-push hook keys on PR state, not branch existence, so it is
unaffected. If Peter would rather keep branches, the check should go: 112 lines,
11 tests and a RUNBOOK section for a row that is green for structural reasons is
the maintenance-with-no-reader shape S163 §7a rejected for P2.

Secondary, unchanged by the fix: the `docs/` exclusion. 82 of the 145 merged
branches since #291 (57%) are `docs/*` — the exclusion hides the majority of
branch names an item could go stale on (G3: `docs/zz-not-on-origin` → OK). The "64 hits,
all doc paths" measurement was not re-run exactly; its shape checks out (186 of
187 backtick `docs/…` strings in `TODO.md` are `.md` paths), so a `docs/` pattern
would need a `.md`-excluding tail rather than exclusion.

## 2. `handoff_gap.py` — L2 FAIL: the measurement is right and both channels are unconfirmed

**The measurement is sound.** Under the box's `python3` (3.6.8) and under
`.venv`: nothing owed → prints nothing; one untracked file in `scripts/` → names
it; one commit touching `scripts/` after the handoff's last commit → names it;
one commit touching only `docs/` → silent (E1–E4). The hook's exact command line
works from another cwd. It runs in **0.05 s**, well inside SessionEnd's 1.5 s
budget.

**The channels are not.** From the Claude Code hooks reference
(`code.claude.com/docs/en/hooks.md`, fetched 2026-09-16, quoted verbatim):

> SessionEnd hooks have no decision control. They can't block session termination
> but can perform cleanup tasks. Claude Code discards their JSON output fields,
> such as `systemMessage`.

> SessionEnd hooks have a default timeout of 1.5 seconds. It applies when you
> exit, run `/clear`, or switch sessions with interactive `/resume`.

The per-event output table gives SessionEnd **"Shows stderr to user only"** — and
the hook command ends in `2>/dev/null`. So on `/clear` — the exact moment
`CLAUDE.md` names ("Always run `/handoff` before `/clear`") — the script computes
the gap, emits it as JSON, and the harness throws it away. **The pre-burst echo
hook had the same fate**; the burst inherited a dead channel and, in `CLAUDE.md`
and the DECISIONS row, described it as one that "names the commits".

PreCompact: the reference says *"Claude Code discards a PreCompact hook's
`systemMessage` and `continue` fields"* and lists PreCompact under events whose
honoured output is the top-level `decision`; `hookSpecificOutput.additionalContext`
is documented for SessionStart, UserPromptSubmit, PostToolUse, Stop, SubagentStart
and PostModelSwitch — **not for PreCompact**. Undocumented is not proven-ignored;
it is unverified, and the burst's own test (`test_json_shape_for_precompact`)
pins the JSON shape, not delivery. ⚠️ **Not checked empirically** — that needs a
`/compact` in a live session with a gap present (touch a file under `scripts/`,
`/compact`, look for the ⚠️ line in the post-compaction context). One try settles
it.

**Fix path, cheap:** SessionEnd is documented to show stderr, so print the plain
message to stderr on that event and drop the `2>/dev/null`. PreCompact: verify
first; if `additionalContext` is honoured, keep; if not, the same stderr route on
manual `/compact` is documented ("the stderr message is shown to the user").

### 2a. Resolved 2026-09-16 (S164, Opus 5) — and the PreCompact fix above is wrong

Settled from the reference without needing the experiment, and it closes the
question the other way:

- **PreCompact cannot inform anyone.** Its decision row is top-level `decision`
  only; the doc explicitly names Stop and SubagentStop as the events in that row
  that *also* accept `additionalContext`, and PreCompact is not among them.
  Exit-0 stdout on that event goes to the debug log. **Its only surface is exit
  2, which blocks compaction** — and *"If compaction was triggered to recover
  from a context-limit error already returned by the API, the underlying error
  surfaces and the current request fails."* A script whose contract is *it can
  never be the reason a session ends badly* may not use that. So §7's "same
  stderr route on manual `/compact`" is **not available**: that route requires
  exit 2. The PreCompact hook is **deleted**, not rewired.
- **`SessionStart` is the channel, and it covers what PreCompact was for.** It
  fires with `source: "compact"` **after** a compaction and `source: "clear"`
  **after** `/clear` — the two moments `CLAUDE.md` names — and its
  `additionalContext` is documented to reach Claude, with `systemMessage` shown
  to the user. It is also strictly better placed: at session start the reader is
  at full context and can act, where at SessionEnd the message arrives too late
  to do anything with.
- **SessionEnd → stderr**, `2>/dev/null` dropped from that hook, as §7 said.

Shipped with 8 mutations red-then-green (`test_handoff_gap.py`), including
re-adding `2>/dev/null` and re-wiring PreCompact. ⚠️ **One of those mutations
caught a defect in the new tests themselves**: `test_session_start_message_does_
not_claim_the_same_session` first asserted on `message(g, at_start=True)` rather
than on what `main()` emits, so flipping `main`'s call site left it green —
`check-where-the-value-can-be-wrong`, written *inside the fix for that class*,
and caught only because the mutation was run.

Cost of the `docs/` exclusion, stated as a number: **126 of 197 non-merge commits
since 2026-09-01 (64%) touch no substantive path**, so the guard cannot see them.
S163 (3 PRs, docs-only) is the case the brief names; it wrote its own handoff, so
nothing was lost there. The exclusion is a design choice with a stated reason and
the number is what it costs; no change recommended.

## 3. `check_decisions_log.py` — holds narrowly; joint A resolved

**Joint A — the cutoff.** `CUTOFF = date(2026, 9, 17)` is a fixed date, so the
rule is not silently permanent-exempt: **C1** (a 2026-09-17 row citing nothing) →
exit 6; **C2** (citing `test_does_not_exist_zzz`) → exit 6, two failures; **C3**
(citing a real test) → 0; **C4** (a 2026-09-16 row citing nothing) → 0, the
one-day exemption the brief flagged. The burst's own ten 2026-09-16 rows were
checked as if the rule applied: **10/10 would pass** — 5 cite a real test, 5 carry
`[unverifiable]` (3 tag only, 2 tag *and* cite). Opus 5 practised the discipline
on rows it had exempted; that is in its favour, and it is also **50% opt-out on
day one** for a tag "nothing audits".

**What the rule is.** C5: a 2026-09-17 row that mentions `check_doc_citations.py`
in passing, about something unrelated → green. The docstring says this plainly
("names a test that EXISTS — not that the test tests the decision"). It is a lint
on the presence of a test-shaped token, and the value is the write-time question,
not the check. Reasonable, if nobody later cites it as verification.

**Rule 2 (back-annotation).** D1: strip `AMENDED 2026-09-08` from the 2026-08-07
`ward_rollup` row → exit 6, names the row. D2: strip `PARTLY AMENDED 2026-09-16`
from the first P2 row → exit 6 via the same-day path. Both real chains. D3: a new
row saying it *"replaces the 2026-08-07 row"* with no mark → **green** — the verb
is outside the five the regex knows. Measured against the file's actual
vocabulary, the miss is small: only 2 rows carry a broader verb + date with no
narrow-verb match, and neither is an announcement. The future writer is a model
that can use any verb, so this is a known false-negative class, not a defect.

**L0 judgement, stated as judgement:** the defect class is real but small (one
dangling pointer found by hand in S161; 13 forward-only supersessions). The cost
is a 210-line prose parser on the merge gate, and every future row must carry a
token or a tag. It holds because its channel has a proven reader and its first
cut already found real chains to check. Count the `[unverifiable]` share at the
next audit; if it stays near half, the write-time question is not being asked.

## 4. The three that pass

**`check_colour_clamps.py`.** A: clamp `50_000 → 5_000` → exit 7; legend
`$50k+ → $5k+` → exit 7; legend `$50K+` (capital K) → exit 7 as "not a money
literal" — fails loud rather than parsing. It reads `colorClamp`, which is the
value `colorFor()` and `moneyScale` actually use (`web/index.html` lines 2012,
4480), and `legendMax`, which is what the legend renders (6734, 6747). B on
**real data**, not fixtures: clamp `$20k` → 48.6% saturating, flagged,
`GITHUB_OUTPUT` carries `flagged=1` and the issue title; clamp `$200k` → 0.3%,
flagged. Joint C: on today's distribution the band goes red at ≤$40k (7.3%) and
stays green from $45k to at least $80k; the upward trigger needs the 22nd-highest
hood ($41,674) to cross $50k — **a ~20% rise in the tail**, a few years out at
assessment growth, which is a reachable signal, not a vacuous one. The band
containing today's 4.5% is Opus 5's argument about Opus 5's guard and I agree with
it on the numbers: excluding 4.5% would red a decision already made.
**One L2 gap:** drift is *persistent* (a clamp stays out of band until re-decided)
and the issue step has no dedup — it files an identical issue every Monday until
the literal moves. The revenue-delta step has the same shape but that signal is
transient. Add a `gh issue list --label clamp-drift --state open` guard before
`create`. Neither `clamp-drift` nor `revenue-delta` has ever fired (neither label
exists yet); the channel is the digest's, which is demonstrably read (#174 closed
in 1 day, #296 in 8).

**`tests/test_loaded_path.py`.** F1: a 4th live file → `assert 4 <= 3` red. F2:
`git mv` the newest handoff into `archive/` → the count test passes and the
order test reds ("the wrong end was archived") — the stated reason both exist,
confirmed. The third test (archive larger than live) is a floor, not a guard.
⚠️ **The defect was NOT occurring.** My first draft of §0 said "5 files were
live when written", read off the window's two `{ => archive}` renames in the diff
stat; `git ls-tree` at `43b324d`, `7238bff~1`, `7238bff` and `adc5e49` shows
**exactly 3 live at every point** — S162 and S163 each archived one as they
added one. The guard enforces a rule that was being kept by hand. It stays
because it costs nothing and the rule had no other check, not because it caught
anything.

**`check_doc_citations.py` extension.** H1: a dead `session-summary/…md` path
in `RUNBOOK.md` → exit 5, message points at `archive/`. H2: the live s163 path →
green. Regex covers `archive/` paths.

## 5. Not checked, and where I am agreeing rather than verifying

- ~~**PreCompact delivery** — not tested empirically (§2).~~ **Resolved from the
  reference 2026-09-16, §2a** — it cannot inform without blocking; hook deleted,
  signal moved to `SessionStart`.
- **The ~950 test lines** were not read line by line; L4 was not reached for any
  component, and the brief says not to do it for the two that fail higher. The
  mutation battery is the L1 evidence.
- **"6 of 8 handoff citations dead"**, **"64 `docs/` false positives"**, **"7 of
  15 stale"** — Opus 5's measurements, not re-run. The first two are consistent
  with what I could see; the third is judgement.
- **The 3.6.8 vacuous-first-write story** — I verified the *fix* runs under
  3.6.8, not the history.
- **One of my own numbers was wrong my way** (`measurements-that-favour-me`):
  the "5 live handoffs" claim in the first draft of §0 would have given
  `test_loaded_path` an occurring defect it never had. Caught by re-measuring
  before commit; recorded in §4 rather than silently fixed.
- **The `$50k` literal** and **P2** — out of scope by the brief.
- **Merge-gate reader**: verified that `test` is a required status check and that
  all 14 PRs merged *after* their tests run completed (`mergedAt` > `completedAt`,
  every one). `enforce_admins` is false, so an admin merge can bypass; none did.
- Where I agree with Opus 5 on argument alone: the band-contains-today reasoning
  (§4), the `docs/` exclusion in `handoff_gap` (§2), and "a skill cannot be what
  reminds you to run it" (S162 §7c) — all three I find sound and none is a
  measurement.

## 6. Against the two handoffs (read after §0–§4 were drafted)

S162 §6a's clamp falsification matches mine (same mutation, same result) and its
table matches the guard's live output to the hood. S162 §7b's "9 hits, all true"
— replay gives 7, all true, **all pre-prune** (§1); the handoff does not mention
that no branch has been deleted since 2026-08-31, which is the fact that decides
L0. S162 §7c says the hooks are "run by PreCompact and SessionEnd" — true — and
does not say what those events do with the output; S163 §4 records the docs-only
blindness honestly and calls it "not a bug; know it", which I agree with. Neither
handoff claims to have checked the channels, so this is an omission, not an error
— but it is the same omission `CLAUDE.md`'s Session Management paragraph exists
to prevent, one level up.

## 7. Recommendations, ranked by what they cost

1. **Repo setting: enable *Automatically delete head branches*** — gives
   `check_todo_branch_refs` an input and retires the manual prune. Or delete the
   check. (Peter's call; one click either way.)
2. **`handoff_gap`: SessionEnd → plain text on stderr, drop `2>/dev/null`**;
   then one `/compact` with a gap present to settle PreCompact. Until then,
   soften `CLAUDE.md`'s "the hooks … name the commits" to what is verified.
3. **`refresh.yml`: dedup the `clamp-drift` issue** (skip `create` when one is
   open with that label).
4. **Next audit of `DECISIONS.md`: count `[unverifiable]` rows** dated ≥
   2026-09-17. The day-one rate was 5/10.
5. Correct the record: `DECISIONS.md` 2026-09-16 backlog row "9 hits" → 7 on
   replay (immaterial); `RUNBOOK.md` §0d and the ACTION string "the branch was
   merged and deleted" → "is no longer on origin" (it cannot know why).

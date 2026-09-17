# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

**Closed items live in `docs/TODO_archive.md`, not here** (moved 2026-07-30).
`## Open work` carries only live work; `## Done` keeps a one-line entry for every
closed item, so **the *never redo a closed item without asking* rule still works
by grepping `## Done`** — the reasoning is one hop away in the archive. This file
is read at the start of every session, so it should hold what is still true, not
the whole history. Keep it that way: when an item closes, move its body to the
archive and leave a `## Done` line.

_Last reconciled: 2026-07-31 (S80 — **the temporal + change lenses are PUBLIC**
(#121, merged + deployed) and **the verify suite is GREEN for the first time on
record: 26 scripts, 0 failures** (#122). Three things closed by *measurement
rather than building*: mobile chrome step 3 was not reproducible; the
45-grey-hoods "blocker" had shipped in S79; and all three verify failures were
stale TEST expectations, not app bugs. Also found and fixed a **data-loss bug in
`tools/todo_archive.py`** — it OVERWROTE the archive instead of appending, and
had destroyed 747 lines of S79 history before it was caught.)_

_Last reconciled: 2026-08-01 (S83 — the touch readout regression is closed: the
peek card now carries **each lens's full rows**, not just its headline, and
Money's readout is split so revenue facts stop printing under the Value map.
**Later the same day: phase 1 of those two numbers is BUILT** — `revenue_by_zone`
ships `revenue_share_city` + 10 `rev_frac_*` columns, and the zoning source
decision reversed on measurement (polygons, not the per-property field). **The
`▶` is now phase 2, the UI.** Original note: the `▶` moved to the two new
numbers Peter asked for (% of city revenue,
top 3 revenue by zone) — both need new columns, so they are proposed rather than
built, and the bottom-sheet decision is demoted (not closed) behind them.
**(That bottom-sheet decision is now CLOSED — refused 2026-08-04, no bottom
sheet; `docs/TODO_archive.md`.)**
Also removed a duplicated preamble block left in this file by the
`todo_archive.py` banner bug fixed in S82.)_

_Last reconciled: 2026-08-07 (S101 — reconciliation pass only, nothing built.
**The `## Done` line and archive entry for West Meadowlark still held the FIRST,
later-inverted answer** ("one new $247.8M parcel"), with no mention of the
renumbering or that the map had been understating the hood — so the settled
record disagreed with the open item that superseded it. Both corrected. Also
fixed a **live contradiction between two open items**: the DATA VINTAGE item
recommended `--geojson-out /tmp/x.geojson` as the safe local-run path while the
item directly above it exists to say that is wrong. And added the
roll-continuity-as-second-guard question, which existed only in a session
summary.)_

_Last reconciled: 2026-08-15 (S108 — **two stale BLOCKERS fell in one session,
and both had parked real work for days.** The open-data request's ASSET
paragraph was unverified because the Alberta manual "returned HTTP 520" — it was
transient, and reading it verified the claim *more strongly* than the draft dared
assert (a Tax Code separating `T` from `E`, a Tax Exemption Code mandatory for
every property *including taxable* ones, and Appendix G naming our exact hospital
and university parcels by MGA section). The break-even lens's first task was
recorded as needing a laptop because "edmonton.ca is unreachable from the Oracle
box" — true of `www.`, **false of `budget.edmonton.ca`**, which returns HTTP 200;
Task 2 then executed here in minutes. ⚠️ **A stale blocker is worse than a stale
bug: nobody reproduces it, because its whole claim is that trying is pointless.
Test the exact host, never the domain, and re-test 5xx before recording it as an
environmental fact.** Nothing was built this session — it was all measurement and
docs.)_

_Last reconciled: 2026-08-16 (S109 — **the session's lesson is that a threshold
which is right for words can be wrong for geometry.** The institutional band
selected hoods by ≥25% institutional SHARE and used that one number for both the
caveat and the outlined range. Share is relative, so it caught hoods where the
share is high and the dollars trivial: RIVER VALLEY CAMERON is 49% institutional
and moves **0 rank places and 0.02 of the colour ramp**. Split into two tiers —
share decides the words, movement on the lens's own ramp decides the geometry.
⚠️ **And the obvious version of "worst drop" was wrong**: SPRUCE AVENUE has the
city's second-largest dollar drop ($30,310/acre) and moves **12 rank places**,
while EDMONTON NORTHLANDS drops fewer dollars and swings **0.62** — measure on
the encoding the reader reads, never in the underlying units. ⚠️ **A second
lesson, from Peter catching it:** the translucent-prism change was justified by
measuring that translucency was UNUSED on Money, without checking whether it was
unused ON PURPOSE — `docs/UI.md` said "always opaque", and the known
depth-ordering quirk it flags was not tested until asked. **Measuring the current
state is not the same as checking the intent.**)_

_Last reconciled: 2026-08-18 (S111 — **three hover fixes, and each one's real
defect was worse than the report**. The revenue sparkline had not "come back":
`git log -S` shows one call site, never removed — 2026-08-01 gave the revenue
cuts a different panel and rewrote the invite's WORDING while leaving the chart,
so the teaser kept promising a chart the click no longer opened. The band prisms
were not merely unhoverable: unpickable geometry over a flattened, transparent
footprint fell through to **whoever stood behind it**, so the tooltip named the
WRONG hood — invisible to any flat overhead check, because at pitch 0 the
transparent footprint picks correctly. And the fix's own no-primacy refusal
(`autoHighlight: false`) silently removed hover CONFIRMATION: 0 pixels moved.
⚠️ **A principled refusal to draw something still has to be checked against the
affordance it removes.** Two new open items came out of it: Services' hover
teases a chart its panel does not open (same defect, blocked on invite copy),
and ratio/uses prisms still pick the hood behind them (blocked on an opacity
call). Also corrected `CONTROLS_MATRIX.md`, which had claimed for six days that
Services carries no sparkline — measured, it does.)_

## Open work

_Last reconciled: 2026-09-09 (S152 — **reconciliation only; no lens, pipeline or
served-value work.** Three records were wrong and one item was already closed by
reality. ⚠️ **A five-day-old environment measurement had INVERTED**: the
`fable-session` item asserted `CLAUDE_CODE_SUBAGENT_MODEL`/`..._FORCE` were unset
*"so nothing is pinned"*; both are now set and **force every subagent to Haiku
4.5 unoverridably**. The bullet now carries the measurement *procedure* instead of
either answer, because the two states want opposite advice. ⚠️ **The Services
audit heading said "closed" above 55 unrelated LIVE items** — `## Open work` was
a flat list until 2026-09-01 and the `###` headings were added over it, so a
2,533-line span read as one closed item; re-parented under a new
`### General backlog`. ⚠️ **My own first read of that was WRONG and worth
keeping**: I believed `tools/todo_archive.py` would archive the whole span, and
running it on an isolated copy disproved it (splits on top-level `- [x]`, ignores
`###`, refuses closed-parents-with-open-children, and zero closed items exist) —
**the hazard is the hand rule in `CLAUDE.md`, not the tool.** Also: the two stale
HTTP servers carried since S146 are **GONE** — verified by PID *and* by both
ports being free *and* by no `http.server` process existing, with 18 weeks of
uptime ruling out a reboot. And `docs/TOKEN_EFFICIENCY.md`'s baseline was
re-measured after 10 weeks: it understated the corpus **~18×** and its verdict
sentence was inverted.
**LATER THE SAME SESSION — the `DECISIONS.md` drift item CLOSED.** §5's open
question was measured (findings §7): where a row points at a doc the argument is
**fully recoverable and the target is RICHER than the row**, so Peter chose
**bless, not trim** — header rewritten, and the mandatory invariant is now the
**pointer**: **273/273 rows carry a doc pointer**, checked by
`check_doc_citations.py`. `AUDIT_LEDGER.md`'s mirrored clause retired with it.
⚠️ **My parser was wrong THREE TIMES on the way (35 → 26 → 22 → 23) and
manufactured one of its own examples** — rows carry pipes inside inline code, and
`L146`, offered as an unpointed row, already pointed where I claimed to have found
its reasoning. **The same bug was in §1, written five days earlier.** ⚠️ **§3's
1,295-facts/16-unique numbers predate the fix and were NOT re-derived.**)_

_Last reconciled: 2026-09-04 (S137 — **no lens, pipeline or served-value work.**
The Fable brief's §1 was rewritten to quote its two cited sections inline instead
of pointing at `DECISIONS.md` + `TODO.md`, cutting its reading list 733 KB → 149 KB.
That measurement then surfaced the item below: ⚠️ **`DECISIONS.md` has drifted off
its own header contract — 13% one-sentence compliance, median row 16× its May
size** — and `AUDIT_LEDGER.md` has the same drift under a header naming the same
rule. ⚠️ **My own first two measurements of it were both wrong** (an inflated
uniqueness count, and a corpus exclusion that could not have failed); both
corrected and falsified in `FINDINGS_decisions_index_drift.md` §3. Also
evaluated a relayed `fable-session` skill draft — **three of its claims about
this repo were false**; kept as an open item with the eval recorded so it
needn't be redone.)_

_Last reconciled: 2026-09-01 (S129 — **the 50 m grid is now an OPTION, not a
replacement**, closing S128's scope correction, and the two questions it was
blocked on were answered by Peter in one line. Three items on this list were
rewritten by MEASUREMENT rather than work: the gaming-laptop perf item was
rescoped twice in one session and its load half **WITHDRAWN** (the same machine
varied 800→409 ms, wider than the between-machine gap it existed to explain),
its DPR hypothesis **refuted** (13.3% FEWER device pixels, not more), and its
GPU question **answered against the premise** — that machine runs integrated
Iris Xe with its RTX `Active: No`, so the comparison was never
discrete-vs-integrated. ⚠️ **`docs/DECISIONS.md`'s last five rows are all
2026-09-01 and two of them retract or correct an earlier one** — read them in
order. Also: a 4x spike-height bug shipped in the 50 m option and was caught by
Peter on a phone, not by any of the ten green verify scripts.)_

_Last reconciled: 2026-09-04 (S136 — **no lens or pipeline work; the session ran
on two tracks, and BOTH found a stale-or-wrong claim in our own records rather
than in the data.** Roads: the NRP publishes per-neighbourhood spend and it had
been in `capital_budget.csv` since 2026-08-22 — the research round that asked for
it returned those profiles only as a *trap*. Front end: the Stage 2 item's own
risk assessment pointed at the wrong half of the repo. ⚠️ **I also shipped a
defect and caught it the same day** — the NRP cross-check took hood acres from
the served GeoJSON, which carries a setback + simplification and understates area
~16%, so every `$/m` was that much too high; `FINDINGS_utility_validation.md` §4
exists to prevent exactly that. Two out-of-repo briefs are written and unsent.)_

_Last reconciled: 2026-09-02 (S133 — **nothing on this list was worked; the
session came entirely from Peter finding a spike on the live public site.**
The `lot_size` item below had its map-defect half CLOSED and DEPLOYED (#312),
and its "⚠️ Not user-visible" bullet was **wrong when written** — it checked
picking and colour and missed that spike HEIGHT is not clamped. ⚠️ **Two
separate stale "it can't be seen" claims** (here and in
`check_value_anchors.py`'s own docstring) had been protecting the same defect.
Also found, and now in `RUNBOOK.md` §3d: **a merged PR that edits `src/` and
regenerates `web/data/*` triggers NO deploy at all** — #312 shipped only
because the refresh was dispatched by hand. ⚠️ `ineligible_points` had drifted
to its band ceiling **exactly** (84/84) and would have red the next weekly
publish on its own, unrelated to any of this — re-pinned.)_

### A `fable-session` credit-discipline skill — evaluated, corrections pending (OPEN 2026-09-04)







- [ ] **Write the corrected `fable-session` skill as a new directory under
  `.claude/skills/`** (same layout as the two there now). Peter deferred it 2026-09-04
  ("later"); the **evaluation is done and is recorded here so it needn't be
  redone**. A relayed draft was checked against the repo — keep its shape, fix
  the below.
  - ⚠️ **Three claims were FALSE about this repo** (the relayed-advice pattern
    again — grep before applying):
    1. It cites *"the project's 'propose don't do' rule"* for `web/index.html`.
       **No such rule.** `CLAUDE.md` scopes propose-first to new modules,
       data-contract/schema changes and CI behaviour, and says *"routine edits
       don't need a proposal."* The index.html edit ban is
       `FABLE_AUDIT_frontend_architecture.md` §4 — **brief-specific**.
    2. It writes plans to `PLAN-<topic>.md`. Ours is **`docs/PLAN_<topic>.md`**.
    3. Its handoff step says `/clear` with no handoff. `CLAUDE.md` requires
       **`/handoff` before `/clear`, always**.
  - ⚠️ **Its Step 1 (regenerate the code graph at session start, verify its
    timestamp) is DEAD WORK here** — the `PostToolUse` hook already re-runs
    `tools/codemap.py` on every `Edit`/`Write` to `web/index.html`, and
    `CODEMAP.md` was verified in sync 2026-09-04. Its *"do not regenerate
    mid-session"* rule is **unenforceable** — the hook fires regardless.
    **Keep only the residual real risk: the hook fires on TOOL edits, so branch
    switches and merges can still drift the graph.**
  - ⚠️ **The biggest gap: it sizes context by "the big file" and is silent on the
    doc reading list.** That is backwards for this repo — the Fable brief's cut
    from **733 KB → 149 KB** never involved `web/index.html` at all; the 80% was
    two markdown index files (see the item below). **Add a step: measure the
    total bytes of everything the brief tells Fable to read, before spending.**
  - ⚠️ **No branch for "the plan is: change nothing."** Its steps 3–4 assume an
    implementation plan handed to a cheaper model, but
    `PLAN_frontend_refactor.md` §6 step 2 makes **"stay as is" a legitimate
    outcome** — as written it would dispatch a Sonnet session to execute a
    decision that says don't.
  - **What holds and should be kept as-is:** the outcome-plus-boundaries prompt
    template (matches how the brief is already written); the subagent-pinning
    step; and the anti-filler rule.
  - ⚠️ **THE PINNING MEASUREMENT INVERTED IN FIVE DAYS — re-measure it, never
    quote it.** On **2026-09-04** `CLAUDE_CODE_SUBAGENT_MODEL` and `..._FORCE`
    were both **unset**, so the note here read *"nothing is pinned and model
    inheritance is the real exposure"*. Re-measured **2026-09-09 (S152)** in a
    bridged child session (`CLAUDE_CODE_CHILD_SESSION=1`), both are **SET**:
    `CLAUDE_CODE_SUBAGENT_MODEL=claude-haiku-4-5-20251001` **and**
    `..._FORCE=1` — so **every** subagent is pinned to Haiku 4.5 and the pin
    **cannot be overridden**: the binary deletes the `model` parameter from the
    Task tool's schema when `_FORCE` is set (`FORCE ? t.omit({model:!0}) : t`)
    and logs `Workflow agent model "X" ignored` for workflow agents. Neither var
    is in any `settings.json`, `~/.bashrc` or `~/.profile` — **grepped, absent**
    — so **this is a launch property, not a repo fact.** ⚠️ **S152 went one step
    further and said "the harness sets them per session". That was WRONG — see
    the S153 correction below.** ⚠️ **The skill must therefore MEASURE (`env | grep
    SUBAGENT`) and branch on the result, not carry either answer as text** —
    the exposure is inheritance in one case and a silent downgrade to the
    weakest model in the other, and those want opposite advice. (The same
    session also found **no `Agent`/`Task` tool exposed at all**, so delegation
    was impossible there rather than merely degraded — a third state the skill
    has to tolerate.)
  - ⚠️ **S153 CORRECTION (2026-09-10) — THE VARS COME FROM PETER'S OWN LAUNCH
    LINE, AND NOTHING EVER "INVERTED".** `/proc/<pid>/environ` on the serving
    process shows both vars in its **launch** environment; the *other* Remote
    Control host on the box (tmux `cc`, PID 1430176) has **neither**. They are
    set by the command in `/home/opc/fable_remote_control_setup_prompt.md`,
    written **2026-09-04 (S139)** to enforce the Fable brief's §4 "no subagents"
    rule:
    `CLAUDE_CODE_SUBAGENT_MODEL=… CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 claude
    --model claude-opus-5 --effort high --disallowed-tools Agent,Task
    --remote-control 'edmonton-fable-audit'`.
    **So the 09-04 "unset" and the 09-09 "set" readings were TWO DIFFERENT
    SESSIONS compared as if they were one** — no drift, no inversion. The same
    line also explains S152's "no `Agent`/`Task` tool exposed at all", which it
    recorded as a discovered third state: that is `--disallowed-tools Agent,Task`,
    a deliberate flag. ⚠️ **`CLAUDE_CODE_CHILD_SESSION=1` is NOT harness-set
    either (corrected 2026-09-10, after S153).** It was on both hosts because
    the tmux server was started from inside a Claude 2.1.201 session, and its
    **global env** leaked `CLAUDECODE`, `CLAUDE_CODE_CHILD_SESSION`,
    `CLAUDE_CODE_SESSION_ID=cc46ba30…`, `CLAUDE_EFFORT=high` and a 2.1.201
    `EXECPATH` into **every** tmux session since. Stripped with
    `tmux set-environment -gu`; a clean `--remote-control` launch carries none of
    them. Check `tmux show-environment -g` before reading a tmux-launched
    session's env as a harness property. (`cc` keeps them until it restarts.)
    ⚠️ **REFINED 2026-09-11 (S154) — the leak was real, but "not harness-set" is
    wrong for TOOL shells.** The relaunched `fable` process (PID 628276) has **no**
    `CLAUDE*` var in its launch env and tmux global env is empty — yet every Bash
    tool shell still shows `CLAUDECODE`, `CLAUDE_CODE_CHILD_SESSION=1`,
    `..._SESSION_ID`, `..._BRIDGE_SESSION_ID`, `CLAUDE_EFFORT`, `CLAUDE_PID`. The
    harness injects those into the shells it spawns. **So `env` from a tool shell
    cannot show a leak; read `/proc/<claude pid>/environ` for the launch env.**
    The SUBAGENT vars are NOT injected — `env | grep SUBAGENT` from a tool shell
    is still a valid check for the pin.
  - **2026-09-10: tmux `fable` relaunched as a GENERAL session** (Peter's call —
    the audit finished 2026-09-05, so its flags only restricted ordinary work):
    `claude --model claude-opus-5 --remote-control 'edmonton-tax-viz'` — no
    FORCE vars, no `--disallowed-tools`. **Subagents there now inherit Opus**, the
    opposite exposure. The flagged line in the setup prompt is for a future
    audit run only.
  - **The measure-don't-quote rule SURVIVES, for a better reason:** the value is
    a property of the launch line, so the skill can read it off the command that
    started the session — and must, because a session started without those vars
    has **working subagents on the inherited model**, the opposite exposure.
    ⚠️ **Check WHICH process you measured** — this box runs two Remote Control
    hosts with different launches, and `ps | grep claude` does not tell them
    apart. Walk up from your own shell:
    `p=$$; while [ "$p" != 1 ]; do readlink -f /proc/$p/exe; p=$(awk '{print $4}' /proc/$p/stat); done`
  - ⚠️ **Hedge the billing claim consistently.** The draft's Step 5 correctly
    calls nested per-model attribution *inferred, not confirmed*, then its
    preamble states it as flat fact. **Unverifiable from here** — the first-party
    model reference covers API rates, not Pro-plan credit mechanics.

### Services cost lens audit — ✅ all 4 calls made 2026-09-07; ⚠️ FOLLOW-ONS BELOW STILL OPEN (opened 2026-09-05 S142)

The ledger's #1 candidate ran: `docs/FABLE_AUDIT_services_cost_lens.md` (brief)
→ `docs/FINDINGS_services_cost_lens_verdict.md` (verdicts). **1× UNSOUND, 5×
CONDITIONAL, 1× SOUND.** The UNSOUND one is **decided and executed**; the three
below are still calls, not tasks.
⚠️ **UPDATE 2026-09-07: ALL FOUR ARE NOW MADE.** The composite was retired
(09-05), the rate re-scoped and the blurb's wrong-base sentence deleted with it
(09-06), and the break-even tension recorded as deliberate (09-07).
⚠️ **The audit itself was wrong in three places**, all caught by re-measuring
rather than by executing what it said — see the last item. **Worth carrying: an
audit's findings are claims to reproduce, not a task list.**

- [ ] **⚠️ OBSERVED MONEY SAYS THE $50/m/yr IS A FLOOR — measured 2026-09-03,
  no value changed.** `docs/FINDINGS_nrp_reconstruction_cross_check.md`. The
  Neighbourhood Renewal Program **does** publish per-neighbourhood spend and it
  was already in `data/capital_budget.csv`; **14 full-reconstruction profiles
  covering ~24 neighbourhoods run $3,151/road-m aggregate (median $3,528)
  against the City's published $1,900/m renew-and-replace** — 10 of 14 above the
  published rate, 6 above twice it.
  **This is the first time the roads model has been checked against dollars
  rather than against another published unit rate off the same page.**
  - ⚠️ **NOT actionable as a rate yet, and do not re-pin anything on it.** Two
    biases of opposite sign: the numerator bundles alleys/sidewalks/lighting/
    drainage with no sub-asset detail published (alley-only profiles alone run
    $521/road-m), while cycle-boundary tails and sub-area projects understate
    others. ⚠️ **The three cheapest profiles are the three that read as
    partial** — the flattering evidence is the least trustworthy.
  - ⚠️ **A first run of this overstated every $/m by ~16%** by taking hood acres
    from the served GeoJSON, which carries a setback + simplification. That is
    `FINDINGS_utility_validation.md` §4's documented gotcha, walked into anyway.
    **Any hood total needs `load_boundaries()` full-res `area_acres`.**
  - **It compounds with the open 25-vs-50 life question rather than offsetting
    it** — both push the same direction. `roadway_om_renewal.sensitivity`
    already calls $50 "a mild lower bound"; this is a third, larger reason.
  - **Unblocking it needs one thing:** a published sub-asset decomposition of an
    NRP reconstruction (§4.2 of the send-back brief, sent by 2026-09-10 — reply pending). Nothing in the
    profile listing or the API carries it.
  - ⚠️ **Touches the LIFECYCLE basis only** — nothing here spoke to the
    $12-vs-operating gap above, which was closed on 2026-09-06 by re-scoping the
    operating rate to $9.32/m/yr. **This finding is unaffected**: both bases now
    read as floors, for independent reasons.

- [ ] **PETER'S CALL — road-per-dwelling is a good DIAGNOSTIC and a bad MAP.**
  Measured 2026-09-03 on a fresh pull:
  `docs/FINDINGS_road_per_dwelling.md`. It discriminates ~1.8× better than the
  shipped `road_m_per_acre` (p90/p10 2.8× vs 1.6×) and orders hoods exactly as
  built form predicts — Garneau 1.09 m/dwelling, Laurier Heights 18.52.
  ⚠️ **But road supply per acre is nearly flat across residential Edmonton (3.1×
  total range, r = −0.10 with density), so the ratio varies almost entirely
  because the DENOMINATOR does — density explains ~79% of it (log r = −0.888).
  A road-per-dwelling map would re-plot dwelling density under a cost-sounding
  name**, which is the objection that made the franchise lenses columns-only on
  2026-07-07. The decision needed is whether that is acceptable; the residual
  ~21% is real road-supply variation and the rank order does change (Spearman
  0.567 vs road/acre).
  - ⚠️ **Four hoods must be excluded BY NAME if this is ever published** —
    WESTVIEW VILLAGE (1,059 dwellings, **1** road metre), MAPLE RIDGE, EVERGREEN,
    CALLINGWOOD SOUTH. **Private internal roads, not a clipping artifact.** The
    per-acre metric hides them; per-dwelling divides by ~nothing.
  - ⚠️ **A per-dwelling denominator is a different normative claim than
    per-acre** — this is a denominator decision like the 25-vs-50 life, not a
    build task.
  - **Already built, do not re-derive:** the dwelling model
    (`load_water.build_connections`, 552,113 dwellings), `road_m_per_acre`, and
    road-per-dwelling itself as an analysis variable
    (`FINDINGS_land_use_diversity.md` §3.2, 2026-07-07, where it is a **null**
    against land-use diversity). ⚠️ **The project has NO population-by-hood
    source**, so the per-capita variant of this cannot be computed at all.

- [ ] **PROPOSED (one line, touches a merge-gate guard so not taken unasked): `check_doc_citations.py`'s path escape hatch is DEAD CODE.** Its bare-name check reads `if name not in docs and (root / name).name not in docs and "/" not in name` — but the regex behind `name` is `\b([A-Za-z][\w.-]*\.md)\b`, whose character class **cannot match a `/`**, so that third clause can never fire. It plainly means to exempt a path-form citation and cannot. **Fix:** test the character *before* the match instead. **Found 2026-09-08 (S148)** writing `docs/FABLE_AUDIT_road_figures.md`, which cites four `.md` files that live in `/home/opc/` **by design** (they must not be committed — they would become a drift surface against `city_unit_costs.json`). ⚠️ **Worked around, not fixed:** those filenames are written **without the `.md` extension**, with a line in §2 saying why — otherwise they add three permanent warnings to the baseline that restoration procedures quote as normal. ⚠️ **That baseline is now ZERO** (2026-09-16, S165): the two standing warnings were both `VIZ_STACK.md` citations, resolved by landing the doc — so any warning at all is now signal, and this escape hatch matters more than it did, not less. Cheap, but it is a guard change.

- [ ] **⚠️ Q1(a) BULLET 2 IS STUCK ON SEARCH — it needs a direct question to
  City staff. The Q1 rewrite stays HELD until it answers.** Is the
  **$600k / $1.9M / $1.5M per km** on *Development Impact on Infrastructure* per
  **centreline** km or per **lane**-km? Two conclusions invert on it (the
  operating-vs-O&M direction, and NRP $3,151/centreline-m at 1.66× vs 0.83× the
  renewal rate) — so publish the flip in **neither** direction and keep **both
  rows** of the conditional table. **Exhausted 2026-09-10 (S154):** the send-back
  round's reply, every claim re-fetched from this box — the page (now reachable,
  was 502) says only *"1 kilometre of a typical Edmonton neighbourhood road"*,
  no lane or centreline anywhere; the 2023 Infrastructure State & Condition
  report has **no road length figure at all**. **Channel:**
  `infrastructure@edmonton.ca`, listed on that page. ⚠️ **Sending is Peter's
  call** — outward-facing. The same message could carry two more asks from Q1:
  the per-class lane-km table (the 3,500 / 1,763 / 4,830 relay has no current
  primary source) and the p4-vs-p16 unit contradiction (`docs/DATA_ISSUES.md`
  G). Round results: `data/DATA.md` §6; correction note in
  `docs/FINDINGS_road_figures_consolidation.md` L2b §1.

- [ ] **⚠️ TWO CONSUMED RATES HAVE UNEXAMINED DENOMINATORS — `bikeway_ops` is the
  live one.** The `source_denominator` field (added 2026-09-09, S150,
  `data/DATA.md` §13) forced the question once per rate and **the answers are
  mostly "nobody asked"**: only `roadway_ops` is ESTABLISHED. **The exposure
  worth acting on is `bikeway_ops`, because it IS consumed**
  (`bike_ops_dollars_per_m` → `transport_cost_ops_per_acre`) and **both halves
  are unexamined**: (a) **$178/km comes from the same Taproot article, same
  sentence family, as the RETIRED $1,285/km** — the article that attaches
  *"linear kilometres"* to the ~11,000 (the City's own 2023-24 Snow & Ice
  report says *"linear km"* too — `docs/DATA_ISSUES.md` G);
  (b) the **$20,100/km snow half** divides ~$30.15M by a ~1,500 km *"cleared
  network"* whose **membership** is already flagged (`denominator_mismatch`)
  but whose **unit** is not. ⚠️ **This bites harder on bikeways than on roads:**
  a bikeway is frequently one direction per side of a street, so route-km and
  lane-km can differ by ~2× on the same street. `bikeway_capital` (678 km, Bike
  Plan Table 3) is also UNEXAMINED but **inert** — not consumed by anything —
  so it has no live exposure. ⚠️ **DO NOT RESOLVE THESE BY ARITHMETIC.** The
  standing rule holds: rates come from a named City publication after a scoped
  question. The right move is a bikeway question in the next research round,
  the same shape as Q1(a). ⚠️ **And do not fill the field in to look tidy** —
  UNEXAMINED is the honest state and the tests permit it.

_Last reconciled: 2026-09-01 (S130 — **no backlog item was worked; both PRs came
from Peter noticing the site was slow to switch grids.** Nothing here opened or
closed as a result, so this list is unchanged except for the capture item above,
whose two halves now sit in different states. The session's transferable result
is a **method** note rather than a build note: a decision recorded as
*unfalsifiable* — the busy stripe's `gridStore`-vs-`gridFetches` gate, which no
arrangement of clicks could distinguish — **became checkable a few hours later**
when the prefetch created the window that separates them. ⚠️ **Re-test parked
"cannot be distinguished" caveats when the system grows; they are not permanent.**
Also three more vacuous checks caught by falsification, all in tests written the
same session — see `docs/DECISIONS.md`'s last two rows.)_

### Reader-facing copy decisions — 18 open rows in `docs/COPY_DECISIONS.md` (OPEN 2026-09-14 S157)

Opened when Peter asked what "municipal levy" means in the Services panel: *"that's
the big unintuitive addition that makes my eyes glaze when i open that panel"*. The
term is never defined on any surface, and the same quantity carries **four different
nouns** (Tax Revenue / Revenue / municipal levy / municipal property-tax revenue).

Full list, with the measured counts and the two locked rows, in
**`docs/COPY_DECISIONS.md`**. Decide a row there, apply it to every surface it
names in one pass, then add a `DECISIONS.md` line citing the id.

⚠️ Two rows are **not** open questions and must not be re-derived:
- **F2** — the gold >100% bar re-introduces the break-even verdict locked against on
  `DECISIONS.md` 2026-07-16 (magnitude, never "pays its way").
- **F3** — a road-cost Ratio *denominator* would duplicate the road-metre map: both
  cost columns are exact constant multiples of road metres ($50.000000/m,
  $9.320000/m, stdev < 0.0001 across 400 hoods). That denominator also already
  existed and was retired 2026-09-05.

**F1 is BUILT — 2026-09-15, PR #399** (`## Done`). The panel follows
`state.svcDriver`; storm/fire/water state their scope rather than showing an empty
group. `verify-services-panel.js` gates it and was merged RED first (#398).

### Controls that reach nothing — audit EXECUTED 2026-09-15 (S159); two decisions open

Brief + instrument: `docs/FABLE_AUDIT_controls_state_space.md`,
`tools/profiling/audit-controls-diff.js`; findings
`docs/FINDINGS_controls_state_space.md`; ledger row 2026-09-15 (S159). Both
builds swept, 9/9 readouts live: **no control reaches nothing** — every finding
is in the `panel` column. T1 is public (3 of 10 service rows). T2 closed (`## Done`).

- [ ] **T3 — `#revcut` does not reach the panel, though `#metric-row` above it
  does.** Measured: `revenueMix` reads no cut, so under **Residential** the map
  is residential $/acre and the panel is headlined with the **total** levy
  (`$146.40M municipal levy · 5.26%` for DOWNTOWN, byte-identical across cuts);
  the residential share is a row inside the mix. Judgement, Peter's: leave it
  (the mix is the decomposition the cut belongs to), light the selected cut's
  row the way `#millrates` lights the rate, or headline the cut's own levy.
  `lab / labcut` is the same three cuts; settle together.
- [ ] **T4 — `#budget-pod`: the yield was decided, the toggle was not.** The
  CSS yield to `#temporal` is deliberate (`styles.css` at `#budget`, `DECISIONS.md`
  2026-08-16) and copies the mill-rates pod — but `body.mills` is **derived** by
  `syncMillRates` and `body.budget` is a **reader toggle**, so §3's "cannot both
  think they own the slot" does not transfer. Measured (findings §4 table):
  with the panel open the opener is **lit over an invisible pod** (no CSS
  exception is possible — `#budget-pod` is not `#temporal`'s sibling), and a
  press under the open panel toggles state with nothing visible but the button,
  so whether the pod is there when the panel closes depends on press parity.
  Remedies are a decision, not a patch: (1) a press under the panel closes the
  panel; (2) opening the panel clears `body.budget`; (3) keep the yield and
  un-light the button from `openTemporal`/`closeTemporal`. Peter's call.
- [x] **Manifest staleness guard — BUILT 2026-09-17 (Peter's yes).** Two checks,
  not one: `check_budget_context` + `check_mill_rate_values`. See `## Done`.
- [ ] **L2 — `~0.9% of units` in the Infill blurb is a typed-in measurement** (S56's
  D3, 2026-07-16) that nothing re-derives, while the permits feed refreshes weekly.
  **Re-derive from the feed, or drop the figure.** ⚠️ Not mechanical — dropping it
  loses a real disclosure, so it is a copy decision, not a guard gap. Findings §4.
- [ ] **~~Retrieval logging — decide the doc question with evidence, not argument.~~**
  A `PostToolUse` hook logging every Read/Grep with a filename gives a per-doc
  read-frequency table in 2–3 weeks; a doc never opened before an action is a
  prune candidate. ⚠️ **The mechanism is already proven here** — `.claude/settings.json`
  runs a `PostToolUse` hook to regenerate `CODEMAP.md`. Cheap, reversible, and it
  replaces a standing argument (is the doc apparatus load-bearing?) with a
  measurement. Context: `/home/opc/doc_load_bearing_or_agent_scaffolding.md`
  (external review, **two of its three repo-specific claims did not survive
  checking** — see the S159 handoff).
- [ ] **T5 is NOT a cleared row.** The two Detail selectors read invariant on
  tooltip/peek only because the probe feeds a hood feature to `viewTooltip` in
  grid modes too. Needs a cell-grain capture before it means anything.

### General backlog — the flat list (no parent item; predates the `###` headings above)

⚠️ **Everything from here down is its OWN top-level work, not a child of the
Services audit above.** `## Open work` was a flat `- [ ]` list until 2026-09-01;
the three `###` headings were added above it on 2026-09-04, and the Services one
was later marked closed **in place** — which left ~55 unrelated live items
rendering as its children. Re-parented 2026-09-09 (S152) after measuring it.
**Do not archive a `###` heading's span on the strength of the heading alone**:
`tools/todo_archive.py` is safe here (it splits on top-level `- [x]` boxes,
ignores `###` headings, refuses when a closed parent carries unchecked children,
and there are currently zero closed top-level items — verified by running it on
an isolated copy), but the hand rule in `CLAUDE.md` (*"move its body to the
archive"*) is not, and this span is 2,533 lines.

- [ ] **`TODO.md` is 89% of the loaded path and grew 149 → 264 KB in 30 days — audit the ~100 open boxes, relocate the ~46 KB of closed sub-items** (opened 2026-09-16, S166; `docs/FINDINGS_doc_growth.md` §3). This is `_PREMISES.md`'s P10 note, which had no `TODO.md` item — it lived only in that file and the ledger's S162 row. The loaded path (`CLAUDE.md` + this file + newest handoff + memory index) moved **173 → 288 KB (+66%)** over the same 30 days the repo grew +69%, so the growth is NOT confined to files outside the loaded path; this file is where it lands. Two halves. ✅ **(2) THE RELOCATION IS DONE 2026-09-16 (S166): 26 KB moved, 261.6 → 238.0 KB**, 27 blocks under 11 open parents, each replaced by a pointer to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents"; every relocated line verified verbatim in the archive and the open-box count identical (103 → 103) before writing. ⚠️ **It was 46 KB on paper and 26 KB in fact: 3 closed sub-items carry OPEN descendants** (L2209 the 8 regroup decisions, L2379 P2.3 security checklist, L2715 "More service layers") **and were held back** — moving them archives live work out of sight, the refusal `tools/todo_archive.py` makes at top level, applied one level down. The open-box count is what caught it; a first pass that lacked the rule silently dropped 5 open boxes. **Those 3 become relocatable when their open children close, not before.** ⬜ **(1) STILL OPEN — the staleness audit**, which is the half that carries wrong-action risk: 103 open boxes, unaudited; a hand sample of 15 items untouched >60 days found **7 stale (47%)** (`DECISIONS.md` 2026-09-16). `CLAUDE.md`: reproduce the symptom and re-measure the stated cause before acting — an open item "has lagged reality twice". Do it as a verify pass (dead / stale-needs-remeasure / live), not a clear-the-easy-ones pass; expect 2–3 sessions for 103 items. **PASS 1 DONE 2026-09-16 (S166): 7 of 103 verified**, chosen as the cheapest-to-falsify shape — items asserting a NEGATIVE about the code. Result **2 stale / 5 accurate**: ✅ corrected — MOBILE USABILITY's *"zero `@media` queries today"* (there are 6, and `MOBILE_USABILITY.md` documents the phone seam + a CONFIRMED 390×844 render pass) and OUTREACH TRACKER's *"five data issues"* (now 10 rows / 11 `NOT SENT` — the item got BIGGER, not stale). ✅ verified LIVE and left alone — break-even "STILL NO CODE" (only comments denying it), bikeway lifecycle (the JSON's own `_status` agrees), Services hover teaser (`index.html`'s own comment confirms the defect; only the predicate NAME was stale, `hasSvcCost` → `hasRoadsLife`, fixed), ratio/uses prisms picking behind (`pickable: false` on both layers). ⚠️ **I nearly mis-called an eighth**: "Zoom-gating does not exist yet" LOOKED stale because `placeSize()`/`PLACE_MIN_ZOOM` scale labels with zoom — but no show/hide GATE exists, so the item is accurate and stays. Checking the specific claim, not the topic, is what separated them. ⚠️ **Do NOT read 2/7 as "29% stale, so the 47% was wrong"** — this sample was deliberately picked for checkable code claims and skews toward verifiable-either-way; the 47% sample was 15 items >60 d. **PASS 2 DONE 2026-09-16 (S166): 5 more, all from the >60 d cohort** (the one the 47% came from). Result **1 corrected / 4 accurate**: ✅ corrected — "per-year archive filenames" (the keep-not-overwrite archive ALREADY EXISTS as `data/temporal_archive.json`, `SPEC_temporal.md` ✅ CLOSED 2026-07-28; only the year selector is still open, and it reads that file). ✅ verified accurate and left alone — auto-fetch `pwis-wc4c` (`download_data.py` still says mill rates are not fetched; the digest only CHECKS them, so "detects + holds, doesn't self-heal" is exactly right), `P2.3d S2` (`docs/security-audit.md` exists), `P2.5 doc-drift` (`ARCHITECTURE.md` L1331 "Reconciliation notes — drift flagged, NOT fixed" still stands), `MA DERELICT RESIDENTIAL` (`apply_tax_rates.py:37` maps it exactly as described). ⚠️ **Nearly mis-called the archive item DEAD** — the archive half is done, but the temporal lens is per-NEIGHBOURHOOD by design, so the map-wide year selector it names does not exist. Second near-miss in two passes, same shape: the topic had moved, the specific claim had not. **RUNNING TOTAL: 12 of 103 checked, 3 corrected, 9 accurate (~25%).** ⚠️ **That is BELOW the 47%, and my "2–3 sessions" estimate now looks oversized — treat both numbers as unsettled, not as a new finding.** In the >60 d cohort specifically it is 1 of 5. **PASS 3 DONE 2026-09-17 (S166): 3 more from the >60 d cohort — and the first finding that is not about staleness at all.** ⚠️ **A2's INPUT is 19 months stale**: `stt5-pzaa` answers 200 but its rows have not moved since 2025-02-19, while controls run the same minute (`qi6a-xuwt` 2026-01-12, `pwis-wc4c` 2026-04-29) prove the field is meaningful and the portal is healthy. The item's "verified 2026-07-18" meant REACHABLE. Recorded in the item; deliberately NOT filed in `DATA_ISSUES.md` yet (a frozen table may be retired or annual, not defective — establish which first). ✅ verified accurate and left alone — **Visual polish**, all four claims re-checked against the tree (`RAMPS[].edge` ×3 present, `TOP_EDGE_COLOR` gone, `HOME`/`HOME_2D` still zoom 10.2, `prefers-color-scheme` 0 in both files, `cividis` present so the 2026-09-16 colourblind correction was right); **Utility cost lenses** and **PUBLIC RELEASE PREP**, both already carrying accurate 2026-09-16 corrections. ⚠️ **Accurate items were NOT annotated** — adding "checked, fine" notes grows the file this exercise exists to shrink; this progress line is the record. **RUNNING TOTAL: 15 of 103 checked, 4 corrected, 11 accurate (~27%); in the >60 d cohort 2 of 8.** ⚠️ **The yield is changing SHAPE, not just rate**: passes 1–2 found claims overtaken by our own work, pass 3 found an external input that went quiet. The second kind cannot be found by reading, only by calling the source — so the remaining passes should re-verify every external dataset an open item names. **PASS 4 DONE 2026-09-17 (S166): the external-dataset sweep — every Socrata id named in `src/`, `scripts/`, `tools/`, `main.py`, `TODO.md` (open work), `data/DATA.md` and `docs/DATA_ISSUES.md`, asked when its ROWS last moved.** 117 candidate ids, **26 real datasets**. ✅ **THE PIPELINE IS CLEAN — every ingested dataset is current**: worst is `gfxq-u8uu` (Catholic schools) at 136 d and `qi6a-xuwt` at 248 d, which is the *annual* historical roll and is supposed to look like that; the four GTFS feeds sit at 90 d, consistent with Edmonton's service-signup cadence; nine sources moved within 3 days. **Only two outliers, and neither is new work:** `stt5-pzaa` 575 d (pass 3, already recorded on A2) and `urjq-fvmq` 2,647 d — which is **NOT a finding**: `DATA.md` §9 already documents it as *"an href-only landing page, no machine-readable blob"*, i.e. deliberately not a source. ⚠️ **MY OWN SWEEP WAS VACUOUS ON FIRST RUN AND PRINTED A CONFIDENT TABLE ANYWAY.** It sliced `TODO.md` between `txt.index("## Open work")` and `txt.index("## Done")` — but the file's *preamble talks about* `## Done`, so the slice was **39 characters** and covered no open item at all. The tell was `stt5-pzaa` missing from a table built to find things like `stt5-pzaa`; the fix anchors on heading LINES and asserts the slice is >50 KB. **This is `check-where-the-value-can-be-wrong` inside the instrument, and the same span-parsing trap `CLAUDE.md` already warns about for `todo_archive.py`.** ⚠️ **Observation, NOT a finding, and NOT verified as an absence:** a case-sensitive grep of `scripts/`, `tests/`, `.github/workflows/` and `src/` found GTFS named only in `download_data.py`, so there may be no freshness guard on the transit feeds — but 90 d is a normal signup gap, so there is no evidence of a problem to guard. **Not proposing one.** **RUNNING TOTAL: 15 of 103 items checked, 4 corrected, plus the dataset sweep. Next pass: the remaining 24 items >60 d (mostly parked lens plans — expect low yield), then the 30–60 d band. The external-input question is now CLOSED — re-run the sweep rather than re-reading the items.** **PASS 5 DONE 2026-09-17 (S168): the 30–60 d band OPENED — it is 12 items wide (by newest date in the item); 3 checked, 2 corrected.** ⚠️ **`DATA VINTAGE` carried TWO dates ~2 MONTHS STALE**: `data/raw/` is **2026-09-03** not 2026-07-06, and the last committed auto-refresh is **2026-09-14** not 2026-07-27 — the hazard is unchanged and live (local raw still trails the shipped site) but the gap is 11 days, not three weeks, and its **1,896-values blast radius was NOT re-derived**. ✅ **`--geojson-out`**: the technical claim RE-VERIFIED in code (the five auxiliary web exports are hardcoded `ROOT / "web/data/…"` constants with no CLI flag, so only `--geojson-out` and `--png-out` redirect at all) but its TITLE was stale — it accused the DATA VINTAGE item of advice that item stopped giving on 2026-08-07; struck. ✅ **`verify-peek.js` flake** verified ACCURATE — 3/3 green alone, 38 checks a run. ⚠️ **THE BAND YIELDS A DIFFERENT SHAPE FROM THE >60 d COHORT: both corrections here are stale NUMBERS inside items whose CLAIMS are still true**, where the >60 d passes found claims overtaken outright. A recent item is likelier to be right-but-mismeasured than wrong, so **re-measure its figures rather than re-litigating its premise.** ⚠️ **An environment finding, not a backlog one:** an orphaned `http.server` from a DEAD session was running 28h50m serving a stale build (recorded on the `verify-peek.js` item) — a **recurrence** of a class S152 declared closed. **RUNNING TOTAL: 18 of 103 checked, 6 corrected, 12 accurate.** **PASS 6 DONE 2026-09-17 (S169): 1 checked, 1 corrected — and the pass found more wrong with the AUDIT'S OWN INSTRUMENT than with the backlog.** ✅ **corrected — the Services HOOD PANEL track** (L1308): its predicted narrow-width failure ("the track collapses toward zero while the row still fits") is **FALSIFIED by measurement** — the track is 210px at 390px against a 164px desktop control, i.e. **WIDEST on a phone**, because desktop pins the panel to a fixed ~300px row. The real legibility limit is the VALUE, not the viewport (21.2% of hoods draw a sub-pixel bike-ops fill at the narrowest track). ⚠️ **THREE INSTRUMENT DEFECTS, and each one inflates the appearance of progress.** **(1) The band is 8 items today, not the 12 pass 5 reported** — pass 5 checked 3 and annotated them with that day's date, which **drops a checked item out of its own cohort**. **(2) `accurate items were NOT annotated` (pass 3's rule) means an accurate item is indistinguishable from an unchecked one, so later passes RE-CHECK it**: `THE RATIO AND USES PRISMS` and `A TRUE BIKEWAY LIFECYCLE` are both in today's 8 and were both verified accurate in **pass 1**. 2 of 8 is a 25% re-check rate. **(3) The cohort metric is AMBIGUOUS and nobody said which one is meant** — by newest date in the item (last touched) the `>60 d` cohort is **1 item**; by oldest date (opened) it is **18**. The progress line's own "remaining 24 items >60 d" matches neither. ⚠️ **`18 of 103` is therefore not a coverage figure** — 103 counts nested boxes (65 top-level, 100 including nested, not 103), and with no per-item record the numerator double-counts re-checks. **The next pass should fix the ledger before checking anything: mark each checked item with a dated tag so the trail survives, and name the cohort definition.** ⚠️ **One-off, not a cadence** — a scheduled manual sweep is the shape rejected the same day for backlog staleness. ⚠️ **Not a growth-instrumentation item** — the doc-growth audit's L0 FAILED and nothing is to be built; re-measure the loaded path with `.venv/bin/python tools/retrieval_report.py | sed -n 4p` at the ~2026-09-30 read-log run and put the number to Peter then. This file is 3,285 lines; a default `Read` returns 2,000.

- [x] **GUARD-BURST AUDIT FOLLOW-ONS — ALL 3 DONE** (opened 2026-09-16, S164;
  closed 2026-09-16, S165. `docs/FINDINGS_guard_burst.md` §7). Two of the six
  pieces were called the project's own failure mode shipped fresh: a working
  guard with no input, and a working guard with no confirmed reader. The reader
  half was real and is fixed (PR #438). **The input half was not real** — see
  below.
  - [x] ~~**`check_todo_branch_refs` has no input**~~ — **VERDICT REVERSED
    2026-09-16 (S165), findings §1a. KEPT as-is; no repo setting changed.** The
    L0 FAIL counted merges only. Merges never feed this check (merged branches
    stay on origin) — **PRUNES do**, and the prune recurs: `chore/branch-prune`
    (#291) removed ~287 branches on 2026-08-31 and **150 have accumulated in the
    16 days since**. Its input arrives in one batch per prune, so long green runs
    are the expected shape. Real defect is *scheduling*, not existence; re-open
    the post-prune-trigger question at the next prune. ACTION string and
    `RUNBOOK.md` §0d reworded to say "no longer on origin (usually a PRUNE)" and
    to tell the reader green is expected. ⚠️ Also withdrawn: enabling
    *Automatically delete head branches* was half-sold as stranding protection
    and would not have helped — `git push` silently RECREATES a deleted remote
    branch.
  - [x] **`handoff_gap.py` reaches nobody confirmed** — DONE 2026-09-16 (S164,
    PR #438), and the fix is **not** the one the finding proposed. The
    `/compact` experiment was unnecessary: PreCompact's only output surface is
    exit 2 (= block compaction, which fails the request on a context-limit
    recovery), so it **cannot carry a message at all** and the hook was deleted
    rather than rewired. The signal moved to **`SessionStart`**, which fires
    after `/clear` and after a compaction and whose `additionalContext` is
    documented to reach Claude; `SessionEnd` now writes to stderr with
    `2>/dev/null` dropped. 8 mutations red-then-green — one of which caught a
    `check-where-the-value-can-be-wrong` defect in the new tests. Findings §2a.
  - [x] **`clamp-drift` issue has no dedup** — DONE 2026-09-16 (S164, PR #438).
    `refresh.yml` skips `gh issue create` while one is open with the label, with
    the transient-vs-persistent reason in the step comment (the revenue-delta
    step above stays undeduped deliberately: that signal *is* per-event).

- [ ] **The exit-4 inconclusive message in `refresh.yml` names the wrong cause**
  (one line; opened 2026-09-16, S165, `docs/FINDINGS_guard_channels.md` §2).
  The case block hardcodes `"::warning::Year-alignment check inconclusive
  (metadata fetch/parse failed)"`, but `check_year_alignment.py` also returns 4
  from its `stale-metadata` branch — where the fetch **succeeded**. Every weekly
  run therefore logs two contradicting lines, and the workflow's is the false
  one. **Fix:** surface the script's own message instead of the workflow's.
  ⚠️ **It is a CI file, so propose before editing**, though the change is a log
  string and not behaviour.
  - ⚠️ **The big version of this item was WITHDRAWN the same day it was opened.**
    It claimed the roll-year guard's blind states were unexamined and that the
    January case was an unnoticed hole. **Both were already settled** —
    `RUNBOOK.md` §1 anticipates the January case with a checklist step, and
    `DECISIONS.md` 2026-08-25 decided exit 4's treatment on this very guard.
    See `FINDINGS_guard_channels.md` §0a; **do not re-open it without reading
    that row's body**, which is where the reasoning lives (the index line is
    about exit 3 and does not mention exit 4 at all).
  - **Left open, reported without recommendation:** the two exit-**0** blind
    states (roll CSV absent, FIR anchor absent → `result=skipped`, green,
    silent). Nothing found addresses exit 0, but both need a committed file to
    go missing — latent, not scheduled. Decide whether that is worth a guard at
    all before building one.

- [ ] **DEV HISTORY FOLLOW-ONS — three, none blocking (opened 2026-09-14, S156,
  after PR #389 merged).**
  - **Nothing verifies `dev_history.json` in CI.** The feature was verified by a
    throwaway probe (25/25) that was **deleted on merge**, so the panel, the
    teaser, the zero-based baseline and the all-zero wording now have **no
    standing check at all** — the one surface where a regression would be silent.
    A `verify-devhistory.js` is ~40 lines and the probe's assertions are recorded
    in the S156 handoff. ⚠️ **Note the honest caveat:** the 42 `verify-*.js`
    scripts gate NOTHING (its own open item below), so this buys a runnable
    check, not an enforced one.
  - **The panel has never been opened on a phone.** Same class as the Services
    panel item below. The chart is 300×96 inside a bottom-sheet at 390px — the
    y-gutter and the two year ticks are the parts most likely to collide.
  - **`#temporal-close`'s aria-label still says "Close the assessment-history
    panel"** — now wrong for **three** of the four panel modes (revenue,
    services, and the new dev history). Pre-existing, but this change widened it
    from one-in-three to one-in-four. Screen-reader-only, one line to fix.

- [ ] **⚠️ 565 UNITS STILL UNATTRIBUTED BY DECISION — the straddling half of the
  comma-list permit names. The other 1,245 units are FIXED (2026-09-14, S156).**
  ✅ **Fixed:** 8 unambiguous names corrected in `PERMIT_NAME_CORRECTIONS` —
  WÎHKWÊNTÔWIN 1,229 → 2,066 (+68%), SOUTH TERWILLEGAR 823 → 1,189 (+45%),
  plus ELSINORE/RUTHERFORD/RITCHIE/MCCONACHIE. Citywide unchanged at 162,414
  (attribution moved, not totals — the invariant that says units were placed,
  not invented). 5 tests, 3 falsified.
  ❗ **STILL OPEN — Peter's call, 565 units across 15 names:** the rows that
  genuinely straddle 2+ hoods (`RUTHERFORD, HERITAGE VALLEY TOWN CENTRE` 327u;
  `THE HAMPTONS, GRANVILLE` 119u; `HOLLICK-KENYON, BRINTNELL, MILLER, BRINTNELL`
  60u across 3). Choose one of **even split / assign to the first-named hood /
  drop loudly**; a test currently pins the non-fix so a later tidy-up cannot
  quietly invent a split. ⚠️ **Not a spatial problem** — 14.9% geocoded, and
  `THE HAMPTONS, GRANVILLE` is 0%.
  ➡️ **Also filed as an upstream defect: `docs/DATA_ISSUES.md` issue 6 (NOT
  SENT, and the only one of the six with NO published notebook)** — asking for a
  single-valued field, ideally the numeric `neighbourhood_id` the City already
  publishes on three other datasets. And as **`AUDIT_LEDGER.md` never-audited
  candidate 8** (the name-join layer).

  <details><summary>Original finding (2026-09-14) — how it hid</summary>

  The
  unmatched permit-side names are rows whose `neighbourhood` field holds a
  **comma-joined LIST** of hoods (`OLIVER, WÎHKWÊNTÔWIN`,
  `SOUTH TERWILLEGAR, SOUTH TERWILLEGAR`), and **every one of them predates
  2021** — which is exactly why this hid: the 5yr window loses **1 unit** and the
  3yr window **0**, so `load_permits`' docstring called it "immaterial" and was
  right about the windows anyone had measured. The anchored `_long` window
  ("since 2009", a **published** column + choropleth since 2026-07-21) loses
  **23 names / 1,810 units / 1.11% citywide**, and the citywide figure badly
  understates the per-hood damage:

  | unmatched name | units | goes to | shown now | understated by |
  |---|---:|---|---:|---:|
  | `OLIVER, WÎHKWÊNTÔWIN` | 837 | WÎHKWÊNTÔWIN | 1,229 | **+68%** |
  | `SOUTH TERWILLEGAR, SOUTH TERWILLEGAR` | 366 | SOUTH TERWILLEGAR | 823 | **+45%** |
  | `CHAPPELLE AREA, HERITAGE VALLEY AREA` | 28 | HERITAGE VALLEY AREA | **0** | shows nothing |

  **Split by how fixable each is** (measured, `/tmp` script — re-run before
  acting): **Tier 1, 1,273 units (70%), unambiguous** — every comma-part
  resolves to ONE rendered hood, because the row is either the same hood twice
  (`RITCHIE, RITCHIE`) or the Oliver→Wîhkwêntôwin **rename** carrying both names.
  These belong in `PERMIT_NAME_CORRECTIONS` and need no decision beyond a yes.
  **Tier 2, 537 units, genuinely straddles 2+ hoods** (`RUTHERFORD, HERITAGE
  VALLEY TOWN CENTRE` 327u; `THE HAMPTONS, GRANVILLE` 119u;
  `HOLLICK-KENYON, BRINTNELL, MILLER, BRINTNELL` 60u across 3) — a name
  correction cannot split these.
  ⚠️ **THE SPATIAL FIX IS DEAD — measured 2026-09-14, and this corrected an
  unverified claim written into this item the same hour.** I wrote "many ARE
  geocoded, so point-in-polygon is available"; measuring it inverted the answer.
  Tier 2 is **14.9% geocoded (23.8% of units)**, and the two biggest rows are the
  worst: `RUTHERFORD, HERITAGE VALLEY TOWN CENTRE` has 59 of 327 units geocoded
  (18%) and `THE HAMPTONS, GRANVILLE` has **0 of 119**. Point-in-polygon would
  resolve 128 of 537 units and leave the big ones untouched. So the real choice
  is a 3-way judgment call — **even split / assign to the first-named hood /
  drop loudly** — not an engineering task. (Tier 1 is 34.6% geocoded and does not
  need geometry anyway.)
  **Scope is CONTAINED to permits** (measured across all five hood-bearing raw
  sources): `fire_response`, both Property CSVs and the historical assessment
  file carry either a numeric `neighbourhood_id`/`Neighbourhood ID` or clean
  single names — **zero comma rows**. In the raw permits file the pattern is 546
  rows / 92 distinct names (0.22%), and **92 of the 95 names that miss the
  boundary file are this one pattern** — so handling comma-lists makes the permit
  name join essentially clean. Not an architectural name-vs-geometry problem.
  ⚠️ **It also cannot GROW**: every affected row predates 2021, so the January
  `PERMIT_YEARS` roll never makes it worse. Safe to defer.
  ⚠️ **One correction to the tier split recorded above:** the first pass called
  it 1,273 / 537 by checking each comma-part against the boundary names *without*
  applying `NAME_CORRECTIONS` first. Re-derived with corrections applied, it is
  **1,245 / 565** — `CHAPPELLE AREA, HERITAGE VALLEY AREA` (28u) is genuinely
  ambiguous, because `CHAPPELLE AREA` resolves to CHAPPELLE, a different real
  hood. It had been about to be "fixed" into the wrong hood.

  </details>
  ⚠️ **This is `a-finer-rendering-audits-the-aggregate` again** — the per-year
  series surfaced a two-month-old defect in the aggregate on its first run.
  ⚠️ **And `check_unmatched_names.py` does NOT cover this path** — it guards the
  assessment money path only; the permit join is warn-not-fail by design, so the
  warning has been printing into the pipeline log unread (the project's standing
  failure mode). Consider whether the guard should extend here.

- [ ] **RATIO vs MONEY — the two remaining colour mismatches, DEFERRED by Peter
  2026-09-12 ("eh leave it till later").** Found while fixing the third (the
  institutional band, now shipped — `DECISIONS.md` 2026-09-12). Both are
  measured, neither is started. Same palette in both views; what differs is what
  the ramp MEANS:
  - **(a) Anchors + transform.** Money is sqrt from **true zero**, user-
    toggleable to linear. Ratio is **log from p2.5**, hardcoded. So the darkest
    colour means *$0* on one view and *"$268/road metre or less"* on the other,
    and **9 kept hoods pile up at that floor rendering identically** (RIVER
    VALLEY GOLD BAR at $161 draws the same as a hood at $268, 1.7x apart); 9 more
    clamp at the top. The legend does label it `≤ $268`, so it is disclosed, not
    hidden. ⚠️ **The log was chosen deliberately** (`FINDINGS` §6.4: raw skew
    19.7, log 0.32) — changing it will flatten the visible spread hard, so
    **re-measure the distribution before touching it**; this is not a one-line
    swap.
  - **(b) `#coloradj` is hidden in Ratio**, so a reader who sets "Colour: linear"
    on Money switches to Ratio and silently gets log anyway, with no control and
    no indication the setting stopped applying. Independent of (a) and much
    smaller — but note it cannot simply be shown until (a) decides what the
    toggle would even switch between here.
  ⚠️ **Do not treat (a) as a bug to fix on sight** — it is a live design
  question (is cross-lens colour comparability worth flattening the lens's own
  signal?), and Peter has seen it and chosen to defer.

- [ ] **INVESTIGATE — `lot_size` holds ownership shares for an unknown number of
  records; 7,984 rows are under 1 m².** Opened 2026-09-01, found by the
  50 m Glass grid (`docs/DATA_ISSUES.md` §E has the full measurement).
  ⚠️ **The MAP half is CLOSED and LIVE (2026-09-02, #312 + refresh) — what is
  still open here is the DATA question only:** what produces the other 7,981
  rows, which is the bar for making this sendable. **Do not re-open the
  rendering side.** (Also: they are commercial storefronts, not condos as
  first recorded.)
  - Confirmed for exactly one parcel: three WESTMOUNT accounts
    (4259396/4259412/4259420, $859,500) whose `lot_size` reads
    0.505/0.218/0.277 — **summing to 1.000**, i.e. shares, not m².
  - ⚠️ **The hypothesis does NOT generalise yet** — only 3 of 158 coordinate
    groups containing sub-1 m² lots sum to ~1.000. What produces the other
    **7,981** rows is unestablished, and it may be several different causes.
    **Do not write a report until that is settled**; a publisher who finds one
    counter-example bins the whole thing.
  - ⚠️ ~~**Not user-visible**~~ — **WRONG, and it was wrong when written
    (corrected 2026-09-02, Peter found it on the live public site).** It checked
    picking and colour and missed **height**: `gridScale` anchors spike
    elevation on the MAXIMUM cell, so this artifact set the vertical scale for
    all 93,201 cells and squashed p97.5 to **0.249%** of full height. Public
    root, Money → Revenue *or* Value → 50 m grid → Lot acres.
  - ✅ **THE MAP DEFECT IS FIXED (2026-09-02)** — `MULTI_UNIT_MIN_LOT_M2`
    (`src/export_value_grid.py`): a **multi-record** point totalling under
    10 m² of lot area leaves the lot-acre metric. `lot_needle_ratio` 79.01 →
    13.93; 50 m and 100 m now agree (13.93 vs 12.82). Cost: 4 changed fields,
    all WESTMOUNT, all ≈0.05%. **What remains open below is the DATA question,
    not a rendering one.**
  - ⚠️ **Do NOT widen the rule to single-record points.** 381 of them hold real
    tiny parcels (median 8.4 m², median value $500 — stalls, slivers). And a
    record-level floor at 1 m² is worse: sub-1 m² values are a *continuous
    graded series* (0.279/0.558/0.837/1.394/5.02 — multiples of one base share)
    inside 400-unit towers, so it halves a coherent population and cascades 66
    points into `majority_null`, dropping **$1.43B (0.598% of city value)** to
    remove $859,500. Tests pin both directions.
  - ⚠️ **The dedupe heuristic is NOT the bug** (`FINDINGS_lot_dedupe.md` §3):
    the three values are distinct and unrepeated, so the rule passes them
    through. Don't "fix" `SHARE_MAX_M2`.
  - ~~Blocks re-tightening `lot_needle_ratio`~~ — **re-pinned 2026-09-02 to
    6.96–20.89 (reading 13.93)**, the condition its own note set. ⚠️ **The old
    band could never have caught this**: 39.5–118.52 was fitted *around* the
    needle, so 79 sat comfortably inside it. Still ±50%, not ±25% — the new
    value has zero observations in the post-fix regime. Also re-pinned:
    `ineligible_points` 28–84 → 42.5–127.5, of which **only +1 is this rule**;
    the rest was the organic drift its own note predicted (56→58→60→**84**),
    which had hit the band ceiling exactly and would have red the next weekly
    publish on its own.
    ⚠️ **That anchor reads `value_grid_50.json`, NOT the served default**
    (2026-09-01, `check_value_anchors.py`) — the 100 m grid merges these three
    records with neighbours holding real lots and the needle disappears
    entirely, so guarding the default would mean this item's defect is no
    longer detected at all. Do not "simplify" the guard back onto the
    canonical file.
  - To promote to a numbered issue it needs a standalone notebook that
    reproduces the population from a live fetch — the bar all five numbered
    issues clear.

- [ ] **CAPTURE — REPEAT LOAD RUNS on both machines, and a CONTROLLED re-run.**
  Opened 2026-09-01; rescoped three times as captures landed. **SHELVED
  2026-09-02 at Peter's call** — the numbers below are recorded, the remaining
  work is measurement, and nothing is broken.
  - ✅ **The old laptop's pan fps is CAPTURED** (2026-09-01, below) and ✅ **its
    GPU is IDENTIFIED** (2026-09-02, below). Both were the long-open halves.
  - **Still missing:** **repeat load samples on either machine** (see the
    variance finding below), and a **controlled** pan re-run — the one we have
    was taken at a short viewport with browser extensions live (below).
  - ✅ Peter's pan claim (*"pans more smoothly on the newer one"*) is
    **CONFIRMED**: 117.3 vs 36.6 fps at 100 m, and the old laptop was measured
    at **22% FEWER device pixels**, so the confound runs in its favour.
  - **Added 2026-09-01: time the Detail-button grid SWITCH, both directions —
    and note the two halves are now in different states.** The bytes half is
    settled: transfer, already gzipped, only ~6% of trimming available and not
    worth taking, and **100 m is now prefetched on idle so its switch should
    feel instant** (`docs/PERFORMANCE.md`). What is **un-costed** is the deck.gl
    layer rebuild and first GPU upload of 93,201 instances, which **cannot be
    measured on the Oracle box** (SwiftShader).
    - ⚠️ **The 100 m switch is now the diagnostic.** Its bytes arrive before the
      click, so if it *still* feels slow, the cost was never the payload and the
      number to get is the layer rebuild.
    - ⚠️ **50 m on a PHONE is the untested case that matters most** — the hover
      warm buys almost nothing on touch, so a phone pays the full 2.78 MB at tap
      time (`docs/MOBILE_USABILITY.md` §2b). ⚠️ **The FEEDBACK half was answered
      2026-09-05** — the cost is now stated on the button before the tap and by
      `#gridbusy` over the map during the fetch (`DECISIONS.md` 2026-09-05) —
      but **the wait itself is still untimed on real mobile data, and the new
      indicator has never been seen on a device either.** Annotating a wait is
      not measuring it; this bullet stays open for the measurement.

  | field | old A | **old B (2026-09-01)** | gaming A (short) | gaming B (tall) |
  |---|---|---|---|---|
  | `dpr` | 1 | **1** | 1.364 | 1.364 |
  | `cssPx` | 1534x503 | **1534x551** | 1363x264 | 1363x428 |
  | `devicePx total` | 771,602 | **845,234** | 668,880 | 1,083,214 |
  | `ttfb_ms` | 26 | **56** | 178 | 150 |
  | `domInteractive_ms` | 481 | **780** | 800 | 409 |
  | `loadEvent_ms` | — | **827** | — | — |
  | `pan fps @100 m` | not captured | **36.6** (295 fr / 8 s) | 139 | 117.3 |
  | `pan fps @50 m` | not captured | **21.4** (171 fr / 8 s) | 133.9 | 105.2 |
  | 50 m cost | — | **42%** | 3.7% | 10.3% |

  **The old laptop's GPU, 2026-09-02 — `about:support`, one adapter only:**
  **GPU #1 `Active: Yes` — Mesa Intel(R) HD Graphics 4400 (HSW GT2)**,
  `0x8086`/`0x0a16`, driver **`mesa/crocus` 25.0.7**, `RAM: 0` (UMA).
  `Target Frame Rate: 60`; `Display0: 1600x900@60Hz`. Firefox 153 **snap**
  (`canonical-002`) on **Wayland**, Ubuntu 24.04, 7.5 GB RAM.
  - **So the machine pair is Haswell GT2 (2013, 20 EU) vs Tiger Lake Iris Xe
    (2020, 96 EU)** — two integrated parts ~7 years apart. No discrete GPU
    exists on either machine (the other's RTX 3050 Ti is `Active: No`).
    `crocus` is Mesa's **legacy** driver for gen4–gen7; `iris` starts at
    Broadwell. This is a representative low end, not a broken machine.
  - ⚠️ **The sanitised WebGL string was RIGHT this time** (`Intel(R) HD
    Graphics`) after being **wrong** on the other machine (it read HD Graphics
    for an Iris Xe). That does not rehabilitate it — it means the placeholder is
    unreliable in **both** directions and the string cannot tell you which case
    you are in. Always read `about:support`.

  ⚠️ **THE LOAD COMPARISON IS NOT ESTABLISHED — WITHDRAW THE EARLIER FINDING.**
  The same machine read `domInteractive` **800 ms then 409 ms**. That 2x spread
  is *larger than the between-machine difference the whole item exists to
  explain* (481 vs 800), and the gaming laptop's fresh reading (**409**) is
  **faster** than the old laptop's single sample (481) — the reverse of the
  reported symptom. **Nothing about load can be concluded from single samples**,
  including the 2026-09-01 "confirmed, and mostly network" entry in
  `DECISIONS.md`, which rested on the 800 ms reading alone.
  - Why this was invisible before: **the fps figures aggregate ~900 frames over
    8 s, while every load figure is n=1** — one navigation, unrepeatable without
    a reload. The same table mixes a well-sampled statistic with a single draw.
  - **Next:** at least 3 reloads per machine, report the spread, not a point.
    Only then is the ttfb split (150–178 vs 26–56) worth interpreting.
  - ⚠️ **And the ttfb split may not be about the site at all.** The old laptop's
    profile carries `security.pki.mitm_canary_issuer` naming an **Aruba network
    appliance**, i.e. TLS interception on some network it has used, and has
    `network.http.speculative-parallel-limit: 0` /  `network.prefetch-next:
    false` / `network.dns.disablePrefetch: true`, which suppress Firefox's own
    speculative connections and add first-connection latency. **Whether the two
    machines were on the same network was never recorded.** (Those prefs do
    **not** affect the site's idle prefetch — that is a JS `fetch()`.)

  ✅ **The 50 m grid's GPU cost is REAL, VIEWPORT-DEPENDENT, and HARDWARE-
  DEPENDENT — 10.3% on Iris Xe, 42% on Haswell GT2.** There is no single number.
  The 3.7% first measured was a short-viewport artifact, exactly as flagged.
  - Superlinear in viewport because a taller window shows **more cells**, not
    just more pixels per cell: both geometry count and fragment load rise.
  - ⚠️ **Do not extrapolate hard from two points.** Fullscreen on the gaming
    laptop is ~2.07M px, **1.91x run B** — plausibly worse than 10.3%, but that
    is arithmetic, not a measurement. Capture it before quoting it.
  - **Still acceptable, and the option STAYS** (Peter, 2026-09-01): opt-in,
    lazily loaded, starts unselected, and 21.4 fps is degraded rather than
    broken. Only the **quoted cost** changes, from a single figure to a range.

  ⚠️ **WITHDRAWN 2026-09-02 — the "marginal ms per cell" arithmetic, including
  the 0.274 / 0.981 ms figures this item previously recorded.** `about:support`
  shows the old laptop is **vsync-capped at 60 Hz** (`Target Frame Rate: 60`,
  60 Hz panel) while the gaming laptop reported **117–139 fps**, i.e. above 60.
  **The two machines were never in the same presentation regime.**
  - rAF frame times **quantise to multiples of 1/refresh**. The old laptop's
    36.6 fps is a *mix* of 1- and 2-vsync frames (~64% spilled), not a 27.3 ms
    render; bounding its true marginal cost gives a range of roughly
    **3–36 ms**, so any point estimate inside that is not a measurement.
  - ⚠️ **The recorded 0.981 ms is smaller than that machine's own vsync quantum**
    (6.9–8.3 ms). It cannot be a measured render cost.
  - **What survives:** mean fps over ~900 frames is a sound *monotone proxy* for
    render cost **within one machine at a fixed viewport**, because sub-quantum
    changes shift how many frames spill. So the **within-machine ratios (42% vs
    10.3%) stand**, and the ~4x difference in relative impact between the two
    GPUs stands. Converting fps to milliseconds and comparing **across**
    machines does not.
  - `client-perf-snippet.js` now captures a `refresh ceiling (idle rAF)` row and
    warns when a reading is within 5% of it. ⚠️ **Gaming A's 139 fps trips that
    guard against a plausible 144 Hz panel** — that run may be clipped, which
    would be a *second*, independent reason 3.7% was meaningless.

  ⚠️ **NEITHER pan capture controlled the browser environment.** The old-laptop
  run had **Dark Reader, AdBlock and uBlock Origin all enabled**; Dark Reader can
  apply a page-level CSS filter, which is a fill-rate cost scaling with viewport
  pixels — the exact variable under test. The gaming laptop's extension set was
  never recorded. **A controlled re-run means: extensions off, viewport tall.**

  ✅ **RESOLVED for the gaming laptop, and it overturns the premise: it is
  running INTEGRATED graphics.** `about:support` 2026-09-01:
  - **GPU #1 — `Active: Yes` — Intel(R) Iris(R) Xe Graphics** (`0x8086`/`0x46a6`),
    corroborated by WebGPU (`wgpuDeviceType: "IntegratedGpu"`).
  - **GPU #2 — `Active: No` — NVIDIA GeForce RTX 3050 Ti Laptop GPU.**
  ⚠️ **So the discrete card has never been in ANY measurement.** The comparison
  was never gaming-GPU vs old-integrated; it is **Intel Iris Xe vs an older
  Intel**, i.e. two integrated parts a few generations apart. Every fps figure
  above — including the 10.3% — is an **Iris Xe** number. **This site has no
  discrete-GPU measurement at all.**
  ⚠️ **Nothing in this codebase can change that.** Which adapter Firefox gets is
  a Windows per-app graphics preference (Settings -> Display -> Graphics) or the
  NVIDIA control panel. Worth switching only to measure the ceiling — integrated
  is the more representative case for the audience, so it is the better default
  to keep tuning against.
  ⚠️ **The placeholder was not merely vague, it was WRONG about the part.** It
  read `Intel(R) HD Graphics`; the adapter is **Iris Xe**, a materially faster
  and much later line. Refusing to read the sanitised string was right, and the
  gap between placeholder and truth is bigger than "less specific".
  ⚠️ **The OLD laptop's GPU is still unidentified** — same placeholder, never
  checked, and it is the machine with the actual pan complaint. Get its
  `about:support` -> Graphics with its fps run.

- [x] **DECIDE — `origin/docs/viz-stack` … 272 lines that never got a PR.**
  Surfaced 2026-08-31 during the branch prune; **LANDED 2026-09-16 (S165)** as
  `docs/VIZ_STACK.md`, cherry-picked onto a fresh branch off master. §0/§1 were
  re-measured on landing (sizes had drifted hard: `web/data/` 8.4 → 16.1 MB, boot
  file 1.4 → 1.04 MB, and the 7.63 MB `value_grid_50.json` did not exist when the
  doc was written); §7's Pages Range check re-run green; §2 left as a dated
  third-party observation and flagged as un-re-measured. The two `VIZ_STACK.md`
  citation warnings in `check_doc_citations.py` resolve as a side effect.
  - One commit (`0efd62b`, 2026-08-07) adding `docs/VIZ_STACK.md` (+272) and a
    `TODO.md` block (+31). **No PR was ever opened**, so nothing has ever
    reviewed or rejected it — it is unmerged by neglect, not by decision.
  - ⚠️ **Not a duplicate of master's `docs/STACK.md`.** Different file,
    different scope; don't assume the shipped stack inventory covers it.
  - S99 (2026-08-07) kept it deliberately: it deleted the *other* stack branch
    (`claude/kunicki-app-stack-analysis-hs3kiv`) only after confirming
    `VIZ_STACK.md` was byte-identical on both, and left this one intact.
  - Nothing outside `session-summary/archive/2026-08-07-s99.md` references the
    file. Read it, then land it, fold it into `docs/STACK.md`, or close it with
    a reason on the record — **the one outcome to avoid is a fourth session
    walking past it.**

- [ ] **PROPOSE-FIRST — `refresh.yml`'s token fallback hid an unset secret for
  months, and the secret is now load-bearing.** Opened 2026-08-31 after the
  weekly refresh failed.
  - `refresh.yml:48` checks out with `secrets.HEARTBEAT_TOKEN || github.token`.
    The secret had **never been set**; the fallback ran as the
    `github-actions` bot and worked fine — until `master` gained a required
    `test` status check, which the bot cannot bypass. First red: 2026-08-31.
  - ⚠️ **The failure mode is exactly the one the surrounding comments guard
    against, one step removed.** They reject `git push || true` because an
    EXPIRED token would report green — but nothing catches the secret being
    **ABSENT**, which is the same silence with a different cause.
  - Proposal: a step that fails loudly when `HEARTBEAT_TOKEN` is unset, so the
    fallback stops being a silent downgrade. **Changes CI behaviour — propose
    before building.** ⚠️ Decide what it does on a *fork or a fresh clone*,
    where no secret exists and hard-failing would be wrong.
  - ⚠️ **Token expires ~2027-09-01** (fine-grained max, 366 days). When it
    lapses the refresh goes red the same way. `RUNBOOK.md` §3.

- [ ] **OUTREACH TRACKER — TEN data issues found, ZERO sent. Every one is
  Peter's call.** ✅ **AS OF 2026-09-17 (S169) NOTHING IS BLOCKED ON WORK.** All
  five sendable issues now carry both published evidence and drafted report
  text; issue 6 was the last gap (notebook + draft landed that day). **The only
  thing between every one of them and a send is the decision to send.** ⚠️ **Count corrected 2026-09-16 (S166): the item said "five",
  and `DATA_ISSUES.md` now carries 10 rows and 11 `NOT SENT` markers. The
  substance did not go stale — it got BIGGER, and "zero sent" is still exactly
  true.** This is the project's standing failure mode in its purest form: a
  finding that never leaves the repo. ⚠️ **`docs/DATA_ISSUES.md` "Status at a glance" is
  AUTHORITATIVE** — this is a one-line mirror so the count is visible from the
  file that gets read every session. If the two disagree, that file is right and
  this is stale.
  - Channel: **`opendata@edmonton.ca`** (portal footer, read 2026-08-25).
    Assessment & Taxation is the *escalation*, not the first stop.
  - **A SECOND channel, added 2026-09-10 (S154): `infrastructure@edmonton.ca`**
    (listed on *Development Impact on Infrastructure*). **One email, NOT SENT,
    not written**, carrying three asks: **Q1(a) bullet 2** (the $600k / $1.9M /
    $1.5M per km — centreline or lane-km?), the **lane-km-by-road-class table**,
    and **`DATA_ISSUES.md` G** (the Snow & Ice report's p4 "linear km" vs p16
    lane km). Detail in the Q1(a) item above. ⚠️ **Deliberately NOT a row in
    the table below** — that table mirrors `DATA_ISSUES.md`'s numbered issues,
    and G is still a candidate there. **Q1(a) is the load-bearing ask** — the Q1
    rewrite is held on it.

  | # | issue | blocked on |
  |---|---|---|
  | 1 | `Period of Coverage` names the wrong year | **nothing — the draft is written**, `docs/DRAFT_bug_report_coverage_year.md` |
  | 3 | `qi6a-xuwt` drops 2,448 accounts | **nothing — the draft is written**, `docs/DRAFT_bug_report_historical_dropout.md` |
  | 4 | no per-parcel exemption status | **nothing — the draft is written**, `docs/DRAFT_open_data_request_exemption_status.md` |
  | 5 | 3 of 5 school boards absent | **nothing — the draft is written**, `docs/DRAFT_open_data_request_school_locations.md` |

  - ✅ **REPORT TEXT WRITTEN FOR 1, 3 AND 5 ON 2026-09-17 (S169).** **All four
    sendable issues now have both published evidence and a drafted message, so
    nothing is blocked on work any more — the only thing left is Peter's send
    decision.** Each draft re-verified its own premises against the live portal
    the day it was written, because a report whose premise moved is worse than
    none: the coverage string is still wrong **and survived the 2026-09-14
    refresh** (a new fact — it is unmaintained, not merely stale);
    `qi6a-xuwt` has not been republished since **2026-01-12**, so the dropout
    stands; and the school absence was re-searched and still holds. The live
    residential base re-measured to **$162,309,281,500**, matching August
    exactly. ⚠️ **Each draft carries a re-check instruction in its own "Notes"
    section** — an absence can be falsified between writing and sending, and a
    corrected field means the report should be dropped, not sent.
  - **Issue 4 is the only one that could go today.** ⚠️ **Do not put the
    $125.4M figure in it** — that asserts an exemption status no public source
    states.
  - **1 and 3 are one email's work each** now that both pages are live and
    linkable; 1 is the cheapest of all five (a single field edit on their end)
    and has never had a draft.
  - **Issue 2 is not outreach** — it is ours, caused by issue 1, and needs a
    decision rather than a message (its own item below).
  - ⚠️ **Detailed context lives in the two long items further down** (the
    `qi6a-xuwt` bug report, and the open-data request). **Do not duplicate their
    content here** — this item exists to make "zero sent" impossible to miss,
    which is exactly how the `qi6a-xuwt` report went invisible for six days
    inside a closed parent.

- [ ] **ACTIVE — how many properties are silently absent from the published
  current roll? One case is proven; the population is a guess.** Full context:
  `docs/DATA_ISSUES.md` "Possible issues" §A. Promoted to active work
  2026-08-26.
  - **The proven case:** Misericordia Community Hospital, continuously assessed
    2012–2025 as `10095840` (~$200–260M, WEST MEADOWLARK PARK), renumbered to
    `11495573`, **absent from `q7d6-ambg` until 2026-08-03**. The map understated
    that neighbourhood by **~$250M** for the duration, and nothing flagged it.
  - **The unproven part:** `tools/audit_roll_continuity.py` (re-run 2026-08-30 vs
    historical 2024) finds **1,457 of 426,913 parcels — 0.34%, $1.07B** with no
    current match, by POSITION (all three identifiers churn, so none can match).
  - ⚠️ **THIS REPLACES 1,534 / $1.62B, re-measured 2026-08-30.** Of 1,578
    position-unmatched parcels, **121 ($592M — 35.6% of the value) are still on
    the roll under the same account number**, recentroided past the 5 m
    tolerance. **The three largest cases the backlog named for three weeks were
    never missing.** Detail + the do-not-widen-the-tolerance warning are on the
    long item further down; don't re-derive them here.
  - ⚠️ **Those 1,457 are candidates, NOT verdicts, and an upper bound.**
    Demolitions, subdivisions and consolidations are indistinguishable from a
    dropout from the outside. **The whole job is separating them** — that is what
    makes this unreportable today, not the measurement.
  - ⚠️ **Do NOT treat identifier churn as the defect.** Renumbering runs
    0.15%–0.37%/yr routinely; `data/DATA.md` states outright that a vanished
    account number is not by itself a finding. The defect is a property absent
    from the roll **while still being assessed**.
  - **Why it is worth the work:** it is the same dataset as `DATA_ISSUES.md` §1
    (the coverage-year mislabel), so a confirmed result could ride along in that
    report instead of needing its own. And it is a **live understatement of the
    map**, unlike every other row in that file.
  - **Done looks like:** a standalone notebook in the house pattern — live
    sources only, figures recomputed at run time, invariants asserted, rendered
    to `web/notebooks/` and added to that folder's hand-written `index.html`.
    ✅ The re-measure this used to ask for is **done (2026-08-30)** and the
    per-parcel baseline is committed at
    `data/roll_continuity_candidates_2026-08-30.csv`. ⚠️ **What is still missing
    is the transient/permanent split** — that needs one more observation diffed
    against that file, and it is the only thing that would make a notebook worth
    writing. A notebook on today's figures would publish an upper bound.

- [ ] **PETER'S CALL — the amenity bands are FIXED at 600 m / 800 m
  (`AMENITY_BANDS` in `web/index.html`).** Built and live behind the weekly
  refresh 2026-08-23; the filter works, the numbers in it are conventions.
  ⚠️ **The control is INFILL-ONLY as of 2026-08-26** — built in Glass, extended
  to Infill 2026-08-25, and the Glass copy removed on Peter's call
  (`DECISIONS.md` 2026-08-26). One place to change now, not two.
  - **What a change would cost:** the band value is repeated in each row's
    tooltip copy, so `AMENITY_BANDS` and the two `title=` strings move together
    (the code comment says so).
  - **Undecided:** whether the LRT band should follow the activity window
    picker — the 3yr kernel wants 800 m where the 5yr wants 600 m. A band that
    moves under the reader needs a reason better than symmetry.
  - **Not urgent.** 600 m is the TOD walkshed convention and 800 m the usual
    school-walk figure; both are defensible as they stand.
  - ⚠️ **Do NOT fold distance into the Infill score** without deliberately
    reopening `DECISIONS.md` 2026-08-22 — proximity is a desirability input, and
    a weighted term nothing can falsify is exactly what that decision refused.
    The Infill highlight grid is a filter overlay, not a step toward this.

- [ ] **PETER'S CALL — the road service life is 50 years and figures in public
  circulation use 25.** Both readings sit on the SAME City page we
  already cite (`city_unit_costs.json` → `roadway_om_renewal.source`,
  "Development Impact on Infrastructure"), which publishes the life as *"usually
  25, extended to 50 with proper maintenance"*. Your call 2026-07-15 took 50.
  - ⚠️ **This is a denominator choice, NOT a data discrepancy** — same $600,000/km
    O&M numerator either way. Do not "reconcile" it by changing the value.
  - **What the choice is worth:** the O&M half is **$12,000/km/yr** at 50 yr vs
    **$24,000/km/yr** at 25 — exactly 2×. The full lifecycle rate the site
    actually ships is **$50,000/km/yr**; at 25 yr it would be **$100,000/km/yr**
    (already recorded as `roadway_om_renewal.sensitivity`).
  - **Why 50 still looks right — but on weaker ground than this item claimed
    until 2026-09-03.** The same page's ~3%/yr set-aside rule on $1.5M/km ≈
    **$45,000/km/yr** does point at the 50-year $50,000 rather than the 25-year
    $100,000. ⚠️ **But it is NOT an "independent cross-check" and this item used
    to call it one.** The City defines that 3% as covering
    operate+maintain+renew+replace — the same $2.5M bundle over the same life —
    so it is the same page's arithmetic restated, and $45k vs $50k is just a
    rounded 3% against the bundle's actual **3.33%/yr**. The rule is
    asset-specific in the source too (fire stations get "at least 6%").
    **What survives:** it still *discriminates* 50 from 25 directionally, since
    the life is the only free variable (3.33% vs 6.67%). **What does not:**
    calling it independent confirmation. Full reasoning in
    `city_unit_costs.json` → `roadway_om_renewal.cross_check`. **This does not
    reopen the 50-year choice** — it removes one supporting argument, and the
    choice was Peter's call on the page's own "extended to 50 with proper
    maintenance", not on the 3% rule.
  - **The decision is only whether the methodology note should SAY SO.** Right now
    nothing in the UI or `DATA.md` explains why a reader who has met the 25-year
    figure elsewhere sees half of it here. Verified 2026-08-20 against served
    output, not config (least-squares back-solve on
    `neighbourhood_value_per_acre.geojson`: road $50.0001/m/yr, fire
    $3,142/event, 404 hoods).
  - ⚠️ **The secondary write-up that carries these figures is NOT a citable
    source and must not be named** in `DATA.md`, methodology notes, UI copy, or
    commits — it publishes them with no footnote. We cite the City page
    directly; that we independently hold the same numbers is a confidence
    signal, not a citation. An accompanying *"30% of road users are not
    Edmonton taxpayers"* claim is traceable to nothing in our reference list and
    must not be repeated even informally.
  - [ ] **DEFERRED 2026-09-03 (Peter: "later") — verify the four external
    service-life figures before any of them informs this call.** Relayed
    road-cost research surfaced: a **60-year** reconstruction life from a City
    staffer (ConstructConnect/Journal of Commerce, 2016, with microsurfacing at
    10 and 40 yrs and overlay at 30); **Alberta Transportation's 20-year**
    pavement design life (provincial highways, not municipal local roads);
    **Calgary "up to 20 years"** for full reconstruction; **Winnipeg 25 years**
    for asphalt *regional* streets (not local). ✅ **A fifth, PRIMARY and checked
    (2026-09-10, S154):** the City's *2023 Infrastructure State and Condition
    Report* p27 gives Roads **average age 43 yrs vs expected life 33 yrs**
    ($9,747,485,291 replacement value). ⚠️ **Asset-class figure** — all roads,
    arterials included, not a neighbourhood street — so it is context, not a
    third reading of the 25-vs-50. ⚠️ **NONE HAS BEEN CHECKED** —
    they are relayed claims of exactly the shape that produced a year-late
    source date in the same batch (`DECISIONS.md` 2026-09-03). **Grep/fetch
    before use.** ⚠️ **Even if all four verify they do not settle this item** —
    it is a *denominator choice* between two readings on the City page we
    already cite, and an Alberta-highway or Winnipeg-regional figure is a
    different asset class. They are context for the methodology note, not a
    tiebreaker.

- [ ] **T8 FOLLOW-UPS — the three unchecked category sets were AUDITED 2026-08-30
  and none carries the 2026-08-18 defect.** Two follow-ups survive; the sweep
  itself is done (`docs/AUDIT_LEDGER.md` 2026-08-30, verdicts + measurements).
  - ✅ **`load_zoning` (area numerator, highest risk) — PASS.** `frac_other` and
    `rev_frac_other` are **0.0000 across all 406 hoods**: every zone code in the
    served `zoning.geojson` classifies, so nothing lands in the unmatched bucket.
  - ✅ **`load_water.HOUSEHOLD_CLASSES` — PASS.** Vocabulary fully enumerated;
    the only household-like class excluded is `FARMLAND` (512 parcels, 0.12%),
    consistent with the residential-only lock (2026-07-06) and logged out-of-scope.
  - ⚠️ **`load_temporal.COMMERCIAL_CLASSES` — WARN, and it is FORCED.** It tests
    `Assessment Class 1` only, but a parcel carries up to three classes: 1,094
    parcels / **$9.06B** have a class 2. Effect is bounded and nearly
    self-cancelling citywide (**−0.50%**, 22.10% vs 22.21% apportioned) but not
    per hood — **max 6.5 pp, 23 hoods >1 pp, 3 hoods >5 pp** (worst: EDMONTON
    SOUTH CENTRAL EAST −6.54, U OF A FARM +6.33). ⚠️ **Do NOT "fix" it by
    apportioning the live half:** `qi6a-xuwt` publishes `mill_class_1` only, no
    class 2/3, so the archive half CANNOT be apportioned and doing one side
    alone would break splice consistency — a worse error than the one it fixes.
    - ✅ **DOCUMENTED 2026-08-30** — `docs/SPEC_temporal.md` §3 carries the cut,
      the per-hood cost and why apportioning one half is worse than the error it
      removes; locked in `DECISIONS.md` the same day. **Nothing is open here —
      do not reopen it as a code change.**
  - ✅ **CLOSED 2026-08-31 — the `other`-in-`frac_nonres` contradiction is gone,
    resolved by DELETING the column.** Nothing consumed `frac_nonres` (it never
    reached the served GeoJSON), so the contradiction had no consumer, only a
    trap. ⚠️ **Measuring the exposure changed the fix:** the served path was
    already honest — `frac_other` renders as "Unclassified" grey. The real
    weakness was `_categorize` only **warning**, which a weekly CI refresh
    swallows; the monthly digest now reports it
    (`vintage_report.check_unclassified_zoning`) rather than failing the
    pipeline. `DECISIONS.md` 2026-08-31. **Nothing is open here.**
  - ⚠️ **METHOD, and it cost a wrong number in this very run:** a parcel-level
    cross-tab on `Property_Info.zoning` said `other` held **$36.8B**. It does
    not — that column's vocabulary is not the one the metric uses
    (`zoning.geojson`). **Audit the actual numerator, never a proxy for it.**
  - **Already settled, do not redo:** `RESIDENTIAL_BUILDING_TYPES` is CLEAR
    (its `units_added` numerator is self-checking — 8 of 25,146 permits carry 0
    units); `export_budget_ranked.py`'s `SERVICE_CATEGORIES` is hardened by
    derivation (`DECISIONS.md` 2026-08-16).
  - ⚠️ **Rank by NUMERATOR, not by how wrong the names look.** A count or
    value-sum over an enumerated category has no self-check — every member
    counts for its full weight whatever it is. A quantity numerator limits the
    damage on its own.
  - Full reasoning: `docs/DATA_INTEGRITY.md` T8, `docs/AUDIT_LEDGER.md`
    2026-08-18 and 2026-08-30, `docs/DECISIONS.md` 2026-08-18.

- [ ] **PETER'S CALL — should Industrial go PUBLIC now that it is grid-capable?**
  ⏸️ **PARKED 2026-09-17 on Peter's call: stays `/full/`-only, he decides when.**
  Not unargued any more — deliberately deferred. Do not re-raise it as an open
  call; the standing state is `/full/` and no code change is owed.
  `docs/DECISIONS.md` 2026-07-23 tagged the Industrial `#devmetric` `/full/`-only
  with one stated reason: *it's choropleth-only, so in public it would leave the
  new 3-way Detail selector with dead options*. ⚠️ **That reason expired
  2026-08-18** — Industrial now has its own 100 m cells, so it would leave no
  dead option. The tag was NOT changed; it is simply now unargued.
  - **What it would cost:** one `BUILD`-flag guard removed (`web/index.html`,
    the `state.hasIndPermits && FULL_BUILD` branch in `syncDevControls`) plus
    the public build's verify expectations.
  - ⚠️ **The public build has no other dollar-valued layer whose numbers are a
    DECLARED ESTIMATE.** The blurb discloses it, but a public reader is likelier
    to read "construction value" as money actually spent than a specialist is —
    weigh that, not just the control-surface tidiness.
  - Full reasoning + measurements: `docs/SPEC_industrial.md` A3 amendment,
    `docs/DECISIONS.md` 2026-08-18 (three rows), `docs/CONTROLS_MATRIX.md` §7.

- [ ] **THE RATIO AND USES PRISMS STILL PICK THE HOOD BEHIND THEM — same defect
  as the band prisms (fixed 2026-08-17), but the fix needs a call on OPACITY
  first.** Measured at pitch 55 over the U of A: hovering up a `ratio-extrusion`
  ghost prism returns `hood-hover :: RIVER VALLEY VICTORIA` / `WÎHKWÊNTÔWIN` —
  the flat hood layer beneath, not the prism the cursor is on. Uses' optional
  residential prisms are the same shape of problem.
  - **Why it was not fixed with the bands:** both layers ride
    `state.prismOpacity` (ratio's default is the 5% *ghost*; the slider reaches
    0). ⚠️ **A pickable prism at opacity 0 hijacks hovers over what looks like
    empty air** — the Services comment already names this trap ("an opacity-0
    layer would still tessellate, draw, pick, and highlight").
  - **The question is Peter's:** should a ghost prism own the hover at all? On
    `ratio` the ROADS are the subject and the prisms are context, so picking the
    prism may be the wrong answer even when it works. Options: always pickable;
    pickable only above some opacity; leave as is.
  - The band fix needs none of this — those prisms have no opacity control and
    the hood beneath them is deliberately blank.
  - Precedent + measurements: `docs/SPEC_revenue.md` "The banded prism is its own
    hover target", `docs/DECISIONS.md` 2026-08-17.

- [ ] **SERVICES' HOVER STILL TEASES A CHART ITS PANEL DOES NOT OPEN — the same
  defect fixed on the revenue cuts 2026-08-16, left live because the replacement
  copy is Peter's call.** In Services (with the cost columns shipped) the hover
  plots the **assessment-share sparkline** and says **`click to pin`**, while the
  click opens the **cost-against-revenue panel** (`servicePanelFor`, 2026-08-10).
  Measured, not inferred: `hoodPanelLens()` is `!serviceLens() || state.hasRoadsLife`,
  so the teaser is appended there like anywhere else. ⚠️ **Predicate name
  corrected 2026-09-16 (S166) — it read `state.hasSvcCost` until 2026-09-05,
  when the retired roads+fire composite took that flag with it; the gate had to
  name a column the PUBLIC build actually shows. The DEFECT is unchanged and
  still live — `web/index.html`'s own comment above `tooltipFor` says so:
  *"SERVICES IS NOT YET EXCEPTED though it should be … the hover still plots
  history under a click that opens costs."*
  - ⚠️ **`docs/CONTROLS_MATRIX.md` asserted the OPPOSITE** ("the sparkline is
    not [offered in Services]") from 2026-08-10 until this was measured on
    2026-08-16. The cell is corrected; the point is that the claim sat unchecked
    for six days because nobody hovered a Services hood.
  - **The fix is one predicate** — the revenue branch in `tooltipFor` already
    demonstrates it; Services needs `servicePanelFor(p)` treated the same way.
  - **What is NOT decided is the invite's wording.** The revenue cuts say
    `click for the revenue mix`; Services would need its own line (`click for the
    cost breakdown`?), and naming a "cost" in one phrase brushes the locked rule
    that ⚠️ **there is no single cost number and there cannot be** — two bases,
    ~10.8× apart, deliberately not summed (`data/DATA.md` §13, `SPEC_services.md`).
    A hint that implies one total would be the same class of error as the chart.
  - Precedent + full reasoning: `docs/DECISIONS.md` 2026-08-16 (the sparkline
    row), `docs/SPEC_temporal.md` §2 (the amended row).

- [ ] **The citywide budget panel is EXPERIMENTAL and full-build-only — decide
  whether it stays, and on what terms.** Built 2026-08-16 (`#budget`,
  `scripts/export_budget_ranked.py`, `web/data/budget_ranked.json`,
  `verify-budget-panel.js`, 26 checks). It ranks the FY2026 approved operating
  budget by branch: 43 service branches, then 5 that deliver no service.
  - **Peter's call, three separable questions:** does it stay at all; does it
    leave `/full/`; and does it get a phone form. Today it is **desktop-only by
    decision** — a 400px readout in a ≤390px column, and the slot it borrows
    (`#millrates`) re-parents into `#title` on a phone, so a phone form is a
    design question, not a width tweak.
  - ⚠️ **It is NOT a lens and must not be made one** — citywide totals, no
    neighbourhood dimension, nothing to draw. `DECISIONS.md` 2026-08-16.
  - ⚠️ **Its data does NOT ride the weekly refresh** and must not be wired into
    it: an *approved* budget moves ~annually (`rowsUpdatedAt` 2026-06-05).
    Re-run the script by hand after a Council budget or adjustment. The panel
    prints the SOURCE vintage, so a stale file is visible rather than silent.
  - ⚠️ **`deploy.yml` excludes `web/data/**` from deploy triggers**, so a
    regenerated JSON alone will NOT deploy — it needs a `web/**` code commit to
    carry it, or a manual run.
  - **Companion available and not built:** `m84q-ghmu` ("Approved Operating
    Budget - Revenues", 1,414 rows, same 8 columns) is the "where the money
    comes from" side. `data/DATA.md` §17's *"there is no revenue side here"* is
    true of the expense feed only. ⚠️ Worth weighing against item ▶ below —
    the revenue split (tax-funded vs fee-funded) is close to what
    `SPEC_breakeven.md` §8.7 is choosing between.

- [ ] **`change` does not carry the institutional treatment.** The consequence
  tier shipped 2026-08-15 on Money's prism mode and the Lab; `glass` followed
  2026-08-19 (`inst_frac` + azure cell bands, `DECISIONS.md`), leaving `change`
  as the one Money mode where the same neighbourhood is outlined-and-uncertain
  on one mode of a view and confident on another.
  - ⚠️ **THIS ITEM SAID `glass` WAS "BLOCKED ON DATA" AND IT NEVER WAS** — the
    cell-level share was one `groupby` off a join `revenue_by_zone` was already
    doing and discarding. The claim sat here unchecked from 2026-08-15 to
    2026-08-19 and would have kept deferring the work. **Re-measure a stated
    blocker before believing it**; that is now twice this file has been wrong
    about one.
  - `change` is share-of-base movement over time, a different quantity again —
    it may need its own answer rather than this one. ⚠️ **Do not assume it is
    blocked either.** Check what the change columns are derived from first.
  - ⚠️ **Re-measure before building.** The 6-hood set is `revenue_per_acre` on
    today's refresh; it moves with the roll.
  - ⚠️ **`value_per_acre` is NOT a candidate and never will be** — exemption
    changes whether a levy is collected, not what a parcel is assessed at.
    Don't "finish the job" by adding a `value_frac_inst`.
  - Full reasoning, both thresholds and the colour measurement:
    `docs/SPEC_revenue.md` "The consequence tier"; `docs/DECISIONS.md`
    2026-08-15 (the second entry, which amends the 2026-08-12 band decision).

- [ ] **BUG REPORT to Edmonton Open Data — the `qi6a-xuwt` 2024/25 dropout.
  Gated on Peter reviewing the notebook by hand; everything else is done.**
  ⚠️ **Re-promoted 2026-08-06 from `docs/TODO_archive.md`, where it had been
  invisible since 2026-07-31** — it was a sub-item of the temporal-graph item,
  which closed and took this, still unchecked, into the archive with it. The
  archive's own header says *"Nothing here is a to-do"*, so nobody would have
  looked. `tools/todo_archive.py` now refuses to archive a closed parent with
  unchecked children (same date). Nothing about the finding changed while it sat
  there.
  - ▶▶ **THE ARTIFACT IS NOW RUN, RENDERED AND PUBLISHED (2026-08-26).**
    `notebooks/standalone/historical_2024_gap.py` / `.ipynb`, served at
    **`/notebooks/historical-2024-gap.html`**. It supersedes
    `notebooks/exploration/03_historical_roll_gap.ipynb` (still there, outputs
    still cleared — **do not send that one**). Standalone: live API only,
    imports nothing from `src/`, every figure computed at run time, 6/6
    invariants asserted, ~4 min cold. **Peter can now read the rendered page
    instead of driving a notebook**, which is what was declined in the form
    offered on 2026-08-07.
  - ⚠️ **FIGURES REFRESHED — re-measured live 2026-08-26, quote these.** The
    account counts are unchanged from 2026-07-28 (**2,448** cumulative, **188**
    neighbourhoods, Downtown **1,292**), which also proves the dataset has NOT
    been corrected. The **value and shares moved** because the control is the
    current roll and the roll rolled to 2026: **$3.008B** (was $2.93B) and
    Downtown **48.4%** of that value (was 53%). Take the figures off the page,
    not from this list.
  - **Two things the run added beyond the old notebook.** (1) All 14 years, both
    detectors, so "11 of 13 testable years are clean" is shown rather than
    asserted — and the self-audit/current-roll disagreement is **464×**, which
    is the single most useful sentence for the City. (2) The loss is
    **building-shaped**: 2,448 accounts at **272 addresses**, **29 of which lose
    every account**; largest are 309 and 261 units at 10310 / 10360 102 ST NW.
  - **Incidental second finding, in the same dataset**: one Downtown address is
    published under three spellings (`102 STREET` / `102 SSTREET` /
    `102 STSREET`), so that building loses **315**, not 309. Cheap for them to
    fix; cut it if it muddies the report.
  - ⚠️ **NEVER the earlier inferred "~8,000"** — that was read off row counts of
    different vintages and most of that gap is new construction.
  - **Cite dataset IDs + the SoQL, not prose:** `qi6a-xuwt` (Historical) and
    `q7d6-ambg` (Current Calendar Year). The notebook prints both. City data
    staff will want exact resource IDs.
  - ⚠️ **LEAVE THE CAUSE UNSTATED.** Describe the symptom — whole multi-unit
    buildings absent together, citywide — and let the City diagnose. No
    speculation about leasehold/condo handling or ETL join logic, however
    tempting the address clustering makes it.
  - **The shipped site is UNAFFECTED** (built from `q7d6-ambg`, the complete
    roll). This is a good-citizen report, not a fix we need. Full evidence:
    `data/DATA.md` §0, `docs/SPEC_temporal.md` §0.1, `docs/AUDIT_LEDGER.md`
    (2026-07-28 row).

- [ ] **The Services panel grouping was never checked on a phone.** Shipped
  2026-08-02 (PR #145). It added 2 group captions + 1 row, so the panel grew by
  3 lines of shared DOM — and `CONTROLS_MATRIX.md` records that grouping drives
  desktop AND mobile. Verified at 1280x800 and 1440x900 only.
  - ~~⚠️ **A SECOND, LARGER thing now needs the same check: the Services HOOD
    PANEL**~~ — ✅ **TRACK MEASURED 2026-09-17 (S169), AND THE PREDICTED FAILURE
    IS FALSIFIED.** The layout claim re-verified in code first: the bar row is a
    3-column flex, 82px label / `flex:1` track / 40px percentage, gap 7px —
    but in **`web/styles.css:724-728`**, not `index.html`. ⚠️ **The track does
    not collapse on a phone; it is WIDEST there.** Desktop pins the panel to a
    fixed ~300px row, while on a phone it spans the viewport:

    | viewport | row | **track** | vs 1400px control |
    |---|---|---|---|
    | 1400 (control) | 300 | **164.0** | — |
    | 390 | 346 | **210.0** | **128%** |
    | 360 | 316 | **180.0** | 110% |
    | 320 | 276 | **140.0** | 85% |

    All four cost drivers, `hasTouch`/`isMobile`, panel open on DOWNTOWN,
    preconditions asserted (driver reached, single service checked, bars
    present) and the row width reconstructed from its three columns to 0.00px
    drift at every cell. Probe: `tools/profiling/probe-svcrow-track.js`.
    ⚠️ **The 1400px control is what makes this readable** — a probe reporting
    thin tracks everywhere would be indistinguishable from a broken one.
    ⚠️ **The worry was aimed at the wrong axis.** Bar legibility here is driven
    by the VALUE, not the viewport: at the narrowest track a nonzero fill is
    sub-pixel for **21.2% of hoods on bike ops** (86/406), 6.9% roads ops, 1.2%
    roads lifecycle, 0.5% transit — and widening to the 390px track only moves
    bike to 15.0%. Separately, **24 rows print a literal `0.0%` for a nonzero
    value** (17 of them bike), which is `index.html`'s own "reads as free rather
    than small" comment recurring one order of magnitude down. **Recorded, NOT
    fixed** — `fmtSvcRatio` is reader-facing wording, so it is a
    `COPY_DECISIONS.md` call, not a silent edit.
  - ~~A probe at 390/360/320 px returned **all zeros**~~ — **the zeros were the
    probe's fault, resolved 2026-08-03.** `#optpanel` carries `.folded` by
    default at ≤640px, so its rows have no layout box; remove the class first
    and everything measures. (The item already recorded this cause for the
    S74 left-edge work — it just wasn't applied here.)
  - ✅ **NO OVERFLOW, measured 2026-08-03** at 390/360/320 px with
    `hasTouch`/`isMobile`, Services active, the pod **unfolded**, and the panel
    at its **worst case — 10 visible rows and 3 captions**, i.e. after Stage 2
    added a caption and three more rows:

    | width | `#controls` | `#services` h | clearance to `#botleft` |
    |---|---|---|---|
    | 390 | l=8 r=382 | 230 | 235px |
    | 360 | l=8 r=352 | 230 | 206px |
    | 320 | l=8 r=312 | 244 | 178px |

    Nothing clips left, nothing overflows right, nothing falls below the fold.
    Headless Chromium measures text **wider** than the real font stack (quirk
    y), so a no-clip result there errs safe.
  - **STILL NEEDS CONFIRMATION:** real device, actual touch interaction with the
    rows (the probe drives `.click()`, which bypasses `pointer-events` — the
    standing verify-script caveat), and the **folded default** state, which is
    what a phone user actually meets first.
  - Read `docs/MOBILE_USABILITY.md` first; keep the CONFIRMED /
    NEEDS-CONFIRMATION split honest.

- [ ] **▶ THE DENSITY/INCOME CONFOUND — it applies to a lens that is ALREADY
  LIVE, and we cannot currently measure it.** Opened 2026-08-11 from the
  break-even spec review (`docs/SPEC_breakeven.md` §9).
  - **The problem:** a revenue-per-acre gap between two hoods can be an **income
    gap wearing a density costume**. Edmonton's density gradient plausibly
    tracks its income gradient, and nothing in this pipeline separates them.
  - ⚠️ **It bites the deviation lens in `/full/` NOW**, not just future work —
    that lens is *entirely* a statement about who sits above and below the
    citywide average, which is the exact reading the confound corrupts.
  - **No income or demographic data is ingested**, so today this can only be
    disclaimed, not measured. Current mitigation is the standing one: purely
    descriptive framing, never a causal claim (*"infill pays for itself"* is the
    sentence to keep out).
  - [ ] **Peter's call: ingest an income variable to MEASURE it?** ⚠️ Not free
    of hazard — a map pairing neighbourhood income with fiscal performance
    invites exactly the editorial framing this project refuses. **Measuring the
    confound and publishing the variable are separate decisions**, and the
    second one should not ride in on the first.

- [ ] **▶ IS THE TRANSIT COST TERM ALLOCATED BY THE WRONG KIND OF DRIVER?**
  Opened 2026-08-11 (`docs/SPEC_breakeven.md` §2b-i). `cost_transit_ops_per_acre`
  distributes the ETS operating budget by **scheduled stop-events in each hood**
  — but a downtown stop's departures are consumed by people boarding from
  everywhere, so the driver is **network-shared being allocated as if it were
  site-bound**. Matters out of proportion: transit is **90.8% of
  `transport_cost_ops_per_acre`**.
  - ⚠️ **DO NOT "FIX" IT BY DELETING THE TERM.** Two things are already recorded
    against a hasty read: the figure is a **share, not a rate** (annual budget ÷
    mean-weekday count — meaningless as a unit, exact as an allocation), and the
    locked framing is **demand-allocation-of-a-fixed-budget**, defensible when
    published as such (`DECISIONS.md` 2026-08-03).
  - **The narrow question:** is *where service is supplied* an honest proxy for
    *who consumes it* at neighbourhood grain? Supply-side is all the data
    supports — **no stop-level ridership exists**, citywide-monthly only
    (`DECISIONS.md` 2026-07-11) — so the live options are relabel, move to the
    break-even residual while the Services lens keeps it as-is, or leave it and
    state the limit.
  - **Does not block the cost register.** Its own decision.

- [ ] **▶ BREAK-EVEN LENS — STILL NO CODE, BUT THE MEASUREMENT IS DONE.
  `docs/SPEC_breakeven.md`; FOUR decisions in its §8 now block all code (#2
  name, #4 residual, #5 revenue scope, #6 transit).** Opened
  2026-08-11 (Peter: pipelines per cost category, improved one at a time,
  composing into a per-hood break-even that stays in the Lab and might one day
  reach specialists). **§4 Tasks 1 and 2 executed 2026-08-13 (PR #208, merged) —
  §4a holds the result.**
  - ✅ **§8 #1 + #7 SETTLED 2026-08-23 (Peter): OPERATING basis, OPERATING-ONLY
    denominator.** Coverage reads **15.5% ($473M / $3,055.2M), not 12.3%** —
    the earlier $3,846M/12.3% figure used the full tax-supported budget and is
    superseded. `DECISIONS.md` 2026-08-23.
  - ⚠️ **THE NUMBER IS COMPUTABLE TODAY AND WOULD BE WRONG IN A KNOWN
    DIRECTION.** Revenue modelled $2,715M against $473M of cost on the
    operating basis — **15.5% of the City's $3,055.2M operating-only budget**
    — so the lens would report **every hood running a 5.7× surplus**,
    by roughly the same factor everywhere, which is exactly what makes it look
    plausible. **Coverage is therefore the product, not a caveat**, and must be
    computed and printed wherever the number is.
  - ✅ **TASK 1 + TASK 2 DONE 2026-08-13 — the register is measured and the head
    is SHORT.** FY2025 tax-supported (pinned to match `ASSESSMENT_YEAR` and to
    stay inside the 2018–2025 naming era): **$3,855.9M, 656 rows, 144 programs —
    and the top 25 programs are 76.5% of it.** Order: **Police $597.2M (15.5%)**,
    Transit `OPS/ETS - Bus and LRT` $449.1M, Tax-supported Debt Charges $221.0M,
    Fire `CS/FRS - Operations and Training` $208.2M, **Alley Renewal $174.4M**.
    Full table in `SPEC_breakeven.md` §4a. ⚠️ **Parks is NOT its own line** — it
    is bundled with roads inside `OPS/PARS - Infrastructure Operations`.
  - ⚠️ **▶ POLICE IS THE TOP LINE, HAS NO DRIVER, AND IS BIGGER THAN EVERYTHING
    CURRENTLY MODELLED PUT TOGETHER** ($597.2M vs $473M). **Do not reach it by
    working down the ranked list.** Allocating it by any spatial driver produces
    a per-neighbourhood policing-cost map, and **the driver choice would be doing
    the arguing** — a far more charged artifact than a roads-cost map. Its own
    decision, and an editorial one before it is a data one. ⚠️ **"Find better
    data" was checked 2026-08-23 and does not escape this** — EPS's crime
    dataset is real and joinable, but its publisher anonymizes locations
    specifically because per-area comparison is unreliable, so adopting it
    would import a documented bias rather than resolve the gap.
    `docs/ANALYSIS_BACKLOG.md` §14.
  - ✅ **§8.7 SETTLED 2026-08-23 (Peter): OPERATING-ONLY denominator,
    $3,055.2M — coverage reads 15.5%, not 12.3%.** Decided together with §8.1
    (basis) because the two can contradict each other made separately. The
    full-budget denominator would have been the §3 basis-mixing failure sitting
    **in the coverage ratio rather than the composite** — the worse location,
    because §6 puts coverage on screen wherever the number is. `DECISIONS.md`
    2026-08-23, `SPEC_breakeven.md` §0/§8.
    - ⚠️ **CAPITAL IS NOT A SYNONYM FOR UNALLOCATABLE — disclosure debt, not a
      closed question.** `Alley Renewal` **$174.4M** is per-neighbourhood
      infrastructure renewal on the **lifecycle** basis the roads term already
      uses — plausibly the most spatially-allocatable line in the whole budget,
      and a larger register entry than anything shipped except transit. **The
      genuinely hard part is the ~$400M of debt service**, not "capital". Must
      not silently drop out of the register once lifecycle-basis work exists.
  - ⚠️ **THE SILENT KILLER IS BASIS MIXING.** Lifecycle $50/road-m/yr vs
    operating $9.32 — same metres, 5.4× apart (10.8× before the 2026-09-06
    re-scope). The composite must HARD-ERROR across bases, not warn. ⚠️ **The
    gap SHRINKING is what makes this more dangerous, not less** — two numbers
    5× apart look more like a plausible sum than two 11× apart.
  - ⚠️ **The revenue half is not the solid half either** — $2,715M modelled vs
    $2,318M budgeted (17%), the ~$125.4M institutional question is open with
    unknown direction, and levy is not all the revenue funding that budget.
  - ~~Decide the publication gate before the number exists (§8.3).~~ **SETTLED
    2026-08-11** — no separate gate; the Lab is full-build-only and `beta`, so
    the requirement collapses into §6's *coverage renders wherever the number
    does*. ⚠️ **Do not re-open** (`SPEC_breakeven.md` §8.3).
  - ⚠️ **THE FETCH IS NOT LAPTOP-ONLY — that blocker was false and had parked
    this task since 2026-08-04.** `budget.edmonton.ca` returns **HTTP 200 from
    the Oracle box**; only `www.edmonton.ca` is blocked. Corrected in
    `data/DATA.md` §17 and `SPEC_breakeven.md` §4. The three real quirks still
    bite: program names do not survive two re-cuts, every figure is gross
    (`account_type` is `Expenses` only), portal and PDF differ (+1.31% on Parks
    and Roads; 0.26% on the tax-supported total).

- [ ] **THE LAB IS OPEN AS A CONTAINER — one experiment in it, and the only
  thing left is PETER'S CALL on whether it graduates.** The phone check closed
  2026-08-15 (eyes-on, PR #207). Built 2026-08-11 (`DECISIONS.md` ×2 same date;
  `verify-deviation.js`, **59 checks green** as of 2026-08-12). A full-build-only
  top-level `#views` button holding unfinished lenses, currently just the
  deviation lens ("vs peer average"), which re-centres the revenue map on its
  peer group's average **per developed acre** and extrudes the deficit half
  BELOW the ground plane.
  - ⚠️ **9 institutional hoods draw NO PRISM** (15 until 2026-08-15, when share
    stopped deciding the geometry) — replaced by two white outlines, one per
    scenario (levied / exempt), asserting no value. The outline colour is
    **achromatic by rule, not by taste**: amber shipped first and measured
    **ΔE 9.5 against the deficit orange under NORMAL vision** (hard floor 15),
    so the *unknown* hoods read as *below average*. Blue was rejected too — a
    cool hue leans toward the teal surplus pole. Verify pins `R === G === B`,
    not a hex. ⚠️ **The rule is local to this lens** — Money uses azure
    `#2ec4ff` against its near-white sequential peaks.
  - ⚠️ **`exempt` is NOT always the lower end** (EVERGREEN +$87, RIVER VALLEY
    CAMERON +$842); a first verify check assumed it was and was wrong, the code
    was right. **Since 2026-08-15 no inverted band is ever DRAWN, and that is
    structural**: inversion needs the hood to lose less than the average's
    $1,303/acre, so its span is under $1,303 against $21,470/$48,047 clamps —
    Δt < 0.061, never the 0.25 required. Both facts are asserted separately, so
    the inversion cannot quietly disappear from the data.
  - ⚠️ **Read both decisions before touching it.** The sub-lens it ships
    without (rate-adjusted revenue per acre) was refused *on measurement*, not
    on taste, and the numbers to re-supply if anyone asks again are recorded.
    The second decision is why an experiment must keep its own state.
  - **ADDING AN EXPERIMENT IS ONE LINE** in `LAB_EXPERIMENTS` plus its view
    (a branch in `buildViewLayers` / `primaryRow` / `viewTooltip` /
    `refreshLegend` and a `VIEWS` entry). The picker renders from the registry
    and reveals itself at 2+, so the second one costs no chrome work.
    ⚠️ **Give it its OWN state, never Money's** — that is the whole reason the
    container exists, and the failure it prevents is silent.
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **Peter's call: does the deviation lens ever leave the Lab? THE CASE
    FOR IT GOT STRONGER 2026-08-12 and the old reason to doubt it is GONE.**
    It was marked `beta` partly because it was rank-identical to the Money map.
    On the developed-acre denominator it is **not**: Spearman 0.900, 242 of 358
    hoods moving >10 rank places. It now carries information Money does not.
    ⚠️ **It also changed what it says** — 21% of hoods below average became
    **63%** — so the question is no longer "is this thin?" but "is this the
    headline?". Still no opinion recorded; `beta` and full-only until Peter
    calls it.

- [ ] **`verify-peek.js` IS FLAKY UNDER PARALLEL LOAD — reproduce before acting on a red.**
  ✅ **RE-VERIFIED ACCURATE 2026-09-17 (S168): 3/3 green alone, 38 checks each
  run.** The item stands exactly as written; nothing to change.
  ⚠️ **AND THE LOAD SOURCE WAS SITTING RIGHT THERE.** Before running it, an
  orphaned `python3 -m http.server 8947` was found **28h50m old, from a DEAD
  session** (S165's scratchpad, 2026-09-16 01:34), still serving that session's
  **stale** `_site` build — with its launching bash also hung. Killed by explicit
  PID (never `pkill -f`, which shoots its own shell). ⚠️ **This is a RECURRENCE:
  S152 verified the previous pair of stale servers GONE and the class was treated
  as closed.** They come back per-session, so *check* rather than *assume* — a
  stale server answering on a port is both the load that reddens this script and
  a silent way to measure the wrong build.
  Found 2026-08-12 running the 33-script sweep: it reported
  `touch: panel open via CARD -- another hood peeks, panel closes`. Re-run while
  the sweep was still competing for CPU it failed **differently**
  (`first tap PEEKS, panel stays shut`, `peek=null`); run three times on an idle
  box it passes **3/3 with zero failures**. Two distinct failure modes under load
  and none without it — the touch-interaction timings are the suspect, not the
  app. ⚠️ **Cost about an hour of diagnosis** (a worktree at the pre-change commit
  and a second server on :8778) before the load hypothesis was confirmed, so the
  cheap first move is to re-run it alone.
  - ⚠️ **The sweep HARNESS produced three separate wrong answers the same day**,
    and all three read as green or as a real failure: a grep pattern that matched
    neither of two crash signatures (reporting ~31 crashed scripts as PASSING);
    a `grep -c green` tail that discarded every RED line; and a URL-fallback that
    triggered on `expected string, got undefined` but not on `verify-smoke.js`'s
    `usage:` message, so that script silently ran without its URL and was scored
    RED with an empty reason. **Nearly every verify script REQUIRES a bare URL
    argument** — `verify-deviation.js` is the exception, it defaults its own.
  - Not a blocker, and not the two known-red scripts (`verify-nonres-revenue.js`,
    `verify-revenue-panel.js`), which are separate and still open above.

- [ ] **A TRUE BIKEWAY LIFECYCLE $/m/yr STILL DOES NOT EXIST** — the residue of
  Stage 2, which shipped 2026-08-03 on an **operating** basis instead. All three
  cost terms are maintenance + snow with **no capital replacement**, because the
  figure offered as a lifecycle rate was not one.
  - ⚠️ **Do not re-propose $178/km/yr.** It is an operating-maintenance line.
    Falsified four ways in `DECISIONS.md` 2026-08-03 and recorded in
    `city_unit_costs.json` → `bikeway_ops.rejected_lifecycle_reading`; the
    shortest version is that the same source puts snow clearing on the same
    network at **113× it**.
  - ✅ **THE CAPITAL HALF IS DONE (2026-08-04, on the laptop).** Bike Plan
    Implementation Guide §1.2 **Table 3** → **$452,065/km** blended
    (bands $365k–$790k by urban form), construction-only. Verified rather than
    relayed — every row's implied $/km sits inside its own stated band and the
    $190.8M City-borne subtotal reconciles. Recorded as `bikeway_capital` in
    `city_unit_costs.json`, **deliberately INERT** (nothing reads it; it is $/km
    of asset value, not a rate). **Do not re-hunt this source.**
  - ⚠️ **WHAT IS ACTUALLY BLOCKING: A SERVICE LIFE, AND EDMONTON PUBLISHES
    NONE.** Searched 2026-08-04 across the Development Impact page, both Bike
    Plan PDFs, the 2025 Infrastructure Report, the Infrastructure
    State-and-Condition / Inventory / Tools pages and the 2023 Capital Asset
    Management Audit. The Bike Plan's action **9.6.2(a) is to *"establish"* a
    bikeway asset-management program** — the City says outright it does not have
    one. **This is not a search that was done badly; it is a number that does
    not exist publicly.** Reopening it means a FOIP/direct-contact route, or
    Peter choosing a life by decision the way he chose 50 years for roads.
  - ⚠️ **Two shortcuts around the missing life are already closed off.** (a) The
    sidewalk page's *"amortized for 20 years"* is a **local-improvement levy
    term, not an asset life.** (b) The **~3% set-aside rule does not transfer**
    — at roads' implied 3.33%/yr the allowance is $15,069/km/yr, but measured
    `bikeway_ops` is **$20,278/km/yr, 1.35× the whole allowance** before any
    renewal. Both recorded in `bikeway_capital`.
  - **For scale, if it is ever derived:** across a 20–50 yr life the answer is
    **$29–43/m/yr, i.e. 0.6–0.9× roads' $50** — the result is insensitive to the
    life because the $20.278/m/yr ops floor dominates. Compare the rejected
    reading's **1/281×**. ⚠️ These are illustrative, **not a shipped number**.
  - **Only then** can a lifecycle bikeway term sit beside `svc_cost_per_acre`'s
    lifecycle roads term. Until then the two bases stay separated by the `_ops`
    suffix, and that separation is load-bearing (~10.8× on the same metres).

- [ ] **⚠️ `--geojson-out /tmp/x.geojson` DOES NOT MAKE A LOCAL `main.py` RUN
  SAFE.** ⚠️ **The title used to end "— the DATA VINTAGE item below says it does,
  and that advice is wrong." That framing was stale: the item below was corrected
  2026-08-07 and now says the right thing. Struck 2026-09-17 (S168); the
  technical claim underneath is unaffected and was RE-VERIFIED in code the same
  day — `ROADS_WEB_OUT`, `ZONING_WEB_OUT`, `GRID_WEB_OUT`, `DEV_GRID_WEB_OUT` and
  `TEMPORAL_WEB_OUT` are hardcoded `ROOT / "web/data/…"` constants with NO CLI
  flag, so only `--geojson-out` and `--png-out` can be redirected at all.**
  The flag redirects only the main GeoJSON. A full run on 2026-08-03 still wrote
  `roads.geojson`, `zoning.geojson`, `value_grid.json`, `dev_grid.json` and
  `temporal.json` into `web/data/` from 2026-07-06 raw data — the exact rollback
  that item exists to prevent. Caught by `git status` immediately after and
  restored from HEAD; **nothing was committed**.
  - **Fix:** give the auxiliary web exports their own out-dir, or one `--out-dir`
    they all honour. Until then the real mitigation is
    **`git checkout -- web/data/` after any local `main.py`**, and the DATA
    VINTAGE item below should say so instead of what it currently says.

- [ ] **DEFERRED TO A LAPTOP — the minimum colour transition on state swaps.**
  Peter, 2026-08-29: *"we may do this on the laptop so I can judge it on local
  host"* — it is a **taste call that needs a real screen**, not a headless one,
  and this box has no way to judge it (three font families, none of the CSS
  stack; screenshots are the only output and they cannot show motion).
  - **Rules are already locked — do not re-derive them.** `docs/TRANSITIONS.md`
    (rules, our controls, the engine's limits) and the `DECISIONS.md` 2026-08-29
    row. This item is the *build*, and only the smallest honest slice of it.
  - **Scope, ~15 lines, one function:** `transitions: { getFillColor: 250 }` on
    `metric-extrusion`, the same on `getColor` for `top-edges` (or the roof
    outlines snap colour while the prisms fade), and a guard computing the
    duration:
    - ramp / `#coloradj` changed with metric+denominator unchanged → 250
    - Revenue ⇄ Residential $ ⇄ Non-res $ → 250
    - **everything else → 0**, i.e. exactly today's hard cut
  - ⚠️ **The bare one-liner is WRONG and looks right** — without the guard it
    also fires on Revenue→**Value**, which `TRANSITIONS.md` §2 rules a
    cross-fade, not a tween.
  - ⚠️ **`prefers-reduced-motion` needs JS here** (`matchMedia`), forcing 0. The
    existing `web/styles.css` block covers CSS only; deck.gl transitions are not
    CSS and would ignore it.
  - **NO height, NO cross-fade, NO view swaps** — height cannot animate at all
    (`TRANSITIONS.md` §5) and cross-fading needs both layer stacks alive, which
    collides on `hood-hover`/`hood-labels`. Keeping to colour is what makes this
    ~15 lines instead of a render-path change.
  - **Cost is measured, and smaller than assumed: CI is UNAFFECTED.**
    `verify-smoke.js` is the only script `refresh.yml` runs and it never clicks
    a control. Exposure is 10 local scripts that click a ramp/metric button,
    concentrated in the 6 `shot-*` screenshot ones — they would need a settle
    wait.

- [ ] **RESIDUAL from the panel/blurb fix (2026-08-02): below ~768px tall,
  Development and Infill have no left column left to give.** The placement fix
  clears the blurb in all ten states at 1440x900 and clears `#botleft` too. At
  1366x768 and 1280x720 the two longest blurbs hit `TEMPORAL_MIN_H` and the
  panel reaches into `#botleft` — Development 2px/50px, Infill **76px/124px**.
  - **No placement rule can fix it, and that is measured, not assumed:** at
    1280x720 Infill's `#title` ends at 499 and `#botleft` starts at 535, so the
    column has **36px** free. The blurb is **479px of a 720px screen**.
  - **The only remaining lever is blurb length** — Development's title box is
    442px and Infill's 479px against a **~179px median** across the other eight
    states. That was an option when this was ruled on and was not the one taken;
    it is now the *only* one that helps here. **Content decision, so it needs
    Peter.**
  - Not obviously worth doing: 1440x900 is clean, and the failure mode is the
    panel overlapping bottom-anchored chrome rather than burying content.

- [ ] **⚠️ DATA VINTAGE: a local `python main.py` REGENERATES THE MAP FROM STALE
  RAW DATA — do not commit the result** (found 2026-08-01). ⚠️ **BOTH DATES
  BELOW WERE ~2 MONTHS STALE — re-measured 2026-09-17 (S168): `data/raw/` is
  **2026-09-03**, not 2026-07-06, and the last committed auto-refresh is
  **2026-09-14**, not 2026-07-27. The hazard is UNCHANGED and still live — local
  raw is 11 days behind what the site ships — but it is now a days-wide gap, not
  a three-week one, and ⚠️ **the 1,896 figure was measured against the OLD gap
  and has NOT been re-derived**; do not quote it as the current blast radius.**
  Regenerating locally and committing silently ROLLS THE SITE BACK — measured
  2026-08-01 against the then-current gap: **1,896 pre-existing values changed**
  across 406 features on a run that was only supposed to ADD columns.
  - **What to do instead:** commit pipeline code only and let the weekly refresh
    add the columns, or run `scripts/download_data.py` first if the data really
    should roll. ⚠️ **For local UI work, `--geojson-out /tmp/x.geojson` is NOT
    enough** — corrected 2026-08-07; this line used to recommend it on its own.
    The flag redirects only the main GeoJSON, and a full run still writes
    `roads.geojson`, `zoning.geojson`, `value_grid.json`, `dev_grid.json` and
    `temporal.json` into `web/data/` (measured 2026-08-03 — see the
    `--geojson-out` item above, which exists to say so). **The mitigation that
    actually works is `git checkout -- web/data/` after any local `main.py`.**
  - **Consequence to watch:** phase 2's UI columns are ABSENT from the served
    geojson until the next auto-refresh runs. The UI must degrade cleanly when
    they are missing (the house pattern), or the site breaks in the gap.

- [ ] **▶ `data/DATA.md` §1 "Tax-exempt flag" WAS FALSE — exempt institutional
  land IS on the taxable roll, ~$5.6B of it. CORRECTED 2026-08-07; only sub-item
  (3) is still open.** Opened 2026-08-07.
  The West Meadowlark investigation asked whether its hospital parcel was
  anomalous. **It is not** — and answering that exposed a much larger stale
  premise.
  - ⚠️ **SUPERSEDED FRAMING, 2026-08-07 (later the same day): "is it supposed to
    be taxable?" WAS THE WRONG QUESTION — it always was.** Misericordia has been
    continuously assessed **2012–2025** as account `10095840` (~$200–260M, always
    WEST MEADOWLARK PARK, always COMMERCIAL). It was **renumbered** to
    `11495573` and was simply **absent from the published current roll** during
    the changeover. ⚠️ **So the map UNDERSTATED West Meadowlark before 2026-08-03
    by ~$250M of assessed value / ~$6M/yr — the +130% was the CORRECTION, not
    the defect.** `$4.63M` was the wrong number; `$10.63M` is right. See
    `data/DATA.md` "Tax-exempt flag" and `tools/audit_roll_continuity.py`.
  - **`DATA.md` §1's "Tax-exempt flag" note used to say:** *"tax-exempt institutional land (Legislature, schools,
    hospitals, City property) is **absent from the taxable roll entirely**, not
    flagged or zeroed"*, listing `AJ/PU/UI/UF` as exempt-proxy zones. **Measured
    against the roll, that is wrong.** Every major hospital is on it and was
    already there in the Jul-6 snapshot:

    | account | site | assessed | zone |
    |---|---|---|---|
    | `11495590` | Royal Alexandra (10520 Kingsway) | $273,762,000 | UF |
    | `11495573` | **Misericordia (16940 87 Ave)** — **the ONLY one absent on Jul-6** | $247,780,500 | UF |
    | `11495606` | Grey Nuns (1100 Youville W) | $196,900,000 | UF |
    | `11495587` | Cross Cancer (11560 University) | $68,062,000 | AJ |
    | `11495614` / `11495565` / `9996778` | U of A campus | $577M / $438M / $431M | AJ |

  - **Full spatial join of the roll against `zoning.geojson`: 2,254 parcels on
    AJ/PU/UI/UF zoning carry $5,622,058,000 of assessed value, which our
    pipeline turns into ~$125.4M/yr of modelled levy — 4.6% of the $2.71B
    citywide served total.** Concentrated: UNIVERSITY OF ALBERTA alone is
    $45.5M/yr across 36 parcels, then SPRUCE AVENUE $9.1M, CENTRAL MCDOUGALL
    $8.5M, DOWNTOWN $7.5M.
  - ⚠️ **So West Meadowlark's $6.0M was never the story — it is 5% of a
    pre-existing exposure that has been in every published number all along.**
    The +130% simply moved one hood into a state ~40 others were already in.
  - ⚠️ **What is NOT established, and must not be asserted either way:** being on
    the assessment roll with an assessed value is **not** the same as being
    levied. This dataset publishes assessments and a `Tax Class`; it does not
    state exemption status, and Alberta assesses some exempt property. Our
    pipeline applies mill rates to every record on the roll. **The open question
    is whether that is the right thing to do for these 2,254 parcels** — not
    whether the data is corrupt.
  - ✅ **(1) `DATA.md` CORRECTED 2026-08-07** — the "Tax-exempt flag" note now
    carries the measured split (present: hospitals, U of A campus; absent: the
    Legislature, 0 rows at 10800 97 AVENUE NW) and the per-zone table. The old
    claim is quoted and marked retracted rather than deleted, and the Known
    Quirks bullet that repeated it is fixed.
  - ✅ **(2) THE TWO ARTIFACTS SURVIVE — re-run 2026-08-07, numbers UNCHANGED,
    and this is the useful part.** `tools/audit_exempt_institutional.py`
    *measures* the taxable footprint on institutional zoning and subtracts it,
    rather than assuming there is none — so land that IS taxed is counted as
    taxed and correctly excluded from `exempt_inst_acres`. **The method never
    used the false premise; only the docstring's motivating sentence did.** The
    fresh run reproduces every published figure exactly (U of A: 145 exempt acres
    of 253 institutional, ×2.0 lift, $15.2M/lot-acre, $2.242B on 47 accounts).
    Premise sentences corrected in both files; ⚠️ **both now say DO NOT "fix" the
    method on account of the retraction.** `ANALYSIS_BACKLOG.md` §7's conclusions
    ride on those same numbers and therefore also stand.
  - ⚠️ **(3) OPEN AND IT IS THE ONLY THING LEFT: should the revenue model treat
    AJ/PU/UI/UF differently at all?** We apply mill rates to every record on the
    roll, which produces the ~$125.4M/yr above. Whether the City actually levies
    those parcels is **not answerable from this dataset** — it publishes
    assessments and a `Tax Class`, not exemption status. ⚠️ **This is a
    public-number change and Peter's call, not a cleanup.** Needs an external
    source on exemption status before it is even decidable.
  - ✅ **(4) `docs/FINDINGS_revenue_scale.md` §4–5 RE-CHECKED AND CORRECTED
    2026-08-08 — and it was NOT "narrative, not a computation others cite".**
    This item said so, and ranked it lowest. ⚠️ **It was cited by a
    USER-FACING STRING that had been LIVE on the site**: the revenue-mix panel
    printed *"Tax-exempt land is not on the roll, so it is absent from every
    share above"*, with a code comment pointing at §4-5 as its authority. The
    retracted premise was **published**, not merely written down, and it
    **pointed the wrong way** — it promised an understatement where the model
    may be overstating. Fixed (PR #184, merged, **confirmed live in
    production**: new string present, old string returns 0 hits). §4's
    conclusion SURVIVED its own premise (measured, not assumed — same as
    `audit_exempt_institutional.py`) and both files now warn against "fixing"
    it; §5's direction was inverted. **The lesson worth keeping: "narrative"
    was the wrong triage — nothing had checked whether prose was quoted by
    code.**
  - ✅ **(5) HOW THE $125.4M/yr MUST BE DESCRIBED — locked 2026-08-08.** It is
    a **gross modelled** figure ("if every institutional/public-zoned parcel
    were fully taxable"), **never** "revenue lost" or "foregone". ⚠️ The
    direction of the error is **unknown, not merely unquantified**. Text in
    `data/DATA.md`; `DECISIONS.md` 2026-08-08.
  - ⚠️ **(6) GIPOT IS NOT A USABLE ANCHOR YET — three specific blockers.**
    Offered as the one hard reference point ("$15.7M for 2021-22") and **not
    written in**, because: (a) **the City publishes no dollar figure at all**,
    only a percentage history — the $15.7M is unsourced and secondary
    reporting says only "$15 million per year"; (b) **2021-22 sits inside the
    2020–2024 window when Alberta paid 50%**, so any receipt from it reads
    ~2× low as a tax equivalent (75% in 2019 and 2025, 100% from 2026); (c)
    **GIPOT covers Government of Alberta property** — that universities and
    hospitals fall outside it is *inference*, since the program page
    enumerates no exclusions. All three recorded in `data/DATA.md`. **Drop the
    number in once a primary source exists; do not publish it before.**

- [ ] **OPEN-DATA REQUEST (DRAFTED, NOT SENT): ask Edmonton to publish the
  taxable/exempt liability code on `q7d6-ambg`.** Opened 2026-08-08.
  `docs/DRAFT_open_data_request_exemption_status.md`. **This is the only route
  that resolves the AJ/UF/UI/PU question** — no public per-parcel exemption
  source exists, confirmed.
  - ▶ **SUPPORTING EVIDENCE IS NOW PUBLISHED (2026-08-26)** — a standalone
    notebook demonstrating *why* the request is necessary rather than asserting
    it: `notebooks/standalone/exemption_uncertainty.py` / `.ipynb`, served at
    **`/notebooks/exemption-uncertainty.html`**. It proves the identification
    failure by construction — two **disjoint** sets of apartment properties,
    60 and 68 of them, each reproducing the same $3.49B aggregate to 100.0000%.
    A sum does not determine its terms, so no amount of public data closes this.
    ⚠️ **Still do NOT put the $125.4M in the message** (unchanged); the page
    asserts nothing about any parcel and is safe to link.
  - ⚠️ **One claim in the brief it came from is FALSE and is corrected in the
    draft: Calgary does NOT publish exemption status as open data.** Verified
    against the live schema of Calgary's `4bsw-nn7w` — 22 fields, **no
    exempt/taxable flag**. Calgary discloses it on the **assessment notice**
    only (*"Tax exemption status is noted on your assessment notice"*, verified
    verbatim). Sending the stronger claim would be trivially checkable and
    wrong.
  - ✅ **THE ASSET / LIABILITY-CODE PARAGRAPH IS CONFIRMED — 2026-08-12, read in
    the primary source, and it came back STRONGER than the draft claimed.** The
    HTTP 520 was transient. *2025 Recording and Reporting Information for
    Assessment Audit and Equalized Assessment Manual*, **Ministerial Order No.
    MAG:016/25** (open.alberta.ca dataset `1718-1771`). The liability code's
    seven components include a **Tax Code** already separating `T` taxable from
    `E` *"assessable but exempt from taxation"*, and a **Tax Exemption Code**
    that is *"mandatory in ASSET"* for **every** property *including taxable
    ones* (`NAA`) — so there is no coverage gap to argue about. Appendix G names
    our parcels by statute: `MGA362(1)(d)` university boards of governors,
    `MGA362(1)(e)` hospital boards. Fallback paragraph retired; draft and
    `DECISIONS.md` updated. ⚠️ **It does NOT tell us what Edmonton coded for any
    parcel** — the $125.4M question is untouched, direction still unknown.
  - ✅ **SUBMISSION CHANNEL FOUND — `opendata@edmonton.ca`, 2026-08-25.** Read
    from the live portal itself (`https://data.edmonton.ca/`, the footer nav's
    "Contact Us" → `mailto:opendata@edmonton.ca`) — primary source, not
    inference. This is the right channel of the three that were listed: the ask
    is *publish a field on dataset `q7d6-ambg`*, which is a portal/dataset
    request, not a per-parcel assessment inquiry. **Assessment & Taxation Branch
    is the escalation if Open Data bounces it**, not the first stop.
    ⚠️ **Still NOT SENT — sending is Peter's call** (outward-facing, and it
    speaks for the project).
  - ⚠️ **THE "edmonton.ca IS UNREACHABLE FROM THE ORACLE BOX" BLOCKER WAS A
    MIS-DIAGNOSIS — RETRACTED 2026-08-25.** This bullet used to read: *"No
    submission channel is recorded in the repo, and `edmonton.ca` is
    **unreachable from the Oracle box** (`000` on 2026-08-12 …). Needs a machine
    that can reach `edmonton.ca`."* **The `000` was real; the cause was wrong,
    and the wrong cause made a client-side problem look like a hardware one for
    13 days.** Re-measured: DNS resolves (`35.190.75.248`), TCP connects, TLS
    negotiates, and the server presents a **valid** cert (`CN=*.edmonton.ca`,
    Entrust OV TLS Issuing RSA CA 2 → **Sectigo Public Server Authentication
    Root R46**). The failure is local: this box's `ca-certificates-2023.2.60`
    bundle (142 roots) **does not contain the Sectigo R46 root**, so curl
    reports the chain-embedded root as `self signed certificate in certificate
    chain`. Fetching with `certifi`'s bundle instead returns **200 / 61,938
    bytes**. `www.edmonton.ca` deep paths 404 (their URL structure moved) — a
    clean 404 is the host serving normally, not a block.
    - **Workaround for any HTTPS fetch from this box:**
      `ssl.create_default_context(cafile=certifi.where())` (or
      `curl --cacert "$(.venv/bin/python -c 'import certifi;print(certifi.where())')"`).
      Affects **any** host chaining to a post-2021 root, not just `edmonton.ca`.
    - ⚠️ **Lesson (the `todo-can-lag-executed-work` pattern, sharper form):** the
      symptom re-measured true and the blocker was *still* wrong. Re-measuring a
      stale blocker means re-deriving its **cause**, not just re-confirming its
      **symptom** — `000` is a client-side verdict, never evidence about the
      remote host.
  - **Keep separate from the `qi6a-xuwt` bug report** — that one asserts a
    defect, this one requests a field. **Do not put the $125.4M in the
    message**; it depends on the very question being asked.
  - ⚠️ **Do NOT hand-flag individual parcels as exempt meanwhile** (Peter,
    2026-08-08). No verified per-parcel source exists, and the worked examples
    circulated for exactly that purpose were **all wrong** — see the `## Done`
    line for the 2026-08-08 verification.

- [ ] **▶▶ AN EXTERNAL LEVY ANCHOR EXISTS AFTER ALL — Alberta FIR Schedule MR.**
  Opened 2026-08-25. ⚠️ **FIRST-PASS, NOT AUDITED — do not publish any number
  here until it is.**
  - ⚠️ **CORRECTION 2026-08-25, same day: this item first said "OUR MODEL READS
    +18.2% AGAINST IT" and that number was WRONG** — it compared our roll to FIR
    **2025** when the roll is **2026** (item above). It is quoted here rather
    than deleted because the error is instructive: an external anchor is only as
    good as the year you align it to, and the mismatch is what exposed the
    vintage drift. **Correct figures are below.**
  - ⚠️ **The premise "no City-given total exists to check against" is FALSE.**
    It was believed because `edmonton.ca` looked unreachable (that blocker is
    retracted above) — but the anchor was never on `edmonton.ca` at all. It is
    in the **same Alberta Municipal Affairs FIR workbooks
    `scripts/fetch_fir_debt.py` already downloads** for the debt lens
    (`data/DATA.md` §11). That script reads **one** sheet (`AA(1)-Debt`) of
    **51**. Three of the others are `MR(1)-Tax Levy`, `MR(2)-Assessment`,
    `MR(3)-Mill Rate`; `EA(1)-Assessment` is equalized assessment.
  - **Edmonton (code `0098`), financial year 2025, Schedule MR — filed by the
    City with the province:**

    | | taxable assessment | municipal levy |
    |---|---|---|
    | Residential | $148,128,818,480 | $1,129,541,492 |
    | Farmland | $59,062,724 | $450,377 |
    | Non-Residential (incl. linear) | $42,291,523,823 | $1,024,423,352 |
    | Machinery & Equipment | $768,976,453 | $0 |
    | Other (annexed, vacant, …) | $17,087,204,280 | $142,984,457 |
    | **TOTAL** | **$208,335,585,760** | **$2,297,399,678** |

  - ✅ **MR(2) IS THE TAXABLE BASE BY CONSTRUCTION — verified, not assumed.**
    `assessment × MR(3) rate` reproduces `MR(1)` levy to **±0.0000%** for
    Residential, Farmland and Non-Residential. ✅ **And MR(3)'s rates match
    `data/mill_rates.json` EXACTLY** (Residential `7.6254`, Non-Residential
    `24.2229`) — our rate inputs are independently confirmed correct.
  - ⚠️ **THE GAP, YEAR-ALIGNED (2026 roll vs FIR 2026, 2026 rates both sides).**
    Ours **$238,448,551,458 assessed / $2,784,219,936 levy**; FIR 2026
    **$224,199,394,806 / $2,509,075,991**. Gap **+$14.2B assessed (+6.4%)** and
    **+$275.1M levy (+11.0%)**. ⚠️ **Vintage WAS a large part of the
    explanation** — the same comparison mis-aligned to FIR 2025 read +14.5% /
    +18.2%, so **roughly half the apparent discrepancy was the wrong year**, not
    a modelling defect.
  - **Where the residual concentrates — and it is NOT residential.** Against FIR
    2026 by class: residential **+1.2%** (essentially matched), non-residential
    **+20.6% / +$9.08B**, "other residential" vs FIR's "Other" **+21%**.
    ⚠️ **This materially strengthens the institutional-exemption hypothesis**:
    the $5.6B of AJ/UF/UI/PU assessment is now **62% of the non-residential
    gap**, not the 19% of total that the mis-aligned comparison implied.
    ⚠️ **The per-class rows are still not 1:1** (FIR's 5 buckets vs our 4) —
    treat the residential fit as the reliable signal and the rest as a lead.
  - ⚠️ **THIS DOES NOT RESOLVE THE INSTITUTIONAL QUESTION — IT RESIZES IT.**
    Exempt institutional land is now the **leading** candidate for the
    non-residential residual (62% of it) rather than a minor one, but 38% of
    that gap is still unaccounted for. **The direction, however, is no longer
    unknown for the aggregate: we are OVER, not under.** (Per-parcel direction
    for any given institutional parcel is still unknown.)
  - **Candidates checked, and what they were worth:**
    - ❌ **Duplicate parcel records — RULED OUT.** 439,581 rows, 439,581 unique
      account numbers, **zero** duplicated accounts.
    - ❌ **Class-percentage apportionment — RULED OUT as a driver.** Slice
      percentages sum to 100 on all but **80** rows (min 85%); mean 99.9996%.
    - ✅ **Roll vintage — CONFIRMED, and it was about half of it** (item above).
    - ✅ **Bucket mapping — RESOLVED from FIR's own headers + implied rates.**
      `MR(2)` col [10] is *"Other (including annexed, vacant, total minimum
      tax, etc.)"*, **not** "Other Residential" — but its **implied rate
      `8.2872`** (levy ÷ assessment) sits within **1.0%** of our Other
      Residential `8.2064`, and cols [5]/[7] reproduce `7.7419`/`25.2216`
      exactly. Edmonton has no apartment slot in `MR`, so it files that
      sub-class under [10]. **The economic pairing was right; the label was
      not.** (Still inference, but rate-corroborated.)
    - ✅ **Machinery & Equipment — RESOLVED, and it is a non-issue for levy.**
      FIR assesses $759,582,941 at a **`0.0000` rate → $0 levy**. Edmonton
      levies no municipal tax on M&E, so it cannot contribute to the levy gap;
      it makes our *assessment* base look $759.6M **smaller**, not larger.
  - ✅ **WHERE THE NON-RESIDENTIAL GAP PHYSICALLY SITS — spatial join run
    2026-08-25, and one zone code closes most of it.** `gpd.sjoin` of all
    439,581 parcels against `zoning.geojson` (439,573 matched, 8 unplaced):

    | exempt-candidate zones | non-res assessed | share of the $9.08B gap |
    |---|---|---|
    | AJ/UF/UI/PU (the old proxy) | $5,199,452,500 | 57% |
    | **+ PS** | **$8,681,376,500** | **96%** |

    ⚠️ **`PS` is "Parks and Services" and was NEVER in the four-zone proxy** —
    991 parcels, $3.48B. The City's own `description` field names the set:
    `AJ` Alternative Jurisdiction, `UF` Urban Facilities, `UI` Urban
    Institution, `PU` Public Utility, `PS` Parks and Services. **96% of the
    non-residential gap coincides with public/institutional/parks zoning.**
    ⚠️ **Coincidence in a zone is NOT proof of exemption** — this is
    correlational, and `UF`/`PU` include privately-owned facilities
    (`data/DATA.md`). But it is a far tighter fit than anything before it.
  - ⚠️ **THE APARTMENT GAP IS A DIFFERENT ANIMAL AND THE ZONING PROXY IS BLIND
    TO IT.** Only **13%** ($515,535,000) of the $4.00B "Other Residential" gap
    sits on exempt-candidate zoning; the rest is on ordinary `RM`/`RS`/`DC2`
    residential zoning. **Consistent with use-based exemptions the zoning proxy
    structurally cannot see** — seniors' housing, non-profit and social housing
    are exempt by *use* under MGA 362, not by zone. **A zone-based method has
    hit its ceiling here; this bucket needs a different instrument.**
  - ⬜ **Still open:** whether the City apportions where we bill 100% of
    assessed value; the residential +1.2% / $1.90B residual; and the 4% of the
    non-res gap outside the five zones.

- [ ] **▶ WHO IS MISSING FROM THE CURRENT ROLL RIGHT NOW? — 1,457 parcels /
  $1.07B with no current-roll match.** Opened 2026-08-07 from
  `tools/audit_roll_continuity.py` (historical 2024 vs the live roll, matched by
  **position** within 5 m so renumbering / re-addressing / hood renames do not
  register). 168 of them are over $1M, totalling **$856M**. Largest: EDMONTON
  SOUTH CENTRAL `10884618` $38.4M, WOODCROFT `1012137` $37.7M, GRANVILLE
  `10501062` $33.8M.
  - ⚠️ **THESE FIGURES REPLACE 1,534 / $1.62B — AND SO DO THE EXAMPLES.**
    Re-measured 2026-08-30 (second observation, below). **The three parcels this
    item used to name as its largest cases — MILL WOODS TOWN CENTRE `9980213`
    $69.0M, YELLOWHEAD CORRIDOR WEST `10275721` $60.5M, SOUTHEAST INDUSTRIAL
    `9985679` $53.5M — were never missing.** All three sit on the current roll
    under their original account numbers. Do not cite them.
  - **The per-parcel list is now committed** —
    `data/roll_continuity_candidates_2026-08-30.csv` (1,578 rows, `acquitted`
    column). ⚠️ **Diff the next run against this file**, and pass `--out`; the
    reason this item stalled three times is that only the headline count ever
    survived a run.
  - **Why it matters:** every one of these is a potential Misericordia — a
    property still assessed but absent from the published current roll, whose
    neighbourhood is **understated on the live map** for as long as the gap
    lasts. That is a silent revenue-side error with no guard behind it before
    the fact (`check_revenue_deltas.py` only catches the *return*).
  - ⚠️ **CANDIDATES, NOT VERDICTS.** Demolitions, subdivisions and
    consolidations legitimately have no 1:1 successor and are in this list. The
    audit cannot tell those apart, and **one run cannot distinguish a transient
    renumber gap from a permanent removal** — that needs a second run later.
  - **Next step is cheap and decisive: RE-RUN IT and diff.** Anything that
    reappears was a transient gap (and its hood was understated meanwhile);
    anything still absent months later is a real removal. Nothing else about
    this item can be settled without that second observation.
  - ✅ **SECOND OBSERVATION DONE 2026-08-30** (first attempted 2026-08-09, when
    the roll had not moved). Roll republished: **439,634** rows against the
    439,631 baseline — **+3 net**, yet the candidate set moved by 44, so a tiny
    row delta hides real churn. ⚠️ **Do not use the row count to decide the
    answer can't have changed** — only to decide whether the source moved at all.
    - **What the diff CANNOT say:** nothing persisted the 2026-08-07 per-parcel
      list, so transient-vs-permanent is still unseparated. Fixed forward — the
      list is committed now.
  - ⚠️ **THE BIG FINDING IS A FALSE-POSITIVE CLASS, NOT THE DELTA.** Position
    matched 1,578 as unmatched; **121 of them ($592M — 35.6% of the value at
    risk) carry an account number still on the current roll.** They never left,
    they were recentroided past the 5 m tolerance. Verified against account
    reuse: 121/121 resolve to a plausible same-property current record (104
    identical hood, 17 boundary/rename churn like `CHAPPELLE` → `CHAPPELLE
    AREA`). The tool now runs an **acquittal pass**.
    - ⚠️ **DO NOT WIDEN `--tolerance-m` TO "FIX" THIS.** The acquitted moved a
      **median 58 m, max 559 m**; at 25 m only 30 of 121 come back, and a
      tolerance that wide starts matching the *neighbouring* parcel — trading a
      visible false positive for a silent false negative. The 5 m figure came
      from a **four-hospital sample** (0.6–1.6 m) that does not generalize to
      large commercial parcels.
    - **Why an identifier is allowed here** after `DECISIONS.md` 2026-08-07 said
      never to match on one: matching **on** an identifier creates false
      negatives (they all churn), but using one only to **acquit** can only
      remove false positives. The asymmetry is the licence.
  - ⚠️ **$1.07B IS STILL AN UPPER BOUND.** A parcel that both renumbered *and*
    recentroided past 5 m is a false positive the acquittal cannot see. Every one
    of the 1,457 has *some* current parcel within 427 m (median 36 m), so
    distance alone acquits no more of them.
  - **Running it again:**
    - **Readiness test before spending a run:** fetch the current roll and
      compare its row count to the baseline. Identical → the source has not
      moved and the answer cannot have changed.
    - ⚠️ **`--cache-dir` DEFAULTS TO `/tmp/roll_continuity` AND A WARM CACHE
      MAKES THE "RE-RUN" A REPLAY.** The first 2026-08-09 attempt reproduced
      1,534 / $1.62B off 45-hour-old files and read as a real null result. The
      tool now logs `CACHE HIT` at WARNING with the file's age — **but pass a
      fresh `--cache-dir` anyway.** A prescribed "just re-run it" that silently
      replays its own first answer is the third time this item's stated next
      step has not survived contact.
    - **Also measured, and not what the audit uses:** the local
      `data/raw/` snapshot was **439,685** rows (2026-07-06) against the API's
      **439,631** — the roll *shrank* by 54 accounts. Irrelevant to this tool,
      which fetches from Socrata directly, but it means a local
      `download_data.py` does **nothing** for this item. Do not repeat that.
  - ⚠️ **Do not report this upstream yet — and the second run STRENGTHENED that.**
    0.34% of parcels is within the range ordinary demolition/subdivision could
    explain, and we still have **no baseline for how much of it is normal** —
    unlike the `qi6a-xuwt` gap, which was measured against a control. A report
    sent on 2026-08-07's figures would have named three parcels that were on the
    roll the whole time.
  - **What would actually settle it, now that a baseline list exists:** diff the
    next observation against `data/roll_continuity_candidates_2026-08-30.csv`.
    A candidate that has reappeared was a transient gap (and its hood was
    understated meanwhile); one still absent months later is a real removal.
    That split is the reportable finding — the raw count never was.
  - ⚠️ **Do NOT "fix" this by dropping the parcels.** We apply published rates to
    the published roll; silently excluding records the City published is the
    exact silent-correctness failure the guards exist to prevent.
  - **Not an Open Data bug report.** Nothing here suggests the City's roll is
    wrong — the earlier framing assumed a defect and the evidence does not
    support one. Keep this separate from the `qi6a-xuwt` item.

- [ ] **PETER'S CALL: wire roll-continuity into `refresh.yml` as a SECOND
  guard?** Opened 2026-08-07 (S101 — it existed only in S100's session summary
  and would have evaporated on the next `/clear`).
  - **What it would catch that nothing else does:** `check_revenue_deltas.py`
    only fires when a missing property **returns** (the +130% correction).
    Nothing fires while a hood is understated, which is the whole window in
    which the map is wrong. A roll-continuity step would catch the *departure*.
  - **What changed in its favour:** the churn baseline now exists — accounts
    vanish at **0.15–0.37%/yr**, spiking to **0.91% (3,893 accounts)** in
    2023→24 — so this is a measured standing property of the data, not a hunch.
    That makes it more defensible than when it was first floated.
  - **What argues against:** it adds a **second issue-filing channel** on top of
    `revenue-delta`, and ⚠️ **the audit itself cannot separate a transient
    renumber gap from a permanent removal in one run** — so a CI version would
    file issues it cannot adjudicate. **Settle the 1,457-parcel item above
    first**; a diff against its committed baseline is what tells us the base
    rate. ⚠️ **The 2026-08-30 run sharpened this argument, not softened it:** a
    third of the value it reported was parcels that never left the roll, so a CI
    version wired up before the false-positive class was understood would have
    filed issues about parcels sitting on the roll the whole time.
  - If built, it must follow the existing guard's shape: **warn-not-fail, always
    exit 0, run BEFORE the commit step** or its baseline becomes the new data.

- [ ] **CARDINALITY GUARD — two small follow-ons (guard shipped 2026-07-28, PR #110).**
  `scripts/check_value_anchors.py` now pins the record-to-parcel *regime* in
  bands and runs in `refresh.yml` after regeneration. Both known bugs were
  re-verified as non-issues (see `AUDIT_LEDGER.md` 2026-07-28); this is
  maintenance, not a defect.
  - _2 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **Optional, Peter's call: lower `STALE_DAYS`.** Currently 14 against a
    weekly cron = one missed run tolerated, two consecutive misses warn. A
    drift failure is therefore viewer-silent for 14 days. If that is too long
    for a public audience, the knob is global (`web/index.html`) and should
    move for ALL failure types at once — deliberately NOT a per-guard banner
    (`DECISIONS.md` 2026-07-28).

- [ ] **GEOGRAPHIC REFERENCE LAYERS — TIERS 2 & 3 (Tier 1 shipped 2026-07-27).**
  Tier 1 (North Saskatchewan River + Anthony Henday ring road) is live and on by
  default; see `DECISIONS.md` 2026-07-27 (×2) and `data/DATA.md` §14. The render
  seam is proven: `buildLayers()` BRACKETS `buildViewLayers()` —
  `referenceUnderLayers()` (river, bottom) before it, `referenceOverLayers()`
  (ring road, top) after — one Display-menu toggle, `verify-reference-layer.js`.
  **Which end a new reference shape belongs at is a real question, not a
  default:** the river went underneath because the hood fabric already traces
  it (set-aside valley = a river-shaped seam), so painting over glitched; the
  ring road has no such seam and is invisible underneath. What's left:
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **Tier 2 — Edmonton internal reference.** District labels (West
    Edmonton, Mill Woods, Castle Downs, Terwillegar, Southeast) + Downtown and
    Old Strathcona/Whyte Ave; major arterials as thin unlabeled lines
    (Whitemud, Yellowhead, Gateway/Calgary Trail) from the existing road feed,
    same allowlist technique as the Henday. **Label collision is DECIDED
    (2026-07-27, Peter):** feed district labels into the existing
    `visibleLabels()` declutterer with districts winning priority — do NOT add
    a second, independent label layer, or "MILL WOODS" will stack on "MILL
    WOODS TOWN CENTRE". Districts have no dataset; coordinates are hardcoded
    and placement is a design call, not a data-fidelity one.
  - _3 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **Zoom-gating does not exist yet** — nothing in `index.html` gates on
    zoom today, so Tier 2/3 introduce the concept. Tier 1 deliberately renders
    at all zooms.
  - **Explicitly out of scope (decided 2026-07-27):** the Edmonton river
    valley/ravine overlay (`gis.edmonton.ca` Common_Layers 115). It is a
    regulatory development-setback polygon, not the river — drawing it near the
    water would read as "the river is this wide."

- [ ] **MOBILE USABILITY (NEW 2026-07-22 — full plan in
  `docs/MOBILE_USABILITY.md`; read it first).** ⚠️ **STALE PREMISE CORRECTED
  2026-09-16 (S166) — re-measured, not re-read.** The item opened *"phone
  rendering is unstyled for small screens (zero `@media` queries today)"*. That
  has been false for some time: **`web/styles.css` carries 6 `@media` blocks**,
  and `MOBILE_USABILITY.md` §1 now names `@media (max-width: 640px)` at the end
  of that file as the phone seam (with an `@media (hover: none)` block before
  it), while its §2 is a CONFIRMED render pass at 390×844 on a real device.
  **Do not act on the original framing — the seam exists and is in use; what
  remains is per-surface work, not the introduction of mobile styling.** The
  quick-pass order below predates the seam and is kept for its ordering only.
  Original: the top third collides — title/blurb + all six control pods stack on
  top of each other at 390 px (screenshot-verified); wide pods clip off the left
  edge. Map render + bottom legend are fine; tap-to-inspect tooltips work on real
  devices. Separation seam is clean: render is shared (one WebGL canvas), but all
  chrome/layout is isolatable behind an `@media` block with zero desktop risk.
  Quick-pass order:
  (1) add the `@media (max-width:640px)` seam, (2) fix the top-third collision
  (collapse pods + shorten the blurb), (3) stop the left-edge clip, (4) re-render
  via `tools/profiling/shot-mobile.js` + real-device check. ~~NOT greenlit for the
  approach yet (single scroll column vs bottom-sheet/hamburger — decide at step 2).~~
  ✅ **APPROACH DECIDED 2026-08-04: the single scroll column, no bottom sheet and
  no hamburger** — steps 1-4 are all closed, so this quick-pass list is a record,
  not a queue (`docs/TODO_archive.md`).
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [x] ~~**BUILD ONCE: implement the 8 regroup decisions in `web/index.html`.**~~
    **BUILT 2026-07-23 (branch `regroup-build-s65`, NOT yet on master).** One reflow:
    the top stack is now a `#controls` flex column (tier order via `order:`), Glass
    is a 2-way Money "Detail" toggle (internal view unchanged), Dev grid+spike is one
    3-way Detail selector (Neighbourhood / 100 m grid — activity / Stock age), Infill
    is a full-only Dev *mode* (`#devmode`), Industrial is a full-only `#devmetric`,
    palette + Labels moved into a "Display" accessibility popover, `Residential only`
    → `Highlight residential`. `BUILD` flag (`public|full`, `?build=public` override)
    gates the two full-only controls. Full verify-`*`.js suite green in **both**
    builds; verify + shot scripts updated to the new controls.
    - [x] ~~**⚠️ merge gate: two-build deploy plumbing**~~ — **RESOLVED 2026-07-23**
      (same branch): the emit now rewrites `DEFAULT_BUILD → public` for the root
      copy, so merging `regroup-build-s65` to master ships the *public* controls to
      the site root. **Branch is now safe to merge** (review + merge is Peter's call).
    - [ ] **THEN mobile CSS** (below) reflows the *final* grouping (inherits the flex
      column + Detail selectors — the structure-before-mobile payoff). *Partly done:*
      move-1 shipped 2026-07-24 (`@media` seam, collapsing title, bounded control
      column) and the `#views` **size** half of the "under-reads as primary" concern
      is fixed 2026-07-25. **Still open: the `#views` POSITION question** — it's
      still a thin strip at the very top. ⚠️ **It used to ride on the move-2 /
      bottom-sheet fork; that fork was REFUSED 2026-08-04**, so position now needs
      its own proposal if it is ever revisited (`MOBILE_USABILITY.md` §3).
    - [x] ~~**Regenerate `docs/LENS_INVENTORY.md`** from the rebuilt wiring.~~
      **DONE 2026-07-25.** Rewritten from the code (not patched): two-build table,
      4/5 views with Glass as Money's `#moneydetail` mode and Infill as
      Development's `#devmode` lens, the three different "doesn't apply here"
      behaviours (`#toggle` hides / `#lens` hides / `#coloradj` greys), per-view
      data gates, combination counts, and a code-anchor table. Every row of the
      matrix was **probed against the live site** in both builds, not inferred.
    - [x] ~~**`CONTROLS_MATRIX.md` §2–§5 still stale.**~~ **DONE 2026-07-25.**
      §1–§5 rewritten against the probed live behaviour: 4/5 views with the two
      internal modes named, the Options-fold structure (T2+T3 both live inside
      `#optpanel`, folded by default ≤640px), corrected §4 rows, and a §5 split
      into **still-open (numbered 1–7)** vs **resolved-by-the-regroup (original
      letters kept, because `DECISIONS.md` cites "§5.G"/"§5.A/B"/"§5.F")**.
      §7 reframed from "not yet on master" to merged & live.
    - [x] ~~**Two stale code comments in `web/index.html`**~~ — DONE 2026-07-26,
      folded into PR #96 rather than spending a deploy on a comment-only diff.
      All three siblings now agree that `devGridOfferable` excludes **only**
      Industrial. `CONTROLS_MATRIX.md` §6 closed out.
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **Selective/partial data regen (DEFERRED — `SPEC_deployment.md`
    "Two deploy paths").** Teach the *data* run which datasets a change needs so
    even a refresh skips untouched sources. Signal exists (`rowsUpdatedAt` per
    dataset; roads static 2+ mo while permits/fire change daily) but needs
    raw-file caching across CI runs, and the weekly cron sits right on GitHub's
    7-day cache eviction. Real payoff on slow static layers (roads/zoning), real
    fragility — separate project, not started.

- [ ] **PARKED: Regional comparison lens (St. Albert / Strathcona; Phase 2,
  not November scope).** Spike complete (PR #69, `docs/SPIKE_regional_lens.md`
  — read it first). Feasible in principle but blocked on: (a) **St. Albert
  licensing** — the LandScape REST service is not a catalogued open dataset
  and its bulk-query-ability is likely incidental, not licensed; needs direct
  confirmation from the City before any raw-data use; (b) Strathcona
  multi-unit dedup rule unsolved; (c) output design undecided beyond
  "citywide aggregate chart is the safe/realistic scope". **Do not commit
  St. Albert per-parcel data to the public repo under any circumstances until
  (a) is resolved.** (Strathcona licensing is clean: OGL-Alberta via
  catalogued open-data hub datasets.)

- [ ] **INDUSTRIAL & NON-RESIDENTIAL LENS FAMILY (NEW 2026-07-18 — full plan in
  `docs/SPEC_industrial.md`; read it first).** Two tracks: A = non-res
  decomposition inside the existing hood/grid frame; B = citywide-aggregate
  regional context from Alberta Municipal Affairs sources (OGL-Alberta,
  established fetch pattern — extends `fetch_fir_debt.py`; NOT the parked
  per-parcel regional lens above, which stays parked untouched). Tone rule is
  stricter here — descriptive only, see the spec. Build order A1 → A3 → A2 →
  B2 → B1 → B3:
  - _2 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **A2 — Shovel-ready industrial land:** `stt5-pzaa` verified 2026-07-18
    (annual snapshots 2016–2023, `servicing` field, centroids); absorption
    computable from snapshot diffs; display undecided. ⚠️ **ITS INPUT IS 19
    MONTHS STALE — measured 2026-09-17 (S166), and "verified" above meant
    REACHABLE, not CURRENT.** `stt5-pzaa` ("Vacant Land - Industrial") answers
    200 and its rows have not moved since **2025-02-19**. Controls run the same
    minute prove the field is meaningful and the portal is fine: `qi6a-xuwt`
    rows=2026-01-12, `pwis-wc4c` rows=2026-04-29. So this table sat out two
    assessment rolls. **Re-check `rowsUpdatedAt` before ingesting it, and treat
    any absorption series built on it as ending in 2025, not today.** This is
    `archived-tables-still-answer` exactly. Not yet filed in
    `docs/DATA_ISSUES.md` — a dataset that stopped updating MAY be a publisher
    defect or may simply be annual/retired; establish which before writing a row.
  - [ ] **A4 — Assessment-lag methods note:** Nov 29 2024 council memo
    attachment (Table 1, permit→assessment 3–5 yr lag) — edmonton.ca fetch,
    likely Peter/laptop.
  - [ ] **B2 — Regional non-res mill rates:** `2026_Tax_Rates.xlsx` on the FIR
    page (verified live) + yearly workbooks; 6 municipalities; reviewed JSON.
  - [ ] **B1 — Regional non-res assessment share:** FIR/SIR + equalized
    assessment XLSX (2024–26 verified on open.alberta.ca — NOT PDF-only);
    rebuild the published-share-series discrepancy from primary data.
  - [ ] **B3 — Industrial-areas context map:** illustrative; municipal
    boundary layer source to verify.

- [ ] **PUBLIC RELEASE PREP (NEW 2026-07-09 — scope + rationale in
  `docs/PLAN_public_release.md`; read it before working these).** An external
  prioritization memo was intaken and reconciled: its build list (WEM/condo fix,
  roads, set-aside, fire, stormwater) is **already shipped or closed** — see the
  plan's reconciliation table. What remains is presentation-layer credibility +
  ops hardening. Release scope locked: everything live stays in; transit/
  recreation/franchise-display stay out. *(AMENDED 2026-07-11, Peter: the
  transit lens is IN — built as the fourth service; see the service-layers
  item below. Recreation + franchise-display still out.)* Items, ranked:
  - _5 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [x] ~~P2.3 Security/PII checklist pass~~ — done 2026-07-09 (Session 33,
    Fable audit): all boxes ticked/dated with evidence; scope updated to the
    Phase-2 static-site + CI surface. **Findings logged, not fixed** — see
    `docs/security-audit.md` "Findings — 2026-07-09" (S1–S6). Follow-ups:
    - [x] ~~**P2.3a Apply S1** (Medium): vendor maplibre-gl@4.7.1 + deck.gl@9.0.38~~
      DONE 2026-07-12 — vendored all three files into `web/vendor/`
      (`maplibre-gl-4.7.1.{js,css}`, `deck.gl-9.0.38.min.js`), `web/index.html`
      points at local copies (no CDN ref remains). Cross-verified vs jsdelivr,
      hashes in `web/vendor/README.md`; basemap is `sources:{}` so zero external
      runtime deps. verify-transit.js 24/24 against the vendored build. See
      security-audit.md S1 RESOLVED. (Branch `vendor/js-libs`, PR #40 merged.)
    - [x] **P2.3b Apply S3 + S4** (2026-07-12): S3 — added `esc()` helper and
      applied it to `neighbourhood_name` + `set_aside_reason` in `tooltipFor`
      (`web/index.html`); verify 24/24. S4 — SHA-pinned all four actions in
      `refresh.yml` (release version in trailing comment). Both → RESOLVED in
      `docs/security-audit.md`. Dependabot auto-bump left out (owner's call).
    - [x] **P2.3c S5 hygiene** (2026-07-12): bumped the 5 dev-freeze pins
      (tornado→6.5.7/bleach→6.4.0/soupsieve→2.8.4/jupyter_server→2.20.0/
      jupyterlab→4.5.9) + a 6th newer CVE found at fix time (mistune→3.3.0);
      `pip-audit -r requirements.txt` now clean. Added a **non-blocking**
      `pip-audit -r requirements-ci.txt` step to `refresh.yml`. → RESOLVED in
      `docs/security-audit.md` S5.
    - [ ] **P2.3d S2** — owner-only content decision, see security-audit.md S2.
  - [ ] **P2.5 Doc-drift fixes** (from the 2026-07-09 architecture
    reconciliation — six items listed in `docs/ARCHITECTURE.md` "Reconciliation
    notes"; no behavioural drift, docs lagging build only). Includes verifying
    the approximate Phase-1 dates in the new `docs/DECISIONS.md` index.
  - [ ] **P3 Decoteau/HHR/Riverview IIMP annotation** (= the existing item
    below; laptop-only) — the OIC-reconciliation credibility anchor; wanted
    before wider outreach, not gating a soft link.
  Platform question RESOLVED (Peter, 2026-07-09): **no new hosting, no new
  engineering** — release ships on the existing Pages deployment, nothing new
  gets built pre-release (plan §2).

- [ ] **Decoteau / Horse Hill / Riverview capital & debt annotation (NEW 2026-07-08).**
  A **citation/annotation layer, NOT a new spatial cost lens**, covering the three
  greenfield growth areas analyzed in the City's IIMP (Integrated Infrastructure
  Management Plan) — a 39-year capital pro forma (developer capital + muni/provincial
  capital + O&M + lifecycle renewal, amortized vs projected tax revenue). This is a
  **fundamentally different unit of analysis** than the citywide recurring-cost map
  (which deliberately excludes capital construction cost). Why now: IIMP is the closest
  existing precedent to the **OIC** (operating-impact-of-capital) accounting the City is
  introducing for the **2027–2030 zero-based budget cycle** — citing it well anchors the
  tool's credibility without rebuilding a citywide capital/debt model we have no data for.
  **Scope (locked — do NOT deviate without flagging):**
  - Click→panel annotation (⚠️ **STALE BLOCKER, corrected 2026-09-16: the pinned
    panel SHIPPED** — `applyHoodMode` / `#hoodmode-btn`, and the temporal,
    services and development lenses all have one. "No sidebar exists" was true
    2026-07-08 and is not now; design against the existing panel) on **three
    specific named hoods only**, clearly labeled as a
    different methodology (multi-decade capital pro forma) from the revenue-per-acre /
    recurring-cost map.
  - **Do NOT** merge these figures into the citywide colour layer, the roads lens, the
    utilities lenses, or any recurring-cost calc; **do NOT** interpolate/extrapolate
    capital-debt cost to other hoods. Only these three growth areas have a published IIMP
    analysis — citywide capital-cost data at this fidelity doesn't exist.
  - Neutral/descriptive framing per project convention: state the IIMP's own projected
    figures + time horizon, don't editorialize.
  **Build:**
  1. Pin Decoteau, Horse Hill, Riverview boundaries in the existing hood boundary file.
  2. Attach a data **annotation (not a computed layer)**: developer capital, muni/provincial
     capital (~$369M piece), build-out horizon, revenue-vs-cost gap — all as stated in the
     source, with explicit citation + "as of" date.
  3. Surface as a click-through popup / footnote-style panel — **NOT** a toggle affecting
     the main colour ramp.
  **Sources — VERIFIED 2026-07-15 (laptop), research half DONE.**
  - **PRIMARY: Report CR_2705, "IIMP – Cumulative Impacts," March 22 2016** (+ 20-pg
    Attachment 1). **Every figure verified against the primary tables** — see
    `docs/FINDINGS_iimp_growth_areas.md`: developer $3.806B (Drainage $2.351B +
    Transportation $1.455B); City/Province $1.362B (full 8-line Table 3 breakdown
    confirmed); ~$1.4B 50-yr cumulative shortfall (**distinct** from the $1.362B
    capital — do NOT conflate, both ~$1.4B by coincidence); areas Decoteau 1,960 ha/
    74,565/39yr, Horse Hill 2,793 ha/70,038/36yr, Riverview 1,435 ha/50,422/30yr;
    combined pop 195,025. All **2016$, projections at build-out, "received for
    information"**. PDFs saved `data/raw/iimp/` (gitignored). doniveson.ca archive
    reachable from Oracle too, so the BUILD (D2) is not laptop-gated.
  - **Currency check done:** the 2016 IIMP is NOT superseded per-area — the new
    CIO/OIO framework (2027–2030 budget) is a citywide 10-yr capital outlook, not a
    per-growth-area pro forma. Cite 2016 IIMP, date-stamped. → build = ticket D2.
  - 2016 Global News coverage (already in project research) as secondary corroboration —
    primary report should supersede it for exact figures.
  - Off-site levy bylaw + capital financing policy — how the ~$369M muni/provincial piece
    was financed (debt vs levy vs grant); that's the "debt" component specifically.
  - City annual financial statements / debt management reports — actual debt-servicing
    cost + interest rates for the relevant financing period, IF we want real debt-service
    cost rather than just capital outlay.
  - Infrastructure committee **mid-2026 OIC presentation** (already in project context) —
    check whether it re-presents/updates the three areas' figures under the new OIC
    framework; if so, cite that instead of the 2016 analysis.
  **Non-goals:** no citywide capital-cost-per-hood dataset this pass; no blending into any
  recurring-cost lens.

- [ ] **GROWTH INFRASTRUCTURE FINANCING PANEL ("Debt Lens") — NEW 2026-07-14
  (brief: `docs/fable_brief_debt_lens.md`; scoped to these tickets same day).**
  From Peter's planning conversation; full research backing lives in claude.ai
  project knowledge (`Edmonton_Growth_Infrastructure_Financing__Feasibility...`),
  NOT in this repo — the brief is the authoritative in-repo doc. **Scope decision
  LOCKED (→ DECISIONS.md 2026-07-14): NO debt-per-parcel/neighbourhood map** —
  citywide debt isn't spatially attributable in public data. Two clearly-labelled
  components instead: (1) spatial growth-area financing transparency panel,
  (2) non-spatial citywide debt context. Framing = "financing transparency", NOT
  "debt attribution" — explicit in UI copy (load-bearing methodological claim).
  **Reachability probed 2026-07-14 (Oracle box):** doniveson.ca IIMP PDFs 200,
  open.alberta.ca FIR page 200 — D2/D5 data is Oracle-doable; only D0's bylaw
  map exhibit is edmonton.ca/laptop-gated.
  **⚠ INTERACTION PREREQ (all display tickets D1–D5-chart):** the app has **no
  sidebar** — ⚠️ **THIS PREREQ IS DISCHARGED. Corrected 2026-09-16: it was true
  2026-07-14 and a pinned click→panel surface has since shipped** —
  `applyHoodMode`, `#hoodmode-btn`, a two-gesture touch gate (DECISIONS
  2026-07-31), and panels on the temporal, services and development lenses.
  **D1–D5 are NOT blocked on designing an interaction; they build into the
  existing panel.** The original text, kept because it is what the tickets below
  were written against: there is no click→panel surface at all; interaction today is
  hover-tooltips only (S54 learning). Every "sidebar entry / extend the existing
  sidebar UI" phrasing below is aspirational shorthand from the brief, NOT an
  existing surface. **A new click→panel interaction must be designed and decided
  (Peter's call) before any D-series display work can start.** Read the phrasing
  below as "which content goes in that panel", not "add to a panel that exists".
  Tickets, build order:
  - _2 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **D1 — levy performance mini-viz.** Cumulative levy collected vs the
    ~$26M single-facility cost, per catchment (simple bar/ratio — makes the gap
    immediate). Figures in the brief (2022–2024 annual reports; cumulative
    $3.83M end-2024, **zero halls levy-funded**). Use the 2024 **Table 6.1**
    figure ($3,033,592), footnote the exec-summary discrepancy ($3,259,866).
    Headline finding to make visually obvious: **Edmonton levies developers for
    fire halls ONLY** — no trunk roads/water/sanitary/storm levy (vs
    Calgary/St. Albert $170K–$270K/ha) — "1 of 5 essential services levied".
    Small manual dataset → reviewed JSON input (mill-rates pattern).
  - [ ] **D2 — IIMP financing split** (extends the Decoteau/HHR/Riverview
    annotation item above — primary source now located, Oracle-reachable). Add
    the developer-vs-City split to the Decoteau/HHR/Riverview click→panel content:
    developer $3.806B (drainage $2.351B + transportation $1.455B) vs
    City/Province $1.362B, net ~$1.4B 50-yr shortfall — 2016 projections,
    **label as projection, not actual**. **Needs the click→panel interaction
    decided first (see INTERACTION PREREQ above — ⚠️ **DISCHARGED 2026-09-16,
    the panel exists**).**
  - [ ] **D3 — Blatchford contrast case study.** 4th panel entry, same content
    pattern: the infill counter-example to the 3 greenfield areas —
    self-liquidating "debt recoverable" financing (Policy C597A), DESS
    district energy, $23.7M federal SREPs grant, own levy catchment
    ($32,813/ha, already in the D0/D1 table).
  - [ ] **D4 — sanitary trunk callout** (one-line panel text, NOT mapped —
    no clean basin boundaries confirmed): SSTC/EA charges paused May 2024;
    growth trunk sanitary currently funded from the accumulated ratepayer
    reserve, not active growth charges (figures in the brief).
  - [ ] **D5 — Component 2: citywide debt context chart (non-spatial).**
    Separate panel/chart, labelled "citywide, not neighbourhood-specific" —
    never a map layer. Headline 2025: $4.6B outstanding, 69% of the
    tax-supported debt-servicing limit (DMFP ≤18%/≤21% limits in the brief).
    - [x] **Data layer DONE 2026-07-14**: `scripts/fetch_fir_debt.py` →
      committed `data/fir_debt_series.json` — Edmonton + St. Albert +
      Strathcona County, **2003–2025** (a year further than the brief
      expected: the 2025 FIR is out, Edmonton total debt $4,592,150,000 =
      the brief's "$4.6B" headline, directly sourced). All four Schedule AA
      fields (debt + limits + servicing). Manual-reviewed-input pattern;
      anchor cross-checks + neighbour-band sanity; Strathcona-2013 $000s
      source quirk corrected + documented. DATA.md §11. +10 pytest (328).
      NB the FIR limit is the MGA regulation limit — Edmonton 2025 = 59.3%
      of it; the brief's "69%" is the DMFP servicing limit, a different
      denominator (quirk documented in §11).
    - [ ] **Display/chart** — undecided design (where does a non-map panel
      live in the UI?); Peter's call before building.
  - **Out of scope (locked in the brief):** any spatial allocation of the
    $4.6B; S&P rating detail / CCBF/MSI/LGFF; Local Improvement levies
    (genuinely parcel-level but not open data — future phase, needs
    FOIP/per-bylaw scraping).

- [ ] **DEVELOPMENT & INFILL LENS family (NEW 2026-07-12 — full plan in
  `docs/SPEC_development.md`).**
  ⚠️ **Stock age was WITHDRAWN from this lens 2026-07-27** (Peter: not
  working well as an option) — see `DECISIONS.md`. The UI and render path
  are gone and `verify-age-spikes.js` is deleted, but `median_year_built`
  still ships in `value_grid.json` and
  `FINDINGS_stock_age_spike_scaling.md` still holds the scaling work, so
  a different presentation would not start from zero. Anything below that
  assumes a 3-way Detail selector is stale.
  Permit-based "where is building actually
  happening" lens family, the direct answer to what `FINDINGS_growth_servicing.md`
  could only proxy with median building-stock age. Data verified live 2026-07-12:
  General Building Permits `24uj-dj8v` (243k rows, 2009→now; has `units_added`,
  `work_type` new-vs-reno, `building_type`, `neighbourhood` UPPERCASE-matches-ours,
  lat/long, `construction_value`). Build one minimal cut of each lens to *see it*
  before designing the next. Three locked decisions (Peter, 2026-07-12) →
  DECISIONS.md: (1) activity = choropleth, (2) infill = suitability×activity
  mismatch shown both ways, (3) combined cost side = city service cost (not
  permit construction_value).
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] **Lens B — Suitability × Activity mismatch, PHASE 2 — SHIPPED; only the
    optional refinement below is still open** (verified 2026-09-16: `far` is
    served, `tools/profiling/verify-infill.js` exists, the Infill view is live).
    Signed diverging
    metric `z(suitability) − z(activity)`: two views off one scale — suitable-
    but-quiet (opportunity) AND less-suitable-but-building (Peter's flip).
    - [x] **Suitability proxy LOCKED 2026-07-13 (Peter): built FAR** (`far` = Σ
      floor area ÷ deduped lot area/hood; low FAR = underused). Backend column
      DONE — `load_property_info` loads `gross_area`, `build_hood_lot_acres`
      emits `far`, `join_and_calculate` carries it into geojson + SLIM
      (unsuppressed by LOW_PARCEL_FRAC); +7 tests, 318 green. DECISIONS.md +
      SPEC_development Lens B + DATA.md §2.
    - [x] **Web `Infill` diverging view DONE 2026-07-13:** `z(suitability) −
      z(activity)` = `−(z(far)+z(activity))` computed live (responds to the
      units/permits × 5yr/3yr pickers); one dark-centred diverging plane (teal =
      suitable-but-quiet, orange = building-where-less-suitable), set-aside
      EXCLUDED from the z population (358 hoods kept). DECISIONS + SPEC_development.
    - [x] **Asymmetric residential opportunity gate DONE 2026-07-13:** a prototype
      showed the planned maturity gate (median `year_built`) DOESN'T fix the
      opportunity end — the pollution is structurally-low-FAR *non-residential*
      land (industrial/fringe, all decades), not new suburbs. Fix: non-residential
      hoods barred from the teal opportunity end (grey) but kept on orange/pressure
      + in the z population (keeps DOWNTOWN). Web-only, no new pipeline column
      (`infillOppSuppressed`). `verify-infill.js` 41/41. DECISIONS + SPEC_development.
    - [x] ~~**Lens B per-arm colour scaling (REOPENED 2026-07-14, handed to Fable).**
      S48 audit: the mismatch score is structurally asymmetric (suitability capped
      +0.97, activity unbounded) so the symmetric p95 clamp leaves the teal arm
      unable to saturate (0 teal vs 18 orange saturations) + median hood on the
      +0.5 verdict line. Fix (web-only): clamp each arm at its own p95 + verdict
      cut-points in `t` space. Brief: `docs/FABLE_infill_perarm_scaling.md`~~ —
      done 2026-07-14 (Fable): `clampPos`/`clampNeg` in `infillStats`, per-arm
      `infillT`, verdict cut at `t = ±0.4`; `verify-infill.js` 44/44; live on the
      next `refresh.yml` run.
    - [ ] **Lens B optional refinement (future, low priority):** one-sided
      opportunity/pressure choropleth toggles (the single diverging map already
      shows both). SPEC_development Lens B.
    - [ ] **Lens B fine-grain "Infill detail" (assessed 2026-07-14, not yet
      decided):** the z-mismatch SCORE doesn't survive 100 m grain (~88% of
      inhabited cells have zero 5yr activity — every quiet cell would read
      "opportunity"; set-aside/residential gates are hood-level constructs).
      The honest fine-grain version is the DECOMPOSED ingredients: a per-cell
      FAR texture (per-point `gross_area` + `_point_lot_stats` lot dedupe —
      `build_hood_lot_acres` keyed on cell instead of hood) under the Lens A
      permit spikes (now shipped), verdict stays hood-level. Middle path if a
      finer score is ever wanted: prototype 250–500 m cells first. Needs
      Peter's call before building.
  - [ ] **Lens C — Activity vs City Service Cost, PHASE 3 / future.** Where new
    building goes vs modeled city service columns (road/storm/water/fire per acre)
    or V2 unit-cost $/acre (laptop-gated). Two-ledger idiom of
    FINDINGS_growth_servicing made spatial. `construction_value` NOT used here.
    Depends on Lens A + V2 unit costs.

- [ ] **Views & lenses follow-ons — its own three asks are all DONE (verified
  2026-09-16), but this stays OPEN because live work is nested under it**
  (utility cost lenses, the deferred Rider T question) — closing it would
  archive that work out of sight, which `tools/todo_archive.py` refused to do.
  ⚠️ The first ask has since been UNDONE — see its note.
  Three asks on top of the then-shipped Money | Roads | Ratio views:
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [x] **More service layers — DONE (verified 2026-09-16: `roads`, `fire`,
    `water`, `storm`, `transit`, `bike` all ship in `METRICS`, each with a
    `src/load_*.py`).** Each needed its
    own SPEC_services section (dataset, filters, locked decisions), a
    per-hood supply column, and a slim web export.
    - [x] ~~**Transit lens**~~ — BUILT 2026-07-11 (Peter's call, AMENDS the
      2026-07-09 release-scope lock that kept transit out): mean-weekday
      scheduled GTFS stop-events/acre (`transit_dep_per_acre`, sqrt colour
      FINDINGS §6.8), Services-view checkbox + 58 LRT-station/transit-centre
      dots, five new weekly GTFS downloads. SPEC_services "Transit lens",
      DATA.md §9. Scheduled supply, NOT ridership (none exists stop-level);
      current-signup seasonality is the standing caveat.
      - [x] ~~**LRT track lines** context layer~~ — added 2026-07-11: the
        operating network (Capital/Metro/Valley) as a `PathLayer` under the
        station dots (`rpjw-4jft` "LRT Routes" → `web/data/lrt_lines.json`,
        343 segs); the HER heritage streetcar is excluded (not ETS LRT
        service). Not part of the metric. DECISIONS.md 2026-07-11.
    - [x] ~~**Services-view UI generalization**~~ — **SHIPPED 2026-07-05:
      PR #14 merged + deployed + LIVE** (run 28767241818 — deploy step
      needed two transient-error reruns, "Deployment failed, try again
      later"; live verified serving the Services button + storm column on
      all 406 hoods; CI regenerated the geojson byte-identical). The Roads
      view is now a "Services" view with per-service checkboxes (Roads,
      Stormwater; Fire added 2026-07-06) and a "colour" radio choosing which checked
      service drives the ramp (others render neutral; defaults = the old
      Roads view exactly). Headless-verified
      (`tools/profiling/verify-services.js` + regressions green) +
      screenshots (`shot-services.js`) + Peter's on-device eyeball. Display
      detail: UI.md "Services views".
    - [x] ~~**"Total services" / Ratio-view denominator reopen**~~ — **DECIDED
      2026-07-10 (Peter) + V1 BUILT same day** (branch
      `feature/ratio-denominator-picker`): the ratio stays **PER-SERVICE** —
      a "Ratio denominator" picker (revenue per road metre | per fire
      event) in the Ratio view. Modeled EPCOR dollars (storm/water) are
      excluded from any levy ratio by the money-flow honesty rule (they'd
      compare unrelated flows / cancel if added to both sides) — so the
      "two dollar services" trigger resolved to per-service, not a $ sum.
      Fire floor 0.005 events/acre/yr + log colour: FINDINGS §6.7;
      SPEC_utilities decision 3 holds the full design; headless-verified
      (`verify-ratio-denom.js`, 27 checks) + regressions + screenshots.
      Also fixed in passing: `verify-labels.js` still clicked the retired
      "roads" view button (stale since the 2026-07-05 generalization).
      **PR #33 merged (`e0da845`) + deployed 2026-07-10** (refresh run
      29099791508 green → auto-refresh `e8f58b4`; github-pages deploy
      success; live-verified 27/27 vs the Pages URL).
    - [x] **V2 — combined "modeled city service cost per acre" — CLOSED AS
      SUPERSEDED (verified 2026-09-16).** `svc_cost_per_acre` was built and then
      **RETIRED 2026-09-05** (`DECISIONS.md`: the roads+fire composite, its
      Services row and its Ratio denominator all removed; the cost side publishes
      DISJOINT per-term columns instead — `cost_roads_ops_per_acre` etc.).
      **Do not rebuild it.** Original design: one
      denominator = road metres × roadway O&M+renewal $/m/yr + fire events ×
      (Fire Rescue operating budget ÷ citywide dispatches). Labeled MODELED,
      "roads + fire only", never "total city cost". Design locked in
      SPEC_utilities decision 3.
      - [x] **Unit-cost source hunt DONE 2026-07-15 (laptop)** — the
        laptop-gated half. `data/city_unit_costs.json` (reviewed input,
        mill-rates pattern): **roadway $50/m/yr** (edmonton.ca Development
        Impact page: $600k O&M + $1.9M renewal per km ÷ 50-yr life; Peter's
        50-yr call; 3%-of-value cross-check ≈ $45) + **Fire Rescue 2026 gross
        operating budget $276.706M** (2026 Approved Operating Budget PDF; net
        $273.598M). Provenance + caveats in the JSON.
      - [x] ~~**Build the composite metric (Oracle-doable).**~~ — done
        2026-07-15: `load_unit_costs` + `unit_costs` arg in
        `join_and_calculate` → `svc_cost_per_acre` = road_m_per_acre ×
        $50/m/yr + fire_events_per_acre × (budget ÷ the fire frame's OWN
        citywide kept-event total, pre-join — unmatched fire hoods stay in
        the denominator). Requires BOTH roads + fire (warn+skip otherwise —
        a one-term composite would be mislabeled). In `SLIM_COLUMNS`, so
        the column ships with the next refresh run (code-only PR; the
        local raw snapshot is older than the live auto-refreshed data,
        so no regenerated GeoJSON was committed). +9 pytest (351).
        Real-data run verified: **$3,142/event** ($276.706M / 88,065 kept
        events/yr), composite on all 406 exported hoods, median
        $3,302/acre/yr (fire-dominated downtown ~$34k, road-dominated
        suburbs ~$3.4k — the allocation caveat is visible in the data).
      - [x] **Display (UI) for the composite — BUILT, then RETIRED. Verified
        2026-09-16: `svc_cost_per_acre` has 0 occurrences in `web/index.html`.**
        Both halves below shipped 2026-07-16 and both were removed 2026-09-05
        (`DECISIONS.md`: the roads+fire composite, its Services row AND the Ratio
        "Per service $" denominator). ⚠️ **Closed as superseded, not as done — do
        not rebuild either.** Original decision:
        (Peter): BOTH, staged** (Services checkbox first, then a Ratio-view
        coverage denominator). Carry the fixed-budget-allocation + "roads +
        fire only, never total city cost" caveats in copy.
        - [x] ~~**(a) Services-view checkbox**~~ — BUILT 2026-07-16
          (`feat/v2-svc-cost-display`): 6th per-service row "Service cost
          (roads+fire) — modeled $/acre" on the shared `svc-plane` (SERVICES
          `servicecost`, sqrt colour), blurb + legend + tooltip with both
          caveats, column-guarded (hides until the column ships on the next
          refresh). `verify-services.js` + `shot-services.js` extended;
          screenshot eyeballed (fire-heavy core bright, greenfield grey).
        - [x] ~~**(b) Ratio-view coverage denominator**~~ — BUILT 2026-07-16
          (`feat/v2-svc-cost-display`): 3rd "Ratio denominator" option "Per
          service $" = revenue ÷ modeled roads+fire cost (dimensionless).
          **Magnitude, not break-even (Peter): same log ramp, no 1.0
          marking; median ≈5.8× so blurb/tooltip own "not a sign the land
          pays its full way".** ×-format legend bounds, $230/acre floor,
          picker opens on hasFire||hasSvcCost, button column-guarded.
          verify-ratio-denom 38/38; screenshot eyeballed.
    - [x] ~~**Fire lens**~~ — **BUILT 2026-07-06** (design DECIDED 2026-07-05,
      Peter, all four recommendations: demand metric events/acre/yr as the
      Services ground plane + 31 station dots; all emergency responses minus
      operational noise, medical share a caveat NOT a filter; 2023–2025
      averaged, pinned `FIRE_YEARS`; built after the Services UI landed).
      As built (branch `claude/session-summary-review-vwweia`):
      `src/load_fire.py` (+21 tests) + `download_data.py` sources
      (`7hsn-idqi`, `b4y7-zhnz`) + `join_and_calculate` FIRE_COLUMNS →
      `fire_events_per_acre` in SLIM_COLUMNS + `main.py --skip-fire` +
      third Services checkbox (shared `svc-plane`, station dots,
      demand/medical caveats) + verify-services/shot-services extended.
      209 pytest green; headless-verified against a SYNTHETIC fire column.
      Dataset facts: DATA.md §7–8; spec: SPEC_services "Fire lens".
      **Remaining follow-ups (blocked on network access to
      data.edmonton.ca — the build session's VM policy denied it):**
      - [x] ~~First real-data run~~ — DONE 2026-07-06 (Session 18, Oracle
        server): `dispatch_datetime` resolved as the first exact candidate
        (186 of 948k unparseable); mix verified (MEDICAL 60%, 4,025 noise
        excluded, 88,065 kept events/yr / 408 fire hoods). Caught + fixed
        TWO real-data bugs: PR #17 (event_type_group carries CODES — filter
        on event_description) and PR #18 (`FIRE_NAME_CORRECTIONS`: fire CSV
        still says OLIVER for WÎHKWÊNTÔWIN, 1,476 events/yr displayed as 0;
        + 3 "AREA" collapses). Live-verified: plane + 31 dots + tooltip.
      - [x] ~~Colour transform check on real `fire_events_per_acre`~~ —
        DECIDED 2026-07-06: **sqrt** (raw skew +7.86, the project's worst;
        clamp/median 5.8×; linear crammed 59% of hoods into the ramp's
        bottom fifth; log undefined on the 5 zero hoods. FINDINGS §6.5).
      - [ ] **January task**: the fire-years roll → **`RUNBOOK.md` §1 step 4**,
        which owns all three pins and the `WINDOWS` copy. (Local instructions
        deleted 2026-09-16: they were a stale partial copy doing 1 pin of 3.)
    - [ ] **Utility cost lenses — SPEC'd 2026-07-05 (`docs/SPEC_utilities.md`);
      stormwater DECIDED first (Peter) and its v1 pipeline built same day.
      ⚠️ **"unmerged on `feature/stormwater-lens`" is STALE (corrected
      2026-09-16): `src/load_stormwater.py` is on master and the branch is gone.**
      The REST of this item is genuinely open.** Five candidates in three
      fidelity tiers, from Peter's methods doc
      (`docs/utility_cost_estimation_lens_methods.md` — verified 2025/2026
      tariffs; rate numbers live there). All outputs MODELED, not billed.
      - [x] ~~Stormwater pipeline (Lens 1)~~ — built 2026-07-05:
        `src/load_stormwater.py` (bylaw A×I×R per point; `ZONE_RUNOFF`
        explicit dict; condo dedupe reused; fixa-tstc zone fallback) +
        year-keyed `data/stormwater_rates.json` + join/main wiring +
        19 tests (182 green). Real data: 287,103/287,163 points, citywide
        $240.4M/yr (2025 rate), ranking sanity passes (industrial top,
        river valley bottom). As-built numbers + caveats: SPEC_utilities
        Lens 1 (serviced-area assumption is the big one — EETP fringe = 5%
        of the total; AG runoff coded 0.1 with VERIFY flag).
      - [x] ~~**Display shape**~~ — DECIDED (Peter; SPEC decision 2) and
        **SHIPPED 2026-07-05 (PR #14, with the Services-view item above)**:
        per-hood ground-plane layer in the generalized Services view —
        linear colour, clamp p97.5 of non-set-aside hoods (≈ $2,700,
        runtime), set-asides grey, legend + blurb labeled MODELED /
        "modeled, not billed"; `storm_charge_per_acre` added to
        `SLIM_COLUMNS` (hood GeoJSON 0.7 MB, all 406 hoods carry it).
        Pipeline PR #13 merged first, as sequenced.
      - [x] ~~Water + sanitary (Lens 2)~~ — BUILT 2026-07-07 (Session 18,
        branch `feature/water-lens`; decisions locked with Peter
        2026-07-06: residential+multi-res scope, two columns, colour by
        TOTAL): `src/load_water.py` (per-connection model — roll points
        as connections, meter-size bands, inclining/declining blocks) +
        `data/water_rates.json` (Apr 2026 tariffs; `WATER_RATE_YEAR` pin)
        + join/main wiring + fourth Services checkbox (LINEAR colour,
        FINDINGS §6.6; tooltip fixed/total split). Real run: 268,489
        connections / 551,831 modeled households, citywide $588.1M/yr
        ($133.9M fixed). 229 tests green; headless-verified on real data.
        As-built numbers + caveats: SPEC_utilities "Lens 2 as built".
        Follow-ups: household count ~20% over census (floor-area→units
        assumption — [x] ~~sensitivity-check M2_GROSS_PER_UNIT~~ DONE
        2026-07-07: 70–120 m²/unit sweep moves households ±7% but citywide
        $ only ±5% — the assumption is NOT the source of the EPCOR gap;
        90 baseline stands. `tools/sensitivity_m2_per_unit.py` +
        FINDINGS_utility_validation §2.1); validation vs EPCOR revenue
        (below, now covers water too).
      - [x] ~~Validation pass vs EPCOR published revenue~~ — DONE
        2026-07-07 (Session 19), full numbers + sources in
        `docs/FINDINGS_utility_validation.md`. **Order-of-magnitude PASS
        both lenses.** Stormwater: $240.4M modeled vs $141.1M published
        2025F (1.70×), but residential slice is 1.11× and the excess is
        localized (notyet+never zones = $49.8M unbilled land; I=1.0 vs
        real DIF reductions on commercial). Water/sanitary: $588.1M vs
        ≈$467M published res+MR scope (≈1.26×); connection count 13%
        UNDER EPCOR's (268k vs 308k accounts) — excess is per-connection.
        [Refined 2026-07-07: the in-city water res+MR share was a flat ~70%
        guess; now derived to ~80% from EPCOR's by-class customer+consumption
        counts (EWS 2024 PBR Progress Report p.9, FINDINGS §2.2), tightening
        the ratio 1.33×→1.26×. The raw water revenue-by-class schedule stays
        unreachable (all edmonton.ca public-files paths dead, no Wayback), so
        ~80% is a blend estimate, not a read-off — but a well-anchored one.]
      - [x] ~~**Peter decision (bracket quantified, FINDINGS §3)**~~ —
        DECIDED 2026-07-07: report BOTH (all-parcels $240.4M AND excl
        notyet+never zones $190.5M). Shipped same day:
        `UNBILLED_CATEGORIES` in `src/load_stormwater.py` — log line +
        `.attrs` carry both totals; per-hood outputs unchanged
        (reporting, not modeling). 230 tests green; real-data verified.
      - [x] ~~Lenses 3–4 (electricity/gas franchise)~~ — BUILT 2026-07-07
        as **columns only, no display layer** (Peter's call: they're
        collinear with dwelling count — flat per-dwelling proxy makes every
        column `dwellings × constant`). `src/load_franchise.py` reuses
        `load_water.build_connections` (extracted shared helper → ONE
        551,831-dwelling model) + `data/franchise_rates.json` + join wiring
        (`FRANCHISE_COLUMNS`, out of SLIM) + `--skip-franchise`; 8 tests
        (238 total). Real run: **$162.6M/yr modeled City revenue** (elec LAF
        $36.9M + gas franchise $125.7M). Modeled LAF ~⅓ low vs published
        $8.33/mo (base schedule vs full distribution revenue — documented).
        As-built + validation: SPEC_utilities "Lens 3+4 as built" +
        FINDINGS_utility_validation §5. Follow-ups: (a) ~~validate vs City
        budget franchise line~~ **DONE 2026-07-07** — vs Note 24 of the 2024
        Financial Annual Report (audited): combined elec+gas modeled $162.6M
        vs actual $175.9M = **0.92×**, but two offsetting errors — gas 1.32×
        over (Rider T in the 35% base; excl → 1.00×), elec 0.46× under (LAF
        floor). FINDINGS §5.1; (b) commercial scope needs a consumption proxy;
        (c) display lens if ever wanted.
      - [ ] **DEFERRED (Peter, 2026-07-07 — revisit later): exclude
        transmission Rider T from the gas franchise base?** Validation §5.1
        found modeled gas franchise ($125.7M) exceeds the all-sector City
        actual ($95.2M) at 1.32×; dropping Rider T ($1.357/GJ) from the 35%
        base → $95.6M ≈ 1.00×. One-line change (`gas_rider_t_per_gj` already
        isolated in `franchise_rates.json`). NOT proven — residential-only
        matching an all-sector actual could be a compensating 115 GJ/dwelling
        overcount. Parked as-is with the Rider-T caveat documented; no model
        change for now.
      - [x] Remaining SPEC open decisions — **both resolved (verified 2026-09-16).**
        (3) modeled $ in the "total services" denominator is **moot**: the
        composite it would have fed was retired 2026-09-05. (4) was already marked
        SETTLED in place. Original: *"(3) modeled $ in the "total services"
        denominator (recommended: not yet); (4) franchise-fee revenue columns
        only with their lenses — SETTLED (columns only, built above)."*
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
- [ ] **Deployment follow-ons (deferred, see `docs/SPEC_deployment.md`):**
  - _1 closed sub-item moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] Auto-**fetch** matching `pwis-wc4c` rates for a newly detected year (the
    guard detects + holds; it doesn't self-heal). Recovery is manual: bump
    `ASSESSMENT_YEAR`, extend `mill_rates.json`, update `generate_status.py` years,
    `--clear-banner`.
  - [ ] Per-year archive filenames (`web/data/YYYY.geojson`, keep-not-overwrite) for
    the future UI year selector. ⚠️ **PREMISE HALF-OVERTAKEN — re-measured
    2026-09-16 (S166). The keep-not-overwrite ARCHIVE already exists and this
    item should not build a second one:** `data/temporal_archive.json` (74 KB,
    committed) is written by `src/load_temporal.write_archive` on every pipeline
    run, and `SPEC_temporal.md` marks it **✅ CLOSED 2026-07-28**, with
    `scripts/check_temporal_archive_year.py` guarding the year each entry is
    filed under. **What is still genuinely open is only the UI year selector** —
    and it would read that file. ⚠️ **It is NOT dead**: the temporal lens is
    per-NEIGHBOURHOOD by design (Peter, 2026-07-28: *"you mouse over and get a
    line graph … for that hood"*), so nothing recolours the whole MAP to a chosen
    year, and no year-selector control exists in `index.html` (checked). Rewrite
    the task as *"a year selector over `temporal_archive.json`"* when it is
    picked up; do not emit per-year geojsons.
  - _2 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
- [ ] **Data-integrity audit follow-ons** (first run 2026-07-01, **second run
  2026-07-11** — see `docs/FINDINGS_data_integrity_audit.md`; second run covered
  all post-07-01 modules: roads/storm/water/franchise/fire/transit/lot-acre/grid.
  **No blocking findings; published numbers confirmed trustworthy.**):
  - _3 closed sub-items moved to `docs/TODO_archive.md` § "Closed sub-items lifted out of still-open parents" (2026-09-16) — they shipped; nothing open was moved._
  - [ ] (Optional, fidelity) map `MA DERELICT RESIDENTIAL` to the dedicated
    "Mature Area Derelict Residential" rate class instead of "Non Residential" —
    identical municipal rate today, differs if `rate_type` ever changes (audit T1).

- [ ] **Visual polish** (pre-existing, untouched):
  - [ ] top-cap edge colour ("not happy yet") — `RAMPS[<ramp>].edge`, **all
    three ramps** (was `TOP_EDGE_COLOR`, one value, until the palette switcher).
  - [ ] deferred zoom-out (`HOME`/`HOME_2D` ~10.2→~9.4) + the per-metric
    `elevationScale` values scaled with it (no global `ELEVATION_SCALE`).
  - [ ] light mode — ⚠️ **the colourblind half is DONE (verified 2026-09-16:
    `cividis` is a named palette in `web/index.html`, "perceptually uniform +
    colour-blind safe"); only LIGHT MODE remains** (no `prefers-color-scheme` in
    the file)

- [ ] **(Optional) exploration notebook** — work `FINDINGS_assessment_classes.md`'s
  "to visualize" list (value vs levy share by class; split-class distribution;
  per-neighbourhood exempt share). Notebooks go in `notebooks/exploration/`;
  use `NotebookEdit`. (A "use the Jupyter MCP server tools, not NotebookEdit"
  line was deleted 2026-09-16 — no such rule, and no MCP server is configured.)

- [ ] **PROPOSED (needs Peter's yes/no): the lens registry — `docs/PROPOSAL_lens_registry.md`.** ⚠️ **Nothing built; do not start it, and do not start it alongside the fix-in-place PR below.** Finishes the registry `VIEWS` already is, moving per-lens decisions out of the dispatchers field by field (title/blurb → legend → layers → tooltip → controls → ensure), six independently shippable PRs each verified by an **identical** render.
  - **The measured problem: 28 symbols branch on lens identity** (`applyView` 50 branches, `refreshLegend` 8, `buildViewLayers` 8, `viewTooltip` 7, `primaryRow` 7, `legendGradient` 6, plus a 22-symbol tail of 1–2 each). ⚠️ **The `the Lab` banner comment's own add-a-lens checklist names FIVE places — it undercounts by 5×**, and that is why lens work feels like it touches everything.
  - ⚠️ **The design constraint that rules out the obvious version:** `applyView` is an ordered pipeline, not a switch — chrome must be final before `buildLayers()` (the label sweep measures live bounding rects; two shipped bugs, SPRUCE GROVE and DEVON), `syncAmenityControls` must follow `await ensureGridData()`, and every await carries a re-entrancy guard. **So the kernel keeps the phase order and lenses contribute pure per-phase functions — NOT `lens.render()`.**
  - **Why it matters beyond tidiness:** it is the **third re-open trigger** on the `DECISIONS.md` 2026-09-05 "stay one file" decision — per-lens ES modules fall out of it for free. It is the only route by which the split becomes correct.
  - ⚠️ **Step 5 (controls) is shared desktop+mobile DOM** — read `docs/CONTROLS_MATRIX.md` first. ⚠️ **No user-visible payoff by design**; if the appetite isn't there, log the NO so this is not re-proposed every time a lens edit touches five files, and fold the 28-branch count into the Lab comment as the corrected checklist.

- [ ] **⚠️ PAIRED with `AUDIT_LEDGER.md` never-audited #3 ("checks that cannot fail") — Peter deferred the audit 2026-09-06 ("later"), and this item is its structural half.** A sound check nothing runs is no better than a vacuous check that does; one brief should answer both. Two more vacuous checks were found 2026-09-05 while retiring the cost composite (`verify-transport-cost.js` comparing against the composite so the *fire* term supplied its gap; `_TRANSPORT_COSTS` with both road rates at $2.0), bringing the class to seven.
- [ ] **⚠️ VACUOUS-GUARD AUDIT RUN 2 (2026-09-08, S147, Fable 5.1) — `docs/FINDINGS_vacuous_guards_r2.md`. Two HIGH, both reproduced end to end; two items are Peter's call, two are test-only and ready to build.**
  - ✅ **DONE 2026-09-08 (S147) — R1 + R3 shipped in one PR (Peter: "whatever is easiest"). 820 → 825; `DECISIONS.md` 2026-09-08.** An all-null baselined column is now a third failing bucket (`EMPTY`) in `check_served_columns.py`, falsified three ways against the real served file, with the partial-null and absent-column directions pinned so it cannot cry wolf; B8 now counts the rows it examined and fails at zero. ⚠️ **The render gate still cannot see an all-null column and that is by design** — re-measured after the fix, smoke passes and the data guard exits 5. Original proposal:
  - **~~PROPOSAL~~ (changes what the PUBLISH gate accepts): R1 + R3 in one PR.** ⚠️ **R1: a served column can go ALL-NULL and the weekly publish stays green** — `res_revenue_per_acre` null on 406/406 → `check_served_columns.py` exit 0 (it counts KEY PRESENCE by design; the 2026-08-03 decision covered a *dropped* column, not an empty one) **and** `verify-smoke.js` ALL CHECKS PASSED on the public build (money legends are static literals; `viewTooltip` omits null rows; `check_revenue_deltas` reads `total_revenue` only). **Sized:** 0 of 67 baselined columns are all-null today, 5 carry nulls, worst 16/406 — an *all-null is drift* rule reds nothing today and both mutations. Fix: per-column null count in `data/expected_columns.json`, fail on all-null (warn on a jump). **R3 (one line):** smoke B8 filters selector misses out, so `data-service` renamed → PASS with 0 rows examined; report `n examined`, fail at 0. Falsification for both is written in the findings.
  - ✅ **DONE 2026-09-08 (S147) — R2 + R4(1) shipped, test-only, 800 → 820, no CI behaviour changed.** All four mutations the audit found green now red **by name**: the three guards' `main()` exit mapping (each with an opposite-direction sibling so an always-drift guard cannot pass), every guard step's membership in all three workflows, the smoke gate's POSITION (`upload - smoke == 1`) and both-builds coverage, `refresh.yml`'s `case` labels DERIVED from each script's `EXIT_*`, and literal pins on all six guard bands. ⚠️ Only the CSV readers are stubbed in the two `main()` tests — the detectors and the exit mapping are real. Original scope:
  - **~~READY TO BUILD~~ (test-only, no CI behaviour change): R2 + R4(1).** ⚠️ **R2: the merge gate's guards can be neutered at their exit line with 800 green** — `check_cost_copy` drift `return 5 → 0`, `check_value_anchors`/`check_temporal_years` `EXIT_DRIFT → EXIT_OK`, and `tests.yml` with the cost-copy step *deleted*: each **800 passed**. No test calls any of the three `main()`s; `test_ci_workflows.py` pins pytest's wiring only (2 of ~14 guard steps) and its one assertion is `any("pytest" in r)`. Build: a `main()`-level exit-code test per guard (`check_cost_copy.main()` takes no argv — monkeypatch `sys.argv`); `test_ci_workflows` pins for every guard step's command, smoke on BOTH builds immediately before `upload-pages-artifact`, and `refresh.yml`'s `case 0/3/4` labels equal to the scripts' `EXIT_*` (mutating `EXIT_HOLD` 3→6 is green today and would turn a hold into a bannerless hard fail). **R4(1):** literal pins on six unpinned guard bands — `HISTORICAL_TOLERANCE` (0.5%→1% unnoticed: the band on settled years, the 2024-signature sentinel), `LIVE_GROWTH_MIN/MAX`, `MAX_PLAUSIBLE_RESIDUAL`, `STALE_RAW_DAYS`, `MISMATCHED_RAW_DAYS` — per the `test_thresholds_are_the_measured_pair` pattern that already pins `MIN_PCT`/`MIN_ABS_DOLLARS`. Each fix must red the named mutation.
  - ✅ **R5 DONE 2026-09-08 (S147) — 827 → 832; `DECISIONS.md` 2026-09-08.** `load_committed` now returns None in exactly one case (the rev resolves and the file is not in it); every other git failure raises `BaselineUnavailable`, which logs an ERROR, writes a fault-shaped issue body and emits `flagged=fault` through the channel `refresh.yml` already keys off. **Direction policy untouched: still exit 0, always** — but the all-clear is no longer printed over neighbourhoods that were never compared. A `--geojson` outside the repo used to raise `ValueError` out of the one guard that must never stop a publish; it now reports. Falsified four ways against the real repo (bad rev → fault, HEAD → 406 compared, the pre-add rev → clean skip, outside-ROOT → fault) and four mutations red by name against the **committed** state, including the cry-wolf direction and the deletion of the issue step from `refresh.yml`. Tests run `main()` against a **real temp git checkout**, not a stubbed subprocess.
  - ✅ **`ZONING_YEAR` DONE 2026-09-08 (S147) — 832 → 843; `DECISIONS.md` 2026-09-08.** Two halves, because the constant and the thing it describes drift apart independently. **(a)** A literal pin in `tests/test_generate_status.py` — ⚠️ it is the ONE published vintage that must **not** track the roll, so the January checklist walks past three adjacent constants and must bump exactly two; the pin's sibling asserts `DATA_YEAR`/`RATE_YEAR` **do** equal `ASSESSMENT_YEAR`, which until now only the MONTHLY digest checked. **(b)** `vintage_report.check_zoning_bylaw` — there is no year field upstream, so the bylaw's identity is its **zone-code vocabulary** (Bylaw 20001 renamed every zone in 2024), measured against `load_zoning.ZONE_CATEGORY` in both directions: **95 = 95, empty both ways, live**. ⚠️ **Not a duplicate of `check_unclassified_zoning`**, which reads `frac_other` on the served file — it needs a refresh to have run, needs measurable area, and is blind to a code that DISAPPEARS. Same commit closed the vacuity beside it: `test_year_constants_flag_drift` asserted only `"DATA_YEAR" in detail`, so dropping `RATE_YEAR` from the check's tuple was green. Seven mutations red by name; digest run live end to end.
  - ✅ **`build_reference_layers` CRS path DONE 2026-09-08 (S147) — 843 → 848; `DECISIONS.md` 2026-09-08. ALL FIVE audit findings and both small leftovers are now closed.** ⚠️ **Re-measured before building and the finding was HALF STALE, which changed the target** (the `todo-can-lag-executed-work` rule earning its keep again): `WORKING_EPSG = 999999` already **failed 3 tests** — but *incidentally*, by crashing the highway path on `CRSError`, and a crash is not a measurement. **`WORKING_EPSG = 4326` was the green one, and it is the dangerous mutation**: 4326 exists, so nothing raises, and every `*_M` tolerance in the module (`MARGIN_M` 60 km, `RIVER_SIMPLIFY_M` 25 m, `HIGHWAY_SIMPLIFY_M` 30 m, `BOUNDARY_SIMPLIFY_M` 100 m) silently becomes **degrees** — a 25° simplify is ~2,800 km and the file still writes. Five tests: three on the constants (projected + metre-based; output is the lon/lat the front end reads; the working CRS is the pipeline's own 3400 — a **consistency** pin, since EPSG:3776 is also projected metres over Edmonton and left 847 green), two on the path end to end through `build()` with every fetch stubbed. ⚠️ **The stubs reproject to `WORKING_EPSG` exactly as the real fetchers do** — a stub hard-coding metres would feed `build()` honest metres under the bug. ⚠️ **The lon/lat assertion alone does NOT catch 4326** (the final `to_crs` becomes a no-op, so coordinates still come out lon/lat); what fails is the SHAPE, so the second test measures the river's area back in metres across the round trip. Six mutations red by name.
  - **Small, unranked:** ⚠️ **Do not quote the sweep's "58 of 75 green" as a defect count** — the triage in R4 puts 6 + 1 in scope; the rest are precision, warnings, self-referential `EXIT_*`, or hand-run scripts (`build_reference_layers` × 10; ⚠️ **its `WORKING_EPSG` line is superseded** — see the row above: the nonexistent CRS was not the hole, a VALID wrong one was).
- [ ] **The 42 `verify-*.js` scripts gate NOTHING, and that is how four of them stayed red for three days.**
  ⚠️ **AUDITED 2026-09-07 (S144) — `docs/FINDINGS_vacuous_guards.md` V3/V4. The item is SHARPER than it was, one count in it was wrong, and **the blocker on scheduling is now CLEARED**.** (a) **It is 42, not 65** — the directory holds 42 `verify` + 17 `shot` + 6 misc. (b) **The merge gate itself is sound**: branch protection requires `test` and it reports — the gap is that `test` contains **no browser check**, so 1 of 42 runs in CI, weekly only. (c) ✅ **FIXED 2026-09-07 — the 4 scripts that were wrong against the build that serves the public.** `verify-transit.js` and `verify-ind-permits.js` **red on a correct build** because their early-exit guards were **DATA**-gated where both builds share the GeoJSON; each now reads `FULL_BUILD` and asserts the control matches the build in **BOTH directions** (`shown === fullBuild`), so it also fails if the public build ever starts showing a full-only control. ⚠️ **The reds were the smaller half.** `click` is a JS `.click()` that ignores visibility, so after failing its row check `verify-transit.js` kept going and **passed 23 further checks against a UI the public cannot reach** — a silent false green inside a red run. (d) ✅ **DONE — 14 early exits across 10 scripts now print `PARTIAL — ran N checks, then stopped: <reason>`, and those 10 print `COMPLETE — ran N checks` otherwise.** A consumer keys on **PARTIAL**; the 32 scripts with no early exit print neither, so absence of PARTIAL is the passing condition. Four scripts counted only failures and needed a `ran` counter. (e) ~~`check_temporal_archive_year.py` is in **no workflow** at all~~ — ✅ **CLOSED 2026-09-07 (S146): the finding was FALSE.** The guard has run monthly since PR #258 (2026-08-27), wired by membership in `vintage_report.CHECKS` (pinned by `tests/test_vintage_report.py:340`) rather than by a workflow line, so its **filename appears in no `.yml`** and the audit's filename grep reported a gap that was not there. **Confirmed in the run log, not the caller:** the 2026-09-01 scheduled `vintage-digest.yml` run (`33539478726`, success) filed `✅ Archived years measure right — 1 archived year(s) measure as filed (2026)`. ⚠️ The method that produced it is corrected in `docs/FABLE_AUDIT_vacuous_guards.md` T2 — **a guard reachable only through a caller is invisible to a filename grep.** ⚠️ The guard is still green on a **population of 1**; it gains a year at each roll-forward.
  ⚠️ **MEASURED, both builds, 2026-09-07 — the sweep nothing had ever run.** All **20 runs exit 0**: `/full/` is **10 of 10 COMPLETE**; public is 6 COMPLETE + 4 correctly PARTIAL (`verify-bike` 3, `verify-transport-cost` 5, `verify-transit` 4, `verify-ind-permits` 2). **Both new build gates were falsified** — patching the built public page to leak the transit row and the industrial button reds each script **by name**. **So (c)'s "fix the gating BEFORE scheduling anything" no longer blocks: the estate is honest against both builds.** What remains is the ORIGINAL question below — what belongs on a schedule — which changes CI behaviour and is therefore a proposal, not a task.
  - ⚠️ **PROPOSED 2026-09-08 (S146), AWAITING PETER'S YES/NO — nothing built. Three tiers; only Tier 1 is unambiguous.** ⚠️ **The question was reframed by a fact the audit's own table contains but does not draw out: `deploy.yml` PUBLISHES TO THE LIVE SITE on every `web/**` master push, and has NO browser check.** `refresh.yml` places `verify-smoke.js` immediately before `upload-pages-artifact` on purpose (*"a red gate here leaves the live site serving the PREVIOUS good data"*); `deploy.yml` has that same build→upload seam **empty**. So the **DATA** path is gated before publish and the **CODE** path — the one that actually changes `web/index.html`, i.e. the rendering — is not. That is an **asymmetry between two existing workflows, not a new policy**, which is what makes Tier 1 cheap to justify.
    - ✅ **TIER 1 SHIPPED 2026-09-08 (S147) — Peter's yes.** `verify-smoke.js` runs on both builds in `deploy.yml` between the build and the upload; blocks the PUBLISH, never the merge. Measured locally at 48s for the pair, and **the first live run came in at 91s** (`npm ci` + playwright 20s, not the 32s harvested from `refresh.yml`; the two smoke runs 49s) — taking the workflow ~25s → **91s**, better than the ~107s proposed; the stale *"Seconds, not the 30-minute pipeline"* header claim was corrected in the same commit. Pinned by `test_the_smoke_gate_sits_between_the_build_and_the_upload[deploy.yml]` and `test_the_smoke_gate_covers_both_builds[deploy.yml]`, both **falsified against the committed state** (moved-after-upload, `/full/` run dropped, step deleted — each reds the right pin; unmutated green). `DECISIONS.md` 2026-09-08. ⚠️ **TIERS 2 AND 3 REMAIN OPEN and this does NOT close the item** — smoke is invariants-only and would probably not have caught the four S140 reds. Original proposal:
    - **~~TIER 1~~ — RECOMMENDED: `verify-smoke.js` on BOTH builds in `deploy.yml`, between build and upload.** Same instrument already trusted weekly, same slot, same rationale. **Measured cost in CI: 4s `setup-node` + 32s `npm ci` + `playwright install` + 46s run = ~82s**, taking `deploy.yml` from **25s → ~107s** (durations harvested from real runs, not estimated). Blocks the **publish**, never the merge — a red leaves the last good site live. ⚠️ `deploy.yml` and `refresh.yml` **already share the `refresh-map-data` concurrency group**, so they serialise and this adds no box contention.
    - **TIER 2 — defensible, Peter's call: the same two invocations in `tests.yml`, gated to PRs touching `web/**`.** Catches it before merge rather than before publish. ~82s on a ~50s gate, and it is the tier that **can block a merge on browser flake**.
    - **TIER 3 — a scheduled NON-BLOCKING sweep of the rest, reported as an issue (the `vintage-digest.yml` pattern). NOT YET — do not scope it from this item.** The locked rule is that only **invariants-only** scripts are safe unattended (`verify-temporal.js` cried wolf on 2026-08-01 by pinning a live year). ⚠️ **A screen of all 42 for pinned data literals returned 37 "clean", but that screen is COARSE and must not be quoted as a classification** — *"no dollar literal"* is far weaker than *"invariants-only"*, and the scripts were **not read** to confirm. Committing to Tier 3 means doing that classification first; it is a session's work.
    - ⚠️ **HONEST LIMIT ON TIER 1: it would probably NOT have caught the four S140 reds.** Smoke is invariants-only by design — it catches shape/garbage regressions, not the control-state defects those four scripts name. **Tier 1 closes the publish hole; it does not reproduce the S140 catch. Tier 3 is what would**, and Tier 3 is the one that cannot yet be responsibly scoped. Do not let Tier 1 shipping be read as this item closing.
    - Two bounds on what ANY gate here is worth, passed through unchanged from the audit: **`enforce_admins: false`** (an admin merge bypasses the required check) and **`strict: false`** (a PR need not be current with master).
  - **Original framing, unchanged:** `refresh.yml` runs `verify-smoke.js` only; `tests.yml` runs none. The suite is the front end's only test coverage and it runs when someone remembers. ⚠️ **The S141 evidence for why this matters: one of the four reds was a real label-occlusion bug that the guard caught at authoring time and nobody saw for three days** — and the other three had decayed into cry-wolf, which is the state that trains people to ignore the suite. Decide what belongs on a schedule. ⚠️ **Not "run all 65 in CI" by default** — they need a served build, they take ~40 min serially on this box, and `verify-smoke.js`'s header argues at length that a flaky gate blocking the weekly publish is worse than the gap it closes. Candidates: the non-pointer, invariant-only scripts on the merge gate; a slower full sweep on a schedule with the result reported, not blocking.

- [ ] **Two carry-overs from the S140 architecture audit, neither started.**
  - **Propose (don't start) the manifest change** (findings §6, data contract): serve `WINDOWS`, `CELLS` and the unit-cost values so the page stops carrying copies and `test_window_labels.py` / `verify-staleness-banner.js` stop regexing the source.
  - **The read-only JS checker in `tests.yml`** is allowed (`DECISIONS.md` 2026-09-05) but unscheduled. ⚠️ **S141 sharpened what it is FOR:** with the module flip withdrawn, parsing the extracted `<script>` block as ESM (`node --check`) is now the **only** thing that would catch a duplicate top-level declaration — 377 names, currently all distinct. It is a ~5-line step, needs no `node_modules`, and writes nothing to `_site/`.

## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **Mobile coverage ceiling — RE-PROBED 2026-09-17 (S168).** Public ceiling is **53.5%** (Money unfolded + peek), not the 52.3% on record — and not for the predicted reason: public Services is roads-only at 38.8%, so the full-build 53.1% state stayed unreachable. ⚠️ The old figure was an understatement when written, and `Development UNFOLDED 52.7%` is internally impossible. — MEASURED 2026-09-17 · `docs/TODO_archive.md`

- [x] **Cold-load cost on the wire — MEASURED 2026-09-17 (S168), and the answer changes nothing about payload.** A cold visit is **2.05 MiB gzipped**, critical path **948 KB**; libraries **62.5%** of it, so per `VIZ_STACK.md` §5 axis 4 there is no cheap lever. ⚠️ The item's own premise was stale (wire numbers existed in `PERFORMANCE.md` since 2026-08-10) and three side-findings came out of it. — MEASURED 2026-09-17 · `docs/TODO_archive.md`

- [x] **Manifest staleness guard — BUILT 2026-09-17 (S167).** Two digest checks: `check_budget_context` + `check_mill_rate_values`. — BUILT 2026-09-17 · `docs/TODO_archive.md`

- [x] **Residential-only lens — SUPERSEDED, and the built version was REMOVED.** — SHIPPED 2026-07-26 · `docs/TODO_archive.md`
- [x] **Colour scale for revenue/value — SUPERSEDED 2026-09-16.** — 2026-09-16 · `docs/TODO_archive.md`

- [x] **`$50k` revenue clamp — DECIDED AND GUARDED 2026-09-16 (S162).** — DECIDED 2026-09-16 · `docs/TODO_archive.md`
- [x] **Services lens — road supply — SHIPPED (verified 2026-09-16: `road_m_per_acre` is served on all 406 hoods, the roads ground layer and Services view are** — SHIPPED 2026-09-16 · `docs/TODO_archive.md`

- [x] **Nothing verifies the Services panel** — CLOSED 2026-09-15 · `docs/TODO_archive.md`
- [x] **Published numbers with no loud check — audit EXECUTED 2026-09-15 (S160, Fable 5.1).** — EXECUTED 2026-09-15 · `docs/TODO_archive.md`
- [x] **L1 + L3 of the three unguarded PUBLIC literals — CLOSED 2026-09-16 (S160), PR #406.** — CLOSED 2026-09-16 · `docs/TODO_archive.md`
- [x] **Retrieval logging — EXECUTED 2026-09-16 (S160).** — EXECUTED 2026-09-16 · `docs/TODO_archive.md`
- [x] **Doc-apparatus audit — EXECUTED 2026-09-16: Session A (S161) `_PREMISES.md`, Session B (S162) `_DISPOSITIONS.md`; recs 1/2/6 wait on the log (~2026-09-** — EXECUTED 2026-09-16 · `docs/TODO_archive.md`

- **F1 — the Services panel follows the colour-driving service. BUILT 2026-09-15 (S159, PR #399, merged).** Closed the defect where one panel served all ten layers. Follows `state.svcDriver`, not the checkbox set (Peter's call — "the picker" was ambiguous for a multi-select control); shows the driver's value + rank, then that service family's cost bars; storm/fire/water state their scope instead of showing an empty group. Two defects it exposed: the operating-basis note said "snow clearing" under a bus network, and `verify-services-public.js` asserted a clause naming rows no longer on screen. `DECISIONS.md` 2026-09-15, `COPY_DECISIONS.md` F1.
- **`verify-services-panel.js` — the T1 verification gap. CLOSED 2026-09-15 (S159, PR #398 merged RED, then #399 green).** Written before the fix so it could be falsified against the broken build: 7 checks red on arrival, all green after F1. 10 distinct panel renderings across 10 layers, 3 across 3 public.
- **T2 `#devwindow` → panel — CLOSED 2026-09-15 (S159): wiring SOUND by decision, not a defect.** `DECISIONS.md` 2026-09-14 makes the Development history panel the *whole* per-year series with the windows as aggregates over it; `devHistoryFor` reads no window. The one copy line that ignores the picker (`… in the last 5 years`) is `COPY_DECISIONS.md` **F4**. `docs/FINDINGS_controls_state_space.md` T2.

- **Development gets a per-year new-supply history — SHIPPED 2026-09-14 (S156, PR #389, merged).** `export_dev_history` → `web/data/dev_history.json` (363 hoods × 17 years, 49 kB, **public**); tooltip sparkline + pinned panel, following the units/permits/industrial picker. ⚠️ **Columns, zero-based — NOT the temporal line and NOT `temporalGeom`** (annual flow of counts vs continuous stock; 61% of hood-years are zero, and temporalGeom's non-zero baseline is a lie for counts). That choice **retired the minimum-non-zero-year gate the feature was specced with**. Rationale `docs/DECISIONS.md` 2026-09-14; design `docs/SPEC_development.md` "Lens A history".

- [x] **`tools/todo_archive.py` swallowed trailing non-item text — FIXED 2026-09-10 (S154).** — 2026-09-10 · `docs/TODO_archive.md`

- **The pointer-style index files drifted off their own contracts** — CLOSED 2026-09-09 (S152). Peter chose **bless, not trim**: `DECISIONS.md`'s header now describes a decision *log* and the mandatory invariant is the **pointer**, not the length — **all 273 rows carry a doc pointer** (was 23 short), checked by `check_doc_citations.py`. Trim rejected on measurement (the target doc is richer than the row, so a trim buys tokens not recoverability); `AUDIT_LEDGER.md`'s mirrored clause retired too. ⚠️ **§3's 1,295-facts/16-unique numbers predate the splitter fix — re-derive before any future trim.**
- **`_classify` fail-open-to-`local`: decided and changed** — DONE 2026-09-09 (S151). An unmappable `functional_class_code` now goes to its own `unknown` group: carried in `road_m_unknown`, out of `road_m_total`, off the web layer, reported at every stage. ⚠️ **`local` was never a neutral holding pen — it is the CHARGED side of the metric.** The manual `CLASS_GROUP` entry is unchanged (every option ended in one); the pipeline just stops guessing during the wait. Under-billing is the accepted cost. Served schema unmoved (67 columns); real feed verified unchanged at 3,654.1 km. ⚠️ The display half would have gone SILENT — a NaN `t` is excluded by both selections in `export_roads_web` without a word. `docs/DECISIONS.md` 2026-09-09.
- **Monthly-digest check for `functional_class_code` vocabulary drift** — DONE 2026-09-09 (S151). `vintage_report.check_road_classes`, both directions, on the Road + City population `_classify` actually sees; a null class is reported separately from a new code because the fix differs; empty vocabulary → UNKNOWN, checked BEFORE the null count. Live: OK, 15 of 15. ⚠️ **The measured count was wrong in three places** — "closed at 15" counted the `null` group; it is 15 real codes now, 14 at the 2026-07-01 survey. 10 mutations red by name. `docs/DECISIONS.md` 2026-09-09, `docs/RUNBOOK.md` §0, `data/DATA.md` §6.

- **Road-cost follow-up brief SENT** — 2026-09-10 (S154). `/home/opc/road_cost_sendback_brief.md` (outside the repo) went out; send date not recorded. **Reply pending — the Q1 rewrite stays held until Q1(a) (centreline vs lane-km) answers.** · `docs/TODO_archive.md`
- [x] **DECIDED 2026-09-08 — STATE THE UNIT, DO NOT CONVERT: `roadway_ops` stays $9.32/m/yr and the basis publishes as a FLOOR** — DECIDED 2026-09-08 · `docs/TODO_archive.md`



- [x] **DONE 2026-09-08 — the road-figure CONSOLIDATION brief RAN (S149, Fable 5.1): `docs/FINDINGS_road_figures_consolidation.md`; L0 SOUND · L1 CONDITIONAL ** — DONE 2026-09-08 · `docs/TODO_archive.md`



- [x] **DONE 2026-09-05 — Peter chose RETIRE, and it shipped the same day.** — DONE 2026-09-05 · `docs/TODO_archive.md`
- [x] **DONE 2026-09-06 — the wrong-base sentence is DELETED, not corrected** — DONE 2026-09-06 · `docs/TODO_archive.md`
- [x] **DONE 2026-09-07 — recorded as deliberate; the panel is UNCHANGED.** — DONE 2026-09-07 · `docs/TODO_archive.md`
- [x] **DONE 2026-09-06 — the $1,285 split treatment is closed by RE-SCOPING** — DONE 2026-09-06 · `docs/TODO_archive.md`
- [x] **DONE 2026-09-06 — RE-SCOPED. `roadway_ops` $4.635 → $9.32/m/yr, maintenance half $1,285 → $5,970/km (Peter's call).** — DONE 2026-09-06 · `docs/TODO_archive.md`
- [x] **DONE 2026-09-07 — `check_cost_copy.py` now searches READER-VISIBLE PROSE, not the raw file** — DONE 2026-09-07 · `docs/TODO_archive.md`



- [x] **Four `verify-*.js` scripts were RED on master since 2026-09-02.** — 2026-09-02 · `docs/TODO_archive.md`



- [x] **Front-end fix-in-place PR — the two defects the S140 architecture audit measured, fixed without a split.** — DONE 2026-09-05 · `docs/TODO_archive.md`



- [x] **CLOSED 2026-09-05 — STAGE 2 of the `web/index.html` split: WON'T DO. The file stays one file (Peter, S140, on the architecture brief's verdict); re-op** — CLOSED 2026-09-05 · `docs/TODO_archive.md`



- [x] **CLOSED 2026-09-03 — "why is value leaving the lot-acre denominator?" It ISN'T, and the trend that opened this item was ONE STEP WITH AN INVENTED MIDPOINT.** The premise was `ineligible_points` 56→58→60 and `ineligible_value_frac` 0.00517→0.00575→0.00633 "monotonically upward on every independent data change, no reversal". ⚠️ **The middle observation was never observed** — it matched no CI run, and all five of its anchors were exact midpoints of the rows either side; it sat as a pinned row in `OBSERVED_IN_CI` until now. The 08-01→08-05 window holds **six** runs and only **two** distinct data states, the step falling between the 05:17 and 11:19 runs of 08-03. ⚠️ **And it reverted on 08-10** and has been flat for 8 independent pulls since (~0.3%); `ineligible_value_frac` sits at **49.4% of its band**, not the 83% two handoffs headlined. ⚠️ **The 83%/85 readings came from a stale local `data/raw/`** (a 2026-07-06 property-info file beside a 2026-08-09 roll) — CI read 58 the same day — and that phantom had already widened a band 84→127.5 in the guard's own *dangerous* direction. Re-pinned to 29–87 on the real reading; `check_value_anchors.py` now prints each raw file's vintage, warns on stale/mismatched pulls, and **refuses `--write-baseline`** on them; a new test pins every band's *centre* to a reading CI actually logged (falsified against the phantom band first). — 2026-09-03 · `docs/TODO_archive.md`

- [x] **CLOSED 2026-09-02 — the Services lens returns to the PUBLIC build, roads only (supply + road cost on both bases); `cost_roads_life_per_acre` published; a copy guard now ties quoted rates to the unit-cost JSON.** (First exercise of the staged-return rule. Ratio and Uses still out, still return one per release.) — CLOSED 2026-09-02 · `docs/SPEC_services.md`

- [x] **CLOSED 2026-09-01 — the 50 m Glass grid is now a THIRD Detail button with 100 m as the default; the scope correction is resolved.** (Both files ship lazily; Infill pins the default; the needle guard anchors on the fine file. Verify falsification exposed a vacuous default check.) — CLOSED 2026-09-01 · `docs/TODO_archive.md`

- [x] **CLOSED 2026-08-30 — the 15 hardcoded activity-window labels now read from one constant, and drift fails the build.** (Audit F4; the `status.json` route was rejected on measurement.) — CLOSED 2026-08-30 · `docs/TODO_archive.md`

- [x] **CLOSED 2026-08-29 — the three verify failures are resolved, and one of them was NEVER a master failure.** — CLOSED 2026-08-29 · `docs/TODO_archive.md`



- [x] **✅ DONE 2026-08-28 — the archive can no longer freeze the wrong year.** — DONE 2026-08-28 · `docs/TODO_archive.md`
- [x] **✅ DONE 2026-08-28 — the merge gate exists.** — DONE 2026-08-28 · `docs/TODO_archive.md`
- [x] **✅ DONE 2026-08-27 — the temporal archive's mislabelled 2025 entry is deleted, and 2025 is accepted as unrecoverable.** — DONE 2026-08-27 · `docs/TODO_archive.md`

- **Wire `check_temporal_archive_year.py` into the monthly vintage digest** — DONE 2026-08-27 (PR #258). No workflow change needed: the digest already runs `vintage_report.py`, so it is a check function + a `CHECKS` entry. Also fixed a FALSE ALARM found while testing — `check_assessment_roll` bypassed the stale-metadata downgrade and would have said "roll has moved to 2025" every month from 2026-09-01. `docs/RUNBOOK.md` §0, `docs/TODO_archive.md`.


- [x] **▶▶ FIXED 2026-08-25 — THE MEASURED ROLL-YEAR GUARD EXISTED BUT RAN NOWHERE — `check_roll_year_against_fir.py` was not wired into any workflow; exit 3 now HOLDS** — 2026-08-25 · `docs/TODO_archive.md`
- [x] **▶▶▶ FIXED 2026-08-25 — THE LIVE ROLL IS THE 2026 ROLL AND WE BILLED IT AT 2025 MILL RATES — the year-alignment guard cannot see it, because it reads a** — 2026-08-25 · `docs/TODO_archive.md`
- [x] **▶▶ FIXED 2026-08-25 — THE MAP'S LEVIED/EXEMPT UNCERTAINTY BAND WAS TOO NARROW — `PS` ("Parks and Services") is categorised `never`, not `inst`, so $88** — 2026-08-25 · `docs/TODO_archive.md`



- [x] **`gross_area` MISSING and `gross_area` ZERO were the same number — `far` now emits `null`, not 0, where no floor area is recorded.** — DONE 2026-08-22 · `docs/TODO_archive.md`
- [x] **The Services lens has no hood panel — BUILT 2026-08-10. Revenue vs each service cost, grouped by basis, NO total (two no-sum rules).** — DONE 2026-08-10 · `docs/TODO_archive.md`
- [x] **Sweep the doc-to-doc citations — DONE 2026-08-09 (S104). ONE REAL DEFECT, and it was a locked decision built on a display artifact.** — DONE 2026-08-09 · `docs/TODO_archive.md`



- [x] **Doc-citation sweep of `src/`, `scripts/`, `tools/` — DONE 2026-08-09, no wrong number reached shipped data.** 216 sites / 51 files, ~20 with a falsifiable number, every one re-derived from `data/raw/`. Three comment-level defects: a **line-number citation that drifted** (`audit_exempt_institutional.py`'s "DATA.md line ~308" — right on 2026-07-09, now ~240 lines off), a **unit mislabel** (`load_temporal.py`'s "19 rows" is 19 *accounts*, 16 rows), and ⚠️ **S102's own follow-up note retracted** — it said `SPEC_temporal.md` §2 "was never updated", but `git log -S` shows the §2 banner and the comment flagging it landed in the SAME commit (`7e065ef`). — 2026-08-09 · `docs/TODO_archive.md`

- [x] **`WEST MEADOWLARK PARK`'s revenue MORE THAN DOUBLED in one auto-refresh — EXPLAINED 2026-08-07: a RENUMBERING GAP CLOSING, so the +130% was the CORRECTION, not the defect.** Misericordia was continuously assessed 2012–2025 and merely absent from the published current roll during a renumber; the map had been UNDERSTATING the hood by ~$250M assessed / ~$6M/yr. ⚠️ **Two earlier answers are WRONG and are recorded in commits** — *"one new $247.8M parcel arrived"* (true but shallow) and *"is a hospital supposed to be taxable?"* (the wrong question; it always was). Read the archive entry before citing either. — 2026-08-07 · `docs/TODO_archive.md`



- [x] **Tighten the cardinality-guard bands — DONE 2026-08-05, and the item's premise was half wrong, so only FOUR of the six moved.** The variance data turned out to exist in a place nobody had looked: **the guard logs every anchor value in CI**, harvested from the refresh runs' job logs. ⚠️ **Five runs but only THREE independent data changes** — the 2026-08-02 and 08-05 runs committed `status.json` only, so their readings re-measure unchanged input. **Four anchors were effectively frozen** (`dup_parcel_points` constant at 33, `lot_needle_ratio` 0.00%, `dedupe_effect_pct` 0.01%, `dup_parcel_value_frac` 0.11%) and were tightened **2×**, to ±25%. ⚠️ **The other two are not noisy, they are TRENDING** — `ineligible_points` 56→58→60 and `ineligible_value_frac` 0.00517→0.00575→0.00633, monotonic, in the guard's own **dangerous** direction — and were **left wide on purpose**: tightening them would red the weekly publish on the next real data change and read as a false alarm. ⚠️ **The item's prescribed mechanism could not express this** — `--write-baseline --tolerance` applies ONE global tolerance to every anchor, so the bands are now hand-set per anchor and that flag would flatten them; the baseline says so in `_bands_are_per_anchor`. **Not tightened further than ±25% because no observation across a January year-roll exists yet**, which is the event the guard was built for. Three new tests pin all of it, and the tightening test was **falsified against the old baseline first**. The drift became its own open item. — 2026-08-05 · `docs/TODO_archive.md`

- [x] **Publish the roads-maintenance correction — DONE 2026-08-05, verified against PRODUCTION.** `refresh.yml` dispatched by hand per RUNBOOK §3d (run `30966755798`, success). The live pod now prints roads at **$103M · 2.7%** with **no asterisk**, was $50.985M · 1.33% with one; `transit:roads` reads **4.6×**. `verify-about.js` against the public root: **ALL CHECKS PASSED** — all four shares recomputed independently from the published dollars, pod still fits at 900/800/768/720px. ⚠️ **The refresh committed `status.json` ONLY** (`8ca6e8f`), i.e. no source data changed on this run — which is what made it a clean publish of the manifest edit and nothing else. — 2026-08-05 · `docs/TODO_archive.md`

- [x] **Source the derived $14.135M roads-maintenance figure — CLOSED 2026-08-04, and the derived figure was ~5× TOO LOW, live on a public page.** Replaced with **$65,671,000**, the Open Budget portal's `Roadway Maintenance` program (FY2017). ⚠️ **The item said "the one soft number in that table"; it was a wrong one.** The derived value was `$1,285/km × ~11,000 km` — a narrow unit rate multiplied across the whole network; the published program implies **~$5,900/km**. Roads moves **1.33% → 2.67%** of the operating budget and transit:roads **9.2× → 4.6×**. ⚠️ **The error was in OUR derivation, not the Taproot source** — that source's *totals* reconcile: roads snow $36.85M + path snow $30.15M = **99.2%** of the portal's published `Snow and Ice Control` program, and **that contrast is what exposed the maintenance line**. **2017 is the only year Edmonton ever published a roads-only maintenance program** (re-cut in 2018 into a line that also covers sidewalks and pathways — using it would double-count this table's own rows — and again in 2026), so Peter chose clean scope over matching vintage. New **`DATA.md` §17** documents the portal, including its **two rename eras** and a **+1.31% portal-vs-PDF** gap. ⚠️ **Not yet on the live site** — budget figures ship only when `refresh.yml` reruns `generate_status.py`; see the open publish item. — 2026-08-04 · `docs/TODO_archive.md`

- [x] **Mobile chrome — the bottom-sheet question — CLOSED 2026-08-04, NO code change: the control column stays a stack.** The quick pass's last open piece was a *decision*, not a build item (steps 1-2 shipped `0089eba`; step 3 closed 2026-07-31 as not reproducible). ⚠️ **Re-measured before deciding, and the basis had moved.** The union method reproduced the default to the decimal (**27.9%**), but **Money unfolded is 47.9%, not the recorded 54.3%** — `#moneymode` left the Options panel on **2026-08-02, one day after that measurement**. ⚠️ **The ">half the screen" claim was attached to the wrong state**: the only >50% states are **Services 53.1%** and **Development 52.7%**, neither ever measured — the 08-01 pass took one view and generalised. ⚠️ **The public build cannot reach the worst state**: Services and Ratio are full-only since 2026-07-28, so **public `#views` is TWO buttons (Money · Development)**, correcting a doc line that claimed four. Worst public state is **52.3%** (Development unfolded + peek), rendered clean. Peter's call: the >50% states are transient and user-initiated, a bottom sheet is a **shared desktop+mobile DOM** refactor, and the default a phone user meets is 27.9% vs desktop 20.3%. ⚠️ **`#views` position loses its vehicle** — it was parked pending this fork. **Tenth time a stated basis did not survive re-measurement; the first where that CLOSED the item.** — 2026-08-04 · `docs/TODO_archive.md`

- [x] **The four Stage 2 cost columns shipped and `expected_columns.json` is re-pinned 62 → 66 — DONE 2026-08-04, on a manually dispatched refresh.** The weekly cron was 6 days out, so `refresh.yml` was dispatched by hand (run `30909649645`, success, commit `024ecc6`). All four `cost_*_ops_per_acre` columns are present on all **406** features and the composite sums exactly (`88.92 + 13820.65 + 129.59 = 14039.16`). ⚠️ **The pre-repin guard behaved exactly as the item predicted** — warned on all four as NEW, exit 0 — and that is also the path it took **in CI**. ⚠️ **The served-column guard has now RUN IN CI for the first time** (step *"Check served columns (guard after regenerating)"*, success), closing an item carried S89 → S91. Re-pin diff is a pure 4-line addition; the re-run is clean at 66. `status.json` carries `budget_context`, so both S90 features' data is live. Verified against **production**: `verify-transport-cost.js` **6 → 41 passed / 0 failed** against `/full/` (including the load-bearing two-bases check, roads ops **$89** vs svc **$7,527**), `verify-about.js` **ALL CHECKS PASSED** against the public root (all four shares recomputed independently from dollars, pod fits at 720px). — 2026-08-04 · `docs/TODO_archive.md`

- [x] **`verify-peek.js` was 71% of the suite's wall time — FIXED 2026-08-04, 437s → 94s, 27/27 still green.** ⚠️ **The item named the wrong loop.** `findTappableHoods` (which it blamed) is 46s of 408s — it exits at `n` hoods and never nears its worst case. The cost was the **empty-map-pixel scan: 346s, 85%**, blind-sweeping ~2,470 picks. ⚠️ **A pick costs ~137ms and neither `radius` nor `deviceScaleFactor` changes it** — deck re-renders the whole picking buffer on the CPU per call, so the only lever is *fewer picks*; the first burst also carries a one-off ~20s shader warm-up, which is what `targets`' residual 46s is (left alone, it is at the floor). ⚠️ **Its "coarsen the grid" lever is a measured trap**: step 25 still costs 30s and **step 40 finds nothing** and fails the check — only 17 of 4,400 grid points are clear. Fixed with its *other* lever: `metric-extrusion` is the only pickable layer, so the pixel is derived from projected geometry (9,236 vertices, 14ms) and confirmed with **one** pick instead of 2,474, landing on the same pixel. — 2026-08-04 · `docs/TODO_archive.md`

- [x] **The verify runner's own default was manufacturing quirk (mmm) — FIXED 2026-08-03.** `verify.js` hardcoded `--jobs 3`, but a **single** verify script draws **~275% CPU** on this 4-core box (headless Chromium on SwiftShader — software rasterisation and software deck.gl picking), so 3-up demanded ~8 cores from 4: `cpu_sum` 385–400%, load 8.2. Measured on three scripts: jobs=3 ~509s **2 failed**, jobs=2 ~505s **1 failed**, jobs=1 615s **all green** — parallelism was buying ~17% wall time for a suite whose red results had to be re-run alone to mean anything (three scripts went red on PR #148, which touched none of them). Default now `floor(cores / 3)` → 1 here, 2 on an 8-core; `--jobs N` still forces. ⚠️ `verify-temporal`'s hand-set 4000ms click timeout deliberately left alone — it passes at the new default, and raising it would treat the symptom of a fixed cause. Not a CI change (`refresh.yml` runs `verify-smoke.js` directly). — 2026-08-03 · `docs/DECISIONS.md`

- [x] **A dropped SERVICES column was invisible to every guard — FIXED 2026-08-03.** Two halves, because the item's own prescribed fix could not catch the failure it named: `verify-smoke.js` gains `B7` (all-or-nothing presence, columns derived from the **union** of `SERVICES[].plane.col` and `RATIO_DENOMS[].col` — Roads is a ground layer, so `road_m_per_acre` lives only in the latter) and `B8` (a services row is offered exactly when its column is present). ⚠️ **B7 provably CANNOT catch a full drop** — falsification F2 shows it passing green — because nothing derived from the served file alone can tell "dropped" from "not shipped yet". That needs memory, so `scripts/check_served_columns.py` + `data/expected_columns.json` (62 columns) hold a committed baseline and fail the refresh on a removal; a new column only warns. — 2026-08-03 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **A data refresh published with no check on the RENDER — FIXED 2026-08-02.** `verify-smoke.js` gates `refresh.yml` before `upload-pages-artifact`, so a red check leaves the live site on the previous good render. Invariant-only by design (a pinned value would cry wolf weekly — #139). ⚠️ The item's premise was wrong: `refresh.yml` **deploys itself**, so the gap was an *unchecked* deploy, not a missing one. Falsification found the check's own hole (a dropped column is *omitted*, not printed as NaN → `B6`); the inverse test caught it crying wolf on absent mill rates. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **`styles.css` had no cache-busting, so a CSS-only deploy could render stale — FIXED 2026-08-02.** `scripts/build_site.py` stamps `styles.css?v=<8 hex of the file's content hash>` into both builds; content hash not commit sha, so an unrelated deploy keeps the cached copy. Drift fails the build loudly. ⚠️ Scope is stale-CSS-under-fresh-HTML only — a stale `index.html` carries the old query with it, so RUNBOOK §3c keeps its private-window step. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **The pinned panel painted over the title blurb in five states — FIXED 2026-08-02.** `#temporal`'s `top: 210px` constant replaced by `syncTemporalPos`, which measures `#title` and `#botleft`; where clearing the blurb leaves no room the **panel** scrolls, not the blurb (`#title` is `.panel`, so pointer-events:none — a capped blurb could not be scrolled to). Two defects found by measuring the fix: content-box `max-height` overshot `#botleft` by 11px, and an absolute close button scrolled away. `verify-temporal.js` 43 → 67 checks, sweeping six states. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **`verify-temporal.js` red since the 2026-08-01 refresh — DIAGNOSED AND FIXED 2026-08-02.** The data moved, the splice did not: 839 changed cells, **every one in 2025**, 2012–2023 bit-identical across all 406 hoods. The defect was in the script, which pinned the live year the pipeline guard deliberately refuses to band. Live-year assertions now derived from the loaded series; historical anchors stay pinned. 42 → 43 checks, green. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **UI BUG: the Display popover and the Data & Methods pod overlap. FIXED 2026-08-02** — 2026-08-02 · `docs/TODO_archive.md`



- [x] **▶ REVENUE-LENS READOUT — phase 2 of 2: the UI. DONE 2026-08-01 (both halves).** — DONE 2026-08-01 · `docs/TODO_archive.md`



- [x] **UI BUG: the hover tooltip `div.tip` rendered on TOUCH, 127px off the right edge. CONFIRMED ON DEVICE and FIXED 2026-07-31.** — 2026-07-31 · `docs/TODO_archive.md`
- [x] **REVENUE-LENS READOUT phase 1 (pipeline) — BUILT 2026-08-01.** `src/revenue_by_zone.py` + 11 tests; ships `total_revenue`, `revenue_share_city` and 10 `rev_frac_*` columns. Zoning source reversed on measurement: the polygons, not `dkk9-cj3x`'s per-property field (null for 42% of Downtown's revenue). Phase 2 (the UI) closed later the same day. — 2026-08-01 · `docs/DECISIONS.md`, `data/DATA.md`
- [x] **`#hoodmode-btn` CONFIRMS instead of toggling off when the panel was opened by a peek card — RULED and BUILT 2026-08-01.** Peter: *"change button name and first press to mean yes, keep it open."* Three label states now (`popup` / `panel` / `panel ✓`); the tick marks the only one that earns one-tap pinning. — 2026-08-01 · `docs/DECISIONS.md`
- [x] **Should the change lens's card carry its `% of city base` endpoints? RULED 2026-08-01: LEAVE IT.** Peter's call; the panel is one tap away and special-casing would put wrapper content in the card for one view only. — 2026-08-01 · `docs/SPEC_temporal.md` §2
- [x] **REGRESSION from that fix: suppressing `.tip` left every lens with a ONE-LINE readout on touch. Reported by Peter and FIXED 2026-08-01** — the peek card now borrows `viewTooltip(info, false)`, so it carries the lens's full rows; Money's readout also split so revenue facts no longer print under the Value map. — 2026-08-01 · `docs/DECISIONS.md`, `docs/MOBILE_USABILITY.md` §2b



- [x] **PROMOTED the temporal + change lenses to the PUBLIC build — DONE 2026-07-31 (PR #121, merged `828bb5a`, deploy green, LIVE).** — DONE 2026-07-31 · `docs/TODO_archive.md`
- [x] **ALL THREE PRE-EXISTING VERIFY FAILURES ARE FIXED (2026-07-31). THE SUITE IS GREEN: 26 scripts, 0 failures.** — 2026-07-31 · `docs/TODO_archive.md`
- [x] **TOUCH: the history panel now takes TWO gestures (tap → peek card → tap the card), and the panel's × is doubled to 44px — DONE 2026-07-31.** Peter: *"the panel on mobile [should be] harder to activate"* + *"the x on the panel needs to be twice as big"*. Gated on `(hover: none)`, all touch paths idempotent (a tap can fire the handler twice). ⚠️ **Two claims here were REVISED the same day:** the gate is armed on EVERY tap (only `#hoodmode-btn` disarms it — committing the card was itself what set panel mode), and *"on touch the tooltip node never exists"* was true of deck's built-in `.deck-tooltip` but NOT of the app's own `.tip`, which did render on a finger. `verify-peek.js`, 25 checks — **the first script in the suite that drives a real pointer at the map.** — `docs/DECISIONS.md` 2026-07-31, `docs/SPEC_temporal.md` §2



- [x] **ASSESSMENT-OVER-TIME GRAPH PER NEIGHBOURHOOD** — COMPLETE 2026-07-29 · `docs/TODO_archive.md`
- [x] **TEMPORAL, ROUND 2 — "HOW MUCH HAS EACH HOOD CHANGED?" AS A MAP METRIC, WITH SELECTABLE WINDOWS (Peter, 2026-07-30).** — BUILT 2026-07-30 · `docs/TODO_archive.md`
- [x] **UI: the pinned panel and the hover popup must not both be up — add an explicit MODE toggle** — DONE 2026-07-30 · `docs/TODO_archive.md`
- [x] **NEEDS A PHONE, NOT A BOX: confirm the double-tap-zoom fix (PR #107).** — 2026-07-27 · `docs/TODO_archive.md`
- [x] **LABEL SWEEP IS BLIND TO DOM CHROME.** — DONE 2026-07-27 · `docs/TODO_archive.md`
- [x] **PUBLIC BUILD SHAPE** — LOCKED 2026-07-28 · `docs/TODO_archive.md`
- [x] **RIVER GEOMETRY IS UNTRIMMED AND UNCHECKED (audited 2026-07-27).** — CLOSED 2026-07-27 · `docs/TODO_archive.md`
- [x] **FLAKY TEST: `verify-uses-prisms.js` "money: control hidden again, state kept" (found 2026-07-27).** — CLOSED 2026-07-28 · `docs/TODO_archive.md`
- [x] **SMALL OPEN UI DECISIONS (2026-07-25).** — CLOSED 2026-07-26 · `docs/TODO_archive.md`
- [x] **Residential revenue metric ("Residential $", Peter 2026-07-16)** — SHIPPED 2026-07-16 · `docs/TODO_archive.md`
- [x] **Dev+Infill ROUND-2 delta audit** — EXECUTED 2026-07-16 · `docs/TODO_archive.md`
- [x] **PRIORITY — Lot-acre denominator TOGGLE on the neighbourhood (first) lens (NEW 2026-07-08, out of the cardinality audit below).** — BUILT 2026-07-08 · `docs/TODO_archive.md`
- [x] **PRE-LAUNCH AUDIT — record-to-parcel cardinality bug (WEM numerator + condo denominator) & lot-acre vs ground-acre methodology (NEW 2026-07-08).** — CLOSED 2026-07-09 · `docs/TODO_archive.md`
- [x] **Neighbourhood labels — finish + ship** — SHIPPED 2026-07-04 · `docs/TODO_archive.md`
- [x] **Ghost prisms over a neutral hood plane (Peter, 2026-07-03; design clarified 2026-07-04).** — SHIPPED 2026-07-05 · `docs/TODO_archive.md`
- [x] **PRIORITY — Lot-size denominator variant for the grid spikes** — SHIPPED 2026-07-05 · `docs/TODO_archive.md`
- [x] **SCOPE: composition numbers now; full zoning POLYGON layer in the viewer is a SEPARATE later product decision** — 2026-07-03 · `docs/TODO_archive.md`
- [x] **UI control hierarchy: separate "Color Adjustment" from lens controls.** — BUILT 2026-07-07 · `docs/TODO_archive.md`
- [x] **Deployment — LIVE (2026-07-01/02)** — 2026-07-01 · `docs/TODO_archive.md`


- [x] Revenue phase backend — per-property municipal levy + `revenue_per_acre`
  (committed `5912576`).
- [x] Web value↔revenue toggle, revenue default (committed `a0cf2a0`).
- [x] Push `feature/phase2-web` to origin.
- [x] **Low-coverage tail separated via the Zoning Bylaw layer (`fixa-tstc`)** —
  end-to-end land-use set-aside feature (2026-07-01). `src/load_zoning.py` (95 base
  codes → never/notyet/inst/dev, overlay → `set_aside_frac`/`is_set_aside`/
  `set_aside_reason`), wired through `join_and_calculate` + `main.py`; 48 hoods set
  aside at ≥0.90. Colour transform **DECIDED: sqrt** (FINDINGS §6.1 — log over-corrects
  to −4.19; the mixed 0.55–0.90 band stays on-scale by design). Frontend: sqrt colour
  + neutral-grey set-aside hoods. Methodology caveat recorded in FINDINGS §5 (zoning
  `UI`/`UF`/`AJ`/`PU` partially flags exempt-roll understatement). Refs:
  `docs/FINDINGS_revenue_scale.md` §§5–6.1, `scripts/investigate_skew.py`,
  `docs/SPEC_revenue.md` "Update 2026-06-29".

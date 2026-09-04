# Fable 5 Brief — Front-End Architecture DECISION Audit

Read this in full before opening any code. `docs/PLAN_frontend_refactor.md` is the
standing container for this initiative — status, artifacts, and what is already
measured; this brief is the instrument it points at. This is **not** the security/architecture
brief (`docs/FABLE_AUDIT_BRIEF.md`) and not the Development-lens brief
(`docs/FABLE_AUDIT_development_lens.md`) — separate sessions, separate questions.

This one asks whether the **frameworkless single-file front end is still the right
architecture**, top-down, highest level first — and if it is not, what replaces it and
in what order.

⚠️ **This brief differs from the others in one way: it is a FORWARD decision, not a
post-hoc audit.** The prior briefs judged something already shipped. Here the shipped
thing (one 7,345-line `web/index.html`) is the *status quo option*, and it competes on
equal terms with the alternatives. Each level therefore needs both a verdict **and**
what you would do instead.

This session uses Fable 5 usage that counts against plan limits at a higher rate than
Opus — don't spend it re-deriving context that is already written down. §3 below is the
measured evidence; take it and argue, don't re-measure.

## 0. The one rule that makes this audit different

**Evaluate the stack in order, and when a level is unsound, say so and treat everything
beneath it as moot.** Do not spend the session choosing module seams if you have
concluded the front end should be generated rather than hand-written, or that the
no-build rule should fall.

For each level return: a one-word verdict — **SOUND**, **CONDITIONAL** (sound only if a
stated caveat holds), or **UNSOUND** — the single sharpest argument against it, **what
you would do instead**, and what evidence would change your verdict.

We are not looking for reassurance. The authors are motivated to believe the current
design works; your value is the argument they did not make against themselves.

⚠️ **Two things are out of scope and will be rejected if they appear as
justifications:**

1. **Token/context savings.** This was measured and is **false** — the file is read in
   grep-located windows via `docs/CODEMAP.md`, never end-to-end. See
   `docs/TOKEN_EFFICIENCY.md` "Files to watch". Justify on navigability, grep
   precision, blast radius, or correctness — or not at all.
2. **Runtime performance of the page.** Boot and render cost are a separate, shelved
   item with their own measurements (`docs/PERFORMANCE.md`). This audit is about the
   *source*, not the frame budget.

## 1. Ground yourself first (in this order, then stop reading and start judging)

⚠️ **Items 2 and 3 are quoted in full below — do NOT open `docs/DECISIONS.md` (367 KB)
or `TODO.md` (214 KB).** Between them they are ~80% of this brief's reading list by
size, and neither holds more than one section that bears on this audit.

1. `docs/STACK.md` — §3 (frameworkless front end) and **§9 (what this project
   deliberately does NOT use)**. §9 is the decision you are being asked to reopen.
2. **`docs/DECISIONS.md` 2026-07-29 — the stage-1 decision, quoted in its load-bearing
   parts:**

   > `web/index.html`'s CSS is extracted to `web/styles.css` — **stage 1 of splitting the
   > single file, and the only stage taken**. The file was 83% JS / 10% CSS / 7% markup,
   > and **the CSS is the one part with zero coupling to the rest**, so it moves at
   > near-zero risk and directly serves the queued mobile-chrome work (which previously
   > had to navigate 3,300 lines of deck.gl layer code to reach 400 lines of styles).
   > **The motivation is navigability and blast radius, NOT tokens** — the file was
   > already read in grep-located windows of 100–400 lines, not end-to-end, so the split
   > saves little context and may cost slightly more for the common change that touches
   > CSS + DOM + handler together (three file opens vs three offsets). **`DEFAULT_BUILD`
   > must stay in `index.html`**: `scripts/build_site.py` regexes it there and hard-fails
   > unless it finds exactly one. Both builds work unchanged — the public root copies the
   > whole `web/` tree, and `/full/` (index.html only) resolves `styles.css` through its
   > existing `<base href="../" />`. Verified by pixel-identical screenshots vs master at
   > 1440px and 390px. **Stage 2 — splitting the JS along its section banners into ES
   > modules — is deliberately NOT taken**; it carries the real risk and should wait
   > until stage 1 proves it helps.

   ⚠️ **That last sentence's stated risk was measured wrong** — see item 3.

3. **`TODO.md` → "STAGE 2 of the `web/index.html` split" — the constraints §3 does not
   carry, quoted** (its numbers are all in §3; re-measured 2026-09-04):

   > - **Gate: wait until stage 1 has actually helped** — the mobile-chrome work in
   >   `MOBILE_USABILITY.md` §3 is the first real test of it. Don't do stage 2
   >   speculatively. ⚠️ **The doubling arguably moots this gate**: the item was deferred
   >   when the file was half its current size. **Re-read the gate before invoking it as
   >   a reason to defer again.**
   > - ⚠️ **`DEFAULT_BUILD` must stay in `index.html`** — if the JS moves, that literal
   >   stays behind or `build_site.py` moves with it.
   > - ⚠️ **"11 verify scripts reference `index.html`" was WRONG, and it pointed the risk
   >   at the wrong half of the repo.** It is **8 of 65**, and **7** name it as a served
   >   **URL** (`localhost:PORT/index.html`), not the source file — an ESM split leaves
   >   those working. ⚠️ **The eighth is the exception:
   >   `tools/profiling/verify-staleness-banner.js` reads `web/index.html` off disk**
   >   (`fs.readFileSync`, line 66) and regexes `const STALE_DAYS = (\d+);` out of the
   >   source — a literal declared under the `tunables` banner, **inside the `<script>`
   >   block a split moves**. It fails loudly (`process.exit(1)`), but it is **the one
   >   JS-side file a split must carry**. **The real coupling is 11 Python/CI files**:
   >   `build_site.py`,
   >   `check_cost_copy.py`, `check_served_columns.py`, `check_doc_citations.py`,
   >   `build_reference_layers.py`, `tools/codemap.py`, `tests/test_build_site.py`,
   >   `tests/test_codemap.py`, `tests/test_window_labels.py`, plus the `refresh.yml` and
   >   `deploy.yml` path triggers. ⚠️ **`tools/codemap.py` is the sharp one** — it parses
   >   the banners out of this file to generate `docs/CODEMAP.md`, the navigation aid
   >   `CLAUDE.md` points at. **Move the JS without moving `codemap.py` and the project's
   >   own navigation aid silently empties.**
4. `docs/CODEMAP.md` — the generated symbol index (278 symbols, 124 element ids)
   **and its `## Dependency graph` section — the evidence for Level 3.**
   ⚠️ **Skim its section list; do NOT read `web/index.html` end to end.** If you need
   code, open one named symbol's range.
5. `docs/security-audit.md` **S1** — why deck.gl and maplibre are vendored rather than
   CDN-loaded. This is the load-bearing constraint on Level 1.
6. `docs/SPEC_deployment.md` — the two-build fan-out (`/` public, `/full/` specialist).
7. `docs/MOBILE_USABILITY.md` §1 and §3 — §1 is the desktop↔mobile separation seam;
   §3 is the queued work that stage 2 was gated behind.

Then confirm one thing back, with the file that proves it:

> ⚠️ **GitHub Pages is NOT what forces the single-file design.** Pages serves arbitrary
> static files; a bundled build deploys to it normally. The no-build rule is a *choice*
> recorded in `STACK.md` §9 and `security-audit.md` S1.

**State that you have confirmed this before proceeding.** Several plausible arguments
collapse if you assume the platform is the constraint, and that assumption is the most
common error made about this repo.

## 2. The decision stack to audit (highest level first)

### Level 0 — Should this front end be hand-written at all?

The alternative is a *generated* artifact: Observable, Quarto, Datasette, kepler.gl, or
any templating of the map from the Python side that already produces every input.

Against the status quo: the project's whole data half is a reproducible pipeline with
guards, tests and pinned versions, while its presentation half is a hand-edited file
with no build, no types and no import graph. That is two different engineering
standards in one repo.

For the status quo: the lenses are not a generic chart — they are 19 sections of
bespoke deck.gl layer logic, per-metric colour transforms, and an uncertainty band with
its own rendering rules. Generators are good at the chart this project is not making.

**If UNSOUND here, say so and stop — every level below is moot.**

### Level 1 — The no-build-step rule, and vendoring

Currently: two vendored `<script>` tags, globals `maplibregl` and `deck`, no npm
install to serve, no transpile. Vendoring is a **security** decision — every displayed
dollar figure executes through those libraries, SHA-256s are recorded and were
cross-verified against two independent CDNs.

The question is not "is a bundler nicer." It is: **does adding a build step degrade the
supply-chain posture the vendoring was chosen for**, and is that trade worth what a
build buys? A bundler adds `node_modules` and a lockfile to a project whose current
answer to "what executes on the page" is *three files with recorded hashes*.

⚠️ Note the second-order effect: because there is no build, `scripts/build_site.py`
fans out the two builds by **regex-rewriting a `DEFAULT_BUILD` literal** in the HTML.
With a bundler that is an env var. The no-build rule is what creates that machinery.

### Level 2 — One file, or modules?

Given 0 and 1, this is the actual queued decision. Native ESM (`<script type="module">`
+ relative imports) needs no bundler and works on Pages, so **it is available without
reopening Level 1**.

The counter-argument the project has already recorded: the split saves little context,
may cost slightly more for the common change that touches CSS + DOM + handler together,
and carries real coupling risk (§3). The pro-argument is §3's growth rate.

**Is a 7,345-line file actually a problem, or is `CODEMAP.md` an adequate answer to it?**
That is the crux, and a defensible UNSOUND verdict on splitting is a legitimate outcome.

### Level 3 — If modules: what are the seams?

The file carries **19 `// --- section ---` banners** and the obvious move is one module
per banner. ⚠️ **THAT IS ALREADY MEASURED AND IT DOES NOT WORK — do not spend the
session rediscovering it.** `docs/CODEMAP.md` → *Dependency graph* has the numbers:
`money view (default)`, the **default lens**, has **1 indexed symbol and 29 lines**
under its banner, while `the citywide budget panel (EXPERIMENTAL, full build only)`
has **35 symbols and 1,587**. Self-containment runs **27–44%** across the large
sections. The banners mark where someone started typing; the tail after each one
absorbs everything until the next.

⚠️ **The banners are in BUILD order, not concern order** — `money view (default)` is
second-to-last despite being the default lens, because it was written before the others
were added around it. A decomposition inherited from chronology is not obviously a
decomposition by responsibility. Consider instead: shared kernel (state, scales, ramps,
formatting) vs per-lens layer builders vs chrome/panels vs reference layers.

⚠️ **`state` IS A GOD OBJECT — in-degree 110**, against 34 for `buildLayers` and 16
for `METRICS`. **Every proposed module boundary crosses it**, so the real question at
this level is not *which sections split* but **can `state` be decomposed at all** — and
if it cannot, whether a split that leaves a god-module is worth taking.

The graph is generated into `CODEMAP.md` on every edit. ⚠️ It is a **regex reference
count, not a call graph** (a name in a comment counts; nested symbols attribute to the
enclosing range) — sound for *what is central*, not for drawing a final boundary.

### Level 4 — The build/guard coupling: constraint, or the real smell?

**11 non-doc files read `web/index.html`**: `build_site.py` (the `DEFAULT_BUILD` regex),
`check_cost_copy.py` and `check_served_columns.py` (both *scan the HTML* for copy and
column gating), `check_doc_citations.py`, `build_reference_layers.py`,
`tools/codemap.py`, `tests/test_build_site.py`, `test_codemap.py`, `test_window_labels.py`
(WINDOWS literals vs `main.py`), plus `refresh.yml` and `deploy.yml` path triggers.

⚠️ **`tools/codemap.py` is the sharp one** — it parses the banners out of this file to
generate `docs/CODEMAP.md`, which a `PostToolUse` hook regenerates and `CLAUDE.md` names
as the way to navigate the front end. **Move the JS without moving codemap.py and the
project's own navigation aid silently empties.**

The question to answer: **is this coupling a cost of splitting, or evidence that the
guards are reading the wrong artifact?** Several of them scan rendered HTML for values
that exist structurally elsewhere. If the guards should read a manifest instead, that is
a finding independent of whether the split happens.

### Level 5 — Sequencing and blast radius

If a split is right: what order, and what is the smallest first move that proves the
seam? Stage 1 (CSS) was chosen because it had **zero coupling** and could be verified by
pixel-identical screenshots. Is there an equivalent first slice here, or is ESM
all-or-nothing?

Note the verification asymmetry: 7 of the 8 `verify-*.js` scripts reference the page by
**URL** (`localhost:PORT/index.html`), not by source file, so they keep working across a
split — they can verify the migration but cannot detect a bad seam. ⚠️ **The eighth,
`verify-staleness-banner.js`, breaks on any split that moves `STALE_DAYS` out of
`index.html`** — so the JS harness is simultaneously too weak to catch a bad seam and
strong enough to fail on a good one.

### Level 6 — Code correctness (only after the above)

Only if Levels 0–5 leave something to say. Not the point of this session.

## 3. Measured facts — take these, do not re-derive

| fact | value | measured |
|---|---|---|
| `web/index.html` total | **7,345 lines**, ~424 KB | 2026-09-04 |
| — `<head>` | ~16 lines | " |
| — `<body>` markup | ~575 lines (124 element ids) | " |
| — one `<script>` block | **~6,748 lines** | " |
| section banners | **19** | " |
| indexed symbols · graph edges | 278 · **852** | `CODEMAP.md` |
| `state` in-degree | **110** (next: `buildLayers` 34) | `CODEMAP.md` |
| **at stage 1 (2026-07-29)** | **3,305 JS lines, 9 banners** | `DECISIONS.md` |
| `web/styles.css` | ~52 KB (extracted stage 1) | `STACK.md` |
| profiling scripts naming `index.html` | **8 of 65** — **7** as a served **URL**, **1 reads the source** | 2026-09-04 |
| Python/CI files reading it | **11** | 2026-09-04 |
| vendored libs | deck.gl 9.0.38, maplibre-gl 4.7.1 | `STACK.md` §3 |

⚠️ **The JS roughly DOUBLED in five weeks** (3,305 → 6,748) while the banner count went
9 → 19. **The trajectory is the strongest argument in this brief and the only one that
came from measurement rather than taste.** Weigh it accordingly — and note that the
2026-07-29 deferral was decided when the file was half its current size.

## 4. Reporting discipline

- Before any finding, point to the file/decision it challenges. If you cannot verify
  something this session, say so — do not report it as confirmed.
- **Do not narrate your reasoning process into the output.** Report the verdict, the
  argument, the alternative, and the evidence — not a transcript of how you got there.
  ⚠️ **The stakes here were stated wrong and are worse than advertised** (corrected
  2026-09-04 by reading the CLI binary, 2.1.258; the original claim came from a relayed
  external report). `reasoning_extraction` **is real** — it is an API refusal category in
  `stop_details.category`, alongside `cyber`, `bio` and `frontier_llm`. But it does
  **not** "silently reroute the session to Opus": refusal fallbacks are a **per-category
  route map**, and for a Fable session that map is `{bio → claude-opus-5,
  cyber → claude-opus-4-8}` — **`reasoning_extraction` is not in it**. An unmapped
  refusal resolves to `matched:"none", reason:"unmapped"`, and **a refused request simply
  stops.** The catch-all that would route it anyway is off unless
  `CLAUDE_CODE_REFUSAL_FALLBACK_CATCH_ALL` is set, and it is not set on this box.
  **So the cost of narrating reasoning is a hard stop mid-audit, not a quiet downgrade.**
- No subagents — single session.
- Do **not** edit `docs/STACK.md`, `docs/DECISIONS.md`, or `web/index.html`. Those are
  the record and the artifact. Log findings; propose changes; don't make them. If a
  decision should be reopened, name it by `DECISIONS.md` date.
- **Pause and ask only for the calls the project owner alone can make.** Those are:
  (a) whether to accept a build step at all, given the vendoring security posture;
  (b) whether the presentation half is allowed to run at a lower engineering standard
  than the pipeline half; (c) whether a split happens before or after the
  `MOBILE_USABILITY.md` §3 work. Don't end on a vague "let me know."

## 5. Before this session ends

Run `/handoff`. The handoff must include:

- A verdict line per level (0–6): SOUND / CONDITIONAL / UNSOUND + the sharpest argument
  + what you would do instead.
- The highest level found UNSOUND, if any, and what it moots beneath it.
- **A single recommendation Peter can act on**, with its first concrete step — this
  brief exists to produce a decision, not a survey.
- Any `DECISIONS.md` line you recommend reopening, by date.
- Anything flagged but not verifiable this session, so it isn't lost.

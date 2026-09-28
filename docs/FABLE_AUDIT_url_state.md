# AUDIT BRIEF — the shareable URL hash

**Read cold.** This is a reusable *instrument*, not a findings doc. No run yet.
Written 2026-09-28 (S203, Opus 5.5) by the session that BUILT the feature
(PR #608), so everything it says about the feature is a self-graded claim.
**Run it on a different model** (house rule: `measurements-that-favour-me`; the
last cross-model row in `docs/AUDIT_LEDGER.md` is S172). Family: **(a) decision
audit**, top-down, and the verify script is the last level, not the first.

The feature: `#view=development&metric=permits&window=3yr` reopens what the
sender saw. Code: `urlHash`, `writeUrlHash`, `offered`, `applyUrlState`,
`restoreFromHash` in `web/index.html` (look them up in `docs/CODEMAP.md`), and the
wiring at the end of `boot`. Spec and rules: `docs/CONTROLS_MATRIX.md` §8.
Decision row: `docs/DECISIONS.md` 2026-09-28 "The URL hash names the view on
screen". Guard: `tools/profiling/verify-url-state.js`.

---

## §0 — Grounding order

1. `docs/CONTROLS_MATRIX.md` §8, then §1–§4 (the state space the hash encodes).
2. The DECISIONS row above, **read in full**, and every row it touches:
   2026-07-22 (two builds), 2026-07-28 (staged return), 2026-09-11 (Ratio's
   public gate is a hidden button). ⚠️ Read bodies, never `cut`/`head` them.
3. `docs/FINDINGS_controls_state_space.md` — the last audit of this control
   surface (S159). Its instrument `tools/profiling/audit-controls-diff.js`
   enumerates controls independently of anything this feature wrote.
4. The code, in one slice: from `URL_METRIC` through `restoreFromHash`.
5. `verify-url-state.js`, header first (it records what was falsified).

**Hinge-fact checkpoint — confirm before going deep, and stop if one is false:**
- PR #608 is on `origin/master` and the deploy after it went green
  (`gh run list --workflow deploy.yml`).
- A live link restores: open
  `https://peterfriedrich.github.io/edmonton-tax-viz/#view=development&window=3yr`
  and the same hash under `/dev-build-full/`. The address bar must keep the
  path it opened on in both.

---

## §1 — The decision stack

Per level: **SOUND / CONDITIONAL / UNSOUND**, the sharpest argument against it,
and the evidence that would change the verdict. An UNSOUND level moots the ones
below it.

### L0 — Should view state be in the URL at all?

- **Every key name is now a public contract.** Once a link is shared, renaming
  `metric=permits` breaks it silently: the key is dropped and the reader lands
  on a default with no message. Is there a stated policy for renaming or
  retiring a key? There is none today. Is silent fallback acceptable for a link
  someone cited?
- **The full build is gated by an awkward path on purpose**
  (memory: *awkward labels are deliberate*: friction against ACCIDENTAL
  visitors). A shareable full-build link carries `/dev-build-full/` into
  whatever it is pasted into. Does this feature erode that friction, and was
  that weighed? The S203 conversation did not weigh it.
- Prior art: `check-convention-before-locking-design`. Name one comparable
  civic/data map and what its URL carries (Our World in Data: query string,
  `tab`, `time`, `country`). A difference is fine; an unexamined one is the
  finding.

### L1 — Is the key set the right one?

- **Does a link reproduce what the sender SAW, or only what the controls
  say?** State persists across views (`state.denom`, `state.devWindow`, …),
  and the hash writes only the current view's keys. Find any render (legend,
  blurb, tooltip, panel, layer) that depends on state the hash does not carry.
  The round trip compares only title, view and active controls, so a
  render-only difference would pass it.
- The deliberate omissions (ramp, labels, reference layer, opacity, readout
  mode, camera, a pinned neighbourhood): argue the strongest case that ONE of
  them belongs in a shared link. A pinned neighbourhood ("look at ARGYLL") is
  the obvious candidate. The decision to defer it was the builder's, not
  Peter's.

### L2 — Is "restore selects only what a button offers" the right gate?

- The rule reuses the DOM as the source of truth for build and data gates.
  **The sharpest attack: `offered()` checks computed `display` only.** List
  every way this page hides or disables a control:
  - `display:none` on the element or an ancestor;
  - the `hidden` attribute;
  - `visibility`;
  - `disabled` (e.g. `#coloradj-btn` sets it);
  - a `.folded` panel, which is deliberately skipped;
  - revealed only after a late fetch.

  Is any gate expressed in a way `offered()` cannot see?
- **Late reveals.** Restore waits for `framePainted`, `temporalReady` and the
  grid fetch inside `applyView`. Enumerate every control revealed in a
  `.then` (`grep -n "\.then" web/index.html` inside `boot`) and check each one
  has its wait. `dev_history.json` and `status.json` both land late. Does
  either gate a control that has a URL key?

### L3 — Does the hash follow every state change?

- The writer is one delegated `click`/`change` listener. It runs a
  `setTimeout(0)` after the handler, relying on `applyView` setting
  `state.view` before its first `await`. **Enumerate every `state.<key> =`
  assignment** (29 on 2026-09-28) and classify each one:
  - (a) synchronously downstream of a click or change;
  - (b) after an `await` or in a `.then`, so the hash is written too early;
  - (c) from no user event at all.

  Anything in (b) or (c) that is a URL key is a stale-hash defect.
- Keyboard and touch activation: does every control reach a `click` or
  `change` event? Check Enter/Space on buttons and the touch peek card.

### L4 — Is restore correct?

- **Order dependence** in `applyUrlState`: metric before detail, detail before
  denominator, Infill before metric. Construct one hand-written hash whose keys
  interact (e.g. `view=development&mode=infill&metric=industrial&detail=hood`)
  and predict the result before loading it.
- **Reload loop:** `hashchange` reloads. Prove nothing on the page assigns
  `location.hash`. `grep` found none on 2026-09-28; re-check, because a future
  in-page anchor link would create the loop.
- `?build=` together with a hash; a hash with an empty value; a repeated key.

### L5 — Does the guard test what it claims? (instrument audit)

- ⚠️ **Shared-instrument blind spot, the one the builder suspects most:**
  `verify-url-state.js` decides what to walk with the PAGE's own `offered()`.
  A control that `offered()` wrongly calls hidden is excluded from BOTH the
  walk and the restore, so a lost URL key would pass. The falsification caught
  `offered()` returning true everywhere. It never tested `offered()` returning
  **false** for one real control.
  - Test: mutate `offered()` to hide one control (e.g. `#denom`) and see
    whether anything goes red.
  - Remedy direction: enumerate with Playwright's `isVisible()` or
    `audit-controls-diff.js`, independently of the page.
- **Walk coverage:**
  - Keys are deduplicated across views (a cost decision, see the header).
  - Depth is capped at 3.
  - Active group buttons are skipped.
  - Count the controls × view contexts NOT walked, and list them.

  The Glass denominator and scale are covered only by one hand-written link.
- **`screen()` compares title + view + active controls only.** Is that enough to
  call a round trip identical? Would a blurb or legend comparison have caught
  anything L1 finds?
- **Channel:** the script gates nothing yet (not in CI; Peter's call pending,
  S203). A guard with no reader is this project's standing failure mode. Is
  the pending decision recorded where the next session will see it?

### L6 — Docs and claims

- Every sentence in CONTROLS_MATRIX §8 and the DECISIONS row, checked against
  the code.
- The four comments reworded from "no persistence" to "the URL hash only selects
  offered buttons" (grep `only selects offered`). ⚠️ One of them, on the
  `#devwindow` long button, sat beside a pre-existing wrong claim ("default is
  5yr"; it is `long`). Deeper: if an older data file hides the long-window
  button, `state.devWindow` defaults to a value no button offers. That is a
  pre-existing latent defect the reword walked past. Size it or dismiss it.

---

## §2 — Out of scope

The roads verified notebook (`04_roads_lens.py`, PR #607) is a different target
with its own queue item. Do not fold it in.

## §3 — Output

`docs/FINDINGS_url_state.md`, ending with a non-empty **What this run got
wrong** section. Then add a ledger row plus findings-register rows, and tick
the queue item.

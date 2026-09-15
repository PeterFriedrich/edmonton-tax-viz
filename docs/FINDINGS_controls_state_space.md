# Findings — controls that reach nothing (run 2026-09-15, S159, Fable 5.1)

Instrument: `docs/FABLE_AUDIT_controls_state_space.md` +
`tools/profiling/audit-controls-diff.js`. Ledger row: 2026-09-15 (S159). The
brief's scoping measurement was taken by Opus 5 the same day (S158); this is the
first execution and the first cross-model read of it.

**Both builds swept, all nine readouts self-tested live on both, no control reaches
nothing, and the matrix reproduced S158's cell for cell.** The finding is the
`panel` column, exactly as the brief said — but of the brief's five ranked targets,
**one is confirmed and public (T1), one is closed by a decision the brief had not
found (T2), one is a mechanism defect that was inherited rather than decided (T4),
two are Peter's calls (T3, and T4's remedy)**, and one open row the brief did not
list was already on the matrix (`ratio-denom`, §6).

⚠️ **The instrument was not extended.** T5 (`moneydetail` / `devdetail` on the
tooltip and peek) is still probe-limited and is **not** reported as clean.

---

## §0 — Method, as run

```
build_site.py --src web --out $SCR/_site
audit-controls-diff.js  http://localhost:8947/full/index.html   (15 groups × 6 views)
audit-controls-diff.js  http://localhost:8947/index.html        (public: 11 groups × 6 views)
_probe-budget-yield.js  (T4 falsification, §4 — scratch, not kept)
```

Server restarted before each Playwright run (it wedges after one). Selftest
block read first each time: **9/9 `live` on both builds, 0 `DEAD`.** Judgement
pass done from code and `DECISIONS.md`, not from the matrix alone.

**Public build differences that matter here:** `services` is **3** rows (not 10);
`devmode`, `ratio-denom` and `budget-btn` are absent (Infill, the second Ratio
denominator and the budget pod are full-only); `devmetric` is 2 rows (Industrial
is full-only) and its `title` cell is `.` there — correct, the title only changes
for Industrial.

---

## T1 — `services / services`: the panel ignores every layer — **CONFIRMED, PUBLIC**

`panel` is `.` across **10 rows in `/full/` and 3 rows on the public build**,
while `blurb`, `legend`, `tooltip`, `tipFor`, `peek` and `layers` all move. This
is the third independent reproduction (S157 by driving keys, S158 by the probe,
this run by the probe on both builds). Nothing new to find; the direction is
locked (`DECISIONS.md` 2026-09-15, `COPY_DECISIONS.md` F1) and it is not built.

**Order of work stands:** `verify-services-panel.js` asserting only *"the panel
differs across layers"* **first**, so it is falsified against this broken build;
then F1.

---

## T2 — `development / devwindow`: the panel does not follow the window — **WIRING SOUND BY DECISION; one line of copy open**

The brief asked *"is `renderDevHistory` deliberately all-time?"* before touching
the wiring. **Yes, by a decision the brief had not located:** `DECISIONS.md`
2026-09-14 — *"the three shipped Development columns are window AGGREGATES
(5yr/3yr/since-2009); `export_dev_history` resolves the same three numerators to
one point per year"*. The panel **is** the whole series; the windows are sums over
it. `devHistoryFor` (`web/index.html`) reads `devHistKey()` and the full
`years`/`vals` arrays — no window input anywhere in the history code. The chart
already shows every year, so the reader on 3 yr sees the 2023–2025 bars inside
the 2009–2025 run. Re-scoping it would silently redefine a published number.

**What survives is copy, not wiring.** `renderDevHistory` writes
`peak N in YYYY · N in the last 5 years · active in N of 17 years` under every
window: on 3 yr the panel volunteers a five-year figure beside a three-year map;
on Since 2009 "the last 5 years" is a window the reader did not pick. Recorded as
**`COPY_DECISIONS.md` F4** (three options, Peter's call). `TODO.md` T2 closed.

---

## T3 — `money / revcut` and `lab / labcut`: the inner level does not reach the panel — **JUDGEMENT, measured and handed over**

`revenueMix(p)` reads `REV_CATEGORIES` and the hood's properties; it does not read
the cut. So under **Residential** the map draws residential $/acre and the pinned
panel is headlined **`$146.40M municipal levy · 5.26% of Edmonton's municipal
revenue`** (DOWNTOWN) — the *total*, byte-identical across the three cuts. The
residential figure is findable inside the mix rows, so the panel is not wrong; it
answers "where does this hood's whole levy come from" regardless of which slice
the map is showing.

The brief's promise test cuts both ways: `#millrates` lights a different rate per
cut on the same screen (the cut is shown to matter), but the mix panel is the
decomposition the cut is a member of (the cut is shown *inside* it). **Not
decided here.** Options: leave it; light the selected cut's row in the mix the
way `#millrates` lights the rate; or headline the cut's own levy under a cut.
`lab / labcut` is the same three cuts and follows whatever is decided.

---

## T4 — `#budget-pod`: the yield was decided, the toggle was not — **INHERITED DEFECT, remedy is Peter's**

**Was the yield decided?** Yes. `web/styles.css` at `#budget`: *"#temporal wins
over both, exactly as it already does over #millrates"*, and `DECISIONS.md`
2026-08-16 records the pod taking `#temporal`'s answer for `#temporal`'s reason.
The CSS is the same sibling selector as the mill rates
(`#temporal.open ~ #budget { display: none }` next to
`#temporal.open ~ #millrates { display: none }`).

**What the analogy skipped:** `body.mills` is **derived** — `syncMillRates`
recomputes it from view and metric, so there is nothing a reader can press that
disagrees with it. `body.budget` is a **toggle** on a reader's press. The
`CONTROLS_MATRIX.md` §3 rule *"so the two cannot both think they own the slot"*
holds for the mill rates because nobody can press them; it does not transfer.

**Measured (1440×900, full build, DOWNTOWN):**

| step | `body` | `#budget` | `#budget-btn` | `#temporal` |
|---|---|---|---|---|
| press `#budget-btn` | `budget` | flex | lit | shut |
| `openTemporal` | `budget` | **none** | **lit** | open |
| press #1 | — | none | unlit | open |
| press #2 | `budget` | none | lit | open |
| `closeTemporal` | `budget` | flex | lit | shut |
| *S2:* one press under the panel, then `closeTemporal` | — | **none** | unlit | shut |
| *S2:* press again | `budget` | flex | lit | shut |

Two reader-visible consequences. **(a) The opener lights over an invisible pod**
— `body.budget #budget-btn` has no `#temporal.open` exception, and `#budget-pod`
is not `#temporal`'s sibling, so CSS cannot give it one. **(b) A press under the
open panel toggles state with no visible effect except the button**, so whether
the pod is there when the panel closes depends on the parity of presses the reader
made while it was hidden. S158 called this "two presses to restore"; the measured
shape is *invisible presses count*, which is the same fact stated where it bites.

⚠️ **Not fixed here — the remedy is a decision, not a patch.** Three honest forms:
(1) a press under the open panel **closes the panel** (budget wins the column,
the same way picking Revenue leaves the change lens, 2026-08-01); (2) opening the
panel **clears `body.budget`** — the pod becomes a reader-reopened surface,
matching how `#peek` dismisses; (3) keep the yield and un-light the button via a
`body` class set from `openTemporal`/`closeTemporal`, accepting that the pod
"remembers". Each changes who owns the column; (1) or (2) makes the two surfaces
a real exclusion instead of a CSS one-way. `TODO.md` T4 carries the table.

---

## T5 — `moneydetail` / `devdetail`: tooltip + peek — **STILL PROBE-LIMITED, not a finding**

Unchanged from the brief §4: both Detail selectors read `.` on `tooltip`,
`tipFor`, `panel` and `peek` because the probe feeds a hood feature to
`viewTooltip` in grid modes too, and the grid has its own cell-grain tooltip.
**Both builds show the same cells.** A cell-grain capture is required before this
row is anything; this run did not add one. Recorded so the next run does not read
the row as cleared.

---

## §6 — The row the brief did not list: `ratio / ratio-denom` panel `.` is `COPY_DECISIONS.md` F3

The matrix has `ratio-denom` reaching every readout except `panel` (full build
only — the second denominator is full-only). That is F3, opened 2026-09-14: the
Ratio panel falls through to the assessment history and says nothing about the
ratio. Same argument as T1 — the sweep reached it without being pointed at it —
and it is already an open copy row, so nothing is added here beyond the
cross-reference. ⚠️ Its own warning stands: a road-cost *denominator* is not the
fix (both cost columns are exact multiples of road metres).

---

## §7 — Cells that read invariant and are honest

Listed so the next run does not re-derive them: `hoodmode-btn` moves only
`tipFor` (it *is* the hover-mode reduction); `coloradj-btn` moves only `blurb`
(§1's own example); `denom` leaves `title` (per-acre either way — the blurb
carries the denominator); `uses-prisms-on` leaves the categorical `legend`;
`budget-btn` moves only `budget`, and its two `.` on every map readout is the
"first pod that never bites in" of `CONTROLS_MATRIX.md` §3.

---

## §8 — Claims formed mid-run and dropped

- **"T4 needs two presses to restore"** (from S158, carried into the brief): the
  probe shows one press under the panel *and one after* — i.e. the second press
  is the one the reader would make anyway. The defect is the invisible press, not
  a press count. Reworded in §4 and in `TODO.md`.
- **`#budget-btn` background readings**: the probe captured within the button's
  120 ms colour transition, so the raw alphas (0.47, 0.835, 0.996) are
  mid-transition noise. The table reports the class-driven steady state, which is
  what `body.budget #budget-btn` renders.

---

## §9 — What this run did not do

- Did not build F1 or its verify script (build work; direction locked).
- Did not extend the instrument to cell-grain tooltips (T5).
- Did not run on a phone viewport — the brief says grouping is shared DOM so the
  wiring findings transfer; the `peek` column is clean on both builds, which is
  the cell that would have raised severity there.
- Did not decide T3 or T4.

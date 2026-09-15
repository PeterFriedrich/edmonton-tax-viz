# AUDIT BRIEF — controls that reach nothing

**Read cold.** This is a reusable *instrument*, not a findings doc. The coverage
map is `docs/AUDIT_LEDGER.md`; the state space this audits is
`docs/CONTROLS_MATRIX.md` (what shows when, what gates what). Scoping
measurement taken 2026-09-15 (S158) with
`tools/profiling/audit-controls-diff.js`.

**Third sibling of a swept family.** `docs/FABLE_AUDIT_proxy_guards.md` covers a
check reading a **stand-in** for the property; `docs/FABLE_AUDIT_vacuous_guards.md`
covers a check reading the **right** property where it **cannot differ**. This
one moves the same shape from the guard estate to the **reader-facing control
surface**: a control the reader can see and press, next to a readout it does not
reach. All three are surfaces that look like they work.

---

## §0 — Why this class exists

**Fresh evidence, which is this list's stated criterion, not absence.**

S157 (2026-09-14) drove all ten `SERVICES` keys and diffed the rendered Services
cost panel: **byte-identical every time**. Select Fire, Water, Transit or Bike,
click a neighbourhood, and the panel reports **road costs**. `renderServiceCost`
reads the fixed `SVC_COST_BASES` and never `state.service`. Three of those rows
are **public** (`SERVICES[k].pub`, roads-only since 2026-09-02), so this is not a
full-build-only defect.

⚠️ **Nothing verifies the Services panel today.** A check asserting only *"the
panel differs across layers"* would have caught it on day one — which is the
whole argument for sweeping the class rather than fixing the instance.

⚠️ **The class already has a written precedent in this repo, and it was right.**
`CONTROLS_MATRIX.md` §5.6, closed 2026-07-27:

> *"if a control ignores the pickers around it, it is probably a lens, not a
> detail mode."*

That was written about Stock age and resolved by removing it. The same sentence
read the other way around is this brief: **if a readout ignores the pickers
around it, the reader has been told a relationship that does not exist.**

---

## §1 — The hinge fact, confirm before descending

> **An invariant readout is a CANDIDATE, not a verdict.** `#coloradj` is
> *supposed* to leave the title alone. The defect is not invariance; it is
> invariance **the layout advertises as responsiveness** — a control and a
> readout that the reader has been given a reason to connect.

So the audit is two passes, and the second is judgement that does not automate:

1. **Mechanical** — drive every value of every visible control, diff every
   readout. Produces the matrix in §3.
2. **Judgement** — for each invariant cell, ask *what did the interface promise?*
   Adjacency in the same panel, a shared caption, a shared noun, or a picker that
   sits directly above the readout are all promises. Distance is not.

⚠️ **Rank by the promise, not by the count.** A control invariant across eight
readouts may be perfectly honest; one invariant across a single readout sitting
directly beneath it is the defect.

---

## §2 — ⚠️ THE INSTRUMENT IS THE FIRST THING TO FALSIFY

**Read this before running anything.** The scoping probe reported "invariant"
**four separate times without looking**, in a script written specifically to hunt
readouts that do not respond. Every one was green, plausible, and wrong:

| # | the probe did | reported | why it could not vary |
|---|---|---|---|
| 1 | `features.find(f => f.properties.name === HOOD)` | tooltip + peek invariant in **all 13 rows** | the field is `neighbourhood_name`; `f` was always `undefined`, so both readouts were a constant sentinel |
| 2 | `String(viewTooltip({object: f}))` | tooltip invariant in **all 13 rows**, second time | `viewTooltip` returns deck's `{ html }` **wrapper**; `String()` on it is a constant `"[object Object]"` |
| 3 | `innerText` on `#peek` | peek invariant everywhere | `#peek` is CSS-gated on `(hover: none)`; `innerText` returns `''` for a hidden element on a desktop viewport. **`textContent` reads it; `innerText` cannot** |
| 4 | captured `#budget` *after* calling `openTemporal` | `#budget-pod` reaches nothing, in **all six views** | the pod yields the left column to `#temporal`, so the probe's own readout-opening **closed the surface it then measured** |

**#4 is the one to internalise: the instrument mutated the state it was
measuring.** A probe that opens panels to read them is not a passive observer of
a UI whose surfaces contend for space.

⚠️ **Therefore: every readout must be shown LIVE before any invariance verdict is
believed.** `audit-controls-diff.js` prints a `selftest` line per readout and
flags empty values, `THREW:`, `(no feature)` and `[object Object]`. **A `DEAD`
selftest line invalidates every `.` in that column** — it does not reduce
confidence, it removes the measurement. This is
`check-where-the-value-can-be-wrong` for the eighth and ninth time, and the third
brief in a row to need its own falsification pass first.

---

## §3 — The measured matrix (full build, 2026-09-15, 1440×900)

`Y` = the readout changed across that control's values; `.` = byte-identical.
Nine readouts: `title` (`#title-h`), `blurb` (`#title-p`), `legend`
(label/min/max/cats), `tooltip` (`viewTooltip`), `tipFor` (`tooltipFor` — the
hover-mode reduction lives here, **not** in `viewTooltip`), `panel`
(`#temporal-body`), `peek` (`#peek`), `budget` (body class **+** rendered
display), `layers` (deck layer ids).

```
view        | control        | n  | title blurb legend tooltip tipFor panel peek budget layers
money       | metric-row     | 2  | Y     Y     Y      Y       Y      Y     Y    .      .
money       | revcut         | 3  | Y     Y     Y      Y       Y      .     Y    .      .
money       | moneydetail    | 3  | .     Y     Y      .       .      .     .    .      Y
money       | denom          | 2  | .     Y     Y      Y       Y      .     Y    .      .
money       | hoodmode-btn   | 2  | .     .     .      .       Y      .     .    .      .
money       | coloradj-btn   | 2  | .     Y     .      .       .      .     .    .      .
money       | budget-btn     | 2  | .     .     .      .       .      .     .    Y      .
development | devmode        | 2  | Y     Y     Y      Y       Y      Y     Y    .      Y
development | devmetric      | 3  | Y     Y     Y      Y       Y      Y     Y    .      .
development | devwindow      | 3  | Y     Y     Y      Y       Y      .     Y    .      .
development | devdetail      | 2  | .     Y     Y      .       .      .     .    .      Y
services    | services       | 10 | .     Y     Y      Y       Y      .     Y    .      Y
ratio       | ratio-denom    | 2  | Y     Y     Y      Y       Y      .     Y    .      .
uses        | uses-prisms-on | 2  | .     Y     .      .       .      .     .    .      Y
lab         | labcut         | 3  | Y     Y     Y      Y       Y      .     Y    .      .
```

(`hoodmode-btn` and `budget-btn` repeat identically in all six views; collapsed
here, full output in the run log.)

**After the four instrument fixes, no control reaches nothing.** The finding is
not a dead control — it is the `panel` column.

---

## §4 — Ranked targets (highest level first; a moot level moots what is under it)

### T1 — `services / services`: the panel ignores all ten layers ⚠️ CONFIRMED

Independently reproduced here by a different method than S157's. `panel` is `.`
across all ten service rows while `blurb`, `legend`, `tooltip`, `tipFor`, `peek`
and `layers` all move. **Six readouts follow the picker and the seventh does
not** — that asymmetry is the promise, and it is made by the picker's own panel.

Direction already locked (`DECISIONS.md` 2026-09-15, `COPY_DECISIONS.md` F1):
the panel follows the picker. ⚠️ **4 of 10 layers (storm, fire, water,
transit-supply) have no cost twin** and must degrade to a shorter form, not an
empty group. **Not built.** Public exposure: 3 rows.

### T2 — `development / devwindow`: two of three sibling pickers reach the panel, one does not

The strongest **new** finding, and the same shape as T1 with no decision behind
it. In one panel, on one view:

| control | reaches `panel` |
|---|---|
| `#devmode` (Housing built / Infill) | **Y** |
| `#devmetric` (Units / Permits / Industrial) | **Y** |
| `#devwindow` (3 yr / 5 yr / Since 2009) | **.** |

Every other readout follows all three. **Ask first whether the panel is
window-scoped at all** — if `renderDevHistory` is deliberately all-time, the
defect is the copy, not the wiring, and T2 becomes a `COPY_DECISIONS.md` row
rather than a build item. ⚠️ **Do not fix the wiring before answering that**; the
cheap fix would silently redefine a published number.

### T3 — `money / revcut`: the inner level of a two-level control does not reach the panel

`#toggle` is the app's only control that nests within a tier
(`CONTROLS_MATRIX.md` §1). The **outer** level (`#metric-row`, Revenue/Value)
reaches the panel — correctly, it swaps `renderRevenueMix` for `renderHistory`.
The **inner** level (`#revcut`) does not.

Plausibly correct by design: the mix panel *is* the decomposition, so a cut
selection may have nothing to add. **But `#millrates` is keyed on the `#revcut`
row's existence** and lights a different rate per cut, so the reader has been
shown the cut mattering elsewhere on the same screen. Judgement row — settle it,
do not assume either way. `lab / labcut` is the same three cuts with the same
`.`, and should be settled together.

### T4 — `#budget-pod`: the state class and the rendered pod disagree

Measured directly, not inferred: clicking `#budget-btn` takes `#budget` from
`display:none` to `flex` and sets `body.budget`; calling `openTemporal` then
returns it to `display:none` **while `body` still carries `budget`**.

`CONTROLS_MATRIX.md` §3 documents the yield deliberately for `#millrates`, with
the stated reason being that CSS is used *"rather than a JS toggle, **so the two
cannot both think they own the slot**"*. ⚠️ **Here they do.** The reader's next
press toggles the class *off* a pod that is already invisible, so restoring it
takes two presses. Check whether the budget yield was ever decided or merely
inherited from the mill-rates rule.

### T5 — `moneydetail` / `devdetail`: tooltip and peek invariant — **probe-limited, do not report as a finding**

Both Detail selectors leave `tooltip`, `tipFor`, `panel` and `peek` unchanged.
**The probe feeds a HOOD feature to `viewTooltip` in every mode**, and the grid
modes have their own cell-grain tooltip — so this cell measures the wrong
surface, exactly like §2 #1. **A cell-grain capture is required before T5 is
anything at all.** Listed so a later run does not mistake it for a cleared row.

---

## §5 — Method

```bash
.venv/bin/python scripts/build_site.py --src web --out $SCR/_site
# ⚠️ restart the server before EVERY Playwright run — it wedges and then serves
# empty responses while still answering
cd tools/profiling            # ⚠️ required: playwright resolves from the SCRIPT dir
node audit-controls-diff.js http://localhost:8947/full/index.html
node audit-controls-diff.js http://localhost:8947/index.html   # public exposure
```

1. **Read the `selftest` block first.** Any `DEAD` line invalidates that
   column entirely (§2). Do not proceed on a partially-live instrument.
2. Take the matrix. For each `.`, ask §1's question: *what promise was made?*
3. For each surviving candidate, **falsify by name** — reintroduce the
   responsiveness by hand and confirm that specific readout moves. A candidate
   that cannot be made to move is a stronger finding, not a weaker one.
4. ⚠️ **Run both builds.** The public build carries fewer controls, so a defect
   can be full-only (rank it lower) or public (rank it higher) — `services` is
   the worked example: 10 rows in `/full/`, 3 public.
5. Add an `AUDIT_LEDGER.md` row when the audit **executes**, with a pointer to
   its findings doc.

⚠️ **Out of scope, so nobody writes it:** *which grouping is better*. This brief
asks whether a control reaches the readout beside it — a falsifiable question.
Regrouping is a design decision and belongs in `CONTROLS_MATRIX.md` §5 with
Peter's call, not in an audit verdict.

⚠️ **Mobile is NOT a separate run, and also not covered.** Grouping is shared DOM
(`CONTROLS_MATRIX.md` §1), so the wiring findings transfer unchanged. What does
**not** transfer is that `#peek` is the phone's only per-hood readout, which
raises the severity of any `peek` column defect. `docs/MOBILE_USABILITY.md` §1.

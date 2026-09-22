# Findings — readout floors and formatters (S173–S186 backlog item #3)

**Run:** 2026-09-22, S188, Opus 5.5, effort high, `edmonton-audit` decision family.
⚠️ Same model family as the author of #476/#483/#495/#520c, so not independent.

**Target:** `money0`, `fmtMix`'s `v > 0` guard, `under2dp` / `SMALL_2DP`, the `<`
floors (`fmtRoadM`, `fmtResShare`, `fmtSvcRatio`), `fmtBike` deliberately
unfloored, and `verify-smoke.js` §C9/§C10. The ledger's two questions: does any
served value now read wrong, and can C9 go red on a real defect rather than
only on the mutations it was written for?

**Grounding read in full:** DECISIONS 2026-09-18 (S3), 2026-09-19 (S5/S6,
`money0`, C9), 2026-09-20 (bike `MIN_PIECE_M`; S7 per-unit), 2026-09-21 (S8,
`fmtRoadM`/`fmtResShare`); `COPY_DECISIONS.md` S3–S9.

**Instrument:** a headless replay of **every hood through every view and
sub-mode's own `viewTooltip`** on both builds: money × 4 metrics × 2
denominators, services with all 10 services on, ratio × both denominators,
development × 2 metrics × 3 windows, infill × 2, change × 2, deviation and uses.
That is **9,338 renders on the full build, 0 throws**. Every zero-looking token
(`$0`, `0.0…`, `0%`, `100%`) was extracted with its context and triaged against
the served value behind it. The point is to check the **surface**, not the
helper, and that difference turned out to be the whole finding. Served file =
`web/data/` at `0c454bb` (built 2026-09-21).

## Verdicts

| Level | Question | Verdict |
|---|---|---|
| L0 | Should a small nonzero value floor (`<$1`, `<0.01`) rather than round to a "none" reading? | **SOUND.** Peter's rule, 2026-09-21. Measured, the two-sided `v > 0` form holds everywhere it is used |
| L1 | Does every surface that renders these values go through the floored helper? | **FAIL.** Two open-coded ratio-view sites bypass it (§1) |
| L2 | Is each floor at its formatter's own rounding boundary? | **SOUND** at the zero end. **WARN** at the top end: `fmtResShare` prints `100%` for 6 hoods that carry non-residential revenue (§2) |
| L3 | Is `fmtBike` right to stay unfloored? | **FAIL from the next refresh.** Its decided condition, "zero base rate", is broken by S188's own boundary split (§3) |
| L4 | Can C9/C10 go red on a real defect? | **FAIL.** They test the helpers over columns, so they are green over L1's live defects. **Separately, and worse: the C-family tooltip-garbage sweep has been VACUOUS since it was written** (§4) |
| L5 | Does `<` in un-escaped tooltip HTML render? | **PASS.** `<` followed by `$` or a digit is not a tag-open per the HTML tokenizer. Verified: the DOM's `textContent` reads `<$1 to $5,115 / acre` |
| — | Surfaced, off-target: the FAR numerator's coverage | **WARN, full build only, routed not fixed** (§5) |

## §1 — L1: two ratio-view sites bypass the floors (live now)

Both are **open-coded at the use site**. That is exactly the class
`COPY_DECISIONS.md` S8 named ("a sweep of `fmt*` could not see them"), and it
survived S8's own fix.

1. **The ratio tooltip's local `money` helper**:
   `const money = v => "$" + Math.round(v).toLocaleString();` inside
   `viewTooltip`'s ratio branch. It renders the institutional band's lower end.
   **UNIVERSITY OF ALBERTA FARM** (`rev_frac_exempt` 0.999997) renders, on the
   fire denominator:
   `$0 to $54,978 / fire event` and `$0 to $5,115 revenue / acre`.
   The Money view renders **the same number** through `money0` as
   `<$1 to $5,115 / acre`. So the two lenses disagree about one quantity, and
   Ratio calls a nonzero amount `$0`, which is the S5 misreading. The two
   `RATIO_DENOMS[*].fmt` point formatters open-code the same expression, but
   every kept hood's point value is far above $0.50, so they are latent.
2. **The ratio floor message**: `` ` (${p[d.col].toFixed(d.floor < 1 ? 3 : 1)})` ``.
   **HERITAGE VALLEY AREA**, `road_m_per_acre` 0.0499, renders
   `No meaningful ratio — road base below 5 m / acre (0.0)`, while the Services
   tooltip renders the same value as `<0.1 road m / acre`. The fire variant
   (`toFixed(3)`) is latent: every hood under 0.0005 today is a true zero or
   set aside.

⚠️ **DECISIONS 2026-09-21 says `road_m_per_acre` "had FOUR render sites" and
that all now share `fmtRoadM`. There were five.** The count came from grepping
for the formatter's idiom, and this site formats a *generic* column
(`p[d.col]`), so a road-specific grep could not see it.

**Fix:** route both through the floored helpers. `money` → `money0`. The floor
message → the denominator's own component formatter, so the words and the
number stay one call (`d.component` already exists for roads; fire needs its
equivalent).

## §2 — L2 top end: `fmtResShare` says `100%` for six mixed hoods

`Math.round(100 * frac)` prints `100% of revenue is residential` for
`frac ∈ [0.995, 1)`. Six served hoods hit it: CRYSTALLINA NERA WEST (0.99563),
HENDERSON ESTATES, ANTHONY HENDAY HORSE HILL, CALLAGHAN, WEDGEWOOD HEIGHTS,
QUESNELL HEIGHTS (0.99904). Each carries 0.1–0.45% non-residential revenue,
and 0 hoods are exactly 100%. This is S8's `0%` misreading mirrored: `0%` read
as *nobody lives here*, and `100%` reads as *nothing else is here*. Peter's
rule ("don't hide activity, just say it's super small") covers it on its face,
but the string (`>99%`) is a wording call → a `COPY_DECISIONS.md` row, not an
audit fix. The same shape appears, less sharply, in the Uses tooltip
(`Industrial 100%` where sub-0.5% categories are filtered) and in the set-aside
`(100% of area)` suffix. Neither is a single-line claim about a remainder, so
they are listed, not ranked.

## §3 — L3: `fmtBike`'s "no floor" rests on a condition S188 just broke

DECISIONS 2026-09-20: *"`fmtBike` gets no floor on purpose… a surviving 1 m
route in a huge hood could in principle land under 0.005 m/acre but today none
does, so no guard was added on a mechanism with a zero base rate."*

The S188 boundary split (PR #535) halves any route lying on a shared hood
boundary. **KING EDWARD PARK**'s only bike length is a 3.39 m corner clip on
its boundary, so it becomes 1.70 m over 368 acres = **0.0046 m/acre**. That
renders `0.00 dedicated bike route m / acre` from the **2026-09-28 refresh**,
measured by re-running `load_bike` on the local feed. Nothing guards it:
§C10 does not note `bike_m_per_acre`. Road is unaffected in kind: ANTHONY
HENDAY ENERGY PARK (0.0468) and HERITAGE VALLEY AREA (0.0483) stay under 0.05
and `fmtRoadM` already floors them.

**Fix (before 2026-09-28):** `fmtBike` through `under2dp`, and bike added to
§C10's `note` list. This is the decided per-unit rule (`fmtFire`/`fmtTransit`)
applied to a unit whose stated exemption no longer holds, not a new policy.

## §4 — L4: the guards test helpers, and the C-family tooltip sweep tests nothing

**(a) C9/C10 are green over §1.** Both run the SHIPPED helper
(`money0`, `fmtFire`, …) over every served column. That was the right answer to
"a fixture copy can drift", but it cannot see a render site that never calls
the helper. §1's two defects are live and C9/C10 pass on them. So the answer to
the ledger's question is **no**: C9 goes red only when `money0` itself breaks,
which is the mutation it was written for.

**(b) The C-family "no NaN/undefined in any hood's readout" check is
vacuous, and has been since it was written (b99af11, 2026-08-02).**

```js
const html = viewTooltip({ object: f });   // returns { className, html }
if (/\bNaN\b|\bundefined\b|…/.test(html))  // tests "[object Object]"
```

`viewTooltip` already returned `{ className, html }` at that commit. The regex
coerces the object to the constant `"[object Object]"`, so it can never match.
**Proved by mutation**: a build whose residential-share line prints
`NaN% of revenue is residential` puts `NaN` in **340 of 406** money tooltips
(read via `.html`), and `verify-smoke.js` reports
`PASS C-money / revenue: no NaN/undefined in any hood's readout`. That run went
red only incidentally, on §C10's true-zero comparison over 51 hoods. A NaN in
any readout outside C9/C10's column list (fire, storm, water, the dev rows, the
deviation line…) would pass the whole gate. The unmutated control build: 49
PASS, 0 FAIL. Every other caller in `tools/profiling/` reads `.html`, and
`audit-controls-diff.js` carries a comment describing **this exact trap**
(*"String() on it yields a constant '[object Object]'"*), so the lesson was
learned once and never ported to the gate that runs weekly.

This is the family the file calls *"THE HIGHEST-VALUE FAMILY"*, and the only
verify script CI runs. It is `check-where-the-value-can-be-wrong` at the gate
itself.

**Fix:** `.html` on line 310, then falsify it (the same NaN mutation must redden
`C-money / revenue`). Then give C a surface-level zero check: run the replay's
token scan inside smoke, asserting no `$0` / `0.00` / `0.0` token sits over a
nonzero value. That is what would have caught §1 and §3.

## §5 — surfaced: the FAR numerator covers built area unevenly (not this target)

⚠️ **Not a re-proposal of a `fmtFar` floor.** S9 is DECIDED and this finding
does not reopen it. What it tests is S9's **premise**, *"a near-unbuilt hood
genuinely has FAR ≈ 0"*, and that premise holds for some of the 10 on-scale
`0.00 FAR` hoods and not for others.

`far` = Σ `gross_area` (rows with a recorded floor area) ÷ Σ lot m² (**all**
eligible lots). A lot whose building's floor area is not recorded therefore
counts as land and adds nothing as floor area. `year_built` separates the two
readings:

| hood | lot area with a floor area recorded | rows without one that have a `year_built` | reading |
|---|---|---|---|
| WHITE INDUSTRIAL | 5.0% | **50 of 60** | built, unrecorded → FAR understated |
| POUNDMAKER INDUSTRIAL | 6.1% | **23 of 26** | built, unrecorded |
| CROSSROADS | 25.1% | 29 of 102 | mixed |
| GOODRIDGE CORNERS / RIVER'S EDGE / MARQUIS | 0.4–14% | **0** | genuinely unbuilt → FAR ≈ 0 is honest |

Citywide, **13%** of the lot area lacking a floor area has a `year_built`. The
exposure is the **full build only**: the Money value tooltip's FAR row (e.g.
WHITE INDUSTRIAL `$1,550,860 / lot acre · 0.00 FAR`), plus Infill, which sets
non-residential hoods off its scale, so the scored surface is mostly spared.
Worth its own audit. It belongs to the Infill / FAR target, not to formatters.

## Fixes proposed (none applied in this run)

| # | Fix | Deadline |
|---|---|---|
| 1 | `verify-smoke.js:310` → `.html`, then falsify with the NaN mutation | now: the weekly gate is blind |
| 2 | `fmtBike` through `under2dp`, bike added to §C10 | **before the 2026-09-28 refresh** |
| 3 | Ratio `money` → `money0`; the ratio floor message through the component formatters | — |
| 4 | A surface-level zero-token check in smoke (this run's replay, minus the triage) | — |
| 5 | `fmtResShare` top end (`>99%`?) | Peter's wording call, `COPY_DECISIONS.md` |
| 6 | FAR numerator coverage | a separate audit |

## What this run got wrong

- **My replay reported a blank headline that did not exist.** UNIVERSITY OF
  ALBERTA FARM's Money tooltip scanned as `" / acre"` with no number. My
  tag-stripping regex (`<[^>]+>`) read `<$1 to $5,115</b>` as one tag and
  deleted it. Caught by re-rendering through a DOM node's `textContent`, which is
  also how L5 got its PASS. The instrument manufactured a finding of the class
  it was hunting, which is this skill's standing warning.
- **§3 is a defect I introduced earlier in this session** (PR #535, the
  boundary split). My pre-merge check compared per-hood metres, not what those
  metres render as, and it never asked which floors assume a zero base rate.
  The 2026-09-20 row names that assumption in plain words. Reading it before
  building the split would have caught this. The broader lesson: a data change
  that lowers small values should re-run the readout floors.
- **The first mutation run measured no server.** System `python3` is 3.6 and
  rejects `--directory`, so both background servers exited, and a smoke run
  against the dead port printed nothing I was grepping for. Re-served with the
  venv's Python and confirmed both roots by `curl` + grep for the mutation
  (1 hit on 8941, 0 on 8942) before believing any result
  (`confirm-the-server-you-measure`).
- **§5 started as a confident "S9's premise is wrong".** The first coverage
  table (industrial hoods) supported it. The greenfield rows then showed the
  opposite reading, and only the `year_built` split turned "wrong" into
  "right for some hoods, wrong for others".

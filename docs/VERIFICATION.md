# Verification

⚠️ **This covers `notebooks/verified/` — the pipeline notebooks that run inside
`refresh.yml` and gate the weekly publish. The public-facing EVIDENCE notebooks
backing `docs/DATA_ISSUES.md` are a different artifact with an opposite purpose:
see `docs/EVIDENCE_NOTEBOOKS.md`.**

[Methods & definitions](https://peterfriedrich.github.io/edmonton-tax-viz/verified/02_methods.html)
explains what the numbers mean and how they're built. This doc is for a different question: **how do you know it actually ran
correctly, this week, on real data** — not just that the method sounds right on
paper?

## The proof

**[The Money lens, end to end](https://peterfriedrich.github.io/edmonton-tax-viz/verified/01_money_lens.html)**
— the real pipeline code, imported and run in production order, against this
week's live data, with every step's invariants checked and reported. It is not
a summary of the pipeline; it *is* the pipeline, with the prose interpolated
around what the run actually produced.

Two rules make that trustworthy rather than just plausible-looking:

- **No number is written by hand.** Every figure in the page is pulled from the
  run you are reading, not typed in by a person. The data refreshes weekly, so
  a hand-typed number would be wrong within days and nobody would notice.
- **Invariants are asserted, values are not.** The page never claims "revenue
  is $2.67B" as a pass/fail condition — a real number like that changes on
  every legitimate data refresh. It claims things that must hold *no matter
  what the data says*: aggregating to neighbourhoods can't lose or duplicate
  assessed value, `value_per_acre` has to equal what it claims to divide, the
  join can't multiply rows. If a check fails, that's the pipeline disagreeing
  with itself, not a number that moved.

This is the same discipline `verify-smoke.js` uses to gate the weekly publish
(see the four-tier table in [`ARCHITECTURE.md`](ARCHITECTURE.md#testing)) —
here it's just rendered for a person to read rather than reduced to a CI
pass/fail line.

**[Methods & definitions](https://peterfriedrich.github.io/edmonton-tax-viz/verified/02_methods.html)**
— the methods write-up, under the same two rules. Before 2026-09-24 it was a
prose `docs/METHODS.md`, which was still quoting the 2025 mill rates after
the pipeline moved to 2026. It now recomputes every figure it quotes from
the week's data, and asserts that the ones it describes are consistent with
what the site serves (for example, that every grey neighbourhood is at or above
the set-aside threshold). Claims resting on one-off investigations are cited to
their `FINDINGS_*` doc without a number.

## Read the source, not just the output

The notebooks that produce those pages are
[`notebooks/verified/01_money_lens.py`](https://github.com/PeterFriedrich/edmonton-tax-viz/blob/master/notebooks/verified/01_money_lens.py)
and [`02_methods.py`](https://github.com/PeterFriedrich/edmonton-tax-viz/blob/master/notebooks/verified/02_methods.py)
— plain Python and markdown (jupytext's percent format), readable and diffable
on GitHub without running anything. If you want to check the *claims*, not just
the output, those are the files to read: every invariant it asserts is a few lines
above the assertion, in the open.

## How it stays current

`web/verified/*.html` is regenerated every time the weekly data
refresh runs (`tools/run_verified_notebooks.py`, wired into `refresh.yml`
alongside the guards that check the served data's column schema and value
ranges). It runs *before* the site publishes, and a failing invariant blocks
the publish the same way those guards do — the last good page keeps serving
rather than a broken one going live silently.

⚠️ Because that render is automated and weekly, anything the page needs beyond
nbconvert's stock output has to live in `run_verified_notebooks.py` itself. It
injects the mobile-wrap CSS (`tools/inject_notebook_mobile_css.py`) after each
successful render for exactly that reason: measured 2026-09-21, the stock lab
template clipped **428px of every code line and 1458px of a wide output table**
at 390px wide, with no scroller. Patching the committed HTML would have lasted
one week. `tests/test_notebook_mobile_css.py::test_render_path_injects` is the
guard.

## What's covered so far

The **Money lens** — the metric the public site defaults to — and the **Roads lens** (below). The methods
page recomputes the figures it quotes, but it is a description, not an
end-to-end re-run of any lens. Stated
explicitly so the silence on everything else isn't mistaken for a clean bill
of health: the Development lens, and the other lenses (the rest of Services, Ratio, Uses,
Glass, Temporal) aren't covered by a verified notebook yet.

**[The main assumptions, sized](https://peterfriedrich.github.io/edmonton-tax-viz/verified/03_assumptions.html)**
(`03_assumptions.py`, 2026-09-28) is the third page. It is not a re-run of a
lens either. It measures how much of the levy, land or homes each main
assumption touches across Money, Glass, Development, Change and Roads. It
gates on structural checks only: a size that can't be computed, or two
measures of the same thing that disagree. It never gates on a size moving.

**[The Roads lens, end to end](https://peterfriedrich.github.io/edmonton-tax-viz/verified/04_roads_lens.html)**
(`04_roads_lens.py`, 2026-09-28) is the second lens re-run. It covers Services'
road metres per acre, from centrelines to both cost columns. It runs `load_roads`
and observes the clip's length accounting and the boundary split, rather than
re-implementing them. It asserts that the split conserves length, that served
equals the rebuild on every neighbourhood, that the map colour matches the
served figure, and that each cost column is length × the configured rate. Its one
value check is a wide citywide-length band. It also tabulates the road moves
against the last committed run. That table never gates, but it is the only
place road deltas show between refreshes (`docs/FINDINGS_roads_end_to_end.md`
§5). Falsified 2026-09-28: disabling the split, leaking it, and changing the
lifecycle rate each fail by name.

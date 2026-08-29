# Verification

⚠️ **This covers `notebooks/verified/` — the pipeline notebooks that run inside
`refresh.yml` and gate the weekly publish. The public-facing EVIDENCE notebooks
backing `docs/DATA_ISSUES.md` are a different artifact with an opposite purpose:
see `docs/EVIDENCE_NOTEBOOKS.md`.**

[`docs/METHODS.md`](METHODS.md) explains what the numbers mean and how they're
built. This doc is for a different question: **how do you know it actually ran
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

## Read the source, not just the output

The notebook that produces that page is
[`notebooks/verified/01_money_lens.py`](https://github.com/PeterFriedrich/edmonton-tax-viz/blob/master/notebooks/verified/01_money_lens.py)
— plain Python and markdown (jupytext's percent format), readable and diffable
on GitHub without running anything. If you want to check the *claims*, not just
the output, that's the file to read: every invariant it asserts is a few lines
above the assertion, in the open.

## How it stays current

`web/verified/01_money_lens.html` is regenerated every time the weekly data
refresh runs (`tools/run_verified_notebooks.py`, wired into `refresh.yml`
alongside the guards that check the served data's column schema and value
ranges). It runs *before* the site publishes, and a failing invariant blocks
the publish the same way those guards do — the last good page keeps serving
rather than a broken one going live silently.

## What's covered so far

Only the **Money lens** — the metric the public site defaults to. Stated
explicitly so the silence on everything else isn't mistaken for a clean bill
of health: the Development lens, and everything `/full/` adds (Services,
Ratio, Uses, Glass, Temporal), aren't covered by a verified notebook yet.

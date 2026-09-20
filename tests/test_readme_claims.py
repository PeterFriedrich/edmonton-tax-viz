"""The README must not promise a verdict the project refuses to render.

`DECISIONS.md` 2026-07-16 (back-filled 2026-09-07) locks cost-vs-revenue as
**magnitude, not break-even** — no 1.0 marking, *"never 'pays its way'"*. The
site honours it: the Services panel shows share-of-levy, the Ratio lens was
denied its 1.0 line, and a road-cost ratio proposed with break-even framing was
rejected again on 2026-09-15.

The README did not. Its headline read *"Which parts of Edmonton pay for
themselves"* from early in the project until 2026-09-20 — the single sentence
the lens work had refused three times, on the most public surface there is, and
the only place in the repo that said it. Nothing pointed the two at each other,
because a lock recorded against a *lens* does not announce itself to whoever
next edits the front page.

That is the whole failure mode: reader-facing copy is edited without reopening
`DECISIONS.md`, which is why `COPY_DECISIONS.md` exists. This test is the part
of that rule a person cannot forget to apply.

It checks the CLAIM, not the vocabulary. Naming the framing to explain what the
project does not do is correct and must stay possible — so a line is only a
failure when it asserts the verdict, which in practice means asserting it
without a negation attached.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# The verdict this project does not render. Each is a claim that some unit of
# land covers its own costs — the thing `svc_cost_per_acre` was measured to be
# incapable of supporting (whole levy over one service: median 10.9x, only 2.2%
# of hoods below 1.0x).
VERDICT_PHRASES = (
    "pay for themselves",
    "pays for itself",
    "pay their way",
    "pays its way",
    "pays for themselves",
)

# A sentence may name the framing in order to DENY it. These mark a denial.
NEGATIONS = ("not ", "never ", "n't ", "without ", "cannot ", "can't ", "no ")


def _claim_lines(text):
    """Lines asserting a verdict phrase with no negation to disarm it."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for phrase in VERDICT_PHRASES:
            if phrase in low:
                before = low[: low.index(phrase)]
                if not any(neg in before for neg in NEGATIONS):
                    out.append((n, line.strip()))
                break
    return out


@pytest.mark.parametrize("name", ["README.md"])
def test_readme_makes_no_break_even_claim(name):
    found = _claim_lines((ROOT / name).read_text(encoding="utf-8"))
    assert not found, (
        f"{name} asserts a break-even verdict the project does not render "
        f"(DECISIONS.md 2026-07-16 — magnitude, never \"pays its way\"): {found}"
    )


def test_the_guard_can_actually_fail():
    """Guard the guard: an undisarmed claim must trip, a denial must not.

    Without this, a broken matcher passes silently on a README that says
    anything at all — the `check-where-the-value-can-be-wrong` failure, where an
    assertion sits somewhere the value cannot be wrong.
    """
    assert _claim_lines("Which parts of Edmonton pay for themselves.")
    assert not _claim_lines("It never rules on whether a neighbourhood pays its way.")
    assert not _claim_lines("This does not show which parts pay for themselves.")

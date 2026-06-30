# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-06-29_

## Open work

- [ ] **Separate the low-coverage tail — PREREQUISITE for the colour scale.**
  The revenue distribution is a **mixture**: a roughly log-normal taxable core
  (log-skew −0.22 with the tail removed) + a near-zero spike of ≈57 neighbourhoods.
  Mixed, `log` over-corrects (left skew −2.16); the transform can't be chosen until
  the spike is split out — **by category, not by a revenue threshold** (thresholding
  is the arbitrary-cap sin).
  **CORRECTION (2026-06-29):** the spike is NOT exempt land. `is_exempt` flags only
  3 parcels citywide; exempt_share = 0.00 across all 57; tax-exempt institutional
  land (Legislature/schools/etc.) is **absent from the taxable roll entirely**, not
  flagged or zeroed. The spike is **low taxable coverage** — undeveloped/natural
  land (20× "RIVER VALLEY", golf courses, ring-road margins, energy parks,
  undeveloped town centres; 55/57 have <200 parcels). So the separator is
  coverage/land-use, not exempt share.
  - [ ] Check the **boundary dataset for a neighbourhood type/descriptor field** —
    if present, that's the principled non-arbitrary separator. Else fall back to
    name-pattern + coverage, or to sqrt-and-document (no set-aside).
  - [ ] Methodology caveat to record: revenue/acre **understates** neighbourhoods
    holding large exempt institutions, and we **cannot detect which** (absent data).
  - [ ] (was: aggregate exempt share — DROPPED, nothing to aggregate.)

- [ ] **Colour scale for revenue/value — decide after exempt split.** Current hard
  clamp ($50k / $4M, ~p97) creates a visible saturated plateau that reads as a fake
  threshold. Once exempt is split, re-run the skew check on the status-defined
  taxable set: if it's ≈ log-normal (likely), use `log` for the taxable scale; `sqrt`
  is the fallback if it stays mixed. Height stays LINEAR (locked honesty choice).
  *In progress, uncommitted in `web/index.html`:* 3 swappable colour ramps
  (Inferno / Glow / Cividis) + palette switcher — done, awaiting Peter's pick.
  *Not yet built:* scale toggle (linear+clamp / sqrt / log) for visual comparison.

- [ ] **Deployment** (per `docs/SPEC_deployment.md`): `.github/workflows/*.yml`
  (scheduled Action), `web/data/status.json` + maintenance banner, per-year archive
  filenames. Three open decisions, with leans:
  - [ ] change-detection — lean: rerun + git-diff
  - [ ] cron cadence — lean: weekly
  - [ ] heartbeat auth — lean: start with `GITHUB_TOKEN`

- [ ] **Visual polish** (pre-existing, untouched):
  - [ ] top-cap edge colour `TOP_EDGE_COLOR=[40,95,120,215]` in `web/index.html`
    ("not happy yet")
  - [ ] deferred zoom-out (~10.2→~9.4) + proportional `ELEVATION_SCALE` bundle
  - [ ] light mode + colourblind (cividis) mode

- [ ] **(Optional) exploration notebook** — work `FINDINGS_assessment_classes.md`'s
  "to visualize" list (value vs levy share by class; split-class distribution;
  per-neighbourhood exempt share). Notebooks go in `notebooks/exploration/`; per
  global CLAUDE.md, use the Jupyter MCP server tools, not NotebookEdit.

## Done

- [x] Revenue phase backend — per-property municipal levy + `revenue_per_acre`
  (committed `5912576`).
- [x] Web value↔revenue toggle, revenue default (committed `a0cf2a0`).
- [x] Push `feature/phase2-web` to origin.

# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-06-29_

## Open work

- [ ] **Surface exempt-heavy neighbourhoods in the UI.** Downtown gov / Legislature
  read legitimately LOW on revenue/acre (denominator is full boundary area with $0
  exempt numerator). `is_exempt` is detected on load but only used for the levy ($0)
  — it is NOT carried to neighbourhood level or into the GeoJSON. To surface it:
  aggregate an exempt share per neighbourhood (exempt assessed value / total) →
  `join_and_calculate` → add to `SLIM_COLUMNS` → annotate in the web tooltip/visual.

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

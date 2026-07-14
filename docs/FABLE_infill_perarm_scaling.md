# Fable work brief — Infill Lens B: per-arm colour scaling

**Goal (web-only, one small PR):** replace the Infill view's single *symmetric*
p95 clamp with **per-arm** clamps so the teal (opportunity) arm can reach full
saturation, and move the tooltip verdict cut-points out of raw-score space into
per-arm / clamped-`t` space. This implements the reopened clamp clause of the
2026-07-13 Infill decision (`docs/DECISIONS.md`, 2026-07-14 line). Nothing else
about Lens B changes.

## Why (the finding this fixes — S48 decision audit)
The mismatch score is `−(z(far) + z(activity))`. It is **structurally
asymmetric**:
- suitability term `−z(far)` is **capped at +0.97** (far ≥ 0 ⇒ `z(far) ≥ −0.97`);
- activity term `−z(activity)` is **unbounded below** (activity max z = +6.16).

On the shipped `units × 5yr` geojson (included pop 358): far mean 0.242 / std
0.249; activity mean 0.418 / std 0.780; **score range −12.03 … +1.51**; the
single symmetric p95-of-`|score|` clamp = **3.038**. Consequence: **18 hoods
saturate the orange arm, ZERO reach even 50 % on the teal arm** (teal `t` maxes
at 1.51 / 3.04 ≈ 0.50), so the legend's full-teal endpoint is unreachable by
construction, and the median hood score **+0.435** sits almost exactly on the
`+0.5` "opportunity" verdict threshold (verdict is a near coin-flip).

## Operational discipline (read before touching anything)
- **Do NOT narrate your reasoning in the chat** — a long chain-of-thought reply
  can trip the classifier reroute to Opus. Work, then report crisply.
- **No subagents.** This is one small, self-contained web change.
- **Ground yourself first, in this order:** `docs/DECISIONS.md` (the 2026-07-14
  REOPENED line + the 2026-07-13 line it amends) → `docs/SPEC_development.md`
  Lens B (the "⚠️ REOPENED" block) → the Infill code in `web/index.html`
  (`infillStats` / `_infillRaw` / `infillScore` / `infillT`, ~lines 1148–1225;
  tooltip verdict ~line 1883–1905; diverging legend `legendGradient` /
  `refreshLegend`).
- **Prototype the thresholds before wiring copy.** See "Step 0" below.
- End with `/handoff`.

## Step 0 — prototype first (pick the verdict cut-points)
Before editing, compute — over the *included* population, for the default
`units × 5yr` column — the per-arm p95 clamps and where hoods land, e.g. a
throwaway node/python read of `web/data/neighbourhood_value_per_acre.geojson`
replicating `_infillRaw` (`−((far−μf)/σf + (act−μa)/σa)`, μ/σ over
`!is_set_aside && far!=null && col!=null`). Report: `clampPos` (p95 of positive
scores), `clampNeg` (p95 of |negative|), and how many hoods fall in each verdict
band under a candidate `t` cut. Aim so ~⅓ of each arm reads as its verdict, not
half the map reading "opportunity". This informs the threshold constant — don't
guess it blind.

## The change (exactly these edits in `web/index.html`)
1. **`infillStats()` (~1159):** instead of one `clamp` = p95 of `|score|`,
   compute **two**: split the included hoods' raw scores by sign, then
   `clampPos = quantile(posScores, 0.95) || 1` and
   `clampNeg = quantile(negMagnitudes, 0.95) || 1` (reuse the existing
   `quantile` helper). Cache both on the per-column object
   (`{ fs, as, clampPos, clampNeg, col }`). Guard empty arms with `|| 1`.
2. **`infillT(p)` (~1194):** normalise per arm —
   `v > 0 ? Math.min(1, v / s.clampPos) : Math.max(-1, v / s.clampNeg)`
   (v === 0 → 0). Keep the `infillOppSuppressed` early-return and the null
   guard unchanged.
3. **Tooltip verdict (~1894):** replace the fixed `score > 0.5 / < -0.5` cut-off
   with cut-points in **`t` space** (compute `t = infillT(p)` and branch on the
   Step-0 constant, e.g. `t > T / t < -T`), so the bands are per-arm and stable.
   Keep the raw-`mismatch` number line in the tooltip (it's still informative).
4. **Legend:** the diverging gradient already maps `t ∈ [−1,1]`; per-arm scaling
   makes the teal endpoint reachable with no gradient change. Check the legend
   aside/label copy still reads true (it must no longer imply symmetry); update
   only if it now misstates the scale.

**Do NOT change:** `_infillRaw`, `infillIncluded`, `infillOppSuppressed` (the
asymmetric residential gate stays), `INFILL_CENTER/POS/NEG` ramp, set-aside
handling, or the pipeline (no backend column — this is web-only).

## Verify
- `tools/profiling/verify-infill.js` — **add ≥2 checks:** (a) a teal hood now
  reaches near-full saturation (`|infillT|` close to 1 on the opportunity arm —
  impossible before this change); (b) `clampPos !== clampNeg` (arms are
  independent) AND the **pressure ranking is unchanged** (DOWNTOWN still the
  top-pressure hood — the orange arm's ordering must not move). Update the header
  count. Serve locally and run it green.
- **`pytest` is unchanged (318)** — web-only, no backend touched. Run it anyway
  to confirm you didn't break an import.
- Screenshot with `tools/profiling/shot-infill.js` and eyeball: teal hoods should
  now show genuinely bright cyan at the top of the opportunity arm.

### Env quirks (Oracle box)
- playwright resolves **only** from `tools/profiling/node_modules` — run verify/
  shot scripts from there (or `node tools/profiling/verify-infill.js …`).
- serve: `bash -c 'cd web && exec python3 -m http.server 8931'` (NOT `--directory`),
  then `until curl -sS -o /dev/null http://localhost:8931/index.html; do :; done`.
- `pkill -f "http.server 8931"` exits 144 — harmless; verify itself prints
  "N passed, 0 failed".
- The committed geojson already carries `far` + `is_residential`, so **NO
  `main.py` regen is needed** — serve the committed data directly.

## On completion (docs to update in the same PR)
- **`docs/DECISIONS.md`:** append a 2026-07-14 line **LOCKING** the per-arm
  decision (supersedes the REOPENED line's "handed to Fable" status) — one line +
  pointer, no rationale duplication.
- **`docs/SPEC_development.md`** Lens B: convert the "⚠️ REOPENED" block to a
  "✅ per-arm scaling DONE" note; bump the verify count.
- **`TODO.md`:** tick the item.

## Deploy
Web-only → **not live until the next `refresh.yml` run** (it redeploys `web/`
even with unchanged data). **Peter triggers it** — do not run the workflow.

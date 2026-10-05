# Findings — the S185–S186 colour claims, re-derived and rendered (queue item 6)

**Run:** 2026-10-05, S215, Opus 5.5, `xhigh`. ⚠️ Same model family as S185/S186.
**Target:** `docs/AUDIT_LEDGER.md` queue item 6. Four claims made at medium
effort, never rendered, with the measurement scripts lost:
1. the landing ramp spends its range where few hoods are;
2. cividis collides with `SET_ASIDE_COLOR`;
3. the backdrop sweep (14.x% of hoods under 3:1; near-black is best);
4. #525's chrome tokenization is inert in dark mode.

The item gates `TODO.md` "Colour legibility".

**Instrument:**
- **Arithmetic.** Re-written from scratch against the shipped code: `RAMPS`
  stops and `rampColorAt` (linear RGB between stops, rounded), `scaleT` (sqrt,
  `colorClamp` 50,000), `SET_ASIDE_COLOR`. sRGB → CIELAB (D65), ΔE76 **and
  ΔE2000**. WCAG 2.x relative luminance and contrast ratio. Served data from
  the CI refresh of 2026-09-28, 358 on-scale hoods.
- **Render, headless Chromium + SwiftShader:**
  - the public build in cividis, camera centred on each probe hood at zoom
    14.5, pitch 0 and pitch 50, with the median of a 7×7 pixel patch at the
    centre;
  - pre- and post-#525 builds (`9e9efed^1` vs `9e9efed`) on identical data,
    four states, plus an after/after control for render noise.

## Verdicts

| Claim | Verdict | Re-derived 2026-10-05 |
|---|---|---|
| 1. Ramp-middle compression | **REPRODUCES** (arithmetic) | IQR **$15.1k–$27.9k → t 0.549–0.747**. `current` decile ΔE76 **48.8, 12.4, 7.0, 6.1, 6.9, 8.1, 10.9, 8.6, 18.5, 30.1**: identical to S186's figures. In ΔE2000, the stricter metric, the middle deciles are **3.7–5.0** (`current`) and **3.1–3.6** (cividis), near the noticeable floor for non-adjacent patches. Not rendered (see "What this run got wrong"). |
| 2. Cividis ↔ set-aside collision | **CONFIRMED, and RENDERED** | Arithmetic: min ΔE76 **2.04** (S186: 2.3) and ΔE2000 **1.85** at t = 0.414. Hoods within ΔE76 3: **4** (HAWKS RIDGE, GORMAN, CLOVERDALE, HAYS RIDGE AREA; $8.2k–$9.2k/acre); within 5: **9** (S186: 8); within ΔE2000 3: 6. **On screen (top-down):** those 4 render **ΔE2000 1.8–2.6** from rendered set-aside land. Rendering darkens both by about 11 RGB levels, so the collision survives. At pitch 50, 2 of 4 still sit within ΔE2000 1.5; the other two probes hit neighbouring prisms, so the 3D numbers are unreliable. **Public**: cividis is in the public Display menu. `current` and `glow` stay ≥ 25 ΔE2000 from the grey. |
| 3. Backdrop sweep | **REPRODUCES**; the ledger's figure is a transcription slip | `current` on `#0a0a0f`: **52 / 358 = 14.5%** under 3:1 (clears above t = 0.507). That is the research file's own 14.5%; the ledger's "14.2%" is a copying error. Among neutral backdrops, **pure black is optimal** (41 failing; grey 128 → 344; grey 250 → 72). Per ramp on its own backdrop: glow 9.5%, cividis 6.4%. |
| 4. #525 inert in dark | **CONFIRMED** | Before vs after: **25 / 25 / 20 / 0** differing pixels (landing, Display menu, pinned panel, Development). The after/after control gives **26 / 26 / 20 / 0** in the same map bounding box. The difference is render jitter, and none of it is chrome. |

## What it means for `TODO.md` "Colour legibility"

The gate this item held is open. **Both measured defects reproduce on current
data, and the categorical one is now seen on screen**:
- The collision TODO's counts are refreshed in this PR: 4 within ΔE 3, now
  $8.2k–$9.2k; 9 within 5.
- Its proposed guard is still the right shape: the minimum ΔE between
  `SET_ASIDE_COLOR` and a dense sample of every ramp, over a stated floor. It
  should use **ΔE2000**, not ΔE76. The two disagree at this distance (2.04 vs
  1.85), and only ΔE2000 is a perceptual-difference metric.
- The compression item's *"Not yet reproduced visually"* still stands for the
  compression itself. Its arithmetic is now confirmed twice, on two vintages.

## What this run got wrong

- **The 3D samples would have refuted the collision for 2 of 4 hoods.** The
  pitch-50 sample put CLOVERDALE at ΔE 66.6 from set-aside, i.e. no collision.
  Had I sampled only the default 3D view, I would have reported that. The centre pixel at pitch 50 was
  a neighbouring hood's lit prism, not CLOVERDALE. Only the top-down sample
  measures the hood under test. The 3D column is reported as unreliable rather
  than as evidence against the collision.
- **Claim 1 was not rendered.** "Is a ΔE2000 of 3.1–5.0 between decile hoods
  legible on screen" is a perception question, and a pixel sample cannot answer
  it. The collision render shows rendering shifts colours roughly uniformly,
  which suggests the arithmetic transfers. That is an inference, not a
  measurement.
- **ΔE76 versus ΔE2000.** S186 and the TODO quote ΔE76 throughout. I re-derived
  both and lead with ΔE2000 where they differ. On the collision that makes the
  defect **worse** (1.85, below the ~2.3 JND), not better, so the change of
  metric is not doing my finding's work. On the compression, ΔE2000 also makes
  the middle look worse.

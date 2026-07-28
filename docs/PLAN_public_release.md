# Public Release Plan — prepping for an external audience

_Written 2026-07-09, from an external prioritization memo Peter brought in (a
planning conversation about opening the tool to a wider public audience). This
doc records the intake — the memo
reconciled against the repo's actual state — and the resulting release plan.
The memo predates Sessions 25–31; most of its build list turned out to be
already shipped. TODO.md carries the actionable items; this doc owns the
scope decisions and rationale._

## 1. The memo, reconciled against reality

The memo proposed a three-tier priority. Checked item-by-item against the repo
on 2026-07-09:

| Memo item | Memo's claim | Actual state |
|---|---|---|
| **Tier 0: WEM + condo cardinality mismatch** | "Known, undocumented bug in the core revenue-per-acre number — fix before anyone sees it" | **CLOSED 2026-07-09 — and the premise is inverted.** The pre-launch audit (`FINDINGS_denominator_cardinality.md`, `tools/audit_cardinality_denominators.py`) proved the neighbourhood lens **immune to both bugs, structurally and empirically**: the numerator sums the real per-account roll and never joins parcel geometry; the denominator is boundary area and never reads `lot_size`. WEM is a *single* $1.285B account (a grid needle, not a numerator double-count); condo denominator inflation is 0.1% citywide and the shipped `SHARE_MAX_M2` dedupe neutralises it. The grid-needle presentation issue was fixed by the lot-acre denominator toggle — shipped on the Glass view (PR #12) and the Money view (PR #23), both live. It is now thoroughly **documented** (three FINDINGS docs + methods notes). |
| **Tier 1: Roads lens** | "Ship it" | **Shipped + live** since 2026-07-02 (PR #8; Services view generalization PR #14). |
| **Tier 1: Zoning pipeline / 48 low-development hoods** | "Correctness plumbing, keep" | **Shipped + live** since 2026-07-01 (set-aside layer: 48 hoods grey, `set_aside_reason` in tooltips). |
| **Tier 2: Recreation** | "Cut for this release" | **Never existed.** No spec, no code — nothing to cut. Confirmed out of scope. |
| **Tier 2: Fire rescue** | "Keep, in re-scoped demand-per-acre form" | **Already built + shipped in exactly that form** (2026-07-06): `fire_events_per_acre`, 2023–2025 averaged, medical share a documented caveat, live on the Services view. |
| **Tier 2: Stormwater** | "Most shovel-ready thing on the roadmap — build it if anything" | **Built + shipped + validated** (2026-07-05/07): bylaw-native A×I×R model, live Services layer, order-of-magnitude validation vs EPCOR published revenue (`FINDINGS_utility_validation.md`). Water/sanitary shipped too; franchise fees as columns-only by design. |
| **Tier 2: Transit** | "Defer to Phase 2" | **Matches.** Never started; stays deferred. |

**Net intake conclusion: the memo's entire build list is done.** What actually
remains for a public release is not lens work — it's **presentation-layer
credibility**: the public-facing surfaces (README, in-app attribution, a
readable methods page) lag far behind the shipped analysis, plus a handful of
ops-hardening items already on TODO.

The memo's core *editorial* principle survives intact and governs this plan:
**fewer, bulletproof lenses beat more, shakier ones** in front of readers who
will reconcile our numbers against Administration's OIC figures.

## 2. Platform question — RESOLVED

**Decided (Peter, 2026-07-09): no new hosting, no new engineering.** The
release ships on the existing GitHub Pages deployment, and the pre-release
scope is narrative tightness — build nothing new. Expansion candidates
(transit lens, per-year archives, parcel-level work per
`PARCEL_LEVEL_OPPORTUNITIES.md`) stay Phase 2.

### 2a. Two-build split — public + specialist (revised 2026-07-22)

The 2026-07-09 note assumed **one** site serving everyone. Revised: ship **two
builds from the same repo and same Pages site** —

- **Public build** at the site root (`…/edmonton-tax-viz/`): a **curated
  subset** — the audited lenses with clean copy, WIP/experimental lenses and
  deep data-detail stripped.
- **Specialist build** at `…/edmonton-tax-viz/full/`: **everything**, with the
  full data-detail. **Unlisted, not access-controlled** — the repo is already
  public, so nothing here is secret; the URL is simply un-advertised. (No auth →
  stays on free Pages; still "no new hosting.")
  - **Labelling is the mitigation, not optional.** Because `/full/` is
    discoverable rather than gated, the build MUST carry a visible "work in
    progress — experimental lenses, figures not final, don't cite" label. That
    label does the load-bearing work auth otherwise would; a stray visitor must
    not mistake a WIP lens for a published claim. Reuse the attribution/status
    footer machinery (§4 P1 #2), don't invent a separate banner.

**Mechanism — single source, no fork.** `web/index.html` stays the only
hand-edited file, with a `BUILD` mode flag (`public | full`); feature/detail
visibility gates on it. A build step emits **two generated copies** into one
Pages artifact (root = public, `/full/` = full). One source of truth, zero
drift. (Forking the 3,200-line file was rejected — the drift risk we spend
sessions fighting.) The `/full/` copy's data paths resolve up one level; handled
in the build step.

**Where the two-copy emit lives (2026-07-22):** it's a *code-shaping* step — no
data download or regen — so its home is the **code deploy path**, not the data
pipeline. Deploy is now split into two workflows (`docs/SPEC_deployment.md`
"Two deploy paths"): `deploy.yml` (push-triggered code deploy, ~seconds) and
`refresh.yml` (weekly data). The two-copy generate step must run before
`upload-pages-artifact` in **both** (each uploads the `web/` artifact), so factor
it as a shared step/script rather than inlining it twice. Building this two-build
is therefore a natural extension of `deploy.yml`, gated on the "organize the
lenses" pass that produces the `public | full` tags.

**The mechanism is locked; the CONTENT split is not — it's coupled to the
control-regrouping work.** "Which lenses are public" and "how the lenses are
grouped" are the same surface (`docs/CONTROLS_MATRIX.md`): each lens/control
carries a `public | full` tag right next to its group, decided in **one**
"organize the lenses" pass, not as a separate deployment exercise. The plumbing
is grouping-agnostic and reads whatever tags that pass produces.

**FINALIZED split (regroup pass, 2026-07-23 — `CONTROLS_MATRIX.md` §7 +
`DECISIONS.md`):** `#views` collapses to **5** (Glass → a mode of Money; Infill →
a full-only mode of Development).
- **Public:** Money (incl. the Glass grid mode) · **Development** (units +
  permits only). _(Uses pulled to full-only 2026-07-24; **Services and Ratio
  pulled 2026-07-28** — both provisional, see below.)_
- **Full-only:** the **Services**, **Ratio** and **Uses** views · the **Infill**
  mode + the **Industrial** metric on Development · deep data-detail (validation
  ratios, modeling quirks, methodology-heavy blurbs).

**Superseded 2026-07-28 — the public build is now 2 views, not 4.** Peter pulled
**Services and Ratio** to full-only while prepping the release, provisional "for
now" (same framing as the Uses pull). Two residues went with them, decided at the
same time: the Money tooltip's `road m/acre` + `$/road metre` rows (Ratio's
headline metric was being published on the *default public view*), and the Data &
Methods pod's modelled-services caveat + its road/fire/transit source credits.
See `DECISIONS.md` 2026-07-28 and `CONTROLS_MATRIX.md` §2. **§3 below still lists
Services/Ratio/Uses as release scope — that is now the FULL build's scope; the
lenses ship, just not at the root URL.**
- Full-only controls are `BUILD`-flag-gated at the control level, so a full-only
  *mode/metric inside a public view* (Infill/Industrial on Development) is exactly
  what the mechanism supports.

## 3. Release scope (proposed lock)

**IN — everything currently live:**
- **Money view** (revenue/value per acre with the revenue class cuts, ground +
  lot-acre denominator toggle, colour-adjust toggle). _The residential fade lens
  was removed 2026-07-26 — superseded by the Residential revenue cut and the
  tooltip's "% of revenue is residential"._
- **Glass** (100 m grid, both denominators) — post-regroup a *mode of Money*,
  not a separate view (still ships public)
- **Services view** (roads; stormwater MODELED; fire demand; water MODELED)
- **Ratio view** (revenue per road metre)
- **Uses view** (zoning composition, real bylaw geometry)

**OUT (unchanged decisions, now release-scoped):**
- Transit — Phase 2 regardless of the fork.
- Recreation — never existed; not building one for this release.
- Franchise-fee display layer — columns-only by design (collinear with
  dwelling count).
- Total-services $ denominator redefinition — stays physical
  (SPEC_utilities decision 3).

**On the modeled utility lenses staying in:** stormwater validates at 1.11× on
the residential slice (excess localized + explained), water at ≈1.26× with the
gap characterized — both are honestly labeled "modeled, not billed" in-app and
carry written validation docs. That meets the "bulletproof or defer" bar via
*honest labeling + published validation* rather than deferral. If Peter wants a
stricter read for the most skeptical readers, the cheap fallback is shipping them
default-unchecked (they already are — roads is the default Services layer) with
the methods page carrying the caveats. **No code change proposed.**

## 4. The actual gap list (ranked)

> **STATUS 2026-07-26 — P1 and P2 are COMPLETE. The plan is done except P3
> (blocked) and P4 (optional).** Per-item status is marked inline below. What
> remains: **P3** is laptop-only (edmonton.ca is unreachable from the Oracle box
> — re-confirmed 2026-07-26) and **P4** is polish, of which the colour-blind
> half is *already shipped* (the `cividis` ramp has been selectable in the
> Display popover all along; this doc was stale in listing it as to-do). So
> nothing on this plan gates a public link any more.

### P1 — Public front door (NEW work; the real Tier 0 now) — ✅ ALL DONE

The analysis is audited; the *storefront* isn't. A skeptical reviewer's path is
site → "where do these numbers come from?" → README/methods, and today that
path dead-ends:

1. **README refresh** — the middle sections still said "Methodology (Planned)",
   "Tooling: QGIS", and "parcel data via AltaLIS or FOIP — still being pursued".
   All pre-build and wrong (the pipeline is Python-only; the parcel question was
   resolved via `dkk9-cj3x` lot sizes + the dedupe). **Done in this PR.**
2. ✅ **DONE 2026-07-25/26 (PRs #94, #95, #97).** **In-app attribution/methods affordance** — the live map had **no link to
   the repo, data sources, or methodology** (verified: nothing in
   `web/index.html`). Add a small footer/info control: data source + assessment
   year, "modeled, not billed" pointer for utility layers, link to the repo /
   methods page. Highest credibility-per-effort item on the list.
3. ✅ **DONE 2026-07-09 (PR #32).** **A single readable METHODS page** — distill the FINDINGS docs into one
   public-facing methodology note: metric definitions; ground vs lot-acre
   denominators + the 15% guard; the set-aside layer; the WEM/condo cardinality
   story (this is where the memo's Tier-0 worry gets answered *proactively* —
   the two easily-spot-checked locations become worked examples, not
   vulnerabilities); utility model formulas + validation ratios; fire caveats.
   Nearly all content exists across `FINDINGS_*.md`; the work is curation.

### P2 — Ops/correctness hardening — ✅ ALL DONE

4. ✅ **DONE 2026-07-11.** **CI unmatched-set assertion** (audit §4) — fail-loud on hood-name drift
   instead of warn-silent. A public site auto-refreshing weekly should not be
   able to silently drop a neighbourhood.
5. ✅ **DONE 2026-07-26 (PR #96)** — built as prevention *plus* detection, since the PAT alone fails silently when the PAT itself expires: the workflow uses `secrets.HEARTBEAT_TOKEN || github.token`, AND the frontend ages `last_checked` to raise its own staleness banner past 14 days. One manual step outstanding: Peter creating the secret (`RUNBOOK.md` §3). **Heartbeat PAT** (SPEC_deployment "Staying awake") — the scheduled Action
   auto-disables after 60 idle days; on a public site that means silently
   stale data. Bumped from "watch" to "do before release".
6. ✅ **DONE 2026-07-09.** **Security/PII checklist pass** — `docs/security-audit.md` exists but its
   boxes are unchecked. Run it once for real (PII in processed outputs/logs,
   gitignore coverage, dependency pins) and tick/date it.

### P3 — Credibility anchor (laptop-only)

7. **Decoteau / Horse Hill / Riverview IIMP annotation** (existing TODO item,
   scope locked there) — the direct bridge to the OIC accounting the City is
   introducing for the 2027–2030 budget cycle. Blocked on a laptop session
   (edmonton.ca unreachable from the Oracle box). Worth doing before wider
   outreach; not a blocker for a soft public link.

### P4 — Polish (nice-to-have, not gating)

8. ~~Colourblind (cividis) mode~~ **already shipped** — the `cividis` ramp is selectable in the Display popover and labelled colour-vision-deficiency-safe; this line was stale. Still open: light mode; top-cap edge colour; the
   colour-scale (post-exempt-split) decision item; deferred zoom bundle.

### Explicitly NOT doing pre-release

New lenses of any kind; parcel-level work; per-year archive filenames (unless
the fork lands engineering hands); the Rider-T gas-franchise change (parked
with its caveat, per Peter 2026-07-07).

## 5. Suggested sequencing

1. This PR (plan + README refresh + TODO update). — *done*
2. P1.2 + P1.3 together (in-app affordance links to the methods page, so build
   the page first). One session.
3. P2 items — small, independent; can ride along or batch into one hardening
   session.
4. P3 on the next laptop session.

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

## 3. Release scope (proposed lock)

**IN — everything currently live:**
- **Money view** (revenue/value per acre, ground + lot-acre denominator toggle,
  residential lens, colour-adjust toggle)
- **Glass view** (100 m grid, both denominators)
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

### P1 — Public front door (NEW work; the real Tier 0 now)

The analysis is audited; the *storefront* isn't. A skeptical reviewer's path is
site → "where do these numbers come from?" → README/methods, and today that
path dead-ends:

1. **README refresh** — the middle sections still said "Methodology (Planned)",
   "Tooling: QGIS", and "parcel data via AltaLIS or FOIP — still being pursued".
   All pre-build and wrong (the pipeline is Python-only; the parcel question was
   resolved via `dkk9-cj3x` lot sizes + the dedupe). **Done in this PR.**
2. **In-app attribution/methods affordance** — the live map has **no link to
   the repo, data sources, or methodology** (verified: nothing in
   `web/index.html`). Add a small footer/info control: data source + assessment
   year, "modeled, not billed" pointer for utility layers, link to the repo /
   methods page. Highest credibility-per-effort item on the list.
3. **A single readable METHODS page** — distill the FINDINGS docs into one
   public-facing methodology note: metric definitions; ground vs lot-acre
   denominators + the 15% guard; the set-aside layer; the WEM/condo cardinality
   story (this is where the memo's Tier-0 worry gets answered *proactively* —
   the two easily-spot-checked locations become worked examples, not
   vulnerabilities); utility model formulas + validation ratios; fire caveats.
   Nearly all content exists across `FINDINGS_*.md`; the work is curation.

### P2 — Ops/correctness hardening (existing TODO items, priority-bumped by the release)

4. **CI unmatched-set assertion** (audit §4) — fail-loud on hood-name drift
   instead of warn-silent. A public site auto-refreshing weekly should not be
   able to silently drop a neighbourhood.
5. **Heartbeat PAT** (SPEC_deployment "Staying awake") — the scheduled Action
   auto-disables after 60 idle days; on a public site that means silently
   stale data. Bumped from "watch" to "do before release".
6. **Security/PII checklist pass** — `docs/security-audit.md` exists but its
   boxes are unchecked. Run it once for real (PII in processed outputs/logs,
   gitignore coverage, dependency pins) and tick/date it.

### P3 — Credibility anchor (laptop-only)

7. **Decoteau / Horse Hill / Riverview IIMP annotation** (existing TODO item,
   scope locked there) — the direct bridge to the OIC accounting the City is
   introducing for the 2027–2030 budget cycle. Blocked on a laptop session
   (edmonton.ca unreachable from the Oracle box). Worth doing before wider
   outreach; not a blocker for a soft public link.

### P4 — Polish (nice-to-have, not gating)

8. Colourblind (cividis) mode + light mode; top-cap edge colour; the
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

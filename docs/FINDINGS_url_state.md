# Findings — the shareable URL hash (run 2026-09-28, S204, Opus 5.5, `xhigh`)

Instrument: `docs/FABLE_AUDIT_url_state.md` (decision stack L0–L6). Target: PR
#608 (`urlHash`, `writeUrlHash`, `offered`, `applyUrlState`, `restoreFromHash`
in `web/index.html`; `tools/profiling/verify-url-state.js`). Ledger row:
2026-09-28 (S204).

⚠️ **SAME MODEL AS THE BUILDER.** The brief says to run this on a different
model. Peter asked for this run on Opus 5.5, which also built #608 in S203. The
three CONFIRMED findings below stand on mutations that went red or stayed
green, not on my reading. **The SOUND verdicts on L1–L4 are the builder's model
grading its own work.** A cross-model read is still owed, and the ledger queue
item stays open for it.

**Verdict: the feature is correct and its guard is not.** Every restore
prediction held, and no render leak was found (L1–L4). But the verify script
passes with two controls silently dropped from every link (F1). It also passes
with a link-breaking rename (F2). The page runs with a wrong comment over a
latent blank-map default (F3).

| Level | Verdict |
|---|---|
| L0 state in the URL at all | **CONDITIONAL:** sound, but only with a stated policy for renaming or retiring a value (F2) |
| L1 key set | **SOUND** (measured; the pinned-neighbourhood key is Peter's call) |
| L2 "restore only what is offered" | **SOUND** |
| L3 hash follows every change | **SOUND** |
| L4 restore correctness | **SOUND:** 40/40 predictions |
| L5 the guard | **UNSOUND** for two defect classes it claims to cover (F1, F2); remedy for F1 validated |
| L6 docs and claims | **WARN:** F3, plus three small claims (§6) |

---

## §0 — Method, as run

- **Hinge facts:**
  - #608 is on `origin/master`, and deploy run 36485567529 was green (21:21 UTC).
  - `#view=development&window=3yr` restores live on both builds, and the address bar keeps `/` and `/dev-build-full/` respectively.
- **Local site:** `build_site.py --src web --out $SCR/site`, served by `.venv` `http.server` on :8956. The serving root was confirmed via `/proc/<pid>/cwd`.
- **Mutants:** `cp -al` copies of the site with one `index.html` changed, served on :8957/:8958.
- **Order:** every Playwright run went alone and sequentially, one browser per load, the verify's own pattern.
- **Probes (scratch, not kept):**
  - `fp.js`: the render fingerprint (L1).
  - `l4.js`: hand-written hashes, predicted before running.
  - A copy of `verify-url-state.js` that decides visibility with the browser's `checkVisibility()` instead of the page's `offered()` (L5).
  - `nl.js`: Development on a data file with the `_long` columns stripped (F3).

## L0 — Should view state be in the URL at all? **CONDITIONAL**

- **Prior art: the choice of URL state is conventional.**
  - Our World in Data's grapher puts its state in the query string.
  - OSM and MapLibre's own `hash` option put the camera in the hash. This page uses MapLibre 4.7.1 and does not turn that option on, so nothing else writes `location.hash`.
- **The full build's friction is not eroded.**
  - The `/dev-build-full/` path was always in the address bar, so any copied URL carried it before #608.
  - `?build=full` on the PUBLIC root already opens the full build. This was confirmed live today: `FULL_BUILD` true, `view=uses` restored.
  - That matches DECISIONS 2026-07-22 ("Unlisted, NOT access-controlled"). The hash adds state to a link. It adds no reach.
- **The condition is F2.**
  - Every value is now a public contract.
  - Nothing states what happens when one is renamed or retired, and this project retires things routinely: Stock age (07-27), the Ratio "Per service $" denominator (09-05).
  - OWID keeps an explicit, tested migration list for exactly this (`GrapherUrlMigrations.ts`: `year`→`time`, entity names).
  - The "silently fall back to the default" rule is Peter's (DECISIONS 2026-09-28). What is missing is the other half: a rename is not a fallback case, and should map the old value rather than drop it.

## L1 — Does a link reproduce what the sender SAW? **SOUND (measured)**

The round trip compares only the title, the view and the active controls, so I
measured the render directly instead.

- **What the fingerprint holds:** title, blurb and legend text, the layer ids from `buildLayers()`, and the fill colour and elevation sampled on 6 features per layer. Also `viewTooltip` HTML for 4 hoods, and the hash.
- **The procedure:**
  1. Set one non-default in view A.
  2. Switch to view B by its button.
  3. Fingerprint the page.
  4. Load B's written hash cold and fingerprint again.
- **Coverage:**
  - Public: 11 settings × 5 targets (4 views + Glass). Full: 17 × 7.
  - The settings cover every public key and every full-only key (Industrial, Infill+amenity, fire, Ratio fire, Uses prisms, Lab cut).
- **Result: 0 differences in either build** (18 and 25 cold loads).
- **The fingerprint has teeth.** It separates each known-different pair in the fields you would expect:
  - `''` vs `denom=lot`: blurb, legend, colours, tooltips;
  - `''` vs `scale=linear`: blurb, colours;
  - `window=3yr`: title, blurb, legend, colours, tooltips;
  - the services colour driver: blurb, legend, colours.
- **Why it holds:** the state that persists across views (`colorAdjust`, `denom`, `metric`, `glassCell`, `amenity`, …) is read only inside its own view's branches. `scaleT` and `fillFor` are reached only from Money and Glass layers, and `revenueLens()` is Money/Glass-scoped.

**The strongest omission is a pinned neighbourhood.** "Look at ARGYLL" is the
obvious link to share from a per-neighbourhood map. The argument against it is
new: it would make the City's neighbourhood names part of this project's link
contract, a vocabulary the repo does not control, on top of F2's. That trade
is Peter's call.

## L2 — Is "restore selects only what a button offers" the right gate? **SOUND**

- **Every build and data gate on the page is `style.display = "none"`.**
  - The only `disabled` (`#coloradj-btn`, `syncColorAdjust`) is set in the same function that hides its pod, so the two never diverge.
  - No gate uses `hidden`, `visibility`, `inert` or `aria-disabled`.
- **Viewport:** no URL-keyed control is hidden by a media query. The two `display:none` rules under `@media` are `#title-p` and `#millrates`. So a phone restores a desktop sender's link.
- **Late reveals:**
  - `temporal.json` reveals `#moneymode`'s Change button, and restore awaits `temporalReady`.
  - `dev_history.json` reveals only `#hoodmode`, which has no key.
  - `status.json` gates no control.
  - The Development grid (`devGridFetch`) and the Glass/Infill grid (`ensureGridData`) are awaited inside `applyView`, and restore awaits `applyView`.
- **DECISIONS 2026-09-11 still holds.** Ratio's public fire denominator stays unreachable, and the verify's `view=ratio&denom=fire` → `view=ratio` check passes.

**Sharpest argument against:** the gate is coupled to one hiding idiom. A future
gate written as `disabled` alone would be restored straight through. That is a
convention to keep, not a present defect, and F1 is what makes it dangerous.

## L3 — Does the hash follow every state change? **SOUND**

- **All 29 `state.<key> =` assignments** fall into three places:
  - synchronously inside a click or change handler's applier;
  - inside restore;
  - the boot-time data gates (`state.services[k] = false`), which run before the first write.
- **Nothing in class (b) or (c).** `applyView` sets `state.view` and resets Infill's Industrial before its first `await`. `applyMoneyDetail` sets `glassCell` before its fetch. Every applier is called only from handlers or restore.
- **Keyboard and touch:** every keyed control is a native `<button>` or `<input>`, so Enter/Space and a tap produce `click`, and radio arrow keys produce `change`.
- **The only `input` listener** is `#prism-opacity`, excluded by decision.
- **`stopPropagation`** appears only on `#a11y-btn`, `#about-btn`, `#budget-btn` and `#budget-close`, none of which carries a key.

## L4 — Is restore correct? **SOUND**

I wrote 19 hand-built hashes with predictions for each build before the first
run, plus 2 `?build=` cases: **40/40 as predicted** (after the instrument error
in §7). Covered:
- the brief's interacting case, `view=development&mode=infill&metric=industrial&detail=hood`:
  - public → `view=development&detail=hood`;
  - full → `view=development&mode=infill`;
- `metric=` alongside `mode=change`;
- Glass with value+lot;
- Industrial × 3yr × hood on full;
- empty values, a repeated key, a key from another view;
- internal view names (`glass`, `infill`), wrong case, a bare word;
- Services driver hand-off (`on=roadscost&colour=roads` → the colour is dropped because one service is on);
- `?build=full`/`?build=public` combined with a hash: the query survives the write.

**Reload loop:** nothing assigns `location.hash`, `location.href` or
`pushState`. There is no `href="#…"` anywhere, and the only `<a>` elements are
five absolute external links.

**Not measured:** a click made during the ~1 s restore window (before
`framePainted` or `temporalReady`) could be overridden when `applyUrlState`
resumes.

## L5 — Does the guard test what it claims? **UNSOUND for two classes**

### F1 — The walk and the restore share `offered()`, so a control it wrongly hides passes: **CONFIRMED**

- **Mutant:** `offered()` returns false for anything inside `#devmetric` or `#revcut`. It is a one-line change in a copy of the built page.
- **Control:** the mutant really breaks links.
  - `#view=development&metric=permits` → `#view=development` with `devMetric` `units`.
  - `#metric=residential` → no hash, and `metric` `revenue_per_acre`. The clean build keeps both.
- **The stock `verify-url-state.js` on the mutant (public):**
  - **All passed.**
  - The walk shrank from 31 to 26 round trips, and nothing checks that count.
- **The brief's suggested mutation (`#denom`) would NOT have shown this.** `#denom` is pinned by the hand-written `detail=grid&denom=lot&scale=linear` link, so it goes red by accident. Pinned that way: `denom`, `scale`, `detail`, Change's `window`, `on=none`, the Uses prisms, and the Lab cut on full.
- **Guarded only by the walk, so blind to this class:**
  - `#devmetric`, `#devdetail`, `#revcut`;
  - Development's window except `3yr`;
  - `#amenity` and `#ratio-denom` on full.
- **Remedy, validated.** Replace the four `offered` uses in the script (`screen`, `keysOf`, `clickKey`, the `views` list) with an independent `el.checkVisibility()`:
  - on the mutant: **6 FAILED, by name** (`round trip money > revcut:… -> #metric=residential`, and nonresidential and `devmetric:permits`, each twice), and the walk is back to 31;
  - on the clean public build: all passed, 31;
  - on the clean full build: all passed, 58.
  - The restore itself keeps `offered()`; only the guard must not share it.

### F2 — No check pins the link vocabulary, and the round trip is self-consistent under a rename: **CONFIRMED**

- **Mutant:** `URL_METRIC` maps `res_revenue_per_acre` to `"res"` instead of `"residential"`. Every shared residential link now silently lands on Total.
- **Stock verify, public: all passed.** The round trip wrote `metric=res` and read `metric=res` back. The Lab link checked on public expects to be dropped anyway.
- On full, the `view=lab&cut=residential` link would go red, by accident. That is from reading the code; I didn't run it (§7).
- **The §8 claim "the values are public names, not column names" holds only for `metric=` and `cut=`**, the two that pass through a map. Nine key contexts write internal state values verbatim:
  - `denom`, both `window`s, the dev `metric`, `amenity`, `on`, `colour`, the Ratio `denom`, and `exp`.
  - Renaming any of those internal values changes the link vocabulary with no signal.
  - "A column rename must not break one" is true. A state-value rename or retirement breaks one silently, and the verify stays green.

**Remedy direction (Peter's call on the policy half):**
1. A frozen list in the verify: every value in the §8 table, as a link that must restore to itself. The `lands` list already carries about 8 of them.
2. A one-line rule beside `URL_METRIC`: renaming or retiring a value adds an alias entry, never a silent drop.

### Coverage, as documented (not a finding)

The walk dedups by control identity per view, to a depth of 3. On full it
makes 58 trips; S203's handoff recorded 57, and both enumerations give 58
today. It never round-trips inside Glass:
- `metric-row`, `revcut`, `denom` and `coloradj` at either cell size: 10 combinations, 2 hand links;
- Infill with a non-default metric or window: 3 combinations, 0 links.

`urlHash()` writes each key independently, so the risk is limited to restore
ordering, which L4 covered for the interacting cases.

**`screen()` compares only title, view and controls.** L1's fingerprint found no
render-only difference to catch, so there is no evidence a richer compare is
needed. It would be cheap (two `innerText` reads) if Peter wants it.

**Channel:** the CI decision is pending, and it's recorded where a session will
see it: the `TODO.md` item and the S203 handoff §2/§4.

## L6 — Docs and claims: **WARN**

### F3 — `#devwindow`'s comment says `state.devWindow` "can't be stuck on" `long`; it starts there

- **What the code does:**
  - The `state` default has been `devWindow: "long"` since `6118795` (2026-07-27).
  - Before #608 the comment claimed "default is 5yr", which was already stale. #608 reworded it to "the URL hash only selects offered buttons" and kept the false conclusion.
- **Reachability:** `join_and_calculate` omits the `_long` columns when no long-window permits are passed, and `test_join_and_calculate.py:1343` asserts exactly that. So this is a supported output, not a corrupt one.
- **Measured on the public build with `_long` stripped:**
  - Development opens titled "New Housing Built (2009–2025)", and no window button is lit.
  - The choropleth column `new_units_per_acre_long` has values for 0 of 406 hoods, and every tooltip reads "no permit data".
  - `window=3yr` renders normally, with all 406.
- **Latent:** the served file carries `_long` for 406/406 hoods.
- **Fix:** one line at the `hasLongWindow` gate (`web/index.html`, after `state.hasLongWindow =`) that moves `state.devWindow` to `"5yr"` when `long` is absent, and correct the comment.

### Smaller claims

- **`web/index.html:727` says "`?build=public|full` overrides locally".** It overrides on the deployed site too (confirmed live), which is consistent with 07-22's "not access-controlled". The word "locally" misleads.
- **The CONTROLS_MATRIX §8 table does not bold `units`**, though it is the Development metric default and is never written.
- **"Clicks every reachable control"** (§8, the DECISIONS row) is true once per control per view, not per context. See the coverage note above.

Everything else in §8 and the DECISIONS row matches the code:
- write on change, read once, and a reload on edit;
- defaults omitted; the three traps;
- the fallback rule;
- `replaceState` with no history.

## §7 — What this run got wrong

1. **My L4 full-build pass ran the PUBLIC build.**
   - `open()` read a global `url` that the loop reassigned only at its END. The first "full" pass reported 3 mispredictions: Infill, Industrial and the Lab each landed where the public build lands.
   - I caught it because the results matched the public predictions exactly. Re-run with the reassignment moved: 19/19.
   - This is the class the skill warns about, a wrong server, in my own instrument.
2. **I planned the brief's `#denom` mutation first.** It would have gone red through a hand-written link and read as "the blind spot is covered". A mutation has to target a control that only the mechanism under test guards. The brief's example did not.
3. **I didn't run the full-build rename mutant.** "The Lab link would go red on full" is from reading the code.
4. **The fingerprint samples; it doesn't compare pixels.**
   - It covers 6 features per array-backed layer and 4 tooltips; layers with non-array data are not colour-sampled.
   - The hood panel's content (`openTemporal`) and the peek card are not in it.
   - "0 differences" is bounded by those fields.
5. **Same model as the builder.** L1–L4's SOUND verdicts are the claims most in need of a different reader. The instrument (`fp.js`) and its teeth check are described above so one can re-run it.

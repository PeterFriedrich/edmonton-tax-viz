

### `verify-services-panel.js` and `verify-ratio-denom.js` are red on the public build (FOUND 2026-09-24 S193)

Four checks fail on master as well as on branches: *"transit / bike / transitcost /
bikecost: the panel opens and is not empty — 0 rows"*. Those services are
full-only (`SERVICES[*].pub` false), so the public build has no rows to show. It
is the missing build gate `tools/profiling/README.md` convention 1 describes.
The script is not in CI, which is why nobody saw it. Fix: gate those four on
`FULL_BUILD` and print `PARTIAL`, the way `verify-transport-cost.js` does.

`verify-ratio-denom.js` has the same defect: *"ratio: picker shown"* fails on
the public build, where the denominator picker is full-only by design
(`ratioDenomShow` requires `FULL_BUILD`). It passes 42/42 on the full build.

**CLOSED 2026-09-24 (S194):** both scripts read `FULL_BUILD`. `verify-services-panel.js` skips §1–3 on a public URL (its §4 already covers the three public layers) and prints `PARTIAL`. `verify-ratio-denom.js` asserts the picker matches the build in both directions, skips the fire §4–9 on public, and prints `COMPLETE`/`PARTIAL`. The public run had been passing ~20 fire checks by JS-clicking the hidden picker. Falsified: ungating `ratioDenomShow` turns the public run red.

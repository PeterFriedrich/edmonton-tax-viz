# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,649-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (331 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 703–707 |  |
| `HOME` | 708–708 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 709–722 |  |
| `WINDOWS` | 723–748 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 749–758 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 759–763 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 764–839 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 840–842 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 843–844 |  |
| `METRICS` | 845–947 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 948–964 |  |
| `RATIO_DENOMS` | 965–998 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 999–999 |  |
| `ratioOf` | 1000–1000 |  |
| `ratioKept` | 1001–1022 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1023–1033 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1034–1061 |  |
| `dominantUse` | 1062–1103 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1104–1254 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1255–1350 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1351–1355 | the Lab: a container for unfinished lenses |
| `inLab` | 1356–1357 |  |
| `DEVIATION_TITLES` | 1358–1362 |  |
| `deviationTitle` | 1363–1368 |  |
| `deviationKind` | 1369–1371 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1372–1379 |  |
| `changeBlurb` | 1380–1397 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1398–1410 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1411–1423 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1424–1432 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1433–1441 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1442–1447 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1448–1455 |  |
| `infillAmenityBlurb` | 1456–1469 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1470–1481 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1482–1487 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1488–1546 |  |
| `setBlurb` | 1547–1559 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1560–1575 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1576–1593 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1594–1600 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1601–1614 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1615–1615 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1616–1630 |  |
| `fmtMB` | 1631–1641 |  |
| `showGridBusy` | 1642–1664 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1665–1681 |  |
| `loadGridData` | 1682–1735 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1736–1789 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1790–1814 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1815–1846 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1847–1847 |  |
| `gridFetches` | 1848–1874 |  |
| `RAMPS` | 1875–1915 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1916–1922 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1923–1928 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1929–1929 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1930–1936 |  |
| `AMENITY_BANDS` | 1937–1938 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1939–1941 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1942–1947 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1948–1962 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1963–1968 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1969–1987 |  |
| `gridScale` | 1988–2008 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2009–2015 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2016–2027 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2028–2030 |  |
| `quantile` | 2031–2045 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2046–2080 |  |
| `moneyBlurb` | 2081–2092 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2093–2105 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2106–2184 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2185–2185 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2186–2212 |  |
| `failLoading` | 2213–2226 |  |
| `hideLoading` | 2227–2282 |  |
| `topRings` | 2283–2299 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2300–2325 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2326–2326 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2327–2339 |  |
| `svcT` | 2340–2348 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2349–2362 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2363–2363 |  |
| `fmtFire` | 2364–2365 |  |
| `fmtTransit` | 2366–2367 |  |
| `fmtBike` | 2368–2380 |  |
| `fmtRoadM` | 2381–2394 |  |
| `fmtResShare` | 2395–2397 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2398–2403 |  |
| `fmtRoadsCost` | 2404–2408 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2409–2410 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2411–2412 |  |
| `fmtBikeCost` | 2413–2424 |  |
| `servicePlaneLayer` | 2425–2457 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2458–2467 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2468–2473 |  |
| `DEV_IND_TOTAL` | 2474–2476 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2477–2482 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2483–2487 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2488–2493 |  |
| `devGridOfferable` | 2494–2495 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2496–2496 |  |
| `devCol` | 2497–2497 |  |
| `_devScale` | 2498–2498 |  |
| `devScale` | 2499–2505 |  |
| `devT` | 2506–2509 |  |
| `developmentPlaneLayer` | 2510–2526 |  |
| `fmtDev` | 2527–2542 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2543–2548 |  |
| `DEV_GRID_IND_N` | 2549–2549 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2550–2552 |  |
| `devGridScale` | 2553–2579 |  |
| `devGridLayer` | 2580–2628 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2629–2630 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2631–2638 |  |
| `_infillStats` | 2639–2639 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2640–2657 |  |
| `_infillRaw` | 2658–2660 |  |
| `infillScore` | 2661–2676 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2677–2678 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2679–2696 |  |
| `INFILL_CENTER` | 2697–2697 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2698–2698 |  |
| `INFILL_NEG` | 2699–2699 |  |
| `infillColorAt` | 2700–2704 |  |
| `infillPlaneLayer` | 2705–2726 |  |
| `fmtFar` | 2727–2736 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2737–2737 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2738–2792 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2793–2800 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2801–2815 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2816–2836 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2837–2837 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2838–2852 |  |
| `chgT` | 2853–2862 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2863–2893 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2894–2982 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2983–2990 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2991–2991 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2992–2999 |  |
| `deviationRate` | 3000–3042 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3043–3043 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3044–3073 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3074–3080 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3081–3092 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3093–3096 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3097–3101 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3102–3112 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3113–3128 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3129–3160 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3161–3185 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3186–3238 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3239–3243 |  |
| `bandHover` | 3244–3252 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3253–3355 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3356–3363 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3364–3365 |  |
| `glassInstBandLayers` | 3366–3406 |  |
| `ratioInstBandLayers` | 3407–3434 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3435–3447 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3448–3449 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3450–3451 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3452–3452 |  |
| `deviationStats` | 3453–3497 |  |
| `deviationOf` | 3498–3499 |  |
| `deviationT` | 3500–3510 |  |
| `fmtDeviation` | 3511–3532 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3533–3576 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3577–3663 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3664–3686 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3687–3687 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3688–3708 |  |
| `ensureFireStations` | 3709–3724 |  |
| `TRANSIT_STATION_COLOR` | 3725–3725 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3726–3743 |  |
| `ensureTransitStations` | 3744–3759 |  |
| `TRANSIT_LINE_COLOR` | 3760–3760 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3761–3777 |  |
| `ensureLrtLines` | 3778–3794 |  |
| `BIKE_LINE_COLOR` | 3795–3795 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3796–3812 |  |
| `ensureBikeLines` | 3813–3870 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3871–3871 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3872–3875 |  |
| `BOUNDARY_COLOR` | 3876–3885 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3886–3886 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3887–3899 |  |
| `referenceSplit` | 3900–3927 |  |
| `referenceUnderLayers` | 3928–3962 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3963–3979 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3980–3999 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4000–4013 |  |
| `servicesBlurb` | 4014–4025 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4026–4049 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4050–4060 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4061–4112 |  |
| `REF_TIERS` | 4113–4134 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4135–4142 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4143–4145 |  |
| `placeAnchors` | 4146–4169 |  |
| `labelPool` | 4170–4177 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4178–4231 |  |
| `CHROME_IDS` | 4232–4236 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4237–4255 |  |
| `visibleLabels` | 4256–4310 |  |
| `labelLayer` | 4311–4363 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4364–4404 |  |
| `_ratioScales` | 4405–4405 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4406–4421 |  |
| `ratioT` | 4422–4444 |  |
| `zMatrix` | 4445–4449 |  |
| `buildLayers` | 4450–4474 |  |
| `flattenDuringEase` | 4475–4499 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4500–4809 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4810–4839 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4840–4849 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4850–4852 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4853–4884 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4885–4891 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4892–4899 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4900–4904 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4905–4915 |  |
| `revenueLens` | 4916–4917 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4918–4950 |  |
| `SVC_COST_BASES` | 4951–4968 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4969–4977 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4978–4987 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4988–4990 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4991–4997 |  |
| `svcRank` | 4998–5002 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5003–5009 |  |
| `svcDriverReading` | 5010–5030 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5031–5031 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5032–5035 |  |
| `servicePanelFor` | 5036–5040 |  |
| `ratioPanelFor` | 5041–5064 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5065–5069 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5070–5087 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5088–5119 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5120–5125 |  |
| `sparklineSvg` | 5126–5141 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5142–5201 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5202–5207 | Development history: new supply per year |
| `devHistKey` | 5208–5217 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5218–5222 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5223–5223 |  |
| `devHistVerb` | 5224–5229 |  |
| `devHistoryFor` | 5230–5268 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5269–5288 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5289–5308 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5309–5344 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5345–5347 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5348–5411 |  |
| `syncTemporalPos` | 5412–5438 |  |
| `openTemporal` | 5439–5476 |  |
| `renderRevenueMix` | 5477–5546 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5547–5621 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5622–5679 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5680–5683 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5684–5734 |  |
| `syncPinnedPanel` | 5735–5768 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5769–5784 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5785–5802 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5803–5850 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5851–5856 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5857–5904 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5905–5921 |  |
| `temporalClick` | 5922–5976 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 5977–5984 | neighbourhood search |
| `searchMatches` | 5985–5999 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6000–6028 |  |
| `openSearch` | 6029–6041 |  |
| `closeSearch` | 6042–6060 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6061–6073 |  |
| `closeGuide` | 6074–6081 |  |
| `maybeAutoGuide` | 6082–6098 |  |
| `flyToHood` | 6099–6118 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6119–6137 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6138–6206 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6207–6584 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6585–6674 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6675–6675 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6676–6694 |  |
| `syncMetricButtons` | 6695–6718 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6719–6725 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6726–6739 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6740–6781 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6782–6824 |  |
| `toggleBudgetPanel` | 6825–6850 |  |
| `syncMillRates` | 6851–6883 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6884–6904 |  |
| `applyColorAdjust` | 6905–6925 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6926–6938 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6939–6953 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6954–6971 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6972–6988 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6989–7010 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7011–7027 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7028–7267 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7268–7278 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7279–7292 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7293–7301 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7302–7312 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7313–7324 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7325–7337 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7338–7358 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7359–7406 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7407–7412 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7413–7434 |  |
| `applyMoneyDetail` | 7435–7459 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7460–7471 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7472–7479 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7480–7498 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7499–7509 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7510–7517 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7518–7534 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7535–7548 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7549–7559 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7560–7803 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7804–7813 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7814–7827 |  |
| `applySvcDriver` | 7828–7860 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7861–7863 |  |
| `urlHash` | 7864–7904 |  |
| `shareLink` | 7905–7913 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7914–7925 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7926–7932 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7933–8005 |  |
| `restoreFromHash` | 8006–8024 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8025–8649 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1058 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 126 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 121 | 63% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 96 | 43% |
| neighbourhood search | 11 | 36% |
| loading overlay | 56 | 34% |
| two tiers, answering two different questions | 29 | 31% |
| Development history: new supply per year | 111 | 30% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| the same doubt, at 100 m | 61 | 26% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 221 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 112 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 69 | 0% |

## Element ids (143) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#loading` | 22 |
| `#loading-box` | 23 |
| `#loading-title` | 34 |
| `#loading-blurb` | 35 |
| `#loading-spinner` | 36 |
| `#loading-text` | 37 |
| `#loading-retry` | 38 |
| `#banner` | 42 |
| `#gridbusy` | 53 |
| `#gridbusy-spinner` | 54 |
| `#gridbusy-text` | 56 |
| `#gridbusy-size` | 57 |
| `#title` | 61 |
| `#title-h` | 62 |
| `#title-p` | 65 |
| `#search` | 75 |
| `#search-btn` | 76 |
| `#search-box` | 79 |
| `#search-input` | 80 |
| `#search-close` | 84 |
| `#search-list` | 86 |
| `#guide-btn` | 94 |
| `#guide` | 96 |
| `#guide-close` | 97 |
| `#guide-ask` | 98 |
| `#guide-show` | 99 |
| `#guide-body` | 102 |
| `#temporal` | 121 |
| `#temporal-close` | 122 |
| `#temporal-name` | 123 |
| `#temporal-body` | 130 |
| `#temporal-chart` | 131 |
| `#temporal-read` | 132 |
| `#temporal-note` | 133 |
| `#temporal-hint` | 137 |
| `#millrates` | 153 |
| `#mill-head` | 154 |
| `#mill-rows` | 155 |
| `#mill-note` | 156 |
| `#budget` | 170 |
| `#budget-close` | 177 |
| `#budget-head` | 178 |
| `#budget-body` | 183 |
| `#budget-rows` | 184 |
| `#budget-other-hd` | 185 |
| `#budget-other` | 186 |
| `#budget-note` | 187 |
| `#peek` | 202 |
| `#peek-name` | 203 |
| `#peek-read` | 204 |
| `#peek-go` | 205 |
| `#controls` | 208 |
| `#toggle` | 221 |
| `#metric-row` | 222 |
| `#revcut` | 226 |
| `#moneymode` | 231 |
| `#views` | 237 |
| `#optpanel` | 251 |
| `#opt-fold` | 252 |
| `#opt-caret` | 252 |
| `#opt-body` | 253 |
| `#layers` | 254 |
| `#chgwindow-hd` | 255 |
| `#chgwindow` | 256 |
| `#labpick-hd` | 265 |
| `#labpick` | 266 |
| `#labcut-hd` | 267 |
| `#labcut` | 268 |
| `#moneydetail-hd` | 273 |
| `#moneydetail` | 274 |
| `#amenity-hd` | 299 |
| `#amenity` | 300 |
| `#amenity-lrt-row` | 301 |
| `#amenity-lrt-on` | 302 |
| `#amenity-school-row` | 304 |
| `#amenity-school-on` | 305 |
| `#uses-prisms-hd` | 308 |
| `#uses-prisms` | 309 |
| `#uses-prisms-on` | 311 |
| `#devmode-hd` | 314 |
| `#devmode` | 315 |
| `#devmetric-hd` | 319 |
| `#devmetric` | 320 |
| `#devwindow-hd` | 325 |
| `#devwindow` | 326 |
| `#devdetail-hd` | 331 |
| `#devdetail` | 332 |
| `#prism-hd` | 336 |
| `#prism-row` | 337 |
| `#prism-opacity` | 339 |
| `#prism-opacity-val` | 340 |
| `#services-hd` | 342 |
| `#services` | 343 |
| `#denom-hd` | 442 |
| `#denom` | 443 |
| `#ratio-denom-hd` | 447 |
| `#ratio-denom` | 448 |
| `#hoodmode` | 458 |
| `#hoodmode-btn` | 459 |
| `#coloradj` | 471 |
| `#coloradj-btn` | 472 |
| `#budget-pod` | 479 |
| `#budget-btn` | 480 |
| `#share` | 487 |
| `#share-btn` | 488 |
| `#a11y` | 491 |
| `#a11y-btn` | 492 |
| `#a11y-menu` | 493 |
| `#palette` | 495 |
| `#labels-on` | 502 |
| `#reference-on` | 510 |
| `#about` | 515 |
| `#about-btn` | 516 |
| `#about-menu` | 517 |
| `#about-src-roads` | 529 |
| `#about-src-services` | 530 |
| `#about-vintage` | 558 |
| `#about-build` | 562 |
| `#about-lot-acres` | 567 |
| `#about-modelled-roads` | 578 |
| `#about-modelled` | 600 |
| `#about-budget` | 610 |
| `#about-budget-lead` | 612 |
| `#about-budget-rows` | 613 |
| `#about-budget-note` | 614 |
| `#about-updated` | 626 |
| `#botleft` | 630 |
| `#compass` | 631 |
| `#rot-ccw` | 632 |
| `#tonorth` | 639 |
| `#needle` | 641 |
| `#rot-cw` | 646 |
| `#viewbtns` | 654 |
| `#recenter` | 656 |
| `#center2d` | 657 |
| `#legend` | 659 |
| `#legend-label` | 660 |
| `#legend-min` | 662 |
| `#legend-max` | 662 |
| `#legend-cats` | 664 |
| `#revmix` | 5496 |
| `#svccost` | 5590 |

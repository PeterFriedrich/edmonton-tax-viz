# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,029-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (311 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 643–647 |  |
| `HOME` | 648–648 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 649–662 |  |
| `WINDOWS` | 663–688 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 689–698 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 699–703 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 704–779 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 780–782 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 783–784 |  |
| `METRICS` | 785–887 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 888–904 |  |
| `RATIO_DENOMS` | 905–938 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 939–939 |  |
| `ratioOf` | 940–940 |  |
| `ratioKept` | 941–962 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 963–973 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 974–1001 |  |
| `dominantUse` | 1002–1043 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1044–1194 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1195–1290 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1291–1295 | the Lab: a container for unfinished lenses |
| `inLab` | 1296–1297 |  |
| `DEVIATION_TITLES` | 1298–1302 |  |
| `deviationTitle` | 1303–1308 |  |
| `deviationKind` | 1309–1311 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1312–1319 |  |
| `changeBlurb` | 1320–1337 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1338–1350 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1351–1363 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1364–1372 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1373–1381 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1382–1387 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1388–1395 |  |
| `infillAmenityBlurb` | 1396–1409 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1410–1421 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1422–1427 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1428–1486 |  |
| `setBlurb` | 1487–1499 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1500–1515 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1516–1533 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1534–1540 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1541–1554 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1555–1555 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1556–1570 |  |
| `fmtMB` | 1571–1581 |  |
| `showGridBusy` | 1582–1604 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1605–1621 |  |
| `loadGridData` | 1622–1675 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1676–1729 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1730–1754 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1755–1786 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1787–1787 |  |
| `gridFetches` | 1788–1812 |  |
| `RAMPS` | 1813–1853 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1854–1860 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1861–1866 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1867–1867 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1868–1874 |  |
| `AMENITY_BANDS` | 1875–1876 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1877–1879 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1880–1885 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1886–1900 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1901–1906 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1907–1925 |  |
| `gridScale` | 1926–1946 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1947–1953 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1954–1965 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1966–1968 |  |
| `quantile` | 1969–1983 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1984–2018 |  |
| `moneyBlurb` | 2019–2030 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2031–2043 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2044–2122 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2123–2123 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2124–2150 |  |
| `failLoading` | 2151–2164 |  |
| `hideLoading` | 2165–2219 |  |
| `topRings` | 2220–2236 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2237–2262 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2263–2263 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2264–2276 |  |
| `svcT` | 2277–2285 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2286–2299 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2300–2300 |  |
| `fmtFire` | 2301–2302 |  |
| `fmtTransit` | 2303–2304 |  |
| `fmtBike` | 2305–2317 |  |
| `fmtRoadM` | 2318–2331 |  |
| `fmtResShare` | 2332–2334 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2335–2340 |  |
| `fmtRoadsCost` | 2341–2345 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2346–2347 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2348–2349 |  |
| `fmtBikeCost` | 2350–2361 |  |
| `servicePlaneLayer` | 2362–2394 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2395–2404 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2405–2410 |  |
| `DEV_IND_TOTAL` | 2411–2413 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2414–2419 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2420–2424 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2425–2430 |  |
| `devGridOfferable` | 2431–2432 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2433–2433 |  |
| `devCol` | 2434–2434 |  |
| `_devScale` | 2435–2435 |  |
| `devScale` | 2436–2442 |  |
| `devT` | 2443–2446 |  |
| `developmentPlaneLayer` | 2447–2463 |  |
| `fmtDev` | 2464–2479 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2480–2485 |  |
| `DEV_GRID_IND_N` | 2486–2486 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2487–2489 |  |
| `devGridScale` | 2490–2516 |  |
| `devGridLayer` | 2517–2565 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2566–2567 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2568–2575 |  |
| `_infillStats` | 2576–2576 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2577–2594 |  |
| `_infillRaw` | 2595–2597 |  |
| `infillScore` | 2598–2613 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2614–2615 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2616–2633 |  |
| `INFILL_CENTER` | 2634–2634 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2635–2635 |  |
| `INFILL_NEG` | 2636–2636 |  |
| `infillColorAt` | 2637–2641 |  |
| `infillPlaneLayer` | 2642–2663 |  |
| `fmtFar` | 2664–2673 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2674–2674 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2675–2729 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2730–2737 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2738–2752 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2753–2773 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2774–2774 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2775–2789 |  |
| `chgT` | 2790–2799 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2800–2830 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2831–2919 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2920–2927 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2928–2928 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2929–2936 |  |
| `deviationRate` | 2937–2979 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2980–2980 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2981–3010 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3011–3017 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3018–3029 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3030–3033 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3034–3038 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3039–3049 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3050–3065 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3066–3097 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3098–3122 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3123–3175 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3176–3180 |  |
| `bandHover` | 3181–3189 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3190–3286 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3287–3294 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3295–3296 |  |
| `glassInstBandLayers` | 3297–3337 |  |
| `ratioInstBandLayers` | 3338–3365 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3366–3378 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3379–3380 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3381–3382 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3383–3383 |  |
| `deviationStats` | 3384–3428 |  |
| `deviationOf` | 3429–3430 |  |
| `deviationT` | 3431–3441 |  |
| `fmtDeviation` | 3442–3463 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3464–3507 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3508–3594 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3595–3617 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3618–3618 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3619–3639 |  |
| `ensureFireStations` | 3640–3655 |  |
| `TRANSIT_STATION_COLOR` | 3656–3656 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3657–3674 |  |
| `ensureTransitStations` | 3675–3690 |  |
| `TRANSIT_LINE_COLOR` | 3691–3691 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3692–3708 |  |
| `ensureLrtLines` | 3709–3725 |  |
| `BIKE_LINE_COLOR` | 3726–3726 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3727–3743 |  |
| `ensureBikeLines` | 3744–3801 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3802–3802 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3803–3806 |  |
| `BOUNDARY_COLOR` | 3807–3816 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3817–3817 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3818–3830 |  |
| `referenceSplit` | 3831–3858 |  |
| `referenceUnderLayers` | 3859–3893 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3894–3910 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3911–3930 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3931–3944 |  |
| `servicesBlurb` | 3945–3956 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3957–3980 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3981–3991 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3992–4043 |  |
| `REF_TIERS` | 4044–4065 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4066–4073 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4074–4076 |  |
| `placeAnchors` | 4077–4100 |  |
| `labelPool` | 4101–4108 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4109–4162 |  |
| `CHROME_IDS` | 4163–4167 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4168–4186 |  |
| `visibleLabels` | 4187–4241 |  |
| `labelLayer` | 4242–4278 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4279–4279 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4280–4295 |  |
| `ratioT` | 4296–4318 |  |
| `zMatrix` | 4319–4323 |  |
| `buildLayers` | 4324–4347 |  |
| `flattenDuringEase` | 4348–4372 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4373–4682 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4683–4712 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4713–4722 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4723–4725 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4726–4757 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4758–4764 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4765–4772 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4773–4777 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4778–4788 |  |
| `revenueLens` | 4789–4790 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4791–4823 |  |
| `SVC_COST_BASES` | 4824–4841 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4842–4850 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4851–4866 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4867–4869 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4870–4876 |  |
| `svcRank` | 4877–4881 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4882–4888 |  |
| `svcDriverReading` | 4889–4909 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4910–4910 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4911–4914 |  |
| `servicePanelFor` | 4915–4935 |  |
| `hoodPanelLens` | 4936–4939 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4940–4957 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4958–4989 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4990–4995 |  |
| `sparklineSvg` | 4996–5011 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5012–5071 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5072–5077 | Development history: new supply per year |
| `devHistKey` | 5078–5087 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5088–5092 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5093–5093 |  |
| `devHistVerb` | 5094–5099 |  |
| `devHistoryFor` | 5100–5121 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5122–5141 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5142–5161 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5162–5197 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5198–5200 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5201–5264 |  |
| `syncTemporalPos` | 5265–5291 |  |
| `openTemporal` | 5292–5326 |  |
| `renderRevenueMix` | 5327–5393 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5394–5473 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5474–5477 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5478–5528 |  |
| `syncPinnedPanel` | 5529–5558 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5559–5574 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5575–5592 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5593–5640 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5641–5646 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5647–5693 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5694–5710 |  |
| `temporalClick` | 5711–5768 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5769–5837 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5838–6218 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6219–6300 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6301–6301 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6302–6320 |  |
| `syncMetricButtons` | 6321–6344 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6345–6351 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6352–6365 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6366–6407 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6408–6450 |  |
| `toggleBudgetPanel` | 6451–6476 |  |
| `syncMillRates` | 6477–6509 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6510–6530 |  |
| `applyColorAdjust` | 6531–6551 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6552–6564 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6565–6579 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6580–6597 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6598–6614 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6615–6636 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6637–6653 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6654–6893 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6894–6904 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6905–6918 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6919–6927 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6928–6938 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6939–6950 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6951–6963 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6964–6984 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6985–7032 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7033–7038 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7039–7060 |  |
| `applyMoneyDetail` | 7061–7085 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7086–7097 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7098–7105 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7106–7124 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7125–7135 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7136–7143 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7144–7160 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7161–7174 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7175–7185 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7186–7429 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7430–7439 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7440–7453 |  |
| `applySvcDriver` | 7454–7467 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7468–8029 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (971 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 119 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 34 | 26% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 194 | 24% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 216 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 59 | 0% |

## Element ids (128) — the control surface

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
| `#temporal` | 75 |
| `#temporal-close` | 76 |
| `#temporal-name` | 77 |
| `#temporal-body` | 84 |
| `#temporal-chart` | 85 |
| `#temporal-read` | 86 |
| `#temporal-note` | 87 |
| `#temporal-hint` | 91 |
| `#millrates` | 107 |
| `#mill-head` | 108 |
| `#mill-rows` | 109 |
| `#mill-note` | 110 |
| `#budget` | 124 |
| `#budget-close` | 131 |
| `#budget-head` | 132 |
| `#budget-body` | 137 |
| `#budget-rows` | 138 |
| `#budget-other-hd` | 139 |
| `#budget-other` | 140 |
| `#budget-note` | 141 |
| `#peek` | 156 |
| `#peek-name` | 157 |
| `#peek-read` | 158 |
| `#peek-go` | 159 |
| `#controls` | 162 |
| `#toggle` | 175 |
| `#metric-row` | 176 |
| `#revcut` | 180 |
| `#moneymode` | 185 |
| `#views` | 191 |
| `#optpanel` | 205 |
| `#opt-fold` | 206 |
| `#opt-caret` | 206 |
| `#opt-body` | 207 |
| `#layers` | 208 |
| `#chgwindow-hd` | 209 |
| `#chgwindow` | 210 |
| `#labpick-hd` | 219 |
| `#labpick` | 220 |
| `#labcut-hd` | 221 |
| `#labcut` | 222 |
| `#moneydetail-hd` | 227 |
| `#moneydetail` | 228 |
| `#amenity-hd` | 253 |
| `#amenity` | 254 |
| `#amenity-lrt-row` | 255 |
| `#amenity-lrt-on` | 256 |
| `#amenity-school-row` | 258 |
| `#amenity-school-on` | 259 |
| `#uses-prisms-hd` | 262 |
| `#uses-prisms` | 263 |
| `#uses-prisms-on` | 265 |
| `#devmode-hd` | 268 |
| `#devmode` | 269 |
| `#devmetric-hd` | 273 |
| `#devmetric` | 274 |
| `#devwindow-hd` | 279 |
| `#devwindow` | 280 |
| `#devdetail-hd` | 285 |
| `#devdetail` | 286 |
| `#prism-hd` | 290 |
| `#prism-row` | 291 |
| `#prism-opacity` | 293 |
| `#prism-opacity-val` | 294 |
| `#services-hd` | 296 |
| `#services` | 297 |
| `#denom-hd` | 396 |
| `#denom` | 397 |
| `#ratio-denom-hd` | 401 |
| `#ratio-denom` | 402 |
| `#hoodmode` | 412 |
| `#hoodmode-btn` | 413 |
| `#coloradj` | 425 |
| `#coloradj-btn` | 426 |
| `#budget-pod` | 433 |
| `#budget-btn` | 434 |
| `#a11y` | 438 |
| `#a11y-btn` | 439 |
| `#a11y-menu` | 440 |
| `#palette` | 442 |
| `#labels-on` | 449 |
| `#reference-on` | 457 |
| `#about` | 462 |
| `#about-btn` | 463 |
| `#about-menu` | 464 |
| `#about-src-roads` | 476 |
| `#about-src-services` | 477 |
| `#about-vintage` | 505 |
| `#about-build` | 509 |
| `#about-modelled-roads` | 523 |
| `#about-modelled` | 541 |
| `#about-budget` | 551 |
| `#about-budget-lead` | 553 |
| `#about-budget-rows` | 554 |
| `#about-budget-note` | 555 |
| `#about-updated` | 566 |
| `#botleft` | 570 |
| `#compass` | 571 |
| `#rot-ccw` | 572 |
| `#tonorth` | 579 |
| `#needle` | 581 |
| `#rot-cw` | 586 |
| `#viewbtns` | 594 |
| `#recenter` | 596 |
| `#center2d` | 597 |
| `#legend` | 599 |
| `#legend-label` | 600 |
| `#legend-min` | 602 |
| `#legend-max` | 602 |
| `#legend-cats` | 604 |
| `#revmix` | 5346 |
| `#svccost` | 5437 |

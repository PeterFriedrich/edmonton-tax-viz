# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,069-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (309 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 642–646 |  |
| `HOME` | 647–647 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 648–661 |  |
| `WINDOWS` | 662–687 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 688–697 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 698–702 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 703–778 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 779–781 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 782–783 |  |
| `METRICS` | 784–914 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 915–931 |  |
| `RATIO_DENOMS` | 932–965 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 966–966 |  |
| `ratioOf` | 967–967 |  |
| `ratioKept` | 968–989 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 990–1000 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1001–1028 |  |
| `dominantUse` | 1029–1070 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1071–1241 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1242–1337 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1338–1342 | the Lab: a container for unfinished lenses |
| `inLab` | 1343–1344 |  |
| `DEVIATION_TITLES` | 1345–1349 |  |
| `deviationTitle` | 1350–1355 |  |
| `deviationKind` | 1356–1358 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1359–1364 |  |
| `changeBlurb` | 1365–1389 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1390–1411 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1412–1424 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1425–1436 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1437–1442 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1443–1448 |  |
| `infillAmenityBlurb` | 1449–1462 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1463–1474 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1475–1480 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1481–1539 |  |
| `setBlurb` | 1540–1554 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `withColourClause` | 1555–1572 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1573–1579 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1580–1593 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1594–1594 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1595–1609 |  |
| `fmtMB` | 1610–1620 |  |
| `showGridBusy` | 1621–1643 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1644–1660 |  |
| `loadGridData` | 1661–1714 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1715–1768 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1769–1793 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1794–1825 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1826–1826 |  |
| `gridFetches` | 1827–1851 |  |
| `RAMPS` | 1852–1892 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1893–1899 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1900–1905 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1906–1906 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1907–1913 |  |
| `AMENITY_BANDS` | 1914–1915 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1916–1918 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1919–1924 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1925–1939 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1940–1945 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1946–1964 |  |
| `gridScale` | 1965–1985 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1986–1992 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1993–2004 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2005–2007 |  |
| `quantile` | 2008–2022 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2023–2055 |  |
| `moneyBlurb` | 2056–2060 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2061–2073 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2074–2152 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2153–2153 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2154–2180 |  |
| `failLoading` | 2181–2194 |  |
| `hideLoading` | 2195–2249 |  |
| `topRings` | 2250–2266 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2267–2292 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2293–2293 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2294–2306 |  |
| `svcT` | 2307–2315 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2316–2329 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2330–2330 |  |
| `fmtFire` | 2331–2332 |  |
| `fmtTransit` | 2333–2334 |  |
| `fmtBike` | 2335–2347 |  |
| `fmtRoadM` | 2348–2361 |  |
| `fmtResShare` | 2362–2364 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2365–2370 |  |
| `fmtRoadsCost` | 2371–2375 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2376–2377 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2378–2379 |  |
| `fmtBikeCost` | 2380–2391 |  |
| `servicePlaneLayer` | 2392–2424 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2425–2434 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2435–2440 |  |
| `DEV_IND_TOTAL` | 2441–2443 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2444–2449 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2450–2454 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2455–2460 |  |
| `devGridOfferable` | 2461–2462 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2463–2463 |  |
| `devCol` | 2464–2464 |  |
| `_devScale` | 2465–2465 |  |
| `devScale` | 2466–2472 |  |
| `devT` | 2473–2476 |  |
| `developmentPlaneLayer` | 2477–2493 |  |
| `fmtDev` | 2494–2509 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2510–2515 |  |
| `DEV_GRID_IND_N` | 2516–2516 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2517–2519 |  |
| `devGridScale` | 2520–2546 |  |
| `devGridLayer` | 2547–2595 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2596–2597 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2598–2605 |  |
| `_infillStats` | 2606–2606 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2607–2624 |  |
| `_infillRaw` | 2625–2627 |  |
| `infillScore` | 2628–2643 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2644–2645 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2646–2663 |  |
| `INFILL_CENTER` | 2664–2664 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2665–2665 |  |
| `INFILL_NEG` | 2666–2666 |  |
| `infillColorAt` | 2667–2671 |  |
| `infillPlaneLayer` | 2672–2693 |  |
| `fmtFar` | 2694–2703 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2704–2704 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2705–2759 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2760–2767 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2768–2782 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2783–2803 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2804–2804 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2805–2819 |  |
| `chgT` | 2820–2829 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2830–2860 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2861–2949 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2950–2957 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2958–2958 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2959–2966 |  |
| `deviationRate` | 2967–3009 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3010–3010 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3011–3040 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3041–3047 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3048–3059 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3060–3063 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3064–3068 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3069–3079 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3080–3095 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3096–3127 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3128–3152 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3153–3205 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3206–3210 |  |
| `bandHover` | 3211–3219 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3220–3316 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3317–3324 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3325–3326 |  |
| `glassInstBandLayers` | 3327–3367 |  |
| `ratioInstBandLayers` | 3368–3395 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3396–3408 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3409–3410 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3411–3412 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3413–3413 |  |
| `deviationStats` | 3414–3458 |  |
| `deviationOf` | 3459–3460 |  |
| `deviationT` | 3461–3471 |  |
| `fmtDeviation` | 3472–3493 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3494–3537 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3538–3624 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3625–3647 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3648–3648 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3649–3669 |  |
| `ensureFireStations` | 3670–3685 |  |
| `TRANSIT_STATION_COLOR` | 3686–3686 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3687–3704 |  |
| `ensureTransitStations` | 3705–3720 |  |
| `TRANSIT_LINE_COLOR` | 3721–3721 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3722–3738 |  |
| `ensureLrtLines` | 3739–3755 |  |
| `BIKE_LINE_COLOR` | 3756–3756 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3757–3773 |  |
| `ensureBikeLines` | 3774–3831 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3832–3832 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3833–3836 |  |
| `BOUNDARY_COLOR` | 3837–3846 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3847–3847 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3848–3860 |  |
| `referenceSplit` | 3861–3888 |  |
| `referenceUnderLayers` | 3889–3923 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3924–3940 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3941–3960 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3961–3973 |  |
| `servicesBlurb` | 3974–3991 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3992–4015 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4016–4026 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4027–4078 |  |
| `REF_TIERS` | 4079–4100 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4101–4108 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4109–4111 |  |
| `placeAnchors` | 4112–4135 |  |
| `labelPool` | 4136–4143 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4144–4197 |  |
| `CHROME_IDS` | 4198–4202 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4203–4221 |  |
| `visibleLabels` | 4222–4276 |  |
| `labelLayer` | 4277–4313 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4314–4314 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4315–4330 |  |
| `ratioT` | 4331–4353 |  |
| `zMatrix` | 4354–4358 |  |
| `buildLayers` | 4359–4382 |  |
| `flattenDuringEase` | 4383–4407 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4408–4717 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4718–4747 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4748–4757 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4758–4760 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4761–4792 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4793–4799 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4800–4807 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4808–4812 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4813–4823 |  |
| `revenueLens` | 4824–4825 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4826–4858 |  |
| `SVC_COST_BASES` | 4859–4876 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4877–4885 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4886–4901 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4902–4904 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4905–4911 |  |
| `svcRank` | 4912–4916 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4917–4923 |  |
| `svcDriverReading` | 4924–4944 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4945–4945 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4946–4949 |  |
| `servicePanelFor` | 4950–4970 |  |
| `hoodPanelLens` | 4971–4974 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4975–4992 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4993–5024 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5025–5030 |  |
| `sparklineSvg` | 5031–5046 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5047–5106 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5107–5112 | Development history: new supply per year |
| `devHistKey` | 5113–5122 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5123–5127 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5128–5128 |  |
| `devHistVerb` | 5129–5134 |  |
| `devHistoryFor` | 5135–5156 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5157–5176 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5177–5196 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5197–5232 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5233–5235 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5236–5299 |  |
| `syncTemporalPos` | 5300–5326 |  |
| `openTemporal` | 5327–5361 |  |
| `renderRevenueMix` | 5362–5428 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5429–5508 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5509–5512 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5513–5563 |  |
| `syncPinnedPanel` | 5564–5593 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5594–5609 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5610–5627 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5628–5675 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5676–5681 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5682–5728 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5729–5745 |  |
| `temporalClick` | 5746–5803 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5804–5872 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5873–6253 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6254–6335 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6336–6336 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6337–6355 |  |
| `syncMetricButtons` | 6356–6379 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6380–6386 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6387–6400 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6401–6442 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6443–6485 |  |
| `toggleBudgetPanel` | 6486–6511 |  |
| `syncMillRates` | 6512–6544 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6545–6565 |  |
| `applyColorAdjust` | 6566–6586 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6587–6599 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6600–6614 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6615–6632 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6633–6649 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6650–6671 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6672–6688 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6689–6928 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6929–6939 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6940–6953 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6954–6962 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6963–6973 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6974–6985 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6986–6998 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6999–7019 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7020–7067 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7068–7073 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7074–7095 |  |
| `applyMoneyDetail` | 7096–7120 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7121–7132 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7133–7140 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7141–7159 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7160–7170 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7171–7178 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7179–7195 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7196–7209 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7210–7220 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7221–7471 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7472–7481 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7482–7495 |  |
| `applySvcDriver` | 7496–7509 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7510–8069 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (959 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 118 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `applyView` | 14 | control appliers + the view/legend dispatchers |
| `setBlurb` | 14 | the Lab: a container for unfinished lenses |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 103 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 34 | 26% |
| the same doubt, at 100 m | 61 | 26% |
| services lens views (SPEC_services.md display architecture) | 4 | 25% |
| Development history: new supply per year | 194 | 24% |
| control appliers + the view/legend dispatchers | 224 | 19% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 17 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 57 | 0% |

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
| `#title-p` | 63 |
| `#temporal` | 74 |
| `#temporal-close` | 75 |
| `#temporal-name` | 76 |
| `#temporal-body` | 83 |
| `#temporal-chart` | 84 |
| `#temporal-read` | 85 |
| `#temporal-note` | 86 |
| `#temporal-hint` | 90 |
| `#millrates` | 106 |
| `#mill-head` | 107 |
| `#mill-rows` | 108 |
| `#mill-note` | 109 |
| `#budget` | 123 |
| `#budget-close` | 130 |
| `#budget-head` | 131 |
| `#budget-body` | 136 |
| `#budget-rows` | 137 |
| `#budget-other-hd` | 138 |
| `#budget-other` | 139 |
| `#budget-note` | 140 |
| `#peek` | 155 |
| `#peek-name` | 156 |
| `#peek-read` | 157 |
| `#peek-go` | 158 |
| `#controls` | 161 |
| `#toggle` | 174 |
| `#metric-row` | 175 |
| `#revcut` | 179 |
| `#moneymode` | 184 |
| `#views` | 190 |
| `#optpanel` | 204 |
| `#opt-fold` | 205 |
| `#opt-caret` | 205 |
| `#opt-body` | 206 |
| `#layers` | 207 |
| `#chgwindow-hd` | 208 |
| `#chgwindow` | 209 |
| `#labpick-hd` | 218 |
| `#labpick` | 219 |
| `#labcut-hd` | 220 |
| `#labcut` | 221 |
| `#moneydetail-hd` | 226 |
| `#moneydetail` | 227 |
| `#amenity-hd` | 252 |
| `#amenity` | 253 |
| `#amenity-lrt-row` | 254 |
| `#amenity-lrt-on` | 255 |
| `#amenity-school-row` | 257 |
| `#amenity-school-on` | 258 |
| `#uses-prisms-hd` | 261 |
| `#uses-prisms` | 262 |
| `#uses-prisms-on` | 264 |
| `#devmode-hd` | 267 |
| `#devmode` | 268 |
| `#devmetric-hd` | 272 |
| `#devmetric` | 273 |
| `#devwindow-hd` | 278 |
| `#devwindow` | 279 |
| `#devdetail-hd` | 284 |
| `#devdetail` | 285 |
| `#prism-hd` | 289 |
| `#prism-row` | 290 |
| `#prism-opacity` | 292 |
| `#prism-opacity-val` | 293 |
| `#services-hd` | 295 |
| `#services` | 296 |
| `#denom-hd` | 395 |
| `#denom` | 396 |
| `#ratio-denom-hd` | 400 |
| `#ratio-denom` | 401 |
| `#hoodmode` | 411 |
| `#hoodmode-btn` | 412 |
| `#coloradj` | 424 |
| `#coloradj-btn` | 425 |
| `#budget-pod` | 432 |
| `#budget-btn` | 433 |
| `#a11y` | 437 |
| `#a11y-btn` | 438 |
| `#a11y-menu` | 439 |
| `#palette` | 441 |
| `#labels-on` | 448 |
| `#reference-on` | 456 |
| `#about` | 461 |
| `#about-btn` | 462 |
| `#about-menu` | 463 |
| `#about-src-roads` | 475 |
| `#about-src-services` | 476 |
| `#about-vintage` | 504 |
| `#about-build` | 508 |
| `#about-modelled-roads` | 522 |
| `#about-modelled` | 540 |
| `#about-budget` | 550 |
| `#about-budget-lead` | 552 |
| `#about-budget-rows` | 553 |
| `#about-budget-note` | 554 |
| `#about-updated` | 565 |
| `#botleft` | 569 |
| `#compass` | 570 |
| `#rot-ccw` | 571 |
| `#tonorth` | 578 |
| `#needle` | 580 |
| `#rot-cw` | 585 |
| `#viewbtns` | 593 |
| `#recenter` | 595 |
| `#center2d` | 596 |
| `#legend` | 598 |
| `#legend-label` | 599 |
| `#legend-min` | 601 |
| `#legend-max` | 601 |
| `#legend-cats` | 603 |
| `#revmix` | 5381 |
| `#svccost` | 5472 |

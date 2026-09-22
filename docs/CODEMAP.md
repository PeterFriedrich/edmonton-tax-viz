# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,992-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (308 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 641–645 |  |
| `HOME` | 646–646 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 647–660 |  |
| `WINDOWS` | 661–686 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 687–696 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 697–701 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 702–777 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 778–780 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 781–782 |  |
| `METRICS` | 783–913 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 914–930 |  |
| `RATIO_DENOMS` | 931–963 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 964–964 |  |
| `ratioOf` | 965–965 |  |
| `ratioKept` | 966–987 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 988–998 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 999–1026 |  |
| `dominantUse` | 1027–1068 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1069–1238 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1239–1343 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1344–1348 | the Lab: a container for unfinished lenses |
| `inLab` | 1349–1350 |  |
| `DEVIATION_TITLES` | 1351–1355 |  |
| `deviationTitle` | 1356–1361 |  |
| `deviationKind` | 1362–1364 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1365–1370 |  |
| `changeBlurb` | 1371–1395 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1396–1417 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1418–1430 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1431–1442 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1443–1448 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1449–1454 |  |
| `infillAmenityBlurb` | 1455–1468 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1469–1483 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1484–1489 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1490–1497 |  |
| `devChoroplethBlurb` | 1498–1499 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1500–1548 |  |
| `withColourClause` | 1549–1566 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1567–1573 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1574–1587 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1588–1588 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1589–1603 |  |
| `fmtMB` | 1604–1614 |  |
| `showGridBusy` | 1615–1637 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1638–1654 |  |
| `loadGridData` | 1655–1708 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1709–1762 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1763–1787 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1788–1819 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1820–1820 |  |
| `gridFetches` | 1821–1845 |  |
| `RAMPS` | 1846–1886 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1887–1893 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1894–1899 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1900–1900 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1901–1907 |  |
| `AMENITY_BANDS` | 1908–1909 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1910–1912 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1913–1918 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1919–1933 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1934–1939 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1940–1958 |  |
| `gridScale` | 1959–1979 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1980–1986 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1987–1998 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1999–2001 |  |
| `quantile` | 2002–2016 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2017–2049 |  |
| `moneyBlurb` | 2050–2054 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2055–2067 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2068–2146 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2147–2147 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2148–2174 |  |
| `failLoading` | 2175–2188 |  |
| `hideLoading` | 2189–2243 |  |
| `topRings` | 2244–2260 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2261–2286 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2287–2287 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2288–2300 |  |
| `svcT` | 2301–2309 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2310–2321 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2322–2322 |  |
| `fmtFire` | 2323–2324 |  |
| `fmtTransit` | 2325–2326 |  |
| `fmtBike` | 2327–2338 |  |
| `fmtRoadM` | 2339–2349 |  |
| `fmtResShare` | 2350–2351 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2352–2357 |  |
| `fmtRoadsCost` | 2358–2362 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2363–2364 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2365–2366 |  |
| `fmtBikeCost` | 2367–2378 |  |
| `servicePlaneLayer` | 2379–2411 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2412–2421 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2422–2427 |  |
| `DEV_IND_TOTAL` | 2428–2430 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2431–2436 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2437–2441 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2442–2447 |  |
| `devGridOfferable` | 2448–2449 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2450–2450 |  |
| `devCol` | 2451–2451 |  |
| `_devScale` | 2452–2452 |  |
| `devScale` | 2453–2459 |  |
| `devT` | 2460–2463 |  |
| `developmentPlaneLayer` | 2464–2480 |  |
| `fmtDev` | 2481–2496 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2497–2502 |  |
| `DEV_GRID_IND_N` | 2503–2503 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2504–2506 |  |
| `devGridScale` | 2507–2533 |  |
| `devGridLayer` | 2534–2582 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2583–2584 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2585–2592 |  |
| `_infillStats` | 2593–2593 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2594–2611 |  |
| `_infillRaw` | 2612–2614 |  |
| `infillScore` | 2615–2630 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2631–2632 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2633–2650 |  |
| `INFILL_CENTER` | 2651–2651 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2652–2652 |  |
| `INFILL_NEG` | 2653–2653 |  |
| `infillColorAt` | 2654–2658 |  |
| `infillPlaneLayer` | 2659–2680 |  |
| `fmtFar` | 2681–2690 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2691–2691 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2692–2746 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2747–2754 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2755–2769 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2770–2790 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2791–2791 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2792–2806 |  |
| `chgT` | 2807–2816 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2817–2847 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2848–2936 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2937–2944 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2945–2945 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2946–2953 |  |
| `deviationRate` | 2954–2996 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2997–2997 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2998–3027 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3028–3034 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3035–3046 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3047–3050 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3051–3055 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3056–3066 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3067–3082 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3083–3114 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3115–3139 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3140–3192 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3193–3197 |  |
| `bandHover` | 3198–3206 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3207–3303 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3304–3311 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3312–3313 |  |
| `glassInstBandLayers` | 3314–3354 |  |
| `ratioInstBandLayers` | 3355–3382 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3383–3395 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3396–3397 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3398–3399 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3400–3400 |  |
| `deviationStats` | 3401–3445 |  |
| `deviationOf` | 3446–3447 |  |
| `deviationT` | 3448–3458 |  |
| `fmtDeviation` | 3459–3480 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3481–3524 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3525–3611 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3612–3634 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3635–3635 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3636–3656 |  |
| `ensureFireStations` | 3657–3672 |  |
| `TRANSIT_STATION_COLOR` | 3673–3673 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3674–3691 |  |
| `ensureTransitStations` | 3692–3707 |  |
| `TRANSIT_LINE_COLOR` | 3708–3708 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3709–3725 |  |
| `ensureLrtLines` | 3726–3742 |  |
| `BIKE_LINE_COLOR` | 3743–3743 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3744–3760 |  |
| `ensureBikeLines` | 3761–3818 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3819–3819 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3820–3823 |  |
| `BOUNDARY_COLOR` | 3824–3833 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3834–3834 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3835–3847 |  |
| `referenceSplit` | 3848–3875 |  |
| `referenceUnderLayers` | 3876–3910 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3911–3927 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3928–3947 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3948–3960 |  |
| `servicesBlurb` | 3961–3978 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3979–4002 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4003–4013 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4014–4065 |  |
| `REF_TIERS` | 4066–4087 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4088–4095 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4096–4098 |  |
| `placeAnchors` | 4099–4122 |  |
| `labelPool` | 4123–4130 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4131–4184 |  |
| `CHROME_IDS` | 4185–4189 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4190–4208 |  |
| `visibleLabels` | 4209–4263 |  |
| `labelLayer` | 4264–4300 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4301–4301 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4302–4317 |  |
| `ratioT` | 4318–4328 |  |
| `buildLayers` | 4329–4341 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4342–4651 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4652–4681 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4682–4691 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4692–4694 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4695–4726 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4727–4733 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4734–4741 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4742–4746 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4747–4757 |  |
| `revenueLens` | 4758–4759 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4760–4791 |  |
| `SVC_COST_BASES` | 4792–4809 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4810–4818 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4819–4834 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4835–4837 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4838–4844 |  |
| `svcRank` | 4845–4849 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4850–4856 |  |
| `svcDriverReading` | 4857–4877 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4878–4878 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4879–4882 |  |
| `servicePanelFor` | 4883–4903 |  |
| `hoodPanelLens` | 4904–4907 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4908–4925 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4926–4957 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4958–4963 |  |
| `sparklineSvg` | 4964–4979 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4980–5039 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5040–5045 | Development history: new supply per year |
| `devHistKey` | 5046–5055 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5056–5060 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5061–5061 |  |
| `devHistVerb` | 5062–5067 |  |
| `devHistoryFor` | 5068–5089 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5090–5109 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5110–5129 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5130–5165 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5166–5168 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5169–5232 |  |
| `syncTemporalPos` | 5233–5259 |  |
| `openTemporal` | 5260–5294 |  |
| `renderRevenueMix` | 5295–5361 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5362–5441 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5442–5445 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5446–5496 |  |
| `syncPinnedPanel` | 5497–5526 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5527–5542 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5543–5560 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5561–5608 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5609–5614 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5615–5661 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5662–5678 |  |
| `temporalClick` | 5679–5736 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5737–5805 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5806–6184 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6185–6266 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6267–6267 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6268–6286 |  |
| `syncMetricButtons` | 6287–6310 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6311–6317 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6318–6331 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6332–6373 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6374–6416 |  |
| `toggleBudgetPanel` | 6417–6442 |  |
| `syncMillRates` | 6443–6475 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6476–6497 |  |
| `applyColorAdjust` | 6498–6519 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6520–6532 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6533–6548 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6549–6566 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6567–6583 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6584–6605 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6606–6622 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6623–6862 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6863–6873 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6874–6887 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6888–6896 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6897–6907 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6908–6919 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6920–6933 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6934–6954 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6955–7002 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7003–7008 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7009–7030 |  |
| `applyMoneyDetail` | 7031–7055 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7056–7067 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7068–7075 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7076–7094 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7095–7105 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7106–7113 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7114–7130 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7131–7144 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7145–7155 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7156–7407 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7408–7417 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7418–7431 |  |
| `applySvcDriver` | 7432–7445 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7446–7992 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (942 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `applyView` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |
| `labelPool` | 8 | geographic reference layers (all views) |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 109 | 65% |
| services lens views (SPEC_services.md display architecture) | 2 | 50% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 87 | 41% |
| loading overlay | 56 | 36% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 34 | 26% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 193 | 24% |
| control appliers + the view/legend dispatchers | 210 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 56 | 0% |

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
| `#center2d` | 594 |
| `#recenter` | 595 |
| `#legend` | 597 |
| `#legend-label` | 598 |
| `#legend-min` | 600 |
| `#legend-max` | 600 |
| `#legend-cats` | 602 |
| `#revmix` | 5314 |
| `#svccost` | 5405 |

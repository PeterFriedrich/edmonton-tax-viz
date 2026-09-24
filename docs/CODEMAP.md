# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,088-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (311 indexed)

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
| `VIEWS` | 1242–1346 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1347–1351 | the Lab: a container for unfinished lenses |
| `inLab` | 1352–1353 |  |
| `DEVIATION_TITLES` | 1354–1358 |  |
| `deviationTitle` | 1359–1364 |  |
| `deviationKind` | 1365–1367 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1368–1373 |  |
| `changeBlurb` | 1374–1398 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1399–1420 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1421–1433 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1434–1445 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1446–1451 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1452–1457 |  |
| `infillAmenityBlurb` | 1458–1471 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1472–1486 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1487–1492 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1493–1501 |  |
| `devChoroplethBlurb` | 1502–1511 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1512–1559 |  |
| `setBlurb` | 1560–1573 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `withColourClause` | 1574–1591 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1592–1598 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1599–1612 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1613–1613 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1614–1628 |  |
| `fmtMB` | 1629–1639 |  |
| `showGridBusy` | 1640–1662 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1663–1679 |  |
| `loadGridData` | 1680–1733 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1734–1787 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1788–1812 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1813–1844 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1845–1845 |  |
| `gridFetches` | 1846–1870 |  |
| `RAMPS` | 1871–1911 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1912–1918 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1919–1924 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1925–1925 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1926–1932 |  |
| `AMENITY_BANDS` | 1933–1934 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1935–1937 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1938–1943 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1944–1958 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1959–1964 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1965–1983 |  |
| `gridScale` | 1984–2004 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2005–2011 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2012–2023 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2024–2026 |  |
| `quantile` | 2027–2041 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2042–2074 |  |
| `moneyBlurb` | 2075–2079 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2080–2092 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2093–2171 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2172–2172 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2173–2199 |  |
| `failLoading` | 2200–2213 |  |
| `hideLoading` | 2214–2268 |  |
| `topRings` | 2269–2285 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2286–2311 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2312–2312 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2313–2325 |  |
| `svcT` | 2326–2334 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2335–2348 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2349–2349 |  |
| `fmtFire` | 2350–2351 |  |
| `fmtTransit` | 2352–2353 |  |
| `fmtBike` | 2354–2366 |  |
| `fmtRoadM` | 2367–2380 |  |
| `fmtResShare` | 2381–2383 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2384–2389 |  |
| `fmtRoadsCost` | 2390–2394 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2395–2396 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2397–2398 |  |
| `fmtBikeCost` | 2399–2410 |  |
| `servicePlaneLayer` | 2411–2443 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2444–2453 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2454–2459 |  |
| `DEV_IND_TOTAL` | 2460–2462 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2463–2468 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2469–2473 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2474–2479 |  |
| `devGridOfferable` | 2480–2481 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2482–2482 |  |
| `devCol` | 2483–2483 |  |
| `_devScale` | 2484–2484 |  |
| `devScale` | 2485–2491 |  |
| `devT` | 2492–2495 |  |
| `developmentPlaneLayer` | 2496–2512 |  |
| `fmtDev` | 2513–2528 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2529–2534 |  |
| `DEV_GRID_IND_N` | 2535–2535 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2536–2538 |  |
| `devGridScale` | 2539–2565 |  |
| `devGridLayer` | 2566–2614 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2615–2616 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2617–2624 |  |
| `_infillStats` | 2625–2625 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2626–2643 |  |
| `_infillRaw` | 2644–2646 |  |
| `infillScore` | 2647–2662 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2663–2664 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2665–2682 |  |
| `INFILL_CENTER` | 2683–2683 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2684–2684 |  |
| `INFILL_NEG` | 2685–2685 |  |
| `infillColorAt` | 2686–2690 |  |
| `infillPlaneLayer` | 2691–2712 |  |
| `fmtFar` | 2713–2722 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2723–2723 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2724–2778 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2779–2786 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2787–2801 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2802–2822 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2823–2823 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2824–2838 |  |
| `chgT` | 2839–2848 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2849–2879 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2880–2968 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2969–2976 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2977–2977 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2978–2985 |  |
| `deviationRate` | 2986–3028 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3029–3029 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3030–3059 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3060–3066 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3067–3078 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3079–3082 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3083–3087 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3088–3098 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3099–3114 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3115–3146 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3147–3171 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3172–3224 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3225–3229 |  |
| `bandHover` | 3230–3238 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3239–3335 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3336–3343 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3344–3345 |  |
| `glassInstBandLayers` | 3346–3386 |  |
| `ratioInstBandLayers` | 3387–3414 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3415–3427 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3428–3429 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3430–3431 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3432–3432 |  |
| `deviationStats` | 3433–3477 |  |
| `deviationOf` | 3478–3479 |  |
| `deviationT` | 3480–3490 |  |
| `fmtDeviation` | 3491–3512 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3513–3556 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3557–3643 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3644–3666 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3667–3667 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3668–3688 |  |
| `ensureFireStations` | 3689–3704 |  |
| `TRANSIT_STATION_COLOR` | 3705–3705 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3706–3723 |  |
| `ensureTransitStations` | 3724–3739 |  |
| `TRANSIT_LINE_COLOR` | 3740–3740 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3741–3757 |  |
| `ensureLrtLines` | 3758–3774 |  |
| `BIKE_LINE_COLOR` | 3775–3775 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3776–3792 |  |
| `ensureBikeLines` | 3793–3850 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3851–3851 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3852–3855 |  |
| `BOUNDARY_COLOR` | 3856–3865 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3866–3866 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3867–3879 |  |
| `referenceSplit` | 3880–3907 |  |
| `referenceUnderLayers` | 3908–3942 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3943–3959 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3960–3979 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3980–3992 |  |
| `servicesBlurb` | 3993–4010 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 4011–4034 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4035–4045 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4046–4097 |  |
| `REF_TIERS` | 4098–4119 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4120–4127 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4128–4130 |  |
| `placeAnchors` | 4131–4154 |  |
| `labelPool` | 4155–4162 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4163–4216 |  |
| `CHROME_IDS` | 4217–4221 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4222–4240 |  |
| `visibleLabels` | 4241–4295 |  |
| `labelLayer` | 4296–4332 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4333–4333 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4334–4349 |  |
| `ratioT` | 4350–4372 |  |
| `zMatrix` | 4373–4377 |  |
| `buildLayers` | 4378–4401 |  |
| `flattenDuringEase` | 4402–4426 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4427–4736 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4737–4766 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4767–4776 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4777–4779 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4780–4811 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4812–4818 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4819–4826 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4827–4831 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4832–4842 |  |
| `revenueLens` | 4843–4844 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4845–4877 |  |
| `SVC_COST_BASES` | 4878–4895 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4896–4904 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4905–4920 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4921–4923 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4924–4930 |  |
| `svcRank` | 4931–4935 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4936–4942 |  |
| `svcDriverReading` | 4943–4963 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4964–4964 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4965–4968 |  |
| `servicePanelFor` | 4969–4989 |  |
| `hoodPanelLens` | 4990–4993 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4994–5011 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5012–5043 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5044–5049 |  |
| `sparklineSvg` | 5050–5065 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5066–5125 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5126–5131 | Development history: new supply per year |
| `devHistKey` | 5132–5141 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5142–5146 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5147–5147 |  |
| `devHistVerb` | 5148–5153 |  |
| `devHistoryFor` | 5154–5175 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5176–5195 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5196–5215 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5216–5251 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5252–5254 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5255–5318 |  |
| `syncTemporalPos` | 5319–5345 |  |
| `openTemporal` | 5346–5380 |  |
| `renderRevenueMix` | 5381–5447 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5448–5527 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5528–5531 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5532–5582 |  |
| `syncPinnedPanel` | 5583–5612 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5613–5628 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5629–5646 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5647–5694 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5695–5700 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5701–5747 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5748–5764 |  |
| `temporalClick` | 5765–5822 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5823–5891 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5892–6272 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6273–6354 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6355–6355 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6356–6374 |  |
| `syncMetricButtons` | 6375–6398 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6399–6405 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6406–6419 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6420–6461 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6462–6504 |  |
| `toggleBudgetPanel` | 6505–6530 |  |
| `syncMillRates` | 6531–6563 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6564–6584 |  |
| `applyColorAdjust` | 6585–6605 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6606–6618 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6619–6633 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6634–6651 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6652–6668 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6669–6690 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6691–6707 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6708–6947 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6948–6958 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6959–6972 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6973–6981 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6982–6992 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6993–7004 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7005–7017 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7018–7038 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7039–7086 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7087–7092 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7093–7114 |  |
| `applyMoneyDetail` | 7115–7139 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7140–7151 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7152–7159 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7160–7178 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7179–7189 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7190–7197 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7198–7214 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7215–7228 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7229–7239 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7240–7490 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7491–7500 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7501–7514 |  |
| `applySvcDriver` | 7515–7528 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7529–8088 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (965 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
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
| the Lab: a container for unfinished lenses | 110 | 65% |
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
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
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
| `#revmix` | 5400 |
| `#svccost` | 5491 |

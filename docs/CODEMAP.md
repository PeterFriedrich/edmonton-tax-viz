# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,529-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (328 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 675–679 |  |
| `HOME` | 680–680 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 681–694 |  |
| `WINDOWS` | 695–720 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 721–730 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 731–735 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 736–811 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 812–814 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 815–816 |  |
| `METRICS` | 817–919 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 920–936 |  |
| `RATIO_DENOMS` | 937–970 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 971–971 |  |
| `ratioOf` | 972–972 |  |
| `ratioKept` | 973–994 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 995–1005 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1006–1033 |  |
| `dominantUse` | 1034–1075 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1076–1226 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1227–1322 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1323–1327 | the Lab: a container for unfinished lenses |
| `inLab` | 1328–1329 |  |
| `DEVIATION_TITLES` | 1330–1334 |  |
| `deviationTitle` | 1335–1340 |  |
| `deviationKind` | 1341–1343 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1344–1351 |  |
| `changeBlurb` | 1352–1369 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1370–1382 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1383–1395 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1396–1404 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1405–1413 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1414–1419 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1420–1427 |  |
| `infillAmenityBlurb` | 1428–1441 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1442–1453 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1454–1459 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1460–1518 |  |
| `setBlurb` | 1519–1531 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1532–1547 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1548–1565 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1566–1572 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1573–1586 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1587–1587 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1588–1602 |  |
| `fmtMB` | 1603–1613 |  |
| `showGridBusy` | 1614–1636 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1637–1653 |  |
| `loadGridData` | 1654–1707 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1708–1761 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1762–1786 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1787–1818 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1819–1819 |  |
| `gridFetches` | 1820–1846 |  |
| `RAMPS` | 1847–1887 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1888–1894 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1895–1900 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1901–1901 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1902–1908 |  |
| `AMENITY_BANDS` | 1909–1910 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1911–1913 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1914–1919 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1920–1934 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1935–1940 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1941–1959 |  |
| `gridScale` | 1960–1980 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1981–1987 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1988–1999 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2000–2002 |  |
| `quantile` | 2003–2017 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2018–2052 |  |
| `moneyBlurb` | 2053–2064 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2065–2077 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2078–2156 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2157–2157 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2158–2184 |  |
| `failLoading` | 2185–2198 |  |
| `hideLoading` | 2199–2253 |  |
| `topRings` | 2254–2270 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2271–2296 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2297–2297 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2298–2310 |  |
| `svcT` | 2311–2319 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2320–2333 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2334–2334 |  |
| `fmtFire` | 2335–2336 |  |
| `fmtTransit` | 2337–2338 |  |
| `fmtBike` | 2339–2351 |  |
| `fmtRoadM` | 2352–2365 |  |
| `fmtResShare` | 2366–2368 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2369–2374 |  |
| `fmtRoadsCost` | 2375–2379 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2380–2381 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2382–2383 |  |
| `fmtBikeCost` | 2384–2395 |  |
| `servicePlaneLayer` | 2396–2428 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2429–2438 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2439–2444 |  |
| `DEV_IND_TOTAL` | 2445–2447 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2448–2453 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2454–2458 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2459–2464 |  |
| `devGridOfferable` | 2465–2466 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2467–2467 |  |
| `devCol` | 2468–2468 |  |
| `_devScale` | 2469–2469 |  |
| `devScale` | 2470–2476 |  |
| `devT` | 2477–2480 |  |
| `developmentPlaneLayer` | 2481–2497 |  |
| `fmtDev` | 2498–2513 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2514–2519 |  |
| `DEV_GRID_IND_N` | 2520–2520 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2521–2523 |  |
| `devGridScale` | 2524–2550 |  |
| `devGridLayer` | 2551–2599 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2600–2601 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2602–2609 |  |
| `_infillStats` | 2610–2610 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2611–2628 |  |
| `_infillRaw` | 2629–2631 |  |
| `infillScore` | 2632–2647 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2648–2649 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2650–2667 |  |
| `INFILL_CENTER` | 2668–2668 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2669–2669 |  |
| `INFILL_NEG` | 2670–2670 |  |
| `infillColorAt` | 2671–2675 |  |
| `infillPlaneLayer` | 2676–2697 |  |
| `fmtFar` | 2698–2707 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2708–2708 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2709–2763 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2764–2771 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2772–2786 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2787–2807 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2808–2808 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2809–2823 |  |
| `chgT` | 2824–2833 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2834–2864 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2865–2953 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2954–2961 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2962–2962 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2963–2970 |  |
| `deviationRate` | 2971–3013 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3014–3014 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3015–3044 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3045–3051 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3052–3063 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3064–3067 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3068–3072 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3073–3083 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3084–3099 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3100–3131 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3132–3156 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3157–3209 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3210–3214 |  |
| `bandHover` | 3215–3223 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3224–3326 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3327–3334 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3335–3336 |  |
| `glassInstBandLayers` | 3337–3377 |  |
| `ratioInstBandLayers` | 3378–3405 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3406–3418 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3419–3420 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3421–3422 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3423–3423 |  |
| `deviationStats` | 3424–3468 |  |
| `deviationOf` | 3469–3470 |  |
| `deviationT` | 3471–3481 |  |
| `fmtDeviation` | 3482–3503 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3504–3547 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3548–3634 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3635–3657 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3658–3658 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3659–3679 |  |
| `ensureFireStations` | 3680–3695 |  |
| `TRANSIT_STATION_COLOR` | 3696–3696 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3697–3714 |  |
| `ensureTransitStations` | 3715–3730 |  |
| `TRANSIT_LINE_COLOR` | 3731–3731 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3732–3748 |  |
| `ensureLrtLines` | 3749–3765 |  |
| `BIKE_LINE_COLOR` | 3766–3766 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3767–3783 |  |
| `ensureBikeLines` | 3784–3841 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3842–3842 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3843–3846 |  |
| `BOUNDARY_COLOR` | 3847–3856 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3857–3857 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3858–3870 |  |
| `referenceSplit` | 3871–3898 |  |
| `referenceUnderLayers` | 3899–3933 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3934–3950 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3951–3970 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3971–3984 |  |
| `servicesBlurb` | 3985–3996 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3997–4020 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4021–4031 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4032–4083 |  |
| `REF_TIERS` | 4084–4105 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4106–4113 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4114–4116 |  |
| `placeAnchors` | 4117–4140 |  |
| `labelPool` | 4141–4148 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4149–4202 |  |
| `CHROME_IDS` | 4203–4207 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4208–4226 |  |
| `visibleLabels` | 4227–4281 |  |
| `labelLayer` | 4282–4319 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `selectedHoodLayer` | 4320–4338 | The outline of the hood being read: the pinned panel's, the peek card's, |
| `_ratioScales` | 4339–4339 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4340–4355 |  |
| `ratioT` | 4356–4378 |  |
| `zMatrix` | 4379–4383 |  |
| `buildLayers` | 4384–4408 |  |
| `flattenDuringEase` | 4409–4433 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4434–4743 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4744–4773 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4774–4783 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4784–4786 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4787–4818 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4819–4825 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4826–4833 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4834–4838 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4839–4849 |  |
| `revenueLens` | 4850–4851 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4852–4884 |  |
| `SVC_COST_BASES` | 4885–4902 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4903–4911 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4912–4921 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4922–4924 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4925–4931 |  |
| `svcRank` | 4932–4936 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4937–4943 |  |
| `svcDriverReading` | 4944–4964 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4965–4965 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4966–4969 |  |
| `servicePanelFor` | 4970–4974 |  |
| `ratioPanelFor` | 4975–4998 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 4999–5003 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5004–5021 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5022–5053 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5054–5059 |  |
| `sparklineSvg` | 5060–5075 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5076–5135 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5136–5141 | Development history: new supply per year |
| `devHistKey` | 5142–5151 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5152–5156 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5157–5157 |  |
| `devHistVerb` | 5158–5163 |  |
| `devHistoryFor` | 5164–5199 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5200–5219 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5220–5239 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5240–5275 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5276–5278 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5279–5342 |  |
| `syncTemporalPos` | 5343–5369 |  |
| `openTemporal` | 5370–5407 |  |
| `renderRevenueMix` | 5408–5477 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5478–5552 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5553–5610 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5611–5614 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5615–5665 |  |
| `syncPinnedPanel` | 5666–5699 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5700–5715 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5716–5733 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5734–5781 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5782–5787 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5788–5835 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5836–5852 |  |
| `temporalClick` | 5853–5907 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 5908–5915 | neighbourhood search |
| `searchMatches` | 5916–5930 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 5931–5959 |  |
| `openSearch` | 5960–5972 |  |
| `closeSearch` | 5973–5987 |  |
| `flyToHood` | 5988–6007 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6008–6026 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6027–6095 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6096–6473 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6474–6563 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6564–6564 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6565–6583 |  |
| `syncMetricButtons` | 6584–6607 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6608–6614 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6615–6628 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6629–6670 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6671–6713 |  |
| `toggleBudgetPanel` | 6714–6739 |  |
| `syncMillRates` | 6740–6772 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6773–6793 |  |
| `applyColorAdjust` | 6794–6814 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6815–6827 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6828–6842 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6843–6860 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6861–6877 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6878–6899 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6900–6916 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6917–7156 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7157–7167 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7168–7181 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7182–7190 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7191–7201 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7202–7213 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7214–7226 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7227–7247 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7248–7295 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7296–7301 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7302–7323 |  |
| `applyMoneyDetail` | 7324–7348 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7349–7360 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7361–7368 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7369–7387 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7388–7398 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7399–7406 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7407–7423 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7424–7437 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7438–7448 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7449–7692 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7693–7702 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7703–7716 |  |
| `applySvcDriver` | 7717–7749 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7750–7752 |  |
| `urlHash` | 7753–7793 |  |
| `shareLink` | 7794–7802 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7803–7814 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7815–7821 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7822–7894 |  |
| `restoreFromHash` | 7895–7913 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7914–8529 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1044 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 126 | the Lab: a container for unfinished lenses |
| `buildLayers` | 40 | geographic reference layers (all views) |
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
| geographic reference layers (all views) | 93 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Development history: new supply per year | 111 | 30% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| the same doubt, at 100 m | 61 | 26% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 221 | 20% |
| neighbourhood search | 115 | 11% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 67 | 0% |

## Element ids (137) — the control surface

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
| `#temporal` | 93 |
| `#temporal-close` | 94 |
| `#temporal-name` | 95 |
| `#temporal-body` | 102 |
| `#temporal-chart` | 103 |
| `#temporal-read` | 104 |
| `#temporal-note` | 105 |
| `#temporal-hint` | 109 |
| `#millrates` | 125 |
| `#mill-head` | 126 |
| `#mill-rows` | 127 |
| `#mill-note` | 128 |
| `#budget` | 142 |
| `#budget-close` | 149 |
| `#budget-head` | 150 |
| `#budget-body` | 155 |
| `#budget-rows` | 156 |
| `#budget-other-hd` | 157 |
| `#budget-other` | 158 |
| `#budget-note` | 159 |
| `#peek` | 174 |
| `#peek-name` | 175 |
| `#peek-read` | 176 |
| `#peek-go` | 177 |
| `#controls` | 180 |
| `#toggle` | 193 |
| `#metric-row` | 194 |
| `#revcut` | 198 |
| `#moneymode` | 203 |
| `#views` | 209 |
| `#optpanel` | 223 |
| `#opt-fold` | 224 |
| `#opt-caret` | 224 |
| `#opt-body` | 225 |
| `#layers` | 226 |
| `#chgwindow-hd` | 227 |
| `#chgwindow` | 228 |
| `#labpick-hd` | 237 |
| `#labpick` | 238 |
| `#labcut-hd` | 239 |
| `#labcut` | 240 |
| `#moneydetail-hd` | 245 |
| `#moneydetail` | 246 |
| `#amenity-hd` | 271 |
| `#amenity` | 272 |
| `#amenity-lrt-row` | 273 |
| `#amenity-lrt-on` | 274 |
| `#amenity-school-row` | 276 |
| `#amenity-school-on` | 277 |
| `#uses-prisms-hd` | 280 |
| `#uses-prisms` | 281 |
| `#uses-prisms-on` | 283 |
| `#devmode-hd` | 286 |
| `#devmode` | 287 |
| `#devmetric-hd` | 291 |
| `#devmetric` | 292 |
| `#devwindow-hd` | 297 |
| `#devwindow` | 298 |
| `#devdetail-hd` | 303 |
| `#devdetail` | 304 |
| `#prism-hd` | 308 |
| `#prism-row` | 309 |
| `#prism-opacity` | 311 |
| `#prism-opacity-val` | 312 |
| `#services-hd` | 314 |
| `#services` | 315 |
| `#denom-hd` | 414 |
| `#denom` | 415 |
| `#ratio-denom-hd` | 419 |
| `#ratio-denom` | 420 |
| `#hoodmode` | 430 |
| `#hoodmode-btn` | 431 |
| `#coloradj` | 443 |
| `#coloradj-btn` | 444 |
| `#budget-pod` | 451 |
| `#budget-btn` | 452 |
| `#share` | 459 |
| `#share-btn` | 460 |
| `#a11y` | 463 |
| `#a11y-btn` | 464 |
| `#a11y-menu` | 465 |
| `#palette` | 467 |
| `#labels-on` | 474 |
| `#reference-on` | 482 |
| `#about` | 487 |
| `#about-btn` | 488 |
| `#about-menu` | 489 |
| `#about-src-roads` | 501 |
| `#about-src-services` | 502 |
| `#about-vintage` | 530 |
| `#about-build` | 534 |
| `#about-lot-acres` | 539 |
| `#about-modelled-roads` | 550 |
| `#about-modelled` | 572 |
| `#about-budget` | 582 |
| `#about-budget-lead` | 584 |
| `#about-budget-rows` | 585 |
| `#about-budget-note` | 586 |
| `#about-updated` | 598 |
| `#botleft` | 602 |
| `#compass` | 603 |
| `#rot-ccw` | 604 |
| `#tonorth` | 611 |
| `#needle` | 613 |
| `#rot-cw` | 618 |
| `#viewbtns` | 626 |
| `#recenter` | 628 |
| `#center2d` | 629 |
| `#legend` | 631 |
| `#legend-label` | 632 |
| `#legend-min` | 634 |
| `#legend-max` | 634 |
| `#legend-cats` | 636 |
| `#revmix` | 5427 |
| `#svccost` | 5521 |

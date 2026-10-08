# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,583-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (329 indexed)

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
| `RAMPS` | 1847–1891 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1892–1897 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `rampSetAside` | 1898–1904 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `GLASS_PLANE_COLOR` | 1905–1910 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1911–1911 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1912–1918 |  |
| `AMENITY_BANDS` | 1919–1920 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1921–1923 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1924–1929 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1930–1944 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1945–1950 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1951–1969 |  |
| `gridScale` | 1970–1990 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1991–1997 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1998–2009 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2010–2012 |  |
| `quantile` | 2013–2027 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2028–2062 |  |
| `moneyBlurb` | 2063–2074 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2075–2087 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2088–2166 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2167–2167 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2168–2194 |  |
| `failLoading` | 2195–2208 |  |
| `hideLoading` | 2209–2263 |  |
| `topRings` | 2264–2280 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2281–2306 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2307–2307 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2308–2320 |  |
| `svcT` | 2321–2329 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2330–2343 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2344–2344 |  |
| `fmtFire` | 2345–2346 |  |
| `fmtTransit` | 2347–2348 |  |
| `fmtBike` | 2349–2361 |  |
| `fmtRoadM` | 2362–2375 |  |
| `fmtResShare` | 2376–2378 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2379–2384 |  |
| `fmtRoadsCost` | 2385–2389 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2390–2391 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2392–2393 |  |
| `fmtBikeCost` | 2394–2405 |  |
| `servicePlaneLayer` | 2406–2438 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2439–2448 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2449–2454 |  |
| `DEV_IND_TOTAL` | 2455–2457 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2458–2463 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2464–2468 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2469–2474 |  |
| `devGridOfferable` | 2475–2476 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2477–2477 |  |
| `devCol` | 2478–2478 |  |
| `_devScale` | 2479–2479 |  |
| `devScale` | 2480–2486 |  |
| `devT` | 2487–2490 |  |
| `developmentPlaneLayer` | 2491–2507 |  |
| `fmtDev` | 2508–2523 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2524–2529 |  |
| `DEV_GRID_IND_N` | 2530–2530 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2531–2533 |  |
| `devGridScale` | 2534–2560 |  |
| `devGridLayer` | 2561–2609 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2610–2611 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2612–2619 |  |
| `_infillStats` | 2620–2620 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2621–2638 |  |
| `_infillRaw` | 2639–2641 |  |
| `infillScore` | 2642–2657 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2658–2659 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2660–2677 |  |
| `INFILL_CENTER` | 2678–2678 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2679–2679 |  |
| `INFILL_NEG` | 2680–2680 |  |
| `infillColorAt` | 2681–2685 |  |
| `infillPlaneLayer` | 2686–2707 |  |
| `fmtFar` | 2708–2717 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2718–2718 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2719–2773 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2774–2781 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2782–2796 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2797–2817 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2818–2818 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2819–2833 |  |
| `chgT` | 2834–2843 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2844–2874 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2875–2963 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2964–2971 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2972–2972 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2973–2980 |  |
| `deviationRate` | 2981–3023 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3024–3024 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3025–3054 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3055–3061 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3062–3073 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3074–3077 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3078–3082 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3083–3093 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3094–3109 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3110–3141 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3142–3166 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3167–3219 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3220–3224 |  |
| `bandHover` | 3225–3233 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3234–3336 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3337–3344 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3345–3346 |  |
| `glassInstBandLayers` | 3347–3387 |  |
| `ratioInstBandLayers` | 3388–3415 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3416–3428 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3429–3430 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3431–3432 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3433–3433 |  |
| `deviationStats` | 3434–3478 |  |
| `deviationOf` | 3479–3480 |  |
| `deviationT` | 3481–3491 |  |
| `fmtDeviation` | 3492–3513 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3514–3557 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3558–3644 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3645–3667 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3668–3668 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3669–3689 |  |
| `ensureFireStations` | 3690–3705 |  |
| `TRANSIT_STATION_COLOR` | 3706–3706 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3707–3724 |  |
| `ensureTransitStations` | 3725–3740 |  |
| `TRANSIT_LINE_COLOR` | 3741–3741 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3742–3758 |  |
| `ensureLrtLines` | 3759–3775 |  |
| `BIKE_LINE_COLOR` | 3776–3776 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3777–3793 |  |
| `ensureBikeLines` | 3794–3851 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3852–3852 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3853–3856 |  |
| `BOUNDARY_COLOR` | 3857–3866 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3867–3867 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3868–3880 |  |
| `referenceSplit` | 3881–3908 |  |
| `referenceUnderLayers` | 3909–3943 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3944–3960 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3961–3980 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3981–3994 |  |
| `servicesBlurb` | 3995–4006 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4007–4030 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4031–4041 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4042–4093 |  |
| `REF_TIERS` | 4094–4115 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4116–4123 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4124–4126 |  |
| `placeAnchors` | 4127–4150 |  |
| `labelPool` | 4151–4158 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4159–4212 |  |
| `CHROME_IDS` | 4213–4217 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4218–4236 |  |
| `visibleLabels` | 4237–4291 |  |
| `labelLayer` | 4292–4344 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4345–4385 |  |
| `_ratioScales` | 4386–4386 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4387–4402 |  |
| `ratioT` | 4403–4425 |  |
| `zMatrix` | 4426–4430 |  |
| `buildLayers` | 4431–4455 |  |
| `flattenDuringEase` | 4456–4480 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4481–4790 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4791–4820 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4821–4830 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4831–4833 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4834–4865 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4866–4872 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4873–4880 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4881–4885 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4886–4896 |  |
| `revenueLens` | 4897–4898 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4899–4931 |  |
| `SVC_COST_BASES` | 4932–4949 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4950–4958 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4959–4968 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4969–4971 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4972–4978 |  |
| `svcRank` | 4979–4983 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4984–4990 |  |
| `svcDriverReading` | 4991–5011 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5012–5012 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5013–5016 |  |
| `servicePanelFor` | 5017–5021 |  |
| `ratioPanelFor` | 5022–5045 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5046–5050 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5051–5068 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5069–5100 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5101–5106 |  |
| `sparklineSvg` | 5107–5122 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5123–5182 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5183–5188 | Development history: new supply per year |
| `devHistKey` | 5189–5198 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5199–5203 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5204–5204 |  |
| `devHistVerb` | 5205–5210 |  |
| `devHistoryFor` | 5211–5249 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5250–5269 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5270–5289 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5290–5325 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5326–5328 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5329–5392 |  |
| `syncTemporalPos` | 5393–5419 |  |
| `openTemporal` | 5420–5457 |  |
| `renderRevenueMix` | 5458–5527 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5528–5602 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5603–5660 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5661–5664 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5665–5715 |  |
| `syncPinnedPanel` | 5716–5749 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5750–5765 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5766–5783 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5784–5831 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5832–5837 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5838–5885 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5886–5902 |  |
| `temporalClick` | 5903–5957 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 5958–5965 | neighbourhood search |
| `searchMatches` | 5966–5980 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 5981–6009 |  |
| `openSearch` | 6010–6022 |  |
| `closeSearch` | 6023–6039 |  |
| `flyToHood` | 6040–6059 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6060–6078 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6079–6147 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6148–6525 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6526–6615 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6616–6616 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6617–6635 |  |
| `syncMetricButtons` | 6636–6659 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6660–6666 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6667–6680 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6681–6722 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6723–6765 |  |
| `toggleBudgetPanel` | 6766–6791 |  |
| `syncMillRates` | 6792–6824 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6825–6845 |  |
| `applyColorAdjust` | 6846–6866 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6867–6879 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6880–6894 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6895–6912 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6913–6929 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6930–6951 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6952–6968 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6969–7208 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7209–7219 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7220–7235 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7236–7244 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7245–7255 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7256–7267 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7268–7280 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7281–7301 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7302–7349 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7350–7355 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7356–7377 |  |
| `applyMoneyDetail` | 7378–7402 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7403–7414 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7415–7422 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7423–7441 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7442–7452 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7453–7460 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7461–7477 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7478–7491 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7492–7502 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7503–7746 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7747–7756 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7757–7770 |  |
| `applySvcDriver` | 7771–7803 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7804–7806 |  |
| `urlHash` | 7807–7847 |  |
| `shareLink` | 7848–7856 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7857–7868 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7869–7875 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7876–7948 |  |
| `restoreFromHash` | 7949–7967 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7968–8583 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1055 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 126 | the Lab: a container for unfinished lenses |
| `buildLayers` | 40 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
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
| the Lab: a container for unfinished lenses | 126 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 97 | 42% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Development history: new supply per year | 111 | 30% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| the same doubt, at 100 m | 61 | 26% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 223 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
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
| `#revmix` | 5477 |
| `#svccost` | 5571 |

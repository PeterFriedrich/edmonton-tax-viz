# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,957-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (306 indexed)

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
| `fmtBike` | 2327–2327 |  |
| `fmtWater` | 2328–2333 |  |
| `fmtRoadsCost` | 2334–2338 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2339–2340 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2341–2342 |  |
| `fmtBikeCost` | 2343–2354 |  |
| `servicePlaneLayer` | 2355–2387 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2388–2397 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2398–2403 |  |
| `DEV_IND_TOTAL` | 2404–2406 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2407–2412 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2413–2417 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2418–2423 |  |
| `devGridOfferable` | 2424–2425 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2426–2426 |  |
| `devCol` | 2427–2427 |  |
| `_devScale` | 2428–2428 |  |
| `devScale` | 2429–2435 |  |
| `devT` | 2436–2439 |  |
| `developmentPlaneLayer` | 2440–2456 |  |
| `fmtDev` | 2457–2472 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2473–2478 |  |
| `DEV_GRID_IND_N` | 2479–2479 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2480–2482 |  |
| `devGridScale` | 2483–2509 |  |
| `devGridLayer` | 2510–2558 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2559–2560 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2561–2568 |  |
| `_infillStats` | 2569–2569 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2570–2587 |  |
| `_infillRaw` | 2588–2590 |  |
| `infillScore` | 2591–2606 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2607–2608 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2609–2626 |  |
| `INFILL_CENTER` | 2627–2627 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2628–2628 |  |
| `INFILL_NEG` | 2629–2629 |  |
| `infillColorAt` | 2630–2634 |  |
| `infillPlaneLayer` | 2635–2649 |  |
| `fmtFar` | 2650–2659 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2660–2660 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2661–2715 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2716–2723 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2724–2738 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2739–2759 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2760–2760 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2761–2775 |  |
| `chgT` | 2776–2785 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2786–2816 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2817–2905 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2906–2913 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2914–2914 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2915–2922 |  |
| `deviationRate` | 2923–2965 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2966–2966 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2967–2996 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2997–3003 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3004–3015 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3016–3019 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3020–3024 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3025–3035 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3036–3051 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3052–3083 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3084–3108 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3109–3161 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3162–3166 |  |
| `bandHover` | 3167–3175 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3176–3272 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3273–3280 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3281–3282 |  |
| `glassInstBandLayers` | 3283–3323 |  |
| `ratioInstBandLayers` | 3324–3351 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3352–3364 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3365–3366 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3367–3368 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3369–3369 |  |
| `deviationStats` | 3370–3414 |  |
| `deviationOf` | 3415–3416 |  |
| `deviationT` | 3417–3427 |  |
| `fmtDeviation` | 3428–3449 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3450–3493 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3494–3580 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3581–3603 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3604–3604 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3605–3625 |  |
| `ensureFireStations` | 3626–3641 |  |
| `TRANSIT_STATION_COLOR` | 3642–3642 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3643–3660 |  |
| `ensureTransitStations` | 3661–3676 |  |
| `TRANSIT_LINE_COLOR` | 3677–3677 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3678–3694 |  |
| `ensureLrtLines` | 3695–3711 |  |
| `BIKE_LINE_COLOR` | 3712–3712 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3713–3729 |  |
| `ensureBikeLines` | 3730–3787 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3788–3788 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3789–3792 |  |
| `BOUNDARY_COLOR` | 3793–3802 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3803–3803 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3804–3816 |  |
| `referenceSplit` | 3817–3844 |  |
| `referenceUnderLayers` | 3845–3879 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3880–3896 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3897–3916 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3917–3929 |  |
| `servicesBlurb` | 3930–3947 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3948–3971 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3972–3982 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3983–4034 |  |
| `REF_TIERS` | 4035–4056 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4057–4064 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4065–4067 |  |
| `placeAnchors` | 4068–4091 |  |
| `labelPool` | 4092–4099 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4100–4153 |  |
| `CHROME_IDS` | 4154–4158 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4159–4177 |  |
| `visibleLabels` | 4178–4232 |  |
| `labelLayer` | 4233–4269 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4270–4270 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4271–4286 |  |
| `ratioT` | 4287–4297 |  |
| `buildLayers` | 4298–4310 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4311–4620 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4621–4650 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4651–4660 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4661–4663 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4664–4695 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4696–4702 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4703–4710 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4711–4715 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4716–4726 |  |
| `revenueLens` | 4727–4728 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4729–4760 |  |
| `SVC_COST_BASES` | 4761–4778 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4779–4787 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4788–4803 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4804–4806 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4807–4813 |  |
| `svcRank` | 4814–4818 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4819–4825 |  |
| `svcDriverReading` | 4826–4846 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4847–4847 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4848–4851 |  |
| `servicePanelFor` | 4852–4872 |  |
| `hoodPanelLens` | 4873–4876 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4877–4894 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4895–4926 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4927–4932 |  |
| `sparklineSvg` | 4933–4948 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4949–5008 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5009–5014 | Development history: new supply per year |
| `devHistKey` | 5015–5024 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5025–5029 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5030–5030 |  |
| `devHistVerb` | 5031–5036 |  |
| `devHistoryFor` | 5037–5058 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5059–5078 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5079–5098 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5099–5134 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5135–5137 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5138–5201 |  |
| `syncTemporalPos` | 5202–5228 |  |
| `openTemporal` | 5229–5263 |  |
| `renderRevenueMix` | 5264–5330 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5331–5410 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5411–5414 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5415–5465 |  |
| `syncPinnedPanel` | 5466–5495 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5496–5511 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5512–5529 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5530–5577 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5578–5583 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5584–5630 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5631–5647 |  |
| `temporalClick` | 5648–5705 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5706–5774 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5775–6149 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6150–6231 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6232–6232 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6233–6251 |  |
| `syncMetricButtons` | 6252–6275 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6276–6282 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6283–6296 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6297–6338 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6339–6381 |  |
| `toggleBudgetPanel` | 6382–6407 |  |
| `syncMillRates` | 6408–6440 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6441–6462 |  |
| `applyColorAdjust` | 6463–6484 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6485–6497 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6498–6513 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6514–6531 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6532–6548 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6549–6570 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6571–6587 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6588–6827 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6828–6838 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6839–6852 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6853–6861 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6862–6872 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6873–6884 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6885–6898 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6899–6919 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6920–6967 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6968–6973 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6974–6995 |  |
| `applyMoneyDetail` | 6996–7020 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7021–7032 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7033–7040 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7041–7059 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7060–7070 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7071–7078 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7079–7095 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7096–7109 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7110–7120 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7121–7372 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7373–7382 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7383–7396 |  |
| `applySvcDriver` | 7397–7410 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7411–7957 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (934 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `applyView` | 14 | control appliers + the view/legend dispatchers |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
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
| services lens views (SPEC_services.md display architecture) | 1 | 100% |
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 26 | 65% |
| the Lab: a container for unfinished lenses | 109 | 65% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 87 | 41% |
| loading overlay | 54 | 37% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 33 | 27% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 190 | 25% |
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
| `#revmix` | 5283 |
| `#svccost` | 5374 |

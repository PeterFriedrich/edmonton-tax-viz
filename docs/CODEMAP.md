# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,877-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (304 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 641–645 |  |
| `HOME` | 646–646 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 647–660 |  |
| `WINDOWS` | 661–679 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 680–689 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 690–694 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 695–762 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 763–764 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 765–890 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 891–907 |  |
| `RATIO_DENOMS` | 908–940 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 941–941 |  |
| `ratioOf` | 942–942 |  |
| `ratioKept` | 943–964 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 965–975 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 976–1003 |  |
| `dominantUse` | 1004–1045 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1046–1215 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1216–1320 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1321–1325 | the Lab: a container for unfinished lenses |
| `inLab` | 1326–1327 |  |
| `DEVIATION_TITLES` | 1328–1332 |  |
| `deviationTitle` | 1333–1338 |  |
| `deviationKind` | 1339–1341 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1342–1347 |  |
| `changeBlurb` | 1348–1372 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1373–1394 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1395–1407 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1408–1419 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1420–1425 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1426–1431 |  |
| `infillAmenityBlurb` | 1432–1445 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1446–1460 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1461–1466 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1467–1474 |  |
| `devChoroplethBlurb` | 1475–1476 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1477–1525 |  |
| `withColourClause` | 1526–1543 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1544–1550 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1551–1564 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1565–1565 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1566–1580 |  |
| `fmtMB` | 1581–1591 |  |
| `showGridBusy` | 1592–1614 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1615–1631 |  |
| `loadGridData` | 1632–1685 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1686–1739 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1740–1764 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1765–1796 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1797–1797 |  |
| `gridFetches` | 1798–1822 |  |
| `RAMPS` | 1823–1863 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1864–1870 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1871–1876 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1877–1877 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1878–1884 |  |
| `AMENITY_BANDS` | 1885–1886 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1887–1889 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1890–1895 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1896–1910 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1911–1916 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1917–1935 |  |
| `gridScale` | 1936–1956 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1957–1963 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1964–1975 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1976–1978 |  |
| `quantile` | 1979–1993 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1994–2026 |  |
| `moneyBlurb` | 2027–2031 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2032–2044 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2045–2123 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2124–2124 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2125–2151 |  |
| `failLoading` | 2152–2165 |  |
| `hideLoading` | 2166–2220 |  |
| `topRings` | 2221–2237 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2238–2263 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2264–2264 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2265–2277 |  |
| `svcT` | 2278–2282 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2283–2284 |  |
| `fmtFire` | 2285–2285 |  |
| `fmtTransit` | 2286–2287 |  |
| `fmtBike` | 2288–2288 |  |
| `fmtWater` | 2289–2294 |  |
| `fmtRoadsCost` | 2295–2299 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2300–2301 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2302–2303 |  |
| `fmtBikeCost` | 2304–2315 |  |
| `servicePlaneLayer` | 2316–2348 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2349–2358 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2359–2364 |  |
| `DEV_IND_TOTAL` | 2365–2367 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2368–2373 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2374–2378 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2379–2384 |  |
| `devGridOfferable` | 2385–2386 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2387–2387 |  |
| `devCol` | 2388–2388 |  |
| `_devScale` | 2389–2389 |  |
| `devScale` | 2390–2396 |  |
| `devT` | 2397–2400 |  |
| `developmentPlaneLayer` | 2401–2417 |  |
| `fmtDev` | 2418–2433 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2434–2439 |  |
| `DEV_GRID_IND_N` | 2440–2440 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2441–2443 |  |
| `devGridScale` | 2444–2470 |  |
| `devGridLayer` | 2471–2519 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2520–2521 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2522–2529 |  |
| `_infillStats` | 2530–2530 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2531–2548 |  |
| `_infillRaw` | 2549–2551 |  |
| `infillScore` | 2552–2567 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2568–2569 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2570–2587 |  |
| `INFILL_CENTER` | 2588–2588 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2589–2589 |  |
| `INFILL_NEG` | 2590–2590 |  |
| `infillColorAt` | 2591–2595 |  |
| `infillPlaneLayer` | 2596–2610 |  |
| `fmtFar` | 2611–2620 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2621–2621 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2622–2676 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2677–2684 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2685–2699 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2700–2720 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2721–2721 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2722–2736 |  |
| `chgT` | 2737–2746 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2747–2777 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2778–2866 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2867–2874 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2875–2875 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2876–2883 |  |
| `deviationRate` | 2884–2926 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2927–2927 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2928–2957 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2958–2964 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2965–2976 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2977–2980 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2981–2985 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2986–2996 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2997–3012 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3013–3044 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3045–3069 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3070–3122 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3123–3127 |  |
| `bandHover` | 3128–3136 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3137–3233 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3234–3241 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3242–3243 |  |
| `glassInstBandLayers` | 3244–3284 |  |
| `ratioInstBandLayers` | 3285–3312 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3313–3325 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3326–3327 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3328–3329 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3330–3330 |  |
| `deviationStats` | 3331–3375 |  |
| `deviationOf` | 3376–3377 |  |
| `deviationT` | 3378–3388 |  |
| `fmtDeviation` | 3389–3410 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3411–3454 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3455–3541 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3542–3564 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3565–3565 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3566–3586 |  |
| `ensureFireStations` | 3587–3602 |  |
| `TRANSIT_STATION_COLOR` | 3603–3603 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3604–3621 |  |
| `ensureTransitStations` | 3622–3637 |  |
| `TRANSIT_LINE_COLOR` | 3638–3638 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3639–3655 |  |
| `ensureLrtLines` | 3656–3672 |  |
| `BIKE_LINE_COLOR` | 3673–3673 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3674–3690 |  |
| `ensureBikeLines` | 3691–3748 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3749–3749 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3750–3753 |  |
| `BOUNDARY_COLOR` | 3754–3763 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3764–3764 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3765–3777 |  |
| `referenceSplit` | 3778–3805 |  |
| `referenceUnderLayers` | 3806–3840 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3841–3857 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3858–3877 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3878–3890 |  |
| `servicesBlurb` | 3891–3908 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3909–3932 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3933–3943 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3944–3995 |  |
| `REF_TIERS` | 3996–4017 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4018–4025 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4026–4028 |  |
| `placeAnchors` | 4029–4052 |  |
| `labelPool` | 4053–4060 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4061–4114 |  |
| `CHROME_IDS` | 4115–4119 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4120–4138 |  |
| `visibleLabels` | 4139–4193 |  |
| `labelLayer` | 4194–4230 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4231–4231 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4232–4247 |  |
| `ratioT` | 4248–4258 |  |
| `buildLayers` | 4259–4271 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4272–4581 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4582–4611 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4612–4615 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4616–4618 |  |
| `fmtBig` | 4619–4646 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4647–4652 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4653–4660 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4661–4665 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4666–4676 |  |
| `revenueLens` | 4677–4678 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4679–4710 |  |
| `SVC_COST_BASES` | 4711–4726 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4727–4735 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4736–4751 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4752–4754 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4755–4761 |  |
| `svcRank` | 4762–4766 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4767–4773 |  |
| `svcDriverReading` | 4774–4794 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4795–4795 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4796–4799 |  |
| `servicePanelFor` | 4800–4820 |  |
| `hoodPanelLens` | 4821–4824 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4825–4842 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4843–4874 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4875–4880 |  |
| `sparklineSvg` | 4881–4896 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4897–4956 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 4957–4962 | Development history: new supply per year |
| `devHistKey` | 4963–4972 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 4973–4977 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 4978–4978 |  |
| `devHistVerb` | 4979–4984 |  |
| `devHistoryFor` | 4985–5006 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5007–5026 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5027–5046 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5047–5082 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5083–5085 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5086–5149 |  |
| `syncTemporalPos` | 5150–5176 |  |
| `openTemporal` | 5177–5211 |  |
| `renderRevenueMix` | 5212–5278 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5279–5346 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5347–5349 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5350–5400 |  |
| `syncPinnedPanel` | 5401–5430 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5431–5446 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5447–5464 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5465–5512 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5513–5518 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5519–5565 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5566–5582 |  |
| `temporalClick` | 5583–5640 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5641–5709 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5710–6069 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6070–6151 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6152–6152 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6153–6171 |  |
| `syncMetricButtons` | 6172–6195 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6196–6202 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6203–6216 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6217–6258 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6259–6301 |  |
| `toggleBudgetPanel` | 6302–6327 |  |
| `syncMillRates` | 6328–6360 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6361–6382 |  |
| `applyColorAdjust` | 6383–6404 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6405–6417 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6418–6433 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6434–6451 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6452–6468 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6469–6490 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6491–6507 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6508–6747 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6748–6758 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6759–6772 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6773–6781 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6782–6792 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6793–6804 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6805–6818 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6819–6839 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6840–6887 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6888–6893 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6894–6915 |  |
| `applyMoneyDetail` | 6916–6940 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6941–6952 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6953–6960 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6961–6979 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6980–6990 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6991–6998 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6999–7015 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7016–7029 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7030–7040 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7041–7292 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7293–7302 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7303–7316 |  |
| `applySvcDriver` | 7317–7330 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7331–7877 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (921 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `applyView` | 13 | control appliers + the view/legend dispatchers |
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
| tunables | 10 | 60% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 87 | 41% |
| loading overlay | 49 | 39% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 33 | 27% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 188 | 25% |
| control appliers + the view/legend dispatchers | 210 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 1 | 0% |
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
| `#revmix` | 5231 |
| `#svccost` | 5316 |

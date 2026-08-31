# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,969-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (267 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 568–572 |  |
| `HOME` | 573–573 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 574–587 |  |
| `WINDOWS` | 588–645 | Every user-facing year range on the page derives from this block — lens |
| `fmtMoney` | 646–647 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 648–773 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 774–790 |  |
| `RATIO_DENOMS` | 791–852 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 853–853 |  |
| `ratioOf` | 854–854 |  |
| `ratioKept` | 855–876 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 877–887 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 888–915 |  |
| `dominantUse` | 916–949 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 950–1104 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1105–1209 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1210–1214 | the Lab: a container for unfinished lenses |
| `inLab` | 1215–1216 |  |
| `DEVIATION_TITLES` | 1217–1221 |  |
| `deviationTitle` | 1222–1227 |  |
| `deviationKind` | 1228–1230 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1231–1236 |  |
| `changeBlurb` | 1237–1259 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1260–1281 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1282–1292 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1293–1298 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1299–1304 |  |
| `infillAmenityBlurb` | 1305–1318 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1319–1333 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1334–1339 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1340–1347 |  |
| `devChoroplethBlurb` | 1348–1349 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1350–1398 |  |
| `withColourClause` | 1399–1413 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1414–1474 |  |
| `state` | 1475–1528 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1529–1569 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1570–1576 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1577–1582 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1583–1583 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1584–1590 |  |
| `AMENITY_BANDS` | 1591–1592 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1593–1595 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1596–1601 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1602–1616 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1617–1622 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1623–1634 |  |
| `gridScale` | 1635–1655 |  |
| `scaleT` | 1656–1662 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1663–1674 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1675–1677 |  |
| `quantile` | 1678–1692 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1693–1725 |  |
| `moneyBlurb` | 1726–1730 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1731–1743 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1744–1822 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1823–1823 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1824–1850 |  |
| `failLoading` | 1851–1864 |  |
| `hideLoading` | 1865–1890 |  |
| `topRings` | 1891–1907 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1908–1933 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1934–1934 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1935–1947 |  |
| `svcT` | 1948–1952 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1953–1954 |  |
| `fmtFire` | 1955–1955 |  |
| `fmtTransit` | 1956–1957 |  |
| `fmtBike` | 1958–1958 |  |
| `fmtWater` | 1959–1961 |  |
| `fmtSvcCost` | 1962–1966 |  |
| `fmtRoadsCost` | 1967–1968 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1969–1970 |  |
| `fmtBikeCost` | 1971–1982 |  |
| `servicePlaneLayer` | 1983–2015 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2016–2025 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2026–2031 |  |
| `DEV_IND_TOTAL` | 2032–2034 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2035–2040 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2041–2045 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2046–2051 |  |
| `devGridOfferable` | 2052–2053 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2054–2054 |  |
| `devCol` | 2055–2055 |  |
| `_devScale` | 2056–2056 |  |
| `devScale` | 2057–2063 |  |
| `devT` | 2064–2067 |  |
| `developmentPlaneLayer` | 2068–2084 |  |
| `fmtDev` | 2085–2100 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2101–2106 |  |
| `DEV_GRID_IND_N` | 2107–2107 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2108–2110 |  |
| `devGridScale` | 2111–2137 |  |
| `devGridLayer` | 2138–2186 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2187–2188 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2189–2196 |  |
| `_infillStats` | 2197–2197 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2198–2215 |  |
| `_infillRaw` | 2216–2218 |  |
| `infillScore` | 2219–2234 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2235–2236 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2237–2254 |  |
| `INFILL_CENTER` | 2255–2255 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2256–2256 |  |
| `INFILL_NEG` | 2257–2257 |  |
| `infillColorAt` | 2258–2262 |  |
| `infillPlaneLayer` | 2263–2277 |  |
| `fmtFar` | 2278–2287 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2288–2288 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2289–2343 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2344–2351 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2352–2366 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2367–2387 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2388–2388 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2389–2403 |  |
| `chgT` | 2404–2413 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2414–2444 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2445–2533 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2534–2541 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2542–2542 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2543–2550 |  |
| `deviationRate` | 2551–2593 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2594–2594 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2595–2624 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2625–2631 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2632–2643 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2644–2647 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2648–2652 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2653–2663 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2664–2679 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2680–2706 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2707–2759 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2760–2764 |  |
| `bandHover` | 2765–2773 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2774–2870 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2871–2878 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2879–2880 |  |
| `glassInstBandLayers` | 2881–2909 |  |
| `deviationRateExempt` | 2910–2922 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2923–2924 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2925–2926 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2927–2927 |  |
| `deviationStats` | 2928–2972 |  |
| `deviationOf` | 2973–2974 |  |
| `deviationT` | 2975–2985 |  |
| `fmtDeviation` | 2986–3007 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3008–3051 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3052–3138 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3139–3161 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3162–3162 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3163–3183 |  |
| `ensureFireStations` | 3184–3199 |  |
| `TRANSIT_STATION_COLOR` | 3200–3200 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3201–3218 |  |
| `ensureTransitStations` | 3219–3234 |  |
| `TRANSIT_LINE_COLOR` | 3235–3235 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3236–3252 |  |
| `ensureLrtLines` | 3253–3269 |  |
| `BIKE_LINE_COLOR` | 3270–3270 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3271–3287 |  |
| `ensureBikeLines` | 3288–3345 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3346–3346 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3347–3350 |  |
| `BOUNDARY_COLOR` | 3351–3360 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3361–3361 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3362–3374 |  |
| `referenceSplit` | 3375–3402 |  |
| `referenceUnderLayers` | 3403–3437 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3438–3454 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3455–3474 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3475–3487 |  |
| `servicesBlurb` | 3488–3505 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3506–3529 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3530–3540 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3541–3592 |  |
| `REF_TIERS` | 3593–3614 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3615–3622 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3623–3625 |  |
| `placeAnchors` | 3626–3649 |  |
| `labelPool` | 3650–3657 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3658–3711 |  |
| `CHROME_IDS` | 3712–3715 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3716–3734 |  |
| `visibleLabels` | 3735–3789 |  |
| `labelLayer` | 3790–3826 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3827–3827 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3828–3843 |  |
| `ratioT` | 3844–3854 |  |
| `buildLayers` | 3855–3867 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3868–4170 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4171–4200 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4201–4204 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4205–4207 |  |
| `fmtBig` | 4208–4235 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4236–4241 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4242–4249 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4250–4254 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4255–4265 |  |
| `revenueLens` | 4266–4267 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4268–4285 |  |
| `SVC_COST_BASES` | 4286–4298 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4299–4299 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4300–4302 |  |
| `servicePanelFor` | 4303–4316 |  |
| `hoodPanelLens` | 4317–4320 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4321–4338 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4339–4370 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4371–4376 |  |
| `sparklineSvg` | 4377–4392 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4393–4462 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4463–4489 |  |
| `openTemporal` | 4490–4518 |  |
| `renderRevenueMix` | 4519–4567 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4568–4601 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4602–4604 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4605–4655 |  |
| `syncPinnedPanel` | 4656–4682 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4683–4698 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4699–4709 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4710–4757 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4758–4763 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4764–4803 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4804–4820 |  |
| `temporalClick` | 4821–4878 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4879–4958 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4959–5291 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5292–5359 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5360–5360 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5361–5379 |  |
| `syncMetricButtons` | 5380–5403 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5404–5410 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5411–5424 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5425–5466 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5467–5509 |  |
| `toggleBudgetPanel` | 5510–5535 |  |
| `syncMillRates` | 5536–5566 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5567–5588 |  |
| `applyColorAdjust` | 5589–5610 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5611–5623 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5624–5639 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5640–5657 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5658–5674 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5675–5690 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5691–5707 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5708–5947 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5948–5958 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5959–5972 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5973–5981 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5982–5992 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5993–6004 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6005–6018 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6019–6039 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6040–6087 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6088–6093 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6094–6111 |  |
| `applyMoneyDetail` | 6112–6121 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 6122–6129 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6130–6148 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6149–6159 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6160–6167 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6168–6184 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6185–6198 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6199–6209 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6210–6445 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6446–6455 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6456–6469 |  |
| `applySvcDriver` | 6470–6969 |  |

## Element ids (121) — the control surface

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
| `#title` | 44 |
| `#title-h` | 45 |
| `#title-p` | 46 |
| `#temporal` | 57 |
| `#temporal-close` | 58 |
| `#temporal-name` | 59 |
| `#temporal-body` | 66 |
| `#temporal-chart` | 67 |
| `#temporal-read` | 68 |
| `#temporal-note` | 69 |
| `#temporal-hint` | 73 |
| `#millrates` | 89 |
| `#mill-head` | 90 |
| `#mill-rows` | 91 |
| `#mill-note` | 92 |
| `#budget` | 106 |
| `#budget-close` | 113 |
| `#budget-head` | 114 |
| `#budget-body` | 119 |
| `#budget-rows` | 120 |
| `#budget-other-hd` | 121 |
| `#budget-other` | 122 |
| `#budget-note` | 123 |
| `#peek` | 138 |
| `#peek-name` | 139 |
| `#peek-read` | 140 |
| `#peek-go` | 141 |
| `#controls` | 144 |
| `#toggle` | 157 |
| `#metric-row` | 158 |
| `#revcut` | 162 |
| `#moneymode` | 167 |
| `#views` | 173 |
| `#optpanel` | 187 |
| `#opt-fold` | 188 |
| `#opt-caret` | 188 |
| `#opt-body` | 189 |
| `#layers` | 190 |
| `#chgwindow-hd` | 191 |
| `#chgwindow` | 192 |
| `#labpick-hd` | 201 |
| `#labpick` | 202 |
| `#labcut-hd` | 203 |
| `#labcut` | 204 |
| `#moneydetail-hd` | 209 |
| `#moneydetail` | 210 |
| `#amenity-hd` | 224 |
| `#amenity` | 225 |
| `#amenity-lrt-row` | 226 |
| `#amenity-lrt-on` | 227 |
| `#amenity-school-row` | 229 |
| `#amenity-school-on` | 230 |
| `#uses-prisms-hd` | 233 |
| `#uses-prisms` | 234 |
| `#uses-prisms-on` | 236 |
| `#devmode-hd` | 239 |
| `#devmode` | 240 |
| `#devmetric-hd` | 244 |
| `#devmetric` | 245 |
| `#devwindow-hd` | 250 |
| `#devwindow` | 251 |
| `#devdetail-hd` | 256 |
| `#devdetail` | 257 |
| `#prism-hd` | 261 |
| `#prism-row` | 262 |
| `#prism-opacity` | 264 |
| `#prism-opacity-val` | 265 |
| `#services-hd` | 267 |
| `#services` | 268 |
| `#denom-hd` | 362 |
| `#denom` | 363 |
| `#ratio-denom-hd` | 367 |
| `#ratio-denom` | 368 |
| `#hoodmode` | 379 |
| `#hoodmode-btn` | 380 |
| `#coloradj` | 392 |
| `#coloradj-btn` | 393 |
| `#budget-pod` | 400 |
| `#budget-btn` | 401 |
| `#a11y` | 405 |
| `#a11y-btn` | 406 |
| `#a11y-menu` | 407 |
| `#palette` | 409 |
| `#labels-on` | 416 |
| `#reference-on` | 424 |
| `#about` | 429 |
| `#about-btn` | 430 |
| `#about-menu` | 431 |
| `#about-src-services` | 440 |
| `#about-vintage` | 468 |
| `#about-modelled` | 475 |
| `#about-budget` | 485 |
| `#about-budget-lead` | 487 |
| `#about-budget-rows` | 488 |
| `#about-budget-note` | 489 |
| `#about-updated` | 500 |
| `#botleft` | 504 |
| `#compass` | 505 |
| `#rot-ccw` | 506 |
| `#tonorth` | 513 |
| `#needle` | 515 |
| `#rot-cw` | 520 |
| `#viewbtns` | 528 |
| `#center2d` | 529 |
| `#recenter` | 530 |
| `#legend` | 532 |
| `#legend-label` | 533 |
| `#legend-min` | 535 |
| `#legend-max` | 535 |
| `#legend-cats` | 537 |
| `#revmix` | 4538 |
| `#svccost` | 4582 |

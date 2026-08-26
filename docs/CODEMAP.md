# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,785-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (262 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 546–550 |  |
| `HOME` | 551–551 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 552–595 |  |
| `fmtMoney` | 596–597 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 598–723 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 724–740 |  |
| `RATIO_DENOMS` | 741–802 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 803–803 |  |
| `ratioOf` | 804–804 |  |
| `ratioKept` | 805–826 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 827–837 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 838–865 |  |
| `dominantUse` | 866–899 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 900–1054 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1055–1159 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1160–1164 | the Lab: a container for unfinished lenses |
| `inLab` | 1165–1166 |  |
| `DEVIATION_TITLES` | 1167–1171 |  |
| `deviationTitle` | 1172–1177 |  |
| `deviationKind` | 1178–1180 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1181–1186 |  |
| `changeBlurb` | 1187–1209 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1210–1231 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1232–1242 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1243–1248 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1249–1254 |  |
| `infillAmenityBlurb` | 1255–1268 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1269–1283 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1284–1289 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1290–1297 |  |
| `devChoroplethBlurb` | 1298–1299 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1300–1348 |  |
| `withColourClause` | 1349–1363 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1364–1424 |  |
| `state` | 1425–1478 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1479–1519 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1520–1526 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1527–1532 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1533–1533 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1534–1540 |  |
| `AMENITY_BANDS` | 1541–1542 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1543–1545 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1546–1551 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1552–1566 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1567–1572 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1573–1584 |  |
| `gridScale` | 1585–1605 |  |
| `scaleT` | 1606–1612 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1613–1624 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1625–1627 |  |
| `quantile` | 1628–1642 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1643–1675 |  |
| `moneyBlurb` | 1676–1680 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1681–1693 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1694–1743 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1744–1760 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1761–1786 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1787–1787 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1788–1800 |  |
| `svcT` | 1801–1805 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1806–1807 |  |
| `fmtFire` | 1808–1808 |  |
| `fmtTransit` | 1809–1810 |  |
| `fmtBike` | 1811–1811 |  |
| `fmtWater` | 1812–1814 |  |
| `fmtSvcCost` | 1815–1819 |  |
| `fmtRoadsCost` | 1820–1821 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1822–1823 |  |
| `fmtBikeCost` | 1824–1835 |  |
| `servicePlaneLayer` | 1836–1868 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1869–1878 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1879–1884 |  |
| `DEV_IND_TOTAL` | 1885–1887 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1888–1893 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1894–1898 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1899–1904 |  |
| `devGridOfferable` | 1905–1906 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1907–1907 |  |
| `devCol` | 1908–1908 |  |
| `_devScale` | 1909–1909 |  |
| `devScale` | 1910–1916 |  |
| `devT` | 1917–1920 |  |
| `developmentPlaneLayer` | 1921–1937 |  |
| `fmtDev` | 1938–1953 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1954–1959 |  |
| `DEV_GRID_IND_N` | 1960–1960 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1961–1963 |  |
| `devGridScale` | 1964–1990 |  |
| `devGridLayer` | 1991–2039 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2040–2041 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2042–2049 |  |
| `_infillStats` | 2050–2050 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2051–2068 |  |
| `_infillRaw` | 2069–2071 |  |
| `infillScore` | 2072–2087 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2088–2089 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2090–2107 |  |
| `INFILL_CENTER` | 2108–2108 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2109–2109 |  |
| `INFILL_NEG` | 2110–2110 |  |
| `infillColorAt` | 2111–2115 |  |
| `infillPlaneLayer` | 2116–2130 |  |
| `fmtFar` | 2131–2140 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2141–2141 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2142–2196 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2197–2197 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2198–2212 |  |
| `changeFor` | 2213–2233 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2234–2234 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2235–2249 |  |
| `chgT` | 2250–2259 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2260–2290 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2291–2379 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2380–2387 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2388–2388 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2389–2396 |  |
| `deviationRate` | 2397–2439 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2440–2440 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2441–2470 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2471–2477 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2478–2489 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2490–2493 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2494–2498 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2499–2509 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2510–2525 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2526–2552 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2553–2605 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2606–2610 |  |
| `bandHover` | 2611–2619 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2620–2716 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2717–2724 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2725–2726 |  |
| `glassInstBandLayers` | 2727–2755 |  |
| `deviationRateExempt` | 2756–2768 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2769–2770 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2771–2772 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2773–2773 |  |
| `deviationStats` | 2774–2818 |  |
| `deviationOf` | 2819–2820 |  |
| `deviationT` | 2821–2831 |  |
| `fmtDeviation` | 2832–2853 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2854–2897 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2898–2984 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2985–3007 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3008–3008 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3009–3029 |  |
| `ensureFireStations` | 3030–3045 |  |
| `TRANSIT_STATION_COLOR` | 3046–3046 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3047–3064 |  |
| `ensureTransitStations` | 3065–3080 |  |
| `TRANSIT_LINE_COLOR` | 3081–3081 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3082–3098 |  |
| `ensureLrtLines` | 3099–3115 |  |
| `BIKE_LINE_COLOR` | 3116–3116 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3117–3133 |  |
| `ensureBikeLines` | 3134–3191 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3192–3192 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3193–3196 |  |
| `BOUNDARY_COLOR` | 3197–3206 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3207–3207 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3208–3220 |  |
| `referenceSplit` | 3221–3248 |  |
| `referenceUnderLayers` | 3249–3283 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3284–3300 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3301–3320 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3321–3333 |  |
| `servicesBlurb` | 3334–3351 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3352–3375 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3376–3386 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3387–3438 |  |
| `REF_TIERS` | 3439–3460 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3461–3468 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3469–3471 |  |
| `placeAnchors` | 3472–3495 |  |
| `labelPool` | 3496–3503 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3504–3557 |  |
| `CHROME_IDS` | 3558–3561 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3562–3580 |  |
| `visibleLabels` | 3581–3635 |  |
| `labelLayer` | 3636–3672 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3673–3673 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3674–3689 |  |
| `ratioT` | 3690–3700 |  |
| `buildLayers` | 3701–3713 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3714–4016 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4017–4046 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4047–4050 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4051–4053 |  |
| `fmtBig` | 4054–4081 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4082–4087 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4088–4095 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4096–4100 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4101–4111 |  |
| `revenueLens` | 4112–4113 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4114–4131 |  |
| `SVC_COST_BASES` | 4132–4144 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4145–4145 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4146–4148 |  |
| `servicePanelFor` | 4149–4162 |  |
| `hoodPanelLens` | 4163–4166 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4167–4184 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4185–4216 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4217–4222 |  |
| `sparklineSvg` | 4223–4238 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4239–4308 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4309–4335 |  |
| `openTemporal` | 4336–4364 |  |
| `renderRevenueMix` | 4365–4413 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4414–4447 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4448–4450 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4451–4501 |  |
| `syncPinnedPanel` | 4502–4528 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4529–4544 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4545–4555 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4556–4603 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4604–4609 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4610–4649 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4650–4666 |  |
| `temporalClick` | 4667–4724 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4725–4804 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4805–5137 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5138–5192 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5193–5193 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5194–5212 |  |
| `syncMetricButtons` | 5213–5236 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5237–5243 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5244–5257 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5258–5299 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5300–5342 |  |
| `toggleBudgetPanel` | 5343–5368 |  |
| `syncMillRates` | 5369–5399 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5400–5421 |  |
| `applyColorAdjust` | 5422–5443 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5444–5456 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5457–5472 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5473–5490 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5491–5507 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5508–5523 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5524–5540 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5541–5780 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5781–5791 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5792–5805 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5806–5814 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5815–5825 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5826–5837 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5838–5851 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5852–5872 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 5873–5920 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5921–5926 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5927–5944 |  |
| `applyMoneyDetail` | 5945–5954 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5955–5962 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5963–5981 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5982–5992 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5993–6000 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6001–6017 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6018–6031 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6032–6042 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6043–6278 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6279–6288 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6289–6302 |  |
| `applySvcDriver` | 6303–6785 |  |

## Element ids (114) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#banner` | 20 |
| `#title` | 22 |
| `#title-h` | 23 |
| `#title-p` | 24 |
| `#temporal` | 35 |
| `#temporal-close` | 36 |
| `#temporal-name` | 37 |
| `#temporal-body` | 44 |
| `#temporal-chart` | 45 |
| `#temporal-read` | 46 |
| `#temporal-note` | 47 |
| `#temporal-hint` | 51 |
| `#millrates` | 67 |
| `#mill-head` | 68 |
| `#mill-rows` | 69 |
| `#mill-note` | 70 |
| `#budget` | 84 |
| `#budget-close` | 91 |
| `#budget-head` | 92 |
| `#budget-body` | 97 |
| `#budget-rows` | 98 |
| `#budget-other-hd` | 99 |
| `#budget-other` | 100 |
| `#budget-note` | 101 |
| `#peek` | 116 |
| `#peek-name` | 117 |
| `#peek-read` | 118 |
| `#peek-go` | 119 |
| `#controls` | 122 |
| `#toggle` | 135 |
| `#metric-row` | 136 |
| `#revcut` | 140 |
| `#moneymode` | 145 |
| `#views` | 151 |
| `#optpanel` | 165 |
| `#opt-fold` | 166 |
| `#opt-caret` | 166 |
| `#opt-body` | 167 |
| `#layers` | 168 |
| `#chgwindow-hd` | 169 |
| `#chgwindow` | 170 |
| `#labpick-hd` | 179 |
| `#labpick` | 180 |
| `#labcut-hd` | 181 |
| `#labcut` | 182 |
| `#moneydetail-hd` | 187 |
| `#moneydetail` | 188 |
| `#amenity-hd` | 202 |
| `#amenity` | 203 |
| `#amenity-lrt-row` | 204 |
| `#amenity-lrt-on` | 205 |
| `#amenity-school-row` | 207 |
| `#amenity-school-on` | 208 |
| `#uses-prisms-hd` | 211 |
| `#uses-prisms` | 212 |
| `#uses-prisms-on` | 214 |
| `#devmode-hd` | 217 |
| `#devmode` | 218 |
| `#devmetric-hd` | 222 |
| `#devmetric` | 223 |
| `#devwindow-hd` | 228 |
| `#devwindow` | 229 |
| `#devdetail-hd` | 234 |
| `#devdetail` | 235 |
| `#prism-hd` | 239 |
| `#prism-row` | 240 |
| `#prism-opacity` | 242 |
| `#prism-opacity-val` | 243 |
| `#services-hd` | 245 |
| `#services` | 246 |
| `#denom-hd` | 340 |
| `#denom` | 341 |
| `#ratio-denom-hd` | 345 |
| `#ratio-denom` | 346 |
| `#hoodmode` | 357 |
| `#hoodmode-btn` | 358 |
| `#coloradj` | 370 |
| `#coloradj-btn` | 371 |
| `#budget-pod` | 378 |
| `#budget-btn` | 379 |
| `#a11y` | 383 |
| `#a11y-btn` | 384 |
| `#a11y-menu` | 385 |
| `#palette` | 387 |
| `#labels-on` | 394 |
| `#reference-on` | 402 |
| `#about` | 407 |
| `#about-btn` | 408 |
| `#about-menu` | 409 |
| `#about-src-services` | 418 |
| `#about-vintage` | 446 |
| `#about-modelled` | 453 |
| `#about-budget` | 463 |
| `#about-budget-lead` | 465 |
| `#about-budget-rows` | 466 |
| `#about-budget-note` | 467 |
| `#about-updated` | 478 |
| `#botleft` | 482 |
| `#compass` | 483 |
| `#rot-ccw` | 484 |
| `#tonorth` | 491 |
| `#needle` | 493 |
| `#rot-cw` | 498 |
| `#viewbtns` | 506 |
| `#center2d` | 507 |
| `#recenter` | 508 |
| `#legend` | 510 |
| `#legend-label` | 511 |
| `#legend-min` | 513 |
| `#legend-max` | 513 |
| `#legend-cats` | 515 |
| `#revmix` | 4384 |
| `#svccost` | 4428 |

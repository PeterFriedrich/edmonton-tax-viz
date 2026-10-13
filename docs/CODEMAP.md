# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,881-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (323 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 739–741 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 742–746 | Throws on a missing or mis-sized light value: deck draws `undefined` |
| `tc` | 747–752 |  |
| `CENTER` | 753–757 |  |
| `HOME` | 758–758 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 759–772 |  |
| `WINDOWS` | 773–798 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 799–808 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 809–813 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 814–889 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 890–892 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 893–894 |  |
| `METRICS` | 895–1014 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1015–1048 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1049–1049 |  |
| `ratioOf` | 1050–1050 |  |
| `ratioKept` | 1051–1072 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1073–1085 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1086–1113 |  |
| `dominantUse` | 1114–1155 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1156–1306 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1307–1402 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1403–1407 | the Lab: a container for unfinished lenses |
| `inLab` | 1408–1409 |  |
| `DEVIATION_TITLES` | 1410–1414 |  |
| `deviationTitle` | 1415–1420 |  |
| `deviationKind` | 1421–1423 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1424–1431 |  |
| `changeBlurb` | 1432–1449 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1450–1462 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1463–1475 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1476–1484 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1485–1493 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1494–1499 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1500–1507 |  |
| `infillAmenityBlurb` | 1508–1521 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1522–1533 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1534–1539 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1540–1601 |  |
| `setBlurb` | 1602–1616 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1617–1632 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1633–1650 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1651–1657 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1658–1671 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1672–1672 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1673–1687 |  |
| `fmtMB` | 1688–1698 |  |
| `showGridBusy` | 1699–1721 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1722–1738 |  |
| `loadGridData` | 1739–1792 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1793–1846 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1847–1871 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1872–1904 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1905–1905 |  |
| `gridFetches` | 1906–1932 |  |
| `RAMPS` | 1933–1985 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1986–2020 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2021–2034 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2035–2047 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2048–2048 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2049–2055 |  |
| `AMENITY_BANDS` | 2056–2057 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2058–2060 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2061–2066 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2067–2081 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2082–2087 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2088–2106 |  |
| `gridScale` | 2107–2127 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2128–2134 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2135–2146 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2147–2149 |  |
| `quantile` | 2150–2164 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2165–2199 |  |
| `moneyBlurb` | 2200–2211 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2212–2224 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2225–2278 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2279–2279 |  |
| `gridName` | 2280–2293 |  |
| `paintBackdrop` | 2294–2331 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2332–2332 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2333–2357 |  |
| `failLoading` | 2358–2371 |  |
| `hideLoading` | 2372–2427 |  |
| `topRings` | 2428–2444 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2445–2470 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2471–2471 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2472–2484 |  |
| `svcT` | 2485–2493 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2494–2507 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2508–2508 |  |
| `fmtFire` | 2509–2510 |  |
| `fmtTransit` | 2511–2512 |  |
| `fmtBike` | 2513–2525 |  |
| `fmtRoadM` | 2526–2539 |  |
| `fmtResShare` | 2540–2542 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2543–2548 |  |
| `fmtRoadsCost` | 2549–2553 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2554–2555 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2556–2557 |  |
| `fmtBikeCost` | 2558–2569 |  |
| `servicePlaneLayer` | 2570–2602 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2603–2612 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2613–2618 |  |
| `DEV_IND_TOTAL` | 2619–2621 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2622–2627 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2628–2632 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2633–2638 |  |
| `devGridOfferable` | 2639–2640 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2641–2641 |  |
| `devCol` | 2642–2642 |  |
| `_devScale` | 2643–2643 |  |
| `devScale` | 2644–2650 |  |
| `devT` | 2651–2654 |  |
| `developmentPlaneLayer` | 2655–2671 |  |
| `fmtDev` | 2672–2687 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2688–2693 |  |
| `DEV_GRID_IND_N` | 2694–2694 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2695–2697 |  |
| `devGridScale` | 2698–2724 |  |
| `devGridLayer` | 2725–2773 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2774–2775 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2776–2783 |  |
| `_infillStats` | 2784–2784 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2785–2802 |  |
| `_infillRaw` | 2803–2805 |  |
| `infillScore` | 2806–2821 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2822–2823 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2824–2844 |  |
| `infillColorAt` | 2845–2849 |  |
| `infillPlaneLayer` | 2850–2871 |  |
| `fmtFar` | 2872–2882 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2883–2937 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2938–2945 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2946–2960 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2961–2981 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2982–2982 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2983–2997 |  |
| `chgT` | 2998–3007 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3008–3038 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3039–3127 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3128–3135 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3136–3136 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3137–3144 |  |
| `deviationRate` | 3145–3188 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3189–3218 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3219–3225 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3226–3237 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3238–3241 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3242–3246 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3247–3257 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3258–3273 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3274–3305 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3306–3383 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3384–3388 |  |
| `bandHover` | 3389–3397 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3398–3500 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3501–3508 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3509–3510 |  |
| `glassInstBandLayers` | 3511–3551 |  |
| `ratioInstBandLayers` | 3552–3579 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3580–3592 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3593–3594 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3595–3596 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3597–3597 |  |
| `deviationStats` | 3598–3642 |  |
| `deviationOf` | 3643–3644 |  |
| `deviationT` | 3645–3655 |  |
| `fmtDeviation` | 3656–3677 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3678–3721 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3722–3808 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3809–3833 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3834–3854 |  |
| `ensureFireStations` | 3855–3871 |  |
| `transitStationsLayer` | 3872–3889 |  |
| `ensureTransitStations` | 3890–3906 |  |
| `lrtLinesLayer` | 3907–3923 |  |
| `ensureLrtLines` | 3924–3941 |  |
| `bikeLinesLayer` | 3942–3958 |  |
| `ensureBikeLines` | 3959–4045 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4046–4073 |  |
| `referenceUnderLayers` | 4074–4108 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4109–4125 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4126–4145 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4146–4160 |  |
| `servicesBlurb` | 4161–4172 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4173–4209 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4210–4220 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4221–4272 |  |
| `REF_TIERS` | 4273–4294 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4295–4303 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4304–4327 |  |
| `labelPool` | 4328–4335 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4336–4389 |  |
| `CHROME_IDS` | 4390–4394 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4395–4413 |  |
| `visibleLabels` | 4414–4482 |  |
| `labelLayer` | 4483–4537 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4538–4578 |  |
| `_ratioScales` | 4579–4579 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4580–4595 |  |
| `ratioT` | 4596–4618 |  |
| `zMatrix` | 4619–4623 |  |
| `buildLayers` | 4624–4648 |  |
| `flattenDuringEase` | 4649–4673 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4674–4988 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4989–5018 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 5019–5028 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 5029–5031 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5032–5063 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5064–5070 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5071–5078 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5079–5083 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5084–5094 |  |
| `revenueLens` | 5095–5096 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5097–5129 |  |
| `SVC_COST_BASES` | 5130–5147 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5148–5156 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5157–5166 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5167–5169 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5170–5176 |  |
| `svcRank` | 5177–5181 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5182–5188 |  |
| `svcDriverReading` | 5189–5209 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5210–5210 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5211–5214 |  |
| `servicePanelFor` | 5215–5219 |  |
| `ratioPanelFor` | 5220–5243 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5244–5248 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5249–5266 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5267–5298 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5299–5304 |  |
| `sparklineSvg` | 5305–5320 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5321–5380 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5381–5386 | Development history: new supply per year |
| `devHistKey` | 5387–5396 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5397–5401 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5402–5402 |  |
| `devHistVerb` | 5403–5408 |  |
| `devHistoryFor` | 5409–5447 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5448–5467 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5468–5487 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5488–5523 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5524–5526 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5527–5590 |  |
| `syncTemporalPos` | 5591–5617 |  |
| `openTemporal` | 5618–5655 |  |
| `renderRevenueMix` | 5656–5725 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5726–5800 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5801–5858 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5859–5862 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5863–5913 |  |
| `syncPinnedPanel` | 5914–5947 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5948–5963 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5964–5981 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5982–6029 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6030–6035 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6036–6083 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6084–6100 |  |
| `temporalClick` | 6101–6155 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6156–6163 | neighbourhood search |
| `searchMatches` | 6164–6178 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6179–6207 |  |
| `openSearch` | 6208–6220 |  |
| `closeSearch` | 6221–6239 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6240–6252 |  |
| `closeGuide` | 6253–6260 |  |
| `maybeAutoGuide` | 6261–6277 |  |
| `flyToHood` | 6278–6297 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6298–6316 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6317–6385 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6386–6763 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6764–6853 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6854–6854 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6855–6873 |  |
| `syncMetricButtons` | 6874–6897 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6898–6904 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6905–6918 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6919–6960 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6961–7003 |  |
| `toggleBudgetPanel` | 7004–7029 |  |
| `syncMillRates` | 7030–7062 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7063–7083 |  |
| `applyColorAdjust` | 7084–7104 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7105–7117 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7118–7132 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7133–7150 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7151–7167 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7168–7189 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7190–7206 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7207–7446 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7447–7459 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7460–7476 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `syncThemeChrome` | 7477–7487 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7488–7502 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7503–7511 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7512–7522 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7523–7534 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7535–7547 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7548–7568 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7569–7616 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7617–7622 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7623–7644 |  |
| `applyMoneyDetail` | 7645–7669 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7670–7681 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7682–7689 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7690–7708 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7709–7719 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7720–7727 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7728–7744 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7745–7758 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7759–7769 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7770–8014 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 8015–8024 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 8025–8038 |  |
| `applySvcDriver` | 8039–8071 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8072–8074 |  |
| `urlHash` | 8075–8115 |  |
| `shareLink` | 8116–8124 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8125–8136 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8137–8143 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8144–8216 |  |
| `restoreFromHash` | 8217–8235 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8236–8881 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1100 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 129 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `tc` | 27 | tunables |
| `themed` | 17 | tunables |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 16 | control appliers + the view/legend dispatchers |
| `setBlurb` | 16 | the Lab: a container for unfinished lenses |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| the Lab: a container for unfinished lenses | 127 | 64% |
| tunables | 16 | 56% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 99 | 34% |
| loading overlay | 57 | 33% |
| Development history: new supply per year | 112 | 29% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 232 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the same doubt, at 100 m | 66 | 18% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 113 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 71 | 0% |

## Element ids (144) — the control surface

| id | line |
|---|---|
| `#map` | 39 |
| `#loading` | 43 |
| `#loading-box` | 44 |
| `#loading-title` | 55 |
| `#loading-blurb` | 56 |
| `#loading-spinner` | 57 |
| `#loading-text` | 58 |
| `#loading-retry` | 59 |
| `#banner` | 63 |
| `#gridbusy` | 74 |
| `#gridbusy-spinner` | 75 |
| `#gridbusy-text` | 77 |
| `#gridbusy-size` | 78 |
| `#title` | 82 |
| `#title-h` | 83 |
| `#title-p` | 87 |
| `#search` | 97 |
| `#search-btn` | 98 |
| `#search-box` | 101 |
| `#search-input` | 102 |
| `#search-close` | 106 |
| `#search-list` | 108 |
| `#guide-btn` | 116 |
| `#guide` | 118 |
| `#guide-close` | 119 |
| `#guide-ask` | 120 |
| `#guide-show` | 121 |
| `#guide-body` | 124 |
| `#temporal` | 143 |
| `#temporal-close` | 144 |
| `#temporal-name` | 145 |
| `#temporal-body` | 152 |
| `#temporal-chart` | 153 |
| `#temporal-read` | 154 |
| `#temporal-note` | 155 |
| `#temporal-hint` | 159 |
| `#millrates` | 175 |
| `#mill-head` | 176 |
| `#mill-rows` | 177 |
| `#mill-note` | 178 |
| `#budget` | 192 |
| `#budget-close` | 199 |
| `#budget-head` | 200 |
| `#budget-body` | 205 |
| `#budget-rows` | 206 |
| `#budget-other-hd` | 207 |
| `#budget-other` | 208 |
| `#budget-note` | 209 |
| `#peek` | 224 |
| `#peek-name` | 225 |
| `#peek-read` | 226 |
| `#peek-go` | 227 |
| `#controls` | 230 |
| `#toggle` | 243 |
| `#metric-row` | 244 |
| `#revcut` | 248 |
| `#moneymode` | 253 |
| `#views` | 259 |
| `#optpanel` | 273 |
| `#opt-fold` | 274 |
| `#opt-caret` | 274 |
| `#opt-body` | 275 |
| `#layers` | 276 |
| `#chgwindow-hd` | 277 |
| `#chgwindow` | 278 |
| `#labpick-hd` | 287 |
| `#labpick` | 288 |
| `#labcut-hd` | 289 |
| `#labcut` | 290 |
| `#moneydetail-hd` | 295 |
| `#moneydetail` | 296 |
| `#amenity-hd` | 321 |
| `#amenity` | 322 |
| `#amenity-lrt-row` | 323 |
| `#amenity-lrt-on` | 324 |
| `#amenity-school-row` | 326 |
| `#amenity-school-on` | 327 |
| `#uses-prisms-hd` | 330 |
| `#uses-prisms` | 331 |
| `#uses-prisms-on` | 333 |
| `#devmode-hd` | 336 |
| `#devmode` | 337 |
| `#devmetric-hd` | 341 |
| `#devmetric` | 342 |
| `#devwindow-hd` | 347 |
| `#devwindow` | 348 |
| `#devdetail-hd` | 353 |
| `#devdetail` | 354 |
| `#prism-hd` | 358 |
| `#prism-row` | 359 |
| `#prism-opacity` | 361 |
| `#prism-opacity-val` | 362 |
| `#services-hd` | 364 |
| `#services` | 365 |
| `#denom-hd` | 464 |
| `#denom` | 465 |
| `#ratio-denom-hd` | 469 |
| `#ratio-denom` | 470 |
| `#hoodmode` | 480 |
| `#hoodmode-btn` | 481 |
| `#coloradj` | 493 |
| `#coloradj-btn` | 494 |
| `#budget-pod` | 501 |
| `#budget-btn` | 502 |
| `#share` | 509 |
| `#share-btn` | 510 |
| `#a11y` | 513 |
| `#a11y-btn` | 514 |
| `#a11y-menu` | 515 |
| `#theme` | 517 |
| `#palette` | 522 |
| `#labels-on` | 529 |
| `#reference-on` | 537 |
| `#about` | 542 |
| `#about-btn` | 543 |
| `#about-menu` | 544 |
| `#about-src-roads` | 556 |
| `#about-src-services` | 557 |
| `#about-vintage` | 590 |
| `#about-build` | 594 |
| `#about-lot-acres` | 599 |
| `#about-modelled-roads` | 610 |
| `#about-modelled` | 632 |
| `#about-budget` | 642 |
| `#about-budget-lead` | 644 |
| `#about-budget-rows` | 645 |
| `#about-budget-note` | 646 |
| `#about-updated` | 658 |
| `#botleft` | 662 |
| `#compass` | 663 |
| `#rot-ccw` | 664 |
| `#tonorth` | 671 |
| `#needle` | 673 |
| `#rot-cw` | 678 |
| `#viewbtns` | 686 |
| `#recenter` | 688 |
| `#center2d` | 689 |
| `#legend` | 691 |
| `#legend-label` | 692 |
| `#legend-min` | 694 |
| `#legend-max` | 694 |
| `#legend-cats` | 696 |
| `#revmix` | 5675 |
| `#svccost` | 5769 |

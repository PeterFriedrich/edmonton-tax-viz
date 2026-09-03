# Findings — Observed NRP Reconstruction Spend vs the Modelled $50/road-m/yr

Captured 2026-09-03 (S136). **The first check the roads cost model has ever
faced against observed money.** Every prior verification — the S114 back-solve,
the demoted 3% set-aside, the two-bases rule — compared the model to published
*unit rates*, most of them from the same City page the model is built on. This
one compares it to dollars the City actually approved for named neighbourhoods.

Sources, all committed and re-derivable without a fresh pull:

- `data/capital_budget.csv` (1,884 rows, FY2023–2037, committed 2026-08-22;
  `data/DATA.md` §19) — service **`Neighbourhoods`**, branch *Building Great
  Neighbourhoods*.
- `web/data/neighbourhood_value_per_acre.geojson` (406 neighbourhoods) —
  `road_m_per_acre`, the collector+local centreline density the roads lens ships.
- `data/city_unit_costs.json` → `roadway_om_renewal` — the published per-km
  figures and the $50/road-m/yr the site serves.

Road metres per neighbourhood are **derived** here as
`road_m_per_acre × boundary acres`, with acres taken from the served geometry
reprojected to **EPSG:3400** (the project's projected CRS). That reproduces
**672.4 km²** across the 406 boundaries and **3,024 km** of collector+local
centreline citywide — the pipeline's own `road_m_total` quantity, which is not
itself exported.

## 1. The Neighbourhood Renewal Program does publish per-neighbourhood spend

This answers the question asked of an external research pass on 2026-09-02
(*"is there a better source class entirely — does the NRP publish actual
per-neighbourhood spend?"*). **It does, and the data was already in the repo.**
The round that went out returned these profiles only as a *trap* — the
`CM-25-0000` composite undercount in `DATA.md` §19 — and never as the answer.

Service `Neighbourhoods`: **50 profiles, 217 rows, $716,465,000** approved,
fiscal years **2023–2029** ($526,466,000 of it in FY2023–26). **43 of the 50
profiles name a real neighbourhood** and match the served set, covering **45
distinct neighbourhoods** and **$660,287,000**. The 7 that do not match are a
street project, a cemetery phase, and program-level composites.

⚠️ **Coverage is roughly half what the profile count suggests.** Only **20
profiles carry $8M or more**, and those 20 hold **$654,281,000 of the
$660,287,000 across 24 neighbourhoods**. The remaining 23 matched profiles run
down to **$1,000** — residual or carrying amounts that mean *the profile exists
in the ledger*, not *this neighbourhood was rebuilt in this cycle*. Counting all
43 as reconstructions overstates coverage about 2×. **The usable series is ~24
neighbourhoods out of 406.**

## 2. Alley-only profiles are a different animal and must be separated first

Splitting the 20 by whether the profile title says *Neighbourhood* or only
*Alley* separates the distribution cleanly — the six alley-only profiles are six
of the seven cheapest, and the gap between the groups is ~6×:

| scope | profiles | approved | collector+local | aggregate | median |
|---|---|---|---|---|---|
| **Alley only** | 6 | $55,270,000 | 87.2 km | **$634/m** | $673/m |
| **Full reconstruction** | 14 | $599,011,000 | 159.2 km | **$3,762/m** | $4,259/m |

Full-reconstruction profiles, cheapest first (per metre of collector+local
centreline in the matched neighbourhood(s)):

| $/m | approved | road m | share by FY26 | last FY | neighbourhood(s) |
|---|---|---|---|---|---|
| 1,229 | $12,319,000 | 10,026 | 100% | 2025 | Beaumaris |
| 1,431 | $10,433,000 | 7,292 | 100% | 2025 | Garneau |
| 1,774 | $29,051,000 | 16,372 | 52% | 2027 | Glenwood |
| 1,829 | $25,587,000 | 13,992 | 100% | 2025 | Calder |
| 3,631 | $89,810,000 | 24,734 | 82% | 2027 | Ottewell |
| 3,737 | $45,032,000 | 12,049 | 100% | 2026 | Baturyn |
| 4,048 | $66,341,000 | 16,390 | 28% | 2029 | Homesteader, Overlanders |
| 4,471 | $39,273,000 | 8,784 | 36% | 2028 | Hillview |
| 4,823 | $35,663,000 | 7,394 | 100% | 2026 | Meyokumin |
| 5,572 | $34,102,000 | 6,120 | 100% | 2026 | Boyle Street |
| 5,616 | $64,544,000 | 11,493 | 100% | 2026 | McCauley |
| 5,702 | $30,587,000 | 5,364 | 100% | 2026 | Gariepy |
| 5,911 | $26,716,000 | 4,519 | 100% | 2026 | Hairsine |
| 6,094 | $89,553,000 | 14,696 | 22% | 2029 | Dunluce |

## 3. The result: observed reconstruction is about **2× the published rate**

The City publishes **renew and replace = $1,900,000/km = $1,900/road-m**, and
the shipped $50/road-m/yr annualizes it over a 50-year life as the **$38/m/yr**
renewal half. Observed full reconstruction runs **$3,762/m aggregate, median
$4,259/m** — **2.0–2.2×** the published figure, with **10 of 14** profiles above
2× and only four at or below it.

**At face value that would put the renewal half near $75/m/yr and the lifecycle
rate near $87/m/yr rather than $50.** ⚠️ **Do not make that change** — see §4.
The finding is directional, and the direction is the point: it lands on the same
side as the open 25-vs-50 service-life question. **Both unresolved questions push
the $50 rate the same way, toward being a floor.** `roadway_om_renewal.sensitivity`
already calls the rate "a mild lower bound" for a different reason (collectors
cost more per metre than locals); this is a third, larger reason.

## 4. ⚠️ Why this cannot become a rate yet — two biases of opposite sign

**Inflating $/m (numerator too broad):** an NRP reconstruction bundles alleys,
sidewalks, streetlights, drainage and landscaping with the roadway, and **neither
the profile listing nor the API carries sub-asset detail** — the City's own
category merges pathways with roadways. The denominator is collector+local
**centreline metres with alleys and arterials excluded**. The alley-only group
gives a crude handle on one component: alley work alone runs **$634 per metre of
road centreline**. Subtracting it leaves ~$3,128/m, still **1.6×** the published
$1,900. Sidewalks, lighting and drainage are not sized at all.

**Deflating $/m (numerator too small, or denominator too big):**

1. **Cycle-boundary tails.** Beaumaris, Garneau and Calder are 100% spent by FY26
   and end in **2025** — they read as the closing years of work begun in an
   earlier cycle, so their totals are a fraction of the project. ⚠️ **These are
   exactly the three that sit closest to the published $1,900/m**, which means
   the profiles most flattering to the current rate are the ones we have most
   reason to distrust.
2. **Sub-area projects.** *Glenwood (163 Street West)* and *NRP Recon - Newton
   (S/123 Ave)* name part of a neighbourhood while the denominator is the whole
   neighbourhood's road metres.
3. **Selection.** These 24 were chosen because they were *due* — old
   neighbourhoods in poor condition, not a random sample of the city.

**Verdict: the cross-check does NOT corroborate $1,900/m, and the sign of the
disagreement is robust to the corrections that can be made. It is not usable as
a replacement rate without a sub-asset decomposition of an NRP reconstruction** —
which is question §4.2 of the follow-up brief (`/home/opc/road_cost_sendback_brief.md`,
outside the repo).

⚠️ **This does not touch the OPERATING basis.** `roadway_ops` ($4.635/m/yr) is
maintenance and snow with no capital; reconstruction spend belongs to the
lifecycle basis only. See `city_unit_costs.json._two_bases` — the 2.6× gap
between $12/m/yr and $4.635/m/yr is a separate open question and nothing here
speaks to it.

## 5. Reproduction

```python
import geopandas as gpd, pandas as pd, re
g = gpd.read_file('web/data/neighbourhood_value_per_acre.geojson')
g['acres'] = g.to_crs('EPSG:3400').geometry.area / 4046.8564224
g['road_m'] = g.road_m_per_acre * g.acres
rm = dict(zip(g.neighbourhood_name.str.upper(), g.road_m)); hoods = set(rm)

n = pd.read_csv('data/capital_budget.csv').query("service == 'Neighbourhoods'")

def match(pr):                       # profile title -> served neighbourhood name(s)
    up = re.sub(r'^(NRP|NARP)[/A-Z]*\s+RECON\s*-\s*', '', pr.upper())
    for pat in (r'\b(NEIGHBOURHOOD|NEIGHBORHOOD|NBHD)S?\b',
                r'\b(AND\s+)?ALLEY(S)?\b',
                r'\b(RECONSTRUCTION|RENEWAL|REVITALIZATION|RECON)\b'):
        up = re.sub(pat, '', up)
    f = [h for h in hoods if re.search(r'(?<![A-Z])' + re.escape(h) + r'(?![A-Z])', up)]
    return sorted(h for h in f if not any(h != o and h in o for o in f))  # drop substrings

for pr, amt in n.groupby('profile')['approved'].sum().items():
    m = match(pr)
    if not m or amt < 8e6:           # the $8M floor drops residual carrying amounts
        continue
    alley_only = 'ALLEY' in pr.upper() and 'NEIGHBO' not in pr.upper()
    metres = sum(rm[h] for h in m)
    print('%-11s $%6.0f/m  %s' % ('alley-only' if alley_only else 'full',
                                  amt / metres, ', '.join(m)))
```

⚠️ **The `$8M` floor is a judgement, not a published threshold.** It was chosen
because the distribution has a clean gap there — $8.08M then $1.19M, with nothing
between — and every profile below it is a residual. Re-check the gap before
reusing the floor on a later budget vintage.

# Findings — Observed NRP Reconstruction Spend vs the Modelled $50/road-m/yr

Captured 2026-09-03 (S136). **The first check the roads cost model has ever
faced against observed money.** Every prior verification — the S114 back-solve,
the demoted 3% set-aside, the two-bases rule — compared the model to published
*unit rates*, most of them from the same City page the model is built on. This
one compares it to dollars the City actually approved for named neighbourhoods.

⚠️ **CORRECTED the same day, before any reader acted on it.** The first run
derived hood road metres from the **served** `neighbourhood_value_per_acre.geojson`
geometry, which carries a display setback and simplification and understates area
**~16%** — the exact trap `FINDINGS_utility_validation.md` §4 was written to
prevent. Every `$/m` was therefore ~16% too high (full reconstruction read
$3,762/m aggregate; it is **$3,151/m**). The conclusion is unchanged in sign and
weaker in size. **Use `load_boundaries()` full-resolution `area_acres`, never the
web geometry, for any hood total.**

Sources, all committed and re-derivable without a fresh pull:

- `data/capital_budget.csv` (1,884 rows, FY2023–2037, committed 2026-08-22;
  `data/DATA.md` §19) — service **`Neighbourhoods`**, branch *Building Great
  Neighbourhoods*.
- `web/data/neighbourhood_value_per_acre.geojson` (406 neighbourhoods) —
  `road_m_per_acre`, the collector+local centreline density the roads lens ships.
- `data/raw/neighbourhoods.geojson` via `src.load_boundaries.load_boundaries` —
  full-resolution `area_acres` (EPSG:3400), the pipeline's own denominator.
- `data/city_unit_costs.json` → `roadway_om_renewal` — the published per-km
  figures and the $50/road-m/yr the site serves.

Road metres per neighbourhood are **derived** as `road_m_per_acre × area_acres`,
joining the two on `neighbourhood_name` (**406/406 matched, no drops**). That
gives **193,237 acres** and **3,654 km** of collector+local centreline citywide —
the pipeline's own `road_m_total`, which is not itself exported. (The served
geometry alone would give 166,155 acres and 3,024 km: the 1.163× gap is the
setback plus simplification.)

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
| **Alley only** | 6 | $55,270,000 | 106.0 km | **$521/m** | $568/m |
| **Full reconstruction** | 14 | $599,011,000 | 190.1 km | **$3,151/m** | $3,528/m |

Full-reconstruction profiles, cheapest first (per metre of collector+local
centreline in the matched neighbourhood(s)):

| $/m | approved | road m | share by FY26 | last FY | neighbourhood(s) |
|---|---|---|---|---|---|
| 1,026 | $12,319,000 | 12,003 | 100% | 2025 | Beaumaris |
| 1,110 | $10,433,000 | 9,402 | 100% | 2025 | Garneau |
| 1,528 | $25,587,000 | 16,741 | 100% | 2025 | Calder |
| 1,535 | $29,051,000 | 18,924 | 52% | 2027 | Glenwood |
| 3,138 | $45,032,000 | 14,348 | 100% | 2026 | Baturyn |
| 3,216 | $89,810,000 | 27,925 | 82% | 2027 | Ottewell |
| 3,339 | $66,341,000 | 19,871 | 28% | 2029 | Homesteader, Overlanders |
| 3,718 | $39,273,000 | 10,564 | 36% | 2028 | Hillview |
| 3,995 | $35,663,000 | 8,926 | 100% | 2026 | Meyokumin |
| 4,246 | $30,587,000 | 7,204 | 100% | 2026 | Gariepy |
| 4,246 | $34,102,000 | 8,031 | 100% | 2026 | Boyle Street |
| 4,625 | $26,716,000 | 5,776 | 100% | 2026 | Hairsine |
| 4,754 | $64,544,000 | 13,578 | 100% | 2026 | McCauley |
| 5,324 | $89,553,000 | 16,819 | 22% | 2029 | Dunluce |

## 3. The result: observed reconstruction runs **1.7× the published rate**

The City publishes **renew and replace = $1,900,000/km = $1,900/road-m**, and
the shipped $50/road-m/yr annualizes it over a 50-year life as the **$38/m/yr**
renewal half. Observed full reconstruction runs **$3,151/m aggregate, median
$3,528/m** — **1.66× / 1.86×** the published figure. **10 of the 14 profiles
exceed $1,900/m; 6 exceed twice it.**

**At face value that would put the renewal half near $63/m/yr and the lifecycle
rate near $75/m/yr rather than $50.** ⚠️ **Do not make that change** — see §4.
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
gives a crude handle on one component: alley work alone runs **$521 per metre of
road centreline**. Subtracting it leaves ~$2,630/m, still **1.38×** the published
$1,900. Sidewalks, lighting and drainage are not sized at all.

**Deflating $/m (numerator too small, or denominator too big):**

1. **Cycle-boundary tails.** Beaumaris, Garneau and Calder are 100% spent by FY26
   and end in **2025** — they read as the closing years of work begun in an
   earlier cycle, so their totals are a fraction of the project. ⚠️ **These are
   exactly the three cheapest profiles in the set**, which means the evidence most
   flattering to the current rate is the evidence we have most reason to distrust.
2. **Sub-area projects.** *Glenwood (163 Street West)* and *NRP Recon - Newton
   (S/123 Ave)* name part of a neighbourhood while the denominator is the whole
   neighbourhood's road metres.
3. **Selection.** These 24 were chosen because they were *due* — old
   neighbourhoods in poor condition, not a random sample of the city.

**Verdict: the cross-check does NOT corroborate $1,900/m, and the sign of the
disagreement survives the corrections that can be made. It is not usable as a
replacement rate without a sub-asset decomposition of an NRP reconstruction** —
which is question §4.2 of the follow-up brief (`/home/opc/road_cost_sendback_brief.md`,
outside the repo).

⚠️ **This does not touch the OPERATING basis.** `roadway_ops` ($4.635/m/yr) is
maintenance and snow with no capital; reconstruction spend belongs to the
lifecycle basis only. See `city_unit_costs.json._two_bases` — the 2.6× gap
between $12/m/yr and $4.635/m/yr is a separate open question and nothing here
speaks to it.

## 5. Reproduction

```python
import sys; sys.path.insert(0, '.')
import geopandas as gpd, pandas as pd, re
from src.load_boundaries import load_boundaries

# ⚠️ full-res area_acres, NOT the served geometry (FINDINGS_utility_validation.md §4)
b = load_boundaries('data/raw/neighbourhoods.geojson')[['neighbourhood_name', 'area_acres']]
g = gpd.read_file('web/data/neighbourhood_value_per_acre.geojson')
g['NAME'] = g.neighbourhood_name.str.upper()
m = g.merge(b, left_on='NAME', right_on='neighbourhood_name', suffixes=('', '_b'))
assert len(m) == len(g), 'boundary join dropped hoods'
m['road_m'] = m.road_m_per_acre * m.area_acres
rm = dict(zip(m.NAME, m.road_m)); hoods = set(rm)

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
    m_ = match(pr)
    if not m_ or amt < 8e6:          # the $8M floor drops residual carrying amounts
        continue
    alley_only = 'ALLEY' in pr.upper() and 'NEIGHBO' not in pr.upper()
    metres = sum(rm[h] for h in m_)
    print('%-11s $%6.0f/m  %s' % ('alley-only' if alley_only else 'full',
                                  amt / metres, ', '.join(m_)))
```

⚠️ **The `$8M` floor is a judgement, not a published threshold.** It was chosen
because the distribution has a clean gap there — $8.08M then $1.19M, with nothing
between — and every profile below it is a residual. Re-check the gap before
reusing the floor on a later budget vintage.

⚠️ **`data/raw/neighbourhoods.geojson` is a static boundary file, not roll data**,
so this runs correctly against a stale `data/raw/` (which is the state of this
box — see the S135 handoff). The assessment CSVs are not read at all.

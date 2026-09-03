# Findings — Road Metres per Dwelling: the distribution, and why it is mostly density

Captured 2026-09-03 (S136), prompted by an externally-drafted task proposing
road-length-per-dwelling as the Roads lens's primary cost-driver metric, on the
Halifax HRM *Settlement Pattern and Form* precedent.

**Most of that task was already built.** `road_m_per_acre` ships; the dwelling
model (`load_water.build_connections`) ships; and road-per-dwelling itself was
computed 2026-07-07 in `FINDINGS_land_use_diversity.md` §3.2 as an analysis
variable. What had **never** been looked at is the thing this file records: its
**distribution**, and how it compares to the per-acre metric the site already
serves.

## 0. Method and vintage

- **Dwellings** — `load_water.build_connections` against a **2026-09-03 fresh
  pull** of both roll CSVs: **552,113 modeled dwellings across 351
  neighbourhoods**. ⚠️ `build_connections` reports **1,015 of 4,354 multi-res
  buildings with null/zero gross floor area, excluded** — their households are
  uncounted, so dense hoods' dwelling totals **understate** and their
  road-per-dwelling **overstates**.
- **Road metres** — `road_m_per_acre × area_acres`, acres from
  `load_boundaries()` full-resolution polygons. ⚠️ **Never the served geometry**,
  which carries a setback + simplification and understates area ~16%
  (`FINDINGS_utility_validation.md` §4).
- ⚠️ **Mixed vintage, stated plainly:** dwellings are 2026-09-03 fresh;
  `road_m_per_acre` comes from the last published refresh. The road network moves
  slowly and the roll does not, so the pairing is defensible — but it is a
  pairing, not one measurement.
- The re-pull also brought a **407th boundary** that has no served row; the join
  is on the 406 served hoods, **406/406 matched, no drops**.

**Analysis set:** `is_residential` and not `is_set_aside` and ≥100 dwellings →
**226 hoods**, less 4 flagged below → **n = 222**.

## 1. ⚠️ Four hoods have dwellings and effectively no city road — private roads, not clipping

The task that prompted this asked for near-zero road length to be flagged as a
likely boundary artifact. **It is not an artifact.** These are neighbourhoods
served by *private* internal roads, which carry no city-maintained centreline:

| road m/dw | dwellings | road m | neighbourhood |
|---|---|---|---|
| 0.00 | 1,059 | **1** | WESTVIEW VILLAGE |
| 0.11 | 845 | 95 | MAPLE RIDGE |
| 0.56 | 647 | 365 | EVERGREEN |
| 0.88 | 3,741 | 3,292 | CALLINGWOOD SOUTH |

⚠️ **The per-acre metric hides this and the per-dwelling metric detonates on
it.** Westview Village has one thousand dwellings behind a single metre of city
road; per-acre that reads as a merely low value, per-dwelling it is a division by
approximately nothing. **Any per-dwelling cost metric needs these four excluded
by name or the map ships four infinities.** (Three are manufactured-home or
private-road communities; MAPLE RIDGE already carries an open `gross_area` item
in `TODO.md`.)

## 2. The distribution (n = 222)

| statistic | road m / dwelling |
|---|---|
| min | 1.09 |
| p5 | 3.70 |
| p25 | 5.81 |
| **median** | **7.21** |
| p75 | 9.73 |
| p95 | 13.42 |
| max | 18.52 |
| mean / sd | 7.85 / 3.10 |

**Lowest** (dense): Garneau 1.09, Ermineskin 1.66, Abbottsfield 1.78, Canon Ridge
2.15, Strathcona 2.74, MacEwan 2.96, Rutherford 3.10.
**Highest** (large-lot, mostly west/southwest ravine estates): Laurier Heights
18.52, Grandview Heights 16.21, Quesnell Heights 16.11, Crestwood 16.09, Capilano
15.73, Ogilvie Ridge 15.69, Parkview 15.58.

**The ordering is exactly what built form predicts**, which is the sanity check
the metric needed and passes.

⚠️ **`is_residential` truncates the low end.** The densest mixed-use cores are
not in the set — **Downtown 0.53 m/dw** (19,797 dwellings) and **Wîhkwêntôwin
0.76** (22,218). Including them would widen max/min from 17× to ~35×.

## 3. It discriminates better than the shipped metric — and is ~80% density

Same 222 hoods, three quantities:

| metric | p10 | median | p90 | p90/p10 | max/min |
|---|---|---|---|---|---|
| **road m / dwelling** | 4.39 | 7.21 | 12.25 | **2.8×** | **17.0×** |
| road m / acre *(shipped)* | 32.07 | 40.93 | 50.79 | 1.6× | 3.1× |
| dwellings / acre | 3.71 | 5.49 | 8.37 | 2.3× | 16.3× |

Correlations on log10, same set:

| pair | r |
|---|---|
| road/dwelling vs **dwellings/acre** | **−0.888** |
| road/dwelling vs road/acre | +0.546 |
| road/acre vs dwellings/acre | −0.099 |

(Spearman rank, road/dwelling vs road/acre: **0.567** — it does reorder hoods.)

**The result, and it decides the question:** road supply per acre is nearly
constant across residential Edmonton — a **3.1× total range**, essentially
uncorrelated with density (−0.10). So `road_m ÷ dwellings` varies almost entirely
because the *denominator* varies. **At r = −0.888 on logs, density explains ~79%
of it.**

⚠️ **A road-per-dwelling map would re-plot dwelling density under a
cost-sounding name.** That is the same objection that made the electricity and
gas franchise lenses columns-only on 2026-07-07 — *"collinear with dwelling
count; a flat per-dwelling proxy makes every column `dwellings × constant`"* —
one step removed. Edmonton is not Halifax: the between-neighbourhood variation
in road *supply* that the Halifax argument turns on is largely absent here.

**What survives:** the residual ~21% is real road-supply variation, it is not
noise, and the metric genuinely separates Laurier Heights from Garneau better
than anything shipped. As a **cost-driver diagnostic** it earns its place. As a
**published map layer** it needs an answer to "why is this not the density map",
and that answer does not currently exist.

## 4. The Halifax comparison does not transfer

The prompting task cited HRM's ~**407 ft vs 5.2 ft** per dwelling and called it a
"~40x spread". ⚠️ **That is 78×, not 40×** — and it is a spread between
*settlement pattern types* across a region that includes rural and exurban land,
not between neighbourhoods of one built-up city. Edmonton's 222 residential
neighbourhoods span **17×** (2.8× p90/p10), or ~35× with the mixed-use cores
included. **The two numbers are not measuring the same population and should not
be presented as a benchmark either way.**

## 5. Reproduction

```python
import sys; sys.path.insert(0, 'src'); sys.path.insert(0, '.')
import geopandas as gpd
from load_boundaries import load_boundaries
from load_water import build_connections

conn = build_connections('data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv',
                         'data/raw/Property_Info__Current_Calendar_Year_.csv')
dw = conn.groupby('neighbourhood_name')['units'].sum().rename('dwellings')

b = load_boundaries('data/raw/neighbourhoods.geojson')[['neighbourhood_name', 'area_acres']]
g = gpd.read_file('web/data/neighbourhood_value_per_acre.geojson')
g['neighbourhood_name'] = g.neighbourhood_name.str.upper()
m = g.merge(b, on='neighbourhood_name').merge(dw, left_on='neighbourhood_name',
                                              right_index=True, how='left')
m['dwellings'] = m.dwellings.fillna(0)
m['road_m'] = m.road_m_per_acre * m.area_acres          # full-res acres, not web geometry

d = m[m.is_residential & ~m.is_set_aside & (m.dwellings >= 100)].copy()
d['rpd'] = d.road_m / d.dwellings
print(d[d.rpd < 1.0][['neighbourhood_name', 'dwellings', 'road_m', 'rpd']])   # the 4 private-road hoods
print(d[d.rpd >= 1.0].rpd.describe(percentiles=[.05, .25, .5, .75, .95]))
```

⚠️ Needs a **fresh, matched pull** of both roll CSVs — `build_connections` reads
them directly, and a stale or mismatched pair is a different measurement
(S135). `neighbourhoods.geojson` is static and safe either way.

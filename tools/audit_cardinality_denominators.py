"""One-off audit: does record-to-parcel cardinality distort the FIRST (neighbourhood)
lens, and what changes if we offered a lot-acre denominator there?

Answers ANALYSIS/TODO audit Q1 (WEM numerator), Q2 (condo denominator inflation),
Q5 (ground-acre vs summed-lot-acre gap) + the neighbourhood ranking shift. Uses the
SHIPPED dedupe heuristic (_point_lot_stats / SHARE_MAX_M2) so numbers match the grid.
Value-based (no mill rates needed) — the denominator swap is what's under test.
"""
import logging
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "src")
from load_assessment import load_assessment
from load_boundaries import load_boundaries
from load_property_info import load_property_info
from export_value_grid import _point_lot_stats, SHARE_MAX_M2

logging.basicConfig(level=logging.WARNING)
SQ_M_PER_ACRE = 4046.856422

ASSESS = "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
PINFO = "data/raw/Property_Info__Current_Calendar_Year_.csv"
BOUND = "data/raw/neighbourhoods.geojson"

a = load_assessment(ASSESS)
pinfo = load_property_info(PINFO)
a = a.merge(pinfo, on="account_number", how="left")
b = load_boundaries(BOUND)[["neighbourhood_name", "area_acres"]]

# ---- Q1: WEM numerator — accounts per exact point, citywide + Summerlea ----
pt = a.groupby(["latitude", "longitude"]).agg(
    n_accounts=("assessed_value", "size"),
    value=("assessed_value", "sum"),
    hood=("neighbourhood_name", "first"),
).reset_index()
print("=== Q1: record-to-point cardinality (numerator side) ===")
print(f"accounts total: {len(a):,}   distinct points: {len(pt):,}")
print(f"points with >1 account: {(pt.n_accounts>1).sum():,} "
      f"({(pt.n_accounts>1).mean()*100:.1f}% of points)")
print("top 5 points by account count:")
for _, r in pt.nlargest(5, "n_accounts").iterrows():
    print(f"  {r.hood:<28} {int(r.n_accounts):>5} accts  ${r.value/1e6:>8.1f}M")
print("top 5 points by summed value (the WEM-type needles):")
for _, r in pt.nlargest(5, "value").iterrows():
    print(f"  {r.hood:<28} {int(r.n_accounts):>5} accts  ${r.value/1e6:>8.1f}M")

# Does the neighbourhood numerator double-count? Only if identical value repeats
# within a point. Flag exact (value repeated) collisions.
dup_rows = a.duplicated(subset=["latitude", "longitude", "assessed_value"], keep=False)
susp = a[dup_rows & (a.assessed_value > 0)]
print(f"\nrows sharing (point, exact value) w/ another row: {len(susp):,} "
      f"= ${susp.assessed_value.sum()/1e6:.1f}M of ${a.assessed_value.sum()/1e9:.2f}B "
      f"({susp.assessed_value.sum()/a.assessed_value.sum()*100:.2f}%)")

# ---- Q2: condo denominator inflation — raw vs deduped lot acres per hood ----
per_point = _point_lot_stats(a[["latitude", "longitude", "lot_size"]])
pt_hood = a.drop_duplicates(["latitude", "longitude"])[["latitude", "longitude", "neighbourhood_name"]]
per_point = per_point.merge(pt_hood, on=["latitude", "longitude"], how="left")

# raw = every record carries its full lot_size (the naive/buggy denominator)
a["_lot_raw"] = a["lot_size"].where(a["lot_size"] > 0)
raw_lot = a.groupby("neighbourhood_name")["_lot_raw"].sum().rename("lot_m2_raw")
# deduped = shipped heuristic, eligible points only
ded_lot = (per_point[per_point.eligible]
           .groupby("neighbourhood_name")["lot_m2"].sum().rename("lot_m2_dedup"))

h = b.merge(raw_lot, on="neighbourhood_name", how="left") \
     .merge(ded_lot, on="neighbourhood_name", how="left")
h["lot_acres_raw"] = h["lot_m2_raw"] / SQ_M_PER_ACRE
h["lot_acres_dedup"] = h["lot_m2_dedup"] / SQ_M_PER_ACRE
h["overcount_pct"] = (h.lot_acres_raw / h.lot_acres_dedup - 1) * 100

city_raw, city_ded = h.lot_acres_raw.sum(), h.lot_acres_dedup.sum()
print("\n=== Q2: condo denominator inflation (raw lot-acre vs deduped) ===")
print(f"citywide summed lot acres: raw {city_raw:,.0f}  dedup {city_ded:,.0f}  "
      f"→ raw overcounts area by {(city_raw/city_ded-1)*100:.1f}%")
print("top 8 hoods by lot-area overcount (condo concentration):")
for _, r in h.nlargest(8, "overcount_pct").iterrows():
    print(f"  {r.neighbourhood_name:<26} raw {r.lot_acres_raw:>7.0f}ac  "
          f"dedup {r.lot_acres_dedup:>6.0f}ac  +{r.overcount_pct:>5.0f}%")

# ---- Q5: ground-acre vs summed-lot-acre gap (what ground includes lot excludes) ----
h["parcel_frac"] = h.lot_acres_dedup / h.area_acres  # parcel land / boundary land
print("\n=== Q5: ground-acre vs deduped-lot-acre (non-parcel land: roads/parks/ROW) ===")
valid = h[(h.area_acres > 0) & h.lot_acres_dedup.notna()]
print(f"citywide: boundary(ground) {h.area_acres.sum():,.0f}ac  "
      f"deduped parcel {city_ded:,.0f}ac  "
      f"→ parcel land is {city_ded/h.area_acres.sum()*100:.0f}% of ground area")
print(f"per-hood parcel/ground fraction — median {valid.parcel_frac.median()*100:.0f}%, "
      f"IQR {valid.parcel_frac.quantile(.25)*100:.0f}–{valid.parcel_frac.quantile(.75)*100:.0f}%, "
      f"range {valid.parcel_frac.min()*100:.0f}–{valid.parcel_frac.max()*100:.0f}%")

# ---- ranking shift: value/ground-acre vs value/lot-acre at the hood level ----
val = a.groupby("neighbourhood_name")["assessed_value"].sum().rename("value")
elig_val = a.merge(per_point[["latitude", "longitude", "eligible"]],
                   on=["latitude", "longitude"], how="left")
elig_val = elig_val[elig_val.eligible.fillna(False)]
val_elig = elig_val.groupby("neighbourhood_name")["assessed_value"].sum().rename("value_elig")
h = h.merge(val, on="neighbourhood_name", how="left").merge(val_elig, on="neighbourhood_name", how="left")
h["vpa_ground"] = h.value / h.area_acres
h["vpa_lot"] = h.value_elig / h.lot_acres_dedup
r = h[(h.vpa_ground > 0) & (h.vpa_lot > 0)].copy()
r["rank_ground"] = r.vpa_ground.rank(ascending=False)
r["rank_lot"] = r.vpa_lot.rank(ascending=False)
r["rank_move"] = (r.rank_ground - r.rank_lot)
print("\n=== ranking shift: value/ground-acre  →  value/lot-acre (n=%d hoods) ===" % len(r))
print(f"Spearman rank corr: {r.rank_ground.corr(r.rank_lot):.3f}")  # pearson-of-ranks = spearman
print(f"hoods moving >20 ranks: {(r.rank_move.abs()>20).sum()}  "
      f">50 ranks: {(r.rank_move.abs()>50).sum()}")
r["boost"] = r.vpa_lot / r.vpa_ground
print("biggest RISERS under lot-acre (low parcel-frac = lots of park/ROW; boost = $/acre multiple):")
for _, x in r.nlargest(10, "rank_move").iterrows():
    print(f"  {x.neighbourhood_name:<26} ground#{int(x.rank_ground):>3} → lot#{int(x.rank_lot):>3} "
          f" ${x.vpa_ground/1e3:>5.0f}k → ${x.vpa_lot/1e3:>5.0f}k/ac  ×{x.boost:>3.1f}  "
          f"(parcel {x.parcel_frac*100:>3.0f}% of ground)")
print("biggest FALLERS under lot-acre:")
for _, x in r.nsmallest(6, "rank_move").iterrows():
    print(f"  {x.neighbourhood_name:<26} ground#{int(x.rank_ground):>3} → lot#{int(x.rank_lot):>3} "
          f" ${x.vpa_ground/1e3:>5.0f}k → ${x.vpa_lot/1e3:>5.0f}k/ac  ×{x.boost:>3.1f}  "
          f"(parcel {x.parcel_frac*100:>3.0f}% of ground)")

# how many low-parcel-fraction (park/river-valley) hoods get a real boost?
lowpf = r[r.parcel_frac < 0.55]
print(f"\nhoods with parcel <55% of ground (park/ROW/river-valley-heavy): {len(lowpf)}")
print(f"  their median $/acre boost under lot-acre: ×{lowpf.boost.median():.2f}  "
      f"(vs ×{r[r.parcel_frac>=0.55].boost.median():.2f} for the rest)")

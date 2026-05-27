"""
Investigation stub: neighbourhood name mismatches between assessment and boundary datasets.

Run this to audit the current state of name alignment. As mismatches are resolved,
add them to the correction dict in src/join_and_calculate.py (and document in DATA.md).

Known unresolved as of 2026-05-27:
  - OLIVER: in assessment, no match in boundaries
  - HERITAGE VALLEY TOWN CENTRE AREA: in assessment, no match in boundaries
  - LEWIS FARMS INDUSTRIAL (assessment) vs LEWIS FARMS BUSINESS EMPLOYMENT (boundary): genuine rename?

Questions to answer:
  1. Does OLIVER exist in the boundary file under a different name entirely?
     (e.g. OLIVER might be listed as part of another neighbourhood)
  2. Is HERITAGE VALLEY TOWN CENTRE AREA a new neighbourhood not yet in the boundary file?
  3. Are LEWIS FARMS INDUSTRIAL / LEWIS FARMS BUSINESS EMPLOYMENT the same polygon?
     Check neighbourhood_number to confirm.
"""

import sys
import geopandas as gpd

sys.path.insert(0, "src")
from load_assessment import load_assessment
from aggregate_by_neighbourhood import aggregate_by_neighbourhood

agg = aggregate_by_neighbourhood(
    load_assessment("data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv")
)
boundaries = gpd.read_file("data/raw/neighbourhoods.geojson")

assessment_names = set(agg["neighbourhood_name"])
boundary_names = set(boundaries["name"].str.strip().str.upper())

in_assessment_only = sorted(assessment_names - boundary_names)
in_boundary_only = sorted(boundary_names - assessment_names)

print("In assessment, not in boundaries:")
for n in in_assessment_only:
    row = agg[agg["neighbourhood_name"] == n].iloc[0]
    print(f"  {n!r:50s}  total_assessed_value={row['total_assessed_value']:,.0f}")

print("\nIn boundaries, not in assessment:")
for n in in_boundary_only:
    row = boundaries[boundaries["name"].str.strip().str.upper() == n].iloc[0]
    print(f"  {n!r:50s}  neighbourhood_number={row['neighbourhood_number']}")

print(f"\nTotal unmatched: {len(in_assessment_only)} assessment / {len(in_boundary_only)} boundary")

# Hint: check if OLIVER appears anywhere in boundary descriptive_name
print("\n--- Boundary rows containing 'OLIVER' ---")
print(boundaries[boundaries["descriptive_name"].str.upper().str.contains("OLIVER", na=False)][
    ["neighbourhood_number", "name", "descriptive_name"]
])

# Hint: check LEWIS FARMS variants by neighbourhood_number
print("\n--- Boundary rows containing 'LEWIS' ---")
print(boundaries[boundaries["name"].str.contains("LEWIS", na=False)][
    ["neighbourhood_number", "name", "descriptive_name"]
])

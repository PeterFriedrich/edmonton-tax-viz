"""
Findings from reverse-engineering open-property (Deno/Fresh app):
https://github.com/[author]/open-property

--- How lot_size works ---
lot_size is NOT calculated. It is a pre-computed number field returned directly
by Edmonton's open data API. The city provides it; this app just displays it.
No geometry math happens anywhere in the repo.

--- What the geo data actually is ---
The API returns a GeoJSON Point (single coordinate) per property, not a polygon:
  point_location: { type: "Point", coordinates: [lng, lat] }
Plus flat latitude/longitude fields. There is no parcel boundary or lot shape.
If you want polygon/boundary data, it's not here — Edmonton transferred parcel
GIS data to AltaLIS in 2021 and it's no longer freely available.

--- How the app queries the data ---
It uses Edmonton's Socrata Open Data API (SODA). Three datasets are queried by
account_number (a unique property ID):
  dkk9-cj3x  Property Info (current year): lot_size, zoning, lat/lng, neighbourhood
  q7d6-ambg  Assessment Data (current year): assessed_value
  qi6a-xuwt  Assessment Data (historical): assessed_value by year
The SODA query format is: /resource/{dataset_id}.json?$where=...&$limit=...

--- What this file is ---
Python equivalents of the four JS functions in the original app:
  search_address()         <- use_search_results.ts
  get_property_info()      <- queryInfo() in routes/[id].tsx       (has lot_size)
  get_current_assessment() <- queryCurrent() in routes/[id].tsx
  get_assessment_history() <- queryHistory() in routes/[id].tsx
"""

import requests

BASE = "https://data.edmonton.ca/resource"


# Mirrors the Consumer/Query chain in src/lib/data.edmonton.ca/soda_client.ts
def _soda_get(dataset_id: str, where: str, limit: int = 10) -> list[dict]:
    url = f"{BASE}/{dataset_id}.json"
    params = {"$where": where, "$limit": limit}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


# Mirrors queryInfo() in src/routes/[id].tsx
def get_property_info(account_number: str) -> dict | None:
    """Lot size, zoning, lat/lng, neighbourhood for a property."""
    rows = _soda_get("dkk9-cj3x", f"account_number='{account_number}'", limit=1)
    if rows:
        row = rows[0]
        return {
            "account_number": row.get("account_number"),
            "lot_size": float(row["lot_size"]) if row.get("lot_size") else None,
            "zoning": row.get("zoning"),
            "neighbourhood": row.get("neighbourhood"),
            "latitude": float(row["latitude"]) if row.get("latitude") else None,
            "longitude": float(row["longitude"]) if row.get("longitude") else None,
            "year_built": row.get("year_built"),
        }
    return None


# Mirrors queryCurrent() in src/routes/[id].tsx
def get_current_assessment(account_number: str) -> dict | None:
    """Most recent assessed value."""
    rows = _soda_get("q7d6-ambg", f"account_number='{account_number}'", limit=1)
    if rows:
        row = rows[0]
        return {
            "account_number": row.get("account_number"),
            "assessed_value": float(row["assessed_value"]) if row.get("assessed_value") else None,
            "assessment_year": int(row["assessment_year"]) if row.get("assessment_year") else None,
            "lot_size": float(row["lot_size"]) if row.get("lot_size") else None,
        }
    return None


# Mirrors queryHistory() + the toSorted() call in src/routes/[id].tsx
def get_assessment_history(account_number: str) -> list[dict]:
    """Assessed values sorted oldest → newest."""
    rows = _soda_get("qi6a-xuwt", f"account_number='{account_number}'", limit=20)
    history = [
        {
            "assessment_year": int(r["assessment_year"]) if r.get("assessment_year") else None,
            "assessed_value": float(r["assessed_value"]) if r.get("assessed_value") else None,
            "lot_size": float(r["lot_size"]) if r.get("lot_size") else None,
        }
        for r in rows
    ]
    return sorted(history, key=lambda r: r["assessment_year"] or 0)


# Mirrors useSearchResults() in src/lib/use_search_results.ts
def search_address(query: str, limit: int = 5) -> list[dict]:
    """
    Address search. Splits on whitespace to try suite/house/street combinations,
    same as the hasSpaceQuery/noSpaceQuery split in use_search_results.ts.
    """
    q = query.upper().strip()
    parts = q.split()

    if len(parts) == 1:
        where = (
            f"suite like '{q}%' "
            f"OR house_number like '{q}%' "
            f"OR street_name like '{q}%'"
        )
    else:
        house = parts[0]
        street = " ".join(parts[1:])
        where = (
            f"(house_number='{house}' AND street_name like '{street}%') "
            f"OR (suite='{house}' AND house_number like '{parts[1]}%' AND street_name like '{' '.join(parts[2:])}%')"
        )

    rows = _soda_get("dkk9-cj3x", where, limit=limit)
    return [
        {
            "account_number": r.get("account_number"),
            "address": f"{r.get('suite', '')} {r.get('house_number', '')} {r.get('street_name', '')}".strip(),
            "lot_size": float(r["lot_size"]) if r.get("lot_size") else None,
            "neighbourhood": r.get("neighbourhood"),
        }
        for r in rows
    ]


if __name__ == "__main__":
    results = search_address("9803 109 ST")
    for r in results:
        print(r)

    if results:
        acct = results[0]["account_number"]
        print("\nProperty info:", get_property_info(acct))
        print("Current assessment:", get_current_assessment(acct))
        print("History:", get_assessment_history(acct))

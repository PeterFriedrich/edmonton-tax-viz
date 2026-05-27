"""
Investigation stub: is Approach B (parcel lot_size) viable for $/acre?

The hypothesis for Approach B:
  Join dkk9-cj3x (lot_size) to q7d6-ambg (assessed_value) on account_number,
  then sum(assessed_value) / sum(lot_size) by neighbourhood.

The blocker: condos. If a 100-unit building has lot_size repeated on every unit
row, summing lot_size overcounts land area by 100x for dense neighbourhoods.

Questions to answer:
  1. Do condo units share an account_number with each other, or is account_number
     unique per unit? (If unique, lot_size is per-unit and summing it is wrong.)
  2. Is there a parcel_id or legal_description that groups units on the same land?
  3. How bad is the duplication in practice — pick a known condo address and check.

Starter: find a high-rise address and inspect its rows.
"""

import requests
import sys

sys.path.insert(0, "src")

BASE = "https://data.edmonton.ca/resource"


def soda_get(dataset_id, where, limit=20):
    resp = requests.get(
        f"{BASE}/{dataset_id}.json",
        params={"$where": where, "$limit": limit},
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Pick a known high-rise — 10180 103 ST is a downtown condo tower
    address = "10180 103 ST"
    house, street = address.split(" ", 1)

    print(f"=== Property Info (dkk9-cj3x) for {address} ===")
    rows = soda_get(
        "dkk9-cj3x",
        f"house_number='{house}' AND street_name like '{street}%'",
        limit=20,
    )
    for r in rows:
        print(
            r.get("account_number"),
            r.get("suite"),
            r.get("lot_size"),
            r.get("legal_description"),
        )

    print(f"\nTotal rows: {len(rows)}")
    lot_sizes = [float(r["lot_size"]) for r in rows if r.get("lot_size")]
    if lot_sizes:
        print(f"lot_size values: min={min(lot_sizes)}, max={max(lot_sizes)}, unique={len(set(lot_sizes))}")
        print("=> If unique==1 and len(rows)>1, lot_size is duplicated across units.")

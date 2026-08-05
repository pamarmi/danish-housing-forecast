"""
Danish Housing Price Forecasting Project
Helper: Explore available tables and their variables

Used to verify table IDs and see
what variables/values are available before fetching data.
"""

import requests
import json

BASE_URL = "https://api.statbank.dk/v1"


def search_tables(query: str, lang: str = "en") -> list:
    """Search for tables matching a keyword."""
    url = f"{BASE_URL}/tables"
    # Send a GET request to the API with the selected language.
    r = requests.get(url, params={"lang": lang}) 
    # Raise an exception if the API request failed.
    r.raise_for_status()
    # Parse the JSON response into Python objects.
    tables = r.json()
    # Return all tables whose text or ID contains the search keyword (case-insensitive).
    return [t for t in tables if query.lower() in t.get("text", "").lower()
            or query.lower() in t.get("id", "").lower()]


def get_variables(table_id: str) -> dict:
    """Get all variables and their possible values for a table."""
    url = f"{BASE_URL}/tableinfo"
    # Send a POST request with the table ID and request the response in JSON format.
    r = requests.post(url, json={"table": table_id, "lang": "en", "format": "JSON"})
    # Raise an exception if the API request failed.
    r.raise_for_status()
    # Parse the JSON response into Python objects and return.
    return r.json()


# ── Search for housing-related tables ────────────────────────────────────────

print("Searching for housing price tables...")
results = search_tables("ejendom")
# Display the first 10 matching tables.
for t in results[:10]:
    # Print the table ID and a shortened description.
    print(f"  {t['id']:12s} | {t.get('text','')[:60]}")

print("\nSearching for property sales tables...")
results2 = search_tables("property")
for t in results2[:10]:
    print(f"  {t['id']:12s} | {t.get('text','')[:60]}")

# ── Inspect EJ121 variables ───────────────────────────────────────────────────

print("\n" + "="*50)
print("Variables in EJ121 (house price index):")
try:
    meta = get_variables("EJ121")
    for v in meta.get("variables", []):
        print(f"\n  Variable: {v['id']} — {v['text']}")
        for val in v.get("values", [])[:10]:
            print(f"    {val['id']:15s} {val['text']}")

except Exception as e2:
    print(f"  ERROR: {e2}")


# ── Inspect DNRNURI variables ───────────────────────────────────────────────────
print("\n" + "="*50)
print("Variables in DNRNURI (mortgage interest rates):")
try:
    meta = get_variables("DNRNURI")
    for v in meta.get("variables", []):
        print(f"\n  Variable: {v['id']} — {v['text']}")
        for val in v.get("values", [])[:10]:
            print(f"    {val['id']:15s} {val['text']}")

except Exception as e2:
    print(f"  ERROR: {e2}")

# ── Inspect AUP01 variables ───────────────────────────────────────────────────
print("\n" + "="*50)
print("Variables in AUP01 (unemployment):")
try:
    meta = get_variables("AUP01")
    for v in meta.get("variables", []):
        print(f"\n  Variable: {v['id']} — {v['text']}")
        for val in v.get("values", [])[:10]:
            print(f"    {val['id']:15s} {val['text']}")

except Exception as e2:
    print(f"  ERROR: {e2}")


# ── Inspect FOLK1A variables ───────────────────────────────────────────────────
print("\n" + "="*50)
print("Variables in FOLK1A (population):")
try:
    meta = get_variables("FOLK1A")
    for v in meta.get("variables", []):
        print(f"\n  Variable: {v['id']} — {v['text']}")
        for val in v.get("values", [])[:10]:
            print(f"    {val['id']:15s} {val['text']}")
except Exception as e2:
    print(f"  ERROR: {e2}")

# ── Inspect BYG5 variables ───────────────────────────────────────────────────
print("\n" + "="*50)
print("Variables in BYG5 (building permits):")
try:
    meta = get_variables("BYG5")
    for v in meta.get("variables", []):
        print(f"\n  Variable: {v['id']} — {v['text']}")
        for val in v.get("values", [])[:10]:
            print(f"    {val['id']:15s} {val['text']}")
except Exception as e2:
    print(f"  ERROR: {e2}")

print("\n Use the variable IDs above to modify the data collection in collect_data.py if needed.")
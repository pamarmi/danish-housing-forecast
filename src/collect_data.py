"""
Danish Housing Price Forecasting Project

This script fetches data from Statistics Denmark's API (Statistikbanken)
and saves it to the data/raw/ folder for further processing.

Tables used:
- EJ121  : Quarterly house prices (seasonally adjusted)
- DNRNURI: Mortgage interest rates (Danmarks Nationalbank)
- AUP01  : Unemployment rate
- FOLK1A : Population by region
- BYG5   : Building permits issued

Run explore_tables.py to inspect available variables and values for each table.

Author: Pablo Martínez-Miravé
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime

# ── Setup ────────────────────────────────────────────────────────────────────

BASE_URL = "https://api.statbank.dk/v1"
RAW_DIR  = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# ── Helper functions ──────────────────────────────────────────────────────────

def get_data(table_id: str, variables: list[dict]) -> pd.DataFrame:
    """
    Fetch data from Statistics Denmark API.

    Parameters
    ----------
    table_id  : DST table identifier, e.g. 'EJ121'
    variables : list of dicts with 'code' and 'values' keys
                Use ['*'] as values to get all available values.

    Returns
    -------
    pd.DataFrame with the raw data
    """
    url = f"{BASE_URL}/data"
    payload = {
        "table":     table_id,
        "format":    "BULK",
        "lang":      "en",
        "delimiter": "Semicolon",
        "variables": variables,
    }
    r = requests.post(url, json=payload)
    r.raise_for_status()

    # BULK format returns semicolon-separated text
    from io import StringIO
    df = pd.read_csv(StringIO(r.text), sep=";")
    return df


def save_raw(df: pd.DataFrame, name: str) -> None:
    """Save a DataFrame to data/raw/ as CSV."""
    path = os.path.join(RAW_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"  Saved {path}  ({len(df)} rows)")


# ── 1. Housing prices — EJ121 ─────────────────────────────────────────────────
# Seasonally adjusted price index for one-family houses, by quarter

print("\n[1/5] Fetching housing prices (EJ121)...")
try:
    df_prices = get_data(
        table_id="EJ121",
        variables=[
            {"code": "REGION",  "values": ["000"]},            # All Denmark
            {"code": "EJKAT20", "values": ["0111", "2103"]}, # Houses + flats
            {"code": "TAL",     "values": ["202"]},           # Price index seasonally adj.
            {"code": "Tid",     "values": ["*"]},             # All quarters
        ]

    )
    save_raw(df_prices, "housing_prices")
except Exception as e:
    print(f"  ERROR: {e}")
    print("  Try alternative table?")


# ── 2. Mortgage interest rates — DNRNURI ─────────────────────────────────────
# Danmarks Nationalbank: representative mortgage rates, quarterly

print("\n[2/5] Fetching mortgage interest rates (DNRNURI)...")
try:
    df_rates = get_data(
        table_id="DNRNURI",
        variables=[
            {"code": "DATA",     "values": ["AL51EFFR"]},  # Annualised agreed rate
            {"code": "INDSEK",   "values": ["1430"]},       # Households - employees
            {"code": "VALUTA",   "values": ["DKK"]},        # DKK only
            {"code": "LØBETID1", "values": ["ALLE"]},       # All maturities
            {"code": "RENTFIX",  "values": ["ALLE"]},       # All fixation periods
            {"code": "LAANSTR",  "values": ["ALLE"]},       # All loan sizes
            {"code": "Tid",      "values": ["*"]},           # All months
        ]

    )
    save_raw(df_rates, "interest_rates")
except Exception as e:
    print(f"  ERROR: {e}")


# ── 3. Unemployment — AUP01 ───────────────────────────────────────────────────
# Gross unemployment rate, quarterly

print("\n[3/5] Fetching unemployment (AUP01)...")
try:
    df_unemp = get_data(
        table_id="AUP01",
        variables=[
            {"code": "OMRÅDE",    "values": ["000"]},  # whole Denmark
            {"code": "ALDER",     "values": ["TOT"]},  #total
            {"code": "KØN",     "values": ["TOT"]},   #total
            {"code": "Tid",      "values": ["*"]},     #All months
        ]
    )
    save_raw(df_unemp, "unemployment")
except Exception as e:
    print(f"  ERROR: {e}")


# ── 4. Population — FOLK1A ────────────────────────────────────────────────────
# Population by region, quarterly

print("\n[4/5] Fetching population (FOLK1A)...")
try:
    df_pop = get_data(
        table_id="FOLK1A",
        variables=[
            {"code": "OMRÅDE",   "values": ["000"]},   # whole Denmark
            {"code": "KØN",      "values": ["*"]},
            {"code": "ALDER",    "values": ["IALT"]},  # all ages
            {"code": "CIVILSTAND","values": ["TOT"]},
            {"code": "Tid",      "values": ["*"]},
        ]
    )
    save_raw(df_pop, "population")
except Exception as e:
    print(f"  ERROR: {e}")


# ── 5. Building permits — BYG5 ────────────────────────────────────────────────
# Number of building permits issued, quarterly

print("\n[5/5] Fetching building permits (BYG5)...")
try:
    df_permits = get_data(
        table_id="BYG5",
        variables=[
            {"code": "HINDEKS", "values": ["01","02","03"]}, #Construction Cost Index for residential buildings, one-family houses, and multi-fmailiy houses
            {"code": "DINDEKS",   "values": ["10000"]},          # Construction Cost Index, total
            {"code": "ART",    "values": ["1002"]},          # total
            {"code": "Tid",        "values": ["*"]},         #all years
        ]
    )
    save_raw(df_permits, "building_permits")
except Exception as e:
    print(f"  ERROR: {e}")


# ── Summary ───────────────────────────────────────────────────────────────────

print("\n" + "="*50)
print("Data collection complete.")
print(f"Files saved to: {os.path.abspath(RAW_DIR)}")
print("="*50)

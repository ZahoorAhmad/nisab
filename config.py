"""
Configuration and constants for the Nisab (Zakat valuation) API.
Gold and silver price data live under data/gold and data/silver.
"""
from pathlib import Path

# Base path: repo root (parent of this file)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Price CSV paths: Date, Price_per_oz_PKR, Price_per_gram_PKR
GOLD_FILE = DATA_DIR / "gold" / "prices.csv"
SILVER_FILE = DATA_DIR / "silver" / "prices.csv"

# Zakat nisab: 1 tola = 11.6638 grams; silver nisab = 52.5 tolas
TOLA_GRAMS = 11.6638
SILVER_TOLAS = 52.5

# CSV date format (DD/MM/YY)
DATE_FMT = "%d/%m/%y"

# Default end year for Hijri range when running from a Gregorian date
DEFAULT_HIJRI_END_YEAR = 1448

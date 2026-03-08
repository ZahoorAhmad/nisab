"""
Nisab (Zakat threshold) calculation from a Gregorian date.
Uses gold and silver price data from data/gold and data/silver.
"""
from datetime import datetime

from hijri_converter import Hijri

from config import (
    DEFAULT_HIJRI_END_YEAR,
    GOLD_FILE,
    SILVER_FILE,
    TOLA_GRAMS,
    SILVER_TOLAS,
)
from utils import (
    load_prices,
    get_price_on_date,
    gregorian_to_hijri,
    get_hijri_month_name,
)


def run_from_gregorian_date(
    g_date: datetime,
    end_hijri_year: int = DEFAULT_HIJRI_END_YEAR,
) -> list[dict]:
    """
    Given a Gregorian date, convert it to Hijri, then compute nisab values
    for that Hijri day/month for each year from that Hijri year through end_hijri_year.

    Returns a list of dicts, each with:
      serial, hijri_date, gregorian_date, gold_1_tola_pkr, silver_52_5_tola_pkr
    (gold/silver are null when price data is missing for that date.)
    """
    gold_prices, gold_dates = load_prices(GOLD_FILE)
    silver_prices, silver_dates = load_prices(SILVER_FILE)

    h_year, h_month, h_day = gregorian_to_hijri(g_date)
    results = []
    serial = 0

    for year in range(h_year, end_hijri_year + 1):
        try:
            h_date = Hijri(year, h_month, h_day)
            g_date_row = h_date.to_gregorian()
        except ValueError:
            continue

        g_rate = get_price_on_date(gold_prices, gold_dates, g_date_row)
        s_rate = get_price_on_date(silver_prices, silver_dates, g_date_row)

        # 1 tola gold = TOLA_GRAMS grams; 52.5 tola silver = 52.5 * TOLA_GRAMS grams
        gold_val = round(g_rate * TOLA_GRAMS, 0) if g_rate is not None else None
        silver_grams = SILVER_TOLAS * TOLA_GRAMS
        silver_val = round(s_rate * silver_grams, 0) if s_rate is not None else None

        h_str = f"{h_day} {get_hijri_month_name(h_month)} {year}"
        g_str = g_date_row.strftime("%d-%b-%Y")

        serial += 1
        results.append({
            "serial": serial,
            "hijri_date": h_str,
            "gregorian_date": g_str,
            "gold_1_tola_pkr": int(gold_val) if gold_val is not None else None,
            "silver_52_5_tola_pkr": int(silver_val) if silver_val is not None else None,
        })

    return results

"""
Utility functions: load price CSVs, resolve price on a date, Gregorian↔Hijri.
"""
import csv
from datetime import date, datetime
from pathlib import Path

from hijri_converter import Gregorian, Hijri

from config import DATE_FMT, GOLD_FILE, SILVER_FILE


def load_prices(path: Path) -> tuple[dict[str, float], list[tuple[datetime, str]]]:
    """
    Load a price CSV (Date, Price_per_oz_PKR, Price_per_gram_PKR).
    Returns (prices_dict, sorted_dates):
      - prices_dict: {'DD/MM/YY': price_per_gram_PKR}
      - sorted_dates: [(date_obj, date_str), ...] sorted by date.
    """
    prices = {}
    rows = []
    if not path.exists():
        return prices, []

    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date_str = row["Date"].strip()
                price = float(row["Price_per_gram_PKR"].replace(",", ""))
                prices[date_str] = price
                dt = datetime.strptime(date_str, DATE_FMT)
                rows.append((dt, date_str))
            except (ValueError, KeyError):
                continue

    rows.sort(key=lambda x: x[0])
    return prices, rows


def get_price_on_date(
    prices: dict[str, float],
    _sorted_dates: list,
    target_date: date | datetime,
) -> float | None:
    """
    Return price_per_gram for target_date if present in data; else None.
    """
    date_str = target_date.strftime(DATE_FMT)
    return prices.get(date_str)


def gregorian_to_hijri(g_date: datetime) -> tuple[int, int, int]:
    """
    Convert a Gregorian date to Hijri.
    Returns (h_year, h_month, h_day).
    """
    gr = Gregorian(g_date.year, g_date.month, g_date.day)
    h = gr.to_hijri()
    return (h.year, h.month, h.day)


def get_hijri_month_name(month: int) -> str:
    """Return Hijri month name by number (1–12)."""
    months = [
        "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani",
        "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban",
        "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
    ]
    return months[month - 1]

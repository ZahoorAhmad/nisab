import csv
from datetime import datetime, timedelta
from pathlib import Path

from hijri_converter import Gregorian, Hijri

# Constants — data files in same directory as this script
SCRIPT_DIR = Path(__file__).resolve().parent
GOLD_FILE = SCRIPT_DIR / "updated_gold_prices_history.csv"
SILVER_FILE = SCRIPT_DIR / "updated_silver_prices_history.csv"

TOLA_G = 11.6638   # 1 tola = 11.6638 grams
SILVER_TOLAS = 52.5
DATE_FMT = "%d/%m/%y"   # CSV uses DD/MM/YY


def load_prices(filename):
    """
    Load CSV: Date, Price_per_oz_PKR, Price_per_gram_PKR.
    Returns (prices_dict, sorted_dates) for lookup and missing-date fallback.
    prices_dict: { 'DD/MM/YY': price_per_gram_PKR }
    sorted_dates: list of (date_obj, date_str) sorted by date_obj.
    """
    prices = {}
    rows = []
    path = Path(filename)
    if not path.exists():
        print(f"Error: {filename} not found.")
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


def get_price_on_date(prices, sorted_dates, target_date):
    """
    Get price_per_gram for target_date only if that date exists in the CSV.
    If the exact date is not present, return None (caller will show N/A).
    """
    date_str = target_date.strftime(DATE_FMT)
    return prices.get(date_str)


def convert_and_calculate(day, month, start_year, end_year):
    gold_prices, gold_dates = load_prices(GOLD_FILE)
    silver_prices, silver_dates = load_prices(SILVER_FILE)

    print(f"{'S.No':<6} | {'Hijri Date':<18} | {'Gregorian':<15} | {'1 Tola Gold (PKR)':<20} | {'52.5 Tola Silver (PKR)'}")
    print("-" * 92)

    serial = 0
    for year in range(start_year, end_year + 1):
        try:
            h_date = Hijri(year, month, day)
            g_date = h_date.to_gregorian()

            g_rate = get_price_on_date(gold_prices, gold_dates, g_date)
            s_rate = get_price_on_date(silver_prices, silver_dates, g_date)

            # 1 tola gold = TOLA_G grams; 52.5 tola silver = 52.5 * TOLA_G grams
            gold_val = f"PKR {g_rate * TOLA_G:,.0f}" if g_rate is not None else "N/A"
            silver_grams = SILVER_TOLAS * TOLA_G
            silver_val = f"PKR {s_rate * silver_grams:,.0f}" if s_rate is not None else "N/A"

            serial += 1
            h_str = f"{day} {get_month_name(month)} {year}"
            g_str = g_date.strftime("%d-%b-%Y")

            print(f"{serial:<6} | {h_str:<18} | {g_str:<15} | {gold_val:<20} | {silver_val}")

        except ValueError:
            continue


def get_month_name(n):
    months = [
        "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani", "Jumada al-ula",
        "Jumada al-akhira", "Rajab", "Sha'ban", "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
    ]
    return months[n - 1]


def gregorian_to_hijri(g_date):
    """
    Convert a Gregorian date to Hijri.
    g_date: date-like with .year, .month, .day (e.g. datetime.date or datetime).
    Returns: (h_year, h_month, h_day).
    """
    gr = Gregorian(g_date.year, g_date.month, g_date.day)
    h = gr.to_hijri()
    return (h.year, h.month, h.day)


def run_from_gregorian_date(g_date):
    """
    Convert the given Gregorian date to Hijri, then run the Zakat price
    calculation for that single date (1 tola gold, 52.5 tola silver).
    g_date: date-like with .year, .month, .day.
    """
    h_year, h_month, h_day = gregorian_to_hijri(g_date)
    convert_and_calculate(day=h_day, month=h_month, start_year=h_year, end_year=1448)


if __name__ == "__main__":
    # Option 1: fixed Hijri date (12 Ramadan) for a range of years
    # convert_and_calculate(day=12, month=9, start_year=1430, end_year=1448)

    # Option 2: single date from Gregorian — uncomment and set date:
    from datetime import date
    run_from_gregorian_date(date(year=2021, month=1, day=9))

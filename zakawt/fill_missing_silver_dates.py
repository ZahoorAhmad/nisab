#!/usr/bin/env python3
"""
Fill missing dates in silver_prices_history.csv using the mean of adjacent
(previous and next) values, then write an updated CSV with complete data.
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path

INPUT_CSV = Path(__file__).resolve().parent / "silver_prices_history.csv"
OUTPUT_CSV = Path(__file__).resolve().parent / "updated_silver_prices_history.csv"
DATE_FMT = "%d/%m/%y"


def parse_date(s: str) -> datetime:
    return datetime.strptime(s.strip(), DATE_FMT)


def format_date(d: datetime) -> str:
    return d.strftime(DATE_FMT)


def load_prices(path: Path) -> list[tuple[datetime, float, float]]:
    """Load CSV as (date, price_oz, price_gram) sorted by date."""
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                dt = parse_date(row["Date"])
                oz = float(row["Price_per_oz_PKR"].replace(",", ""))
                gram = float(row["Price_per_gram_PKR"].replace(",", ""))
                rows.append((dt, oz, gram))
            except (ValueError, KeyError):
                continue
    rows.sort(key=lambda x: x[0])
    return rows


def fill_missing(rows: list[tuple[datetime, float, float]]) -> list[tuple[datetime, float, float]]:
    """
    Insert missing dates between consecutive rows using the mean of
    the adjacent previous and next prices.
    """
    if not rows:
        return rows

    out = []
    for i in range(len(rows)):
        out.append(rows[i])
        if i + 1 >= len(rows):
            break
        prev_dt, prev_oz, prev_gram = rows[i]
        next_dt, next_oz, next_gram = rows[i + 1]
        delta = (next_dt - prev_dt).days
        if delta <= 1:
            continue
        # Fill days between prev_dt and next_dt (exclusive)
        for j in range(1, delta):
            fill_dt = prev_dt + timedelta(days=j)
            fill_oz = round((prev_oz + next_oz) / 2, 2)
            fill_gram = round((prev_gram + next_gram) / 2, 2)
            out.append((fill_dt, fill_oz, fill_gram))
    out.sort(key=lambda x: x[0])
    return out


def write_csv(path: Path, rows: list[tuple[datetime, float, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Price_per_oz_PKR", "Price_per_gram_PKR"])
        for dt, oz, gram in rows:
            w.writerow([format_date(dt), round(oz, 2), round(gram, 2)])


def main() -> None:
    if not INPUT_CSV.exists():
        raise SystemExit(f"Input file not found: {INPUT_CSV}")

    rows = load_prices(INPUT_CSV)
    print(f"Loaded {len(rows)} rows from {INPUT_CSV.name}")
    print(f"Date range: {format_date(rows[0][0])} to {format_date(rows[-1][0])}")

    filled = fill_missing(rows)
    added = len(filled) - len(rows)
    print(f"Filled {added} missing dates. Total rows: {len(filled)}")

    write_csv(OUTPUT_CSV, filled)
    print(f"Written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

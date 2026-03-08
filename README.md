# Nisab API

Zakat nisab valuation from a Gregorian date: converts to Hijri and returns gold (1 tola) and silver (52.5 tolas) values in PKR using historical price data.

## Layout

- **`data/gold/prices.csv`** — Gold price per gram (PKR) by date.
- **`data/silver/prices.csv`** — Silver price per gram (PKR) by date.  
  CSV format: `Date,Price_per_oz_PKR,Price_per_gram_PKR` (date as `DD/MM/YY`).
- **`config.py`** — Paths and constants (tola grams, date format).
- **`utils.py`** — Load CSVs, get price on date, Gregorian↔Hijri.
- **`nisab.py`** — `run_from_gregorian_date(g_date)` → list of nisab rows.
- **`api.py`** — FastAPI app exposing the flow.

## Run locally

```bash
pip install -r requirements.txt
uvicorn api:app --reload
```

- Docs: http://localhost:8000/docs  
- Example: `GET /nisab?date=2021-01-09`

## Run with Docker

```bash
docker-compose up --build
```

API on http://localhost:8000. `data/` is mounted read-only so gold/silver CSVs are available.

## API

- **`GET /health`** — Health check.
- **`GET /nisab?date=YYYY-MM-DD`** — Run nisab from the given Gregorian date.  
  Optional: `end_hijri_year` (default 1448).  
  Response: `{ "date": "...", "rows": [ { "serial", "hijri_date", "gregorian_date", "gold_1_tola_pkr", "silver_52_5_tola_pkr" }, ... ] }`.

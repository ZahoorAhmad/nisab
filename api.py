"""
REST API for Nisab (Zakat valuation) — run_from_gregorian_date flow.
"""
from datetime import datetime

from fastapi import FastAPI, Query, HTTPException

from nisab import run_from_gregorian_date

app = FastAPI(
    title="Nisab API",
    description="Zakat nisab values from gold/silver prices by Gregorian date.",
    version="1.0.0",
)


@app.get("/health")
def health():
    """Health check for Docker/load balancers."""
    return {"status": "ok"}


@app.get("/nisab")
def get_nisab(
    date: str = Query(
        ...,
        description="Gregorian date in YYYY-MM-DD format (e.g. 2021-01-09)",
    ),
    end_hijri_year: int = Query(
        1448,
        description="Last Hijri year to include in the range",
        ge=1,
        le=1500,
    ),
):
    """
    Run the nisab flow from a Gregorian date: convert to Hijri, then return
    gold (1 tola) and silver (52.5 tolas) nisab values in PKR for that
    Hijri day/month for each year up to end_hijri_year.
    """
    try:
        g_date = datetime.strptime(date.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date. Use YYYY-MM-DD (e.g. 2021-01-09).",
        )

    # run_from_gregorian_date expects a date-like with .year, .month, .day
    results = run_from_gregorian_date(g_date, end_hijri_year=end_hijri_year)
    return {"date": date, "rows": results}

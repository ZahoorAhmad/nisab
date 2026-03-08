import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime


def get_silver_prices_to_csv():
    # Define the starting year and get the current date info
    start_year = 2007
    current_year = datetime.now().year
    current_month = datetime.now().month
    filename = "silver_prices_history.csv"

    # Browser-like headers to avoid being blocked by the server
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Date', 'Price_per_oz_PKR', 'Price_per_gram_PKR'])

        print(f"Starting silver price scrape from {start_year} to {current_year}...")

        for year in range(start_year, current_year + 1):
            # Limit the last month to the current month if we are in the current year
            last_month = current_month if year == current_year else 12

            for month in range(1, last_month + 1):
                # Construct the silver-specific URL
                url = f"https://www.bullion-rates.com/silver/PKR/{year}-{month}-history.htm"

                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code != 200:
                        # Skip if the page does not exist (e.g., future months)
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Target the specific table ID used in the site's history pages
                    table = soup.find('table', {'id': 'dtDGrid'})

                    if not table:
                        continue

                    # Each record is stored in a row with the class 'DataRow'
                    rows = table.find_all('tr', class_='DataRow')
                    month_data_count = 0

                    for row in rows:
                        # Values (Date, Price/oz, Price/gram) are in cells with the class 'rate'
                        cells = row.find_all('td', class_='rate')
                        if len(cells) >= 3:
                            date = cells[0].text.strip()
                            # Clean the numeric data by removing commas for easier analysis
                            price_oz = cells[1].text.strip().replace(',', '')
                            price_gram = cells[2].text.strip().replace(',', '')

                            writer.writerow([date, price_oz, price_gram])
                            month_data_count += 1

                    print(f"Saved {month_data_count} silver records for {month}/{year}")

                    # Wait 1 second between requests to be polite to the server
                    time.sleep(1)

                except Exception as e:
                    print(f"\nError fetching silver data for {year}-{month}: {e}")
                    continue

    print(f"\nCompleted! Silver data saved to '{filename}'.")


if __name__ == "__main__":
    get_silver_prices_to_csv()
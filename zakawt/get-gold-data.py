import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime


def get_gold_prices_to_csv():
    # Define range and filename
    start_year = 2007
    current_year = datetime.now().year
    current_month = datetime.now().month
    filename = "gold_prices_history.csv"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Open CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Date', 'Price_per_oz_PKR', 'Price_per_gram_PKR'])

        print(f"Starting scrape from {start_year} to {current_year}...")

        for year in range(start_year, current_year + 1):
            last_month = current_month if year == current_year else 12

            for month in range(1, last_month + 1):
                url = f"https://www.bullion-rates.com/gold/PKR/{year}-{month}-history.htm"

                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code != 200:
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')
                    table = soup.find('table', {'id': 'dtDGrid'})

                    if not table:
                        continue

                    rows = table.find_all('tr', class_='DataRow')
                    month_data_count = 0

                    for row in rows:
                        cells = row.find_all('td', class_='rate')
                        if len(cells) >= 3:
                            date = cells[0].text.strip()
                            # Removing commas from prices so they are saved as clean numbers
                            price_oz = cells[1].text.strip().replace(',', '')
                            price_gram = cells[2].text.strip().replace(',', '')

                            writer.writerow([date, price_oz, price_gram])
                            month_data_count += 1

                    print(f"Saved {month_data_count} entries for {month}/{year}")

                    # Polite 1-second delay to avoid IP blocking
                    time.sleep(1)

                except Exception as e:
                    print(f"\nError fetching {year}-{month}: {e}")
                    continue

    print(f"\nSuccess! All data has been saved to '{filename}'.")


if __name__ == "__main__":
    get_gold_prices_to_csv()
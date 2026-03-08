from hijri_converter import Hijri


def convert_hijri_range(day, month, start_year, end_year):
    print(f"{'Hijri Date':<20} | {'Gregorian Date':<20}")
    print("-" * 45)

    for year in range(start_year, end_year + 1):
        try:
            # Create Hijri object
            hijri_date = Hijri(year, month, day)

            # Convert to Gregorian
            gregorian_date = hijri_date.to_gregorian()

            # Formatting for output
            h_str = f"{day} {get_month_name(month)} {year}"
            g_str = gregorian_date.strftime("%A, %d %B %Y")

            print(f"{h_str:<20} | {g_str:<20}")
        except ValueError:
            # Handles cases where the day might not exist in a specific Hijri year
            print(f"{day}/{month}/{year:<14} | Date does not exist in this Hijri year")


def get_month_name(n):
    months = ["Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani",
              "Jumada al-ula", "Jumada al-akhira", "Rajab", "Sha'ban",
              "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"]
    return months[n - 1]


# Configuration: 12 Ramadan (9th month) from 1430 to 1447
convert_hijri_range(day=12, month=9, start_year=1430, end_year=1447)
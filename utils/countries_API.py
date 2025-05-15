import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ggtravel',
    'user': 'root',
    'password': ''  # Use env vars or secrets management in production
}

# API and fields
COUNTRIES_API_URL = "https://restcountries.com/v3.1/all"
FIELDS = "name,cca2,currencies"

def get_countries():
    """Fetch countries data from REST Countries API."""
    url = f"{COUNTRIES_API_URL}?fields={FIELDS}"
    print(f"Fetching countries from URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch countries data")
        return []

def extract_country_info(country):
    """Extract relevant data for DB from API response."""
    try:
        common_name = country['name']['common']
        official_name = country['name']['official']
        cca2 = country['cca2']
        
        currencies = country.get('currencies', {})
        currency = ','.join(currencies.keys()) if currencies else None

        return {
            'commonname': common_name,
            'officialname': official_name,
            'cca2': cca2,
            'currency': currency
        }
    except KeyError as e:
        print(f"Missing field in data: {e}")
        return None

def update_countries_table(countries_data):
    """Insert or update country records in the database."""
    try:
        con = mysql.connector.connect(**DB_CONFIG)
        cursor = con.cursor()

        for country in countries_data:
            info = extract_country_info(country)
            if info is None:
                continue
            
            # UPSERT: Try to update first, then insert if not exists
            update_sql = """
                INSERT INTO country (commonname, officialname, cca2, currency)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    commonname = VALUES(commonname),
                    officialname = VALUES(officialname),
                    currency = VALUES(currency)
            """
            values = (
                info['commonname'],
                info['officialname'],
                info['cca2'],
                info['currency']
            )

            cursor.execute(update_sql, values)

        con.commit()
        print("Countries table updated.")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

if __name__ == "__main__":
    countries_data = get_countries()
    if countries_data:
        update_countries_table(countries_data)
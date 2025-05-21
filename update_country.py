import requests
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'kknb2025.mysql.pythonanywhere-services.com',
    'database': 'kknb2025$ggtravel',
    'user': 'kknb2025',
    'password': 'rootwsaa$ggtravel'
}

# API and fields
COUNTRIES_API_URL = "https://restcountries.com/v3.1/all?fields=name,capital,population,cca2,currencies,languages,flags,maps"

def update_countries():
    """Fetch and update countries data from REST Countries API."""
    url = f"{COUNTRIES_API_URL}"
    print("Starting country data update...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            countries = response.json()

            # Connect to the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # SQL query for inserting or updating country data
            update_sql = """
            INSERT INTO country (common_name, official_name, capital, population, cca2, currency, languages, flag_url, map_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                official_name = VALUES(official_name),
                capital = VALUES(capital),
                population = VALUES(population),
                currency = VALUES(currency),
                languages = VALUES(languages),
                flag_url = VALUES(flag_url),
                map_url = VALUES(map_url)
            """

            for country in countries:
                # Extract country data
                common_name = country.get('name', {}).get('common')
                official_name = country.get('name', {}).get('official')
                capital_list = country.get('capital')
                capital = capital_list[0] if capital_list else None
                population = country.get('population')
                cca2 = country.get('cca2')
                currency_dict = country.get('currencies', {})
                currency = ', '.join([currency_info.get('name', '') for currency_info in currency_dict.values()]) if currency_dict else None
                languages_dict = country.get('languages', {})
                languages = ', '.join(languages_dict.values()) if languages_dict else None
                flag_url = country.get('flags', {}).get('png')
                map_url = country.get('maps', {}).get('googleMaps')

                # Execute the query
                cursor.execute(update_sql, (
                    common_name,
                    official_name,
                    capital,
                    population,
                    cca2,
                    currency,
                    languages,
                    flag_url,
                    map_url
                ))

            # Commit the transaction
            conn.commit()
            print("Countries data updated successfully.")

        else:
            print(f"Failed to fetch countries data. Status code: {response.status_code}")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    update_countries()
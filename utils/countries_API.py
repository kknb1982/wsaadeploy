import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ggtravel',
    'user': 'root',
    'password': ''  
}

# API and fields
COUNTRIES_API_URL = "https://restcountries.com/v3.1/all?fields=name,capital,population,cca2,currencies,languages,flags,maps"

def get_countries():
    """Fetch countries data from REST Countries API."""
    url = f"{COUNTRIES_API_URL}"
    print(f"Fetching countries from URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            countries = response.json()
            insert_query = """
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


            # Connect to the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            for country in countries:
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

                cursor.execute(insert_query, (
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
            print("Countries data inserted successfully.")

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
                INSERT INTO country (common_name, official_name, capital, population, cca2, currency ,flag_url, map_url)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    common_name = VALUES(common_name),
                    official_name = VALUES(official_name),
                    capital = VALUES(capital),
                    population = VALUES(population),
                    currency = VALUES(currency)
                    flag_url = VALUES(flag_url),
                    map_url = VALUES(map_url)
            """
            values = (
                info['common_name'],
                info['official_name'],
                info['capital'],
                info['population'],
                info['cca2'],
                info['currency'],
                info['flag_url'],
                info['map_url']
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

import requests
import os
import json
from datetime import datetime, timedelta

COUNTRIES_API_URL = "https://restcountries.com/v3.1/all"
FIELDS = "name,cca2,capital,car,currencies,flags,languages,maps"
CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/countries_cache.json')
CACHE_EXPIRY_DAYS = 7

def get_countries():
    try:
        # Ensure the data folder exists
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        
        if os.path.exists(CACHE_FILE):
            print("Cache file found. Loading data from cache.")
            with open(CACHE_FILE, 'r') as cache_file:
                cache_data = json.load(cache_file)
                last_updated = datetime.strptime(cache_data['timestamp'], '%Y-%m-%dT%H:%M:%S')
                if (datetime.now() - last_updated).days < CACHE_EXPIRY_DAYS:
                    print("Using cached countries data.")
                    return cache_data['data']
        
        # If cache is missing or expired, fetch fresh data from the API
        url = f"{COUNTRIES_API_URL}?fields={FIELDS}"
        print(f"Fetching countries from URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            countries_data = response.json()

            # Update the cache with the new data and timestamp
            with open(CACHE_FILE, 'w') as cache_file:
                json.dump({
                    'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    'data': countries_data
                }, cache_file)

            return countries_data
        else:
            print(f"Error fetching countries: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None


def get_country_details(country_name):
    with open(CACHE_FILE, 'r') as f:
        countries_data = json.load(f)
        
    print(f"Searching for country: {country_name}")  # Debugging log
    available_countries = [country['name']['common'].lower() for country in countries_data['data']]
    print(f"Available countries: {available_countries}")  # Debugging log

    for country in countries_data['data']:
        if country['name']['common'].lower() == country_name.lower():
            return {
                'name': country['name']['common'],
                'official_name': country['name']['official'],
                'capital': country.get('capital', ['N/A'])[0],
                'cca2': country.get('cca2', 'N/A'),  # Ensure cca2 is included
                'languages': ', '.join(country.get('languages', {}).values()),
                'currencies': ', '.join([currency['name'] for currency in country.get('currencies', {}).values()]),
                'flag': country.get('flags', {}).get('png', ''),
                'maps': country.get('maps', {}).get('googleMaps', '')
            }
    return None
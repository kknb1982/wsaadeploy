import requests
import json
import os

def fetch_country_slugs():
    url = "https://www.gov.uk/api/content/foreign-travel-advice"
    response = requests.get(url)
    data = response.json()

    country_map = {}

    for item in data.get('links', {}).get('children', []):
        country_name = item.get('title', '').strip()
        base_path = item.get('base_path', '')
        slug = base_path.split('/')[-1]  # Get the last part of URL

        if country_name and slug:
            country_map[country_name] = slug

# Save to JSON file in the staticpages directory
    staticpages_dir = os.path.dirname(__file__)  # Get the directory of this script
    file_path = os.path.join(staticpages_dir, 'country_slugs.json')

    with open(file_path, 'w') as f:
        json.dump(country_map, f, indent=2)

    print(f"Saved {len(country_map)} countries to {file_path}.")

if __name__ == "__main__":
    fetch_country_slugs()
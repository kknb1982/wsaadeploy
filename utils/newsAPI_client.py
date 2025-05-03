import os
import json
import requests
from datetime import datetime, timedelta
from data_handler import current_travel

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(CONFIG_FILE_PATH, 'r') as config_file:
    config = json.load(config_file)
    
WEBZIO_API_KEY = config.get('WEBZIO_API_KEY')

if not WEBZIO_API_KEY:
    raise ValueError("WEBZIO_API_KEY not found in config.json")

WEBZIO_URL = "https://api.webz.io/newsApiLite"

def fetch_news(location):
    query = f"(+{location})"
    
    parameters = {
        'token': WEBZIO_API_KEY,
        'q': query
    }
    
    # Prepare the full URL with parameters
    request = requests.Request('GET', WEBZIO_URL, params=parameters).prepare()
    print(f"Fetching news from URL: {request.url}")  # Print the full URL
    
    # Make the API request
    response = requests.get(WEBZIO_URL, params=parameters)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

# Test the function
news = fetch_news("Australia")
print(news)
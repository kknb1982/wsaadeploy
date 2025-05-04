import os
import json
import requests
from datetime import datetime, timedelta
from .data_handler import current_travel

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(CONFIG_FILE_PATH, 'r') as config_file:
    config = json.load(config_file)

NEWS_API_KEY = config.get('NEWS_API_KEY')
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in config.json")

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(current_travel):
    # Construct the query parameters
    city = current_travel['city']
    country = current_travel['country']
    today = datetime.now()
    three_days_ago = today - timedelta(days=3)
    today = today.strftime('%Y-%m-%d')
    three_days_ago = three_days_ago.strftime('%Y-%m-%d')

    parameters = {
        'q': f"(+{country}) AND (shooting OR killed OR injured OR disaster OR risk OR danger)",
        'from': three_days_ago,
        'to': today,
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }
    
    # Prepare the full URL with parameters
    request = requests.Request('GET', NEWS_API_URL, params=parameters).prepare()
    print(f"Fetching news from URL: {request.url}")  # Print the full URL
    
    # Make the API request
    response = requests.get(NEWS_API_URL, params=parameters)
    if response.status_code == 200:
        data = response.json()
        return [{"title": article['title'], "url": article['url']} for article in data.get('articles', [])]
    else:
        print(f"Error fetching news: {response.status_code}, {response.text}")
        return None



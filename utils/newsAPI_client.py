import os
import json
import requests
from datetime import datetime, timedelta
from utils.data_handler import current_travel

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(CONFIG_FILE_PATH, 'r') as config_file:
    config = json.load(config_file)

NEWS_API_KEY = config.get('NEWS_API_KEY')
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in config.json")

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(current_travel, keywords='', search_in='title,description,content'):
    
    news_results = []
    
    # Construct the query parameters
    for travel in current_travel:
        city = travel.get('city', '')
        country = travel.get('country', '')
        today = datetime.now()
        three_days_ago = today - timedelta(days=3)
        today = today.strftime('%Y-%m-%d')
        three_days_ago = three_days_ago.strftime('%Y-%m-%d')

    parameters = {
        'q': f"{keywords} {city} {country}".strip(),
        'searchIn': search_in,
        'from': three_days_ago,
        'to': today,
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }
    
    # Make the API request
    response = requests.get(NEWS_API_URL, params=parameters)
    if response.status_code == 200:
        data = response.json()
        articles = [{"title": article['title'], "url": article['url']} for article in data.get('articles', [])]
        news_results.append({'travel': travel, 'articles': articles})
    else:
        print(f"Error fetching news for {city}, {country}: {response.status_code}, {response.text}")
        news_results.append({'travel': travel, 'articles': []})

    return news_results



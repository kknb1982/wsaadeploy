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

NEWS_API_URL = "https://newsapi.org/v2/everything"

HEADLINES_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(keyword='', search_in='title,description,content', date_from=None, date_to=None):
    if not keyword:
        keyword = 'news'  # Default keyword if none is provided
    if not date_from:
        date_from = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    if not date_to:
        date_to = datetime.now().strftime('%Y-%m-%d')
        
    parameters = {
        'q': keyword.strip(),
        'searchIn': search_in,
        'from': date_from,
        'to': date_to,
        'language': 'en',
        'apiKey': NEWS_API_KEY
    }
    # Make the API request
    response = requests.get(NEWS_API_URL, params=parameters)
    if response.status_code == 200:
        data = response.json()
        return [{"title": article['title'], "description": article.get('description', ''), "url": article['url']} for article in data.get('articles', [])]
    else:
        print(f"Error fetching news: {response.status_code}, {response.text}")
        return []

def fetch_headlines(country_code):
    parameters = {
        'country': country_code,
        'apiKey': NEWS_API_KEY
    }

    # Make the API request
    response = requests.get(HEADLINES_API_URL, params=parameters)
    if response.status_code == 200:
        data = response.json()
        return [{"title": article['title'], "description": article.get('description', ''), "url": article['url']} for article in data.get('articles', [])]
    else:
        print(f"Error fetching headlines: {response.status_code}, {response.text}")
        return []
import os
import json
import requests
from datetime import datetime, timedelta
from data_handler import current_travel

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    
WEBZIO_API_KEY = config.get('WEBZIO_API_KEY')
if not WEBZIO_API_KEY:
    raise ValueError("WEBZIO_API_KEY not found in config.json")

WEBZIO_URL = "https://api.webz.io/newsApiLite"

def fetch_news(location):
    query = f"title:({location})"
    
    parameters = {
        'token' : WEBZIO_API_KEY,
        'q': query}
    
    response = requests.get(WEBZIO_URL, params=parameters)
    if response.status_code == 200:
        return response.json().get('articles',[])
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

fetch_news("Uppsala")
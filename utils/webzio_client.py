import os
import json
import requests
from datetime import datetime, timedelta
from data_handler import read_travel_data

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    
WEBZIO_API_KEY = config.get('WEBZIO_API_KEY')
if not WEBZIO_API_KEY:
    raise ValueError("WEBZIO_API_KEY not found in config.json")

WEBZIO_URL = "https://api.webz.io/newsApiLite"

def fetch_news(location):
    parameters = {
        'loc' : location,
        'token' : WEBZIO_API_KEY}
    
    response = requests.get(WEBZIO_URL, params=parameters)
    if response.status_code == 200:
        return response.json().get('articles',[])
    else:
        print(f"Error fetching news: {response.status_code}")
        return None
    
def check_travel_alerts():
    alerts = []
    travel_data = read_travel_data()
    
    for plan in travel_data:
        articles = fetch_news(plan['city'], plan['travelstart'], plan['travelend'])
        if articles:
            alerts.append({
                'userid': plan['userid'],
                'travelid': plan['travelid'],
                'articles': articles
            })
            
    return alerts

articles = fetch_news('New York', '2023-10-01', '2023-10-15')
print(articles)  # Print the fetched articles for debugging
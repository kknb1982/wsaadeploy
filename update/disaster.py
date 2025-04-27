import requests
import geopy.distance

def get_disaster_data():
    url = 'https://api.reliefweb.int/v1/disasters'
    params = {'appname': 'your-app', 'limit': 100}
    response = requests.get(url, params=params)
    data = response.json()
    # Extract relevant fields
    return data

Use geopy to calculate proximity between:

Disaster locations

Staff/student travel locations

If within X km radius (e.g., 300 km), flag as a concern.


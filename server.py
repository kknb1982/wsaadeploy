# This retrieves the dataset for the "students enrolled in and entrant to third level courses" from the CSO and stores it into a file called "student.json"

# Author: Kirstin Barnett

# Importing necessary libraries
from flask import Flask, redirect, url_for, request, jsonify, abort
from geopy.distance import geodesic
import TravelPlan

from geopy.distance import geodesic
import os

# Mapping the URL to the Flask app
app = Flask(__name__, static_url_path='', static_folder='staticpages')

#@app.route('/')
#def index():
 #   return "<h1>Welcome to the WSAA Project!</h1>"

# Get all students enrolled in and entrants to third level courses
#@app.route('/students', methods=['GET'])
def get_students():
    return "<h1>Getting all students enrolled in and entrants to third level courses</h1>"

# Get a specific student 

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return f"Getting student with ID {student_id}"

# Create a new student enrolled in and entrants to third level courses
#@app.route('/students', methods=['POST'])
#def create_student():
    student = request.json
    return f"Creating student: {student}", 201

# Update a specific student enrolled in and entrants to third level courses
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    return f"Updating student with ID {student_id}"

# Delete a specific student enrolled in and entrants to third level courses
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    return f"Deleting student with ID {student_id}"


@app.route("/enquiry")
def enquiry():
    name = request.args["name"]
    return f"<h1>Enquiry page for {name}</h1>"

#@app.route("/inbody", methods=["POST"])
#def inbody():
    name = request.json["name"]
    return f"<h1>Inbody page for {name}</h1>"


#app.send_static_file('students.json')





@app.route('/invalid', methods=['GET'])
def invalid():
    return redirect(url_for('index'))

@app.route('/student')
def get_user():
    student = {
        "name": "John Doe",
        "age": 20,
        "course": "Computer Science"
    }
    return jsonify(student)

@app.route('/login')
def login():
    abort(401)
if __name__ == '__main__':
    app.run(debug=True)
 
 
 ######################################   
#import requests
#import json

# URL for the dataset
#url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/EDA99/JSON-stat/2.0/en"

# Function to get the dataset
#def getAll():
 #   response = requests.get(url)
  #  return response.json()

# Write the dataset to a file
#if __name__ == "__main__":
 #   with open("students.json", "wt") as fp:
  #      print(json.dumps(getAll()), file=fp)

from flask import request, jsonify
from flask_login import login_required, current_user
from models import TravelPlan  # Assuming you have TravelPlan model
from datetime import datetime
import GOOGLE_MAPS_API_KEY  from config

@app.route('/api/add-travel', methods=['POST'])
#@login_required
def api_add_travel():
    city = request.form.get('city')
    country = request.form.get('country')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    new_travel = TravelPlan(
        user_id=current_user.id,
        location_city=city,
        location_country=country,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_travel)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/api/view-travel', methods=['GET'])
#@login_required
def api_view_travel():
    # Grab filters if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    location = request.args.get('location')
    
    query = TravelPlan.query.filter_by(user_id=current_user.id)
    
    if start_date:
        query = query.filter(TravelPlan.start_date >= start_date)
    if end_date:
        query = query.filter(TravelPlan.end_date <= end_date)
    if location:
        search = f"%{location.lower()}%"
        query = query.filter(
            (TravelPlan.location_city.ilike(search)) |
            (TravelPlan.location_country.ilike(search))
        )
    
    travels = query.all()
    
    results = []
    for travel in travels:
        results.append({
            'city': travel.location_city,
            'country': travel.location_country,
            'start_date': travel.start_date.strftime('%Y-%m-%d'),
            'end_date': travel.end_date.strftime('%Y-%m-%d')
        })

    return jsonify(results)

## get disasters

RELIEFWEB_API_URL = "https://api.reliefweb.int/v1/disasters"
def geocode_location(city, country):
    address = f"{city}, {country}"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return (location['lat'], location['lng'])
    else:
        return (None, None)
    
    
#@login_required
@app.route('/api/check-disasters', methods=['GET'])
def check_disasters():
    # Get all travels for the logged-in user
    travels = TravelPlan.query.filter_by(user_id=current_user.id).all()

    matched_disasters = []

    for travel in travels:
        if not (travel.location_lat and travel.location_lng):
            continue  # Skip if no coordinates available

        # Build the ReliefWeb API query
        # NOTE: You can customize the dates better if you want.
        query_params = {
            'appname': 'rwint-user-0',
            'profile': 'list',
            'preset': 'latest',
            'slim': '1',
            'query[value]': f'date.event:[{travel.start_date} TO {travel.end_date}]',
            'query[operator]': 'AND'
        }

        response = requests.get(RELIEFWEB_API_URL, params=query_params)
        if response.status_code != 200:
            continue  # Skip if ReliefWeb failed

        disaster_data = response.json().get('data', [])

        for disaster in disaster_data:
            fields = disaster.get('fields', {})
            disaster_name = fields.get('name')
            disaster_url = fields.get('url')
            disaster_country = fields.get('country', [{}])[0].get('name')

            # Disaster coordinates (we approximate using country center for now — better with event location if possible)
            disaster_coords = None

            # Try to find disaster location if available (some disasters have detailed fields)
            if 'primary_country' in fields and 'location' in fields['primary_country']:
                locations = fields['primary_country']['location']
                if locations and len(locations) > 0:
                    # Take the first location as approximation
                    loc = locations[0]
                    disaster_coords = (loc['lat'], loc['lon'])

            # If no location info, skip
            if not disaster_coords:
                continue

            travel_coords = (travel.location_lat, travel.location_lng)

            # Calculate distance
            distance_km = geodesic(travel_coords, disaster_coords).km

            if distance_km <= 100:  # Within 100 km
                matched_disasters.append({
                    'travel_city': travel.location_city,
                    'travel_country': travel.location_country,
                    'travel_start': str(travel.start_date),
                    'travel_end': str(travel.end_date),
                    'travel_lat': travel.location_lat,
                    'travel_lng': travel.location_lng,
                    'disaster_name': disaster_name,
                    'disaster_country': disaster_country,
                    'disaster_url': disaster_url,
                    'disaster_lat': disaster_coords[0],
                    'disaster_lng': disaster_coords[1],
                    'distance_km': round(distance_km, 1)
                })

    return jsonify(matched_disasters)


@app.route('/add-travel', methods=['GET', 'POST'])
#@login_required
def add_travel():
    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not (city and country and start_date and end_date):
            flash('All fields are required.', 'danger')
            return redirect(url_for('add_travel'))

        # Geocode city & country
        lat, lng = geocode_location(city, country)

        if lat is None or lng is None:
            flash('Failed to find coordinates for the entered city/country.', 'danger')
            return redirect(url_for('add_travel'))

        new_travel = TravelPlan(
            user_id=current_user.id,
            location_city=city,
            location_country=country,
            start_date=start_date,
            end_date=end_date,
            location_lat=lat,
            location_lng=lng
        )

        db.session.add(new_travel)
        db.session.commit()

        flash('Travel added successfully!', 'success')
        return redirect(url_for('view_travel'))

    return render_template('add_travel.html')

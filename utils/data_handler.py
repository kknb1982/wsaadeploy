import csv
import json
import os
from datetime import timedelta, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
TRAVEL_DATA_FILE = os.path.join(BASE_DIR, '../data/travel_data.csv')  # Adjust the path to travel_plan.csv
USERS_DATA_FILE = os.path.join(BASE_DIR, '../data/users.csv')  # Adjust the path to users.csv
COUNTRIES_FILE = os.path.join(BASE_DIR, '../data/countries_cache.json')  # Adjust the path to countries.csv

def is_valid_country(country_name):
    COUNTRIES_FILE = os.path.join(BASE_DIR, '../data/countries_cache.json')
    if not os.path.exists(COUNTRIES_FILE):
        print(f"Countries file not found: {COUNTRIES_FILE}")
        return False
    
    with open(COUNTRIES_FILE, 'r') as f:
        countries_data = json.load(f)
    
    for country in countries_data['data']:
        if country['name']['common'].lower() == country_name.lower():
            return True
    return False
    
def read_travel_data():
    with open(TRAVEL_DATA_FILE, mode='r', newline='', encoding='utf-8') as f:
        travel_data = csv.DictReader(f)
        return list(travel_data)  # Read all rows into a list and return it

def add_travel_record(travel_info):
    try:
        if not is_valid_country(travel_info['country']):
            print(f"Invalid country: {travel_info['country']}")
            return False
    
        # Read existing travel data
        all_travel_data = read_travel_data()

        # Calculate the next available travelid
        max_travelid = max((int(travel['travelid']) for travel in all_travel_data if travel['travelid'].isdigit()), default=0)
        travel_info['travelid'] = str(max_travelid + 1)  # Assign the next travelid as a string
        
        # Ensure dates are in YYYY-MM-DD format
        travel_info['travelstart'] = datetime.strptime(travel_info['travelstart'], '%Y-%m-%d').strftime('%Y-%m-%d')
        travel_info['travelend'] = datetime.strptime(travel_info['travelend'], '%Y-%m-%d').strftime('%Y-%m-%d')
        
        with open(TRAVEL_DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['userid', 'travelid', 'institution', 'travelstart', 'travelend', 'city','country'])
            writer.writerow(travel_info)
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False
    
def read_users_data():
    with open(USERS_DATA_FILE, mode='r', newline='', encoding='utf-8') as f:
        users = csv.DictReader(f)
        return list(users)
    
def get_user_info(userid):
    print(f"Fetching user info for userid: {userid}")  # Debugging log
    users = read_users_data()
    for user in users:
        if user['userid'] == userid:
            print(f"User found: {user}")
            return user
    return None

def get_travel_data_for_user(userid):
    all_travel_data = read_travel_data()
    return [travel for travel in all_travel_data if travel['userid'] == userid]

def get_travel_by_id(travel_id):
    all_travel_data = read_travel_data()
    for travel in all_travel_data:
        if travel['travelid'] == travel_id:
            return travel
    return None

def update_travel_record(updated_travel):
    if not is_valid_country(updated_travel['country']):
        print(f"Invalid country: {updated_travel['country']}")
        return False  # Reject the operation
    
    all_travel_data = read_travel_data()
    for travel in all_travel_data:
        if travel['id'] == updated_travel['id']:
            travel['institution'] = updated_travel.get('institution', travel['institution'])
            travel['city'] = updated_travel.get('city', travel['city'])
            travel['country'] = updated_travel.get('country', travel['country'])
            travel['travelstart'] = updated_travel.get('travelstart', travel['travelstart'])
            travel['travelend'] = updated_travel.get('travelend', travel['travelend'])
            break

    # Write the updated data back to the CSV file
    with open(TRAVEL_DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'institution', 'city', 'country', 'travelstart', 'travelend'])
        writer.writeheader()
        writer.writerows(all_travel_data)

def update_user_record(updated_user):
    users = read_users_data()  # Read all users
    for user in users:
        if user['userid'] == updated_user['userid']:
            # Update the user's details
            user['firstname'] = updated_user.get('firstname', user['firstname'])
            user['surname'] = updated_user.get('surname', user['surname'])
            user['email'] = updated_user.get('email', user['email'])
            user['phone'] = updated_user.get('phone', user['phone'])
            user['role'] = updated_user.get('role', user['role'])
            print(f"Updating user record: {user}")  # Debugging log
            break

    # Write the updated users back to the CSV file
    with open(USERS_DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['userid', 'firstname', 'surname', 'role', 'email', 'phone'])
        writer.writeheader()
        writer.writerows(users)
        
def current_travel():
    all_travel_data = read_travel_data()
    current_travel = []
    today = datetime.now()
    three_days_ago = today - timedelta(days=3)
    
    for travel in all_travel_data:
        travel_start = datetime.strptime(travel['travelstart'], '%Y-%m-%d').date()
        travel_end = datetime.strptime(travel['travelend'], '%Y-%m-%d').date()

        # Check if the travel is ongoing or ended within the last three days
        if (travel_start <= today <= travel_end) or (three_days_ago <= travel_end <= today):
            current_travel.append(travel)

    return current_travel


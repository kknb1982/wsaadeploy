from flask import Flask, render_template, request, jsonify, redirect, session
from utils.data_handler import read_travel_data, get_travel_by_id, current_travel, add_travel_record, update_travel_record, get_user_info, update_user_record, get_travel_data_for_user
from utils.newsAPI_client import fetch_news
from utils.countries_API import get_countries
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')
        user_info = get_user_info(userid)
        if user_info:
            session['userid'] = userid
            session['firstname'] = user_info['firstname']
            session['surname'] = user_info['surname']
            session['role'] = user_info['role']
            session['email'] = user_info['email']
            session['phone'] = user_info['phone']
            return redirect(f'/dashboard/{userid}')
        else:
            return "Invalid User ID. Please try again.", 401
    return render_template('login.html')

@app.route('/dashboard/<userid>')
def dashboard(userid):
    if 'userid' not in session:
        return redirect('/login')
    
    print(f"Session User ID: {session['userid']}")  # Debugging log
    print(f"Requested User ID: {userid}")  # Debugging log
    if session['userid'] != userid:
        return "Unauthorised access", 403
    return render_template('dashboard.html', user=session)

@app.route('/update-user/<userid>')
def update_user(userid):
    if 'userid' not in session:
        return redirect('/login')

    user_data = get_user_info(userid)
    if not user_data:
        return "User not found.", 404
    return render_template('update-user.html', user=user_data)

@app.route('/add-travel/<userid>')
def add_travel(userid):
    if 'userid' not in session:
        return redirect('/login')
    return render_template('add-travel.html')


@app.route('/view-travel/<userid>', methods=['GET'])
def view_travel(userid):
    if 'userid' not in session:
        return redirect('/login')
        # Pass the user data from the session to the template
    user = {       
        'userid': session['userid'],
        'firstname': session['firstname'],
        'surname': session['surname']}
    return render_template('view-travel.html', user=user)
    
@app.route('/update-travel/<travelid>', methods = ['GET'])
def update_travel(travelid):
    if 'userid' not in session:
        return redirect('/login')  # Redirect to login if the user is not logged in

    # Fetch the travel details by ID
    travel_data = get_travel_by_id(travelid)  # Use the travelid directly from the URL

    if not travel_data:
        return "Travel record not found.", 404
    travel_data['travelstart'] = datetime.strptime(travel_data['travelstart'], '%Y-%m-%d').strftime('%d/%m/%Y')
    travel_data['travelend'] = datetime.strptime(travel_data['travelend'], '%Y-%m-%d').strftime('%d/%m/%Y')
    return render_template('update-travel.html', travel=travel_data)
    
@app.route('/personal-report/<userid>', methods=['GET'])
def report(userid):
    if 'userid' not in session:
        return redirect('/login')
    user = {       
        'userid': session['userid'],
        'firstname': session['firstname'],
        'surname': session['surname']}
    travel_data = get_travel_data_for_user(user['userid'])
    if not travel_data:
        return "No travel records found for this user.", 404
    
    alerts = check_travel_alerts()
    
    for travel in travel_data:
        travel['alerts'] = next((alert['articles'] for alert in alerts if alert['travelid'] == travel['travelid']), [])
    return render_template('personal-report.html', user=user, travel_data=travel_data)

@app.route('/current_travel/<userid>', methods=['GET'])
def current_travel_admin(userid):
    if 'userid' not in session:
        return redirect('/login')
    
    travels = current_travel()
    travel_data_with_news = []
    if travels:
        for travel in travels:
            news = fetch_news(travel)
            travel['news'] = news
            travel_data_with_news.append(travel)
    
    return render_template('current_travel.html', travel_data=travel_data_with_news)

@app.route('/country-list', methods=['GET'])
def country_list():
    countries_data = get_countries()
    if not countries_data:
        return "No countries found.", 404
    formatted_countries = [
        {
            'name': country['name']['common'],
            'code': country['cca2']
        } for country in countries_data]
    
    return jsonify(formatted_countries)


@app.route('/country-details/<country>', methods=['GET'])
def country_details(country):
    countries_data = get_countries()
    country_data = next((country for country in countries_data if country['name'].lower() == country.lower()), None)
    
    if not country_data:
        return "Country not found.", 404
    
    return render_template('country-details.html', country=country_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# API to get all travel records
@app.route('/api/travel', methods=['GET'])
def get_travel():
    if 'userid' not in session:
        return jsonify([])

    userid = session['userid']
    travel_data = get_travel_data_for_user(userid)
    print("User ID:", userid)
    print("Travel Data:", travel_data)
    return jsonify(travel_data)

# API to add a new travel record
@app.route('/api/travel', methods=['POST'])
def api_add_travel():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    travel_data = request.get_json()
    if not travel_data:
        return jsonify({'error': 'No data provided'}), 400

    # Add the travel record
    travel_data['userid'] = session['userid']  # Add the logged-in user's ID
    success = add_travel_record(travel_data)
    if success:
        return jsonify({'message': 'Travel record added successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to add travel record.'}), 500

# API to update user information
@app.route('/api/user', methods=['POST'])
def api_update_user():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_data = request.get_json()
    userid = session['userid']
    
    print(f"Session userid: {userid}")  # Debugging log
    print(f"Request userid: {user_data['userid']}")  # Debugging log

    # Ensure the userid matches the logged-in user
    if user_data['userid'] != userid:
        return jsonify({'error': 'Unauthorized'}), 403

    # Update the user record
    update_user_record(user_data)
    return jsonify({'message': 'User record updated successfully.'}), 200

@app.route('/api/update-travel', methods=['POST'])
def api_update_travel():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    travel_data = request.get_json()
    update_travel_record(travel_data)  # Update the travel record in the CSV
    return jsonify({'message': 'Travel record updated successfully.'}), 200

@app.route('/api/travel/<travel_id>', methods=['GET'])
def get_travel_by_id(travel_id):
    try:
        # Read all travel data
        all_travel_data = read_travel_data()

        # Find the travel record with the matching ID
        travel = next((t for t in all_travel_data if t['travelid'] == travel_id), None)
        if travel:
            return jsonify(travel), 200
        else:
            return jsonify({'error': 'Travel record not found'}), 404
    except Exception as e:
        print(f"Error fetching travel record: {e}")
        return jsonify({'error': 'An error occurred while fetching the travel record'}), 500

@app.route('/api/current-travel', methods=['GET'])
def api_current_travel():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    current_travel_data = current_travel()  # Use the `current_travel` function from `data_handler.py`
    return jsonify(current_travel_data)

@app.route('/api/news', methods=['GET'])
def api_news():
    city = request.args.get('city')
    country = request.args.get('country')

    if not city or not country:
        return jsonify({'error': 'City and country are required'}), 400

    # Fetch news using the News API client
    from utils.newsAPI_client import fetch_news
    news = fetch_news({'city': city, 'country': country})

    if news is None:
        return jsonify({'error': 'Failed to fetch news'}), 500

    return jsonify(news)

if __name__ == '__main__':
    print("Loading countries data...")
    countries_data = get_countries()
    if countries_data:
        print("Countries data loaded successfully.")
    else:
        print("Failed to load countries data.")
    app.run(debug=True)
    


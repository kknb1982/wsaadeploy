from flask import Flask, render_template, request, jsonify, redirect, session
from utils.data_handler import get_travel_by_id, current_travel, add_travel_record, update_travel_record, get_user_info, update_user_record, get_travel_data_for_user
from utils.newsAPI_client import fetch_news
from utils.countries_API import get_countries
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

# Run get_countries() on app load
print("Loading countries data...")
countries_data = get_countries()
if countries_data:
    print("Countries data loaded successfully.")
else:
    print("Failed to load countries data.")

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
            return redirect('/dashboard')
        else:
            return "Invalid User ID. Please try again.", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'userid' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session)

@app.route('/update-user')
def update_user():
    if 'userid' not in session:
        return redirect('/login')
    return render_template('update-user.html', user=session)

@app.route('/add-travel')
def add_travel():
    if 'userid' not in session:
        return redirect('/login')
    return render_template('add-travel.html')


@app.route('/view-travel')
def view_travel():
    if 'userid' not in session:
        return redirect('/login')
        # Pass the user data from the session to the template
    user = {       
        'userid': session['userid'],
        'firstname': session['firstname'],
        'surname': session['surname']}
    return render_template('view-travel.html', user=user)
    
@app.route('/update-travel')
def update_travel():
    if 'userid' not in session:
        return redirect('/login')  # Redirect to login if the user is not logged in

    travel_id = request.args.get('id')  # Get the travel ID from the query parameter
    travel_data = get_travel_by_id(travel_id)  # Fetch the travel details by ID

    if not travel_data:
        return "Travel record not found.", 404
    
    try: 
        travel_data['travelstart'] = datetime.strptime(travel_data['travelstart'], '%d/%m/%Y').strftime('%Y-%m-%d')
        travel_data['travelend'] = datetime.strptime(travel_data['travelend'], '%d/%m/%Y').strftime('%Y-%m-%d')
    except (ValueError, KeyError) as e:
        travel_data['travelstart'] = ''
        travel_data['travelend'] = ''
    return render_template('update-travel.html', travel=travel_data)
    
@app.route('/personal-report')
def report():
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

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'userid' not in session:
        return redirect('/login')
    
    travels = current_travel()
    travel_data_with_news = []
    if travels:
        for travel in travels:
            news = fetch_news(travel)
            travel['news'] = news
            travel_data_with_news.append(travel)
    
    return render_template('admin-dashboard.html', travel_data=travel_data_with_news)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# API to get all travel records
@app.route('/api/travel', methods=['GET'])
def get_travel():
    if 'userid' not in session:
        return jsonify([])

    user_id = session['userid']
    travel_data = get_travel_data_for_user(user_id)
    print("User ID:", user_id)
    print("Travel Data:", travel_data)
    return jsonify(travel_data)

# API to add a new travel record
app.route('/api/travel', methods=['POST'])
def post_travel():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    travel_info = request.json
    travel_info['id'] = session['userid']  # Pre-fill user ID from session
    travel_info['firstname'] = session['firstname']
    travel_info['surname'] = session['surname']
    travel_info['role'] = session['role']
    travel_info['institution'] = 'MyUniversity'  # Example institution
    add_travel_record(travel_info)
    return jsonify({'status': 'success'})

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
    update_user_record(user_data)  # This function should be defined in data_handler.py
    return jsonify({'message': 'User record updated successfully.'}), 200

@app.route('/api/update-travel', methods=['POST'])
def api_update_travel():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    travel_data = request.get_json()
    update_travel_record(travel_data)  # Update the travel record in the CSV
    return jsonify({'message': 'Travel record updated successfully.'}), 200



if __name__ == '__main__':
    app.run(debug=True)
    


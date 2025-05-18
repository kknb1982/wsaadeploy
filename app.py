from flask import Flask, render_template, request, jsonify, redirect, session
from flask_session import Session
from utils.newsAPI_client import *
from utils.countries_API import *
from travelDAO import *
from datetime import datetime
import json


app = Flask(__name__,static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key'  # Required for sessions
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the filesystem
Session(app)

@app.route('/')
def home():
    session.clear()  # Clear session on home page load
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = 'student'

        try:
            con = connect()
            cursor = con.cursor()
            sql = "INSERT INTO users (firstname, lastname, email, phone, role) VALUES (%s, %s, %s, %s, %s)"
            values = (firstname, lastname, email, phone, role)
            cursor.execute(sql, values)
            con.commit()
            cursor.close()
            con.close()
            return redirect(url_for('success'))  # Redirect to a success page
        except mysql.connector.Error as err:
            return f"Error: {err}"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')  # Get the userid from the form
        user_info = get_user_info(userid)  # Fetch user info from the database or data source
        if user_info:
            # Store user details in the session
            session['userid'] = userid
            session['firstname'] = user_info['firstname']
            session['lastname'] = user_info['lastname']
            session['role'] = user_info['role']
            session['email'] = user_info['email']
            session['phone'] = user_info['phone']
            # Redirect to the dashboard with the userid
            return redirect(f'/dashboard/{userid}')
        else:
            return "Invalid User ID. Please try again.", 401
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')

@app.route('/dashboard/<userid>')
def dashboard(userid):
    if 'userid' not in session:
        return redirect('/login')
    
    print(f"Session User ID: {session['userid']}")  # Debugging log
    print(f"Requested User ID: {userid}")  # Debugging log
    if str(session['userid']) != str(userid):
        return "Unauthorised access", 403
    return render_template('dashboard.html', user=session)

@app.route('/update-user/<int:userid>', methods=['GET', 'POST'])
def update_user(userid):
    if 'userid' not in session:
        return redirect ('/login')
    if str(session['userid']) != str(userid):
        return "Unauthorised access", 403
    if request.method == 'POST':
        updated_user = {
            'userid': userid,
            'firstname': request.form.get('firstname'),
            'lastname': request.form.get('lastname'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'role': request.form.get('role')
        }
        # Call your function to update the user record in the database
        update_user_record(updated_user)
        return redirect(url_for('user_profile', userid=userid))
    else:
        # Handle GET request, e.g., render the update form
        user_info = get_user_info(userid)
        print(f"User info fetched for ID {userid}: {user_info}")  # Debugging log
        return render_template('update-user.html', user=user_info)


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
        'lastname': session['lastname']}
    user_travel_data = get_travel_by_id(userid)
    return render_template('view-travel.html', user=user,travel=user_travel_data)
    
@app.route('/update-travel/<travelid>', methods=['GET','POST'])
def update_travel(travelid):
    if 'userid' not in session:
        return redirect('/login')  # Redirect to login if the user is not logged in

    if request.method == 'GET':

        travel_data = get_travel_by_id(travelid)
        print(f"Travel data fetched for ID {travelid}: {travel_data}")  # Debugging log
        if not travel_data:
            return "Travel record not found.", 404
        if not isinstance(travel_data, dict):
            return "Invalid travel data format.", 500

        # Format the travel start and end dates for display (dd-mm-yyyy)
        #travel_data['travelstart_display'] = datetime.strptime(travel_data['travelstart'], '%Y-%m-%d').strftime('%d-%m-%Y')
        #travel_data['travelend_display'] = datetime.strptime(travel_data['travelend'], '%Y-%m-%d').strftime('%d-%m-%Y')
    
        # Keep the original dates in yyyy-mm-dd format for the input fields
        #travel_data['travelstart'] = datetime.strptime(travel_data['travelstart'], '%Y-%m-%d').strftime('%Y-%m-%d')
        #travel_data['travelend'] = datetime.strptime(travel_data['travelend'], '%Y-%m-%d').strftime('%Y-%m-%d')

        return render_template('update-travel.html', travel=travel_data)
    
    elif request.method == 'POST':
        try: 
            # Handle the update request
            updated_travel = request.get_json()
            print(f"Updated travel data: {updated_travel}")  # Debugging log

            success, error_message = update_travel_record(updated_travel)
            if success:
                return jsonify({'message': 'Travel record updated successfully.'}), 200
            else:
                return jsonify({'error': error_message}), 400
        except Exception as e:
            print(f"Error updating travel record: {e}")  # Debugging log
            return jsonify({'error': 'An internal server error occurred.'}), 500

@app.route('/admin-dashboard/<userid>', methods=['GET'])
def admin_dashboard(userid):
    if 'userid' not in session:
        print("Session is missing. Redirecting to login.")
        return redirect('/login')
    
    if session['role'] != 'admin':
        print(f"Unauthorized access attempt by user {session['userid']} with role {session['role']}")
        return "Unauthorized access", 403
    
    print(f"Admin dashboard accessed by {session['userid']}")
    user = {       
        'userid': session['userid'],
        'firstname': session['firstname'],
        'lastname': session['lastname']}
    
    return render_template('admin-dashboard.html', user=user)

@app.route('/current_travel/<userid>', methods=['GET'])
def current_travel_admin(userid):
    if 'userid' not in session:
        return redirect('/login')
    if session['role'] != "admin":
        return redirect('/login')
    else:
        travels = get_current_travel()
        return render_template('current_travel.html', travel_data=travels)

@app.route('/country-list', methods=['GET'])
def country_list():
    countries_data = load_countries()
    countries_data = sorted(countries_data, key=lambda x: x['name']['common'].lower())
    return render_template('country-list.html', countries=countries_data)

@app.route('/country-details/<country_name>', methods=['GET'])
def country_details(country_name):
    normalised_country_name = country_name.replace("-", " ").replace("_", " ")
    country = get_country_details(normalised_country_name)

    if not country:
        return "Country details not found.", 404

    print(f"Country details: {country}")  # Debugging log

    return render_template('country-details.html', country=country)


@app.route('/news-search', methods=['GET'])
def news_search():
    keyword = request.args.get('keyword', '')
    search_in = request.args.get('searchIn', 'title')
    
    # Fetch news using the News API client
    news = fetch_news(keyword=keyword, search_in=search_in)
    return render_template('news-search.html', news=news)

@app.route('/headlines/<country_code>', methods=['GET'])
def headlines(country_code):
    from utils.newsAPI_client import fetch_headlines

    # Fetch top headlines for the given country code
    headlines = fetch_headlines(country_code)

    country = None
    with open(CACHE_FILE, 'r') as f:
        countries_data = json.load(f)
        for c in countries_data['data']:
            if c.get('cca2', '').lower() == country_code.lower():
                country = c
                break

    if not country:
        return "Country details not found.", 404

    return render_template('headlines.html', country_code=country_code, headlines=headlines, country=country)

# Add a new user
@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    phone = data['phone']

    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (firstname, lastname, email, phone, role) VALUES (?, ?, ?, ?, ?)",
            (firstname, lastname, email, phone, 'student')
        )
        conn.commit()
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        conn.close()

# API to get all travel records
@app.route('/api/travel/<userid>', methods=['GET'])
def get_travel(userid):
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Ensure the userid in the session matches the requested userid
    if session['userid'] != userid:
        return jsonify({'error': 'Unauthorized access'}), 403

    travel_data = get_travel_by_userid(userid)  # Fetch travel data for the user
    if not travel_data:
        return jsonify({'error': 'No travel records found'}), 404

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
    
@app.route('/api/travel/<travelid>', methods=['DELETE'])
def delete_travel(travelid):
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Call the delete_travel_record function
    deleted_travel = delete_travel_record(travelid)

    if not deleted_travel:
        return jsonify({'error': 'Travel record not found or could not be deleted'}), 404

    return jsonify({
        'message': 'Travel record deleted successfully',
        'institution': deleted_travel['institution'],
        'travelstart': deleted_travel['travelstart'],
        'travelend': deleted_travel['travelend'],
        'userid': deleted_travel['userid']
    }), 200

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

@app.route('/api/check-admin/<userid>', methods=['GET'])
def check_admin(userid):
    user_info = get_user_info(userid)  # Fetch user info from the data source
    if not user_info:
        return jsonify({'error': 'User not found'}), 404

    is_admin = user_info.get('role') == 'admin'
    return jsonify({'isAdmin': is_admin})


@app.route('/api/admin-login/<userid>', methods=['POST'])
def admin_login(userid):
    user_info = get_user_info(userid)  # Fetch user info from the data source
    if not user_info:
        return jsonify({'error': 'User not found'}), 404

    if user_info.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    # Set the session for the admin user
    session['userid'] = user_info['userid']
    session['firstname'] = user_info['firstname']
    session['lastname'] = user_info['lastname']
    session['role'] = user_info['role']
    session['email'] = user_info['email']
    session['phone'] = user_info['phone']

    return jsonify({'message': 'Admin login successful'}), 200

@app.route('/api/update-travel/<travelid>', methods=['POST'])
def api_update_travel():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    travel_data = request.get_json()
    update_travel_record(travel_data)  # Update the travel record in the CSV
    return jsonify({'message': 'Travel record updated successfully.'}), 200

@app.route('/api/travel/<travelid>', methods=['GET'])
def api_get_travel_by_id(travelid):
    try:
        # Read all travel data
        all_travel_data = read_travel_data()

        # Find the travel record with the matching ID
        travel = next((t for t in all_travel_data if t['travelid'] == travelid), None)
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
    if session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    current_travel_data = current_travel()  # Use the `current_travel` function from `data_handler.py`
    
    for record in current_travel_data:
        if 'travelid' not in record:
            print(f"Missing travelid in record: {record}")  # Debugging log

    return jsonify(current_travel_data)

@app.route('/api/countries', methods=['GET'])
def api_countries():
    countries_data = load_countries()
    countries_data = sorted(countries_data, key=lambda x: x['name']['common'].lower())
    return jsonify(countries_data)

@app.route('/api/countries-simple', methods=['GET'])
def api_countries_simple():
    countries = load_countries()
    # Return only countryid and commonname
    simple = [{'countryid': c['countryid'], 'commonname': c['common_name']} for c in countries]
    return jsonify(simple)

@app.route('/api/news', methods=['GET'])
def api_news():
    keyword = request.args.get('keyword', '')
    search_in = request.args.get('searchIn', 'title,description,content')
    date_from = request.args.get('from', None)
    date_to = request.args.get('to', None)

    # Fetch news using the News API client
    news = fetch_news(keyword=keyword, search_in=search_in, date_from=date_from, date_to=date_to)
    if not news:
        return jsonify({'error': 'No news found'}), 404
    return jsonify(news)

@app.route('/api/download-names', methods=['GET'])
def download_names():
    if 'userid' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    if session['role'] != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    

    # Fetch the travel data for the logged-in user


if __name__ == '__main__':
    app.run(debug=True)
    


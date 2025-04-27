from flask import Flask, render_template, request, jsonify, redirect, session
from utils.data_handler import read_travel_data, add_travel_record

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')
        session['userid'] = userid
        return redirect('/add-travel')
    return render_template('login.html')

@app.route('/add-travel')
def add_travel():
    if 'userid' not in session:
        return redirect('/login')
    return render_template('add-travel.html')


@app.route('/view-travel')
def view_travel():
    if 'userid' not in session:
        return redirect('/login')
    return render_template('view-travel.html')

@app.route('/report')
def report():
    if 'userid' not in session:
        return redirect('/login')
    return render_template('report.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin-dashboard.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/login')

# API to get all travel records
@app.route('/api/travel', methods=['GET'])
def get_travel():
    data = read_travel_data()
    user = session.get('userid', None)
    if user:
        filtered = [record for record in data if record['userid'] == user]
        return jsonify(filtered)
    else:
        return jsonify([])

# API to add a new travel record
@app.route('/api/travel', methods=['POST'])
def post_travel():
    travel_info = request.json
    travel_info['username'] = session.get('username')
    add_travel_record(travel_info)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

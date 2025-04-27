from flask import Flask, render_template, request, jsonify
from utils.data_handler import read_travel_data, add_travel_record

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view-travel')
def view_travel():
    return render_template('view_travel.html')

@app.route('/add-travel')
def add_travel():
    return render_template('add_travel.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# API to get all travel records
@app.route('/api/travel', methods=['GET'])
def get_travel():
    data = read_travel_data()
    return jsonify(data)

# API to add a new travel record
@app.route('/api/travel', methods=['POST'])
def post_travel():
    travel_info = request.json
    add_travel_record(travel_info)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

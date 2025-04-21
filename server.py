# This retrieves the dataset for the "students enrolled in and entrant to third level courses" from the CSO and stores it into a file called "student.json"

# Author: Kirstin Barnett

# Importing necessary libraries
from flask import Flask, redirect, url_for, request, jsonify, abort
# Mapping the URL to the Flask app
app = Flask(__name__, static_url_path='', static_folder='staticpages')

@app.route('/')
def index():
    return "<h1>Welcome to the WSAA Project!</h1>"

# Get all students enrolled in and entrants to third level courses
@app.route('/students', methods=['GET'])
def get_students():
    return "<h1>Getting all students enrolled in and entrants to third level courses</h1>"

# Get a specific student enrolled in and entrants to third level courses
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return f"Getting student with ID {student_id}"

# Create a new student enrolled in and entrants to third level courses
@app.route('/students', methods=['POST'])
def create_student():
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

@app.route("/inbody", methods=["POST"])
def inbody():
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


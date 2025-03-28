# This retrieves the dataset for the "students enrolled in and entrant to third level courses" from the CSO and stores it into a file called "student.json"

# Author: Kirstin Barnett
from flask import Flask, redirect, url_for

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return "<h1>Welcome to the WSAA Project!</h1>"

@app.route('/students', methods=['GET'])
def get_students():
    return "<h1>Getting all students enrolled in and entrants to third level courses</h1>"
#app.send_static_file('students.json')

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return f"Getting student with ID {student_id}"

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    return f"Updating student with ID {student_id}"

@app.route('/invalid', methods=['GET'])
def invalid():
    return redirect(url_for('index'))

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


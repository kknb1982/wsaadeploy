# This retrieves the dataset for the "students enrolled in and entrant to third level courses" from the CSO and stores it into a file called "student.json"

# Author: Kirstin Barnett
from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return 'Hello, World!'

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


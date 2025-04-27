import csv

DATA_FILE = "https://github.com/kknb1982/WSAA_project/blob/main/data/travel_plan.csv"

import csv
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/travel_data.csv')

def read_travel_data():
    with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def add_travel_record(travel_info):
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=travel_info.keys())
        writer.writerow(travel_info)


import csv

travel_plans = db.relationship('TravelPlan', back_populates='user', cascade='all, delete-orphan')

def load_admin_ids():
    admin_ids = []
    with open('admin_ids.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            admin_ids.append(row[0])  # Assuming the ID is in the first column
            return admin_ids
import csv

url = "https://github.com/kknb1982/WSAA_project/blob/main/data/"

def get_travel_plan_data():
    with open('travel_plan.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        travel_plan_data = []
        for row in csv_reader:
            travel_plan_data.append(row)
    return travel_plan_data

def get_user_travel_plan_data(user_id):
    travel_plan_data = get_travel_plan_data()
    user_travel_plans = []
    for plan in travel_plan_data:
        if plan['user_id'] == str(user_id):
            user_travel_plans.append(plan)
    return user_travel_plans

def update_travel_plan(user_id, user_travel_plan, updated_plan):
    travel_plan_data = get_travel_plan_data()
    for plan in travel_plan_data:
        if plan['user_id'] == str(user_id) and plan['travel_plan'] == user_travel_plan:
            plan.update(updated_plan)
            break
    with open('travel_plan.csv', 'w', newline='') as file:
        fieldnames = travel_plan_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(travel_plan_data)
    
# This file handles accessing and working with the travel data

import mysql.connector as msql
from datetime import datetime
##
def connect():
    con = msql.connect(host='localhost', database='ggtravel', user='root', password='')
    cursor = con.cursor

# Get the information for a specific user
def get_user_info(userid):
    if not con:
        connect()
    sql = "SELECT * from users WHERE userid=%s"
    value = (xxxxxxxx,)
    cursor.execute(sql,values)
    user_info = cursor.fetchone()
    cursor.close
    return user_info

# Update the user record with inputted details
def update_user_record(updated_user):
    if not con:
        connect()
    sql = """UPDATE users 
    SET firstname = %s, lastname = %s, email = %s, phone =%s
    WHERE userid = %s
    """
    values = (updated_user['firstname'],updated_user['lastname'], updated_user['email'], updated_user['phone'],)
    cursor.execute(sql,values)
    print(f"Updating user record: {user}")
    cursor.close
    return True

# Update the role of the user
def update_user_role(input_userid, input_role):
    if not con:
        connect()
    sql = "UPDATE users SET role = %s WHERE userid = %s"
    values =  (input_role,input_userid,)
    cursor.execute(sql,values)
    cursor.close 
    return True

def is_valid_country(country_name):
    if not con:
        connect()
    sql = "Select countryid from country WHERE commonname = %s"
    values = (xxxxxxxxxxxxxx,)
    cursor.execute(sql,values)
    valid_country = cursor.fetchone()
    cursor.close()
    return valid_country

def get_all_travel():
    if not con:
        connect()
    sql = "Select * from travel"
    cursor.execute(sql)
    all_travel = cursor.fetchall()
    cursor.close()
    return all_travel

def get_travel_by_userid(userid):
    if not con:
        connect()
    sql = "SELECT * from travel where userid = %s"
    value = (userid,)
    cursor.execute(sql,value)
    user_travel_data = cursor.fetchall()
    cursor.close()
    return user_travel_data

def get_travel_by_id(travelid):
    if not con:
        connect()
    sql = "SELECT * from travel where travelid = %s"
    value = (travelid,)
    cursor.execute(sql,value)
    travel_data = cursor.fetchall()
    cursor.close
    return travel_data

def update_travel_record(updated_travel):
    if not con:
        connect()
    sql = """UPDATE travel
    SET institution = updated_travel['institution'], city = updated_travel['city'], country = updated_travel['country'], travelstart = updated_travel['travelstart'], travelend = updated_travel['travelend']
    WHERE travelid = %s"""
    value = (updated_travel['travelid'],)
    cursor.execute(sql,value)
    cursor.close

def add_travel_record(travel_info):
    if not con:
        connect()
    if not is_valid_country(travel_info['country']):
        print(f"Invalid country: {travel_info['country']}")
        return False
    sql = "INSERT INTO travel (userid, institution, city, country, travelstart, travelend)"
    values = (travel_info['userid'], travel_info['institution'], travel_info['city'], travel_info['country'], travel_info['travelstart'], travel_info['travelend'])
    cursor.execute(sql, values)
    con.commit()
    cursor.close()

    
def delete_travel_record(travelid):
    if not con:
        connect()
    sql = "DELETE FROM travel where travelid =%s"
    values = (travelid,)
    cursor.execute(sql,values)
    print(f"Travel with ID {travelid} was deleted")
    cursor.close()

def get_current_travel():
    if not con:
        connect()
    sql = "SELECT * from travel WHERE travelstart > %s AND travelend < %s"
    value = (datetime.now(),)
    cursor.execute(sql,value)
    current_travel = cursor.fetchall()
    return current_travel






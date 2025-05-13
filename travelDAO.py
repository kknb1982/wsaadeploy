# This file handles accessing and working with the travel data

import mysql.connector as msql
from datetime import datetime
##
def connect():
    con = msql.connect(host='localhost', database='travel', user='root', password='')
    cursor = con.cursor


# Create the users tables
def create_user_table():
    try:
        connect()
        cursor = con.cursor
        # Drop the table if it exists
        cursor.execute('DROP TABLE IF EXISTS users')
        
        # Create the table
        sql = """CREATE TABLE users
            (userid INT(5) PRIMARY KEY,
            firstname VARCHAR(20),
            lastname VARCHAR(20),
            email VARCHAR (30),
            phone VARCHAR (40),
            role enum student, staff, admin"""
        cursor.execute(sql)
        cursor.close()
    except:
        print("Unable to create users table")

# Create the travel tables
def create_travel_table()
    cursor = con.cursor
    cursor.execute('DROP TABLE IF EXISTS travel')
    fields = """
    CREATE TABLE travel(
        travelid VARCHAR(5),
        institution VARCHAR (20),
        city VARCHAR (25),
        countryid INT,
        travelstart DATETIME,
        travelend DATETIME,
        userid int,
        PRIMARY KEY (travelid)
        FOREIGN KEY (userid) REFERENCES users(userid)
        FOREIGN KEY (countryid) REFERENCE country(countryid)
    )
    """
    cursor.execute(fields)
    cursor.close()


# Create the country table
def create_country_table():
    cursor = con.cursor
    cursor.execute('DROP TABLE IF EXISTS country')
    fields = """
    CREATE TABLE country(
        countryid INT PRIMARY KEY,
        commonname VARCHAR (20),
        officialname VARCHAR (25),
        cca2 VARCHAR (2),
        currency VARCHAR (10)
    )
    """
    cursor.execute(fields)
    cursor.close()

# Check user is in the users tables
def is_user():
    if not con:
        connect()
    sql = "SELECT from users WHERE userid =%"
    value = (xxxxxxxxxxxxxxx,)
    cursor.execute(sql,value)
    is_valid_user = cursor.fetchone
    cursor.close
    return is_valid_user

# Check user is administrator
def is_user():
    if not con:
        connect()
    sql = "SELECT firstname from users WHERE userid=% AND role =%"
    values = (xxxxxxxxxxxxxxx,yyyyyyyyyyyyyyyyyyyy,)
    cursor.execute(sql,values)
    is_admin = cursor.fetchone()
    cursor.close
    return is_admin

# Fetch user
def fetch_user():
    if not con:
        connect()
    sql = "SELECT * from users WHERE userid=%s"
    value = (xxxxxxxx,)
    cursor.execute(sql,values)

def get_user_info(userid):
    if not con:
        connect()
    sql = "SELECT * from users WHERE userid=%s"
    value = (xxxxxxxx,)
    cursor.execute(sql,values)
    user_info = cursor.fetchone()
    cursor.close
    return user_info

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




def is_valid_country(country_name):
    if not con:
        connect()
    sql = "Select countryid from country WHERE commonname = %s"
    values = (xxxxxxxxxxxxxx,)
    cursor.execute(sql,values)
    is_valid_country = cursor.fetchone()
    cursor.close()
    return is_valid_country

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

def current_travel():
    if not con:
        connect()
    sql = "SELECT * from travel WHERE travelstart > %s AND travelend < %s"
    value = (datetime.now(),)
    cursor.execute(sql,value)
    current_travel = cursor.fetchall()
    
    return current_travel






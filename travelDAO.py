# This file handles accessing and working with the travel data

import mysql.connector as msql
##
def connect():
    con = msql.connect(host='localhost', database='travel', user='root', password='')
    cursor = con.cursor
        

# Create the database


# Create the users tables
def create_user_table():
    try:
        connect()
        cursor = con.cursor
        # Drop the table if it exists
        cursor.execute('DROP TABLE IF EXISTS users')
        
        # Create the table
        sql = """CREATE TABLE users
            (userid VARCHAR(10) PRIMARY KEY,
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
        travelid VARCHAR(5) PRIMARY ID,
        institution VARCHAR (20),
        city VARCHAR (25),
        countryid (5),
        travelstart DATETIME,
        travelend DATETIME
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
        countryid VARCHAR(5) PRIMARY ID,
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
    sql = "SELECT from users WHERE userid=% AND role =%"
    values = (xxxxxxxxxxxxxxx,yyyyyyyyyyyyyyyyyyyy,)
    cursor.execute(sql,values)
    is_admin = cursor.fetchone
    cursor.close
    return is_admin

# Fetch user
def fetch_user():
    if not con:
        connect()
    sql = "SELECT from users WHERE userid=%"
    value = (xxxxxxxx,)





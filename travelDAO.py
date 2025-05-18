import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': 'localhost',
    'database': 'ggtravel',
    'user': 'root',
    'password': ''
}

def connect():
    con = mysql.connector.connect(**DB_CONFIG)
    cursor = con.cursor(dictionary=True)
    return con, cursor

# ---------------- USER HANDLING ---------------- #

def add_user(firstname, lastname, email, phone, role='student'):
    con, cursor = connect()
    sql = "INSERT INTO users (firstname, lastname, email, phone, role) VALUES (%s, %s, %s, %s, %s)"
    values = (firstname, lastname, email, phone, role)
    cursor.execute(sql, values)
    con.commit()
    cursor.close()
    con.close()
    return True, "User added successfully"

def get_user_info(userid):
    con, cursor = connect()
    sql = "SELECT * FROM users WHERE userid = %s"
    cursor.execute(sql, (userid,))
    user_info = cursor.fetchone()
    cursor.close()
    con.close()
    return user_info

def update_user_record(updated_user):
    con, cursor = connect()
    sql = """UPDATE users 
            SET firstname = %s, lastname = %s, email = %s, phone = %s 
            WHERE userid = %s"""
    values = (
        updated_user['firstname'],
        updated_user['lastname'],
        updated_user['email'],
        updated_user['phone'],
        updated_user['userid']
    )
    cursor.execute(sql, values)
    con.commit()
    cursor.close()
    con.close()
    return True

def update_user_role(userid, role):
    con, cursor = connect()
    sql = "UPDATE users SET role = %s WHERE userid = %s"
    cursor.execute(sql, (role, userid))
    con.commit()
    cursor.close()
    con.close()
    return True

# ---------------- COUNTRY VALIDATION ---------------- #

def is_valid_country(country_name):
    con, cursor = connect()
    sql = "SELECT countryid FROM country WHERE commonname = %s"
    cursor.execute(sql, (country_name,))
    valid_country = cursor.fetchone()
    cursor.close()
    con.close()
    return valid_country is not None

# ---------------- TRAVEL HANDLING ---------------- #

def add_travel_record(travel_info):
    if not is_valid_country(travel_info['country']):
        return False

    con, cursor = connect()
    sql = """INSERT INTO travel (userid, institution, city, country, travelstart, travelend)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (
        travel_info['userid'],
        travel_info['institution'],
        travel_info['city'],
        travel_info['country'],
        travel_info['travelstart'],
        travel_info['travelend']
    )
    cursor.execute(sql, values)
    con.commit()
    cursor.close()
    con.close()
    return True

def get_all_travel():
    con, cursor = connect()
    cursor.execute("SELECT * FROM travel")
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def get_travel_by_userid(userid):
    con, cursor = connect()
    cursor.execute("SELECT * FROM travel WHERE userid = %s", (userid,))
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def get_travel_by_id(travelid):
    con, cursor = connect()
    cursor.execute("SELECT * FROM travel WHERE travelid = %s", (travelid,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    return result

def update_travel_record(updated_travel):
    con, cursor = connect()
    sql = """UPDATE travel
             SET institution = %s, city = %s, country = %s, travelstart = %s, travelend = %s
             WHERE travelid = %s"""
    values = (
        updated_travel['institution'],
        updated_travel['city'],
        updated_travel['country'],
        updated_travel['travelstart'],
        updated_travel['travelend'],
        updated_travel['travelid']
    )
    cursor.execute(sql, values)
    con.commit()
    cursor.close()
    con.close()
    return True

def delete_travel_record(travelid):
    con, cursor = connect()
    cursor.execute("DELETE FROM travel WHERE travelid = %s", (travelid,))
    con.commit()
    cursor.close()
    con.close()
    return True

def get_current_travel():
    con, cursor = connect()
    today = datetime.now().date()
    three_days_ago = today - timedelta(days=3)
    sql = """
    SELECT * FROM travel 
    WHERE (travelstart <= %s AND travelend >= %s)
    OR (travelend BETWEEN %s AND %s)
    """
    values = (today, today, three_days_ago, today)
    cursor.execute(sql, values)
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def get_country_details(normalised_country_name):
    con, cursor = connect()
    cursor.execute("SELECT * FROM country WHERE commonname = %s", (normalised_country_name,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    return result

#--------------------COUNTRY DATA
def load_countries():
    con, cursor = connect()
    cursor.execute("SELECT * FROM country")
    countries_data = cursor.fetchall()
    cursor.close()
    con.close()
    return countries_data
    

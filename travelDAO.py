import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': 'kirstinb2025.mysql.pythonanywhere-services.com',
    'database': 'ggtravel',
    'user': 'kirstinb2025',
    'password': 'rootwsaa'
}

def connect():
    con = mysql.connector.connect(**DB_CONFIG)
    cursor = con.cursor(dictionary=True)
    return con, cursor


"""CREATE TABLE users (
    userid INT NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50),
    PRIMARY KEY (userid)
);

#CREATE TABLE country (
    countryid INT AUTO_INCREMENT PRIMARY KEY,
    common_name VARCHAR(100),
    official_name VARCHAR(150),
    capital VARCHAR(100),
    population BIGINT,
    cca2 CHAR(2) UNIQUE,
    currency VARCHAR(255),
    languages VARCHAR(255),
    flag_url VARCHAR(255),
    map_url VARCHAR(255)
);

#CREATE TABLE travel (
    travelid INT NOT NULL AUTO_INCREMENT,
    userid INT NOT NULL,
    institution VARCHAR(255),
    city VARCHAR(100),
    countryid INT NOT NULL,
    travelstart DATE,
    travelend DATE,
    PRIMARY KEY (travelid),
    FOREIGN KEY (userid) REFERENCES users(userid),
    FOREIGN KEY (countryid) REFERENCES country(countryid)
);"""

# ---------------- USER HANDLING ---------------- #

def add_user(firstname, lastname, email, phone, role):
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

"""def update_user_role(userid, role):
    con, cursor = connect()
    sql = "UPDATE users SET role = %s WHERE userid = %s"
    cursor.execute(sql, (role, userid))
    con.commit()
    cursor.close()
    con.close()
    return True"""


# ---------------- TRAVEL HANDLING ---------------- #

def add_travel_record(travel_info):
    con, cursor = connect()
    sql = """INSERT INTO travel (userid, institution, city, countryid, travelstart, travelend)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (
        travel_info['userid'],
        travel_info['institution'],
        travel_info['city'],
        travel_info['countryid'],
        travel_info['travelstart'],
        travel_info['travelend']
    )
    cursor.execute(sql, values)
    con.commit()
    cursor.close()
    con.close()
    return True

"""def get_all_travel():
    con, cursor = connect()
    cursor.execute("SELECT * FROM travel")
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results"""

def get_travel_by_userid(userid):
    con, cursor = connect()
    sql = """
    SELECT 
        t.travelid, 
        t.userid, 
        t.institution, 
        t.city, 
        t.countryid, 
        c.common_name AS country_name, 
        t.travelstart, 
        t.travelend
    FROM 
        travel t
    JOIN 
        country c ON t.countryid = c.countryid
    WHERE 
        t.userid = %s
    """
    cursor.execute(sql, (userid,))
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def get_travel_by_id(travelid):
    con, cursor = connect()
    sql = """
    SELECT 
        t.travelid, 
        t.userid, 
        t.institution, 
        t.city, 
        t.countryid, 
        c.common_name AS country_name, 
        t.travelstart, 
        t.travelend
    FROM 
        travel t
    JOIN 
        country c ON t.countryid = c.countryid
    WHERE 
        t.travelid = %s
    """
    cursor.execute(sql, (travelid,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    return result

def update_travel_record(updated_travel):
    con, cursor = connect()
    sql = """UPDATE travel
             SET institution = %s, city = %s, countryid = %s, travelstart = %s, travelend = %s
             WHERE travelid = %s"""
    values = (
        updated_travel['institution'],
        updated_travel['city'],
        updated_travel['countryid'],
        updated_travel['travelstart'],
        updated_travel['travelend'],
        updated_travel['travelid']
    )
    try:
        cursor.execute(sql, values)
        con.commit()
        return True, None
    except Exception as e:
        error_message = f"Error updating travel record: {e}"
        print(error_message)
    finally:
        cursor.close()
        con.close()

def delete_travel_record(travelid):
    con, cursor = connect()
    try:
        # Fetch the travel record before deleting
        cursor.execute("SELECT * FROM travel WHERE travelid = %s", (travelid,))
        travel_record = cursor.fetchone()

        if not travel_record:
            return None  # Return None if the record does not exist

        # Delete the travel record
        cursor.execute("DELETE FROM travel WHERE travelid = %s", (travelid,))
        con.commit()
        return travel_record  # Return the deleted travel record
    except Exception as e:
        print(f"Error deleting travel record: {e}")
        return None
    finally:
        cursor.close()
        con.close()

def get_current_travel():
    con, cursor = connect()
    today = datetime.now().date()
    sql = """
    SELECT 
        u.firstname, 
        u.lastname, 
        t.travelid, 
        t.institution, 
        t.city, 
        c.common_name, 
        t.travelstart, 
        t.travelend
    FROM 
        travel t
    JOIN 
        country c ON t.countryid = c.countryid
    JOIN 
        users u ON t.userid = u.userid
    WHERE 
        t.travelstart <= %s AND t.travelend >= %s
    """
    values = (today, today)
    cursor.execute(sql, values)
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def get_all_travel():
    con, cursor = connect()
    sql = """
    SELECT 
        u.firstname, 
        u.lastname, 
        t.travelid, 
        t.institution, 
        t.city, 
        c.common_name, 
        t.travelstart, 
        t.travelend
    FROM 
        travel t
    JOIN 
        country c ON t.countryid = c.countryid
    JOIN 
        users u ON t.userid = u.userid
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    con.close()
    return results

def get_country_details(normalised_country_name):
    con, cursor = connect()
    cursor.execute("SELECT * FROM country WHERE common_name = %s", (normalised_country_name,))
    result = cursor.fetchone()
    cursor.close()
    con.close()
    return result

#--------------------COUNTRY DATA
def load_countries():
    con, cursor = connect()
    cursor.execute("SELECT DISTINCT common_name, official_name, countryid, cca2 FROM country")
    countries_data = cursor.fetchall()
    cursor.close()
    con.close()
    return countries_data
    

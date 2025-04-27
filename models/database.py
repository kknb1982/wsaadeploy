import mysql.connector as mysql
from mysql.connector import Error
import csv

# File path to the admins.csv file
file_path = r"C:\Users\kirst\OneDrive - Atlantic TU\WSAA-project\WSAA_project\data\admins.csv"

try:
    # Connect to the MySQL database
    con = mysql.connect(
        host='localhost',
        user='travel_user',
        password='super_secure_password',
        database='travel_app'
    )
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        # Prepare the SQL query for inserting data
        sql = """INSERT INTO admin (id, adminstatus) VALUES (%s, %s)"""

        # Open the CSV file and read its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Extract the id and adminstatus from each row
                id = int(row['id'])  
                adminstatus = row['status']  

                # Validate the adminstatus value
                if adminstatus not in ['active', 'inactive', 'pending']:
                    print(f"Invalid status '{adminstatus}' for ID {id}. Skipping this record.")
                    continue

                # Execute the SQL query
                cursor.execute(sql, (id, adminstatus))

        # Commit the transaction
        con.commit()
        print(f"{cursor.rowcount} records inserted successfully into admin table.")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close the database connection
    if 'con' in locals() and con.is_connected():
        con.close()
        print("MySQL connection is closed")
        
        
        
file_path = r"C:\Users\kirst\OneDrive - Atlantic TU\WSAA-project\WSAA_project\data\users.csv"

try:
    # Connect to the MySQL database
    con = mysql.connect(
        host='localhost',
        user='travel_user',
        password='super_secure_password',
        database='travel_app'
    )
    if con.is_connected():
        cursor = con.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        # Prepare the SQL query for inserting data
        sql = """INSERT INTO users (firstname, lastname,email,role,phone, status) VALUES (%s, %s, %s, %s, %s, %s)"""

        # Open the CSV file and read its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Extract the id and adminstatus from each row
                firstname = (row['firstname'])  
                adminstatus = row['status']  

                # Validate the adminstatus value
                if adminstatus not in ['active', 'inactive', 'pending']:
                    print(f"Invalid status '{adminstatus}' for ID {id}. Skipping this record.")
                    continue

                # Execute the SQL query
                cursor.execute(sql, (id, adminstatus))

        # Commit the transaction
        con.commit()
        print(f"{cursor.rowcount} records inserted successfully into admin table.")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close the database connection
    if 'con' in locals() and con.is_connected():
        con.close()
        print("MySQL connection is closed")
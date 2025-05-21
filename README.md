# WSAA_project: Global Galway Travel Management System
This Project for Web Services and Applications

## Author
This project has been written by Kirstin Barnett a student at Atlantic Technological University Galway.

## Description
The **Travel Management System** is a web application designed to manage user registrations, travel records, and country data. It provides features for users to register, log in, and manage their travel details, while administrators can oversee all travel records and dynamically search news that may be relevant to travellers. Country details are from the Rest Countries API [https://restcountries.com/](https://restcountries.com/). The news and headlines are dynamically provided by accessing NewsAPI [https://newsapi.org/](https://newsapi.org/).

The editable code to run your own version of the travel management system is available at: [https://github.com/kknb1982/WSAA_project.git](https://github.com/kknb1982/WSAA_project.git)

There is web-hosted version at: [https://kknb2025.pythonanywhere.com/](https://kknb2025.pythonanywhere.com/).

---

## Table of Contents
1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [Installation and Setup](#installation-and-setup)  
4. [How to Use](#how-to-use)
5. [Web-hosted version](#web-hosted-version)  
6. [Database Schema](#database-schema)  
7. [API Endpoints](#api-endpoints)  
8. [Credits](#credits)

---

## Features
- **User Management**: Register, log in, and update user profiles.  
- **Travel Records**: Add, view, update, and delete travel records.  
- **Country Data**: Fetch and update country details from the REST Countries API.  
- **Admin Dashboard**: View all and current travel records.  
- **News Integration**: Fetch news and headlines related to travel destinations.  

---

## Technologies Used
- **Backend**: Python, Flask, Flask-Session  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: MySQL  
- **APIs**: REST Countries API (https://restcountries.com/), News API (https://newsapi.org/)

---

## Installation and Setup
### Prerequisites
- Python 3.12 or higher  
- MySQL database  

### Steps
1. Clone the repository:
   ```bash
   `git clone https://github.com/kknb1982/WSAA_project.git
   cd WSAA_project`

2. Set up a virtual environment:
`python -m venv venv`
`source venv/bin/activate`

3. Install dependencies:
`pip install -r requirements.txt`

4. Configure the database:
Update the DB_CONFIG in travelDAO.py and update_country.py with your MySQL credentials.
Create the database and tables using the schema provided in the travelDAO.py comments.

5. Run the application:
`python server.py`
Access the application at http://127.0.0.1:5000.

# How to Use
## User Features
 - Register: Fill out the registration form to create a new account.
 - Log In: Use your user ID to log in and access your dashboard.
 - Manage Travel Records: Add, view, update, or delete your travel records.

## Admin Features
 - Admin Login: Log in as an admin to access the admin dashboard.
 - All Travel Records: View travel records for all users.

# Web-hosted version
A deployable version of the code has been created and hosted on [PythonAnywhere](https://www.pythonanywhere.com/). The webapp can be found at [https://kknb2025.pythonanywhere.com/](https://kknb2025.pythonanywhere.com/).To look at the staff and student side of the webapp use user id 1,3,4,5,6. To look at the admin functions use login 2.

# Database Schema
## Users Table
```
CREATE TABLE users (
    userid INT NOT NULL AUTO_INCREMENT,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50),
    PRIMARY KEY (userid)
);
```

## Country Table
```
CREATE TABLE country (
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
```

## Travel Table
```
CREATE TABLE travel (
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
);
```

# API Endpoints
## User Management
POST /register: Register a new user.
POST /login: Log in a user.
POST /api/user: Update user information.

## Travel Management
POST /api/travel: Add a new travel record.
GET /api/travel/<userid>: Get all travel records for a user.
DELETE /api/travel/<travelid>: Delete a travel record.

## Country Management
GET /api/countries-simple: Get a list of countries.
GET /country-details/<country_name>: Get details of a specific country.

## Credits
REST Countries API: For country data.
News API: For fetching travel-related news.
PythonAnywhere: For hosting and scheduled tasks.
# Setup Instructions
1. Clone the Repository
   
To get started, clone the repository to your local machine.


git clone https://github.com/CodeChampOne/Group1.git

cd Group1

2. Create a Virtual Environment
Make sure you are using a virtual environment to manage dependencies. Run the following commands:

**python3 -m venv venv**

**source venv/bin/activate**   
On Windows, use 

**venv\Scripts\activate**

3. Install Dependencies
Install all the required packages by running:

**pip install -r requirements.txt**

4. Set Up the Database
The application uses SQLite by default for the database. The database file will be created automatically when you run the application for the first time.

If you want to use MySQL, you can change the connection string in the __init__.py file:

**app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/roundspheres'**

If the database file (roundspheres.db) is not created, ensure you’ve correctly set the SQLALCHEMY_DATABASE_URI in the __init__.py file. If you're using SQLite, make sure the URI is:

**app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roundspheres.db'**

5. Run the Application

Start the Flask application by running:

**python app.py**

The API will be available at http://127.0.0.1:5000.

6. Test the API Endpoints
   
You can now test the API using Postman or cURL.

Project Structure
**app.py**: The main entry point of the Flask application. It initializes the app, sets the configuration, and defines the routes.

**database.py**: Contains the database setup with SQLAlchemy and Marshmallow for ORM and serialization.

**models.py**: Defines the database models (Location, Device, Observation) and their relationships.

**schemas.py**: Contains Marshmallow schemas for serializing and validating the models.

**utils.py**: Contains helper functions, including pagination logic for API responses.

**__init__.py**: Initializes the Flask app, sets up database connections, and handles error routes.

**roundspheres.db**: The SQLite database file, is created automatically upon running the app.

API Endpoints

1. Locations
   
GET /locations

Fetches a list of locations with pagination.

POST /locations

Adds a new location.

GET /locations/<int:location_id>

Retrieves a single location by ID.

PUT /locations/<int:location_id>

Updates an existing location by ID.

DELETE /locations/<int:location_id>

Deletes a location by ID.

2. Devices
   
GET /devices

Fetches a list of devices with pagination.

POST /devices

Adds a new device.

GET /devices/<int:device_id>

Retrieves a single device by ID.

PUT /devices/<int:device_id>

Updates an existing device by ID.

DELETE /devices/<int:device_id>

Deletes a device by ID.

3. Observations
   
GET /observations

Fetches a list of observations with pagination.

POST /observations

Adds a new observation.

GET /observations/<int:observation_id>

Retrieves a single observation by ID.

PUT /observations/<int:observation_id>

Updates an existing observation by ID.

DELETE /observations/<int:observation_id>

Deletes an observation by ID.

Database Models

Location Model

The Location model contains information about physical locations, including:

Location_ID: Unique identifier for each location.

Location_Name: Name of the location.

Coordinates: Coordinates for the location (latitude and longitude).

Relationships:

Each location can have multiple devices and observations.

Device Model

The Device model represents devices associated with a location. It contains:

Device_ID: Unique identifier for each device.

Location_ID: Foreign key referencing the Location model.

Sphere_Name: Name of the device.

Sphere_Address: Address of the device.

Relationships:

Each device is associated with a location and can have multiple observations.

Observation Model

The Observation model records environmental data associated with a device and location. It contains:

id: Unique identifier for each observation.

Device_ID: Foreign key referencing the Device model.

Location_ID: Foreign key referencing the Location model.

Date: Date of the observation.

Time: Time of the observation.

Time_Zone: Time zone of the observation.

Temperature: Temperature recorded during the observation.

Humidity: Humidity level recorded during the observation.

Wind_Direction: Wind direction in degrees.

Precipitation: Amount of precipitation recorded.

Haze: Description of haze conditions.

Pagination

The application supports pagination for endpoints that return lists (e.g., locations, devices, observations). It returns up to 10 items per page by default, supporting custom limit and offset parameters.

Example:

GET /devices?limit=5&offset=10

This will return 5 devices starting from the 11th device.


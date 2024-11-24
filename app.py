from flask import Flask, request
from database import db, ma  # Import db and ma from database module
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy to avoid NameError
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/farnofar/Documents/Github/GROUP1/roundspheres.db' #path to db 
app.config['SQLALCHEMY_ECHO'] = True #echos SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow with the Flask app
db.init_app(app)
ma.init_app(app)

# Import models and schemas  after initializing db and ma
from models import Location, RoundSphere, Observation, APIUser, APIRequest
from schemas import LocationSchema, RoundSphereSchema, ObservationSchema, APIUserSchema, APIRequestSchema


# Initialize schema instances
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
round_sphere_schema = RoundSphereSchema()
round_spheres_schema = RoundSphereSchema(many=True)
observation_schema = ObservationSchema()
observations_schema = ObservationSchema(many=True)
api_user_schema = APIUserSchema()
api_users_schema = APIUserSchema(many=True)
api_request_schema = APIRequestSchema()
api_requests_schema = APIRequestSchema(many=True)

# Endpoint to add a new location
@app.route('/locations', methods=['POST'])
def add_location():
    data = request.get_json()
    new_location = Location(
        Location_Name=data['Location_Name'],
        Location_Address=data['Location_Address']
    )
    db.session.add(new_location)
    db.session.commit()
    return location_schema.jsonify(new_location)

# Endpoint to add a new round sphere
@app.route('/round_spheres', methods=['POST'])
def add_round_sphere():
    data = request.get_json()
    new_sphere = RoundSphere(
        Location_ID=data['Location_ID'],
        Sphere_Name=data['Sphere_Name'],
        Sphere_Address=data['Sphere_Address']
    )
    db.session.add(new_sphere)
    db.session.commit()
    return round_sphere_schema.jsonify(new_sphere)

# Endpoint to add a new observation
@app.route('/observations', methods=['POST'])
def add_observation():
    data = request.get_json()
    new_observation = Observation(
        Sphere_ID=data['Sphere_ID'],
        Location_ID=data['Location_ID'],
        Date=data['Date'],
        Time=data['Time'],
        Temperature=data['Temperature'],
        Humidity=data['Humidity'],
        Status=data['Status']
    )
    db.session.add(new_observation)
    db.session.commit()
    return observation_schema.jsonify(new_observation)

# Endpoint to get all locations
@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return locations_schema.jsonify(locations)

# Endpoint to add a new API user
@app.route('/api_users', methods=['POST'])
def add_api_user():
    data = request.get_json()
    new_user = APIUser(
        apiToken=data['apiToken'],
        User_First_Name=data['User_First_Name'],
        User_Last_Name=data['User_Last_Name'],
        User_Name=data['User_Name'],
        Email=data['Email'],
        Date_Joined=data['Date_Joined'],
        Last_Modified=data['Last_Modified']
    )
    db.session.add(new_user)
    db.session.commit()
    return api_user_schema.jsonify(new_user)

# Add database initialization and start the Flask server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the tables based on your models if they don't exist
    app.run(debug=True)


@app.get("/")
def RoundSpheres():
    return "Hello RoundSpheres"


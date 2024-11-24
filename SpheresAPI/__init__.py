from flask import Flask, request, jsonify
from SpheresAPI.database import db, ma
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from SpheresAPI.database import db, ma
from SpheresAPI.utils import paginate_query


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/farnofar/Documents/Github/GROUP1/roundspheres.db' #path to db 
    app.config['SQLALCHEMY_ECHO'] = True #echos SQL for debug
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db and ma with the Flask app
    db.init_app(app)
    ma.init_app(app)

    # Import models and schemas  after initializing db and ma
    from SpheresAPI.models import Location, RoundSphere, Observation, APIUser, APIRequest
    from SpheresAPI.schemas import LocationSchema, RoundSphereSchema, ObservationSchema, APIUserSchema, APIRequestSchema


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

    # Define Routes with Pagination

    @app.route('/round_spheres', methods=['GET'])
    def get_round_spheres():
        return paginate_query(RoundSphere.query, round_sphere_schema)

    @app.route('/locations', methods=['GET'])
    def get_locations():
        return paginate_query(Location.query, location_schema)

    @app.route('/observations', methods=['GET'])
    def get_observations():
        return paginate_query(Observation.query, observation_schema)

    @app.route('/api_users', methods=['GET'])
    def get_api_users():
        return paginate_query(APIUser.query, api_user_schema)

    @app.route('/api_requests', methods=['GET'])
    def get_api_requests():
        return paginate_query(APIRequest.query, api_request_schema)

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad request"}), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"message": "An internal error occurred"}), 500

    # CRUD Endpoints for Location

    # POST - Endpoint to add a new location
    @app.route('/locations', methods=['POST'])
    def add_location():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = location_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        new_location = Location(
            Location_Name=data['Location_Name'],
            Location_Address=data['Location_Address']
        )
        db.session.add(new_location)
        db.session.commit()
        return location_schema.jsonify(new_location), 201

    #GET - Endpoint to get all locations
    @app.route('/locations', methods=['GET'])
    def get_locations():
        locations = Location.query.all()
        return locations_schema.jsonify(locations)

    #GET -  Endpoint to get a single Location by ID
    @app.route('/locations/<int:location_id>', methods=['GET'])
    def get_location(location_id):
        location = Location.query.get_or_404(location_id)
        return location_schema.jsonify(location)

    #PUT - Endpoint to update an existing Location
    def update_location(location_id):
        location = Location.query.get_or_404(location_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = location_schema.load(json_data, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        if 'Location_Name' in data:
            location.Location_Name = data['Location_Name']
        if 'Location_Address' in data:
            location.Location_Address = data['Location_Address']

        db.session.commit()
        return location_schema.jsonify(location)

    #DELETE - Endpoint to delete an existing Location
    @app.route('/locations/<int:location_id>', methods=['DELETE'])
    def delete_location(location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return jsonify({"message": f"Location with ID {location_id} deleted"}), 200

    # CRUD Endpoints for Round Sphere

    #POST - Endpoint to add a new round sphere
    @app.route('/round_spheres', methods=['POST'])
    def add_round_sphere():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400
        try:
            data = round_sphere_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        
        new_sphere = RoundSphere(
            Location_ID=data['Location_ID'],
            Sphere_Name=data['Sphere_Name'],
            Sphere_Address=data['Sphere_Address']
        )
        db.session.add(new_sphere)
        db.session.commit()
        return round_sphere_schema.jsonify(new_sphere), 201

    #GET - Endpoint to get all round spheres
    @app.route('/round_spheres', methods=['GET'])
    def get_round_spheres():
        spheres = RoundSphere.query.all()
        return round_spheres_schema.jsonify(spheres)

    #GET - Endpoint to get a single round sphere by ID
    @app.route('/round_spheres/<int:sphere_id>', methods=['GET'])
    def get_round_sphere(sphere_id):
        sphere = RoundSphere.query.get_or_404(sphere_id)
        return round_sphere_schema.jsonify(sphere)

    #PUT - Endpoint to update a single round sphere by ID
    @app.route('/round_spheres/<int:sphere_id>', methods=['PUT'])
    def update_round_sphere(sphere_id):
        sphere = RoundSphere.query.get_or_404(sphere_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = round_sphere_schema.load(json_data, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        if 'Sphere_Name' in data:
            sphere.Sphere_Name = data['Sphere_Name']
        if 'Sphere_Address' in data:
            sphere.Sphere_Address = data['Sphere_Address']
        if 'Location_ID' in data:
            sphere.Location_ID = data['Location_ID']

        db.session.commit()
        return round_sphere_schema.jsonify(sphere)

    #DELETE - Endpoint to delete an existing round sphere
    @app.route('/round_spheres/<int:sphere_id>', methods=['DELETE'])
    def delete_round_sphere(sphere_id):
        sphere = RoundSphere.query.get_or_404(sphere_id)
        db.session.delete(sphere)
        db.session.commit()
        return jsonify({"message": f"RoundSphere with ID {sphere_id} deleted"}), 200

    # CRUD Endpoints for Observation

    #POST - Endpoint to add a new observation
    @app.route('/observations', methods=['POST'])
    def add_observation():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = observation_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

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
        return observation_schema.jsonify(new_observation), 201

    #GET - Endpoint to get all observations
    @app.route('/observations', methods=['GET'])
    def get_observations():
        observations = Observation.query.all()
        return observations_schema.jsonify(observations)

    #GET - Endpoint to get a single observation by ID
    @app.route('/observations/<int:observation_id>', methods=['GET'])
    def get_observation(observation_id):
        observation = Observation.query.get_or_404(observation_id)
        return observation_schema.jsonify(observation)

    #PUT - Endpoint to update a single observation by ID
    @app.route('/observations/<int:observation_id>', methods=['PUT'])
    def update_observation(observation_id):
        observation = Observation.query.get_or_404(observation_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = observation_schema.load(json_data, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        if 'Temperature' in data:
            observation.Temperature = data['Temperature']
        if 'Humidity' in data:
            observation.Humidity = data['Humidity']
        if 'Status' in data:
            observation.Status = data['Status']
        if 'Date' in data:
            observation.Date = data['Date']
        if 'Time' in data:
            observation.Time = data['Time']
        if 'Location_ID' in data:
            observation.Location_ID = data['Location_ID']
        if 'Sphere_ID' in data:
            observation.Sphere_ID = data['Sphere_ID']

        db.session.commit()
        return observation_schema.jsonify(observation)

    #DELETE - Endpoint to delete a existing observation by ID
    @app.route('/observations/<int:observation_id>', methods=['DELETE'])
    def delete_observation(observation_id):
        observation = Observation.query.get_or_404(observation_id)
        db.session.delete(observation)
        db.session.commit()
        return jsonify({"message": f"Observation with ID {observation_id} deleted"}), 200

    # CRUD Endpoints for API user

    #POST - Endpoint to add a new API user
    @app.route('/api_users', methods=['POST'])
    def add_api_user():
        print("Endpoint /api_users accessed.")
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = api_user_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

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
        return api_user_schema.jsonify(new_user), 201

    #GET - Endpoint to get all API users
    @app.route('/api_users', methods=['GET'])
    def get_api_users():
        users = APIUser.query.all()
        return api_users_schema.jsonify(users)

    #GET - Endpoint to get a single API user by ID
    @app.route('/api_users/<int:user_id>', methods=['GET'])
    def get_api_user(user_id):
        user = APIUser.query.get_or_404(user_id)
        return api_user_schema.jsonify(user)

    #PUT - Endpoint to update a single API user by ID
    @app.route('/api_users/<int:user_id>', methods=['PUT'])
    def update_api_user(user_id):
        user = APIUser.query.get_or_404(user_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = api_user_schema.load(json_data, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        if 'User_First_Name' in data:
            user.User_First_Name = data['User_First_Name']
        if 'User_Last_Name' in data:
            user.User_Last_Name = data['User_Last_Name']
        if 'User_Name' in data:
            user.User_Name = data['User_Name']
        if 'Email' in data:
            user.Email = data['Email']
        if 'apiToken' in data:
            user.apiToken = data['apiToken']
        if 'Date_Joined' in data:
            user.Date_Joined = data['Date_Joined']
        if 'Last_Modified' in data:
            user.Last_Modified = data['Last_Modified']

        db.session.commit()
        return api_user_schema.jsonify(user)

    #DELETE - Endpoint to delete a single API user by ID
    @app.route('/api_users/<int:user_id>', methods=['DELETE'])
    def delete_api_user(user_id):
        user = APIUser.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"APIUser with ID {user_id} deleted"}), 200


   # Create the tables if they don't exist
    with app.app_context():
        db.create_all()

    return app



    

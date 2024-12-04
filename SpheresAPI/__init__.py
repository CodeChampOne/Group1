from flask import Flask, request, jsonify
from SpheresAPI.database import db, ma
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from SpheresAPI.database import db, ma
from SpheresAPI.utils import paginate_query

def create_app():
    app = Flask(__name__)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hello@localhost/roundspheres'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roundspheres.db'


    app.config['SQLALCHEMY_ECHO'] = True #echos SQL for debug
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db and ma with the Flask app
    db.init_app(app)
    ma.init_app(app)

    # Import models and schemas
    from SpheresAPI.models import Location, Device, Observation
    from SpheresAPI.schemas import LocationSchema, DeviceSchema, ObservationSchema

    # Initialize schema instances
    location_schema = LocationSchema()
    locations_schema = LocationSchema(many=True)
    device_schema = DeviceSchema()
    devices_schema = DeviceSchema(many=True)
    observation_schema = ObservationSchema()
    observations_schema = ObservationSchema(many=True)

    # Define Routes with Pagination

    @app.route('/devices', methods=['GET'])
    def get_devices():
        return paginate_query(Device.query, device_schema)

    @app.route('/locations', methods=['GET'])
    def get_locations():
        return paginate_query(Location.query, location_schema)

    @app.route('/observations', methods=['GET'])
    def get_observations():
        return paginate_query(Observation.query, observation_schema)

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
            Coordinates=data['Coordinates']
        )
        
        db.session.add(new_location)
        db.session.commit()
        return location_schema.jsonify(new_location), 201

    #GET -  Endpoint to get a single Location by ID
    @app.route('/locations/<int:location_id>', methods=['GET'])
    def get_location(location_id):
        location = Location.query.get_or_404(location_id)
        return location_schema.jsonify(location)

    #PUT - Endpoint to update an existing Location
    @app.route('/locations/<int:location_id>', methods=['PUT'])
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
        if 'Coordinates' in data:
            location.Coordinates = data['Coordinates']

        db.session.commit()
        return location_schema.jsonify(location)

    #DELETE - Endpoint to delete an existing Location
    @app.route('/locations/<int:location_id>', methods=['DELETE'])
    def delete_location(location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return jsonify({"message": f"Location with ID {location_id} deleted"}), 200

    # CRUD Endpoints for Device

    #POST - Endpoint to add a new Device
    @app.route('/devices', methods=['POST'])
    def add_device():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400
        try:
            data = device_schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        
        new_device = Device(
            Location_ID=data['Location_ID'],
            Sphere_Name=data['Sphere_Name'],
            Sphere_Address=data['Sphere_Address']
        )
        db.session.add(new_device)
        db.session.commit()
        return device_schema.jsonify(new_device), 201

    #GET - Endpoint to get a single round sphere by ID
    @app.route('/devices/<int:device_id>', methods=['GET'])
    def get_device(device_id):
        device = Device.query.get_or_404(device_id)
        return device_schema.jsonify(device)

    #PUT - Endpoint to update a single round sphere by ID
    @app.route('/devices/<int:device_id>', methods=['PUT'])
    def update_device(device_id):
        device = Device.query.get_or_404(device_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"message": "No input data provided"}), 400

        try:
            data = device_schema.load(json_data, partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400

        if 'Sphere_Name' in data:
            device.Sphere_Name = data['Sphere_Name']
        if 'Sphere_Address' in data:
            device.Sphere_Address = data['Sphere_Address']
        if 'Location_ID' in data:
            device.Location_ID = data['Location_ID']

        db.session.commit()
        return device_schema.jsonify(device)

    #DELETE - Endpoint to delete an existing round sphere
    @app.route('/devices/<int:device_id>', methods=['DELETE'])
    def delete_device(device_id):
        device = Device.query.get_or_404(device_id)
        db.session.delete(device)
        db.session.commit()
        return jsonify({"message": f"Device with ID {device_id} deleted"}), 200

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
            Device_ID=data['Device_ID'],
            Location_ID=data['Location_ID'],
            Date=data['Date'],
            Time=data['Time'],
            Time_Zone=data['Time_Zone'],
            Temperature=data['Temperature'],
            Humidity=data['Humidity'],
            Wind_Direction=data['Wind_Direction'],
            Precipitation=data['Precipitation'],
            Haze=data['Haze']
        )
        db.session.add(new_observation)
        db.session.commit()
        return observation_schema.jsonify(new_observation), 201


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

        if 'Device_ID' in data:
            observation.Device_ID = data['Device_ID']
        if 'Location_ID' in data:
            observation.Location_ID = data['Location_ID']
        if 'Date' in data:
            observation.Date = data['Date']
        if 'Time' in data:
            observation.Time = data['Time']
        if 'Time_Zone' in data:
            observation.Time_Zone = data['Time_Zone']
        if 'Temperature' in data:
            observation.Temperature = data['Temperature']
        if 'Humidity' in data:
            observation.Humidity = data['Humidity']
        if 'Wind_Direction' in data:
            observation.Wind_Direction = data['Wind_Direction']
        if 'Precipitation' in data:
            observation.Precipitation = data['Precipitation']
        if 'Haze' in data:
            observation.Haze = data['Haze']

        db.session.commit()
        return observation_schema.jsonify(observation)


    #DELETE - Endpoint to delete a existing observation by ID
    @app.route('/observations/<int:observation_id>', methods=['DELETE'])
    def delete_observation(observation_id):
        observation = Observation.query.get_or_404(observation_id)
        db.session.delete(observation)
        db.session.commit()
        return jsonify({"message": f"Observation with ID {observation_id} deleted"}), 200

   # Create the tables if they don't exist
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created.")

    return app



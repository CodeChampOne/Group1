import pytest
from SpheresAPI import create_app
from SpheresAPI.database import db
from SpheresAPI.models import Location, RoundSphere, Observation, APIUser, APIRequest
from datetime import datetime

@pytest.fixture
def app():
    # Set up the Flask application for testing with an in-memory SQLite database
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    # Set up the database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_location_crud(client):
    # Create
    location = Location(Location_Name="Test Location", Location_Address="123 Test St")
    db.session.add(location)
    db.session.commit()

    # Read
    retrieved_location = Location.query.first()
    assert retrieved_location is not None
    assert retrieved_location.Location_Name == "Test Location"
    assert retrieved_location.Location_Address == "123 Test St"

    # Update
    retrieved_location.Location_Name = "Updated Location"
    db.session.commit()
    updated_location = Location.query.first()
    assert updated_location.Location_Name == "Updated Location"

    # Delete
    db.session.delete(updated_location)
    db.session.commit()
    assert Location.query.first() is None

def test_round_sphere_crud(client):
    # Create
    location = Location(Location_Name="Test Location", Location_Address="123 Test St")
    db.session.add(location)
    db.session.commit()

    sphere = RoundSphere(Location_ID=location.Location_ID, Sphere_Name="Test Sphere", Sphere_Address="456 Sphere Ave")
    db.session.add(sphere)
    db.session.commit()

    # Read
    retrieved_sphere = RoundSphere.query.first()
    assert retrieved_sphere is not None
    assert retrieved_sphere.Sphere_Name == "Test Sphere"
    assert retrieved_sphere.Sphere_Address == "456 Sphere Ave"
    assert retrieved_sphere.location == location

    # Update
    retrieved_sphere.Sphere_Name = "Updated Sphere"
    db.session.commit()
    updated_sphere = RoundSphere.query.first()
    assert updated_sphere.Sphere_Name == "Updated Sphere"

    # Delete
    db.session.delete(updated_sphere)
    db.session.commit()
    assert RoundSphere.query.first() is None

def test_observation_crud(client):
    # Create
    location = Location(Location_Name="Test Location", Location_Address="123 Test St")
    db.session.add(location)
    db.session.commit()

    sphere = RoundSphere(Location_ID=location.Location_ID, Sphere_Name="Test Sphere", Sphere_Address="456 Sphere Ave")
    db.session.add(sphere)
    db.session.commit()

    observation = Observation(Sphere_ID=sphere.Sphere_ID, Location_ID=location.Location_ID, Date=datetime(2024, 11, 24), Time=datetime.strptime("10:00:00", "%H:%M:%S").time(), Temperature=25.0, Humidity=50.0, Status="Normal")
    db.session.add(observation)
    db.session.commit()

    # Read
    retrieved_observation = Observation.query.first()
    assert retrieved_observation is not None
    assert retrieved_observation.Temperature == 25.0
    assert retrieved_observation.Humidity == 50.0
    assert retrieved_observation.Status == "Normal"
    assert retrieved_observation.location == location
    assert retrieved_observation.sphere == sphere

    # Update
    retrieved_observation.Temperature = 30.0
    db.session.commit()
    updated_observation = Observation.query.first()
    assert updated_observation.Temperature == 30.0

    # Delete
    db.session.delete(updated_observation)
    db.session.commit()
    assert Observation.query.first() is None

def test_api_user_crud(client):
    # Create
    user = APIUser(apiToken="token12345", User_First_Name="John", User_Last_Name="Doe", User_Name="johndoe", Email="john.doe@example.com", Date_Joined="2024-01-01", Last_Modified="2024-01-02")
    db.session.add(user)
    db.session.commit()

    # Read
    retrieved_user = APIUser.query.first()
    assert retrieved_user is not None
    assert retrieved_user.User_First_Name == "John"
    assert retrieved_user.User_Last_Name == "Doe"
    assert retrieved_user.User_Name == "johndoe"
    assert retrieved_user.Email == "john.doe@example.com"

    # Update
    retrieved_user.User_First_Name = "Jane"
    db.session.commit()
    updated_user = APIUser.query.first()
    assert updated_user.User_First_Name == "Jane"

    # Delete
    db.session.delete(updated_user)
    db.session.commit()
    assert APIUser.query.first() is None

def test_api_request_crud(client):
    # Create
    user = APIUser(apiToken="token12345", User_First_Name="John", User_Last_Name="Doe", User_Name="johndoe", Email="john.doe@example.com", Date_Joined="2024-01-01", Last_Modified="2024-01-02")
    db.session.add(user)
    db.session.commit()

    request = APIRequest(endpoint="/api/test", parameters="param=value", timestamp=datetime(2024, 11, 24, 10, 0, 0), status="Success", User_ID=user.User_ID)
    db.session.add(request)
    db.session.commit()

    # Read
    retrieved_request = APIRequest.query.first()
    assert retrieved_request is not None
    assert retrieved_request.endpoint == "/api/test"
    assert retrieved_request.parameters == "param=value"
    assert retrieved_request.status == "Success"
    assert retrieved_request.user == user

    # Update
    retrieved_request.status = "Failed"
    db.session.commit()
    updated_request = APIRequest.query.first()
    assert updated_request.status == "Failed"

    # Delete
    db.session.delete(updated_request)
    db.session.commit()
    assert APIRequest.query.first() is None

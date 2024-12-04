import pytest
from SpheresAPI import create_app
from SpheresAPI.database import db
from SpheresAPI.models import Location, Device, Observation
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
    location = Location(Location="Test Location", Coordinates="40.7128,-74.0060")
    db.session.add(location)
    db.session.commit()

    # Read
    retrieved_location = Location.query.first()
    assert retrieved_location is not None
    assert retrieved_location.Location == "Test Location"
    assert retrieved_location.Coordinates == "40.7128,-74.0060"

    # Update
    retrieved_location.Location = "Updated Location"
    db.session.commit()
    updated_location = Location.query.first()
    assert updated_location.Location == "Updated Location"

    # Delete
    db.session.delete(updated_location)
    db.session.commit()
    assert Location.query.first() is None

def test_device_crud(client):
    # Create
    location = Location(Location="Test Location", Coordinates="40.7128,-74.0060")
    db.session.add(location)
    db.session.commit()

    device = Device(Location_ID=location.Location_ID, Sphere_Name="Test Device", Sphere_Address="123 Device St")
    db.session.add(device)
    db.session.commit()

    # Read
    retrieved_device = Device.query.first()
    assert retrieved_device is not None
    assert retrieved_device.Sphere_Name == "Test Device"
    assert retrieved_device.Sphere_Address == "123 Device St"
    assert retrieved_device.location == location

    # Update
    retrieved_device.Sphere_Name = "Updated Device"
    db.session.commit()
    updated_device = Device.query.first()
    assert updated_device.Sphere_Name == "Updated Device"

    # Delete
    db.session.delete(updated_device)
    db.session.commit()
    assert Device.query.first() is None

def test_observation_crud(client):
    # Create
    location = Location(Location="Test Location", Coordinates="40.7128,-74.0060")
    db.session.add(location)
    db.session.commit()

    device = Device(Location_ID=location.Location_ID, Sphere_Name="Test Device", Sphere_Address="123 Device St")
    db.session.add(device)
    db.session.commit()

    observation = Observation(
        Device_ID=device.Device_ID,
        Location_ID=location.Location_ID,
        Date=datetime(2024, 11, 24).date(),
        Time=datetime.strptime("10:00:00", "%H:%M:%S").time(),
        Time_Zone="UTC+01:00",
        Temperature=25.0,
        Humidity=50.0,
        Wind_Direction=180.0,
        Precipitation=5.0,
        Haze="Clear skies",
    )
    db.session.add(observation)
    db.session.commit()

    # Read
    retrieved_observation = Observation.query.first()
    assert retrieved_observation is not None
    assert retrieved_observation.Temperature == 25.0
    assert retrieved_observation.Humidity == 50.0
    assert retrieved_observation.device == device

    # Update
    retrieved_observation.Temperature = 30.0
    db.session.commit()
    updated_observation = Observation.query.first()
    assert updated_observation.Temperature == 30.0

    # Delete
    db.session.delete(updated_observation)
    db.session.commit()
    assert Observation.query.first() is None

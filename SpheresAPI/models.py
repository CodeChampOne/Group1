from SpheresAPI.database import db  # Import db from database.py


class Location(db.Model):
    __tablename__ = 'locations'
    Location_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location = db.Column(db.String(100), nullable=False)
    Coordinates = db.Column(db.String(200))

    # Relationships
    devices = db.relationship("Device", back_populates="location", cascade="all, delete-orphan")
    observations = db.relationship("Observation", back_populates="location", cascade="all, delete-orphan")


class Device(db.Model):
    __tablename__ = 'devices'
    Device_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location_ID = db.Column(db.Integer, db.ForeignKey('locations.Location_ID'), nullable=False)
    Sphere_Name = db.Column(db.String(100), nullable=False)
    Sphere_Address = db.Column(db.String(200))

    # Relationships
    location = db.relationship("Location", back_populates="devices")
    observations = db.relationship("Observation", back_populates="device", cascade="all, delete-orphan")


class Observation(db.Model):
    __tablename__ = 'observations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Device_ID = db.Column(db.Integer, db.ForeignKey('devices.Device_ID'), nullable=False)
    Location_ID = db.Column(db.Integer, db.ForeignKey('locations.Location_ID'), nullable=False)
    Date = db.Column(db.Date, nullable=False)  # ISO 8601 - YYYYMMDD
    Time = db.Column(db.Time, nullable=False)  # ISO 8601 - hh:mm:ss
    Time_Zone = db.Column(db.String(10), nullable=False)  # ISO 8601 timezone e.g., UTC+10:00
    Temperature = db.Column(db.Float, nullable=False)  # Water/air temperature in °C
    Humidity = db.Column(db.Float, nullable=True)  # g/kg
    Wind_Direction = db.Column(db.Float, nullable=True)  # Wind direction in Decimal degrees
    Precipitation = db.Column(db.Float, nullable=True)  # Precipitation in mm
    Haze = db.Column(db.String(255), nullable=True)  # % % and notes

    # Relationships
    location = db.relationship("Location", back_populates="observations")
    device = db.relationship("Device", back_populates="observations")
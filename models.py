from database import db

class Location(db.Model):
    __tablename__ = 'locations'
    Location_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location_Name = db.Column(db.String(100), nullable=False)
    Location_Address = db.Column(db.String(200))

    # Relationships
    round_spheres = db.relationship("RoundSphere", back_populates="location")
    observations = db.relationship("Observation", back_populates="location")

class RoundSphere(db.Model):
    __tablename__ = 'round_spheres'
    Sphere_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location_ID = db.Column(db.Integer, db.ForeignKey('locations.Location_ID'))
    Sphere_Name = db.Column(db.String(100), nullable=False)
    Sphere_Address = db.Column(db.String(200))

    # Relationships
    location = db.relationship("Location", back_populates="round_spheres")
    observations = db.relationship("Observation", back_populates="sphere")

class Observation(db.Model):
    __tablename__ = 'observations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Sphere_ID = db.Column(db.Integer, db.ForeignKey('round_spheres.Sphere_ID'))
    Location_ID = db.Column(db.Integer, db.ForeignKey('locations.Location_ID'))
    Date = db.Column(db.DateTime)
    Time = db.Column(db.Time)
    Temperature = db.Column(db.Float)
    Humidity = db.Column(db.Float)
    Status = db.Column(db.String(100))

    # Relationships
    location = db.relationship("Location", back_populates="observations")
    sphere = db.relationship("RoundSphere", back_populates="observations")

class APIUser(db.Model):
    __tablename__ = 'api_users'
    User_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apiToken = db.Column(db.String(100), unique=True, nullable=False)
    User_First_Name = db.Column(db.String(100))
    User_Last_Name = db.Column(db.String(100))
    User_Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    Date_Joined = db.Column(db.DateTime)
    Last_Modified = db.Column(db.DateTime)

    # Relationships
    api_requests = db.relationship("APIRequest", back_populates="user")

class APIRequest(db.Model):
    __tablename__ = 'api_requests'
    requestid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    endpoint = db.Column(db.String(200), nullable=False)
    parameters = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.String(100))
    User_ID = db.Column(db.Integer, db.ForeignKey('api_users.User_ID'))

    # Relationships
    user = db.relationship("APIUser", back_populates="api_requests")

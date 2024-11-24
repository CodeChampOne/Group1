from marshmallow import fields, validate, ValidationError
from SpheresAPI.database import ma
from SpheresAPI.models import Location, RoundSphere, Observation, APIUser, APIRequest

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        fields = ("Location_ID", "Location_Name", "Location_Address")

    Location_Name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    Location_Address = fields.String(required=True, validate=validate.Length(min=1, max=200))

class RoundSphereSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoundSphere
        fields = ("Sphere_ID", "Location_ID", "Sphere_Name", "Sphere_Address")

    Sphere_Name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    Sphere_Address = fields.String(required=True, validate=validate.Length(min=1, max=200))
    Location_ID = fields.Integer(required=True)

class ObservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Observation
        fields = ("id", "Sphere_ID", "Location_ID", "Date", "Time", "Temperature", "Humidity", "Status")

    Sphere_ID = fields.Integer(required=True)
    Location_ID = fields.Integer(required=True)
    Date = fields.String(required=True)  # Add format validation if needed
    Time = fields.String(required=True)  # Add format validation if needed
    Temperature = fields.Float(required=True)
    Humidity = fields.Float(required=True)
    Status = fields.String(required=True, validate=validate.Length(min=1))

class APIUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = APIUser
        fields = ("User_ID", "apiToken", "User_First_Name", "User_Last_Name", "User_Name", "Email", "Date_Joined", "Last_Modified")

    User_First_Name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    User_Last_Name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    User_Name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    Email = fields.Email(required=True)
    apiToken = fields.String(required=True, validate=validate.Length(min=10))
    Date_Joined = fields.String(required=True)  # Could use a date field and validate formatting
    Last_Modified = fields.String(required=True)

class APIRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = APIRequest
        fields = ("requestid", "endpoint", "parameters", "timestamp", "status", "User_ID")

    endpoint = fields.String(required=True, validate=validate.Length(min=1, max=200))
    parameters = fields.String(validate=validate.Length(max=500))
    timestamp = fields.String(required=True)  # Use a DateTime field with validation if needed
    status = fields.String(required=True, validate=validate.Length(min=1, max=100))
    User_ID = fields.Integer(required=True)


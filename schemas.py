# schemas.py
from database import ma
from models import Location, RoundSphere, Observation, APIUser, APIRequest


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        fields = ("Location_ID", "Location_Name", "Location_Address")

class RoundSphereSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoundSphere
        fields = ("Sphere_ID", "Location_ID", "Sphere_Name", "Sphere_Address")

class ObservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Observation
        fields = ("id", "Sphere_ID", "Location_ID", "Date", "Time", "Temperature", "Humidity", "Status")

class APIUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = APIUser
        fields = ("User_ID", "apiToken", "User_First_Name", "User_Last_Name", "User_Name", "Email", "Date_Joined", "Last_Modified")

class APIRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = APIRequest
        fields = ("requestid", "endpoint", "parameters", "timestamp", "status", "User_ID")

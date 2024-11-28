from marshmallow import fields, validate, ValidationError
from SpheresAPI.database import ma
from SpheresAPI.models import Location, Device, Observation

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        fields = ("Location_ID", "Location", "Coordinates")

    Location = fields.String(required=True, validate=validate.Length(min=1, max=100))
    Coordinates = fields.String(validate=validate.Length(max=200))


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Device
        fields = ("Device_ID", "Location_ID", "Sphere_Name", "Sphere_Address")

    Sphere_Name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    Sphere_Address = fields.String(validate=validate.Length(max=200))
    Location_ID = fields.Integer(required=True)


class ObservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Observation
        fields = (
            "id",
            "Device_ID",
            "Location_ID",
            "Date",
            "Time",
            "Time_Zone",
            "Temperature",
            "Humidity",
            "Wind_Direction",
            "Precipitation",
            "Haze",
        )

    Device_ID = fields.Integer(required=True)
    Location_ID = fields.Integer(required=True)
    Date = fields.Date(required=True)  # Validate as ISO 8601 date (YYYY-MM-DD)
    Time = fields.Time(required=True)  # Validate as ISO 8601 time (HH:MM:SS)
    Time_Zone = fields.String(required=True, validate=validate.Length(min=3, max=10))  # e.g., UTC+10:00
    Temperature = fields.Float(required=True, validate=validate.Range(min=-100, max=100))  # Example temperature range
    Humidity = fields.Float(validate=validate.Range(min=0, max=100)) 
    Wind_Direction = fields.Float(validate=validate.Range(min=0, max=360))  
    Precipitation = fields.Float(validate=validate.Range(min=0))
    Haze = fields.String(validate=validate.Length(max=255))

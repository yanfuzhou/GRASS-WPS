from app.control.API import api
from flask_restplus import fields

crs = api.model('projection', {
    'name': fields.String(required=True, readOnly=True, description='Use EPSG/OGC standard')
})

crs_properties = api.model('crs', {
    'properties': fields.Nested(crs, required=True, readOnly=True),
    'type': fields.String(required=True, readOnly=True, description="Must be 'name'")
})

properties = api.model('properties', {
    'property_1': fields.Date(readOnly=True, description='Date'),
    'property_2': fields.DateTime(readOnly=True, description='Date Time'),
    'property_3': fields.Float(readOnly=True, description='Value'),
    'property_4': fields.Integer(readOnly=True, description='Value'),
    'property_5': fields.String(readOnly=True, description='Text')
})

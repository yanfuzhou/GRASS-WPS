from grass_app.control.API import api
from flask_restplus import fields
from grass_app.control.Schemas.ogc import crs_properties

wps = api.model('wps', {
    'service': fields.String(required=True, readOnly=True, description="WPS name"),
    'projection': fields.String(required=True, readOnly=True, description="Use EPSG/OGC standard")
})

polygon_geometry = api.model('polygon.geometry', {
    'coordinates': fields.List(fields.List(fields.List(fields.Float)),
                               required=True, readOnly=True,
                               description='[[Longitude, Latitude]]'),
    'type': fields.String(required=True, readOnly=True, description='Polygon')
})

polygon_feature = api.model('polygon.feature', {
    'geometry': fields.Nested(polygon_geometry, required=True, readOnly=True),
    'type': fields.String(required=True, readOnly=True, description="Must be 'Feature'")
})

polygon = api.model('polygon', {
    'crs': fields.Nested(crs_properties, required=True, readOnly=True),
    'features': fields.List(fields.Nested(polygon_feature), required=True, readOnly=True),
    'type': fields.String(required=True, readOnly=True, description="Must be 'FeatureCollection'")
})

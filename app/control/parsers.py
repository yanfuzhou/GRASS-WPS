from flask_restplus import reqparse

viewshed_arguments = reqparse.RequestParser()
viewshed_arguments.add_argument('angle', type=float, required=False, default=0.0, help='View angle 0d ~ 90d')
viewshed_arguments.add_argument('coordinates', type=str, required=True, help='Longitude, Latitude')
viewshed_arguments.add_argument('distance', type=float, required=False, default=1000.0, help='View distance (meters)')

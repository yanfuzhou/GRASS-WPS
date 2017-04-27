from labels import VIEWSHED_LABEL
from flask_restplus import reqparse

viewshed_arguments = reqparse.RequestParser()
viewshed_arguments.add_argument(VIEWSHED_LABEL['coordinates'], type=str, required=True,
                                help='Longitude, Latitude', location='args')
viewshed_arguments.add_argument(VIEWSHED_LABEL['distance'], type=float, required=False, default=1000.0,
                                help='View distance (meters)', location='args')
viewshed_arguments.add_argument(VIEWSHED_LABEL['height'], type=float, required=False, default=1.75,
                                help='Observer height (meters)', location='args')

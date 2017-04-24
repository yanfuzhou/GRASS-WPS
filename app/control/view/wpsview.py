import logging
import math

from flask import request
from flask_restplus import Resource

from app.control.API import api
from app.control.Parsers import viewshed_arguments
from app.control.Schemas import polygon, wps
from app.model import ServiceRegister
from app.model import ViewShed

ns = api.namespace('wps', description='Perform web spatial analysis')
log = logging.getLogger(__name__)


@ns.route('/')
class GetWPSCapabilities(Resource):
    @api.marshal_list_with(wps)
    @api.response(201, 'WPS is running!')
    def get(self):
        """
        Returns capabilities.
        """
        return ServiceRegister().services


@ns.route('/viewshed')
class ViewshedMethod(Resource):
    @api.expect(viewshed_arguments, validate=True)
    # @api.marshal_with(polygon)
    @api.response(201, 'Viewshed successfully created!')
    def get(self):
        """
        Returns viewshed analysis result.
        """
        args = viewshed_arguments.parse_args(request)
        angle = args.get('angle')
        coordinates = args.get('coordinates')
        distance = args.get('distance')
        height = args.get('height')
        if args.get('angle') is not None:
            angle = args.get('angle')
        if angle < 0.0 or angle > 45.0:
            return {"message": "angle must be between 0.0d ~ 45.0d"}
        if args.get('distance') is not None:
             distance = args.get('distance')
        if args.get('height') is not None:
            height = args.get('height')
        if angle is not 0:
            height = height + (math.tan((angle * math.pi)/180) * distance)
        if ',' in coordinates:
            try:
                x = float(coordinates.split(',')[0])
                y = float(coordinates.split(',')[1])
                user = ViewShed(angle=angle, x=x, y=y, distance=distance, height=height)
                user.analysis()
                return {"message": "yes"}
            except Exception as e:
                log.info(e)
                return {"message": "invalid literal for coordinates"}
        else:
            return {"message": "longitude and latitude must be comma separated"}

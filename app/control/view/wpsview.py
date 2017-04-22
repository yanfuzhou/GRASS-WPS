import logging

from flask import request
from flask_restplus import Resource

from app.control.API import api
from app.control.Parsers import viewshed_arguments
from app.control.Schemas import polygon, wps
from app.model import ServiceRegister

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
    @api.marshal_with(polygon)
    @api.response(201, 'Viewshed successfully created!')
    def get(self):
        """
        Returns viewshed analysis result.
        """
        args = viewshed_arguments.parse_args(request)
        if args.get('angle', 0.0) is not None:
            angle = args.get('angle', 0.0)
        coordinates = args.get('coordinates')
        if args.get('distance', 1000.0) is not None:
            distance = args.get('distance', 1000.0)

        return None

import logging
from flask import request
from flask_restplus import Resource
from app.control.API import api
from app.control.parsers import viewshed_arguments

log = logging.getLogger(__name__)

ns = api.namespace('wps', description='Perform web spatial analysis')


@ns.route('/viewshed')
class ViewshedMethod(Resource):

    @api.expect(viewshed_arguments)
    def get(self):
        """
        Returns viewshed analysis result.
        """
        args = viewshed_arguments.parse_args(request)
        coordinates = args.get('coordinates')
        distance = args.get('distance', 1000.0)
        angle = args.get('angle', 0.0)

        return None


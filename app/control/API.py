import logging
from flask_restplus import Api
from app import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='GRASS WPS',
          description='<a href="https://grass.osgeo.org">GRASS</a> '
                      'Web Processing Service built on top of '
                      '<a href="http://geoserver.org">GeoServer</a> '
                      'by using python binding/wrapper')


@api.errorhandler
def default_error_handler(e):
    print(e)
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

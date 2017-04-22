import logging
from flask_restplus import Api
from app import settings

log = logging.getLogger(__name__)

api = Api(version='1.0 (alpha)', title='GRASS WPS',
          description='<a href="https://grass.osgeo.org">GRASS</a> '
                      'web processing service built on top of '
                      '<a href="http://geoserver.org">GeoServer</a> '
                      'by using python binding/wrapper (see <a href="wps/demo">Demo</a>).')


@api.errorhandler
def default_error_handler(e):
    print(e)
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

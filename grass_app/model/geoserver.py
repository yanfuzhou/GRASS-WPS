import os
GEOSERVER_HOST = None
if os.uname()[0] == 'Darwin':
    GEOSERVER_HOST = 'localhost'
    GEOSERVER_URL = 'http://localhost/geoserver/wcs'
if os.uname()[0] == 'Linux':
    GEOSERVER_HOST = 'docker'
GEOSERVER_URL = 'http://' + GEOSERVER_HOST + '/geoserver/wcs'

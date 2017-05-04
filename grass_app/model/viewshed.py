import os
import sys
import uuid
import shutil
import logging
import binascii
import tempfile
import subprocess

log = logging.getLogger(__name__)


def raster_viewshed(coordinates, distance, height, rasterfile):
    # Todo: Set grass7bin to $GRASS_BIN (executable)
    grass7bin = os.getenv('GRASS_BIN')
    # Todo: Set path to $LD_LIBRARY_PATH
    path = os.getenv('LD_LIBRARY_PATH')
    # Todo: Set gisbase to $GISBASE
    gisbase = os.getenv('GISBASE')
    # set GISBASE environment variable
    os.environ['GISBASE'] = gisbase
    # define GRASS-Python environment
    # Todo: If you haven't done following in the terminal
    # Todo: e.g, $ add2virtualenv /usr/local/Cellar/grass7/7.2.0/grass-base/etc/python
    # Todo: please enable below two lines
    # gpydir = os.path.join(gisbase, "etc", "python")
    # sys.path.append(gpydir)
    ########
    # define GRASS DATABASE
    gisdb = os.path.join(tempfile.gettempdir(), 'grassdata')
    try:
        os.stat(gisdb)
    except Exception as e:
        log.info(e)
        os.mkdir(gisdb)
    # location/mapset: use random names for batch jobs
    string_length = 16
    location = binascii.hexlify(os.urandom(string_length))
    mapset = 'PERMANENT'
    location_path = os.path.join(gisdb, location)
    # Create new location (we assume that grass7bin is in the PATH)
    #  from SHAPE or GeoTIFF file
    startcmd = grass7bin + ' -c ' + rasterfile + ' -e ' + location_path
    log.info(startcmd)
    try:
        p = subprocess.Popen(startcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    except OSError as error:
        sys.exit("ERROR: Cannot find GRASS GIS start script"
                 " {cmd}: {error}".format(cmd=startcmd[0], error=error))
    if p.returncode != 0:
        log.info('ERROR: %s' % err)
        log.info('ERROR: Cannot generate location (%s)' % startcmd)
        sys.exit(-1)
    else:
        log.info('Created location %s' % location_path)
    # Now the location with PERMANENT mapset exists.
    ########
    # Now we can use PyGRASS or GRASS Scripting library etc. after
    # having started the session with gsetup.init() etc
    # Set GISDBASE environment variable
    os.environ['GISDBASE'] = gisdb
    dir = os.path.join(gisbase, 'lib')
    if path:
        path = dir + os.pathsep + path
    else:
        path = dir
    os.environ['LD_LIBRARY_PATH'] = path
    # language
    os.environ['LANG'] = 'en_US'
    os.environ['LOCALE'] = 'C'
    # Import GRASS Python bindings
    import grass.script as grass
    import grass.script.setup as gsetup
    ###########
    # Launch session and do something
    gsetup.init(gisbase, gisdb, location, mapset)
    # do something else: r.mapcalc, v.rectify, ...
    rastermap = 'dem'
    outraster = 'viewshed'
    outvector = 'polygonized'
    dissolved = 'dissolved'
    grass.run_command('r.in.gdal', quiet=True, input=rasterfile, output=rastermap)
    grass.run_command('r.viewshed', quiet=True, input=rastermap, output=outraster, coordinates=coordinates,
                      observer_elevation=height, max_distance=distance)
    grass.run_command('r.to.vect', input=outraster, output=outvector, type='area')
    grass.run_command('v.db.addcolumn', map=outvector, columns='dis int')
    grass.run_command('v.db.update', map=outvector, column='dis', value=1)
    grass.run_command('v.dissolve', input=outvector, column='dis', output=dissolved)
    vectorfile = os.path.join(tempfile.gettempdir(), str(uuid.uuid1()) + '.geojson')
    grass.run_command('v.out.ogr', input=dissolved, output=vectorfile, format='GeoJSON')
    # Finally remove the temporary batch location from disk
    log.info('Removing location %s' % location_path)
    shutil.rmtree(location_path)
    return vectorfile


def viewshed_payload(min_x, min_y, max_x, max_y):
    lower_corner = str(min_x) + ' ' + str(min_y)
    upper_corner = str(max_x) + ' ' + str(max_y)
    data = '<?xml version="1.0" encoding="UTF-8"?>' \
           '<GetCoverage ' \
           'version="1.1.1" ' \
           'service="WCS" ' \
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
           'xmlns="http://www.opengis.net/wcs/1.1.1" ' \
           'xmlns:ows="http://www.opengis.net/ows/1.1" ' \
           'xmlns:gml="http://www.opengis.net/gml" ' \
           'xmlns:ogc="http://www.opengis.net/ogc" ' \
           'xsi:schemaLocation="http://www.opengis.net/wcs/1.1.1 http://schemas.opengis.net/wcs/1.1.1/wcsAll.xsd">' \
           '<ows:Identifier>demo:new_york_dem</ows:Identifier>' \
           '<DomainSubset>' \
           '<ows:BoundingBox crs="urn:ogc:def:crs:EPSG::3857">' \
           '<ows:LowerCorner>' + lower_corner + '</ows:LowerCorner>' \
           '<ows:UpperCorner>' + upper_corner + '</ows:UpperCorner>' \
           '</ows:BoundingBox>' \
           '</DomainSubset>' \
           '<Output store="true" format="image/tiff"></Output>' \
           '</GetCoverage>'
    return data
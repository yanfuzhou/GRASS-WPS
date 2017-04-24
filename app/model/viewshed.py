import os
import sys
import subprocess
import shutil
import binascii
import tempfile
import logging

log = logging.getLogger(__name__)


def raster_viewshed(coordinates, height, rasterfile):
    # Linux: Set path to GRASS bin executable (TODO: NEEDED?)
    grass7bin = os.getenv('GRASS_BIN')
    # Linux: Set path to GRASS libs (TODO: NEEDED?)
    path = os.getenv('LD_LIBRARY_PATH')
    # query GRASS GIS itself for its GISBASE
    startcmd = grass7bin + ' --config path'
    try:
        p = subprocess.Popen(startcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    except OSError as error:
        sys.exit("ERROR: Cannot find GRASS GIS start script"
                 " {cmd}: {error}".format(cmd=startcmd[0], error=error))
    if p.returncode != 0:
        print >> sys.stderr, "ERROR: %s" % err
        print >> sys.stderr, "ERROR: Cannot find GRASS GIS 7 start script (%s)" % startcmd
        sys.exit(-1)
    gisbase = out.strip(os.linesep)
    # set GISBASE environment variable
    os.environ['GISBASE'] = gisbase
    # define GRASS-Python environment
    gpydir = os.path.join(gisbase, "etc", "python")
    sys.path.append(gpydir)
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
        print >> sys.stderr, 'ERROR: %s' % err
        print >> sys.stderr, 'ERROR: Cannot generate location (%s)' % startcmd
        sys.exit(-1)
    else:
        print 'Created location %s' % location_path
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
    # say hello
    grass.message('--- GRASS GIS 7: Current GRASS GIS 7 environment:')
    print grass.gisenv()
    # do something in GRASS now...
    grass.message('--- GRASS GIS 7: Checking projection info:')
    in_proj = grass.read_command('g.proj', flags='jf')
    # selective proj parameter printing
    kv = grass.parse_key_val(in_proj)
    print kv
    print kv['+proj']
    # print full proj parameter printing
    in_proj = in_proj.strip()
    grass.message("--- Found projection parameters: '%s'" % in_proj)
    # show current region:
    grass.message('--- GRASS GIS 7: Checking computational region info:')
    in_region = grass.region()
    grass.message("--- Computational region: '%s'" % in_region)
    # do something else: r.mapcalc, v.rectify, ...


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
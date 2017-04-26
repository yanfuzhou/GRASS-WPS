import os
import json
import pycurl
import urllib
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import logging
import tempfile
import xml.etree.ElementTree as ET
from app.control.Schemas.ogc.epsg import WGS84WM
from app.model.geoserver import GEOSERVER_URL
from app.model.viewshed import viewshed_payload, raster_viewshed

log = logging.getLogger(__name__)


class ServiceRegister(object):
    def __init__(self):
        self.services = json.loads(str('['
                                       '{"service": "viewshed", "projection": "' + WGS84WM + '"}'
                                       ']'))


class ViewShed(object):
    def __init__(self, x, y, distance, height):
        self.x = x
        self.y = y
        self.distance = distance
        self.height = height

    def analysis(self):
        crs = json.loads('{"type": "name", "properties": { "name": "' + WGS84WM + '" }}')
        min_x = self.x - self.distance
        max_x = self.x + self.distance
        min_y = self.y - self.distance
        max_y = self.y + self.distance
        data = viewshed_payload(min_x, min_y, max_x, max_y)
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, GEOSERVER_URL)
        c.setopt(pycurl.HTTPHEADER, ['content-type: application/xml'])
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.WRITEDATA, buffer)
        c.perform()
        if c.getinfo(pycurl.RESPONSE_CODE) is 200:
            log.info('Downloaded in: ' + str(c.getinfo(pycurl.TOTAL_TIME)) + 's')
            root = ET.fromstring(buffer.getvalue())
            ns = {'ows': 'http://www.opengis.net/ows/1.1'}
            link = None
            for child in root:
                link = child.find('ows:Reference', ns).attrib['{http://www.w3.org/1999/xlink}href']
            rasterfile = os.path.join(tempfile.gettempdir(), os.path.basename(link))
            urllib.urlretrieve(link, rasterfile)
            vectorfile = raster_viewshed(coordinates=str(self.x) + ',' + str(self.y), distance=self.distance,
                                         height=self.height, rasterfile=rasterfile)
            with open(vectorfile, 'r') as data:
                result = json.loads(data.read())
                result[u'crs'] = crs
            data.close()
            for record in result[u'features']:
                del record[u'properties']
            os.remove(rasterfile)
            os.remove(vectorfile)
            return result
        c.close()

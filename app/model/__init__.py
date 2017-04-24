import json
import uuid
import pycurl
import logging
import tempfile
from app.control.Schemas.ogc.epsg import WGS84WM
from app.model.geoserver import GEOSERVER_URL
from app.model.viewshed import viewshed_payload

log = logging.getLogger(__name__)


class ServiceRegister(object):
    def __init__(self):
        self.services = json.loads(str('['
                                       '{"service": "viewshed", "projection": "' + WGS84WM + '"}'
                                       ']'))


class ViewShed(object):
    def __init__(self, angle, x, y, distance, height):
        self.angle = angle
        self.x = x
        self.y = y
        self.distance = distance
        self.height = height

    def analysis(self):
        min_x = self.x - self.distance
        max_x = self.x + self.distance
        min_y = self.y - self.distance
        max_y = self.y + self.distance
        data = viewshed_payload(min_x, min_y, max_x, max_y)
        tfdem = tempfile.NamedTemporaryFile(mode='w+b', prefix=str(uuid.uuid1()) + '-', suffix='.tif', delete=False)
        with open(tfdem.name, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(pycurl.URL, GEOSERVER_URL)
            c.setopt(pycurl.HTTPHEADER, ['content-type: application/xml'])
            c.setopt(pycurl.POST, 1)
            c.setopt(pycurl.POSTFIELDS, data)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            if c.getinfo(pycurl.RESPONSE_CODE) is 200:
                log.info('Downloaded in: ' + str(c.getinfo(pycurl.TOTAL_TIME)) + 's')
                print tfdem.name
            c.close()
            f.close()

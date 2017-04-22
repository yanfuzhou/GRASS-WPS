import json
from app.control.Schemas.ogc.epsg import WGS84WM


class ServiceRegister(object):
    def __init__(self):
        self.services = json.loads(str('['
                                       '{"service": "viewshed", "projection": "' + WGS84WM + '"}'
                                                                                             ']'))

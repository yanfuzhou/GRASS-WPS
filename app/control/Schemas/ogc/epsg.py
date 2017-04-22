from crs import EPSG

# EPSG code for supported OGC standard that defined in 'ogc.standard' package
# Reference: https://portal.opengeospatial.org/files/?artifact_id=24045 (See Table 3)

code = [
    '3857',     # WGS Web Mercator
    '4326',     # WGS84 longitude-latitude
    '4269',     # NAD83 longitude-latitude
    '4267',     # NAD27 longitude-latitude
    '5703'      # NAVD88
]

WGS84WM = EPSG + code[0]
WGS84 = EPSG + code[1]
NAD83 = EPSG + code[2]
NAD27 = EPSG + code[3]
NAVD88 = EPSG + code[4]

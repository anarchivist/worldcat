"""
mark matienzo 2009

dependencies: web.py, worldcat, simplejson, geopy, & elementtree
to run: python holdingsmap.py
point your web browser at http://localhost:8080/
"""
from worldcat.request.search import LibrariesRequest, CitationRequest
from worldcat.request.xid import xOCLCNUMRequest
from worldcat.request.registry import OCLCSymbolRequest
import simplejson
import web
from elementtree import ElementTree as ET
from urllib2 import urlopen, HTTPError
from geopy import geocoders as gc
from multiprocessing import Pool

REG_BASE_NS = 'info:rfa/rfaRegistry/xmlSchemas/institution'


class QGoogleGC(gc.Google):
    """subclassing the Google geocoder from geopy because of its
    annoying print statements"""

    def __init__(self, api_key=None, domain='maps.google.com',
                 resource='maps/geo', format_string='%s',
                 output_format='kml'):
        super(QGoogleGC, self).__init__(api_key, domain, resource,
                                        format_string, output_format)

    def geocode_url(self, url, exactly_one=True):
        page = urlopen(url)
        dispatch = getattr(self, 'parse_' + self.output_format)
        return dispatch(page, exactly_one)

WSKEY = 'your worldcat api key'
GMAPKEY = 'your google maps api key'

XPATHS = {
    'lat': '{info:rfa/rfaRegistry/xmlSchemas/institutions/nameLocation}nameLocation''/{info:rfa/rfaRegistry/xmlSchemas/institutions/nameLocation}mainAddress/{info:rfa/rfaRegistry/xmlSchemas/institutions/nameLocation}latitude',
    'lng':
'{info:rfa/rfaRegistry/xmlSchemas/institutions/nameLocation}nameLocation/{info:rfa/rfaRegistry/xmlSchemas/institutions/nameLocation}mainAddress/{info:rfa/rfaRegistry/xmlSchemas/institutions/nameLocation}longitude',
}

gcoder = QGoogleGC(GMAPKEY)
urls = (
        '/', 'index',
        '/locations', 'locations',
        '/json', 'json',
        '/(locations|json)?__history__.html', 'history',
        '/(.*)favicon.ico', 'history')
render = web.template.render('templates/')


def process_libraries(result):
    _ = {}
    _['oclcid'] = result.findtext('institutionIdentifier/value')
    _['label'] = result.findtext('physicalLocation')
    _['type'] = 'library'
    _['address'] = result.findtext('physicalAddress/text')
    _['numberOfCopies'] = result.findtext('holdingSimple/copiesSummary/copiesCount')
    try:
        _['link'] = result.findtext('electronicAddress/text')
    except AttributeError:
        pass
    try:
        reginfo = OCLCSymbolRequest(symbol=_['oclcid']).get_response()
        reginfo = ET.XML(reginfo.data)
        lat = reginfo.findtext(XPATHS['lat'])
        if lat is None:
            c, (lat, lng) = gcoder.geocode(_['address'])
        else:
            lng = reginfo.findtext(XPATHS['lng'])
        _['addressLatLng'] = '%s,%s' % (lat, lng)
    except ValueError:
        pass
    return _


class index:

    def GET(self):
        rdata = {'key': GMAPKEY, 'ctr': ('40.77', '-73.98')}
        return render.index(rdata=rdata)


class json:

    def GET(self):
        args = web.input(oclcnum=None, zip='11216')
        jsonout = {'items': [],
                    'types': {'library': {'pluralLabel': 'libraries'}}}
        lookup = LibrariesRequest(wskey=WSKEY, rec_num=args.oclcnum,
                    location=args.zip, maximumLibraries=100).get_response()
        results = ET.XML(lookup.data)
        jsonout['items'] = Pool(processes=20).map(process_libraries, results)
        web.header('Content-Type', 'application/json')
        return simplejson.dumps(jsonout)


class locations:

    def GET(self):
        rdata = web.input(oclcnum=None, zip='11216')
        c, rdata['ctr'] = gcoder.geocode(rdata['zip'])
        rdata['key'] = GMAPKEY
        rdata['cit'] = CitationRequest(wskey=WSKEY,
                        rec_num=rdata['oclcnum']).get_response().data
        o = xOCLCNUMRequest(rec_num=rdata['oclcnum']).get_response().data
        rdata['others'] = []
        try:
            for _ in o['list']:
                if _.has_key('presentOclcnum') is False \
                    and _['oclcnum'][0] not in _['oclcnum']:
                    rdata['others'].extend(_['oclcnum'])
        except:
            pass
        c, (lat, lon) = gcoder.geocode(rdata['zip'])
        return render.locations(rdata=rdata)

    def POST(self):
        rdata = web.input(oclcnum=None, zip='11216')
        c, rdata['ctr'] = gcoder.geocode(rdata['zip'])
        rdata['key'] = GMAPKEY
        rdata['cit'] = CitationRequest(wskey=WSKEY,
                            rec_num=rdata['oclcnum']).get_response().data
        o = xOCLCNUMRequest(rec_num=rdata['oclcnum']).get_response().data
        rdata['others'] = []
        try:
            for _ in o['list']:
                if _.has_key('presentOclcnum') is False \
                    and _['oclcnum'][0] not in _['oclcnum']:
                    rdata['others'].extend(_['oclcnum'])
        except:
            pass
        c, (lat, lon) = gcoder.geocode(rdata['zip'])
        return render.locations(rdata=rdata)


class history:

    def GET(self, _=None):
        return '<html><body></body></html>'


def runfcgi_apache(func):
    web.wsgi.runfcgi(func, None)

if __name__ == '__main__':
    #web.wsgi.runwsgi = runfcgi_apache
    web.application(urls, globals()).run()

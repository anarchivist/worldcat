"""
mark matienzo 2008

dependencies: web.py, lxml, worldcat, lxml, geopy

to run: python holdingsmap.py
point your web browser at http://localhost:8080/
"""
from worldcat.request.search import LibrariesRequest, CitationRequest
from worldcat.request.xid import xOCLCNUMRequest
#from worldcat.util.extract import extract_elements, pymarc_extract

import simplejson
import web
from lxml import etree as ET
from urllib2 import urlopen, HTTPError

from geopy import geocoders as gc



urls = ('/', 'index', '/locations/(.*)', 'locations', '/locations', 'locations', '/json/(.*)', 'json', '/(.*)__history__.html', 'history')
render = web.template.render('templates/')
WSKEY = 'YOUR API KEY'
gmapkey = 'YOUR API KEY FOR GMAPSA'

class QGoogleGC(gc.Google):
    """docstring for QGoogleGC"""
    def __init__(self, api_key=None, domain='maps.google.com',
                 resource='maps/geo', format_string='%s',
                 output_format='kml'):
        super(QGoogleGC, self).__init__(api_key, domain, resource, format_string, output_format)
    
    def geocode_url(self, url, exactly_one=True):
        page = urlopen(url)
        dispatch = getattr(self, 'parse_' + self.output_format)
        return dispatch(page, exactly_one)

gcoder  = QGoogleGC(gmapkey)

class index:
    def GET(self):
        print render.index(gmapkey=gmapkey)
        
class json:
    def GET(self, oclcnum):
        jsonout = {'items': [], 'types': {'library': {'pluralLabel': 'libraries'}}}
        lookup = LibrariesRequest(wskey=WSKEY, rec_num=oclcnum, maximumLibraries=100, ip='67.99.185.2').get_response()
        results = ET.XML(lookup.data)
        for result in results.findall('holding'):
            _ = {}
            _['oclcid'] = result.find('institutionIdentifier/value').text
            _['label'] = result.find('physicalLocation').text
            _['type'] = 'library'
            _['address'] = result.find('physicalAddress/text').text
            _['numberOfCopies'] = result.find('holdingSimple/copiesSummary/copiesCount').text
            try:
                _['link'] = result.find('electronicAddress/text').text
            except AttributeError:
                pass
            try:
                c, (lat, lng) = gcoder.geocode(_['address'])
                _['addressLatLng'] = '%s,%s' % (lat, lng)
            except ValueError:
                pass
            jsonout['items'].append(_)
        web.header('Content-Type', 'application/json')
        print simplejson.dumps(jsonout)


class locations:
    def GET(self, oclcnum):
        citation = CitationRequest(wskey=WSKEY, rec_num=oclcnum).get_response().data
        o = xOCLCNUMRequest(rec_num=oclcnum).get_response().data
        others = []
        try:
            for _ in o['list']:
                others.extend(_['oclcnum'])
            others.remove(oclcnum)
        except:
            pass
        print render.locations(gmapkey=gmapkey, oclcnum=oclcnum, citation=citation, others=others)
    
    def POST(self):
        oclcnum = web.input().oclcnum
        citation = CitationRequest(wskey=WSKEY, rec_num=oclcnum).get_response().data
        o = xOCLCNUMRequest(rec_num=oclcnum).get_response().data
        others = []
        try:
            for _ in o['list']:
                others.extend(_['oclcnum'])
            others.remove(oclcnum)
        except:
            pass
        print render.locations(gmapkey=gmapkey, oclcnum=oclcnum, citation=citation, others=others)
        
class history:
    def GET(self):
        print '<html><body></body></html>'

web.webapi.internalerror = web.debugerror
if __name__ == '__main__':
    web.run(urls, globals(), web.reloader)
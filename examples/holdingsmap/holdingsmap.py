"""
mark matienzo 2009

dependencies: web.py, worldcat, simplejson, geopy, & elementtree
to run: python holdingsmap.py
point your web browser at http://localhost:8080/
"""
from worldcat.request.search import LibrariesRequest, CitationRequest
from worldcat.request.xid import xOCLCNUMRequest
import simplejson
import web
from elementtree import ElementTree as ET
from urllib2 import urlopen, HTTPError
from geopy import geocoders as gc

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

WSKEY = 'YOUR WORLDCAT API KEY'
GMAPKEY = 'YOUR GOOGLE MAPS API KEY'
gcoder = QGoogleGC(GMAPKEY)
urls = (
        '/', 'index',
        '/locations', 'locations',
        '/json', 'json',
        '/(locations|json)?__history__.html', 'history'
        )
render = web.template.render('templates/')

class index:
    def GET(self):
        rdata = {'key': GMAPKEY, 'ctr': ('40.77','-73.98')}
        print render.index(rdata=rdata)

class json:
    def GET(self):
        args = web.input(oclcnum=None, zip='11216')
        jsonout = {'items': [],
                    'types': {'library': {'pluralLabel': 'libraries'}} }
        lookup = LibrariesRequest(wskey=WSKEY, rec_num=args.oclcnum,
                    location=args.zip, maximumLibraries=100).get_response()
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
                rdata['others'].extend(_['oclcnum'])
            rdata['others'].remove(rdata['oclcnum'])
        except:
            pass
	    c, (lat, lon) = gcoder.geocode(rdata['zip'])
        print render.locations(rdata=rdata)
    
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
                rdata['others'].extend(_['oclcnum'])
            rdata['others'].remove(rdata['oclcnum'])
        except:
            pass
	    c, (lat, lon) = gcoder.geocode(rdata['zip'])
        print render.locations(rdata=rdata)
        
class history:
    def GET(self, _=None):
        print '<html><body></body></html>'

def runfcgi_apache(func):
    web.wsgi.runfcgi(func, None)
      
if __name__ == '__main__':
    web.wsgi.runwsgi = runfcgi_apache
    web.run(urls, globals())
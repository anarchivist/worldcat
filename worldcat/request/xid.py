# Copyright (C) 2008 Mark A. Matienzo
# 
# This file is part of worldcat, the Python WorldCat API module.
# 
# worldcat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# worldcat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with worldcat.  If not, see <http://www.gnu.org/licenses/>.

# request/xid.py -- Request objects for xID APIs (xISBN and xISSN)

from worldcat.request import WorldCatRequest
from worldcat.response import xIDResponse

class xIDRequest(WorldCatRequest):
    """request.xid.xIDRequest: Base class for requests from xID APIs"""
    def __init__(self, rec_num=None, **kwargs):
        """Constructor for xIDRequests."""
        if 'method' not in kwargs:
            kwargs['method'] = 'getEditions'
        if 'format' not in kwargs:
            kwargs['format'] = 'python'
        WorldCatRequest.__init__(self, **kwargs)
        self.rec_num = rec_num
        
    def get_response(self):
        self.http_get()
        return xIDResponse(self)
        
    def subclass_validator(self, quiet=False):
        """Validator method for xIDRequests.

        Does not validate ISSN or ISBN values; this should be handled
        by the xID APIs.
        
        """
        if self.rec_num == None:
            if quiet == True:
                return False
            else:
                raise EmptyRecordNumberError
        else:
            return True

class xISSNRequest(xIDRequest):
    """request.xid.xISSNRequest: Class for xISSN requests
    
    Other request methods to the xISSN API have not yet been implemented
    (e.g. unAPI). These should be subclasses, probably.
    """
    def __init__(self, rec_num=None, **kwargs):
        """Constructor method for xISSNRequests."""
        xIDRequest.__init__(self, rec_num, **kwargs)
        self._validators = {
            'method': ('getForms', 'getHistory', 'fixChecksum',
                        'getMetadata', 'getEditions'),
            'format': ('xml', 'html', 'json', 'python', 'ruby')
            }
        
    def api_url(self):
        self.url = 'http://xissn.worldcat.org/webservices/xid/issn/%s' \
            % self.rec_num
            
class xISBNRequest(xIDRequest):
    """request.xisbn.xISBNRequest: Class for xISBN requests

    Other request methods to the xISBN API have not yet been implemented
    (e.g. unAPI). These should be subclasses, probably.
    """
    def __init__(self, rec_num=None, **kwargs):
        """Constructor method for xISBNRequests."""
        xIDRequest.__init__(self, rec_num, **kwargs)
        self._validators = {
            'method': ('to10', 'to13', 'fixChecksum',
                        'getMetadata', 'getEditions'),
            'format': ('xml', 'html', 'json', 'python', 'ruby', 'txt', 'csv')
            }

    def api_url(self):
        self.url = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s' \
            % self.rec_num
            
class xOCLCNUMRequest(xIDRequest):
    """request.xisbn.xOCLCNUMRequest: Class for xOCLCNUM requests

    """
    def __init__(self, rec_num=None, **kwargs):
        """Constructor method for xISBNRequests."""
        xIDRequest.__init__(self, rec_num, **kwargs)
        self._validators = {
            'method': ('getVariants', 'getMetadata', 'getEditions'),
            'format': ('xml', 'html', 'json', 'python', 'ruby', 'txt', 'csv')
            }

    def api_url(self):
        self.url = 'http://xisbn.worldcat.org/webservices/xid/oclcnum/%s' \
            % self.rec_num
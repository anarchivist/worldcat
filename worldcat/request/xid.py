# Copyright (C) 2008-2009 Mark A. Matienzo
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

""" worldcat/request/xid.py -- Request objects for xID APIs

    xID APIs as of this writing include xISBN, xISSN, and xOCLCNUM.

    'Alternate request formats' (such as OpenURL and unAPI) have not been
    implemented.

"""

from worldcat.exceptions import EmptyRecordNumberError
from worldcat.request import WorldCatRequest
from worldcat.response.xid import xIDResponse


class xIDRequest(WorldCatRequest):
    """request.xid.xIDRequest: Base class for requests from xID APIs.

    All xIDRequests require a record number ('rec_num') to be passed when
    a class is instantiated. Depending on the request, this will either be
    an ISBN, an ISSN, or an OCLC record number.

    xIDRequests by default have their 'method' set as 'getEditions' and their
    response format set as 'python'.

    """

    def __init__(self, rec_num=None, **kwargs):
        """Constructor for xIDRequests."""
        if 'method' not in kwargs:
            kwargs['method'] = 'getEditions'
        if 'format' not in kwargs:
            kwargs['format'] = 'python'
        if 'fl' not in kwargs:
            kwargs['fl'] = '*'
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

    For more information on the xISSN API, see
    <http://xissn.worldcat.org/xissnadmin/doc/api.htm>.

    Example of an xISSNRequest:

        >>> from worldcat.request.xid import xISSNRequest
        >>> x = xISSNRequest(rec_num='1895-104X')
        >>> x.validate()
        >>> r = x.get_response()

    """

    def __init__(self, rec_num=None, **kwargs):
        """Constructor method for xISSNRequests."""
        xIDRequest.__init__(self, rec_num, **kwargs)
        self._validators = {
            'method': ('getForms', 'getHistory', 'fixChecksum',
                        'getMetadata', 'getEditions', 'hyphen'),
            'format': ('xml', 'html', 'json', 'python',
                        'ruby', 'text', 'csv', 'php')}

    def api_url(self):
        self.url = 'http://xissn.worldcat.org/webservices/xid/issn/%s' \
            % self.rec_num


class xISBNRequest(xIDRequest):
    """request.xid.xISBNRequest: Class for xISBN requests
    """

    def __init__(self, rec_num=None, **kwargs):
        """Constructor method for xISBNRequests."""
        xIDRequest.__init__(self, rec_num, **kwargs)
        self._validators = {
            'method': ('to10', 'to13', 'fixChecksum',
                        'getMetadata', 'getEditions'),
            'format': ('xml', 'html', 'json', 'python',
                        'ruby', 'txt', 'csv', 'php')}

    def api_url(self):
        self.url = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s' \
            % self.rec_num


class xOCLCNUMRequest(xIDRequest):
    """request.xid.xOCLCNUMRequest: Class for xOCLCNUM requests
    
    This now replaces the old xOCLCNUMRequest class in worldcat >= 0.3.1. 
    xOCLCNUMRequest now takes a 'type' argument; one of "oclcnum", "lccn",
    or "owi", for OCLC record numbers, Library of Congress Catalog Numbers, or
    OCLC Work Identifiers.

    """

    def __init__(self, rec_num=None, numtype='oclcnum' **kwargs):
        """Constructor method for xISBNRequests."""
        xIDRequest.__init__(self, rec_num, **kwargs)
        self._validators = {
            'method': ('getVariants', 'getMetadata', 'getEditions'),
            'format': ('xml', 'html', 'json', 'python',
                        'ruby', 'txt', 'csv', 'php')}

    def api_url(self):
        self.url = 'http://xisbn.worldcat.org/webservices/xid/%s/%s' \
            % (numtype, self.rec_num)

# Copyright (C) 2009 Mark A. Matienzo
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

# request/registry.py -- Request objects for WorldCat Registry data

from worldcat.response.registry import RegistryResponse
from worldcat.request import WorldCatRequest
#from worldcat.request.search import SRURequest
from worldcat.exceptions import EmptyQueryError

from urllib import quote

# TODO: Add SRU search interface

class OCLCSymbolRequest(WorldCatRequest):
    """request.registry.OCLCSymbolRequest: get registry data by OCLC symbol"""
    
    def __init__(self, symbol=None, **kwargs):
        """Constructor for LookupByOCLCSymbolRequest."""
        if 'serviceLabel' not in kwargs:
            kwargs['serviceLabel'] = 'content'
        WorldCatRequest.__init__(self, **kwargs)
        self.symbol = symbol

    def api_url(self):
        self.url = \
'http://worldcat.org/webservices/registry/lookup/Institutions/oclcSymbol/%s' \
            % quote(self.symbol)
       
    def get_response(self):
        self.http_get()
        return RegistryResponse(self)
        
    def subclass_validator(self, quiet=False):
        """Validator method for LookupByOCLCSymbolRequests."""
        if self.symbol == None:
            if quiet == True:
                return False
            else:
                raise EmptyQueryError
        else:
            return True
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

# response.py - Contains response objects for requests from WorldCat API

import warnings

class WorldCatResponse(object):
    """response.WorldCatResponse: Base class for responses from WorldCat APIs
    
    """
    def __init__(self, _r):
        self.data = _r.response
        self.eval = False
        self.response_type = _r.__class__.__name__
        
    def safe_eval(self, _obj=dict):
        """Only eval a response if self.data is an instance of _obj"""
        if isinstance(self.data, _obj):
            self.data = eval(self.data)
            self.eval = True
        else:
            warnings.warn("Response is not an instance of %s" % _obj,
                            RuntimeWarning)

class SearchAPIResponse(WorldCatResponse):
    """response.SearchAPIResponse: Response class for WorldCat Search API"""
    def __init__(self, _r=None):
        WorldCatResponse.__init__(self, _r)
        self.response_format = 'xml'
        if self.response_type == 'HoldingsRequest':
            self.record_format = 'iso20775'
        elif self.response_type in ('OpenSearchRequest', 'CitationRequest'):
            if self.response_type == 'CitationRequest':
                self.response_format = 'html'
            elif 'format' in _r.args:
                self.record_format =_r.args['format']
            else:
                self.record_format = 'atom'
        elif self.response_type in ('BibRequest', 'SRURequest'):
            self.record_format = 'marcxml'
            if 'recordSchema' in _r.args:
                if _r.args['recordSchema'] == 'info:srw/schema/1/dc':
                    self.record_format = 'dc'

class xIDResponse(WorldCatResponse):
    """response.xIDResponse: Response class for xID APIS (xISBN/XISSN)
    
    xIDRequests can specify Python objects as a response format. The 
    xIDRequest constructor method does a sanity check on the response before
    evaling it into a Python object so arbitrary code is not run.
    """
    def __init__(self, _r=None):
        """docstring for __init__"""
        WorldCatResponse.__init__(self, _r)
        self.response_format = _r.args['format']
        self.method = _r.args['method']
        if (self.response_format == 'python'):
            self.safe_eval()
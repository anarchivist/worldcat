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

# response/xid.py - Response objects for xID API requests

from worldcat.response import WorldCatResponse

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
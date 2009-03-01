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

# response/__init__.py - Contains response objects for WorldCat API requests

import warnings
import worldcat.util.safeeval


class WorldCatResponse(object):
    """response.WorldCatResponse: Base class for responses from WorldCat APIs

    """

    def __init__(self, _r):
        """Constructor for WorldCatResponses"""
        self.data = _r.response
        self.eval = False
        self.response_type = _r.__class__.__name__

    def safe_eval(self):
        """Only eval a response if self.data is an instance of _obj"""
        try:
            self.data = worldcat.util.safeeval.const_eval(self.data)
            self.eval = True
        except:
            warnings.warn("Response does not eval safely", RuntimeWarning)

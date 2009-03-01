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

# response/registry.py - Response objects for WorldCat Registry requests

from worldcat.response import WorldCatResponse


class RegistryResponse(WorldCatResponse):
    """response.registry.RegistryResponse: Response class for Registry data"""

    def __init__(self, _r=None):
        """Constructor for xIDResponses"""
        WorldCatResponse.__init__(self, _r)
        self.response_format = 'xml'
        self.record_format = 'registry'
        self.service_label = _r.args['serviceLabel']

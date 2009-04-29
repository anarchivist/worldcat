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

# response/search.py - Response objects for WorldCat Search API requests

from worldcat.response import WorldCatResponse
from worldcat.util.extract import extract_elements


class SearchAPIResponse(WorldCatResponse):
    """response.search.SearchAPIResponse: WorldCat Search API response class

    """

    def __init__(self, _r=None):
        """Constructor for SearchAPIResponses"""
        WorldCatResponse.__init__(self, _r)
        self.response_format = 'xml'
        if self.response_type == 'LibrariesRequest':
            self.record_format = 'iso20775'
        elif self.response_type in ('OpenSearchRequest', 'CitationRequest'):
            if self.response_type == 'CitationRequest':
                self.response_format = 'html'
            elif 'format' in _r.args:
                self.record_format = _r.args['format']
            else:
                self.record_format = 'atom'
        elif self.response_type in ('BibRequest', 'SRURequest'):
            self.record_format = 'marcxml'
            if 'recordSchema' in _r.args:
                if _r.args['recordSchema'] in \
                    ['info:srw/schema/1/dc', 'info:srw/schema/1/dc-v1.1']:
                    self.record_format = 'dc'

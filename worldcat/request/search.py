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

# request/search.py -- Request objects for WorldCat Search API

import urllib2
from exceptions import StopIteration

from worldcat.exceptions import APIKeyError, APIKeyNotSpecifiedError, \
                                EmptyQueryError, EmptyRecordNumberError, \
                                InvalidArgumentError, ExtractError
from worldcat.request import WorldCatRequest
from worldcat.response.search import SearchAPIResponse
from worldcat.util.extract import extract_elements


class SearchAPIRequest(WorldCatRequest):
    """request.search.SearchAPIRequest: base class for all search API requests

    SearchAPIRequests require an API key when an instance is created. This is
    done by passing the 'wskey' kwarg. E.g.:

        >>> s = SearchAPIRequest(wskey='...insert your api key here')

    """

    def __init__(self, **kwargs):
        """Constructor for SearchAPIRequest"""
        if 'wskey' not in kwargs:
            raise APIKeyNotSpecifiedError
        WorldCatRequest.__init__(self, **kwargs)
        self._validators = {
            'servicelevel': ('default', 'full'),
            'cformat': ('apa', 'chicago', 'harvard',
                        'mla', 'turabian', 'all'),
            'recordSchema': ('info:srw/schema/1/marcxml-v1.1',
                                'info:srw/schema/1/dc-v1.1'),
            'format': ('atom', 'rss')}

    def get_response(self):
        """Get method for SearchAPIRequests.

        Exception handling is specific to SearchAPIRequests.
        """
        try:
            self.http_get()
        except urllib2.HTTPError, e:
            if e.code == 407:
                raise APIKeyError
            elif e.code == 400:
                raise APIKeyNotSpecifiedError
            else:
                raise
        return SearchAPIResponse(self)


class OpenSearchRequest(SearchAPIRequest):
    """request.search.OpenSearchRequest: queries search API using OpenSearch

    OpenSearchRequests are always keyword searches."""

    def __init__(self, **kwargs):
        """Constructor for OpenSearch requests"""
        SearchAPIRequest.__init__(self, **kwargs)

    def __iter__(self):
        return self

    def api_url(self):
        """API ase URL method for OpenSearchRequests."""
        self.url = 'http://worldcat.org/webservices/catalog/search/opensearch'

    def next(self):
        _i = extract_elements(self.response,
                element='{http://a9.com/-/spec/opensearch/1.1/}startIndex')
        _p = extract_elements(self.response,
                element='{http://a9.com/-/spec/opensearch/1.1/}itemsPerPage')
        _t = extract_elements(self.response,
                element='{http://a9.com/-/spec/opensearch/1.1/}totalResults')
        try:
            if int(_t[0].text) > (int(_i[0].text) + int(_p[0].text)):
                self.args['start'] = int(_i[0].text) + int(_p[0].text)
            else:
                raise StopIteration
        except ValueError:
            raise StopIteration

    def subclass_validator(self, quiet=False):
        """Validator method for OpenSearchRequests."""
        if 'q' not in self.args:
            if quiet == True:
                return False
            else:
                raise EmptyQueryError
        else:
            return True


class SRURequest(SearchAPIRequest):
    """request.search.SRURequest: queries search API using SRU

    SRURequests should be used when fielded searching is desired.
    """

    def __init__(self, **kwargs):
        """Constructor method for SRURequests."""
        SearchAPIRequest.__init__(self, **kwargs)

    def __iter__(self):
        return self

    def api_url(self):
        self.url = 'http://worldcat.org/webservices/catalog/search/sru'

    def next(self):
        _i = extract_elements(self.response,
                element='{http://www.loc.gov/zing/srw/}nextRecordPosition')
        if len(_i) != 0:
            if _i[0].text is not None:
                self.args['startRecord'] = int(_i[0].text)
            else:
                raise StopIteration
        else:
            raise StopIteration

    def subclass_validator(self, quiet=False):
        """Validator method for SRURequests."""
        if 'query' not in self.args:
            if quiet == True:
                return False
            else:
                raise EmptyQueryError
        else:
            return True


class ContentRequest(SearchAPIRequest):
    """request.search.ContentRequest: search API content request metaclass

    ContentRequests are always for an individual record number; they must have
    rec_num as a mandatory parameter when an instance is created.

    """

    def __init__(self, rec_num, **kwargs):
        """Constructor method for ContentRequests."""
        SearchAPIRequest.__init__(self, **kwargs)
        self.rec_num = rec_num

    def subclass_validator(self, quiet=False):
        """Validator method for ContentRequests."""
        if self.rec_num is None:
            if quiet == True:
                return False
            else:
                raise EmptyRecordNumberError
        else:
            return True


class BibRequest(ContentRequest):
    """request.search.BibRequest: retrieves single bibliographic records

    BibRequests only provide SearchAPIResponses where response_format is
    'xml' and record_format is 'marcxml'.

    """

    def __init__(self, rec_num=None, **kwargs):
        """Constructor for BibRequests."""
        ContentRequest.__init__(self, rec_num, **kwargs)

    def api_url(self):
        """Get method for BibRequests."""
        self.url = 'http://worldcat.org/webservices/catalog/content/%s' \
            % self.rec_num


class CitationRequest(ContentRequest):
    """request.search.CitationRequest: retrieves formatted HTML citations

    CitationRequests should always have a SearchAPIResponse where
    response_format is 'html' and record_format is unset.

    TODO: Consider handling citation format."""

    def __init__(self, rec_num=None, **kwargs):
        """Constructor for CitationRequests."""
        ContentRequest.__init__(self, rec_num, **kwargs)

    def api_url(self):
        """Get method for CitationRequests."""
        self.url = \
            'http://worldcat.org/webservices/catalog/content/citations/%s' \
            % self.rec_num


class LibrariesRequest(ContentRequest):
    """request.search.LibrariesRequest: retrieves holdings for a single record

    HoldingsRequests universally going to have a SearchAPIResponse where
    response_format is 'xml' and record_format is 'iso20775'.

    TODO: Add code to allow request w/o recnum to get based on OCLC symbol
    """

    def __init__(self, rec_num=None, num_type='oclc', **kwargs):
        """Constructor for HoldingsRequests."""
        self._nt_validator = {'oclc': '', 'isbn': 'isbn/'}
        self.num_type = num_type
        ContentRequest.__init__(self, rec_num, **kwargs)

    def api_url(self):
        """Get method for HoldingsRequests."""
        self.url = 'http://worldcat.org/webservices/catalog/content/libraries'
        if self.rec_num is not None:
            self.url = '%s/%s%s' \
                % (self.url, self._nt_validator[self.num_type], self.rec_num)

    def subclass_validator(self, quiet=False):
        """Validator method for HoldingsRequests.

        Despite HoldingsRequests being able to handle ISBNs,
        HoldingsRequest.validate() does not validate ISBNS."""
        if self.num_type not in self._nt_validator:
            if quiet == True:
                return False
            else:
                raise InvalidNumberTypeError
        else:
            return True

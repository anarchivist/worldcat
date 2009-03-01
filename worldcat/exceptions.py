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

# exceptions.py - Errors for WorldCat API module

class ExtractError(Exception):
    """exceptions.ExtractError: Exceptions for worldcat.util.extract
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class WorldCatAPIError(Exception):
    """exceptions.WorldCatAPIError: Base class for all WorldCat API exceptions

    """
    pass


class APIKeyError(WorldCatAPIError):
    """exceptions.APIKeyError: General API key exception"""

    def __str__(self):
        return "Invalid API key"


class APIKeyNotSpecifiedError(APIKeyError):
    """exceptions.APIKeyNotSpecifiedError: For empty API Key values"""

    def __str__(self):
        return "API key not specified"


class ValidationError(WorldCatAPIError):
    """exceptions.ValidationError: Base class for validation errors"""
    pass


class EmptyQueryError(ValidationError):
    """exceptions.EmptyQueryError: Query exception for null queries

    for OpenSearchRequests and SRURequests."""

    def __str__(self):
        return "Query terms missing"


class EmptyRecordNumberError(ValidationError):
    """exceptions.EmptyRecordNumberError: For unspecified rec_num values

    For BibRequests, CitationRequests, HoldingsRequests, and xIDRequests.

    """

    def __str__(self):
        return "Record number for content request missing"


class InvalidNumberTypeError(ValidationError):
    """exceptions.InvalidNumberTypeError: For invalid number type selections

    For HoldingsRequsts.
    """

    def __str__(self):
        return "Invalid record number type"


class InvalidArgumentError(ValidationError):
    """exceptions.InvalidArgumentError: For invalid arguments

    This relies on the WorldCatRequest._validators dict; see docstring for
    request.WorldCatRequest.__init__ for more information.
    """

    def __init__(self, arg, value):
        self.arg = arg
        self.value = value

    def __str__(self):
        return "API argument '%s' has invalid value '%s'" % (self.arg,
                                                                self.value)

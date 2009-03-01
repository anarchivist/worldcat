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
# along with wo.  If not, see <http://www.gnu.org/licenses/>.

# request/__init__.py - Base request classes for WorldCat APIs

import urllib
import urllib2
from worldcat.exceptions import APIKeyError, APIKeyNotSpecifiedError, \
                         EmptyQueryError, EmptyRecordNumberError, \
                         InvalidArgumentError, InvalidNumberTypeError
from worldcat.response import WorldCatResponse


class WorldCatRequest(object):
    """request.WorldCatRequest: base class for all requests to WorldCat APIs
    """

    def __init__(self, **kwargs):
        """Constructor method for WorldCatRequests.

        Subclasses should pass kwargs and set their subclass-specific
        _validators from their __init__ methods, e.g.:

            class WCSubClass(WorldCatRequest):
                def __init__(self, **kwargs):
                    WorldCatRequest.__init__(self, **kwargs)
                    self._validators = {'breakfast': ('spam', 'ham', 'eggs')}

        """
        self.args = kwargs
        self._validators = {}

    def api_url(self):
        """Dummy method to set API URL; should be overridden by subclasses."""
        pass

    def get_response(self):
        """Dummy method to get response; should be overrriden by subclasses.

        Subclass get_response methods should override this method in part as
        they should return the relevant subclass of WorldCatResponse.
        """
        self.http_get()
        return WorldCatResponse(self)

    def http_get(self):
        """HTTP Get method for all WorldCatRequests."""
        self.api_url()
        _query_url = '%s?%s' % (self.url, urllib.urlencode(self.args))
        self.response = urllib2.urlopen(_query_url).read()

    def subclass_validator(self, quiet):
        """Dummy validator method; should be overriden by subclasses.

        Subclasses should use the subclass_validator method to perform
        any validation that doesn't rely on the _validators dict object, e.g.:

        class WCSubClass(WorldCatRequest):
            def __init__ ...
            def validate(self):
                if 'argument' not in self.args:
                    raise MissingArgException
                elif self.args['argument'] == 'quux':
                    raise QuuxException
        """
        pass

    def validate(self, quiet=False):
        """Validate arguments using a dict of valid values for each argument.

           Validators are specified as dicts with arguments as keys,
           associated with tuples of valid values.

           The validate method should be called before the get_response
           method.

        """
        subvalid = self.subclass_validator(quiet)
        for key in self._validators:
            if key in self.args:
                if (self.args[key] in self._validators[key]):
                    pass
                elif quiet == True:
                    return False
                else:
                    raise InvalidArgumentError(key, self.args[key])
            else:
                pass

        if quiet == True:
            if subvalid == True:
                return True
            else:
                return False
        else:
            pass

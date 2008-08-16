"request.py - Request classes for WorldCat API module"

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
        """Dummy method to get response; should be overrriden by subclasses"""
        self.http_get()
        return WorldCatResponse(self)
        
    def http_get(self):
        """HTTP Get method for all WorldCatRequests.
        
        Should be called by as separate get method."""
        self.api_url()
        _query_url = '%s?%s' % (self.url, urllib.urlencode(self.args))
        self.response = urllib2.urlopen(_query_url).read()
        
    def subclass_validator(self, quiet):
        """Dummy validator method; should be overriden by subclasses."""
        pass
        
    def validate(self, quiet=False):
        """Validate arguments using a dict of valid values for each argument.

           Validators are specified as dicts with arguments as keys,
           associated with tuples of valid values.
           
           Validator methods should be called before get methods.
           
           Subclasses should perform any non-dict validation before passing
           off to WorldCatRequest.validate(), e.g.:
           
            class WCSubClass(WorldCatRequest):
                def __init__ ...
                def get ...
                def validate(self):
                    if 'argument' not in self.args:
                        raise MissingArgException
                    elif self.args['argument'] != 'quux':
                        raise NonQuuxException
                    else:
                        WorldCatRequest.validate(self)
        
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
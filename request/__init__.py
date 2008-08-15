"request.py - Request classes for WorldCat API module"

import urllib
import urllib2
from worldcat.exceptions import APIKeyError, APIKeyNotSpecifiedError, \
                         EmptyQueryError, EmptyRecordNumberError, \
                         InvalidArgumentError, InvalidNumberTypeError
                         
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
        
    def get(self):
        """Get method for all WorldCatRequests.
        
        Subclasses should set the base API URL before passing self onto
        WorldCatRequest.get():
        
            class WCSubClass(WorldCatRequest):
                def __init__ ...
                def get(self):
                    self.url = 'http://api.stuff.oclc.org/foo/bar'
                    return WorldCatRequest.get(self)
                    
        """
        _query_url = '%s?%s' % (self.url, urllib.urlencode(self.args))
        self.response = urllib2.urlopen(_query_url).read()
        
    def validate(self, quiet):
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
            return True
        else:
            pass
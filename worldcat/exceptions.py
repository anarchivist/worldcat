"exceptions.py - Errors for WorldCat API module"

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
        return "API argument '%s' has invalid value '%s'" % (self.arg, self.value)
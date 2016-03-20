# directory-wide and shared processes
import logging
from functools import wraps

# initiates logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# http://stackoverflow.com/a/6307868/4013571
def wrap_all(decorator):
    """wraps all function with the wrapper provided as an argument"""
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

def log_me(func):
    """Adds a logging facility to all functions it wraps"""
    @wraps(func)
    def tmp(*args, **kwargs):
        func_name = func.__name__
        if func_name != '__init__':
            args[0].logger.debug('...running {}'.format(func_name))
        return func(*args, **kwargs)
    return tmp
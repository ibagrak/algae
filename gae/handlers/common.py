import logging
import cgi
import sys
import traceback

from google.appengine.ext import webapp
from sessions import get_current_session
import settings
import model

def withsession(func):
    def wrapper(*args, **kwargs):
        kwargs['session'] = get_current_session()
        res = func(*args, **kwargs)
        return res
    
    return wrapper

def withuser(func):
    def wrapper(*args, **kwargs):
        if 'session' in kwargs:
            kwargs['user'] = model.User.get_user_from_session(kwargs['session'].sid)
        else:
            session = get_current_session()
            kwargs['user'] = model.User.get_user_from_session(session.sid)
        
        args[0].logger.debug("session object: \n %s" % session)    
        res = func(*args, **kwargs)
        return res
    
    return wrapper

def logapi(func):
    def wrapper(*args, **kwargs):
        args[0].logger.debug("API: %s args: %s" % (func.__name__, args))
        res = func(*args, **kwargs)
        args[0].logger.debug("API: %s result: %s" % (func.__name__, res))
        return res
    
    return wrapper

def loghandler(func):
    def wrapper(*args, **kwargs):
        args[0].logger.debug("API: %s args: %s" % (func.__name__, args))
        res = func(*args, **kwargs)
        return res
    
    return wrapper
                
class AbstractRequestHandler(webapp.RequestHandler):
    def __init__(self):
        super(AbstractRequestHandler, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
    
    # if we don't have this then spammy head requests would clutter the error log
    def head(self, *args):
        pass
        
    def handle_exception(self, exception, debug_mode):    
        self.logger.exception(exception)
        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            self.response.clear()
            self.response.out.write('<pre>%s</pre>' % (cgi.escape(lines, quote=True)))
        else:
            self.redirect(settings.ERROR_URL)
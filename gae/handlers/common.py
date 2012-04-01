import logging
import cgi
import sys
import traceback
from functools import wraps

import webapp2
from webapp2_extras import sessions

import settings

def logapi(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("API call: %s args: %s kwargs: %s" % (func.__name__, args[1:], kwargs))
        res = func(*args, **kwargs)
        logging.debug("API call: %s result: %s" % (func.__name__, res))
        return res
    
    return wrapper

def loghandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("HTML Request: %s args: %s kwargs: %s" % (func.__name__, args[1:], kwargs))
        res = func(*args, **kwargs)
        return res
    
    return wrapper
                
class BaseHandler(webapp2.RequestHandler):
    # if we don't have this then spammy head requests would clutter the error log
    def head(self):
        pass
        
    def handle_exception(self, exception, debug_mode):    
        logging.exception(exception)
        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            self.response.clear()
            self.response.out.write('<pre>%s</pre>' % (cgi.escape(lines, quote=True)))
        else:
            self.redirect(settings.ERROR_URL)
            
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
    def session_init(self):
        # initialize default cookie values
        for k,v in settings.cookie: 
            self.session[k] = v
    
    def session_inc_pageviews(self):
        self.session.session['pageviews'] = self.session['pageviews'] + 1
    
    def session_login(self):
        self.session['authed'] = True
    
    def session_logout(self):
        self.session['authed'] = False
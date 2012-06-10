import logging
import cgi
import sys
import traceback
import hashlib
import os
from functools import wraps

import webapp2
from webapp2_extras import sessions, json

import settings
import model

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
            self.response.write('<pre>%s</pre>' % (cgi.escape(lines, quote=True)))
        else:
            self.redirect(settings.ERROR_PATH)
            
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
        for k, v in settings.cookie: 
            self.session[k] = v
        
        # initialize random session ID
        self.session['id'] = hashlib.md5(os.urandom(16)).hexdigest()
        
    def session_regenerate_id(self):
        self.session['id'] = hashlib.md5(os.urandom(16)).hexdigest()
        
    def session_inc_pageviews(self):
        self.session['pageviews'] = self.session['pageviews'] + 1
    
    def session_login(self):
        self.session['authed'] = True
    
    def session_logout(self):
        self.session['authed'] = False

class BaseAPIHandler(BaseHandler):
    
    def handle_exception(self, exception, debug_mode):
        # Log the error.
        logging.exception(exception)

        # Set a custom message.
        self.response.write('An error occurred.')

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)
            
        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            result = ({'code': settings.GENERAL_ERROR, 'message': lines}) 
        else:
            result = ({'code': settings.GENERAL_ERROR, 'message': 'Please contact application administrator for support'})
            
        self.response.clear()
        self.response.write(json.encode(result))
        
    def get(self, *args):
        action = self.request.get('action')
        args = self.request.GET.to_dict()
        args.remove('action')
        
        kvs = {}
        kvs['user'] = model.User.get_user_from_session(self.session['id'])
        for arg in args:
            kvs[arg] = self.request.get(arg)
        
        if not action in settings.APIS:
            result = ({'code': settings.INVALID_API_ERROR, 'message': 'Unsupported API action'})
        else:    
            result = getattr(self, action)(**kvs)
        
        self.response.clear()
        self.response.write(json.encode(result))

    def put(self):
        pass
    
    def post(self):
        pass
    
    def delete(self):
        pass
    
class BaseRESTHandler(BaseAPIHandler):
        
    def get(self, obj_t, identifier, *args):
        cls = getattr(sys.modules['model'], obj_t)
        obj = cls.get(identifier)
        return json.encode(obj)
    
    def put(self, obj_t, identifier, *args):
        kvs = json.decode(self.request.body)
        cls = getattr(sys.modules['model'], obj_t, kvs)
        obj = cls.put(identifier)
        return json.encode(obj)
    
    def post(self, obj_t, identifier, *args):
        kvs = json.decode(self.request.body)
        cls = getattr(sys.modules['model'], obj_t, kvs)
        obj = cls.post(identifier)
        return json.encode(obj)
    
    def delete(self, obj_t, identifier, *args):
        cls = getattr(sys.modules['model'], obj_t)
        obj = cls.delete(identifier)
        return json.encode(obj)
    

    
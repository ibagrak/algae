import logging
import cgi
import sys
import traceback
import hashlib
import os


from functools import wraps

import webapp2

from webapp2_extras import sessions, json, auth
from jinja2.runtime import TemplateNotFound

import settings
import model
import utils
from handlers import jinja_environment

def get_json_error(code, key = None, message = None, *args):
    logging.info(json.encode(get_error(code, key = key, message = message, *args)))
    return json.encode(get_error(code, key = key, message = message, *args))

def get_error(code, key = None, message = None, *args):
    if message:
        return {'code' : code, 'message' : message}
    elif key: 
        return {'code' : code, 'message' : settings.API_CODES[code][key]}
    else:
        return {'code' : code, 'message' : settings.API_CODES[code]}

def with_login(func):
    def _with_login(*args, **kwargs):
        self = args[0]
        if not self.logged_in and issubclass(args[0].__class__, BaseAPIHandler):
            return args[0].prep_json_response(401)
        elif not args[0].logged_in and issubclass(args[0].__class__, BaseHandler):
            return args[0].prep_html_response("generic_error.html", { 'code' : 401 })

        func(*args, **kwargs)
    return _with_login

class BaseHandler(webapp2.RequestHandler):
    # if we don't have this then spammy head requests would clutter the error log
    def head(self):
        pass
        
    def handle_exception(self, exception, debug_mode):    
        logging.exception(exception)
        self.response.clear()

        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            self.response.write('<pre>%s</pre>' % (cgi.escape(lines, quote=True)))
        else:
            # If the exception is a HTTPException, use its error code.
            # Otherwise use a generic 500 error code.
            if isinstance(exception, webapp2.HTTPException):
                code = exception.code
            else:
                code = 500
            
            self.response.set_status(code)
            self.response.out.write(jinja_environment.get_template("generic_error.html").render({'code' : 500}))
            
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
        session = self.session_store.get_session()
        
        if len(session) == 0:
            for k, v in settings.COOKIE_TEMPLATE.iteritems(): 
                session[k] = v
        
            # initialize random session ID
            session['id'] = hashlib.md5(os.urandom(16)).hexdigest()
        # Returns a session using the default cookie key.
        return session
    
    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()
  
    @webapp2.cached_property
    def current_user(self):
        """Returns currently logged in user"""
        user_dict = self.auth.get_user_by_session()
        return self.auth.store.user_model.get_by_id(user_dict['user_id'])
      
    @webapp2.cached_property
    def logged_in(self):
        """Returns true if a user is currently logged in, false otherwise"""
        return self.auth.get_user_by_session() is not None
        
    def session_inc_pageviews(self):
        self.session['pageviews'] = self.session['pageviews'] + 1
    
    def prep_html_response(self, template_name, template_vars={}):
        # Preset values for the template
        values = {
          'url_for'      : self.uri_for,
          'logged_in'    : self.logged_in,
          'current_user' : self.current_user if self.logged_in else None
        }
        
        # Add manually supplied template values
        values.update(template_vars)
        
        logging.info("session: %s" % self.session)
        logging.info("template vars: %s" % values)
        
        try:
            template = jinja_environment.get_template(template_name)
            self.response.out.write(template.render(**values))
        except TemplateNotFound:
            self.abort(404)

class BaseAPIHandler(BaseHandler):

    def handle_exception(self, exception, debug_mode):
        # Log the error.
        logging.exception(exception)

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)
            
        if debug_mode:
            lines = ''.join(traceback.format_exception(*sys.exc_info()))
            result = get_error(500, message = lines) 
        else:
            result = get_error(500, key = 'admin_required') 
            
        self.response.clear()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(result))
        
    def get(self, *args):
        action = self.request.get('action')
        args = self.request.GET
        
        args['user'] = model.User.get_user_from_session(self.session['id'])
        for arg in args:
            args[arg] = self.request.get(arg)
        
        if not 'action' in args or not args['action'] in settings.APIS:
            result = get_error(400, key = 'unsupported')
        else:    
            result = getattr(self, action)(args)
        
        self.response.clear()
        self.response.set_status(result['code'])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(result))

    def put(self):
        pass
    
    def post(self):
        pass
    
    def delete(self):
        pass
    
    def prep_json_response(self, code, key = None, message = None, *args):
        self.response.set_status(code)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(get_json_error(code, key = key, message = message, *args))

class BaseRESTHandler(BaseAPIHandler):
    
    @with_login
    def put(self, obj_t, *args):
        kvs = json.decode(self.request.body)
        
        # find model class
        cls = getattr(sys.modules['model'], obj_t)
        
        # dispatch put to that model class. all model classes need to a subclass model.RESTModel
        obj = utils.to_dict(cls.put(kvs))
        
        return self.prep_json_response(200, message = obj)

    def get(self, obj_t, identifier, *args):
        cls = getattr(sys.modules['model'], obj_t)
        
        # dispatch put to that model class. all model classes need to a subclass model.RESTModel
        obj = utils.to_dict(cls.get(int(identifier)))
        
        return self.prep_json_response(200, message = obj)

    def post(self, obj_t, identifier, *args):
        logging.error("post contents: %s", self.request.body)
        kvs = json.decode(self.request.body)

        # find model class
        cls = getattr(sys.modules['model'], obj_t)

        obj = utils.to_dict(cls.post(int(identifier), kvs))

        return self.prep_json_response(200, message = obj)
    
    @with_login
    def delete(self, obj_t, identifier, *args):
        cls = getattr(sys.modules['model'], obj_t)
        obj = cls.delete1(int(identifier))
        return self.prep_json_response(200, message = json.encode(obj))
    
def handle_404(request, response, exception):
    response.set_status(404)
    response.out.write(jinja_environment.get_template("404.html").render({'code' : 404}))

def handle_500(request, response, exception): 
    response.set_status(500)
    response.out.write(jinja_environment.get_template("generic_error.html").render({'code' : 500}))
    

    
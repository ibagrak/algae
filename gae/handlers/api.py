from google.appengine.ext import ndb

import settings
from core import model
import common

class RPCHandler(common.BaseAPIHandler):
    
    def get(self, action, *args):
        args = self.request.GET
        
        for arg in args:
            args[arg] = self.request.get(arg)
        
        if not action in settings.APIS:
            self.prep_json_response(400, key = 'unsupported')
        else:    
            getattr(self, action)(args)

    def signup_mailing_list(self, args):
    	if 'email' in args:
            if not model.EmailAddr.query().filter(model.EmailAddr.email == args['email']).get():
                model.EmailAddr(email = args['email']).put()
                
            self.prep_json_response(200, message = "Thanks for signing up!")
    	else:
    		self.prep_json_response(400, key = "noemail")

    @common.with_login
    def change_email_addr(self, args):
    	if 'email' in args: 
    		self.current_user.email = args['email']
    		self.current_user.put()

    		self.prep_json_response(200, message = "Email updated!")
    	else:
    		self.prep_json_response(400, key = "noemail")

class RESTHandler(common.BaseRESTHandler):
	
	def get(self, *args, **kwargs):
		pass

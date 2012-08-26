import json
import settings

from core import model
import common

class RPCHandler(common.BaseAPIHandler):
    
    def get(self, *args):
        action = self.request.get('action')
        args = self.request.GET
        
        args['user'] = model.User.get_user_from_session(self.session['id'])
        for arg in args:
            args[arg] = self.request.get(arg)
        
        if not 'action' in args or not args['action'] in settings.APIS:
            result = common.get_error(400, key = 'unsupported')
        else:    
            result = getattr(self, action)(args)
        
        self.response.clear()
        self.response.set_status(result['code'])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(result))

    def signup_mailing_list(self, args):
    	if 'email' in args:
			model.EmailAddr(email = args['email']).put()
			return self.get_error(200, message = "Thanks for signing up!")
    	else:
    		return self.get_error(400, key = "noemail")

    @common.with_login
    def change_email_addr(self, args):
    	if 'email' in args: 
    		self.current_user.email = args['email']
    		self.current_user.put()

    		return self.get_error(200, message = "Email updated!")
    	else:
    		return self.get_error(400, key = "noemail")

class RESTHandler(common.BaseRESTHandler):
	
	def get(self, *args, **kwargs):
		pass

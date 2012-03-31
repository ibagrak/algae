import os
from google.appengine.ext.webapp import template

import common
            
class Index(common.AbstractRequestHandler):
    
    @common.loghandler
    @common.withuser
    def get(self, *args, **kwargs):
        self.logger.debug("hello, world!")
        
        t_args = { 'user' : kwargs['user'] }
        path = os.path.join(os.path.dirname(__file__), "../static/templates/index.html")
        self.response.out.write(template.render(path, t_args))
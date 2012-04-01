import os

from handlers import jinja_environment
import common
import logging
            
class Index(common.BaseHandler):
    
    def get(self, *args, **kwargs):
        logging.debug("hello, world!")
        logging.debug("session: %s" % self.session)
        
        t_args = { 'session' : self.session}
        path = os.path.join(os.path.dirname(__file__), "../static/templates/index.html")
        logging.error("path: %s" % path)
        
        template = jinja_environment.get_template("index.html")
        self.response.out.write(template.render(t_args))
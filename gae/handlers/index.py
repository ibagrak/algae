import os

from handlers import jinja_environment
import common
import logging
            
class Index(common.BaseHandler):
    
    def get(self, *args, **kwargs):
        logging.debug("hello, world!")
        logging.debug("session: %s" % self.session)
        
        self.session_inc_pageviews()
        
        t_args = { 'pageviews' : self.session['pageviews']}
        
        template = jinja_environment.get_template("index.html")
        self.response.out.write(template.render(t_args))

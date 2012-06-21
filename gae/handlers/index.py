import common
import logging
            
class Index(common.BaseHandler):
    
    def get(self):
        logging.info("hello, world!")

        # demonstrates how session state can be changed        
        self.session_inc_pageviews()
        
        self.prep_html_response('index.html', { 'pageviews' : self.session['pageviews']})

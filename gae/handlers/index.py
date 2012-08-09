import common
import logging
import model

from google.appengine.ext import db

class Index(common.BaseHandler):
    
    def get(self):
        logging.info("hello, world!")

        # demonstrates how session state can be changed        
        self.session_inc_pageviews()
        
        self.prep_html_response('index.html', 
                                { 'pageviews' : self.session['pageviews'], 
                                                'widgets' : db.Query(model.Widget).order('-__key__').fetch(5), 
                                                'form' : model.generate_model_form(model.Widget)})
        


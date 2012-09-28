import common
import logging
from core import model

from google.appengine.ext import ndb

class Index(common.BaseHandler):
    
    def get(self):
        # demonstrates how session state can be changed        
        self.session_inc_pageviews()
        
        self.prep_html_response('index.html', 
                                { 'pageviews' : self.session['pageviews'], 
                                'widgets' : model.Widget.query().order(-model.Widget._key).fetch(5),
                                'form' : model.generate_model_form(model.Widget)})


class WithLogin(common.BaseHandler):
	@common.with_login
	def get(self):
		self.prep_html_response('index.html', 
                                { 'pageviews' : self.session['pageviews'], 
                                'widgets' : model.Widget.query().order(-model.Widget._key).fetch(5),
                                'form' : model.generate_model_form(model.Widget)})

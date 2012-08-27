import webapp2
import webtest
import unittest2
import copy
import urllib
import logging

from google.appengine.ext import testbed
from google.appengine.ext import db
from webapp2_extras import json
from webapp2_extras.appengine.auth import models as users

import app
import settings
import handlers
from core import model

class RESTTest(unittest2.TestCase):
	str_widget = '{"int_field":1,"email_field":"i@co.co","boolean_field":true,"date_field":"12-02-2012","text_field":"daf","id":2,"string_field":"dfa","link_field":"http://i.co"}'
	json_widget = json.decode(str_widget)

	faux_db_user = {'email' : 'ibagrak@hotmail.com', 
					'password_raw' : 'blah', 
					'pic' : 'http://www.gravatar.com/avatar/759e5b31901d7d20a106f7f8f60a9383?d=http%3A//green-algae.appspot.com/img/algae.png', 
					'profile' : 'mailto:ibagrak@hotmail.com', 
					'username' : 'ilya' }
	
	def signin_faux_user(self):
		users.User.create_user('own:ibagrak@hotmail.com', **self.faux_db_user)

		response = self.testapp.get('/email-signin?action=signin_email&email=%s&password=%s' % (self.faux_db_user['email'], self.faux_db_user['password_raw']))
		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'application/json')

	def setUp(self):
		# Create a WSGI application.
		application = webapp2.WSGIApplication(app.routes, debug = True, config = settings.app_config)
		application.error_handlers[404] = handlers.common.handle_404
		application.error_handlers[500] = handlers.common.handle_500
	
		# Wrap the app with WebTest's TestApp.
		self.testapp = webtest.TestApp(application)

		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()

		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()

		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def tearDown(self):
		self.testbed.deactivate()

	# test the handler.
	def test_handler_smoke(self):
		response = self.testapp.get('/')
		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'text/html')

	# test common.BaseRESTHandler APIs
	def test_put_unauth(self):
		response = self.testapp.put('/rest/Widgets', 
				params = self.str_widget, 
				expect_errors=True, 
				content_type = "application/json; charset=utf-8")
		
		self.assertEqual(response.status_int, 401)
		self.assertEqual(json.decode(response.body)['code'], 401)

	def test_get(self):
		# create widget in DB and get its id
		widget = copy.copy(self.json_widget)
		ident = model.Widget.put(widget).key().id()

		self.assertEqual(1, len(model.Widget.all().fetch(2)))

		# get widget with the same id through API and verify that email field is correct
		response = self.testapp.get('/rest/Widget/' + str(ident), 
				params = self.str_widget, 
				expect_errors=True)
		
		self.assertEqual(response.status_int, 200)
		self.assertEqual(json.decode(response.body)['code'], 200)
		self.assertEqual(json.decode(response.body)['message']['email_field'], "i@co.co")
	
	def test_post(self):
		# create widget in DB and get its id
		widget = copy.copy(self.json_widget)
		ident = model.Widget.put(widget).key().id()

		self.assertEqual(1, len(model.Widget.all().fetch(2)))

		# update widget with the same id through API
		widget = copy.copy(self.json_widget)
		widget['email_field'] = 'newemail@co.co'
		response = self.testapp.post('/rest/Widget/' + str(ident), 
				params = json.encode(widget), 
				expect_errors=True, 
				content_type = "application/json; charset=utf-8")
		
		self.assertEqual(response.status_int, 200)
		self.assertEqual(json.decode(response.body)['code'], 200)

		# get widget with the same id through API and verify that email field is correct
		response = self.testapp.get('/rest/Widget/' + str(ident), 
				params = self.str_widget, 
				expect_errors=True)
		
		self.assertEqual(response.status_int, 200)
		self.assertEqual(json.decode(response.body)['code'], 200)
		self.assertEqual(json.decode(response.body)['message']['email_field'], "newemail@co.co")

	def test_delete_unauth(self):
		# create widget in DB and get its id
		widget = copy.copy(self.json_widget)
		ident = model.Widget.put(widget).key().id()

		self.assertEqual(1, len(model.Widget.all().fetch(2)))

		response = self.testapp.delete('/rest/Widget/' + str(ident), 
				expect_errors=True)
		
		self.assertEqual(response.status_int, 401)
		self.assertEqual(json.decode(response.body)['code'], 401)

	def test_put_auth(self):
		self.signin_faux_user()

		response = self.testapp.put('/rest/Widgets', 
				params = self.str_widget, 
				expect_errors=True, 
				content_type = "application/json; charset=utf-8")
		
		self.assertEqual(response.status_int, 200)
		self.assertEqual(json.decode(response.body)['code'], 200)

	def test_delete_auth(self):
		self.signin_faux_user()

		# create widget in DB and get its id
		widget = copy.copy(self.json_widget)
		ident = model.Widget.put(widget).key().id()

		self.assertEqual(1, len(model.Widget.all().fetch(2)))

		response = self.testapp.delete('/rest/Widget/' + str(ident), 
				expect_errors=True)
		
		self.assertEqual(response.status_int, 200)
		self.assertEqual(json.decode(response.body)['code'], 200)

class RPCTest(unittest2.TestCase):
	str_widget = '{"int_field":1,"email_field":"i@co.co","boolean_field":true,"date_field":"12-02-2012","text_field":"daf","id":2,"string_field":"dfa","link_field":"http://i.co"}'
	json_widget = json.decode(str_widget)

	faux_db_user = {'email' : 'ibagrak@hotmail.com', 
					'password_raw' : 'blah', 
					'pic' : 'http://www.gravatar.com/avatar/759e5b31901d7d20a106f7f8f60a9383?d=http%3A//green-algae.appspot.com/img/algae.png', 
					'profile' : 'mailto:ibagrak@hotmail.com', 
					'username' : 'ilya' }

	user = None
	def signin_faux_user(self):
		ok, self.user = users.User.create_user('own:ibagrak@hotmail.com', **self.faux_db_user)

		response = self.testapp.get('/email-signin?action=signin_email&email=%s&password=%s' % (self.faux_db_user['email'], self.faux_db_user['password_raw']))
		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'application/json')

	def setUp(self):
		# Create a WSGI application.
		application = webapp2.WSGIApplication(app.routes, debug = True, config = settings.app_config)
		application.error_handlers[404] = handlers.common.handle_404
		application.error_handlers[500] = handlers.common.handle_500
	
		# Wrap the app with WebTest's TestApp.
		self.testapp = webtest.TestApp(application)

		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()

		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()

		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def test_mailing_list(self):
		response = self.testapp.get('/rpc/signup_mailing_list?email=%s' % urllib.quote('ibagrak@hotmail.com'))
		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'application/json')

		self.assertNotEqual(None, db.Query(model.EmailAddr).filter('email =', 'ibagrak@hotmail.com').get())

	def test_update_email_noauth(self):
		response = self.testapp.get('/rpc/change_email_addr?email=%s' % urllib.quote('ibagrak@hotmail.com'), expect_errors=True)
		self.assertEqual(response.status_int, 401)
		self.assertEqual(response.content_type, 'application/json')

	def test_update_email_auth(self):
		self.signin_faux_user()

		response = self.testapp.get('/rpc/change_email_addr?email=%s' % urllib.quote('ibagrak@hotmail.com'))
		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.content_type, 'application/json')

		self.assertEqual(self.user.email, 'ibagrak@hotmail.com')




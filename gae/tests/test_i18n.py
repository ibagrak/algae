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
import re
from core import model

class I18NTest(unittest2.TestCase):
	# Language-Accept: header values for tests
	hdr_english_accept = {'Accept-Language': 'en'}
	hdr_other_accept   = {'Accept-Language': 'da, fr'}
	hdr_german_accept  = {'Accept-Language': 'de'}
	hdr_english_prefer = {'Accept-Language': 'en, de'}
	hdr_german_prefer  = {'Accept-Language': 'de, en'}

	# text to check if english response
	txt_in_english = r'was created by'
	txt_in_german  = r'ist ein Werk von'

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

	# test with 'only english'
	def test_english(self):
		response = self.testapp.get('/', headers=self.hdr_english_accept)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_english, response.body)
		self.assertNotIn(self.txt_in_german, response.body)

	# test with 'only german'
	def test_german(self):
		response = self.testapp.get('/', headers=self.hdr_german_accept)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_german, response.body)
		self.assertNotIn(self.txt_in_english, response.body)

	# test with 'english preferred'
	def test_english_preferred(self):
		response = self.testapp.get('/', headers=self.hdr_english_prefer)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_english, response.body)
		self.assertNotIn(self.txt_in_german, response.body)

	# test with 'german preferred'
	def test_german(self):
		response = self.testapp.get('/', headers=self.hdr_german_prefer)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_german, response.body)
		self.assertNotIn(self.txt_in_english, response.body)

	# test with 'other'
	def test_other(self):
		response = self.testapp.get('/', headers=self.hdr_other_accept)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_english, response.body)
		self.assertNotIn(self.txt_in_german, response.body)

	# test with 'english', then request german
	def test_german_explicit(self):
		response = self.testapp.get('/', headers=self.hdr_english_accept)
		response = self.testapp.get('/locale/de_DE', headers=self.hdr_english_accept)
		self.assertEqual(response.status_int, 302)
		response = self.testapp.get('/', headers=self.hdr_english_accept)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_german, response.body)
		self.assertNotIn(self.txt_in_english, response.body)

	# test with 'german', then request english
	def test_english_explicit(self):
		response = self.testapp.get('/', headers=self.hdr_german_accept)
		response = self.testapp.get('/locale/en_US', headers=self.hdr_german_accept)
		self.assertEqual(response.status_int, 302)
		response = self.testapp.get('/', headers=self.hdr_german_accept)
		self.assertEqual(response.status_int, 200)
		self.assertIn(self.txt_in_english, response.body)
		self.assertNotIn(self.txt_in_german, response.body)

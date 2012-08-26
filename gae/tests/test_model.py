import unittest2
import copy

from google.appengine.ext import testbed
from webapp2_extras import json

from core import model

class ModelTestCase(unittest2.TestCase):

	fixture_widget = json.decode('{"int_field":1,"email_field":"i@co.co","boolean_field":true,"date_field":"12-02-2012","text_field":"daf","id":2,"string_field":"dfa","link_field":"http://i.co"}')

	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()

		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()

		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def test_create(self):
		widget = copy.copy(self.fixture_widget)
		model.Widget.put(widget)

		self.assertEqual(1, len(model.Widget.all().fetch(2)))

	def test_read(self):
		widget = copy.copy(self.fixture_widget)
		widget['int_field'] = 123

		entity = model.Widget.put(widget)
		
		self.assertNotEqual(None, entity)

		entity = model.Widget.get(entity.key().id())
		self.assertEqual(entity.int_field, 123)

	def test_update(self):
		widget = copy.copy(self.fixture_widget)
		identifier = model.Widget.put(widget).key().id()

		widget = copy.copy(self.fixture_widget)
		widget['int_field'] = 234
		widget['email_field'] = 'ibagrak@co.co'
		widget['boolean_field'] = False

		entity = model.Widget.post(identifier, widget)
		self.assertEqual(entity.int_field, 234)
		self.assertEqual(entity.email_field, 'ibagrak@co.co')
		self.assertEqual(entity.boolean_field, False)

	def test_delete(self):
		widget = copy.copy(self.fixture_widget)
		identifier = model.Widget.put(widget).key().id()

		self.assertEqual(model.Widget.delete1(identifier), True)

		self.assertEqual(0, len(model.Widget.all().fetch(2)))
		
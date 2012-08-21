import unittest

from google.appengine.ext import testbed

from core import model

class ModelTestCase(unittest.TestCase):

	fixture_widget = {"int_field":1,"email_field":"i@co.co","boolean_field":True,"date_field":"12-02-2012","text_field":"daf","id":2,"string_field":"dfa","link_field":"http://i.co"}

	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()

		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()

		self.testbed.setup_env(app_id='green-algae')

		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def test_create(self):
		model.Widget.put(self.fixture_widget)

		self.assertEqual(1, len(model.Widget.all().fetch(2)))

	def test_read(self):
		pass

	def test_update(self):
		pass

	def test_delete(self):
		pass


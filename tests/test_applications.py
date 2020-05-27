from .__meta__ import *
from tracer.resources.applications import Applications, Application
from tracer.resources.collections import ApplicationsCollection, ProcessesCollection

try:
	from unittest.mock import patch
except:
	from mock import patch


class TestApplications(unittest.TestCase):

	def test_apps_types(self):
		self.assertIsInstance(Applications.all(), ApplicationsCollection)

	def test_application_processes(self):
		application = Applications.all()[0]
		self.assertIsInstance(application.instances, ProcessesCollection)

	def test_apps_attributes(self):
		i = 1
		for a in Applications.all():
			if ("name" not in a) or len(a) <= 1:
				self.fail("Missing name in definition #" + str(i))

			if "type" in a and a.type not in Applications.TYPES.values():
				self.fail("Unknown type in application: " + a.type)

			n = 6 if "rename" in a else 5
			self.assertEqual(len(a), n, "Application {0} has unsupported attribute".format(a.name))

			i += 1

	def test_apps_duplicity(self):
		apps = Applications.all()
		for a in apps:
			if self._count(a.name, apps) > 1:
				self.fail("Duplicate definitions for: " + a.name)

	@patch('tracer.resources.applications.System.init_system', return_value="dummy")
	def test_app_with_no_definition(self, init_system):
		app_name = "NON_EXISTING_APPLICATION"
		app = Applications.find(app_name)
		self.assertEquals(app.name, app_name)
		self.assertEqual(app.type, Applications.DEFAULT_TYPE)
		self.assertEqual(app.helper, None)
		self.assertEqual(app.note, None)
		self.assertEqual(len(app), 5, "Application {0} has unsupported attribute".format(app.name))

	def test_representations(self):
		rule = Application({"name": "foo"})
		self.assertEquals(str(rule), "<Application: foo>")
		self.assertEquals(repr(rule), "<Application: foo>")

	def test_contains_name(self):
		a1 = Application({"name": "foo", "type": "applicaiton", "helper": "some helper"})
		a2 = Application({"name": "foo", "type": "application", "helper": "some helper with {NAME} argument"})
		self.assertFalse(a1.helper_contains_name)
		self.assertTrue(a2.helper_contains_name)

	def test_contains_formating(self):
		a1 = Application({"name": "foo", "type": "applicaiton", "helper": "some helper"})
		a3 = Application({"name": "foo", "type": "application", "helper": "some helper with {FOO} argument"})
		self.assertFalse(a1.helper_contains_formating)
		self.assertTrue(a3.helper_contains_formating)

	def test_helper_contains_when_none(self):
		a1 = Application({"name": "foo", "type": "applicaiton", "helper": None})
		self.assertFalse(a1.helper_contains_formating)
		self.assertFalse(a1.helper_contains_name)

	def _count(self, app_name, apps):
		count = 0
		for a in apps:
			if a.name == app_name:
				count += 1
		return count


if __name__ == '__main__':
	unittest.main()

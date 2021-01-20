from .__meta__ import *
from tracer.paths import DATA_DIR
from tracer.resources.applications import Applications, Application
from tracer.resources.collections import ApplicationsCollection, ProcessesCollection

try:
	from unittest.mock import patch, mock_open
	builtins_open = "builtins.open"
except:
	from mock import patch, mock_open
	builtins_open = "__builtin__.open"


class TestApplications(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.DEFINITIONS = [x for x in Applications.DEFINITIONS
						   if x.startswith(DATA_DIR)]

	def setUp(self):
		Applications.DEFINITIONS = self.DEFINITIONS
		Applications._apps = None

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
		self.assertEqual(app.name, app_name)
		self.assertEqual(app.type, Applications.DEFAULT_TYPE)
		self.assertEqual(app.helper, None)
		self.assertEqual(app.note, None)
		self.assertEqual(len(app), 5, "Application {0} has unsupported attribute".format(app.name))

	def test_representations(self):
		rule = Application({"name": "foo"})
		self.assertEqual(str(rule), "<Application: foo>")
		self.assertEqual(repr(rule), "<Application: foo>")

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

	@patch("tracer.resources.system.System.init_system", return_value="systemd")
	def test_load(self, _init_system):
		"""
		Test parsing a single XML file with applications
		"""
		Applications.DEFINITIONS = ["whatever-file.xml"]
		data = (
			"<applications>"
			"    <app name='foo' type='daemon' />"
			"    <group type='session'>"
			"        <app name='bar' />"
			"        <app name='baz' helper='Or kill it and see what happens' />"
			"    </group>"
			"</applications>"
		)
		with patch(builtins_open, mock_open(read_data=data)):
			apps = Applications.all()
			self.assertEqual(len(apps), 3)
			self.assertTrue(all([isinstance(x, Application) for x in apps]))
			self.assertEqual(apps[0].name, "foo")
			self.assertTrue(apps[0].helper.endswith("systemctl restart foo"))
			self.assertEqual(apps[2].type, "session")
			self.assertIn("kill it", apps[2].helper)

	def _count(self, app_name, apps):
		count = 0
		for a in apps:
			if a.name == app_name:
				count += 1
		return count


if __name__ == '__main__':
	unittest.main()

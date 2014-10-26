#!/usr/bin/env python

from __meta__ import *
from tracer.resources.applications import Applications, Application
from tracer.resources.collections import ApplicationsCollection, ProcessesCollection

from bs4 import BeautifulSoup
from os.path import dirname, realpath

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

			self.assertEqual(len(a), 4, "Application {0} has unsupported attribute".format(a.name))

			i += 1

	def test_apps_duplicity(self):
		apps = Applications.all()
		for a in apps:
			if self._count(a.name, apps) > 1:
				self.fail("Duplicate definitions for: " + a.name)

	def test_app_with_no_definition(self):
		app_name = "NON_EXISTING_APPLICATION"
		app = Applications.find(app_name)
		self.assertEquals(app.name, app_name)
		self.assertEqual(app.type, Applications.DEFAULT_TYPE)
		self.assertEqual(app.helper, None)
		self.assertEqual(len(app), 4, "Application {0} has unsupported attribute".format(app.name))

	def _count(self, app_name, apps):
		count = 0
		for a in apps:
			if a.name == app_name:
				count += 1
		return count


if __name__ == '__main__':
	unittest.main()


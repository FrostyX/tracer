#!/usr/bin/env python

from __meta__ import *
from resources.applications import Applications

from bs4 import BeautifulSoup
from os.path import dirname, realpath

class TestApplications(unittest.TestCase):

	def test_apps_attributes(self):
		i = 1
		for a in Applications.all():
			if ("name" not in a) or len(a) <= 1:
				self.fail("Missing name in definition #" + str(i))

			if a["type"] and a["type"] not in Applications.TYPES.values():
				self.fail("Unknown type in application: " + a["name"])

			allowed_keys = ["name", "type", "helper", "rename"]
			for key in a.keys():
				self.assertIn(key, allowed_keys,
					"Unsupported attribute '{0}' in application: {1}"
						.format(key, a["name"]))

			i += 1

	def test_apps_duplicity(self):
		apps = Applications.all()
		for a in apps:
			if self._count(a["name"], apps) > 1:
				self.fail("Duplicate definitions for: " + a["name"])

	def test_app_with_no_definition(self):
		self.assertIsNone(Applications.find("NON_EXISTING_APPLICATION"))

	def _count(self, app_name, apps):
		count = 0
		for a in apps:
			if a["name"] == app_name:
				count += 1
		return count


if __name__ == '__main__':
	unittest.main()


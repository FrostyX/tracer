#!/usr/bin/env python

from __meta__ import *
from resources.rules import Rules

from bs4 import BeautifulSoup
from os.path import dirname, realpath

class TestRules(unittest.TestCase):

	def test_rules_attributes(self):
		i = 1
		for r in Rules.all():
			if ("name" not in r) or ("action" not in r):
				self.fail("Missing attributes in rule #" + str(i))

			if r["action"] not in Rules.ACTIONS.values():
				self.fail("Unknown action in rule: " + r["name"])

			if len(r) > 2:
				self.fail("Unsupported attributes in rule: " + r["name"])

			i += 1

	def test_rules_duplicity(self):
		rules = Rules.all()
		for r in rules:
			if self._count(r["name"], rules) > 1:
				self.fail("Duplicate rules for: " + r["name"])


	def _count(self, app_name, rules):
		count = 0
		for r in rules:
			if r["name"] == app_name:
				count += 1
		return count


if __name__ == '__main__':
	unittest.main()

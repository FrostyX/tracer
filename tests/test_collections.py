#!/usr/bin/env python

from __meta__ import *
from tracer.resources.applications import Application
from tracer.resources.collections import ApplicationsCollection


class TestApplications(unittest.TestCase):

	def test_applications_sorted(self):
		a1 = Application({'name': 'foo', 'helper': 'bar'})
		a2 = Application({'name': 'baz', 'helper': 'qux'})
		a3 = Application({'name': 'quux', 'helper': 'corge'})
		collection = ApplicationsCollection([a1, a2, a3])

		self.assertEqual(collection.sorted('name'), ApplicationsCollection([a2, a1, a3]))
		self.assertEqual(collection.sorted('helper'), ApplicationsCollection([a1, a3, a2]))

#!/usr/bin/env python

from __meta__ import *
from tracer.resources.applications import Application
from tracer.resources.processes import Processes
from tracer.resources.package import Package
from tracer.resources.collections import ApplicationsCollection, ProcessesCollection, PackagesCollection


class TestCollections(unittest.TestCase):

	def test_applications_sorted(self):
		a1 = Application({'name': 'foo', 'helper': 'bar'})
		a2 = Application({'name': 'baz', 'helper': 'qux'})
		a3 = Application({'name': 'quux', 'helper': 'corge'})
		collection = ApplicationsCollection([a1, a2, a3])

		self.assertEqual(collection.sorted('name'), ApplicationsCollection([a2, a1, a3]))
		self.assertEqual(collection.sorted('helper'), ApplicationsCollection([a1, a3, a2]))
		self.assertIsInstance(collection, ApplicationsCollection)

	def test_processes_types(self):
		collection = Processes.all()
		self.assertIsInstance(collection, ProcessesCollection)
		self.assertIsInstance(collection.owned_by('user'), ProcessesCollection)
		self.assertIsInstance(collection.newer_than(1414006430.1), ProcessesCollection)

	def test_processes_none_user(self):
		collection = Processes.all().owned_by(None)
		self.assertGreater(len(collection), 0)

	def test_packages_intersection(self):
		p1 = Package("foo")
		p2 = Package("bar")
		p3 = Package("baz")
		p4 = Package("qux")
		c1 = PackagesCollection([p1, p2, p3, p4])
		self.assertEqual(c1.intersection([p1, p3]), PackagesCollection([p1, p3]))
		self.assertEqual(c1.intersection(None), c1)

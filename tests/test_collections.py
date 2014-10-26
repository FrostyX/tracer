#!/usr/bin/env python

from __meta__ import *
from tracer.resources.applications import Application
from tracer.resources.processes import Processes
from tracer.resources.collections import ApplicationsCollection, ProcessesCollection


class TestApplications(unittest.TestCase):

	def test_applications_sorted(self):
		a1 = Application({'name': 'foo', 'helper': 'bar'})
		a2 = Application({'name': 'baz', 'helper': 'qux'})
		a3 = Application({'name': 'quux', 'helper': 'corge'})
		collection = ApplicationsCollection([a1, a2, a3])

		self.assertEqual(collection.sorted('name'), ApplicationsCollection([a2, a1, a3]))
		self.assertEqual(collection.sorted('helper'), ApplicationsCollection([a1, a3, a2]))
		self.assertIsInstance(collection, ApplicationsCollection)

	def test_processes_types(self):
		processes = Processes.all()
		self.assertIsInstance(processes, ProcessesCollection)
		self.assertIsInstance(processes.owned_by('user'), ProcessesCollection)
		self.assertIsInstance(processes.newer_than(1414006430.1), ProcessesCollection)

#!/usr/bin/env python

from __meta__ import *
from tracer.resources.processes import Processes, Process
from tracer.resources.collections import ProcessesCollection


@unittest.skipIf(True, "@TODO Create Mock for Processes class")
class TestProcesses(unittest.TestCase):

	def test_children(self):
		process = Processes.all()[0]
		children = process.get_children()
		self.assertIsInstance(children, ProcessesCollection)

		for child in children:
			self.assertIsInstance(child, Process)


from .__meta__ import *
from tracer.resources.processes import Processes, Process
from tracer.resources.collections import ProcessesCollection
import os
import subprocess

@unittest.skipIf(True, "@TODO Create Mock for Processes class")
class TestProcesses(unittest.TestCase):

	def test_children(self):
		process = Processes.all()[0]
		children = process.children()
		self.assertIsInstance(children, ProcessesCollection)

		for child in children:
			self.assertIsInstance(child, Process)

	def test_unique_process(self):
		process = Process(os.getpid())
		parent = Process(os.getppid())

		self.assertIs(process, Process(os.getpid()))
		self.assertIs(parent, process.parent())
		self.assertIn(process, parent.children())

		Process.reset_cache()
		process2 = Process(os.getpid())
		self.assertEqual(process, process2)
		self.assertIsNot(process, process2)

	def test_process_caching(self):
		process = Process(os.getpid())

		# Populate the cache entry for children
		process.children()

		child = subprocess.Popen(os.sys.executable, stdin=subprocess.PIPE)
		self.assertEqual(0, len(process.children()))

		process.rebuild_cache()
		self.assertEqual(1, len(process.children()))

		child.terminate()

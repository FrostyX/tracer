from .__meta__ import *
from tracer.resources.processes import Processes, Process, ProcessWrapper
from tracer.resources.SystemdDbus import SystemdDbus
from tracer.resources.collections import ProcessesCollection
import os
import subprocess


class TestProcesses(unittest.TestCase):

	@unittest.skipIf(True, "@TODO Create Mock for Processes class")
	def test_children(self):
		process = Processes.all()[0]
		children = process.children()
		self.assertIsInstance(children, ProcessesCollection)

		for child in children:
			self.assertIsInstance(child, Process)

	@unittest.skipIf(True, "@TODO Create Mock for Processes class")
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

	@unittest.skipIf(True, "@TODO Create Mock for Processes class")
	def test_process_caching(self):
		process = Process(os.getpid())

		# Populate the cache entry for children
		process.children()

		child = subprocess.Popen(os.sys.executable, stdin=subprocess.PIPE)
		self.assertEqual(0, len(process.children()))

		process.rebuild_cache()
		self.assertEqual(1, len(process.children()))

		child.terminate()

	def test_name_sshd(self):
		p1 = ProcessMock()
		p1.data = {"name": "sshd",
			   "exe": "/usr/sbin/sshd",
			   "cmdline": ["/usr/sbin/sshd", "-D", "foo", "bar"]}
		assert p1.name() == "sshd"

		p2 = ProcessMock()
		p2.data = {"name": "sshd",
			   "exe": "/usr/sbin/sshd",
			   "cmdline": ["some", "thing", "and", "arguments", "idk", "what"]}
		assert p2.name() == "ssh-thing-session"

		# I don't know what case this is in a real life but see #129 and #125
		p3 = ProcessMock()
		p3.data = {"name": "sshd", "exe": "/usr/sbin/sshd",
			   "cmdline": ["withoutparams"]}
		assert p3.name() == "sshd"

	@unittest.skipIf(True, "@TODO Create Mock for Processes class")
	def test_dbus(self):
		dbus = SystemdDbus()
		pids = Processes.pids()
		nonexisting = max(pids) + 999
		assert dbus.has_service_property_from_pid(1, "PAMName") is False
		assert dbus.has_service_property_from_pid(nonexisting, "PAMName") is False


class ProcessMock(ProcessWrapper):
	def __init__(self):
		self.data = {}

	def _attr(self, name):
		return self.data[name]

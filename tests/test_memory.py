import unittest

import psutil

from tracer.resources import memory

from .__meta__ import *


class ProcessMock:
	def __init__(self, pid, files):
		self.pid = pid
		self._files = files

	@property
	def files(self):
		return self._files


def _denied_files(self):
	raise psutil.AccessDenied(self.pid, None)


def _no_such_process_files(self):
	raise psutil.NoSuchProcess(self.pid, None)


class _BadProcess(ProcessMock):
	@property
	def files(self):
		return _denied_files(self)


class _GoneProcess(ProcessMock):
	@property
	def files(self):
		return _no_such_process_files(self)


class TestMemory(unittest.TestCase):

	def setUp(self):
		self._original = memory.Processes

	def tearDown(self):
		memory.Processes = self._original

	class _FakeCollection(list):
		def owned_by(self, user):
			return self
		def unique(self):
			return self

	def _fake_processes(self, processes):
		memory.Processes = type('FakeProcesses', (), {
			'all': staticmethod(lambda: TestMemory._FakeCollection(processes))
		})

	def test_dump_memory_groups_by_file(self):
		p1 = ProcessMock(1, ['/bin/foo', '/bin/bar'])
		p2 = ProcessMock(2, ['/bin/foo'])
		self._fake_processes([p1, p2])
		result = memory.dump_memory()
		self.assertEqual(result, {
			'/bin/foo': [p1, p2],
			'/bin/bar': [p1]
		})

	def test_dump_memory_empty(self):
		self._fake_processes([])
		self.assertEqual(memory.dump_memory(), {})

	def test_dump_memory_ignores_access_denied(self):
		p1 = ProcessMock(1, ['/bin/foo'])
		p2 = _BadProcess(2, [])
		self._fake_processes([p1, p2])
		self.assertEqual(memory.dump_memory(), {'/bin/foo': [p1]})

	def test_dump_memory_ignores_no_such_process(self):
		p1 = ProcessMock(1, ['/bin/foo'])
		p2 = _GoneProcess(2, [])
		self._fake_processes([p1, p2])
		self.assertEqual(memory.dump_memory(), {'/bin/foo': [p1]})


if __name__ == '__main__':
	unittest.main()

from __meta__ import *
from tracer.resources.tracer import Tracer
from tracer.resources.collections import ProcessesCollection, PackagesCollection, ApplicationsCollection
from tracer.resources.rules import Rules
from tracer.resources.applications import Applications


class TestRules(unittest.TestCase):
	def setUp(self):
		self.tracer = Tracer(PackageManagerMock(), Rules, Applications, memory=dump_memory_mock)
		self.tracer.timestamp = 5555  # Sure, it should be a UNIX timestamp value

	def test_trace_affected(self):
		affected = self.tracer.trace_affected()
		self.assertSetEqual(set(affected), set([Applications.find("baz"), Applications.find("qux")]))
		self.assertIsInstance(affected, ApplicationsCollection)


class ProcessMock(object):
	def __init__(self, pid, name, create_time, files):
		self.parent = None
		self.pid = pid
		self.files = files
		self._name = name
		self._create_time = create_time

	def name(self):
		return self._name

	def create_time(self):
		return self._create_time


class ProcessesMock(object):
	@staticmethod
	def all():
		return ProcessesCollection([
			ProcessMock(2, "foo", 1111, ["file1", "file2", "file3"]),
			ProcessMock(3, "bar", 9999, ["file10", "file11", "file12"]),
			ProcessMock(4, "baz", 6666, ["file7", "file1", "file3"]),
			ProcessMock(5, "qux", 7777, ["file4", "file9"]),
		])


class PackageMock(object):
	def __init__(self, name, modified, files):
		self.name = name
		self.modified = modified
		self.files = files


class PackageManagerMock(object):
	_packages = [
		PackageMock("A", 3333, ["file1", "file2", "file3"]),
		PackageMock("B", 4444, ["file4", "file5", "file6"]),
		PackageMock("C", 7777, ["file7", "file8", "file9"]),
		PackageMock("D", 8888, ["file10", "file11", "file12"]),
	]

	def packages_newer_than(self, unix_time):
		return PackagesCollection(filter(lambda p: p.modified >= unix_time, self._packages))

	def package_files(self, pkg_name):
		for package in self._packages:
			if package.name == pkg_name:
				return package.files


def dump_memory_mock(user=None):
	memory = {}
	for process in ProcessesMock.all():
			for file in process.files:
				if file in memory:
					memory[file].append(process)
				else:
					memory[file] = [process]
	return memory


if __name__ == '__main__':
	unittest.main()

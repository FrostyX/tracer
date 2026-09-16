from .__meta__ import *
from tracer.resources.tracer import Tracer
from tracer.resources.rules import Rules
from tracer.resources.applications import Applications, Application
from tracer.resources.processes import AffectedProcess
from tracer.resources.collections import \
	ProcessesCollection, \
	PackagesCollection, \
	ApplicationsCollection, \
	AffectedProcessesCollection

try:
	from unittest.mock import patch
except:
	from mock import patch


class TestRules(unittest.TestCase):
	def setUp(self):
		Applications._apps = ApplicationsCollection()
		self.tracer = Tracer(PackageManagerMock(), Rules, Applications, memory=dump_memory_mock)
		self.tracer.timestamp = 5555  # Sure, it should be a UNIX timestamp value
		Applications._append_application({"name": "kernel", "ignore": True})
		Applications._append_application({"name": "glibc", "type": "static-package"})
		Application.processes_factory = ProcessesMock

	@patch('tracer.resources.applications.System.init_system', return_value="dummy")
	def test_trace_affected(self, init_system):
		affected = self.tracer.trace_affected()
		self.assertSetEqual(set(affected), set([
			Applications.find("baz"),
			Applications.find("qux"),
			Applications.find("glibc"),
		]))
		self.assertIsInstance(affected, ApplicationsCollection)

	@patch('tracer.resources.applications.System.init_system', return_value="dummy")
	def test_trace_affected_static_package(self, init_system):
		"""static-package apps are detected by package name even with no running process."""
		affected = self.tracer.trace_affected()
		self.assertIn(Applications.find("glibc"), affected)

	def test_trace_application(self):
		affected = self.tracer.trace_application(Applications.find("baz"), AffectedProcessMock)
		self.assertIsInstance(affected, AffectedProcessesCollection)
		self.assertEqual(len(affected), 1)

		process = affected[0]
		self.assertIsInstance(process, AffectedProcess)
		self.assertEqual(process.pid, 4)  # pid of "baz" in our mock


class ProcessMock(object):
	def __init__(self, pid, name, create_time, files):
		self.pid = pid
		self.files = files
		self._name = name
		self._create_time = create_time

	def name(self):
		return self._name

	@property
	def real_name(self):
		return self._name

	@property
	def is_interpreted(self):
		return False

	@property
	def is_session(self):
                return False

	def create_time(self):
		return self._create_time

	def children(self):
		return []

	def parent(self):
		return None


class AffectedProcessMock(AffectedProcess):
	def __init__(self, pid=None):
		# Do not run the parent __init__
		self.pid = pid
		self.packages = set()
		self.files = set()


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
		PackageMock("glibc", 6666, ["file13", "file14"]),
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


class TestStaticPackageDedup(unittest.TestCase):
	"""Ensure an app detected by both process walk and static-package logic is emitted once."""

	def setUp(self):
		Applications._apps = ApplicationsCollection()
		Applications._append_application({"name": "kernel", "ignore": True})
		Applications._append_application({"name": "systemd", "type": "static-package"})
		Application.processes_factory = ProcessesDedupMock

	@patch('tracer.resources.applications.System.init_system', return_value="dummy")
	def test_static_package_not_duplicated(self, init_system):
		tracer = Tracer(PackageManagerDedupMock(), Rules, Applications, memory=dump_memory_dedup_mock)
		tracer.timestamp = 5555
		affected = tracer.trace_affected()
		systemd_apps = [a for a in affected if a.name == "systemd"]
		self.assertEqual(len(systemd_apps), 1)


class ProcessesDedupMock(object):
	@staticmethod
	def all():
		return ProcessesCollection([
			ProcessMock(6, "systemd", 1111, ["file15"]),
		])


class PackageManagerDedupMock(object):
	_packages = [
		PackageMock("systemd", 6666, ["file15"]),
	]

	def packages_newer_than(self, unix_time):
		return PackagesCollection(filter(lambda p: p.modified >= unix_time, self._packages))

	def package_files(self, pkg_name):
		for package in self._packages:
			if package.name == pkg_name:
				return package.files


def dump_memory_dedup_mock(user=None):
	memory = {}
	for process in ProcessesDedupMock.all():
		for file in process.files:
			if file in memory:
				memory[file].append(process)
			else:
				memory[file] = [process]
	return memory


if __name__ == '__main__':
	unittest.main()

from .__meta__ import *
from tracer.resources.applications import Applications, Application
from tracer.resources.processes import Processes, AffectedProcess
from tracer.resources.package import Package
from tracer.resources.collections import ApplicationsCollection, ProcessesCollection, PackagesCollection, AffectedProcessesCollection


class TestCollections(unittest.TestCase):

	def test_applications_sorted(self):
		default_type = Applications.DEFAULT_TYPE
		a1 = Application({'name': 'foo', 'helper': 'bar', 'type': default_type})
		a2 = Application({'name': 'baz', 'helper': 'qux', 'type': default_type})
		a3 = Application({'name': 'quux', 'helper': 'corge', 'type': default_type})
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

	@unittest.skipIf(True, "@TODO Create Mock for Processes class")
	def test_processes_update(self):
		p1 = AffectedProcess(1234)
		p2 = AffectedProcess(1234)
		p2.files = set(['foo', 'bar', 'baz'])

		c = AffectedProcessesCollection()
		c.update([p1])
		c.update([p2])

		self.assertIn(p1, c)
		self.assertIn('bar', c[c.index(p1)].files)

	def test_packages_intersection(self):
		p1 = Package("foo")
		p2 = Package("bar")
		p3 = Package("baz")
		p4 = Package("qux", 123)
		p5 = Package("qux")
		c1 = PackagesCollection([p1, p2, p3, p4])
		self.assertEqual(c1.intersection([p1, p3]).sorted("name"), PackagesCollection([p1, p3]).sorted("name"))
		self.assertEqual(c1.intersection(None), c1)
		self.assertIsNotNone(c1.intersection([p5])[0].modified)

	def test_replace_values(self):
		a1 = Application({"name": "foo"})
		a2 = Application({"name": "bar"})
		a3 = Application({"name": "baz"})
		c1 = ApplicationsCollection([a1, a2, a3])

		assert {a.name for a in c1} == {"foo", "bar", "baz"}
		c1.replace_values("name", "foo", "qux")
		assert {a.name for a in c1} == {"qux", "bar", "baz"}

	def test_collection_sorted_callable(self):
		c1 = Processes.all()
		c2 = c1.sorted("create_time")

		for i in range(len(c2) - 1):
			if c2[i].create_time() > c2[i+1].create_time():
				raise Exception("The collection isn't sorted properly")

	def test_application_sorted_none_helper(self):
		"""
		https://github.com/FrostyX/tracer/issues/151
		https://github.com/FrostyX/tracer/issues/156
		"""
		default_type = Applications.DEFAULT_TYPE
		a1 = Application({'name': 'foo', 'helper': None, 'type': default_type})
		a2 = Application({'name': 'baz', 'helper': 'qux', 'type': default_type})
		collection = ApplicationsCollection([a1, a2])
		collection_sorted = collection.sorted('helper')
		self.assertEqual([app.helper for app in collection_sorted],
						 ["qux", None])

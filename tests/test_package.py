from .__meta__ import *
from tracer.resources.package import Package


class TestPackage(unittest.TestCase):

	def test_equality(self):
		p1 = Package("foo")
		p2 = Package("foo")
		p3 = Package("bar")

		self.assertEqual(p1, p2)
		self.assertNotEqual(p1, p3)

	def test_representation(self):
		package = Package("foo")
		self.assertEqual(repr(package), "<Package:foo>")

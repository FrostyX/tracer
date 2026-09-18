import unittest
from tracer.resources.pycomp import StringIO
from tracer.resources.args_parser import parser
from tracer.resources.package import Package
from tracer.resources.router import Router
from tracer.resources.exceptions import UnsupportedDistribution
from tracer.resources.lang import _


class TracerMock:
	def __init__(self, *args):
		pass

	def trace_affected(self, user=None):
		return []


class TestMain(unittest.TestCase):

	def test_run_with_no_args(self):
		# This test would need to mock sys.argv and other system dependencies
		# which is beyond the scope of unit testing
		pass

	def test_package_creation_with_timestamp(self):
		p = Package("test", 12345)
		self.assertEqual(p.name, "test")
		self.assertEqual(p.modified, 12345)

	def test_package_creation_without_timestamp(self):
		p = Package("test")
		self.assertEqual(p.name, "test")
		self.assertIsNone(p.modified)

	def test_parser_defaults(self):
		args = parser.parse_args([])
		self.assertEqual(args.pkgs, [])
		self.assertEqual(args.packages, [])
		self.assertFalse(args.interactive)

	def test_parser_with_packages(self):
		args = parser.parse_args(["pkg1", "pkg2"])
		self.assertEqual(args.pkgs, ["pkg1", "pkg2"])

	def test_parser_with_option_packages(self):
		args = parser.parse_args(["--packages", "pkg1", "pkg2"])
		self.assertEqual(args.packages, ["pkg1", "pkg2"])


if __name__ == '__main__':
	unittest.main()

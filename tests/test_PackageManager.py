from .__meta__ import *
from tracer.resources.PackageManager import PackageManager


class FirstManager(object):
	def package_name_only(self, pkg_object):
		return "first"


class SecondManager(object):
	def package_name_only(self, pkg_object):
		return "second"


class TestPackageManager(unittest.TestCase):
	def test_package_name_only_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		self.assertEqual(pm.package_name_only("pkg"), "first")


if __name__ == '__main__':
	unittest.main()

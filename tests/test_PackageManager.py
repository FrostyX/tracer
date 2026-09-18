from .__meta__ import *
from tracer.resources.PackageManager import PackageManager
from tracer.resources.package import Package


class FirstManager(object):
	def package_name_only(self, pkg_object):
		return "first"

	def packages_newer_than(self, unix_time):
		return [Package("first_new", 100)]

	def package_files(self, pkg_name):
		return ["first_files"]

	def load_package_info(self, package):
		package.description = "loaded_from_first"
		return package

	def provided_by(self, app):
		return "first_provider"

	def find_package(self, pkg_name, search):
		return "first_match"

	def compare_packages(self, package1, package2):
		return 1


class SecondManager(object):
	def package_name_only(self, pkg_object):
		return "second"

	def packages_newer_than(self, unix_time):
		return [Package("second_new", 200)]

	def package_files(self, pkg_name):
		return ["second_files"]

	def load_package_info(self, package):
		package.description = "loaded_from_second"
		return package

	def provided_by(self, app):
		return "second_provider"

	def find_package(self, pkg_name, search):
		return "second_match"

	def compare_packages(self, package1, package2):
		return -1


class TestPackageManager(unittest.TestCase):
	def test_package_name_only_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		self.assertEqual(pm.package_name_only("pkg"), "first")

	def test_names_lists_manager_class_names(self):
		pm = PackageManager(FirstManager(), SecondManager())
		names = list(pm.names())
		self.assertIn("FirstManager", names)
		self.assertIn("SecondManager", names)

	def test_packages_newer_than_merges_all_managers(self):
		pm = PackageManager(FirstManager(), SecondManager())
		result = pm.packages_newer_than(0)
		self.assertIsInstance(result, list)
		self.assertEqual(len(result), 2)

	def test_package_files_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		self.assertEqual(pm.package_files("pkg"), ["first_files"])

	def test_load_package_info_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		package = Package("pkg")
		pm.load_package_info(package)
		self.assertEqual(package.description, "loaded_from_first")

	def test_provided_by_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		self.assertEqual(pm.provided_by("app"), "first_provider")

	def test_find_package_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		self.assertEqual(pm.find_package("pkg", "search"), "first_match")

	def test_compare_packages_delegates_to_first_manager(self):
		pm = PackageManager(FirstManager(), SecondManager())
		self.assertEqual(pm.compare_packages("p1", "p2"), 1)

	def test_package_name_only_delegates_to_first_manager_with_different_second(self):
		pm = PackageManager(FirstManager(), SecondManager())
		result = pm.package_name_only("pkg")
		self.assertEqual(result, "first")
		self.assertNotEqual(result, "second")


if __name__ == '__main__':
	unittest.main()

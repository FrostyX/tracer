#!/usr/bin/env python

from __meta__ import *
from packageManagers.ipackageManager import IPackageManager
from packageManagers.yum import Yum

class TestYum(unittest.TestCase):
	def setUp(self):
		self.manager = Yum()

	def test_implements_package_manager_interface(self):
		self.assertIsInstance(self.manager, IPackageManager, "Every package manager should inherit from IPackageManager")

	def test_package_newer_than_implemented(self):
		try: self.manager.packages_newer_than(0)
		except NotImplementedError: self.fail("packages_newer_than() is not implemented!")
		except Exception: pass

	def test_package_info(self):
		try: self.manager.package_info("")
		except NotImplementedError: self.fail("package_info() is not implemented!")
		except Exception: pass

	def test_package_files_implemented(self):
		try: self.manager.package_files("")
		except NotImplementedError: self.fail("packages_files() is not implemented!")
		except Exception: pass

	def test_provided_by(self):
		try: self.manager.provided_by("")
		except NotImplementedError: self.fail("provided_by() is not implemented!")
		except Exception: pass


if __name__ == '__main__':
	unittest.main()

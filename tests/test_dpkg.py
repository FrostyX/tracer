from .__meta__ import *
try:
	from tracer.packageManagers.ipackageManager import IPackageManager
	from tracer.packageManagers.dpkg import Dpkg
except ImportError: pass

@unittest.skipIf(DISTRO != 'debian', "Skipping tests because they are distro-specific")
class TestDpkg(unittest.TestCase):
	def setUp(self):
		self.manager = Dpkg()

	def test_implements_package_manager_interface(self):
		self.assertIsInstance(self.manager, IPackageManager, "Every package manager should inherit from IPackageManager")

	def test_package_newer_than_implemented(self):
		try: self.manager.packages_newer_than(0)
		except NotImplementedError: self.fail("packages_newer_than() is not implemented!")
		except Exception: pass

	def test_load_package_info(self):
		try: self.manager.load_package_info("")
		except NotImplementedError: self.fail("load_package_info() is not implemented!")
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

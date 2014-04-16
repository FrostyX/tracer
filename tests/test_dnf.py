#!/usr/bin/env python

from __meta__ import *
from packageManagers.dnf import Dnf

class TestDnf(unittest.TestCase):
	def setUp(self):
		self.manager = Dnf()

	def test_package_newer_than_implemented(self):
		try: self.manager.packages_newer_than(0)
		except NotImplemented: self.fail("packages_newer_than() is not implemented!")
		except Exception: pass

	def test_package_files_implemented(self):
		try: self.manager.package_files("")
		except NotImplemented: self.fail("packages_files() is not implemented!")
		except Exception: pass


if __name__ == '__main__':
	unittest.main()

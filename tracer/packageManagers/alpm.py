#-*- coding: utf-8 -*-
# alpm.py
#
# Copyright (C) 2016 Patrick Griffis <tingping@tingping.se>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from __future__ import absolute_import

from tracer.resources.system import System
if System.distribution() in ["arch", "archarm"]:

	import bisect
	from .ipackageManager import IPackageManager
	from tracer.resources.package import Package
	from tracer.resources.collections import PackagesCollection
	from tracer.resources.applications import Applications
	import pyalpm

	class Alpm(IPackageManager):

		def __init__(self, *args, **kwargs):
			self.opts = kwargs
			self.handle = pyalpm.Handle('/', '/var/lib/pacman')
			self.db = self.handle.get_localdb()

		def packages_newer_than(self, unix_time):
			"""
			Returns list of packages which were modified between unix_time and present
			"""
			new_pkgs = PackagesCollection()
			for pkg in self.db.pkgcache:
				if pkg.installdate > unix_time:
					new_pkgs.append(Package(pkg.name, pkg.installdate))

			return new_pkgs

		def package_files(self, pkg_name):
			"""
			Returns list of files provided by package
			"""
			pkg = self.db.get_pkg(pkg_name)
			if not pkg:
				return []

			return ['/' + f[0] for f in pkg.files]

		def load_package_info(self, package):
			"""
			From database load informations about given package and set them to it
			"""
			if not package:
				return

			pkg = self.db.get_pkg(package.name)
			if not pkg:
				return

			package.description = pkg.desc
			package.modified = pkg.installdate
			# Don't have categories

		def provided_by(self, app):
			"""
			Returns name of package which provides given application
			"""
			# We need a full path to the binary
			process = app.instances[0]
			return self._file_provided_by(process.exe)

		def find_package(self, pkg_name, version):
			"""
			Find a package by name and some other input criteria
			"""
			pkg = self.db.get_pkg(pkg_name)
			if pkg and pyalpm.vercmp(pkg.version, version) == 0:
				return pkg

		def compare_packages(self, package1, package2):
			"""
			vercmp returns:
			< 0 if ver1 < ver2
			0 if ver1 == ver2
			> 0 if ver1 > ver2
			"""
			return pyalpm.vercmp(package1.version, package2.version)

		@staticmethod
		def _bsearch_list(l, item):
			"""
			Searches a sorted list, returns True if found
			"""
			i = bisect.bisect_left(l, item)
			if i != len(l) and l[i] == item:
				return True
			else:
				return False

		def _file_provided_by(self, file_name):
			"""
			Returns name of package which provides given file
			"""
			# This is a bit slow
			for pkg in self.db.pkgcache:
				files = [f[0] for f in pkg.files]
				if self._bsearch_list(files, file_name[1:]):
					return Package(pkg.name, pkg.installdate)
			else:
				return None


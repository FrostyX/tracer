#-*- coding: utf-8 -*-
# PackageManager.py
# Wrapper class for package managers.
# Provides their API and allows to use multiple package managers at once.
#
# Copyright (C) 2016 Jakub Kadlcik
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

import itertools


class PackageManager:

	"""
	Wrapper class for package managers.
	Provides their API and allows to use multiple package managers at once.

	In actions where it makes no sense to merge results from more package managers,
	result from first manager is used.
	"""

	package_managers = None

	def __init__(self, *instances):
		self.package_managers = instances

	def names(self):
		return map(lambda x: x.__class__.__name__ ,self.package_managers)

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Packages in list should be dictionaries with keys {"name", "modified"}
		"""
		# @FIXME move import to top-level
		from tracer.resources.collections import PackagesCollection
		packages_lists = [p.packages_newer_than(unix_time) for p in self.package_managers]
		return PackagesCollection(itertools.chain.from_iterable(packages_lists))

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		return self.package_managers[0].package_files(pkg_name)

	def load_package_info(self, package):
		"""From database load informations about given package and set them to it"""
		return self.package_managers[0].load_package_info(package)

	def provided_by(self, app):
		"""Returns name of package which provides given application"""
		return self.package_managers[0].provided_by(app)

	def find_package(self, pkg_name, search):
		"""Find a package by name and some other input criteria"""
		return self.package_managers[0].find_package(pkg_name, search)

	def compare_packages(self, package1, package2):
		"""
		Compares two packages by their version information
		Returns:
		0 if they are equal
		1 if package1 > package2
		-1 if package2 > package1
		"""
		return self.package_managers[0].compare_packages(package1, package2)

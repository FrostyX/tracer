#-*- coding: utf-8 -*-
# ipackageManager.py
# This class should be inherited by any other package manager
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


class IPackageManager(object):

	def __init__(self, **kwargs):
		"""This class is 'interface' so you can't create an instance"""
		raise NotImplementedError

	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Packages in list should be dictionaries with keys {"name", "modified"}
		"""
		raise NotImplementedError

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		raise NotImplementedError

	def load_package_info(self, package):
		"""From database load informations about given package and set them to it"""
		raise NotImplementedError

	def provided_by(self, app):
		"""Returns name of package which provides given application"""
		raise NotImplementedError

	def find_package(self, pkg_name, search):
		"""Find a package by name and some other input criteria"""
		raise NotImplementedError

	def compare_packages(self, package1, package2):
		"""
		Compares two packages by their version information
		Returns:
		0 if they are equal
		1 if package1 > package2
		-1 if package2 > package1
		"""
		raise NotImplementedError

	@staticmethod
	def _pkg_name_without_version(pkg_name):
		try:
			pkg_name = pkg_name[:pkg_name.index('.')]  # Cut from first . to end
			pkg_name = pkg_name[:pkg_name.rindex('-')] # Cut from last  - to end
		except ValueError: pass
		return pkg_name

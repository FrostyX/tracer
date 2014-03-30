#-*- coding: utf-8 -*-
# ipackageManager.py
# This class should be inherited by any other package manager
#
# Copyright (C) 2013 Jakub Kadlčík
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

class IPackageManager:
	def packages_newer_than(self, unix_time):
		"""
		Returns list of packages which were modified between unix_time and present
		Packages in list should be dictionaries with keys {"name", "modified"}
		"""
		raise NotImplementedError

	def package_files(self, pkg_name):
		"""Returns list of files provided by package"""
		raise NotImplementedError

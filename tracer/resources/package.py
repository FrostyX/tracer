#-*- coding: utf-8 -*-
# package.py
# Represents linux package
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


class Package:
	"""Represents linux package"""

	name = None
	modified = None
	description = None
	pkg_type = None
	category = None

	def __init__(self, name, modified=None):
		self.name = name
		self.modified = modified

	def __eq__(self, package):
		"""Packages are equal when they have same name"""
		return (isinstance(package, self.__class__)
			and self.name == package.name)

	def __ne__(self, package):
		return not self.__eq__(package)

	def __repr__(self):
		return "<Package:" + self.name + ">"

	def __str__(self):
		return self.name

	def __hash__(self):
		return hash(self.name)

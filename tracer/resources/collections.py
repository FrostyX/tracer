#-*- coding: utf-8 -*-
# collections.py
# Define various kind of collections
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

from functools import cmp_to_key
from psutil import NoSuchProcess


class Collection(list):

	def replace_values(self, attribute, source_value, required_value):
		for app in self:
			if getattr(app, attribute) == source_value:
				app.update({attribute: required_value})


	def sorted(self, attribute):
		def _sort(app1, app2):
			value1 = _value(app1, attribute)
			value2 = _value(app2, attribute)

			# Make sure the None values are at the end
			# This shouldn't happen anyway but sometimes if does,
			# for some reason, see #151 or #156
			if not value1:
				return 1

			if not value2:
				return -1

			# https://stackoverflow.com/a/13239857/3285282
			if value1 < value2:
				return -1
			if value1 > value2:
				return 1
			return 0

		def _value(app, attribute):
			if callable(getattr(self[0], attribute)):
				return getattr(app, attribute)()
			return getattr(app, attribute)

		return sorted(self, key=cmp_to_key(_sort))


class ApplicationsCollection(Collection):

	def with_helpers(self):
		applications = filter(lambda app: app.helper, self)
		return ApplicationsCollection(applications)

	def without_helpers(self):
		applications = filter(lambda app: not app.helper, self)
		return ApplicationsCollection(applications)

	def exclude_types(self, app_types):
		"""app_types -- see Applications.TYPES"""
		applications = filter(lambda app: app.type not in app_types, self)
		return ApplicationsCollection(applications)

	def filter_types(self, app_types):
		"""app_types -- see Applications.TYPES"""
		applications = filter(lambda app: app.type in app_types, self)
		return ApplicationsCollection(applications)

	def count_type(self, app_type):
		count = 0
		for application in self:
			if application.type == app_type:
				count += 1
		return count

	def unique(self):
		return ApplicationsCollection(set(self))


class ProcessesCollection(Collection):

	def owned_by(self, user):
		if not user:
			return self
		return self.filtered(lambda process: process.username() == user)

	def newer_than(self, timestamp):
		return self.filtered(lambda process: process.create_time() >= timestamp)

	def unique(self):
		unique = set()
		for process in self:
			try: unique.add(process)
			except NoSuchProcess: pass
		return ProcessesCollection(unique)

	def filtered(self, function):
		processes = ProcessesCollection()
		for process in self:
			try:
				if function(process):
					processes.append(process)
			except NoSuchProcess: pass
		return processes


class AffectedProcessesCollection(ProcessesCollection):

	def update(self, iterable):
		for x in iterable:
			if x in self:
				self[self.index(x)].update(x)
			else:
				self.append(x)


class PackagesCollection(Collection):

	_package_manager = None

	def __init__(self, *args):
		list.__init__(self, *args)

	def intersection(self, packages):
		if packages is not None:
			return PackagesCollection(set(packages).intersection(self))
		return self

	@property
	def files(self):
		files = []
		for package in self:
			files.extend(self._package_manager.package_files(package.name))
		return set(files)

	def unique_newest(self):
		packages = {}
		for p in self:
			if p.name in packages:
				if packages[p.name].modified > p.modified:
					continue
			packages[p.name] = p
		return PackagesCollection(packages.values())

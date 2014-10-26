#-*- coding: utf-8 -*-
# tracer.py
# Tracer finds outdated running applications in your system
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

from __future__ import absolute_import

import psutil
from tracer.resources.rules import Rules
from tracer.resources.FilenameCleaner import FilenameCleaner
import tracer.resources.memory as Memory
import tracer.resources.system as System


class Tracer:
	"""Tracer finds outdated running applications in your system"""

	"""List of packages that only should be traced"""
	_specified_packages = None

	"""
	When true, tracer pretends that specified packages have been updated just now.
	Benefit of this is absolutely no need for openning the package history database
	"""
	_now = False

	"""
	Timestamp since when the updates should be
	"""
	timestamp = None

	"""Instance of package manager class. Set by __init__"""
	_PACKAGE_MANAGER = None

	def __init__(self):
		self._PACKAGE_MANAGER = System.package_manager()

	def _modified_packages(self):
		"""Returns list of packages what tracer should care about"""
		if self.specified_packages and self.now:
			return self.specified_packages

		timestamp = self.timestamp if self.timestamp else psutil.BOOT_TIME
		packages = self._PACKAGE_MANAGER.packages_newer_than(timestamp)
		if self.specified_packages:
			for package in packages:
				if package not in self.specified_packages:
					packages.remove(package)
		return packages

	def package_info(self, app_name):
		return self._PACKAGE_MANAGER.package_info(app_name)

	def trace_running(self, user=None):
		"""
		Returns list of processes which uses some files that have been modified
		@TODO This function should be hardly optimized
		"""

		memory = Memory.dump_memory(user)
		packages = self.specified_packages if self.specified_packages and self._now else self._modified_packages()

		running = set()
		found = []
		for package in packages:
			for file in self._PACKAGE_MANAGER.package_files(package.name):

				file = FilenameCleaner.strip(file)
				try:
					for p in memory[file]:
						if p.pid in found:
							continue

						if p.create_time <= package.modified:
							found.append(p.pid)
							p = self._apply_rules(p)
							running.add(p)
				except KeyError: pass
		return running

	def _apply_rules(self, process):
		parent = process.parent
		if not parent:
			return process

		rule = Rules.find(parent.name)

		if not rule or not rule.action:
			return process

		if rule.action == Rules.ACTIONS["CALL-PARENT"]:
			return self._apply_rules(parent)

		# Only PRINT action left
		# PRINT rule is defined for parent process
		return parent

	def who_affected(self, app_name):
		"""
		Returns list of packages and their files who affected the process
		Packages and files are wrapped with dict containing process as a key.
		[ {process : {pkg_name : [file1, file2, ...]}, ... }, ... ]
		"""
		process = Memory.processes_by_name(app_name)[0]  # @TODO Reimplement for all processes
		packages = self._modified_packages()
		affected_by = self._affecting_packages(process, packages)
		affected_by.update(self._affecting_children(process, packages))
		return affected_by

	def _affecting_packages(self, process, packages):
		affected_by = {}
		process_files = Memory.process_files(process.pid)
		for package in packages:
			matching_files = set()
			for package_file in self._PACKAGE_MANAGER.package_files(package.name):
				package_file = FilenameCleaner.strip(package_file)
				if not package_file in process_files:
					continue

				if process.create_time <= package.modified:
					matching_files.add(package_file)

			if matching_files: affected_by[process] = {package.name : matching_files}
		return affected_by

	def _affecting_children(self, process, packages):
		if not Rules.find(process.name):
			return {}

		affected_by = {}
		for child in process.get_children():
			affected_by.update(self._affecting_packages(child, packages))
		return affected_by

	@property
	def specified_packages(self):
		return self._specified_packages

	@specified_packages.setter
	def specified_packages(self, packages):
		self._specified_packages = packages

	@property
	def now(self):
		return self._now

	@now.setter
	def now(self, value):
		self._now = value

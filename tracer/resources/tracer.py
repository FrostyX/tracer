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

from tracer.resources.system import System
from tracer.resources.FilenameCleaner import FilenameCleaner
from tracer.resources.processes import AffectedProcess
from tracer.resources.collections import ApplicationsCollection, AffectedProcessesCollection
from tracer.resources.exceptions import UnsupportedDistribution


class Tracer(object):
	"""Tracer finds outdated running applications in your system"""

	"""List of packages that only should be traced"""
	specified_packages = None

	"""
	When true, tracer pretends that specified packages have been updated just now.
	Benefit of this is absolutely no need for openning the package history database
	"""
	now = False

	"""
	Timestamp since when the updates should be
	"""
	timestamp = None

	"""Instance of package manager class. Set by __init__"""
	_PACKAGE_MANAGER = None

	"""Structure representing all processes and files they use. See ``tracer.resources.memory.dump_memory``"""
	_memory = None

	"""Objects responsible for providing applications and rules settings form config files"""
	_rules = None
	_applications = None

	"""Observer object responsible for calling desired hooks"""
	_hooks_observer = None

	def __init__(self, package_manager, rules, applications, memory=None, hooks_observer=None):
		if not package_manager:
			raise UnsupportedDistribution(System.distribution())

		self._PACKAGE_MANAGER = package_manager
		self._rules = rules
		self._applications = applications
		self._memory = memory
		self._hooks_observer = hooks_observer

	def _modified_packages(self):
		"""Returns list of packages what tracer should care about"""
		if self.specified_packages and self.now:
			return self.specified_packages

		timestamp = self.timestamp if self.timestamp else System.boot_time()
		packages = self._PACKAGE_MANAGER.packages_newer_than(timestamp)
		packages = packages.intersection(self.specified_packages)
		return packages

	def trace_affected(self, user=None):
		"""
		Returns collection of applications which uses some files that have been modified
		@TODO This function should be hardly optimized
		"""

		memory = self._memory(user)
		packages = self._modified_packages()

		affected = {}
		found = []
		for package in packages:
			for file in self._PACKAGE_MANAGER.package_files(package.name):

				file = FilenameCleaner.strip(file)
				if not file in memory:
					continue

				for p in memory[file]:
					if p.pid in found:
						continue

					if p.create_time() <= package.modified:
						found.append(p.pid)
						p = self._apply_rules(p)
						a = self._applications.find(p.name())

						if a.name not in affected:
							affected[a.name] = a
							affected[a.name].affected_instances = AffectedProcessesCollection()
							self._call_hook(a)
						affected[a.name].affected_instances.append(p)
		return ApplicationsCollection(affected.values())

	def _apply_rules(self, process):
		parent = process.parent()
		if not parent:
			return process

		c_rule = self._rules.find(process.name())
		p_rule = self._rules.find(parent.name())

		if c_rule and c_rule.action == self._rules.ACTIONS["RETURN"]:
			return process

		if not p_rule or not p_rule.action:
			return process

		if p_rule.action == self._rules.ACTIONS["CALL-PARENT"]:
			return self._apply_rules(parent)

		# Only RETURN action left
		# RETURN rule is defined for parent process
		return parent

	def _call_hook(self, app):
		if self._hooks_observer:
			self._hooks_observer(app.name)

	def trace_application(self, app_name, affected_process_factory=AffectedProcess):
		"""
		Returns collection of processes where each of them contains
		packages which affected it. Packages contains only files matching
		with the particular process
		"""
		packages = self._modified_packages()
		processes = AffectedProcessesCollection()
		for process in self._applications.find(app_name).instances:
			processes.update(self._affecting_processes(process, packages, affected_process_factory))
			processes.update(self._affecting_children(process, packages, affected_process_factory))
		return processes

	def _affecting_processes(self, process, packages, affected_process_factory=AffectedProcess):
		collection = AffectedProcessesCollection()
		process_files = process.files
		for package in packages:
			matching_files = set()
			for package_file in self._PACKAGE_MANAGER.package_files(package.name):
				package_file = FilenameCleaner.strip(package_file)
				if not package_file in process_files:
					continue

				if process.create_time() <= package.modified:
					matching_files.add(package_file)

			if matching_files:
				aff_pkg = package
				aff_pkg.files = matching_files

				affected = affected_process_factory(process.pid)
				affected.__dict__.update(process.__dict__)
				affected.packages.update([aff_pkg])
				collection.update([affected])
		return collection

	def _affecting_children(self, process, packages, affected_process_factory):
		if not self._rules.find(process.name()):
			return {}

		processes = AffectedProcessesCollection()
		for child in process.children():
			processes.update(self._affecting_processes(child, packages, affected_process_factory))
			processes.update(self._affecting_children(child, packages, affected_process_factory))
		return processes

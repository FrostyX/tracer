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

# System modules
import re
import psutil
import platform

# Tracer modules
from packageManagers.dnf import Dnf
from packageManagers.yum import Yum
from packageManagers.portage import Portage
from packageManagers.dpkg import Dpkg
from resources.package import Package
from resources.exceptions import UnsupportedDistribution
from resources.rules import Rules
import resources.memory as memory

class Tracer:
	"""Tracer finds outdated running applications in your system"""

	"""List of packages that only should be traced"""
	_specified_packages = None

	"""
	When true, tracer pretends that specified packages have been updated just now.
	Benefit of this is absolutely no need for openning the package history database
	"""
	_now = False

	"""Instance of package manager class. Set by __init__"""
	_PACKAGE_MANAGER = None

	def __init__(self):
		self._PACKAGE_MANAGER = self._PACKAGE_MANAGER()

	def _PACKAGE_MANAGER(self):
		"""Returns instance of package manager according to installed linux distribution"""

		distro = platform.linux_distribution(full_distribution_name=False)[0]
		def e(): raise UnsupportedDistribution(distro)

		return {
			'gentoo': Portage,
			'fedora': Dnf,
			'debian': Dpkg,
		}.get(distro, e)()

	def _modified_packages(self):
		"""Returns list of packages what tracer should care about"""
		if self.specified_packages and self.now:
			return self.specified_packages

		packages = self._PACKAGE_MANAGER.packages_newer_than(psutil.BOOT_TIME)
		if self.specified_packages:
			for package in packages:
				if package not in self.specified_packages:
					packages.remove(package)
		return packages

	def trace_running(self):
		"""
		Returns list of processes which uses some files that have been modified
		@TODO This function should be hardly optimized
		"""

		files_in_memory = memory.processes_with_files()
		packages = self.specified_packages if self.specified_packages and self._now else self._modified_packages()

		running = []
		for package in set(packages):
			for file in self._PACKAGE_MANAGER.package_files(package.name):
				# Doesnt matter what is after dot cause in package files there is version number after it
				try: file = file[:file.index('.')]
				except ValueError: pass

				p = memory.is_in_memory(file, files_in_memory)
				if p and p.create_time <= package.modified:
					p = self._apply_rules(p)
					running.append(p)
					break
		return running

	def _apply_rules(self, process):
		parent = process.parent
		rule = Rules.find(parent.name)

		if not rule or not rule["action"]:
			return process

		if rule["action"] == Rules.ACTIONS["CALL-PARENT"]:
			return self._apply_rules(parent)

		return process


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

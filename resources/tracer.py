# -*- coding: utf-8 -*-

# System modules
import re
import psutil
import platform

# Tracer modules
from packageManagers.dnf import Dnf
from packageManagers.yum import Yum
from packageManagers.portage import Portage
from resources.args_parser import args
from resources.package import Package
import resources.memory as memory

class Tracer:

	_PACKAGE_MANAGER = None
	_specified_packages = None

	def __init__(self):
		self._PACKAGE_MANAGER = self._PACKAGE_MANAGER()

	# Returns instance of package manager according to installed linux distribution
	def _PACKAGE_MANAGER(self):
		def e(): raise OSError("Unknown or unsupported linux distribution")

		distro = platform.linux_distribution(full_distribution_name=False)[0]
		return {
			'gentoo': Portage(),
			'fedora': Dnf(),
		}.get(distro, e)

	# Returns list of packages what tracer should care about
	def _modified_packages(self):
		if self.specified_packages and args.now:
			return self.specified_packages

		packages = self._PACKAGE_MANAGER.packages_newer_than(psutil.BOOT_TIME)
		if self.specified_packages:
			for package in packages:
				if package not in self.specified_packages:
					packages.remove(package)
		return packages

	# Returns list of packages which have some files loaded in memory
	def trace_running(self):
		"""
		Returns list of package names which owns outdated files loaded in memory
		packages -- set of packages, what ONLY should be traced
		@TODO This function should be hardly optimized
		"""

		files_in_memory = memory.processes_with_files()
		packages = self.specified_packages if self.specified_packages and args.now else self._modified_packages()

		modified = []
		for package in packages:
			for file in self._PACKAGE_MANAGER.package_files(package.name):
				# Doesnt matter what is after dot cause in package files there is version number after it
				regex = re.compile('^' + re.escape(file) + "(\.*|$)")
				p = memory.is_in_memory(regex, files_in_memory)
				if p and p.create_time <= package.modified:
					modified.append(package.name)
					break
		return modified

	@property
	def specified_packages(self):
		return self._specified_packages

	@specified_packages.setter
	def specified_packages(self, packages):
		self._specified_packages = packages


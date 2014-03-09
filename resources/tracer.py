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

	PACKAGE_MANAGER = None

	def __init__(self):
		self.PACKAGE_MANAGER = self.package_manager()

	# Returns instance of package manager according to installed linux distribution
	def package_manager(self):
		def e(): raise OSError("Unknown or unsupported linux distribution")

		distro = platform.linux_distribution(full_distribution_name=False)[0]
		return {
			'gentoo': Portage(),
			'fedora': Dnf(),
		}.get(distro, e)

	# Returns list of packages what tracer should care about
	def modified_packages(self, specified_packages=None):
		if specified_packages and args.now:
			return specified_packages

		packages = self.PACKAGE_MANAGER.packages_newer_than(psutil.BOOT_TIME)
		if specified_packages:
			for package in packages:
				if package not in specified_packages:
					packages.remove(package)
		return packages

	# Returns list of packages which have some files loaded in memory
	def trace_running(self, specified_packages=None):
		"""
		Returns list of package names which owns outdated files loaded in memory
		packages -- set of packages, what ONLY should be traced
		@TODO This function should be hardly optimized
		"""

		files_in_memory = memory.processes_with_files()
		packages = specified_packages if specified_packages and args.now else self.modified_packages(specified_packages)

		modified = []
		for package in packages:
			for file in self.PACKAGE_MANAGER.package_files(package.name):
				# Doesnt matter what is after dot cause in package files there is version number after it
				regex = re.compile('^' + re.escape(file) + "(\.*|$)")
				p = memory.is_in_memory(regex, files_in_memory)
				if p and p.create_time <= package.modified:
					modified.append(package.name)
					break
		return modified


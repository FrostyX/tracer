#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tracer finds outdated running packages in your system
# Copyright 2013 Jakub Kadlčík

# Enable importing modules from parent directory (tracer's root directory)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.sys.path.insert(0, parentdir)

# System modules
import sys
import re
import psutil
import platform
import time

# Tracer modules
from packageManagers.dnf import Dnf
from packageManagers.yum import Yum
from packageManagers.portage import Portage
from resources.args_parser import args
from resources.package import Package
import resources.memory as memory

# Returns instance of package manager according to installed linux distribution
def package_manager():
	def e(): raise OSError("Unknown or unsupported linux distribution")

	distro = platform.linux_distribution(full_distribution_name=False)[0]
	return {
		'gentoo': Portage(),
		'fedora': Dnf(),
	}.get(distro, e)

PACKAGE_MANAGER = package_manager()

# Returns list of packages what tracer should care about
def modified_packages(specified_packages=None):
	if specified_packages and args.now:
		return specified_packages

	packages = PACKAGE_MANAGER.packages_newer_than(psutil.BOOT_TIME)
	if specified_packages:
		for package in packages:
			if package not in specified_packages:
				packages.remove(package)
	return packages

# Returns list of packages which have some files loaded in memory
def trace_running(specified_packages=None):
	"""
	Returns list of package names which owns outdated files loaded in memory
	packages -- set of packages, what ONLY should be traced
	@TODO This function should be hardly optimized
	"""

	files_in_memory = memory.processes_with_files()
	packages = specified_packages if specified_packages and args.now else modified_packages(specified_packages)

	modified = []
	for package in packages:
		for file in PACKAGE_MANAGER.package_files(package.name):
			# Doesnt matter what is after dot cause in package files there is version number after it
			regex = re.compile('^' + re.escape(file) + "(\.*|$)")
			p = memory.is_in_memory(regex, files_in_memory)
			if p and p.create_time <= package.modified:
				modified.append(package.name)
				break
	return modified



def main(argv=sys.argv, stdin=[]):
	# If there is something on stdin (that means piped into tracer)
	stdin_packages = []
	if not sys.stdin.isatty():
		stdin_packages = sys.stdin.readline().split()

	# All input packages enchanced by actual time (as modified time)
	packages = []
	for package in args.packages + stdin_packages:
		packages.append(Package(package, time.time() if args.now else None))

	# More times a package is updated the more times it is contained in a package list.
	for package in set(trace_running(packages)):
		print package

if __name__ == '__main__':
	main()

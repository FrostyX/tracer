#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tracer finds outdated running packages in your system
# Copyright 2013 Jakub Kadlčík

# Enable importing modules from parent directory (tracer's root directory)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.sys.path.insert(0, parentdir)

# System modules
import re
import psutil
import platform

# Tracer modules
from packageManagers.yum import Yum
from packageManagers.portage import Portage
import resources.memory as memory

# Returns instance of package manager according to installed linux distribution
def package_manager():
	def e(): raise OSError("Unknown or unsupported linux distribution")

	distro = platform.linux_distribution(full_distribution_name=False)[0]
	return {
		'gentoo': Portage(),
		'fedora': Yum(),
	}.get(distro, e)

PACKAGE_MANAGER = package_manager()

# Returns list of packages what tracer should care about
def modified_packages():
	# Else branch is only for dev and testing purposes
	# Use: if True   or   if not True
	if True:
		packages = PACKAGE_MANAGER.packages_newer_than(psutil.BOOT_TIME)
	else:
		# Lets say these packages were updated
		packages = [
			{'name': 'xterm'},
			{'name': 'ark'},
			{'name': 'kactivities'},
		]
	return packages

# Returns list of packages which have some files loaded in memory
def trace_running():
	"""
	Returns list of package names which owns outdated files loaded in memory
	@TODO This function should be hardly optimized
	"""

	files_in_memory = memory.files_in_memory()
	packages = modified_packages()

	modified = []
	for package in packages:
		for file in PACKAGE_MANAGER.package_files(package['name']):
			# Doesnt matter what is after dot cause in package files there is version number after it
			regex = re.compile('^' + re.escape(file) + "(\.*|$)")
			if memory.is_in_memory(regex, files_in_memory):
				modified.append(package['name'])
				break
	return modified

# More times a package is updated the more times it is contained in a package list.
for package in set(trace_running()):
	print package

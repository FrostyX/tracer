#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tracer finds outdated running packages in your system
# Copyright 2013 Jakub Kadlčík

# Enable importing modules from parent directory (tracer's root directory)
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

# System modules
import re
import psutil

# Tracer modules
from packageManagers.yum import Yum
import resources.memory as memory

PACKAGE_MANAGER = Yum()

# Returns list of packages what tracer should care about
def modified_packages():
	if not True:
		packages = PACKAGE_MANAGER.packages_newer_than(psutil.BOOT_TIME)
	else:
		# Lets say its got from standard input
		packages = [
			{'name': 'xterm'},
			{'name': 'ark'},
			{'name': 'kactivities'},
		]
	return packages

# Returns list of packages which have some files loaded in memory
def trace_running():
	files_in_memory = memory.files_in_memory()
	packages = modified_packages()

	modified = []
	for package in packages:
		for file in PACKAGE_MANAGER._package_files(package['name']):

			regex = re.compile('^' + re.escape(file) + "(\.*|$)")
			if memory.is_in_memory(regex, files_in_memory):
				modified.append(package['name'])
				break;
	return modified

# More times a package is updated the more times it is contained in a package list.
for package in set(trace_running()):
	print package

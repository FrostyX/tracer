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

def modified(manager):
	packages = manager.packages_newer_than(psutil.BOOT_TIME)
	files_in_memory = memory.files_in_memory()

	modified = []
	for package in packages:
		for file in manager._package_files(package['name']):

			regex = re.compile('^' + re.escape(file) + "(\.*|$)")
			if memory.is_in_memory(regex, files_in_memory):
				modified.append(package['name'])
				break;
	return modified

# More times a package is updated the more times it is contained in a package list.
for package in set(modified(Yum())):
	print package

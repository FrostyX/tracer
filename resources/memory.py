#-*- coding: utf-8 -*-
"""Module to work with files in memory
Copyright 2013 Jakub Kadlčík"""

import psutil
import re

def process_files(pid):
	"""
	Returns list of files which are used by process with given pid
	"""
	# By default work only with applications
	paths = ['\/usr/bin', '\/usr/sbin']

	# Work with libs too
	paths.append('\/usr/lib')

	# Make a regex that matches if any of our regexes match.
	combined = "(" + ")|(".join(paths) + ")"

	files = []
	p = psutil.Process(pid)
	for mmap in p.get_memory_maps():
		if re.match(combined, mmap.path):
			files.append(mmap.path)

	return files

def is_in_memory(regex_file, memory):
	"""
	Predicates if file is loaded in memory
	memory -- list given by self.processes_with_files()
	return psutil.Process if true, otherwise False
	@TODO This function should be hardly optimized
	"""
	for process in memory:
		for file in process[1]:
			if regex_file.match(file):
				return process[0]
	return False

def files_in_memory():
	"""
	Returns list of all files loaded in memory
	"""
	files = []
	for pid in psutil.get_pid_list():
		try:
			files += process_files(pid)
		except psutil._error.NoSuchProcess:
			pass

	return set(files)

def processes_with_files():
	"""
	Returns multidimensional list with this pattern - list[psutil.Process][files]
	"""
	processes = []
	for pid in psutil.get_pid_list():
		try:
			processes.append([psutil.Process(pid), process_files(pid)])
		except psutil._error.NoSuchProcess:
			pass
		except psutil._error.AccessDenied:
			pass

	return processes


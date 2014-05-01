#-*- coding: utf-8 -*-
# memory.py
# Module to work with files in memory
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

import resources.psutils as psutil
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
			file = mmap.path

			# Doesnt matter what is after dot cause in package files there is version number after it
			try: file = file[:file.index('.')]
			except ValueError: pass

			# Doesnt matter what is after space cause filename ends with first space
			try: file = file[:file.index(' ')]
			except ValueError: pass

			files.append(file)

	return sorted(files)

def processes_using_file(file, memory):
	"""
	Returns list of processes which have file loaded into memory
	memory -- list given by self.processes_with_files()
	return list of psutil.Process
	@TODO This function should be hardly optimized
	"""
	used_by = []
	for process in memory:
		l = 0
		r = len(process[1])
		while l <= r:
			m = (l + r) / 2
			if m >= len(process[1]): break
			if file == process[1][m]: used_by.append(process[0]); break
			if file < process[1][m]:  r = m - 1
			else: l = m + 1
	return used_by

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

def process_by_name(name):
	for pid in psutil.get_pid_list():
		try:
			p = psutil.Process(pid)
			if p.name == name:
				return p

		except psutil._error.NoSuchProcess: pass
		except psutil._error.AccessDenied: pass

	return None

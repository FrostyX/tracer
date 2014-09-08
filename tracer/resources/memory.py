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

from __future__ import absolute_import

from tracer.resources.psutils import TracerProcess
import psutil
import os


def process_files(pid):
	"""
	Returns list of files which are used by process with given pid
	"""

	files = []
	p = TracerProcess(pid)

	# Files from memory maps
	for mmap in p.get_memory_maps():
		file = mmap.path

		# Doesnt matter what is after space cause filename ends with first space
		try: file = file[:file.index(' ')]
		except ValueError: pass

		# On Gentoo, there is #new after some files in lsof
		# i.e. /usr/bin/gvim#new (deleted)
		if file.endswith('#new'):
			file = file[0:-4]

		files.append(_filename_without_version(file))

	# Process arguments
	for arg in p.cmdline[1:]:
		if os.path.isfile(arg):
			files.append(arg)

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
		except psutil.NoSuchProcess:
			pass

	return set(files)


def processes_with_files():
	"""
	Returns multidimensional list with this pattern - list[psutil.Process][files]
	"""
	processes = []
	for p in all_processes():
		try:
			processes.append([p, process_files(p.pid)])
		except psutil.NoSuchProcess: pass
		except psutil.AccessDenied: pass

	return processes


def dump_memory(user=None):
	"""
	Returns memory in BTree structure

	{ file_1 : [process_1, process_2, ..., process_n],
		...
	}

	Which describes that processes 1 to `n` is using file_1
	"""
	memory = {}
	for process in all_processes(user):
		try:
			for file in process_files(process.pid):
				if file in memory:
					memory[file].append(process)
				else:
					memory[file] = [process]

		except psutil.NoSuchProcess: pass
		except psutil.AccessDenied: pass

	return memory


def process_by_name(name):
	for pid in psutil.get_pid_list():
		try:
			p = TracerProcess(pid)
			if p.name == name:
				return p

		except psutil.NoSuchProcess: pass
		except psutil.AccessDenied: pass

	return None


def all_processes(user=None):
	processes = set()
	for pid in psutil.get_pid_list():
		try:
			p = TracerProcess(pid)
			if not user or p.username == user:
				processes.add(p)
		except psutil.NoSuchProcess: pass
		except psutil.AccessDenied: pass

	return processes


def _filename_without_version(file):
	try:
		slash = file.rindex('/')
		dirname = file[:slash]
		basename = file[slash+1:]

		dot_split = basename.split(".")
		if dot_split[1] == "so":
			basename = dot_split[0] + '.' + dot_split[1]
		else: basename = dot_split[0]
		return dirname + '/' + basename
	except IndexError: pass
	except ValueError: pass
	return file

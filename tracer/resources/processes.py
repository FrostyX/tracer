#-*- coding: utf-8 -*-
# processes.py
# Module providing informations about processes
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

from collections import ProcessesCollection
from FilenameCleaner import FilenameCleaner
import psutil
import datetime
import time
import os


class Processes(object):

	@staticmethod
	def all():
		processes = ProcessesCollection()
		for pid in psutil.get_pid_list():
			try:
				processes.append(Process(pid))
			except psutil.NoSuchProcess: pass
			except psutil.AccessDenied: pass
		return processes


class Process(psutil.Process):
	def __eq__(self, process):
		"""For our purposes, two processes are equal when they have same name"""
		return self.pid == process.pid

	def __ne__(self, process):
		return not self.__eq__(process)

	def __hash__(self):
		return hash(self.pid)

	@property
	def files(self):
		files = []

		# Files from memory maps
		for mmap in self.get_memory_maps():
			files.append(FilenameCleaner.strip(mmap.path))

		# Process arguments
		for arg in self.cmdline[1:]:
			if os.path.isfile(arg):
				files.append(arg)

		return sorted(files)

	@property
	def parent(self):
		p = super(Process, self).parent
		if p:
			p.__class__ = Process
		return p

	@property
	def username(self):
		# User who run the process can be deleted
		try:
			return super(Process, self).username
		except KeyError:
			return None

	def get_children(self, recursive=False):
		children = super(Process, self).get_children(recursive)
		for child in children:
			child.__class__ = Process
		return ProcessesCollection(children)

	@property
	def exe(self):
		# On Gentoo, there is #new after some files in lsof
		# i.e. /usr/bin/gvim#new (deleted)
		exe = super(Process, self).exe
		if exe.endswith('#new'):
			exe = exe[0:-4]

		# On Fedora, there is something like ;541350b3 after some files in lsof
		if ';' in exe:
			exe = exe[0:exe.index(';')]

		return exe

	@property
	def str_started_ago(self):
		now = datetime.datetime.fromtimestamp(time.time())
		started = datetime.datetime.fromtimestamp(self.create_time)
		started = now - started

		started_str = ""
		if started.days > 0:
			started_str = str(started.days) + " days"
		elif started.seconds >= 60 * 60:
			started_str = str(started.seconds / (60 * 60)) + " hours"
		elif started.seconds >= 60:
			started_str = str(started.seconds / 60) + " minutes"
		elif started.seconds >= 0:
			started_str = str(started.seconds) + " seconds"

		return started_str


class AffectedProcess(Process):
	packages = None
	files = None

	def __init__(self, pid=None):
		Process.__init__(self, pid)
		self.packages = set()
		self.files = set()

	def update(self, process):
		self.files = self.files.union(process.files)
		self.packages = self.packages.union(process.packages)

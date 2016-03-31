#-*- coding: utf-8 -*-
# processes.py
# Module providing informations about processes
#
# Copyright (C) 2013 Jakub Kadlcik
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

from .collections import ProcessesCollection
from .FilenameCleaner import FilenameCleaner
import psutil
import datetime
import time
import os


class Processes(object):

	# psutil 3.x to 1.x backward compatibility
	@staticmethod
	def pids():
		try:
			return psutil.pids()
		except AttributeError:
			return psutil.get_pid_list()

	@staticmethod
	def all():
		processes = ProcessesCollection()
		for pid in Processes.pids():
			try:
				processes.append(Process(pid))
			except psutil.NoSuchProcess: pass
			except psutil.AccessDenied: pass
		return processes


class ProcessWrapper(object):
	"""
	Wrapper for ``psutil.Process class``
	Library ``psutil`` is not backward compatible from version 2.x.x to 1.x.x.

	Purpose of this class is cover incompatibility in ``psutil.Process`` class and
	provide interface of new version. It allows using new interface even with
	old version of ``psutil``.
	"""

	_process = None

	def __init__(self, pid=None):
		self._process = psutil.Process(pid)

	def __nonzero__(self):
		return bool(self._process)

	def name(self):
		return self._attr("name")

	def exe(self):
		return self._attr("exe")

	def cmdline(self):
		return self._attr("cmdline")

	def ppid(self):
		return self._attr("ppid")

	def parent(self):
		return self._attr("parent")

	def username(self):
		return self._attr("username")

	def create_time(self):
		return self._attr("create_time")

	def children(self, recursive=False):
		try: return self._process.children()
		except AttributeError: return self._process.get_children()

	def _attr(self, name):
		attr = getattr(self._process, name)
		try: return attr()
		except TypeError: return attr

	def __getattr__(self, item):
		return getattr(self._process, item)

	# psutil 3.x to 1.x backward compatibility
	def memory_maps(self, grouped=True):
		try: return self._process.memory_maps(grouped=grouped)
		except AttributeError: return self._process.get_memory_maps()


class Process(ProcessWrapper):
	"""
	Represent the process instance uniquely identifiable through PID

	For all class properties and methods, please see
	http://pythonhosted.org/psutil/#process-class

	Bellow listed are only reimplemented ones.
	"""

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
		for mmap in self.memory_maps():
			files.append(FilenameCleaner.strip(mmap.path))

		# Process arguments
		for arg in self.cmdline()[1:]:
			if os.path.isfile(arg):
				files.append(arg)

		return sorted(files)

	def parent(self):
		"""The parent process casted from ``psutil.Process`` to tracer ``Process``"""
		if self.ppid():
			return Process(self.ppid())
		return None

	def username(self):
		"""The user who owns the process. If user was deleted in the meantime,
		``None`` is returned instead."""

		# User who run the process can be deleted
		try:
			return super(Process, self).username()
		except KeyError:
			return None

	def children(self, recursive=False):
		"""The collection of process's children. Each of them casted from ``psutil.Process``
		to tracer ``Process``."""
		children = super(Process, self).children(recursive)
		return ProcessesCollection([Process(child.pid) for child in children])

	@property
	def exe(self):
		"""The absolute path to process executable. Cleaned from arbitrary strings
		which appears on the end."""

		# On Gentoo, there is #new after some files in lsof
		# i.e. /usr/bin/gvim#new (deleted)
		exe = super(Process, self).exe()
		if exe.endswith('#new'):
			exe = exe[0:-4]

		# On Fedora, there is something like ;541350b3 after some files in lsof
		if ';' in exe:
			exe = exe[0:exe.index(';')]

		return exe

	@property
	def str_started_ago(self):
		"""
		The time of how long process is running. Returned as string
		in format ``XX unit`` where unit is one of
		``days`` | ``hours`` | ``minutes`` | ``seconds``
		"""

		now = datetime.datetime.fromtimestamp(time.time())
		started = datetime.datetime.fromtimestamp(self.create_time())
		started = now - started

		started_str = ""
		if started.days > 0:
			started_str = str(started.days) + " days"
		elif started.seconds >= 60 * 60:
			started_str = str(int(started.seconds / (60 * 60))) + " hours"
		elif started.seconds >= 60:
			started_str = str(int(started.seconds / 60)) + " minutes"
		elif started.seconds >= 0:
			started_str = str(int(started.seconds)) + " seconds"

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

#-*- coding: utf-8 -*-
# processes.py
# Module providing informations about processes
#
# Copyright (C) 2016 Jakub Kadlcik
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
from subprocess import PIPE, Popen
from threading import Timer
from six import with_metaclass


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

	Note that, for performance reasons, process information is cached at
	object creation. To force a refresh, invoke the ``rebuild_cache()``
	method.
	"""

	def __init__(self, pid=None):
		self._process = psutil.Process(pid)
		self.rebuild_cache()

	def __nonzero__(self):
		return bool(self._process)

	def rebuild_cache(self):
		self._procdict = self._process.as_dict(attrs=['name', 'exe', 'cmdline', 'ppid', 'username', 'create_time'])

	def name(self):
		# Special case for sshd, if its cmd contains the execuatable is must be the daemon
		# else must be the session.
		try:
			if self._attr("name") == 'sshd':
				if self._attr("exe") not in self._attr("cmdline") and len(self._attr("cmdline")) > 1:
					username= self._attr("cmdline")[1].split("@")[0]
					return 'ssh-{0}-session'.format(username)
		except psutil.AccessDenied:
			pass
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
		key = 'children-{0}'.format(recursive)
		if key not in self._procdict:
			try:
				self._procdict[key] = self._process.children(recursive)
			except AttributeError:
				self._procdict[key] = self._process.get_children(recursive)
		return self._procdict[key]

	def _attr(self, name):
		if name not in self._procdict:
			attr = getattr(self._process, name)
			try:
				self._procdict[name] = attr()
			except TypeError:
				self._procdict[name] = attr
		return self._procdict[name]

	def __getattr__(self, item):
		return getattr(self._process, item)

	# psutil 3.x to 1.x backward compatibility
	def memory_maps(self, grouped=True):
		key = 'memory_maps-{0}'.format(grouped)
		if key not in self._procdict:
			try:
				self._procdict[key] = self._process.memory_maps(grouped=grouped)
			except AttributeError:
				self._procdict[key] = self._process.get_memory_maps(grouped=grouped)
		return self._procdict[key]


class ProcessMeta(type):
	"""
	Caching metaclass that ensures that only one ``Process`` object is ever
	instantiated for any given PID. The cache can be cleared by calling
	``Process.reset_cache()``.

	Based on https://stackoverflow.com/a/33458129
	"""

	def __init__(cls, name, bases, attributes):
		super(ProcessMeta, cls).__init__(name, bases, attributes)
		def reset_cache():
			cls._cache = {}
		reset_cache()
		setattr(cls, 'reset_cache', reset_cache)

	def __call__(cls, *args, **kwargs):
		pid = args[0]
		if pid not in cls._cache:
			self = cls.__new__(cls, *args, **kwargs)
			cls.__init__(self, *args, **kwargs)
			cls._cache[pid] = self
		return cls._cache[pid]


class Process(with_metaclass(ProcessMeta, ProcessWrapper)):
	"""
	Represent the process instance uniquely identifiable through PID

	For all class properties and methods, please see
	http://pythonhosted.org/psutil/#process-class

	Below listed are only reimplemented ones.

	For performance reasons, instances are cached based on PID, and
	multiple instantiations of a ``Process`` object with the same PID will
	return the same object. To clear the cache, invoke
	``Process.reset_cache()``. Additionally, as with ``ProcessWrapper``,
	process information is cached at object creation. To force a refresh,
	invoke the ``rebuild_cache()`` method on the object.
	"""

	def __eq__(self, process):
		"""For our purposes, two processes are equal when they have same name"""
		return self.pid == process.pid

	def __ne__(self, process):
		return not self.__eq__(process)

	def __hash__(self):
		return hash(self.pid)

	@staticmethod
	def safe_isfile(file_path, timeout=0.5):
		"""
		Process arguments could be referring to files on remote filesystems and
		os.path.isfile will hang forever if the shared FS is offline.
		Instead, use a subprocess that we can time out if we can't reach some file.
		"""
		process = Popen(['test', '-f', file_path], stdout=PIPE, stderr=PIPE)
		timer = Timer(timeout, process.kill)
		try:
			timer.start()
			process.communicate()
			return process.returncode == 0
		finally:
			timer.cancel()

	@property
	def files(self):
		files = []

		# Files from memory maps
		for mmap in self.memory_maps():
			files.append(FilenameCleaner.strip(mmap.path))

		# Process arguments
		for arg in self.cmdline()[1:]:
			if not os.path.isabs(arg):
				continue

			if Process.safe_isfile(arg):
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
	def is_interpreted(self):
		# @TODO implement better detection of interpreted processes
		return self.name() in ["python"]

	@property
	def is_session(self):
		terminal = self.terminal()
		if terminal is None:
			return None
		parent = self.parent()
		if parent is None or terminal != parent.terminal():
			return True

	@property
	def real_name(self):
		if self.is_interpreted:
			for arg in self.cmdline()[1:]:
				if os.path.isfile(arg):
					return os.path.basename(arg)
		return self.name()

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

from __future__ import absolute_import

import os
from tracer.resources.applications import Applications


class ProcessesList(list):

	"""
	`Application` objects for contained processes

	_applications = {
		process.pid: Application(name=process.name),
		...
	}
	"""
	_applications = {}

	"""
	Overrited methods
	"""
	def __init__(self, *args):
		list.__init__(self, *args)
		for process in self:
			self._applications[process.pid] = Applications.find(process.name)
			self._set_application_sudo_helper(process)

	def append(self, x):
		self._applications[x.pid] = Applications.find(x.name)
		self._set_application_sudo_helper(x)
		super(ProcessesList, self).append(x)

	def insert(self, i, x):
		self._applications[x.pid] = Applications.find(x.name)
		self._set_application_sudo_helper(x)
		super(ProcessesList, self).insert(i, x)

	def extend(self, t):
		for x in t:
			self._applications[x.pid] = Applications.find(x.name)
			self._set_application_sudo_helper(x)
		super(ProcessesList, self).extend(t)

	def remove(self, x):
		del self._applications[x.pid]
		super(ProcessesList, self).remove(x)

	def pop(self, i=-1):
		del self._applications[self[i].pid]
		return super(ProcessesList, self).pop(i)

	"""
	Added methods
	"""
	def application(self, process):
		return self._applications[process.pid]

	def exclude_type(self, app_type):
		"""app_type -- see Applications.TYPES"""
		return self.exclude_types([app_type])

	def exclude_types(self, app_types):
		"""app_types -- see Applications.TYPES"""
		without = ProcessesList()
		for p in self:
			a = Applications.find(p.name)
			if a.type not in app_types:
				without.append(p)
		return without

	def count_type(self, app_type):
		count = 0
		for p in self:
			a = Applications.find(p.name)
			if a.type == app_type:
				count += 1
		return count

	def with_helpers(self):
		processes = ProcessesList()
		for p in self:
			if self._applications[p.pid].helper:
				processes.append(p)
		return processes

	def without_helpers(self):
		processes = ProcessesList()
		for p in self:
			if not self._applications[p.pid].helper:
				processes.append(p)
		return processes

	def _set_application_sudo_helper(self, process):
		if os.getlogin() != "root":
			helper = self._applications[process.pid].helper
			if helper and not helper.startswith("sudo "):
				self._applications[process.pid].helper = "sudo " + helper

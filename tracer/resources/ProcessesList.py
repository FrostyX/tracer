from __future__ import absolute_import

import os
from tracer.resources.applications import Applications
from operator import attrgetter


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
			self._add(process)

	def append(self, x):
		if self._add(x):
			super(ProcessesList, self).append(x)

	def insert(self, i, x):
		if self._add(x):
			super(ProcessesList, self).insert(i, x)

	def extend(self, t):
		for x in t:
			if not self._add(x):
				t.remove(x)
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

	def sorted(self, attribute):
		return sorted(self, key=attrgetter(attribute))

	def _add(self, x):
		application = Applications.find(x.name)
		if not application.ignore:
			self._applications[x.pid] = application
			self._set_application_sudo_helper(x)
			return True
		return False

	def _set_application_sudo_helper(self, process):
		if os.getlogin() != "root" and self._applications[process.pid].type == Applications.TYPES['DAEMON']:
			helper = self._applications[process.pid].helper
			if helper and not helper.startswith("sudo "):
				self._applications[process.pid].helper = "sudo " + helper

from __future__ import absolute_import

from tracer.resources.applications import Applications


class ProcessesList(list):

	def __init__(self, *args):
		list.__init__(self, *args)

	def exclude_type(self, app_type):
		"""app_type -- see Applications.TYPES"""
		return self.exclude_types([app_type])

	def exclude_types(self, app_types):
		"""app_types -- see Applications.TYPES"""
		without = []
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

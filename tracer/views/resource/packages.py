from __future__ import unicode_literals

from .. import View
from datetime import datetime


class PackagesView(View):
	def render(self):
		line = "{0: <15}{1: <10}{2: <40}"
		print(line.format("Date", "Time", "Package name"))
		print(55 * "-")
		for package in self.args.packages:
			modified = datetime.fromtimestamp(package.modified)
			date = modified.strftime('%Y-%m-%d')
			time = modified.strftime('%H:%M')
			print(line.format(date, time, package.name))

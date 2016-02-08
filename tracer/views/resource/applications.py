from __future__ import unicode_literals

from .. import View


class ApplicationsView(View):
	def render(self):
		line = "{0:<40}{1:<20}{2:<10}{3:<50}"
		print(line.format("Application", "Type", "Ignore", "Helper"))
		print(120 * "-")
		for application in self.args.applications:
			print(line.format(application.name, application.type, application.ignore, application.helper or ""))

from __future__ import unicode_literals

from .. import View


class SystemView(View):
	def render(self):
		line = "{0:<20}{1}"
		print(line.format("Python:", self.args.python))
		print(line.format("Distribution:", self.args.distribution))
		print(line.format("Package Manager:", ", ".join(self.args.package_managers)))
		print(line.format("Init system:", self.args.init))
		print(line.format("Uptime:", self.args.uptime))
		print(line.format("User:", self.args.user))

		if len(self.args.users) > 1:
			print(line.format("Users:", self.args.users))

		print("")
		print(line.format("Tracer version:", self.args.version))
		print(line.format("Rules:", self.args.rules_count))
		print(line.format("Applications:", self.args.applications_count))

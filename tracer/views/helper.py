from __future__ import print_function
from __future__ import unicode_literals

from . import View
from tracer.resources.lang import _


class HelperView(View):
	def render(self):

		print("* {app_name}"                       .format(app_name=self.args.application.name), file=self.out)

		# Package informations
		if self.args.package:
			print("    Package:     {pkg_name}"        .format(pkg_name=self.args.package.name), file=self.out)
			print("    Description: {pkg_description}" .format(pkg_description=self.args.package.description), file=self.out)
			print("    Type:        {type}"            .format(type=self.args.application.type.capitalize()), file=self.out)
		else:
			print("    Package:     {app_name} is not provided by any package"
				.format(app_name=self.args.application.name), file=self.out)

		# State
		indent = "    State:       "
		i = 0
		for process in self.args.processes:
			print(indent + "{app_name} has been started by {user} {time} ago. PID - {pid}".format(
					app_name=self.args.application.name,
					user=process.username(),
					time=process.str_started_ago,
					pid=process.pid
			), file=self.out)
			indent = "                 "
			i += 1
			if i >= 3:
				print("                 ...", file=self.out)
				break

		# Affected by
		if self.args.args.verbose > 0:
			print("", file=self.out)
			self.render_affected_by()

		# How to restart
		if self.args.application.helper or self.args.affects:
			print("", file=self.out)
			print("    {title}:".format(title=_('How to restart')), file=self.out)
			if not self.args.affected_by:
				print("        {app_name} does not need restarting".format(app_name=self.args.application.name), file=self.out)
			elif self.args.affects:
				print("        ", _("It's a part of application called {0}").format(self.args.affects), file=self.out)
			else:
				for helper in self.args.application.helpers:
					print("        {how_to_restart}".format(how_to_restart=helper), file=self.out)

	def render_affected_by(self):
		default_level = 2
		indent = "    "
		print(indent + _("Affected by") + ":", file=self.out)

		if type(self.args.affected_by) == str:
			print(default_level * indent + self.args.affected_by, file=self.out)
			return

		for process in self.args.affected_by:
			indent_level = default_level

			if process not in self.args.processes:
				print(indent_level * indent + "{0} ({1})".format(process.name(), process.pid), file=self.out)
				indent_level += 1

			for package in process.packages:
				print(indent_level * indent + package.name, file=self.out)

				if self.args.args.verbose < 2:
					continue

				indent_level += 1
				for file in package.files:
					print(indent_level * indent + file, file=self.out)

				indent_level -= 1

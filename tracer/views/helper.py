from __future__ import print_function
from __future__ import unicode_literals

from . import View
from tracer.resources.lang import _


class HelperView(View):
	def render(self):

		self.print("* {app_name}".format(app_name=self.args.application.name))

		# Package informations
		if self.args.package:
			self.print("    Package:     {pkg_name}"        .format(pkg_name=self.args.package.name))
			self.print("    Description: {pkg_description}" .format(pkg_description=self.args.package.description))
			self.print("    Type:        {type}"            .format(type=self.args.application.type.capitalize()))
			if self.args.application.affected_instances:
				self.print("    Executable:  {executable}".format(executable=self.args.application.affected_instances[0].exe))
		else:
			self.print("    Package:     {app_name} is not provided by any package"
				.format(app_name=self.args.application.name))

		# State
		indent = "    State:       "
		i = 0
		for process in self.args.processes:
			self.print(indent + "{app_name} has been started by {user} {time} ago. PID - {pid}".format(
					app_name=self.args.application.name,
					user=process.username(),
					time=process.str_started_ago,
					pid=process.pid
			))
			indent = "                 "
			i += 1
			if i >= 3:
				self.print("                 ...")
				break

		# Affected by
		if self.args.args.verbose > 0:
			self.print("")
			self.render_affected_by()

		# How to restart
		if self.args.application.helper or self.args.affects:
			self.print("")
			self.print("    {title}:".format(title=_('How to restart')))
			if not self.args.affected_by:
				self.print("        {app_name} does not need restarting".format(app_name=self.args.application.name))
			elif self.args.affects:
				self.print("        " + _("It's a part of application called {0}").format(self.args.affects))
			else:
				for helper in self.args.application.helpers:
					self.print("        {how_to_restart}".format(how_to_restart=helper))

				if self.args.application.note:
					self.print("\n       - " + self.args.application.note)

	def render_affected_by(self):
		default_level = 2
		indent = "    "
		self.print(indent + _("Affected by") + ":")

		if type(self.args.affected_by) == str:
			self.print(default_level * indent + self.args.affected_by)
			return

		printed_packages = set()
		for process in self.args.affected_by:
			indent_level = default_level

			if process not in self.args.processes:
				self.print(indent_level * indent + "{0} ({1})".format(process.name(), process.pid))
				indent_level += 1

			for package in process.packages:
				if package.name not in printed_packages or indent_level > 2:
					self.print(indent_level * indent + package.name)
					printed_packages.add(package.name)

				if self.args.args.verbose < 2:
					continue

				indent_level += 1
				for file in package.files:
					self.print(indent_level * indent + file)

				indent_level -= 1

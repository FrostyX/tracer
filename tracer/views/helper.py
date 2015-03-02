from . import View
from tracer.resources.lang import _


class HelperView(View):
	def render(self):

		print >>self.out, "* {app_name}"                       .format(app_name=self.args.application.name)

		# Package informations
		if self.args.package:
			print >>self.out, "    Package:     {pkg_name}"        .format(pkg_name=self.args.package.name)
			print >>self.out, "    Description: {pkg_description}" .format(pkg_description=self.args.package.description)
			print >>self.out, "    Type:        {type}"            .format(type=self.args.application.type.capitalize())
		else:
			print >>self.out, "    Package:     {app_name} is not provided by any package".format(app_name=self.args.application.name)

		# State
		indent = "    State:       "
		i = 0
		for process in self.args.processes:
			print >>self.out, indent + "{app_name} has been started by {user} {time} ago. PID - {pid}".format(
					app_name=self.args.application.name,
					user=process.username(),
					time=process.str_started_ago,
					pid=process.pid
			)
			indent = "                 "
			i += 1
			if i >= 3:
				print >>self.out, "                 ..."
				break

		# Affected by
		if self.args.args.verbose > 0:
			print >>self.out, ""
			self.render_affected_by()

		# How to restart
		if self.args.application.helper:
			print >>self.out, ""
			print >>self.out, "    {title}:".format(title=_('how_to_restart'))

			if not self.args.affected_by:
				print >>self.out, "        {app_name} does not need restarting".format(app_name=self.args.application.name)
			else:
				for helper in self.args.application.helpers:
					print >>self.out, "        {how_to_restart}".format(how_to_restart=helper)

	def render_affected_by(self):

		indent = "    "
		print >>self.out, indent + _("affected_by") + ":"

		indent_level = 2
		if type(self.args.affected_by) == str:
			print >>self.out, indent_level * indent + self.args.affected_by
			return

		for process in self.args.affected_by:
			if process not in self.args.processes:
				print >>self.out, indent_level * indent + "{0} ({1})".format(process.name(), process.pid)
				indent_level += 1

			for package in process.packages:
				print >>self.out, indent_level * indent + package.name

				if self.args.args.verbose < 2:
					continue

				indent_level += 1
				for file in package.files:
					print >>self.out, indent_level * indent + file

				indent_level -= 1

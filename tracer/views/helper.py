from . import View
from tracer.resources.lang import _


class HelperView(View):
	def render(self):

		print "* {app_name}"                       .format(app_name=self.args.application.name)

		# Package informations
		if self.args.package:
			print "    Package:     {pkg_name}"        .format(pkg_name=self.args.package.name)
			print "    Description: {pkg_description}" .format(pkg_description=self.args.package.description)
			print "    Type:        {type}"            .format(type=self.args.application.type.capitalize())
		else:
			print "    Package:     {app_name} is not provided by any package".format(app_name=self.args.application.name)

		# State
		print "    State:       {app_name} has been started by {user} {time} ago. PID - {pid}".format(
				app_name=self.args.application.name,
				user=self.args.process.username,
				time=self.args.time,
				pid=self.args.process.pid
		)

		# Affected by
		if self.args.args.verbose > 0:
			print ""
			self.render_affected_by()

		# How to restart
		if self.args.application.helper:
			print ""
			print "    {title}:".format(title=_('how_to_restart'))

			if not self.args.affected_by:
				print "        {app_name} does not need restarting".format(app_name=self.args.application.name)
			else:
				print "        {how_to_restart}".format(how_to_restart=self.args.application.helper)

	def render_affected_by(self):

		indent = "    "
		print indent + _("affected_by") + ":"

		indent_level = 2
		if type(self.args.affected_by) == str:
			print indent_level * indent + self.args.affected_by
			return

		for process in self.args.affected_by:
			if process != self.args.process:
				print indent_level * indent + "{0} ({1})".format(process.name, process.pid)
				indent_level += 1

			for package in self.args.affected_by[process]:
				print indent_level * indent + package

				if self.args.args.verbose < 2:
					continue

				indent_level += 1
				for file in self.args.affected_by[process][package]:
					print indent_level * indent + file

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
			print "        {how_to_restart}".format(how_to_restart=self.args.application.helper)

	def render_affected_by(self):

		indent = "    "
		print indent + _("affected_by") + ":"

		if type(self.args.affected_by) == str:
			print 2 * indent + self.args.affected_by
			return

		for package in self.args.affected_by:
			print 2 * indent + package

			if self.args.args.verbose < 2:
				continue

			for file in self.args.affected_by[package]:
				print 3 * indent + file

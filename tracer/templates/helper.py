from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
import tracer.templates.note_for_hidden

def render(args=None, process=None, application=None, package=None, time=None, affected_by=None, how_to_restart=None):

	print "* {app_name}"                       .format(app_name=application['name'])

	# Package informations
	print "    Package:     {pkg_name}"        .format(pkg_name=package.name)
	print "    Description: {pkg_description}" .format(pkg_description=package.description)
	print "    Type:        {type}"            .format(type=application['type'].capitalize())

	# State
	print "    State:       {app_name} has been started by {user} {time} ago. PID - {pid}".format(
			app_name=application['name'],
			user=process.username,
			time=time,
			pid=process.pid
	)

	# Affected by
	if args.verbose > 0:
		print ""
		render_affected_by(args=args, affected_by=affected_by)

	# How to restart
	print ""
	print "    {title}:".format(title=_('how_to_restart'))
	print "        {how_to_restart}".format(how_to_restart=how_to_restart)




def render_affected_by(args=None, affected_by=None):

	indent = "    "
	print indent + _("affected_by") + ":"

	if type(affected_by) == str:
		print 2 * indent + affected_by
		return

	for package in affected_by:
		print 2 * indent + package

		if args.verbose < 2:
			continue

		for file in affected_by[package]:
			print 3 * indent + file

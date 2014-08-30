from tracer.resources.lang import _
import tracer.views.note_for_hidden


def render(processes=None, args=None, total_count=None, session_count=None, static_count=None):

	# If there are only hidden applications (any listed)
	if total_count != session_count + static_count:
		print _("you_should_restart")

	for process in processes:
		print "  " + _(process.name)

	if not args.all: tracer.views.note_for_hidden.render(
		args = args,
		total_count = total_count,
		session_count = session_count,
		static_count = static_count
	)

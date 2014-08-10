from tracer.resources.lang import _
import tracer.templates.note_for_hidden

def render(processes=None, args=None, total_count=None, session_count=None, static_count=None):

	print _("you_should_restart")

	for process in processes:
		print "  " + _(process.name)

	if not args.all: tracer.templates.note_for_hidden.render(
		args = args,
		total_count = total_count,
		session_count = session_count,
		static_count = static_count
	)

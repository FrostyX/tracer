from tracer.resources.lang import _
import tracer.templates.note_for_hidden


def render(processes=None, args=None, total_count=None, session_count=None, static_count=None):
	i = 1
	digits = len(str(len(processes)))
	for process in processes:
		n = "[{0}]".format(i).ljust(digits + 2)
		print "{} {}".format(n, process.name)
		i += 1

	if not args.all: tracer.templates.note_for_hidden.render(
		args = args,
		total_count = total_count,
		session_count = session_count,
		static_count = static_count
	)

	print "\n" + _("prompt_help")

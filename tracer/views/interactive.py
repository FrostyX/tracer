from tracer.resources.lang import _
from tracer.views.note_for_hidden import NoteForHiddenView


class InteractiveView(object):
	def render(self, processes=None, args=None, total_count=None, session_count=None, static_count=None):
		i = 1
		digits = len(str(len(processes)))
		for process in processes:
			n = "[{0}]".format(i).ljust(digits + 2)
			print "{} {}".format(n, process.name)
			i += 1

		view = NoteForHiddenView()
		if not args.all: view.render(
			args = args,
			total_count = total_count,
			session_count = session_count,
			static_count = static_count
		)

		print "\n" + _("prompt_help")

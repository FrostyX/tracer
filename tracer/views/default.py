from . import View
from tracer.resources.lang import _
from tracer.views.note_for_hidden import NoteForHiddenView


class DefaultView(View):
	def render(self):

		# If there are only hidden applications (any listed)
		if self.args.total_count != self.args.session_count + self.args.static_count:
			print _("you_should_restart")

		for process in self.args.processes:
			print "  " + process.name

		if not self.args.args.all:
			view = NoteForHiddenView()
			view.assign("args", self.args.args)
			view.assign("total_count", self.args.total_count)
			view.assign("session_count", self.args.session_count)
			view.assign("static_count", self.args.static_count)
			view.render()

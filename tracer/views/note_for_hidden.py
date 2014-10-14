from . import View
from tracer.resources.lang import _


class NoteForHiddenView(View):
	def render(self):

		if not self.args.args.quiet and (self.args.session_count > 0 or self.args.static_count > 0):

			print _("note_unlisted_apps")
			if self.args.session_count > 0:
				print _("requires_session").format(self.args.session_count)

			if self.args.static_count > 0:
				print _("requires_reboot").format(self.args.static_count)


from . import View
from tracer.resources.lang import _


class NoteForHiddenView(View):
	def render(self):

		if not self.args.args.quiet and (self.args.session_count > 0 or self.args.static_count > 0):

			if self.args.session_count + self.args.static_count == self.args.total_count:
				print >>self.out, _("note_unlisted_apps_short")
			else:
				print >>self.out, _("note_unlisted_apps")

			if self.args.session_count > 0:
				print >>self.out, _("requires_session").format(self.args.session_count)

			if self.args.static_count > 0:
				print >>self.out, _("requires_reboot").format(self.args.static_count)


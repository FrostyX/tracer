from . import View
from tracer.resources.lang import _


class NoteForHiddenView(View):
	def render(self):

		if not self.args.args.quiet and (self.args.session_count > 0 or self.args.static_count > 0):

			# If there are only hidden applications (any listed)
			if self.args.total_count != self.args.session_count + self.args.static_count:
				print ""

			print _("note_unlisted_apps")
			if self.args.session_count > 0:
				print _("requires_session").format(self.args.session_count)

			if self.args.static_count > 0:
				print _("requires_reboot").format(self.args.static_count)


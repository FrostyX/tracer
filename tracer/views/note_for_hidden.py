from __future__ import print_function

from . import View
from tracer.resources.lang import _


class NoteForHiddenView(View):
	def render(self):

		if not self.args.args.quiet and (self.args.session_count > 0 or self.args.static_count > 0):

			if self.args.session_count + self.args.static_count == self.args.total_count:
				print(_("There are:"), file=self.out)
			else:
				print(_("Additionally to those process above, there are:"), file=self.out)

			if self.args.session_count > 0:
				print("  - " + \
					_("{0} processes requiring restart of your session (i.e. Logging out & Logging in again)")\
						.format(self.args.session_count),
					file=self.out
				)

			if self.args.static_count > 0:
				print >>self.out, "  - " + _("{0} processes requiring reboot").format(self.args.static_count)


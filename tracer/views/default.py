from __future__ import print_function

from . import View
from tracer.resources.lang import _
from tracer.resources.applications import Applications
from tracer.views.note_for_hidden import NoteForHiddenView
from tracer.views.blocks import BlocksView
from io import StringIO
import re


class DefaultView(View):
	def render(self):

		def with_helpers_content():
			content = ""
			types = [Applications.TYPES["SESSION"], Applications.TYPES["STATIC"]]
			applications = self.args.applications.with_helpers().exclude_types(types).sorted("helper")
			for application in applications:
				helpers = "; ".join(application.helpers)
				if application.helper_contains_formating and not application.helper_contains_name:
					helpers += "  # {}".format(application.name)
				content += "      " + helpers + "\n"
			return content

		def without_helpers_content():
			content = ""
			for application in self.args.applications.without_helpers().sorted("name"):
				content += "      " + application.name + "\n"
			return content

		def unrestartable_content(app_type):
			content = ""
			applications = self.args.applications.with_helpers().filter_types([app_type]).sorted("name")
			for application in applications:
				content += "      " + application.name + "\n"
			return content

		def note_content():
			content = StringIO.StringIO()
			view = NoteForHiddenView(content)
			view.assign("args", self.args.args)
			view.assign("total_count", len(self.args.applications))
			view.assign("session_count", self.args.applications.count_type(Applications.TYPES["SESSION"]))
			view.assign("static_count", self.args.applications.count_type(Applications.TYPES["STATIC"]))
			view.render()
			return content.getvalue()

		blocks = [
			{"title": "  * " + _("Some applications using:"), "content": with_helpers_content()},
			{"title": "  * " + _("These applications manually:"), "content": without_helpers_content()},
		]

		if self.args.args.all:
			blocks.append({
				"title": "  * " + _("These applications restarting your session:"),
				"content": unrestartable_content(Applications.TYPES["SESSION"])
			})
			blocks.append({
				"title": "  * " + _("These applications rebooting your computer:"),
				"content": unrestartable_content(Applications.TYPES["STATIC"])
			})
		else:
			blocks.append({"content": note_content()})

		view = BlocksView(self.out)
		view.assign("blocks", blocks)
		if view.has_content():
			print(_("You should restart:"), file=self.out)
		view.render()

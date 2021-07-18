from __future__ import print_function
from __future__ import unicode_literals

from . import View
from tracer.resources.lang import _
from tracer.resources.applications import Applications
from tracer.views.note_for_hidden import NoteForHiddenView
from tracer.views.blocks import BlocksView
from tracer.resources.pycomp import StringIO
from sys import version_info
import re


class DefaultView(View):
	def render(self):

		def with_helpers_content():
			content = ""
			types = [Applications.TYPES["SESSION"], Applications.TYPES["STATIC"], Applications.TYPES["ERASED"]]
			applications = (self.args.applications
							.with_helpers()
							.exclude_types(types)
							.unique()
							.sorted("helper"))
			for application in applications:
				helpers = "; ".join(application.helpers)
				if application.helper_contains_formating and not application.helper_contains_name:
					helpers += "  # {}".format(application.name)
				content += "      " + helpers + "\n"
			return content

		def without_helpers_content():
			content = ""
			apps = (self.args.applications
					.exclude_types(Applications.TYPES["ERASED"])
					.unique()
					.without_helpers()
					.sorted("name"))
			for application in apps:
				content += "      " + application.name + "\n"
			return content

		def erased_content():
			content = ""
			apps = (self.args.applications
					.filter_types([Applications.TYPES["ERASED"]])
					.unique()
					.sorted("name"))
			for application in apps:
				content += "      " + application.name + "\n"
			return content

		def unrestartable_content(app_type):
			content = ""
			applications = (self.args.applications
							.with_helpers()
							.filter_types([app_type])
							.unique()
							.sorted("name"))
			for application in applications:
				content += "      " + application.name + "\n"
			return content

		def note_content():
			content = StringIO()
			view = NoteForHiddenView(content)
			view.assign("args", self.args.args)
			view.assign("total_count", len(self.args.applications))
			view.assign("session_count", self.args.applications.count_type(Applications.TYPES["SESSION"]))
			view.assign("static_count", self.args.applications.count_type(Applications.TYPES["STATIC"]))
			view.render()
			return content.getvalue() if version_info.major >= 3 else content.getvalue().decode("utf8")

		blocks = [
			{"title": "  * " + _("Some applications using:"), "content": with_helpers_content()},
			{"title": "  * " + _("These applications manually:"), "content": without_helpers_content()},
			{"title": "  * " + _("Uninstalled applications:"), "content": erased_content()},
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
		if view.has_content_and_title():
			self.print(_("You should restart:"))
		view.render()

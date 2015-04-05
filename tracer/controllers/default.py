#-*- coding: utf-8 -*-
# default.py
# Defines DefaultController
#
# Copyright (C) 2013 Jakub Kadlčík
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import os
from tracer.views.default import DefaultView
from tracer.views.interactive import InteractiveView
from tracer.views.note_for_hidden import NoteForHiddenView
from tracer.resources.lang import _
from tracer.resources.tracer import Tracer
from tracer.resources.system import System
from tracer.resources.memory import dump_memory
from tracer.resources.applications import Applications
from tracer.resources.rules import Rules
from tracer.controllers.helper import HelperController


class DefaultController(object):

	args = None
	tracer = None
	processes = None

	def __init__(self, args, packages):
		self.args = args
		self.tracer = Tracer(System.package_manager(), Rules, Applications, memory=dump_memory)
		self.tracer.now = args.now
		self.tracer.timestamp = args.timestamp[0]
		if packages:
			self.tracer.specified_packages = packages

		self.applications = self.tracer.trace_affected(self._user(args.user))

	def render(self):
		view = DefaultView()
		view.assign("applications", self.applications)
		view.assign("args", self.args)
		view.render()

	def render_helpers(self):
		helper_controller = HelperController(self.args)
		for application in self._restartable_applications(self.applications, self.args):
			helper_controller.print_helper(application.name, self.args)
			print("")

		view = NoteForHiddenView()
		view.assign("args", self.args)
		view.assign("total_count", len(self.applications))
		view.assign("session_count", self.applications.count_type(Applications.TYPES['SESSION']))
		view.assign("static_count", self.applications.count_type(Applications.TYPES['STATIC']))
		view.render()

	def render_interactive(self):
		helper_controller = HelperController(self.args)
		filtered = self._restartable_applications(self.applications, self.args).sorted("name")

		while True:
			view = InteractiveView()
			view.assign("applications", filtered)
			view.assign("args", self.args)
			view.assign("total_count", len(self.applications))
			view.assign("session_count", self.applications.count_type(Applications.TYPES['SESSION']))
			view.assign("static_count", self.applications.count_type(Applications.TYPES['STATIC']))
			view.render()

			# If there are only hidden applications (any listed)
			if view.get("total_count") == view.get("session_count") + view.get("static_count"):
				break

			print("\n" + _("Press application number for help or 'q' to quit"))
			answer = raw_input("--> ")
			try:
				if answer == "q": return
				elif int(answer) <= 0 or int(answer) > len(filtered): raise IndexError
				helper_controller.print_helper(filtered[int(answer) - 1].name, self.args)

			except (SyntaxError, IndexError, ValueError):
				print(_("Wrong application number"))

			raw_input("\n-- " + _("Press <enter> to get list of applications") + " --")

	def _restartable_applications(self, applications, args):
		return applications.exclude_types([
			Applications.TYPES['STATIC'],
			Applications.TYPES['SESSION']
		]) if not args.all else applications

	def _user(self, user):
		if   user == '*':    return None
		elif not user:       return os.getlogin()
		else: return user[0]

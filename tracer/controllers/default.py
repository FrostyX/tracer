#-*- coding: utf-8 -*-
# default.py
# Defines DefaultController
#
# Copyright (C) 2016 Jakub Kadlcik
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
import sys
from tracer.hooks import HooksObserver
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


# compatibility with Py2 and Py3 - rename raw_input() to input() on Py2
try:
	input = raw_input
except NameError:
	pass


class DefaultController(object):

	args = None
	tracer = None
	processes = None

	def __init__(self, args, packages):
		self.args = args
		self.tracer = Tracer(
			System.package_manager(erased=args.erased),
			Rules,
			Applications,
			memory=dump_memory,
			hooks_observer=HooksObserver(),
			erased=args.erased
		)
		self.tracer.now = args.now
		self.tracer.timestamp = args.timestamp[0]
		if packages:
			self.tracer.specified_packages = packages

		self.applications = self.tracer.trace_affected(self._user(args.user))
		if self.args.daemons_only:
			self.applications = self.applications.filter_types([Applications.TYPES["DAEMON"]])

	def render(self):
		if not self.args.hooks_only:
			view = DefaultView()
			view.assign("applications", self.applications)
			view.assign("args", self.args)
			view.render()
			self.create_reboot_required_file()
		exit(self.status_code())

	def render_helpers(self):
		helper_controller = HelperController(self.args)
		for application in self._restartable_applications(self.applications, self.args):
			helper_controller.print_helper(application, self.args)
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
			answer = input("--> ")
			try:
				if answer == "q": return
				elif int(answer) <= 0 or int(answer) > len(filtered): raise IndexError
				helper_controller.print_helper(filtered[int(answer) - 1], self.args)

			except (SyntaxError, IndexError, ValueError):
				print(_("Wrong application number"))

			sys.stdout.write("\n-- " + _("Press <enter> to get list of applications") + " --")
			input()

	def status_code(self):
		"""
		0   - No affected applications
		101 - Found some affected applications
		102 - Found some affected daemons
		103 - Session restart needed
		104 - Reboot needed
		"""
		code = 0
		if len(self.applications) > 0:
			code = 101

		if self.applications.count_type(Applications.TYPES['DAEMON']):
			code = 102

		if self.applications.count_type(Applications.TYPES['SESSION']):
			code = 103

		if self.applications.count_type(Applications.TYPES['STATIC']):
			code = 104
		return code

	def create_reboot_required_file(self):
		"""
		If a reboot is needed, create a /run/reboot-required file.
		This is how Debian/Ubuntu distros does it.
		"""
		if self.applications.count_type(Applications.TYPES["STATIC"]):
			with open("/run/reboot-required", "w") as fp:
				fp.write("Tracer says reboot is required\n")

	def _restartable_applications(self, applications, args):
		return applications.exclude_types([
			Applications.TYPES['STATIC'],
			Applications.TYPES['SESSION']
		]) if not args.all else applications

	def _user(self, user):
		if   user == ['*'] or user == '*':    return None
		elif user == 'root': return user
		elif not user:       return System.user()
		else: return user[0]

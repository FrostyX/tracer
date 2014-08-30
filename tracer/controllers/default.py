#!/usr/bin/python
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
from tracer.resources.applications import Applications
from tracer.resources.ProcessesList import ProcessesList
from tracer.controllers.helper import HelperController


class DefaultController(object):

	args = None
	tracer = None
	processes = None

	def __init__(self, args, packages):
		self.args = args
		self.tracer = Tracer()
		self.tracer.specified_packages = packages
		self.tracer.now = args.now
		self.processes = ProcessesList(self.tracer.trace_running(self._user(args.user)))

	def render(self):
		self._print_all(self.processes, self.args)

	def render_helpers(self):
		helper_controller = HelperController(self.args)
		for process in self._processes(self.processes, self.args):
			helper_controller.print_helper(process.name, self.args)
			print ""

		view = NoteForHiddenView()
		view.assign("args", self.args)
		view.assign("total_count", len(self.processes))
		view.assign("session_count", self.processes.count_type(Applications.TYPES['SESSION']))
		view.assign("static_count", self.processes.count_type(Applications.TYPES['STATIC']))
		view.render()

	def render_interactive(self):
		helper_controller = HelperController(self.args)
		filtered = self._processes(self.processes, self.args)

		while True:
			view = InteractiveView()
			view.assign("processes", filtered)
			view.assign("args", self.args)
			view.assign("total_count", len(self.processes))
			view.assign("session_count", self.processes.count_type(Applications.TYPES['SESSION']))
			view.assign("static_count", self.processes.count_type(Applications.TYPES['STATIC']))
			view.render()

			answer = raw_input("--> ")
			try:
				if answer == "q": return
				elif int(answer) <= 0 or int(answer) > len(filtered): raise IndexError
				helper_controller.print_helper(filtered[int(answer) - 1].name, self.args)

			except (SyntaxError, IndexError, ValueError):
				print _("wrong_app_number")

			raw_input("\n" + _("press_enter"))

	def _print_all(self, processes, args):
		filtered = self._processes(processes, args)

		view = DefaultView()
		view.assign("processes", filtered)
		view.assign("args", args)
		view.assign("total_count", len(processes))
		view.assign("session_count", processes.count_type(Applications.TYPES['SESSION']))
		view.assign("static_count", processes.count_type(Applications.TYPES['STATIC']))
		view.render()

	def _processes(self, processes, args):
		return processes.exclude_types([
			Applications.TYPES['STATIC'],
			Applications.TYPES['SESSION']
		]) if not args.all else processes

	def _user(self, user):
		if   user == '*':    return None
		elif not user:       return os.getlogin()
		else: return user[0]

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

import tracer.templates.default
from tracer.resources.lang import _
from tracer.resources.applications import Applications
from tracer.controllers.helper import HelperController


class DefaultController(object):

	def render(self, processes, args):
		self._print_all(processes, args)

	def render_helpers(self, processes, args):
		helper_controller = HelperController()
		for process in self._processes(processes, args):
			helper_controller.print_helper(process.name, args)
			print ""

		tracer.templates.note_for_hidden.render(
			args = args,
			total_count = len(processes),
			session_count = processes.count_type(Applications.TYPES['SESSION']),
			static_count = processes.count_type(Applications.TYPES['STATIC'])
		)

	def render_interactive(self, processes, args):
		helper_controller = HelperController()
		filtered = self._processes(processes, args)

		while True:
			tracer.templates.interactive.render(
				processes = filtered,
				args = args,
				total_count = len(processes),
				session_count = processes.count_type(Applications.TYPES['SESSION']),
				static_count = processes.count_type(Applications.TYPES['STATIC'])
			)

			answer = raw_input("--> ")
			try:
				if answer == "q": return
				elif int(answer) <= 0 or int(answer) > len(filtered): raise IndexError
				helper_controller.print_helper(filtered[int(answer) - 1].name, args)

			except (SyntaxError, IndexError, ValueError):
				print _("wrong_app_number")

			raw_input("\n" + _("press_enter"))

	def _print_all(self, processes, args):
		filtered = self._processes(processes, args)

		tracer.templates.default.render(
			processes = filtered,
			args = args,
			total_count = len(processes),
			session_count = processes.count_type(Applications.TYPES['SESSION']),
			static_count = processes.count_type(Applications.TYPES['STATIC'])
		)

	def _processes(self, processes, args):
		return processes.exclude_types([
			Applications.TYPES['STATIC'],
			Applications.TYPES['SESSION']
		]) if not args.all else processes
